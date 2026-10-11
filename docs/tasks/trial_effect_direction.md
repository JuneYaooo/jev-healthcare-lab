# 试验报告结局方向判读

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 判断报告中升高、降低或无显著差异，方向不等于获益，不选择患者治疗方案。

## 任务是什么

根据完整试验报告，判断指定干预相对对照对指定结局的报告结果：显著降低、无显著差异或显著升高。方向不等同临床优劣。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `trial_effect_direction` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 证据与一致性 |
| 评测类别 | 临床计算、解读与证据 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [Evidence Inference 2.0 — CC-BY article subset](../datasets/evidence_inference.md) | 100 | [原始来源](https://github.com/jayded/evidence-inference) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`trial_effect_direction:evidence_inference:209`；语种：英语；来源组：`evidence_inference:PMC2206488`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "-1": "Significantly decreased",
        "0": "No significant difference",
        "1": "Significantly increased"
      },
      "instructions": "根据完整试验报告，判断指定干预相对对照对指定结局的报告结果：显著降低、无显著差异或显著升高。方向不等同临床优劣。",
      "type": "choice"
    }
  },
  "state": {
    "comparator": "identical amounts of gelatin infusion",
    "intervention": "dextran-70 infusion was administered at a dose of 7.5 ml/kg before the initiation of cardiopulmonary bypass and at a dose of 12.5 ml/kg after the cessation of cardiopulmonary bypass",
    "outcome": "Cardiac index ",
    "trial_report": ""
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `1`，对应选项：

```json
"Significantly increased"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "trial_effect_direction:evidence_inference:209", "choice": "1"}
```

### 样例溯源

[上游资源](https://codeload.github.com/jayded/evidence-inference/zip/a661e8c14f973398380c8865cf2f27a535aaaf6d) · [数据集说明](../datasets/evidence_inference.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "MIT (annotations); CC-BY (articles, per-record version)",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "annotation_csv_rows": [
      287,
      288,
      289,
      290,
      291
    ],
    "annotation_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/annotations_merged.csv",
    "csv_row": 89,
    "license_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/xml_files/PMC2206488.nxml",
    "prompt_id": "209",
    "split_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/splits/test_article_ids.txt",
    "text_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/txt_files/PMC2206488.txt",
    "zip_member": "evidence-inference-a661e8c14f973398380c8865cf2f27a535aaaf6d/annotations/prompts_merged.csv"
  },
  "material_kind": "published_clinical_trial_reports",
  "resource": "evidence_inference__corpus.zip",
  "resource_sha256": "cfccb8f35a7ae825eea920a8ecfd2b59573907b7cdf3fb9902d3aabee591f8e7",
  "resource_url": "https://codeload.github.com/jayded/evidence-inference/zip/a661e8c14f973398380c8865cf2f27a535aaaf6d",
  "source_id": "evidence_inference",
  "source_url": "https://github.com/jayded/evidence-inference",
  "split": "official_test_articles",
  "upstream_group": "PMC2206488",
  "upstream_id": "209",
  "version": "a661e8c14f973398380c8865cf2f27a535aaaf6d"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：-1 33 题、0 34 题、1 33 题。

**[Evidence Inference 2.0 — CC-BY article subset](../datasets/evidence_inference.md)**：已发表临床试验报告及医生判断；不是患者级原始病历。只纳入官方测试文章中 XML 明确标注 CC-BY 的文章。 答案依据：PromptID 连接原 ICO 提示和医生标注；仅保留验证通过、全部有效标注的方向一致且至少有一条有效理由的条目。复制 Label Code (-1/0/1)。排除作者列出的 incorrect/questionable/malformed 提示。

判断指定干预相对对照对指定结局的报告方向，不把降低某结局直接当作治疗更优，也不把无显著差异当作等效证明。输入完整原始文章文本；统计和人群外推不在该任务的评测范围。

其中 31 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/trial_effect_direction/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/trial_effect_direction/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
