"""Additional public-label pilots; no explanations or reference answers enter requests."""
import benchmark as b
import duckdb,tarfile,csv,io,collections,json
D=b.DATA/'more';rows=[];audit={}
def add(task,r,state,criteria,gold,**meta):
 req=b.choice(state,'Select the best answer supported by the supplied question or article. For trial outcomes, compare the specified intervention against the specified comparator.',criteria)
 x=b.record(task,str(r['id']),str(r.get('group',r['id'])),req,gold,**meta);x['request_sha256']=b.sha(req);rows.append(x)
for name in ['medqa-en-test','medqa-zh-test','medmcqa-validation']:
 c=duckdb.sql(f"SELECT * FROM read_parquet('{D/(name+'.parquet')}')");pool=[dict(zip(c.columns,x)) for x in c.fetchall()]
 for i,r in enumerate(pool):r['id']=str(r.get('id',i))
 for r in b.sample(pool,100,name):
  if name.startswith('medqa'):criteria={x['key']:x['value'] for x in r['options']};gold=r['answer_idx']
  else:criteria={str(i):r['op'+k] for i,k in enumerate('abcd')};gold=str(r['cop'])
  assert gold in criteria
  add(name.replace('-','_'),r,r['question'],criteria,gold,source='HF public mirror of published '+name,source_rows=len(pool),note='MedMCQA released cop is one answer index even when choice_type says multi; scored as published MCQ, not multiselect')
with tarfile.open(D/'evidence-inference.tar.gz') as t:
 def csvread(n):return list(csv.DictReader(io.StringIO(t.extractfile(n).read().decode('utf-8-sig'))))
 ann=csvread('annotations_merged.csv');prompts=csvread('prompts_merged.csv');test=set(t.extractfile('splits/test_article_ids.txt').read().decode().split());votes=collections.defaultdict(lambda:collections.defaultdict(set));excluded=collections.Counter()
 for a in ann:
  if a['Valid Label'].lower() in ['true','1'] and a['Label Code'] in ['-1','0','1']:votes[a['PromptID']][a['UserID']].add(a['Label Code'])
 pool=[]
 for p in prompts:
  if p['PMCID'] not in test:continue
  vv=votes[p['PromptID']]
  if not vv or any(len(v)!=1 for v in vv.values()):excluded['missing_or_inconsistent_annotator']+=1;continue
  tally=collections.Counter(next(iter(v)) for v in vv.values());top=tally.most_common()
  if len(top)>1 and top[0][1]==top[1][1]:excluded['tied_label']+=1;continue
  try:text=t.extractfile('txt_files/PMC'+p['PMCID']+'.txt').read().decode()
  except KeyError:excluded['missing_article']+=1;continue
  if len(text)>70000:excluded['article_over_70000_chars']+=1;continue
  pool.append(dict(id=p['PromptID'],group=p['PMCID'],gold=top[0][0],article=text,ico={k:p[k] for k in ['Intervention','Comparator','Outcome']},votes=dict(tally)))
 for r in b.sample(pool,100,'evidence_inference'):
  add('evidence_inference_fulltext',r,{'article':r['article'],**r['ico']},{'-1':'Significantly decreased','0':'No significant difference','1':'Significantly increased'},r['gold'],source='Evidence Inference v2 official test article split; majority of distinct valid annotators; ties excluded; full untruncated article <=70000 characters',valid_label_votes=r['votes'])
 audit['evidence_inference']={'eligible_pool':len(pool),'excluded':dict(excluded),'article_length_cap_chars':70000}
(b.DATA/'last_datasets_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));(b.OUT/'last_datasets_preparation.json').write_text(json.dumps(audit,indent=2));print(len(rows),audit)
