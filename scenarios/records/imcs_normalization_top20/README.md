# 中文症状术语归一化

任务 ID：`imcs_normalization_top20` · 场景：[ 病历实体、否定状态与术语标准化 ](../README.md)

| 记录数 | 来源 group 数 | API 响应 | 程序空预测 | 指标 | 结果 |
| ---: | ---: | ---: | ---: | --- | ---: |
| 100 | 92 | 100 | 0 | Accuracy | **93.0%** |

## 和 DeepSeek 同题比较

| 项目 | Jev | DeepSeek V4.1 Flash（非思考） |
| --- | ---: | ---: |
| Accuracy | 93.0% | 92.0% |
| 最终未能按要求作答 | 0 | 0 |
| 成功请求典型等待（中位数） | 0.90 秒 | 0.52 秒 |
| 每千条 API 费用估算 | $0.037 | $0.049 |

同一批输入与金标，Jev 使用历史真实响应，DeepSeek 使用本次非思考模式调用；不是同期测速。费用单位美元，含留存的重试用量；不含 OCR、语音识别和人工。

[DeepSeek 原始回答](comparison/deepseek_responses.jsonl) · [本任务对比结果](comparison/results.json) · [完整对比方法](../../../comparisons/deepseek-flash/README.md)

## Jev 如何评测

候选由训练集别名频次与固定术语表字符相似度排序，取前 20 项并加入 __none__；输入句子和目标片段，Choice 选择标准名；金标不在候选也保留计分。

实际模型为 `jev-1.13.0`。92 个 group 是数据源分组标识，不能直接当作独立患者数。

请求仅发送 `sample.request` 中的 `state` 和 `questions`，另添加模型名。`gold` 与 `metadata` 留在本地用于评分，不发送给模型。

### 输入与问题结构

- 输入字段：`sentence, target_mention`。
- 问题类型与总数：`choice` 100 个。
- 去重后的完整问题对象：47 种，见 [prompts.json](prompts.json)，包含原文提示词及实际选项。

### 实际提示词

以下展示归档中首个问题对象，原文未改写。动态候选、其他问题与选项变体均保存在 prompts.json；逐样本对应关系保存在 samples.jsonl。

```json
{
  "criteria": {
    "EB病毒感染": "归一化症状：EB病毒感染",
    "__none__": "候选列表没有正确标准名称",
    "上呼吸道感染": "归一化症状：上呼吸道感染",
    "上火": "归一化症状：上火",
    "下呼吸道感染": "归一化症状：下呼吸道感染",
    "中毒性脑病": "归一化症状：中毒性脑病",
    "中等度热": "归一化症状：中等度热",
    "中耳炎": "归一化症状：中耳炎",
    "乏力": "归一化症状：乏力",
    "乳糖不耐受": "归一化症状：乳糖不耐受",
    "呼吸困难": "归一化症状：呼吸困难",
    "呼吸急促": "归一化症状：呼吸急促",
    "呼吸衰竭": "归一化症状：呼吸衰竭",
    "呼吸道感染": "归一化症状：呼吸道感染",
    "啰音": "归一化症状：啰音",
    "声音嘶哑": "归一化症状：声音嘶哑",
    "急性上呼吸道感染": "归一化症状：急性上呼吸道感染",
    "痰鸣音": "归一化症状：痰鸣音",
    "粗呼吸音": "归一化症状：粗呼吸音",
    "粗糙呼吸音": "归一化症状：粗糙呼吸音",
    "肠鸣音": "归一化症状：肠鸣音"
  },
  "instructions": "将 target_mention 映射为标准症状。不要增加新诊断。候选不正确时选择 __none__。",
  "type": "choice"
}
```

### 金标与计分

读取 response.answers.decision.choice，与 gold 做精确标签比较。Accuracy = 标签正确记录数 / 全部计分记录数；不同病例的多个字段或配对条件不合并成独立患者。

金标分布：`中等度热`：1，`低热`：1，`出汗`：1，`发热`：14，`呃逆`：1，`呕吐`：4，`呼吸道感染`：1，`咳嗽`：18，`咽喉炎`：1，`哭闹`：2，`大便粘液`：1，`头痛`：1，`干咳`：2，`感冒`：6，`扁桃体炎`：1，`支原体感染`：1，`支气管炎`：1，`消化不良`：3，`生理性黄疸`：1，`畏寒`：1，`病毒感染`：3，`痰`：4，`痰鸣音`：1，`皮疹`：1，`稀便`：5，`细菌感染`：2，`肠炎`：1，`肺炎`：2，`脱水`：2，`腹泻`：7，`蛋花汤样便`：1，`血便`：1，`过敏体质`：1，`高热`：1，`黄疸`：2，`鼻流涕`：4。

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

原始适配元数据：

- given_gold_span; candidates from train aliases + fixed vocabulary only

原准备分片：`prepared.jsonl`。

## 关联实验

- [规则／候选基线](baseline.json)
