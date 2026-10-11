# 文本同一事件指代识别

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 关联同一事件的不同提及，不作临床诊断。

## 任务是什么

给定病例中的目标事件，从原文事件候选中选择原 IDENTICAL 标注唯一关联的同一事件提及。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `event_coreference` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 关联与匹配 |
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

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`event_coreference:maccrobat:21067996.ann:T26`；语种：英语；来源组：`maccrobat:21067996`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T11": "intraabdominal pathology [characters 123:147]",
        "T12": "CT [characters 161:163]",
        "T16": "positive oral contrast [characters 284:306]",
        "T17": "barium sulfate suspension [characters 317:342]",
        "T20": "iopromide [characters 394:403]",
        "T3": "weight loss [characters 23:34]",
        "T31": "Axial sections [characters 571:585]",
        "T33": "mass [characters 660:664]",
        "T4": "nausea [characters 36:42]",
        "T41": "surgical resection [characters 930:948]",
        "T42": "mass [characters 969:973]",
        "T44": "adrenocortical carcinoma [characters 1042:1066]",
        "T46": "pathologic examination [characters 994:1016]",
        "T5": "vomiting [characters 44:52]",
        "T6": "pain [characters 68:72]",
        "T8": "referred [characters 77:85]",
        "T9": "CT scan [characters 103:110]"
      },
      "instructions": "给定病例中的目标事件，从原文事件候选中选择原 IDENTICAL 标注唯一关联的同一事件提及。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "A 41-year-old man with weight loss, nausea, vomiting, and abdominal pain was referred for an abdominal CT scan to rule out intraabdominal pathology.\nA dedicated CT of the abdomen was performed at our institution according to our standard venous phase protocol.\nFollowing ingestion of positive oral contrast material (barium sulfate suspension 2.1% w/v, Mallinckrodt) and injection of 125 ml of iopromide, 300 mg I/mL (Ultravist, Bayer HealthCare), helical CT was obtained with a 65-s delays using a 64-slice GE Lightspeed VCT scanner (GE Medical Systems; Milwaukee, WI).\nAxial sections of the abdomen showed a large (18×22×22 cm) heterogeneous retroperitoneal mass probably arising from the left adrenal gland containing multiple areas of macroscopic fat (Fig.1).\nThe patient had no documented clinical or laboratory evidence of adrenal hormonal excess.\nOn the basis of the clinical history and CT findings, the patient underwent surgical resection of the left adrenal mass, which was found on pathologic examination to represent a low-grade adrenocortical carcinoma.\n",
    "target": {
      "end": 458,
      "start": 456,
      "text": "CT"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T12`，对应选项：

```json
"CT [characters 161:163]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "event_coreference:maccrobat:21067996.ann:T26", "choice": "T12"}
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
    "answer_entity_id": "T12",
    "direction_reversed": false,
    "query_entity_id": "T26",
    "relation_ids": [
      "R17"
    ],
    "zip_member": "21067996.ann"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "maccrobat__MACCROBAT2020.zip",
  "resource_sha256": "a2d34ccd1a605d9147fc7368293e61dcf2090357b26f7bce6c2b3d257204acc6",
  "resource_url": "https://ndownloader.figshare.com/files/21489405",
  "source_id": "maccrobat",
  "source_url": "https://doi.org/10.6084/m9.figshare.9764942.v2",
  "split": "published_corpus_no_official_split",
  "upstream_group": "21067996",
  "upstream_id": "21067996.ann:T26",
  "version": "figshare.9764942.v2/MACCROBAT2020"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T10 1 题、T100 1 题、T102 2 题、T103 1 题、T104 1 题、T107 1 题、T11 1 题、T112 1 题、T12 1 题、T122 1 题、T137 1 题、T145 1 题、T15 1 题、T150 1 题、T159 1 题、T16 1 题、T167 1 题、T175 1 题、T19 1 题、T20 2 题、T21 1 题、T22 3 题、T25 2 题、T26 1 题、T27 1 题、T29 1 题、T3 3 题、T30 2 题、T32 1 题、T33 2 题、T36 1 题、T37 1 题、T39 1 题、T40 1 题、T41 1 题、T42 1 题、T44 3 题、T45 1 题、T46 1 题、T47 2 题、T5 3 题、T50 1 题、T54 1 题、T57 4 题、T61 2 题、T62 2 题、T64 1 题、T65 1 题、T66 1 题、T67 2 题、T69 2 题、T7 1 题、T70 1 题、T71 1 题、T72 3 题、T73 3 题、T75 1 题、T76 1 题、T77 1 题、T79 1 题、T8 1 题、T80 3 题、T81 1 题、T82 1 题、T87 1 题、T89 2 题、T9 1 题、T90 1 题、T92 1 题、T94 2 题、T96 1 题。

**[MACCROBAT2020](../datasets/maccrobat.md)**：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。 答案依据：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/event_coreference/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/event_coreference/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
