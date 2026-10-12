# 药物基因结果对应的指南建议选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 输出用药建议，方向适合但为固定指南规则选择，无完整患者记录；应与病例治疗分层而非声称个体处方能力。

## 任务是什么

给定药物、人群及基因结果，选择 CPIC 固定快照中对应的原始用药建议；不外推为完整个体处方。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `pgx_guideline_recommendation` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 资格与适宜性 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 25 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CPIC curated pharmacogenomic tables](../datasets/cpic.md) | 100 | [原始来源](https://www.clinpgx.org/cpic) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | **55.00%** | 100 / 100 | 0.993 | 0.930 | 1.278 | 12.980 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 54.00% | 100 / 100 | **0.492** | **0.449** | **0.740** | **6.775** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 51.00% | 100 / 100 | 1.084 | 1.023 | 1.718 | 13.954 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 39.00% | 100 / 100 | 0.865 | 0.689 | 1.692 | 11.128 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 54.00% | 100 / 100 | 3.176 | 1.820 | 8.361 | 40.282 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

本轮多题结果（固定最大打包档，对比 Flash）：JEV 63.54%，Flash 48.96%；JEV 耗时少 48.8%；JEV 成本低 25.2%–62.6%。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 62.50% | 8.345 | 3.83 / 2.40 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 52.08% | 20.748 | 1.54 / 0.80 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 63.54% | 1.593 | 20.08 / 12.76 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 52.08% | 3.011 | 10.63 / 5.54 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | JEV 1.13 | 62.50% | 11.021 | 2.90 / 1.81 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 52.08% | 1.374 | 23.04 / 12.13 | 95 / 96 | 1 |
| 多题打包 | 1 | 8 | JEV 1.13 | 59.38% | 1.293 | 24.75 / 14.70 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 36.46% | 3.116 | 10.27 / 3.74 | 12 / 12 | 0 |
| 多题打包 | 1 | 32 | JEV 1.13 | 63.54% | 0.765 | 41.83 / 26.58 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 48.96% | 1.493 | 21.43 / 10.49 | 3 / 3 | 0 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 7.896–8.608 | 0.248 | 0.324 | 0.700 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-228.jsonl) · [轮2](../../results/task-performance-v1/cell-451.jsonl) · [轮3](../../results/task-performance-v1/cell-594.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 19.507–22.038 | 0.643 | 0.858 | 1.040 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-235.jsonl) · [轮2](../../results/task-performance-v1/cell-398.jsonl) · [轮3](../../results/task-performance-v1/cell-674.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.040–2.032 | 0.267 | 1.134 | 1.357 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-011.jsonl) · [轮2](../../results/task-performance-v1/cell-436.jsonl) · [轮3](../../results/task-performance-v1/cell-488.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.571–3.407 | 0.656 | 0.984 | 1.567 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-152.jsonl) · [轮2](../../results/task-performance-v1/cell-304.jsonl) · [轮3](../../results/task-performance-v1/cell-707.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.334–32.344 | 0.291 | 31.773 | 32.325 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-117.jsonl) · [轮2](../../results/task-performance-v1/cell-383.jsonl) · [轮3](../../results/task-performance-v1/cell-519.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 1.132–1.610 | 0.823 | 1.386 | 1.596 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-194.jsonl) · [轮2](../../results/task-performance-v1/cell-237.jsonl) · [轮3](../../results/task-performance-v1/cell-510.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.108–1.655 | 0.273 | 样本不足 | 0.944 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-160.jsonl) · [轮2](../../results/task-performance-v1/cell-341.jsonl) · [轮3](../../results/task-performance-v1/cell-679.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 2.920–3.265 | 0.786 | 样本不足 | 0.986 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-034.jsonl) · [轮2](../../results/task-performance-v1/cell-429.jsonl) · [轮3](../../results/task-performance-v1/cell-547.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.480–1.316 | 0.499 | 样本不足 | 1.316 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-054.jsonl) · [轮2](../../results/task-performance-v1/cell-267.jsonl) · [轮3](../../results/task-performance-v1/cell-571.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 1.227–1.801 | 1.452 | 样本不足 | 1.801 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-059.jsonl) · [轮2](../../results/task-performance-v1/cell-338.jsonl) · [轮3](../../results/task-performance-v1/cell-646.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0469 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0622–0.1244 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0461 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0622–0.1244 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0469 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | — | 1 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0358 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0720–0.1440 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0318 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0425–0.0849 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`pgx_guideline_recommendation:cpic:8479701`；语种：英语；来源组：`cpic:guideline:https://www.clinpgx.org/guideline/PA166251444`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "action_0": "Abacavir is not recommended",
        "action_1": "Use abacavir per standard dosing guidelines"
      },
      "instructions": "给定药物、人群及基因结果，选择 CPIC 固定快照中对应的原始用药建议；不外推为完整个体处方。",
      "type": "choice"
    }
  },
  "state": {
    "drug": "abacavir",
    "gene_results": {
      "HLA-B": "*57:01 negative"
    },
    "guideline": "HLA-B and Abacavir",
    "population": "general",
    "reference_snapshot": "CPIC API v1, 2026-10-10"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `action_1`，对应选项：

```json
"Use abacavir per standard dosing guidelines"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "pgx_guideline_recommendation:cpic:8479701", "choice": "action_1"}
```

### 样例溯源

[上游资源](https://api.cpicpgx.org/v1/recommendation_view?order=recommendationid) · [数据集说明](../datasets/cpic.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC0-1.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "candidate_json_indices": [
      0,
      1
    ],
    "json_index": 0,
    "recommendation_id": 8479701
  },
  "material_kind": "curated_guideline_rules",
  "resource": "cpic__recommendation_view.json",
  "resource_sha256": "8b4559a9b0b851fec69464cc5c62932d95d385bca59d725b03570f92c700bc85",
  "resource_url": "https://api.cpicpgx.org/v1/recommendation_view?order=recommendationid",
  "source_id": "cpic",
  "source_url": "https://www.clinpgx.org/cpic",
  "split": "curated_rules_no_patient_split",
  "upstream_group": "guideline:https://www.clinpgx.org/guideline/PA166251444",
  "upstream_id": "8479701",
  "version": "API v1 response snapshot 2026-10-10"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：action_0 23 题、action_1 19 题、action_11 1 题、action_14 1 题、action_2 24 题、action_3 17 题、action_4 9 题、action_5 2 题、action_6 1 题、action_8 2 题、action_9 1 题。

**[CPIC curated pharmacogenomic tables](../datasets/cpic.md)**：CPIC 专家整理的功能到表型映射和基因结果用药建议表，不是患者病例。API 的原始响应随数据包冻结，访问日期不冒充数据库发布版本。 答案依据：功能表型题按 gene_result_lookup.phenotypeid 连接 gene_result.id，复制 result；用药题复制 recommendation_view.drugrecommendation，候选来自相同指南、药物和人群的原始建议。冲突输入和无替代选项排除，不生成临床答案。

只评价固定快照中的规则映射；不代表完整基因型检测、个体化处方或临床结局。指南会更新，应查看对应 guideline URL 的最新内容。按基因和指南分组，每组最多 5 题。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/pgx_guideline_recommendation/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/pgx_guideline_recommendation/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
