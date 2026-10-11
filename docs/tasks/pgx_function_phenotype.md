# 药物基因功能表型映射

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：辅助评测（不计临床主分数）。** 根据已给功能、活性等映射固定规则，非检测全流程或治疗选择；84 题只有 19 个基因来源组。

## 任务是什么

给定基因、等位基因功能或活性分值，选择 CPIC 固定快照对应的功能表型或等位基因状态。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `pgx_function_phenotype` |
| 医疗场景 | 检查与检验 |
| 能力维度 | 分类与标准化 |
| 评测类别 | 临床计算、解读与证据 |
| 当前题数 / 目标题数 | 84 / 100 |
| 来源组数 | 19 |
| 语种 | 英语 84 题 |
| 数据范围 | 开放许可部分 84 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CPIC curated pharmacogenomic tables](../datasets/cpic.md) | 84 | [原始来源](https://www.clinpgx.org/cpic) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

后续比较模型时，使用相同题目子集，分别记录本任务得分、完整决策耗时与失败率。计时口径见 [评测方法](../EVALUATION.md#耗时测量与结果记录)。当前没有该任务的模型对比成绩。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`pgx_function_phenotype:cpic:8475126`；语种：英语；来源组：`cpic:gene:HLA-A`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "phenotype_0": "*31:01 negative",
        "phenotype_1": "*31:01 positive"
      },
      "instructions": "给定基因、等位基因功能或活性分值，选择 CPIC 固定快照对应的功能表型或等位基因状态。",
      "type": "choice"
    }
  },
  "state": {
    "allele_activity_1": null,
    "allele_activity_2": null,
    "allele_function_1": null,
    "allele_function_2": null,
    "gene": "HLA-A",
    "genetic_findings": {
      "*31:01 negative": 1
    },
    "reference_snapshot": "CPIC API v1, 2026-10-10",
    "total_activity_score": null
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `phenotype_0`，对应选项：

```json
"*31:01 negative"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "pgx_function_phenotype:cpic:8475126", "choice": "phenotype_0"}
```

### 样例溯源

[上游资源](https://api.cpicpgx.org/v1/gene_result_lookup?order=id) · [数据集说明](../datasets/cpic.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "CC0-1.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "gene_result_id": 8475125,
    "json_index": 200,
    "lookup_id": 8475126,
    "supporting_resources": [
      "cpic__gene_result.json"
    ]
  },
  "material_kind": "curated_guideline_rules",
  "resource": "cpic__gene_result_lookup.json",
  "resource_sha256": "f6f4ab80890c0e9db93c313c24a990db969f83f8ce4c409d9b85e741051aa5f1",
  "resource_url": "https://api.cpicpgx.org/v1/gene_result_lookup?order=id",
  "source_id": "cpic",
  "source_url": "https://www.clinpgx.org/cpic",
  "split": "curated_rules_no_patient_split",
  "upstream_group": "gene:HLA-A",
  "upstream_id": "8475126",
  "version": "API v1 response snapshot 2026-10-10"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：phenotype_0 40 题、phenotype_1 16 题、phenotype_2 12 题、phenotype_3 9 题、phenotype_4 4 题、phenotype_5 3 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[CPIC curated pharmacogenomic tables](../datasets/cpic.md)**：CPIC 专家整理的功能到表型映射和基因结果用药建议表，不是患者病例。API 的原始响应随数据包冻结，访问日期不冒充数据库发布版本。 答案依据：功能表型题按 gene_result_lookup.phenotypeid 连接 gene_result.id，复制 result；用药题复制 recommendation_view.drugrecommendation，候选来自相同指南、药物和人群的原始建议。冲突输入和无替代选项排除，不生成临床答案。

只评价固定快照中的规则映射；不代表完整基因型检测、个体化处方或临床结局。指南会更新，应查看对应 guideline URL 的最新内容。按基因和指南分组，每组最多 5 题。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/pgx_function_phenotype/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/pgx_function_phenotype/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
