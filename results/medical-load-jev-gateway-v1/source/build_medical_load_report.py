"""Recompute the task comparison from frozen requests, raw responses and timestamps."""
from __future__ import annotations
import argparse
from collections import defaultdict, deque
import gzip
import json
import math
from pathlib import Path
import statistics

import run_medical_load as run


def read_rows(path):
    if not path.exists():
        return []
    with gzip.open(path, 'rt') as stream:
        return [json.loads(line) for line in stream]


def percentile(values, p=.95):
    return sorted(values)[math.ceil(len(values)*p)-1] if values else None


def validate(row, items):
    item = items[row['item_id']]
    expected = run.choices(item, row.get('response', {}), row['model']) if row['http_status'] == 200 else {}
    if row['predicted'] != expected or row['correct'] != sum(v == item['gold'][k] for k, v in expected.items()):
        raise ValueError('Raw response score mismatch')
    if row['valid'] != len(expected) or row['decisions'] != len(item['gold']):
        raise ValueError('Decision count mismatch')
    if row['request_sha256'] != run.data.digest(run.payload(item, row['model'])):
        raise ValueError('Request hash mismatch')
    if row['cost_cny'] != run.cost(row.get('response', {}), row['model']):
        raise ValueError('Cost mismatch')
    if not row['queued_s'] <= row['http_start_s'] <= row['completion_s']:
        raise ValueError('Timestamp ordering')
    if abs(row['completion_s'] - row['http_start_s'] - row['http_s']) > 1e-6:
        raise ValueError('Timing mismatch')


def quality(rows, items, fixed=False):
    by_id = defaultdict(list)
    for row in rows:
        by_id[row['item_id']].append(row)
    received = {}
    for uid in items:
        responses = [r for r in by_id[uid] if r['http_status'] == 200]
        if responses:
            received[uid] = responses[0]
    complete = set(received) == set(items)
    n = sum(len(i['gold']) for i in items.values())
    pairs = [(gold, received[uid]['predicted'].get(k)) for uid, item in items.items()
             if uid in received for k, gold in item['gold'].items()]
    correct = sum(a == b for a, b in pairs)
    f1 = None
    if fixed and complete:
        # Same predeclared, gold-supported classes for every model. Candidate
        # lists may contain many classes absent from this evaluation subset.
        labels = sorted({gold for item in items.values() for gold in item['gold'].values()})
        values = []
        for label in labels:
            tp = sum(a == b == label for a, b in pairs)
            fp = sum(a != label and b == label for a, b in pairs)
            fn = sum(a == label and b != label for a, b in pairs)
            values.append(2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.)
        f1 = statistics.mean(values)
    # Comparable new-case list price: final responses only, no cache discount or
    # retry billing. Observed spending stays separately in the raw archive.
    charges = []
    for r in received.values():
        response = r.get('response', {})
        if r['model'] == 'deepseek-flash':
            u = response.get('usage', {})
            response = {'usage': {**u, 'prompt_cache_hit_tokens': 0,
                                 'prompt_cache_miss_tokens': u.get('prompt_tokens', 0)}}
        charges.append(run.cost(response, r['model']))
    priced = bool(charges) and all(c is not None for c in charges)
    unit_cost = [sum(c[i] for c in charges)*1000/n for i in (0, 1)] if complete and priced else None
    return {'decisions': n, 'complete': complete, 'received_decisions': len(pairs),
            'accuracy': correct/n if complete else None, 'macro_f1': f1,
            'cost_cny_per_1000': unit_cost,
            'prompt_tokens': sum(r.get('response', {}).get('usage', {}).get('prompt_tokens',
                                 r.get('response', {}).get('usage', {}).get('input_tokens', 0)) for r in rows),
            'diagnostics': {'requests': len(rows), 'unpriced': sum(r['cost_cny'] is None for r in rows)}}


def window(rows, meta):
    left, right = meta['warmup_s'], meta['warmup_s'] + meta['window_s']
    completed = [r for r in rows if left <= r['completion_s'] < right]
    admitted = [r for r in rows if left <= r['http_start_s'] < right]
    occupancy = sum(max(0., min(right, r['completion_s']) - max(left, r['http_start_s'])) for r in rows)
    events = [(max(left, r['http_start_s']), 1) for r in rows if r['http_start_s'] < right and r['completion_s'] > left]
    events += [(min(right, r['completion_s']), -1) for r in rows if r['http_start_s'] < right and r['completion_s'] > left]
    active = peak = 0
    for _, delta in sorted(events):
        active += delta
        peak = max(peak, active)
    recent = deque(maxlen=20)
    circuit = False
    for r in rows:
        recent.append(r['http_status'] != 200)
        circuit |= len(recent) == 20 and sum(recent) >= 10
    full = meta['stop'] is None and meta['wall_s'] >= right and not circuit
    return {**meta, 'full': full, 'throughput': sum(r['valid'] for r in completed)/meta['window_s'] if full else None,
            'valid_completed': sum(r['valid'] for r in completed),
            'p95_http_s': percentile([r['http_s'] for r in admitted if r['http_status'] == 200]),
            'mean_http_concurrency': occupancy/meta['window_s'], 'peak_http_concurrency': peak,
            'http_samples': [r['http_s'] for r in admitted if r['http_status'] == 200],
            'diagnostics': {'requests': len(rows), 'completed': len(completed), 'admitted': len(admitted)}}


def combine(cells, expected_repeats):
    complete = len(cells) == expected_repeats and all(c['full'] for c in cells)
    seconds = sum(c['window_s'] for c in cells)
    samples = [t for c in cells for t in c['http_samples']]
    return {'complete': complete, 'repeats': len(cells), 'window_total_s': seconds,
            'throughput': sum(c['valid_completed'] for c in cells)/seconds if complete else None,
            'throughput_range': [min(c['throughput'] for c in cells), max(c['throughput'] for c in cells)] if complete else None,
            'p95_http_s': percentile(samples) if complete and len(samples) >= 20 else None,
            'http_sample_count': len(samples),
            'mean_http_concurrency': sum(c['mean_http_concurrency']*c['window_s'] for c in cells)/seconds if seconds else None,
            'peak_http_concurrency': max((c['peak_http_concurrency'] for c in cells), default=0)}


def build(root=run.RUN):
    cfg = json.loads((root / 'config.json').read_text())
    if run.data.file_sha(root / 'packets.jsonl') != cfg['packets_sha256']:
        raise ValueError('Workload hash mismatch')
    items = {p['id']: p for p in run.data.read_jsonl(root / 'packets.jsonl')}
    fixed = {'trial_referral', 'triage_urgency', 'tcm_syndrome',
             'tcm_pathogenesis_candidate', 'trial_shared_patient'}
    result = {'config': cfg, 'models': {}, 'families': {}, 'known_cost_cny_upper': 0.}
    for model in cfg['models']:
        path = root / model
        qrows = read_rows(path / 'quality.jsonl.gz')
        for row in qrows:
            validate(row, items)
        load = defaultdict(list)
        for meta_path in path.glob('*-r*-c*.json'):
            meta = json.loads(meta_path.read_text())
            rows = read_rows(path / meta['raw_file'])
            for row in rows:
                validate(row, items)
            load[(meta['family'], meta['concurrency'])].append(window(rows, meta))
        known = 0.
        for raw_path in path.rglob('*.jsonl.gz'):
            known += sum(r['cost_cny'][1] for r in read_rows(raw_path) if r.get('cost_cny'))
        smoke_path = path / 'smoke.json'
        if smoke_path.exists():
            smoke = json.loads(smoke_path.read_text())
            if smoke.get('cost_cny'):
                known += smoke['cost_cny'][1]
        result['known_cost_cny_upper'] += known
        result['models'][model] = {'label': run.clinical.MODELS[model]['label'], 'known_cost_cny_upper': known}
        for family in cfg['families']:
            fid = family['id']
            entry = result['families'].setdefault(fid, {**family, 'models': {}})
            part = {uid: p for uid, p in items.items() if p['family'] == fid}
            entry['models'][model] = {'quality': quality([r for r in qrows if r['item_id'] in part], part, fid in fixed),
                                     'load': {str(c): combine(load[(fid, c)], cfg['repeats']) for c in cfg['concurrency']}}
    scenes = json.loads((run.data.DEFAULT / 'taxonomy.json').read_text())['scenarios']
    scene_order = {s['id']: i for i, s in enumerate(scenes)}
    original_order = {f['id']: i for i, f in enumerate(cfg['families'])}
    result['families'] = dict(sorted(result['families'].items(),
        key=lambda pair: (scene_order[pair[1]['scenario']], original_order[pair[0]])))
    return result


def freeze():
    manifest = {str(p.relative_to(run.RUN)): run.data.file_sha(p) for p in sorted(run.RUN.rglob('*'))
                if p.is_file() and p.name not in ('archive_manifest.json', 'comparison.json', 'README.md')}
    run.data.write_json(run.RUN / 'archive_manifest.json', {'files': manifest})


def verify_archive(root=run.RUN):
    frozen = json.loads((root / 'archive_manifest.json').read_text())
    for filename, sha in frozen['files'].items():
        if run.data.file_sha(root / filename) != sha:
            raise ValueError('Archive hash mismatch: ' + filename)
    return build(root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = verify_archive() if args.check else build()
    if args.check:
        if result != json.loads((run.RUN / 'comparison.json').read_text()):
            raise SystemExit('Comparison is stale')
    else:
        run.data.write_json(run.RUN / 'comparison.json', result)
    if args.freeze:
        freeze()
    print('Recomputed', len(result['families']), 'tasks;', round(result['known_cost_cny_upper'], 3), 'CNY known upper cost')
