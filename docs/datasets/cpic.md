# CPIC curated pharmacogenomic tables

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

CPIC 专家整理的功能到表型映射和基因结果用药建议表，不是患者病例。API 的原始响应随数据包冻结，访问日期不冒充数据库发布版本。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `cpic` |
| 上游入口 | [发布方页面](https://www.clinpgx.org/cpic) |
| 收录情况 | 184 题 / 2 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | CC0-1.0 |
| 收录语种 | 英语 184 题 |

## 来源与引用

Clinical Pharmacogenetics Implementation Consortium (CPIC), curated database API v1, accessed 2026-10-10. Primary source: www.clinpgx.org; recommendation records retain their specific guideline URL.

[论文或项目引用](https://github.com/cpicpgx/cpic-data/wiki) · [数据许可](https://raw.githubusercontent.com/cpicpgx/cpic-data/82aa2518f1051bb2db9c42c1023a9f08db5a5f80/LICENSE.md)

许可与说明快照：[LICENSE.md](../../benchmarks/medical_decision_v1/sources/cpic/LICENSE.md) · [api-documentation.md](../../benchmarks/medical_decision_v1/sources/cpic/api-documentation.md)

### 使用限制

只评价固定快照中的规则映射；不代表完整基因型检测、个体化处方或临床结局。指南会更新，应查看对应 guideline URL 的最新内容。按基因和指南分组，每组最多 5 题。

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [药物基因检测功能表型判定](../tasks/pgx_function_phenotype.md) | 84 | 给定基因、等位基因功能或活性分值，选择 CPIC 固定快照对应的功能表型或等位基因状态。 |
| [药物基因结果用药建议匹配](../tasks/pgx_guideline_recommendation.md) | 100 | 给定药物、人群及基因结果，选择 CPIC 固定快照中对应的原始用药建议；不外推为完整个体处方。 |

## 答案与格式转换

功能表型题按 gene_result_lookup.phenotypeid 连接 gene_result.id，复制 result；用药题复制 recommendation_view.drugrecommendation，候选来自相同指南、药物和人群的原始建议。冲突输入和无替代选项排除，不生成临床答案。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

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

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[药物基因结果用药建议匹配](../tasks/pgx_guideline_recommendation.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
