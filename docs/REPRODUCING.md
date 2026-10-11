# 数据使用与复建

[返回首页](../README.md) · [下载与校验和](../releases/README.md)

Python 3.10+，仅标准库。数据构建、校验和评分不调用模型 API。

## 使用整理包

下载页按临床主评测 / 辅助评测、开放许可 / 非商业附加分成四包。各包互不重复。解压后在包目录执行：

```bash
python3 tools/medical_decision_release.py verify --dataset .
python3 tools/medical_decision_release.py trace --dataset . --id '完整题目ID'
python3 tools/medical_decision_release.py score --dataset . --predictions predictions.jsonl --output scores.json
```

模型使用包内 requests.jsonl，只发送 request。独立评分器自动使用本包的范围与许可，暂停任务不在任何包内。需要同时评测主范围两种许可时，可在仓库导出完整临床范围，合并对应预测后用 --include-research 评分；不同题目范围的总分不能直接比较。

追溯默认离线。使用 `trace --fetch-source` 可下载该题直接依赖并核对锁定 SHA-256；失效链接或哈希变化会报错。原始大文件与整理包的体积不同，只用整理包不需要全量下载。

## 从仓库导出与评分

```bash
python3 scripts/medical_decision_dataset.py validate
python3 scripts/medical_decision_dataset.py export --output work/clinical-requests.jsonl
python3 scripts/medical_decision_dataset.py score --predictions work/predictions.jsonl --output work/clinical-scores.json
```

默认临床主评测、开放许可，共 1,284 题。增加 `--include-research` 后为 1,514 题。辅助评测须在导出与评分时都加 `--scope auxiliary`，并分别报告；暂停题目不可选择。必须使用同一范围、许可子集和题号集合，范围外预测会报错。

仓库底稿目录中的 samples.jsonl、requests.jsonl、answers.jsonl 保留全部原始整理记录供追溯，包括辅助与暂停任务；不要绕过范围导出把底稿全部当作临床主评测。每个样本的原题号保留，用户任务合并关系记录在 evaluation_scope.json，评分结果 task_families 为合并任务，tasks 为原来源子集。

## 复建与本地验证

```bash
python3 scripts/medical_decision_dataset.py fetch
python3 scripts/medical_decision_dataset.py build
python3 scripts/generate_catalog_docs.py
python3 scripts/medical_decision_release.py build
python3 -m unittest discover -s tests -v
```

fetch 按 sources.lock.json 下载并核对固定资源，缓存位于 work/decision-benchmark-v1/raw/。部分小型文件和易变 API 响应随仓库冻结；API 在线内容变化不会自动替换已有快照。Parquet 与标准库解码 JSON 同时冻结，可选用 PyArrow 运行 `python3 scripts/verify_source_tables.py` 独立核验解码。

build 使用固定种子、原适配器和冻结的 exposure_index.json 重建来源底稿、范围统计及清单；不生成新题或新答案。不要为复建重新运行 index。其他模型的训练材料需要另做暴露筛查，并冻结共同子集后再比较。

下载包只取策略允许的任务与相应许可，附原许可、逐题溯源、独立评分器及内容清单。文件顺序和 ZIP 时间戳固定，可重复比较校验和。正式使用以内容清单和范围策略哈希标识数据。

## 更新说明页与范围

```bash
python3 scripts/generate_catalog_docs.py
python3 scripts/generate_catalog_docs.py --check
python3 scripts/audit_task_scope.py
```

说明页生成器从实际记录与执行范围生成首页、任务页和来源页。审查脚本复核调整前底稿的分组统计及姓名捷径，供回溯问题，不把暂停题重新加入评分。变更范围时需同步重建底稿清单、说明页和下载包；运行本地检查。
