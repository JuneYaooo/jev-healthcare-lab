"""Render reader-facing task/source cards from the committed benchmark records.

No network, model calls, new examples, or modifications to benchmark data.
Run with --check to detect outdated cards without writing files.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import medical_decision_dataset as data

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "benchmarks/medical_decision_v1"
DATA_LINK = "../../benchmarks/medical_decision_v1"
STAGES = {
    "material_judgment": "材料判断",
    "clinical_choice": "临床候选方案选择",
    "outcome_prediction": "结局预测",
    "clinical_action": "临床行动选择",
    "risk_classification": "风险分类",
}
DISTRIBUTIONS = {
    "open": "开放许可部分",
    "research_noncommercial": "非商业研究附加集",
    "reference_only": "仅作参考，未收录题目",
}
LANGUAGES = {"zh": "中文", "en": "英语", "es": "西班牙语"}
SCOPES = {"clinical": "临床主评测", "auxiliary": "辅助评测（不计临床主分数）", "suspended": "暂停使用（不导出、不评分）"}
CATEGORIES = {"support": "临床计算、解读与证据", "risk": "风险、结局与历史去向预测", "workflow": "流程与记录核对", "text": "文本理解与标注"}


def read_json(path):
    return json.loads(path.read_text())


def inline(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def prose(value):
    # Project release labels are not part of the user-facing catalog.
    return re.sub(r"\bv0\.\d+\.\d+\s*", "", str(value)).strip()


def link(title, target):
    return f"[{inline(title)}]({target})"


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(map(inline, row)) + " |" for row in rows)
    return "\n".join(lines)


def block(value, *, compact=False):
    body = json.dumps(value, ensure_ascii=False, indent=None if compact else 2)
    runs = re.findall(r"`+", body)
    fence = "`" * max(3, max(map(len, runs), default=0) + 1)
    return f"{fence}json\n{body}\n{fence}"


def counts_text(counts, names=None):
    names = names or {}
    return "、".join(f"{names.get(key, key)} {count} 题" for key, count in sorted(counts.items()))


def example(rows):
    return min(rows, key=lambda row: (len(json.dumps(row["request"], ensure_ascii=False)), row["id"]))


def example_sections(row):
    p = row["provenance"]
    request = row["request"]
    criteria = request["questions"]["decision"]["criteria"]
    assert row["gold"] in criteria
    parts = [
        "## 收录样例",
        "以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。",
        f"题目 ID：`{row['id']}`；语种：{LANGUAGES.get(row['language'], row['language'])}；来源组：`{row['group_id']}`。",
        "### 模型输入",
        "只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。",
        block(request),
        "### 标准答案与预测格式",
        f"原始标注映射后的正确选项键为 `{row['gold']}`，对应选项：",
        block(criteria[row["gold"]]),
        "评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：",
        block({"id": row["id"], "choice": row["gold"]}, compact=True),
        "### 样例溯源",
        f"[上游资源]({p['resource_url']}) · [数据集说明](../datasets/{p['source_id']}.md)",
        "以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：",
        block(p),
    ]
    adaptation = row.get("metadata", {}).get("adaptation")
    if adaptation:
        parts.extend(["该题的格式转换说明：", prose(adaptation)])
    return parts


def render():
    taxonomy = read_json(DATA / "taxonomy.json")
    tasks = {t["id"]: t for t in taxonomy["tasks"]}
    reports = {t["id"]: t for t in read_json(DATA / "summary.json")["tasks"]}
    sources = {s["id"]: s for s in read_json(DATA / "sources.json")["sources"]}
    scenes = {s["id"]: s for s in taxonomy["scenarios"]}
    dimensions = {d["id"]: d["title"] for d in taxonomy["dimensions"]}
    policy = data.evaluation_policy(DATA)
    inventory = data.evaluation_inventory(DATA)
    rules = policy["tasks"]
    for tid, task in tasks.items():
        task["title"] = rules[tid]["title"]
    by_task, by_source = defaultdict(list), defaultdict(list)
    for line in (DATA / "samples.jsonl").read_text().splitlines():
        row = json.loads(line)
        by_task[row["task"]].append(row)
        by_source[row["provenance"]["source_id"]].append(row)
    assert set(by_task) <= tasks.keys()
    assert set(by_source) <= sources.keys()
    output = {}

    def source_link(sid):
        return link(sources[sid]["name"], f"../datasets/{sid}.md")

    def task_link(tid):
        return link(tasks[tid]["title"], f"../tasks/{tid}.md")

    for tid, task in tasks.items():
        rows, report = by_task[tid], reports[tid]
        rule = rules[tid]
        source_counts = Counter(r["provenance"]["source_id"] for r in rows)
        assert len(rows) == report["count"]
        assert dict(source_counts) == report["source_counts"]
        parts = [
            f"# {task['title']}",
            "[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)",
            f"**当前用途：{SCOPES[rule['scope']]}。** {rule['notes']}",
            "## 任务是什么",
            task["definition"],
            table(["项目", "说明"], [
                ["任务 ID", f"`{tid}`"],
                ["医疗场景", scenes[task["primary_scenario"]]["title"]],
                ["能力维度", "、".join(dimensions[d] for d in task["ability_tags"])],
                ["评测类别", "临床判断与行动" if rule["scope"] == "clinical" else CATEGORIES[rule["category"]]],
                ["当前题数 / 目标题数", f"{len(rows)} / {task['target_count']}"],
                ["来源组数", str(len({r["group_id"] for r in rows}))],
                ["语种", counts_text(Counter(r["language"] for r in rows), LANGUAGES) or "待补"],
                ["数据范围", counts_text(Counter(r["provenance"]["distribution"] for r in rows), DISTRIBUTIONS) or "待补"],
            ]),
            "## 数据集来源",
        ]
        if rows:
            parts.append(table(["数据集说明", "收录题数", "上游入口"], [
                [source_link(sid), str(n), link("原始来源", sources[sid]["url"])]
                for sid, n in sorted(source_counts.items())
            ]))
            parts.extend([
                "## 如何作答与评分",
                "根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。" + ("固定语义标签计算准确率、宏 F1、召回与混淆矩阵。" if rule["label_semantics"] == "fixed" else "按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。"),
                "暂停任务仅保留来源与构造示例，不导出、不评分。" if rule["scope"] == "suspended" else "合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。",
                "后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。",
            ])
            parts.extend(example_sections(example(rows)))
            parts.extend([
                "## 覆盖与使用边界",
                "题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。",
                f"当前标准标签分布：{counts_text(Counter(r['gold'] for r in rows))}。",
            ])
            if len(rows) < task["target_count"]:
                parts.append("当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。")
            for sid in sorted(source_counts):
                source = sources[sid]
                parts.append(f"**{source_link(sid)}**：{prose(source['authenticity'])} 答案依据：{prose(source['gold_provenance'])}")
                if source.get("evaluation_limits"):
                    parts.append(prose(source["evaluation_limits"]))
            historical = sum(r["exposure"]["historical_material_signature_match"] for r in rows)
            if historical:
                parts.append(f"其中 {historical} 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。")
        else:
            parts.extend([
                "当前没有收录题目，不参与评分。",
                "## 样例与缺口",
                "**样例待补。** 尚无符合此任务定义的可用题目，不提供虚构输入、选项或答案。",
                prose(task.get("missing_reason") or "尚无可用于本任务的已核验数据。"),
            ])
        candidates = sorted((set(task.get("source_ids", [])) | set(task.get("candidate_source_ids", []))) - set(source_counts))
        if candidates:
            parts.extend([
                "## 调研过的其他来源",
                "这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。",
                table(["来源说明", "登记情况"], [
                    [source_link(sid), prose(sources[sid].get("reason") or "本任务暂无收录，是否适用需按任务定义核验。")]
                    for sid in candidates
                ]),
            ])
        parts.extend([
            "## 数据文件",
            f"[本任务全部记录]({DATA_LINK}/tasks/{tid}/samples.jsonl) · [任务定义与统计]({DATA_LINK}/tasks/{tid}/task.json) · [格式与使用方法](../REPRODUCING.md)",
            "[返回首页](../../README.md)",
        ])
        if rule["family"] != tid:
            parts.insert(3, f"本页为来源子集，统一并入 [{rule['family_title']}]({rule['family']}.md) 计分，不另增加任务权重。")
        output[ROOT / f"docs/tasks/{tid}.md"] = "\n\n".join(parts) + "\n"

    for sid, source in sources.items():
        rows = by_source[sid]
        task_counts = Counter(r["task"] for r in rows)
        related = [tid for tid, task in tasks.items() if sid in task.get("source_ids", []) + task.get("candidate_source_ids", []) and tid not in task_counts]
        parts = [
            f"# {source['name']}",
            "[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)",
            "## 这是什么数据",
            prose(source.get("authenticity") or source.get("reason") or "尚未收录题目，材料性质待核验。"),
            table(["项目", "说明"], [
                ["来源 ID", f"`{sid}`"],
                ["上游入口", link("发布方页面", source["url"])],
                ["收录情况", f"{len(rows)} 题 / {len(task_counts)} 个任务" if rows else "0 题；仅作参考"],
                ["评测用途", counts_text(Counter(rules[r["task"]]["scope"] for r in rows), SCOPES) or "仅作参考"],
                ["使用范围", DISTRIBUTIONS[source["distribution"]]],
                ["登记的数据许可", source.get("data_license", "未确认；不据此再分发数据")],
                ["收录语种", counts_text(Counter(r["language"] for r in rows), LANGUAGES) or "无收录题目"],
            ]),
            "## 来源与引用",
        ]
        if source.get("attribution"):
            parts.append(prose(source["attribution"]))
        urls = [("论文或项目引用", source.get("citation_url")), ("数据许可", source.get("license_url")), ("补充核验依据", source.get("evidence_url"))]
        parts.append(" · ".join(link(title, url) for title, url in urls if url) or f"已登记入口：[上游页面]({source['url']})。独立论文引用与数据许可未完整登记。")
        snapshots = source.get("license_evidence", [])
        if snapshots:
            parts.append("许可与说明快照：" + " · ".join(link(Path(path).name, f"{DATA_LINK}/{path}") for path in snapshots))
        if source.get("reason"):
            parts.extend(["### 登记边界", prose(source["reason"])])
        if source.get("evaluation_limits"):
            parts.extend(["### 使用限制", prose(source["evaluation_limits"])])
        parts.append("## 用于哪些任务")
        if rows:
            parts.append(table(["任务或来源子集", "用途", "此来源贡献题数", "评测内容"], [
                [task_link(tid), SCOPES[rules[tid]["scope"]], str(n), tasks[tid]["definition"]]
                for tid, n in sorted(task_counts.items())
            ]))
            parts.extend([
                "## 答案与格式转换",
                prose(source["gold_provenance"]),
                "这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。",
            ])
            parts.extend(example_sections(example(rows)))
            parts.append(f"更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：{task_link(example(rows)['task'])}。")
        else:
            parts.extend([
                "当前没有使用该来源的评测任务。",
                "## 样例数据",
                "**样例留空。** 当前未收录可用于本评测集的题目，仅保留来源与调研信息；不复制许可未闭合或需受控访问的原文。",
            ])
        if related:
            parts.extend([
                "## 相关任务调研",
                "以下为曾考虑使用此来源的任务，不代表已采用：",
                table(["任务说明", "任务内容"], [[task_link(tid), tasks[tid]["definition"]] for tid in related]),
            ])
        parts.extend([
            "## 追溯与使用",
            f"来源元数据保存在 [来源登记文件]({DATA_LINK}/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件]({DATA_LINK}/sources.lock.json)。原始数据各自的许可独立适用。",
            "[返回首页](../../README.md)",
        ])
        output[ROOT / f"docs/datasets/{sid}.md"] = "\n\n".join(parts) + "\n"

    clinical = inventory['clinical']
    families = clinical['families']
    status_names = {'empty': '待补', 'exploratory': '探索性', 'summary_eligible': '可参与汇总'}
    parts = ['# 临床主评测任务', '[返回首页](../../README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)',
             f"共 {clinical['defined_families']} 个任务定义、{clinical['populated_families']} 个有题任务，{clinical['records']:,} 题。病例诊断的两个来源子集合并计分；小样本任务保留逐项结果，不进入汇总。状态按完整临床范围展示，实际评分按本次许可子集重新计算题数门槛。"]
    for scene_id, scene in scenes.items():
        parts.extend([f"## {scene['title']}", table(['任务说明', '能力维度', '题数', '状态'], [
            [link(f['title'], f"{f['id']}.md"), '、'.join(dimensions[d] for d in f['ability_tags']), f['records'], status_names[f['status']]]
            for f in families if f['scenario'] == scene_id])])
    output[ROOT / 'docs/tasks/README.md'] = '\n\n'.join(parts) + '\n'
    parts = ['# 辅助与暂停任务', '[返回首页](../../README.md) · [临床主评测任务](README.md)',
             '这些任务不计入临床主分数。辅助任务可通过 --scope auxiliary 单独导出和评分；暂停任务仅保留追溯材料。']
    for category, title in CATEGORIES.items():
        parts.extend([f'## {title}', table(['任务说明', '题数', '当前用途'], [
            [task_link(tid), len(by_task[tid]), rules[tid]['notes']] for tid in tasks
            if rules[tid]['scope'] == 'auxiliary' and rules[tid]['category'] == category])])
    parts.extend(['## 暂停使用', table(['任务说明', '底稿题数', '原因'], [
        [task_link(tid), len(by_task[tid]), rules[tid]['notes']] for tid in tasks if rules[tid]['scope'] == 'suspended'])])
    output[ROOT / 'docs/tasks/AUXILIARY.md'] = '\n\n'.join(parts) + '\n'
    diagnosis = next(f for f in families if f['id'] == 'diagnosis')
    parts = ['# 病例诊断选择', '[返回首页](../../README.md) · [临床主评测任务](README.md)',
             '根据给定病例资料，从候选中选择诊断。考试病例与模拟病例作为同一个评测任务的来源子集；题目和原答案保留，不因拆分来源重复增加任务权重。',
             f"共 {diagnosis['records']} 题。合并后按全部题目计算任务准确率，并保留每个来源子集的结果。选项含义随题变化，不计算临床类别 F1。",
             table(['来源子集与完整样例', '题数'], [[task_link(tid), len(by_task[tid])] for tid in diagnosis['task_ids']]),
             '## 样例与来源', '两个来源子集的说明页分别给出完整输入、原选项、标准答案和溯源。以下为考试病例子集中的一题：']
    parts.extend(example_sections(example(by_task['diagnosis_choice'])))
    parts.extend(['## 评测边界', '考试病例与模拟病例分别报告，不能把模拟患者当成真实患者。候选数量与题型不同，比较模型时冻结同一批题目和选项。', '[返回首页](../../README.md)'])
    output[ROOT / 'docs/tasks/diagnosis.md'] = '\n\n'.join(parts) + '\n'

    parts = ['# 数据集与参考来源目录', '[返回首页](../../README.md) · [临床主评测任务](../tasks/README.md) · [辅助与暂停任务](../tasks/AUXILIARY.md)',
             f"临床主评测使用 {len(clinical['sources'])} 个来源。底稿累计登记 {len(sources)} 个来源，其中 {sum(bool(by_source[s]) for s in sources)} 个有收录记录；其余仅作参考。下表按当前用途统计，底稿题数不等于主评测题数。"]
    for distribution, title in DISTRIBUTIONS.items():
        parts.extend([f'## {title}', table(['数据集 / 来源说明', '主评测题数', '辅助题数', '暂停题数', '材料性质或未采用原因'], [
            [link(s['name'], f'{sid}.md'),
             sum(rules[r['task']]['scope'] == 'clinical' for r in by_source[sid]),
             sum(rules[r['task']]['scope'] == 'auxiliary' for r in by_source[sid]),
             sum(rules[r['task']]['scope'] == 'suspended' for r in by_source[sid]),
             prose(s.get('authenticity') if by_source[sid] else s.get('reason') or s.get('authenticity') or '待核验')]
            for sid, s in sources.items() if s['distribution'] == distribution])])
    output[ROOT / 'docs/datasets/README.md'] = '\n\n'.join(parts) + '\n'

    used_tags = sorted({d for f in families for d in f['ability_tags']})
    parts = ['# Jev Healthcare Lab',
        '用于逐任务比较 **JEV 与其他模型的医疗决策准确率和完整运行耗时**。主评测围绕病例诊断、检查、治疗、用药、分诊、护理、随访与试验转介，要求从给定候选中作出选择；不包含自由生成任务。',
        f"**{len(scenes)} 个医疗场景、{len(used_tags)} 个能力标签、{clinical['defined_families']} 个任务定义。** 其中 {clinical['populated_families']} 个任务有题，共 {clinical['records']:,} 题（中文 {clinical['languages'].get('zh', 0):,} 题），采用 {len(clinical['sources'])} 个数据来源。{sum(f['status'] == 'empty' for f in families)} 个任务待补；{sum(f['status'] == 'exploratory' for f in families)} 个不足 20 题的任务作为探索项，暂不进入汇总。当前尚无模型对比成绩。",
        '[场景与任务](#场景与任务) · [任务说明与样例](docs/tasks/README.md) · [数据集说明与样例](docs/datasets/README.md) · [辅助任务](docs/tasks/AUXILIARY.md)',
        '## 能力维度',
        '场景表示医疗流程环节；能力标签描述判断方式，可以重叠。任务是逐项比较的单位，数据来源或语言子集不重复算作独立任务。',
        table(['能力维度', '关联任务数（含待补）'], [[dimensions[d], sum(d in f['ability_tags'] for f in families)] for d in used_tags]),
        '## 场景与任务',
        '任务名称链接到说明页，包含任务定义、输入样例、选项与原答案；数据集名称链接到来源、引用与许可。来源后的数字为实际题数，† 表示非商业附加来源。“可参与汇总”只代表达到最低题量门槛，不表示已通过临床验证。',
        table(['医疗场景', '有题任务 / 定义任务', '题数'], [[s['title'], f"{sum(f['records'] > 0 for f in families if f['scenario'] == sid)} / {sum(f['scenario'] == sid for f in families)}", sum(f['records'] for f in families if f['scenario'] == sid)] for sid, s in scenes.items()])]
    for sid, scene in scenes.items():
        parts.extend([f"### {scene['title']}", table(['任务', '能力维度', '题数', '状态', '数据集来源（题数）'], [
            [link(f['title'], f"docs/tasks/{f['id']}.md"), '、'.join(dimensions[d] for d in f['ability_tags']), f['records'], status_names[f['status']],
             '；'.join(link(sources[source]['name'], f'docs/datasets/{source}.md') + ('†' if sources[source]['distribution']=='research_noncommercial' else '') + f'（{n}）' for source,n in sorted(f['sources'].items())) or '待补数据']
            for f in families if f['scenario'] == sid])])
    parts.extend(['## 模型得分与耗时对比',
        '每个模型使用相同题目、候选项和许可范围，分别报告逐任务准确率、完整决策耗时（均值、P50、P95）、任务总耗时及失败率。多阶段调用、工具与重试计入完整决策耗时，运行配置随结果保存。',
        '病例诊断的两个来源子集合并为一个任务。汇总先对场景内达到 20 题的任务等权，再对有分数场景等权；不足 20 题仅给探索结果，空任务不计零分。题量门槛按本次所选许可范围计算。固定语义分类额外报告 F1、召回、混淆矩阵与多数类基线；A/B/C 等随题变化的选项不报告临床类别 F1。',
        '**现有工具支持离线质量评分，尚未实现模型调用和耗时采集。** 详细口径见 [评测方法](docs/EVALUATION.md)。',
        '## 许可', '代码采用 [MIT](LICENSE)。第三方数据保留原许可，代码许可不覆盖题目材料；见 [第三方声明](THIRD_PARTY_NOTICES.md) 和包内 LICENSE-DATA.md。'])
    output[ROOT / 'README.md'] = '\n\n'.join(parts) + '\n'
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = render()
    stale = []
    for path, content in files.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if stale:
        raise SystemExit("Outdated catalog pages:\n" + "\n".join(stale))
    print(f"{'Checked' if args.check else 'Wrote'} {len(files)} catalog pages.")


if __name__ == "__main__":
    main()
