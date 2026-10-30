"""Discover Codex skills per cwd and the paginated model catalog via app-server."""
import argparse
import json
import os
from pathlib import Path
import selectors
import subprocess
import time

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
                                            start_new_session=True)
            self.selector.register(self.process.stdout, selectors.EVENT_READ, 'stdout')
            self.selector.register(self.process.stderr, selectors.EVENT_READ, 'stderr')
            self.call('initialize', {'clientInfo': {'name': 'nxs-dev-lead', 'version': '1'}})
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
                row = json.loads(line)
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


def discover(cwds, codex='codex', timeout=30):
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


def skill_status(inventory, cwd, name):
    row = inventory['skills'].get(str(Path(cwd).resolve()))
    if not row or row['status'] != 'ok':
        return {'status': 'discovery_failed', 'error': (row or {}).get('error', 'cwd not queried')}
    matches = [skill for skill in row['skills'] if skill['name'] == name]
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
    parser.add_argument('--codex', default='codex', help='Codex executable')
    parser.add_argument('--timeout', type=float, default=30, help='Total app-server deadline in seconds')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    value = discover(args.cwd, args.codex, args.timeout)
    atomic_json(args.output, value)
    print(json.dumps(value))
    return int(value['models']['status'] != 'ok' or any(r['status'] != 'ok' for r in value['skills'].values()))


if __name__ == '__main__':
    raise SystemExit(main())
