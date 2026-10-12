"""Four-provider, task-specific multi-decision quality and sustained load benchmark.

New archive generation; historical frozen runners are deliberately untouched.
"""
from __future__ import annotations
import argparse
import asyncio
from collections import defaultdict, deque
import gzip
import fcntl
import json
from pathlib import Path
import shutil
import socket
import time
from urllib.parse import urlsplit

import aiohttp
import medical_decision_dataset as data
import run_model_evaluation as clinical
import run_task_performance as task
from run_sustained_throughput import Pacer, RunResolver

ROOT = task.ROOT
RUN = ROOT / 'results/medical-load-v2'
MODELS = ['jev-1.13.0', 'deepseek-flash', 'qwen3.5-9b', 'qwen3.8-27b']
SEED = 2026101204
FX = 6.7313
SYSTEM = task.SYSTEM.replace('its designated record in state.records', 'its designated material').replace(
    'Records are separate cases;', 'For a shared patient, evaluate each candidate trial separately; otherwise records are separate cases;')
RATES = {'jev-1.13.0': (76, 90000), 'deepseek-flash': (None, None),
         'qwen3.5-9b': (15, 1200), 'qwen3.8-27b': (15, 600)}


def payload(item, model):
    clean = {k: item['request'][k] for k in ('state', 'questions')}
    if model == MODELS[0]:
        return {'model': model, **clean}
    body = {'model': clinical.MODELS[model].get('remote_model', model), 'temperature': 0,
            'max_tokens': max(512, 40 * len(item['gold'])), 'response_format': {'type': 'json_object'},
            'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': data.dumps(clean)}]}
    if model.startswith('qwen'):
        body['enable_thinking'] = False
    else:
        body['thinking'] = {'type': 'disabled'}
    return body


def choices(item, response, model):
    try:
        if model == MODELS[0]:
            answer = {k: v.get('choice') for k, v in response['answers'].items()}
        else:
            part = response['choices'][0]
            if part['finish_reason'] != 'stop':
                return {}
            answer = json.loads(part['message']['content'], object_pairs_hook=task.metrics.unique_object)
        if not isinstance(answer, dict):
            return {}
        return {k: v for k, v in answer.items() if k in item['gold'] and isinstance(v, str)
                and v in item['request']['questions'][k]['criteria']}
    except (ValueError, KeyError, TypeError, IndexError):
        return {}


def cost(response, model):
    """CNY list-price bounds, actual provider usage, no invented cache discounts."""
    u = response.get('usage', {})
    if model == MODELS[0]:
        if 'input_tokens' not in u:
            return None
        value = u['input_tokens'] * .042 * FX / 1e6
        return [value, value]
    if not all(k in u for k in ('prompt_tokens', 'completion_tokens')):
        return None
    inp, out = u['prompt_tokens'], u['completion_tokens']
    if model == 'deepseek-flash':
        if not all(k in u for k in ('prompt_cache_hit_tokens', 'prompt_cache_miss_tokens')):
            return None
        value = (u['prompt_cache_hit_tokens'] * .003 + u['prompt_cache_miss_tokens'] * .15 + out * .6) * FX / 1e6
        return [value, value * 2]
    if model == 'qwen3.5-9b':
        if inp >= 128000:
            raise ValueError('Unverified exact 128k price boundary; do not cross')
        value = (inp * .5 + out * 4) / 1e6
    else:
        value = (inp * 3 + out * 12) / 1e6
    return [value, value]


def prepare():
    if RUN.exists():
        raise ValueError('Archive already exists')
    policy = data.evaluation_policy(data.DEFAULT)
    groups = defaultdict(list)
    for row in data.evaluation_rows(data.DEFAULT, True, 'clinical'):
        groups[policy['tasks'][row['task']]['family']].append(row)
    families, packets = [], []
    for family in data.evaluation_inventory(data.DEFAULT)['clinical']['families']:
        fid = family['id']
        rows = sorted(groups[fid], key=lambda r: data.digest([SEED, r['id']]))
        if not rows:
            continue
        # target remains 8 even for a tail of one: identical flat q-ID schema.
        items = task.pack(rows, fid, 8)
        packets.extend(items)
        families.append({**family, 'cases': len({r['group_id'] for r in rows}), 'decisions': len(rows),
                         'batch': 8, 'load_ids': [p['id'] for p in items[:4]],
                         'load_decisions': sum(len(p['gold']) for p in items[:4])})
    rawpath = ROOT / 'work/decision-benchmark-v1/raw/trialgpt__dataset_sigir_retrieved_trials.json'
    raw = json.loads(rawpath.read_text())
    selected = sorted(raw, key=lambda p: data.digest([SEED, p['patient_id']]))[:8]
    fid = 'trial_shared_patient'
    trial_packets = []
    for index, patient in enumerate(selected):
        trials = [(label, trial) for label in ('0', '1', '2') for trial in patient[label]]
        trials.sort(key=lambda x: data.digest([SEED, patient['patient_id'], x[1]['NCTID']]))
        questions, gold, source_ids = {}, {}, {}
        # Fixed 8 trials for every patient, selected without conditioning on gold.
        for i, (label, trial) in enumerate(trials[:8]):
            key = f'q{i:03d}'
            material = {k: trial[k] for k in ('brief_title', 'brief_summary', 'inclusion_criteria', 'exclusion_criteria')}
            questions[key] = {'type': 'choice', 'criteria': {
                '0': 'Irrelevant: would not refer', '1': 'Potential: consider referral after further investigation',
                '2': 'Eligible: highly likely to refer'},
                'instructions': 'Use the shared patient in state.patient and only this candidate trial. '
                'Judge referral relevance, not each individual eligibility criterion. Trial: ' + data.dumps(material)}
            gold[key] = label
            source_ids[key] = patient['patient_id'] + ':' + trial['NCTID']
        item = {'id': f'{fid}/b8/{index}', 'family': fid, 'target': 8,
                'request': {'state': {'patient': patient['patient']}, 'questions': questions},
                'gold': gold, 'source_ids': source_ids}
        if not task.fits(item):
            raise ValueError('Shared-patient panel exceeds context guard')
        trial_packets.append(item)
    packets.extend(trial_packets)
    families.append({'id': fid, 'title': '同一患者的多项试验转介筛选', 'scenario': 'trials', 'cases': 8,
                     'decisions': 64, 'batch': 8, 'small_sample': True,
                     'load_ids': [p['id'] for p in trial_packets[:4]], 'load_decisions': 32})
    RUN.mkdir(parents=True)
    data.write_jsonl(RUN / 'packets.jsonl', packets)
    pricing = {'as_of': '2026-10-12', 'currency': 'CNY', 'usd_cny': FX,
               'fx_source': 'https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do',
               'typesafe_source': 'https://docs.typesafe.ai/models',
               'deepseek_source': 'https://api-docs.deepseek.com/quick_start/pricing/',
               'siliconflow_source': 'https://cloud.siliconflow.cn/me/models',
               'jev_usd_input_per_million': .042,
               'flash_usd_offpeak_per_million': {'hit': .003, 'miss': .15, 'output': .6},
               'flash_peak_multiplier': 2,
               'qwen_cny_per_million': {'qwen3.5-9b': {'input': .5, 'output': 4},
                                       'qwen3.8-27b': {'input': 3, 'output': 12}},
               'qwen_verified_account_tpm': {'qwen3.5-9b': 80000, 'qwen3.8-27b': 40000}}
    data.write_json(RUN / 'pricing.json', pricing)
    config = {'version': 2, 'created_at': clinical.now(), 'seed': SEED, 'models': MODELS,
              'families': families, 'concurrency': [8, 32], 'repeats': 2, 'window_s': 20, 'warmup_s': 3,
              'timeout_s': 90, 'budget_cny': 120, 'quality_concurrency': 8,
              'rates': RATES, 'clinical_manifest_sha256': data.file_sha(data.DEFAULT / 'manifest.json'),
              'trial_resource_sha256': data.file_sha(rawpath),
              'packets_sha256': data.file_sha(RUN / 'packets.jsonl'),
              'quality': 'All unique decisions once, batches <=8, API-only retries up to 3; invalid output is wrong.',
              'load': 'First up to four preselected packets per task; continuous closed-loop workers, two repeats, C8/C32. Window=max(20s,4*largest calibrated token reservation / token rate), capped at 120s. Same model window at both C levels. No response reuse.',
              'pricing': 'Quality-pass usage per 1000 unique decisions. Flash offpeak/peak bounds. Load replay costs archived separately.',
              'limits': 'Smooth admission within published quotas; Qwen reserves prompt plus max output. Configured concurrency is only a ceiling.',
              'shared_patient': '8 hash-selected SIGIR synthetic patients, 8 hash-selected trials each, upstream 0/1/2 gold unchanged. Overlap with existing referral pool possible; not added to overall 26-task mean.'}
    data.write_json(RUN / 'config.json', config)
    (RUN / 'source').mkdir()
    for name in ['run_medical_load.py', 'medical_decision_dataset.py', 'run_model_evaluation.py',
                 'run_task_performance.py', 'run_performance_evaluation.py', 'run_sustained_throughput.py']:
        shutil.copy2(ROOT / 'scripts' / name, RUN / 'source' / name)
    print(json.dumps({'prepared': len(families), 'packets': len(packets), 'decisions': sum(f['decisions'] for f in families)}))


class Budget:
    def __init__(self, limit):
        self.limit, self.used, self.held = limit, 0., 0.

    def reserve(self, amount):
        if self.used + self.held + amount > self.limit:
            raise RuntimeError('budget_limit')
        self.held += amount

    def settle(self, reserved, actual):
        self.held -= reserved
        self.used += actual if actual is not None else reserved


class Runner:
    def __init__(self, model, config, items, budget):
        self.model, self.config, self.items, self.budget = model, config, items, budget
        self.pacer = Pacer(*RATES[model])
        self.estimated = {}
        # Historical usage only sizes the admission reservation, never supplies
        # predictions, quality or billing in this new run. Sum per-question inputs
        # plus explicit packing overhead; repeated old system prompts make this
        # conservative for these <=8-question packets.
        old = ROOT / 'results/clinical-v1' / model / 'responses.jsonl'
        if old.exists():
            prior = {}
            for r in data.read_jsonl(old):
                for attempt in r['attempt_history']:
                    u = attempt.get('response', {}).get('usage', {})
                    tokens = u.get('input_tokens', u.get('prompt_tokens'))
                    if tokens:
                        prior[r['id']] = max(tokens, prior.get(r['id'], 0))
            for uid, item in items.items():
                if all(sid in prior for sid in item['source_ids'].values()):
                    self.estimated[uid] = (sum(prior[sid] for sid in item['source_ids'].values())
                                           + 100 * len(item['gold']) + 256) * 1.1
        self.path = RUN / model
        self.path.mkdir(exist_ok=True)

    def tokens(self, item):
        body = payload(item, self.model)
        # UTF-8 bytes conservatively bound initial input tokens; actual usage thereafter.
        inp = self.estimated.get(item['id'], len(data.dumps(body).encode()))
        return inp + (body.get('max_tokens', 0) if self.model.startswith('qwen') else 0)

    async def request(self, session, item, epoch, deadline=float('inf')):
        queued = time.perf_counter()
        if await self.pacer.acquire(self.tokens(item), deadline) is None:
            return None
        body = payload(item, self.model)
        # Worst-case byte-token bound and output allowance across supported price tiers.
        reserve = (len(data.dumps(body).encode()) * 3 + body.get('max_tokens', 0) * 12) / 1e6
        self.budget.reserve(reserve)
        started = time.perf_counter()
        row = {'item_id': item['id'], 'model': self.model, 'started_at': clinical.now(),
               'queued_s': queued - epoch, 'http_start_s': started - epoch,
               'request_sha256': data.digest(body), 'decisions': len(item['gold'])}
        try:
            async with session.post(clinical.MODELS[self.model]['endpoint'], json=body) as response:
                row['http_status'] = response.status
                raw = await response.read()
                try:
                    row['response'] = json.loads(raw)
                except (ValueError, UnicodeDecodeError):
                    row['response'] = {}
                if response.status in (429, 503, 529):
                    value = response.headers.get('Retry-After', '')
                    self.pacer.pause(max(5, min(float(value), 60)) if value.replace('.', '').isdigit() else 10)
        except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as exc:
            row['http_status'] = 0
            row['error_type'] = type(exc).__name__
            if isinstance(exc, aiohttp.ClientConnectorError):
                row['connection_not_established'] = True
                row['os_errno'] = getattr(exc.os_error, 'errno', None)
                # A connector error occurs before an HTTP request can be sent.
                self.pacer.pause(2)
                session.connector.clear_dns_cache()
            row['response'] = {}
        ended = time.perf_counter()
        predicted = choices(item, row['response'], self.model) if row['http_status'] == 200 else {}
        row.update(completion_s=ended-epoch, http_s=ended-started, end_to_end_s=ended-queued,
                   predicted=predicted, valid=len(predicted),
                   correct=sum(v == item['gold'][k] for k, v in predicted.items()), cost_cny=cost(row['response'], self.model))
        row['budget_reservation_cny'] = reserve
        self.budget.settle(reserve, row['cost_cny'][1] if row['cost_cny'] else
                           (0 if row.get('connection_not_established') else None))
        u = row['response'].get('usage', {})
        actual = u.get('input_tokens', u.get('prompt_tokens'))
        if actual:
            self.estimated[item['id']] = actual * 1.1
        if row['http_status'] in (401, 402, 403):
            raise RuntimeError('authorization_or_balance_' + str(row['http_status']))
        return row

    async def quality(self, session, items):
        path = self.path / 'quality.jsonl.gz'
        if path.exists():
            with gzip.open(path, 'rt') as stream:
                previous = [json.loads(s) for s in stream]
            for r in previous:
                u = r.get('response', {}).get('usage', {})
                actual = u.get('input_tokens', u.get('prompt_tokens'))
                if actual:
                    self.estimated[r['item_id']] = actual * 1.1
        else:
            previous = []
        done = {r['item_id'] for r in previous if r['http_status'] == 200}
        sem = asyncio.Semaphore(self.config['quality_concurrency'])
        epoch = time.perf_counter()
        with gzip.open(path, 'at') as stream:
            async def one(item):
                if item['id'] in done:
                    return
                async with sem:
                    for attempt in range(3):
                        row = await self.request(session, item, epoch)
                        row['attempt'] = attempt
                        stream.write(data.dumps(row) + '\n')
                        stream.flush()
                        if row['http_status'] == 200:
                            done.add(item['id'])
                            break
                        await asyncio.sleep(2 ** attempt)
            await asyncio.gather(*(one(item) for item in items))
        return len(done) == len(items)

    async def load(self, session, family, repeat, concurrency):
        stem = f"{family['id']}-r{repeat}-c{concurrency}"
        meta = self.path / (stem + '.json')
        if meta.exists():
            return
        items = [self.items[k] for k in family['load_ids']]
        rate = RATES[self.model][1]
        window = max(self.config['window_s'], 4 * max(self.tokens(i) for i in items) / rate) if rate else self.config['window_s']
        window = min(120, window)
        warmup = self.config['warmup_s']
        # A previous task's token reservation must not consume this task's
        # measurement interval. This wait is outside warmup and measurement.
        loop = asyncio.get_running_loop()
        await asyncio.sleep(max(0., self.pacer.next_token - loop.time(),
                                self.pacer.next_request - loop.time(), self.pacer.pause_until - loop.time()))
        epoch = time.perf_counter()
        deadline = loop.time() + warmup + window
        index = 0
        stop = None
        recent = deque(maxlen=20)
        with gzip.open(self.path / (stem + '.jsonl.gz'), 'wt') as stream:
            async def worker():
                nonlocal index, stop
                while stop is None:
                    item = items[index % len(items)]
                    index += 1
                    try:
                        row = await self.request(session, item, epoch, deadline)
                    except RuntimeError as exc:
                        stop = str(exc)
                        return
                    if row is None:
                        return
                    stream.write(data.dumps(row) + '\n')
                    stream.flush()
                    recent.append(row['http_status'] == 200)
                    if len(recent) == 20 and sum(not ok for ok in recent) >= 10:
                        stop = 'service_or_connection_circuit'
                    if row['http_status'] in (400, 404, 422):
                        stop = 'request_configuration_error'
            await asyncio.gather(*(worker() for _ in range(concurrency)))
            # Rate-limited workers may stop admitting before the window ends.
            # Observe the remaining idle interval instead of ending early.
            if stop is None:
                await asyncio.sleep(max(0., deadline - loop.time()))
        data.write_json(meta, {'family': family['id'], 'model': self.model, 'repeat': repeat,
            'concurrency': concurrency, 'window_s': window, 'warmup_s': warmup,
            'wall_s': time.perf_counter()-epoch, 'stop': stop, 'raw_file': stem + '.jsonl.gz'})
        print(json.dumps({'model': self.model, 'task': family['id'], 'repeat': repeat,
                          'concurrency': concurrency, 'budget_used_cny': round(self.budget.used, 3), 'stop': stop}), flush=True)
        if stop:
            raise RuntimeError(stop)

    async def run(self, smoke=False):
        cfg = clinical.MODELS[self.model]
        key = clinical.credentials(ROOT / '.env')[cfg['key_env']]
        host = urlsplit(cfg['endpoint']).hostname
        # Follow normal system DNS changes during long runs. Indefinite address
        # pinning can outlive the network route and confound a load window.
        connector = aiohttp.TCPConnector(limit=40, resolver=aiohttp.resolver.ThreadedResolver(),
                                         ttl_dns_cache=60, family=socket.AF_INET)
        async with aiohttp.ClientSession(connector=connector,
                headers={'Authorization': 'Bearer ' + key}, timeout=aiohttp.ClientTimeout(total=90)) as session:
            if smoke:
                first = next(iter(self.items.values()))
                row = await self.request(session, first, time.perf_counter())
                data.write_json(self.path / 'smoke.json', row)
                print(json.dumps({'model': self.model, 'http': row['http_status'], 'valid': row['valid'],
                                  'decisions': row['decisions'], 'cost': row['cost_cny'],
                                  'usage': row['response'].get('usage')}), flush=True)
                return
            # Fixed full-set quality pass before any load replay.
            complete = await self.quality(session, list(self.items.values()))
            print(json.dumps({'model': self.model, 'quality_complete': complete}), flush=True)
            if not complete:
                raise RuntimeError('quality_incomplete')
            for repeat in range(self.config['repeats']):
                families = sorted(self.config['families'], key=lambda f: data.digest([SEED, repeat, f['id']]))
                for family in families:
                    for c in (self.config['concurrency'] if repeat == 0 else self.config['concurrency'][::-1]):
                        await self.load(session, family, repeat, c)
        data.write_json(self.path / 'complete.json', {'ended_at': clinical.now()})


async def run(smoke, models):
    config = json.loads((RUN / 'config.json').read_text())
    items = {p['id']: p for p in data.read_jsonl(RUN / 'packets.jsonl')}
    if data.file_sha(RUN / 'packets.jsonl') != config['packets_sha256']:
        raise ValueError('Workload changed')
    budget = Budget(config['budget_cny'])
    if (RUN / 'resume-note.json').exists():
        budget.used += json.loads((RUN / 'resume-note.json').read_text()).get('extra_budget_reserve_cny', 0)
    # Resume accounts for already observed spending; never reset the run budget.
    for path in RUN.glob('**/*.jsonl.gz'):
        with gzip.open(path, 'rt') as stream:
            for line in stream:
                row = json.loads(line)
                if row.get('cost_cny'):
                    budget.used += row['cost_cny'][1]
                elif row.get('error_type') != 'ClientConnectorError':
                    budget.used += row.get('budget_reservation_cny',
                        (len(data.dumps(payload(items[row['item_id']], row['model'])).encode())*3
                         + payload(items[row['item_id']], row['model']).get('max_tokens', 0)*12)/1e6)
    results = await asyncio.gather(*(Runner(m, config, items, budget).run(smoke) for m in models), return_exceptions=True)
    errors = {m: str(r) for m, r in zip(models, results) if isinstance(r, BaseException)}
    data.write_json(RUN / ('smoke-status.json' if smoke else 'status.json'),
                    {'ended_at': clinical.now(), 'errors': errors, 'known_or_reserved_cost_cny': budget.used})
    print(json.dumps({'errors': errors, 'cost_cny': budget.used}), flush=True)
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--smoke', action='store_true')
    parser.add_argument('--models', nargs='+', default=MODELS, choices=MODELS)
    args = parser.parse_args()
    if args.prepare:
        prepare()
    else:
        with (ROOT / '.local-medical-load.lock').open('w') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise SystemExit('A medical-load run is already active')
            asyncio.run(run(args.smoke, args.models))
