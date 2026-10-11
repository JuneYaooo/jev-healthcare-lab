# 中药处方审核规范情境问答

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 11 题多为一般审核规范、签名或用量规则，没有完整患者与处方；有政策时效和适用范围条件，暂不当作个体处方适宜性评测。

## 任务是什么

给定处方审核情境，从原始选项中选择上游标注的处理行动或审核要求。按发布版本评分，不等同现行政策核验或完整个体处方审核。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `prescription_audit_action` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 分类与标准化 |
| 评测类别 | 流程与记录核对 |
| 当前题数 / 目标题数 | 11 / 100 |
| 来源组数 | 11 |
| 语种 | 中文 11 题 |
| 数据范围 | 开放许可部分 11 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [TCMEval-PA](../datasets/tcmeval_pa.md) | 11 | [原始来源](https://doi.org/10.6084/m9.figshare.29651261.v3) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`prescription_audit_action:tcmeval_pa:226`；语种：中文；来源组：`tcmeval_pa:5edec134991920173defec35`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "患者书面同意",
        "B": "医师双签字确认",
        "C": "药师加注备注",
        "D": "护士会诊",
        "E": "药房主任批准"
      },
      "instructions": "给定处方审核情境，从原始选项中选择上游标注的处理行动或审核要求。按发布版本评分，不等同现行政策核验或完整个体处方审核。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "若确因病情需要超规格使用药味数，通过审核前必须满足哪项要求？"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `B`，对应选项：

```json
"医师双签字确认"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "prescription_audit_action:tcmeval_pa:226", "choice": "B"}
```

### 样例溯源

[上游资源](https://ndownloader.figshare.com/files/56581880) · [数据集说明](../datasets/tcmeval_pa.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_column": "D",
    "upstream_id": "226",
    "xlsx_row": 227,
    "xlsx_sheet": "单选-多选"
  },
  "material_kind": "exam_and_rule_based_scenarios",
  "resource": "tcmeval_pa__TCMEval-PA.xlsx",
  "resource_sha256": "905cb28f145ba50f3b1c912265ff6649e0bb38f56adf6cd588d77ca768db92c1",
  "resource_url": "https://ndownloader.figshare.com/files/56581880",
  "source_id": "tcmeval_pa",
  "source_url": "https://doi.org/10.6084/m9.figshare.29651261.v3",
  "split": "published_benchmark_no_official_split",
  "upstream_group": "5edec134991920173defec35",
  "upstream_id": "226",
  "version": "Figshare 29651261.v3"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：B 2 题、C 7 题、D 2 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[TCMEval-PA](../datasets/tcmeval_pa.md)**：考试题与规则情境题，经上游中医执业医师核验；不是实际处方审核日志。 答案依据：保留原 Excel 单选答案；仅纳入固定清单的情境处置题，不使用解释字段作为输入。

固定发布版本的上游答案；未作本项目独立临床或现行规范核验。数据许可按 Figshare 数据记录，区别于论文或仓库其他内容许可。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/prescription_audit_action/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/prescription_audit_action/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
