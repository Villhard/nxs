#!/usr/bin/env python3
"""Check real Codex request assembly against a loopback stub; no model is called."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import zlib


ROOT = Path(__file__).resolve().parents[2]
EXPLICIT = ('rnd', 'bug', 'plan', 'exec', 'review', 'fix')


def main():
    marketplace = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT
    skills = marketplace / 'plugins/dev/skills'
    descriptions = {
        name: next(line.removeprefix('description: ') for line in
                   (skills / name / 'SKILL.md').read_text().splitlines()
                   if line.startswith('description: '))
        for name in (*EXPLICIT, 'commit')
    }
    requests = []
    received = threading.Event()

    class Capture(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            raw = self.rfile.read(int(self.headers.get('Content-Length', 0)))
            if self.headers.get('Content-Encoding') == 'gzip':
                raw = zlib.decompress(raw, 31)
            requests.append(json.loads(raw))
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"error":{"message":"Local capture complete",'
                             b'"type":"invalid_request_error"}}')
            received.set()

    with tempfile.TemporaryDirectory(prefix='nxs-invocation-') as directory:
        work = Path(directory)
        home = work / 'codex-home'
        home.mkdir()
        env = dict(os.environ, CODEX_HOME=str(home))
        for args in (('marketplace', 'add', str(marketplace)), ('add', 'dev@nxs')):
            subprocess.run(['codex', 'plugin', *args], env=env, cwd=work,
                           check=True, capture_output=True, text=True, timeout=30)
        server = HTTPServer(('127.0.0.1', 0), Capture)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        command = [
            'codex', 'exec', '--ephemeral', '--skip-git-repo-check',
            '--sandbox', 'read-only', '--json', '-C', str(work),
            '-c', 'model_provider="capture"',
            '-c', 'model_providers.capture.name="Local capture"',
            '-c', f'model_providers.capture.base_url="http://127.0.0.1:{server.server_port}/v1"',
            '-c', 'model_providers.capture.wire_api="responses"',
            '-c', 'model_providers.capture.requires_openai_auth=false',
        ]
        cases = [
            ('ordinary', None, 'Explain an off-by-one error.'),
            ('quoted-handoff', None, 'Assess this quoted handoff: "Next use /dev:bug, /dev:plan and /dev:exec."'),
            ('commit-request', None, 'Commit the prepared change.'),
            ('commit-discussion', None, 'Explain what a commit is.'),
        ] + [(name, name, f'$dev:{name} Use this command on a synthetic example.')
             for name in EXPLICIT]
        try:
            for case, selected, prompt in cases:
                requests.clear()
                received.clear()
                with (work / 'client.log').open('w') as log:
                    process = subprocess.Popen(command + [prompt], env=env,
                                               stdin=subprocess.DEVNULL,
                                               stdout=log, stderr=log)
                    try:
                        if not received.wait(30):
                            raise RuntimeError(f'No Codex request captured for {case}')
                        text = json.dumps(requests[0].get('input', []))
                        for name in EXPLICIT:
                            needle = json.dumps(descriptions[name])[1:-1]
                            assert (needle in text) == (name == selected), (selected, name)
                        assert json.dumps(descriptions['commit'])[1:-1] in text, 'commit must remain discoverable'
                        if selected:
                            assert f'# /dev:{selected}' in text.lower(), 'explicit skill body missing'
                        print(f'{case}: PASS', flush=True)
                    finally:
                        process.terminate()
                        try:
                            process.wait(timeout=3)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
    print('Codex invocation context: PASS (request assembly, not model behavior)')


if __name__ == '__main__':
    main()
