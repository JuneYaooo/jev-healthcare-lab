# 合成病例主要诊断

任务 ID：`ddxplus_synthetic_primary` · 场景：[ 合成病例主要诊断 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 100 | 100 | 0 | Accuracy | **67.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 67.0% | 71.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.69 秒 | 0.58 秒 |
| 每千条 API 费用估算 | $0.072 | $0.095 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

原始站点访问失败后使用第三方镜像 test.csv 前 1 MiB 的 1,574 条完整记录，固定抽 100 条；输入已出现的症状，Choice 在 49 个病种中选主要诊断；非全量测试分布。

实际模型为 `jev-1.13.0`。100 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`age, observed_positive_or_categorical_findings, sex`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "0": "Acute COPD exacerbation / infection",
    "1": "Acute dystonic reactions",
    "10": "Boerhaave",
    "11": "Bronchiectasis",
    "12": "Bronchiolitis",
    "13": "Bronchitis",
    "14": "Bronchospasm / acute asthma exacerbation",
    "15": "Chagas",
    "16": "Chronic rhinosinusitis",
    "17": "Cluster headache",
    "18": "Croup",
    "19": "Ebola",
    "2": "Acute laryngitis",
    "20": "Epiglottitis",
    "21": "GERD",
    "22": "Guillain-Barré syndrome",
    "23": "HIV (initial infection)",
    "24": "Influenza",
    "25": "Inguinal hernia",
    "26": "Larygospasm",
    "27": "Localized edema",
    "28": "Myasthenia gravis",
    "29": "Myocarditis",
    "3": "Acute otitis media",
    "30": "PSVT",
    "31": "Pancreatic neoplasm",
    "32": "Panic attack",
    "33": "Pericarditis",
    "34": "Pneumonia",
    "35": "Possible NSTEMI / STEMI",
    "36": "Pulmonary embolism",
    "37": "Pulmonary neoplasm",
    "38": "SLE",
    "39": "Sarcoidosis",
    "4": "Acute pulmonary edema",
    "40": "Scombroid food poisoning",
    "41": "Spontaneous pneumothorax",
    "42": "Spontaneous rib fracture",
    "43": "Stable angina",
    "44": "Tuberculosis",
    "45": "URTI",
    "46": "Unstable angina",
    "47": "Viral pharyngitis",
    "48": "Whooping cough",
    "5": "Acute rhinosinusitis",
    "6": "Allergic sinusitis",
    "7": "Anaphylaxis",
    "8": "Anemia",
    "9": "Atrial fibrillation"
  },
  "instructions": "Choose the most likely primary pathology in this synthetic DDXPlus record from the full disease vocabulary. Only recorded positive/categorical findings are given; no gold differential diagnoses or probabilities are supplied.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`0`：2，`1`：1，`10`：1，`11`：1，`13`：3，`14`：1，`15`：1，`16`：2，`2`：3，`20`：3，`21`：5，`22`：7，`23`：4，`24`：4，`25`：3，`26`：1，`27`：2，`29`：1，`3`：2，`31`：2，`32`：1，`33`：2，`34`：1，`35`：2，`36`：3，`37`：1，`38`：1，`39`：2，`4`：1，`42`：2，`43`：4，`44`：4，`45`：8，`46`：3，`47`：4，`6`：1，`7`：2，`8`：7，`9`：2。

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

数据适配：[ prepare_ddxplus.py ](../../../scripts/prepare_ddxplus.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [DDXPlus](https://github.com/mila-iqia/ddxplus)：第三方HF镜像test前1MiB中的1574条完整记录固定抽100，49病种；原始Figshare403，非完整官方测试分布。

原始适配元数据：

- Published English evidence translations retained, including awkward word choices; only observed findings, not full negative evidence expansion
- Third-party HF mirror aai530-group6/ddxplus test.csv first1MiB; stable100 sampled complete prefix records; original Figshare403; not whole official test distribution or verified primary bytes

原准备分片：`ddxplus_prepared.jsonl`。

## 关联实验

- [源数据版本与字节校验](source_verification.json)
