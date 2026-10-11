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

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

| 模型 | 准确率 | 有效回答 / 题数 | 平均秒 | P50 秒 | P95 秒 | 任务总秒 | 超时 / 请求失败 / 无效回答 | 重试次数 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | 53.00% | 100 / 100 | 1.046 | 0.976 | 1.390 | 13.689 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/jev-1.13.0/config.json) · [响应](../../results/clinical-20261012/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-20261012/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 60.00% | 100 / 100 | 0.698 | 0.489 | 0.928 | 21.024 | 0 / 0 / 0 | 2 | [配置](../../results/clinical-20261012/deepseek-flash/config.json) · [响应](../../results/clinical-20261012/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-20261012/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 58.00% | 100 / 100 | 1.282 | 1.297 | 1.730 | 16.575 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/deepseek-v4-pro/config.json) · [响应](../../results/clinical-20261012/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-20261012/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 50.00% | 84 / 100 | 3.040 | 3.392 | 4.717 | 38.262 | 0 / 16 / 0 | 136 | [配置](../../results/clinical-20261012/qwen3.5-9b/config.json) · [响应](../../results/clinical-20261012/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-20261012/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 58.00% | 99 / 100 | 2.092 | 1.643 | 6.797 | 28.939 | 0 / 1 / 0 | 3 | [配置](../../results/clinical-20261012/qwen3.8-27b/config.json) · [响应](../../results/clinical-20261012/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-20261012/qwen3.8-27b/scores.json) |

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
