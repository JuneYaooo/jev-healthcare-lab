import benchmark as b
import json,collections
rows=[]
for n in ['prepared','extended','additional','clinical_extra','pipeline']:
 rows.extend(json.loads(s) for s in (b.DATA/(n+'_prepared.jsonl' if n!='prepared' else 'prepared.jsonl')).read_text().splitlines())
lookup={(r['task'],r['id']):r for r in rows}
def cache(r):return json.loads((b.DATA/'runs/jev-1.13.0'/(b.sha([r['task'],r['id'],r['request_sha256']])+'.json')).read_text())
def decision(r):return cache(r)['response']['answers']['decision']['choice']
result={};groups=collections.defaultdict(list);rtok=0;fail=[]
for r in map(json.loads,(b.DATA/'robustness_prepared.jsonl').read_text().splitlines()):
 a=cache(r)
 if a['status']!='ok':fail.append([r['task'],r['id']]);continue
 rtok+=a['response']['usage']['input_tokens'];p=a['response']['answers']['decision']['choice'];m=r['metadata'];orig=lookup[(m['original_task'],m['original_id'])];norm=m.get('inverse_labels',{}).get(p,p);groups[(m['original_task'],m['variant'])].append((norm!=decision(orig),p==r['gold'],decision(orig)==orig['gold']))
result['robustness']={'input_tokens':rtok,'failures':fail,'rows':sum(map(len,groups.values())),'tasks':{t+':'+v:{'n':len(x),'changed_predictions':sum(a for a,_,_ in x),'correct':sum(c for _,c,_ in x),'original_correct':sum(c for _,_,c in x)} for (t,v),x in groups.items()}}
bmi=[]
for r in [r for r in rows if r['task']=='bmi_weight_selection']:
 h=lookup[('bmi_height_selection',r['id'])];wp=decision(r);hp=decision(h);wm=r['metadata'];hm=h['metadata'];wv=wm['candidate_values'][int(wp)] if wp!='unknown' else None;hv=hm['candidate_values'][int(hp)] if hp!='unknown' else None
 correct=wv is not None and hv is not None and abs(wv-wm['expected_value'])<1e-5 and abs(hv-hm['expected_value'])<1e-5
 baseline=bool(wm['candidate_values'] and hm['candidate_values'] and abs(wm['candidate_values'][0]-wm['expected_value'])<1e-5 and abs(hm['candidate_values'][0]-hm['expected_value'])<1e-5)
 bmi.append(dict(id=r['id'],weight=wv,height=hv,bmi=wv/(hv*hv) if wv and hv else None,reference_bmi=wm['expected_bmi'],both_inputs_correct=correct,first_candidate_baseline_correct=baseline,candidates_cover_both=wm['candidate_gold_covered'] and hm['candidate_gold_covered']))
result['bmi_hybrid']={'n':len(bmi),'correct_input_pairs':sum(x['both_inputs_correct'] for x in bmi),'emitted_numeric_results':sum(x['bmi'] is not None for x in bmi),'candidate_covered_pairs':sum(x['candidates_cover_both'] for x in bmi),'first_candidate_baseline_correct_pairs':sum(x['first_candidate_baseline_correct'] for x in bmi),'note':'Actual current value selection + deterministic BMI formula; correct input pairs, not clinical endorsement. Unknowns count as failure to complete. Reference may be rounded.','cases':bmi}
p=[r for r in rows if r['task']=='cdrugred_discharge_candidate_pipeline'];result['cdrugred_baseline']={'quality':b.sets_metric([(set(r['gold']),set(r['metadata']['baseline_candidates'])) for r in p]),'candidate_recall':sum(r['metadata']['candidate_recall_hits'] for r in p)/sum(r['metadata']['gold_count'] for r in p),'n':len(p)}
(b.OUT/'ablations.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps({k:{a:v for a,v in d.items() if a not in ['cases','tasks']} for k,d in result.items()}));print(result['robustness']['tasks'])
