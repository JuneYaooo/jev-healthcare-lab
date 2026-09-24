"""Auditable scoring of cached real responses; group bootstrap, calibration and failures."""
import json,collections,random,math,statistics
import benchmark as b

def pct(xs,q):
 xs=sorted(xs)
 if not xs:return None
 return xs[round((len(xs)-1)*q)]
def ci_group(items,kind):
 groups=collections.defaultdict(list)
 for group,stats in items:groups[group].append(stats)
 keys=sorted(groups);rng=random.Random(20260924);vals=[]
 if not keys:return None
 for _ in range(1000):
  totals=[0,0,0]
  for _ in keys:
   for s in groups[rng.choice(keys)]:
    for i,v in enumerate(s):totals[i]+=v
  if kind=='accuracy':v=totals[0]/totals[1] if totals[1] else 0
  else:v=2*totals[0]/(2*totals[0]+totals[1]+totals[2]) if sum(totals) else 0
  vals.append(v)
 return {'method':'1000 group bootstrap, percentile; exploratory pilot','groups':len(keys),'lower':pct(vals,.025),'upper':pct(vals,.975)}
def main():
 rows=b.read_prepared()
 for filename in ('extended_prepared.jsonl','additional_prepared.jsonl','evidence_prepared.jsonl','pipeline_prepared.jsonl','clinical_extra_prepared.jsonl','hallucination_prepared.jsonl','medspacy_prepared.jsonl','final_tasks_prepared.jsonl','last_datasets_prepared.jsonl','bioscope_prepared.jsonl','pubhealth_prepared.jsonl','medcalc_verified_prepared.jsonl','ddxplus_prepared.jsonl'):
  path=b.DATA/filename
  if path.exists():rows.extend(json.loads(s) for s in path.read_text().splitlines())
 report={};errors=[];totaltokens=0;totaloutput=0;alltimes=[];apiresponses=0;empty=0
 for task in sorted({r['task'] for r in rows}):
  rr=[r for r in rows if r['task']==task];gold=[];pred=[];sets=[];groupstats=[];confs=[];briers=[];times=[];tok=0;outtok=0;successful=0;deterministic=0;indicators=collections.defaultdict(list);failed=[]
  for r in rr:
   f=b.DATA/'runs/jev-1.13.0'/(b.sha([task,r['id'],r['request_sha256']])+'.json')
   if not f.exists():failed.append({'id':r['id'],'status':'missing'});continue
   result=json.loads(f.read_text())
   if result['status']!='ok':failed.append({'id':r['id'],'status':result['status'],'error':result.get('error')});continue
   successful+=1;resp=result['response'];a=resp['answers'];tok+=resp['usage']['input_tokens'];outtok+=resp['usage']['output_tokens']
   if result.get('deterministic_empty'):deterministic+=1;empty+=1
   else:times.append(result['elapsed_s']);alltimes.append(result['elapsed_s']);apiresponses+=1
   if r['metadata'].get('scoring')=='multi_label_vocabulary':g=set(r['gold']);p={r['metadata']['label_vocabulary'][int(k)] for k,v in a.items() if v['noul']>=.5}
   elif r['metadata'].get('scoring')=='multi_question_keys':g=set(r['gold']);p={k for k,v in a.items() if v['noul']>=.5}
   elif task=='imcs_ner_dictionary_pipeline':
    g={tuple(x) for x in r['gold']};p={(s,e,a['s'+str(i)]['choice']) for i,(s,e,_) in enumerate(r['metadata']['candidates']) if a['s'+str(i)]['choice']!='none'}
   elif task=='nli4ct_evidence':g=set(r['gold']);p={k for k,v in a.items() if v['noul']>=.5}
   elif task=='medjourney_departments':g=set(r['gold']);p={r['metadata']['label_vocabulary'][int(k)] for k,v in a.items() if v['noul']>=.5}
   else:
    aa=a['decision'];g=r['gold'];p=aa['choice'];gold.append(g);pred.append(p);ok=int(g==p);groupstats.append((r['group'],(ok,1)))
    prob=aa['probabilities'][p];confidence=aa.get('confidence');confs.append((prob,confidence,ok))
    if g in aa['probabilities']:briers.append(sum((v-int(k==g))**2 for k,v in aa['probabilities'].items()))
    if 'indicator' in r['metadata']:indicators[r['metadata']['indicator']].append(ok)
    if not ok:errors.append({'task':task,'id':r['id'],'gold':g,'prediction':p,'selected_probability':prob,'confidence':confidence,'synthetic_challenge':task.startswith('challenge_')})
    continue
   sets.append((g,p));groupstats.append((r['group'],(len(g&p),len(p-g),len(g-p))))
  if sets:quality=b.sets_metric(sets);interval=ci_group(groupstats,'f1')
  else:quality=b.classification(gold,pred) if gold else None;interval=ci_group(groupstats,'accuracy')
  calibration=None
  if confs:
   bins=[];ece=0
   for i in range(10):
    bucket=[x for x in confs if min(9,int(x[0]*10))==i]
    if not bucket:continue
    avg=sum(x[0] for x in bucket)/len(bucket);acc=sum(x[2] for x in bucket)/len(bucket);ece+=len(bucket)/len(confs)*abs(avg-acc);bins.append({'lower':i/10,'n':len(bucket),'mean_selected_probability':avg,'accuracy':acc})
   gating={}
   for cutoff in (.8,.9,.95):
    subset=[x for x in confs if x[0]>=cutoff];both=[x for x in confs if x[0]>=cutoff and x[1] is not None and x[1]>=cutoff]
    gating[str(cutoff)]={'by_selected_probability':{'n':len(subset),'coverage':len(subset)/len(confs),'accuracy':sum(x[2] for x in subset)/len(subset) if subset else None},'by_probability_and_api_confidence':{'n':len(both),'coverage':len(both)/len(confs),'accuracy':sum(x[2] for x in both)/len(both) if both else None}}
   calibration={'ece10_selected_probability':ece,'multiclass_brier_sum':sum(briers)/len(briers) if briers else None,'brier_n':len(briers),'bins':bins,'exploratory_gating_not_validated_policy':gating}
  totaltokens+=tok;totaloutput+=outtok
  report[task]={'planned':len(rr),'successful':successful,'failed_or_missing':failed,'deterministic_empty':deterministic,'quality':quality,'group_bootstrap_95ci':interval,'calibration':calibration,'input_tokens':tok,'output_tokens':outtok,'latency_successful_api_p50_s':statistics.median(times) if times else None,'latency_successful_api_p95_s':pct(times,.95),'per_indicator':{k:{'n':len(v),'accuracy':sum(v)/len(v)} for k,v in indicators.items()}}
 failedhistory=list((b.DATA/'runs/jev-1.13.0/attempt_history').glob('*.json'))
 summary={'planned_rows':len(rows),'successful_api_responses':apiresponses,'deterministic_empty_rows':empty,'input_tokens_successful_only':totaltokens,'output_tokens_successful_only':totaloutput,'failed_attempt_records_preserved':len(failedhistory),'successful_api_latency_p50_s':statistics.median(alltimes),'successful_api_latency_p95_s':pct(alltimes,.95),'model':'jev-1.13.0','cost_note':'Successful-response token usage only; smoke test and unknown usage for failed attempts excluded. No invoice claim.'}
 (b.OUT/'all_results.json').write_text(json.dumps({'summary':summary,'tasks':report},ensure_ascii=False,indent=2));(b.OUT/'error_cases.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2))
 print(b.dumps(summary))
 for t,r in report.items():
  q=r['quality'] or {};print(t,r['successful'],round(q.get('accuracy',q.get('micro_f1',0)),4))
if __name__=='__main__':main()
