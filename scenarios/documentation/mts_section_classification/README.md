# 问诊对话对应病历章节

任务 ID：`mts_section_classification` · 场景：[ 病历章节、文书质控与随访记录 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 100 | 100 | 0 | Accuracy | **76.0%** |

## Jev 如何评测

固定哈希抽取 MTS 验证集 100 段合成问诊，输入 dialogue，不提供参考病历正文；Choice 从固定章节表选择标签，对照 section_header。

实际模型为 `jev-1.13.0`，历史实验日期为 2026-09-24。100 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`dialogue`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "ALLERGY": "Allergies",
    "ASSESSMENT": "Clinical assessment",
    "CC": "Chief complaint",
    "DIAGNOSIS": "Diagnosis",
    "DISPOSITION": "Disposition",
    "EDCOURSE": "Emergency department course",
    "EXAM": "Physical examination",
    "FAM/SOCHX": "Family or social history",
    "GENHX": "History of present illness or general history",
    "GYNHX": "Gynecologic history",
    "IMAGING": "Imaging",
    "IMMUNIZATIONS": "Immunizations",
    "LABS": "Laboratory results",
    "MEDICATIONS": "Medications",
    "OTHER_HISTORY": "Other history",
    "PASTMEDICALHX": "Past medical history",
    "PASTSURGICAL": "Past surgical history",
    "PLAN": "Plan",
    "PROCEDURES": "Procedures",
    "ROS": "Review of systems"
  },
  "instructions": "Which clinical note section best matches the content of this dialogue?",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`ALLERGY`：4，`ASSESSMENT`：4，`CC`：4，`DIAGNOSIS`：1，`DISPOSITION`：2，`EDCOURSE`：3，`EXAM`：1，`FAM/SOCHX`：22，`GENHX`：20，`GYNHX`：1，`IMAGING`：1，`IMMUNIZATIONS`：1，`LABS`：1，`MEDICATIONS`：7，`OTHER_HISTORY`：1，`PASTMEDICALHX`：4，`PASTSURGICAL`：8，`PLAN`：3，`PROCEDURES`：1，`ROS`：11。

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

- [MTS-Dialog](https://github.com/microsoft/clinical_visit_note_summarization_corpus)：按实际任务适配与抽样完成，非全数据/临床验证。

原始适配元数据：

- synthetic encounters; reference note text excluded from input

原准备分片：`prepared.jsonl`。
