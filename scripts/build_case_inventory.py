"""Count source cases separately from records and expose per-case paired results."""
import argparse,collections,json,re
from pathlib import Path
import benchmark as b
from verify_experiments import prediction
ROOT=Path(__file__).resolve().parents[1]
def read(p):return [json.loads(l) for l in p.read_text().splitlines()]
def case_key(row):
 task=row['task']
 if task=='nubes_scope_status':return row['id'].split(':')[0]
 if task.startswith('clinocr_'):
  return row['metadata'].get('source_case_id') or re.search(r't\d+_s\d+',row['id'])[0]
 return str(row.get('group',row['id']))
def unit(task):
 if task.startswith('primock_'):return '不同公开演绎会话'
 if task.startswith('clinocr_'):return '不同原始文档（同一文档的扫描变体合并）'
 if task=='nubes_scope_status':return '不同源文件临床片段（同一片段多个标注合并）'
 if task.startswith('challenge_'):return '自编测试案例（含相关模板变体）'
 return '来源分组中的不同病例、文档或题目；不等于患者数'
def quality(pairs):
 return b.sets_metric(pairs) if isinstance(pairs[0][0],set) else b.classification([g for g,p in pairs],[p for g,p in pairs])
def display(q):return f'{q["accuracy"]:.1%}' if 'accuracy' in q else f'{q["micro_f1"]*100:.1f} 分 F1'
def safe(s):return re.sub(r'\s+',' ',str(s)).replace('|','／').replace('<','＜').replace('>','＞')
def preview(state):
 if isinstance(state,str):return safe(state)[:110]
 return safe(json.dumps(state,ensure_ascii=False))[:110]
def build():
 methods=json.loads((ROOT/'results/task_methods.json').read_text());scenes=json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes'];tasks={};files={}
 for scene in scenes:
  for task in scene['task_ids']:
   folder=ROOT/'scenarios'/scene['id']/task;rows=read(folder/'samples.jsonl');j={r['id']:r for r in read(folder/'responses.jsonl')};d={r['id']:r for r in read(folder/'comparison/deepseek_responses.jsonl')};groups=collections.defaultdict(list);cohorts=collections.defaultdict(list)
   for r in rows:groups[case_key(r)].append(r);cohorts[r['metadata'].get('cohort','原归档样本')].append(r)
   def pairs(rs,provider):
    if provider=='jev':return [prediction(r,j[r['id']]) for r in rs]
    result=[]
    for r in rs:
     record=d[r['id']]
     if record['status']=='ok':result.append(prediction(r,{'response':{'answers':record['normalized_answers']}}))
     else:
      g=prediction(r,j[r['id']])[0];result.append((g,set() if isinstance(g,set) else '__FAILURE__'))
    return result
   info={'scene':scene['id'],'title':methods[task]['title'],'records':len(rows),'cases':len(groups),'case_unit':unit(task),'cohorts':{}}
   lines=[f'# {methods[task]["title"]}：逐案例结果','',f'{len(groups)} 个案例，共 {len(rows)} 条测试记录。案例口径：{unit(task)}。同一案例内的多条记录不重复算案例。','', '下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。','']
   if len(cohorts)>1:
    lines+=['## 不同来源的表现','','| 来源分组 | 案例 | 测试记录 | Jev | DeepSeek |','| --- | ---: | ---: | ---: | ---: |']
   for name,rs in cohorts.items():
    c={'cases':len({case_key(r) for r in rs}),'records':len(rs),'jev':quality(pairs(rs,'jev')),'deepseek':quality(pairs(rs,'deepseek'))};info['cohorts'][name]=c
    if len(cohorts)>1:lines.append(f'| {name} | {c["cases"]} | {c["records"]} | {display(c["jev"])} | {display(c["deepseek"])} |')
   lines+=['','## 案例明细','','| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |','| --- | --- | ---: | ---: | ---: |']
   for key,rs in groups.items():lines.append(f'| {safe(key)} | {preview(rs[0]["request"]["state"])}… | {len(rs)} | {display(quality(pairs(rs,"jev")))} | {display(quality(pairs(rs,"deepseek")))} |')
   files[folder/'cases.md']='\n'.join(lines)+'\n';tasks[task]=info
 summary={'tasks':tasks,'task_count':len(tasks),'minimum_cases_per_task':min(v['cases'] for v in tasks.values()),'main_records':sum(v['records'] for v in tasks.values())}
 files[ROOT/'results/case_inventory.json']=json.dumps(summary,ensure_ascii=False,indent=2)+'\n'
 return summary,files
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args();summary,files=build()
 assert summary['task_count']==96 and summary['minimum_cases_per_task']>=20,[(t,v['cases']) for t,v in summary['tasks'].items() if v['cases']<20]
 for p,text in files.items():
  if a.check:assert p.read_text()==text,p
  else:p.write_text(text)
 print('Verified',summary['task_count'],'tasks; minimum',summary['minimum_cases_per_task'],'source cases; records',summary['main_records'])
if __name__=='__main__':main()
