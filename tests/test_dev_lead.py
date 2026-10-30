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
FAKE_CODEX = r'''#!/usr/bin/env python3
import json, pathlib, sys, time
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
    result = pathlib.Path(args[args.index('-o') + 1])
    status = 'blocked' if mode == 'blocked' else ('needs_input' if mode == 'question' and 'resume' not in args else 'done')
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
import json, pathlib, shlex, subprocess, sys, time
root = pathlib.Path(__file__).parent
config = json.loads((root / 'fixture.json').read_text())
args = sys.argv[1:]
assert args[:2] == ['session', 'new']
assert '--wait' in args and '--cwd' in args
command = shlex.split(args[args.index('--command') + 1])
with (root / 'launches.jsonl').open('a') as f:
    f.write(json.dumps(command) + '\n')
with (root / 'visible.log').open('ab') as f:
    child = subprocess.Popen(command, stdout=f, stderr=f, start_new_session=True)
(root / 'worker-pid').write_text(str(child.pid))
if config.get('agterm') == 'lost':
    time.sleep(10)
elif config.get('agterm') != 'async':
    child.wait(timeout=10)
print(json.dumps({'ok': True, 'result': {'id': 'visible-fixture'}, 'pid': child.pid}))
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
        self.catalog = inventory.discover([self.repo], str(self.codex), 3)
        self.assertEqual(self.catalog['models']['status'], 'ok')

    def tearDown(self):
        # Interrupted workers have independent process groups; fixtures own their cleanup.
        for file in self.task.glob('research/dev-lead/runs/*/execution/process.json'):
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
        result = runner.launch(run, str(self.bin / 'missing-agterm'))
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
        runner.launch(run, str(self.bin / 'missing-agterm'))
        next_run = self.prepare('next')
        with self.assertRaisesRegex(ValueError, 'no durable exit'):
            runner.launch(next_run, str(self.agterm))
        with self.assertRaisesRegex(ValueError, 'confirmed absent'):
            runner.acknowledge_stopped(run, 'Cannot prove a lost launch did not occur')
        self.assertFalse((next_run / 'launch.json').exists())

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

    def test_public_cli_help(self):
        for module in ('inventory', 'runner', 'outcome', 'journal', 'commit'):
            result = subprocess.run([sys.executable, str(SCRIPTS / (module + '.py')), '--help'], capture_output=True, timeout=3)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(b'usage:', result.stdout)


if __name__ == '__main__':
    unittest.main()
