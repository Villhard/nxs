"""Discover native skills, exact sources and supported model efforts."""
import argparse
import contextlib
import base64
import urllib.parse
import urllib.request
import hashlib
import secrets
import fnmatch
import re
import json
import os
from pathlib import Path
import selectors
import subprocess
import time

import harness as native
from journal import atomic_json
from mechanics import sha256, stop


class AppServer:
    def __init__(self, codex='codex', timeout=30):
        self.command = [codex, 'app-server', '--stdio']
        self.deadline = time.monotonic() + timeout
        self.process = None
        self.selector = selectors.DefaultSelector()
        self.buffer = b''
        self.sequence = 0

    def __enter__(self):
        try:
            self.process = subprocess.Popen(self.command, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            start_new_session=True, cwd=getattr(self, 'cwd', None))
            self.selector.register(self.process.stdout, selectors.EVENT_READ, 'stdout')
            self.selector.register(self.process.stderr, selectors.EVENT_READ, 'stderr')
            self.initial = self.call('initialize', {'clientInfo': {'name': 'nxs-dev-lead', 'version': '1'}})
            self.send({'method': 'initialized'})
            return self
        except BaseException:
            self.close()
            raise

    def send(self, message):
        self.process.stdin.write((json.dumps(message) + '\n').encode())
        self.process.stdin.flush()

    def call(self, method, params):
        self.sequence += 1
        request_id = self.sequence
        self.send({'id': request_id, 'method': method, 'params': params})
        while True:
            while b'\n' in self.buffer:
                line, self.buffer = self.buffer.split(b'\n', 1)
                row = self.message(json.loads(line))
                if not isinstance(row, dict):
                    raise ValueError('malformed app-server response')
                if row.get('id') == request_id:
                    if 'error' in row:
                        raise ValueError(method + ': ' + json.dumps(row['error']))
                    if 'result' not in row:
                        raise ValueError('missing RPC result')
                    return row['result']
            remaining = self.deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('app-server timeout: ' + method)
            for key, _ in self.selector.select(min(remaining, 0.2)):
                chunk = os.read(key.fd, 65536)
                if not chunk:
                    self.selector.unregister(key.fileobj)
                    if key.data == 'stdout':
                        raise ValueError('app-server exited before response: ' + method)
                elif key.data == 'stdout':
                    self.buffer += chunk
                    if len(self.buffer) > 16 * 1024 * 1024:
                        raise ValueError('app-server response exceeds 16 MiB')

    def message(self, row):
        return row

    def close(self):
        if self.process is not None:
            stop(self.process)
            for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
                stream.close()
        self.selector.close()

    def __exit__(self, *args):
        self.close()


def skill_hashes(path):
    """Pin every bundled runtime resource, excluding interpreter caches."""
    path = Path(path).resolve(strict=True)
    root = path.parent
    files = {}
    for entry in sorted(root.rglob('*')):
        if '__pycache__' in entry.parts or entry.suffix == '.pyc' or not entry.is_file():
            continue
        if not entry.resolve().is_relative_to(root):
            raise ValueError('skill resource escapes its directory')
        files[str(entry.relative_to(root))] = sha256(entry)
    return files


def discover_codex(cwds, codex='codex', timeout=30):
    cwds = list(dict.fromkeys(str(Path(p).resolve(strict=True)) for p in cwds))
    result = {'skills': {p: {'status': 'discovery_failed', 'error': 'not queried', 'skills': []}
                         for p in cwds},
              'models': {'status': 'discovery_failed', 'error': 'not queried', 'data': []}}
    try:
        with AppServer(codex, timeout) as server:
            for cwd in cwds:
                try:
                    response = server.call('skills/list', {'cwds': [cwd], 'forceReload': True})
                    matches = [row for row in response['data'] if row['cwd'] == cwd]
                    if len(matches) != 1:
                        raise ValueError('missing or duplicate cwd inventory')
                    row = matches[0]
                    if row.get('errors'):
                        raise ValueError('skills/list errors: ' + json.dumps(row['errors']))
                    skills = []
                    for skill in row['skills']:
                        if (not isinstance(skill['name'], str) or not isinstance(skill['path'], str)
                                or not Path(skill['path']).is_absolute()
                                or type(skill['enabled']) is not bool):
                            raise ValueError('malformed skill catalog entry')
                        skills.append({**skill, 'sha256': sha256(skill['path']), 'files': skill_hashes(skill['path'])})
                    result['skills'][cwd] = {'status': 'ok', 'skills': skills}
                except (OSError, ValueError, KeyError, TypeError, TimeoutError) as error:
                    result['skills'][cwd]['error'] = str(error)
            try:
                models, cursors, cursor = [], set(), None
                while True:
                    params = {'limit': 100}
                    if cursor is not None:
                        params['cursor'] = cursor
                    page = server.call('model/list', params)
                    for model in page['data']:
                        if (not isinstance(model['model'], str)
                                or not isinstance(model['supportedReasoningEfforts'], list)):
                            raise ValueError('malformed model catalog entry')
                        for effort in model['supportedReasoningEfforts']:
                            if not isinstance(effort['reasoningEffort'], str):
                                raise ValueError('malformed reasoning effort')
                    models.extend(page['data'])
                    cursor = page.get('nextCursor')
                    if cursor is None:
                        break
                    if not isinstance(cursor, str) or not cursor or cursor in cursors:
                        raise ValueError('invalid or repeated model cursor')
                    cursors.add(cursor)
                result['models'] = {'status': 'ok', 'data': models}
            except (OSError, ValueError, KeyError, TypeError, TimeoutError) as error:
                result['models']['error'] = str(error)
    except (OSError, ValueError, KeyError, TypeError, TimeoutError) as error:
        for row in result['skills'].values():
            if row['status'] != 'ok':
                row['error'] = str(error)
        result['models']['error'] = str(error)
    return result


class ClaudeControl(AppServer):
    """Read initialize metadata using the CLI's documented Agent SDK transport."""
    def __init__(self, executable, cwd, timeout):
        super().__init__(executable, timeout)
        self.command = [executable, '-p', '--input-format', 'stream-json', '--output-format',
                        'stream-json', '--verbose', '--permission-mode', 'dontAsk', '--tools', '']
        self.cwd = cwd

    def send(self, message):
        if 'id' in message:
            row = {'type': 'control_request', 'request_id': str(message['id']),
                   'request': {'subtype': 'initialize'}}
            super().send(row)

    def message(self, row):
        if not isinstance(row, dict):
            raise ValueError('malformed Claude control response')
        if row.get('type') != 'control_response':
            return row
        value = row['response']
        if value['subtype'] != 'success':
            return {'id': int(value['request_id']), 'error': value.get('error', 'initialize failed')}
        return {'id': int(value['request_id']), 'result': value['response']}


def _skill(path, name, enabled=True, **extra):
    path = str(Path(path).resolve(strict=True))
    return {'name': name, 'path': path, 'enabled': enabled,
            'sha256': sha256(path), 'files': skill_hashes(path), **extra}


def _claude_skills(cwd, metadata, extra_roots):
    commands = {x['name']: x for x in metadata['commands']}
    config = Path(os.environ.get('CLAUDE_CONFIG_DIR', str(Path.home() / '.claude')))
    roots = [(config / 'skills', False), (Path(cwd) / '.claude/skills', False)]
    roots += [(Path(root), True) for root in extra_roots]
    skills = {}
    for root, explicit in roots:
        if not root.exists():
            continue
        for path in root.glob('*/SKILL.md'):
            resolved = str(path.resolve())
            if resolved in skills and not explicit:
                continue
            match = re.search(r'^name:[ \t]*[\"\']?([A-Za-z0-9_-]+)', path.read_text(), re.M)
            if not match:
                raise ValueError('cannot resolve Claude skill name: ' + str(path))
            name = match[1]
            registered = name in commands
            disabled = commands.get(name, {}).get('disabled') is True
            # SDK command names alone never establish the registered file path.
            # Explicit candidates are delivered as pinned text, not native registration.
            skills[resolved] = _skill(path, name, explicit and registered and not disabled,
                                     visibility='context' if explicit and registered else 'unconfirmed',
                                     native_name_registered=registered)
    return list(skills.values()), sorted(set(commands) - {x['name'] for x in skills.values()})


@contextlib.contextmanager
def opencode_catalog(executable, cwd, timeout):
    """Own a private server: one-shot API snapshots precede plugin settlement."""
    env = {**os.environ, 'OPENCODE_PASSWORD': secrets.token_urlsafe(32)}
    process = subprocess.Popen([executable, 'serve', '--hostname', '127.0.0.1', '--port', '0'],
                               cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    selector = selectors.DefaultSelector()
    deadline = time.monotonic() + timeout
    try:
        selector.register(process.stdout, selectors.EVENT_READ)
        pending = b''
        while b'\n' not in pending:
            if not selector.select(max(0, deadline - time.monotonic())):
                raise TimeoutError('OpenCode server startup timeout')
            chunk = os.read(process.stdout.fileno(), 65536)
            if not chunk:
                raise ValueError('OpenCode server exited before its address')
            pending += chunk
            if len(pending) > 65536:
                raise ValueError('OpenCode startup output exceeds limit')
        line = pending.split(b'\n', 1)[0].decode()
        address = re.search(r'http://127\.0\.0\.1:[0-9]+', line)
        if not address:
            raise ValueError('OpenCode did not return a local server address')
        def query(operation):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('OpenCode inventory timeout')
            paths = {'plugin.list': '/api/plugin', 'model.list': '/api/model',
                     'agent.list': '/api/agent', 'skill.list': '/api/skill'}
            url = address[0] + paths[operation] + '?' + urllib.parse.urlencode({'location[directory]': cwd})
            credentials = env.get('OPENCODE_USERNAME', 'opencode') + ':' + env['OPENCODE_PASSWORD']
            request = urllib.request.Request(url, headers={'Authorization': 'Basic ' + base64.b64encode(credentials.encode()).decode()})
            with urllib.request.urlopen(request, timeout=remaining) as response:
                value = json.load(response)
            if Path(value['location']['directory']).resolve() != Path(cwd).resolve():
                raise ValueError('OpenCode returned another location')
            return value['data']
        while True:
            plugins = query('plugin.list')
            states = {p.get('id'): p['state']['status'] for p in plugins}
            required = ('opencode.skill', 'opencode.config.skill', 'opencode.tool.skill')
            if any(states.get(k) == 'failed' for k in required):
                raise ValueError('OpenCode skill plugin failed')
            if all(states.get(k) == 'active' for k in required):
                break
            if time.monotonic() >= deadline:
                raise TimeoutError('OpenCode skill discovery did not settle')
            time.sleep(min(.1, max(0, deadline - time.monotonic())))
        yield query
    finally:
        stop(process)
        process.stdout.close()
        process.stderr.close()
        selector.close()


def discover(cwds, codex='codex', timeout=30, harness='codex', executable=None, skill_roots=()):
    if harness == 'codex':
        return {**discover_codex(cwds, executable or codex, timeout), 'harness': 'codex'}
    if harness not in native.NAMES:
        raise ValueError('unsupported harness')
    cwds = list(dict.fromkeys(str(Path(p).resolve(strict=True)) for p in cwds))
    result = {'harness': harness, 'skills': {},
              'models': {'status': 'discovery_failed', 'error': 'not queried', 'data': []}}
    executable = executable or harness
    for cwd in cwds:
        result['skills'][cwd] = {'status': 'discovery_failed', 'skills': []}
        try:
            if harness == 'opencode':
                with opencode_catalog(executable, cwd, timeout) as query:
                    models = query('model.list')
                    agents = query('agent.list')
                    entries = query('skill.list')
                agent = next((a for a in agents if a['id'] == 'build'), None)
                if agent is None:
                    raise ValueError('OpenCode build agent is unavailable')
                skills = []
                for item in entries:
                    effect = 'ask'
                    for rule in agent['permissions']:
                        if fnmatch.fnmatchcase('skill', rule['action']) and fnmatch.fnmatchcase(item['id'], rule['resource']):
                            effect = rule['effect']
                    if item['path'].startswith('/builtin/') and not Path(item['path']).exists():
                        skills.append({'name': item['id'], 'path': item['path'], 'enabled': effect != 'deny',
                                       'virtual': True, 'sha256': hashlib.sha256(item['content'].encode()).hexdigest(),
                                       'files': {}, 'permission': effect})
                    else:
                        skills.append(_skill(item['path'], item['id'], effect != 'deny',
                                             native_id=item['id'], permission=effect))
                catalog = [{'model': m['providerID'] + '/' + m['id'],
                            'supportedReasoningEfforts': [{'reasoningEffort': v['id']} for v in m['variants']] or [{'reasoningEffort': None}]}
                           for m in models if m['enabled'] and m.get('type', 'chat') == 'chat']
                unresolved = []
            else:
                with ClaudeControl(executable, cwd, timeout) as server:
                    metadata = server.initial
                skills, unresolved = _claude_skills(cwd, metadata, skill_roots)
                catalog = [{'model': m['value'], 'supportedReasoningEfforts':
                            [{'reasoningEffort': v} for v in m.get('supportedEffortLevels', [])] or [{'reasoningEffort': None}]}
                           for m in metadata['models']]
            if not catalog or any(not isinstance(m['model'], str) or not m['model'] for m in catalog):
                raise ValueError('native model catalog is empty or malformed')
            result['skills'][cwd] = {'status': 'ok', 'skills': skills, 'unresolved': unresolved}
            if result['models']['status'] == 'ok' and result['models']['data'] != catalog:
                raise ValueError('model catalogs differ across cwd values; query each cwd separately')
            result['models'] = {'status': 'ok', 'data': catalog}
        except (OSError, ValueError, KeyError, TypeError, TimeoutError, subprocess.TimeoutExpired) as error:
            result['skills'][cwd]['status'] = 'discovery_failed'
            result['skills'][cwd]['error'] = str(error)
            result['models'] = {'status': 'discovery_failed', 'error': str(error), 'data': []}
    return result


def skill_status(inventory, cwd, name):
    row = inventory['skills'].get(str(Path(cwd).resolve()))
    if not row or row['status'] != 'ok':
        return {'status': 'discovery_failed', 'error': (row or {}).get('error', 'cwd not queried')}
    matches = [skill for skill in row['skills'] if skill['name'] == name]
    contexts = [s for s in matches if s.get('visibility') == 'context']
    if contexts:
        return {'status': 'context' if any(s['enabled'] for s in contexts) else 'disabled', 'matches': contexts}
    if name in row.get('unresolved', []) or any(s.get('visibility') == 'unconfirmed' for s in matches):
        return {'status': 'discovery_failed', 'error': 'native skill visibility/path is unconfirmed', 'matches': matches}
    return {'status': ('enabled' if any(s['enabled'] for s in matches) else 'disabled')
            if matches else 'missing', 'matches': matches}


def validate_model(inventory, model, effort):
    row = inventory['models']
    if row['status'] != 'ok':
        raise ValueError('model discovery failed: ' + row.get('error', 'unknown'))
    matches = [entry for entry in row['data'] if entry['model'] == model]
    if len(matches) != 1:
        raise ValueError('model is absent or ambiguous in catalog')
    if effort not in [item['reasoningEffort'] for item in matches[0]['supportedReasoningEfforts']]:
        raise ValueError('unsupported reasoning effort for selected model')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cwd', action='append', required=True, help='Repeat for each repository')
    parser.add_argument('--harness', choices=native.NAMES, required=True)
    parser.add_argument('--executable', help='Selected harness executable')
    parser.add_argument('--skill-root', action='append', default=[], help='Explicit Claude candidate skills root for pinned context delivery')
    parser.add_argument('--codex', default='codex', help='Codex executable')
    parser.add_argument('--timeout', type=float, default=30, help='Discovery deadline: total for Codex, per cwd for Claude/OpenCode')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    value = discover(args.cwd, args.codex, args.timeout, args.harness, args.executable, args.skill_root)
    atomic_json(args.output, value)
    print(json.dumps(value))
    return int(value['models']['status'] != 'ok' or any(r['status'] != 'ok' for r in value['skills'].values()))


if __name__ == '__main__':
    raise SystemExit(main())
