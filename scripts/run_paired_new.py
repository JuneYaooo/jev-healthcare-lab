"""Run locked fresh-data grouping comparisons with pooled connections."""
import argparse,concurrent.futures as cf,json,threading,time,random
from pathlib import Path
import httpx
import benchmark as b
from compare_deepseek import request_payload,normalize
from prepare_paired_new import BASE

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--env-file',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--off-peak',action='store_true');a=ap.parse_args()
 assert not a.output.exists(),'Use a new output directory; never merge incomplete runs'
 rows=[json.loads(x) for x in (BASE/'inputs.jsonl').read_text().splitlines()];protocol=json.loads((BASE/'protocol.json').read_text());assert b.sha(rows)==protocol['selection_sha256']
 keys={k:v.strip().strip('"').strip("'") for line in a.env_file.read_text().splitlines() if '=' in line and not line.startswith('#') for k,v in [line.split('=',1)]}
 urls={'jev':'https://api.typesafe.ai/v1/systemone','deepseek':'https://api.deepseek.com/chat/completions'}
 clients={p:httpx.Client(timeout=httpx.Timeout(30,connect=10),limits=httpx.Limits(max_connections=4,max_keepalive_connections=4,keepalive_expiry=300),headers={'Authorization':'Bearer '+keys['TYPESAFE_API_KEY' if p=='jev' else 'DEEPSEEK_API_KEY']}) for p in urls}
 a.output.mkdir(parents=True);stop=threading.Event();lock=threading.Lock();spend=0
 (a.output/'protocol.json').write_text((BASE/'protocol.json').read_text())
 try:
  with (a.output/'responses.jsonl').open('w') as out,(a.output/'blocks.jsonl').open('w') as blocks:
   for block in protocol['order']:
    if stop.is_set():break
    p=block['provider'];size=block['group_size'];ordered=rows[:];random.Random(421+block['round']).shuffle(ordered);t0=time.perf_counter();done=[]
    def one(row):
     nonlocal spend
     start=time.perf_counter();result=dict(block,id=row['id'],started_after_s=start-t0,calls=[])
     qs=list(row['request']['questions'])
     for offset in range(0,len(qs),size):
      names=qs[offset:offset+size];req={'state':row['request']['state'],'questions':{q:row['request']['questions'][q] for q in names}}
      payload=dict(req,model='jev-1.13.0') if p=='jev' else request_payload({'request':req})
      call={'question_ids':names,'request_sha256':b.sha(req),'provider_request_sha256':b.sha(payload),'attempts':[]}
      for attempt in range(2):
       if stop.is_set():break
       begin=time.perf_counter();rec={'started_after_s':begin-t0,'trace':[]}
       def trace(name,info):rec['trace'].append({'event':name,'after_s':time.perf_counter()-begin})
       try:
        response=clients[p].post(urls[p],json=payload,extensions={'trace':trace});response.raise_for_status();data=response.json();rec['response']=data;u=data['usage']
        if p=='jev':cost=u['input_tokens']*.042/1e6
        else:
         hit=u.get('prompt_cache_hit_tokens',0);miss=u.get('prompt_cache_miss_tokens',u['prompt_tokens']-hit);cost=(hit*.003+miss*.15+u['completion_tokens']*.6)*(1 if a.off_peak else 2)/1e6
        rec['cost_usd']=cost;rec['tariff']='off_peak' if a.off_peak else 'peak'
        with lock:
         spend+=cost
         if spend>=2:stop.set()
        if p=='jev':b.validate_response(req,data);answers={q:data['answers'][q]['choice'] for q in names}
        else:
         if data['choices'][0]['finish_reason']!='stop':raise ValueError('Incomplete output')
         norm=normalize({'request':req},data);answers={q:norm[q]['choice'] for q in names}
        rec.update(status='ok',answers=answers)
       except httpx.HTTPStatusError as e:
        rec.update(status='http_error',http_status=e.response.status_code)
        if e.response.status_code in (401,402,403,429):stop.set()
       except Exception as e:rec.update(status='error',error_type=type(e).__name__)
       rec['elapsed_s']=time.perf_counter()-begin;rec['finished_after_s']=time.perf_counter()-t0;call['attempts'].append(rec)
       if rec['status']=='ok' or stop.is_set():break
       if attempt==0:time.sleep(1)
      result['calls'].append(call)
     result['finished_after_s']=time.perf_counter()-t0;result['elapsed_s']=time.perf_counter()-start;return result
    with cf.ThreadPoolExecutor(max_workers=4) as pool:
     for f in cf.as_completed([pool.submit(one,r) for r in ordered]):
      r=f.result();done.append(r);out.write(b.dumps(r)+'\n');out.flush()
    stats=dict(block,batch_elapsed_s=time.perf_counter()-t0,documents=len(done),aborted=stop.is_set(),reported_cost_usd=sum(at.get('cost_usd',0) for r in done for c in r['calls'] for at in c['attempts']))
    blocks.write(b.dumps(stats)+'\n');blocks.flush();print(b.dumps(stats),flush=True)
 finally:
  for c in clients.values():c.close()
 if stop.is_set():raise SystemExit('Stopped on service/auth/budget condition; incomplete run remains archived locally')
 print('Completed all paired blocks; reported USD',round(spend,6),flush=True)
if __name__=='__main__':main()
