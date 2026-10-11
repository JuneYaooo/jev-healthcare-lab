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

## 运行模型与复核结果

本轮完整结果见 [模型对比](MODEL_RESULTS.md)，逐题响应与配置位于 results/clinical-v1/。复核现有结果不调用 API：

```bash
python3 scripts/build_model_report.py --check
```

新一轮运行从环境变量或本地 .env 读取 TYPESAFE_API_KEY、DEEPSEEK_API_KEY、SILICONFLOW_API_KEY，调用对应官方服务。使用新的输出目录保留独立运行记录：

```bash
python3 scripts/run_model_evaluation.py run --model jev-1.13.0 --include-research --output work/new-run/jev-1.13.0
python3 scripts/run_model_evaluation.py run --model deepseek-flash --include-research --output work/new-run/deepseek-flash
python3 scripts/run_model_evaluation.py run --model deepseek-v4-pro --include-research --output work/new-run/deepseek-v4-pro
python3 scripts/run_model_evaluation.py run --model qwen3.5-9b --include-research --output work/new-run/qwen3.5-9b
python3 scripts/run_model_evaluation.py run --model qwen3.8-27b --include-research --output work/new-run/qwen3.8-27b
```

默认每模型并发 8、单次请求超时 120 秒，最多 3 次尝试；只重试暂时性请求失败。返回错误或格式无效的答案照常保存，不按得分重跑。省略 --include-research 只评测开放部分，--scope auxiliary 运行辅助部分。脚本不自动预热，新运行应另记外部连通性检查与预热设置。

重复指定相同目录会核对配置与输入并跳过已经结束的题目，不覆盖原响应。中断续跑的任务不提供单次完整任务墙钟数，分段时间仍保留；需要完整可比计时应建立新的运行目录。生成器与评分器依据范围策略、固定输入和原始响应复核结果，所有密钥均不写入结果。

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
