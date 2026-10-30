"""Native adapter protocol tests. Claude fixtures are not live CLI evidence."""
import json
import os
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/dev-lead/scripts'))
import harness
import inventory
import runner
import test_dev_lead as fixtures
SESSION = fixtures.SESSION


class Protocols(unittest.TestCase):
    def test_native_ids(self):
        for client in ('codex', 'claude'):
            self.assertEqual(harness.session_id(client, SESSION), SESSION)
            with self.assertRaises(ValueError):
                harness.session_id(client, 'ses_fixture')
        self.assertEqual(harness.session_id('opencode', 'ses_fixture'), 'ses_fixture')
        with self.assertRaises(ValueError):
            harness.session_id('opencode', '../session')

    def test_claude_structured_completion(self):
        events = [{'type': 'result', 'subtype': 'success', 'is_error': False,
                   'session_id': SESSION, 'structured_output': {'status': 'needs_input'}}]
        self.assertEqual(harness.extract_outcome('claude', events), {'status': 'needs_input'})
        for change in ({'is_error': True}, {'subtype': 'error_max_turns'}, {'structured_output': None}):
            changed = [{**events[0], **change}]
            if 'structured_output' in change:
                self.assertIsNone(harness.extract_outcome('claude', changed))  # Envelope validator rejects null.
            else:
                with self.assertRaises(ValueError):
                    harness.extract_outcome('claude', changed)
        del events[0]['structured_output']
        with self.assertRaises(ValueError):
            harness.extract_outcome('claude', events)

    def test_opencode_final_message_only(self):
        events = [{'type': 'text', 'part': {'messageID': 'tool', 'text': 'ignore'}},
                  {'type': 'step_finish', 'part': {'messageID': 'tool', 'reason': 'tool-calls'}},
                  {'type': 'text', 'part': {'messageID': 'final', 'text': '{"status":'}},
                  {'type': 'text', 'part': {'messageID': 'final', 'text': '"done"}'}},
                  {'type': 'step_finish', 'part': {'messageID': 'final', 'reason': 'stop'}}]
        self.assertEqual(harness.extract_outcome('opencode', events), {'status': 'done'})
        with self.assertRaises(ValueError):
            harness.extract_outcome('opencode', events[:2])
        events[2]['part']['text'] = '```json\n'
        with self.assertRaises(ValueError):
            harness.extract_outcome('opencode', events)

    def test_native_commands_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'schema.json').write_text('{}')
            for client in ('claude', 'opencode'):
                with patch('harness.shutil.which', side_effect=lambda x: '/bin/' + x):
                    cmd = harness.command(client, client, root, 'fixture', None, 'read-only', root, SESSION if client == 'claude' else 'ses_fixture')
                self.assertEqual(cmd[0], '/bin/sandbox-exec')
                self.assertIn(str(root.resolve()), cmd[2])
                self.assertFalse(any('bypass' in s or 'dangerously' in s for s in cmd))
                if client == 'claude':
                    self.assertIn('dontAsk', cmd); self.assertNotIn('--effort', cmd)
                else:
                    self.assertIn('--standalone', cmd); self.assertIn('--session', cmd)
                with patch('harness.shutil.which', return_value=None), self.assertRaises(ValueError):
                    harness.command(client, client, root, 'fixture', None, 'read-only', root)

    def test_resume_requires_existing_opencode_session(self):
        with patch('harness.api', return_value={'id': 'ses_other', 'location': {'directory': '/tmp'}}), self.assertRaises(ValueError):
            harness.check_resume('opencode', 'opencode', 'ses_fixture', '/tmp', 1)

    def test_missing_cli_is_discovery_failure(self):
        for client in ('claude', 'opencode'):
            value = inventory.discover([Path.cwd()], harness=client, executable='/nonexistent/cli', timeout=1)
            self.assertEqual(inventory.skill_status(value, Path.cwd(), 'dev-lead')['status'], 'discovery_failed')

    def test_claude_control_transport(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve(); skill = root / '.claude/skills/fixture/SKILL.md'; skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: fixture\n---\n')
            cli = root / 'claude'; cli.write_text('''#!/usr/bin/env python3
import json,sys
for line in sys.stdin:
 row=json.loads(line)
 assert row['type']=='control_request' and row['request']['subtype']=='initialize'
 print(json.dumps({'type':'control_response','response':{'subtype':'success','request_id':row['request_id'],'response':{'models':[{'value':'fixture-model'}],'commands':[{'name':'fixture'}]}}}),flush=True)
'''); cli.chmod(0o755)
            with patch.dict(os.environ, {'CLAUDE_CONFIG_DIR': str(root / 'empty')}):
                value = inventory.discover([root], harness='claude', executable=str(cli), timeout=3, skill_roots=[root / '.claude/skills'])
            self.assertEqual(value['models']['status'], 'ok')
            inventory.validate_model(value, 'fixture-model', None)
            with self.assertRaises(ValueError):
                inventory.validate_model(value, 'fixture-model', 'high')
            self.assertEqual(inventory.skill_status(value, root, 'fixture')['status'], 'context')
            self.assertEqual(value['skills'][str(root)]['skills'][0]['path'], str(skill))
            metadata = {'commands': [{'name': 'fixture'}]}
            with patch.dict(os.environ, {'CLAUDE_CONFIG_DIR': str(root / 'empty')}):
                native, _ = inventory._claude_skills(root, metadata, [])
                self.assertFalse(native[0]['enabled'])
                self.assertEqual(native[0]['visibility'], 'unconfirmed')
                candidate = root / 'checkout/fixture/SKILL.md'
                candidate.parent.mkdir(parents=True)
                candidate.write_text('---\nname: fixture\n---\nCandidate content differs from installed.\n')
                selected, _ = inventory._claude_skills(root, metadata, [candidate.parent.parent])
            candidate_row = next(x for x in selected if x['path'] == str(candidate))
            self.assertEqual(candidate_row['visibility'], 'context')
            self.assertNotIn('registered', candidate_row['visibility'])
            self.assertTrue(candidate_row['enabled'])


    @unittest.skipUnless(sys.platform == 'darwin', 'macOS source-write guard')
    def test_readonly_guard_denies_actual_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve(); (root / 'schema.json').write_text('{}')
            source = root / 'source.py'; source.write_text('baseline\n')
            guard = harness.command('claude', 'claude', root, 'fixture', None, 'read-only', root)[:3]
            self.assertIn('(deny file-write*', guard[2])
            write = f'from pathlib import Path; print("started", flush=True); Path({str(source)!r}).write_text("changed")'
            denied = subprocess.run([*guard, sys.executable, '-c', write], capture_output=True, text=True, timeout=5)
            self.assertIn('started', denied.stdout)  # The sandbox ran Python before refusing the write.
            self.assertNotEqual(denied.returncode, 0)
            self.assertEqual(source.read_text(), 'baseline\n')
            subprocess.run([sys.executable, '-c', write], check=True, capture_output=True, timeout=5)
            self.assertEqual(source.read_text(), 'changed')


class NativeRuns(unittest.TestCase):
    setUp = fixtures.Helpers.setUp
    tearDown = fixtures.Helpers.tearDown
    git = fixtures.Helpers.git
    configure = fixtures.Helpers.configure
    prepare = fixtures.Helpers.prepare
    execute = fixtures.Helpers.execute
    def test_native_question_resume_and_tamper(self):
        cli = self.bin / 'claude-fixture'
        cli.write_text('''#!/usr/bin/env python3
import json,sys,pathlib
text=sys.stdin.read();args=sys.argv[1:]
resume='--resume' in args
if resume: assert args[args.index('--resume')+1]=='12345678-1234-4234-8234-123456789abc'
v={'status':'done' if resume else 'needs_input','step_id':'step-1','summary':'Fixture','artifacts':[],'evidence':[],'question':'' if resume else 'Approve ticket?','reason':''}
print(json.dumps({'type':'system','subtype':'init','session_id':'12345678-1234-4234-8234-123456789abc'}))
print(json.dumps({'type':'result','subtype':'success','is_error':False,'session_id':'12345678-1234-4234-8234-123456789abc','structured_output':v}))
'''); cli.chmod(0o755)
        catalog = {**self.catalog, 'harness': 'claude'}
        kwargs = dict(harness='claude', executable=str(cli), inventory=catalog, skill_paths=[])
        first = self.execute('native-question', **kwargs)
        self.assertEqual(runner.reconcile(first)['status'], 'needs_input')
        with self.assertRaises(ValueError):
            self.prepare('cross-client', resume_from=first)
        second = self.execute('native-answer', resume_from=first, **kwargs)
        self.assertEqual(runner.reconcile(second)['status'], 'unverified')
        path = second / 'result.json'; value = json.loads(path.read_text()); value['summary'] = 'forged'; path.write_text(json.dumps(value))
        state = runner.reconcile(second)
        self.assertEqual(state['status'], 'invalid'); self.assertIn('native final output', state['reason'])

    def test_explicit_candidate_is_delivered_without_claiming_native_registration(self):
        catalog = json.loads(json.dumps(self.catalog)); catalog['harness'] = 'claude'
        skill = catalog['skills'][str(self.repo)]['skills'][0]
        skill['visibility'] = 'context'
        run = self.prepare('candidate-context', harness='claude', executable='claude', inventory=catalog)
        packet = json.loads((run / 'input.json').read_text())['prompt']
        self.assertIn('Fixture skill', packet)
        self.assertIn('Base directory: ' + str(self.bin / 'skill'), packet)
        self.assertEqual(json.loads((run / 'spec.json').read_text())['skills'][0]['delivery'], 'context')

FAKE_OPENCODE = r'''#!/usr/bin/env python3
import json,sys,os,pathlib,http.server,urllib.parse
root=pathlib.Path(__file__).parent
args=sys.argv[1:]
if args[0]=='serve':
 class API(http.server.BaseHTTPRequestHandler):
  polls=0
  def do_GET(self):
   path=urllib.parse.urlsplit(self.path)
   cwd=urllib.parse.parse_qs(path.query)['location[directory]'][0]
   if path.path=='/api/plugin':
    API.polls+=1
    mode=json.loads((root/'fixture.json').read_text()).get('plugin_state','delayed')
    status='failed' if mode=='failed' else 'active'
    data=[] if mode=='waiting' or API.polls<2 else [{'id':k,'state':{'status':status}} for k in ['opencode.skill','opencode.tool.skill','opencode.config.skill']]
   elif path.path=='/api/model':
    assert API.polls>=2, 'catalog read before plugin readiness'
    data=[{'providerID':'fixture','id':'model','enabled':True,'variants':[{'id':'low'}]}]
   elif path.path=='/api/agent':
    data=[{'id':'build','permissions':[{'action':'skill','resource':'*','effect':'allow'},{'action':'skill','resource':'disabled','effect':'deny'}]}]
   else:
    data=[{'id':k,'name':k,'path':str(root/'skill/SKILL.md'),'content':'x'*300000} for k in ['fixture','disabled']]
   raw=json.dumps({'location':{'directory':cwd},'data':data}).encode()
   self.send_response(200);self.end_headers();self.wfile.write(raw)
  def log_message(self,*args): pass
 server=http.server.HTTPServer(('127.0.0.1',0),API)
 print('server listening on http://127.0.0.1:'+str(server.server_port),flush=True)
 server.serve_forever()
elif args[0]=='api':
 assert args[1]=='session.get'
 print(json.dumps({'data':{'id':'ses_fixture','location':{'directory':os.getcwd()}}}))
else:
 assert '--standalone' in args and '--format' in args and '--agent' in args
 prompt=sys.stdin.read();assert 'schema' in prompt
 resume='--session' in args
 if resume: assert args[args.index('--session')+1]=='ses_fixture'
 value={'status':'done' if resume else 'needs_input','step_id':'step-1','summary':'Fixture','artifacts':[],'evidence':[],'question':'' if resume else 'Approve ticket?','reason':''}
 for row in [{'type':'text','part':{'messageID':'final','text':json.dumps(value)}},{'type':'step_finish','part':{'messageID':'final','reason':'stop'}}]:
  print(json.dumps({**row,'sessionID':'ses_fixture'}))
'''


class OpenCodeRuns(unittest.TestCase):
    setUp = fixtures.Helpers.setUp
    tearDown = fixtures.Helpers.tearDown
    git = fixtures.Helpers.git
    configure = fixtures.Helpers.configure
    prepare = fixtures.Helpers.prepare
    execute = fixtures.Helpers.execute

    def test_inventory_and_exact_resume(self):
        cli = self.bin / 'opencode-fixture'; cli.write_text(FAKE_OPENCODE); cli.chmod(0o755)
        catalog = inventory.discover([self.repo], harness='opencode', executable=str(cli), timeout=5)
        self.assertEqual(catalog['models']['status'], 'ok', catalog)
        self.assertEqual(inventory.skill_status(catalog, self.repo, 'disabled')['status'], 'disabled')
        self.assertEqual(inventory.skill_status(catalog, self.repo, 'fixture')['status'], 'enabled')
        self.assertEqual(inventory.skill_status(catalog, self.repo, 'absent')['status'], 'missing')
        kwargs = dict(harness='opencode', executable=str(cli), inventory=catalog, model='fixture/model', effort='low', skill_paths=[])
        first = self.execute('oc-question', **kwargs)
        self.assertEqual(runner.reconcile(first)['status'], 'needs_input')
        second = self.execute('oc-answer', resume_from=first, **kwargs)
        self.assertEqual(runner.reconcile(second)['status'], 'unverified')
        with self.assertRaises(ValueError):
            self.prepare('invalid-effort', **{**kwargs, 'effort': 'high'})

    def test_failed_and_unsettled_plugins(self):
        cli = self.bin / 'opencode-fixture'; cli.write_text(FAKE_OPENCODE); cli.chmod(0o755)
        for state, error in [('failed', 'plugin failed'), ('waiting', 'timeout')]:
            with self.subTest(state=state):
                self.configure(plugin_state=state)
                value = inventory.discover([self.repo], harness='opencode', executable=str(cli), timeout=.8)
                self.assertEqual(inventory.skill_status(value, self.repo, 'dev-lead')['status'], 'discovery_failed')
                self.assertIn(error, value['models']['error'].lower())
