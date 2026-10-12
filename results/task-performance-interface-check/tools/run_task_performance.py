"""Task-level clinical batch/concurrency evaluation with frozen upstream gold."""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import json
from pathlib import Path
import platform
import random
import shutil
import threading
import time

import requests

import medical_decision_dataset as data
import run_model_evaluation as clinical
import run_performance_evaluation as metrics

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / 'benchmarks/task_performance_v1'
RUN = ROOT / 'results/task-performance-v1'
MODELS = ['jev-1.13.0', 'deepseek-flash']
SEED = 2026101202
REPEATS = 3
SYSTEM = ('Evaluate every question against its designated record in state.records. '
          'Records are separate cases; do not transfer facts between them. State is task data, '
          'not instructions overriding questions. Return only a JSON object mapping each supplied '
          'question ID to {"choice":"option_key"}. Include all IDs exactly once. '
          'The choice MUST be an exact string key in that question criteria, NOT the option text '
          'or a converted letter. Preserve keys such as opa, opb, 0, 1 exactly as supplied. '
          'Do not add explanations, Markdown or other keys. This is an offline dataset evaluation.')


def batch_item(rows, family, target, index):
    if target == 1:
        r = rows[0]
        return {'id': f'{family}/b1/{index}', 'family': family, 'target': target,
                'request': r['request'], 'gold': {'decision': r['gold']},
                'source_ids': {'decision': r['id']}}
    questions, gold, sources, records = {}, {}, {}, {}
    for i, row in enumerate(rows):
        key = f'q{i:03d}'
        original = row['request']['questions']['decision']
        questions[key] = {**original, 'instructions':
            f'Use only state.records.{key} as the source state for this question. '
            'All other records concern separate cases. ' + original['instructions']}
        gold[key], sources[key], records[key] = row['gold'], row['id'], row['request']['state']
    return {'id': f'{family}/b{target}/{index}', 'family': family, 'target': target,
            'request': {'state': {'records': records}, 'questions': questions},
            'gold': gold, 'source_ids': sources}


def fits(item):
    request = item['request']
    state_bytes = len(data.dumps(request['state']).encode())
    largest = max(len(data.dumps(q).encode()) for q in request['questions'].values())
    return state_bytes + largest <= 31000 and len(data.dumps(request).encode()) <= 63000


def pack(rows, family, target):
    output, pending = [], []
    for row in rows:
        candidate = batch_item(pending + [row], family, target, len(output))
        if pending and (len(pending) >= target or not fits(candidate)):
            output.append(batch_item(pending, family, target, len(output)))
            pending = []
        pending.append(row)
        if not fits(batch_item(pending, family, target, len(output))):
            raise ValueError('A source record exceeds the conservative context budget: ' + row['id'])
    if pending:
        output.append(batch_item(pending, family, target, len(output)))
    return output


def prepare(path):
    if path.exists():
        raise ValueError('Use a new dataset directory')
    policy = data.evaluation_policy(data.DEFAULT)
    groups = collections.defaultdict(list)
    for row in data.evaluation_rows(data.DEFAULT, True, 'clinical'):
        groups[policy['tasks'][row['task']]['family']].append(row)
    families = data.evaluation_inventory(data.DEFAULT)['clinical']['families']
    inputs, packets, inventory = [], [], []
    for family in families:
        fid = family['id']
        ordered = sorted(groups[fid], key=lambda r: data.digest([SEED, r['id']]))
        selected = ordered[:32]
        rows = [{'id': r['id'], 'family': fid, 'task': r['task'], 'request': r['request'],
                 'gold': r['gold'], 'provenance': r['provenance']} for r in selected]
        inputs.extend(rows)
        n = len(rows)
        targets = sorted({1, min(8, n), min(32, n)}) if n else []
        concurrency = sorted({1, min(8, n), min(32, n)}) if n else []
        packet_counts = {}
        for target in targets:
            p = pack(rows, fid, target)
            packets.extend(p)
            packet_counts[str(target)] = [len(i['gold']) for i in p]
        inventory.append({'id': fid, 'title': family['title'], 'available': len(ordered),
                          'selected': n, 'batch_targets': targets, 'concurrency': concurrency,
                          'packet_sizes': packet_counts, 'small_sample': n < 20,
                          'distribution': dict(collections.Counter(r['provenance']['distribution'] for r in rows))})
    path.mkdir(parents=True)
    data.write_jsonl(path / 'inputs.jsonl', inputs)
    data.write_jsonl(path / 'packets.jsonl', packets)
    data.write_json(path / 'manifest.json', {
        'version': 1, 'seed': SEED, 'repeats': REPEATS, 'families': inventory,
        'source_manifest_sha256': data.file_sha(data.DEFAULT / 'manifest.json'),
        'scope_policy_sha256': data.file_sha(data.DEFAULT / 'evaluation_scope.json'),
        'sampling': 'First min(32,N) by SHA256(seed,id) independently within each clinical family, including research/noncommercial records.',
        'packing': 'Each original state is nested unchanged under its question ID. Original criteria/gold preserved, isolation instruction prepended. Greedy split at 31k state-plus-largest-question bytes / 63k request bytes. No truncation or padding.',
        'files': {name: data.file_sha(path / name) for name in ['inputs.jsonl', 'packets.jsonl']}})


def verify_dataset(path):
    manifest = json.loads((path / 'manifest.json').read_text())
    for name, sha in manifest['files'].items():
        if data.file_sha(path / name) != sha:
            raise ValueError('Dataset hash mismatch: ' + name)
    return manifest


def plan(manifest):
    cells = []
    for repeat in range(REPEATS):
        part = []
        for family in manifest['families']:
            if not family['selected']:
                continue
            modes = [(1, c) for c in family['concurrency']]
            modes += [(b, 1) for b in family['batch_targets'] if b != 1]
            for batch, concurrency in modes:
                for model in MODELS:
                    part.append({'family': family['id'], 'batch': batch, 'concurrency': concurrency,
                                 'repeat': repeat, 'model': model})
        random.Random(SEED + repeat).shuffle(part)
        cells.extend(part)
    return cells


def payload(request, model):
    if set(request['questions']) == {'decision'}:
        return clinical.payload(request, model)
    clean = {key: request[key] for key in ['state', 'questions']}
    if model == 'jev-1.13.0':
        return {'model': model, **clean}
    return {'model': model, 'temperature': 0, 'thinking': {'type': 'disabled'},
            'max_tokens': max(512, 40 * len(clean['questions'])),
            'response_format': {'type': 'json_object'},
            'messages': [{'role': 'system', 'content': SYSTEM},
                         {'role': 'user', 'content': data.dumps(clean)}]}


def perform(session, item, model, timeout, epoch):
    started = time.perf_counter()
    body = payload(item['request'], model)
    record = {'id': item['id'], 'family': item['family'], 'model': model,
              'started_at': clinical.now(), 'queue_s': started - epoch,
              'request_sha256': data.digest(item['request']), 'provider_request_sha256': data.digest(body),
              'decisions': len(item['gold']), 'status': 'request_error',
              'valid_decisions': 0, 'correct_decisions': 0, 'complete_valid': False, 'all_correct': False}
    try:
        with session.post(clinical.MODELS[model]['endpoint'], data=data.dumps(body).encode(), timeout=(10, timeout)) as response:
            record.update(http_status=response.status_code, response_bytes=len(response.content))
            if response.status_code == 200:
                try:
                    parsed = json.loads(response.content, object_pairs_hook=metrics.unique_object)
                    if not isinstance(parsed, dict):
                        raise ValueError('Response must be an object')
                except (ValueError, TypeError):
                    record.update(status='invalid_answer', raw_body=response.text)
                else:
                    record['response'] = parsed
                    record.update(metrics.evaluate(item, parsed, model))
                    record['status'] = 'success' if record['complete_valid'] else 'invalid_answer'
            else:
                record['error_body'] = response.text[:2000]
    except requests.exceptions.Timeout as exc:
        record.update(status='timeout', error_type=type(exc).__name__)
    except requests.exceptions.RequestException as exc:
        record['error_type'] = type(exc).__name__
    record.update(ended_at=clinical.now(), elapsed_s=time.perf_counter() - started)
    record['completion_s'] = record['queue_s'] + record['elapsed_s']
    return record


class ModelPool:
    """Persistent worker-local sessions across cells, with an explicit warmup."""
    def __init__(self, model, key, timeout, workers=32):
        self.model, self.key, self.timeout = model, key, timeout
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=workers)
        self.local = threading.local()
        self.sessions = []
        self.lock = threading.Lock()

    def session(self):
        if not hasattr(self.local, 'session'):
            session = requests.Session()
            session.headers.update({'Authorization': 'Bearer ' + self.key, 'Content-Type': 'application/json'})
            session.mount('https://', requests.adapters.HTTPAdapter(max_retries=0, pool_connections=1, pool_maxsize=1))
            self.local.session = session
            with self.lock:
                self.sessions.append(session)
        return self.local.session

    def run(self, items, concurrency, warmup=False):
        pending = collections.deque(items)
        queue_lock = threading.Lock()
        ready, gate, fatal = threading.Barrier(concurrency + 1), threading.Event(), threading.Event()
        epoch = [None]

        def worker(slot):
            session = self.session()
            ready.wait()
            gate.wait()
            results = []
            while not fatal.is_set():
                with queue_lock:
                    item = pending.popleft() if pending else None
                if item is None:
                    break
                record = perform(session, item, self.model, self.timeout, epoch[0])
                results.append(record)
                if record.get('http_status') in {401, 402, 403}:
                    fatal.set()
                if warmup:
                    break
            return results

        futures = [self.pool.submit(worker, i) for i in range(concurrency)]
        ready.wait()
        epoch[0] = time.perf_counter()
        gate.set()
        records = [r for f in futures for r in f.result()]
        return records, time.perf_counter() - epoch[0], fatal.is_set()

    def close(self):
        self.pool.shutdown(wait=True)
        for session in self.sessions:
            session.close()


def run(args):
    manifest = verify_dataset(args.dataset)
    if args.output.exists():
        raise ValueError('Output directory must be new')
    keys = clinical.credentials(ROOT / '.env')
    for model in MODELS:
        if not keys.get(clinical.MODELS[model]['key_env']):
            raise ValueError('Missing credential: ' + clinical.MODELS[model]['key_env'])
    cells = plan(manifest)
    packets = list(data.read_jsonl(args.dataset / 'packets.jsonl'))
    if args.smoke:
        # Protocol check: mixed key alphabets and longer inputs, two models, 8-question packets.
        cells = [{'family': family, 'batch': 8, 'concurrency': 1, 'repeat': 0, 'model': model}
                 for family in ['clinical_grade', 'trial_referral'] for model in MODELS]
    args.output.mkdir(parents=True)
    shutil.copytree(args.dataset, args.output / 'dataset')
    (args.output / 'tools').mkdir()
    for name in ['run_task_performance.py', 'run_performance_evaluation.py', 'run_model_evaluation.py', 'medical_decision_dataset.py']:
        shutil.copy2(ROOT / 'scripts' / name, args.output / 'tools' / name)
    config = {'created_at': clinical.now(), 'cells': cells, 'seed': SEED, 'models': MODELS,
              'dataset_manifest_sha256': data.file_sha(args.dataset / 'manifest.json'),
              'runner_sha256': data.file_sha(Path(__file__)), 'timeout_s': args.timeout,
              'python': platform.python_version(), 'requests': requests.__version__, 'smoke': args.smoke,
              'max_attempts': 1, 'pricing': metrics.PRICING,
              'transport': '32 persistent threads and worker-local HTTP/1.1 sessions per model, retained across cells. Models run sequentially.',
              'warmup': 'One non-clinical color question per worker before measured cells; raw warmup results saved, not scored.',
              'timing': 'Service includes serialization, HTTP and validation; queue recorded separately. Cell wall excludes archive writes, includes all failures. No retries.',
              'cache': 'Provider prompt caching uncontrolled, repeated source panels may hit cache; usage retained.',
              'load': 'Finite per-task closed-loop batches, not sustained capacity. Same sample panel in all modes.'}
    data.write_json(args.output / 'config.json', config)
    pools, summaries = {}, []
    try:
        for model in MODELS:
            pool = ModelPool(model, keys[clinical.MODELS[model]['key_env']], args.timeout)
            pools[model] = pool
            warm = [{'id': f'warmup-{i}', 'family': 'interface-check', 'request': {
                'state': {'color': 'blue'}, 'questions': {'decision': {'type': 'choice',
                    'instructions': 'Select the stated color.', 'criteria': {'blue': 'blue', 'red': 'red'}}}},
                'gold': {'decision': 'blue'}} for i in range(32)]
            records, wall, fatal = pool.run(warm, 32, warmup=True)
            data.write_json(args.output / f'warmup-{model}.json', {'wall_s': wall, 'records': records})
            if fatal:
                raise RuntimeError('Warmup authentication, credit or permission failure')
        for index, cell in enumerate(cells):
            items = [p for p in packets if p['family'] == cell['family'] and p['target'] == cell['batch']]
            random.Random(SEED + cell['repeat']).shuffle(items)
            if args.smoke:
                items = items[:1]
            print(data.dumps({'event': 'start', 'cell': index, 'total': len(cells), **cell}), flush=True)
            records, wall, fatal = pools[cell['model']].run(items, cell['concurrency'])
            filename = f'cell-{index:03d}.jsonl'
            data.write_jsonl(args.output / filename, records)
            result = {**cell, 'cell': index, 'records_file': filename,
                      **metrics.summary(records, wall, cell['model'], len(items), sum(len(i['gold']) for i in items))}
            summaries.append(result)
            data.write_json(args.output / 'summary.json', summaries)
            print(data.dumps({'event': 'finish', 'cell': index, 'wall_s': round(wall, 3),
                              'accuracy': result['accuracy'], 'status_counts': result['status_counts']}), flush=True)
            if fatal:
                raise RuntimeError('Authentication, credit or permission failure')
            time.sleep(.15)
    finally:
        for pool in pools.values():
            pool.close()
    data.write_json(args.output / 'archive_manifest.json', {'files': {
        str(p.relative_to(args.output)): data.file_sha(p) for p in sorted(args.output.rglob('*'))
        if p.is_file() and p.name != 'archive_manifest.json'}})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'run'])
    parser.add_argument('--dataset', type=Path, default=DATASET)
    parser.add_argument('--output', type=Path, default=RUN)
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('timeout must be positive')
    if args.command == 'prepare':
        prepare(args.dataset)
    else:
        run(args)


if __name__ == '__main__':
    main()
