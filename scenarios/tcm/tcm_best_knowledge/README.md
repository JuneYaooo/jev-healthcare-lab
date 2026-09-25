# 中医基础知识单选

任务 ID：`tcm_best_knowledge` · 场景：[ 中医知识、辨证与安全 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 89 | 89 | 89 | 0 | Accuracy | **91.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 91.0% | 83.1% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.63 秒 | 0.51 秒 |
| 每千条 API 费用估算 | $0.016 | $0.040 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

使用发布客观题的一次运行结果；按金标答案个数拆成单选与多选，Choice 选择原始选项，对照原始答案。

实际模型为 `jev-1.13.0`。89 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`choice` 89 个。
- 去重后的完整问题对象：88 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "A": "散风除湿，宣痹止痛",
    "B": "疏风通络，散寒除湿",
    "C": "发汗祛湿，兼清里热",
    "D": "疏风清热，宣痹止痛",
    "E": "发汗解表，祛风胜湿"
  },
  "instructions": "选择题目的最佳答案。",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`A`：15，`B`：22，`C`：22，`D`：22，`E`：8。

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

数据适配：[ prepare_additional.py ](../../../scripts/prepare_additional.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [TCM-BEST4SDT](https://github.com/DYJG-research/TCM-BEST4SDT)：知识/伦理/安全与SDT多维；安全金标存在明显过度拒绝倾向。

原始适配元数据：

- TCM-BEST4SDT objective items; one pass not official three-repeat metric

原准备分片：`additional_prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)
