"""Verify and summarize the locked fresh-document paired experiment."""
import argparse,collections,json,math,statistics,shutil
from pathlib import Path
import benchmark as b
from compare_deepseek import request_payload,normalize
from prepare_paired_new import BASE

def analyze(folder):
 protocol=json.loads((BASE/'protocol.json').read_text());samples=[json.loads(x) for x in (BASE/'inputs.jsonl').read_text().splitlines()];assert b.sha(samples)==protocol['selection_sha256'];source={r['id']:r for r in samples}
 blocks=[json.loads(x) for x in (folder/'blocks.jsonl').read_text().splitlines()];records=[json.loads(x) for x in (folder/'responses.jsonl').read_text().splitlines()]
 assert [{k:s[k] for k in ['round','provider','group_size']} for s in blocks]==protocol['order'];assert all(not s['aborted'] and s['documents']==20 for s in blocks)
 blockmap={(s['round'],s['provider'],s['group_size']):s for s in blocks};seen=set();groups=collections.defaultdict(list)
 for r in records:
  key=(r['round'],r['provider'],r['group_size']);identity=(*key,r['id']);assert identity not in seen;seen.add(identity);sample=source[r['id']];p=r['provider'];seenq=[];pred={};cost=0;retries=0;usage=collections.Counter();errors=collections.Counter();connection_starts=0;attempts=0
  assert 0<=r['started_after_s']<=r['finished_after_s']<=blockmap[key]['batch_elapsed_s']
  assert math.isclose(r['elapsed_s'],r['finished_after_s']-r['started_after_s'],abs_tol=.01)
  for c in r['calls']:
   names=c['question_ids'];seenq+=names;req={'state':sample['request']['state'],'questions':{q:sample['request']['questions'][q] for q in names}}
   assert len(names)==r['group_size'] and c['request_sha256']==b.sha(req)
   payload=dict(req,model='jev-1.13.0') if p=='jev' else request_payload({'request':req});assert c['provider_request_sha256']==b.sha(payload)
   assert 1<=len(c['attempts'])<=2;retries+=len(c['attempts'])-1
   for a in c['attempts']:
    attempts+=1;connection_starts+=sum(e['event']=='connection.connect_tcp.started' for e in a['trace'])
    assert r['started_after_s']<=a['started_after_s']<=a['finished_after_s']<=r['finished_after_s']
    if a['status']!='ok':errors[a.get('error_type',str(a.get('http_status',a['status'])))]+=1
    if 'response' in a:
     data=a['response'];assert data['model']==('jev-1.13.0' if p=='jev' else 'deepseek-flash');u=data['usage']
     for k,v in u.items():
      if isinstance(v,(int,float)):usage[k]+=v
     if p=='jev':expected=u['input_tokens']*.042/1e6
     else:
      hit=u.get('prompt_cache_hit_tokens',0);miss=u.get('prompt_cache_miss_tokens',u['prompt_tokens']-hit);expected=(hit*.003+miss*.15+u['completion_tokens']*.6)*(1 if a['tariff']=='off_peak' else 2)/1e6
     assert math.isclose(expected,a['cost_usd'],abs_tol=1e-12);cost+=expected
     if a['status']=='ok':
      if p=='jev':b.validate_response(req,data);ans={q:data['answers'][q]['choice'] for q in names}
      else:
       assert data['choices'][0]['finish_reason']=='stop';norm=normalize({'request':req},data);ans={q:norm[q]['choice'] for q in names}
      assert ans==a['answers']
   if len(c['attempts'])==2:assert c['attempts'][0]['status']!='ok'
   if c['attempts'][-1]['status']=='ok':pred.update(c['attempts'][-1]['answers'])
  assert seenq==list(sample['request']['questions'])
  groups[key].append({'id':r['id'],'correct':sum(pred.get(q)==g for q,g in sample['gold'].items()),'missing':10-len(pred),'cost_usd':cost,'elapsed_s':r['elapsed_s'],'retries':retries,'usage':dict(usage),'errors':dict(errors),'connection_starts':connection_starts,'attempts':attempts})
 assert len(seen)==240
 for key,rs in groups.items():
  assert {r['id'] for r in rs}==set(source)
  assert math.isclose(sum(r['cost_usd'] for r in rs),blockmap[key]['reported_cost_usd'],abs_tol=1e-9)
 results=[]
 for size in protocol['group_sizes']:
  result={'group_size':size}
  for p in ['jev','deepseek']:
   rs=[r for rep in [1,2] for r in groups[(rep,p,size)]];cost=sum(r['cost_usd'] for r in rs);use=collections.Counter();errors=collections.Counter()
   for r in rs:use.update(r['usage']);errors.update(r['errors'])
   result[p]={'scored_decisions':400,'correct':sum(r['correct'] for r in rs),'accuracy':sum(r['correct'] for r in rs)/400,'missing_answers':sum(r['missing'] for r in rs),'document_elapsed_median_s':statistics.median(r['elapsed_s'] for r in rs),'batch_elapsed_s':[blockmap[(rep,p,size)]['batch_elapsed_s'] for rep in [1,2]],'batch_elapsed_mean_s':statistics.mean(blockmap[(rep,p,size)]['batch_elapsed_s'] for rep in [1,2]),'cost_usd':cost,'cost_per_1000_decisions_usd':cost/400*1000,'retry_attempts':sum(r['retries'] for r in rs),'attempts':sum(r['attempts'] for r in rs),'connection_starts':sum(r['connection_starts'] for r in rs),'usage':dict(use),'errors':dict(errors),'round_accuracy':[sum(r['correct'] for r in groups[(rep,p,size)])/200 for rep in [1,2]],'round_cost_usd':[sum(r['cost_usd'] for r in groups[(rep,p,size)]) for rep in [1,2]],'round_cache_hit_fraction':[sum(r['usage'].get('prompt_cache_hit_tokens',0) for r in groups[(rep,p,size)])/max(1,sum(r['usage'].get('prompt_tokens',0) for r in groups[(rep,p,size)])) if p=='deepseek' else None for rep in [1,2]]}
  results.append(result)
 return {'documents':20,'unique_decisions':200,'repetitions':2,'results':results}

def table(summary):
 lines=['| 每次处理的判断数 | 正确率：Jev / DeepSeek | 完成全部 20 篇总耗时：Jev / DeepSeek | 每千项判断费用：Jev / DeepSeek |','| --- | ---: | ---: | ---: |']
 for r in summary['results']:
  j,d=r['jev'],r['deepseek'];lines.append(f'| {r["group_size"]} 项 | {j["accuracy"]:.1%} / {d["accuracy"]:.1%} | {j["batch_elapsed_mean_s"]:.1f} / {d["batch_elapsed_mean_s"]:.1f} 秒 | ${j["cost_per_1000_decisions_usd"]:.3f} / ${d["cost_per_1000_decisions_usd"]:.3f} |')
 return lines

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--check',action='store_true');args=ap.parse_args();folder=args.source or BASE
 summary=analyze(folder)
 if args.check:
  assert json.loads((BASE/'summary.json').read_text())==summary;print('Verified all 240 document runs, paired questions, scores, timing and fees.');return
 if args.source:
  for name in ['responses.jsonl','blocks.jsonl']:shutil.copyfile(folder/name,BASE/name)
 (BASE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 lines=['# 新材料：逐项与多项合并处理对照','','使用 20 篇未进入原主评测的临床试验摘要，每篇固定 10 个句子，判断其属于背景、目的、方法、结果还是结论。答案来自 PubMed 20k RCT 的原始标注，不由参评模型生成。共 200 个不同判断，每种配置完整测两轮。','',*table(summary),'','时间为两轮各自处理完整 20 篇摘要的实际经过时间的平均值，包含重试、排队和最终失败；每次同时处理 4 篇摘要，每篇内部依次完成其请求。正确率合并两轮的 400 次判断，重复测量不是新增样本。费用按全部判断计，包含收到用量的重试。','','## 两轮结果','','| 模型 | 每次判断数 | 第一轮总耗时 | 第二轮总耗时 | 第一轮正确率 | 第二轮正确率 | 最终缺失答案 | 重试次数 |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
 for r in summary['results']:
  for p,label in [('jev','Jev'),('deepseek','DeepSeek')]:
   s=r[p];lines.append(f'| {label} | {r["group_size"]} | {s["batch_elapsed_s"][0]:.2f} 秒 | {s["batch_elapsed_s"][1]:.2f} 秒 | {s["round_accuracy"][0]:.1%} | {s["round_accuracy"][1]:.1%} | {s["missing_answers"]} | {s["retry_attempts"]} |')
 lines+=['','## 缓存与费用','','| 模型 | 每次判断数 | 第一轮每千项费用 | 第二轮每千项费用 | 第一轮输入缓存命中 | 第二轮输入缓存命中 |','| --- | ---: | ---: | ---: | ---: | ---: |']
 for r in summary['results']:
  for p,label in [('jev','Jev'),('deepseek','DeepSeek')]:
   s=r[p];h=['—' if x is None else f'{x:.1%}' for x in s['round_cache_hit_fraction']];lines.append(f'| {label} | {r["group_size"]} | ${s["round_cost_usd"][0]*5:.4f} | ${s["round_cost_usd"][1]*5:.4f} | {h[0]} | {h[1]} |')
 lines+=['','DeepSeek 第二轮的缓存命中增加，10 项合并组的费用低于 Jev；两轮平均费用不代表所有缓存条件下的固定优势。']
 lines+=['','## 对照方法','','- 每种配置都读取相同完整摘要、回答相同十道问题。每次 1 项需调用 10 次；5 项需调用 2 次；10 项只调用 1 次。单项配置同样保留全文，衡量的是共享上下文工作流；它不代表仅发送孤立句子的最低费用。','- 固定 20 篇新材料及原始答案后才开始调用；排除原归档中的摘要 ID 和逐句文本重合。样本从测试集前 300 篇完整摘要中，筛选 10–24 句材料并按固定哈希顺序选择，不能代表全部医疗场景。','- 每家使用独立的持久连接池，HTTP/1.1，最多 4 个连接。连接超时 10 秒、读取超时 30 秒，失败最多补试一次；有效但错误的答案不重试。连接事件及请求全过程保留在响应记录中。','- 第一轮固定随机配置顺序，第二轮反向执行；同轮各配置的材料顺序一致。没有用不同组的旧材料来替代配对，也没有按得分挑选运行。','- Jev 使用 jev-1.13.0；DeepSeek 使用 deepseek-flash、关闭思考，只输出标签。两者业务判断目标一致，原生概率输出能力不同。','- 重复调用会受到服务端缓存影响，没有强行清除缓存或声称是冷缓存实验；DeepSeek 按本次空闲时段价格及实际缓存用量计费。成本与准确率均基于完整原始响应。','- 每篇内串行处理单项请求，同时处理 4 篇；这是固定并发下的工作流比较，不是单项请求任意并发后的极限吞吐测试。只进行两轮，服务波动仍可能影响时间差，失败不删去。','','## 数据与复核','','[原始数据来源](https://github.com/Franck-Dernoncourt/pubmed-rct) · [输入、问题及金标](inputs.jsonl) · [调用前固定的实验方案](protocol.json) · [每次真实响应](responses.jsonl) · [批次计时](blocks.jsonl) · [汇总](summary.json)','','[数据准备](../../../../scripts/prepare_paired_new.py) · [实际调用](../../../../scripts/run_paired_new.py) · [离线重算与核验](../../../../scripts/analyze_paired_new.py)','','摘要文本及标注沿用原数据来源的权利条件，仓库 MIT 许可不覆盖第三方原文。','']
 (BASE/'README.md').write_text('\n'.join(lines));print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
