# 中文症状肯否定状态

任务 ID：`imcs_assertion_oracle_span` · 场景：[ 病历实体、否定状态与术语标准化 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 91 | 100 | 0 | Accuracy | **79.0%** |

## Jev 如何评测

输入主诉、完整对话、目标话轮和已给定症状片段；Choice 判断明确否定、明确肯定或仍无法确定，对照 symptom_type。使用完整对话回顾性判断。

实际模型为 `jev-1.13.0`，历史实验日期为 2026-09-24。91 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`dialogue, self_report, target_mention, target_turn`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "0": "明确否定该症状",
    "1": "明确肯定该症状",
    "2": "根据完整对话仍无法确定"
  },
  "instructions": "根据完整对话，判断 target_turn 的 target_mention 对该患者的症状状态。医生询问本身不表示阳性，需看回答。",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`0`：10，`1`：75，`2`：15。

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

数据适配：[ benchmark.py ](../../../scripts/benchmark.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [IMCS21](https://github.com/lemuria-wchen/imcs21)：按实际任务适配与抽样完成，非全数据/临床验证。

原始适配元数据：

- given_gold_span; full-dialogue retrospective status, not online triage

原准备分片：`prepared.jsonl`。

## 配对鲁棒性实验

| 变体 | 样本数 | 预测改变 | 原条件正确 | 扰动后正确 |
| --- | ---: | ---: | ---: | ---: |
| [重复调用](robustness/repeat/README.md) | 20 | 0 | 16 | 16 |
| [选项标签轮换](robustness/rotate/README.md) | 20 | 0 | 16 | 16 |
| [无关说明](robustness/irrelevant/README.md) | 20 | 0 | 16 | 16 |
