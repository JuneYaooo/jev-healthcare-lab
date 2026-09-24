"""Bounded concurrent real Jev evaluation; no synthetic response fallback."""
import argparse,concurrent.futures as cf,collections,json,time,urllib.request,urllib.error,threading
import benchmark as b

def run(args):
 key=b.credentials(args.env_file)
 if not key:raise SystemExit('Missing TYPESAFE_API_KEY')
 model=args.model;folder=b.DATA/'runs'/model;folder.mkdir(parents=True,exist_ok=True)
 rows=b.read_prepared() if not args.input else [json.loads(s) for s in open(args.input)]
 counts=collections.Counter();selected=[]
 for r in rows:
  if b.sha(r["request"]) != r["request_sha256"]: raise ValueError("Prepared request hash mismatch")
  if args.task and r['task']!=args.task:continue
  counts[r['task']]+=1
  if args.per_task and counts[r['task']]>args.per_task:continue
  dest=folder/(b.sha([r['task'],r['id'],r['request_sha256']])+'.json')
  if dest.exists() and json.loads(dest.read_text()).get('status')=='ok':continue
  selected.append((r,dest))
 # Bound submitted work; a fatal response stops submission, already running requests may complete.
 selected=selected[:args.max_calls];stop=threading.Event();t0=time.time();total=collections.Counter()
 def one(item):
  r,dest=item
  if stop.is_set():return {'status':'cancelled'}
  result={k:r[k] for k in ('task','id','request_sha256')};start=time.perf_counter()
  if not r['request']['questions']:
   result.update(status='ok',response={'answers':{},'usage':{'input_tokens':0,'output_tokens':0}},elapsed_s=0,deterministic_empty=True)
  else:
   req=urllib.request.Request('https://api.typesafe.ai/v1/systemone',data=b.dumps(dict(r['request'],model=model)).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
   try:
    with urllib.request.urlopen(req,timeout=45) as s:response=json.load(s)
    b.validate_response(r['request'],response)
    result.update(status='ok',response=response)
   except urllib.error.HTTPError as e:
    result.update(status='error',error='HTTPError',http_status=e.code)
    if e.code in (401,402,403,429):stop.set()
   except Exception as e:result.update(status='error',error=type(e).__name__)
   result['elapsed_s']=time.perf_counter()-start
  if dest.exists():
   previous=json.loads(dest.read_text())
   if previous.get('status')!='ok':
    hist=folder/'attempt_history';hist.mkdir(exist_ok=True)
    (hist/(dest.stem+'-'+str(time.time_ns())+'.json')).write_text(b.dumps(previous))
  temp=dest.with_suffix('.tmp');temp.write_text(b.dumps(result));temp.replace(dest);return result
 with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
  it=iter(selected);pending=set()
  for _ in range(args.workers):
   try:pending.add(pool.submit(one,next(it)))
   except StopIteration:break
  while pending:
   done,pending=cf.wait(pending,return_when=cf.FIRST_COMPLETED)
   for f in done:
    result=f.result();total[result['status']]+=1
    total['deterministic_empty']+=bool(result.get('deterministic_empty'))
    if sum(total[k] for k in ('ok','error','cancelled'))%25==0 or result['status']!='ok':print(b.dumps({'counts':dict(total),'elapsed_s':round(time.time()-t0,1),'task':result.get('task'),'error':result.get('error'),'http_status':result.get('http_status')}),flush=True)
    if not stop.is_set():
     try:pending.add(pool.submit(one,next(it)))
     except StopIteration:pass
 status={'status':'STOPPED_ON_FATAL_RESPONSE' if stop.is_set() else 'BATCH_FINISHED','model_requested':model,'selected_uncached':len(selected),'counts':dict(total),'elapsed_s':time.time()-t0}
 (b.OUT/'live_status.json').write_text(b.dumps(status));print(b.dumps(status),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--env-file');p.add_argument('--model',default='jev-1.13.0');p.add_argument('--workers',type=int,default=4);p.add_argument('--max-calls',type=int,default=1200);p.add_argument('--per-task',type=int,default=0);p.add_argument('--task');p.add_argument('--input');a=p.parse_args();assert 1<=a.workers<=8 and a.max_calls>=0;run(a)
