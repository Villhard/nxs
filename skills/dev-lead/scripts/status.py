"""Lead-owned progress and HUD presentation. Never accept work or choose an action."""
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import tempfile
import time
import uuid

from journal import append_event, atomic_json, fsync_directory, read_events
from mechanics import load
import runner


def _owner(task):
    task = Path(task).resolve(strict=True)
    if task not in getattr(runner._owners, 'tasks', set()):
        raise ValueError('visibility requires the held lifetime controller in this thread')
    return task


def _directory(task):
    return Path(task) / 'research' / 'dev-lead'


def _text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        fsync_directory(path.parent)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def _node(identity):
    _, sessions = runner._agterm_tree(identity, timeout=5)
    return sessions[identity['session_id']][1]


def _occupied(node):
    return any(node.get(key) for key in ('overlay', 'htmlOverlays', 'paneOverlays', 'ask'))


def _intended_matches(hud, intended):
    return (isinstance(hud, dict) and isinstance(intended, dict)
            and all(hud.get(k) == v for k, v in intended.items())
            and not any(hud.get(k) for k in ('pane', 'textColor')))


def _pending(rows):
    return [r['data']['ui_question_id'] for r in rows if r['kind'] == 'question.open.intent'
            and not any(e['event_id'] in (r['data']['ui_question_id'] + ':answer',
                                         r['data']['ui_question_id'] + ':dismissed') for e in rows)]


def _progress(value, rows):
    fields = {'stage', 'step_id', 'action', 'reason', 'current_run', 'accepted_tickets', 'last_commit'}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError('explicit progress fields required')
    if any(not isinstance(value[k], str) or not value[k] for k in ('stage', 'step_id', 'action')):
        raise ValueError('stage, step_id and action must be nonempty text')
    if not isinstance(value['reason'], str) or not isinstance(value['accepted_tickets'], list):
        raise ValueError('text reason and accepted ticket list required')
    events = {r['event_id']: r for r in rows}
    seen = set()
    for item in value['accepted_tickets']:
        if (not isinstance(item, dict) or set(item) != {'ticket', 'event_id'}
                or any(not isinstance(item[k], str) or not item[k] for k in ('ticket', 'event_id'))):
            raise ValueError('accepted ticket requires ticket path and acceptance event_id')
        row = events.get(item['event_id'], {})
        if (item['ticket'] in seen or row.get('kind') != 'ticket.implementation.accepted'
                or row['data'].get('ticket') != item['ticket'] or not row['data'].get('evidence')):
            raise ValueError('distinct tickets and explicit lead acceptance evidence required')
        seen.add(item['ticket'])
    commit = value['last_commit']
    if commit is not None:
        if (not isinstance(commit, dict) or set(commit) != {'head', 'event_id'}
                or any(not isinstance(commit[k], str) or not commit[k] for k in ('head', 'event_id'))):
            raise ValueError('last_commit requires head and checkpoint event_id')
        row = events.get(commit['event_id'], {})
        if (row.get('kind') != 'ticket.checkpoint.accepted' or row['data'].get('head') != commit['head']
                or not row['data'].get('evidence')):
            raise ValueError('last_commit requires explicit lead checkpoint evidence')
    if value['current_run'] is not None:
        if not isinstance(value['current_run'], str):
            raise ValueError('current_run must be an exact run ID or None')
        runner._identity(value['current_run'])
    return value


def adopt_hud(task, event_id, identity, observed_hud):
    """Lead explicitly identifies its own manual HUD by its complete observed spec."""
    task = _owner(task)
    identity, _ = runner._checked_agterm(identity, 5)
    node = _node(identity)
    if _occupied(node) or not observed_hud or node.get('hud') != observed_hud:
        raise ValueError('HUD adoption requires the exact unobstructed observed specification')
    return append_event(task / 'decision.log', event_id, 'hud.owned',
                        {'identity': identity, 'hud': observed_hud})


def publish(task, event_id, progress, identity):
    task = _owner(task)
    rows = read_events(task / 'decision.log')
    _progress(progress, rows)
    # No UI effect precedes the durable semantic transition.
    append_event(task / 'decision.log', event_id, 'progress.changed',
                 {'progress': progress, 'identity': identity, 'step_id': progress['step_id']})
    return refresh(task, identity)


def finish(task, event_id, identity):
    """End presentation explicitly; keep final progress and ownership evidence."""
    task = _owner(task)
    rows = read_events(task / 'decision.log')
    changes = [r for r in rows if r['kind'] == 'progress.changed']
    if not changes or changes[-1]['data']['identity'] != identity:
        raise ValueError('publish final progress for this lead before finishing')
    change = changes[-1]
    progress = _progress(change['data']['progress'], rows)
    if progress['current_run'] is not None or _pending(rows):
        raise ValueError('finish requires no current run or pending questionnaire')
    append_event(task / 'decision.log', event_id, 'hud.finished',
                 {'identity': identity, 'progress_event_id': change['event_id']})
    return refresh(task, identity)


def _short(text):
    return ''.join(c if c.isprintable() else ' ' for c in text)[:256]


def _utc(stamp):
    return datetime.fromtimestamp(stamp, timezone.utc).isoformat(timespec='seconds')


def refresh(task, identity):
    """One bounded presentation tick; return diagnostics for the lead to report."""
    task = _owner(task)
    rows = read_events(task / 'decision.log')
    changes = [r for r in rows if r['kind'] == 'progress.changed']
    if not changes:
        raise ValueError('publish explicit progress before refreshing')
    change = changes[-1]
    if change['data']['identity'] != identity:
        raise ValueError('progress belongs to another recorded lead identity')
    progress = _progress(change['data']['progress'], rows)
    finished = [r for r in rows if r['kind'] == 'hud.finished'
                and r['data']['identity'] == identity
                and r['data']['progress_event_id'] == change['event_id']]
    directory = _directory(task)
    cache = load(directory / 'presentation.json') if (directory / 'presentation.json').exists() else {}
    stamp, tick = time.time(), time.monotonic()
    report = {'event_id': change['event_id'], 'identity': identity, 'updated': stamp,
              'semantic_changed': change['data']['timestamp'], 'monotonic': tick,
              'progress': progress, 'ui': 'suppressed', 'reason': '', 'stale': []}
    if not finished and 0 < cache.get('monotonic', tick) < tick - 60:
        report['stale'].append('active presentation polling exceeded 60 seconds')
    run = progress['current_run']
    if run is not None:
        spec = directory / 'runs' / run / 'spec.json'
        if not spec.exists() or load(spec).get('run_id') != run:
            report['stale'].append('current run evidence missing or mismatched')
    if progress['last_commit'] is not None:
        try:
            head = subprocess.run(['git', '-C', str(task), 'rev-parse', 'HEAD'], check=True,
                                  capture_output=True, timeout=5).stdout.decode().strip()
            if head != progress['last_commit']['head']:
                report['stale'].append('HEAD differs from last verified checkpoint')
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            report['stale'].append(str(error))
    ownership = [r for r in rows if r['kind'] == 'hud.owned' and r['data']['identity'] == identity]
    ownership_id = ownership[-1]['event_id'] if ownership else None
    owned = (cache.get('owned_hud') if cache.get('identity') == identity
             and cache.get('ownership_event_id') == ownership_id else None)
    if owned is None and ownership:
        owned = ownership[-1]['data']['hud']
    report['owned_hud'] = owned
    report['ownership_event_id'] = ownership_id
    try:
        identity, _ = runner._checked_agterm(identity, 5)
        node = _node(identity)
        if _pending(rows):
            report['reason'] = 'owned questionnaire pending reconciliation'
        elif _occupied(node):
            report['reason'] = 'existing overlay or ask owns the UI'
        elif finished:
            intent_id = finished[-1]['event_id'] + ':close'
            if not node.get('hud'):
                report['ui'] = 'cleared'
            elif node['hud'] != owned:
                report['reason'] = 'HUD ownership changed or unknown'
            elif any(r['event_id'] == intent_id for r in rows):
                report.update(ui='uncertain', reason='HUD close not confirmed; observe without replay')
            else:
                command = [identity['cli'], 'session', 'hud', 'close',
                           '--target', identity['session_id'], '--window', identity['window_id'],
                           '--socket', identity['socket'], '--json']
                append_event(task / 'decision.log', intent_id, 'hud.close.intent',
                             {'identity': identity, 'hud': owned, 'command': command})
                report['response'] = runner._ipc(command, 5)
                runner._reply(report['response'])
                if _node(identity).get('hud'):
                    raise ValueError('HUD close not confirmed by the pinned tree')
                report['ui'] = 'cleared'
        elif (node.get('hud') and node['hud'] != owned
              and not (cache.get('ui') != 'visible' and _intended_matches(node['hud'], cache.get('intended_hud')))):
            report['reason'] = 'HUD ownership changed or unknown'
        else:
            message = _short(progress['stage'] + ' / ' + progress['step_id'] + ': ' + progress['action'])
            detail = _short(_utc(stamp) + ' | ' + (progress['reason'] or run or 'active'))
            # Persist intended presentation before IPC; a lost response is observed, not replayed here.
            intended = {'message': message, 'detail': detail, 'position': 'top-right', 'spinner': 'dot',
                        'hideAfter': 0, 'markdown': False, 'sticky': False, 'frame': True}
            for fixed in ('fontSize', 'backgroundColor'):
                if fixed in (node.get('hud') or {}):
                    intended[fixed] = node['hud'][fixed]
            report['intended_hud'] = intended
            atomic_json(directory / 'presentation.json', report)
            verb = 'update' if node.get('hud') else 'open'
            command = [identity['cli'], 'session', 'hud', verb, message, '--detail', detail,
                       '--position', 'top-right', '--spinner-style', 'dot',
                       '--target', identity['session_id'], '--window', identity['window_id'],
                       '--socket', identity['socket'], '--json']
            response = runner._ipc(command, 5)
            report['response'] = response
            runner._reply(response)
            observed = _node(identity).get('hud')
            if not observed or any(observed.get(k) != v for k, v in intended.items()):
                raise ValueError('HUD write not confirmed by the pinned tree')
            report.update(ui='visible', reason='', owned_hud=observed)
            if not ownership or ownership[-1]['data']['hud'] != observed:
                event_id = change['event_id'] + ':hud-owned:' + uuid.uuid4().hex
                row = append_event(task / 'decision.log', event_id, 'hud.owned',
                                   {'identity': identity, 'hud': observed})
                report['ownership_event_id'] = row['event_id']
    except (OSError, ValueError, KeyError) as error:
        report.update(ui='error', reason=str(error))
    atomic_json(directory / 'presentation.json', report)
    lines = ['# Lead status', '', 'Updated (UTC): ' + _utc(stamp),
             'Semantic change (UTC): ' + _utc(report['semantic_changed']), '',
             'Stage: ' + progress['stage'], 'Ticket/step: ' + progress['step_id'],
             'Action: ' + progress['action'], 'Waiting/blocker: ' + (progress['reason'] or 'none'),
             'Accepted tickets: ' + str(len(progress['accepted_tickets'])),
             'Accepted IDs: ' + (', '.join(i['ticket'] for i in progress['accepted_tickets']) or 'none'),
             'Current run: ' + (run or 'none'),
             'Last verified commit: ' + (progress['last_commit']['head'] if progress['last_commit'] else 'unknown'),
             'Presentation: ' + report['ui'] + (' - ' + report['reason'] if report['reason'] else ''),
             'Reconciliation: ' + ('; '.join(report['stale']) or 'no stale references observed'), '']
    _text(directory / 'status.md', '\n'.join(lines))
    return report


def reconcile(task, identity):
    """Rebuild semantics from the journal and observe UI before restoring an owned HUD."""
    return refresh(task, identity)
