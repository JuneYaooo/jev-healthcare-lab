# OCR 文本医疗文档类型识别

任务 ID：`clinocr_ocr_doctype` · 场景：[ 语音病历、医疗文档 OCR 与报告断言 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 6 | 2 | 6 | 0 | Accuracy | **83.3%** |

## Jev 如何评测

ClinOCR 六种失真各一份文件，仅两个内容模板；输入 Tesseract 实际识别文本，Choice 在七个文档类型（含 unknown）中选择；金标由模板内容人工定义。

实际模型为 `jev-1.13.0`，历史实验日期为 2026-09-24。2 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`choice` 6 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "billing": "Billing/insurance document",
    "discharge": "Discharge summary",
    "lab": "Laboratory result",
    "medication_list": "Medication list/reconciliation",
    "radiology": "Radiology report",
    "referral": "Referral letter",
    "unknown": "Unreadable or none of these"
  },
  "instructions": "Classify this document by its primary clinical purpose.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`medication_list`：2，`radiology`：4。

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

- [ClinOCR-Bench](https://github.com/ClinOCR-Bench/ClinOCR-Bench)：6类失真文档，实际Tesseract；只有2种模板内容，后续只测文档类型。

原始适配元数据：

- one eval doc per artifact; manually derived doc-type gold from reference; not full OCR benchmark

原准备分片：`final_tasks_prepared.jsonl`。

## 关联实验

- [实际上游音频／图像／转写文件及哈希](upstream/manifest.json)
- [OCR／ASR 上游指标](upstream/results.json)
