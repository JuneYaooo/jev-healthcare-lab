# 患者临床试验初筛与转介判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 输入含患者与试验条件并输出转介相关等级，适合主评测；不是最终入组资格，原 material_judgment 标签应调整。

## 任务是什么

根据患者和试验材料，判断不相关、可能适合或很可能适合转介。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `trial_referral` |
| 医疗场景 | 临床试验筛选 |
| 能力维度 | 资格与适宜性、证据与一致性 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 58 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [TrialGPT SIGIR](../datasets/trialgpt.md) | 100 | [原始来源](https://github.com/ncbi-nlp/TrialGPT) |

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
| JEV 1.13 | 53.00% | 100 / 100 | 1.046 | 0.976 | 1.390 | **13.689** | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | **60.00%** | 100 / 100 | **0.698** | **0.489** | **0.928** | 21.024 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 58.00% | 100 / 100 | 1.282 | 1.297 | 1.730 | 16.575 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 50.00% | 84 / 100 | 3.040 | 3.392 | 4.717 | 38.262 | 0 / 16 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 58.00% | 99 / 100 | 2.092 | 1.643 | 6.797 | 28.939 | 0 / 1 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 53.12% | 9.286 | 3.45 / 1.83 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 60.42% | 21.551 | 1.45 / 0.90 | 94 / 96 | 2 |
| 逐题 | 8 | 1 | JEV 1.13 | 53.12% | 11.715 | 2.73 / 1.45 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 61.46% | 3.414 | 9.27 / 5.76 | 95 / 96 | 1 |
| 逐题 | 32 | 1 | JEV 1.13 | 53.12% | 0.583 | 54.87 / 29.15 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 61.46% | 1.488 | 21.05 / 13.21 | 94 / 96 | 2 |
| 多题打包 | 1 | 8 | JEV 1.13 | 57.29% | 1.481 | 21.61 / 12.38 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 56.25% | 3.426 | 9.34 / 5.25 | 12 / 12 | 0 |
| 多题打包 | 1 | 2–17 | JEV 1.13 | 50.00% | 1.427 | 22.43 / 11.22 | 9 / 9 | 0 |
| 多题打包 | 1 | 2–17 | DeepSeek V4.1 Flash | 55.21% | 2.642 | 12.11 / 6.69 | 9 / 9 | 0 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 8.421–10.023 | 0.260 | 0.427 | 0.902 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-138.jsonl) · [轮2](../../results/task-performance-v1/cell-320.jsonl) · [轮3](../../results/task-performance-v1/cell-558.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 19.343–24.499 | 0.623 | 1.197 | 2.148 | 0 | 2 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-214.jsonl) · [轮2](../../results/task-performance-v1/cell-432.jsonl) · [轮3](../../results/task-performance-v1/cell-474.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.633–31.831 | 0.257 | 30.754 | 30.935 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-139.jsonl) · [轮2](../../results/task-performance-v1/cell-471.jsonl) · [轮3](../../results/task-performance-v1/cell-493.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 3.165–3.722 | 0.693 | 1.282 | 1.829 | 0 | 1 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-202.jsonl) · [轮2](../../results/task-performance-v1/cell-274.jsonl) · [轮3](../../results/task-performance-v1/cell-692.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.307–1.122 | 0.279 | 0.330 | 1.122 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-089.jsonl) · [轮2](../../results/task-performance-v1/cell-301.jsonl) · [轮3](../../results/task-performance-v1/cell-619.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 1.227–1.795 | 0.979 | 1.743 | 1.795 | 0 | 2 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-012.jsonl) · [轮2](../../results/task-performance-v1/cell-392.jsonl) · [轮3](../../results/task-performance-v1/cell-621.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.174–2.013 | 0.310 | 样本不足 | 0.709 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-112.jsonl) · [轮2](../../results/task-performance-v1/cell-322.jsonl) · [轮3](../../results/task-performance-v1/cell-653.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 3.173–3.668 | 0.856 | 样本不足 | 1.256 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-070.jsonl) · [轮2](../../results/task-performance-v1/cell-370.jsonl) · [轮3](../../results/task-performance-v1/cell-573.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 1.018–1.831 | 0.421 | 样本不足 | 0.789 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-116.jsonl) · [轮2](../../results/task-performance-v1/cell-293.jsonl) · [轮3](../../results/task-performance-v1/cell-524.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 2.331–3.199 | 0.863 | 样本不足 | 1.515 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-068.jsonl) · [轮2](../../results/task-performance-v1/cell-468.jsonl) · [轮3](../../results/task-performance-v1/cell-669.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0655 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | — | 2 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0655 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | — | 1 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0655 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | — | 2 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0468 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0416–0.0833 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0529 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0526–0.1052 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`trial_referral:trialgpt:sigir-201512:NCT02418169`；语种：英语；来源组：`trialgpt:sigir-201512`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "0": "Irrelevant: would not refer",
        "1": "Potential: consider referral after further investigation",
        "2": "Eligible: highly likely to refer"
      },
      "instructions": "根据患者和试验材料，判断不相关、可能适合或很可能适合转介。",
      "type": "choice"
    }
  },
  "state": {
    "patient": "A 44-year-old man was recently in an automobile accident where he sustained a skull fracture. In the emergency room, he noted clear fluid dripping from his nose. The following day he started complaining of severe headache and fever. Nuchal rigidity was found on physical examination.",
    "trial": {
      "brief_summary": "This study evaluates the association between traumatic brain injuries and craniofacial or/and skull fractures. Purpose is to find out the amount of missed diagnoses and improve primary diagnostics of trauma patients.",
      "brief_title": "Association Between Craniofacial Fractures and Brain Injuries: Diagnostic and Therapeutic Considerations",
      "exclusion_criteria": ": \n\n Died before admitted to hospital",
      "inclusion_criteria": "inclusion criteria: \n\n Severe traumatic brain injury, GCS 8 or less and/or Craniofacial fracture \n\n "
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `1`，对应选项：

```json
"Potential: consider referral after further investigation"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "trial_referral:trialgpt:sigir-201512:NCT02418169", "choice": "1"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/ncbi-nlp/TrialGPT/1b3242cd50c153a9c324661d4a0bd94fc68a4226/dataset/sigir/retrieved_trials.json) · [数据集说明](../datasets/trialgpt.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "LicenseRef-NCBI-Public-Domain",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "nct_id": "NCT02418169",
    "patient_id": "sigir-201512",
    "relevance": "1"
  },
  "material_kind": "synthetic_patient_real_trial",
  "resource": "trialgpt__dataset_sigir_retrieved_trials.json",
  "resource_sha256": "8516049da9f4663b1288086532cc885da232532bd2e081a2b70f54fb035ddb81",
  "resource_url": "https://raw.githubusercontent.com/ncbi-nlp/TrialGPT/1b3242cd50c153a9c324661d4a0bd94fc68a4226/dataset/sigir/retrieved_trials.json",
  "source_id": "trialgpt",
  "source_url": "https://github.com/ncbi-nlp/TrialGPT",
  "split": "sigir_judged_pool",
  "upstream_group": "sigir-201512",
  "upstream_id": "sigir-201512:NCT02418169",
  "version": "1b3242cd50c153a9c324661d4a0bd94fc68a4226"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：0 34 题、1 33 题、2 33 题。

**[TrialGPT SIGIR](../datasets/trialgpt.md)**：患者题设配真实试验文件；不是实际入组结局。 答案依据：SIGIR 公开 relevance 0/1/2；0 不相关、1 可能转介、2 高度适合转介。

其中 82 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/trial_referral/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/trial_referral/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
