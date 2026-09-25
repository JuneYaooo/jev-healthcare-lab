# OCR 文本医疗文档类型识别

任务 ID：`clinocr_ocr_doctype` · 场景：[ 语音病历、医疗文档 OCR 与报告断言 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 20 | 16 | 20 | 0 | Accuracy | **95.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 95.0% | 85.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.63 秒 | 0.55 秒 |
| 每千条 API 费用估算 | $0.037 | $0.088 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

共 20 张公开 ClinOCR-Bench 扫描图，覆盖 16 个文档模板：保留原来的 6 张失真样本，另从 normal/tables 官方测试分片选取此前未覆盖的 14 个模板各一张。使用 Tesseract English --psm 3 实际识别，并以参考文本作为对照。文档类型金标按参考文档主要用途人工映射；补充题明确将病理报告归入 lab、术后离院指导归入 discharge、其他病史表/临床记录归入 unknown。扫描图及参考、OCR 文本全部保留；不同扫描版本不等于独立患者。

实际模型为 `jev-1.13.0`。16 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`choice` 20 个。
- 去重后的完整问题对象：2 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

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

金标分布：`discharge`：1，`lab`：5，`medication_list`：2，`radiology`：4，`referral`：1，`unknown`：7。

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

数据适配：[ prepare_media_expansion.py ](../../../scripts/prepare_media_expansion.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [ClinOCR-Bench](https://github.com/ClinOCR-Bench/ClinOCR-Bench)：20 张扫描文档、16 个模板；Tesseract 实际 OCR 与参考文本对照，评测文档类型。

原始适配元数据：

- ClinOCR-Bench official test, one additional scan for each previously unrepresented template; doc-type gold manually mapped from reference purpose
- one eval doc per artifact; manually derived doc-type gold from reference; not full OCR benchmark

原准备分片：`final_tasks_prepared.jsonl`。

## 关联实验

- [实际上游音频／图像／转写文件及哈希](upstream/manifest.json)
- [OCR／ASR 上游指标](upstream/results.json)
