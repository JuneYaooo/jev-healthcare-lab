# 复现说明

## 结果与输入的边界

仓库包含历史聚合结果、评测身份/哈希和实现代码，不包含第三方基准原文或真实API缓存。因此，`scripts/summary.py`可以离线查看已发布快照，重新调用/重新计分则需要自行取得原始数据并生成请求、保留响应。没有声称这是从空目录一键复现全部数据集的发行包。

默认数据目录为仓库根下 `data/`；核心脚本可用环境变量 `JEV_DATA_DIR` 指向已经取得的数据与缓存目录。数据目录不进入Git。原实验中的 `work/medical-bench/...` 在新仓库统一对应 `data/...`。少量OCR/ASR辅助脚本使用根目录相对路径，应在仓库根目录运行。

## 调用API

先在本机设置 `TYPESAFE_API_KEY`，不把实际密钥写进代码、README或Git；`.env.example`仅为格式示例，不会自动加载。

```sh
python3 scripts/live_batch.py --input data/EXAMPLE_prepared.jsonl --max-calls 10 --workers 4
```

也可用 `--env-file` 指向自己的私有env文件。示例中的EXAMPLE应替换成真实准备文件。默认模型固定jev-1.13.0。成功结果缓存跳过；网络错误再次运行才重试，失败历史保留。真实调用会收费。不会用模拟预测替代失败请求。

首次运行应检查数据许可、状态字段和标签是否正确；取得数据许可并不自动意味着可以把真实患者信息发送给任意云服务。

## 核验范围

当前仓库测试检查结果计数、重复身份、评分函数、请求校验与独立目录结构，不调用外部API。原联合研究的24项检查覆盖当时本地完整输入和缓存；它们不是本仓库重新执行了所有医学或媒体基准的证明。

旧实验曾遇到磁盘满，少量返回结果未保存，后续重跑缺失项。费用只统计最终被引用的成功响应，不代表完整账单。公开数据可能存在闭源模型训练暴露，跨条件的相关样本不能合并成总体临床/商业准确率。

## 医疗数据适配

- `download_sources.py`：第一轮固定Git blob的公开文件；需要GitHub与源站可达，不处理受限申请。
- `benchmark.py prepare`：IMCS、NLI4CT、MTS、MEDEC等首轮任务；它不会自动重建全部后续任务。
- `prepare_*.py`：各扩展数据的适配；文件名、金标字段、选择规则和下载镜像见代码及results里的来源说明。
- `analyze_results.py`：对医疗准备文件和成功响应逐任务评分。
- `analyze_ablations.py`：300条配对扰动、BMI链路和用药基线。
- `run_asr.py` / `run_ocr.py`：需要本地音频、权重、Tesseract及对应输入元数据。

示例：

```sh
python3 scripts/download_sources.py
python3 scripts/benchmark.py prepare --n 100
python3 scripts/prepare_extended.py
python3 scripts/live_batch.py --input data/extended_prepared.jsonl --max-calls 1000
python3 scripts/analyze_results.py
```

额外parquet/medspaCy/ASR依赖在`requirements-optional.txt`。各数据集必须按来源分别获取，不能用其他版本替换后仍宣称复现原快照。自编挑战、PriMock字段与OCR文档类型没有独立医生金标。未运行的资源保留在覆盖账本中。

EvidenceBench有37条历史哈希绑定修正：准备阶段整数键经过JSON序列化变成字符串，排序不同；最终按实际发送格式校正索引，响应未改变。见`results/hash_normalization_audit.json`。


## 更新场景目录与 README 统计

`results/medical_catalog.json` 保存全部资源来源、状态与任务映射；`results/scenario_manifest.json` 保存场景归属和人工撰写的结果摘要。修改快照或场景后运行：

```sh
python3 scripts/build_scenario_report.py
python3 scripts/build_scenario_report.py --check
```

脚本从 `all_results.json`、`ablations.json` 和 `snapshot.json` 生成 README 中标记范围内的分场景表，以及 `docs/场景数据集与实验.md`。它检查全部资源恰好归属一个场景、全部主评测任务无遗漏、任务去重后的记录/API/空预测总数与快照一致。人工摘要与实验解释仍需随结果变化复核。CI 使用 `--check` 防止生成文档过期；这不会调用 API 或重跑医疗评测。
