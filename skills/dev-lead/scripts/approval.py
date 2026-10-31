"""Durable questionnaire transport. The lead interprets answers and chooses every action."""
import argparse
import html
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

from journal import append_event, atomic_json, fsync_directory, lock, read_events
from mechanics import capture, contained, load, sha256
import runner
import status


def _directory(task, question_id):
    return Path(task) / 'research' / 'dev-lead' / 'questions' / runner._identity(question_id)


def _events(task):
    return {r['event_id']: r for r in read_events(Path(task) / 'decision.log')}


def _saved(task, question_id):
    directory = _directory(task, question_id)
    spec = load(directory / 'question.json')
    row = _events(task).get(question_id + ':question', {})
    if (spec['task'] != str(Path(task).resolve()) or spec['question_id'] != question_id
            or row.get('kind') != 'question' or row['data'].get('sha256') != sha256(directory / 'question.json')
            or spec['form_sha256'] != sha256(directory / 'form.html')):
        raise ValueError('question or form differs from its durable evidence')
    return directory, spec


def _form(question):
    escape = html.escape
    fields = []
    for field in question['fields']:
        name = escape(field['name'], quote=True)
        required = ' required' if field['required'] else ''
        if field['options']:
            controls = []
            for number, option in enumerate(field['options']):
                checked = ' checked' if question['purpose'] == 'probe' and number == 0 else ''
                controls.append('<label><input type="radio" name="' + name + '" value="' +
                                escape(option, quote=True) + '"' + required + checked + '>' + escape(option) + '</label>')
            control = ''.join(controls)
        else:
            control = '<textarea name="' + name + '"' + required + '></textarea>'
        fields.append('<fieldset><legend>' + escape(field['label']) + '</legend>' + control + '</fieldset>')
    auto = 'setTimeout(() => form.requestSubmit(), 8000);' if question['purpose'] == 'probe' else ''
    return ('<!doctype html><meta charset="utf-8"><title>Lead questionnaire</title>'
            '<style>body{font:16px system-ui;padding:24px;background:var(--agterm-background,Canvas);'
            'color:var(--agterm-foreground,CanvasText)}label{display:block;margin:12px}fieldset{margin:16px 0}'
            'textarea{width:95%;min-height:5em}button{padding:10px 20px}</style><h1>' +
            ('Presentation probe - no approval' if question['purpose'] == 'probe' else 'Lead question') +
            '</h1><p>' + escape(question['text']) + '</p><form id="answers">' + ''.join(fields) +
            '<button type="submit">Submit answers</button></form><script>'
            'const form=document.getElementById("answers");'
            'form.addEventListener("submit",async event=>{event.preventDefault();'
            'await agterm.request("session.overlay.submit",{args:{value:JSON.stringify('
            'Object.fromEntries(new FormData(form)))}});});' + auto + '</script>\n')


def prepare(task, question_id, question, identity):
    task = status._owner(task)
    identity, _ = runner._checked_agterm(identity, 5)
    required = {'text', 'step_id', 'purpose', 'scope', 'artifact', 'fields', 'worker_run'}
    if (not isinstance(question, dict) or set(question) != required
            or question['purpose'] not in ('decision', 'probe')
            or any(not isinstance(question[k], str) or not question[k] for k in ('text', 'step_id', 'scope'))
            or not isinstance(question['fields'], list) or not question['fields']):
        raise ValueError('explicit question text, step, purpose, scope and fields required')
    names = set()
    for field in question['fields']:
        if (not isinstance(field, dict) or set(field) != {'name', 'label', 'options', 'required'}
                or not isinstance(field['name'], str) or not field['name'] or field['name'] in names
                or not isinstance(field['label'], str) or type(field['required']) is not bool
                or not isinstance(field['options'], list)
                or any(not isinstance(s, str) or not s for s in field['options'])
                or len(set(field['options'])) != len(field['options'])):
            raise ValueError('distinct named text/choice fields with explicit required flags expected')
        names.add(field['name'])
    artifact = question['artifact']
    if artifact is not None:
        if (not isinstance(artifact, dict) or set(artifact) != {'path', 'sha256'}
                or sha256(contained(task, artifact['path'])) != artifact['sha256']):
            raise ValueError('question artifact hash mismatch')
    if question['purpose'] == 'probe' and artifact is not None:
        raise ValueError('a presentation probe cannot request artifact approval')
    origin = question['worker_run']
    if origin is not None:
        runner._identity(origin)
        prior = runner.reconcile(task / 'research' / 'dev-lead' / 'runs' / origin)
        if prior['status'] != 'needs_input' or not prior.get('session_id'):
            raise ValueError('worker question requires a reconciled exact needs_input session')
    rows = _events(task)
    for row in rows.values():
        other = row['data'].get('ui_question_id') if row['kind'] == 'question' else None
        if other and not any(other + suffix in rows for suffix in (':used', ':dismissed')):
            raise ValueError('reconcile and consume the existing questionnaire before another round')
    directory = _directory(task, question_id)
    directory.mkdir(parents=True)
    fsync_directory(directory.parent)
    status._text(directory / 'form.html', _form(question))
    spec = {'task': str(task), 'question_id': question_id, 'identity': identity,
            'question': question, 'form_sha256': sha256(directory / 'form.html')}
    if origin is not None:
        prior_spec = load(task / 'research' / 'dev-lead' / 'runs' / origin / 'spec.json')
        spec['origin'] = {'run_id': origin, 'harness': prior_spec['harness'], 'session_id': prior['session_id']}
    atomic_json(directory / 'question.json', spec)
    append_event(task / 'decision.log', question_id + ':question', 'question',
                 {'ui_question_id': question_id, 'question': question['text'], 'step_id': question['step_id'],
                  'artifact': str((directory / 'question.json').relative_to(task)),
                  'sha256': sha256(directory / 'question.json')})
    return {'status': 'prepared', 'question_id': question_id, 'directory': str(directory)}


def _command(directory, spec):
    identity = spec['identity']
    return [identity['cli'], 'session', 'overlay', 'open', '--html', str(directory / 'form.html'),
            '--js', '--block', '--follow', '--target', identity['session_id'],
            '--window', identity['window_id'], '--socket', identity['socket'], '--json']


def _check_slot(task, spec):
    runner._checked_agterm(spec['identity'], 5)
    node = status._node(spec['identity'])
    if status._occupied(node):
        raise ValueError('existing overlay or ask owns the UI')
    if node.get('hud'):
        cache_path = status._directory(task) / 'presentation.json'
        cache = load(cache_path) if cache_path.exists() else {}
        owned = [r['data']['hud'] for r in _events(task).values()
                 if r['kind'] == 'hud.owned' and r['data']['identity'] == spec['identity']]
        if not ((cache.get('identity') == spec['identity'] and cache.get('owned_hud') == node['hud'])
                or (owned and owned[-1] == node['hud'])):
            raise ValueError('questionnaire cannot replace an unowned HUD')


def open(task, question_id, timeout):
    """Start exactly one bounded CLI waiter. Caller retains/reaps the returned Popen handle."""
    task = status._owner(task)
    if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('finite positive waiter timeout required')
    directory, spec = _saved(task, question_id)
    key = question_id + ':open'
    if key in _events(task):
        raise ValueError('question open intent exists; reconcile without reopening')
    _check_slot(task, spec)
    wait_directory = directory / 'wait'
    wait_directory.mkdir()
    append_event(task / 'decision.log', key, 'question.open.intent',
                 {'ui_question_id': question_id, 'command': _command(directory, spec), 'timeout': timeout,
                  'question_sha256': sha256(directory / 'question.json')})
    command = [sys.executable, str(Path(__file__).resolve()), 'wait', '--question',
               str(directory / 'question.json'), '--timeout', str(timeout)]
    with (wait_directory / 'wrapper.stdout').open('wb') as out, (wait_directory / 'wrapper.stderr').open('wb') as err:
        try:
            process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=out, stderr=err, start_new_session=True)
        except OSError as error:
            atomic_json(wait_directory / 'error.json', {'command': command, 'error': str(error)})
            raise
    atomic_json(wait_directory / 'launch.json', {'pid': process.pid, 'command': command})
    return process


def _wait(path, timeout):
    spec = load(path)
    task, question_id = Path(spec['task']), spec['question_id']
    directory, spec = _saved(task, question_id)
    intent = _events(task).get(question_id + ':open', {})
    if (intent.get('kind') != 'question.open.intent' or intent['data']['timeout'] != timeout
            or intent['data']['command'] != _command(directory, spec)):
        raise ValueError('matching durable question open intent required')
    with lock(directory / 'wait.lock'):
        # Like the runner claim, this durable exclusive file survives process death.
        with (directory / 'wait' / 'claim').open('x') as stream:
            stream.write(str(os.getpid()) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        fsync_directory(directory / 'wait')
        atomic_json(directory / 'wait' / 'waiter.json', {'pid': os.getpid(), 'started': time.time()})
        try:
            _check_slot(task, spec)
            capture(_command(directory, spec), str(directory), directory / 'wait', timeout, terminal=False)
        except (OSError, ValueError) as error:
            atomic_json(directory / 'wait' / 'error.json', {'error': str(error)})
            raise


def _json(text):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError('duplicate JSON key in page reply: ' + key)
            value[key] = item
        return value
    return json.loads(text, object_pairs_hook=unique)


def parse_outcome(response, expected_page=None, *, direct=False):
    """Direct shape is permitted only for explicitly non-JSON blocking-open captures."""
    try:
        raw = _json(response['stdout'])
        if direct:
            outcome = raw
        else:
            if not isinstance(raw, dict) or raw.get('ok') is not True:
                raise ValueError('agterm page query failed: ' + str(raw))
            if (set(raw) != {'ok', 'result'} or not isinstance(raw['result'], dict)
                    or set(raw['result']) != {'pageOutcome'}):
                raise ValueError('ambiguous page reply envelope')
            outcome = raw['result']['pageOutcome']
        if not isinstance(outcome, dict) or set(outcome) - {'pageID', 'outcome', 'value'}:
            raise ValueError('invalid page outcome shape')
        page = runner._uuid(outcome['pageID'])
        if expected_page is not None and page != runner._uuid(expected_page):
            raise ValueError('page outcome identity mismatch')
        name = outcome['outcome']
        if name not in ('pending', 'submitted', 'dismissed'):
            raise ValueError('unknown page outcome')
        if response['exit_code'] != {'pending': 1, 'submitted': 0, 'dismissed': 2}[name]:
            raise ValueError('page outcome and CLI exit disagree')
        if name == 'submitted':
            if not isinstance(outcome.get('value'), str):
                raise ValueError('submitted page value must be a JSON string')
            value = _json(outcome['value'])
            if not isinstance(value, dict):
                raise ValueError('page answers must be an object')
        elif 'value' in outcome:
            raise ValueError('unsubmitted page cannot carry an answer')
        return {**outcome, 'pageID': page}
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError('malformed page reply: ' + str(response)) from error


def _answers(spec, outcome):
    value = json.loads(outcome['value'])
    fields = {f['name']: f for f in spec['question']['fields']}
    if set(value) - set(fields):
        raise ValueError('unknown answer field')
    for name, field in fields.items():
        answer = value.get(name, '')
        if (not isinstance(answer, str) or (field['required'] and not answer.strip())
                or (answer and field['options'] and answer not in field['options'])):
            raise ValueError('missing or invalid answer: ' + name)
    return value


def _record(task, directory, spec, response, page):
    outcome = parse_outcome(response, page)
    question_id = spec['question_id']
    if outcome['outcome'] == 'pending':
        return {'status': 'pending', 'page_id': outcome['pageID']}
    if outcome['outcome'] == 'dismissed':
        append_event(task / 'decision.log', question_id + ':dismissed', 'question.dismissed',
                     {'question_id': question_id, 'page_id': outcome['pageID']})
        return {'status': 'dismissed', 'page_id': outcome['pageID']}
    value = _answers(spec, outcome)
    receipt = {'response': response, 'page_id': outcome['pageID'],
               'question_sha256': sha256(directory / 'question.json')}
    if (directory / 'receipt.json').exists() and load(directory / 'receipt.json') != receipt:
        # A query may have different argv/formatting, but must attest the same submitted value.
        old = load(directory / 'receipt.json')
        if parse_outcome(old['response'], outcome['pageID']) != outcome:
            raise ValueError('conflicting submitted answer evidence')
    else:
        atomic_json(directory / 'receipt.json', receipt)
    answer = {'question_id': question_id, 'page_id': outcome['pageID'], 'value': value,
              'purpose': spec['question']['purpose'], 'question_sha256': sha256(directory / 'question.json')}
    if (directory / 'answer.json').exists() and load(directory / 'answer.json') != answer:
        raise ValueError('conflicting durable answer')
    atomic_json(directory / 'answer.json', answer)
    append_event(task / 'decision.log', question_id + ':answer', 'answer',
                 {'question_id': question_id, 'answer': value, 'page_id': outcome['pageID'],
                  'purpose': spec['question']['purpose'], 'sha256': sha256(directory / 'answer.json')})
    return {'status': 'submitted', 'answer': answer, 'page_id': outcome['pageID']}


def poll(task, question_id):
    """Observe one question and journal an answer once; never approve, reopen or continue."""
    task = status._owner(task)
    directory, spec = _saved(task, question_id)
    rows = _events(task)
    report = {'question_id': question_id, 'status': 'uncertain', 'updated': time.time(), 'replay_safe': False}
    try:
        page_event = rows.get(question_id + ':page')
        page = page_event['data']['page_id'] if page_event else None
        answer_event = rows.get(question_id + ':answer')
        if answer_event:
            if sha256(directory / 'answer.json') != answer_event['data']['sha256']:
                raise ValueError('answer differs from durable event')
            report.update(status='consumed' if question_id + ':used' in rows else 'submitted',
                          answer=load(directory / 'answer.json'), page_id=answer_event['data']['page_id'])
        elif question_id + ':dismissed' in rows:
            report.update(status='dismissed', page_id=rows[question_id + ':dismissed']['data']['page_id'])
        elif (directory / 'receipt.json').exists():
            receipt = load(directory / 'receipt.json')
            if receipt['question_sha256'] != sha256(directory / 'question.json'):
                raise ValueError('receipt question hash mismatch')
            report.update(_record(task, directory, spec, receipt['response'], page or receipt['page_id']))
        else:
            if question_id + ':open' not in rows:
                report['status'] = 'prepared'
            else:
                exit_path = directory / 'wait' / 'exit.json'
                if exit_path.exists():
                    exit_record = load(exit_path)
                    report['wait_exit'] = exit_record
                    if exit_record['command'] != _command(directory, spec):
                        raise ValueError('wait command differs from open intent')
                    if not exit_record['timed_out'] and exit_record['exit_code'] in (0, 2):
                        response = {**exit_record, 'stdout': (directory / 'wait' / 'stdout').read_text(),
                                    'stderr': (directory / 'wait' / 'stderr').read_text()}
                        report.update(_record(task, directory, spec, response, page))
                    elif not exit_record['timed_out']:
                        report['wait_error'] = {**exit_record, 'stdout': (directory / 'wait' / 'stdout').read_text(),
                                                'stderr': (directory / 'wait' / 'stderr').read_text()}
                if report['status'] == 'uncertain':
                    node = status._node(spec['identity'])
                    matches = [p for p in node.get('htmlOverlays', [])
                               if p.get('file') == str(directory / 'form.html')]
                    if len(matches) > 1:
                        raise ValueError('ambiguous questionnaire page association')
                    if matches:
                        found = runner._uuid(matches[0]['id'])
                        if page and page != found:
                            raise ValueError('questionnaire page identity changed')
                        page = found
                        append_event(task / 'decision.log', question_id + ':page', 'question.page.observed',
                                     {'question_id': question_id, 'page_id': page})
                    if page:
                        identity = spec['identity']
                        command = [identity['cli'], 'session', 'overlay', 'result', '--page', page,
                                   '--window', identity['window_id'], '--socket', identity['socket'], '--json']
                        response = runner._ipc(command, 5)
                        atomic_json(directory / 'observation.json', response)
                        report.update(_record(task, directory, spec, response, page))
                    else:
                        error = report.get('wait_error', {})
                        report['reason'] = (error.get('spawn_error') or error.get('stderr') or error.get('stdout')
                                            or 'open effect unknown; inspect waiter and page before any retry')
        for name in ('waiter.json', 'process.json'):
            path = directory / 'wait' / name
            if path.exists():
                record = load(path)
                report[name] = {**record, 'pid_present': runner._pid_present(record['pid']),
                                'group_present': runner._group_present(record['pid'])}
        if (directory / 'wait' / 'error.json').exists():
            report['waiter_error'] = load(directory / 'wait' / 'error.json')
            if report['status'] == 'uncertain':
                report['reason'] = report['waiter_error']['error']
    except (ValueError, OSError, KeyError) as error:
        report.update(status='uncertain', reason=str(error))
    atomic_json(directory / 'state.json', report)
    return report


def reconcile(task, question_id):
    return poll(task, question_id)


def consume(task, question_id, decision_event_id):
    task = status._owner(task)
    result = poll(task, question_id)
    if result['status'] not in ('submitted', 'consumed'):
        raise ValueError('a durable submitted answer is required before consumption')
    rows = _events(task)
    decision = rows.get(decision_event_id, {})
    data = decision.get('data', {})
    if (data.get('question_id') != question_id or data.get('answer_event_id') != question_id + ':answer'
            or decision.get('kind') not in ('decision', 'approval', 'probe.observed')):
        raise ValueError('explicit lead decision must reference the exact question and answer event')
    if result['answer']['purpose'] == 'probe' and decision['kind'] != 'probe.observed':
        raise ValueError('probe answers cannot grant feature approval or drive a workflow decision')
    if decision['kind'] == 'approval':
        _, spec = _saved(task, question_id)
        artifact = spec['question']['artifact']
        if (artifact is None or data.get('plan_sha256') != artifact['sha256']
                or data.get('artifact') != artifact['path'] or data.get('scope') != spec['question']['scope']
                or sha256(contained(task, artifact['path'])) != artifact['sha256']):
            raise ValueError('approval must pin the exact current question artifact and scope')
    append_event(task / 'decision.log', question_id + ':used', 'answer.used',
                 {'question_id': question_id, 'answer_event_id': question_id + ':answer',
                  'decision_event_id': decision_event_id})
    return poll(task, question_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    wait = sub.add_parser('wait', help='One intent-bound bounded page wait, never a coordinator')
    wait.add_argument('--question', type=Path, required=True)
    wait.add_argument('--timeout', type=float, required=True)
    args = parser.parse_args()
    _wait(args.question, args.timeout)
