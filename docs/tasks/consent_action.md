# 知情同意与隐私处置选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 只有 3 题，存在伦理和法律语境差异；暂作行动选择探索项，不证明跨地区合规判断能力。

## 任务是什么

根据情境选择知情同意、隐私披露或尊重患者意愿的具体行动；不评价伦理原则名称。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `consent_action` |
| 医疗场景 | 病历与医疗质量控制 |
| 能力维度 | 临床候选方案、流程与下一步行动 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 3 / 100 |
| 来源组数 | 3 |
| 语种 | 英语 2 题、中文 1 题 |
| 数据范围 | 开放许可部分 3 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 1 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [PrinciplismQA](../datasets/principlismqa.md) | 2 | [原始来源](https://github.com/FreedomIntelligence/PrinciplismQA) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`consent_action:cmb:upstream_train_reserved_for_local_evaluation:49762`；语种：中文；来源组：`zh_exam_case:9ed87af4866af3e02cbdd73e`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "王某本人",
        "B": "王某的父母",
        "C": "王某的配偶",
        "D": "王某的单位",
        "E": "王某所在地的卫生行政部门"
      },
      "instructions": "根据情境选择知情同意、隐私披露或尊重患者意愿的具体行动；不评价伦理原则名称。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "王某，35岁，有长期的吸毒史。因为和他人共用同一针头注射而感染了艾滋病。王某住所地的疾病预防控制机构欲以真实姓名公布他的相关病情和有关资料，以引起社会对艾滋病防治工作的关注，此时，应当得到谁的同意"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `A`，对应选项：

```json
"王某本人"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "consent_action:cmb:upstream_train_reserved_for_local_evaluation:49762", "choice": "A"}
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
    "json_index": 49762,
    "zip_member": "CMB/CMB-Exam/CMB-train/CMB-train-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "upstream_train_reserved_for_local_evaluation",
  "upstream_group": "9ed87af4866af3e02cbdd73e",
  "upstream_id": "upstream_train_reserved_for_local_evaluation:49762",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 1 题、C 2 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[PrinciplismQA](../datasets/principlismqa.md)**：上游模型根据医学伦理教材构造题目，经医学专家审核；不是实际临床记录。 答案依据：保留固定清单中处置选择题的原问题、选项及 correct_answer；不纳入开放式问答或原则分类题。

模型构题与筛选可能引入偏差；少量情境题只提供探索性覆盖，不能代表国际伦理共识或法律意见。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/consent_action/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/consent_action/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
