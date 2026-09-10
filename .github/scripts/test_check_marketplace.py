#!/usr/bin/env python3
"""Regression checks through the public CLI, using disposable Git repositories."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

CLI = Path(__file__).with_name('check-marketplace.sh').resolve()


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


def main():
    with tempfile.TemporaryDirectory(prefix='marketplace-check-') as directory:
        root = Path(directory)
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

        repo = fresh(root, 'metadata')
        path = repo / 'plugins/sample/.codex-plugin/plugin.json'
        path.write_text('{"name": "wrong", "version": "0.23.9"}')
        check(repo, False, diagnostic='name/version must match')
        path.write_text('{"name": "sample", "version": "0.23.10"}')
        check(repo, False, diagnostic='name/version must match')
        path.unlink()  # Codex metadata is optional.
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
        path = repo / 'plugins/sample/CHANGELOG.md'
        path.write_text(path.read_text() + '\n## [0.23.10] - 2026-09-10\n\n- Already here.\n')
        commit(repo)
        release(repo, body=False)
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
        write(repo, 'plugins/sample/skills/one/new.md', 'change')
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
