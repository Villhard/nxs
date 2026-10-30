"""Bounded visible native CLI runs. Mechanics only: never choose or replay an action."""
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

import harness as native
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


def _uuid(value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9a-fA-F-]{36}', value):
        raise ValueError('full agterm UUID required')
    return str(uuid.UUID(value))


def _ipc(command, timeout):
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('timeout must be finite and positive')
    try:
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  timeout=timeout, check=False)
        return {'command': command, 'exit_code': response.returncode,
                'stdout': response.stdout.decode(errors='replace'),
                'stderr': response.stderr.decode(errors='replace')}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {'command': command, 'error': str(error)}


def _reply(response):
    if response.get('exit_code') != 0:
        raise ValueError('agterm IPC failed: ' + response.get('stderr', response.get('error', 'unknown error')))
    try:
        reply = json.loads(response['stdout'])
        if not isinstance(reply, dict) or reply.get('ok') is not True or not isinstance(reply.get('result'), dict):
            raise ValueError('failed or malformed agterm reply: ' + str(reply))
        return reply['result']
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError('malformed agterm reply') from error


def _query(identity, arguments, timeout):
    return _reply(_ipc([identity['cli'], *arguments, '--socket', identity['socket'], '--json'], timeout))


def _agterm_tree(identity, timeout=15, require_lead=True):
    """Check an explicit open window; tree itself has no window ID."""
    windows = _query(identity, ['window', 'list'], timeout).get('windows')
    if not isinstance(windows, list):
        raise ValueError('malformed agterm window inventory')
    if any(not isinstance(w, dict) or 'id' not in w for w in windows):
        raise ValueError('malformed agterm window identity')
    matches = [w for w in windows if _uuid(w['id']) == identity['window_id']]
    if len(matches) != 1 or matches[0].get('open') is not True:
        raise ValueError('stale agterm window identity')
    tree = _query(identity, ['tree', '--window', identity['window_id']], timeout).get('tree')
    if not isinstance(tree, dict) or not isinstance(tree.get('workspaces'), list):
        raise ValueError('malformed agterm tree')
    workspaces, sessions = {}, {}
    for workspace in tree['workspaces']:
        if not isinstance(workspace, dict) or 'id' not in workspace:
            raise ValueError('malformed agterm workspace identity')
        wid = _uuid(workspace['id'])
        if wid in workspaces or not isinstance(workspace.get('sessions'), list):
            raise ValueError('contradictory agterm workspace identity')
        workspaces[wid] = workspace
        for session in workspace['sessions']:
            if not isinstance(session, dict) or 'id' not in session:
                raise ValueError('malformed agterm session identity')
            sid = _uuid(session['id'])
            if sid in sessions:
                raise ValueError('contradictory agterm session identity')
            sessions[sid] = (wid, session)
    if identity['workspace_id'] not in workspaces:
        raise ValueError('stale agterm workspace identity')
    if require_lead:
        lead = sessions.get(identity['session_id'])
        if lead is None or lead[0] != identity['workspace_id'] or lead[1].get('realized') is not True:
            raise ValueError('stale or mismatched live agterm lead identity')
    return tree, sessions


def _checked_agterm(identity, timeout):
    if not isinstance(identity, dict) or any(key not in identity for key in ('window_id', 'workspace_id', 'session_id')):
        raise ValueError('recorded agterm identity required')
    value = {key: _uuid(identity[key]) for key in ('window_id', 'workspace_id', 'session_id')}
    socket = identity.get('socket')
    if not isinstance(socket, str) or not Path(socket).is_absolute():
        raise ValueError('absolute agterm socket required')
    if not isinstance(identity.get('cli'), str) or not identity['cli']:
        raise ValueError('recorded agterm CLI required')
    cli = shutil.which(identity['cli'])
    if cli is None:
        raise ValueError('agterm CLI missing')
    value.update(socket=socket, cli=str(Path(cli).resolve()))
    tree, _ = _agterm_tree(value, timeout)
    return value, tree


def preflight(agtermctl='agtermctl', timeout=15):
    """Read-only entry gate. Call before task records, controller or discovery."""
    if os.environ.get('AGTERM_ENABLED') != '1':
        raise ValueError('dev-lead requires agterm; open this repository in agterm and invoke dev-lead again. Standalone dev skills remain available.')
    fields = {'socket': 'AGTERM_SOCKET', 'window_id': 'AGTERM_WINDOW_ID',
              'workspace_id': 'AGTERM_WORKSPACE_ID', 'session_id': 'AGTERM_SESSION_ID'}
    if any(not os.environ.get(env) for env in fields.values()):
        raise ValueError('incomplete agterm environment; a live lead session is required')
    identity = {key: os.environ[env] for key, env in fields.items()}
    identity['cli'] = agtermctl
    return _checked_agterm(identity, timeout)[0]


def _terminal_name(task, step, run_id, occupied):
    def normalize(value):
        return re.sub(r'[^a-z0-9]+', '_', value.lower()).strip('_') or 'x'
    base = 'nxs_' + '_'.join(normalize(v) for v in (task.name, step, run_id))
    if base not in occupied:
        return base
    digest = hashlib.sha256(json.dumps([str(task), step, run_id], ensure_ascii=True).encode()).hexdigest()
    for size in range(8, 65, 8):
        candidate = base + '_' + digest[:size]
        if candidate not in occupied:
            return candidate
    number = 2
    while base + '_' + digest + '_' + str(number) in occupied:
        number += 1
    return base + '_' + digest + '_' + str(number)


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
            skill_paths=(), resume_from=None, harness='codex', executable=None, *,
            agterm_identity=None, agtermctl='agtermctl'):
    """Reserve one ID and persist immutable launch inputs. Does not launch anything."""
    task, cwd = Path(task).resolve(), Path(cwd).resolve(strict=True)
    artifact_root = Path(artifact_root).resolve(strict=True)
    if not artifact_root.is_dir() or not step_id or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('existing artifact root, step_id and positive timeout required')
    if harness not in native.NAMES or inventory.get('harness', 'codex') != harness:
        raise ValueError('inventory and selected harness must match')
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
        selected.append({'path': str(path), 'sha256': matches[0]['sha256'], 'files': skill_hashes(path),
                         'delivery': 'context' if matches[0].get('visibility') == 'context' else 'native'})
    run_id = _identity(run_id)
    schema = Path(schema) if schema else Path(__file__).resolve().parent.parent / 'assets/outcome.schema.json'
    schema_value = load(schema)
    session = None
    if agterm_identity is None:
        agterm_identity = preflight(agtermctl)
    agterm_identity, tree = _checked_agterm(agterm_identity, 15)
    with controller(task):
        if resume_from is not None:
            previous = Path(resume_from).resolve(strict=True)
            prior = load(previous / 'spec.json')
            if prior.get('harness', 'codex') != harness:
                raise ValueError('a native session cannot resume in another harness')
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
            if not _processes_stopped(previous):
                raise ValueError('resume requires confirmed stopped processes for ' + prior['run_id'] + '; reconcile before continuation')
            session = state['session_id']
            native.check_resume(harness, executable or (codex if harness == 'codex' else harness), session, cwd, timeout)
        run = task / 'research' / 'dev-lead' / 'runs' / run_id
        occupied = {s.get('name') for w in tree['workspaces'] for s in w['sessions']}
        for path in run.parent.glob('*/spec.json'):
            occupied.add(load(path).get('terminal_name'))
        terminal_name = _terminal_name(task, step_id, run_id, occupied)
        run.parent.mkdir(parents=True, exist_ok=True)
        run.mkdir()  # No reuse, even if a previous reservation crashed before journaling.
        fsync_directory(run.parent)
        atomic_json(run / 'schema.json', schema_value)
        instructions = []
        for skill in selected:
            source = Path(skill['path'])
            if skill['delivery'] == 'context':
                instructions.append('Explicit candidate skill content from ' + str(source) +
                                    ' (sha256 ' + skill['sha256'] + '). Base directory: ' + str(source.parent) +
                                    '. Resolve bundled resources there; do not substitute a same-name installed skill.\n' + source.read_text())
            else:
                instructions.append('Read exact skill: ' + skill['path'] + ' (sha256 ' + skill['sha256'] + ').')
        instructions = '\n'.join(instructions)
        atomic_json(run / 'input.json', {'prompt': instructions + '\n' + prompt})
        command = native.command(harness, executable or (codex if harness == 'codex' else harness), cwd, model, effort, sandbox, run, session)
        spec = {'task': str(task), 'run_id': run_id, 'step_id': step_id, 'cwd': str(cwd),
                'artifact_root': str(artifact_root), 'harness': harness, 'model': model, 'effort': effort,
                'sandbox': sandbox, 'command': command, 'timeout': timeout,
                'resume_session': session, 'resume_from': str(previous) if resume_from else None,
                'skills': selected, 'schema_sha256': sha256(run / 'schema.json'),
                'input_sha256': sha256(run / 'input.json'), 'before': git_snapshot(cwd)}
        spec.update(agterm_identity=agterm_identity, terminal_name=terminal_name)
        atomic_json(run / 'spec.json', spec)
        event(task, run_id + ':prepared', 'run.prepared',
              {'run': str(run), 'spec_sha256': sha256(run / 'spec.json'),
               'agterm_identity': agterm_identity, 'terminal_name': terminal_name})
        if resume_from is not None:
            event(task, prior['run_id'] + ':continuation', 'resume.intent',
                  {'run': str(run), 'session_id': session})
    return run


def _launch_command(run, spec):
    identity = spec.get('agterm_identity')
    if not identity or not spec.get('terminal_name'):
        raise ValueError('legacy run has no pinned agterm destination; reconcile before preparing a new run')
    wrapper = [str(Path(sys.executable).resolve()), str(Path(__file__).resolve()), 'worker', '--run', str(run)]
    return [identity['cli'], 'session', 'new', '--socket', identity['socket'],
            '--window', identity['window_id'], '--workspace', identity['workspace_id'],
            '--cwd', spec['cwd'], '--name', spec['terminal_name'],
            '--command', shlex.join(wrapper), '--wait', '--no-select', '--json']


def launch(run, agtermctl=None, timeout=15):
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
                if not _processes_stopped(previous):
                    raise ValueError('previous launch requires confirmed stopped processes for ' + previous.name + '; reconcile before another launch')
        if any(row['event_id'] == spec['run_id'] + ':launch' for row in read_events(Path(spec['task']) / 'decision.log')):
            raise ValueError('launch already attempted; reconcile without replay')
        command = _launch_command(run, spec)
        if agtermctl is not None and str(Path(shutil.which(agtermctl) or agtermctl).resolve()) != command[0]:
            raise ValueError('agterm CLI differs from pinned identity')
        tree, _ = _agterm_tree(spec['agterm_identity'], timeout)
        if any(s.get('name') == spec['terminal_name'] for w in tree['workspaces'] for s in w['sessions']):
            raise ValueError('reserved terminal name is now occupied; reconcile before preparing a new run')
        event(spec['task'], spec['run_id'] + ':launch', 'launch.intent', {'command': command})
        value = _ipc(command, timeout)
        value['uncertain'] = True
        try:
            sid = _uuid(_reply(value)['id'])
            value['agterm_session_id'] = sid
            if (run / 'terminal.json').exists() and load(run / 'terminal.json')['session_id'] != sid:
                raise ValueError('worker and launch terminal IDs differ')
            _, sessions = _agterm_tree(spec['agterm_identity'], timeout)
            found = sessions.get(sid)
            if (found is None or found[0] != spec['agterm_identity']['workspace_id']
                    or found[1].get('realized') is not True
                    or not (found[1].get('foreground') or (run / 'execution/exit.json').exists())):
                raise ValueError('worker terminal not yet confirmed realized and running in pinned destination')
            value['uncertain'] = False
        except (ValueError, KeyError, TypeError) as error:
            value['error'] = str(error)
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
        if 'agterm_identity' in spec:
            identity = spec['agterm_identity']
            observed = {key: _uuid(os.environ.get(env)) for key, env in
                        [('window_id', 'AGTERM_WINDOW_ID'), ('workspace_id', 'AGTERM_WORKSPACE_ID'),
                         ('session_id', 'AGTERM_SESSION_ID'), ('pane_id', 'AGTERM_PANE_ID')]}
            if (os.environ.get('AGTERM_ENABLED') != '1' or os.environ.get('AGTERM_SOCKET') != identity['socket']
                    or observed['window_id'] != identity['window_id']
                    or observed['workspace_id'] != identity['workspace_id']
                    or observed['session_id'] == identity['session_id']):
                raise ValueError('worker agterm identity differs from pinned destination')
            atomic_json(run / 'terminal.json', {'task': spec['task'], 'run_id': spec['run_id'], **observed})
            event(spec['task'], spec['run_id'] + ':terminal', 'terminal.observed',
                  {'sha256': sha256(run / 'terminal.json')})
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
                session = native.observed_session(spec.get('harness', 'codex'), row)
                if session:
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
            if spec.get('harness', 'codex') == 'opencode':
                stream.write('\nReturn only a JSON object matching this schema, without Markdown fences or commentary:\n' + (run / 'schema.json').read_text())
        with prompt_path.open('rb') as stream:
            result = capture(spec['command'], spec['cwd'], run / 'execution', spec['timeout'],
                             stdin=stream, terminal=terminal, on_stdout=on_stdout)
        if pending:
            raise ValueError('incomplete worker JSONL')
        if result['exit_code'] == 0 and not result['timed_out']:
            native.save_outcome(spec.get('harness', 'codex'), run)
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
    if 'agterm_identity' in spec:
        hashes['terminal.json'] = sha256(run / 'terminal.json')
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
    if 'agterm_identity' in load(run / 'spec.json'):
        names.append('terminal.json')
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
                    native.session_id(spec.get('harness', 'codex'), session)
                    base['session_id'] = session
                return {**base, 'status': 'interrupted', 'reason': report['reason']}
        return {**base, 'status': 'uncertain', 'reason': 'no durable exit; inspect process, files and events'}
    exit_record = load(run / 'execution/exit.json')
    if exit_record['exit_code'] != 0 or exit_record['timed_out']:
        return {**base, 'status': 'blocked', 'reason': 'worker failed or timed out', 'exit': exit_record}
    try:
        _intent(run, 'launch')
        session = load(run / 'session.json')['session_id']
        native.session_id(spec.get('harness', 'codex'), session)
        raw_events = (run / 'execution/stdout').read_bytes()
        if not raw_events.endswith(b'\n'):
            raise ValueError('incomplete worker event stream')
        events = [json.loads(line) for line in raw_events.splitlines()]
        if not all(isinstance(e, dict) for e in events):
            raise ValueError('malformed worker event')
        if not native.completed(spec.get('harness', 'codex'), events):
            raise ValueError('missing successful native completion event')
        if exit_record['command'] != spec['command'] or exit_record['cwd'] != spec['cwd']:
            raise ValueError('exit record launch mismatch')
        ids = {native_id for e in events if (native_id := native.observed_session(spec.get('harness', 'codex'), e))}
        if ids != {session} or (spec['resume_session'] and session != spec['resume_session']):
            raise ValueError('session evidence mismatch')
        result = load(run / 'result.json')
        if spec.get('harness', 'codex') != 'codex' and native.extract_outcome(spec['harness'], events) != result:
            raise ValueError('result differs from native final output')
        value = validate(result, spec['step_id'], spec['artifact_root'])
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
    spec = load(run / 'spec.json')
    with controller(spec['task']):
        value = _reconcile(run)
        if any(r['event_id'] == spec['run_id'] + ':cleanup' for r in read_events(Path(spec['task']) / 'decision.log')):
            with lock(run / 'cleanup.lock'):
                value['cleanup'] = _cleanup_state(run, spec, 15)
        return value


def _owned_terminal(run, spec):
    """Bind ownership to the run claim and worker observation, never the label alone."""
    expected = Path(spec['task']) / 'research' / 'dev-lead' / 'runs' / spec['run_id']
    if run != expected.resolve() or 'agterm_identity' not in spec:
        raise ValueError('no owned terminal evidence for this task/run')
    if _intent(run, 'launch')['data']['command'] != _launch_command(run, spec):
        raise ValueError('terminal launch command changed')
    terminal = load(run / 'terminal.json')
    row = _intent(run, 'terminal')
    if row['data']['sha256'] != sha256(run / 'terminal.json'):
        raise ValueError('terminal ownership evidence changed')
    identity = spec['agterm_identity']
    sid = _uuid(terminal['session_id'])
    if (terminal['task'] != spec['task'] or terminal['run_id'] != spec['run_id']
            or terminal['window_id'] != identity['window_id']
            or terminal['workspace_id'] != identity['workspace_id'] or sid == identity['session_id']):
        raise ValueError('terminal ownership identity mismatch')
    launch_record = load(run / 'launch.json') if (run / 'launch.json').exists() else {}
    if 'agterm_session_id' in launch_record and launch_record['agterm_session_id'] != sid:
        raise ValueError('worker and launch terminal IDs differ')
    return sid


def _cleanup_state(run, spec, timeout):
    """Observe one close intent. Reconciliation never sends another close."""
    try:
        intent = _intent(run, 'cleanup')['data']
        sid = _owned_terminal(run, spec)
        if (intent['terminal_id'] != sid or intent['terminal_sha256'] != sha256(run / 'terminal.json')
                or intent['command'] != _close_command(spec, sid)):
            raise ValueError('cleanup ownership evidence changed')
        tree, sessions = _agterm_tree(spec['agterm_identity'], timeout, require_lead=False)
        closed = sid not in sessions
        rows = read_events(Path(spec['task']) / 'decision.log')
        was_closed = any(r['event_id'] == spec['run_id'] + ':cleanup-observed' for r in rows)
        value = {'status': 'closed' if closed else ('reappeared' if was_closed else 'uncertain'),
                 'terminal_id': sid, 'tree': tree, 'replay_safe': False}
        if closed:
            event(spec['task'], spec['run_id'] + ':cleanup-observed', 'cleanup.observed',
                  {'terminal_id': sid, 'summary': 'Exact owned terminal absent from reachable pinned window tree'})
    except (ValueError, KeyError, TypeError, OSError) as error:
        value = {'status': 'uncertain', 'reason': str(error), 'replay_safe': False}
    atomic_json(run / 'cleanup.json', value)
    return value


def _close_command(spec, sid):
    identity = spec['agterm_identity']
    return [identity['cli'], 'session', 'close', '--socket', identity['socket'],
            '--window', identity['window_id'], '--target', sid, '--json']


def _close_reply(response, sid):
    result = _reply(response)
    if set(result) == {'id'}:
        if _uuid(result['id']) == sid:
            return
    elif set(result) == {'affected'}:
        if type(result['affected']) is int and result['affected'] == 1:
            return
    raise ValueError('close reply must identify the exact terminal or exactly one affected session')


def _cleanup_acceptance(run, accepted_continuation):
    state = _reconcile(run)
    if state['status'] == 'done' and accepted_continuation is None:
        return run, state, {str(run): _source(run)}
    if (state['status'] not in ('needs_input', 'blocked') or 'session_id' not in state
            or accepted_continuation is None):
        raise ValueError('cleanup requires current independent acceptance of done or an explicitly answered turn')
    accepted = Path(accepted_continuation).resolve(strict=True)
    original = load(run / 'spec.json')
    fields = ('task', 'cwd', 'step_id', 'harness', 'artifact_root')
    session = state['session_id']
    sources, terminals = {}, set()
    current, descendant = accepted, None
    while True:
        spec = load(current / 'spec.json')
        if (current.parent != run.parent or str(current) in sources
                or any(spec.get(key) != original.get(key) for key in fields)):
            raise ValueError('answered-turn continuation identity mismatch or cycle')
        current_state = _reconcile(current)
        if current == accepted:
            if current_state['status'] != 'done':
                raise ValueError('answered-turn cleanup requires a current independently accepted done continuation')
            accepted_state = current_state
        elif current_state['status'] not in ('needs_input', 'blocked'):
            raise ValueError('preserve an unresolved or invalid continuation ancestor')
        if current_state['status'] == 'blocked':
            resolutions = [r for r in read_events(Path(spec['task']) / 'decision.log')
                           if r['event_id'] == spec['run_id'] + ':resolution']
            if len(resolutions) != 1 or not resolutions[0]['data'].get('evidence'):
                raise ValueError('blocked continuation requires recorded resolution evidence')
        if current_state.get('session_id') != session:
            raise ValueError('answered-turn native session identity mismatch')
        if descendant is not None:
            intent = _intent(current, 'continuation')
            if (intent['kind'] != 'resume.intent' or intent['data'].get('run') != str(descendant)
                    or intent['data'].get('session_id') != session):
                raise ValueError('answered-turn continuation intent mismatch')
        terminal = _owned_terminal(current, spec)
        if terminal in terminals or not _processes_stopped(current):
            raise ValueError('answered-turn cleanup requires distinct owned terminals and stopped processes')
        terminals.add(terminal)
        sources[str(current)] = _source(current)
        if current == run:
            break
        if not spec.get('resume_from') or spec.get('resume_session') != session:
            raise ValueError('accepted run is not an exact continuation of this answered turn')
        descendant, current = current, Path(spec['resume_from']).resolve(strict=True)
    return accepted, accepted_state, sources


def cleanup(run, reason, agtermctl=None, timeout=15, *, accepted_continuation=None):
    """Close one owned accepted terminal once, after the lead retires it explicitly."""
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError('lead cleanup reason/evidence required')
    run = Path(run).resolve(strict=True)
    spec = load(run / 'spec.json')
    with controller(spec['task']), lock(run / 'cleanup.lock'):
        rows = read_events(Path(spec['task']) / 'decision.log')
        if any(r['event_id'] == spec['run_id'] + ':cleanup' for r in rows):
            return _cleanup_state(run, spec, timeout)
        acceptance_run, state, sources = _cleanup_acceptance(run, accepted_continuation)
        verification_sha256 = sha256(acceptance_run / 'verification.json')
        sid = _owned_terminal(run, spec)
        command = _close_command(spec, sid)
        if agtermctl is not None and str(Path(shutil.which(agtermctl) or agtermctl).resolve()) != command[0]:
            raise ValueError('agterm CLI differs from pinned identity')
        with lock(run / 'run.lock'):
            if not _processes_stopped(run):
                raise ValueError('cleanup requires confirmed stopped worker processes and group')
            if acceptance_run == run and any(r['event_id'] == spec['run_id'] + ':continuation' for r in rows):
                raise ValueError('preserve a terminal with a continuation intent until reconciled')
            tree, sessions = _agterm_tree(spec['agterm_identity'], timeout)
            found = sessions.get(sid)
            if found is None or found[0] != spec['agterm_identity']['workspace_id']:
                raise ValueError('owned terminal missing or moved; reconcile without close')
            node = found[1]
            surfaces = node.get('surfaces')
            primary = surfaces[0] if isinstance(surfaces, list) and len(surfaces) == 1 else {}
            cwd = node.get('cwd')
            if (node.get('name') != spec['terminal_name'] or node.get('realized') is not True
                    or not (node.get('foregroundShell') or node.get('commandWait') is True)
                    or node.get('foreground')
                    or (node.get('status') == 'blocked' and acceptance_run == run)
                    or not isinstance(cwd, str) or not Path(cwd).is_absolute()
                    or str(Path(cwd).resolve()) != spec['cwd']
                    or not isinstance(primary, dict) or primary.get('kind') != 'left'
                    or not primary.get('paneID')
                    or _uuid(primary['paneID']) != load(run / 'terminal.json').get('pane_id')
                    or any(node.get(key) for key in ('hasSplit', 'split', 'scratch', 'overlay', 'hud',
                                                   'ask', 'paneOverlays', 'remoteHost', 'remoteOverlays'))):
                raise ValueError('terminal repurposed or process state unknown; preserve it')
            # Recheck the pinned evidence after observing the terminal and before intent.
            if (any(_source(Path(path)) != digest for path, digest in sources.items())
                    or sha256(acceptance_run / 'verification.json') != verification_sha256
                    or git_snapshot(spec['cwd']) != state['git']):
                raise ValueError('cleanup acceptance evidence changed')
            event(spec['task'], spec['run_id'] + ':cleanup', 'cleanup.intent',
                  {'terminal_id': sid, 'terminal_sha256': sha256(run / 'terminal.json'),
                   'acceptance_run': str(acceptance_run), 'source': sources,
                   'verification_sha256': verification_sha256, 'reason': reason,
                   'command': command, 'tree': tree})
            response = _ipc(command, timeout)
            try:
                _close_reply(response, sid)
                response['valid_reply'] = True
            except (ValueError, KeyError, TypeError) as error:
                response.update(valid_reply=False, reply_error=str(error))
            atomic_json(run / 'cleanup-response.json', response)
        return _cleanup_state(run, spec, timeout)


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
    gate = sub.add_parser('preflight', help='Read-only agterm entry check before any task side effect')
    gate.add_argument('--agtermctl', default='agtermctl')
    gate.add_argument('--timeout', type=float, default=15)
    prep = sub.add_parser('prepare', help='Reserve run ID; persist inputs and intent without launch')
    for name in ('task', 'cwd', 'inventory', 'prompt', 'artifact-root'):
        prep.add_argument('--' + name, type=Path, required=True)
    for name in ('run-id', 'step', 'model', 'effort', 'sandbox'):
        prep.add_argument('--' + name, required=True)
    prep.add_argument('--timeout', type=float, default=600)
    prep.add_argument('--codex', default='codex', help='Legacy Codex executable override')
    prep.add_argument('--harness', choices=native.NAMES, required=True)
    prep.add_argument('--executable', help='Selected harness executable')
    prep.add_argument('--schema', type=Path)
    prep.add_argument('--skill-path', action='append', default=[])
    prep.add_argument('--resume-from', type=Path, help='Exited needs_input run; uses its exact saved UUID')
    prep.add_argument('--agterm-identity', type=Path, help='Saved preflight identity JSON; revalidated before prepare')
    prep.add_argument('--agtermctl', default='agtermctl')
    for action, description in [('launch', 'Send one intent-protected agterm launch'),
                                ('worker', 'Internal agterm entry; claim ID and stream bounded exec'),
                                ('reconcile', 'Observe process/run/events/result/Git; never replay'),
                                ('verify', 'Run separate independent acceptance commands'),
                                ('acknowledge-stopped', 'Pin inspected files after confirmed process death; never replay'),
                                ('cleanup', 'Close one owned accepted terminal, or reconcile its existing close intent')]:
        command = sub.add_parser(action, help=description)
        command.add_argument('--run', type=Path, required=True)
        if action in ('launch', 'cleanup'):
            command.add_argument('--agtermctl')
            command.add_argument('--timeout', type=float, default=15)
        if action in ('acknowledge-stopped', 'cleanup'):
            command.add_argument('--reason', required=True)
        if action == 'cleanup':
            command.add_argument('--accepted-continuation', type=Path,
                                 help='Explicit verified done continuation superseding an answered or resolved blocked turn')
        if action == 'verify':
            command.add_argument('--commands', type=Path, required=True, help='JSON array of command argv arrays')
            command.add_argument('--attempt-id', default='first', help='Unique explicit verification attempt; preserve previous evidence')
            command.add_argument('--verifier', required=True, help='Independent acceptance-check identity')
            command.add_argument('--timeout', type=float, default=120)
    args = parser.parse_args()
    if args.action == 'preflight':
        value = preflight(args.agtermctl, args.timeout)
    elif args.action == 'prepare':
        value = str(prepare(args.task, args.run_id, args.step, args.cwd, load(args.inventory), args.model,
                            None if args.effort == 'default' else args.effort, args.sandbox, args.prompt.read_text(), args.artifact_root,
                            args.timeout, args.schema, args.codex, args.skill_path, args.resume_from, args.harness, args.executable,
                            agterm_identity=load(args.agterm_identity) if args.agterm_identity else None, agtermctl=args.agtermctl))
    elif args.action == 'launch':
        value = launch(args.run, args.agtermctl, args.timeout)
    elif args.action == 'worker':
        value = worker(args.run)
    elif args.action == 'acknowledge-stopped':
        value = acknowledge_stopped(args.run, args.reason)
    elif args.action == 'cleanup':
        value = cleanup(args.run, args.reason, args.agtermctl, args.timeout,
                        accepted_continuation=args.accepted_continuation)
    elif args.action == 'verify':
        value = verify(args.run, load(args.commands), args.verifier, args.timeout, args.attempt_id)
    else:
        value = reconcile(args.run)
    print(json.dumps(value))
    return (value['exit_code'] if value['exit_code'] is not None else 1) if args.action == 'worker' else 0


if __name__ == '__main__':
    raise SystemExit(main())
