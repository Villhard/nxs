#!/usr/bin/env python3
"""Regression checks through the public CLI, using disposable Git repositories."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

CLI = Path(__file__).with_name('check-marketplace.sh').resolve()
ROOT = CLI.parents[2]
HOOK = ROOT / '.claude/hooks/check-version-bump.sh'


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def write(repo, path, text):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


def catalog(repo, names):
    write(repo, '.claude-plugin/marketplace.json', json.dumps({'plugins': [
        {'name': name, 'source': f'./plugins/{name}'} for name in names]}))


def plugin(repo, name='sample', value='0.23.9', codex=True):
    manifest = json.dumps({'name': name, 'version': value})
    write(repo, f'plugins/{name}/.claude-plugin/plugin.json', manifest)
    if codex:
        write(repo, f'plugins/{name}/.codex-plugin/plugin.json', manifest)
    write(repo, f'plugins/{name}/CHANGELOG.md', f'# Changelog\n\n## [{value}] - 2026-09-10\n\n- Initial.\n')
    write(repo, f'plugins/{name}/skills/one/SKILL.md', '# ONE\n\nA skill.\n')


def commit(repo):
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'fixture')
    return git(repo, 'rev-parse', 'HEAD')


def release(repo, value='0.23.10', name='sample', body=True):
    for client in ('claude', 'codex'):
        path = repo / f'plugins/{name}/.{client}-plugin/plugin.json'
        if path.exists():
            data = json.loads(path.read_text())
            data['version'] = value
            path.write_text(json.dumps(data))
    if body:
        path = repo / f'plugins/{name}/CHANGELOG.md'
        path.write_text(f'# Changelog\n\n## [{value}] - 2026-09-10\n\n- Updated.\n\n' + path.read_text())


def state(repo):
    # Include working bytes, index and loose objects: validation must not write any of them.
    return {str(path.relative_to(repo)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in repo.rglob('*') if path.is_file()}


def check(repo, expected=True, *args, diagnostic=''):
    before = state(repo)
    result = subprocess.run(['bash', str(CLI), *args], cwd=repo, capture_output=True, text=True)
    assert state(repo) == before, 'checker modified repository state'
    output = result.stdout + result.stderr
    assert (result.returncode == 0) == expected, (args, output)
    assert diagnostic in output, output


def fresh(root, name):
    repo = root / name
    repo.mkdir()
    git(repo, 'init', '-q')
    git(repo, 'config', 'user.name', 'Fixture')
    git(repo, 'config', 'user.email', 'fixture@example.invalid')
    git(repo, 'config', 'commit.gpgsign', 'false')
    hooks = repo / '.git/fixture-hooks'
    hooks.mkdir()
    git(repo, 'config', 'core.hooksPath', str(hooks))
    catalog(repo, ['sample'])
    plugin(repo)
    commit(repo)
    return repo


def hook(repo, command=None, diagnostic='', payload=None):
    if payload is None:
        payload = json.dumps({'tool_input': {'command': command}})
    before = state(repo)
    result = subprocess.run(['bash', str(HOOK)], input=payload, cwd=repo,
                            capture_output=True, text=True)
    assert state(repo) == before, 'hook modified repository state'
    assert result.returncode == 0, result.stderr
    if diagnostic:
        output = json.loads(result.stdout)['hookSpecificOutput']
        assert output['permissionDecision'] == 'deny', output
        assert diagnostic in output['permissionDecisionReason'], output
    else:
        assert not result.stdout, result.stdout


def ci_check(repo, event, head, before='', target='', default='main', expected=True):
    # Execute the actual CI block, without a YAML dependency or a second baseline algorithm.
    workflow = (ROOT / '.github/workflows/ci.yml').read_text()
    block = workflow.split('      - name: Check release snapshots\n', 1)[1]
    block = block.split('        run: |\n', 1)[1].split('\n      - name:', 1)[0]
    script = '\n'.join(line[10:] for line in block.splitlines())
    env = dict(os.environ, EVENT_NAME=event, HEAD_SHA=head, BEFORE_SHA=before,
               TARGET_SHA=target, DEFAULT_BRANCH=default)
    snapshot = state(repo)
    result = subprocess.run(['bash', '-c', script], cwd=repo, env=env,
                            capture_output=True, text=True)
    assert state(repo) == snapshot, 'CI check modified repository state'
    assert (result.returncode == 0) == expected, result.stdout + result.stderr


def integration(root):
    repo = fresh(root, 'integration')
    for name in ('check-marketplace.sh', 'check-marketplace.py'):
        write(repo, '.github/scripts/' + name, CLI.with_name(name).read_text())
    base = commit(repo)
    hook(repo, 'git status')
    hook(repo, 'git log --grep commit')
    hook(repo, 'git show HEAD:README.md | rg commit')
    hook(repo, 'git -C /tmp log --grep commit')
    hook(repo, 'echo "git commit"')
    hook(repo, "rg 'git commit' CONTRIBUTING.md")
    hook(repo, payload='{broken', diagnostic='Invalid Bash hook payload')
    write(repo, 'plugins/sample/skills/one/SKILL.md', '[asset](asset.md)\n')
    git(repo, 'add', '.')
    hook(repo, 'git commit -m update', diagnostic='version must increase')
    release(repo)
    write(repo, 'plugins/sample/skills/one/asset.md', 'Asset\n')
    git(repo, 'add', '.')
    (repo / 'plugins/sample/skills/one/asset.md').unlink()
    hook(repo, 'git commit -m "valid staged release"')
    hook(repo, "git commit -m 'refactor(dev): extract artifact templates'")
    hook(repo, "git commit -m 'fix(dev): literal $ and & and ;'")
    hook(repo, 'git commit -m "refactor(dev): extract templates"')
    for command in ('git commit -a', 'git commit -am update', 'git commit --all',
                    'git commit --only README.md', 'git commit --include README.md',
                    'git commit README.md', 'git commit --amend',
                    'git commit -m update && git status', 'cd /tmp && git commit',
                    'git status\ngit commit',
                    'git -C /tmp commit', 'git commit -m "$MESSAGE"',
                    'git commit -m "$(echo substituted)"',
                    'env GIT_INDEX_FILE=other git commit', 'bash -c "git commit"'):
        hook(repo, command, diagnostic='Stage the intended files first')
    git(repo, 'commit', '-qm', 'valid index')
    head = git(repo, 'rev-parse', 'HEAD')
    ci_check(repo, 'push', head, before=base)
    ci_check(repo, 'pull_request', head, target=base)
    git(repo, 'update-ref', 'refs/remotes/origin/main', base)
    ci_check(repo, 'push', head, before='0' * 40)
    skill = repo / 'plugins/sample/skills/one/SKILL.md'
    current_skill = skill.read_text()
    skill.write_text('Previous release implementation.\n')
    git(repo, 'add', str(skill))
    previous_tree = git(repo, 'write-tree')
    git(repo, 'read-tree', head)
    skill.write_text(current_skill)
    previous = git(repo, 'commit-tree', previous_tree,
                   '-p', base, '-m', 'rewritten previous tip')
    # The old CI baseline falsely rejected differing content at the same version.
    check(repo, False, '--base', previous, '--head', head, diagnostic='version must increase')
    ci_check(repo, 'push', head, before=previous)
    ci_check(repo, 'push', head, before='f' * 40)
    git(repo, 'update-ref', 'refs/remotes/origin/main', head)
    ci_check(repo, 'push', head, before='0' * 40)
    ci_check(repo, 'push', head, before='0' * 40, default='missing')
    # A real missing bump must still fail under all release baselines.
    write(repo, 'plugins/sample/skills/one/SKILL.md', 'Unreleased change\n')
    bad = commit(repo)
    ci_check(repo, 'push', bad, before=head, expected=False)
    ci_check(repo, 'push', bad, before=previous, expected=False)
    ci_check(repo, 'push', bad, before='f' * 40, expected=False)
    ci_check(repo, 'pull_request', bad, target=head, expected=False)
    ci_check(repo, 'push', bad, before='0' * 40, expected=False)
    ci_check(repo, 'push', bad, before='0' * 40, default='missing', expected=False)

    repo = root / 'initial'
    repo.mkdir()
    git(repo, 'init', '-q')
    git(repo, 'config', 'user.name', 'Fixture')
    git(repo, 'config', 'user.email', 'fixture@example.invalid')
    git(repo, 'config', 'commit.gpgsign', 'false')
    git(repo, 'config', 'core.hooksPath', str(repo / 'disabled-hooks'))
    catalog(repo, ['sample'])
    plugin(repo, value='0.1.0')
    for name in ('check-marketplace.sh', 'check-marketplace.py'):
        write(repo, '.github/scripts/' + name, CLI.with_name(name).read_text())
    head = commit(repo)
    ci_check(repo, 'push', head, before='0' * 40)


def main():
    with tempfile.TemporaryDirectory(prefix='marketplace-check-') as directory:
        root = Path(directory)
        integration(root)
        repo = fresh(root, 'releases')
        check(repo)
        write(repo, 'README.md', 'Root-only change.\n')
        check(repo)
        write(repo, 'plugins/sample/skills/one/new.md', 'Bundled untracked file.\n')
        check(repo, False, diagnostic='version must increase')
        release(repo)
        check(repo)  # Numeric ordering: 0.23.9 -> 0.23.10.
        commit(repo)
        release(repo, '0.23.9')
        check(repo, False, diagnostic='never regress')

        for edit in ('readme', 'manifest-description', 'changelog-text', 'executable-bit'):
            repo = fresh(root, edit)
            if edit == 'readme':
                write(repo, 'plugins/sample/README.md', 'Documentation edit.\n')
            elif edit == 'manifest-description':
                path = repo / 'plugins/sample/.claude-plugin/plugin.json'
                data = json.loads(path.read_text())
                data['description'] = 'Updated description'
                path.write_text(json.dumps(data))
            elif edit == 'changelog-text':
                path = repo / 'plugins/sample/CHANGELOG.md'
                path.write_text(path.read_text().replace('Initial.', 'Corrected wording.'))
            else:
                path = repo / 'plugins/sample/skills/one/SKILL.md'
                path.chmod(path.stat().st_mode | 0o111)
            check(repo, False, diagnostic='version must increase')
            git(repo, 'add', '.')
            check(repo, False, '--staged', diagnostic='version must increase')
            release(repo)
            check(repo)
            git(repo, 'add', '.')
            check(repo, True, '--staged')

        repo = fresh(root, 'metadata')
        path = repo / 'plugins/sample/.codex-plugin/plugin.json'
        path.write_text('{"name": "wrong", "version": "0.23.9"}')
        check(repo, False, diagnostic='name/version must match')
        path.write_text('{"name": "sample", "version": "0.23.10"}')
        check(repo, False, diagnostic='name/version must match')
        path.unlink()  # Optional metadata removal still changes the bundle.
        check(repo, False, diagnostic='version must increase')
        release(repo)
        check(repo)
        commit(repo)
        check(repo)  # An existing plugin without Codex metadata is valid.
        path.write_text('{"name": "sample", "version": "0.23.10"}')
        check(repo, False, diagnostic='version must increase')
        release(repo, '0.23.11')
        check(repo)
        path = repo / 'plugins/sample/.claude-plugin/plugin.json'
        path.write_text('{broken')
        check(repo, False, diagnostic='malformed JSON')
        path.unlink()
        check(repo, False, diagnostic='missing required file')

        repo = fresh(root, 'changelog')
        release(repo, body=False)
        check(repo, False, diagnostic='missing dated')
        path = repo / 'plugins/sample/CHANGELOG.md'
        path.write_text('## [0.23.10] - 2026-02-30\n')
        check(repo, False, diagnostic='invalid release date')
        path.write_text('## [0.23.10] - 2026-09-10\n\n')
        check(repo, False, diagnostic='has no content')
        path.unlink()
        check(repo, False, diagnostic='missing required file')

        repo = fresh(root, 'reused-entry')
        release(repo)
        path = repo / 'plugins/sample/CHANGELOG.md'
        path.write_text(path.read_text() + '\n## [0.23.11] - 2026-09-10\n\n- Already here.\n')
        check(repo)
        commit(repo)
        release(repo, '0.23.11', body=False)
        check(repo, False, diagnostic='must be new relative to base')

        repo = fresh(root, 'semver')
        for invalid in ('1.02.3', '1.2', '1.0.0-01', 'v1.0.0'):
            release(repo, invalid)
            check(repo, False, diagnostic='invalid SemVer')
        release(repo, '1.0.0-alpha.9')
        commit(repo)
        release(repo, '1.0.0-alpha.10')
        check(repo)
        commit(repo)
        release(repo, '1.0.0')
        check(repo)
        commit(repo)
        release(repo, '1.0.0+build')
        check(repo, False, diagnostic='version must increase')

        repo = fresh(root, 'catalog')
        plugin(repo, 'new', '0.1.0', codex=False)
        check(repo, False, diagnostic='catalog membership')
        catalog(repo, ['sample', 'new'])
        check(repo)
        release(repo, '0.2.0', name='new')
        check(repo, False, diagnostic='new plugin must start at 0.1.0')
        plugin(repo, 'new', '0.1.0', codex=False)
        commit(repo)
        shutil.rmtree(repo / 'plugins/new')
        check(repo, False, diagnostic='catalog membership')
        catalog(repo, ['sample'])
        check(repo)
        write(repo, '.claude-plugin/marketplace.json', '{"plugins":[{"name":"sample","source":"../sample"}]}')
        check(repo, False, diagnostic='source must be')

        repo = fresh(root, 'links')
        skill = 'plugins/sample/skills/one/SKILL.md'
        write(repo, skill, '# ONE\n\n[asset](assets/file.md#part)\n[site](https://example.invalid)\n[section](#part)\n')
        release(repo)
        check(repo, False, diagnostic='missing local Markdown resource')
        write(repo, 'plugins/sample/skills/one/assets/file.md', '# File\n')
        check(repo)
        write(repo, 'plugins/sample/skills/one/assets/file.md', '[nested](../SKILL.md)\n')
        check(repo)
        write(repo, 'plugins/sample/skills/one/assets/file.md', '[nested](../missing.md)\n')
        check(repo, False, diagnostic='missing local Markdown resource')

        repo = fresh(root, 'severity')
        plugin(repo, 'dev', '0.1.0', codex=False)
        catalog(repo, ['sample', 'dev'])
        for skill in ('review', 'fix'):
            write(repo, f'plugins/dev/skills/{skill}/SKILL.md', '# SKILL\n\n## SEVERITY BAR\n\nExact text.\n\n## END\n')
        check(repo)
        write(repo, 'plugins/dev/skills/fix/SKILL.md', '# FIX\n')
        check(repo, False, diagnostic='missing SEVERITY BAR')
        write(repo, 'plugins/dev/skills/fix/SKILL.md', '## SEVERITY BAR\n\nDifferent.\n\n## END\n')
        check(repo, False, diagnostic='must match exactly')

        repo = fresh(root, 'snapshots')
        base = git(repo, 'rev-parse', 'HEAD')
        write(repo, 'plugins/sample/skills/one/SKILL.md', '[resource](asset.md)\n')
        git(repo, 'add', '.')
        release(repo)
        write(repo, 'plugins/sample/skills/one/asset.md', 'Asset\n')
        check(repo)
        check(repo, False, '--staged', diagnostic='version must increase')
        git(repo, 'add', 'plugins/sample/.claude-plugin/plugin.json',
            'plugins/sample/.codex-plugin/plugin.json', 'plugins/sample/CHANGELOG.md')
        check(repo, False, '--staged', diagnostic='missing local Markdown resource')
        git(repo, 'add', '.')
        check(repo, True, '--staged')
        (repo / 'plugins/sample/skills/one/asset.md').unlink()
        check(repo, False, diagnostic='missing local Markdown resource')
        check(repo, True, '--staged')
        # Commit the valid index, leaving the broken disk untouched.
        git(repo, 'commit', '-qm', 'selected snapshot')
        head = git(repo, 'rev-parse', 'HEAD')
        check(repo, True, '--base', base, '--head', head)
        check(repo, False, '--base', head, '--head', base, diagnostic='never regress')
        check(repo, False, '--base', 'missing-ref', '--head', head)
        check(repo, False, '--base', base)
        check(repo, False, '--staged', '--base', base, '--head', head)
        check(repo, False, '--unknown')
        check(repo, False, '--base', '', '--head', '', diagnostic='must not be empty')
        check(repo, False, '--staged', '--base', '', '--head', '')
        check(repo, False, '--base=--help', '--head', head)
        release(repo, '0.23.11')
        git(repo, 'add', '.')  # Stage resource deletion, then repair disk only.
        write(repo, 'plugins/sample/skills/one/asset.md', 'Asset\n')
        check(repo)
        check(repo, False, '--staged', diagnostic='missing local Markdown resource')

        repo = fresh(root, 'ignored')
        write(repo, '.gitignore', 'plugins/sample/ignored.md\n')
        write(repo, 'plugins/sample/ignored.md', 'Ignored\n')
        check(repo)
    print('marketplace CLI regression checks: passed')


if __name__ == '__main__':
    main()
