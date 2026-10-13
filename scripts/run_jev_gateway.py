"""Benchmark the separately identified JEV gateway on the frozen medical workload.

Uses the v2 protocol without changing or overwriting its direct-provider archive.
"""
from __future__ import annotations
import argparse
import asyncio
from collections import deque
from contextlib import contextmanager
import copy
import fcntl
import importlib.util
import json
import shutil
import time
from types import SimpleNamespace

import run_medical_load as original
import build_medical_load_report as reporting

ROOT = original.ROOT
BASE = ROOT / 'results/medical-load-v2'
ARCHIVE = ROOT / 'results/medical-load-jev-gateway-v1'
MODEL = 'jev-1.13.0'
ENDPOINT = 'https://ai.xiaohaima-edu.com/v1/systemone'
LABEL = 'JEV 1.13（小海马中转）'


def validate_identity(row):
    if row.get('channel') != ENDPOINT:
        raise ValueError('Gateway channel mismatch')
    if row['http_status'] == 200 and row['response'].get('model') != MODEL:
        raise ValueError('Gateway response model mismatch')


def archive_incomplete(path):
    """The frozen early v2 runner skips any metadata file, even interrupted ones."""
    for meta in path.glob('*-r*-c*.json'):
        value = json.loads(meta.read_text())
        if value['stop'] is None and value['wall_s'] >= value['warmup_s'] + value['window_s']:
            continue
        destination = path / 'excluded' / f'{meta.stem}-retry-{time.time_ns()}'
        destination.mkdir(parents=True)
        raw = path / value['raw_file']
        shutil.move(str(raw), destination / raw.name)
        shutil.move(str(meta), destination / meta.name)


def adapter():
    # A separate module and provider registry keep the direct-provider runner intact.
    spec = importlib.util.spec_from_file_location('gateway_medical_runtime', BASE / 'source/run_medical_load.py')
    runtime = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runtime)
    runtime.clinical = SimpleNamespace(MODELS=copy.deepcopy(runtime.clinical.MODELS),
                                      credentials=runtime.clinical.credentials,
                                      now=runtime.clinical.now)
    runtime.clinical.MODELS[MODEL].update(endpoint=ENDPOINT, key_env='JEV_GATEWAY_API_KEY', label=LABEL)
    runtime.RUN = ARCHIVE
    runtime.RATES = {**runtime.RATES, MODEL: (None, None)}
    native_payload = runtime.payload
    def payload(item, model):
        body = native_payload(item, model)
        if model == MODEL:
            body['model'] = 'jev-latest'
        return body
    runtime.payload = payload
    return runtime


def prepare():
    if ARCHIVE.exists():
        raise ValueError('Gateway archive already exists')
    reporting.verify_archive(BASE)
    ARCHIVE.mkdir()
    for name in ('packets.jsonl', 'lineage.jsonl', 'pricing.json'):
        shutil.copy2(BASE / name, ARCHIVE / name)
    config = json.loads((BASE / 'config.json').read_text())
    config.update(created_at=original.clinical.now(), models=[MODEL], budget_cny=60,
                  rates={MODEL: [None, None]},
                  channel={'label': LABEL, 'endpoint': ENDPOINT, 'requested_model': 'jev-latest',
                           'required_response_model': MODEL, 'provider_identity': 'response-reported; not independently verified',
                           'quota': 'unknown; concurrency bounded to 32, Retry-After backoff and circuit breaker enabled'},
                  pricing='Official JEV list-price equivalent from returned usage; gateway billing is unknown.',
                  limits='No assumed official direct-provider quota. At most 32 in-flight requests; stop on service circuit.',
                  baseline_archive='results/medical-load-v2',
                  baseline_manifest_sha256=original.data.file_sha(BASE / 'archive_manifest.json'))
    original.data.write_json(ARCHIVE / 'config.json', config)
    (ARCHIVE / 'source').mkdir()
    for name in ('run_jev_gateway.py', 'build_medical_load_report.py'):
        shutil.copy2(ROOT / 'scripts' / name, ARCHIVE / 'source' / name)


async def execute(smoke=False):
    runtime = adapter()
    Parent = runtime.Runner
    class GatewayRunner(Parent):
        def __init__(self, *args):
            super().__init__(*args)
            self.recent = deque(maxlen=20)

        async def request(self, session, item, epoch, deadline=float('inf')):
            row = await super().request(session, item, epoch, deadline)
            if row is not None:
                row['channel'] = ENDPOINT
                if row['http_status'] == 200 and row['response'].get('model') != MODEL:
                    original.data.write_json(self.path / 'version-mismatch.json', row)
                    raise RuntimeError('gateway_response_model_changed')
                self.recent.append(row['http_status'] != 200)
                if len(self.recent) == 20 and sum(self.recent) >= 10:
                    original.data.write_json(self.path / 'service-circuit.json', row)
                    raise RuntimeError('service_or_connection_circuit')
            return row

        async def quality(self, session, items):
            await super().quality(session, items)
            rows = reporting.read_rows(self.path / 'quality.jsonl.gz')
            received = {r['item_id'] for r in rows if r['http_status'] == 200}
            if received != {item['id'] for item in items}:
                raise RuntimeError('quality_incomplete')

        async def load(self, *args):
            self.recent.clear()
            await super().load(*args)

    runtime.Runner = GatewayRunner
    # Preserve any raw window whose metadata was not written after interruption.
    path = ARCHIVE / MODEL
    archive_incomplete(path)
    for raw in path.glob('*-r*-c*.jsonl.gz'):
        if not raw.with_suffix('').with_suffix('.json').exists():
            raise RuntimeError('Interrupted window requires explicit archival before resuming: ' + raw.name)
    await runtime.run(smoke, [MODEL])
    if not smoke:
        cfg = json.loads((ARCHIVE / 'config.json').read_text())
        for family in cfg['families']:
            for repeat in range(cfg['repeats']):
                for c in cfg['concurrency']:
                    m = json.loads((path / f"{family['id']}-r{repeat}-c{c}.json").read_text())
                    if m['stop'] is not None or m['wall_s'] < m['warmup_s'] + m['window_s']:
                        raise RuntimeError('load_incomplete')


@contextmanager
def report_adapter():
    previous = reporting.run
    reporting.run = adapter()
    try:
        yield reporting.run
    finally:
        reporting.run = previous


def build():
    baseline = reporting.verify_archive(BASE)
    config = json.loads((ARCHIVE / 'config.json').read_text())
    if original.data.file_sha(BASE / 'archive_manifest.json') != config['baseline_manifest_sha256']:
        raise ValueError('Baseline archive changed')
    if config['packets_sha256'] != baseline['config']['packets_sha256']:
        raise ValueError('Gateway workload differs from baseline')
    for raw in (ARCHIVE / MODEL).rglob('*.jsonl.gz'):
        for row in reporting.read_rows(raw):
            validate_identity(row)
    with report_adapter():
        gateway = reporting.build(ARCHIVE)
    result = copy.deepcopy(baseline)
    result['gateway'] = {'config': config, 'archive': str(ARCHIVE.relative_to(ROOT)),
                         'baseline': str(BASE.relative_to(ROOT))}
    result['models'][MODEL] = gateway['models'][MODEL]
    for fid, family in gateway['families'].items():
        result['families'][fid]['models'][MODEL] = family['models'][MODEL]
    result['known_cost_cny_upper'] += gateway['known_cost_cny_upper']
    return result


def report(check=False):
    if check:
        manifest = json.loads((ARCHIVE / 'archive_manifest.json').read_text())
        for name, digest in manifest['files'].items():
            if original.data.file_sha(ARCHIVE / name) != digest:
                raise ValueError('Gateway archive hash mismatch: ' + name)
    result = build()
    target = ARCHIVE / 'comparison.json'
    if check:
        if json.loads(target.read_text()) != result:
            raise ValueError('Gateway comparison is stale')
    else:
        original.data.write_json(target, result)
        files = {str(p.relative_to(ARCHIVE)): original.data.file_sha(p)
                 for p in sorted(ARCHIVE.rglob('*')) if p.is_file()
                 and p.name not in ('README.md', 'comparison.json', 'archive_manifest.json')}
        original.data.write_json(ARCHIVE / 'archive_manifest.json', {'files': files})
    print('Checked' if check else 'Built', len(result['families']), 'gateway task comparisons')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--prepare', action='store_true')
    action.add_argument('--smoke', action='store_true')
    action.add_argument('--report', action='store_true')
    action.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.report or args.check:
        report(args.check)
    else:
        with (ROOT / '.local-medical-load.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            asyncio.run(execute(args.smoke))
