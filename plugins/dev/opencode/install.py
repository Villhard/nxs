#!/usr/bin/env python3
"""Install dev into OpenCode 2: a versioned copy, its skills entry, review subagents and the /plan command."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


PLUGIN = Path(__file__).resolve().parents[1]
HOME = Path.home()
SCHEMA = 'https://opencode.ai/config.json'
MANIFEST = 'nxs/dev-install.json'
SNAPSHOT = 'nxs/dev'
SKILLS = ('rnd', 'bug', 'review', 'commit')
# Claude Code role tools -> OpenCode permission actions.
TOOLS = {
    'Read': 'read', 'Grep': 'grep', 'Glob': 'glob', 'Bash': 'shell',
    'Write': 'edit', 'Edit': 'edit', 'MultiEdit': 'edit',
    'WebFetch': 'webfetch', 'WebSearch': 'websearch',
}
# The host's default secret prompts, restored after the deny-all rule.
ENV_RULES = (('*.env', 'ask'), ('*.env.*', 'ask'), ('*.env.example', 'allow'))


class Stop(Exception):
    pass


def config_dir(arg):
    if arg:
        return Path(arg).expanduser().resolve()
    if os.environ.get('OPENCODE_CONFIG_DIR'):
        return Path(os.environ['OPENCODE_CONFIG_DIR']).expanduser().resolve()
    base = os.environ.get('XDG_CONFIG_HOME') or HOME / '.config'
    return (Path(base).expanduser() / 'opencode').resolve()


def check_opencode():
    binary = shutil.which('opencode')
    if not binary:
        print('warning: opencode is not on PATH; installing without a version check')
        return
    out = subprocess.run([binary, '--version'], capture_output=True, text=True, timeout=60).stdout
    match = re.search(r'(\d+)\.\d+\.\d+', out)
    if not match:
        raise Stop(f'cannot read the OpenCode version from: {out.strip()!r}')
    if match[1] != '2':
        raise Stop(f'OpenCode {match[0]} found; this installer supports OpenCode 2 only')


def frontmatter(path):
    text = path.read_text()
    match = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise Stop(f'{path}: missing frontmatter')
    fields = {}
    for line in match[1].splitlines():
        key, sep, value = line.partition(':')
        if sep and not line.startswith((' ', '\t')):
            fields[key.strip()] = value.strip()
    return fields, text[match.end():]


def unquote(value):
    if len(value) > 1 and value[0] == value[-1] and value[0] in '"\'':
        return value[1:-1]
    return value


def home_form(path):
    try:
        return '~/' + path.relative_to(HOME).as_posix()
    except ValueError:
        return path.as_posix()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot_files():
    files = {}
    for path in sorted(PLUGIN.rglob('*')):
        rel = path.relative_to(PLUGIN)
        if not path.is_file() or '__pycache__' in rel.parts:
            continue
        if any(part.startswith('.') for part in rel.parts):
            continue
        files[f'{SNAPSHOT}/{rel.as_posix()}'] = path.read_bytes()
    return files


def agent_file(path):
    fields, body = frontmatter(path)
    rules = [('*', '*', 'deny')]
    for tool in (item.strip() for item in fields.get('tools', '').split(',')):
        if tool not in TOOLS:
            raise Stop(f'{path}: role tool {tool!r} has no OpenCode permission action')
        action = TOOLS[tool]
        if any(rule == (action, '*', 'allow') for rule in rules):
            continue
        rules.append((action, '*', 'allow'))
        if action == 'read':
            rules += [('read', pattern, effect) for pattern, effect in ENV_RULES]
    lines = ['---', 'description: ' + json.dumps(unquote(fields['description']), ensure_ascii=False),
             'mode: subagent', 'permissions:']
    for action, resource, effect in rules:
        lines += [f'  - action: {json.dumps(action)}', f'    resource: {json.dumps(resource)}',
                  f'    effect: {effect}']
    return ('\n'.join(lines) + '\n---\n' + body).encode()


PLAN_FILE = '\n'.join([
    '---',
    'description: "Plan the given task or ticket with the Plan agent (installed by nxs dev)"',
    'agent: plan',
    '---',
    '$ARGUMENTS',
    '',
]).encode()


# JSONC: blank out comments with spaces so offsets stay valid for byte-exact edits.
def blank_comments(text):
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == '\\' else 1
            out.append(text[i:j + 1])
            i = j + 1
        elif text.startswith('//', i):
            j = text.find('\n', i)
            j = n if j < 0 else j
            out.append(' ' * (j - i))
            i = j
        elif text.startswith('/*', i):
            j = text.find('*/', i + 2)
            if j < 0:
                raise Stop('unterminated block comment')
            out.append(re.sub(r'[^\n]', ' ', text[i:j + 2]))
            i = j + 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def parse_jsonc(text):
    clean = blank_comments(text)
    strict = re.sub(r'("(?:[^"\\]|\\.)*")|,(\s*[}\]])', lambda m: m[1] or m[2], clean)
    return clean, json.loads(strict)


def top_level_value(clean, key):
    """Return the span of the top-level `key` value in an object, or None."""
    depth, i, n = 0, 0, len(clean)
    while i < n:
        c = clean[i]
        if c == '"':
            j = i + 1
            while clean[j] != '"':
                j += 2 if clean[j] == '\\' else 1
            if depth == 1 and json.loads(clean[i:j + 1]) == key:
                rest = clean[j + 1:].lstrip()
                if rest.startswith(':'):
                    start = n - len(rest[1:].lstrip())
                    return start, matching(clean, start)
            i = j + 1
            continue
        if c in '{[':
            depth += 1
        elif c in '}]':
            depth -= 1
        i += 1
    return None


def matching(clean, start):
    if clean[start] not in '{[':
        return start
    depth, i = 0, start
    while True:
        c = clean[i]
        if c == '"':
            i += 1
            while clean[i] != '"':
                i += 2 if clean[i] == '\\' else 1
        elif c in '{[':
            depth += 1
        elif c in '}]':
            depth -= 1
            if depth == 0:
                return i
        i += 1


def config_target(config):
    existing = [config / name for name in ('opencode.json', 'opencode.jsonc') if (config / name).exists()]
    return existing[-1] if existing else config / 'opencode.jsonc'


def add_skills_entry(text, entry):
    """Insert entry into the top-level skills array; return the new text or None when present."""
    if text is None:
        return json.dumps({'$schema': SCHEMA, 'skills': [entry]}, indent=2) + '\n'
    clean, data = parse_jsonc(text)
    if not isinstance(data, dict):
        raise Stop('top-level config value is not an object')
    skills = data.get('skills')
    token = json.dumps(entry)
    if skills is None:
        start = clean.index('{')
        last = clean[start + 1:matching(clean, start)].rstrip()
        at = start + 1 + len(last)
        if not data:
            return text[:at] + f'\n  "skills": [{token}]\n' + text[at:]
        return text[:at] + ('' if last.endswith(',') else ',') + f'\n  "skills": [{token}]' + text[at:]
    if not isinstance(skills, list) or not all(isinstance(item, str) for item in skills):
        raise Stop('config "skills" is not an array of strings')
    if entry in skills:
        return None
    start, end = top_level_value(clean, 'skills')
    last = clean[start + 1:end].rstrip()
    if not last:
        return text[:start + 1] + token + text[end:]
    at = start + 1 + len(last)
    return text[:at] + (' ' if last.endswith(',') else ', ') + token + text[at:]


def remove_skills_entry(text, entry):
    clean, data = parse_jsonc(text)
    if entry not in (data.get('skills') or []):
        return text
    start, end = top_level_value(clean, 'skills')
    token = json.dumps(entry)
    at = clean.index(token, start, end)
    stop = at + len(token)
    after = re.match(r'\s*,', clean[stop:end])
    if after:
        stop += after.end()
    else:
        before = re.search(r',\s*$', clean[start + 1:at])
        if before:
            at = start + 1 + before.start()
    return text[:at] + text[stop:]


def plan_defined(config):
    for name in ('commands/plan.md', 'command/plan.md'):
        if (config / name).exists():
            return name
    for name in ('opencode.json', 'opencode.jsonc'):
        path = config / name
        if path.exists():
            commands = parse_jsonc(path.read_text())[1].get('commands')
            if isinstance(commands, dict) and 'plan' in commands:
                return f'{name} commands.plan'
    return None


def git_state():
    try:
        commit = subprocess.run(['git', '-C', str(PLUGIN), 'rev-parse', 'HEAD'],
                                capture_output=True, text=True, check=True).stdout.strip()
        dirty = bool(subprocess.run(['git', '-C', str(PLUGIN), 'status', '--porcelain', '--', '.'],
                                    capture_output=True, text=True, check=True).stdout.strip())
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


def write(path, data, dry_run, log):
    if path.exists() and path.read_bytes() == data:
        return
    log.append(('update ' if path.exists() else 'create ') + str(path))
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.nxs-tmp')
    temp.write_bytes(data)
    os.replace(temp, path)


def remove(path, dry_run, log):
    log.append(f'remove {path}')
    if not dry_run:
        path.unlink()


def prune(config, dry_run):
    for name in (SNAPSHOT, 'nxs', 'agents/dev', 'commands/dev'):
        path = config / name
        if path.is_dir() and not dry_run:
            for sub in sorted(path.rglob('*'), reverse=True):
                if sub.is_dir() and not any(sub.iterdir()):
                    sub.rmdir()
            if not any(path.iterdir()):
                path.rmdir()


def load_manifest(config):
    path = config / MANIFEST
    return json.loads(path.read_text()) if path.exists() else None


def install(config, dry_run):
    check_opencode()
    if re.search(r'[`$]', str(config)):
        raise Stop(f'unsupported character in config path {config}')
    manifest = load_manifest(config)
    owned = (manifest or {}).get('files', {})
    if manifest is None and (config / SNAPSHOT).exists():
        raise Stop(f'{config / SNAPSHOT} exists but was not installed by this script')
    skills = config / SNAPSHOT / 'skills'
    entry = home_form(skills)
    files = snapshot_files()
    for path in sorted((PLUGIN / 'agents').glob('*.md')):
        files[f'agents/dev/{path.name}'] = agent_file(path)
    plan = 'installed' if 'commands/plan.md' in owned else None
    if plan is None:
        other = plan_defined(config)
        plan = f'skipped: {other} exists' if other else 'installed'
    if plan == 'installed':
        files['commands/plan.md'] = PLAN_FILE

    conflicts = []
    for rel in files:
        path = config / rel
        legacy = config / re.sub(r'^(agent|command)s/', r'\1/', rel)
        for candidate in {path, legacy}:
            if candidate.exists() and digest(candidate.read_bytes()) != owned.get(rel) and \
                    not rel.startswith(SNAPSHOT + '/'):
                conflicts.append(str(candidate))
    if conflicts:
        raise Stop('files not owned by this installer: ' + ', '.join(sorted(set(conflicts))))
    for name in SKILLS:
        for root in (HOME / '.claude/skills', HOME / '.agents/skills', config / 'skills'):
            if (root / name / 'SKILL.md').exists():
                print(f'warning: {root / name} has the same skill ID; the dev skills entry takes precedence')

    target = Path(manifest['config_file']) if manifest else config_target(config)
    original = target.read_text() if target.exists() else None
    updated = add_skills_entry(original, entry)

    log = []
    for rel, data in files.items():
        write(config / rel, data, dry_run, log)
    for rel in owned:
        if rel not in files and (config / rel).exists():
            remove(config / rel, dry_run, log)
    if (config / SNAPSHOT).exists():
        for path in sorted((config / SNAPSHOT).rglob('*')):
            rel = path.relative_to(config).as_posix()
            if path.is_file() and rel not in files:
                remove(path, dry_run, log)
    if updated is not None:
        write(target, updated.encode(), dry_run, log)
    prune(config, dry_run)
    commit, dirty = git_state()
    version = json.loads((PLUGIN / '.claude-plugin/plugin.json').read_text())['version']
    record = {
        'plugin': 'dev', 'version': version, 'source': str(PLUGIN), 'commit': commit, 'dirty': dirty,
        'config_file': str(target),
        'config_created': manifest['config_created'] if manifest else original is None,
        'skills_entry': entry,
        'skills_entry_added': manifest['skills_entry_added'] if manifest else updated is not None,
        'plan_command': plan,
        'files': {rel: digest(data) for rel, data in sorted(files.items())},
    }
    write(config / MANIFEST, (json.dumps(record, indent=2) + '\n').encode(), dry_run, log)
    for line in log:
        print(('would ' if dry_run else '') + line)
    print(f'dev {version} {"would be installed" if dry_run else "installed"} in {config}'
          + ('' if log else ' (no changes)') + f'; /plan: {plan}')
    if not dry_run and log:
        print('Restart OpenCode to load the changes.')


def uninstall(config, dry_run):
    manifest = load_manifest(config)
    if manifest is None:
        raise Stop(f'no dev installation recorded in {config / MANIFEST}')
    log, kept = [], []
    for rel, sha in manifest['files'].items():
        path = config / rel
        if not path.exists():
            continue
        if digest(path.read_bytes()) == sha:
            remove(path, dry_run, log)
        else:
            kept.append(str(path))
    target = Path(manifest['config_file'])
    if manifest['skills_entry_added'] and target.exists():
        text = remove_skills_entry(target.read_text(), manifest['skills_entry'])
        data = parse_jsonc(text)[1]
        if manifest['config_created'] and data in ({'$schema': SCHEMA, 'skills': []}, {'skills': []}):
            remove(target, dry_run, log)
        else:
            write(target, text.encode(), dry_run, log)
    remove(config / MANIFEST, dry_run, log)
    prune(config, dry_run)
    for line in log:
        print(('would ' if dry_run else '') + line)
    for path in kept:
        print(f'kept edited file {path}')
    print(f'dev {"would be removed" if dry_run else "removed"} from {config}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config-dir', help='OpenCode config directory (default: $OPENCODE_CONFIG_DIR, '
                        '$XDG_CONFIG_HOME/opencode or ~/.config/opencode)')
    parser.add_argument('--uninstall', action='store_true', help='remove the files this script installed')
    parser.add_argument('--dry-run', action='store_true', help='print the changes without writing')
    args = parser.parse_args()
    config = config_dir(args.config_dir)
    print(f'OpenCode config: {config}')
    try:
        (uninstall if args.uninstall else install)(config, args.dry_run)
    except (Stop, json.JSONDecodeError) as error:
        print(f'stopped: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
