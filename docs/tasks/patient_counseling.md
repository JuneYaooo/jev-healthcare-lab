# 患者教育与沟通选择

[返回首页](../../README.md) · [全部任务](README.md) · [数据集目录](../datasets/README.md)

## 任务是什么

根据情境选择教育重点、教育方式或沟通表达；仅选择上游选项，不生成话术。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `patient_counseling` |
| 医疗场景 | 出院与随访 |
| 能力维度 | 临床候选方案、流程与下一步行动 |
| 决策类型 | 临床候选方案选择 |
| 当前题数 / 目标题数 | 11 / 100 |
| 来源组数 | 11 |
| 语种 | 中文 11 题 |
| 数据范围 | 开放许可核心集 11 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 11 | [原始来源](https://github.com/FreedomIntelligence/CMB) |

## 如何作答与评分

根据题目给定的材料和规则，从 `request.questions.decision.criteria` 选择一个选项键。选项随题目变化；`gold` 保存标准选项键，不向模型发送。按选项键计准确率、宏 F1 和逐类召回，缺失或无效回答按错计。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`patient_counseling:cmb:upstream_train_reserved_for_local_evaluation:131110`；语种：中文；来源组：`zh_exam_case:0d24cc604d5962397b85e9b6`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "录像",
        "B": "小册子",
        "C": "座谈会",
        "D": "个别教育",
        "E": "专题讲座"
      },
      "instructions": "根据情境选择教育重点、教育方式或沟通表达；仅选择上游选项，不生成话术。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "王先生，68岁，3个月前因急性脑梗死致左侧肢体偏瘫，出院后生活在家中，由老伴照顾。对王某进行健康教育时，首选的健康教育形式是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `D`，对应选项：

```json
"个别教育"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "patient_counseling:cmb:upstream_train_reserved_for_local_evaluation:131110", "choice": "D"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip) · [数据集说明](../datasets/cmb.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "Apache-2.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field": "answer",
    "json_index": 131110,
    "zip_member": "CMB/CMB-Exam/CMB-train/CMB-train-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "upstream_train_reserved_for_local_evaluation",
  "upstream_group": "0d24cc604d5962397b85e9b6",
  "upstream_id": "upstream_train_reserved_for_local_evaluation:131110",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 1 题、C 4 题、D 4 题、E 2 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 本任务暂无收录，是否适用需按任务定义核验。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/patient_counseling/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/patient_counseling/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
