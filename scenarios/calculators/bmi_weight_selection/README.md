# BMI 当前体重参数选择

任务 ID：`bmi_weight_selection` · 场景：[ 临床计算、参数选择与评分量表 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 20 | 20 | 20 | 0 | Accuracy | **95.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 95.0% | 90.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.63 秒 | 0.49 秒 |
| 每千条 API 费用估算 | $0.043 | $0.111 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

全部 20 个 BMI 病例，使用数值与单位正则构造体重候选；Choice 选择属于当前患者／当前时点的体重或 unknown，对照参考体重；身高与体重两次判断来自同一病例。

实际模型为 `jev-1.13.0`。20 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`choice` 20 个。
- 去重后的完整问题对象：20 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "0": "**正常。\n\n查体:\n\n婚前体重105斤，现体重130斤，身高1",
    "1": "体:\n\n婚前体重105斤，现体重130斤，身高162厘米，脸部痤",
    "unknown": "病历中没有可可靠选取的当前测量值"
  },
  "instructions": "选择用于计算当前BMI的体重记录；排除历史值和其他人物的值，不补造数据。",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`0`：15，`1`：4，`unknown`：1。

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

数据适配：[ prepare_clinical_extra.py ](../../../scripts/prepare_clinical_extra.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [CMedCalc-Bench](https://github.com/Zhihong-Zhu/CMedCalc-Bench)：充分性、分级与20条BMI选择＋公式；不是全部数值指标原始成绩。

原始适配元数据：

- all20 BMI cases; exact numeric-unit regex candidates

原准备分片：`clinical_extra_prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)
- [BMI 参数选择与程序公式联合实验](hybrid.json)
