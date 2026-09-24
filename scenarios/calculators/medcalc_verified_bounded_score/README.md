# 五种临床量表闭集数值评分

任务 ID：`medcalc_verified_bounded_score` · 场景：[ 临床计算、参数选择与评分量表 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 100 | 100 | 0 | Accuracy | **25.0%** |

## Jev 如何评测

经 Git blob 校验的 Verified 发布 test CSV；GCS、CURB-65、SIRS、CHA2DS2-VASc、FeverPAIN 各 20 条。输入病历和问题，以各评分全部整数范围加 unknown 构成 Choice；不提供公式、参考参数或解释，对照数值金标。

实际模型为 `jev-1.13.0`。100 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`patient_note, question`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：4 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "unknown": "The patient note lacks information necessary to determine the score"
  },
  "instructions": "Determine the requested clinical score from this patient note. Select its numeric value from the fixed full score range. No reference parameters or explanation are supplied. If essential information is missing, select unknown.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`0`：7，`1`：17，`10`：3，`11`：1，`12`：2，`15`：2，`2`：17，`3`：21，`4`：11，`5`：4，`6`：5，`7`：3，`8`：2，`9`：5。

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

数据适配：[ prepare_medcalc_verified.py ](../../../scripts/prepare_medcalc_verified.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [MedCalc-Bench / Verified](https://github.com/ncbi-nlp/MedCalc-Bench)：Verified发布方CSV通过Git blob校验；5种有界评分各20条，闭集数值选择，不是55种指标全量数值生成。

原始适配元数据：

- MedCalc-Bench-Verified published test CSV via publisher HF mirror;5 full bounded-score calculators x20; converted to closed numeric choice, NOT full55-calculator numerical generation benchmark

原准备分片：`medcalc_verified_prepared.jsonl`。

## 关联实验

- [源数据版本与字节校验](source_verification.json)
