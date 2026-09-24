import benchmark as b
import json,collections
pool=[dict(r,id=str(i)) for i,r in enumerate(json.loads((b.DATA/'more/medhallu.json').read_text()))];rows=[]
for r in b.sample(pool,100,'medhallu'):
 for label,key in [('supported','Ground Truth'),('hallucinated','Hallucinated Answer')]:
  for condition in ['with_evidence','without_evidence']:
   state={'question':r['Question'],'answer_to_check':r[key]}
   if condition=='with_evidence':state['evidence']=r['Knowledge']
   req=b.choice(state,'Determine whether the answer contains medical or scientific hallucinations. Judge factual consistency'+(' with the supplied evidence.' if condition=='with_evidence' else ' using your medical/scientific knowledge.'),{'supported':'Factually grounded answer','hallucinated':'Contains hallucinated or unsupported factual claims'})
   x=b.record('medhallu_'+condition,r['id']+':'+label,r['id'],req,label,source='100 fixed pqa_labeled questions, paired gold/generated answers,1000row release; published train split, no local training; paired evidence ablation',indicator=r['Difficulty Level'],hallucination_category=r['Category of Hallucination']);x['request_sha256']=b.sha(req);rows.append(x)
(b.DATA/'hallucination_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print(len(rows))
