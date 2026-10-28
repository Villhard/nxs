#!/usr/bin/env python3
"""Read-only skills-tree checks for working files, the index, or two Git trees."""
import argparse
import datetime
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

SKILLS = ('dev-rnd', 'dev-bug', 'dev-review', 'dev-spec', 'dev-setup', 'dev-commit')
EXPLICIT = ('dev-rnd', 'dev-bug', 'dev-review', 'dev-spec', 'dev-setup')
ROLES = ('review-quality', 'review-testing', 'review-simplification', 'review-verify')
# Files copied into every consuming skill and required to stay byte-identical.
SHARED = {
    'references/ticket.md': ('dev-rnd', 'dev-bug', 'dev-review'),
    'references/feature-directory.md': ('dev-rnd', 'dev-bug'),
    'references/project-specs.md': ('dev-rnd', 'dev-bug', 'dev-review', 'dev-spec'),
    'assets/spec.md': ('dev-rnd', 'dev-bug'),
    'assets/ticket.md': ('dev-rnd', 'dev-bug', 'dev-review'),
}


class Invalid(ValueError):
    pass


def git(*args):
    result = subprocess.run(['git', *args], capture_output=True)
    if result.returncode:
        raise Invalid(result.stderr.decode(errors='replace').strip())
    return result.stdout


def tree_ref(ref):
    return git('rev-parse', '--verify', '--end-of-options', ref + '^{tree}').decode().strip()


def snapshot(kind, ref=None):
    files = {}
    if kind == 'working':
        paths = git('ls-files', '--cached', '--others', '--exclude-standard', '-z')
        for raw in paths.split(b'\0'):
            if not raw:
                continue
            name = os.fsdecode(raw)
            path = Path(name)
            if path.is_symlink():
                files[name] = ('120000', os.fsencode(os.readlink(path)))
            elif path.is_file():
                files[name] = ('100755' if path.stat().st_mode & 0o111 else '100644', path.read_bytes())
        return files
    rows = git('ls-files', '--stage', '-z') if kind == 'staged' else git('ls-tree', '-rz', ref)
    for row in rows.split(b'\0'):
        if not row:
            continue
        meta, raw = row.split(b'\t', 1)
        mode, middle, last = meta.decode().split()
        name = os.fsdecode(raw)
        if kind == 'staged' and last != '0':
            raise Invalid(f'{name}: unresolved index conflict')
        oid = middle if kind == 'staged' else last
        if mode == '160000':
            files[name] = (mode, oid.encode())
        else:
            files[name] = (mode, git('cat-file', 'blob', oid))
    return files


def read(files, path):
    if path not in files:
        raise Invalid(f'{path}: missing required file')
    try:
        return files[path][1].decode('utf-8')
    except UnicodeError as error:
        raise Invalid(f'{path}: invalid UTF-8') from error


def releases(text, path):
    entries = []
    for value, date, body in re.findall(r'^## \[([^\]]+)\] - (\d{4}-\d{2}-\d{2})[ \t]*\n(.*?)(?=^## |\Z)', text, re.M | re.S):
        if value == 'Unreleased':
            continue
        try:
            datetime.date.fromisoformat(date)
        except ValueError as error:
            raise Invalid(f'{path}: invalid release date {date}') from error
        if not any(line.strip() and not line.startswith('#') for line in body.splitlines()):
            raise Invalid(f'{path}: release entry [{value}] has no content')
        entries.append(value)
    if not entries:
        raise Invalid(f'{path}: no dated release entries')
    return entries


def frontmatter(files, path):
    """Inspect the bounded top-level fields used by this repository, not general YAML."""
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', read(files, path), re.S)
    if not match:
        raise Invalid(f'{path}: missing or unclosed frontmatter')
    fields = {}
    key = None
    for line in match[1].splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        field = re.match(r'^([A-Za-z][\w-]*):[ \t]*(.*)$', line)
        if field:
            key, value = field.groups()
            if key in fields:
                raise Invalid(f'{path}: duplicate frontmatter field {key}')
            fields[key] = value
        elif line.startswith(' ') and key:
            fields[key] += '\n' + line
        else:
            raise Invalid(f'{path}: unsupported frontmatter line {line!r}')
    return fields


def scalar(fields, key, path):
    value = fields.get(key, '').strip()
    if re.match(r'^[>|][+-]?(?:\n|$)', value):
        value = ' '.join(line.strip() for line in value.splitlines()[1:])
    elif value.startswith('"'):
        import json
        try:
            value = json.loads(value)
        except ValueError as error:
            raise Invalid(f'{path}: invalid quoted {key}') from error
    elif value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise Invalid(f'{path}: invalid quoted {key}')
        value = value[1:-1].replace("''", "'")
    else:
        value = re.split(r'\s+#', value, maxsplit=1)[0].strip()
        if value.startswith('#'):
            value = ''
        if value in ('null', '~', 'true', 'false') or value.startswith(('[', '{', '&', '*', '!')):
            raise Invalid(f'{path}: {key} must be a text scalar')
    if not isinstance(value, str) or not value.strip():
        raise Invalid(f'{path}: missing or empty {key} frontmatter field')
    return value


def check_skills(files):
    present = {path.split('/')[1] for path in files if re.fullmatch(r'skills/[^/]+/SKILL\.md', path)}
    if present != set(SKILLS):
        raise Invalid(f'skills: expected {sorted(SKILLS)}, found {sorted(present)}')
    for name in SKILLS:
        path = f'skills/{name}/SKILL.md'
        fields = frontmatter(files, path)
        if scalar(fields, 'name', path) != name:
            raise Invalid(f'{path}: name must match directory {name}')
        description = scalar(fields, 'description', path)
        if len(description) > 1024:
            raise Invalid(f'{path}: description exceeds 1024 characters')
        for flag in ('user-invocable', 'disable-model-invocation'):
            if flag in fields and fields[flag] not in ('true', 'false'):
                raise Invalid(f'{path}: {flag} must be an unquoted boolean')
        explicit = name in EXPLICIT
        if (fields.get('disable-model-invocation') == 'true') != explicit:
            raise Invalid(f'{path}: incorrect invocation policy')
        policy = f'skills/{name}/agents/openai.yaml'
        if explicit or policy in files:
            blocks = re.findall(r'^policy:[ \t]*\n((?:[ \t]+[^\n]*\n?|\n)*)', read(files, policy), re.M)
            values = re.findall(r'^  allow_implicit_invocation:[ \t]*(\S+)[ \t]*$', blocks[0], re.M) if len(blocks) == 1 else []
            if values != (['false'] if explicit else ['true']):
                raise Invalid(f'{policy}: incorrect invocation policy')
    roles = {Path(p).stem for p in files if re.fullmatch(r'skills/dev-review/roles/[^/]+\.md', p)}
    if roles != set(ROLES):
        raise Invalid(f'skills/dev-review/roles: expected {sorted(ROLES)}, found {sorted(roles)}')
    for role in ROLES:
        path = f'skills/dev-review/roles/{role}.md'
        fields = frontmatter(files, path)
        if scalar(fields, 'name', path) != role:
            raise Invalid(f'{path}: role name must match filename')
        scalar(fields, 'description', path)
        declared = [item.strip() for item in scalar(fields, 'tools', path).split(',')]
        if len(declared) != len(set(declared)) or not all(declared):
            raise Invalid(f'{path}: duplicate or empty role tools')
        if set(declared) != {'Read', 'Grep', 'Glob', 'Bash'}:
            raise Invalid(f'{path}: unexpected role tools')
    for relative, consumers in SHARED.items():
        canonical = f'skills/{consumers[0]}/{relative}'
        content = files.get(canonical)
        if content is None:
            raise Invalid(f'{canonical}: missing shared file')
        for consumer in consumers[1:]:
            other = f'skills/{consumer}/{relative}'
            if files.get(other) != content:
                raise Invalid(f'{other}: shared file differs from {canonical}; propagate the copy')


def check_links(files):
    for path in sorted(files):
        if not re.match(r'^skills/[^/]+/.+\.md$', path, re.I):
            continue
        text = read(files, path)
        # Only Markdown destinations, not arbitrary paths mentioned in prose or code.
        text = re.sub(r'^(`{3,}|~{3,}).*?^\1[^\n]*$', '', text, flags=re.M | re.S)
        text = re.sub(r'`[^`\n]*`', '', text)
        destinations = re.findall(r'\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)', text)
        destinations += re.findall(r'^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)', text, re.M)
        skill_root = '/'.join(path.split('/')[:2]) + '/'
        for destination in destinations:
            url = urlsplit(destination.strip('<>'))
            if url.scheme or url.netloc or not url.path:
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(url.path)))
            if target != skill_root.rstrip('/') and not target.startswith(skill_root):
                raise Invalid(f'{path}: bundled Markdown resource escapes its skill: {destination}')
            if target not in files and not any(p.startswith(target.rstrip('/') + '/') for p in files):
                raise Invalid(f'{path}: missing local Markdown resource {destination} ({target})')


def check(current):
    check_skills(current)
    check_links(current)
    releases(read(current, 'CHANGELOG.md'), 'CHANGELOG.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true', help='validate index against HEAD')
    parser.add_argument('--base', help='baseline Git commit/tree; requires --head')
    parser.add_argument('--head', help='selected Git commit/tree; requires --base')
    args = parser.parse_args()
    if (args.base is None) != (args.head is None) or (args.staged and args.base is not None):
        parser.error('use either --staged or --base REF --head REF')
    if args.base == '' or args.head == '':
        parser.error('base and head refs must not be empty')
    try:
        os.chdir(os.fsdecode(git('rev-parse', '--show-toplevel')).strip())
        if args.base is not None:
            current = snapshot('tree', tree_ref(args.head))
        else:
            current = snapshot('staged' if args.staged else 'working')
        check(current)
    except (Invalid, OSError, ValueError) as error:
        print(f'skills check: {error}', file=sys.stderr)
        return 1
    print('skills check: passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
