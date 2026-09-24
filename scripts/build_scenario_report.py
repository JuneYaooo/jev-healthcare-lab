"""Build scene-level documentation from published snapshots, without API calls."""
import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- BEGIN GENERATED SCENARIOS -->'
END = '<!-- END GENERATED SCENARIOS -->'


def read(name):
    return json.loads((ROOT / 'results' / name).read_text())


def metric(task):
    q = task['quality']
    key = 'accuracy' if 'accuracy' in q else 'micro_f1'
    return ('Accuracy' if key == 'accuracy' else 'micro-F1'), f'{q[key]:.1%}'


def build():
    catalog = read('medical_catalog.json')
    tasks = read('all_results.json')['tasks']
    snapshot = read('snapshot.json')
    ablation = read('ablations.json')
    scenes = read('scenario_manifest.json')['scenes']
    by_id = {r['catalog_id']: r for r in catalog}
    ids = [i for s in scenes for i in s['resource_ids']]
    if Counter(ids) != Counter(by_id.keys()):
        raise ValueError('Every catalog resource must belong to exactly one scene')
    assigned = set()
    for s in scenes:
        s['resources'] = [by_id[i] for i in s['resource_ids']]
        s['tasks'] = []
        for r in s['resources']:
            for t in r['tested_tasks']:
                if t not in tasks:
                    raise ValueError(f'Unknown task: {t}')
                if t not in assigned:
                    s['tasks'].append(t)
                    assigned.add(t)
        if s['id'] == 'challenge':
            s['tasks'] = sorted(t for t in tasks if t.startswith('challenge_'))
            assigned.update(s['tasks'])
        s['rows'] = sum(tasks[t]['successful'] for t in s['tasks'])
        s['empty'] = sum(tasks[t]['deterministic_empty'] for t in s['tasks'])
    if assigned != set(tasks):
        raise ValueError(f'Unmapped tasks: {set(tasks) - assigned}')
    rows = sum(s['rows'] for s in scenes)
    empty = sum(s['empty'] for s in scenes)
    if rows + ablation['robustness']['rows'] != snapshot['evaluation_rows']:
        raise ValueError('Snapshot count mismatch')
    if empty != snapshot['deterministic_empty_rows']:
        raise ValueError('Empty prediction count mismatch')
    if rows - empty + ablation['robustness']['rows'] != snapshot['successful_api_responses']:
        raise ValueError('API count mismatch')

    def resource_names(t, prefix=''):
        rs = [r for r in catalog if t in r['tested_tasks']]
        return ' / '.join(f"[{r['resource']}]({prefix}docs/场景数据集与实验.md#resource-{r['catalog_id']})" for r in rs) or '自编挑战'

    lines = [START, '## 医疗场景与统计总览', '',
             f"快照日期 **{snapshot['date']}**，模型 **`{snapshot['model']}`**。以下覆盖仓库现有的全部医疗任务与资源清单；未测场景明确列出，不表示已经穷尽或验证所有医疗业务。", '',
             '| 统计项 | 数量与口径 |', '| --- | --- |',
             f'| 资源入口 | {len(catalog)} 项；含数据集、赛事、工具与重叠入口 |',
             f"| 有实测映射的资源 | {sum(bool(r['tested_tasks']) for r in catalog)} 项；不等于独立数据集数量 |",
             f"| 医疗任务条件 | {len(tasks)} 个：{sum(not t.startswith('challenge_') for t in tasks)} 个公开数据／材料适配 + {sum(t.startswith('challenge_') for t in tasks)} 类自编挑战 |",
             f'| 主评测 | {rows:,} 条，其中真实 API 响应 {rows-empty:,} 条，程序空预测 {empty} 条 |',
             f"| 配对鲁棒性 | {ablation['robustness']['rows']} 条额外调用，5 个任务 × 20 个原始案例 × 3 种扰动 |",
             f"| 总计 | {snapshot['evaluation_rows']:,} 条记录，{snapshot['successful_api_responses']:,} 条真实 API 响应；不是独立患者数 |", '',
             '**数据包含范围：**仓库包含数据集目录、适配与评分代码、聚合指标、样本身份／哈希和失败案例摘要。原始基准文本、prepared 请求与真实响应缓存未随仓库分发；需按数据来源自行取得，不能仅凭公开快照重新计分。', '',
             '完整的 [场景数据集与实验清单](docs/场景数据集与实验.md) 收录全部 90 项资源的来源、状态、任务映射与范围说明。', '',
             '| 医疗场景 | 资源入口 | 计数任务 | 评测记录 | API 响应 | 空预测 |', '| --- | ---: | ---: | ---: | ---: | ---: |']
    for s in scenes:
        lines.append(f"| [{s['title']}](#scene-{s['id']}) | {len(s['resources'])} | {len(s['tasks'])} | {s['rows']:,} | {s['rows']-s['empty']:,} | {s['empty']} |")
    lines += [f'| **主评测合计** | **{len(catalog)}** | **{len(tasks)}** | **{rows:,}** | **{rows-empty:,}** | **{empty}** |', '',
              '每个任务只归入一个场景；工具关联的相同任务不重复计数。鲁棒性额外 300 条在后文单列。Accuracy 和 micro-F1 不混算，不提供跨场景“总准确率”。', '', '## 分场景数据集与效果', '']
    for s in scenes:
        lines += [f'<a id="scene-{s["id"]}"></a>', '', f'### {s["title"]}', '', s['note'], '', '**主要结果：**' + s['headline'] + '。', '']
        if s['tasks']:
            lines += ['<details>', f'<summary>查看全部 {len(s["tasks"])} 个任务条件 · {s["rows"]:,} 条记录</summary>', '',
                      '| 数据集／资源 | 任务 ID | 样本记录 | 指标 | 结果 |', '| --- | --- | ---: | --- | ---: |']
            for t in s['tasks']:
                m, val = metric(tasks[t])
                lines.append(f'| {resource_names(t)} | `{t}` | {tasks[t]["successful"]} | {m} | {val} |')
            lines += ['', '</details>', '']
        else:
            lines += ['本场景没有额外计入的 Jev 评测记录。', '']
        pending = [r for r in s['resources'] if not r['tested_tasks']]
        if pending:
            lines += ['<details>', f'<summary>未测／待补齐：{len(pending)} 项资源</summary>', '']
            lines += [f"- [{r['resource']}](docs/场景数据集与实验.md#resource-{r['catalog_id']})：{r['status']}。" for r in pending]
            lines += ['', '</details>', '']
    lines += ['## 基线、消融与上下游实验', '',
              '以下实验复用主评测样本，除鲁棒性的 300 条额外请求外，不再累加记录数。', '',
              '| 实验 | 对照与结果 | 范围／证据 |', '| --- | --- | --- |',
              '| 中文实体抽取 | 词典 F1 42.6% → Jev 候选筛选 F1 59.5% | 100 条；[规则基线](results/offline_baselines.json) |',
              '| 术语归一化 | 简单别名规则 98% → Jev 93% | 100 条；此设置下规则更好；[规则基线](results/offline_baselines.json) |',
              '| 英文实体抽取 | medspaCy F1 58.9% → Jev 筛选 F1 69.4%；FP 467 → 155，FN 364 → 368 | 100 篇；[medspaCy 基线](results/medspacy_results.json)、[Jev 指标](results/all_results.json) |',
              '| 出院带药 | top-5 基线 F1 25.4% → Jev F1 48.6%；候选召回 67.4% | 100 条；[用药基线](results/ablations.json) |',
              '| BMI 参数 + 公式 | 首个候选正确参数对 14/20 → Jev 17/20；候选覆盖 18/20 | 20 病例，对应主表 40 个参数判断；[混合实验](results/ablations.json) |',
              '| MedHallu 证据消融 | 无证据 60% → 有证据 82% | 同 100 问题 × 真／幻觉回答 × 两条件，共 400 条；[结果](results/all_results.json) |',
              '| PUBHEALTH 证据消融 | 仅论断 20% → 提供核查文章 67% | 同 100 论断 × 两条件，共 200 条；文章可能直接包含结论；[结果](results/all_results.json) |',
              '| ASR 误差传播 | Whisper WER 32.2%；参考转写字段 12/12 → ASR 字段 11/12 | 457.92 秒扮演患者音频；[ASR 实验](results/asr_results.json) |',
              '| OCR 误差传播 | 参考文本类型 6/6 → OCR 文本类型 5/6 | Tesseract、六类失真、两种模板；[逐文档 OCR 指标](results/ocr_results.json) |', '',
              '### 配对鲁棒性：全部 15 组实验', '',
              '重复调用、轮换选项标签、加入无关说明各 100 条；预测分别改变 **1 / 8 / 3** 条。改变预测不必然意味着变差，所以下表同时报告正确数。', '',
              '| 原任务 | 扰动 | 记录数 | 预测改变 | 原条件正确数 | 扰动后正确数 |', '| --- | --- | ---: | ---: | ---: | ---: |']
    for key, v in ablation['robustness']['tasks'].items():
        task, variant = key.split(':')
        label = {'repeat':'重复调用','rotate':'选项标签轮换','irrelevant':'加入无关说明'}[variant]
        lines.append(f'| `{task}` | {label} | {v["n"]} | {v["changed_predictions"]} | {v["original_correct"]} | {v["correct"]} |')
    summary = read('all_results.json')['summary']
    lines += ['', '数据见 [ablations.json](results/ablations.json)；生成与评分见 [prepare_robustness.py](scripts/prepare_robustness.py)、[analyze_ablations.py](scripts/analyze_ablations.py)。', '',
              '### 延迟、用量与核验', '',
              f"主评测成功 API 响应的网络延迟 P50 **{summary['successful_api_latency_p50_s']:.3f} 秒**、P95 **{summary['successful_api_latency_p95_s']:.3f} 秒**；输入 token **{summary['input_tokens_successful_only']:,}**。鲁棒性另记录输入 token **{ablation['robustness']['input_tokens']:,}**。这些只覆盖留存成功响应，不是完整账单或纯模型推理时间。", '',
              '全部任务的置信区间与逐类指标见 [结果总表](docs/结果总表.md) 和 [all_results.json](results/all_results.json)；错误示例见 [error_cases.json](results/error_cases.json)。EvidenceBench 的 37 条请求哈希格式修正见 [审计记录](results/hash_normalization_audit.json)，响应未改变。', '',
              '这些是有限样本、适配任务的探索性结果，不是官方排行榜成绩。闭源模型训练暴露情况未知；多个条件或字段可能来自同一病例。单组和少组 bootstrap 区间不能代表人群泛化，也未证明医院工时节约或临床收益。', END]

    docs = ['# 场景数据集与实验清单', '',
            '由 `python3 scripts/build_scenario_report.py` 从资源目录、场景映射和已发布结果生成。', '',
            '收录全部 90 个资源入口和 96 个主评测任务条件；39 个入口有实测映射。资源数不等于独立数据集数，任务数不等于患者数。', '',
            '## 数据文件与复现入口', '',
            '| 内容 | 位置 |', '| --- | --- |',
            '| 场景划分 | [scenario_manifest.json](../results/scenario_manifest.json) |',
            '| 数据集来源、适配目的与状态 | [medical_catalog.json](../results/medical_catalog.json) |',
            '| 主评测指标、置信区间、校准和延迟 | [all_results.json](../results/all_results.json) |',
            '| 样本身份与请求哈希（包含配对扰动） | [evaluation_index.jsonl](../results/evaluation_index.jsonl) |',
            '| 基线与消融 | [offline_baselines.json](../results/offline_baselines.json)、[medspacy_results.json](../results/medspacy_results.json)、[ablations.json](../results/ablations.json) |',
            '| 原始数据、prepared 请求和响应缓存 | 未分发；取得数据后在本地生成，见 [复现说明](REPRODUCING.md) |', '',
            '不能用索引和哈希还原原始样本。现有下载器只覆盖部分来源；全部历史任务尚不具备从空目录一键重建的条件。', '',
            '## 实验代码入口', '',
            '| 环节 | 代码 |', '| --- | --- |',
            '| 数据下载与首轮适配 | [download_sources.py](../scripts/download_sources.py)、[benchmark.py](../scripts/benchmark.py) |',
            '| 批量调用与逐任务评分 | [live_batch.py](../scripts/live_batch.py)、[analyze_results.py](../scripts/analyze_results.py) |',
            '| 基线／消融评分 | [analyze_ablations.py](../scripts/analyze_ablations.py) |',
            '| ASR／OCR 上游 | [run_asr.py](../scripts/run_asr.py)、[run_ocr.py](../scripts/run_ocr.py) |', '',
            '其余适配器（输入路径、抽样规则与金标字段以代码为准）：', '']
    docs += [f'- [{p.name}](../scripts/{p.name})' for p in sorted((ROOT/'scripts').glob('prepare_*.py'))]
    for s in scenes:
        docs += ['', f'## {s["title"]}', '', s['note'], '']
        for r in s['resources']:
            docs += [f'<a id="resource-{r["catalog_id"]}"></a>', '', f'### {r["catalog_id"]}. {r["resource"]}', '',
                     f"- 原始入口：[{r['resource']}]({r['source']})", f"- 场景与 Jev 职责：{r['scenario']}；{r['jev_role']}。",
                     f"- 状态：**{r['status']}**。", f"- 本轮范围／阻塞：{r['completion_note']}。"]
            if r['tested_tasks']:
                docs += ['', '| 任务 | 记录 | 指标 | 结果 |', '| --- | ---: | --- | ---: |']
                for t in r['tested_tasks']:
                    m,v = metric(tasks[t])
                    docs.append(f'| `{t}` | {tasks[t]["successful"]} | {m} | {v} |')
            else:
                docs += ['- 实测结果：未运行，无可报告的 Jev 指标。']
            docs.append('')
        if s['id'] == 'challenge':
            docs += ['| 挑战任务 | 记录 | 指标 | 结果 |', '| --- | ---: | --- | ---: |']
            for t in s['tasks']:
                m,v=metric(tasks[t]); docs.append(f'| `{t}` | {tasks[t]["successful"]} | {m} | {v} |')
    docs += ['', '## 尚未覆盖的验证', '',
             '受限数据获取、无金标任务、下载故障、未适配任务与非原生输入分别保留状态。DDXPlus 全量数据、Verified 其余计算器、替代框架对照、真实医院工时和人工复核成本实验均未完成。上述范围不能由现有选择题、合成挑战或有限样本成绩替代。', '']
    return '\n'.join(lines), '\n'.join(docs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check generated files without writing')
    args = parser.parse_args()
    section, catalog = build()
    readme = ROOT / 'README.md'
    content = readme.read_text()
    before, rest = content.split(START, 1)
    _, after = rest.split(END, 1)
    outputs = {readme: before + section + after,
               ROOT / 'docs/场景数据集与实验.md': catalog}
    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, text in outputs.items() if not p.exists() or p.read_text() != text]
        if stale:
            raise SystemExit('Outdated generated documentation: ' + ', '.join(stale))
        print('Scene documentation is current; all resources, tasks and row totals reconcile.')
    else:
        for path, text in outputs.items():
            path.write_text(text)
        print('Updated README scenario section and full dataset/experiment catalog.')


if __name__ == '__main__':
    main()
