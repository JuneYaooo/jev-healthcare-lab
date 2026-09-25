"""Measure end-to-end batch wall time with equal concurrency and retry limits."""
import argparse,concurrent.futures as cf,collections,json,threading,time,urllib.request,urllib.error
from pathlib import Path
import benchmark as b
from compare_deepseek import request_payload,normalize

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--env-file',type=Path,required=True);ap.add_argument('--provider',choices=['jev','deepseek'],required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--workers',type=int,default=8);ap.add_argument('--timeout',type=int,default=45);ap.add_argument('--max-usd',type=float,default=5);ap.add_argument('--off-peak',action='store_true');a=ap.parse_args()
 if a.output.exists():raise SystemExit('Output already exists; refusing to blend batches')
 rows=[json.loads(x) for x in a.input.read_text().splitlines()];assert len({(r['task'],r['id']) for r in rows})==len(rows)
 secrets=dict(x.split('=',1) for x in a.env_file.read_text().splitlines() if '=' in x and not x.startswith('#'))
 key=secrets['TYPESAFE_API_KEY' if a.provider=='jev' else 'DEEPSEEK_API_KEY'];url='https://api.typesafe.ai/v1/systemone' if a.provider=='jev' else 'https://api.deepseek.com/chat/completions'
 a.output.mkdir(parents=True);stop=threading.Event();lock=threading.Lock();cost=0;counts=collections.Counter();completed=[]
 t0=time.perf_counter()
 def one(row):
  nonlocal cost
  result={'task':row['task'],'id':row['id'],'request_sha256':row['request_sha256'],'started_after_s':time.perf_counter()-t0,'attempts':[]}
  payload=dict(row['request'],model='jev-1.13.0') if a.provider=='jev' else request_payload(row)
  result['provider_request_sha256']=b.sha(payload)
  if not row['request']['questions']:
   result.update(status='ok',deterministic_empty=True,finished_after_s=time.perf_counter()-t0);return result
  for attempt in range(2):
   if stop.is_set():result['status']='cancelled';break
   rec={'started_after_s':time.perf_counter()-t0};start=time.perf_counter()
   try:
    req=urllib.request.Request(url,data=b.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=a.timeout) as response:data=json.load(response)
    rec['response']=data;u=data['usage']
    if a.provider=='jev':c=u['input_tokens']*.042/1e6
    else:
     h=u.get('prompt_cache_hit_tokens',0);m=u.get('prompt_cache_miss_tokens',u['prompt_tokens']-h);c=(h*.003+m*.15+u['completion_tokens']*.6)*(1 if a.off_peak else 2)/1e6
    rec['cost_usd']=c
    with lock:
     cost+=c
     if cost>=a.max_usd:stop.set()
    if a.provider=='jev':b.validate_response(row['request'],data)
    else:
     if data['choices'][0]['finish_reason']!='stop':raise ValueError('Incomplete output')
     normalize(row,data)
    rec['status']='ok'
   except urllib.error.HTTPError as e:
    rec.update(status='http_error',http_status=e.code)
    if e.code in (401,402,403,429):stop.set()
   except Exception as e:rec.update(status='error',error_type=type(e).__name__)
   rec['elapsed_s']=time.perf_counter()-start;rec['finished_after_s']=time.perf_counter()-t0;result['attempts'].append(rec);result['status']=rec['status']
   if rec['status']=='ok' or stop.is_set():break
   if attempt==0:time.sleep(1)
  result['finished_after_s']=time.perf_counter()-t0
  return result
 with (a.output/'responses.jsonl').open('w') as out,cf.ThreadPoolExecutor(max_workers=a.workers) as pool:
  for future in cf.as_completed([pool.submit(one,r) for r in rows]):
   r=future.result();completed.append(r);counts[r['status']]+=1;out.write(b.dumps(r)+'\n');out.flush()
   if len(completed)%250==0:print(b.dumps({'provider':a.provider,'completed':len(completed),'planned':len(rows),'elapsed_s':round(time.perf_counter()-t0,2),'counts':dict(counts)}),flush=True)
 elapsed=time.perf_counter()-t0
 summary={'provider':a.provider,'rows':len(rows),'workers':a.workers,'socket_timeout_s':a.timeout,'max_attempts_per_input':2,'retry_delay_s':1,'batch_elapsed_s':elapsed,'counts':dict(counts),'completed_without_abort':not stop.is_set(),'input_sha256':b.sha([(r['task'],r['id'],r['request_sha256']) for r in rows]),'cost_usd':cost,'cost_scope':'Separate timing replay; not included in original evaluation fee estimates.','scope':'Full batch wall time from submission through all terminal results; includes queueing, timeouts, retry delays and failures; no local response-cache reuse. One trial only.','off_peak_pricing':a.off_peak if a.provider=='deepseek' else None}
 (a.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(b.dumps(summary),flush=True)
if __name__=='__main__':main()
