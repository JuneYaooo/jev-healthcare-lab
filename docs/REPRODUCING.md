# 数据使用与复建

Python 3.10+，仅标准库。构建和评分不调用模型 API。

## 使用整理好的数据包

从 [下载页](../releases/README.md) 选择开放核心集或非商业研究附加集，按同页 `SHA256SUMS` 校验下载文件。解压后进入数据包目录：

```bash
python3 tools/medical_decision_release.py verify --dataset .
python3 tools/medical_decision_release.py trace --dataset . --id '完整题目ID'
python3 tools/medical_decision_release.py trace --dataset . --id '完整题目ID' --fetch-source
python3 tools/medical_decision_release.py score --dataset . --predictions predictions.jsonl --output scores.json
```

各包 README 提供一个实际题号；`example-trace.json` 展示该题的完整溯源。`verify` 核验包内文件哈希、题目/答案一致性、来源链和许可分组。`trace` 默认离线；显式传入 `--fetch-source` 才下载该题直接依赖的上游文件，并校验锁定哈希。链接失效或哈希变化会报错。

`requests.jsonl` 可直接用于组织模型请求，`answers.jsonl` 独立保存答案。评分工具只读取预测文件，不发起模型调用。

## 从仓库复建

在仓库根目录执行：

```bash
python3 scripts/medical_decision_dataset.py validate
python3 -m unittest discover -s tests -v
python3 scripts/medical_decision_dataset.py fetch
python3 scripts/medical_decision_dataset.py build
python3 scripts/medical_decision_release.py build
```

`fetch` 下载 `sources.lock.json` 中的固定源文件并检查 SHA-256，缓存位于 `work/decision-benchmark-v1/raw/`。完整原始数据不随压缩包发布。`build` 使用已发布的任务定义、适配器、固定抽样种子和冻结筛查索引重建题目，不调用模型生成答案。复建依赖上游锁定资源仍可下载；本地已有且哈希正确的缓存可复用。

`exposure_index.json` 保存构建时的训练与历史材料指纹。复建当前版本应保留该索引，不运行 `index` 子命令；当前仓库不包含这些历史训练与实验原文。重新筛查其他训练材料属于新版本数据准备，需要重新审核、冻结并标版本。

`medical_decision_release.py build` 生成两个互不重叠的包、发布索引和 SHA256SUMS。归档文件排序与时间戳固定；同一份代码和数据应产生字节一致的包。

## 导出与评分

```bash
python3 scripts/medical_decision_dataset.py export --output work/requests.jsonl
python3 scripts/medical_decision_dataset.py score --predictions work/predictions.jsonl --output work/scores.json
```

默认只处理开放核心集。若使用完整 2,200 题，在上述命令加 `--include-research`，并遵守研究附加来源的许可。独立包内的评分工具自动按该包范围计分。

评分规则见 [评测方法](EVALUATION.md)，来源与许可见 [来源登记](../benchmarks/medical_decision_v1/SOURCES.md)。
