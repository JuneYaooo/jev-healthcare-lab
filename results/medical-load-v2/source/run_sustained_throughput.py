"""Sustained multi-question API load with raw completion windows and quota accounting."""
from __future__ import annotations
import argparse
import asyncio
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import platform
import random
import shutil
import statistics
import time
from urllib.parse import urlsplit

import aiohttp
import medical_decision_dataset as data
import run_task_performance as task

ROOT = task.ROOT
MODELS = task.MODELS
DEFAULT_FAMILIES = ['case_complication', 'medication_choice', 'diagnosis', 'tcm_syndrome']
SEED = 2026101203
RUN = ROOT / 'results/sustained-throughput-v1'
LIMITS = {
    'as_of': '2026-10-12',
    'sources': ['https://docs.typesafe.ai/models', 'https://api-docs.deepseek.com/quick_start/rate_limit/'],
    'jev_published_requests_per_s': 80, 'jev_published_input_tokens_per_s': 100000,
    'jev_client_requests_per_s': 76, 'jev_client_input_tokens_per_s': 95000,
    'flash_published_concurrency': 2500,
    'policy': 'Respect published account quotas, do not rotate keys or bypass 429. Client pacing is visible, not attributed to model compute.'}


class RunResolver(aiohttp.abc.AbstractResolver):
    """Reuse this run's system DNS answer; retain normal host/TLS validation."""
    def __init__(self, host, answers):
        self.host, self.answers = host, answers

    async def resolve(self, host, port=0, family=0):
        if host != self.host:
            raise OSError('Unexpected endpoint hostname')
        return [{**answer, 'port': port} for answer in self.answers]

    async def close(self):
        pass


def workload(families):
    manifest = task.verify_dataset(task.DATASET)
    available = {f['id']: f for f in manifest['families']}
    if len(set(families)) != len(families) or any(fid not in available or not available[fid]['selected'] for fid in families):
        raise ValueError('Choose distinct populated clinical families')
    packets = list(data.read_jsonl(task.DATASET / 'packets.jsonl'))
    items = []
    for fid in families:
        # Actual packet size remains visible when long states split a target-8 pack.
        target = min(8, available[fid]['selected'])
        items.extend({**p, 'scope': 'clinical'} for p in packets if p['family'] == fid and p['target'] == target)
    for original in data.read_jsonl(ROOT / 'benchmarks/performance_v1/fanout.jsonl'):
        items.append({**original, 'id': 'routing/' + original['id'], 'family': 'routing_200',
                      'target': original['questions'], 'scope': 'synthetic_rules',
                      'source_ids': {k: f"board-{original['repeat']}/{k}" for k in original['gold']}})
    return items, [available[fid] for fid in families]


def plan(families, repeats=2, concurrency=(8, 32, 64), seconds=30.0, warmup=5.0):
    cells = []
    for repeat in range(repeats):
        names = list(families) + ['routing_200']
        random.Random(SEED + repeat).shuffle(names)
        for fid in names:
            for c in concurrency:
                if fid == 'routing_200' and c > 32:
                    continue
                models = MODELS[:] if (repeat + c.bit_length()) % 2 else MODELS[::-1]
                for model in models:
                    cells.append({'family': fid, 'model': model, 'concurrency': c,
                                  'repeat': repeat, 'window_s': seconds, 'warmup_s': warmup,
                                  'target': 200 if fid == 'routing_200' else 8})
    return cells


class Pacer:
    """Smooth admission, including calibrated token cost; no one-second burst."""
    def __init__(self, requests_per_s=None, tokens_per_s=None):
        self.rps, self.tps = requests_per_s, tokens_per_s
        self.next_request = self.next_token = self.pause_until = 0.0
        self.lock = asyncio.Lock()

    async def acquire(self, tokens, deadline):
        loop = asyncio.get_running_loop()
        async with self.lock:
            while True:
                now = loop.time()
                allowed = max(now, self.next_request, self.next_token, self.pause_until)
                if allowed >= deadline:
                    return None
                if allowed > now:
                    await asyncio.sleep(allowed - now)
                    continue
                self.next_request = now + (1 / self.rps if self.rps else 0)
                self.next_token = now + (tokens / self.tps if self.tps else 0)
                return now

    def pause(self, seconds):
        self.pause_until = max(self.pause_until, asyncio.get_running_loop().time() + seconds)


def summarize(records, cell, wall_s, stop_reason, lag_samples, expected_packets):
    start, end = cell['warmup_s'], cell['warmup_s'] + cell['window_s']
    # Completions count at their actual time; trailing responses do not inflate the window.
    done = [r for r in records if start <= r['completion_s'] < end]
    cohort = [r for r in records if start <= r['http_start_s'] < end]
    sums = Counter()
    for r in done:
        for k in ['valid_decisions', 'correct_decisions', 'decisions']:
            sums[k] += r[k]
    n = sum(r['decisions'] for r in cohort)
    by_packet = defaultdict(list)
    for r in cohort:
        by_packet[r['item_id']].append(r)
    coverage = set(by_packet) == set(expected_packets)
    balanced_accuracy = (sum(statistics.mean(r['correct_decisions'] for r in by_packet[uid]) for uid in expected_packets)
                         / sum(expected_packets.values())) if coverage else None
    occupancy = sum(max(0.0, min(end, r['completion_s']) - max(start, r['http_start_s'])) for r in records)
    events = sorted([(max(start, r['http_start_s']), 1) for r in records if r['http_start_s'] < end and r['completion_s'] > start] +
                    [(min(end, r['completion_s']), -1) for r in records if r['http_start_s'] < end and r['completion_s'] > start])
    active = maximum = 0
    for _, delta in events:
        active += delta
        maximum = max(maximum, active)
    costs = task.metrics.costs(cohort, cell['model'])
    quota_wait = [r['admission_wait_s'] for r in cohort]
    bins = []
    for left in range(0, math.ceil(cell['window_s']), 5):
        right = min(cell['window_s'], left + 5)
        group = [r for r in done if start + left <= r['completion_s'] < start + right]
        bins.append({'from_s': left, 'to_s': right, 'valid_decisions_per_s': sum(r['valid_decisions'] for r in group) / (right - left),
                     'correct_decisions_per_s': sum(r['correct_decisions'] for r in group) / (right - left), 'requests': len(group)})
    goodput = sums['valid_decisions'] / cell['window_s']
    correct_goodput = sums['correct_decisions'] / cell['window_s']
    return {**cell, 'wall_s': wall_s, 'stop_reason': stop_reason,
            'full_window': stop_reason is None and wall_s >= end,
            'drain_s': max(0, wall_s - end), 'all_requests': len(records),
            'window_completed_requests': len(done), 'window_complete_packets': sum(r['complete_valid'] for r in done),
            'valid_decisions_per_s': goodput, 'correct_decisions_per_s': correct_goodput,
            'complete_packets_per_s': sum(r['complete_valid'] for r in done) / cell['window_s'],
            'cohort_requests': len(cohort), 'cohort_decisions': n,
            'cohort_accuracy': sum(r['correct_decisions'] for r in cohort) / n if n else None,
            'balanced_accuracy': balanced_accuracy, 'packet_coverage': len(by_packet), 'expected_packets': len(expected_packets),
            'cohort_complete_rate': sum(r['complete_valid'] for r in cohort) / len(cohort) if cohort else None,
            'status_counts': dict(Counter(r['status'] for r in cohort)),
            'http_counts': dict(Counter(str(r.get('http_status', 'none')) for r in cohort)),
            'response_p50_s': task.clinical.percentile([r['elapsed_s'] for r in cohort], .5),
            'response_p95_s': task.clinical.percentile([r['elapsed_s'] for r in cohort], .95),
            'end_to_end_p95_s': task.clinical.percentile([r['elapsed_s'] + r['admission_wait_s'] for r in cohort], .95),
            'admission_wait_mean_s': statistics.mean(quota_wait) if quota_wait else None,
            'mean_http_concurrency': occupancy / cell['window_s'], 'max_http_concurrency': maximum,
            'event_loop_lag_p95_s': task.clinical.percentile(lag_samples, .95),
            'event_loop_lag_max_s': max(lag_samples, default=0),
            'cost': costs, 'window_bins': bins}


async def request(session, item, model, origin, admission_wait, timeout):
    loop = asyncio.get_running_loop()
    started = loop.time()
    record = {'item_id': item['id'], 'family': item['family'], 'model': model,
              'http_start_s': started - origin, 'admission_wait_s': admission_wait,
              'started_at': task.clinical.now(), 'decisions': len(item['gold']),
              'request_sha256': data.digest(item['request']),
              'provider_request_sha256': data.digest(task.payload(item['request'], model)),
              'status': 'request_error', 'valid_decisions': 0, 'correct_decisions': 0,
              'complete_valid': False, 'all_correct': False}
    body = data.dumps(task.payload(item['request'], model)).encode()
    try:
        async with asyncio.timeout(timeout):
            async with session.post(task.clinical.MODELS[model]['endpoint'], data=body, allow_redirects=False) as response:
                content = await response.read()
                record.update(http_status=response.status, response_bytes=len(content))
                # Preserve only non-secret diagnostics. Never archive request headers.
                record['response_headers'] = {k: response.headers[k] for k in
                    ['retry-after', 'retry-after-ms', 'x-typesafe-request-id'] if k in response.headers}
                if response.status == 200:
                    try:
                        parsed = json.loads(content, object_pairs_hook=task.metrics.unique_object)
                        if not isinstance(parsed, dict):
                            raise ValueError('Expected response object')
                    except (ValueError, TypeError):
                        record.update(status='invalid_answer', raw_body=content.decode(errors='replace'))
                    else:
                        record['response'] = parsed
                        record.update(task.evaluate(item, parsed, model))
                        record['status'] = 'success' if record['complete_valid'] else 'invalid_answer'
                else:
                    record['error_body'] = content.decode(errors='replace')[:2000]
    except TimeoutError as exc:
        record['status'] = 'timeout'
        record['error_type'] = type(exc).__name__
    except aiohttp.ClientError as exc:
        record['error_type'] = type(exc).__name__
    record.update(elapsed_s=loop.time() - started, ended_at=task.clinical.now())
    record['completion_s'] = record['http_start_s'] + record['elapsed_s']
    return record


async def run_cell(session, items, cell, pacer, estimates, timeout, max_requests=5000):
    loop = asyncio.get_running_loop()
    origin = loop.time()
    deadline = origin + cell['warmup_s'] + cell['window_s']
    records, lag_samples, recent = [], [], deque(maxlen=20)
    index = 0
    stop_reason = None
    stop_monitor = asyncio.Event()

    async def monitor():
        while not stop_monitor.is_set():
            due = loop.time() + .1
            await asyncio.sleep(.1)
            if origin + cell['warmup_s'] <= loop.time() < deadline:
                lag_samples.append(max(0, loop.time() - due))

    async def worker():
        nonlocal index, stop_reason
        while loop.time() < deadline and stop_reason is None:
            if index >= max_requests:
                stop_reason = 'request_budget'
                break
            item = items[index % len(items)]
            index += 1
            ready = loop.time()
            admitted = await pacer.acquire(estimates[item['id']], deadline)
            if admitted is None or stop_reason:
                break
            record = await request(session, item, cell['model'], origin, admitted - ready, timeout)
            record['sequence'] = len(records)
            records.append(record)
            actual_tokens = record.get('response', {}).get('usage', {}).get('input_tokens')
            if actual_tokens:
                estimates[item['id']] = max(estimates[item['id']], math.ceil(actual_tokens * 1.1))
            status = record.get('http_status')
            if status in {400, 401, 402, 403, 404, 422}:
                stop_reason = 'fatal_http_' + str(status)
            if status in {429, 503, 529}:
                headers = record.get('response_headers', {})
                try:
                    delay = float(headers.get('retry-after', 1))
                    delay = max(delay, float(headers.get('retry-after-ms', 0)) / 1000)
                except ValueError:
                    delay = 1
                pacer.pause(max(1, delay))
            recent.append(record['status'] in {'request_error', 'timeout'})
            if len(recent) == 20 and sum(recent) >= 10:
                stop_reason = 'service_error_circuit'
    observer = asyncio.create_task(monitor())
    await asyncio.gather(*(worker() for _ in range(cell['concurrency'])))
    # A slow quota schedule may leave no more admissible work before the boundary.
    if stop_reason is None and loop.time() < deadline:
        await asyncio.sleep(deadline - loop.time())
    wall = loop.time() - origin
    stop_monitor.set()
    await observer
    expected = {i['id']: len(i['gold']) for i in items}
    return records, summarize(records, cell, wall, stop_reason, lag_samples, expected), lag_samples


async def run(args):
    if args.output.exists():
        raise ValueError('Output directory must be new')
    families = ['case_complication'] if args.smoke else (args.families or DEFAULT_FAMILIES)
    if args.all_tasks:
        families = [f['id'] for f in task.verify_dataset(task.DATASET)['families'] if f['selected']]
    items, inventory = workload(families)
    cells = plan(families, args.repeats, tuple(args.concurrency), args.seconds, args.warmup)
    if args.smoke:
        cells = [{'family': 'case_complication', 'model': model, 'concurrency': 8, 'repeat': 0,
                  'window_s': 3.0, 'warmup_s': 1.0, 'target': 8} for model in MODELS]
    keys = task.clinical.credentials(ROOT / '.env')
    if any(not keys.get(task.clinical.MODELS[model]['key_env']) for model in MODELS):
        raise ValueError('Missing model credential')
    args.output.mkdir(parents=True)
    data.write_jsonl(args.output / 'workloads.jsonl', items)
    shutil.copy2(task.DATASET / 'inputs.jsonl', args.output / 'source-inputs.jsonl')
    (args.output / 'tools').mkdir()
    helper_names = ['run_sustained_throughput.py', 'run_task_performance.py', 'run_performance_evaluation.py',
                    'run_model_evaluation.py', 'medical_decision_dataset.py']
    for name in helper_names:
        shutil.copy2(ROOT / 'scripts' / name, args.output / 'tools' / name)
    config = {'created_at': task.clinical.now(), 'families': inventory, 'cells': cells,
              'smoke': args.smoke, 'seed': SEED, 'python': platform.python_version(), 'aiohttp': aiohttp.__version__,
              'limits': LIMITS, 'pricing': task.metrics.PRICING, 'timeout_total_s': args.timeout,
              'timeout_connect_s': 10,
              'max_requests_per_cell': args.max_requests, 'max_cost_upper_usd': args.max_cost,
              'workloads_sha256': data.file_sha(args.output / 'workloads.jsonl'),
              'clinical_manifest_sha256': data.file_sha(task.DATASET / 'manifest.json'),
              'synthetic_manifest_sha256': data.file_sha(ROOT / 'benchmarks/performance_v1/manifest.json'),
              'transport': 'aiohttp HTTP/1.1, one reused pool per model, 128 sockets, 15s idle keepalive, no retries, trust_env=False, models measured sequentially.',
              'dns': 'System DNS resolved once per provider before calibration, frozen for this run. No custom address, endpoint, Host or TLS override. Lookup latency recorded separately.',
              'load': 'Closed-loop sustained multi-question requests: a worker immediately requests another packet after response. Not an open-loop arrival/SLA capacity test.',
              'measurement': '5s warmup then 30s fixed completion window by default. Drain responses are retained but not counted as window completions. Admitted cohort defines accuracy, latency, failure and cost.',
              'cache': 'Finite original panels repeat; calibration and warmup may populate provider caches. Cache usage retained, no cold-cache claim.',
              'synthetic_scope': 'routing_200 is a deterministic non-clinical 200-question board; performance only, never medical accuracy.'}
    data.write_json(args.output / 'config.json', config)
    sessions, pacers, estimates = {}, {}, {}
    summaries, blocked, fatal = [], {}, None
    spent = 0.0
    try:
        for model in MODELS:
            host = urlsplit(task.clinical.MODELS[model]['endpoint']).hostname
            resolver = aiohttp.resolver.ThreadedResolver()
            started = time.monotonic()
            try:
                answers = await asyncio.wait_for(resolver.resolve(host, 443), 120)
            finally:
                await resolver.close()
            data.write_json(args.output / f'dns-{model}.json', {'host': host, 'elapsed_s': time.monotonic() - started, 'answers': answers})
            sessions[model] = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=128, limit_per_host=128, keepalive_timeout=15,
                                              resolver=RunResolver(host, answers), ttl_dns_cache=None),
                timeout=aiohttp.ClientTimeout(total=args.timeout, connect=10),
                headers={'Authorization': 'Bearer ' + keys[task.clinical.MODELS[model]['key_env']], 'Content-Type': 'application/json'},
                cookie_jar=aiohttp.DummyCookieJar(), trust_env=False)
            pacers[model] = Pacer(76, 95000) if model == 'jev-1.13.0' else Pacer()
            estimates[model] = {i['id']: len(data.dumps(i['request']).encode()) + 512 for i in items}
            calibration = []
            for item in items:
                if args.smoke and item['family'] != 'case_complication':
                    continue
                ready = asyncio.get_running_loop().time()
                admitted = await pacers[model].acquire(estimates[model][item['id']], ready + args.timeout)
                if admitted is None:
                    fatal = 'calibration_admission_timeout'
                    break
                record = await request(sessions[model], item, model, ready, admitted - ready, args.timeout)
                calibration.append(record)
                usage = record.get('response', {}).get('usage', {})
                if usage.get('input_tokens'):
                    estimates[model][item['id']] = math.ceil(usage['input_tokens'] * 1.1)
                if record.get('http_status') in {400, 401, 402, 403, 404, 422}:
                    fatal = 'calibration_http_' + str(record['http_status'])
                    break
            data.write_json(args.output / f'calibration-{model}.json', {'records': calibration, 'token_estimates': estimates[model]})
            spent += task.metrics.costs(calibration, model)['usd_upper']
            if fatal:
                break
        for index, cell in enumerate(cells):
            if fatal:
                break
            if spent >= args.max_cost:
                fatal = 'cost_budget'
                break
            key = (cell['family'], cell['model'])
            if key in blocked:
                summaries.append({**cell, 'cell': index, 'skipped': blocked[key]})
                data.write_json(args.output / 'summary.json', summaries)
                continue
            packets = [i for i in items if i['family'] == cell['family'] and
                       (i['target'] == 200 if cell['family'] == 'routing_200' else True)]
            print(data.dumps({'event': 'start', 'cell': index, 'total': len(cells), **cell}), flush=True)
            rows, summary, lags = await run_cell(sessions[cell['model']], packets, cell, pacers[cell['model']],
                                                estimates[cell['model']], args.timeout, args.max_requests)
            filename = f'cell-{index:03d}.jsonl'
            data.write_jsonl(args.output / filename, rows)
            data.write_json(args.output / f'lag-{index:03d}.json', lags)
            summary.update(cell=index, records_file=filename)
            summaries.append(summary)
            spent += task.metrics.costs(rows, cell['model'])['usd_upper']
            data.write_json(args.output / 'summary.json', summaries)
            print(data.dumps({'event': 'finish', 'cell': index, 'valid_per_s': summary['valid_decisions_per_s'],
                              'correct_per_s': summary['correct_decisions_per_s'], 'stop': summary['stop_reason'],
                              'cost_upper_usd_so_far': round(spent, 4)}), flush=True)
            if summary['stop_reason']:
                if summary['stop_reason'].startswith('fatal_http'):
                    fatal = summary['stop_reason']
                else:
                    blocked[key] = summary['stop_reason']
            await asyncio.sleep(2)
    finally:
        await asyncio.gather(*(session.close() for session in sessions.values()))
    data.write_json(args.output / 'run_status.json', {'finished_at': task.clinical.now(), 'fatal': fatal,
                    'finished_cells': len(summaries), 'planned_cells': len(cells), 'cost_upper_usd': spent})
    data.write_json(args.output / 'archive_manifest.json', {'files': {
        str(p.relative_to(args.output)): data.file_sha(p) for p in sorted(args.output.rglob('*'))
        if p.is_file() and p.name != 'archive_manifest.json'}})
    if fatal:
        raise RuntimeError(fatal)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=RUN)
    parser.add_argument('--families', nargs='+')
    parser.add_argument('--all-tasks', action='store_true')
    parser.add_argument('--repeats', type=int, default=2)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--warmup', type=float, default=5)
    parser.add_argument('--concurrency', nargs='+', type=int, default=[8, 32, 64])
    parser.add_argument('--timeout', type=float, default=30)
    parser.add_argument('--max-requests', type=int, default=5000)
    parser.add_argument('--max-cost', type=float, default=25)
    parser.add_argument('--smoke', action='store_true')
    args = parser.parse_args()
    if args.seconds <= 0 or args.warmup < 0 or args.repeats < 1 or args.timeout <= 0 or args.max_cost <= 0 or args.max_requests < 1:
        parser.error('Invalid duration, repeats or budget')
    if any(c < 1 or c > 128 for c in args.concurrency) or len(set(args.concurrency)) != len(args.concurrency):
        parser.error('Concurrency must be distinct values in 1..128')
    if args.all_tasks and args.families:
        parser.error('Select families or all tasks, not both')
    asyncio.run(run(args))


if __name__ == '__main__':
    main()
