# medspaCy 候选与 Jev 疾病实体筛选

任务 ID：`ncbi_medspacy_jev_ner` · 场景：[ 病历实体、否定状态与术语标准化 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 100 | 100 | 0 | micro-F1 | **69.4%** |

## Jev 如何评测

NCBI 官方 test 固定取 100 篇，medspaCy 1.3.1 使用仅训练集词典构造候选；每个候选跨度 NOUL 判断完整疾病实体，阈值 0.5，与所有金标跨度严格比较；疾病类别合并。

实际模型为 `jev-1.13.0`，历史实验日期为 2026-09-24。100 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`noul` 1063 个。
- 去重后的完整问题对象：1048 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "instructions": "Is the target mention a disease/disease class or disease modifier in this abstract? Evaluate only this occurrence, not whether the patient currently has it. Target 'AS' at character range [1025,1027).",
  "type": "noul"
}
```

### 金标与计分

选择 NOUL ≥ 0.5 的问题键形成预测集合，和 gold 集合严格比较。跨样本汇总 TP、FP、FN，micro-F1 = 2TP / (2TP + FP + FN)；不对每行 F1 简单平均。

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

数据适配：[ prepare_medspacy.py ](../../../scripts/prepare_medspacy.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [NCBI Disease](https://www.ncbi.nlm.nih.gov/CBBresearch/Dogan/DISEASE/)：同时完成给定实体分类与medspaCy候选→Jev端到端严格跨度评价。
- [medspaCy](https://github.com/medspacy/medspacy)：已实际安装medspaCy1.3.1并在100篇NCBI测试摘要运行；仅词典target matcher。

原始适配元数据：

- official NCBI test100docs; training-only lexical candidates via medspaCy; strict span detection collapsed disease category

原准备分片：`medspacy_prepared.jsonl`。

## 关联实验

- [规则／候选基线](baseline.json)
