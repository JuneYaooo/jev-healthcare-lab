# 英文 MedQA医学考试

任务 ID：`medqa_en_test` · 场景：[ 医学知识与考试对照 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 100 | 100 | 0 | Accuracy | **83.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 83.0% | 78.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.62 秒 | 0.61 秒 |
| 每千条 API 费用估算 | $0.024 | $0.053 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

从发布数据镜像对应 split 固定哈希抽取 100 题；输入 question 与原始选项，Choice 单选，对照发布答案索引。MedMCQA 即使标记 multi 也按发布的单个 cop 计分。

实际模型为 `jev-1.13.0`。100 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：100 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "A": "Sympathetic underactivity",
    "B": "Anti-thyroglobin antibodies",
    "C": "Exophthalmos",
    "D": "Increased TSH release",
    "E": "Multinucleate giant cells present in the thyroid"
  },
  "instructions": "Select the best answer supported by the supplied question or article. For trial outcomes, compare the specified intervention against the specified comparator.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`A`：21，`B`：18，`C`：22，`D`：17，`E`：22。

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

数据适配：[ prepare_last_datasets.py ](../../../scripts/prepare_last_datasets.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [MedQA](https://github.com/jind11/MedQA)：按实际任务适配与抽样完成，非全数据/临床验证。

原始适配元数据：

- HF public mirror of published medqa-en-test
- MedMCQA released cop is one answer index even when choice_type says multi; scored as published MCQ, not multiselect

原准备分片：`last_datasets_prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)
