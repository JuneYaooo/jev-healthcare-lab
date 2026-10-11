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
    "open": "开放许可核心集",
    "research_noncommercial": "非商业研究附加集",
    "reference_only": "仅作参考，未收录题目",
}
LANGUAGES = {"zh": "中文", "en": "英语", "es": "西班牙语"}


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
        source_counts = Counter(r["provenance"]["source_id"] for r in rows)
        assert len(rows) == report["count"]
        assert dict(source_counts) == report["source_counts"]
        parts = [
            f"# {task['title']}",
            "[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)",
            "## 任务是什么",
            task["definition"],
            table(["项目", "说明"], [
                ["任务 ID", f"`{tid}`"],
                ["医疗场景", scenes[task["primary_scenario"]]["title"]],
                ["能力维度", "、".join(dimensions[d] for d in task["ability_tags"])],
                ["决策类型", STAGES[task["decision_stage"]]],
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
                "根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。",
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
            parts.append(table(["任务说明", "此来源贡献题数", "评测内容"], [
                [task_link(tid), str(n), tasks[tid]["definition"]]
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

    parts = ["# 任务说明目录", "[返回首页](../../README.md) · [数据集目录](../datasets/README.md)", f"共 {len(tasks)} 个任务定义，{len([t for t in tasks if by_task[t]])} 个有题任务。每页说明判断目标、来源、样例输入、标准答案与使用边界；空任务保留定义和缺口。"]
    for scene_id, scene in scenes.items():
        parts.extend([f"## {scene['title']}", scene["scope"], table(["任务说明", "能力维度", "题数"], [
            [link(t['title'], f"{tid}.md"), "、".join(dimensions[d] for d in t['ability_tags']), str(len(by_task[tid]))]
            for tid, t in tasks.items() if t['primary_scenario'] == scene_id
        ])])
    output[ROOT / "docs/tasks/README.md"] = "\n\n".join(parts) + "\n"

    parts = ["# 数据集与参考来源目录", "[返回首页](../../README.md) · [任务目录](../tasks/README.md)", f"登记 {len(sources)} 个来源，其中 {len([s for s in sources if by_source[s]])} 个实际提供题目。其余仅作调研参考，包括受控数据、许可待核验数据及标准规范，不能按已收录数据集统计。页面中的题数均为本评测集实际采用的数量，不是上游数据总量。"]
    for distribution, title in DISTRIBUTIONS.items():
        parts.extend([f"## {title}", table(["数据集 / 来源说明", "题数", "采用任务数", "材料性质或未采用原因"], [
            [link(s['name'], f"{sid}.md"), str(len(by_source[sid])), str(len({r['task'] for r in by_source[sid]})), prose(s.get('authenticity') if by_source[sid] else s.get('reason') or s.get('authenticity') or '待核验')]
            for sid, s in sources.items() if s['distribution'] == distribution
        ])])
    output[ROOT / "docs/datasets/README.md"] = "\n\n".join(parts) + "\n"
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
