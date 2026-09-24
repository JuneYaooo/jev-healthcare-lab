"""Verify archived request/response hashes and recompute metrics without API access."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

import benchmark as b

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    return [json.loads(s) for s in path.read_text().splitlines()]


def prediction(row, response):
    a=response['response']['answers'];task=row['task'];meta=row['metadata']
    if meta.get('scoring')=='multi_label_vocabulary' or task=='medjourney_departments':
        return set(row['gold']),{meta['label_vocabulary'][int(k)] for k,v in a.items() if v['noul']>=.5}
    if meta.get('scoring')=='multi_question_keys' or task=='nli4ct_evidence':
        return set(row['gold']),{k for k,v in a.items() if v['noul']>=.5}
    if task=='imcs_ner_dictionary_pipeline':
        return {tuple(v) for v in row['gold']},{(s,e,a['s'+str(i)]['choice']) for i,(s,e,_) in enumerate(meta['candidates']) if a['s'+str(i)]['choice']!='none'}
    return row['gold'],a['decision']['choice']


def same_metrics(actual, expected):
    """Allow rounding noise from Python's float summation, never count drift."""
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(same_metrics(actual[k], expected[k]) for k in actual)
    if isinstance(actual, list) and isinstance(expected, list):
        return len(actual) == len(expected) and all(same_metrics(a, e) for a, e in zip(actual, expected))
    if isinstance(actual, float) and isinstance(expected, float):
        return math.isfinite(actual) and math.isfinite(expected) and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)
    return actual == expected


def verify():
    scenes=json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes']
    expected=rows(ROOT/'results/evaluation_index.jsonl');index={(r['task'],r['id']):r for r in expected}
    if len(index)!=len(expected):raise ValueError('Duplicate global sample identity')
    tasks=json.loads((ROOT/'results/all_results.json').read_text())['tasks']
    paths={t:ROOT/'scenarios'/s['id']/t for s in scenes for t in s['task_ids']}
    if len(paths)!=sum(len(s['task_ids']) for s in scenes) or set(paths)!=set(tasks):raise ValueError('Task mapping differs from original metrics')
    seen=set();main={};perturb=[];count=Counter()
    for folder in sorted((ROOT/'scenarios').rglob('samples.jsonl')):
        folder=folder.parent
        rr=rows(folder/'samples.jsonl');aa=rows(folder/'responses.jsonl');local_index=rows(folder/'index.jsonl')
        if not (len(rr)==len(aa)==len(local_index)):raise ValueError(f'Unequal archive file lengths: {folder}')
        response_bytes=(folder/'responses.jsonl').read_bytes().splitlines()
        res=json.loads((folder/'results.json').read_text())
        provenance=json.loads((folder/'provenance.json').read_text())
        for name,entry in provenance['files'].items():
            raw=(folder/name).read_bytes()
            if len(raw)!=entry['bytes'] or hashlib.sha256(raw).hexdigest()!=entry['sha256']:raise ValueError(f'File hash mismatch: {folder/name}')
        pairs=[];tokens=0;outtokens=0;empty=0;prompt_counts=Counter()
        for row,response,ix,raw in zip(rr,aa,local_index,response_bytes):
            key=(row['task'],row['id'])
            if key in seen or key not in index:raise ValueError(f'Unexpected/duplicate identity: {key}')
            if ix!=index[key]:raise ValueError(f'Index differs: {key}')
            if b.sha(row['request'])!=ix['request_sha256'] or row['request_sha256']!=ix['request_sha256']:raise ValueError(f'Request hash differs: {key}')
            if hashlib.sha256(raw).hexdigest()!=ix['response_sha256']:raise ValueError(f'Response hash differs: {key}')
            if (response['task'],response['id'])!=key or response['request_sha256']!=row['request_sha256']:raise ValueError(f'Wrong paired response: {key}')
            if response['status']!='ok':raise ValueError(f'Invalid final response status: {key}')
            det=bool(response.get('deterministic_empty'))
            if det!=ix['deterministic_empty'] or det!= (not row['request']['questions']):raise ValueError(f'Empty prediction flag differs: {key}')
            if not det and response['response']['model']!='jev-1.13.0':raise ValueError(f'Unexpected model: {key}')
            b.validate_response(row['request'],response['response'])
            for q in row['request']['questions'].values():prompt_counts[b.sha(q)]+=1
            empty+=det;tokens+=response['response']['usage']['input_tokens'];outtokens+=response['response']['usage']['output_tokens']
            pair=prediction(row,response);pairs.append(pair)
            if row['task'].startswith('robust_'):perturb.append((row,response))
            else:main[key]=(row,response)
            count['all_rows']+=1;count['empty']+=det;seen.add(key)
        prompts=json.loads((folder/'prompts.json').read_text())['variants']
        archived=Counter({b.sha(p['question']):p['occurrences'] for p in prompts})
        if archived!=prompt_counts or len(prompts)!=len(archived):raise ValueError(f'Prompt coverage differs: {folder}')
        if rr[0]['task'].startswith('robust_'):
            if len(rr)!=res['n']:raise ValueError('Robustness count mismatch')
        else:
            task=rr[0]['task']
            actual=b.sets_metric(pairs) if isinstance(pairs[0][0],set) else b.classification([g for g,p in pairs],[p for g,p in pairs])
            if not same_metrics(actual,res['quality']) or res!=tasks[task]:raise ValueError(f'Recomputed quality differs: {task}')
            if (len(rr),empty,tokens,outtokens)!=(res['successful'],res['deterministic_empty'],res['input_tokens'],res['output_tokens']):raise ValueError(f'Counts or token usage differ: {task}')
    if seen!=set(index):raise ValueError(f'Missing rows: {set(index)-seen}')
    groups={}
    for row,response in perturb:
        m=row['metadata'];original,resp=main[(m['original_task'],m['original_id'])]
        op=resp['response']['answers']['decision']['choice'];p=response['response']['answers']['decision']['choice']
        normalized=m.get('inverse_labels',{}).get(p,p)
        key=m['original_task']+':'+m['variant']
        if key not in groups:groups[key]={'n':0,'changed_predictions':0,'correct':0,'original_correct':0}
        v=groups[key];v['n']+=1;v['changed_predictions']+=normalized!=op;v['correct']+=p==row['gold'];v['original_correct']+=op==original['gold']
    ab=json.loads((ROOT/'results/ablations.json').read_text())
    if groups!=ab['robustness']['tasks']:raise ValueError('Robustness recomputation differs')
    for task,path in paths.items():
        for var in ('repeat','rotate','irrelevant'):
            p=path/'robustness'/var/'results.json'
            if p.exists() and json.loads(p.read_text())!=groups[task+':'+var]:raise ValueError('Local robustness result differs')
    for path in (ROOT/'scenarios').rglob('upstream/manifest.json'):
        for entry in json.loads(path.read_text()):
            raw=(path.parent.parent/entry['file']).read_bytes()
            if len(raw)!=entry['bytes'] or hashlib.sha256(raw).hexdigest()!=entry['sha256']:raise ValueError(f'Upstream bytes changed: {entry["file"]}')
    snapshot=json.loads((ROOT/'results/snapshot.json').read_text())
    if (count['all_rows'],count['empty'],count['all_rows']-count['empty'])!=(snapshot['evaluation_rows'],snapshot['deterministic_empty_rows'],snapshot['successful_api_responses']):raise ValueError('Snapshot totals differ')
    return {'clinical_scenarios':len(scenes),'main_tasks':len(tasks),'main_rows':len(main),'robustness_groups':len(groups),'robustness_rows':len(perturb),'verified_pairs':count['all_rows'],'deterministic_empty':count['empty'],'recomputed_main_metrics':'all matched','recomputed_robustness':'all matched'}


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
