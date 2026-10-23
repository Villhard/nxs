#!/usr/bin/env python3
"""Check the dev OpenCode installer against temporary config directories; no model is called."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / 'plugins/dev/opencode/install.py'
ROLES = ('review-quality', 'review-testing', 'review-simplification', 'review-verify')
SKILLS = ('rnd', 'bug', 'review', 'commit')


def run(config, *args, version='2.1.2'):
    bin_dir = config.parent / 'bin'
    bin_dir.mkdir(exist_ok=True)
    fake = bin_dir / 'opencode'
    if version:
        fake.write_text(f'#!/bin/sh\necho "opencode v{version}"\n')
        fake.chmod(0o755)
    elif fake.exists():
        fake.unlink()
    env = dict(os.environ, PATH=f'{bin_dir}:/usr/bin:/bin')
    env.pop('OPENCODE_CONFIG_DIR', None)
    return subprocess.run([sys.executable, str(INSTALLER), '--config-dir', str(config), *args],
                          env=env, capture_output=True, text=True, timeout=60)


def tree(config):
    return {p.relative_to(config).as_posix(): p.read_bytes() for p in sorted(config.rglob('*')) if p.is_file()}


def fields(text):
    head = re.match(r'---\n(.*?)\n---\n', text, re.S)[1]
    return {line.split(':')[0] for line in head.splitlines() if not line.startswith(' ')}, text[len(head) + 9:]


def case(name, func):
    with tempfile.TemporaryDirectory(prefix='nxs-opencode-') as directory:
        config = Path(directory).resolve() / 'config'
        config.mkdir()
        func(config)
    print(f'{name}: PASS', flush=True)


def fresh_install(config):
    result = run(config)
    assert result.returncode == 0, result.stderr
    files = tree(config)
    for name in SKILLS:
        source = ROOT / f'plugins/dev/skills/{name}/SKILL.md'
        assert files[f'nxs/dev/skills/{name}/SKILL.md'] == source.read_bytes()
    assert not [rel for rel in files if rel.startswith('commands/dev/')], 'skills need no proxy commands'
    for role in ROLES:
        agent = files[f'agents/dev/{role}.md'].decode()
        keys, body = fields(agent)
        assert keys == {'description', 'mode', 'permissions'}, keys
        assert 'mode: subagent' in agent and 'hidden' not in keys
        first = agent.index('  - action: "*"\n    resource: "*"\n    effect: deny')
        assert first < agent.index('action: "shell"'), 'deny-all must come first'
        assert '*.env.example' in agent
        source = (ROOT / f'plugins/dev/agents/{role}.md').read_text()
        assert body == source[source.index('\n---\n', 4) + 5:], role
    assert files['commands/plan.md'].decode().startswith('---\ndescription:')
    assert 'agent: plan' in files['commands/plan.md'].decode()
    config_text = files['opencode.jsonc'].decode()
    assert json.loads(config_text)['skills'] == [str(config / 'nxs/dev/skills')]
    manifest = json.loads(files['nxs/dev-install.json'])
    assert manifest['plan_command'] == 'installed' and manifest['config_created']
    again = run(config)
    assert again.returncode == 0 and '(no changes)' in again.stdout, again.stdout
    assert tree(config) == files, 'second run must not change files'
    removed = run(config, '--uninstall')
    assert removed.returncode == 0, removed.stderr
    assert tree(config) == {}, tree(config)


def existing_jsonc(config):
    text = ('{\n  // keep this comment\n  "model": "x/y", /* block */\n'
            '  "agents": {"build": {"skills": ["nested"]}},\n  "skills": [\n    "~/mine", // mine\n  ],\n}\n')
    (config / 'opencode.jsonc').write_text(text)
    assert run(config).returncode == 0
    updated = (config / 'opencode.jsonc').read_text()
    assert '// keep this comment' in updated and '/* block */' in updated and '// mine' in updated
    assert updated.count(str(config / 'nxs/dev/skills')) == 1
    assert '"nested"]' in updated, 'nested skills key must stay untouched'
    assert run(config).returncode == 0
    assert (config / 'opencode.jsonc').read_text() == updated, 're-run must not add the entry twice'
    assert run(config, '--uninstall').returncode == 0
    assert (config / 'opencode.jsonc').read_text().count('nxs/dev/skills') == 0
    assert '"~/mine"' in (config / 'opencode.jsonc').read_text()


def existing_json_without_skills(config):
    (config / 'opencode.json').write_text('{"$schema": "https://opencode.ai/config.json", "model": "x/y"}\n')
    assert run(config).returncode == 0
    data = json.loads((config / 'opencode.json').read_text())
    assert data['model'] == 'x/y' and data['skills'] == [str(config / 'nxs/dev/skills')]
    assert not (config / 'opencode.jsonc').exists()
    assert run(config, '--uninstall').returncode == 0
    assert json.loads((config / 'opencode.json').read_text()) == {
        '$schema': 'https://opencode.ai/config.json', 'model': 'x/y', 'skills': []}


def malformed_config(config):
    (config / 'opencode.json').write_text('{"skills": [}\n')
    result = run(config)
    assert result.returncode == 1 and 'stopped' in result.stderr, result
    assert set(tree(config)) == {'opencode.json'}, 'no writes before validation'


def user_files(config):
    (config / 'commands').mkdir()
    (config / 'commands/plan.md').write_text('---\ndescription: mine\n---\nmine\n')
    result = run(config)
    assert result.returncode == 0 and '/plan: skipped' in result.stdout, result.stdout
    assert (config / 'commands/plan.md').read_text().endswith('mine\n')
    assert run(config, '--uninstall').returncode == 0
    assert set(tree(config)) == {'commands/plan.md'}
    (config / 'agents/dev').mkdir(parents=True)
    (config / 'agents/dev/review-quality.md').write_text('mine\n')
    result = run(config)
    assert result.returncode == 1 and 'not owned' in result.stderr, result
    assert not (config / 'nxs').exists()


def upgrade_removes_proxy_commands(config):
    assert run(config).returncode == 0
    path = config / 'nxs/dev-install.json'
    manifest = json.loads(path.read_text())
    for name in SKILLS:
        command = config / f'commands/dev/{name}.md'
        command.parent.mkdir(exist_ok=True)
        command.write_text(f'The user explicitly invoked /dev/{name}.\n')
        manifest['files'][f'commands/dev/{name}.md'] = hashlib.sha256(command.read_bytes()).hexdigest()
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    result = run(config)
    assert result.returncode == 0, result.stderr
    assert not (config / 'commands/dev').exists(), tree(config)
    assert 'commands/plan.md' in tree(config)
    assert not [rel for rel in json.loads(path.read_text())['files'] if rel.startswith('commands/dev/')]


def versions(config):
    refused = run(config, version='1.19.3')
    assert refused.returncode == 1 and 'OpenCode 2 only' in refused.stderr, refused
    assert tree(config) == {}
    missing = run(config, version=None)
    assert missing.returncode == 0 and 'not on PATH' in missing.stdout, missing


def main():
    case('fresh install, re-run, uninstall', fresh_install)
    case('existing JSONC keeps comments', existing_jsonc)
    case('existing JSON without skills', existing_json_without_skills)
    case('malformed config stops', malformed_config)
    case('user-owned files', user_files)
    case('upgrade removes proxy commands', upgrade_removes_proxy_commands)
    case('OpenCode version check', versions)
    print('OpenCode installer: PASS (generated files and config edits, not model behavior)')


if __name__ == '__main__':
    main()
