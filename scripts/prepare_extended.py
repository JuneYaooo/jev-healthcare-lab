"""Additional public datasets. Gold never enters request state; closed label spaces declared independently."""
import json,collections,re,zipfile,xml.etree.ElementTree as ET,hashlib
import benchmark as b
rows=[]
def add(task,id_,group,state,instruction,criteria,gold,**meta):
 r=b.record(task,id_,group,b.choice(state,instruction,criteria),gold,**meta)
 assert gold in criteria,(task,id_,gold)
 r['request_sha256']=b.sha(r['request']);rows.append(r)
# Public DDI test set, class-stratified diagnostic panel. Given entity pairs, not end-to-end discovery.
criteria={'none':'No stated interaction between the two target mentions.', 'mechanism':'Pharmacokinetic mechanism (e.g. concentration, absorption, metabolism).','effect':'Pharmacodynamic effect or clinical outcome of co-use.','advise':'Advice, precaution or contraindication about co-use.','int':'Interaction stated without specifying its kind.'}
buckets=collections.defaultdict(list)
with zipfile.ZipFile(b.DATA/'ddi2013.zip') as z:
 for name in z.namelist():
  if not(name.endswith('.xml') and '/Test/' in name and 'Extraction' in name):continue
  root=ET.fromstring(z.read(name))
  for s in root.findall('sentence'):
   entities={e.attrib['id']:e.attrib for e in s.findall('entity')}
   for p in s.findall('pair'):
    label=p.attrib.get('type','none')
    state={'sentence':s.attrib['text'],'target_1':{k:entities[p.attrib['e1']][k] for k in ('text','charOffset')},'target_2':{k:entities[p.attrib['e2']][k] for k in ('text','charOffset')}}
    buckets[label].append({'id':p.attrib['id'],'group':root.attrib.get('id',name),'state':state})
 for label,pool in buckets.items():
  for r in b.sample(pool,30,'ddi-'+label):add('ddi_relation_oracle_pairs',r['id'],r['group'],r['state'],'Classify only the relation stated between the two target drug mentions in this sentence, not outside drug knowledge.',criteria,label,scope='official test subset; 30/class; given gold entity pair, not end-to-end NER',population_class_count=len(pool))
# Public clinical calculator benchmark, sufficient and insufficient cases mixed.
faith=b.load('cmedcalc-faithful.json')
positive=[]
for split in ('equation','score','semantic'):
 for x in b.load('cmedcalc-'+split+'.json'):positive.append(dict(x,id=split+':'+str(x['id'])))
for label,pool in [('insufficient',faith),('sufficient',positive)]:
 for r in b.sample(pool,100,'cmedcalc-'+label):
  add('cmedcalc_input_sufficiency',label+':'+str(r['id']),str(r['id']),{'indicator':r['指标名称'],'note':r['record_final']},'只判断病历是否提供了计算/分级该指标所必需且不矛盾的资料。不要编造缺失参数。正常知识可以用于理解指标，但不能替代患者资料。',{'sufficient':'必要资料完整且不矛盾，可以计算或分级','insufficient':'缺失必要资料或有未解决矛盾，不能可靠计算或分级'},label,scope='adapted binary gate; 100 original unanswerable +100 original answerable; not original numerical score')
# Semantic grade labels use predefined complete scales, not per-row gold-derived distractors.
roman={'Ⅰ':'I','Ⅱ':'II','Ⅲ':'III','Ⅳ':'IV'}
def canon(s):
 for a,c in roman.items():s=s.replace(a,c)
 return s
for r in b.load('cmedcalc-semantic.json'):
 name=r['指标名称'];answer=canon(str(r['answer_final']));options=None;gold=None
 if name.startswith('ASIA'):options=list('ABCDE');gold=re.search('[ABCDE]',answer)[0]
 elif name.startswith(('Barnett','Killip','NYHA')):options=['I','II','III','IV'];gold=re.search('IV|III|II|I',answer)[0]
 elif name.startswith('Forrest'):options=['Ia','Ib','IIa','IIb','IIc','III'];gold=re.search('II[abc]|I[ab]|III',answer)[0]
 elif name.startswith('MRC'):options=['0','1','1+','2-','2','2+','3-','3','3+','4-','4','4+','5-','5'];gold=re.search(r'\d[+-]?',answer)[0]
 elif name.startswith('Levine'):options=list('0123456');gold=re.search(r'\d',answer)[0]
 elif name.startswith('Wagner'):options=list('012345');gold=re.search(r'\d',answer)[0]
 elif name.startswith('吞咽'):options=list('12345');gold=re.search(r'\d',answer)[0]
 elif name.startswith('Taylor'):
  options=['0','I','II','III','IV'];gold=re.search('IV|III|II|I|[01234]',answer)[0];gold={'1':'I','2':'II','3':'III','4':'IV'}.get(gold,gold)
 elif name.startswith('SLEDAI'):
  options=['无活动','轻度活动','中度活动','高度活动','极高度活动'];gold=next(x for x in reversed(options) if x in answer)
 elif name.startswith('三度'):options=['I度','浅II度','深II度','III度'];gold=answer
 else:raise ValueError(name)
 criteria={x:x for x in options};criteria['unknown']='病历资料不足，不能确定分级'
 add('cmedcalc_semantic_grade',str(r['id']),str(r['id']),{'indicator':name,'note':r['record_final']},'按指定指标的分级体系选择最符合病历的级别。仅依据病例资料，不猜测未记录事实。',criteria,gold,indicator=name,scope='all162 public semantic cases; canonicalized labels, no gold explanation; explicit grading not free generation')
# LongHealth: all source texts for each patient; no answer locations, diagnosis metadata or gold.
for pid,patient in b.load('longhealth.json').items():
 qs=[dict(q,id=str(q['No'])) for q in patient['questions']]
 for q in b.sample(qs,5,pid):
  criteria={}
  for x in 'abcde':
   if q['answer_'+x] not in criteria.values():criteria[x]=q['answer_'+x]
  correct=str(q['correct']).lower().strip()
  if correct not in criteria:
   matches=[k for k,v in criteria.items() if v==q['correct']]
   if len(matches)!=1:raise ValueError('Unknown LongHealth answer encoding')
   correct=matches[0]
  add('longhealth_full_context',pid+':'+str(q['No']),pid,{'clinical_documents':patient['texts'],'question':q['question']},'Use the supplied patient documents to answer the question. Select exactly one answer.',criteria,correct,scope='5questions/patient; 20fictional patients; full patient context; no official missing-document task emulation')
# Chinese department routing: target is populated; keyentity is incomplete and is never used as gold.
if (b.DATA/'medjourney-dr.json').exists():
 pool=[dict(json.loads(s),id=str(i)) for i,s in enumerate((b.DATA/'medjourney-dr.json').read_text().splitlines()) if s.strip()]
 split=lambda s:sorted(set(v.strip() for v in re.split('[，,、;；]',s) if v.strip()))
 vocabulary=sorted({v for r in pool for v in split(r['target'])})
 for r in b.sample(pool,100,'medjourney_departments'):
  questions={str(i):{'type':'noul','instructions':f'对于所给主诉，{v}是否属于应推荐的就诊科室？判断具体科室是否适合；可以有多个科室，也可以不选。不要仅因科室名与症状共享词就选择。'} for i,v in enumerate(vocabulary)}
  row=b.record('medjourney_departments',r['id'],r['id'],{'state':{'source_prompt':r['prompt']},'questions':questions},split(r['target']),label_vocabulary=vocabulary,scope='adapted multilabel fixed inventory from whole public target column; 0.5 threshold; no alias normalization; not official generative metric')
  row['request_sha256']=b.sha(row['request']);rows.append(row)
# TCM: official148-label vocabulary, held-out test notes only; diagnostic metadata omitted.
if (b.DATA/'tcm-test.json').exists():
 with zipfile.ZipFile(b.DATA/'tcm-train-dev.zip') as z:vocab=z.read('syndrome_vocab.txt').decode().splitlines()
 criteria={v:v for v in vocab};criteria['unknown']='资料不足，不能确定证型'
 pool=[dict(json.loads(s),id=str(i)) for i,s in enumerate((b.DATA/'tcm-test.json').read_text().splitlines()) if s.strip()]
 for r in b.sample(pool,100,'tcm_syndrome'):
  add('tcm_syndrome',r['id'],b.sha(r['user_id']),{k:r[k] for k in ('chief_complaint','description','detection')},'根据主诉、病情描述和检查资料，选择最符合病例的中医证型。仅评测原数据集分类，不提供处方。',criteria,r['norm_syndrome'],scope='100 official test rows;148 fixed official labels+unknown; research only; CC BY-NC-SA4.0')
# Manually authored challenge panel, separate from public benchmark scores.
challenge=b.OUT/'challenge_cases.json'
if challenge.exists():
 for r in json.loads(challenge.read_text()):
  add('challenge_'+r['family'],r['id'],r['id'],{'note':r['text']},r['instruction'],r['choices'],r['gold'],scope='author-written synthetic diagnostic challenge; not physician-validated or population-representative')
path=b.DATA/'extended_prepared.jsonl';path.write_text(''.join(b.dumps(r)+'\n' for r in rows))
manifest={'counts':dict(collections.Counter(r['task'] for r in rows)),'samples':len(rows),'requests':len(rows),'source_files':{},'cases':[{'task':r['task'],'id':r['id'],'group':r['group'],'request_sha256':r['request_sha256']} for r in rows]}
for name in ['ddi2013.zip','longhealth.json','cmedcalc-semantic.json','cmedcalc-equation.json','cmedcalc-score.json','cmedcalc-faithful.json','medjourney-dr.json','tcm-test.json','tcm-train-dev.zip']:
 raw=(b.DATA/name).read_bytes();manifest['source_files'][name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
(b.OUT/'extended_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(b.dumps({k:v for k,v in manifest.items() if k not in ('cases','source_files')}))
