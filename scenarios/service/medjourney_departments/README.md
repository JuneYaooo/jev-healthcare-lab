# 主诉推荐就诊科室

任务 ID：`medjourney_departments` · 场景：[ 患者咨询、服务路由与就医流程 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 100 | 100 | 0 | micro-F1 | **36.9%** |

## Jev 如何评测

从发布科室任务固定哈希取 100 条；以全发布目标列构成固定科室词表，每个科室一个 NOUL 问题；阈值 0.5 得到多标签集合，与 target 按分隔符拆出的科室集合比较。

实际模型为 `jev-1.13.0`。100 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`source_prompt`。
- 问题类型与总数：`noul` 11100 个。
- 去重后的完整问题对象：111 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "instructions": "对于所给主诉，中医科是否属于应推荐的就诊科室？判断具体科室是否适合；可以有多个科室，也可以不选。不要仅因科室名与症状共享词就选择。",
  "type": "noul"
}
```

### 金标与计分

将每个 NOUL ≥ 0.5 的问题编号映射到 metadata.label_vocabulary，得到预测标签集合。与 gold 完整标签集合比较；候选外金标仍计为 FN。汇总 TP、FP、FN，micro-F1 = 2TP / (2TP + FP + FN)。

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

数据适配：[ prepare_extended.py ](../../../scripts/prepare_extended.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [MedJourney](https://github.com/Medical-AI-Learning/MedJourney)：按实际任务适配与抽样完成，非全数据/临床验证。

原始适配元数据：

- adapted multilabel fixed inventory from whole public target column; 0.5 threshold; no alias normalization; not official generative metric

原准备分片：`extended_prepared.jsonl`。
