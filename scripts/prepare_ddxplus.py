import benchmark as b
import csv,io,json,ast,hashlib,collections
D=b.DATA/'more';raw=(D/'ddxplus-test-first1m.csv').read_bytes();raw=raw[:raw.rfind(b'\n')+1];pool=list(csv.DictReader(io.StringIO(raw.decode())));ev=json.loads((D/'ddxplus-evidences.json').read_text());cond=json.loads((D/'ddxplus-conditions.json').read_text());tree=json.loads((D/'ddxplus-mirror-tree.json').read_text());audit={}
for name,local in [('release_evidences.json','ddxplus-evidences.json'),('release_conditions.json','ddxplus-conditions.json')]:
 data=(D/local).read_bytes();entry=next(x for x in tree if x['path']==name);assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['oid']
 audit[name]=entry['oid']
valid=[]
for i,r in enumerate(pool):
 try:codes=ast.literal_eval(r['EVIDENCES']);assert r['PATHOLOGY'] in cond
 except Exception:continue
 valid.append(dict(r,id=str(i),codes=codes))
rows=[];criteria={str(i):n for i,n in enumerate(sorted(cond))};idx={v:k for k,v in criteria.items()}
for r in b.sample(valid,100,'ddxplus_prefix'):
 findings=[]
 for code in r['codes']:
  k,*val=code.split('_@_');e=ev[k];answer=e.get('value_meaning',{}).get(val[0],{}).get('en',val[0]) if val else 'yes';findings.append({'question':e['question_en'],'value':answer})
 req=b.choice({'age':r['AGE'],'sex':r['SEX'],'observed_positive_or_categorical_findings':findings},'Choose the most likely primary pathology in this synthetic DDXPlus record from the full disease vocabulary. Only recorded positive/categorical findings are given; no gold differential diagnoses or probabilities are supplied.',criteria)
 x=b.record('ddxplus_synthetic_primary',r['id'],r['id'],req,idx[r['PATHOLOGY']],source='Third-party HF mirror aai530-group6/ddxplus test.csv first1MiB; stable100 sampled complete prefix records; original Figshare403; not whole official test distribution or verified primary bytes',note='Published English evidence translations retained, including awkward word choices; only observed findings, not full negative evidence expansion');x['request_sha256']=b.sha(req);rows.append(x)
(b.DATA/'ddxplus_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));(b.OUT/'ddxplus_source.json').write_text(json.dumps({'original':'https://figshare.com/articles/dataset/DDXPlus_Dataset/20043374','mirror':'https://huggingface.co/datasets/aai530-group6/ddxplus','prefix_bytes':1048576,'complete_valid_prefix_rows':len(valid),'prefix_sha256':hashlib.sha256((D/'ddxplus-test-first1m.csv').read_bytes()).hexdigest(),'metadata_git_blobs':audit,'full_csv_hash_verified':False,'disease_count':len(criteria)},indent=2));print(len(rows),len(valid),len(criteria))
