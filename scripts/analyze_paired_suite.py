"""Recompute all expanded paired runs and publish scenario-level comparisons."""
import argparse,json,shutil,collections
from pathlib import Path
import benchmark as b
from analyze_paired_new import analyze
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'comparisons/paired-suite'
def readlines(path):return [json.loads(x) for x in path.read_text().splitlines()]
def table(experiments, prefix=''):
 lines=['| 医疗工作（材料数） | 每次判断数 | 正确率：Jev / DeepSeek | 整批总耗时：Jev / DeepSeek | 每千项判断费用：Jev / DeepSeek |','| --- | ---: | ---: | ---: | ---: |']
 for e in experiments:
  for r in e['summary']['results']:
   j,d=r['jev'],r['deepseek']
   lines.append(f'| [{e["title"]}（{e["materials"]}）]({prefix}{e["path"]}/README.md) | {r["group_size"]} | {j["accuracy"]:.1%} / {d["accuracy"]:.1%} | {j["batch_elapsed_mean_s"]:.1f} / {d["batch_elapsed_mean_s"]:.1f} 秒 | ${j["cost_per_1000_decisions_usd"]:.3f} / ${d["cost_per_1000_decisions_usd"]:.3f} |')
 return lines

def artifacts(e,folder):
 base=ROOT/e['path'];protocol=json.loads((base/'protocol.json').read_text());summary=analyze(folder,base)
 samples=readlines(base/'inputs.jsonl');source={r['id']:r for r in samples};records=readlines(folder/'responses.jsonl')
 assert len(source)==e['materials']==protocol['documents']
 assert e['selection_sha256']==protocol['selection_sha256']
 assert all(r['request_sha256']==b.sha(r['request']) and len(r['gold'])==10 for r in samples)
 metrics=collections.defaultdict(lambda: [[],[]]);semantic=collections.defaultdict(lambda: [[],[]]);converted=collections.Counter()
 for r in records:
  pred={q:v for c in r['calls'] if c['attempts'][-1]['status']=='ok' for q,v in c['attempts'][-1]['answers'].items()}
  g,p=metrics[(r['provider'],r['group_size'])]
  for q,label in source[r['id']]['gold'].items():g.append(label);p.append(pred.get(q,'MISSING'))
  if protocol['positive_label']:
   loose=dict(pred)
   for c in r['calls']:
    final=c['attempts'][-1]
    if r['provider']=='deepseek' and final['status']!='ok' and 'response' in final:
     try:
      choice=final['response']['choices'][0];obj=json.loads(choice['message']['content']);answers=obj['answers']
      if choice['finish_reason']=='stop' and set(obj)=={'answers'} and set(answers)==set(c['question_ids']):
       for q,v in answers.items():
        if type(v) is bool:loose[q]='evidence' if v else 'not_evidence';converted[(r['provider'],r['group_size'])]+=1
        elif isinstance(v,str) and v in source[r['id']]['request']['questions'][q]['criteria']:loose[q]=v
     except (ValueError,KeyError,TypeError):pass
   sg,sp=semantic[(r['provider'],r['group_size'])]
   for q,label in source[r['id']]['gold'].items():sg.append(label);sp.append(loose.get(q,'MISSING'))
 for r in summary['results']:
  for provider in ['jev','deepseek']:
   r[provider]['quality_detail']=b.classification(*metrics[(provider,r['group_size'])])
   assert r[provider]['quality_detail']['accuracy']==r[provider]['accuracy']
   if protocol['positive_label']:
    r[provider]['semantic_review']=b.classification(*semantic[(provider,r['group_size'])]);r[provider]['boolean_answers_converted']=converted[(provider,r['group_size'])]
 lines=[f'# {e["title"]}：新增材料对照','',protocol['description'], '',*table([{**e,'summary':summary}], '../../../../'), '',
 '总时间是完成本场景全部材料的实际经过时间，两轮取平均，包含排队、重试和失败等待；同时处理 4 份材料，每份内部依次发请求。每份材料固定 10 项判断，各种分组使用相同全文和问题。正确率合并两轮；重复测试不计作新案例。', '',
 '## 两轮明细','', '| 模型 | 每次判断数 | 第一轮总耗时 | 第二轮总耗时 | 第一轮正确率 | 第二轮正确率 | 缺失答案 | 重试次数 |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
 for r in summary['results']:
  for p,label in [('jev','Jev'),('deepseek','DeepSeek')]:
   s=r[p];lines.append(f'| {label} | {r["group_size"]} | {s["batch_elapsed_s"][0]:.2f} 秒 | {s["batch_elapsed_s"][1]:.2f} 秒 | {s["round_accuracy"][0]:.1%} | {s["round_accuracy"][1]:.1%} | {s["missing_answers"]} | {s["retry_attempts"]} |')
 lines+=['','## 缓存与费用','','| 模型 | 每次判断数 | 第一轮每千项费用 | 第二轮每千项费用 | 第一轮输入缓存命中 | 第二轮输入缓存命中 |','| --- | ---: | ---: | ---: | ---: | ---: |']
 for r in summary['results']:
  for p,label in [('jev','Jev'),('deepseek','DeepSeek')]:
   s=r[p];hit=['—' if v is None else f'{v:.1%}' for v in s['round_cache_hit_fraction']];cost=[v/e['unique_decisions']*1000 for v in s['round_cost_usd']];lines.append(f'| {label} | {r["group_size"]} | ${cost[0]:.4f} | ${cost[1]:.4f} | {hit[0]} | {hit[1]} |')
 if protocol['positive_label']:
  lines+=['','## 证据筛选是否漏检、误报？','','正确率会受到非证据句占比较高的影响。下表单独评估真正的证据句：查准率表示选出的句子中有多少正确，召回率表示找到了多少原标注证据，综合分 F1 同时考虑两者。','','| 每次判断数 | Jev 查准率 / 召回率 / F1 | DeepSeek 查准率 / 召回率 / F1 |','| --- | ---: | ---: |']
  for r in summary['results']:
   vals=[r[p]['quality_detail']['per_class']['evidence'] for p in ['jev','deepseek']];lines.append('| '+str(r['group_size'])+' | '+' | '.join(' / '.join(f'{m[k]:.1%}' for k in ['precision','recall','f1']) for m in vals)+' |')
  lines+=['','### 格式差异的补充复核','','DeepSeek 有时用布尔值回答标签选择题。主表按调用前约定计分，格式不符的输出计为缺失；下面另把最后一次响应中明确的 true／false 对应为 evidence／not_evidence，并接纳同次响应中的有效标签。只转换含义明确的答案，不改变原始记录、重试、耗时或费用。这是测试后补充分析，不是重新调用。','','| 每次判断数 | Jev 含义正确率 / 证据 F1 | DeepSeek 含义正确率 / 证据 F1 | DeepSeek 布尔值转换数 |','| --- | ---: | ---: | ---: |']
  for r in summary['results']:
   m=[r[p]['semantic_review'] for p in ['jev','deepseek']];lines.append(f'| {r["group_size"]} | {m[0]["accuracy"]:.1%} / {m[0]["per_class"]["evidence"]["f1"]:.1%} | {m[1]["accuracy"]:.1%} / {m[1]["per_class"]["evidence"]["f1"]:.1%} | {r["deepseek"]["boolean_answers_converted"]} |')
  lines+=['','使用 SciFact 训练集中的公开人工标注，仅表示这些材料未用于本仓库先前调用，不意味着参评模型未见过。样本选入全部标注证据句，并补足非证据句至 10 句；原标注可能不包含所有合理证据，结果对应这一筛选任务，不能等同于主张真伪判断。']
 lines+=['','## 数据与方法','',f'[原始来源]({protocol["source_url"]}) · [完整输入、问题与原标注答案](inputs.jsonl) · [逐案例结果](cases.md) · [真实响应](responses.jsonl) · [批次计时](blocks.jsonl) · [统计结果](summary.json) · [调用前方案](protocol.json)','',
 '样本按固定哈希顺序选择并在调用前锁定。PubMed 排除旧摘要及逐句重复；IMCS 排除主评测中的患者 ID；SciFact 排除旧主张和摘要重复，并采用不同文献。选择范围与源数据哈希见方案。','',
 'Jev 使用 jev-1.13.0；DeepSeek 使用 deepseek-flash，关闭思考、仅返回标签。每家独立复用最多 4 个 HTTP/1.1 连接；连接超时 10 秒，读取超时 30 秒，失败最多补试一次，错误答案不重试。第二轮反向执行配置顺序。服务端缓存未控制，时间反映当前网络和服务条件，不是模型纯推理速度。','',
 '费用按实际返回用量估算：Jev 每百万输入 token 0.042 美元，输出免费；DeepSeek 本次空闲时段每百万缓存输入／非缓存输入／输出分别为 0.003／0.15／0.6 美元。有用量的重试也计费，不含系统接入与人工复核。缓存条件变化会改变费用排序。','',
 '第三方原文和标注遵循各自数据来源条件，仓库代码许可不覆盖第三方数据。','']
 case_lines=[f'# {e["title"]}：逐案例结果','', '每份材料含 10 个不同判断。下表为一次合并 10 项时，两轮分别答对的数量；全部材料、问题及答案见 [inputs.jsonl](inputs.jsonl)。', '', '| 原始案例 ID | Jev 两轮答对数（每轮 10 项） | DeepSeek 两轮答对数（每轮 10 项） |','| --- | ---: | ---: |']
 # Records finish out of order; explicitly sort by round for per-case reporting.
 for sample in samples:
  values=[]
  for p in ['jev','deepseek']:
   runs=sorted((r for r in records if r['id']==sample['id'] and r['provider']==p and r['group_size']==10),key=lambda r:r['round'])
   correct=[]
   for r in runs:
    pred={q:v for c in r['calls'] if c['attempts'][-1]['status']=='ok' for q,v in c['attempts'][-1]['answers'].items()};correct.append(sum(pred.get(q)==g for q,g in sample['gold'].items()))
   values.append(' / '.join(map(str,correct)))
  case_lines.append(f'| {sample["id"]} | {values[0]} | {values[1]} |')
 return summary,{'README.md':'\n'.join(lines),'cases.md':'\n'.join(case_lines)+'\n','summary.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--check',action='store_true');a=ap.parse_args();manifest=json.loads((BASE/'manifest.json').read_text());experiments=[]
 for e in manifest['experiments']:
  base=ROOT/e['path'];folder=a.source/e['id'] if a.source else base
  summary,files=artifacts(e,folder);experiments.append({**e,'summary':summary})
  if a.source and not a.check:
   for name in ['responses.jsonl','blocks.jsonl']:shutil.copyfile(folder/name,base/name)
  for name,content in files.items():
   if a.check:assert (base/name).read_text()==content,(e['id'],name)
   else:(base/name).write_text(content)
 report={'materials':manifest['materials'],'unique_decisions':manifest['unique_decisions'],'experiments':experiments}
 lines=['# 三类医疗工作的新增案例对照','', '新增 140 份材料、1,400 个不同判断：60 篇临床试验摘要、40 段中文问诊、40 组医学主张与文献。与此前 20 篇摘要没有材料重合；主评测 96 项任务的统计单独保留。每种配置测两轮。','',*table(experiments,'../../'),'','总耗时按本场景整批材料计，两轮取平均；每家同时处理 4 份材料，每份内部依次请求。每份均有相同的 10 个问题：每次 1 项调用 10 次，每次 5 项调用 2 次，每次 10 项调用 1 次。单项配置仍传完整上下文，因此不代表孤立短句调用的最低成本。','','正确率、成本均计入全部输入，缺失答案算错，失败重试耗时不剔除。费用包括有用量的重试。缓存未控制，重复轮次可能使 DeepSeek 更便宜；各场景明细提供分轮费用与命中率。证据筛选还需结合子页中的查准率、召回率及 F1 判断，不能只看正确率。','','这些任务评估内容整理和证据筛选，不能据此判断诊疗决策能力。每个场景的完整案例、提示词、原答案、原始响应、选择范围和逐案例对比均在对应目录。','','[首次 20 篇摘要对照](../../scenarios/evidence/pubmed_rct_section/paired-new/README.md) · [实验清单](manifest.json) · [汇总数据](summary.json)','']
 for name,content in {'summary.json':json.dumps(report,ensure_ascii=False,indent=2)+'\n','README.md':'\n'.join(lines)}.items():
  if a.check:assert (BASE/name).read_text()==content,name
  else:(BASE/name).write_text(content)
 print('Verified expanded suite:',manifest['materials'],'materials,',manifest['unique_decisions'],'unique decisions')
if __name__=='__main__':main()
