import medspacy,json,zipfile,re,collections,time
from medspacy.target_matcher import TargetRule
from loguru import logger
import benchmark as b
logger.remove();D=b.DATA/'more'
def read(name):
 with zipfile.ZipFile(D/name) as z:raw=z.read(z.namelist()[0]).decode()
 docs=[]
 for block in raw.strip().split('\n\n'):
  lines=block.splitlines();pid=lines[0].split('|')[0];text=' '.join(s.split('|',2)[2] for s in lines if '|t|' in s or '|a|' in s);ents=[]
  for s in lines:
   v=s.split('\t')
   if len(v)==6:
    start,end=int(v[1]),int(v[2])
    if text[start:end]!=v[3]:
     print('Excluded inconsistent annotation',name,pid,start,end);continue
    ents.append((start,end,v[3]))
  docs.append(dict(id=pid,text=text,ents=ents))
 return docs
train=read('ncbi-train.zip');test=read('ncbi-test.zip');vocab=sorted({t.lower() for r in train for _,_,t in r['ents']});nlp=medspacy.load();nlp.get_pipe('medspacy_target_matcher').add([TargetRule(t,'DISEASE') for t in vocab]);rows=[];baseline=[];t=time.perf_counter()
for r in b.sample(test,100,'ncbi-e2e'):
 doc=nlp(r['text']);candidates=[(e.start_char,e.end_char,e.text) for e in doc.ents];gold=[str(s)+':'+str(e) for s,e,_ in r['ents']];pred=[str(s)+':'+str(e) for s,e,_ in candidates];qs={str(s)+':'+str(e):{'type':'noul','instructions':'Is the target mention a disease/disease class or disease modifier in this abstract? Evaluate only this occurrence, not whether the patient currently has it. Target '+repr(text)+f' at character range [{s},{e}).'} for s,e,text in candidates}
 row=b.record('ncbi_medspacy_jev_ner',r['id'],r['id'],{'state':r['text'],'questions':qs},gold,scoring='multi_question_keys',source='official NCBI test100docs; training-only lexical candidates via medspaCy; strict span detection collapsed disease category',baseline_predictions=pred,candidate_count=len(candidates));row['request_sha256']=b.sha(row['request']);rows.append(row);baseline.append((set(gold),set(pred)))
(b.DATA/'medspacy_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));out=dict(version=medspacy.__version__,training_lexicon=len(vocab),test_documents=len(rows),quality=b.sets_metric(baseline),elapsed_seconds=time.perf_counter()-t,scope='Dictionary medspaCy target matcher, no UMLS proprietary files; strict span NER; no training or prompt tuning on these test docs');(b.OUT/'medspacy_results.json').write_text(json.dumps(out,indent=2));print(out)
