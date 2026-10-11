# 病历章节分类

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 识别病史、检查、评估等章节类别，不判断内容是否正确。

## 任务是什么

给定去除章节标题的原文片段，选择原始章节类别。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `note_section` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 分类与标准化 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [ACI-Bench](../datasets/aci_bench.md) | 100 | [原始来源](https://github.com/microsoft/clinical_visit_note_summarization_corpus) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`note_section:aci_bench:D2N144:0`；语种：英语；来源组：`aci_bench:D2N144`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "assessment_plan": "Assessment or plan",
        "exam": "Physical examination or vital signs",
        "history": "History, symptoms, medications or allergies",
        "results": "Laboratory, imaging or diagnostic results"
      },
      "instructions": "给定去除章节标题的原文片段，选择原始章节类别。",
      "type": "choice"
    }
  },
  "state": {
    "section_text": "Rheumatoid arthritis management."
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `history`，对应选项：

```json
"History, symptoms, medications or allergies"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "note_section:aci_bench:D2N144:0", "choice": "history"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/microsoft/clinical_visit_note_summarization_corpus/293e454917c562361409232f65e9d870a45af026/data/aci-bench/challenge_data/clinicalnlp_taskC_test2.csv) · [数据集说明](../datasets/aci_bench.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 18,
    "encounter_id": "D2N144",
    "heading": "CHIEF COMPLAINT"
  },
  "material_kind": "expert_simulated",
  "resource": "aci_bench__data_aci-bench_challenge_data_clinicalnlp_taskC_test2.csv",
  "resource_sha256": "599e3330a14e25a0e056aee1365ffac7ebe50058f15821eae42a5513c2bb5a4f",
  "resource_url": "https://raw.githubusercontent.com/microsoft/clinical_visit_note_summarization_corpus/293e454917c562361409232f65e9d870a45af026/data/aci-bench/challenge_data/clinicalnlp_taskC_test2.csv",
  "source_id": "aci_bench",
  "source_url": "https://github.com/microsoft/clinical_visit_note_summarization_corpus",
  "split": "official_test_1_2_3",
  "upstream_group": "D2N144",
  "upstream_id": "D2N144:0",
  "version": "293e454917c562361409232f65e9d870a45af026"
}
```

该题的格式转换说明：

Removed original heading; mapped section titles into four fixed categories.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：assessment_plan 25 题、exam 25 题、history 25 题、results 25 题。

**[ACI-Bench](../datasets/aci_bench.md)**：合成就诊会话与人工文书；不是自然发生的医院记录。 答案依据：沿用人工文书的章节标题；去除标题后作分类。

其中 18 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/note_section/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/note_section/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
