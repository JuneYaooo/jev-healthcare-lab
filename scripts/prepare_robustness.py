import json,copy,collections
import benchmark as b
allrows=[]
for n in ['prepared.jsonl','extended_prepared.jsonl','additional_prepared.jsonl']:
 allrows.extend(json.loads(s) for s in (b.DATA/n).read_text().splitlines())
rows=[]
for task in ['imcs_assertion_oracle_span','medec_error_detection','ddi_relation_oracle_pairs','cmedcalc_semantic_grade','cmexam_mcq']:
 pool=[r for r in allrows if r['task']==task and 'decision' in r['request']['questions']]
 for orig in b.sample(pool,20,'robust'+task):
  for variant in ['repeat','rotate','irrelevant']:
   r=copy.deepcopy(orig);r['task']='robust_'+variant+'_'+task;r['metadata'].update(original_task=task,original_id=orig['id'],variant=variant,source='paired perturbation of existing held-out pilot; not new independent cases')
   if variant=='rotate':
    q=r['request']['questions']['decision'];keys=list(q['criteria']);rot=keys[1:]+keys[:1];mapping=dict(zip(keys,rot));q['criteria']={mapping[k]:v for k,v in q['criteria'].items()};r['gold']=mapping[r['gold']];r['metadata']['inverse_labels']={v:k for k,v in mapping.items()}
   if variant=='irrelevant':r['request']['state']={'clinical_input':r['request']['state'],'administrative_note':'Document imported on Tuesday. Printer paper restocked. Meeting room chairs replaced. This administrative note is unrelated to the patient or task.'}
   r['request_sha256']=b.sha(r['request']);rows.append(r)
(b.DATA/'robustness_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print(len(rows))
