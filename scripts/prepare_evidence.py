import json,re,tarfile,gzip,zipfile,collections,ast,csv
import benchmark as b
D=b.DATA/'more';rows=[]
def add(task,id_,group,state,instruction,criteria,gold,**meta):
 assert gold in criteria,(task,id_,gold)
 r=b.record(task,str(id_),str(group),b.choice(state,instruction,criteria),gold,**meta);r['request_sha256']=b.sha(r['request']);rows.append(r)
def multi(task,id_,group,state,questions,gold,**meta):
 assert set(gold)<=set(questions)
 r=b.record(task,str(id_),str(group),{'state':state,'questions':questions},gold,scoring='multi_question_keys',**meta);r['request_sha256']=b.sha(r['request']);rows.append(r)
# SciFact: known cited abstract; includes NOINFO, neither gold rationale nor gold evidence supplied.
with tarfile.open(D/'scifact-data.tar.gz') as z:
 corpus={str(r['doc_id']):r for r in map(json.loads,z.extractfile('data/corpus.jsonl'))};claims=list(map(json.loads,z.extractfile('data/claims_dev.jsonl')))
 for r in b.sample(claims,100,'scifact'):
  for docid in r['cited_doc_ids']:
   ev=r['evidence'].get(str(docid),[]);labels={e['label'] for e in ev};assert len(labels)<=1
   add('scifact_cited_abstract',str(r['id'])+':'+str(docid),r['id'],{'claim':r['claim'],'abstract':corpus[str(docid)]['abstract']},'Does this supplied abstract support or refute the scientific claim? Use NOINFO if neither follows. Assess only this abstract.',{'SUPPORT':'Supports','CONTRADICT':'Contradicts','NOINFO':'Insufficient evidence'},next(iter(labels)) if labels else 'NOINFO',source='SciFact dev; cited-document oracle retrieval, includes NEI, not end-to-end corpus search')
# MedMentions ST21pv: official test, given gold mention boundary; no concept IDs in model state.
vocab=dict(re.findall(r'\*\s+(T\d+): (.+?) \(level',(D/'MedMentions/st21pv/ReadMe.md').read_text()))
test=set((D/'MedMentions/full/data/corpus_pubtator_pmids_test.txt').read_text().split())
pool=[]
with gzip.open(D/'MedMentions/st21pv/data/corpus_pubtator.txt.gz','rt') as f:
 for block in f.read().strip().split('\n\n'):
  lines=block.splitlines();pid=lines[0].split('|')[0]
  if pid not in test:continue
  text=' '.join(s.split('|',2)[2] for s in lines if '|t|' in s or '|a|' in s)
  for s in lines:
   v=s.split('\t')
   if len(v)>=6 and v[4] in vocab:pool.append(dict(id=pid+':'+v[1],pid=pid,text=text,mention=v[3],gold=v[4]))
for r in b.sample(pool,100,'medmentions'):
 add('medmentions_type_oracle_span',r['id'],r['pid'],{'abstract':r['text'],'mention':r['mention']},'Classify the target mention into the supplied UMLS semantic type categories, considering this context.',vocab,r['gold'],source='ST21pv official test; gold boundaries; not linking to CUIs or end-to-end NER')
# NCBI Disease: exact annotated mention category, official test.
with zipfile.ZipFile(D/'ncbi-test.zip') as z:raw=z.read('NCBItestset_corpus.txt').decode()
pool=[]
for block in raw.strip().split('\n\n'):
 lines=block.splitlines();text=' '.join(s.split('|',2)[2] for s in lines if '|t|' in s or '|a|' in s)
 for s in lines:
  v=s.split('\t')
  if len(v)==6:pool.append(dict(id=v[0]+':'+v[1],pid=v[0],text=text,mention=v[3],gold=v[4]))
criteria={'SpecificDisease':'Specific disease entity','DiseaseClass':'A class or category of diseases','CompositeMention':'Composite mention combining multiple diseases','Modifier':'Disease term used as a modifier'}
for r in b.sample(pool,100,'ncbi'):
 add('ncbi_disease_category_oracle_span',r['id'],r['pid'],{'abstract':r['text'],'mention':r['mention']},'Classify the annotated disease mention category in context.',criteria,r['gold'],source='NCBI Disease official test, given span; not disease detection or normalization')
# EBM-NLP: expert aggregated starting-spans. Fixed 8-token windows avoid gold-selected boundaries.
with tarfile.open(D/'EBM-NLP/ebm_nlp_1_00.tar.gz') as z:
 names={n for n in z.getnames()};prefix='ebm_nlp_1_00/annotations/aggregated/starting_spans/';cats=['participants','interventions','outcomes'];pids=sorted({n.split('/')[-1].split('_')[0] for n in names if n.startswith(prefix+'participants/test/gold/') and n.endswith('.ann')})
 pool=[]
 for pid in pids:
  paths=[prefix+c+'/test/gold/'+pid+'_AGGREGATED.ann' for c in cats]
  if not all(p in names for p in paths):continue
  tokens=z.extractfile('ebm_nlp_1_00/documents/'+pid+'.tokens').read().decode().split();labs=[list(map(int,re.split(r'[,\s]+',z.extractfile(p).read().decode().strip()))) for p in paths]
  assert all(len(x)==len(tokens) for x in labs)
  for start in range(0,len(tokens),8):
   end=min(start+8,len(tokens));gold=[c for c,lab in zip(cats,labs) if sum(lab[start:end])>(end-start)/2]
   pool.append(dict(id=pid+':'+str(start),pid=pid,state={'abstract':' '.join(tokens),'target_window':' '.join(tokens[start:end]),'token_start':start},gold=gold))
 for r in b.sample(pool,100,'ebm'):
  qs={c:{'type':'noul','instructions':f'Does more than half of the target token window describe the {c} of this clinical trial? Use surrounding abstract for context.'} for c in cats}
  multi('ebm_pico_fixed_windows',r['id'],r['pid'],r['state'],qs,r['gold'],source='expert aggregated test gold, adapted 8-token-window multilabel not official token F1')
# EvidenceBench all37dev full papers, adapted relevant-sentence selection; union-aspect labels.
for id_,r in json.loads((D/'EvidenceBench/datasets/evidencebench_dev_set.json').read_text()).items():
 texts=r['paper_as_candidate_pool'];mapping=r['sentence_index2aspects'];mapping=ast.literal_eval(mapping) if isinstance(mapping,str) else mapping
 gold=[str(i) for i in range(len(texts)) if mapping.get(str(i))];qs={str(i):{'type':'noul','instructions':f'Does sentence {i} contain evidence relevant to assessing the hypothesis? Select evidence on population, intervention/exposure, comparison, outcomes or findings; exclude mere background.'} for i in range(len(texts))}
 multi('evidencebench_sentence_selection',id_,r['paper_id'],{'hypothesis':r['hypothesis'],'sentences':{str(i):t for i,t in enumerate(texts)}},qs,gold,source='all37dev; adapted union of annotated evidence-aspect sentences, not official set-cover ranking metric')
# MedAL published toy sample: fixed vocabulary from whole demo; no train/test claim.
medal=list(csv.DictReader((D/'medal/toy_data/sample.csv').open()));vocab=sorted({r['LABEL'] for r in medal});criteria={str(i):x for i,x in enumerate(vocab)}
for i,r in enumerate(medal[:100]):
 toks=r['TEXT'].split();loc=int(r['LOCATION']);add('medal_demo_disambiguation',i,r['ABSTRACT_ID'],{'abstract':r['TEXT'],'target_token_position_zero_based':loc,'target_token':toks[loc]},'Select the intended expansion of the target abbreviation in this abstract.',criteria,str(vocab.index(r['LABEL'])),source='first100 published toy rows; full-demo expansion vocabulary, not held-out full MedAL performance')
(b.DATA/'evidence_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print(collections.Counter(r['task'] for r in rows),len(rows))
