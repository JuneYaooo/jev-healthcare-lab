# 中文词典候选实体抽取

任务 ID：`imcs_ner_dictionary_pipeline` · 场景：[ 病历实体、否定状态与术语标准化 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 92 | 57 | 43 | micro-F1 | **59.5%** |

## Jev 如何评测

训练集实体构成词典，在开发集句子中精确匹配所有候选跨度；每个候选一个 Choice，选择实体类型或 none；将非 none 预测还原为 (start,end,type)，与全部金标跨度严格比较。43 条无候选样本输出空集并计入漏检。

实际模型为 `jev-1.13.0`。92 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`sentence`。
- 问题类型与总数：`choice` 193 个。
- 去重后的完整问题对象：182 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "Drug": "具体药品名称",
    "Drug_Category": "药物类别而非具体药品",
    "Medical_Examination": "医学检查检验",
    "Operation": "医疗操作",
    "Symptom": "症状或临床表现",
    "none": "不是完整医疗实体"
  },
  "instructions": "判断 sentence 中 [3,5) 的候选片段“炎症”是否是完整医疗实体。边界不完整或不是实体选 none。",
  "type": "choice"
}
```

### 金标与计分

逐候选读取 Choice；去除 none 后，将候选起止位置与预测类型组合成 (start,end,type) 集合。严格匹配全部 gold 跨度，汇总 TP、FP、FN 计算 micro-F1。无候选的 43 条记录输出空集，未调用 API；金标仍计入 FN。

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

- [规则／候选基线](baseline.json)
