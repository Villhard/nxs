"""Native CLI boundaries. Shared workflow state belongs to runner, not a client."""
import json
import re
import shutil
import subprocess
import uuid
from pathlib import Path

from journal import atomic_json

NAMES = ('codex', 'claude', 'opencode')


def session_id(harness, value):
    if harness not in NAMES or not isinstance(value, str):
        raise ValueError('unknown harness or invalid session ID')
    if harness == 'opencode':
        if not re.fullmatch(r'ses[A-Za-z0-9_-]+', value):
            raise ValueError('invalid OpenCode session ID')
    else:
        uuid.UUID(value)
    return value


def api(executable, operation, cwd, timeout=30, params=()):
    command = [executable, 'api', operation, '--param', 'location[directory]=' + str(cwd)]
    for key, value in params:
        command += ['--param', key + '=' + value]
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise ValueError('OpenCode API failed: ' + result.stderr.strip())
    value = json.loads(result.stdout)
    if not isinstance(value, dict) or '_tag' in value or 'data' not in value:
        raise ValueError('invalid OpenCode API response: ' + str(value.get('_tag') if isinstance(value, dict) else type(value)))
    location = value.get('location', {}).get('directory')
    if location is not None and Path(location).resolve() != Path(cwd).resolve():
        raise ValueError('OpenCode API returned a different cwd')
    return value['data']


def check_resume(harness, executable, session, cwd, timeout):
    session_id(harness, session)
    if harness == 'opencode':
        # The CLI creates an unknown --session ID. Never let that masquerade as resume.
        value = api(executable, 'session.get', cwd, timeout, [('sessionID', session)])
        if value.get('id') != session or Path(value['location']['directory']).resolve() != Path(cwd).resolve():
            raise ValueError('saved OpenCode session is missing or belongs to a different cwd')


def command(harness, executable, cwd, model, effort, sandbox, run, resume=None):
    if harness not in NAMES:
        raise ValueError('unsupported harness')
    executable = shutil.which(executable) or executable
    if resume:
        session_id(harness, resume)
    run = Path(run)
    if harness == 'codex':
        args = [executable, 'exec', '--ignore-user-config', '-C', str(cwd), '-m', model,
                '-c', 'model_reasoning_effort=' + json.dumps(effort), '-c', 'approval_policy="never"',
                '-s', sandbox, '--json', '--output-schema', str(run / 'schema.json'),
                '-o', str(run / 'result.json')]
        args += ['resume', resume, '-'] if resume else ['-']
        return args
    if harness == 'claude':
        args = [executable, '-p', '--output-format', 'stream-json', '--verbose', '--model', model,
                '--json-schema', (run / 'schema.json').read_text(), '--permission-mode',
                'dontAsk' if sandbox == 'read-only' else 'acceptEdits']
        if effort is not None:
            args += ['--effort', effort]
        # No permission bypass or broad approval grants. Existing native allow rules remain in force.
        args += ['--tools', 'Read,Glob,Grep,Bash' if sandbox == 'read-only' else 'Read,Glob,Grep,Edit,Write,Bash']
        if resume:
            args += ['--resume', resume]
    else:
        args = [executable, 'run', '--standalone', '--format', 'json', '--agent', 'build', '--model',
                model + ('#' + effort if effort is not None else '')]
        if resume:
            args += ['--session', resume]
    if sandbox == 'read-only':
        guard = shutil.which('sandbox-exec')
        if not guard:
            raise ValueError('read-only Claude/OpenCode workers require macOS sandbox-exec')
        # Restrict source writes without blocking the CLI's own session/cache storage.
        profile = '(version 1)(allow default)(deny file-write* (subpath ' + json.dumps(str(Path(cwd).resolve())) + '))'
        args = [guard, '-p', profile, *args]
    return args


def observed_session(harness, row):
    if harness == 'codex':
        value = row.get('thread_id') if row.get('type') == 'thread.started' else None
    elif harness == 'claude':
        value = row.get('session_id') if row.get('type') in ('system', 'result') else None
    else:
        value = row.get('sessionID')
    return session_id(harness, value) if value else None


def completed(harness, events):
    if harness == 'codex':
        return any(e.get('type') == 'turn.completed' for e in events)
    if harness == 'claude':
        results = [e for e in events if e.get('type') == 'result']
        return (len(results) == 1 and results[0].get('subtype') == 'success'
                and results[0].get('is_error') is False)
    finishes = [e for e in events if e.get('type') == 'step_finish']
    return (bool(finishes) and finishes[-1].get('part', {}).get('reason') == 'stop'
            and not any(e.get('type') == 'error' for e in events))


def extract_outcome(harness, events):
    """Extract only a successful native final result, never prose or a tool step."""
    if not all(isinstance(e, dict) for e in events) or not completed(harness, events):
        raise ValueError('native turn did not finish successfully')
    if harness == 'claude':
        result = next(e for e in events if e.get('type') == 'result')
        if 'structured_output' not in result:
            raise ValueError('Claude result has no structured_output')
        value = result['structured_output']
    else:
        finish = next(e for e in reversed(events) if e.get('type') == 'step_finish' and e.get('part', {}).get('reason') == 'stop')
        message = finish['part']['messageID']
        texts = [e['part']['text'] for e in events if e.get('type') == 'text' and e.get('part', {}).get('messageID') == message]
        if not texts:
            raise ValueError('OpenCode completed without final text')
        value = json.loads(''.join(texts))
    return value


def save_outcome(harness, run):
    """Keep native events intact; derive envelopes for clients without -o."""
    if harness == 'codex':
        return
    run = Path(run)
    raw = (run / 'execution/stdout').read_bytes()
    if not raw.endswith(b'\n'):
        raise ValueError('incomplete native event stream')
    atomic_json(run / 'result.json', extract_outcome(harness, [json.loads(line) for line in raw.splitlines()]))
