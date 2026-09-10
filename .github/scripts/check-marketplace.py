#!/usr/bin/env python3
"""Read-only marketplace checks for working files, the index, or two Git trees."""
import argparse
import datetime
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


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


def object_at(files, path):
    try:
        value = json.loads(read(files, path))
    except json.JSONDecodeError as error:
        raise Invalid(f'{path}: malformed JSON: {error}') from error
    if not isinstance(value, dict):
        raise Invalid(f'{path}: expected JSON object')
    return value


def version(value, path):
    match = re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?', str(value))
    if not match:
        raise Invalid(f'{path}: invalid SemVer {value!r}')
    pre = match[4]
    identifiers = []
    for item in pre.split('.') if pre else []:
        if item.isdigit() and len(item) > 1 and item.startswith('0'):
            raise Invalid(f'{path}: invalid SemVer prerelease {value!r}')
        identifiers.append((0, int(item)) if item.isdigit() else (1, item))
    return (*map(int, match.group(1, 2, 3)), pre is None, tuple(identifiers))


def plugin_names(files):
    return {path.split('/')[1] for path in files if path.startswith('plugins/') and len(path.split('/')) > 2}


def releases(text, path):
    entries = []
    for value, date, body in re.findall(r'^## \[([^\]]+)\] - (\d{4}-\d{2}-\d{2})[ \t]*\n(.*?)(?=^## |\Z)', text, re.M | re.S):
        try:
            datetime.date.fromisoformat(date)
        except ValueError as error:
            raise Invalid(f'{path}: invalid release date {date}') from error
        if not any(line.strip() and not line.startswith('#') for line in body.splitlines()):
            raise Invalid(f'{path}: release entry [{value}] has no content')
        entries.append(value)
    return entries


def check(base, current):
    names = plugin_names(current)
    catalog_path = '.claude-plugin/marketplace.json'
    entries = object_at(current, catalog_path).get('plugins')
    if not isinstance(entries, list):
        raise Invalid(f'{catalog_path}: plugins must be an array')
    catalog_names = []
    for item in entries:
        if not isinstance(item, dict) or not isinstance(item.get('name'), str):
            raise Invalid(f'{catalog_path}: plugin entry must have a name')
        name = item['name']
        if item.get('source') != f'./plugins/{name}':
            raise Invalid(f'{catalog_path}: {name}: source must be ./plugins/{name}')
        catalog_names.append(name)
    if len(catalog_names) != len(set(catalog_names)) or set(catalog_names) != names:
        raise Invalid(f'{catalog_path}: catalog membership must match plugin directories (catalog={sorted(catalog_names)}, plugins={sorted(names)})')
    for name in sorted(names):
        prefix = f'plugins/{name}/'
        manifest = prefix + '.claude-plugin/plugin.json'
        codex = prefix + '.codex-plugin/plugin.json'
        changelog = prefix + 'CHANGELOG.md'
        data = object_at(current, manifest)
        if data.get('name') != name:
            raise Invalid(f'{manifest}: name must match directory {name}')
        new_version = data.get('version')
        new = version(new_version, manifest)
        if codex in current:
            other = object_at(current, codex)
            if (other.get('name'), other.get('version')) != (name, new_version):
                raise Invalid(f'{codex}: name/version must match {manifest}')
        release_entries = releases(read(current, changelog), changelog)
        if new_version not in release_entries:
            raise Invalid(f'{changelog}: missing dated ## [{new_version}] release entry')
        if name not in plugin_names(base):
            if new_version != '0.1.0':
                raise Invalid(f'{manifest}: new plugin must start at 0.1.0')
            continue
        old_version = object_at(base, manifest).get('version')
        old = version(old_version, manifest + ' (base)')
        changed = any(base.get(path) != current.get(path) for path in base.keys() | current.keys()
                      if path.startswith(prefix))
        if new < old or (changed and new <= old):
            raise Invalid(f'{manifest}: version must increase for bundled changes and never regress ({old_version} -> {new_version})')
        if new > old and new_version in releases(read(base, changelog), changelog + ' (base)'):
            raise Invalid(f'{changelog}: release entry [{new_version}] must be new relative to base')
    for path in sorted(current):
        if not re.match(r'^plugins/[^/]+/skills/.+\.md$', path, re.I):
            continue
        text = read(current, path)
        # Only Markdown destinations, not arbitrary paths mentioned in prose or code.
        text = re.sub(r'^(`{3,}|~{3,}).*?^\1[^\n]*$', '', text, flags=re.M | re.S)
        text = re.sub(r'`[^`\n]*`', '', text)
        destinations = re.findall(r'\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)', text)
        destinations += re.findall(r'^\s{0,3}\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)', text, re.M)
        for destination in destinations:
            url = urlsplit(destination.strip('<>'))
            if url.scheme or url.netloc or not url.path:
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(path), unquote(url.path)))
            if target not in current and not any(p.startswith(target.rstrip('/') + '/') for p in current):
                raise Invalid(f'{path}: missing local Markdown resource {destination} ({target})')
    if 'dev' in names:
        bars = []
        for skill in ('review', 'fix'):
            path = f'plugins/dev/skills/{skill}/SKILL.md'
            found = re.search(r'^## SEVERITY BAR\n(.*?)(?=^## |\Z)', read(current, path), re.M | re.S)
            if not found or not found[1].strip():
                raise Invalid(f'{path}: missing SEVERITY BAR section')
            bars.append(found[1])
        if bars[0] != bars[1]:
            raise Invalid('plugins/dev/skills/{review,fix}/SKILL.md: SEVERITY BAR sections must match exactly')


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
            base = snapshot('tree', tree_ref(args.base))
            current = snapshot('tree', tree_ref(args.head))
        else:
            base = snapshot('tree', tree_ref('HEAD'))
            current = snapshot('staged' if args.staged else 'working')
        check(base, current)
    except (Invalid, OSError, ValueError) as error:
        print(f'marketplace check: {error}', file=sys.stderr)
        return 1
    print('marketplace check: passed')
    return 0


if __name__ == '__main__':
    sys.exit(main())
