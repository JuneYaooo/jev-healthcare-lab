# 临床量表语义分级

任务 ID：`cmedcalc_semantic_grade` · 场景：[ 临床计算、参数选择与评分量表 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 162 | 162 | 162 | 0 | Accuracy | **60.5%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 60.5% | 39.5% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.89 秒 | 0.61 秒 |
| 每千条 API 费用估算 | $0.027 | $0.046 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

使用全部 162 个语义分级病例；各量表使用预先定义的完整等级并加 unknown；统一罗马数字等标签，Choice 选择等级，对照规范化的 answer_final。

实际模型为 `jev-1.13.0`。162 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`indicator, note`。
- 问题类型与总数：`choice` 162 个。
- 去重后的完整问题对象：10 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "0": "0",
    "1": "1",
    "1+": "1+",
    "2": "2",
    "2+": "2+",
    "2-": "2-",
    "3": "3",
    "3+": "3+",
    "3-": "3-",
    "4": "4",
    "4+": "4+",
    "4-": "4-",
    "5": "5",
    "5-": "5-",
    "unknown": "病历资料不足，不能确定分级"
  },
  "instructions": "按指定指标的分级体系选择最符合病历的级别。仅依据病例资料，不猜测未记录事实。",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`0`：28，`1`：15，`1+`：1，`2`：4，`2+`：1，`2-`：1，`3`：7，`3+`：1，`3-`：1，`4`：5，`4+`：1，`4-`：1，`5`：2，`5-`：1，`A`：3，`B`：2，`C`：2，`D`：2，`E`：1，`I`：22，`II`：11，`III`：8，`III度`：2，`IIa`：2，`IV`：8，`Ia`：1，`Ib`：1，`I度`：3，`中度活动`：10，`极高度活动`：4，`浅II度`：3，`深II度`：2，`高度活动`：6。

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

- all162 public semantic cases; canonicalized labels, no gold explanation; explicit grading not free generation

原准备分片：`extended_prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)

## 配对鲁棒性实验

| 变体 | 样本数 | 预测改变 | 原条件正确 | 扰动后正确 |
| --- | ---: | ---: | ---: | ---: |
| [重复调用](robustness/repeat/README.md) | 20 | 0 | 16 | 16 |
| [选项标签轮换](robustness/rotate/README.md) | 20 | 6 | 16 | 10 |
| [无关说明](robustness/irrelevant/README.md) | 20 | 0 | 16 | 16 |
