import json,re,collections
import benchmark as b
D=b.DATA/'more';rows=[]
def add(task,id_,group,state,instruction,criteria,gold,**meta):
 assert gold in criteria,(task,id_,gold)
 r=b.record(task,str(id_),str(group),b.choice(state,instruction,criteria),gold,**meta);r['request_sha256']=b.sha(r['request']);rows.append(r)
def multi(task,id_,group,state,questions,gold,**meta):
 assert set(gold)<=set(questions)
 r=b.record(task,str(id_),str(group),{'state':state,'questions':questions},gold,scoring='multi_question_keys',**meta);r['request_sha256']=b.sha(r['request']);rows.append(r)
for code in ['dp','ep','mp','tp']:
 pool=[];skips=[]
 for i,line in enumerate((D/f'MedJourney/data/basic/{code}.json').read_text().splitlines()):
  r=json.loads(line);r['id']=str(i);m=re.search(r'可能的.+?包括[:：](.+?)。请从',r['prompt'])
  if not m:skips.append(i);continue
  opts=m[1].split('、')
  if r['target'] not in opts:skips.append(i);continue
  r['options']=opts;pool.append(r)
 for r in b.sample(pool,100,code):
  criteria={str(i):x for i,x in enumerate(r['options'])}
  add('medjourney_'+code+'_mcq',r['id'],r['id'],r['prompt'],'从题目提供的选项中选择最佳答案。仅作离线评测。',criteria,str(r['options'].index(r['target'])),source='MedJourney public original options',parser_exclusions=len(skips),parseable_pool=len(pool))
# Patient-hash split; never use target-patient records in candidate retrieval.
pool=[json.loads(s) for s in (D/'CDrugRed/CDrugRed_train.jsonl').read_text().splitlines()]
train=[r for r in pool if int(b.sha(str(r['患者序号']))[:8],16)%5!=0];test=[dict(r,id=r['就诊标识']) for r in pool if int(b.sha(str(r['患者序号']))[:8],16)%5==0]
assert {str(r['患者序号']) for r in train}.isdisjoint(str(r['患者序号']) for r in test)
vocab=json.loads((D/'CDrugRed/候选药物列表.json').read_text());prior=collections.Counter(d for r in train for d in r['出院带药列表']);lookup=collections.defaultdict(collections.Counter)
for r in train:
 for dx in r['出院诊断']:lookup[dx].update(r['出院带药列表'])
for r in b.sample(test,100,'cdr'):
 # Candidate retrieval uses diagnoses and training co-occurrence, plus all vocabulary literal mentions.
 state={k:r[k] for k in ['性别','BMI','诊疗过程描述','入院情况','现病史','既往史','主诉','出院诊断']};scores=collections.Counter()
 for dx in r['出院诊断']:scores.update(lookup.get(dx,{}))
 text=b.dumps(state);candidates=sorted(set([x for x in vocab if x in text]+[x for x,_ in scores.most_common(30)]+[x for x,_ in prior.most_common(10)]))
 # Gold outside candidates retained through label vocabulary universe with scorer mapping.
 questions={str(i):{'type':'noul','instructions':'根据病历判断是否应列入该次就诊的出院带药列表，排除已停用、过敏禁忌和仅在住院中使用的药。仅离线复现数据集，不给患者治疗建议。候选药物：'+x} for i,x in enumerate(candidates)}
 row=b.record('cdrugred_discharge_candidate_pipeline',r['id'],b.sha(str(r['患者序号'])),{'state':state,'questions':questions},r['出院带药列表'],scoring='multi_label_vocabulary',label_vocabulary=candidates,source='patient-hash heldout20% of released training data; 100visits; not official test',candidate_recall_hits=len(set(candidates)&set(r['出院带药列表'])),gold_count=len(set(r['出院带药列表'])),baseline_candidates=[x for x,_ in scores.most_common(5)])
 row['request_sha256']=b.sha(row['request']);rows.append(row)
# Spanish NUBes: gold scope relation to marker. Classify actual target scope, not the marker itself.
pool=[]
for ann in (D/'NUBes-negation-uncertainty-biomedical-corpus/NUBes').rglob('*.ann'):
 ents={};rels=[]
 for s in ann.read_text().splitlines():
  v=s.split('\t')
  if s.startswith('T') and len(v)>=3:
   m=re.fullmatch(r'(\w+) (\d+) (\d+)',v[1])
   if m:ents[v[0]]=(m[1],int(m[2]),int(m[3]),v[2])
  elif s.startswith('R'):
   m=re.fullmatch(r'Scope Arg1:(T\d+) Arg2:(T\d+)',v[1])
   if m:rels.append((m[1],m[2]))
 text=ann.with_suffix('.txt').read_text()
 for cue,target in rels:
  if cue not in ents or target not in ents:continue
  c=ents[cue];t=ents[target];label='negative' if c[0].startswith('Neg') else 'uncertain' if c[0].startswith('Uncert') else None
  if label is None:continue
  lo=max(0,min(c[1],t[1])-160);hi=min(len(text),max(c[2],t[2])+160)
  pool.append(dict(id=ann.stem+':'+target,group=ann.parent.name,state={'excerpt':text[lo:hi],'target':t[3]},gold=label))
for lab in ['negative','uncertain']:
 for r in b.sample([r for r in pool if r['gold']==lab],50,'nubes'+lab):
  add('nubes_scope_status',r['id'],r['group'],r['state'],'Determine the status of the target finding in the Spanish clinical excerpt.','negative uncertain positive'.split() if False else {'negative':'Negated or absent','uncertain':'Possible, suspected or uncertain','positive':'Affirmed present'},lab,source='50/label from published scope annotations; given gold target scope, no positive-class examples; not end-to-end assertion')
(b.DATA/'pipeline_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print(collections.Counter(r['task'] for r in rows),len(rows))
