"""Create standalone medical decision releases and trace individual samples.

Standard library only. No model calls or uploads. Packages retain source licenses.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import shlex
import tempfile
import urllib.request
import zipfile

import medical_decision_dataset as data

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/JuneYaooo/jev-healthcare-lab"


def checked_path(root, name):
    part = PurePosixPath(name)
    if part.is_absolute() or ".." in part.parts or "\\" in name:
        raise ValueError("Unsafe relative path: " + name)
    path = root / name
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Path outside package: " + name)
    return path


def source_identity(entry):
    return entry.get("source_id", entry.get("source"))


def trace_record(row, cards, resources, tasks, builder_sha):
    provenance = row["provenance"]
    source = cards[provenance["source_id"]]
    names = [provenance["resource"]]
    if provenance["locator"].get("text_resource"):
        names.append(provenance["locator"]["text_resource"])
    names.extend(provenance["locator"].get("supporting_resources", []))
    if provenance["source_id"] == "ddxplus":
        names += ["ddxplus__release_evidences.json", "ddxplus__release_conditions.json"]
    return {"id": row["id"], "task": row["task"], "primary_scenario": row["primary_scenario"],
            "record_sha256": data.digest(row), "request_sha256": row["request_sha256"],
            "gold": row["gold"], "gold_option": row["request"]["questions"]["decision"]["criteria"][row["gold"]],
            "provenance": provenance, "source_title": source["name"],
            "citation_url": source["citation_url"], "attribution": source["attribution"],
            "license_url": source["license_url"], "license_evidence": source["license_evidence"],
            "adaptation": {"task_definition": tasks[row["task"]]["definition"],
                           "gold_mapping": source["gold_provenance"],
                           "row_metadata": row["metadata"], "builder_sha256": builder_sha},
            "resources": [resources[name] for name in names]}


def package_files(dataset, distribution):
    """Return an explicit allowlist; never archive a workspace recursively."""
    rows = [r for r in data.read_jsonl(dataset / "samples.jsonl")
            if r["provenance"]["distribution"] == distribution]
    if not rows:
        raise ValueError("Empty release: " + distribution)
    selected_sources = {r["provenance"]["source_id"] for r in rows}
    all_cards = json.loads((dataset / "sources.json").read_text())["sources"]
    cards = {s["id"]: s for s in all_cards if s["id"] in selected_sources}
    lock = json.loads((dataset / "sources.lock.json").read_text())["files"]
    lock = [{**entry, "source_id": source_identity(entry)} for entry in lock if source_identity(entry) in selected_sources]
    resources = {r["name"]: r for r in lock}
    taxonomy = json.loads((dataset / "taxonomy.json").read_text())
    tasks = {t["id"]: t for t in taxonomy["tasks"]}
    builder_path = ROOT / "scripts/medical_decision_dataset.py"
    builder_sha = data.file_sha(builder_path)
    files = {}

    def js(name, value):
        files[name] = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()

    def jl(name, values):
        files[name] = "".join(data.dumps(v) + "\n" for v in values).encode()

    def md(name, lines):
        files[name] = ("\n".join(lines) + "\n").encode()

    jl("samples.jsonl", rows)
    jl("requests.jsonl", ({"id": r["id"], "task": r["task"], "request": r["request"]} for r in rows))
    jl("answers.jsonl", ({"id": r["id"], "gold": r["gold"], "group_id": r["group_id"]} for r in rows))
    jl("provenance.jsonl", (trace_record(r, cards, resources, tasks, builder_sha) for r in rows))
    example = next((r for r in rows if r["provenance"]["source_id"] == "medcalc"), rows[0])
    js("example-trace.json", trace_record(example, cards, resources, tasks, builder_sha))
    js("taxonomy.json", taxonomy)
    js("sources.json", {"sources": list(cards.values())})
    js("sources.lock.json", {"files": lock})
    for source in cards.values():
        for name in source["license_evidence"]:
            files[name] = checked_path(dataset, name).read_bytes()
    for name in ["medical_decision_dataset.py", "medical_decision_release.py"]:
        files["tools/" + name] = (ROOT / "scripts" / name).read_bytes()
    files["LICENSE-CODE.txt"] = (ROOT / "LICENSE").read_bytes()
    count = Counter(r["task"] for r in rows)
    summary = {"dataset_version": taxonomy["version"], "distribution": distribution,
               "records": len(rows), "tasks_with_data": len(count), "task_counts": dict(count),
               "source_counts": dict(Counter(r["provenance"]["source_id"] for r in rows)),
               "languages": dict(Counter(r["language"] for r in rows)),
               "historical_material_matches": sum(r["exposure"]["historical_material_signature_match"] for r in rows),
               "source_dataset_manifest_sha256": data.file_sha(dataset / "manifest.json"),
               "builder_sha256": builder_sha, "repository": REPOSITORY,
               "package_revision": 1, "use": "frozen_evaluation", "model_evaluation_performed": False}
    js("release.json", summary)
    notices = ["# 数据许可与来源署名", "",
               "本包是多个来源的选题合集，各题按 provenance.data_license 保留原许可；题目适配随相应来源许可提供。代码的 MIT 许可不覆盖第三方材料。", "",
               "开放核心包没有纳入非商业限制来源，但部分材料有相同方式共享要求；开放使用不等于无条件使用。非商业附加包不能作为开放核心包再许可。", "",
               "| 来源 | 题数 | 数据许可 |", "| --- | ---: | --- |"]
    for sid, card in cards.items():
        notices.append(f"| [{card['name']}]({card['url']}) | {summary['source_counts'][sid]} | [{card['data_license']}]({card['license_url']}) |")
    for card in cards.values():
        notices += ["", "## " + card["name"], "", f"{card['attribution']}。引用：{card['citation_url']}。", "",
                    "材料性质：" + card["authenticity"], "", "本次适配：" + card["gold_provenance"], "",
                    "原声明：" + "、".join(f"[{Path(p).name}]({p})" for p in card["license_evidence"]) + "。"]
    md("LICENSE-DATA.md", notices)
    md("FORMAT.md", ["# 数据格式与追溯", "",
        "全部 JSONL 文件均为 UTF-8，一行一条记录，以 id 关联，不依赖文件顺序。", "",
        "| 文件 | 内容 |", "| --- | --- |",
        "| samples.jsonl | 完整整理题目：id、task、primary_scenario、ability_tags、language、group_id、request、gold、provenance、exposure |",
        "| requests.jsonl | 仅 id、task、request；调用模型只发送 request 并按接口添加 model |",
        "| answers.jsonl | 独立答案：id、gold、group_id |",
        "| provenance.jsonl | 逐题来源版本、资源 URL/哈希、原标注位置、引用、许可、转换说明与代码哈希 |",
        "| taxonomy.json | 八个场景和全部任务定义；本包未收录的任务不算已覆盖 |",
        "| sources.lock.json | 仅本包来源的上游文件锁定清单 |",
        "| manifest.json | 包内每个交付文件的 SHA-256 和字节数 |", "",
        "request.state 是输入材料；questions.decision.criteria 为选项键与显示文本；gold 是选项键。provenance.locator 按来源采用 CSV 行号（含表头）、JSONL 行号、压缩包成员和标注 ID 等定位。", "",
        "追溯链：id → 整理题目及答案 → provenance.locator → resource_url + version + SHA-256 → 原文件与原标注。SHA-256 用于确认版本和完整性，不等同临床答案审核。", "",
        "原始全量数据不包含在本包中；需要时使用 trace 的 --fetch-source 下载该题直接依赖并校验哈希。失效链接或哈希变化会报错，不会静默换用新版本。", "",
        "例：先从 samples.jsonl 取得完整 id，再运行 `python3 tools/medical_decision_release.py trace --dataset . --id '完整ID'`。"])
    md("README.md", [f"# Jev 医疗决策评测集 v{taxonomy['version']} · {distribution}", "",
        f"本包包含 {len(rows):,} 道整理后的决策题，{len(count)} 个任务；无需下载全量上游数据即可读取和评测。", "",
        "[数据格式与追溯](FORMAT.md) · [逐题溯源示例](example-trace.json) · [数据许可与引用](LICENSE-DATA.md) · [题目](samples.jsonl) · [无答案请求](requests.jsonl) · [答案](answers.jsonl)", "",
        "## 快速使用", "", "在解压后的目录执行，Python 3.10+，仅标准库：", "", "```bash",
        "python3 tools/medical_decision_release.py verify --dataset .",
        "python3 tools/medical_decision_release.py trace --dataset . --id " + shlex.quote(example["id"]),
        "python3 tools/medical_decision_release.py score --dataset . --predictions predictions.jsonl --output scores.json",
        "```", "", "预测文件每行形如 `{" + '"id":"完整样本ID","choice":"选项键"' + "}`；缺失与无效回答计错，重复或未知 ID 报错。只评分本包题目，先任务内统计，再按场景等权汇总；空场景分数为 null。", "",
        "## 读取", "", "```python", "import json", 'with open("requests.jsonl", encoding="utf-8") as f:',
        "    for line in f:", "        row = json.loads(line)", '        request = row["request"]  # 将此对象交给模型；勿发送答案或来源标注', "```", "",
        "## 来源与复建", "", f"项目：[Jev Healthcare Lab]({REPOSITORY})。本包包含锁定资源清单、原许可声明和精确版本的转换/评分代码。", "",
        "完整重建在项目仓库执行 `python3 scripts/medical_decision_dataset.py fetch`、`python3 scripts/medical_decision_dataset.py build`，再运行 `python3 scripts/medical_decision_release.py build`。以 release.json 的版本和源清单哈希核对，勿将不同版本成绩直接比较。", "",
        "## 使用边界", "", "这是冻结评测子集，不是训练集。用于训练会影响后续同题比较。材料包括模拟病例、考试改编、临床病例报告等，不能统称真实患者病历。答案沿用上游标注，尚未经过本项目独立医生逐题审核。", "",
        f"本包中 {summary['historical_material_matches']} 题的材料或片段命中过往评测，已逐题标记；通用片段可能误报。分组不一律等于患者；同来源组的题需配对或聚类分析。", "",
        "模型成绩未随包生成。法律许可和来源署名以 LICENSE-DATA.md 及原声明为准。"])
    js("manifest.json", {"format_version": 1, "files": {name: {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
                                                          for name, raw in sorted(files.items())}})
    return files, summary


def verify(dataset):
    manifest = json.loads((dataset / "manifest.json").read_text())
    required = {"samples.jsonl", "requests.jsonl", "answers.jsonl", "provenance.jsonl", "taxonomy.json",
                "sources.json", "sources.lock.json", "release.json", "LICENSE-CODE.txt", "LICENSE-DATA.md",
                "tools/medical_decision_dataset.py", "tools/medical_decision_release.py"}
    if not required <= set(manifest["files"]):
        raise ValueError("Incomplete package manifest")
    for name, record in manifest["files"].items():
        path = checked_path(dataset, name)
        if data.file_sha(path) != record["sha256"] or path.stat().st_size != record["bytes"]:
            raise ValueError("Package hash mismatch: " + name)
    rows = list(data.read_jsonl(dataset / "samples.jsonl"))
    meta = json.loads((dataset / "release.json").read_text())
    if meta["distribution"] not in {"open", "research_noncommercial"}:
        raise ValueError("Unknown license distribution")
    cards = {s["id"]: s for s in json.loads((dataset / "sources.json").read_text())["sources"]}
    resources = {r["name"]: r for r in json.loads((dataset / "sources.lock.json").read_text())["files"]}
    tasks = {t["id"]: t for t in json.loads((dataset / "taxonomy.json").read_text())["tasks"]}
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)) or len(rows) != meta["records"]:
        raise ValueError("Duplicate IDs or wrong count")
    for row in rows:
        p = row["provenance"]
        card = cards[p["source_id"]]
        if p["distribution"] != meta["distribution"] or p["distribution"] != card["distribution"]:
            raise ValueError("Mixed license distribution")
        if p["data_license"] != card["data_license"] or p["resource_sha256"] != resources[p["resource"]]["sha256"]:
            raise ValueError("Source license/hash mismatch")
        if p["resource_url"] != resources[p["resource"]]["url"] or p["version"] != resources[p["resource"]]["version"] or not p["locator"]:
            raise ValueError("Source URL/version/locator mismatch")
        if row["request_sha256"] != data.digest(row["request"]):
            raise ValueError("Request changed")
        if row["gold"] not in row["request"]["questions"]["decision"]["criteria"]:
            raise ValueError("Gold outside choices")
        for name in card["license_evidence"]:
            if name not in manifest["files"]:
                raise ValueError("Missing license evidence: " + name)
    expected = [trace_record(r, cards, resources, tasks, meta["builder_sha256"]) for r in rows]
    if list(data.read_jsonl(dataset / "provenance.jsonl")) != expected:
        raise ValueError("Broken source trace")
    if list(data.read_jsonl(dataset / "requests.jsonl")) != [{"id": r["id"], "task": r["task"], "request": r["request"]} for r in rows]:
        raise ValueError("Request export differs")
    if list(data.read_jsonl(dataset / "answers.jsonl")) != [{"id": r["id"], "gold": r["gold"], "group_id": r["group_id"]} for r in rows]:
        raise ValueError("Answer export differs")
    if data.file_sha(dataset / "tools/medical_decision_dataset.py") != meta["builder_sha256"]:
        raise ValueError("Builder version differs")
    return {"passed": True, "records": len(rows), "distribution": meta["distribution"], "source_traces": len(expected)}


def trace(dataset, uid, fetch_source=False, cache=None):
    verify(dataset)
    row = next((r for r in data.read_jsonl(dataset / "provenance.jsonl") if r["id"] == uid), None)
    if row is None:
        raise ValueError("Unknown sample ID: " + uid)
    if fetch_source:
        cache = cache or dataset / "upstream-cache"
        cache.mkdir(parents=True, exist_ok=True)
        for resource in row["resources"]:
            path = checked_path(cache, resource["name"])
            if not path.exists() or data.file_sha(path) != resource["sha256"]:
                request = urllib.request.Request(resource["url"], headers={"User-Agent": "Jev-Medical-Decision-Trace"})
                with urllib.request.urlopen(request, timeout=60) as response:
                    raw = response.read()
                if hashlib.sha256(raw).hexdigest() != resource["sha256"]:
                    raise ValueError("Upstream changed: " + resource["name"])
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
        row["upstream_hashes_verified"] = True
    return row


def build(dataset, output):
    data.validate(dataset)
    output.mkdir(parents=True, exist_ok=True)
    releases = []
    for distribution, suffix in [("open", "open"), ("research_noncommercial", "research-noncommercial")]:
        files, meta = package_files(dataset, distribution)
        name = f"jev-medical-decision-v{meta['dataset_version']}-{suffix}"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for part, raw in files.items():
                target = checked_path(root, part)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
            verify(root)
        path = output / (name + ".zip")
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for part, raw in sorted(files.items()):
                info = zipfile.ZipInfo(name + "/" + part, date_time=(2026, 10, 10, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, raw, compresslevel=9)
        releases.append({"file": path.name, "sha256": data.file_sha(path), "bytes": path.stat().st_size,
                         "records": meta["records"], "distribution": distribution})
    data.write_json(output / "release-index.json", {"releases": releases})
    (output / "SHA256SUMS").write_text("".join(f"{r['sha256']}  {r['file']}\n" for r in releases))
    (output / "README.md").write_text("# 医疗决策数据集下载\n\n" +
        "每个包都含整理后的题目、独立答案、无答案请求、逐题溯源索引、原许可与引用，以及离线校验/评分工具。解压即可使用，Python 3.10+，无第三方依赖。\n\n" +
        "| 数据包 | 题数 | 使用范围 |\n| --- | ---: | --- |\n" + "".join(
            f"| [{r['file']}]({r['file']}) | {r['records']:,} | " + ("开放许可核心集；遵循各来源署名及相同方式共享等条件" if r['distribution']=='open' else "非商业研究附加集；不得按开放核心许可混用") + " |\n" for r in releases) +
        "\n[校验和](SHA256SUMS) · [场景与任务](../benchmarks/medical_decision_v1/README.md) · [全部来源登记](../benchmarks/medical_decision_v1/SOURCES.md)\n\n" +
        "两个包互不重复；共同使用时仍分别遵守原许可。开放核心集可独立运行，不依赖非商业附加集。数据为评测子集，实际训练会影响后续同题对比。\n\n" +
        "重建：`python3 scripts/medical_decision_release.py build`。压缩包按固定顺序和时间戳生成，可重复校验字节一致性。\n")
    return releases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "verify", "trace", "score"])
    parser.add_argument("--dataset", type=Path, default=data.DEFAULT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--id")
    parser.add_argument("--fetch-source", action="store_true")
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--predictions", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        result = build(args.dataset, args.output or ROOT / "releases")
    elif args.command == "verify":
        result = verify(args.dataset)
    elif args.command == "trace":
        if not args.id:
            parser.error("trace requires --id")
        result = trace(args.dataset, args.id, args.fetch_source, args.cache)
    else:
        if not args.predictions or not args.output:
            parser.error("score requires --predictions and --output")
        verify(args.dataset)
        meta = json.loads((args.dataset / "release.json").read_text())
        result = data.score(args.dataset, args.predictions, meta["distribution"] == "research_noncommercial")
        result["release_distribution"] = meta["distribution"]
        data.write_json(args.output, result)
        result = {key: result[key] for key in ["records", "scored_tasks", "scenario_macro_accuracy", "release_distribution"]}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
