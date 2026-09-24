import json,re,zipfile,collections,csv,xml.etree.ElementTree as ET
import benchmark as b
D=b.DATA/'more';rows=[]
def add(task,id_,group,state,instruction,criteria,gold,**meta):
 assert gold in criteria,(task,id_,gold)
 r=b.record(task,str(id_),str(group),b.choice(state,instruction,criteria),gold,**meta);r['request_sha256']=b.sha(r['request']);rows.append(r)
# SIGIR has potential, unlike TREC's excluded middle category. Official cohort definitions retained.
for label in ['0','1','2']:
 pool=[]
 for patient in json.loads((D/'TrialGPT/dataset/sigir/retrieved_trials.json').read_text()):
  for trial in patient[label]:pool.append(dict(id=patient['patient_id']+':'+trial['NCTID'],group=patient['patient_id'],state={'patient':patient['patient'],'trial':{k:trial[k] for k in ['brief_title','brief_summary','inclusion_criteria','exclusion_criteria']}}))
 for r in b.sample(pool,50,'trial'+label):
  add('trialgpt_sigir_referral',r['id'],r['group'],r['state'],'Based on this patient and trial, classify referral suitability. Potential means further investigation is needed; do not treat undocumented criteria as confirmed.',{'0':'Irrelevant: would not refer this patient','1':'Potential: would consider referring upon further investigation','2':'Eligible: highly likely to refer this patient'},label,source='SIGIR released judged pool,50/class; direct trial classification not original TrialGPT criterion reasoning or full retrieval')
# BC5CDR official test: given annotated entities; all same-document chemical/disease pairs.
with zipfile.ZipFile(D/'bc5cdr.zip') as z:raw=z.read('CDR_Data/CDR.Corpus.v010516/CDR_TestSet.PubTator.txt').decode()
pool=[]
for block in raw.strip().split('\n\n'):
 lines=block.splitlines();pid=lines[0].split('|')[0];text=' '.join(s.split('|',2)[2] for s in lines if '|t|' in s or '|a|' in s);ents=collections.defaultdict(set);types={};rel=set()
 for s in lines:
  v=s.split('\t')
  if len(v)==4 and v[1]=='CID':rel.add((v[2],v[3]))
  elif len(v)==6:
   for cid in v[5].split('|'):
    if cid!='-1':ents[cid].add(v[3]);types[cid]=v[4]
 for c in [k for k in ents if types[k]=='Chemical']:
  for d in [k for k in ents if types[k]=='Disease']:
   pool.append(dict(id=pid+':'+c+':'+d,pid=pid,state={'abstract':text,'chemical_mentions':sorted(ents[c]),'disease_mentions':sorted(ents[d])},gold='yes' if (c,d) in rel else 'no'))
for lab in ['yes','no']:
 for r in b.sample([x for x in pool if x['gold']==lab],50,'cdr'+lab):add('bc5cdr_relation_oracle_entities',r['id'],r['pid'],r['state'],'Does the abstract establish a chemical-induced disease relation for these target entities, rather than a treatment relation or mere co-occurrence?',{'yes':'Chemical induces the disease','no':'No annotated chemical-induced disease relation'},lab,source='official test;50/class; given entity IDs/mentions, not end-to-end extraction')
# Medical question routing: source question-type metadata, no answer text.
pool=[]
for p in (D/'MedQuAD').rglob('*.xml'):
 root=ET.parse(p).getroot()
 for qa in root.findall('.//QAPair'):
  q=qa.find('Question')
  if q is not None and q.text and q.attrib.get('qtype'):pool.append(dict(id=str(p.relative_to(D/'MedQuAD'))+':'+qa.attrib.get('pid',''),group=str(p),text=q.text,label=q.attrib['qtype']))
vocab=collections.Counter(r['label'] for r in pool);top=[x for x,n in vocab.most_common(12)];criteria={x:x.replace('_',' ') for x in top}
for r in b.sample([r for r in pool if r['label'] in top],100,'medquad'):
 add('medquad_question_type',r['id'],r['group'],r['text'],'Classify the medical information need expressed by this question.',criteria,r['label'],source='public MedQuAD question metadata; top12 types; not answer accuracy')
# ACI sections: given reference section, determine its four-way role. Not generation quality.
root=D/'aci-bench/data/challenge_data_json';pool=[]
for section in ['subjective','objective_exam','objective_results','assessment_and_plan']:
 p=root/('clinicalnlp_taskB_test1_'+section+'.json');data=json.loads(p.read_text())
 for i,r in enumerate(data['data']):
  if r.get('tgt','').strip():pool.append(dict(id=section+':'+str(i),group=r['file'].split('-')[0],text=re.sub(r'(?m)^[A-Z][A-Z /&\-]+$','',r['tgt']).strip(),gold=section))
for r in b.sample(pool,100,'aci_sections'):
 add('aci_note_section',r['id'],r['group'],r['text'],'Classify this clinical note section by its role.',{'subjective':'Patient history, symptoms and subjective narrative','objective_exam':'Physical examination','objective_results':'Objective laboratory, imaging or diagnostic results','assessment_and_plan':'Clinical assessment, diagnoses and treatment/follow-up plan'},r['gold'],source='ACI-Bench test1 reference sections; given section boundaries; not note generation or factual quality')
# Numerator/denominator are selected from literal numeric-unit candidates; gold values used only for scoring.
for r in b.load('cmedcalc-equation.json'):
 if r['指标名称']!='体重指数(BMI)':continue
 note=r['record_final']
 for param,kind in [('weight','体重'),('height','身高')]:
  pattern=r'(\d+(?:\.\d+)?)\s*(公斤|千克|kg|KG|斤|厘米|cm|CM|米|m)(?![a-zA-Z])';candidates=[]
  for m in re.finditer(pattern,note):
   unit=m[2];value=float(m[1]);belongs='weight' if unit in ['公斤','千克','kg','KG','斤'] else 'height'
   if belongs!=param:continue
   norm=value*(.5 if unit=='斤' else .01 if unit in ['厘米','cm','CM'] else 1)
   candidates.append(dict(value=norm,quote=note[max(0,m.start()-16):m.end()+12]))
  merged={}
  for c in candidates:
   if c['value'] in merged:merged[c['value']]['quote']+=' / '+c['quote']
   else:merged[c['value']]=c.copy()
  candidates=list(merged.values())
  criteria={str(i):c['quote'] for i,c in enumerate(candidates)};criteria['unknown']='病历中没有可可靠选取的当前测量值'
  expected=float(r['input_params_final'][param][0]);match=[str(i) for i,c in enumerate(candidates) if abs(c['value']-expected)<1e-5]
  gold=match[0] if match else 'unknown'
  add('bmi_'+param+'_selection',r['id'],r['id'],note,'选择用于计算当前BMI的'+kind+'记录；排除历史值和其他人物的值，不补造数据。',criteria,gold,source='all20 BMI cases; exact numeric-unit regex candidates',candidate_values=[c['value'] for c in candidates],expected_value=expected,candidate_gold_covered=bool(match),expected_bmi=r['answer_final'],alternative_gold_choices=match)
(b.DATA/'clinical_extra_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print(collections.Counter(r['task'] for r in rows),len(rows));print('ACI parsed',len(pool),'MedQuAD types',vocab.most_common(12))
