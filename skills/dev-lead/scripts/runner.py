"""Bounded visible Codex runs. Mechanics only: never choose or replay an action."""
import argparse
import contextlib
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import threading
import uuid

from inventory import validate_model, skill_hashes
from journal import append_event, atomic_json, fsync_directory, lock, read_events, recover_state
from mechanics import capture, contained, git_snapshot, load, sha256
from outcome import validate


def event(task, identity, kind, data):
    return append_event(Path(task) / 'decision.log', identity, kind, data)


_owners = threading.local()


@contextlib.contextmanager
def controller(task):
    """Hold task ownership across API calls; nested calls in the same thread reuse it."""
    task = Path(task).resolve()
    owned = getattr(_owners, 'tasks', set())
    if task in owned:
        yield
        return
    with lock(task / 'research' / 'dev-lead' / 'controller.lock'):
        _owners.tasks = owned
        owned.add(task)
        try:
            yield
        finally:
            owned.remove(task)


def _identity(value):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}', value):
        raise ValueError('run ID must be a safe single path component')
    return value


def _intent(run, kind):
    spec = load(run / 'spec.json')
    matches = [row for row in read_events(Path(spec['task']) / 'decision.log')
               if row['event_id'] == spec['run_id'] + ':' + kind]
    if len(matches) != 1:
        raise ValueError('missing durable ' + kind + ' intent')
    if kind == 'prepared' and matches[0]['data']['spec_sha256'] != sha256(run / 'spec.json'):
        raise ValueError('run specification changed')
    return matches[0]


def prepare(task, run_id, step_id, cwd, inventory, model, effort, sandbox,
            prompt, artifact_root, timeout=600, schema=None, codex='codex',
            skill_paths=(), resume_from=None):
    """Reserve one ID and persist immutable launch inputs. Does not launch anything."""
    task, cwd = Path(task).resolve(), Path(cwd).resolve(strict=True)
    artifact_root = Path(artifact_root).resolve(strict=True)
    if not artifact_root.is_dir() or not step_id or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('existing artifact root, step_id and positive timeout required')
    validate_model(inventory, model, effort)
    if sandbox not in ('read-only', 'workspace-write'):
        raise ValueError('supported sandbox: read-only or workspace-write')
    skill_row = inventory['skills'].get(str(cwd), {})
    if skill_row.get('status') != 'ok':
        raise ValueError('skill discovery failed for cwd')
    selected = []
    for path in skill_paths:
        matches = [s for s in skill_row['skills'] if s['path'] == str(path) and s['enabled']]
        if (len(matches) != 1 or sha256(path) != matches[0]['sha256']
                or skill_hashes(path) != matches[0]['files']):
            raise ValueError('selected exact skill path is missing, disabled or changed')
        selected.append({'path': str(path), 'sha256': matches[0]['sha256'], 'files': skill_hashes(path)})
    run_id = _identity(run_id)
    schema = Path(schema) if schema else Path(__file__).resolve().parent.parent / 'assets/outcome.schema.json'
    schema_value = load(schema)
    session = None
    with controller(task):
        if resume_from is not None:
            previous = Path(resume_from).resolve(strict=True)
            prior = load(previous / 'spec.json')
            if (prior['task'] != str(task) or prior['cwd'] != str(cwd)
                    or prior['step_id'] != step_id or prior['artifact_root'] != str(artifact_root)):
                raise ValueError('resume must preserve task, cwd, step and artifact root')
            state = _reconcile(previous)
            if state['status'] not in ('needs_input', 'interrupted', 'blocked') or 'session_id' not in state:
                raise ValueError('resume requires saved needs_input or acknowledged stopped session')
            if any(row['event_id'] == prior['run_id'] + ':continuation'
                   for row in read_events(task / 'decision.log')):
                raise ValueError('question already has a continuation intent; reconcile it')
            if state['status'] == 'blocked':
                resolutions = [r for r in read_events(task / 'decision.log')
                               if r['event_id'] == prior['run_id'] + ':resolution']
                if len(resolutions) != 1 or not resolutions[0]['data'].get('evidence'):
                    raise ValueError('blocked continuation requires recorded resolution evidence')
            session = state['session_id']
            uuid.UUID(session)
        run = task / 'research' / 'dev-lead' / 'runs' / run_id
        run.parent.mkdir(parents=True, exist_ok=True)
        run.mkdir()  # No reuse, even if a previous reservation crashed before journaling.
        fsync_directory(run.parent)
        atomic_json(run / 'schema.json', schema_value)
        instructions = '\n'.join('Read exact skill: ' + s['path'] + ' (sha256 ' + s['sha256'] + ').'
                                 for s in selected)
        atomic_json(run / 'input.json', {'prompt': instructions + '\n' + prompt})
        codex = shutil.which(codex) or codex
        command = [codex, 'exec', '--ignore-user-config', '-C', str(cwd), '-m', model,
                   '-c', 'model_reasoning_effort=' + json.dumps(effort),
                   '-c', 'approval_policy="never"', '-s', sandbox, '--json',
                   '--output-schema', str(run / 'schema.json'), '-o', str(run / 'result.json')]
        command += ['resume', session, '-'] if session else ['-']
        spec = {'task': str(task), 'run_id': run_id, 'step_id': step_id, 'cwd': str(cwd),
                'artifact_root': str(artifact_root), 'command': command, 'timeout': timeout,
                'resume_session': session, 'resume_from': str(previous) if resume_from else None,
                'skills': selected, 'schema_sha256': sha256(run / 'schema.json'),
                'input_sha256': sha256(run / 'input.json'), 'before': git_snapshot(cwd)}
        atomic_json(run / 'spec.json', spec)
        event(task, run_id + ':prepared', 'run.prepared',
              {'run': str(run), 'spec_sha256': sha256(run / 'spec.json')})
        if resume_from is not None:
            event(task, prior['run_id'] + ':continuation', 'resume.intent',
                  {'run': str(run), 'session_id': session})
    return run


def launch(run, agtermctl='agtermctl', timeout=15):
    """Record intent before agterm IPC. Any response loss requires reconciliation."""
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('timeout must be finite and positive')
    run = Path(run).resolve(strict=True)
    spec = load(run / 'spec.json')
    with controller(spec['task']):
        _intent(run, 'prepared')
        rows = read_events(Path(spec['task']) / 'decision.log')
        for row in rows:
            if row['kind'] == 'launch.intent' and row['event_id'] != spec['run_id'] + ':launch':
                previous = Path(spec['task']) / 'research' / 'dev-lead' / 'runs' / row['event_id'].removesuffix(':launch')
                if (not (previous / 'execution/exit.json').exists()
                        and _reconcile(previous)['status'] != 'interrupted'):
                    raise ValueError('previous launch has no durable exit; reconcile before another launch')
        if any(row['event_id'] == spec['run_id'] + ':launch' for row in read_events(Path(spec['task']) / 'decision.log')):
            raise ValueError('launch already attempted; reconcile without replay')
        wrapper = [sys.executable, str(Path(__file__).resolve()), 'worker', '--run', str(run)]
        command = [agtermctl, 'session', 'new', '--cwd', spec['cwd'], '--name', spec['run_id'],
                   '--command', shlex.join(wrapper), '--wait', '--no-select', '--json']
        event(spec['task'], spec['run_id'] + ':launch', 'launch.intent', {'command': command})
        try:
            response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      timeout=timeout, check=False)
            value = {'exit_code': response.returncode, 'stdout': response.stdout.decode(errors='replace'),
                     'stderr': response.stderr.decode(errors='replace'), 'uncertain': response.returncode != 0}
        except (OSError, subprocess.TimeoutExpired) as error:
            value = {'uncertain': True, 'error': str(error)}
        if value.get('exit_code') == 0:
            try:
                reply = json.loads(value['stdout'])
                if reply.get('ok') is not True:
                    raise ValueError('agterm returned a failed reply')
                value['agterm_session_id'] = reply['result']['id']
            except (ValueError, KeyError, TypeError) as error:
                value['uncertain'] = True
                value['error'] = 'invalid agterm launch reply: ' + str(error)
        atomic_json(run / 'launch.json', value)
        return value


def worker(run, terminal=True):
    """Internal visible-session entry point. A durable claim prevents duplicate exec."""
    run = Path(run).resolve(strict=True)
    spec = load(run / 'spec.json')
    with lock(run / 'run.lock'), lock(Path(spec['task']) / 'worker.lock'):
        _intent(run, 'prepared')
        _intent(run, 'launch')
        if spec['resume_from']:
            previous = load(Path(spec['resume_from']) / 'spec.json')
            rows = read_events(Path(spec['task']) / 'decision.log')
            claims = [r for r in rows if r['event_id'] == previous['run_id'] + ':continuation']
            if len(claims) != 1 or claims[0]['data']['run'] != str(run):
                raise ValueError('missing exact-session continuation intent')
        # O_EXCL survives interruption between claim and Popen; it is never auto-cleared.
        fd = os.open(run / 'claim', os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, 'w') as stream:
            stream.write(str(os.getpid()) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        fsync_directory(run)
        for key, filename in [('schema_sha256', 'schema.json'), ('input_sha256', 'input.json')]:
            if sha256(run / filename) != spec[key]:
                raise ValueError('launch input changed')
        for skill in spec['skills']:
            if sha256(skill['path']) != skill['sha256'] or skill_hashes(skill['path']) != skill['files']:
                raise ValueError('selected skill changed')
        event(spec['task'], spec['run_id'] + ':started', 'worker.started', {'pid': os.getpid()})
        pending = b''
        sessions = set()

        def on_stdout(chunk):
            nonlocal pending
            pending += chunk
            while b'\n' in pending:
                raw, pending = pending.split(b'\n', 1)
                try:
                    row = json.loads(raw)
                except ValueError:
                    continue  # Raw evidence is retained; reconciliation rejects invalid JSONL.
                if row.get('type') == 'thread.started':
                    session = row['thread_id']
                    uuid.UUID(session)
                    if spec['resume_session'] and session != spec['resume_session']:
                        raise ValueError('resume returned a different session')
                    sessions.add(session)
                    if len(sessions) != 1:
                        raise ValueError('multiple worker sessions')
                    atomic_json(run / 'session.json', {'session_id': session})
        # A file, rather than a PIPE writer, cannot block on a long prompt.
        prompt_path = run / 'prompt.txt'
        with prompt_path.open('w') as stream:
            stream.write(load(run / 'input.json')['prompt'])
        with prompt_path.open('rb') as stream:
            result = capture(spec['command'], spec['cwd'], run / 'execution', spec['timeout'],
                             stdin=stream, terminal=terminal, on_stdout=on_stdout)
        if pending:
            raise ValueError('incomplete worker JSONL')
        event(spec['task'], spec['run_id'] + ':exited', 'worker.exited', result)
        return result


def artifact_evidence(spec, path):
    file = contained(spec['artifact_root'], path)
    journal = (Path(spec['task']) / 'decision.log').resolve()
    cache = journal.parent / 'research' / 'dev-lead' / 'journal-state.json'
    if file in (journal, cache):
        rows = read_events(journal)
        if file == cache and load(cache) != {'last_event_id': rows[-1]['event_id'] if rows else None, 'events': rows}:
            raise ValueError('journal cache does not match authoritative events')
        raw = journal.read_bytes()
        return {'prefix_sha256': hashlib.sha256(raw).hexdigest(), 'size': len(raw)}
    return sha256(file)


def artifact_matches(spec, path, evidence):
    file = contained(spec['artifact_root'], path)
    if isinstance(evidence, dict):
        journal = (Path(spec['task']) / 'decision.log').resolve()
        cache = journal.parent / 'research' / 'dev-lead' / 'journal-state.json'
        if (file not in (journal, cache) or set(evidence) != {'prefix_sha256', 'size'}
                or type(evidence['size']) is not int or evidence['size'] < 0):
            return False
        rows = read_events(journal)
        if file == cache and load(cache) != {'last_event_id': rows[-1]['event_id'] if rows else None, 'events': rows}:
            return False
        raw = journal.read_bytes()
        return len(raw) >= evidence['size'] and hashlib.sha256(raw[:evidence['size']]).hexdigest() == evidence['prefix_sha256']
    return sha256(file) == evidence


def _source(run):
    paths = ['spec.json', 'input.json', 'schema.json', 'result.json', 'session.json',
             'execution/stdout', 'execution/stderr', 'execution/exit.json', 'execution/process.json']
    hashes = {path: sha256(run / path) for path in paths}
    spec = load(run / 'spec.json')
    if hashes['input.json'] != spec['input_sha256'] or hashes['schema.json'] != spec['schema_sha256']:
        raise ValueError('frozen launch input changed')
    for skill in spec['skills']:
        digest = sha256(skill['path'])
        if digest != skill['sha256'] or skill_hashes(skill['path']) != skill['files']:
            raise ValueError('selected skill changed')
        hashes['skill:' + skill['path']] = digest
    return hashes


def _pid_present(pid):
    # PID reuse is deliberately conservative: a present PID never proves it is safe.
    if type(pid) is not int or pid <= 0:
        raise ValueError('invalid recorded PID')
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _interruption_source(run):
    names = ['spec.json', 'input.json', 'schema.json', 'claim', 'launch.json',
             'session.json', 'result.json', 'execution/stdout', 'execution/stderr',
             'execution/process.json', 'execution/exit.json']
    return {name: sha256(run / name) if (run / name).exists() else None for name in names}


def _group_present(pid):
    try:
        os.killpg(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _processes_stopped(run):
    if not (run / 'claim').exists() or not (run / 'execution/process.json').exists():
        return False  # An unobserved launch may still arrive late.
    process = load(run / 'execution/process.json')
    return (not _pid_present(int((run / 'claim').read_text()))
            and not _pid_present(process['owner_pid']) and not _pid_present(process['pid'])
            and not _group_present(process['pid']))


def acknowledge_stopped(run, reason):
    """Pin inspected interruption evidence; allow a new action, never replay this run.

    The lead supplies its reason after inspecting files/processes. Absence of both
    recorded processes and an available run lock is required, not inferred exit 0.
    """
    run = Path(run).resolve(strict=True)
    spec = load(run / 'spec.json')
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError('reconciliation reason required')
    with controller(spec['task']), lock(run / 'run.lock'):
        _intent(run, 'prepared')
        _intent(run, 'launch')
        if (run / 'execution/exit.json').exists() or not _processes_stopped(run):
            raise ValueError('recovery requires a claimed run with confirmed absent recorded processes and no exit')
        if (run / 'recovery.json').exists():
            raise ValueError('recovery already recorded; reconcile it')
        report = {'reason': reason, 'git': git_snapshot(spec['cwd']), 'source': _interruption_source(run)}
        atomic_json(run / 'recovery.json', report)
        event(spec['task'], spec['run_id'] + ':recovered', 'run.interruption_reconciled',
              {'sha256': sha256(run / 'recovery.json')})
        return report


def _reconcile(run):
    spec = load(run / 'spec.json')
    _intent(run, 'prepared')
    recover_state(Path(spec['task']) / 'decision.log')
    snapshot = git_snapshot(spec['cwd'])
    observed = {}
    for name in ('launch.json', 'execution/process.json', 'execution/exit.json', 'session.json'):
        if (run / name).exists():
            observed[name] = load(run / name)
    base = {'run_id': spec['run_id'], 'git': snapshot,
            'changed_since_intent': snapshot != spec['before'], 'replay_safe': False, 'records': observed,
            'journal_events': [r['event_id'] for r in read_events(Path(spec['task']) / 'decision.log')
                               if r['event_id'].startswith(spec['run_id'] + ':')]}
    if 'execution/process.json' in observed:
        base['process_pid_present'] = _pid_present(observed['execution/process.json']['pid'])
    try:
        with lock(run / 'run.lock'):
            pass
    except BlockingIOError:
        return {**base, 'status': 'live', 'reason': 'run lock is owned'}
    if not (run / 'execution/exit.json').exists():
        if (run / 'recovery.json').exists():
            report = load(run / 'recovery.json')
            rows = read_events(Path(spec['task']) / 'decision.log')
            records = [r for r in rows if r['event_id'] == spec['run_id'] + ':recovered']
            if (len(records) == 1 and records[0]['data']['sha256'] == sha256(run / 'recovery.json')
                    and report['git'] == snapshot and report['source'] == _interruption_source(run)
                    and _processes_stopped(run)):
                if (run / 'session.json').exists():
                    session = load(run / 'session.json')['session_id']
                    uuid.UUID(session)
                    base['session_id'] = session
                return {**base, 'status': 'interrupted', 'reason': report['reason']}
        return {**base, 'status': 'uncertain', 'reason': 'no durable exit; inspect process, files and events'}
    exit_record = load(run / 'execution/exit.json')
    if exit_record['exit_code'] != 0 or exit_record['timed_out']:
        return {**base, 'status': 'blocked', 'reason': 'worker failed or timed out', 'exit': exit_record}
    try:
        _intent(run, 'launch')
        session = load(run / 'session.json')['session_id']
        uuid.UUID(session)
        raw_events = (run / 'execution/stdout').read_bytes()
        if not raw_events.endswith(b'\n'):
            raise ValueError('incomplete worker event stream')
        events = [json.loads(line) for line in raw_events.splitlines()]
        if not all(isinstance(e, dict) for e in events):
            raise ValueError('malformed worker event')
        if not any(e.get('type') == 'turn.completed' for e in events):
            raise ValueError('missing turn.completed event')
        if exit_record['command'] != spec['command'] or exit_record['cwd'] != spec['cwd']:
            raise ValueError('exit record launch mismatch')
        ids = {e['thread_id'] for e in events if e.get('type') == 'thread.started'}
        if ids != {session} or (spec['resume_session'] and session != spec['resume_session']):
            raise ValueError('session evidence mismatch')
        value = validate(load(run / 'result.json'), spec['step_id'], spec['artifact_root'])
        hashes = _source(run)
    except (ValueError, KeyError, TypeError, OSError) as error:
        return {**base, 'status': 'invalid', 'reason': str(error)}
    base.update({'outcome': value, 'session_id': session})
    if value['status'] != 'done':
        return {**base, 'status': value['status']}
    if not (run / 'verification.json').exists():
        return {**base, 'status': 'unverified', 'reason': 'independent verification required'}
    try:
        report = load(run / 'verification.json')
        recorded = [row for row in read_events(Path(spec['task']) / 'decision.log')
                    if row['event_id'] == spec['run_id'] + ':verified:' + report['attempt_id']]
        if len(recorded) != 1 or recorded[0]['data']['sha256'] != sha256(run / 'verification.json'):
            raise ValueError('missing independent verification event')
        if hashes != report['source'] or snapshot != report['git']:
            raise ValueError('worker evidence or Git snapshot changed')
        for path, digest in report['artifacts'].items():
            if not artifact_matches(spec, path, digest):
                raise ValueError('artifact changed')
        for name, digest in report['checks'].items():
            if sha256(run / name) != digest:
                raise ValueError('verification output changed')
    except (OSError, ValueError, KeyError, TypeError) as error:
        return {**base, 'status': 'stale', 'reason': str(error)}
    return {**base, 'status': 'done', 'verification': report}


def reconcile(run):
    """Observe state only; never relaunch, resume or commit."""
    run = Path(run).resolve(strict=True)
    with controller(load(run / 'spec.json')['task']):
        return _reconcile(run)


def verify(run, commands, verifier, timeout=120, attempt_id="first"):
    """Execute independent checks after worker exit and pin all evidence to Git/files."""
    run = Path(run).resolve(strict=True)
    spec = load(run / 'spec.json')
    if (not isinstance(verifier, str) or not verifier.strip() or not isinstance(commands, list)
            or not commands or any(not isinstance(c, list) or not c
                                   or not all(isinstance(s, str) and s for s in c) for c in commands)):
        raise ValueError('independent verifier and explicit command argv lists required')
    with controller(spec['task']), lock(run / 'verification.lock'):
        state = _reconcile(run)
        if state['status'] not in ('unverified', 'stale'):
            raise ValueError('verify requires an exited unverified or stale done outcome')
        attempt_id = _identity(attempt_id)
        before = git_snapshot(spec['cwd'])
        source = _source(run)
        artifacts = {p: artifact_evidence(spec, p) for p in state['outcome']['artifacts']}
        directory = run / 'checks' / attempt_id
        directory.parent.mkdir(exist_ok=True)
        directory.mkdir()  # Never overwrite a possibly partially executed verification.
        checks = {}
        for number, command in enumerate(commands):
            target = directory / str(number)
            value = capture(command, spec['cwd'], target, timeout)
            if value['exit_code'] != 0 or value['timed_out']:
                raise ValueError('independent check failed; actual output retained')
            for file in ('stdout', 'stderr', 'exit.json'):
                name = str((target / file).relative_to(run))
                checks[name] = sha256(run / name)
        if (git_snapshot(spec['cwd']) != before or _source(run) != source
                or any(not artifact_matches(spec, p, h) for p, h in artifacts.items())):
            raise ValueError('evidence changed during independent checks')
        report = {'attempt_id': attempt_id, 'verifier': verifier, 'source': source, 'artifacts': artifacts,
                  'checks': checks, 'git': before}
        atomic_json(directory / 'verification.json', report)
        atomic_json(run / 'verification.json', report)
        event(spec['task'], spec['run_id'] + ':verified:' + attempt_id, 'run.verified',
              {'sha256': sha256(run / 'verification.json'), 'verifier': verifier})
        return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    prep = sub.add_parser('prepare', help='Reserve run ID; persist inputs and intent without launch')
    for name in ('task', 'cwd', 'inventory', 'prompt', 'artifact-root'):
        prep.add_argument('--' + name, type=Path, required=True)
    for name in ('run-id', 'step', 'model', 'effort', 'sandbox'):
        prep.add_argument('--' + name, required=True)
    prep.add_argument('--timeout', type=float, default=600)
    prep.add_argument('--codex', default='codex')
    prep.add_argument('--schema', type=Path)
    prep.add_argument('--skill-path', action='append', default=[])
    prep.add_argument('--resume-from', type=Path, help='Exited needs_input run; uses its exact saved UUID')
    for action, description in [('launch', 'Send one intent-protected agterm launch'),
                                ('worker', 'Internal agterm entry; claim ID and stream bounded exec'),
                                ('reconcile', 'Observe process/run/events/result/Git; never replay'),
                                ('verify', 'Run separate independent acceptance commands'),
                                ('acknowledge-stopped', 'Pin inspected files after confirmed process death; never replay')]:
        command = sub.add_parser(action, help=description)
        command.add_argument('--run', type=Path, required=True)
        if action == 'launch':
            command.add_argument('--agtermctl', default='agtermctl')
            command.add_argument('--timeout', type=float, default=15)
        if action == 'acknowledge-stopped':
            command.add_argument('--reason', required=True)
        if action == 'verify':
            command.add_argument('--commands', type=Path, required=True, help='JSON array of command argv arrays')
            command.add_argument('--attempt-id', default='first', help='Unique explicit verification attempt; preserve previous evidence')
            command.add_argument('--verifier', required=True, help='Independent acceptance-check identity')
            command.add_argument('--timeout', type=float, default=120)
    args = parser.parse_args()
    if args.action == 'prepare':
        value = str(prepare(args.task, args.run_id, args.step, args.cwd, load(args.inventory), args.model,
                            args.effort, args.sandbox, args.prompt.read_text(), args.artifact_root,
                            args.timeout, args.schema, args.codex, args.skill_path, args.resume_from))
    elif args.action == 'launch':
        value = launch(args.run, args.agtermctl, args.timeout)
    elif args.action == 'worker':
        value = worker(args.run)
    elif args.action == 'acknowledge-stopped':
        value = acknowledge_stopped(args.run, args.reason)
    elif args.action == 'verify':
        value = verify(args.run, load(args.commands), args.verifier, args.timeout, args.attempt_id)
    else:
        value = reconcile(args.run)
    print(json.dumps(value))
    return (value['exit_code'] if value['exit_code'] is not None else 1) if args.action == 'worker' else 0


if __name__ == '__main__':
    raise SystemExit(main())
