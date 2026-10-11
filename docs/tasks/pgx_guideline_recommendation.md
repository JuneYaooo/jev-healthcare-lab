# 药物基因结果对应的指南建议选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 输出用药建议，方向适合但为固定指南规则选择，无完整患者记录；应与病例治疗分层而非声称个体处方能力。

## 任务是什么

给定药物、人群及基因结果，选择 CPIC 固定快照中对应的原始用药建议；不外推为完整个体处方。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `pgx_guideline_recommendation` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 资格与适宜性 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 25 |
| 语种 | 英语 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CPIC curated pharmacogenomic tables](../datasets/cpic.md) | 100 | [原始来源](https://www.clinpgx.org/cpic) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

本轮 JEV 与两个 DeepSeek 模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

| 模型 | 准确率 | 平均完整耗时（秒） | P95（秒） |
| --- | --- | --- | --- |
| JEV 1.13 | 55.00% | 0.993 | 1.278 |
| DeepSeek V4.1 Flash | 54.00% | 0.492 | 0.740 |
| DeepSeek V4 Pro | 51.00% | 1.084 | 1.718 |

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`pgx_guideline_recommendation:cpic:8479701`；语种：英语；来源组：`cpic:guideline:https://www.clinpgx.org/guideline/PA166251444`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "action_0": "Abacavir is not recommended",
        "action_1": "Use abacavir per standard dosing guidelines"
      },
      "instructions": "给定药物、人群及基因结果，选择 CPIC 固定快照中对应的原始用药建议；不外推为完整个体处方。",
      "type": "choice"
    }
  },
  "state": {
    "drug": "abacavir",
    "gene_results": {
      "HLA-B": "*57:01 negative"
    },
    "guideline": "HLA-B and Abacavir",
    "population": "general",
    "reference_snapshot": "CPIC API v1, 2026-10-10"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `action_1`，对应选项：

```json
"Use abacavir per standard dosing guidelines"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "pgx_guideline_recommendation:cpic:8479701", "choice": "action_1"}
```

### 样例溯源

[上游资源](https://api.cpicpgx.org/v1/recommendation_view?order=recommendationid) · [数据集说明](../datasets/cpic.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC0-1.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "candidate_json_indices": [
      0,
      1
    ],
    "json_index": 0,
    "recommendation_id": 8479701
  },
  "material_kind": "curated_guideline_rules",
  "resource": "cpic__recommendation_view.json",
  "resource_sha256": "8b4559a9b0b851fec69464cc5c62932d95d385bca59d725b03570f92c700bc85",
  "resource_url": "https://api.cpicpgx.org/v1/recommendation_view?order=recommendationid",
  "source_id": "cpic",
  "source_url": "https://www.clinpgx.org/cpic",
  "split": "curated_rules_no_patient_split",
  "upstream_group": "guideline:https://www.clinpgx.org/guideline/PA166251444",
  "upstream_id": "8479701",
  "version": "API v1 response snapshot 2026-10-10"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：action_0 23 题、action_1 19 题、action_11 1 题、action_14 1 题、action_2 24 题、action_3 17 题、action_4 9 题、action_5 2 题、action_6 1 题、action_8 2 题、action_9 1 题。

**[CPIC curated pharmacogenomic tables](../datasets/cpic.md)**：CPIC 专家整理的功能到表型映射和基因结果用药建议表，不是患者病例。API 的原始响应随数据包冻结，访问日期不冒充数据库发布版本。 答案依据：功能表型题按 gene_result_lookup.phenotypeid 连接 gene_result.id，复制 result；用药题复制 recommendation_view.drugrecommendation，候选来自相同指南、药物和人群的原始建议。冲突输入和无替代选项排除，不生成临床答案。

只评价固定快照中的规则映射；不代表完整基因型检测、个体化处方或临床结局。指南会更新，应查看对应 guideline URL 的最新内容。按基因和指南分组，每组最多 5 题。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/pgx_guideline_recommendation/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/pgx_guideline_recommendation/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
