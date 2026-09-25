# 中文医学考试多选

任务 ID：`cmexam_mcq_multi` · 场景：[ 医学知识与考试对照 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 20 | 20 | 20 | 0 | micro-F1 | **83.2%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| micro-F1 | 83.2% | 90.3% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.60 秒 | 0.69 秒 |
| 每千条 API 费用估算 | $0.020 | $0.061 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

从 CMExam 官方 test 固定哈希取 100 题后按答案数拆分；输入 Question 和原始选项，每个选项一个 NOUL 问题，阈值 0.5，按金标答案集合计 micro-F1。 补充阶段在完整官方 test 中筛选未使用的多选题，按固定哈希选入 15 道，共 20 道；只使用公开答案，解析与集合评分规则不变。

实际模型为 `jev-1.13.0`。20 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`noul` 95 个。
- 去重后的完整问题对象：95 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "instructions": "判断该候选是否为多选题的正确答案。 Candidate: 抗惊厥",
  "type": "noul"
}
```

### 金标与计分

选择 NOUL ≥ 0.5 的问题键形成预测集合，和 gold 集合严格比较。跨样本汇总 TP、FP、FN，micro-F1 = 2TP / (2TP + FP + FN)；不对每行 F1 简单平均。

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

- [CMExam](https://github.com/williamliujl/CMExam)：按实际任务适配与抽样完成，非全数据/临床验证。

原始适配元数据：

- CMExam official test
- CMExam official test; additional multiselect items selected by stable hash before model calls

原准备分片：`additional_prepared.jsonl`。
