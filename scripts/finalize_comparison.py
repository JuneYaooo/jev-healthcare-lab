"""Normalize unambiguous numeric labels, then archive real provider outputs per task."""
import argparse
import json
from pathlib import Path
from collections import defaultdict
import hashlib

from compare_deepseek import ROOT,load_rows,normalize,dumps,request_payload,sha


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--normalize-only',action='store_true');args=ap.parse_args()
    source={(r['task'],r['id']):r for r in load_rows()}
    base=ROOT/'comparisons/deepseek-flash'
    normalized=0
    for p in (base/'runs').glob('*.json'):
        d=json.loads(p.read_text())
        if 'response' not in d or d.get('deterministic_empty'):continue
        row=source[(d['task'],d['id'])]
        if d['response']['choices'][0]['finish_reason']!='stop':continue
        try:answers=normalize(row,d['response'])
        except (ValueError,KeyError,TypeError):continue
        if d['status']!='ok':
            d['original_parse_status']=d['status'];d['normalization_note']='Numeric JSON choice converted to identical string key; no gold used and raw response unchanged.'
            d['status']='ok';d['normalized_answers']=answers;p.write_text(dumps(d)+'\n');normalized+=1
    print('Normalized valid numeric-label responses:',normalized)
    if args.normalize_only:return
    from analyze_comparison import summarize
    result=summarize()
    if not result['summary']['complete']:raise ValueError('Comparison is not complete')
    owners={t:s['id'] for s in json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes'] for t in s['task_ids']}
    groups=defaultdict(list);attempts=defaultdict(list)
    for p in sorted((base/'runs').glob('*.json')):
        r=json.loads(p.read_text());groups[r['task']].append(r)
    for p in sorted((base/'attempt_history').glob('*.json')):
        r=json.loads(p.read_text());attempts[r['task']].append(r)
    manifest=[]
    for task,rows in groups.items():
        folder=ROOT/'scenarios'/owners[task]/task/'comparison';folder.mkdir(exist_ok=True)
        rows.sort(key=lambda x:x['id'])
        targets={'deepseek_responses.jsonl':''.join(dumps(r)+'\n' for r in rows),'results.json':json.dumps(result['tasks'][task],ensure_ascii=False,indent=2)+'\n'}
        if attempts[task]:targets['deepseek_attempts.jsonl']=''.join(dumps(r)+'\n' for r in attempts[task])
        for name,text in targets.items():
            p=folder/name;p.write_text(text);manifest.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (base/'archive_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print('Archived comparison records under all task directories.')


if __name__=='__main__':main()
