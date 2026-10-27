#!/usr/bin/env python3
"""Regression checks through the public CLI, using disposable Git repositories."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

CLI = Path(__file__).with_name('check-skills.sh').resolve()
ROOT = CLI.parents[2]
PRE_COMMIT = ROOT / '.githooks/pre-commit'

SKILLS = ('dev-rnd', 'dev-bug', 'dev-review', 'dev-commit')
SHARED = {
    'references/ticket.md': ('dev-rnd', 'dev-bug', 'dev-review'),
    'references/feature-directory.md': ('dev-rnd', 'dev-bug'),
    'assets/spec.md': ('dev-rnd', 'dev-bug'),
    'assets/ticket.md': ('dev-rnd', 'dev-bug', 'dev-review'),
}


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def write(repo, path, text):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)


def build_tree(repo):
    for name in SKILLS:
        header = f'---\nname: {name}\ndescription: Fixture skill {name}.\n'
        if name != 'dev-commit':
            header += 'disable-model-invocation: true\n'
            write(repo, f'skills/{name}/agents/openai.yaml',
                  'policy:\n  allow_implicit_invocation: false\n')
        write(repo, f'skills/{name}/SKILL.md', header + '---\n\n# SKILL\n\nA skill.\n')
    for role in ('review-quality', 'review-testing', 'review-simplification', 'review-verify'):
        write(repo, f'skills/dev-review/roles/{role}.md',
              f'---\nname: {role}\ndescription: Fixture role.\ntools: Read, Grep, Glob, Bash\n---\n\n# ROLE\n')
    for relative, consumers in SHARED.items():
        for consumer in consumers:
            write(repo, f'skills/{consumer}/{relative}', f'# {relative}\n\nShared fixture content.\n')
    write(repo, 'CHANGELOG.md', '# Changelog\n\n## [Unreleased]\n\n## [0.1.0] - 2026-09-10\n\n- Initial.\n')


def commit(repo):
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'fixture')
    return git(repo, 'rev-parse', 'HEAD')


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
    if expected:
        assert 'skills check: passed' in output, output
    else:
        assert 'skills check: ' in output and diagnostic in output, output


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
    build_tree(repo)
    commit(repo)
    return repo


def hooked_commit(repo, expected=True, diagnostic=''):
    head = git(repo, 'rev-parse', 'HEAD')
    result = subprocess.run(['git', '-C', str(repo), 'commit', '-qm', 'hooked'],
                            capture_output=True, text=True)
    output = result.stdout + result.stderr
    assert (result.returncode == 0) == expected, output
    assert diagnostic in output, output
    assert (git(repo, 'rev-parse', 'HEAD') != head) == expected, 'unexpected commit state'


def main():
    with tempfile.TemporaryDirectory() as raw:
        root = Path(raw)

        # Valid tree passes in every mode, and the checker never writes.
        repo = fresh(root, 'valid')
        check(repo)
        check(repo, True, '--staged')
        head = git(repo, 'rev-parse', 'HEAD')
        check(repo, True, '--base', head, '--head', head)

        # A broken working tree fails without touching the index.
        write(repo, 'skills/dev-rnd/SKILL.md',
              '---\nname: rnd\ndescription: Fixture.\ndisable-model-invocation: true\n---\n')
        check(repo, False, diagnostic='name must match directory')
        check(repo, True, '--staged')  # the index still holds the valid tree
        git(repo, 'checkout', '--', 'skills/dev-rnd/SKILL.md')

        # Missing skill fails.
        shutil.rmtree(repo / 'skills/dev-commit')
        check(repo, False, diagnostic="expected ['dev-bug', 'dev-commit', 'dev-review', 'dev-rnd']")
        git(repo, 'checkout', '--', 'skills/dev-commit')

        # A link escaping its skill fails, and so does a missing destination.
        write(repo, 'skills/dev-rnd/SKILL.md',
              '---\nname: dev-rnd\ndescription: Fixture.\ndisable-model-invocation: true\n---\n\n'
              '[ticket](../../dev-bug/references/ticket.md)\n')
        check(repo, False, diagnostic='escapes its skill')
        write(repo, 'skills/dev-rnd/SKILL.md',
              '---\nname: dev-rnd\ndescription: Fixture.\ndisable-model-invocation: true\n---\n\n'
              '[ticket](references/missing.md)\n')
        check(repo, False, diagnostic='missing local Markdown resource')
        git(repo, 'checkout', '--', 'skills/dev-rnd/SKILL.md')

        # Divergent shared copies fail.
        write(repo, 'skills/dev-review/references/ticket.md', '# TICKET\n\nDivergent copy.\n')
        check(repo, False, diagnostic='shared file differs')
        git(repo, 'checkout', '--', 'skills/dev-review/references/ticket.md')

        # Wrong invocation policy fails.
        write(repo, 'skills/dev-bug/SKILL.md',
              '---\nname: dev-bug\ndescription: Fixture.\n---\n')
        check(repo, False, diagnostic='incorrect invocation policy')
        git(repo, 'checkout', '--', 'skills/dev-bug/SKILL.md')

        # An empty release entry fails.
        write(repo, 'CHANGELOG.md', '# Changelog\n\n## [Unreleased]\n\n## [0.1.0] - 2026-09-10\n\n')
        check(repo, False, diagnostic='has no content')
        git(repo, 'checkout', '--', 'CHANGELOG.md')

        # Two snapshots compare the selected trees, not the working files.
        base = git(repo, 'rev-parse', 'HEAD')
        for consumer in ('dev-rnd', 'dev-bug', 'dev-review'):
            write(repo, f'skills/{consumer}/references/ticket.md', '# TICKET\n\nEdited in all copies.\n')
        check(repo)  # the working tree stays internally consistent
        commit(repo)
        head = git(repo, 'rev-parse', 'HEAD')
        write(repo, 'skills/dev-rnd/references/ticket.md', '# TICKET\n\nDivergent working copy.\n')
        check(repo, False, diagnostic='shared file differs')  # the working tree is broken
        check(repo, True, '--base', head, '--head', head)  # the committed tree is still valid
        git(repo, 'checkout', '--', 'skills/dev-rnd/references/ticket.md')

        # The pre-commit hook validates the index being committed.
        hooked = fresh(root, 'hooked')
        for name in ('check-skills.sh', 'check-skills.py'):
            write(hooked, f'.github/scripts/{name}', CLI.with_name(name).read_text())
        commit(hooked)  # fixture hooks are still disabled for this commit
        git(hooked, 'config', 'core.hooksPath', str(ROOT / '.githooks'))
        write(hooked, 'skills/dev-review/assets/ticket.md', '# TICKET\n\nDivergent copy.\n')
        git(hooked, 'add', 'skills/dev-review/assets/ticket.md')
        hooked_commit(hooked, expected=False, diagnostic='shared file differs')
        git(hooked, 'reset', '-q', 'HEAD')
        git(hooked, 'checkout', '--', 'skills/dev-review/assets/ticket.md')

    print('test_check_skills: passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
