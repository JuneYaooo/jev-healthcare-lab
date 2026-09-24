# 医学缩写消歧

任务 ID：`medal_demo_disambiguation` · 场景：[ 病历实体、否定状态与术语标准化 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 34 | 100 | 0 | Accuracy | **67.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 67.0% | 35.0% |
| 最终未能按要求作答 | 0 | 17 |
| 成功请求典型等待（中位数） | 0.67 秒 | 0.58 秒 |
| 每千条 API 费用估算 | $0.116 | $0.082 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

取发布演示 CSV 前 100 行，候选为整个 demo 的扩展词表；输入摘要、目标 token 及位置，Choice 选扩展词，对照 LABEL；不是完整 MedAL 独立测试。

实际模型为 `jev-1.13.0`。34 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`abstract, target_token, target_token_position_zero_based`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：1 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "0": "acetone",
    "1": "acetyltransferase",
    "10": "alkaline",
    "100": "pentose phosphate pathway",
    "101": "phosphate buffer",
    "102": "photosystem",
    "103": "picrotoxin",
    "104": "pnitrophenol",
    "105": "polyacrylamide gel electrophoresis",
    "106": "polymer",
    "107": "preparations",
    "108": "pretreatment",
    "109": "proteases",
    "11": "alone",
    "110": "red cells",
    "111": "redistribution",
    "112": "respiration",
    "113": "reticular",
    "114": "secondary",
    "115": "serum",
    "116": "sites",
    "117": "slope",
    "118": "slow myosin",
    "119": "smooth endoplasmic reticulum",
    "12": "amino acid",
    "120": "specific",
    "121": "spleen",
    "122": "spontaneously hypertensive",
    "123": "stable",
    "124": "strain",
    "125": "study",
    "126": "substrate",
    "127": "subunit",
    "128": "sucrose density gradient",
    "129": "symptoms",
    "13": "arginine",
    "130": "synaptic vesicles",
    "131": "tissue culture",
    "132": "transition state",
    "133": "transitions",
    "134": "tritiated",
    "135": "trypsin",
    "136": "turning point",
    "137": "tyrosine",
    "138": "ultracentrifugation",
    "139": "variation",
    "14": "arsenic",
    "140": "ventral",
    "141": "ventricular",
    "142": "vesicles",
    "15": "assay",
    "16": "binding",
    "17": "blood serum",
    "18": "brain",
    "19": "brain stem",
    "2": "activated",
    "20": "cancer",
    "21": "carcinosarcoma",
    "22": "casein",
    "23": "casein kinases",
    "24": "caudate",
    "25": "cb",
    "26": "cerebral",
    "27": "cervical",
    "28": "change",
    "29": "common bile duct",
    "3": "activation energies",
    "30": "complete",
    "31": "compounds",
    "32": "conditioned",
    "33": "correlation",
    "34": "cortex",
    "35": "crude extract",
    "36": "crude synaptosomal",
    "37": "detection",
    "38": "development",
    "39": "dihydrofolate",
    "4": "active",
    "40": "distribution",
    "41": "duodenal",
    "42": "effective",
    "43": "electrical activity",
    "44": "electromagnetic",
    "45": "electrophoresis",
    "46": "energy",
    "47": "enriched",
    "48": "enzyme activity",
    "49": "erythrocyte",
    "5": "activities",
    "50": "experimental",
    "51": "exposure",
    "52": "extracellular fluid",
    "53": "extraction",
    "54": "factors",
    "55": "fatty acid",
    "56": "fatty acid synthetase",
    "57": "feeding",
    "58": "function",
    "59": "functioning",
    "6": "actomyosin",
    "60": "glucose",
    "61": "glutamate",
    "62": "groups",
    "63": "guanosine cyclic monophosphate",
    "64": "hyperglycemia",
    "65": "hypotension",
    "66": "hypothermia",
    "67": "inhibitory",
    "68": "intrinsic activity",
    "69": "invertase",
    "7": "affinity chromatography",
    "70": "large",
    "71": "layer",
    "72": "levels",
    "73": "light",
    "74": "line",
    "75": "live weight",
    "76": "liver",
    "77": "major",
    "78": "mean arterial",
    "79": "membrane conductance",
    "8": "after",
    "80": "membranebound",
    "81": "membranes",
    "82": "michaelis constant",
    "83": "midpoint",
    "84": "model",
    "85": "motoneurons",
    "86": "myocardial blood flow",
    "87": "myosin",
    "88": "myosin light chains",
    "89": "nervous system",
    "9": "albumin",
    "90": "neurons",
    "91": "nicotine",
    "92": "nitrofurazone",
    "93": "nterminal",
    "94": "oligosaccharides",
    "95": "onset",
    "96": "operation",
    "97": "output",
    "98": "oxygen affinity",
    "99": "pattern"
  },
  "instructions": "Select the intended expansion of the target abbreviation in this abstract.",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`1`：2，`10`：1，`100`：1，`102`：1，`107`：2，`11`：1，`110`：4，`111`：1，`114`：1，`116`：1，`12`：1，`120`：2，`123`：1，`124`：1，`126`：2，`13`：1，`131`：1，`132`：1，`133`：2，`134`：2，`137`：1，`138`：1，`139`：1，`141`：1，`15`：1，`16`：5，`18`：1，`2`：1，`21`：1，`24`：1，`3`：1，`31`：2，`38`：1，`39`：2，`4`：5，`40`：2，`42`：1，`45`：3，`46`：1，`47`：1，`5`：4，`50`：1，`54`：1，`57`：1，`58`：1，`61`：3，`62`：2，`64`：2，`66`：1，`67`：1，`7`：1，`72`：1，`74`：1，`75`：1，`76`：2，`77`：2，`8`：4，`81`：2，`84`：1，`86`：1，`91`：2，`95`：1，`99`：2。

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

数据适配：[ prepare_evidence.py ](../../../scripts/prepare_evidence.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [MedAL](https://github.com/BruceWen120/medal)：仅100条发布方演示样本；不是独立测试集。

原始适配元数据：

- first100 published toy rows; full-demo expansion vocabulary, not held-out full MedAL performance

原准备分片：`evidence_prepared.jsonl`。
