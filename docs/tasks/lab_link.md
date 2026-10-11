# 检验结果与项目文本关联

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 在已标注数值和项目间找对应关系，不判断异常、诊断或处置。

## 任务是什么

给定病例全文和已标注的数值结果片段，从候选检查/评估中选择原始标注关联的项目；包含量表，不判断结果是否异常。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `lab_link` |
| 医疗场景 | 检查与检验 |
| 能力维度 | 关联与匹配、证据与一致性 |
| 评测类别 | 文本理解与标注 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [MACCROBAT2020](../datasets/maccrobat.md) | 100 | [原始来源](https://doi.org/10.6084/m9.figshare.9764942.v2) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`lab_link:maccrobat:26474553.ann:T41`；语种：英语；来源组：`maccrobat:26474553`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T17": "lung function [characters 541:554]",
        "T19": "body plethysmography [characters 599:619]",
        "T20": "spirometry [characters 624:634]",
        "T22": "Sputum cultures [characters 668:683]",
        "T31": "physical performance [characters 880:900]",
        "T33": "body weight [characters 946:957]",
        "T36": "sweat chloride level [characters 1034:1054]",
        "T43": "FEV1 [characters 1211:1215]",
        "T50": "LCI [characters 1319:1322]"
      },
      "instructions": "给定病例全文和已标注的数值结果片段，从候选检查/评估中选择原始标注关联的项目；包含量表，不判断结果是否异常。",
      "type": "choice"
    }
  },
  "state": {
    "case_report": "An 8-year-old boy with S549R/1717-1G > A genotype was started on ivacaftor (150 mg b.i.d.) on compassionate use.\nAt the age of 9 months he was diagnosed with CF due to failure to thrive.\nHis previous history was remarkable for recurring nasal polyposis requiring endoscopic surgery and exocrine pancreatic insufficiency necessitating enzyme replacement therapy.\nHe grew with body weight and height along the 10th percentile.\nHe suffered from rather mild respiratory symptoms, primarily intermittent productive cough, and had close to normal lung function parameters in previous years as measured by body plethysmography and spirometry (minimal z-score of FEV1: −1.2).\nSputum cultures grew Haemophilus influenzae and Staphylococcus aureus on several occasions.\nAfter 6 weeks of ivacaftor treatment, the patient reported clinical improvements in cough frequency, sputum production, physical performance, and less salt cravings.\nHe gained 1.4 kg in body weight without changing the dose of his pancreatic enzyme replacement therapy.\nHis sweat chloride level (Macroduct®) decreased from 115 mmol/l before ivacaftor to 40 mmol/l after 6 weeks and 52 mmol/l after 41 weeks (normal < 30 mmol/l [11]) of treatment.\nHis FEV1 increased from 1.25 L (−1.2 z-score) to 1.65 L (+0.5 z-score) after 41 weeks of ivacaftor therapy.\nThe LCI (normal < 8) measured by N2-MBW decreased from 14.5 to 8.3 after 6 weeks and 7.8 after 41 weeks of ivacaftor treatment (Table 1 and Fig.1).\n",
    "target": {
      "end": 1151,
      "start": 1142,
      "text": "52 mmol/l"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T36`，对应选项：

```json
"sweat chloride level [characters 1034:1054]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "lab_link:maccrobat:26474553.ann:T41", "choice": "T36"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/21489405) · [数据集说明](../datasets/maccrobat.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "linked_entity_id": "T36",
    "modifier_id": "T41",
    "relation_ids": [
      "R18"
    ],
    "zip_member": "26474553.ann"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "maccrobat__MACCROBAT2020.zip",
  "resource_sha256": "a2d34ccd1a605d9147fc7368293e61dcf2090357b26f7bce6c2b3d257204acc6",
  "resource_url": "https://ndownloader.figshare.com/files/21489405",
  "source_id": "maccrobat",
  "source_url": "https://doi.org/10.6084/m9.figshare.9764942.v2",
  "split": "published_corpus_no_official_split",
  "upstream_group": "26474553",
  "upstream_id": "26474553.ann:T41",
  "version": "figshare.9764942.v2/MACCROBAT2020"
}
```

该题的格式转换说明：

Resolve event IDs to text anchors; unique original MODIFY link; all valid same-type entities are options.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T100 2 题、T103 1 题、T104 1 题、T105 1 题、T108 1 题、T109 1 题、T110 1 题、T113 1 题、T116 1 题、T117 2 题、T118 1 题、T12 1 题、T121 1 题、T123 1 题、T125 1 题、T133 1 题、T146 1 题、T154 1 题、T16 1 题、T165 1 题、T166 1 题、T167 1 题、T17 1 题、T184 1 题、T185 1 题、T19 1 题、T20 1 题、T202 1 题、T23 1 题、T24 1 题、T25 2 题、T26 1 题、T28 2 题、T29 1 题、T31 3 题、T32 1 题、T33 1 题、T34 2 题、T36 1 题、T37 1 题、T38 2 题、T39 1 题、T41 1 题、T42 2 题、T44 4 题、T45 1 题、T46 4 题、T48 1 题、T49 1 题、T51 3 题、T52 1 题、T53 3 题、T54 3 题、T55 1 题、T56 1 题、T57 1 题、T59 1 题、T63 1 题、T64 2 题、T65 1 题、T66 1 题、T68 2 题、T69 1 题、T72 1 题、T75 1 题、T76 1 题、T77 2 题、T79 1 题、T81 1 题、T83 1 题、T85 1 题、T87 1 题、T94 1 题、T95 1 题、T99 2 题。

**[MACCROBAT2020](../datasets/maccrobat.md)**：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。 答案依据：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/lab_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/lab_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
