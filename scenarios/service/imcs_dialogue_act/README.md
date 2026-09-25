# 中文问诊对话行为分类

任务 ID：`imcs_dialogue_act` · 场景：[ 患者咨询、服务路由与就医流程 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 95 | 100 | 0 | Accuracy | **70.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 70.0% | 68.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.90 秒 | 0.54 秒 |
| 每千条 API 费用估算 | $0.033 | $0.042 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

从 IMCS 开发集按固定哈希抽取 100 个话轮；输入当前话轮及最多两个前文话轮，Choice 在固定对话行为标签中选一项，对照原始 dialogue_act。

实际模型为 `jev-1.13.0`。95 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`context, target`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "Diagnose": "给出诊断",
    "Inform-Basic_Information": "提供基本信息",
    "Inform-Drug_Recommendation": "提供用药建议",
    "Inform-Etiology": "解释病因",
    "Inform-Existing_Examination_and_Treatment": "提供已进行的检查治疗",
    "Inform-Medical_Advice": "提供就医或处理建议",
    "Inform-Precautions": "告知注意事项",
    "Inform-Symptom": "告知症状",
    "Other": "其他对话行为",
    "Request-Basic_Information": "询问年龄等基本信息",
    "Request-Drug_Recommendation": "请求用药建议",
    "Request-Etiology": "询问病因",
    "Request-Existing_Examination_and_Treatment": "询问已进行的检查治疗",
    "Request-Medical_Advice": "请求就医或处理建议",
    "Request-Precautions": "询问注意事项",
    "Request-Symptom": "询问症状"
  },
  "instructions": "只判断 target 这一轮的主要对话行为。context 仅帮助理解。",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`Diagnose`：3，`Inform-Basic_Information`：3，`Inform-Drug_Recommendation`：5，`Inform-Etiology`：3，`Inform-Existing_Examination_and_Treatment`：8，`Inform-Medical_Advice`：7，`Inform-Precautions`：2，`Inform-Symptom`：7，`Other`：39，`Request-Basic_Information`：5，`Request-Drug_Recommendation`：2，`Request-Etiology`：2，`Request-Existing_Examination_and_Treatment`：1，`Request-Medical_Advice`：3，`Request-Symptom`：10。

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

原准备分片：`prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)
- [新增材料与逐案例对照](paired-expanded/README.md)
