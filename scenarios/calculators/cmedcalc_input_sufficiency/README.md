# 临床计算输入充分性

任务 ID：`cmedcalc_input_sufficiency` · 场景：[ 临床计算、参数选择与评分量表 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 200 | 200 | 200 | 0 | Accuracy | **81.5%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 81.5% | 84.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.93 秒 | 0.55 秒 |
| 每千条 API 费用估算 | $0.043 | $0.078 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

从原无答案池与可回答池分别固定哈希取 100 条；输入指标名称及病历，Choice 判断 sufficient/insufficient；不发送参考参数和答案。

实际模型为 `jev-1.13.0`。200 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`indicator, note`。
- 问题类型与总数：`choice` 200 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "insufficient": "缺失必要资料或有未解决矛盾，不能可靠计算或分级",
    "sufficient": "必要资料完整且不矛盾，可以计算或分级"
  },
  "instructions": "只判断病历是否提供了计算/分级该指标所必需且不矛盾的资料。不要编造缺失参数。正常知识可以用于理解指标，但不能替代患者资料。",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`insufficient`：100，`sufficient`：100。

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

- [CMedCalc-Bench](https://github.com/Zhihong-Zhu/CMedCalc-Bench)：充分性、分级与20条BMI选择＋公式；不是全部数值指标原始成绩。

原始适配元数据：

- adapted binary gate; 100 original unanswerable +100 original answerable; not original numerical score

原准备分片：`extended_prepared.jsonl`。
