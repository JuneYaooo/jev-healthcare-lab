"""Verify full-batch timing evidence against all archived evaluation inputs."""
import collections,json,math
from pathlib import Path
import benchmark as b
from compare_deepseek import request_payload,normalize,load_rows
ROOT=Path(__file__).resolve().parents[1]

def verify():
 base=ROOT/'comparisons/batch-time';sources={(r['task'],r['id']):r for r in load_rows()}
 order=[json.loads(x) for x in (base/'input_index.jsonl').read_text().splitlines()]
 assert len(order)==len(sources) and {(r['task'],r['id']) for r in order}==set(sources)
 digest=b.sha([(r['task'],r['id'],r['request_sha256']) for r in order])
 for provider in ['jev','deepseek']:
  folder=base/provider;summary=json.loads((folder/'summary.json').read_text());seen=set();counts=collections.Counter();total_cost=0
  assert summary['completed_without_abort'] and summary['rows']==len(order)
  assert summary['input_sha256']==digest and summary['workers']==8 and summary['socket_timeout_s']==45 and summary['max_attempts_per_input']==2
  for line in (folder/'responses.jsonl').read_text().splitlines():
   r=json.loads(line);key=(r['task'],r['id']);row=sources[key];assert key not in seen;seen.add(key);counts[r['status']]+=1
   assert r['request_sha256']==row['request_sha256']
   payload=dict(row['request'],model='jev-1.13.0') if provider=='jev' else request_payload(row)
   assert r['provider_request_sha256']==b.sha(payload)
   assert 0<=r['started_after_s']<=r['finished_after_s']<=summary['batch_elapsed_s']
   if not row['request']['questions']:
    assert r.get('deterministic_empty') and r['status']=='ok' and not r['attempts'];continue
   assert 1<=len(r['attempts'])<=2 and r['status']==r['attempts'][-1]['status']
   previous=r['started_after_s']
   for attempt in r['attempts']:
    assert previous<=attempt['started_after_s']<=attempt['finished_after_s']<=r['finished_after_s'];previous=attempt['finished_after_s']
    assert math.isclose(attempt['elapsed_s'],attempt['finished_after_s']-attempt['started_after_s'],abs_tol=.02)
    if 'response' not in attempt:
     assert attempt['status']!='ok';continue
    data=attempt['response'];u=data['usage']
    if provider=='jev':cost=u['input_tokens']*.042/1e6
    else:
     h=u.get('prompt_cache_hit_tokens',0);m=u.get('prompt_cache_miss_tokens',u['prompt_tokens']-h);cost=(h*.003+m*.15+u['completion_tokens']*.6)*(1 if summary['off_peak_pricing'] else 2)/1e6
    assert math.isclose(cost,attempt['cost_usd'],abs_tol=1e-12);total_cost+=cost
    if attempt['status']=='ok':
     if provider=='jev':b.validate_response(row['request'],data)
     else:assert data['choices'][0]['finish_reason']=='stop';normalize(row,data)
   if len(r['attempts'])==2:assert r['attempts'][0]['status']!='ok'
  assert seen==set(sources) and dict(counts)==summary['counts']
  assert math.isclose(total_cost,summary['cost_usd'],abs_tol=1e-9)
  print(provider,summary['rows'],'inputs, batch seconds',round(summary['batch_elapsed_s'],2),'verified')
if __name__=='__main__':verify()
