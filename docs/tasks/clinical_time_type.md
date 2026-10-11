# 临床时间表达类别

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

给定病例及时间片段，选择原 E3C TIMEX3 类别：时长、周期集合、日期、数量时间或前后表达。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `clinical_time_type` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 分类与标准化 |
| 决策类型 | 材料判断 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 41 |
| 语种 | 英语 100 题 |
| 数据范围 | 非商业研究附加集 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [E3C English Layer 1](../datasets/e3c.md) | 100 | [原始来源](https://github.com/hltfbk/E3C-Corpus) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`clinical_time_type:e3c:EN105094:1982`；语种：英语；来源组：`e3c:EN105094`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "DATE": "Date",
        "DURATION": "Duration",
        "PREPOSTEXP": "Before/after expression",
        "QUANTIFIER": "Time quantity",
        "SET": "Recurring time set"
      },
      "instructions": "给定病例及时间片段，选择原 E3C TIMEX3 类别：时长、周期集合、日期、数量时间或前后表达。",
      "type": "choice"
    }
  },
  "state": {
    "case_report": "We present a case of a 77-year-old Caucasian woman with obstructive jaundice. Laboratory tests revealed that she had elevated bilirubin and liver enzyme levels. A computed tomographic scan showed a homogeneous 5 × 3-cm mass obstructing the common bile duct. The results of brush cytology were consistent with a bile duct villous papilloma. However, on the basis of the tumor's radiological features, a preliminary diagnosis of extrahepatic bile duct malignant tumor was made. After discussion among the multidisciplinary team, a surgical resection of the bile duct tumor was performed. Histopathological examination confirmed a villous adenoma. The patient's postoperative course was uneventful.\r\n",
    "target": {
      "end": 672,
      "start": 659,
      "text": "postoperative"
    }
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `PREPOSTEXP`，对应选项：

```json
"Before/after expression"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "clinical_time_type:e3c:EN105094:1982", "choice": "PREPOSTEXP"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/hltfbk/E3C-Corpus/8196181eacd5d65828d324dcc63970c503aff5e9/data_annotation/English/layer1/EN105094.xml) · [数据集说明](../datasets/e3c.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-NC (publisher does not specify version)",
  "distribution": "research_noncommercial",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "attribute": "timex3Class",
    "supporting_resources": [
      "e3c__train_test_split.txt"
    ],
    "utf16_begin": 659,
    "utf16_end": 672,
    "xmi_id": "1982"
  },
  "material_kind": "published_clinical_case_reports",
  "resource": "e3c__EN105094.xml",
  "resource_sha256": "f2bffebfc3e91f05125afe34a29760eb647fd2f371ceac31977d840c9afc6e9f",
  "resource_url": "https://raw.githubusercontent.com/hltfbk/E3C-Corpus/8196181eacd5d65828d324dcc63970c503aff5e9/data_annotation/English/layer1/EN105094.xml",
  "source_id": "e3c",
  "source_url": "https://github.com/hltfbk/E3C-Corpus",
  "split": "official_test",
  "upstream_group": "EN105094",
  "upstream_id": "EN105094:1982",
  "version": "8196181eacd5d65828d324dcc63970c503aff5e9"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：DATE 28 题、DURATION 35 题、PREPOSTEXP 21 题、QUANTIFIER 5 题、SET 11 题。

**[E3C English Layer 1](../datasets/e3c.md)**：公开病例报道；Layer 1 人工事件与时间标注。保留各文献原作者、DOI、原文许可。 答案依据：仅官方英文测试文档；原 docTimeRel、permanence、TIMEX3 类型及 timexLink 唯一目标机械适配，不使用自动标注层。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/clinical_time_type/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/clinical_time_type/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
