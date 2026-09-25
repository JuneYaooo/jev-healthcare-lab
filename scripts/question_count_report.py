"""Describe archived timing by questions per request; no new API calls."""
import argparse,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'comparisons/batch-time'

def analyze():
 rows={}
 for path in sorted((ROOT/'scenarios').glob('*/*/samples.jsonl')):
  for line in path.read_text().splitlines():
   r=json.loads(line);rows[(r['task'],r['id'])]=r
 runs={}
 for provider in ['jev','deepseek']:
  records=[json.loads(x) for x in (BASE/provider/'responses.jsonl').read_text().splitlines()]
  runs[provider]={(r['task'],r['id']):r for r in records}
  assert len(records)==len(rows) and set(runs[provider])==set(rows)
 groups=[]
 for label,low,high in [('单项判断',1,1),('2–10 项同时判断',2,10),('11 项及以上同时判断',11,float('inf'))]:
  keys=[k for k,r in rows.items() if low<=len(r['request']['questions'])<=high]
  g={'label':label,'inputs':len(keys),'question_range':[min(len(rows[k]['request']['questions']) for k in keys),max(len(rows[k]['request']['questions']) for k in keys)]}
  for provider,records in runs.items():
   chosen=[records[k] for k in keys]
   assert all(r['attempts'] for r in chosen)
   g[provider]={'median_input_elapsed_s':statistics.median(r['finished_after_s']-r['started_after_s'] for r in chosen),'failed_inputs':sum(r['status']!='ok' for r in chosen),'retry_inputs':sum(len(r['attempts'])>1 for r in chosen),'cost_usd':sum(a.get('cost_usd',0) for r in chosen for a in r['attempts'])}
  groups.append(g)
 empty=sum(not r['request']['questions'] for r in rows.values())
 assert sum(g['inputs'] for g in groups)+empty==len(rows)
 return {'total_inputs':len(rows),'deterministic_empty_inputs':empty,'scope':'Descriptive groups from one existing replay, not a controlled question-count experiment. Input elapsed time includes retries and terminal failures, excludes waiting before a worker starts.','groups':groups}

def table(report):
 lines=['| 每份输入的判断数量 | 输入数 | Jev 单次等待中位数 | DeepSeek 单次等待中位数 |','| --- | ---: | ---: | ---: |']
 for g in report['groups']:lines.append(f'| {g["label"]} | {g["inputs"]:,} | {g["jev"]["median_input_elapsed_s"]:.3f} 秒 | {g["deepseek"]["median_input_elapsed_s"]:.3f} 秒 |')
 return lines

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();report=analyze()
 lines=['# 按单次请求的判断数量比较等待时间','','从同一批全量测速记录中，按每份输入包含的问题数量分组。单项判断例如确定一段文字所属病历章节；多项判断例如在一份材料中同时核对多个实体候选。这里的判断数量不等于仓库的任务种类数，也不等于 API 并发数。','']+table(report)+['','单次等待从工作线程开始处理该输入，到成功或最终失败为止，包含该输入的重试及等待；最终失败记录也保留在统计内。它不含任务开始前的队列等待，不能代替整批总耗时。43 条无候选、未调用 API 的输入不进入本表。','','## 失败与重试','','| 分组 | 最终失败：Jev / DeepSeek | 发生重试：Jev / DeepSeek |','| --- | ---: | ---: |']
 for g in report['groups']:lines.append(f'| {g["label"]} | {g["jev"]["failed_inputs"]} / {g["deepseek"]["failed_inputs"]} | {g["jev"]["retry_inputs"]} / {g["deepseek"]["retry_inputs"]} |')
 lines+=['','## 结果适用于什么情况？','','这些记录中，单问题组的 DeepSeek 等待中位数更低，11 项及以上组的 Jev 更低。各组的材料长度、任务内容和候选数量不同，因此不能把组间差异归因于增加问题数量，也不能据此预测某份病历改成多问题调用后会快多少。','','DeepSeek 关闭思考，只返回选项或布尔值；Jev 同时返回其原生概率信息。输入是重复测速材料，DeepSeek 整批缓存命中约 81%，没有单独控制各组缓存状态。客户端每次请求建立连接，未复用连接。','','严格比较单项与多项处理，需要固定同一份材料和同一组判断，分别拆成单问题请求与合成多问题请求；两种模型均采用相同分组，并同时核对准确率、完成所有判断的总耗时和费用。本表是已有记录的分组观察，不是上述配对实验。','','[统计 JSON](question_counts.json) · [统计代码](../../scripts/question_count_report.py) · [整批耗时及原始响应](README.md)','']
 outputs={BASE/'question_counts.json':json.dumps(report,ensure_ascii=False,indent=2)+'\n',BASE/'question_counts.md':'\n'.join(lines)}
 for p,value in outputs.items():
  if args.check:assert p.read_text()==value,str(p)
  else:p.write_text(value)
 print('Question-count groups verified:',[(g['label'],g['inputs']) for g in report['groups']])
if __name__=='__main__':main()
