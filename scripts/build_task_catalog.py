"""Build the business-task catalog without changing archived experiment identities."""
import argparse
from collections import Counter
import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = Path('results/task_taxonomy.json')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate(data, root=ROOT, training_dir=None):
    manifest = load(root / 'results/scenario_manifest.json')['scenes']
    tasks = [task for scene in manifest for task in scene['task_ids']]
    if len(tasks) != len(set(tasks)):
        raise ValueError('Duplicate task in scenario manifest')
    if set(data['benchmark_tasks']) != set(tasks):
        raise ValueError('Benchmark mapping must cover exactly the archived main tasks')
    families = {row['id']: row for row in data['families']}
    if len(families) != len(data['families']):
        raise ValueError('Duplicate family ID')
    for row in families.values():
        if row['domain'] not in data['domains']:
            raise ValueError(f"Unknown domain: {row['id']}")
        if not row['abilities'] or not set(row['abilities']) <= set(data['abilities']):
            raise ValueError(f"Unknown or empty abilities: {row['id']}")
        if row['scope'] not in ('component', 'external_system') or not row['boundary'].strip():
            raise ValueError(f"Missing scope or boundary: {row['id']}")
    methods = load(root / 'results/task_methods.json')
    for scene in manifest:
        for task in scene['task_ids']:
            if task not in methods or not (root / 'scenarios' / scene['id'] / task / 'README.md').is_file():
                raise ValueError(f'Missing archive or method: {task}')
    snapshot = data['training_snapshot']
    for task, row in snapshot['tasks'].items():
        if type(row['records']) is not int or row['records'] <= 0 or not row['title']:
            raise ValueError(f'Invalid training count/title: {task}')
    if sum(row['records'] for row in snapshot['tasks'].values()) != snapshot['records']:
        raise ValueError('Training snapshot total mismatch')
    for mapping in (data['benchmark_tasks'], snapshot['tasks']):
        for task, row in mapping.items():
            if row['family'] not in families:
                raise ValueError(f'Unknown family: {task}')
    for task, row in data['benchmark_tasks'].items():
        if not isinstance(row['tags'], list) or any(not isinstance(t, str) for t in row['tags']):
            raise ValueError(f'Invalid tags: {task}')
    # An explicit path requires all four splits; a plain checkout needs no training package.
    if training_dir is not None:
        counts = Counter()
        for split in ('train', 'dev', 'calibration', 'test'):
            path = Path(training_dir) / f'{split}.jsonl'
            if not path.is_file():
                raise ValueError(f'Missing training split: {path}')
            if hashlib.sha256(path.read_bytes()).hexdigest() != snapshot['split_sha256'][split]:
                raise ValueError(f'Training split hash differs from snapshot: {path}')
            for line in path.read_text(encoding='utf-8').splitlines():
                row = json.loads(line)
                if row['metadata']['language'] != 'zh':
                    raise ValueError(f'Non-Chinese row in Chinese snapshot: {path}')
                counts[row['metadata']['task']] += 1
        expected = Counter({t: r['records'] for t, r in snapshot['tasks'].items()})
        if counts != expected:
            raise ValueError('Training package differs from the frozen task snapshot')
    return manifest, methods


def status(family, benchmark, training):
    if benchmark:
        return '部分已测'
    if training:
        return '训练扩展；主评测未测'
    if family['scope'] == 'external_system':
        return '需组合系统；未测'
    return '未测'


def render(data, manifest, methods):
    families = {row['id']: row for row in data['families']}
    bench = data['benchmark_tasks']
    training = data['training_snapshot']['tasks']
    counts = Counter(row['family'] for row in bench.values())
    train_counts = Counter(row['family'] for row in training.values())
    scene_of = {task: s['id'] for s in manifest for task in s['task_ids']}
    total = sum(load(ROOT / 'scenarios' / scene_of[t] / t / 'results.json')['successful'] for t in bench)
    out = [
        '# 医疗任务总目录', '',
        '[首页](../README.md) · [逐项任务映射](医疗任务映射.md) · [效果与费用](任务对比.md) · [资源与阻塞](覆盖与阻塞账本.md)', '',
        f'按 **{len(data["domains"])} 个业务领域、{len(families)} 个任务族** 浏览已有实验与待补工作。任务族是可持续扩展的项目目录，不是穷尽医疗工作的行业标准。', '',
        f'主评测为 **{len(bench)} 个任务条件、{total:,} 条输入**；独立训练快照为 **{len(training)} 类、{data["training_snapshot"]["records"]:,} 条中文材料判断题**。语言、选项形式、有无证据和转写条件可能分别计作任务条件，不能相加为独立医疗工作数或患者数。', '',
        '## 如何读这个目录', '',
        '- **业务领域 → 任务族 → 能力**：例如用药管理 → 剂量、频次、途径与给药进度 → 关联与状态判断。每项评测有一个主要任务族；跨领域复用通过能力和标签检索，不重复累计。',
        '- **标签**：中医、OCR 文本、ASR 文本、选择题、给定实体和人工边界题描述专业或实验条件，不与业务领域并列。标签不是完整的专科或人群覆盖声明。',
        '- **部分已测**：任务族有有限样本或子任务实测，完整业务链路仍有缺口。逐项映射中的“有限实测”只指该实验条件已执行。',
        '- **训练扩展；主评测未测**：只有独立训练数据及其本地审计线索，没有对应 Jev 主评测；不能借用训练样本数或其他模型结果宣称 Jev 能力。',
        '- **未测**：没有对应主评测或训练映射。**需组合系统；未测**：还需要生成、感知、工具执行或专门预测优化系统；不是永远不可做。', '',
        '## 业务覆盖总览', '',
        '| 业务领域 | 任务族 | 主评测条件 | 训练任务类型 |',
        '| --- | ---: | ---: | ---: |',
    ]
    for domain, title in data['domains'].items():
        fs = [f for f in families.values() if f['domain'] == domain]
        out.append(f'| [{title}](#{domain}) | {len(fs)} | {sum(counts[f["id"]] for f in fs)} | {sum(train_counts[f["id"]] for f in fs)} |')
    out += ['', '目前没有任何任务族被标为“完整工作流已验证”。上述列数反映归档与训练映射，不能据此计算临床覆盖率。', '']
    for domain, title in data['domains'].items():
        out += [f'<a id="{domain}"></a>', '', f'## {title}', '',
                '| 任务族 | 能力 | 覆盖状态 | 主评测／训练类型 | 已有范围与关键缺口 |',
                '| --- | --- | --- | --- | --- |']
        for f in families.values():
            if f['domain'] != domain:
                continue
            n, m = counts[f['id']], train_counts[f['id']]
            ability = '、'.join(data['abilities'][a] for a in f['abilities'])
            out.append(f'| [{f["title"]}](医疗任务映射.md#{f["id"]}) | {ability} | {status(f,n,m)} | {n}／{m} | {f["boundary"]} |')
        out.append('')
    out += ['## 下一步优先补什么', '',
            '以下为工程与评测优先级建议，不是已测收益排序。新增任务先定义输入、输出、判定依据和独立验证材料，再选择模型。', '',
            '| 顺序 | 工作 | 应新增的证据 |', '| --- | --- | --- |',
            '| 1 | 从原始文书到结构化结果的完整链路 | 候选漏召回、字段遗漏、错误关联、整份病例全对率与人工修订量 |',
            '| 2 | 用药核对、逐条入组、出院随访三个具体流程 | 每项判断的证据、未知与冲突处理、事件状态及任务完成验证 |',
            '| 3 | 护理、围术期、营养康复和医院运营缺口 | 经授权的专属材料、独立金标、实际使用者与业务收益指标 |',
            '| 4 | 生成、感知、工具执行和预测优化 | 组合系统基线、上下游错误传播、真实流程结果；分别评价组件与整链 |', '',
            '横向验证还应覆盖机构、时间、语言、专科、人群、长材料和输入质量变化，以及错误严重度、拒答/升级和人工复核成本。已有任务名称不代表这些维度均有足够样本。', '',
            '## 分类与维护依据', '',
            '本目录按项目任务目的人工映射。MedJourney 用药题归入用药管理，诊断和检查治疗题归入诊疗支持；NLI4CT 归入科研证据理解；中医题按诊断、治疗、知识和伦理分别映射。旧目录继续作为实验归档路径，便于复验历史链接。', '',
            '可参考 [MedHELM 官方分类说明](https://github.com/stanford-crfm/helm/blob/main/docs/medhelm.md)检查业务广度；本项目未采用其任务编号，也不能用本目录数量直接比较其 121 个任务。', '',
            '机器可读定义为 [task_taxonomy.json](../results/task_taxonomy.json)，归档身份来自 [scenario_manifest.json](../results/scenario_manifest.json)。详细验证命令见[复现与维护](REPRODUCING.md#任务目录维护)。', '']
    mapping = ['# 医疗任务逐项映射', '',
               '[业务总目录](医疗任务总目录.md) · [实验归档](../scenarios/README.md) · [任务成绩](任务对比.md)', '',
               '每个主评测条件只出现一次；名称、旧路径和成绩保留。相同能力可用于多个业务领域，此处按主要目的归类。训练任务另表列出，不并入主评测。', '']
    for f in families.values():
        mapping += [f'<a id="{f["id"]}"></a>', '', f'## {data["domains"][f["domain"]]} · {f["title"]}', '', f['boundary'], '']
        task_ids = [t for t, r in bench.items() if r['family'] == f['id']]
        if task_ids:
            mapping += ['| 主评测任务 | 任务 ID | 能力类型 | 条件标签 | 状态 |', '| --- | --- | --- | --- | --- |']
            for task in task_ids:
                method = methods[task]
                tags = '、'.join(bench[task]['tags']) or '文本条件；详见方法页'
                mapping.append(f'| [{method["title"]}](../scenarios/{scene_of[task]}/{task}/README.md) | `{task}` | {method["task_type"]} | {tags} | 有限实测 |')
        else:
            mapping.append('无对应主评测。')
        training_ids = [t for t, r in training.items() if r['family'] == f['id']]
        if training_ids:
            mapping += ['', '训练扩展：'+ '、'.join(f'{training[t]["title"]}（`{t}`）' for t in training_ids)+'。数量及口径见下表。']
        mapping.append('')
    mapping += ['## 训练任务统计快照', '',
                f'来源包：`{data["training_snapshot"]["package"]}` 中文主集，含 train/dev/calibration/test 四个分区，共 {data["training_snapshot"]["records"]:,} 条。下表仅为任务结构与数量快照，不包含训练材料，不是 Jev 主评测成绩；样本数不代表独立患者数或专家审核量。', '',
                '原训练包作为独立扩展使用。基础仓库不依赖它即可检查本目录；持有该包时，可按[维护说明](REPRODUCING.md#任务目录维护)核对四个分区的条数与 SHA-256。', '',
                '| 训练任务 | 任务 ID | 主要任务族 | 四分区合计 |', '| --- | --- | --- | ---: |']
    for task, row in sorted(training.items()):
        f = families[row['family']]
        mapping.append(f'| {row["title"]} | `{task}` | [{f["title"]}](#{f["id"]}) | {row["records"]} |')
    mapping += [f'| 合计 | {len(training)} 类 | — | {data["training_snapshot"]["records"]:,} |', '']
    archive = ['# 实验归档目录', '',
               '[按医疗业务任务浏览](../docs/医疗任务总目录.md) · [96 项逐项映射](../docs/医疗任务映射.md) · [成绩与费用](../docs/任务对比.md)', '',
               '这里保留 12 个历史归档分组；业务目录采用统一分类，并链接到同一批任务。归档分组名不代表完整工作流已经验证。', '',
               '| 归档分组 | 主评测条件 |', '| --- | ---: |']
    for s in manifest:
        archive.append(f'| [{s["title"]}]({s["id"]}/README.md) | {len(s["task_ids"])} |')
    archive += ['', '每个任务目录保留输入、提示词、金标、响应、方法和评分。扰动与配对实验位于对应任务下，不重复计算主任务。', '']
    return {Path('docs/医疗任务总目录.md'): '\n'.join(out),
            Path('docs/医疗任务映射.md'): '\n'.join(mapping),
            Path('scenarios/README.md'): '\n'.join(archive)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate mappings and reject stale generated pages')
    parser.add_argument('--training-dir', type=Path, help='Additionally verify all four Chinese training splits')
    args = parser.parse_args()
    data = load(ROOT / CATALOG)
    manifest, methods = validate(data, training_dir=args.training_dir)
    stale = []
    for path, content in render(data, manifest, methods).items():
        target = ROOT / path
        if args.check:
            if not target.is_file() or target.read_text(encoding='utf-8') != content:
                stale.append(str(path))
        else:
            target.write_text(content, encoding='utf-8')
    if stale:
        raise SystemExit('Stale task catalog: ' + ', '.join(stale))
    print(f"Task catalog OK: {len(data['families'])} families, {len(data['benchmark_tasks'])} benchmark conditions, {len(data['training_snapshot']['tasks'])} training types")


if __name__ == '__main__':
    main()
