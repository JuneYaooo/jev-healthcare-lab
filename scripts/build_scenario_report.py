"""Generate statistical README pages from the archived, real Jev experiments."""
import argparse
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT/path).read_text())


def lines(path):
    return [json.loads(x) for x in path.read_text().splitlines()]


def metric(result):
    q = result['quality']
    key = 'accuracy' if 'accuracy' in q else 'micro_f1'
    return ('Accuracy' if key == 'accuracy' else 'micro-F1'), f'{q[key]:.1%}'


def scoring(row):
    task = row['task']
    mode = row['metadata'].get('scoring')
    if mode == 'multi_label_vocabulary' or task == 'medjourney_departments':
        return '将每个 NOUL ≥ 0.5 的问题编号映射到 metadata.label_vocabulary，得到预测标签集合。与 gold 完整标签集合比较；候选外金标仍计为 FN。汇总 TP、FP、FN，micro-F1 = 2TP / (2TP + FP + FN)。'
    if task == 'imcs_ner_dictionary_pipeline':
        return '逐候选读取 Choice；去除 none 后，将候选起止位置与预测类型组合成 (start,end,type) 集合。严格匹配全部 gold 跨度，汇总 TP、FP、FN 计算 micro-F1。无候选的 43 条记录输出空集，未调用 API；金标仍计入 FN。'
    if mode == 'multi_question_keys' or task == 'nli4ct_evidence':
        return '选择 NOUL ≥ 0.5 的问题键形成预测集合，和 gold 集合严格比较。跨样本汇总 TP、FP、FN，micro-F1 = 2TP / (2TP + FP + FN)；不对每行 F1 简单平均。'
    return '读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。'


def task_doc(scene, task, method, result):
    folder = ROOT/'scenarios'/scene['id']/task
    rows = lines(folder/'samples.jsonl')
    provenance = load(str((folder/'provenance.json').relative_to(ROOT)))
    prompts = load(str((folder/'prompts.json').relative_to(ROOT)))['variants']
    m, v = metric(result)
    groups = len({r['group'] for r in rows})
    qtypes = Counter(q['type'] for r in rows for q in r['request']['questions'].values())
    labels = Counter(str(r['gold']) for r in rows) if 'accuracy' in result['quality'] else None
    out = [f'# {method["title"]}', '', f'任务 ID：`{task}` · 场景：[ {scene["title"]} ](../README.md)', '',
           '| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |', '| ---: | ---: | ---: | ---: | --- | ---: |',
           f'| {len(rows)} | {groups} | {len(rows)-result["deterministic_empty"]} | {result["deterministic_empty"]} | {m} | **{v}** |', '',
           '## Jev 如何评测', '', method['method'], '',
           f'实际模型为 `jev-1.13.0`，历史实验日期为 2026-09-24。{groups} 个 group 是数据源分组标识，不能直接当作独立患者数。', '',
           '请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。', '',
           '### 输入与问题结构', '']
    shapes = sorted({', '.join(r['request']['state'].keys()) if isinstance(r['request']['state'],dict) else '完整文本字符串' for r in rows})
    out += ['- 输入字段：' + '；'.join('`'+x+'`' for x in shapes) + '。',
            '- 问题类型与总数：' + '，'.join(f'`{k}` {n} 个' for k,n in sorted(qtypes.items())) + '。',
            f'- 去重后的完整问题对象：{len(prompts)} 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。', '',
            '### 实际提示词', '',
            '以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。', '']
    if prompts:
        out += ['```json', json.dumps(prompts[0]['question'],ensure_ascii=False,indent=2), '```', '']
    out += ['### 金标与计分', '', scoring(rows[0]), '']
    notes = sorted({str(r['metadata'][k]) for r in rows for k in ('source','scope','oracle','note') if k in r['metadata']})
    if labels:
        out += ['金标分布：'+'，'.join(f'`{k}`：{n}' for k,n in sorted(labels.items()))+'。', '']
    out += ['## 数据与实验记录', '',
            '| 文件 | 内容 |', '| --- | --- |',
            '| [samples.jsonl](samples.jsonl) | 本任务全部真实评测输入、完整请求、gold、group、适配元数据及请求哈希 |',
            '| [responses.jsonl](responses.jsonl) | 对应的原始成功响应记录；空候选时保留程序输出标记 |',
            '| [prompts.json](prompts.json) | 从真实请求提取的全部问题／提示词／选项变体 |',
            '| [example.json](example.json) | 一条完整实际样本与其对应响应，无合成替换 |',
            '| [results.json](results.json) | 指标、置信区间、逐类表现、校准、token 与延迟 |',
            '| [index.jsonl](index.jsonl) | 样本身份、请求哈希和响应原文件哈希 |',
            '| [provenance.json](provenance.json) | 来源、归档文件哈希与原准备分片 |', '',
            '通过 `(task, id)` 关联输入、响应与索引；响应哈希针对 JSONL 每行去掉换行分隔符后的原始字节计算。', '',
            f'数据适配：[ {method["adapter"]} ](../../../scripts/{method["adapter"]})；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。', '',
            '## 来源与实验范围', '']
    if provenance['resources']:
        out += [f"- [{r['resource']}]({r['source']})：{r['completion_note']}。" for r in provenance['resources']]
    else:
        out += ['- 原实验自行编写的挑战案例，完整题面、选项与人工金标已在本目录保留。']
    if notes:
        out += ['', '原始适配元数据：', ''] + ['- '+x for x in notes]
    out += ['', '原准备分片：'+ '、'.join('`'+x+'`' for x in provenance['prepared_shards'])+'。', '']
    attachments = [('baseline.json','规则／候选基线'),('hybrid.json','BMI 参数选择与程序公式联合实验'),('source_verification.json','源数据版本与字节校验'),('hash_audit.json','历史哈希格式修正'),('upstream/manifest.json','实际上游音频／图像／转写文件及哈希'),('upstream/results.json','OCR／ASR 上游指标')]
    present=[(name,label) for name,label in attachments if (folder/name).exists()]
    if present:
        out += ['## 关联实验', '']+[f'- [{label}]({name})' for name,label in present]+['']
    if task=='bmi_height_selection':out += ['配对实验：[身高 + 体重 + BMI 公式](../bmi_weight_selection/hybrid.json)。', '']
    if task=='primock_reference_fields':out += ['配对实验与原音频：[ASR 条件](../primock_asr_fields/README.md)。', '']
    if task=='clinocr_reference_doctype':out += ['配对实验与原始扫描图：[OCR 条件](../clinocr_ocr_doctype/README.md)。', '']
    if (folder/'robustness').exists():
        out += ['## 配对鲁棒性实验', '', '| 变体 | 样本数 | 预测改变 | 原条件正确 | 扰动后正确 |','| --- | ---: | ---: | ---: | ---: |']
        for variant, title in [('repeat','重复调用'),('rotate','选项标签轮换'),('irrelevant','无关说明')]:
            res=load(str((folder/'robustness'/variant/'results.json').relative_to(ROOT)))
            out += [f'| [{title}](robustness/{variant}/README.md) | {res["n"]} | {res["changed_predictions"]} | {res["original_correct"]} | {res["correct"]} |']
        out.append('')
    return '\n'.join(out)


def build():
    scenes=load('results/scenario_manifest.json')['scenes']
    methods=load('results/task_methods.json')
    tasks=load('results/all_results.json')['tasks']
    snapshot=load('results/snapshot.json')
    catalog=load('results/medical_catalog.json')
    assigned=[t for s in scenes for t in s['task_ids']]
    if len(assigned)!=len(set(assigned)) or set(assigned)!=set(tasks):raise ValueError('Task coverage mismatch')
    if set(methods)!=set(tasks):raise ValueError('Task methodology coverage mismatch')
    outputs={}
    intro=['# Jev 医疗场景评测统计', '',
           f'**{len(scenes)} 类医疗场景 · {len(tasks)} 个主评测任务条件 · {snapshot["evaluation_rows"]:,} 条计分记录**', '',
           '主评测包含 **72 个公开数据／材料适配任务 + 24 个自编边界挑战任务**，共 **6,586 条记录**；另有 **15 组配对扰动实验、300 条额外记录**。其中 **6,843 条有真实 API 响应，43 条无实体候选由程序输出空预测**。', '',
           '每个任务均有独立实验目录，保留实际测试输入、金标、完整提示词、模型响应、评分结果和方法说明。测试记录包含同一病例的多个字段或条件，不是独立患者数；Accuracy 与 micro-F1 分别列示，不混算总体准确率。', '',
           '## 场景覆盖', '', '| 医疗场景 | 数据适配任务 | 自编挑战任务 | 主评测记录 | 额外扰动记录 |', '| --- | ---: | ---: | ---: | ---: |']
    robust=load('results/ablations.json')['robustness']['tasks']
    for s in scenes:
        ts=s['task_ids'];n=sum(tasks[t]['successful'] for t in ts)
        pert=sum(v['n'] for k,v in robust.items() if k.split(':')[0] in ts)
        intro.append(f'| [{s["title"]}](scenarios/{s["id"]}/README.md) | {sum(not t.startswith("challenge_") for t in ts)} | {sum(t.startswith("challenge_") for t in ts)} | {n:,} | {pert} |')
    intro += ['| **合计** | **72** | **24** | **6,586** | **300** |', '',
              '“覆盖”仅指下列已测文本任务与适配链路。例如语音／OCR 场景已测转写后的字段与文档类型，不能理解为已完成医学影像识别或 ECG 诊断。', '',
              '## 各场景任务与结果', '']
    for s in scenes:
        ts=s['task_ids'];n=sum(tasks[t]['successful'] for t in ts)
        table=['| 任务（点击查看完整方法与数据） | 类型 | 记录数 | 指标 | 结果 |', '| --- | --- | ---: | --- | ---: |']
        scene_table=list(table)
        intro += [f'### {s["title"]}', '', s['note'], '', '**主要结果：**'+s['headline']+'。', '']
        for t in ts:
            m,v=metric(tasks[t]);kind='自编挑战' if t.startswith('challenge_') else '数据适配'
            label=methods[t]['title']
            table.append(f'| [{label}](scenarios/{s["id"]}/{t}/README.md) | {kind} | {tasks[t]["successful"]} | {m} | {v} |')
            scene_table.append(f'| [{label}]({t}/README.md) | {kind} | {tasks[t]["successful"]} | {m} | {v} |')
            outputs[ROOT/'scenarios'/s['id']/t/'README.md']=task_doc(s,t,methods[t],tasks[t])
            folder=ROOT/'scenarios'/s['id']/t
            for var,title in [('repeat','重复调用'),('rotate','选项标签轮换'),('irrelevant','无关说明')]:
                if not (folder/'robustness'/var).exists():continue
                result=load(str((folder/'robustness'/var/'results.json').relative_to(ROOT)))
                body=[f'# {methods[t]["title"]}：{title}', '', f'配对主任务：[原实验](../../README.md)。固定抽取 20 个原始案例，金标与原样本身份可由 metadata.original_task / original_id 关联。', '',
                      {'repeat':'保持输入与选项不变，额外调用一次，比较预测稳定性。','rotate':'轮换选项键并同步转换金标；比较预测变化时通过 metadata.inverse_labels 还原到原标签。','irrelevant':'在临床输入外添加与病例无关的行政说明，其余条件保持一致。'}[var], '',
                      f'记录数 **{result["n"]}**；预测改变 **{result["changed_predictions"]}**；原条件正确 **{result["original_correct"]}**；扰动后正确 **{result["correct"]}**。', '',
                      '[真实样本与金标](samples.jsonl) · [实际响应](responses.jsonl) · [完整提示词](prompts.json) · [完整示例](example.json) · [结果](results.json) · [来源与哈希](provenance.json)', '',
                      '比较预测变化时恢复标签，判断扰动样本正确性时使用该样本自身的 gold；不能把 300 条扰动当作新增独立患者。', '']
                outputs[folder/'robustness'/var/'README.md']='\n'.join(body)
        intro += table+['']
        scene_doc=[f'# {s["title"]}', '', f'**{len(ts)} 个任务条件，{n:,} 条主评测记录。** [全部场景](../../README.md)', '',s['note'],'']+scene_table+['']
        outputs[ROOT/'scenarios'/s['id']/'README.md']='\n'.join(scene_doc)
    intro += ['## 基线与配对实验', '',
              '| 实验 | 对照结果 | 详细实验 |', '| --- | --- | --- |',
              '| 中文实体抽取 | 词典 micro-F1 42.6% → Jev 59.5% | [输入、响应与基线](scenarios/records/imcs_ner_dictionary_pipeline/README.md) |',
              '| 中文术语归一化 | 规则 Accuracy 98% → Jev 93% | [输入、响应与基线](scenarios/records/imcs_normalization_top20/README.md) |',
              '| 英文实体抽取 | medspaCy micro-F1 58.9% → Jev 69.4% | [候选与基线](scenarios/records/ncbi_medspacy_jev_ner/README.md) |',
              '| 出院带药 | top-5 micro-F1 25.4% → Jev 48.6% | [候选与基线](scenarios/medication/cdrugred_discharge_candidate_pipeline/README.md) |',
              '| BMI 参数 + 公式 | 首个候选正确参数对 14/20 → Jev 17/20 | [逐病例联合结果](scenarios/calculators/bmi_weight_selection/hybrid.json) |',
              '| MedHallu 证据消融 | 无证据 Accuracy 60% → 有证据 82% | [有证据](scenarios/quality/medhallu_with_evidence/README.md) / [无证据](scenarios/quality/medhallu_without_evidence/README.md) |',
              '| PUBHEALTH 证据消融 | 仅论断 Accuracy 20% → 提供核查文章 67% | [仅论断](scenarios/evidence/pubhealth_claim_only/README.md) / [核查文章](scenarios/evidence/pubhealth_with_article/README.md) |',
              '| ASR 误差传播 | Whisper WER 32.2%；参考字段 12/12 → ASR 字段 11/12 | [音频、转写与 Jev 实验](scenarios/multimodal/primock_asr_fields/README.md) |',
              '| OCR 误差传播 | 参考文档类型 6/6 → OCR 文本类型 5/6 | [扫描图、识别文本与 Jev 实验](scenarios/multimodal/clinocr_ocr_doctype/README.md) |', '',
              '以上基线和配对条件已包含于主评测及关联统计，不再次累计样本。', '',
              '## 鲁棒性实验', '', '| 主任务 | 扰动 | 记录数 | 预测改变 | 原条件正确 | 扰动后正确 |', '| --- | --- | ---: | ---: | ---: | ---: |']
    owner={t:s['id'] for s in scenes for t in s['task_ids']}
    for key,v in robust.items():
        t,var=key.split(':');label={'repeat':'重复调用','rotate':'标签轮换','irrelevant':'无关说明'}[var]
        intro.append(f'| [{methods[t]["title"]}](scenarios/{owner[t]}/{t}/robustness/{var}/README.md) | {label} | {v["n"]} | {v["changed_predictions"]} | {v["original_correct"]} | {v["correct"]} |')
    intro += ['', '## 尚未完成的覆盖', '',
              f'另有 [90 项资源的调研与阻塞清单](docs/覆盖与阻塞账本.md)，其中 {sum(bool(r["tested_tasks"]) for r in catalog)} 项入口映射到已有实验；包含同一数据集的重叠入口和工具，不能称为 90 个已测数据集。受限数据、缺失金标、完整医学影像／ECG、其余临床计算器和真实医院流程验证未计入上述已测覆盖。', '']
    outputs[ROOT/'README.md']='\n'.join(intro)
    outputs[ROOT/'docs/场景数据集与实验.md']='\n'.join(['# 场景数据集与实验索引','','所有实际实验均按场景和任务归档：','']+[f'- [{s["title"]}](../scenarios/{s["id"]}/README.md)：{len(s["task_ids"])} 个任务。' for s in scenes]+['','[全部资源来源与未完成项](覆盖与阻塞账本.md) · [资源元数据](../results/medical_catalog.json) · [总指标](../results/all_results.json) · [归档核验统计](../results/archive_summary.json)',''])
    return outputs


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    outputs=build()
    if args.check:
        stale=[str(p.relative_to(ROOT)) for p,text in outputs.items() if not p.exists() or p.read_text()!=text]
        if stale:raise SystemExit('Outdated generated pages: '+', '.join(stale))
        print(f'All {len(outputs)} statistical and task-method pages are current.')
    else:
        for p,text in outputs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
        print(f'Generated {len(outputs)} statistical and task-method pages.')


if __name__=='__main__':main()
