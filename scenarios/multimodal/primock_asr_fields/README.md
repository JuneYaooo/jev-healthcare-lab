# ASR 转写病史字段判断

任务 ID：`primock_asr_fields` · 场景：[ 语音病历、医疗文档 OCR 与报告断言 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 12 | 1 | 12 | 0 | Accuracy | **91.7%** |

## Jev 如何评测

同一段 457.92 秒扮演患者音频；使用 Whisper tiny.en-q5_1 实际转写，完整转写分别搭配 12 个字段 Choice 问题；金标由原实验根据参考文本人工定义，两条件共用金标。

实际模型为 `jev-1.13.0`，历史实验日期为 2026-09-24。1 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`choice` 12 个。
- 去重后的完整问题对象：12 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "no": "absent",
    "unknown": "not established",
    "yes": "present"
  },
  "instructions": "Is diarrhea currently present? Only use what this transcript says.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`3`：1，`6_7`：1，`accountant`：1，`left`：1，`low`：1，`no`：5，`yes`：2。

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

数据适配：[ prepare_final_tasks.py ](../../../scripts/prepare_final_tasks.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [PriMock57](https://github.com/babylonhealth/primock57)：一段公开扮演患者音频，真实Whisper转写＋12字段；字段金标由本轮人工定义，非临床评测。

原始适配元数据：

- one patient audio channel;12manually authored field gold from reference; gold reused for ASR propagation, not original published field annotations

原准备分片：`final_tasks_prepared.jsonl`。

## 关联实验

- [实际上游音频／图像／转写文件及哈希](upstream/manifest.json)
- [OCR／ASR 上游指标](upstream/results.json)
