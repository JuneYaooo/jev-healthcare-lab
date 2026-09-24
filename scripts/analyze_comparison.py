"""Score identical task inputs for Jev and DeepSeek; retain coverage and costs."""
from collections import Counter,defaultdict
import json
from pathlib import Path
import statistics

import benchmark as b
from verify_experiments import prediction

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'comparisons/deepseek-flash'


def summarize(write=True, archived=False):
    methods=json.loads((ROOT/'results/task_methods.json').read_text())
    scenes=json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes']
    owners={t:s['id'] for s in scenes for t in s['task_ids']}
    cached={}
    if not archived and (OUT/'runs').exists():
        records=[json.loads(p.read_text()) for p in (OUT/'runs').glob('*.json')]
    else:
        records=[json.loads(line) for p in (ROOT/'scenarios').glob('*/*/comparison/deepseek_responses.jsonl') for line in p.read_text().splitlines()]
    for r in records:
        key=(r['task'],r['id'])
        if key in cached:raise ValueError('Duplicate comparison row')
        cached[key]=r
    tasks={};counts=Counter();allj=[];alld=[];costj=costd=0;outtokens=0;prompt=0;cachedtokens=0;returned=Counter();tariffs=Counter();failures=[]
    for folder in sorted((ROOT/'scenarios').glob('*/*/samples.jsonl')):
        rows=[json.loads(x) for x in folder.read_text().splitlines()];task=rows[0]['task']
        original={(x['task'],x['id']):x for x in map(json.loads,(folder.parent/'responses.jsonl').read_text().splitlines())}
        jp=[];dp=[];jt=[];dt=[];jc=dc=0;errors=[];done=0
        for row in rows:
            key=(task,row['id']);d=cached.get(key)
            if d is None:continue
            done+=1
            if d['request_sha256']!=row['request_sha256']:raise ValueError('Input hash mismatch')
            j=original[key];jp.append(prediction(row,j));dc+=d.get('cost_usd',0);jc+=j['response']['usage']['input_tokens']*.042/1e6
            if not j.get('deterministic_empty'):jt.append(j['elapsed_s'])
            if 'response' in d:
                usage=d['response']['usage'];prompt+=usage['prompt_tokens'];cachedtokens+=usage.get('prompt_cache_hit_tokens',0);outtokens+=usage['completion_tokens']
            if d['status']=='ok':
                dp.append(prediction(row,{'response':{'answers':d['normalized_answers']}}))
                if not d.get('deterministic_empty'):
                    dt.append(d['elapsed_s']);returned[d['response']['model']]+=1;tariffs[d['tariff']]+=1
                counts['ok']+=1
            else:
                errors.append({'id':row['id'],'status':d['status'],'error_type':d.get('error_type'),'http_status':d.get('http_status')})
                # Failed choices are incorrect; failed set predictions emit no labels and are disclosed.
                gold=jp[-1][0];dp.append((gold,set() if isinstance(gold,set) else '__API_OR_FORMAT_FAILURE__'))
                counts['failed']+=1
        def quality(pairs):
            if not pairs:return None
            return b.sets_metric(pairs) if isinstance(pairs[0][0],set) else b.classification([g for g,p in pairs],[p for g,p in pairs])
        def med(vals):return statistics.median(vals) if vals else None
        tasks[task]={'title':methods[task]['title'],'scene':owners[task],'synthetic':task.startswith('challenge_'),'planned':len(rows),'compared':done,'failures':errors,'jev':{'quality':quality(jp),'latency_median_s':med(jt),'cost_usd':jc,'cost_per_1000_usd':jc/done*1000 if done else None},'deepseek':{'quality':quality(dp),'latency_median_s':med(dt),'cost_usd':dc,'cost_per_1000_usd':dc/done*1000 if done else None}}
        allj+=jt;alld+=dt;costj+=jc;costd+=dc;failures += [{'task':task,**e} for e in errors]
    attempts=[json.loads(p.read_text()) for p in (OUT/'attempt_history').glob('*.json')] if not archived and (OUT/'runs').exists() else [json.loads(line) for p in (ROOT/'scenarios').glob('*/*/comparison/deepseek_attempts.jsonl') for line in p.read_text().splitlines()]
    for r in attempts:
        t=tasks[r['task']];t['deepseek']['cost_usd']+=r.get('cost_usd',0)
        t['deepseek']['cost_per_1000_usd']=t['deepseek']['cost_usd']/t['compared']*1000 if t['compared'] else None
        if 'response' in r:
            usage=r['response']['usage'];prompt+=usage['prompt_tokens'];cachedtokens+=usage.get('prompt_cache_hit_tokens',0);outtokens+=usage['completion_tokens']
    for task,t in tasks.items():
        t['deepseek']['prior_attempts']=sum(r['task']==task for r in attempts)
    retry_cost=sum(r.get('cost_usd',0) for r in attempts)
    summary={'planned_rows':sum(t['planned'] for t in tasks.values()),'compared_rows':sum(t['compared'] for t in tasks.values()),'successful_rows':counts['ok'],'failed_rows':counts['failed'],'complete':all(t['planned']==t['compared'] for t in tasks.values()),'jev_model':'jev-1.13.0','deepseek_model_requested':'deepseek-flash','deepseek_model_display':'DeepSeek V4.1 Flash','deepseek_returned_model_counts':dict(returned),'deepseek_thinking':'disabled','latency_comparability':'Same questions, historical Jev and new DeepSeek runs; not simultaneous. Full-response network elapsed time, excluding zero-call empty candidates.','jev':{'latency_median_s':statistics.median(allj) if allj else None,'cost_usd':costj,'cost_per_1000_usd':costj/sum(t['compared'] for t in tasks.values())*1000 if cached else None},'deepseek':{'latency_median_s':statistics.median(alld) if alld else None,'cost_usd':costd+retry_cost,'cost_per_1000_usd':(costd+retry_cost)/sum(t['compared'] for t in tasks.values())*1000 if cached else None,'prompt_tokens':prompt,'cache_hit_tokens':cachedtokens,'completion_tokens':outtokens,'tariff_counts':dict(tariffs),'prior_attempts':len(attempts),'prior_attempt_cost_usd':retry_cost,'normalized_numeric_labels':sum('normalization_note' in r for r in cached.values())},'cost_scope':'USD estimate from provider token usage and published tariff; includes retained charged retry responses, excludes unreported usage and upstream OCR/ASR. Not a verified invoice.'}
    result={'summary':summary,'tasks':tasks,'failures':failures}
    if write:
        (OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(summary,ensure_ascii=False,indent=2))
    return result


if __name__=='__main__':summarize()
