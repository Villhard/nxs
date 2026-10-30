"""Validate a controlled worker envelope; a done outcome is not verified completion."""
import argparse
import json
from pathlib import Path

from mechanics import contained, load


def validate(value, step_id, allowed_root):
    if not isinstance(value, dict) or set(value) != {'status', 'step_id', 'summary', 'artifacts', 'evidence', 'question', 'reason'}:
        raise ValueError('outcome must contain exactly the documented fields')
    if value['status'] not in ('done', 'needs_input', 'blocked'):
        raise ValueError('invalid outcome status')
    for field in ('step_id', 'summary', 'question', 'reason'):
        if not isinstance(value[field], str):
            raise ValueError(field + ' must be a string')
    if value['step_id'] != step_id or not step_id or not value['summary'].strip():
        raise ValueError('wrong step_id or missing summary')
    if value['status'] == 'needs_input' and not value['question'].strip():
        raise ValueError('needs_input requires a question')
    if value['status'] == 'blocked' and not value['reason'].strip():
        raise ValueError('blocked requires a reason')
    if value['status'] != 'needs_input' and value['question']:
        raise ValueError('question belongs only to needs_input')
    if value['status'] == 'done' and value['reason']:
        raise ValueError('done cannot retain a blocking reason')
    if not isinstance(value['evidence'], list) or any(not isinstance(e, str) or not e.strip() for e in value['evidence']):
        raise ValueError('evidence must be a list of nonempty check descriptions or references')
    artifacts = value['artifacts']
    if not isinstance(artifacts, list) or any(not isinstance(p, str) or not p for p in artifacts):
        raise ValueError('artifacts must be file path strings')
    resolved = [str(contained(allowed_root, p)) for p in artifacts]
    if len(resolved) != len(set(resolved)):
        raise ValueError('duplicate artifact')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('result', type=Path)
    parser.add_argument('--step', required=True)
    parser.add_argument('--root', type=Path, required=True, help='Allowed existing artifact root')
    args = parser.parse_args()
    print(json.dumps(validate(load(args.result), args.step, args.root)))


if __name__ == '__main__':
    main()
