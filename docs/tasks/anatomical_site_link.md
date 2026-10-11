# 文本事件与解剖部位关联

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 复制原文修饰关系，不判断疾病部位或病灶定位。

## 任务是什么

给定病例和临床事件，从原文解剖部位候选中选择原 MODIFY 关系唯一关联的部位。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `anatomical_site_link` |
| 医疗场景 | 诊断与鉴别 |
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

题目 ID：`anatomical_site_link:maccrobat:25926582.ann:T25`；语种：英语；来源组：`maccrobat:25926582`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "T20": "choanal [characters 413:420]",
        "T21": "left-sided [characters 402:412]",
        "T26": "head [characters 527:531]",
        "T28": "sellar [characters 541:547]",
        "T29": "infra-sellar [characters 552:564]",
        "T30": "extending into the nasopharynx [characters 570:600]"
      },
      "instructions": "给定病例和临床事件，从原文解剖部位候选中选择原 MODIFY 关系唯一关联的部位。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "A 35-year-old woman presented to the ear, nose and throat outpatient department with headache and a blocked left-sided nasal canal with epistaxis for 2 years.\nMedical history revealed secondary amenorrhoea for the past 19 years with regression of secondary sexual characteristics with no galactorrhoea.\nPhysical and ophthalmological examinations were within normal limits.\nNasal examination revealed a left-sided choanal mass.\nAs the mass was bleeding on palpation, imaging was advised prior to performing a biopsy.\nMRI of the head showed a sellar and infra-sellar mass extending into the nasopharynx (figure 1).\nThe patient was then referred to the endocrinologist for further hormonal investigation.\nHer serum prolactin was very high—7443 µg/L (N<20).\nOther pituitary hormones were within normal limits.\nA final diagnosis of giant prolactinoma was made and the patient was prescribed cabergoline 0.25 mg twice per week with the associated risks explained in advance.\n",
    "target": {
      "end": 519,
      "start": 516,
      "text": "MRI"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `T26`，对应选项：

```json
"head [characters 527:531]"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "anatomical_site_link:maccrobat:25926582.ann:T25", "choice": "T26"}
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
    "answer_entity_id": "T26",
    "direction_reversed": true,
    "query_entity_id": "T25",
    "relation_ids": [
      "R9"
    ],
    "zip_member": "25926582.ann"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "maccrobat__MACCROBAT2020.zip",
  "resource_sha256": "a2d34ccd1a605d9147fc7368293e61dcf2090357b26f7bce6c2b3d257204acc6",
  "resource_url": "https://ndownloader.figshare.com/files/21489405",
  "source_id": "maccrobat",
  "source_url": "https://doi.org/10.6084/m9.figshare.9764942.v2",
  "split": "published_corpus_no_official_split",
  "upstream_group": "25926582",
  "upstream_id": "25926582.ann:T25",
  "version": "figshare.9764942.v2/MACCROBAT2020"
}
```

该题的格式转换说明：

All valid entities of prespecified candidate types; unique explicit relation; no invented negatives.

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：T100 1 题、T103 1 题、T106 1 题、T107 3 题、T108 1 题、T110 1 题、T111 1 题、T115 1 题、T118 3 题、T119 2 题、T123 1 题、T124 1 题、T126 4 题、T127 2 题、T131 2 题、T135 1 题、T137 1 题、T14 1 题、T15 2 题、T154 1 题、T156 1 题、T16 3 题、T160 1 题、T169 1 题、T178 1 题、T192 1 题、T20 1 题、T21 1 题、T213 1 题、T215 1 题、T22 1 题、T24 2 题、T25 1 题、T26 3 题、T27 1 题、T28 3 题、T29 2 题、T31 1 题、T36 2 题、T38 1 题、T39 2 题、T4 1 题、T43 1 题、T44 4 题、T47 1 题、T50 1 题、T56 1 题、T57 1 题、T60 2 题、T63 2 题、T65 1 题、T67 1 题、T68 3 题、T7 3 题、T70 1 题、T72 1 题、T73 2 题、T74 1 题、T75 1 题、T77 1 题、T81 1 题、T87 1 题、T88 1 题、T89 1 题、T90 1 题、T93 1 题、T94 1 题、T97 1 题、T99 1 题。

**[MACCROBAT2020](../datasets/maccrobat.md)**：公开发表的临床病例报告；原病例被编辑整理，不等同医院原始 EHR。 答案依据：原始 BRAT MODIFY 关系；把事件引用解析为文本实体，只保留目标检查/药物唯一的关联。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/anatomical_site_link/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/anatomical_site_link/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
