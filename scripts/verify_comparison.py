"""Check complete same-input comparison, raw archives, adaptation and recomputed scores."""
import hashlib
import json
from pathlib import Path
from compare_deepseek import ROOT,load_rows,normalize,request_payload,sha
from analyze_comparison import summarize
from verify_experiments import same_metrics


def verify_cost(record):
    if 'response' not in record:
        if record.get('cost_usd',0)!=0:raise ValueError('Cost has no usage evidence')
        return
    u=record['response']['usage'];factor=2 if record['tariff']=='peak' else 1
    hit=u.get('prompt_cache_hit_tokens',0);miss=u.get('prompt_cache_miss_tokens',u['prompt_tokens']-hit)
    cost=(hit*.003+miss*.15+u['completion_tokens']*.6)*factor/1e6
    if abs(cost-record['cost_usd'])>1e-12:raise ValueError('Cost mismatch')


def verify():
    source={(r['task'],r['id']):r for r in load_rows()}
    base=ROOT/'comparisons/deepseek-flash'
    for item in json.loads((base/'archive_manifest.json').read_text()):
        if hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Comparison file hash changed: '+item['path'])
    seen=set()
    for p in (ROOT/'scenarios').glob('*/*/comparison/deepseek_responses.jsonl'):
        for line in p.read_text().splitlines():
            r=json.loads(line);key=(r['task'],r['id']);row=source[key]
            if key in seen:raise ValueError('Duplicate comparison identity')
            seen.add(key)
            if r['request_sha256']!=row['request_sha256'] or r['provider_request_sha256']!=sha(request_payload(row)):raise ValueError('Provider input changed')
            verify_cost(r)
            if r['status']!='ok':
                if 'response' in r and r['response']['choices'][0]['finish_reason']=='stop':
                    try:normalize(row,r['response'])
                    except (ValueError,KeyError,TypeError):pass
                    else:raise ValueError('Valid response incorrectly counted as failure')
                continue
            if not row['request']['questions']:
                if not r.get('deterministic_empty') or r['normalized_answers']!={}:raise ValueError('Empty response mismatch')
                continue
            if normalize(row,r['response'])!=r['normalized_answers']:raise ValueError('Output adaptation changed')
            if r['response']['choices'][0]['finish_reason']!='stop':raise ValueError('Incomplete final response')
    for p in (ROOT/'scenarios').glob('*/*/comparison/deepseek_attempts.jsonl'):
        for line in p.read_text().splitlines():
            r=json.loads(line);row=source[(r['task'],r['id'])]
            if r['request_sha256']!=row['request_sha256'] or r['provider_request_sha256']!=sha(request_payload(row)):raise ValueError('Retry input changed')
            if r['status']=='ok':raise ValueError('A valid response was retried')
            verify_cost(r)
    if seen!=set(source):raise ValueError('Comparison does not cover all original main rows')
    expected=json.loads((base/'summary.json').read_text());actual=summarize(write=False,archived=True)
    if not same_metrics(actual,expected):raise ValueError('Recomputed comparison differs from published results')
    for p in (ROOT/'scenarios').glob('*/*/comparison/results.json'):
        if not same_metrics(json.loads(p.read_text()),actual['tasks'][p.parent.parent.name]):raise ValueError('Task comparison differs')
    print(f'Verified {len(seen)} same-input comparison rows; scores, prompts, costs and archives match.')


if __name__=='__main__':verify()
