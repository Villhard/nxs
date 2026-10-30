"""Deterministic public-helper regressions. No live Codex, agterm or skill install."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/dev-lead/scripts'
sys.path.insert(0, str(SCRIPTS))
import inventory
import journal
import mechanics
import outcome
import runner

spec = importlib.util.spec_from_file_location('lead_commit', SCRIPTS / 'commit.py')
commit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(commit)

SESSION = '12345678-1234-4234-8234-123456789abc'
WINDOW = '11111111-1111-4111-8111-111111111111'
WORKSPACE = '22222222-2222-4222-8222-222222222222'
LEAD = '33333333-3333-4333-8333-333333333333'
FAKE_CODEX = r'''#!/usr/bin/env python3
import json, os, pathlib, subprocess, sys, time
root = pathlib.Path(__file__).parent
config = json.loads((root / 'fixture.json').read_text())
def trace(row):
    with (root / 'trace.jsonl').open('a') as f:
        f.write(json.dumps(row) + '\n')
if sys.argv[1] == 'app-server':
    for line in sys.stdin:
        row = json.loads(line)
        trace(row)
        if 'id' not in row:
            continue
        method = row['method']
        if config.get('init_timeout') and method == 'initialize':
            time.sleep(5)
        if config.get('malformed_rpc') == method:
            print('[]', flush=True)
            continue
        if config.get('rpc_error') == method:
            print(json.dumps({'id': row['id'], 'error': {'message': 'fixture denied'}}), flush=True)
            continue
        if method == 'initialize':
            value = {}
        elif method == 'skills/list':
            cwd = row['params']['cwds'][0]
            value = {'data': [{'cwd': cwd, 'skills': [
                {'name': 'fixture-skill', 'path': str(root / 'skill/SKILL.md'), 'enabled': True},
                {'name': 'disabled-skill', 'path': str(root / 'skill/SKILL.md'), 'enabled': False}],
                'errors': [{'message': 'bad skill'}] if config.get('skill_error') else []}]}
        elif method == 'model/list':
            if row['params'].get('cursor'):
                value = {'data': [{'model': 'fixture-model', 'supportedReasoningEfforts': [{'reasoningEffort': 'high'}]}], 'nextCursor': None}
            else:
                value = {'data': [], 'nextCursor': 'page-two'}
        print(json.dumps({'id': row['id'], 'result': value}), flush=True)
else:
    args = sys.argv[1:]
    trace({'exec': args})
    assert args[0] == 'exec'
    for flag in ['--ignore-user-config', '-C', '-m', '-s', '--json', '--output-schema', '-o']:
        assert flag in args, flag
    assert args[args.index('-m') + 1] == 'fixture-model'
    assert 'model_reasoning_effort="high"' in args
    if 'resume' in args:
        assert args[args.index('resume') + 1] == '12345678-1234-4234-8234-123456789abc'
        assert '--last' not in args
    received = sys.stdin.read()
    (root / "last-prompt.txt").write_text(received)
    print(json.dumps({'type': 'thread.started', 'thread_id': '12345678-1234-4234-8234-123456789abc'}), flush=True)
    path = pathlib.Path(config['artifact'])
    mode = config.get('worker', 'done')
    if mode != 'missing_artifact':
        path.write_text('worker result\n')
    if mode == 'sleep':
        time.sleep(10)
    if mode == 'slow':
        time.sleep(.4)
    if config.get('background_child'):
        release = root / 'release-child'
        child_code = "import pathlib,sys,time; release=pathlib.Path(sys.argv[1]); deadline=time.monotonic()+15\nwhile not release.exists() and time.monotonic()<deadline: time.sleep(.02)"
        child = subprocess.Popen([sys.executable, '-c', child_code, str(release)],
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        (root / 'background.json').write_text(json.dumps({'pid': child.pid, 'pgid': os.getpgrp()}))
    result = pathlib.Path(args[args.index('-o') + 1])
    status = 'blocked' if mode == 'blocked' else ('needs_input' if mode == 'question' and ('resume' not in args or config.get('repeat_question')) else 'done')
    value = {'status': status, 'step_id': 'step-1', 'summary': 'Fixture outcome', 'evidence': ['fixture check'], 'artifacts': [str(path)],
             'question': 'Which option?' if status == 'needs_input' else '', 'reason': 'Missing external evidence' if status == 'blocked' else ''}
    if mode != 'missing_result':
        result.write_text('{bad' if mode == 'malformed' else json.dumps(value))
    if config.get('malformed_events'): print('{bad', flush=True)
    if not config.get('omit_completed'): print(json.dumps({'type': 'turn.completed'}), flush=True)
    print('fixture stderr', file=sys.stderr, flush=True)
    sys.exit(7 if mode == 'nonzero' else 0)
'''
FAKE_AGTERM = r'''#!/usr/bin/env python3
import json, os, pathlib, shlex, subprocess, sys, time, uuid
root = pathlib.Path(__file__).parent
config = json.loads((root / 'fixture.json').read_text())
args = sys.argv[1:]
state_path = root / 'agterm.json'
state = json.loads(state_path.read_text())
def option(name): return args[args.index(name)+1]
def save(): state_path.write_text(json.dumps(state))
def reply(value):
    print(json.dumps({'ok': True, 'result': value}), flush=True)
    sys.exit(0)
assert option('--socket') == str(root / 'agterm.sock')
if config.get('ipc_error'):
    print(config['ipc_error'], file=sys.stderr); sys.exit(1)
if config.get('bad_reply'):
    print('[]'); sys.exit(0)
if config.get('ipc_sleep'): time.sleep(5)
if args[:2] == ['window', 'list']: reply({'windows': state['windows']})
window = option('--window')
tree = state['trees'][window]
if args[0] == 'tree': reply({'tree': tree})
if args[:2] == ['session', 'close']:
    sid = option('--target')
    with (root / 'closes.jsonl').open('a') as f: f.write(json.dumps(args)+'\n')
    if config.get('close') == 'lost-before': time.sleep(5); sys.exit(1)
    for workspace in tree['workspaces']:
        workspace['sessions'] = [s for s in workspace['sessions'] if s['id'] != sid]
    save()
    if config.get('close') == 'lost-after': time.sleep(5)
    reply(config.get('close_reply', {'affected': 1}) if config.get('close') != 'id' else {'id': sid})
assert args[:2] == ['session', 'new']
assert '--wait' in args and '--cwd' in args
if config.get('agterm') == 'no-process': sys.exit(1)
command = shlex.split(args[args.index('--command') + 1])
sid = str(uuid.uuid4())
pane_id = str(uuid.uuid4())
workspace = next(w for w in tree['workspaces'] if w['id'] == option('--workspace'))
# Shape observed for an agterm completed --wait terminal; IDs/cwd are disposable.
node = {'id': sid, 'name': option('--name'), 'realized': not config.get('unrealized'),
        'foreground': command, 'commandWait': True, 'cwd': option('--cwd'),
        'active': False, 'scratch': False, 'split': False, 'overlay': False,
        'backedByZmx': False, 'flagged': False, 'fontSize': 13,
        'surfaces': [{'id': 'surface:'+sid+':left', 'kind': 'left', 'paneID': pane_id,
                      'active': True, 'visible': True, 'backedByZmx': False}]}
workspace['sessions'].append(node)
save()
with (root / 'launches.jsonl').open('a') as f:
    f.write(json.dumps(command) + '\n')
with (root / 'create-args.jsonl').open('a') as f: f.write(json.dumps(args)+'\n')
env = dict(os.environ, AGTERM_ENABLED='1', AGTERM_SOCKET=option('--socket'),
           AGTERM_WINDOW_ID=window, AGTERM_WORKSPACE_ID=workspace['id'], AGTERM_SESSION_ID=sid,
           AGTERM_PANE_ID=pane_id)
with (root / 'visible.log').open('ab') as f:
    child = subprocess.Popen(command, stdout=f, stderr=f, start_new_session=True, env=env)
(root / 'worker-pid').write_text(str(child.pid))
if config.get('agterm') == 'lost':
    time.sleep(10)
elif config.get('agterm') != 'async':
    child.wait(timeout=10)
    node.pop('foreground', None)
    if config.get('hold') != 'wait': node['foregroundShell'] = 'zsh'
    save()
reply({'id': sid})
'''


class Helpers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.task = self.root / 'task'
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.artifact = self.repo / 'result.txt'
        self.artifact.write_text('baseline\n')
        self.git('init', '-q')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('add', '.')
        self.git('commit', '-qm', 'Fixture baseline')
        self.codex = self.bin / 'codex'
        self.agterm = self.bin / 'agtermctl'
        for path, source in [(self.codex, FAKE_CODEX), (self.agterm, FAKE_AGTERM)]:
            path.write_text(source)
            path.chmod(0o755)
        (self.bin / 'skill').mkdir()
        (self.bin / 'skill/SKILL.md').write_text('Fixture skill\n')
        self.config = {'artifact': str(self.artifact)}
        self.configure()
        journal.atomic_json(self.bin / 'agterm.json', {
            'windows': [{'id': WINDOW, 'open': True, 'active': True}],
            'trees': {WINDOW: {'workspaces': [{'id': WORKSPACE, 'sessions': [
                {'id': LEAD, 'name': 'lead', 'realized': True, 'foregroundShell': 'zsh'}]}]}}})
        self.env = patch.dict(os.environ, {'AGTERM_ENABLED': '1', 'AGTERM_SOCKET': str(self.bin / 'agterm.sock'),
                                         'AGTERM_WINDOW_ID': WINDOW, 'AGTERM_WORKSPACE_ID': WORKSPACE,
                                         'AGTERM_SESSION_ID': LEAD})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.catalog = inventory.discover([self.repo], str(self.codex), 3)
        self.assertEqual(self.catalog['models']['status'], 'ok')

    def tearDown(self):
        # Interrupted workers have independent process groups; fixtures own their cleanup.
        for file in self.root.glob('*/research/dev-lead/runs/*/execution/process.json'):
            try:
                os.killpg(mechanics.load(file)['pid'], signal.SIGKILL)
            except ProcessLookupError:
                pass
        if (self.bin / 'worker-pid').exists():
            try:
                os.kill(int((self.bin / 'worker-pid').read_text()), signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.temp.cleanup()

    def configure(self, **changes):
        self.config.update(changes)
        (self.bin / 'fixture.json').write_text(json.dumps(self.config))

    def git(self, *args):
        return mechanics.git(self.repo, *args)

    def prepare(self, identity='one', **kwargs):
        options = dict(task=self.task, run_id=identity, step_id='step-1', cwd=self.repo,
                       inventory=self.catalog, model='fixture-model', effort='high',
                       sandbox='workspace-write', prompt='Bounded fixture task',
                       artifact_root=self.repo, codex=str(self.codex), timeout=3,
                       agtermctl=str(self.agterm),
                       skill_paths=[str(self.bin / 'skill/SKILL.md')])
        options.update(kwargs)
        return runner.prepare(**options)

    def execute(self, identity='one', **kwargs):
        run = self.prepare(identity, **kwargs)
        result = runner.launch(run, str(self.agterm), 5)
        self.assertFalse(result['uncertain'], result)
        return run

    def wait_for(self, predicate, timeout=5):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(.02)
        self.fail('fixture did not reach expected state')

    def checks(self):
        return [[sys.executable, '-c', "from pathlib import Path; assert Path('result.txt').read_text() == 'worker result\\n'; print('acceptance passed')"]]

    def verify(self, run):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return runner.verify(run, self.checks(), 'independent-fixture-check')

    def test_real_protocol_inventory_pagination_paths_and_hashes(self):
        skill = inventory.skill_status(self.catalog, self.repo, 'fixture-skill')
        self.assertEqual(skill['status'], 'enabled')
        self.assertEqual(skill['matches'][0]['path'], str(self.bin / 'skill/SKILL.md'))
        self.assertEqual(skill['matches'][0]['sha256'], mechanics.sha256(self.bin / 'skill/SKILL.md'))
        rows = [json.loads(s) for s in (self.bin / 'trace.jsonl').read_text().splitlines()]
        self.assertEqual(rows[0]['method'], 'initialize')
        self.assertEqual(rows[1]['method'], 'initialized')
        self.assertEqual([r['params'] for r in rows if r['method'] == 'model/list'],
                         [{'limit': 100}, {'limit': 100, 'cursor': 'page-two'}])
        self.assertEqual(inventory.skill_status(self.catalog, self.repo, 'disabled-skill')['status'], 'disabled')
        self.assertEqual(inventory.skill_status(self.catalog, self.repo, 'absent')['status'], 'missing')

    def test_inventory_per_cwd(self):
        second = self.root / 'second'
        second.mkdir()
        value = inventory.discover([self.repo, second], str(self.codex), 3)
        self.assertEqual(set(value['skills']), {str(self.repo), str(second)})
        self.assertTrue(all(s['status'] == 'ok' for s in value['skills'].values()))

    def test_inventory_errors_are_not_missing(self):
        for changes in [{'skill_error': True}, {'rpc_error': 'skills/list'}]:
            with self.subTest(changes=changes):
                self.configure(**{'skill_error': False, 'rpc_error': None, **changes})
                value = inventory.discover([self.repo], str(self.codex), 2)
                self.assertEqual(inventory.skill_status(value, self.repo, 'absent')['status'], 'discovery_failed')
                self.assertEqual(value['models']['status'], 'ok')

    def test_inventory_initialize_timeout_and_missing_executable(self):
        self.configure(init_timeout=True)
        started = time.monotonic()
        value = inventory.discover([self.repo], str(self.codex), .1)
        self.assertLess(time.monotonic() - started, 2)
        self.assertEqual(value['models']['status'], 'discovery_failed')
        self.assertEqual(inventory.skill_status(value, self.repo, 'absent')['status'], 'discovery_failed')
        value = inventory.discover([self.repo], str(self.bin / 'absent'), .1)
        self.assertEqual(value['models']['status'], 'discovery_failed')

    def test_model_discovery_error_and_unsupported_effort(self):
        self.configure(rpc_error='model/list')
        value = inventory.discover([self.repo], str(self.codex), 2)
        with self.assertRaisesRegex(ValueError, 'discovery failed'):
            inventory.validate_model(value, 'fixture-model', 'high')
        with self.assertRaisesRegex(ValueError, 'unsupported reasoning'):
            self.prepare(effort='unsupported')
        self.assertFalse((self.task / 'research/dev-lead/runs').exists())

    def test_question_saved_and_exact_id_resume(self):
        self.configure(worker='question')
        question = self.execute('question')
        state = runner.reconcile(question)
        self.assertEqual(state['status'], 'needs_input')
        self.assertEqual(state['outcome']['question'], 'Which option?')
        self.assertEqual(state['session_id'], SESSION)
        resumed = self.execute('answer', resume_from=question)
        self.assertEqual(runner.reconcile(resumed)['status'], 'unverified')
        command = mechanics.load(resumed / 'spec.json')['command']
        self.assertEqual(command[-3:], ['resume', SESSION, '-'])
        self.verify(resumed)
        self.assertEqual(runner.reconcile(resumed)['status'], 'done')

    def test_done_requires_independent_actual_checks(self):
        run = self.execute()
        self.assertEqual(runner.reconcile(run)['status'], 'unverified')
        report = self.verify(run)
        self.assertEqual(runner.reconcile(run)['status'], 'done')
        self.assertIn('acceptance passed', (run / 'checks/first/0/stdout').read_text())
        self.assertEqual(mechanics.load(run / 'checks/first/0/exit.json')['exit_code'], 0)
        self.assertEqual(report['artifacts'][str(self.artifact)], mechanics.sha256(self.artifact))
        self.assertEqual(report['git'], mechanics.git_snapshot(self.repo))
        self.assertIn('thread.started', (run / 'execution/stdout').read_text())
        self.assertIn('thread.started', (self.bin / 'visible.log').read_text())
        self.assertEqual((run / 'execution/stderr').read_text(), 'fixture stderr\n')

    def test_malformed_missing_json_and_missing_artifacts(self):
        for mode in ('malformed', 'missing_result', 'missing_artifact'):
            with self.subTest(mode=mode):
                self.configure(worker=mode)
                if mode == 'missing_artifact':
                    self.artifact.unlink()
                run = self.execute(mode)
                self.assertEqual(runner.reconcile(run)['status'], 'invalid')

    def test_outcome_step_question_reason_and_path_validation(self):
        value = dict(status='done', step_id='step-1', summary='Complete',
                     artifacts=[str(self.artifact)], evidence=['fixture check'], question='', reason='')
        self.assertEqual(outcome.validate(value, 'step-1', self.repo), value)
        for change in [dict(step_id='wrong'), dict(status='needs_input'), dict(status='blocked'),
                       dict(artifacts=['../outside']), dict(extra=True), dict(question='unexpected')]:
            with self.subTest(change=change), self.assertRaises((ValueError, OSError)):
                outcome.validate({**value, **change}, 'step-1', self.repo)
        self.assertEqual(outcome.validate({**value, 'status': 'needs_input', 'question': 'Choose', 'reason': 'A user decision is required'}, 'step-1', self.repo)['status'], 'needs_input')
        outside = self.root / 'outside'
        outside.write_text('outside')
        link = self.repo / 'link'
        link.symlink_to(outside)
        with self.assertRaises(ValueError):
            outcome.validate({**value, 'evidence': ['fixture check'], 'artifacts': ['link']}, 'step-1', self.repo)
        self.assertEqual(outcome.validate({**value, 'status': 'blocked', 'reason': 'Unavailable'}, 'step-1', self.repo)['status'], 'blocked')

    def test_duplicate_run_and_duplicate_launch_cannot_execute_twice(self):
        run = self.execute()
        with self.assertRaises(FileExistsError):
            self.prepare()
        with self.assertRaisesRegex(ValueError, 'already attempted'):
            runner.launch(run, str(self.agterm))
        with self.assertRaises(FileExistsError):
            runner.worker(run, terminal=False)
        self.assertEqual(len((self.bin / 'launches.jsonl').read_text().splitlines()), 1)

    def test_second_controller_is_rejected_by_os_lock(self):
        with runner.controller(self.task):
            command = [sys.executable, '-c',
                       'import sys; sys.path.insert(0, sys.argv[1]); import runner; '\
                       'c=runner.controller(sys.argv[2]); c.__enter__()', str(SCRIPTS), str(self.task)]
            response = subprocess.run(command, capture_output=True, timeout=3)
            self.assertNotEqual(response.returncode, 0)
            self.assertIn(b'BlockingIOError', response.stderr)
        with runner.controller(self.task):
            pass

    def test_journal_idempotence_conflict_and_torn_record(self):
        path = self.task / 'decision.log'
        first = journal.append_event(path, 'unique', 'question', {'text': 'Choose'})
        self.assertEqual(journal.append_event(path, 'unique', 'question', {'text': 'Choose'}), first)
        self.assertEqual(len(journal.read_events(path)), 1)
        with self.assertRaises(ValueError):
            journal.append_event(path, 'unique', 'question', {'text': 'Different'})
        with path.open('ab') as stream:
            stream.write(b'{"event_id":')
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            journal.recover_state(path)

    def test_event_before_state_crash_recovery_and_retry(self):
        path = self.task / 'decision.log'
        with patch.object(journal, '_cache', side_effect=OSError('simulated state replacement interruption')):
            with self.assertRaises(OSError):
                journal.append_event(path, 'durable', 'decision', {'answer': 42})
        self.assertFalse((self.task / 'research/dev-lead/journal-state.json').exists())
        self.assertEqual(journal.recover_state(path)['last_event_id'], 'durable')
        journal.append_event(path, 'durable', 'decision', {'answer': 42})
        self.assertEqual(len(journal.read_events(path)), 1)

    def test_standalone_journal_copy_cli(self):
        copy = self.root / 'journal.py'
        copy.write_bytes((SCRIPTS / 'journal.py').read_bytes())
        response = subprocess.run([sys.executable, str(copy), 'append', str(self.task / 'decision.log'),
                                   'manual', 'handoff', '{"next":"review"}'], capture_output=True, timeout=3)
        self.assertEqual(response.returncode, 0, response.stderr)
        self.assertEqual(journal.read_events(self.task / 'decision.log')[0]['data']['next'], 'review')
        self.assertIsInstance(journal.read_events(self.task / 'decision.log')[0]['data']['timestamp'], (int, float))
        self.assertEqual({p.name for p in self.task.iterdir()}, {'decision.log', 'research'})

    def test_live_worker_session_is_saved_before_exit(self):
        self.configure(worker='sleep', agterm='async')
        run = self.execute(timeout=1)
        self.wait_for(lambda: (run / 'session.json').exists())
        self.assertFalse((run / 'execution/exit.json').exists())
        self.assertEqual(mechanics.load(run / 'session.json')['session_id'], SESSION)
        self.assertEqual(runner.reconcile(run)['status'], 'live')
        self.wait_for(lambda: (run / 'execution/exit.json').exists())
        self.assertEqual(runner.reconcile(run)['status'], 'blocked')
        self.assertTrue(mechanics.load(run / 'execution/exit.json')['timed_out'])

    def test_interruption_after_worker_files_never_replays(self):
        self.configure(worker='sleep', agterm='async')
        run = self.execute()
        self.wait_for(lambda: self.artifact.read_text() == 'worker result\n' and (run / 'execution/process.json').exists())
        os.kill(int((self.bin / 'worker-pid').read_text()), signal.SIGKILL)
        self.wait_for(lambda: self._run_lock_available(run))
        state = runner.reconcile(run)
        self.assertEqual(state['status'], 'uncertain')
        self.assertTrue(state['changed_since_intent'])
        self.assertIn('execution/process.json', state['records'])
        with self.assertRaises(ValueError):
            runner.launch(run, str(self.agterm))
        self.assertEqual(self.artifact.read_text(), 'worker result\n')

    @staticmethod
    def _run_lock_available(run):
        try:
            with journal.lock(run / 'run.lock'):
                return True
        except BlockingIOError:
            return False

    def test_lost_launch_response_reconciles_completed_worker(self):
        self.configure(agterm='lost', worker='slow')
        run = self.prepare()
        result = runner.launch(run, str(self.agterm), .8)
        self.assertTrue(result['uncertain'])
        self.wait_for(lambda: (run / 'execution/exit.json').exists())
        self.assertEqual(runner.reconcile(run)['status'], 'unverified')
        with self.assertRaises(ValueError):
            runner.launch(run, str(self.agterm))
        self.assertEqual(len((self.bin / 'launches.jsonl').read_text().splitlines()), 1)
        self.verify(run)
        self.assertEqual(runner.reconcile(run)['status'], 'done')

    def test_lost_launch_without_process_is_uncertain(self):
        run = self.prepare()
        self.configure(agterm='no-process')
        result = runner.launch(run, str(self.agterm))
        self.assertTrue(result['uncertain'])
        self.assertEqual(runner.reconcile(run)['status'], 'uncertain')
        with self.assertRaises(ValueError):
            runner.launch(run, str(self.agterm))

    def test_worker_nonzero_exit_is_blocked_with_output(self):
        self.configure(worker='nonzero')
        run = self.execute()
        state = runner.reconcile(run)
        self.assertEqual(state['status'], 'blocked')
        self.assertEqual(state['exit']['exit_code'], 7)
        self.assertIn('turn.completed', (run / 'execution/stdout').read_text())

    def test_failed_independent_check_never_completes(self):
        run = self.execute()
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(ValueError):
            runner.verify(run, [[sys.executable, '-c', "import sys; print('failed', file=sys.stderr); sys.exit(4)"]], 'independent')
        self.assertEqual(runner.reconcile(run)['status'], 'unverified')
        self.assertEqual(mechanics.load(run / 'checks/first/0/exit.json')['exit_code'], 4)
        self.assertIn('failed', (run / 'checks/first/0/stderr').read_text())

    def test_changed_evidence_invalidates_done(self):
        for change in ('artifact', 'untracked', 'index', 'head', 'output'):
            with self.subTest(change=change):
                run = self.execute(change)
                self.verify(run)
                if change == 'artifact':
                    self.artifact.write_text('changed')
                elif change == 'untracked':
                    (self.repo / 'new.txt').write_text('untracked')
                elif change == 'index':
                    self.git('add', 'result.txt')
                elif change == 'head':
                    self.git('commit', '--allow-empty', '-qm', 'Later commit')
                else:
                    (run / 'checks/first/0/stdout').write_text('different evidence')
                self.assertEqual(runner.reconcile(run)['status'], 'stale')

    def test_verification_commands_changing_evidence_are_rejected(self):
        run = self.execute()
        with self.assertRaisesRegex(ValueError, 'changed during'):
            runner.verify(run, [[sys.executable, '-c', "from pathlib import Path; Path('new').write_text('changed')"]], 'independent')
        self.assertFalse((run / 'verification.json').exists())

    def test_skill_hash_change_prevents_launch_exec(self):
        run = self.prepare()
        (self.bin / 'skill/SKILL.md').write_text('Changed skill')
        runner.launch(run, str(self.agterm), 3)
        self.assertFalse((run / 'execution/process.json').exists())
        self.assertEqual(runner.reconcile(run)['status'], 'uncertain')

    def test_commit_intent_lost_response_known_head_without_retry(self):
        self.artifact.write_text('staged change')
        self.git('add', 'result.txt')
        commit.intent(self.task, 'commit-one', self.repo)
        self.assertEqual(commit.reconcile(self.task, 'commit-one', self.repo)['status'], 'uncertain')
        self.git('commit', '-qm', 'Fixture change')  # Response deliberately not recorded.
        state = commit.reconcile(self.task, 'commit-one', self.repo)
        self.assertEqual(state['status'], 'committed_observed')
        self.assertFalse(state['replay_safe'])
        with self.assertRaises(ValueError):
            commit.intent(self.task, 'commit-one', self.repo)
        self.git('commit', '--allow-empty', '-qm', 'Unrelated later commit')
        self.assertEqual(commit.reconcile(self.task, 'commit-one', self.repo)['status'], 'uncertain')

    def test_prepared_spec_change_and_unknown_resume_are_rejected(self):
        run = self.prepare()
        value = mechanics.load(run / 'spec.json')
        value['step_id'] = 'changed'
        journal.atomic_json(run / 'spec.json', value)
        with self.assertRaisesRegex(ValueError, 'specification changed'):
            runner.launch(run, str(self.agterm))
        done = self.execute('done')
        with self.assertRaisesRegex(ValueError, 'needs_input'):
            self.prepare('bad-resume', resume_from=done)

    def test_controller_can_span_nested_public_api_calls(self):
        with runner.controller(self.task):
            run = self.execute()
            self.assertEqual(runner.reconcile(run)['status'], 'unverified')
            self.verify(run)
            self.assertEqual(runner.reconcile(run)['status'], 'done')

    def test_question_continuation_cannot_be_reserved_twice(self):
        self.configure(worker='question')
        question = self.execute('question')
        self.prepare('answer', resume_from=question)
        with self.assertRaisesRegex(ValueError, 'continuation intent'):
            self.prepare('duplicate-answer', resume_from=question)
        self.assertFalse((self.task / 'research/dev-lead/runs/duplicate-answer').exists())

    def test_unresolved_launch_blocks_new_worker(self):
        run = self.prepare()
        self.configure(agterm='no-process')
        runner.launch(run, str(self.agterm))
        next_run = self.prepare('next')
        with self.assertRaisesRegex(ValueError, 'no durable exit'):
            runner.launch(next_run, str(self.agterm))
        with self.assertRaisesRegex(ValueError, 'confirmed absent'):
            runner.acknowledge_stopped(run, 'Cannot prove a lost launch did not occur')
        self.assertFalse((next_run / 'launch.json').exists())

    def background_run(self, mode):
        self.task = self.root / ('task-' + mode)
        (self.bin / 'release-child').unlink(missing_ok=True)
        self.configure(worker=mode, background_child=True)
        run = self.execute('background')
        process = mechanics.load(run / 'execution/process.json')
        child = mechanics.load(self.bin / 'background.json')
        self.assertEqual(mechanics.load(run / 'execution/exit.json')['exit_code'], 0)
        self.assertEqual(child['pgid'], process['pid'])
        self.assertFalse(runner._pid_present(int((run / 'claim').read_text())))
        self.assertFalse(runner._pid_present(process['owner_pid']))
        self.assertFalse(runner._pid_present(process['pid']))
        self.assertTrue(runner._pid_present(child['pid']))
        self.assertTrue(runner._group_present(process['pid']))
        self.assertFalse(runner._processes_stopped(run))
        return run

    def release_background(self, run):
        (self.bin / 'release-child').touch()
        process = mechanics.load(run / 'execution/process.json')
        self.wait_for(lambda: not runner._group_present(process['pid']))

    def test_successful_exit_live_group_blocks_continuation(self):
        for mode in ('question', 'blocked'):
            with self.subTest(mode=mode):
                run = self.background_run(mode)
                try:
                    if mode == 'blocked':
                        runner.event(self.task, 'background:resolution', 'blocker.resolved',
                                     {'evidence': ['Fixture prerequisite checked']})
                    with patch.object(runner.native, 'check_resume') as resume:
                        with self.assertRaisesRegex(ValueError, 'stopped processes'):
                            self.prepare('answer', resume_from=run)
                        resume.assert_not_called()
                    self.assertFalse((run.parent / 'answer').exists())
                    self.assertNotIn('background:continuation',
                                     [r['event_id'] for r in journal.read_events(self.task / 'decision.log')])
                finally:
                    self.release_background(run)
                self.configure(worker='done', background_child=False)
                resumed = self.execute('answer', resume_from=run)
                self.assertEqual(mechanics.load(resumed / 'spec.json')['resume_session'], SESSION)

    def test_successful_exit_live_group_blocks_next_launch(self):
        for mode in ('question', 'done'):
            with self.subTest(mode=mode):
                run = self.background_run(mode)
                next_run = self.prepare('next')
                before = mechanics.git_snapshot(self.repo)
                trace = (self.bin / 'trace.jsonl').read_bytes()
                creates = (self.bin / 'create-args.jsonl').read_bytes()
                try:
                    with self.assertRaisesRegex(ValueError, 'stopped processes'):
                        runner.launch(next_run, str(self.agterm))
                    self.assertEqual(mechanics.git_snapshot(self.repo), before)
                    self.assertEqual((self.bin / 'trace.jsonl').read_bytes(), trace)
                    self.assertEqual((self.bin / 'create-args.jsonl').read_bytes(), creates)
                    self.assertNotIn('next:launch',
                                     [r['event_id'] for r in journal.read_events(self.task / 'decision.log')])
                    self.assertFalse((next_run / 'claim').exists())
                    self.assertFalse((self.bin / 'closes.jsonl').exists())
                finally:
                    self.release_background(run)
                self.configure(worker='done', background_child=False)
                self.assertFalse(runner.launch(next_run, str(self.agterm))['uncertain'])

    def test_worker_rejects_wrong_destination_before_native_execution(self):
        for field in ('AGTERM_WINDOW_ID', 'AGTERM_WORKSPACE_ID'):
            with self.subTest(field=field):
                self.task = self.root / field.lower()
                run = self.prepare()
                runner.event(self.task, 'one:launch', 'launch.intent', {'command': ['fixture-entry']})
                before = mechanics.git_snapshot(self.repo)
                trace = (self.bin / 'trace.jsonl').read_bytes()
                env = {'AGTERM_SESSION_ID': '44444444-4444-4444-8444-444444444444',
                       'AGTERM_PANE_ID': '55555555-5555-4555-8555-555555555555',
                       field: '66666666-6666-4666-8666-666666666666'}
                with patch.dict(os.environ, env), patch.object(runner, 'capture',
                        side_effect=AssertionError('native execution reached')) as capture:
                    with self.assertRaisesRegex(ValueError, 'worker agterm identity differs from pinned destination'):
                        runner.worker(run, terminal=False)
                    capture.assert_not_called()
                self.assertTrue((run / 'claim').exists())
                self.assertFalse((run / 'terminal.json').exists())
                self.assertFalse((run / 'execution').exists())
                self.assertEqual(mechanics.git_snapshot(self.repo), before)
                self.assertEqual((self.bin / 'trace.jsonl').read_bytes(), trace)
                self.assertEqual([r['kind'] for r in journal.read_events(self.task / 'decision.log')],
                                 ['run.prepared', 'launch.intent'])
                self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_transition_rechecks_missing_or_live_process_evidence(self):
        self.configure(worker='question')
        run = self.execute()
        queued = self.prepare('queued')
        claim = (run / 'claim').read_bytes()
        process = (run / 'execution/process.json').read_bytes()
        for case in ('missing-claim', 'missing-process', 'wrapper', 'owner', 'cli', 'group-permission'):
            with self.subTest(case=case):
                value = json.loads(process)
                if case == 'missing-claim':
                    (run / 'claim').unlink()
                elif case == 'missing-process':
                    (run / 'execution/process.json').unlink()
                elif case == 'wrapper':
                    (run / 'claim').write_text(str(os.getpid()))
                elif case in ('owner', 'cli'):
                    value['owner_pid' if case == 'owner' else 'pid'] = os.getpid()
                    journal.atomic_json(run / 'execution/process.json', value)
                probe = (patch.object(runner.os, 'killpg', side_effect=PermissionError('fixture denied'))
                         if case == 'group-permission' else contextlib.nullcontext())
                try:
                    with probe, patch.object(runner.native, 'check_resume') as resume:
                        self.assertFalse(runner._processes_stopped(run))
                        message = ('saved needs_input' if case == 'missing-process' else 'stopped processes')
                        with self.assertRaisesRegex(ValueError, message):
                            self.prepare('answer', resume_from=run)
                        resume.assert_not_called()
                        with patch.object(runner, '_ipc') as ipc:
                            with self.assertRaisesRegex(ValueError, 'stopped processes'):
                                runner.launch(queued, str(self.agterm))
                            ipc.assert_not_called()
                    self.assertFalse((queued.parent / 'answer').exists())
                    self.assertFalse((queued / 'claim').exists())
                finally:
                    (run / 'claim').write_bytes(claim)
                    (run / 'execution/process.json').write_bytes(process)
        self.assertTrue(runner._processes_stopped(run))
        resumed = self.execute('answer', resume_from=run)
        self.assertEqual(mechanics.load(resumed / 'spec.json')['resume_session'], SESSION)
        self.assertFalse(runner.launch(queued, str(self.agterm))['uncertain'])

    def test_stopped_historical_exit_does_not_require_current_acceptance(self):
        first = self.execute()
        self.verify(first)
        self.artifact.write_text('later accepted work\n')
        self.assertEqual(runner.reconcile(first)['status'], 'stale')
        self.assertTrue(runner._processes_stopped(first))
        later = self.execute('later')
        self.assertEqual(runner.reconcile(later)['status'], 'unverified')

    def test_interrupted_files_can_be_acknowledged_and_exact_session_continued(self):
        self.configure(worker='sleep', agterm='async')
        run = self.execute()
        self.wait_for(lambda: (run / 'session.json').exists()
                      and self.artifact.read_text() == 'worker result\n')
        with self.assertRaises(BlockingIOError):
            runner.acknowledge_stopped(run, 'Still live')
        os.kill(int((self.bin / 'worker-pid').read_text()), signal.SIGKILL)
        child = mechanics.load(run / 'execution/process.json')['pid']
        os.killpg(child, signal.SIGKILL)
        self.wait_for(lambda: self._run_lock_available(run))

        def acknowledge():
            try:
                runner.acknowledge_stopped(run, 'Inspected partial files; recorded processes are absent')
                return True
            except (ValueError, BlockingIOError):
                return False
        self.wait_for(acknowledge)
        self.assertEqual(runner.reconcile(run)['status'], 'interrupted')
        with self.assertRaises(FileExistsError):
            runner.worker(run, terminal=False)
        self.configure(worker='done', agterm='normal')
        continued = self.execute('continued', resume_from=run)
        self.assertEqual(mechanics.load(continued / 'spec.json')['command'][-3:], ['resume', SESSION, '-'])
        self.verify(continued)
        self.assertEqual(runner.reconcile(continued)['status'], 'done')

    def test_verifier_rejects_non_argv_commands(self):
        run = self.execute()
        for commands in ('echo yes', ['echo yes'], [[]], [[1]], []):
            with self.subTest(commands=commands), self.assertRaises(ValueError):
                runner.verify(run, commands, 'independent')
        self.assertFalse((run / 'checks').exists())

    def test_selected_skill_change_invalidates_completion(self):
        run = self.execute()
        self.verify(run)
        (self.bin / 'skill/SKILL.md').write_text('Changed after verification')
        self.assertNotEqual(runner.reconcile(run)['status'], 'done')

    def test_malformed_inventory_response_is_a_discovery_failure(self):
        self.configure(malformed_rpc='initialize')
        value = inventory.discover([self.repo], str(self.codex), 2)
        self.assertEqual(value['models']['status'], 'discovery_failed')
        self.assertIn('malformed', value['models']['error'])

    def test_missing_worker_executable_records_spawn_failure(self):
        run = self.prepare(codex=str(self.bin / 'missing-codex'))
        runner.launch(run, str(self.agterm), 3)
        state = runner.reconcile(run)
        self.assertEqual(state['status'], 'blocked')
        self.assertIsNone(state['exit']['exit_code'])
        self.assertIn('spawn_error', state['exit'])

    def test_concurrent_standalone_appends_keep_one_event(self):
        command = [sys.executable, str(SCRIPTS / 'journal.py'), 'append', str(self.task / 'decision.log'),
                   'same-id', 'decision', '{"answer":42}']
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(4)]
        for process in processes:
            stdout, stderr = process.communicate(timeout=5)
            self.assertEqual(process.returncode, 0, stderr)
            self.assertEqual(json.loads(stdout)['event_id'], 'same-id')
        self.assertEqual(len(journal.read_events(self.task / 'decision.log')), 1)

    def test_bundled_reference_change_invalidates_completion(self):
        reference = self.bin / 'skill/rules.md'
        reference.write_text('Original rule')
        self.catalog = inventory.discover([self.repo], str(self.codex), 3)
        run = self.execute()
        self.verify(run)
        reference.write_text('Changed rule')
        self.assertEqual(runner.reconcile(run)['status'], 'invalid')

    def test_journal_and_cache_artifacts_accept_append_but_reject_rewritten_prefix(self):
        run = self.execute(artifact_root=self.root)
        value = mechanics.load(run / 'result.json')
        value['artifacts'].extend([str(self.task / 'decision.log'), str(self.task / 'research/dev-lead/journal-state.json')])
        journal.atomic_json(run / 'result.json', value)
        self.verify(run)
        self.assertEqual(runner.reconcile(run)['status'], 'done')
        journal.append_event(self.task / 'decision.log', 'next-stage', 'handoff', {'next': 'review'})
        self.assertEqual(runner.reconcile(run)['status'], 'done')
        journal_path = self.task / 'decision.log'
        journal_path.write_text(journal_path.read_text().replace('run.prepared', 'run.tampered', 1))
        self.assertEqual(runner.reconcile(run)['status'], 'stale')

    def test_explicit_reverification_preserves_old_check_evidence(self):
        run = self.execute()
        self.verify(run)
        first = (run / 'checks/first/verification.json').read_bytes()
        self.artifact.write_text('changed')
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            runner.verify(run, [[sys.executable, '-c', "from pathlib import Path; assert Path('result.txt').read_text() == 'changed'"]], 'independent', attempt_id='after-inspection')
        self.assertEqual((run / 'checks/first/verification.json').read_bytes(), first)
        self.assertEqual(runner.reconcile(run)['status'], 'done')

    def test_blocked_session_needs_resolution_evidence_before_exact_resume(self):
        self.configure(worker='blocked')
        first = self.execute()
        self.assertEqual(runner.reconcile(first)['status'], 'blocked')
        with self.assertRaisesRegex(ValueError, 'resolution evidence'):
            self.prepare('continued', resume_from=first)
        runner.event(self.task, 'one:resolution', 'blocker.resolved', {'evidence': ['Fixture prerequisite checked']})
        self.configure(worker='done')
        continued = self.execute('continued', resume_from=first)
        self.assertEqual(runner.reconcile(continued)['status'], 'unverified')
        self.assertIn(SESSION, mechanics.load(continued / 'spec.json')['command'])

    def test_reference_change_between_discovery_and_prepare_is_rejected(self):
        (self.bin / 'skill/new-rule.md').write_text('New behavior')
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.prepare()

    def test_surviving_process_group_blocks_interruption_acknowledgement(self):
        command = [sys.executable, '-c', "import subprocess, sys; p=subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); print(p.pid, flush=True)"]
        parent = subprocess.Popen(command, stdout=subprocess.PIPE, start_new_session=True, text=True)
        parent.communicate(timeout=3)
        self.assertFalse(runner._pid_present(parent.pid))
        run = self.prepare('orphaned')
        runner.event(self.task, 'orphaned:launch', 'launch.intent', {'command': command})
        (run / 'claim').write_text(str(parent.pid))
        journal.atomic_json(run / 'execution/process.json', {'pid': parent.pid, 'owner_pid': parent.pid})
        try:
            self.assertTrue(runner._group_present(parent.pid))
            with self.assertRaisesRegex(ValueError, 'confirmed absent'):
                runner.acknowledge_stopped(run, 'Parents exited but a tool child remains')
        finally:
            os.killpg(parent.pid, signal.SIGKILL)
            (run / 'execution/process.json').unlink()

    def test_incomplete_malformed_and_mismatched_session_streams_are_invalid(self):
        for mode in ('omit_completed', 'malformed_events', 'mismatched_session'):
            self.configure(omit_completed=mode=='omit_completed', malformed_events=mode=='malformed_events')
            run = self.execute(mode)
            if mode == 'mismatched_session':
                journal.atomic_json(run / 'session.json', {'session_id': 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'})
            self.assertEqual(runner.reconcile(run)['status'], 'invalid')
            self.assertFalse((run / 'verification.json').exists())

    def test_worker_receives_task_skill_identity_and_resume_answer(self):
        self.configure(worker='question')
        first = self.execute(prompt='Inspect the greeting task and ask its unresolved choice.')
        initial = (self.bin / 'last-prompt.txt').read_text()
        self.assertIn('Inspect the greeting task', initial)
        self.assertIn(str(self.bin / 'skill/SKILL.md'), initial)
        self.assertIn(mechanics.sha256(self.bin / 'skill/SKILL.md'), initial)
        resumed = self.execute('answer', resume_from=first, prompt='Approved answer: choose option B; preserve nonempty names.')
        self.assertIn('Approved answer: choose option B', (self.bin / 'last-prompt.txt').read_text())
        self.assertEqual(runner.reconcile(resumed)['status'], 'unverified')

    def test_agterm_preflight_failure_has_no_task_side_effects(self):
        for changes, message in [({'AGTERM_ENABLED': '0'}, 'requires agterm'),
                                 ({'AGTERM_SESSION_ID': ''}, 'incomplete agterm'),
                                 ({'AGTERM_WORKSPACE_ID': LEAD}, 'stale agterm workspace')]:
            with self.subTest(changes=changes), patch.dict(os.environ, changes):
                with self.assertRaisesRegex(ValueError, message):
                    self.prepare()
                self.assertFalse(self.task.exists())
        with self.assertRaisesRegex(ValueError, 'CLI missing'):
            self.prepare(agtermctl=str(self.bin / 'missing'))
        self.configure(ipc_error='connect failed: Operation not permitted')
        with self.assertRaisesRegex(ValueError, 'Operation not permitted'):
            self.prepare()
        self.assertFalse(self.task.exists())
        self.assertFalse((self.bin / 'launches.jsonl').exists())

    def test_agterm_preflight_rejects_bad_reply_timeout_and_mismatched_membership(self):
        self.configure(bad_reply=True)
        with self.assertRaisesRegex(ValueError, 'malformed'):
            runner.preflight(str(self.agterm))
        self.configure(bad_reply=False, ipc_sleep=True)
        with self.assertRaisesRegex(ValueError, 'timed out'):
            runner.preflight(str(self.agterm), .05)
        self.configure(ipc_sleep=False)
        state = mechanics.load(self.bin / 'agterm.json')
        state['trees'][WINDOW]['workspaces'].append({'id': LEAD, 'sessions': []})
        journal.atomic_json(self.bin / 'agterm.json', state)
        with patch.dict(os.environ, {'AGTERM_WORKSPACE_ID': LEAD}):
            with self.assertRaisesRegex(ValueError, 'mismatched'):
                self.prepare()
        self.assertFalse(self.task.exists())

    def test_worker_destination_survives_focus_and_environment_change(self):
        identity = runner.preflight(str(self.agterm))
        state = mechanics.load(self.bin / 'agterm.json')
        other_window = '44444444-4444-4444-8444-444444444444'
        state['windows'][0]['active'] = False
        state['windows'].append({'id': other_window, 'open': True, 'active': True})
        state['trees'][other_window] = {'workspaces': [{'id': LEAD, 'sessions': []}]}
        journal.atomic_json(self.bin / 'agterm.json', state)
        with patch.dict(os.environ, {'AGTERM_WINDOW_ID': other_window, 'AGTERM_WORKSPACE_ID': LEAD}):
            run = self.execute('pinned', agterm_identity=identity)
        args = json.loads((self.bin / 'create-args.jsonl').read_text().splitlines()[-1])
        self.assertEqual(args[args.index('--window') + 1], WINDOW)
        self.assertEqual(args[args.index('--workspace') + 1], WORKSPACE)
        self.assertIn('--no-select', args)
        terminal = mechanics.load(run / 'terminal.json')
        self.assertEqual(terminal['window_id'], WINDOW)
        self.assertNotEqual(terminal['session_id'], LEAD)
        self.assertEqual(mechanics.load(run / 'session.json')['session_id'], SESSION)
        self.assertEqual(mechanics.load(self.bin / 'agterm.json')['windows'], state['windows'])

    def test_safe_names_cover_unsafe_components_and_collisions(self):
        occupied = set()
        names = []
        for step, run_id in [('A / B\n$(bad)', 'Foo-Bar'), ('A / B\n$(bad)', 'Foo.Bar'),
                             ('', 'safe'), ('a_b', 'c'), ('a', 'b_c')]:
            label = runner._terminal_name(self.root / 'Unsafe Feature!', step, run_id, occupied)
            self.assertRegex(label, r'^nxs_[a-z0-9]+(?:_[a-z0-9]+)*$')
            self.assertNotIn(label, occupied)
            names.append(label); occupied.add(label)
        self.assertEqual(len(names), len(set(names)))
        original = runner._terminal_name(self.task, 'x', 'y', set())
        suffixed = runner._terminal_name(self.task, 'x', 'y', {original})
        self.assertEqual(suffixed, runner._terminal_name(self.task, 'x', 'y', {original}))
        self.assertNotEqual(suffixed, runner._terminal_name(self.task, 'x', 'y', {original, suffixed}))
        first = self.prepare('Foo-Bar')
        second = self.prepare('Foo.Bar')
        self.assertNotEqual(mechanics.load(first / 'spec.json')['terminal_name'], mechanics.load(second / 'spec.json')['terminal_name'])
        self.assertEqual(mechanics.load(second / 'spec.json')['run_id'], 'Foo.Bar')
        with self.assertRaisesRegex(ValueError, 'safe single path'):
            self.prepare('unsafe/path')

    def test_cleanup_only_closes_owned_accepted_terminal_and_retains_native_identity(self):
        run = self.execute()
        with self.assertRaisesRegex(ValueError, 'independent acceptance'):
            runner.cleanup(run, 'Not independently checked yet')
        self.verify(run)
        before = mechanics.load(self.bin / 'agterm.json')
        sid = mechanics.load(run / 'terminal.json')['session_id']
        self.assertEqual(runner.cleanup(run, 'Lead inspected acceptance; terminal no longer needed')['status'], 'closed')
        self.assertEqual(runner.reconcile(run)['status'], 'done')
        self.assertEqual(runner.reconcile(run)['cleanup']['status'], 'closed')
        after = mechanics.load(self.bin / 'agterm.json')
        self.assertEqual([s for s in before['trees'][WINDOW]['workspaces'][0]['sessions'] if s['id'] != sid],
                         after['trees'][WINDOW]['workspaces'][0]['sessions'])
        command = runner.native.command('codex', str(self.codex), self.repo, 'fixture-model', 'high',
                                        'workspace-write', run, mechanics.load(run / 'session.json')['session_id'])
        self.assertEqual(command[-3:], ['resume', SESSION, '-'])
        runner.cleanup(run, 'Repeated observation, never a second close')
        self.assertEqual(len((self.bin / 'closes.jsonl').read_text().splitlines()), 1)

    def test_cleanup_rechecks_acceptance_after_terminal_observation(self):
        run = self.execute()
        self.verify(run)
        self.assertEqual(runner.reconcile(run)['status'], 'done')
        before = mechanics.load(self.bin / 'agterm.json')
        sid = mechanics.load(run / 'terminal.json')['session_id']
        self.assertIn(sid, [s['id'] for s in before['trees'][WINDOW]['workspaces'][0]['sessions']])
        native = (run / 'session.json').read_bytes()
        observe = runner._agterm_tree

        def change_evidence(*args, **kwargs):
            observed = observe(*args, **kwargs)
            self.artifact.write_text('changed during terminal observation\n')
            return observed

        with patch.object(runner, '_agterm_tree', side_effect=change_evidence) as observed:
            with self.assertRaisesRegex(ValueError, '^cleanup acceptance evidence changed$'):
                runner.cleanup(run, 'Acceptance must remain current through terminal observation')
        observed.assert_called_once()
        self.assertEqual(self.artifact.read_text(), 'changed during terminal observation\n')
        rows = journal.read_events(self.task / 'decision.log')
        self.assertFalse(any(r['kind'] == 'cleanup.intent' or r['event_id'] == 'one:cleanup' for r in rows))
        self.assertFalse((run / 'cleanup-response.json').exists())
        self.assertFalse((self.bin / 'closes.jsonl').exists())
        self.assertEqual(mechanics.load(self.bin / 'agterm.json'), before)
        self.assertEqual((run / 'session.json').read_bytes(), native)

    def test_cleanup_preserves_changed_or_unknown_terminal_and_ownership(self):
        run = self.execute()
        self.verify(run)
        baseline = mechanics.load(self.bin / 'agterm.json')
        for changes in ({'foreground': ['user-program']}, {'hasSplit': True}, {'scratch': True},
                        {'overlay': True}, {'foregroundShell': '', 'commandWait': False}, {'name': 'user-renamed'}):
            state = json.loads(json.dumps(baseline))
            state['trees'][WINDOW]['workspaces'][0]['sessions'][-1].update(changes)
            journal.atomic_json(self.bin / 'agterm.json', state)
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'repurposed'):
                runner.cleanup(run, 'Inspected but repurposed')
        journal.atomic_json(self.bin / 'agterm.json', baseline)
        with patch.object(runner, '_processes_stopped', return_value=False):
            with self.assertRaisesRegex(ValueError, 'stopped worker'):
                runner.cleanup(run, 'Process evidence unavailable')
        observed = mechanics.load(run / 'terminal.json')
        observed['session_id'] = LEAD
        journal.atomic_json(run / 'terminal.json', observed)
        with self.assertRaisesRegex(ValueError, 'acceptance'):
            runner.cleanup(run, 'Ownership was changed')
        self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_cleanup_preserves_question_blocked_invalid_and_live_runs(self):
        for mode in ('question', 'blocked', 'malformed', 'sleep'):
            self.configure(worker=mode, agterm='async' if mode == 'sleep' else 'normal')
            run = self.execute(mode, timeout=.5 if mode == 'sleep' else 3)
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, 'acceptance'):
                runner.cleanup(run, 'Ineligible outcome')
        self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_observed_completed_wait_envelope_allows_owned_cleanup_without_shell_field(self):
        self.configure(hold='wait')
        run = self.execute()
        self.verify(run)
        node = mechanics.load(self.bin / 'agterm.json')['trees'][WINDOW]['workspaces'][0]['sessions'][-1]
        self.assertTrue(node['realized'] and node['commandWait'])
        self.assertNotIn('foreground', node)
        self.assertNotIn('foregroundShell', node)
        self.assertEqual(node['surfaces'][0]['paneID'], mechanics.load(run / 'terminal.json')['pane_id'])
        self.assertEqual(runner.cleanup(run, 'Accepted stopped --wait command; original cwd and primary pane intact')['status'], 'closed')
        self.assertEqual(runner.reconcile(run)['status'], 'done')

    def test_wait_cleanup_preserves_unknown_hold_changed_cwd_and_hidden_or_replaced_panes(self):
        self.configure(hold='wait')
        run = self.execute()
        self.verify(run)
        baseline = mechanics.load(self.bin / 'agterm.json')
        for mode in ('live-program', 'missing-hold', 'changed-cwd', 'missing-cwd',
                     'hidden-split', 'hidden-scratch', 'replaced-primary', 'missing-surfaces', 'overlay'):
            state = json.loads(json.dumps(baseline))
            node = state['trees'][WINDOW]['workspaces'][0]['sessions'][-1]
            if mode == 'live-program': node['foreground'] = ['user-program']
            elif mode == 'missing-hold': node.pop('commandWait')
            elif mode == 'changed-cwd': node['cwd'] = str(self.root)
            elif mode == 'missing-cwd': node.pop('cwd')
            elif mode in ('hidden-split', 'hidden-scratch'):
                node['surfaces'].append({'kind': 'right' if mode == 'hidden-split' else 'scratch',
                                         'paneID': LEAD, 'visible': False})
            elif mode == 'replaced-primary': node['surfaces'][0]['paneID'] = LEAD
            elif mode == 'missing-surfaces': node.pop('surfaces')
            else: node['overlay'] = True
            journal.atomic_json(self.bin / 'agterm.json', state)
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, 'repurposed'):
                runner.cleanup(run, 'Preserve unknown or repurposed held terminal')
        self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_command_wait_metadata_never_substitutes_for_stopped_process_evidence(self):
        self.configure(worker='sleep', agterm='async', hold='wait')
        run = self.execute(timeout=.5)
        state = mechanics.load(self.bin / 'agterm.json')
        node = state['trees'][WINDOW]['workspaces'][0]['sessions'][-1]
        node.pop('foreground')
        self.assertTrue(node['commandWait'])
        self.assertNotIn('foregroundShell', node)
        journal.atomic_json(self.bin / 'agterm.json', state)
        with self.assertRaisesRegex(ValueError, 'independent acceptance'):
            runner.cleanup(run, 'Live worker remains protected despite absent foreground metadata')
        self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_resolved_blocked_terminal_retires_only_after_accepted_exact_continuation(self):
        self.configure(worker='blocked', hold='wait')
        blocked = self.execute('blocked')
        with self.assertRaisesRegex(ValueError, 'resolution evidence'):
            self.prepare('premature', resume_from=blocked)
        runner.event(self.task, 'blocked:resolution', 'resolution', {'evidence': 'Lead checked the resolved blocker'})
        self.configure(worker='done')
        accepted = self.execute('accepted', resume_from=blocked)
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(blocked, 'Unaccepted exact continuation', accepted_continuation=accepted)
        self.verify(accepted)
        state = mechanics.load(self.bin / 'agterm.json')
        state['trees'][WINDOW]['workspaces'][0]['sessions'][1]['status'] = 'blocked'
        journal.atomic_json(self.bin / 'agterm.json', state)
        self.assertEqual(runner.cleanup(blocked, 'Blocker resolved and exact continuation independently accepted',
                                        accepted_continuation=accepted)['status'], 'closed')
        self.assertEqual(runner.reconcile(blocked)['status'], 'blocked')
        self.assertEqual(runner.reconcile(accepted)['status'], 'done')
        self.assertEqual(mechanics.load(blocked / 'session.json'), mechanics.load(accepted / 'session.json'))
        self.assertEqual(len((self.bin / 'closes.jsonl').read_text().splitlines()), 1)

    def test_answered_plan_cleanup_requires_explicit_accepted_exact_continuation(self):
        self.configure(worker='question')
        plan = self.execute('plan')
        with self.assertRaisesRegex(ValueError, 'independent acceptance'):
            runner.cleanup(plan, 'Question still pending')
        build = self.execute('build', resume_from=plan)
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(plan, 'Continuation not independently accepted', accepted_continuation=build)
        self.verify(build)
        with self.assertRaisesRegex(ValueError, 'explicitly answered turn'):
            runner.cleanup(plan, 'Accepted continuation must be named explicitly')
        before = mechanics.load(self.bin / 'agterm.json')
        plan_id = mechanics.load(plan / 'terminal.json')['session_id']
        build_id = mechanics.load(build / 'terminal.json')['session_id']
        self.assertEqual(runner.cleanup(plan, 'Lead accepted the exact build; old plan terminal no longer needed',
                                        accepted_continuation=build)['status'], 'closed')
        remaining = mechanics.load(self.bin / 'agterm.json')['trees'][WINDOW]['workspaces'][0]['sessions']
        self.assertEqual(remaining, [s for s in before['trees'][WINDOW]['workspaces'][0]['sessions'] if s['id'] != plan_id])
        self.assertIn(build_id, {s['id'] for s in remaining})
        self.assertEqual(runner.reconcile(plan)['status'], 'needs_input')
        self.assertEqual(runner.reconcile(plan)['cleanup']['status'], 'closed')
        self.assertEqual(runner.reconcile(build)['status'], 'done')
        intent = next(r for r in journal.read_events(self.task / 'decision.log') if r['event_id'] == 'plan:cleanup')
        self.assertEqual(intent['data']['acceptance_run'], str(build))
        self.assertEqual(intent['data']['verification_sha256'], mechanics.sha256(build / 'verification.json'))
        self.assertEqual(set(intent['data']['source']), {str(plan), str(build)})
        runner.cleanup(plan, 'Observe existing close without another request')
        self.assertEqual(len((self.bin / 'closes.jsonl').read_text().splitlines()), 1)
        self.assertEqual(mechanics.load(plan / 'session.json'), mechanics.load(build / 'session.json'))

    def test_answered_turn_chain_requires_every_intermediate_turn_reconciled(self):
        self.configure(worker='question')
        plan = self.execute('plan')
        self.configure(repeat_question=True)
        waiting = self.execute('checks-pending', resume_from=plan)
        self.assertEqual(runner.reconcile(waiting)['status'], 'needs_input')
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(plan, 'Controller evidence still pending', accepted_continuation=waiting)
        self.configure(repeat_question=False)
        accepted = self.execute('accepted', resume_from=waiting)
        self.verify(accepted)
        self.assertEqual(runner.cleanup(plan, 'All answers reconciled by accepted endpoint',
                                        accepted_continuation=accepted)['status'], 'closed')
        self.assertEqual(runner.cleanup(waiting, 'Controller answer consumed; old turn retired',
                                        accepted_continuation=accepted)['status'], 'closed')
        self.assertEqual(runner.reconcile(accepted)['status'], 'done')
        self.assertEqual(len((self.bin / 'closes.jsonl').read_text().splitlines()), 2)

    def test_answered_cleanup_rejects_unrelated_blocked_invalid_uncertain_and_stale_evidence(self):
        self.configure(worker='question')
        plan = self.execute('plan')
        self.configure(worker='done')
        unrelated = self.execute('unrelated')
        self.verify(unrelated)
        with self.assertRaisesRegex(ValueError, 'not an exact continuation'):
            runner.cleanup(plan, 'Same native fixture ID does not establish continuation', accepted_continuation=unrelated)
        prepared = self.prepare('not-launched')
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(plan, 'No durable continuation outcome', accepted_continuation=prepared)
        self.configure(worker='blocked')
        blocked = self.execute('blocked', resume_from=plan)
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(plan, 'Blocked answer is not accepted', accepted_continuation=blocked)
        runner.event(self.task, 'blocked:resolution', 'resolution', {'evidence': 'Fixture cause resolved'})
        self.configure(worker='done')
        accepted = self.execute('after-blocked', resume_from=blocked)
        self.verify(accepted)
        rows = [r for r in journal.read_events(self.task / 'decision.log') if r['event_id'] != 'blocked:resolution']
        (self.task / 'decision.log').write_text(''.join(json.dumps(r)+'\n' for r in rows))
        with self.assertRaisesRegex(ValueError, 'recorded resolution evidence'):
            runner.cleanup(plan, 'Unresolved blocked intermediate turn remains protected', accepted_continuation=accepted)
        self.artifact.write_text('changed after acceptance\n')
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(blocked, 'Blocked parent remains protected', accepted_continuation=accepted)
        (accepted / 'result.json').write_text('{bad')
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(plan, 'Invalid continuation is not accepted', accepted_continuation=accepted)
        self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_answered_cleanup_preserves_stale_acceptance_repurposed_terminal_and_ownership(self):
        self.configure(worker='question')
        plan = self.execute('plan')
        accepted = self.execute('build', resume_from=plan)
        self.verify(accepted)
        baseline = self.artifact.read_text()
        self.artifact.write_text('stale evidence\n')
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(plan, 'Stale endpoint', accepted_continuation=accepted)
        self.artifact.write_text(baseline)
        state = mechanics.load(self.bin / 'agterm.json')
        plan_node = state['trees'][WINDOW]['workspaces'][0]['sessions'][1]
        plan_node['foreground'] = ['user-program']
        journal.atomic_json(self.bin / 'agterm.json', state)
        with self.assertRaisesRegex(ValueError, 'repurposed'):
            runner.cleanup(plan, 'Repurposed answered plan', accepted_continuation=accepted)
        plan_node.pop('foreground')
        journal.atomic_json(self.bin / 'agterm.json', state)
        with patch.object(runner, '_processes_stopped', return_value=False):
            with self.assertRaisesRegex(ValueError, 'stopped processes'):
                runner.cleanup(plan, 'Process ownership unknown', accepted_continuation=accepted)
        terminal = mechanics.load(plan / 'terminal.json')
        terminal['session_id'] = LEAD
        journal.atomic_json(plan / 'terminal.json', terminal)
        with self.assertRaisesRegex(ValueError, 'ownership evidence changed'):
            runner.cleanup(plan, 'Changed parent ownership', accepted_continuation=accepted)
        self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_answered_cleanup_requires_matching_identity_and_durable_continuation_intent(self):
        self.configure(worker='question')
        plan = self.execute('plan')
        accepted = self.execute('build', resume_from=plan)
        self.verify(accepted)
        original = (accepted / 'spec.json').read_bytes()
        for key in ('task', 'cwd', 'step_id', 'harness', 'artifact_root'):
            changed = json.loads(original)
            changed[key] = 'different'
            journal.atomic_json(accepted / 'spec.json', changed)
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'identity mismatch'):
                runner.cleanup(plan, 'Mismatched identity', accepted_continuation=accepted)
            (accepted / 'spec.json').write_bytes(original)
        native = (accepted / 'session.json').read_bytes()
        journal.atomic_json(accepted / 'session.json', {'session_id': LEAD})
        with self.assertRaisesRegex(ValueError, 'accepted done continuation'):
            runner.cleanup(plan, 'Mismatched native session', accepted_continuation=accepted)
        (accepted / 'session.json').write_bytes(native)
        log = (self.task / 'decision.log').read_bytes()
        rows = journal.read_events(self.task / 'decision.log')
        for row in rows:
            if row['event_id'] == 'plan:continuation':
                row['data']['run'] = str(plan)
        (self.task / 'decision.log').write_text(''.join(json.dumps(r)+'\n' for r in rows))
        with self.assertRaisesRegex(ValueError, 'continuation intent mismatch'):
            runner.cleanup(plan, 'Mismatched consumed question', accepted_continuation=accepted)
        (self.task / 'decision.log').write_bytes(log)
        journal.recover_state(self.task / 'decision.log')
        foreign = self.root / 'foreign-task/research/dev-lead/runs/foreign'
        foreign.mkdir(parents=True)
        (foreign / 'spec.json').write_bytes(original)
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            runner.cleanup(plan, 'Foreign task', accepted_continuation=foreign)
        self.assertEqual(list(foreign.iterdir()), [foreign / 'spec.json'])
        self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_lost_close_reply_observed_without_replaying_and_undo_preserved(self):
        run = self.execute()
        self.verify(run)
        before = mechanics.load(self.bin / 'agterm.json')
        self.configure(close='lost-after')
        self.assertEqual(runner.cleanup(run, 'Accepted and no longer needed', timeout=.1)['status'], 'closed')
        self.assertFalse(mechanics.load(run / 'cleanup-response.json')['valid_reply'])
        journal.atomic_json(self.bin / 'agterm.json', before)
        self.assertEqual(runner.cleanup(run, 'Reconcile undo')['status'], 'reappeared')
        self.assertEqual(len((self.bin / 'closes.jsonl').read_text().splitlines()), 1)

    def test_lost_close_before_effect_and_denied_observation_stay_uncertain(self):
        run = self.execute()
        self.verify(run)
        self.configure(close='lost-before')
        self.assertEqual(runner.cleanup(run, 'Accepted', timeout=.1)['status'], 'uncertain')
        self.configure(ipc_error='Operation not permitted')
        state = runner.cleanup(run, 'Observation denied')
        self.assertEqual(state['status'], 'uncertain')
        self.assertIn('Operation not permitted', state['reason'])
        self.assertEqual(len((self.bin / 'closes.jsonl').read_text().splitlines()), 1)

    def test_close_reply_accepts_only_exact_id_or_one_affected_session(self):
        for result in ({'id': LEAD}, {'affected': 1}):
            runner._close_reply({'exit_code': 0, 'stdout': json.dumps({'ok': True, 'result': result})}, LEAD)
        for result in ({'id': SESSION}, {'affected': 0}, {'affected': 2}, {'affected': True},
                       {'count': 1}, {'id': LEAD, 'affected': 1}):
            with self.subTest(result=result), self.assertRaises(ValueError):
                runner._close_reply({'exit_code': 0, 'stdout': json.dumps({'ok': True, 'result': result})}, LEAD)
        run = self.execute()
        self.verify(run)
        self.configure(close='id')
        self.assertEqual(runner.cleanup(run, 'Accepted')['status'], 'closed')
        self.assertTrue(mechanics.load(run / 'cleanup-response.json')['valid_reply'])

    def test_close_event_before_state_failure_is_reconciled_once(self):
        run = self.execute()
        self.verify(run)
        original = runner.atomic_json
        def interrupt(path, value):
            if Path(path).name == 'cleanup-response.json':
                raise OSError('lost local response persistence')
            return original(path, value)
        with patch.object(runner, 'atomic_json', side_effect=interrupt):
            with self.assertRaises(OSError):
                runner.cleanup(run, 'Accepted')
        self.assertEqual(runner.reconcile(run)['cleanup']['status'], 'closed')
        self.assertEqual(len((self.bin / 'closes.jsonl').read_text().splitlines()), 1)

    def test_lost_launch_can_recover_owned_terminal_without_label_guessing(self):
        self.configure(agterm='lost', worker='slow')
        run = self.prepare()
        self.assertTrue(runner.launch(run, timeout=.2)['uncertain'])
        self.wait_for(lambda: (run / 'execution/exit.json').exists())
        (run / 'launch.json').unlink()  # Controller died before persisting its lost reply.
        self.verify(run)
        # The fake app lost its reply before replacing foreground with a shell.
        state = mechanics.load(self.bin / 'agterm.json')
        node = state['trees'][WINDOW]['workspaces'][0]['sessions'][-1]
        node.pop('foreground'); node['foregroundShell'] = 'zsh'
        journal.atomic_json(self.bin / 'agterm.json', state)
        self.assertEqual(runner.cleanup(run, 'Launch independently reconciled and accepted')['status'], 'closed')

    def test_legacy_runs_reconcile_and_resume_without_fabricating_ownership(self):
        def legacy(run):
            value = mechanics.load(run / 'spec.json')
            value.pop('agterm_identity'); value.pop('terminal_name')
            journal.atomic_json(run / 'spec.json', value)
            rows = journal.read_events(self.task / 'decision.log')
            for row in rows:
                if row['event_id'] == value['run_id'] + ':prepared':
                    row['data']['spec_sha256'] = mechanics.sha256(run / 'spec.json')
            (self.task / 'decision.log').write_text(''.join(json.dumps(r)+'\n' for r in rows))
            journal.recover_state(self.task / 'decision.log')
        prepared = self.prepare('legacy-prepared')
        legacy(prepared)
        with self.assertRaisesRegex(ValueError, 'legacy run'):
            runner.launch(prepared)
        self.configure(worker='question')
        question = self.execute('legacy-question')
        legacy(question)
        before = (question / 'spec.json').read_bytes()
        self.assertEqual(runner.reconcile(question)['status'], 'needs_input')
        resumed = self.execute('legacy-answer', resume_from=question)
        self.assertEqual(mechanics.load(resumed / 'spec.json')['resume_session'], SESSION)
        self.assertEqual((question / 'spec.json').read_bytes(), before)
        self.assertIn('agterm_identity', mechanics.load(resumed / 'spec.json'))
        legacy(resumed)
        self.verify(resumed)
        with self.assertRaisesRegex(ValueError, 'owned terminal evidence'):
            runner.cleanup(resumed, 'Legacy ownership is unproven')

    def test_launch_rechecks_name_collision_and_realization(self):
        run = self.prepare()
        state = mechanics.load(self.bin / 'agterm.json')
        node = {'id': SESSION, 'name': mechanics.load(run / 'spec.json')['terminal_name'], 'realized': True}
        state['trees'][WINDOW]['workspaces'][0]['sessions'].append(node)
        journal.atomic_json(self.bin / 'agterm.json', state)
        with self.assertRaisesRegex(ValueError, 'now occupied'):
            runner.launch(run)
        self.assertFalse((run / 'launch.json').exists())
        state['trees'][WINDOW]['workspaces'][0]['sessions'].pop()
        journal.atomic_json(self.bin / 'agterm.json', state)
        self.configure(unrealized=True)
        self.assertTrue(runner.launch(run)['uncertain'])

    def test_cleanup_intent_before_request_is_not_replayed_after_interruption(self):
        run = self.execute()
        self.verify(run)
        ipc = runner._ipc
        def interrupt(command, timeout):
            if command[1:3] == ['session', 'close']:
                raise RuntimeError('interrupted before IPC observation')
            return ipc(command, timeout)
        with patch.object(runner, '_ipc', side_effect=interrupt), self.assertRaises(RuntimeError):
            runner.cleanup(run, 'Accepted')
        self.assertEqual(runner.cleanup(run, 'Inspect existing intent')['status'], 'uncertain')
        self.assertFalse((self.bin / 'closes.jsonl').exists())

    def test_public_cli_help(self):
        for module in ('inventory', 'runner', 'outcome', 'journal', 'commit'):
            result = subprocess.run([sys.executable, str(SCRIPTS / (module + '.py')), '--help'], capture_output=True, timeout=3)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(b'usage:', result.stdout)


if __name__ == '__main__':
    unittest.main()
