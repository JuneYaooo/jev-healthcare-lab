# 病例医学错误检出

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 有医疗质量审核意义，但测错误是否存在，非诊疗行动；与错误定位合为一个审核任务的两项指标更合理。

## 任务是什么

判断给定病例文本是否含原数据标注的医学错误。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `clinical_error_detection` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 证据与一致性、临床候选方案 |
| 评测类别 | 临床计算、解读与证据 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 英语 50 题、中文 50 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [MEDEC-MS](../datasets/medec.md) | 50 | [原始来源](https://github.com/abachaa/MEDEC) |
| [MedErrBench CN](../datasets/mederr.md) | 50 | [原始来源](https://github.com/congboma/MedErrBench) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。固定语义标签计算准确率、宏 F1、召回与混淆矩阵。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`clinical_error_detection:mederr:cn-test-17`；语种：中文；来源组：`mederr:cn-test-17`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "0": "No annotated medical error",
        "1": "Contains an annotated medical error"
      },
      "instructions": "判断给定病例文本是否含原数据标注的医学错误。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_text": "男，43岁。外伤致右胸积血，右侧呼吸音弱，叩诊为浊音，胸穿抽出混浊胸液。进行胸穿。"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `1`，对应选项：

```json
"Contains an annotated medical error"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "clinical_error_detection:mederr:cn-test-17", "choice": "1"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/congboma/MedErrBench/754c2e083b794f2922f002b893bc2e8890feb16d/datasets/test/reviewed_data_CN_test.csv) · [数据集说明](../datasets/mederr.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "MIT",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "csv_row": 19,
    "text_id": "cn-test-17"
  },
  "material_kind": "exam_and_expert_authored",
  "resource": "mederr__datasets_test_reviewed_data_CN_test.csv",
  "resource_sha256": "79fcad4ed1c587904e2ad26f655c373ac7bcbe65cd867f5dcc09f76bc614655d",
  "resource_url": "https://raw.githubusercontent.com/congboma/MedErrBench/754c2e083b794f2922f002b893bc2e8890feb16d/datasets/test/reviewed_data_CN_test.csv",
  "source_id": "mederr",
  "source_url": "https://github.com/congboma/MedErrBench",
  "split": "official_test",
  "upstream_group": "cn-test-17",
  "upstream_id": "cn-test-17",
  "version": "754c2e083b794f2922f002b893bc2e8890feb16d"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：0 50 题、1 50 题。

**[MEDEC-MS](../datasets/medec.md)**：MedQA 考试病例改编与专家错误注入；未使用 UW 受控病历。 答案依据：原始 Error Flag 与 Error Sentence ID；原文和更正文均不作模型参考答案。

**[MedErrBench CN](../datasets/mederr.md)**：考试病例改编及专家补充，不声称全部是原始病历。 答案依据：发布方 reviewed_data_CN_test 的错误标记和句子标记。

其中 21 题材料或片段命中过往评测指纹；训练效果对比应核查材料暴露，并对各模型冻结相同子集。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/clinical_error_detection/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/clinical_error_detection/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
