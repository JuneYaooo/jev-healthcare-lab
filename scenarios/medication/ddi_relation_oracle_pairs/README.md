# 给定药物对相互作用分类

任务 ID：`ddi_relation_oracle_pairs` · 场景：[ 药物关系、用药变更与出院带药 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 150 | 77 | 150 | 0 | Accuracy | **79.3%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 79.3% | 74.7% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.91 秒 | 0.53 秒 |
| 每千条 API 费用估算 | $0.024 | $0.038 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

DDI 官方 Test/Extraction 中每类固定哈希取 30 条，共 150；输入句子与两个金标药物片段／偏移；Choice 在 none、mechanism、effect、advise、int 五类中选择。

实际模型为 `jev-1.13.0`。77 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`sentence, target_1, target_2`。
- 问题类型与总数：`choice` 150 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "advise": "Advice, precaution or contraindication about co-use.",
    "effect": "Pharmacodynamic effect or clinical outcome of co-use.",
    "int": "Interaction stated without specifying its kind.",
    "mechanism": "Pharmacokinetic mechanism (e.g. concentration, absorption, metabolism).",
    "none": "No stated interaction between the two target mentions."
  },
  "instructions": "Classify only the relation stated between the two target drug mentions in this sentence, not outside drug knowledge.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`advise`：30，`effect`：30，`int`：30，`mechanism`：30，`none`：30。

## 数据与实验记录

| 文件 | 内容 |
| --- | --- |
| [samples.jsonl](samples.jsonl) | 本任务全部真实评测输入、完整请求、gold、group、适配元数据及请求哈希 |
| [responses.jsonl](responses.jsonl) | 对应的原始成功响应记录；空候选时保留程序输出标记 |
| [prompts.json](prompts.json) | 从真实请求提取的全部问题／提示词／选项变体 |
| [example.json](example.json) | 一条完整实际样本与其对应响应，无合成替换 |
| [results.json](results.json) | 指标、置信区间、逐类表现、校准、token 与延迟 |
| [index.jsonl](index.jsonl) | 样本身份、请求哈希和响应原文件哈希 |
| [provenance.json](provenance.json) | 来源、归档文件哈希与原准备分片 |

通过 `(task, id)` 关联输入、响应与索引；响应哈希针对 JSONL 每行去掉换行分隔符后的原始字节计算。

数据适配：[ prepare_extended.py ](../../../scripts/prepare_extended.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [DDI Corpus](https://github.com/isegura/DDICorpus)：按实际任务适配与抽样完成，非全数据/临床验证。

原始适配元数据：

- official test subset; 30/class; given gold entity pair, not end-to-end NER

原准备分片：`extended_prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)

## 配对鲁棒性实验

| 变体 | 样本数 | 预测改变 | 原条件正确 | 扰动后正确 |
| --- | ---: | ---: | ---: | ---: |
| [重复调用](robustness/repeat/README.md) | 20 | 1 | 16 | 17 |
| [选项标签轮换](robustness/rotate/README.md) | 20 | 1 | 16 | 17 |
| [无关说明](robustness/irrelevant/README.md) | 20 | 1 | 16 | 17 |
