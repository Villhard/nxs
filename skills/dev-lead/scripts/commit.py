"""Record commit intent and inspect a known HEAD after response loss. Never commit."""
import argparse
import json
import os
from pathlib import Path

from journal import append_event, read_events
from mechanics import git, git_snapshot
from runner import controller, _identity


def intent(task, operation_id, cwd):
    """Persist before the lead invokes its authorized commit command elsewhere."""
    task = Path(task).resolve()
    operation_id = _identity(operation_id)
    with controller(task):
        key = operation_id + ':commit'
        if any(e['event_id'] == key for e in read_events(task / 'decision.log')):
            raise ValueError('commit intent exists; reconcile without repeating the commit')
        return append_event(task / 'decision.log', key, 'commit.intent',
                            {'cwd': str(Path(cwd).resolve()), 'before': git_snapshot(cwd)})


def reconcile(task, operation_id, cwd):
    """Identify a direct child HEAD with the intended index and unchanged files.

    Matching content identifies an observed result, not who performed the commit.
    Missing, ambiguous or later commits are uncertain and never authorize retries.
    """
    task = Path(task).resolve()
    with controller(task):
        rows = [e for e in read_events(task / 'decision.log') if e['event_id'] == operation_id + ':commit']
        if len(rows) != 1 or rows[0]['kind'] != 'commit.intent':
            raise ValueError('missing commit intent')
        data = rows[0]['data']
        if str(Path(cwd).resolve()) != data['cwd']:
            raise ValueError('commit cwd mismatch')
        current = git_snapshot(cwd)
        before = data['before']
        base = {'head': current['head'], 'git': current, 'replay_safe': False}
        if current['head'] == before['head']:
            return {**base, 'status': 'uncertain', 'reason': 'HEAD unchanged; do not repeat uncertain commit'}
        parents = git(cwd, 'rev-list', '--parents', '-n', '1', current['head']).decode().split()[1:]
        tree = []
        for row in git(cwd, 'ls-tree', '-r', '-z', current['head']).split(b'\0'):
            if row:
                meta, path = row.split(b'\t', 1)
                mode, _, oid = meta.split()
                tree.append([os.fsdecode(path), mode.decode(), oid.decode()])
        if (parents == [before['head']] and sorted(tree) == before['index']
                and current['index'] == before['index'] and current['files'] == before['files']
                and current['branch'] == before['branch']):
            return {**base, 'status': 'committed_observed', 'reason': 'known HEAD matches intended staged tree and parent'}
        return {**base, 'status': 'uncertain', 'reason': 'HEAD or files differ from commit intent; inspect without retry'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['intent', 'reconcile'])
    parser.add_argument('--task', type=Path, required=True)
    parser.add_argument('--operation-id', required=True)
    parser.add_argument('--cwd', type=Path, required=True)
    args = parser.parse_args()
    fn = intent if args.action == 'intent' else reconcile
    print(json.dumps(fn(args.task, args.operation_id, args.cwd)))


if __name__ == '__main__':
    main()
