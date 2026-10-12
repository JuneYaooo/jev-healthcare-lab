"""Recompute task performance from raw responses; results rendered in task pages."""
from __future__ import annotations
import argparse
import collections
import json
from pathlib import Path
import statistics

import medical_decision_dataset as data
import run_task_performance as runner

RUN = runner.RUN


def verify(run):
    archive = json.loads((run / 'archive_manifest.json').read_text())
    for filename, sha in archive['files'].items():
        if data.file_sha(run / filename) != sha:
            raise ValueError('Archive hash mismatch: ' + filename)
    config = json.loads((run / 'config.json').read_text())
    manifest = runner.verify_dataset(run / 'dataset')
    if config['smoke'] or config['cells'] != runner.plan(manifest):
        raise ValueError('Incomplete, changed or smoke experiment matrix')
    if config['dataset_manifest_sha256'] != data.file_sha(run / 'dataset/manifest.json') or config['dataset_manifest_sha256'] != data.file_sha(runner.DATASET / 'manifest.json'):
        raise ValueError('Frozen dataset mismatch')
    for filename in ['run_task_performance.py', 'run_performance_evaluation.py', 'run_model_evaluation.py', 'medical_decision_dataset.py']:
        if data.file_sha(run / 'tools' / filename) != data.file_sha(runner.ROOT / 'scripts' / filename):
            raise ValueError('Scoring helper differs from run snapshot: ' + filename)
    if config['runner_sha256'] != data.file_sha(Path(runner.__file__)) or config['pricing'] != runner.metrics.PRICING:
        raise ValueError('Runner or price snapshot mismatch')
    if manifest['source_manifest_sha256'] != data.file_sha(data.DEFAULT / 'manifest.json') or manifest['scope_policy_sha256'] != data.file_sha(data.DEFAULT / 'evaluation_scope.json'):
        raise ValueError('Source dataset or scope changed')
    policy = data.evaluation_policy(data.DEFAULT)
    original = {r['id']: r for r in data.evaluation_rows(data.DEFAULT, True, 'clinical')}
    inputs = list(data.read_jsonl(run / 'dataset/inputs.jsonl'))
    for item in inputs:
        row = original[item['id']]
        if any(row[k] != item[k] for k in ['request', 'gold', 'provenance', 'task']):
            raise ValueError('Clinical input or gold changed')
    for family in manifest['families']:
        source_rows = sorted([r for r in original.values() if policy['tasks'][r['task']]['family'] == family['id']],
                             key=lambda r: data.digest([runner.SEED, r['id']]))[:32]
        if [r['id'] for r in source_rows] != [r['id'] for r in inputs if r['family'] == family['id']]:
            raise ValueError('Task sampling changed')
    packets = list(data.read_jsonl(run / 'dataset/packets.jsonl'))
    reconstructed = []
    for family in manifest['families']:
        rows = [r for r in inputs if r['family'] == family['id']]
        for target in family['batch_targets']:
            reconstructed.extend(runner.pack(rows, family['id'], target))
    if reconstructed != packets:
        raise ValueError('Batch packing differs from frozen source records')
    summaries = json.loads((run / 'summary.json').read_text())
    if len(summaries) != len(config['cells']):
        raise ValueError('Missing completed cells')
    verified = []
    for index, (cell, saved) in enumerate(zip(config['cells'], summaries)):
        if saved['cell'] != index or any(saved[k] != v for k, v in cell.items()):
            raise ValueError('Cell identity mismatch')
        expected = {p['id']: p for p in packets if p['family'] == cell['family'] and p['target'] == cell['batch']}
        records = list(data.read_jsonl(run / saved['records_file']))
        seen = set()
        for record in records:
            uid = record['id']
            if uid not in expected or uid in seen or record['model'] != cell['model'] or record['family'] != cell['family']:
                raise ValueError('Unknown or duplicated response')
            seen.add(uid)
            item = expected[uid]
            if record['request_sha256'] != data.digest(item['request']) or record['provider_request_sha256'] != data.digest(runner.payload(item['request'], cell['model'])):
                raise ValueError('Payload hash mismatch')
            if record['decisions'] != len(item['gold']):
                raise ValueError('Decision count mismatch')
            if min(record['elapsed_s'], record['queue_s']) < 0 or abs(record['completion_s'] - record['elapsed_s'] - record['queue_s']) > 1e-8 or record['completion_s'] > saved['wall_s'] + .001:
                raise ValueError('Invalid timing')
            if 'response' in record:
                evaluated = runner.evaluate(item, record['response'], cell['model'])
                if any(record[k] != v for k, v in evaluated.items()):
                    raise ValueError('Raw response score mismatch')
                if record['status'] != ('success' if evaluated['complete_valid'] else 'invalid_answer'):
                    raise ValueError('Raw response status mismatch')
            elif any(record[k] for k in ['valid_decisions', 'correct_decisions', 'complete_valid', 'all_correct']):
                raise ValueError('Failed request contains positive score')
        if seen != set(expected):
            raise ValueError('Missing response in completed cell')
        computed = runner.metrics.summary(records, saved['wall_s'], cell['model'], len(expected), sum(len(i['gold']) for i in expected.values()))
        if any(saved[k] != v for k, v in computed.items()):
            raise ValueError('Stored summary mismatch')
        verified.append((saved, records))
    return manifest, verified


def aggregate(manifest, verified):
    groups = collections.defaultdict(list)
    families = {f['id']: {**f, 'modes': []} for f in manifest['families']}
    for cell, records in verified:
        groups[(cell['family'], cell['batch'], cell['concurrency'], cell['model'])].append((cell, records))
    for (family, batch, concurrency, model), parts in sorted(groups.items(), key=lambda pair: (*pair[0][:3], runner.MODELS.index(pair[0][3]))):
        records = [r for _, rows in parts for r in rows]
        wall = [c['wall_s'] for c, _ in parts]
        summary = runner.metrics.summary(records, sum(wall), model, sum(c['expected_requests'] for c, _ in parts), sum(c['decisions'] for c, _ in parts))
        families[family]['modes'].append({'batch': batch, 'concurrency': concurrency, 'model': model,
            'repeats': len(parts), **summary, 'mean_batch_wall_s': statistics.mean(wall),
            'median_batch_wall_s': statistics.median(wall), 'wall_per_repeat_s': wall,
            'max_elapsed_s': max(r['elapsed_s'] for r in records),
            'records_files': [c['records_file'] for c, _ in parts],
            'packet_sizes': families[family]['packet_sizes'][str(batch)]})
    return {'dataset_manifest_sha256': data.file_sha(runner.DATASET / 'manifest.json'),
            'models': runner.MODELS, 'repeats': runner.REPEATS, 'families': families,
            'measured_requests': sum(len(rows) for _, rows in verified)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    manifest, verified = verify(RUN)
    result = aggregate(manifest, verified)
    content = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    path = RUN / 'comparison.json'
    if args.check:
        if path.read_text() != content:
            raise ValueError('Stale task comparison')
    else:
        path.write_text(content)
    print(f"Verified {len(verified)} cells / {result['measured_requests']} requests / 26 populated tasks.")


if __name__ == '__main__':
    main()
