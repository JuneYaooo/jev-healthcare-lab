"""Append verified real evaluations while preserving every existing sample and response."""
import argparse,collections,hashlib,json,shutil
from pathlib import Path
import benchmark as b
import analyze_results
ROOT=Path(__file__).resolve().parents[1]
def read(p):return [json.loads(x) for x in p.read_text().splitlines()]
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def file_info(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,nargs='+',required=True);ap.add_argument('--preparation',nargs='+',default=['scripts/prepare_expansion.py','scripts/prepare_media_expansion.py']);args=ap.parse_args()
 scenes=json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes'];folders={t:ROOT/'scenarios'/s['id']/t for s in scenes for t in s['task_ids']}
 additions=collections.defaultdict(list)
 for p in args.input:
  for r in read(p):additions[r['task']].append(r)
 cache=ROOT/'data/expansion/runs/jev-1.13.0';indices=read(ROOT/'results/evaluation_index.jsonl');added=0
 # Validate all new responses before mutating any archive.
 for task,rs in additions.items():
  for r in rs:
   response=json.loads((cache/(b.sha([task,r['id'],r['request_sha256']])+'.json')).read_text())
   assert response['status']=='ok',(task,r['id'],response['status'])
   b.validate_response(r['request'],response['response'])
 for task,rs in additions.items():
  folder=folders[task];old=read(folder/'samples.jsonl');seen={r['id']:r['request_sha256'] for r in old};new=[];raws=[];local=read(folder/'index.jsonl')
  for r in rs:
   if r['id'] in seen:
    assert seen[r['id']]==r['request_sha256'];continue
   raw=(cache/(b.sha([task,r['id'],r['request_sha256']])+'.json')).read_bytes().rstrip(b'\n');new.append(r);raws.append(raw)
   ix={'task':task,'id':r['id'],'group':r['group'],'domain':'medical','deterministic_empty':False,'request_sha256':r['request_sha256'],'response_sha256':hashlib.sha256(raw).hexdigest()};local.append(ix);indices.append(ix)
  if not new:continue
  added+=len(new)
  with (folder/'samples.jsonl').open('a') as f:f.write(''.join(b.dumps(r)+'\n' for r in new))
  with (folder/'responses.jsonl').open('ab') as f:f.write(b'\n'.join(raws)+b'\n')
  (folder/'index.jsonl').write_text(''.join(b.dumps(i)+'\n' for i in local))
  allrows=old+new;prompts={}
  for r in allrows:
   for q in r['request']['questions'].values():
    key=b.sha(q);prompts.setdefault(key,{'question':q,'occurrences':0,'example_sample_id':r['id']});prompts[key]['occurrences']+=1
  dump(folder/'prompts.json',{'origin':'Exact question objects from archived requests.','variants':list(prompts.values())})
  prov=json.loads((folder/'provenance.json').read_text());prov['sample_count']=len(allrows);prov['groups']=len({r['group'] for r in allrows});prov['files']={n:file_info(folder/n) for n in prov['files']}
  prov.setdefault('supplements',[]).append({'sample_ids':[r['id'] for r in new],'sources':sorted({r['metadata']['source'] for r in new}),'preparation':args.preparation})
  dump(folder/'provenance.json',prov)
 (ROOT/'results/evaluation_index.jsonl').write_text(''.join(b.dumps(i)+'\n' for i in indices))
 allrows=[]
 for folder in folders.values():
  allrows+=read(folder/'samples.jsonl')
  for raw in (folder/'responses.jsonl').read_bytes().splitlines():
   r=json.loads(raw);p=cache/(b.sha([r['task'],r['id'],r['request_sha256']])+'.json')
   if not p.exists():p.write_bytes(raw)
 b.DATA=ROOT/'data/expansion';b.OUT=ROOT/'results';b.read_prepared=lambda:allrows
 analyze_results.main()
 metrics=json.loads((ROOT/'results/all_results.json').read_text())
 for task,folder in folders.items():dump(folder/'results.json',metrics['tasks'][task])
 snapshot=json.loads((ROOT/'results/snapshot.json').read_text());snapshot.update(evaluation_rows=len(indices),deterministic_empty_rows=sum(i['deterministic_empty'] for i in indices),successful_api_responses=sum(not i['deterministic_empty'] for i in indices));dump(ROOT/'results/snapshot.json',snapshot)
 archive=json.loads((ROOT/'results/archive_summary.json').read_text());archive.update(main_rows=len(allrows),verified_request_response_pairs=len(indices),raw_scope='Actual text inputs, labels, prompts and real model responses; selected upstream ASR audio excerpts and OCR scans. Not the full source datasets.');dump(ROOT/'results/archive_summary.json',archive)
 assetfile=ROOT/'data/expansion/media_assets.json'
 if assetfile.exists():
  for a in json.loads(assetfile.read_text()):
   folder=folders[a['task']];target=folder/'upstream/expansion'/a['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'data/expansion/media'/a['path'],target)
   manifest=folder/'upstream/manifest.json';items=json.loads(manifest.read_text());rel=str(target.relative_to(folder));items=[i for i in items if i['file']!=rel];items.append({'file':rel,'source':a['source'],**file_info(target)});dump(manifest,items)
 attempts=collections.defaultdict(list)
 for p in sorted((cache/'attempt_history').glob('*.json')):
  r=json.loads(p.read_text())
  if r['task'] in folders:attempts[r['task']].append(r)
 for task,records in attempts.items():
  folder=folders[task];p=folder/'attempts.jsonl';p.write_text(''.join(b.dumps(r)+'\n' for r in records))
  prov=json.loads((folder/'provenance.json').read_text());prov['files']['attempts.jsonl']=file_info(p);dump(folder/'provenance.json',prov)
 print('Appended',added,'records; total main records',len(allrows))
if __name__=='__main__':main()
