"""Freeze case-disjoint splits and request-only payloads before a future run."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import benchmark as b
from build_case_inventory import case_key


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def partition(rows, seed, development_fraction):
    """Union source cases and exact shared states, including across tasks."""
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    seen = {}
    identities = set()
    for i, row in enumerate(rows):
        key = (row['task'], row['id'])
        if key in identities:
            raise ValueError('Duplicate sample identity')
        identities.add(key)
        if not row.get('group'):
            raise ValueError('Source group is required')
        if b.sha(row['request']) != row['request_sha256']:
            raise ValueError('Request hash mismatch')
        for tag in [('case', case_key(row)), ('state', b.sha(row['request']['state']))]:
            if tag in seen:
                parent[find(i)] = find(seen[tag])
            else:
                seen[tag] = i
    members = {}
    for i, row in enumerate(rows):
        members.setdefault(find(i), []).append((row['task'], row['id']))
    components = {root: b.sha(sorted(keys)) for root, keys in members.items()}
    splits = {}
    for i, row in enumerate(rows):
        component = components[find(i)]
        value = int(b.sha([seed, component])[:16], 16)/2**64
        splits[(row['task'], row['id'])] = ('development' if value < development_fraction else 'test', component)
    return splits


def validate_config(config):
    required = {'study_status', 'seed', 'development_fraction', 'providers', 'primary_metrics',
                'safety_events', 'acceptance_criteria', 'retry_policy', 'max_calls', 'data_status'}
    if not required <= config.keys():
        raise ValueError('Missing protocol fields: '+str(sorted(required-config.keys())))
    if config['study_status'] not in ('prospective', 'retrospective_exploratory'):
        raise ValueError('Invalid study status')
    if not 0 < config['development_fraction'] < 1:
        raise ValueError('development_fraction must be between zero and one')
    if type(config['max_calls']) is not int or config['max_calls'] <= 0:
        raise ValueError('max_calls must be positive')
    if not config['providers'] or any(not v.get('model') for v in config['providers'].values()):
        raise ValueError('Specify model versions for every provider')
    if not config['primary_metrics'] or not config['acceptance_criteria']:
        raise ValueError('Specify metrics and acceptance criteria')
    if config['study_status'] == 'prospective' and config['data_status'] != 'unseen_labels_and_responses':
        raise ValueError('Historical data cannot be declared prospective')


def freeze(input_path, config_path, output):
    config = json.loads(config_path.read_text())
    validate_config(config)
    rows = [json.loads(line) for line in input_path.read_text().splitlines() if line.strip()]
    if not rows:
        raise ValueError('No input records')
    splits = partition(rows, config['seed'], config['development_fraction'])
    counts = Counter(split for split, _ in splits.values())
    if len(counts) != 2:
        raise ValueError('Too few independent components to form both splits')
    # All validation precedes creation; never overwrite a frozen run.
    output.mkdir(parents=True, exist_ok=False)
    files = {}
    config_copy = output/'protocol.json'
    config_copy.write_text(json.dumps(config, ensure_ascii=False, indent=2)+'\n')
    files[config_copy.name] = digest(config_copy)
    for split in ('development', 'test'):
        selected = [row for row in rows if splits[(row['task'], row['id'])][0] == split]
        prepared = output/(split+'.jsonl')
        prepared.write_text(''.join(b.dumps(row)+'\n' for row in selected))
        files[prepared.name] = digest(prepared)
        # Use this file for inference: labels, group IDs and metadata excluded.
        payload = output/(split+'_requests.jsonl')
        payload.write_text(''.join(b.dumps({k: row[k] for k in ('task', 'id', 'request_sha256', 'request')})+'\n' for row in selected))
        files[payload.name] = digest(payload)
    manifest = {'schema_version': 1, 'study_status': config['study_status'],
                'source_sha256': digest(input_path), 'config_sha256': digest(config_path),
                'files': files, 'records': len(rows), 'split_counts': dict(counts),
                'assignment': [{'task': r['task'], 'id': r['id'], 'split': splits[(r['task'], r['id'])][0],
                                'component': splits[(r['task'], r['id'])][1]} for r in rows]}
    (output/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    return manifest


def verify(output):
    manifest = json.loads((output/'manifest.json').read_text())
    config = json.loads((output/'protocol.json').read_text())
    validate_config(config)
    for filename, expected in manifest['files'].items():
        if filename not in {'protocol.json', 'development.jsonl', 'test.jsonl', 'development_requests.jsonl', 'test_requests.jsonl'}:
            raise ValueError('Unexpected manifest path')
        if digest(output/filename) != expected:
            raise ValueError('Frozen file changed: '+filename)
    expected_files = {'protocol.json', 'development.jsonl', 'test.jsonl', 'development_requests.jsonl', 'test_requests.jsonl'}
    if set(manifest['files']) != expected_files:
        raise ValueError('Missing frozen file')
    rows = []; assignments = {}
    for split in ('development', 'test'):
        samples = [json.loads(l) for l in (output/(split+'.jsonl')).read_text().splitlines()]
        payloads = [json.loads(l) for l in (output/(split+'_requests.jsonl')).read_text().splitlines()]
        if payloads != [{k: r[k] for k in ('task', 'id', 'request_sha256', 'request')} for r in samples]:
            raise ValueError('Inference payload differs from frozen input')
        rows.extend(samples)
        for r in samples:
            assignments[(r['task'], r['id'])] = split
    actual = partition(rows, config['seed'], config['development_fraction'])
    declared = {(a['task'], a['id']): (a['split'], a['component']) for a in manifest['assignment']}
    if actual != declared or len(declared) != len(manifest['assignment']) or any(assignments[k] != value[0] for k, value in actual.items()):
        raise ValueError('Split assignment changed')
    if manifest['records'] != len(rows) or manifest['split_counts'] != dict(Counter(assignments.values())) or manifest['study_status'] != config['study_status']:
        raise ValueError('Manifest summary changed')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    make = sub.add_parser('create')
    make.add_argument('--input', type=Path, required=True)
    make.add_argument('--config', type=Path, required=True)
    make.add_argument('--output', type=Path, required=True)
    check = sub.add_parser('verify')
    check.add_argument('output', type=Path)
    args = parser.parse_args()
    manifest = freeze(args.input, args.config, args.output) if args.command == 'create' else verify(args.output)
    print(json.dumps({'records': manifest['records'], 'splits': manifest['split_counts'], 'status': manifest['study_status']}))


if __name__ == '__main__':
    main()
