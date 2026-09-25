# 中医证型多选

任务 ID：`tcm_best_syndrome_multi` · 场景：[ 中医知识、辨证与安全 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 32 | 32 | 32 | 0 | micro-F1 | **52.8%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| micro-F1 | 52.8% | 36.7% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.65 秒 | 0.59 秒 |
| 每千条 API 费用估算 | $0.036 | $0.110 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

辨证病例仅保留 ID 可被 3 整除的行，解析对应维度选项及答案；病例输入不包含诊断解释；按金标答案个数拆成单选与多选，每项 NOUL、0.5 阈值，比较答案集合。

实际模型为 `jev-1.13.0`。32 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`完整文本字符串`。
- 问题类型与总数：`noul` 319 个。
- 去重后的完整问题对象：232 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "instructions": "根据病例判断该选项是否是正确的证型。 Candidate: 阴暑",
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

数据适配：[ prepare_additional.py ](../../../scripts/prepare_additional.py)；实际调用：[live_batch.py](../../../scripts/live_batch.py)；原计分：[analyze_results.py](../../../scripts/analyze_results.py)。

## 来源与实验范围

- [TCM-BEST4SDT](https://github.com/DYJG-research/TCM-BEST4SDT)：知识/伦理/安全与SDT多维；安全金标存在明显过度拒绝倾向。

原始适配元数据：

- TCM-BEST4SDT SDT multilabel, threshold0.5

原准备分片：`additional_prepared.jsonl`。

## 关联实验

- [逐案例输入片段、成绩与来源分组](cases.md)
