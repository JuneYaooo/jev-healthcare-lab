"""Run Qwen3.5-9B on the frozen main cohort with the existing JSON adapter."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import threading
import time
import urllib.error
import urllib.request

from compare_deepseek import ROOT, SYSTEM, dumps, load_rows, normalize, request_payload as deepseek_payload, sha

OUT = ROOT / 'comparisons/qwen3.5-9b'
CACHE = ROOT / 'work/qwen3.5-9b'
ENDPOINT = 'https://api.siliconflow.cn/v1/chat/completions'
MODEL = 'Qwen/Qwen3.5-9B'


def request_payload(row):
    payload = deepseek_payload(row)
    payload.pop('thinking')
    payload.update(model=MODEL, enable_thinking=False)
    return payload


def config():
    return {
        'model_requested': MODEL, 'provider': 'SiliconFlow China', 'endpoint': ENDPOINT,
        'enable_thinking': False, 'temperature': 0, 'response_format': {'type': 'json_object'},
        'max_tokens_rule': 'max(512, min(16384, 40 * question_count + 128))',
        'system_prompt': SYSTEM, 'adapter': 'compare_deepseek.normalize; no gold in request or normalization',
        'workers': 8, 'timeout_s': 120, 'max_attempts': 3,
        'retry_policy': 'Up to 3 attempts per execution. Transport-only recovery passes retain previous attempts. HTTP 429 triggers a shared 60-second cooldown. Never retry based on gold or score.',
        'pricing': {'currency': 'CNY', 'input_per_million': 1.5, 'output_per_million': 12},
        'pricing_note': 'China catalog snapshot in pricing_source.json; list-price estimate, no cache discount or USD conversion assumed.',
        'api_reference': 'https://docs.siliconflow.cn/docs/api/chat-completions-post',
        'scope': 'All 96 main tasks, 7133 input rows; historical Jev and DeepSeek references, not simultaneous timing. Empty candidate sets use zero API calls.',
    }


def cache_path(row):
    return CACHE / 'runs' / (sha([row['task'], row['id'], request_payload(row)]) + '.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key-file', type=Path, help='Private file outside the repository containing only the API key')
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--retry-transport', action='store_true', help='Recover transport failures while preserving every earlier attempt')
    parser.add_argument('--max-tokens', type=int, default=30000000, help='Stop scheduling when reported cumulative usage reaches this bound')
    args = parser.parse_args()
    key = args.key_file.read_text().strip() if args.key_file else os.environ['SILICONFLOW_API_KEY']
    OUT.mkdir(parents=True, exist_ok=True)
    (CACHE / 'runs').mkdir(parents=True, exist_ok=True)
    cfg = config()
    cp = OUT / 'config.json'
    if cp.exists() and json.loads(cp.read_text()) != cfg:
        raise ValueError('Existing run configuration differs')
    cp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n')
    rows = load_rows()
    if len(rows) != 7133 or len({r['task'] for r in rows}) != 96:
        raise ValueError('Frozen cohort changed')
    def needs_run(row):
        path = cache_path(row)
        if not path.exists():
            return True
        record = json.loads(path.read_text())
        return args.retry_transport and (record.get('http_status') == 429 or record.get('http_status', 0) >= 500 or
                                        record.get('error_type') in ('URLError', 'TimeoutError', 'RemoteDisconnected', 'ConnectionResetError', 'SSLError', 'SSLEOFError', 'IncompleteRead'))
    selected = [r for r in rows if needs_run(r)]
    if args.limit:
        selected = selected[:args.limit]
    counts = Counter()
    lock, stop = threading.Lock(), threading.Event()
    spent_tokens = sum(json.loads(p.read_text()).get('reported_total_tokens', 0) for p in (CACHE / 'runs').glob('*.json'))
    started = time.perf_counter()
    started_utc = datetime.now(timezone.utc).isoformat()
    cooldown_until = 0.0

    def run(row):
        nonlocal spent_tokens, cooldown_until
        if stop.is_set():
            return
        payload = request_payload(row)
        base = {'task': row['task'], 'id': row['id'], 'request_sha256': row['request_sha256'],
                'provider_request_sha256': sha(payload)}
        attempts = []
        if cache_path(row).exists():
            previous = json.loads(cache_path(row).read_text())
            attempts.extend(previous.pop('prior_attempts'))
            previous.pop('reported_total_tokens')
            attempts.append(previous)
        if not row['request']['questions']:
            result = dict(base, status='ok', deterministic_empty=True, elapsed_s=0, normalized_answers={})
        else:
            for index in range(cfg['max_attempts']):
                while True:
                    with lock:
                        remaining = cooldown_until - time.monotonic()
                    if remaining <= 0:
                        break
                    time.sleep(min(remaining, 1))
                result = dict(base, attempt=len(attempts) + 1, started_utc=datetime.now(timezone.utc).isoformat())
                t = time.perf_counter()
                retry = False
                req = urllib.request.Request(ENDPOINT, data=dumps(payload).encode(),
                                             headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
                try:
                    with urllib.request.urlopen(req, timeout=cfg['timeout_s']) as response:
                        data = json.load(response)
                    result.update(response=data, elapsed_s=time.perf_counter() - t)
                    if data['model'] != MODEL:
                        stop.set()
                        raise ValueError('Unexpected returned model')
                    if data['choices'][0]['finish_reason'] != 'stop':
                        raise ValueError('Incomplete generation')
                    result.update(normalized_answers=normalize(row, data), status='ok')
                except urllib.error.HTTPError as error:
                    result.update(status='http_error', http_status=error.code, elapsed_s=time.perf_counter() - t)
                    retry = error.code == 429 or error.code >= 500
                    if error.code == 429:
                        with lock:
                            cooldown_until = max(cooldown_until, time.monotonic() + 60)
                    if error.code in (401, 402, 403, 404):
                        stop.set()
                except Exception as error:
                    result.update(status='error', error_type=type(error).__name__, elapsed_s=time.perf_counter() - t)
                    retry = True
                usage = result.get('response', {}).get('usage', {})
                with lock:
                    spent_tokens += usage.get('total_tokens', 0)
                    if spent_tokens >= args.max_tokens:
                        stop.set()
                attempts.append(result)
                if result['status'] == 'ok' or not retry or stop.is_set() or index == cfg['max_attempts'] - 1:
                    break
                time.sleep(min(2 ** (index + 1), 8))
        final = dict(result)
        final['prior_attempts'] = attempts[:-1]
        final['reported_total_tokens'] = sum(a.get('response', {}).get('usage', {}).get('total_tokens', 0) for a in attempts)
        with lock:
            path = cache_path(row)
            temp = path.with_suffix('.tmp')
            temp.write_text(dumps(final) + '\n')
            temp.replace(path)
            counts[final['status']] += 1
            if sum(counts.values()) % 100 == 0 or final['status'] != 'ok':
                print(dumps({'completed': sum(counts.values()), 'selected': len(selected), 'counts': dict(counts),
                             'elapsed_s': round(time.perf_counter() - started, 1), 'reported_tokens': spent_tokens}), flush=True)

    with ThreadPoolExecutor(max_workers=cfg['workers']) as pool:
        iterator = iter(selected)
        pending = set()
        for _ in range(cfg['workers']):
            row = next(iterator, None)
            if row is not None:
                pending.add(pool.submit(run, row))
        while pending:
            done, pending = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                future.result()
                if not stop.is_set():
                    row = next(iterator, None)
                    if row is not None:
                        pending.add(pool.submit(run, row))
    session = {'started_utc': started_utc, 'finished_utc': datetime.now(timezone.utc).isoformat(),
               'elapsed_s': time.perf_counter() - started, 'workers': cfg['workers'],
               'selected': len(selected), 'completed': sum(counts.values()), 'counts': dict(counts),
               'stopped': stop.is_set(), 'reported_cumulative_tokens': spent_tokens,
               'retry_transport': args.retry_transport, 'rate_limit_cooldown_s': 60}
    with (OUT / 'sessions.jsonl').open('a') as file:
        file.write(dumps(session) + '\n')
    print(dumps(session), flush=True)
    if stop.is_set():
        raise SystemExit(1)


if __name__ == '__main__':
    main()
