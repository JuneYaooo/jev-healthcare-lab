"""Small, auditable Jev medical pilot. Python standard library only.

prepare: build requests without gold labels; live: call real API; score: evaluate.
No mock prediction is ever substituted for a missing API response.
"""
import argparse
import collections
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import time
import urllib.error
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(os.environ.get('JEV_DATA_DIR', ROOT / 'data'))
OUT = ROOT / 'results'
SEED = 20260924
ENTITY = {'Symptom': '症状或临床表现', 'Drug': '具体药品名称',
          'Drug_Category': '药物类别而非具体药品', 'Medical_Examination': '医学检查检验', 'Operation': '医疗操作'}
ACT = {'Request-Symptom': '询问症状', 'Inform-Symptom': '告知症状',
       'Request-Etiology': '询问病因', 'Inform-Etiology': '解释病因',
       'Request-Basic_Information': '询问年龄等基本信息', 'Inform-Basic_Information': '提供基本信息',
       'Request-Existing_Examination_and_Treatment': '询问已进行的检查治疗',
       'Inform-Existing_Examination_and_Treatment': '提供已进行的检查治疗',
       'Request-Drug_Recommendation': '请求用药建议', 'Inform-Drug_Recommendation': '提供用药建议',
       'Request-Medical_Advice': '请求就医或处理建议', 'Inform-Medical_Advice': '提供就医或处理建议',
       'Request-Precautions': '询问注意事项', 'Inform-Precautions': '告知注意事项',
       'Diagnose': '给出诊断', 'Other': '其他对话行为'}
STATUS = {'0': '明确否定该症状', '1': '明确肯定该症状', '2': '根据完整对话仍无法确定'}
SECTIONS = {'GENHX': 'History of present illness or general history', 'CC': 'Chief complaint',
            'PASTMEDICALHX': 'Past medical history', 'PASTSURGICAL': 'Past surgical history',
            'FAM/SOCHX': 'Family or social history', 'MEDICATIONS': 'Medications',
            'ALLERGY': 'Allergies', 'ROS': 'Review of systems', 'EXAM': 'Physical examination',
            'ASSESSMENT': 'Clinical assessment', 'DIAGNOSIS': 'Diagnosis', 'PLAN': 'Plan',
            'DISPOSITION': 'Disposition', 'LABS': 'Laboratory results', 'IMAGING': 'Imaging',
            'PROCEDURES': 'Procedures', 'IMMUNIZATIONS': 'Immunizations', 'GYNHX': 'Gynecologic history',
            'EDCOURSE': 'Emergency department course', 'OTHER_HISTORY': 'Other history'}


def dumps(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True)


def sha(x):
    return hashlib.sha256(dumps(x).encode()).hexdigest()


def load(name):
    return json.loads((DATA / name).read_text())


def spans(utterance):
    text = utterance['sentence']
    labels = utterance['BIO_label'].split()
    if len(text) != len(labels):
        raise ValueError('BIO/text length mismatch')
    result, start, kind = [], None, None
    for i, tag in enumerate(labels + ['O']):
        if start is not None and tag != 'I-' + kind:
            result.append((start, i, kind, text[start:i]))
            start, kind = None, None
        if tag.startswith('B-'):
            start, kind = i, tag[2:]
        elif tag.startswith('I-') and start is None:
            raise ValueError('Invalid BIO continuation')
    return result


def sample(rows, n, name):
    # Stable hash sampling; no label-based selection and no prompt tuning on scores.
    return sorted(rows, key=lambda x: sha([SEED, name, x['id']]))[:n]


def choice(state, instruction, criteria):
    return {'state': state, 'questions': {'decision': {
        'type': 'choice', 'instructions': instruction, 'criteria': criteria}}}


def record(task, id_, group, payload, gold, **meta):
    return {'task': task, 'id': str(id_), 'group': str(group), 'request': payload,
            'gold': gold, 'metadata': meta}


def imcs_tasks(n):
    dev, train = load('imcs-dev.json'), load('imcs-train.json')
    vocab = (DATA / 'imcs-symptom_norm.csv').read_text().splitlines()[1:]
    alias = collections.defaultdict(collections.Counter)
    dictionary = collections.defaultdict(collections.Counter)
    bad_train = bad_dev = 0
    for case in train.values():
        for u in case['dialogue']:
            try:
                ss = spans(u)
            except ValueError:
                bad_train += 1
                continue
            for a, b, typ, surface in ss:
                dictionary[surface][typ] += 1
            symptoms = [x for x in ss if x[2] == 'Symptom']
            if len(symptoms) == len(u['symptom_norm']):
                for sp, norm in zip(symptoms, u['symptom_norm']):
                    alias[sp[3]][norm] += 1
    tables = collections.defaultdict(list)
    for cid, case in dev.items():
        turns = [{k: u[k] for k in ('sentence_id', 'speaker', 'sentence')} for u in case['dialogue']]
        for i, u in enumerate(case['dialogue']):
            uid = cid + ':' + u['sentence_id']
            state = {'context': turns[max(0, i-2):i], 'target': turns[i]}
            tables['imcs_dialogue_act'].append(record('imcs_dialogue_act', uid, cid,
                choice(state, '只判断 target 这一轮的主要对话行为。context 仅帮助理解。', ACT), u['dialogue_act']))
            try:
                ss = spans(u)
            except ValueError:
                bad_dev += 1
                continue
            for j, sp in enumerate(ss):
                a, b, typ, surface = sp
                st = {'sentence': u['sentence'], 'target_span': surface, 'start': a, 'end_exclusive': b}
                tables['imcs_entity_type_oracle_span'].append(record('imcs_entity_type_oracle_span', uid+':'+str(j), cid,
                    choice(st, '已给定实体边界，只判断 target_span 的类型。', ENTITY), typ,
                    oracle='given_gold_span; not end-to-end extraction'))
            symptoms = [x for x in ss if x[2] == 'Symptom']
            if len(symptoms) == len(u['symptom_norm']) == len(u['symptom_type']):
                for j, (sp, norm, status) in enumerate(zip(symptoms, u['symptom_norm'], u['symptom_type'])):
                    st = {'self_report': case.get('self_report', ''), 'dialogue': turns,
                          'target_turn': u['sentence_id'], 'target_mention': sp[3]}
                    tables['imcs_assertion_oracle_span'].append(record('imcs_assertion_oracle_span', uid+':'+str(j), cid,
                        choice(st, '根据完整对话，判断 target_turn 的 target_mention 对该患者的症状状态。'
                               '医生询问本身不表示阳性，需看回答。', STATUS), str(status),
                        oracle='given_gold_span; full-dialogue retrospective status, not online triage'))
                    surface = sp[3]
                    def sim(v):
                        aa, bb = set(surface), set(v)
                        return len(aa & bb) / max(1, len(aa | bb))
                    candidates = sorted(set(vocab), key=lambda v: (-alias[surface][v], -sim(v), v))[:20]
                    criteria = {v: '归一化症状：'+v for v in candidates}
                    criteria['__none__'] = '候选列表没有正确标准名称'
                    st = {'sentence': u['sentence'], 'target_mention': surface}
                    tables['imcs_normalization_top20'].append(record('imcs_normalization_top20', uid+':'+str(j), cid,
                        choice(st, '将 target_mention 映射为标准症状。不要增加新诊断。候选不正确时选择 __none__。', criteria), norm,
                        oracle='given_gold_span; candidates from train aliases + fixed vocabulary only',
                        candidate_hit=norm in candidates, baseline=candidates[0]))
            # True end-to-end span evaluation: candidates from training dictionary, not dev gold.
            candidates = []
            text = u['sentence']
            for term in dictionary:
                start = text.find(term)
                while start >= 0:
                    candidates.append((start, start+len(term), term))
                    start = text.find(term, start+1)
            candidates.sort(key=lambda x: (x[0], -(x[1]-x[0]), x[2]))
            q = {}
            for j, (a,b,term) in enumerate(candidates):
                q['s'+str(j)] = {'type':'choice', 'instructions':
                    f'判断 sentence 中 [{a},{b}) 的候选片段“{term}”是否是完整医疗实体。边界不完整或不是实体选 none。',
                    'criteria': dict(ENTITY, none='不是完整医疗实体')}
            # Empty candidates are a valid deterministic empty prediction, not a dropped row.
            tables['imcs_ner_dictionary_pipeline'].append(record('imcs_ner_dictionary_pipeline', uid, cid,
                {'state': {'sentence':text}, 'questions':q}, [[a,b,t] for a,b,t,_ in ss],
                candidates=candidates, baseline=[[a,b,dictionary[term].most_common(1)[0][0]] for a,b,term in candidates]))
    selected = []
    for task, rows in tables.items():
        selected.extend(sample(rows, n, task))
    return selected, {'train_dialogues':len(train), 'dev_dialogues':len(dev),
                     'bad_train_bio_utterances_skipped_for_lexicon':bad_train,
                     'bad_dev_bio_utterances_skipped_for_extraction':bad_dev,
                     'fixed_vocabulary_size':len(vocab), 'dictionary_size':len(dictionary)}


def nli_tasks(n):
    out = []
    with zipfile.ZipFile(DATA/'nli4ct.zip') as z:
        rows = json.loads(z.read('Complete_dataset/dev.json'))
        mapping = {'Eligibility criteria':'Eligibility', 'Adverse events':'Adverse Events', 'Results':'Results', 'Intervention':'Intervention'}
        for uid, r in rows.items():
            st = {'statement':r['Statement'], 'section':r['Section_id']}
            gold_evidence = []
            for side in ['Primary','Secondary']:
                if side+'_id' not in r:
                    continue
                trial = json.loads(z.read('Complete_dataset/CT json/'+r[side+'_id']+'.json'))
                st[side.lower()] = {str(i):text for i,text in enumerate(trial[mapping.get(r['Section_id'], r['Section_id'])])}
                gold_evidence.extend(side.lower()+':'+str(i) for i in r.get(side+'_evidence_index', []))
            out.append(record('nli4ct_entailment', uid, r['Primary_id'], choice(st,
                'Using only the supplied trial section(s), is the statement entailed or contradicted? '
                'Primary and secondary refer to the named trial objects.',
                {'Entailment':'The supplied records support the statement.', 'Contradiction':'The statement conflicts with the supplied records.'}), r['Label'],
                scope='official binary task; not a calibrated clinical safety gate'))
            questions = {}
            for side in ['primary','secondary']:
                for i in st.get(side, {}):
                    questions[side+':'+i] = {'type':'noul', 'instructions':
                        f'Is line {i} of {side} evidence needed to determine whether statement is supported or contradicted? '
                        'Select relevant evidence for either verdict, not just supporting evidence.'}
            out.append(record('nli4ct_evidence', uid, r['Primary_id'], {'state':st,'questions':questions}, gold_evidence))
    return [x for task in ['nli4ct_entailment','nli4ct_evidence'] for x in sample([r for r in out if r['task']==task], n, task)]


def extra_tasks(n):
    out = []
    f = DATA/'MTS_Dataset_ValidationSet.csv'
    if f.exists():
        rows = list(csv.DictReader(f.open()))
        for r in rows:
            if r['section_header'] not in SECTIONS:
                raise ValueError('Unmapped MTS section: '+r['section_header'])
            out.append(record('mts_section_classification', r['ID'], r['ID'], choice({'dialogue':r['dialogue']},
                'Which clinical note section best matches the content of this dialogue?', SECTIONS), r['section_header'],
                scope='synthetic encounters; reference note text excluded from input'))
    f = DATA/'MEDEC-MS-ValidationSet-with-GroundTruth-and-ErrorType.csv'
    if f.exists():
        for r in csv.DictReader(f.open()):
            st = {'clinical_text':r['Text'], 'numbered_sentences':r['Sentences']}
            out.append(record('medec_error_detection', r['Text ID'], r['Text ID'], choice(st,
                'Does this clinical text contain a medical error? Judge clinical correctness, not style.',
                {'0':'No medical error', '1':'Contains a medical error'}), r['Error Flag']))
            ids = re.findall(r'(?m)^(\d+)\s', r['Sentences'])
            if not ids:
                raise ValueError('Cannot parse MEDEC sentence ids')
            criteria = {i:'Error is in sentence '+i for i in ids}
            criteria['none'] = 'No medical error'
            gold = r['Error Sentence ID'] if r['Error Flag']=='1' else 'none'
            out.append(record('medec_error_localization', r['Text ID'], r['Text ID'], choice(st,
                'Select the ID of the medically erroneous sentence. If no medical error, select none.',criteria),gold))
    f = DATA/'pubmedqa.json'
    if f.exists():
        for uid,r in json.loads(f.read_text()).items():
            out.append(record('pubmedqa_evidence_qa', uid, uid, choice({'question':r['QUESTION'],'context':r['CONTEXTS']},
                'Answer the research question based on the supplied abstract context.',
                {'yes':'Evidence supports yes','no':'Evidence supports no','maybe':'Inconclusive or uncertain'}), r['final_decision'],
                scope='hash-sampled labeled pool, not official held-out test; LONG_ANSWER excluded'))
    f = DATA/'rct-dev.txt'
    if f.exists():
        # Require the complete pinned official file, never accept a truncated download.
        import hashlib
        raw=f.read_bytes()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='30b4dabf34ef8a47d19363e86f5cb1308222c43d'
        criteria={'BACKGROUND':'Background and motivation','OBJECTIVE':'Study objective',
                  'METHODS':'Study methods','RESULTS':'Study results','CONCLUSIONS':'Conclusions'}
        doc=None;index=0
        for line in raw.decode().splitlines():
            if line.startswith('###'):doc=line[3:];index=0
            elif '\t' in line:
                label,text=line.split('\t',1)
                out.append(record('pubmed_rct_section',doc+':'+str(index),doc,
                    choice({'sentence':text},'Classify the rhetorical role of this abstract sentence.',criteria),label,
                    scope='single sentence classification, not a full-document sequence labeling comparison'))
                index+=1
    result=[]
    for task in sorted({r['task'] for r in out}):result.extend(sample([r for r in out if r['task']==task], n, task))
    return result


def prepare(n):
    imcs, audit = imcs_tasks(n)
    rows = imcs+nli_tasks(n)+extra_tasks(n)
    ids = [r['task']+'/'+r['id'] for r in rows]
    assert len(ids)==len(set(ids))
    for row in rows:
        assert set(row['request'])=={'state','questions'}
        for q in row['request']['questions'].values():
            if q['type']=='choice':assert 1 < len(q['criteria']) <= 255
        row['request_sha256'] = sha(row['request'])
    # Prepared rows can be archived per task with archive_experiments.py after hash verification.
    (DATA/'prepared.jsonl').write_text(''.join(dumps(r)+'\n' for r in rows))
    counts = collections.Counter(r['task'] for r in rows)
    files = {}
    for name in ['imcs-dev.json','imcs-train.json','imcs-symptom_norm.csv','nli4ct.zip',
                 'MTS_Dataset_ValidationSet.csv','MEDEC-MS-ValidationSet-with-GroundTruth-and-ErrorType.csv','pubmedqa.json','rct-dev.txt']:
        p=DATA/name
        if p.exists():files[name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    manifest={'seed':SEED,'sampling':'stable hash per task; development-set pilot, not leaderboard',
              'counts':dict(counts),'requests':sum(bool(r['request']['questions']) for r in rows),
              'questions':sum(len(r['request']['questions']) for r in rows),
              'imcs_data_audit':audit,'source_files':files,
              'cases':[{'task':r['task'],'id':r['id'],'group':r['group'],'request_sha256':r['request_sha256']} for r in rows]}
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print(dumps({k:v for k,v in manifest.items() if k not in ['cases','source_files']}))


def read_prepared():
    return [json.loads(s) for s in (DATA/'prepared.jsonl').read_text().splitlines()]


def credentials(env_file):
    # Parse only literal assignments; never execute a shell or print credential values.
    if env_file:
        for line in Path(env_file).read_text().splitlines():
            if '=' not in line or line.lstrip().startswith('#'):continue
            k,v=line.split('=',1);k=k.strip().removeprefix('export ')
            if k in ['TYPESAFE_API_KEY','TYPESAFE_MODEL']:
                os.environ[k]=v.strip().strip('\"\'')
    return os.environ.get('TYPESAFE_API_KEY')


def live(args):
    key=credentials(args.env_file)
    if not key:
        status={'status':'BLOCKED_MISSING_API_KEY','live_requests':0,
                'message':'No Jev predictions exist. Offline preparation is not a model test.'}
        (OUT/'live_status.json').write_text(json.dumps(status,indent=2))
        print(dumps(status));return 2
    model=args.model or os.environ.get('TYPESAFE_MODEL','jev-1.13.0')
    folder=DATA/'runs'/model;folder.mkdir(parents=True,exist_ok=True)
    rows=[r for r in read_prepared() if not args.task or r['task']==args.task]
    calls=0
    for row in rows:
        dest=folder/(sha([row['task'],row['id'],row['request_sha256']])+'.json')
        if dest.exists() and json.loads(dest.read_text()).get('status')=='ok':continue
        if calls>=args.max_calls:break
        body=dict(row['request'],model=model)
        if not body['questions']:
            dest.write_text(dumps({'status':'ok','task':row['task'],'id':row['id'],
                'request_sha256':row['request_sha256'],'response':{'answers':{},'usage':{'input_tokens':0,'output_tokens':0}},
                'elapsed_s':0,'deterministic_empty':True}));continue
        start=time.perf_counter();calls+=1
        req=urllib.request.Request('https://api.typesafe.ai/v1/systemone',data=dumps(body).encode(),
            headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
        result={'task':row['task'],'id':row['id'],'request_sha256':row['request_sha256']}
        fatal=False
        try:
            with urllib.request.urlopen(req,timeout=45) as response:obj=json.load(response)
            validate_response(row['request'],obj)
            result.update(status='ok',response=obj)
        except urllib.error.HTTPError as e:
            result.update(status='error',http_status=e.code,error='HTTPError')
            fatal=e.code in (401,403,402,429)
        except Exception as e:
            result.update(status='error',error=type(e).__name__)
        result['elapsed_s']=time.perf_counter()-start
        dest.write_text(dumps(result))
        print(dumps({'task':row['task'],'id':row['id'],'status':result['status'],'call':calls}),flush=True)
        if fatal:break
    (OUT/'live_status.json').write_text(dumps({'status':'RUN_ATTEMPTED','model_requested':model,'new_requests':calls}))
    return 0


def validate_response(request, response):
    answers=response['answers']
    if set(answers)!=set(request['questions']):raise ValueError('Question IDs mismatch')
    for key,q in request['questions'].items():
        a=answers[key]
        if q['type']=='choice':
            if a['choice'] not in q['criteria']:raise ValueError('Invalid choice')
            p=a['probabilities']
            if set(p)!=set(q['criteria']):raise ValueError('Probability labels mismatch')
            if any(not isinstance(v,(float,int)) or not math.isfinite(v) or not 0<=v<=1 for v in p.values()):raise ValueError('Invalid probability')
            if abs(sum(p.values())-1)>.03:raise ValueError('Probabilities do not sum to one')
        else:
            if not isinstance(a['noul'],(float,int)) or not 0<=a['noul']<=1:raise ValueError('Invalid Noul')


def classification(gold,pred):
    labels=sorted(set(gold)|set(pred));metrics={}
    for label in labels:
        tp=sum(g==label and p==label for g,p in zip(gold,pred))
        fp=sum(g!=label and p==label for g,p in zip(gold,pred))
        fn=sum(g==label and p!=label for g,p in zip(gold,pred))
        metrics[label]={'support':gold.count(label),'precision':tp/(tp+fp) if tp+fp else 0,
                        'recall':tp/(tp+fn) if tp+fn else 0,'f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0}
    gold_labels=set(gold)
    return {'n':len(gold),'accuracy':sum(g==p for g,p in zip(gold,pred))/len(gold) if gold else None,
            'macro_f1_observed_gold_classes':sum(metrics[l]['f1'] for l in gold_labels)/len(gold_labels) if gold_labels else None,
            'per_class':metrics}


def sets_metric(pairs):
    tp=fp=fn=0
    for g,p in pairs:tp+=len(g&p);fp+=len(p-g);fn+=len(g-p)
    return {'tp':tp,'fp':fp,'fn':fn,'precision':tp/(tp+fp) if tp+fp else 0,
            'recall':tp/(tp+fn) if tp+fn else 0,'micro_f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0}


def score(model):
    rows=read_prepared();report={}
    for task in sorted({r['task'] for r in rows}):
        subset=[r for r in rows if r['task']==task];pairs=[];cg=[];cp=[];times=[];tokens=0;models=set();errors=[];done=0
        for r in subset:
            path=DATA/'runs'/model/(sha([r['task'],r['id'],r['request_sha256']])+'.json')
            if not path.exists():continue
            result=json.loads(path.read_text())
            if result['status']!='ok':errors.append(r['id']);continue
            done+=1;response=result['response'];a=response['answers'];times.append(result['elapsed_s'])
            tokens+=response.get('usage',{}).get('input_tokens',0);models.add(response.get('model','deterministic_empty'))
            if task=='imcs_ner_dictionary_pipeline':
                pred={tuple([s,e,a['s'+str(i)]['choice']]) for i,(s,e,_) in enumerate(r['metadata']['candidates']) if a['s'+str(i)]['choice']!='none'}
                pairs.append(({tuple(x) for x in r['gold']},pred))
            elif task=='nli4ct_evidence':pairs.append((set(r['gold']),{k for k,v in a.items() if v['noul']>=.5}))
            else:cg.append(r['gold']);cp.append(a['decision']['choice'])
        metrics=sets_metric(pairs) if pairs else classification(cg,cp) if cg else None
        report[task]={'planned':len(subset),'successful':done,'missing_or_failed':len(subset)-done,
                      'completion_rate':done/len(subset),'quality_on_successful_only':metrics,
                      'input_tokens':tokens,'returned_models':sorted(models),'error_ids':errors,
                      'latency_median_s':sorted(times)[len(times)//2] if times else None}
    (OUT/'jev_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(dumps(report))


def offline():
    rows=read_prepared();report={'status':'OFFLINE_BASELINES_ONLY_NOT_JEV','tasks':{}}
    for task in ['imcs_normalization_top20','imcs_ner_dictionary_pipeline']:
        rr=[r for r in rows if r['task']==task]
        if task=='imcs_normalization_top20':
            result=classification([r['gold'] for r in rr],[r['metadata']['baseline'] for r in rr])
            result['candidate_recall_at20']=sum(r['metadata']['candidate_hit'] for r in rr)/len(rr)
            result['warning']='Gold spans supplied. Candidate recall is not end-to-end extraction recall.'
        else:
            result=sets_metric([({tuple(x) for x in r['gold']},{tuple(x) for x in r['metadata']['baseline']}) for r in rr])
            total=sum(len(r['gold']) for r in rr)
            hits=sum(sum((a,b) in {(x[0],x[1]) for x in r['metadata']['candidates']} for a,b,_ in r['gold']) for r in rr)
            result['candidate_span_recall_upper_bound']=hits/total if total else 0
            result['warning']='All training-dictionary matches kept; overlapping matches allowed. No Jev used.'
        result['n']=len(rr);report['tasks'][task]=result
    (OUT/'offline_baselines.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(dumps({t:{k:v for k,v in r.items() if k!='per_class'} for t,r in report['tasks'].items()}))


def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','live','score','offline'])
    p.add_argument('--n',type=int,default=100);p.add_argument('--model',default=None)
    p.add_argument('--env-file');p.add_argument('--task');p.add_argument('--max-calls',type=int,default=1000)
    args=p.parse_args()
    if args.action=='prepare':prepare(args.n)
    elif args.action=='offline':offline()
    elif args.action=='score':score(args.model or 'jev-1.13.0')
    else:return live(args)
    return 0


if __name__=='__main__':raise SystemExit(main())
