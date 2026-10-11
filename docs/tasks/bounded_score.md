# 临床量表计算

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 计算五种指定量表的分值，有医疗用途，但没有评价评分后应采取的行动；各量表分层报告。

## 任务是什么

根据病例选择 GCS、CURB-65、SIRS、CHA2DS2-VASc 或 FeverPAIN 的数值。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `bounded_score` |
| 医疗场景 | 诊断与鉴别 |
| 能力维度 | 规则与数值、证据与一致性 |
| 评测类别 | 临床计算、解读与证据 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [MedCalc-Bench GitHub test release](../datasets/medcalc.md) | 100 | [原始来源](https://github.com/ncbi-nlp/MedCalc-Bench) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`bounded_score:medcalc:652`；语种：英语；来源组：`medcalc:trec-cds-2016-23`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4"
      },
      "instructions": "根据病例选择 GCS、CURB-65、SIRS、CHA2DS2-VASc 或 FeverPAIN 的数值。",
      "type": "choice"
    }
  },
  "state": {
    "patient_note": "85M dementia, colon cancer and recent colectomy with primary reanastomosis  p/w melena. HCT 30 to 23 but hemodynamically stable. NGL negative.  Exam notable for Tm 99 BP 128/50 HR 70 RR 16 with sat 100 on RA. WD man, NAD. Chest clear, JVP 8cm. RR s1s2. Soft abdomen, well healed surgical scar. No edema or cord. Labs notable for WBC 7K, HCT 24, K+ 4.0, Cr 0.7.",
    "question": "What are the number of SIRS critiera met by the patient? You should use the patient's medical values and health status when they were first admitted to the hospital prior to any treatment."
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `0`，对应选项：

```json
"0"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "bounded_score:medcalc:652", "choice": "0"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/ncbi-nlp/MedCalc-Bench/20b10f9d66a8c3b0356ae3138533f5ec91666b6a/datasets/test_data.csv) · [数据集说明](../datasets/medcalc.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-SA-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 653,
    "note_id": "trec-cds-2016-23",
    "row_number": "652"
  },
  "material_kind": "mixed_extracted_generated_template",
  "resource": "medcalc__datasets_test_data.csv",
  "resource_sha256": "c9d219a30e43f50646b73fa5fe5fe86d1ef47e7d9b2c7403a0edb7f3e5290e3a",
  "resource_url": "https://raw.githubusercontent.com/ncbi-nlp/MedCalc-Bench/20b10f9d66a8c3b0356ae3138533f5ec91666b6a/datasets/test_data.csv",
  "source_id": "medcalc",
  "source_url": "https://github.com/ncbi-nlp/MedCalc-Bench",
  "split": "official_github_test",
  "upstream_group": "trec-cds-2016-23",
  "upstream_id": "652",
  "version": "20b10f9d66a8c3b0356ae3138533f5ec91666b6a"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：0 7 题、1 17 题、10 3 题、11 1 题、12 2 题、15 2 题、2 19 题、3 20 题、4 10 题、5 5 题、6 4 题、7 3 题、8 2 题、9 5 题。

**[MedCalc-Bench GitHub test release](../datasets/medcalc.md)**：文献提取、生成后人工编辑、模板混合；逐题保留 Note Type。 答案依据：原测试 CSV Ground Truth Answer；完整整数范围作为候选，不由答案生成干扰项。

其中 100 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/bounded_score/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/bounded_score/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
