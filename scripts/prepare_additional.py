"""Public expansion; source labels are excluded from request states."""
import json,csv,re,collections
import benchmark as b
D=b.DATA/'more'; rows=[]
def add(task,id_,group,state,instruction,criteria,gold,**meta):
 assert gold in criteria,(task,id_,gold)
 r=b.record(task,str(id_),str(group),b.choice(state,instruction,criteria),gold,**meta);r['request_sha256']=b.sha(r['request']);rows.append(r)
def multi(task,id_,group,state,instruction,criteria,gold,**meta):
 assert set(gold)<=set(criteria)
 req={'state':state,'questions':{k:{'type':'noul','instructions':instruction+' Candidate: '+v} for k,v in criteria.items()}}
 r=b.record(task,str(id_),str(group),req,gold,scoring='multi_question_keys',**meta);r['request_sha256']=b.sha(req);rows.append(r)
for lang in ['CN','EN','ARA']:
 pool=[dict(r,id=r['Text ID']) for r in csv.DictReader((D/f'MedErrBench/datasets/test/reviewed_data_{lang}_test.csv').open())]
 for r in b.sample(pool,100,lang):
  add('mederrbench_'+lang,r['id'],r['id'],r['Text'],'Does this clinical narrative contain a medical factual or reasoning error? Evaluate the content, not encoding or grammar.',{'0':'No medical error','1':'Contains a medical error'},r['Error Flag'],source='MedErrBench official test',language=lang)
pool=[dict(r,id=str(i)) for i,r in enumerate(csv.DictReader((D/'CMExam/data/test_with_annotations.csv').open()))]
for r in b.sample(pool,100,'cmexam'):
 opt=dict(re.findall(r'^([A-Z])\s+(.+)$',r['Options'],re.M))
 if len(r['Answer'])==1:add('cmexam_mcq',r['id'],r['id'],r['Question'],'选择医学考试题的最佳答案。',opt,r['Answer'],source='CMExam official test',indicator=r['Medical Discipline'])
 else:multi('cmexam_mcq',r['id'],r['id'],r['Question'],'判断该候选是否为多选题的正确答案。',opt,list(r['Answer']),source='CMExam official test')
for r in json.loads((D/'TCM-BEST4SDT/TCM-BEST4SDT.json').read_text()):
 if 'question' in r:
  task={'中医基础知识':'tcm_best_knowledge','医学伦理':'tcm_best_ethics','大语言模型内容安全':'tcm_best_safety'}.get(r['class'],'tcm_best_'+r['class'])
  gold=re.findall('[A-J]',r['answer'])
  if len(gold)==1:add(task,r['id'],r['id'],r['question'],'选择题目的最佳答案。',r['option'],gold[0],source='TCM-BEST4SDT objective items; one pass not official three-repeat metric')
  else:multi(task,r['id'],r['id'],r['question'],'判断该候选是否为此多选题的正确答案。',r['option'],gold,source='TCM-BEST4SDT objective multilabel; threshold0.5')
 else:
  if int(r['id'])%3:continue
  vals=dict(s.split('：',1) for s in r['output'] if '：' in s)
  for field,task in [('证型','tcm_best_syndrome'),('病性','tcm_best_nature'),('病位','tcm_best_location'),('治则治法','tcm_best_principles')]:
   opt=dict(re.findall(r'([A-J]):([^;]+)',vals[field+'选项']));gold=re.findall('[A-J]',vals[field+'答案'])
   if len(gold)==1:add(task,r['id'],r['id'],r['instruction'],'根据病例选择'+field+'的最佳选项。',opt,gold[0],source='TCM-BEST4SDT every third SDT case; no diagnosis or explanation in state')
   else:multi(task,r['id'],r['id'],r['instruction'],'根据病例判断该选项是否是正确的'+field+'。',opt,gold,source='TCM-BEST4SDT SDT multilabel, threshold0.5')
# Keep single and multi scoring separate because some tasks mix them.
for r in rows:
 if r['metadata'].get('scoring'):r['task']+='_multi'
p=b.DATA/'additional_prepared.jsonl';p.write_text(''.join(b.dumps(r)+'\n' for r in rows));print(collections.Counter(r['task'] for r in rows),len(rows))
