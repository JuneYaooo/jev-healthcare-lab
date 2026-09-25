# 出院带药候选筛选

任务 ID：`cdrugred_discharge_candidate_pipeline` · 场景：[ 药物关系、用药变更与出院带药 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 83 | 100 | 0 | micro-F1 | **48.6%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| micro-F1 | 48.6% | 47.9% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.78 秒 | 0.93 秒 |
| 每千条 API 费用估算 | $0.218 | $0.587 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

发布训练池按患者哈希留出约 20%，留出池固定取 100 次就诊；训练共现与先验构造候选，输入病历字段，每药一个 NOUL，0.5 阈值选药；与完整带药金标集合比较，保留候选外漏检。

实际模型为 `jev-1.13.0`。83 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`BMI, 主诉, 入院情况, 出院诊断, 性别, 既往史, 现病史, 诊疗过程描述`。
- 问题类型与总数：`noul` 3254 个。
- 去重后的完整问题对象：172 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "instructions": "根据病历判断是否应列入该次就诊的出院带药列表，排除已停用、过敏禁忌和仅在住院中使用的药。仅离线复现数据集，不给患者治疗建议。候选药物：丹参软胶囊",
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

数据适配：[ prepare_pipeline.py ](../../../scripts/prepare_pipeline.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [CDrugRed / CHIP2025 Task2](https://github.com/bxx-seu/CDrugRed)：官方test无金标；训练发布池按患者hash分离100条holdout，非官方竞赛成绩。

原始适配元数据：

- patient-hash heldout20% of released training data; 100visits; not official test

原准备分片：`pipeline_prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)
- [规则／候选基线](baseline.json)
