# 分诊与就医紧急程度判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 根据当前披露消息选择澄清、自护、非紧急或紧急就医，属于行动决策；材料为重构轨迹，应单列来源性质。

## 任务是什么

仅根据当前已披露消息，选择澄清信息、自护监测、非紧急就医或紧急就医；不生成建议文本。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `triage_urgency` |
| 医疗场景 | 接诊与分诊 |
| 能力维度 | 风险与升级 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 62 |
| 语种 | 英语 100 题 |
| 数据范围 | 非商业研究附加集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CARE-Bench](../datasets/care_bench.md) | 100 | [原始来源](https://github.com/ningkko/CARE-bench) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | 63.00% | 100 / 100 | 0.971 | 0.931 | 1.276 | 12.462 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 61.00% | 100 / 100 | **0.511** | **0.495** | **0.706** | **6.749** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 57.00% | 100 / 100 | 1.003 | 0.993 | 1.403 | 12.946 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 50.00% | 99 / 100 | 1.075 | 0.832 | 2.282 | 18.657 | 0 / 0 / 1 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | **65.00%** | 100 / 100 | 2.201 | 1.800 | 2.697 | 42.586 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

持续多题并发尚未测试。以下为历史有限批次结果，不作为高并发高吞吐证据。

### 历史有限批次测试

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

历史多题结果（固定最大打包档，对比 Flash）：JEV 58.33%，Flash 59.38%；JEV 耗时多 351.1%；JEV 成本低 41.8%–70.9%。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 56.25% | 18.921 | 1.69 / 0.95 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 43.75% | 21.671 | 1.48 / 0.65 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 58.33% | 11.327 | 2.83 / 1.65 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 43.75% | 3.164 | 10.12 / 4.43 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | JEV 1.13 | 55.21% | 0.809 | 39.56 / 21.84 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 43.75% | 1.388 | 23.06 / 10.09 | 96 / 96 | 0 |
| 多题打包 | 1 | 8 | JEV 1.13 | 56.25% | 1.393 | 22.96 / 12.92 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 53.12% | 4.059 | 7.88 / 4.19 | 12 / 12 | 0 |
| 多题打包 | 1 | 32 | JEV 1.13 | 58.33% | 10.547 | 3.03 / 1.77 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 59.38% | 2.338 | 13.69 / 8.13 | 3 / 3 | 0 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 7.763–41.024 | 0.255 | 0.367 | 30.962 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-221.jsonl) · [轮2](../../results/task-performance-v1/cell-357.jsonl) · [轮3](../../results/task-performance-v1/cell-535.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 20.461–23.386 | 0.654 | 1.013 | 1.585 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-052.jsonl) · [轮2](../../results/task-performance-v1/cell-389.jsonl) · [轮3](../../results/task-performance-v1/cell-661.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.142–31.666 | 0.256 | 30.803 | 30.860 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-207.jsonl) · [轮2](../../results/task-performance-v1/cell-374.jsonl) · [轮3](../../results/task-performance-v1/cell-507.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 3.110–3.215 | 0.679 | 1.032 | 1.333 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-211.jsonl) · [轮2](../../results/task-performance-v1/cell-306.jsonl) · [轮3](../../results/task-performance-v1/cell-521.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.379–1.343 | 0.318 | 1.196 | 1.341 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-231.jsonl) · [轮2](../../results/task-performance-v1/cell-302.jsonl) · [轮3](../../results/task-performance-v1/cell-706.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.985–1.663 | 0.666 | 1.238 | 1.657 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-179.jsonl) · [轮2](../../results/task-performance-v1/cell-345.jsonl) · [轮3](../../results/task-performance-v1/cell-556.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.051–1.593 | 0.259 | 样本不足 | 0.819 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-136.jsonl) · [轮2](../../results/task-performance-v1/cell-358.jsonl) · [轮3](../../results/task-performance-v1/cell-477.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 4.009–4.093 | 0.995 | 样本不足 | 1.251 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-044.jsonl) · [轮2](../../results/task-performance-v1/cell-294.jsonl) · [轮3](../../results/task-performance-v1/cell-592.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.280–30.949 | 0.412 | 样本不足 | 30.949 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-195.jsonl) · [轮2](../../results/task-performance-v1/cell-410.jsonl) · [轮3](../../results/task-performance-v1/cell-491.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 2.270–2.411 | 2.332 | 样本不足 | 2.411 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-226.jsonl) · [轮2](../../results/task-performance-v1/cell-447.jsonl) · [轮3](../../results/task-performance-v1/cell-587.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0368 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0819–0.1638 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0354 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0819–0.1639 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0374 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.0819–0.1638 | 0 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0224 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0368–0.0735 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0198 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0341–0.0681 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`triage_urgency:care_bench:meb_v1_case_0389_r01`；语种：英语；来源组：`care_bench:meb_v1_case_0389`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "0A_NO_ESCALATION_INFO_NEEDED": "Ask for necessary clarification",
        "0B_NO_ESCALATION_SELF_CARE_MONITOR": "Self-care or monitoring",
        "1A_ESCALATION_NONURGENT_CARE": "Nonurgent professional care",
        "1B_ESCALATION_URGENT_CARE": "Urgent or emergency care"
      },
      "instructions": "仅根据当前已披露消息，选择澄清信息、自护监测、非紧急就医或紧急就医；不生成建议文本。",
      "type": "choice"
    }
  },
  "state": {
    "patient_messages_so_far": [
      "My tummy hurts."
    ]
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `0A_NO_ESCALATION_INFO_NEEDED`，对应选项：

```json
"Ask for necessary clarification"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "triage_urgency:care_bench:meb_v1_case_0389_r01", "choice": "0A_NO_ESCALATION_INFO_NEEDED"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/ningkko/CARE-bench/090e84167f23c72d29c3a4d9c4f73e857afe0458/data/public/evaluation_prefixes_public.jsonl) · [数据集说明](../datasets/care_bench.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC-4.0",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "case_id": "meb_v1_case_0389",
    "jsonl_line": 774,
    "prefix_id": "meb_v1_case_0389_r01",
    "supporting_resources": [
      "care_bench__cases_public.jsonl"
    ]
  },
  "material_kind": "source_grounded_model_assisted_reconstructed",
  "resource": "care_bench__evaluation_prefixes_public.jsonl",
  "resource_sha256": "6d2850f303d05b8f92035c31a11233f41a965e77b3e878e1425f956a00cff534",
  "resource_url": "https://raw.githubusercontent.com/ningkko/CARE-bench/090e84167f23c72d29c3a4d9c4f73e857afe0458/data/public/evaluation_prefixes_public.jsonl",
  "source_id": "care_bench",
  "source_url": "https://github.com/ningkko/CARE-bench",
  "split": "official_public_test_1",
  "upstream_group": "meb_v1_case_0389",
  "upstream_id": "meb_v1_case_0389_r01",
  "version": "090e84167f23c72d29c3a4d9c4f73e857afe0458"
}
```

该题的格式转换说明：

Only disclosed patient turns; no reference response, future turns, or construction metadata.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：0A_NO_ESCALATION_INFO_NEEDED 30 题、0B_NO_ESCALATION_SELF_CARE_MONITOR 20 题、1A_ESCALATION_NONURGENT_CARE 30 题、1B_ESCALATION_URGENT_CARE 20 题。

**[CARE-Bench](../datasets/care_bench.md)**：来源约束的重构咨询轨迹；GPT-5.5 辅助构建后人工审核（发布方说明），不是原始真实分诊记录。 答案依据：只用 public_test_1 的四类 gold_label；只给当前已披露患者消息，不给后续轮次、参考回复、信息充分性和构造标签。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [MIMIC-IV-ED](../datasets/mimic_iv_ed.md) | 需凭证与 DUA；构建入院分诊任务时必须排除出院诊断、去向等未来信息。 |
| [TRIAGE](../datasets/triage.md) | 公开数据未见明确许可，87病例的提示变体不当作独立病例 |
| [TriageBench（Wong，一致性探针）](../datasets/triagebench_wong.md) | 仅作另行设计的一致性附加实验，不填分诊正确性主任务。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/triage_urgency/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/triage_urgency/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
