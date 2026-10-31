"""Standalone durable task journal. JSONL is authoritative; state.json is a cache."""
import argparse
import contextlib
import fcntl
import json
import os
from pathlib import Path
import tempfile
import time


def fsync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_json(path, value):
    """Replace a JSON file, syncing both contents and its directory."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream, sort_keys=True, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        fsync_directory(path.parent)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextlib.contextmanager
def lock(path, blocking=False):
    """OS ownership, released on death. Never unlink a lock file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def state_directory(path):
    return Path(path).parent / 'research' / 'dev-lead'


def journal_lock(path):
    return state_directory(path) / 'decision.lock'


def _read_events(path):
    """Fail closed on torn, conflicting or malformed records; never truncate history."""
    path = Path(path)
    if not path.exists():
        return []
    rows, seen = [], set()
    for line in path.read_bytes().splitlines(keepends=True):
        if not line.endswith(b'\n'):
            raise ValueError('incomplete journal record; reconcile before writing')
        row = json.loads(line)
        if (not isinstance(row, dict) or set(row) != {'event_id', 'kind', 'data'}
                or not isinstance(row['event_id'], str) or not row['event_id']
                or not isinstance(row['kind'], str) or not row['kind']
                or not isinstance(row['data'], dict) or row['event_id'] in seen):
            raise ValueError('invalid or duplicate journal record')
        seen.add(row['event_id'])
        rows.append(row)
    return rows


def read_events(path):
    """Read a consistent journal while concurrent copies append."""
    path = Path(path)
    with lock(journal_lock(path), blocking=True):
        return _read_events(path)


def _cache(path, rows):
    state = {'last_event_id': rows[-1]['event_id'] if rows else None, 'events': rows}
    atomic_json(state_directory(path) / 'journal-state.json', state)
    return state


def append_event(path, event_id, kind, data):
    """Append exactly once; retrying an identical ID/content only repairs the cache."""
    path = Path(path)
    if (not isinstance(event_id, str) or not event_id or not isinstance(kind, str)
            or not kind or not isinstance(data, dict)):
        raise ValueError('event_id, kind and object data are required')
    with lock(journal_lock(path), blocking=True):
        rows = _read_events(path)
        previous = next((r for r in rows if r['event_id'] == event_id), None)
        stamped = dict(data)
        stamped.setdefault('timestamp', previous['data'].get('timestamp') if previous else time.time())
        row = {'event_id': event_id, 'kind': kind, 'data': stamped}
        raw = (json.dumps(row, sort_keys=True, allow_nan=False) + '\n').encode()
        for old in rows:
            if old['event_id'] == event_id:
                if (json.dumps(old, sort_keys=True, allow_nan=False) + '\n').encode() != raw:
                    raise ValueError('event ID reused with different content')
                _cache(path, rows)
                return old
        with path.open('ab') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        fsync_directory(path.parent)
        rows.append(row)
        _cache(path, rows)
    return row


def recover_state(path):
    """Rebuild after a crash between durable append and atomic cache replacement."""
    path = Path(path)
    with lock(journal_lock(path), blocking=True):
        return _cache(path, _read_events(path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    add = sub.add_parser('append', help='Append an idempotent semantic event and sync state')
    add.add_argument('journal', type=Path)
    add.add_argument('event_id')
    add.add_argument('kind')
    add.add_argument('data', help='JSON object')
    recover = sub.add_parser('recover', help='Rebuild state cache from authoritative JSONL')
    recover.add_argument('journal', type=Path)
    args = parser.parse_args()
    value = (append_event(args.journal, args.event_id, args.kind, json.loads(args.data))
             if args.action == 'append' else recover_state(args.journal))
    print(json.dumps(value))


if __name__ == '__main__':
    main()
