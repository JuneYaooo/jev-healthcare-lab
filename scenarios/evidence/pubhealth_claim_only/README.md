# 公共卫生核查：仅论断

任务 ID：`pubhealth_claim_only` · 场景：[ 循证研究、PICO 与公共卫生核查 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 100 | 100 | 0 | Accuracy | **20.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 20.0% | 44.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.77 秒 | 0.55 秒 |
| 每千条 API 费用估算 | $0.016 | $0.033 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

从发布方 test 镜像固定抽 100 个历史论断；只给 claim，排除 explanation；Choice 对照历史标签。两条件为同题配对，文章可能直接写出结论。

实际模型为 `jev-1.13.0`。100 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`claim, publication_date`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "0": "False",
    "1": "Mixture of true and false",
    "2": "True",
    "3": "Unproven"
  },
  "instructions": "Classify this historical public-health claim as of the publication date. No retrieval evidence is supplied.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`0`：31，`1`：13，`2`：54，`3`：2。

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

数据适配：[ prepare_pubhealth.py ](../../../scripts/prepare_pubhealth.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [PUBHEALTH](https://github.com/neemakot/Health-Fact-Checking)：100个历史claim双条件；给定事实核查文章不等于实时互联网核查。

原始适配元数据：

- official publisher HF converted test mirrored via hf-mirror,100 paired claims; main_text is a fact-check article not independent raw evidence; explanation excluded; historical labels not current clinical guidance

原准备分片：`pubhealth_prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)
