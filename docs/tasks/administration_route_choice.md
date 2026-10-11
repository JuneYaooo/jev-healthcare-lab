# 给药途径与实施方法选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 方向适合，仅 4 题，包含途径、皮试浓度和脱敏注射方法；不等同原文途径关联。

## 任务是什么

根据给药情境选择途径或实施方法；不等同从原文提取给药途径。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `administration_route_choice` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 临床候选方案、流程与下一步行动 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 4 / 100 |
| 来源组数 | 4 |
| 语种 | 中文 4 题 |
| 数据范围 | 开放许可部分 4 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 3 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 1 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

本轮 JEV 与两个 DeepSeek 模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

| 模型 | 准确率 | 平均完整耗时（秒） | P95（秒） |
| --- | --- | --- | --- |
| JEV 1.13 | 75.00% | 0.946 | 1.008 |
| DeepSeek V4.1 Flash | 75.00% | 0.576 | 0.832 |
| DeepSeek V4 Pro | 75.00% | 0.883 | 0.951 |

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`administration_route_choice:cnmleqa:5f268e0d-c97b-56d4-8a6d-489b6720824c`；语种：中文；来源组：`zh_exam_case:5c70aad5caab3d168071c866`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "opa": "静脉注射",
        "opb": "心内注射",
        "opc": "肌肉注射",
        "opd": "气管内给药",
        "ope": "皮下注射"
      },
      "instructions": "根据给药情境选择途径或实施方法；不等同从原文提取给药途径。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "男，72岁。排便时突然跌倒，意识丧失，呼吸断续。有陈旧心肌梗死和糖尿病病史，无高血压病史，诊断为心脏骤停。3．最佳的给药途径是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `opa`，对应选项：

```json
"静脉注射"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "administration_route_choice:cnmleqa:5f268e0d-c97b-56d4-8a6d-489b6720824c", "choice": "opa"}
```

### 样例溯源

[上游资源](https://zenodo.org/api/records/18951465/files/CNMLEQA-10k.json/content) · [数据集说明](../datasets/cnmleqa.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC-BY-4.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_field": "answer",
    "json_index": 6450,
    "question_id": "5f268e0d-c97b-56d4-8a6d-489b6720824c"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cnmleqa__CNMLEQA-10k.json",
  "resource_sha256": "c6a87366474b6ef638df7d093f4f004f726cb859d5c9d1c8784185d9d2029275",
  "resource_url": "https://zenodo.org/api/records/18951465/files/CNMLEQA-10k.json/content",
  "source_id": "cnmleqa",
  "source_url": "https://doi.org/10.5281/zenodo.18951465",
  "split": "published_benchmark_no_official_split",
  "upstream_group": "5c70aad5caab3d168071c866",
  "upstream_id": "5f268e0d-c97b-56d4-8a6d-489b6720824c",
  "version": "zenodo.18951465"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：C 2 题、E 1 题、opa 1 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/administration_route_choice/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/administration_route_choice/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
