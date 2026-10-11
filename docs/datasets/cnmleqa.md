# CNMLEQA-10k（中文案例分析子集）

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `cnmleqa` |
| 上游入口 | [发布方页面](https://doi.org/10.5281/zenodo.18951465) |
| 收录情况 | 426 题 / 15 个任务 |
| 评测用途 | 临床主评测 426 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | CC-BY-4.0 |
| 收录语种 | 中文 426 题 |

## 来源与引用

Zong et al., Scientific Data (2026)

[论文或项目引用](https://doi.org/10.1038/s41597-026-07261-9) · [数据许可](https://creativecommons.org/licenses/by/4.0/)

许可与说明快照：[zenodo-metadata.json](../../benchmarks/medical_decision_v1/sources/cnmleqa/zenodo-metadata.json) · [README.md](../../benchmarks/medical_decision_v1/sources/cnmleqa/README.md)

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [给药途径与实施方法选择](../tasks/administration_route_choice.md) | 临床主评测 | 1 | 根据给药情境选择途径或实施方法；不等同从原文提取给药途径。 |
| [病例并发症判断](../tasks/case_complication.md) | 临床主评测 | 36 | 根据病例从原选项中选择最可能的并发症；不是主诊断任务。 |
| [病例病因判断](../tasks/case_etiology.md) | 临床主评测 | 50 | 根据病例从原选项中选择导致所述疾病、症状或事件的最可能原因。 |
| [疾病分期与严重程度判断](../tasks/clinical_grade.md) | 临床主评测 | 30 | 根据病例从原选项中选择疾病分期、严重程度分度或功能分级。 |
| [病例诊断选择：考试病例子集](../tasks/diagnosis_choice.md) | 临床主评测 | 50 | 从给定诊断候选中选择最符合病例者。 |
| [检查方案选择](../tasks/examination_choice.md) | 临床主评测 | 81 | 根据病例从给定候选中选择检查。 |
| [补液方案选择](../tasks/fluid_plan.md) | 临床主评测 | 7 | 根据病例从原选项中选择补液量、溶液或补液方案。 |
| [复查项目与随访时机选择](../tasks/followup_plan.md) | 临床主评测 | 2 | 根据完整病例选择复查项目或随访时机；不等同待办是否完成或逾期。 |
| [感染防控措施选择](../tasks/infection_precaution.md) | 临床主评测 | 1 | 根据患者或病区情境选择隔离、无菌操作、消毒或阻断传播措施。 |
| [用药方案选择](../tasks/medication_choice.md) | 临床主评测 | 88 | 根据病例从给定候选中选择用药。 |
| [营养与饮食方案选择](../tasks/nutrition_plan.md) | 临床主评测 | 1 | 根据病例选择原题要求的饮食或营养支持方案；保留上游选项及答案，不生成食谱。 |
| [患者方案禁忌判断](../tasks/patient_contraindication.md) | 临床主评测 | 21 | 根据病例从原选项中选择不宜使用或禁忌的药物、检查或治疗方案。 |
| [护理与操作体位选择](../tasks/positioning_choice.md) | 临床主评测 | 2 | 根据患者病情或操作情境，从原始选项中选择合适体位。 |
| [预防措施选择](../tasks/prevention_choice.md) | 临床主评测 | 2 | 根据病例、暴露或复发风险，选择预防行动；不评价预防等级概念。 |
| [治疗方案选择](../tasks/treatment_choice.md) | 临床主评测 | 54 | 根据病例从给定候选中选择治疗。 |

## 答案与格式转换

只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`diagnosis_choice:cnmleqa:70b95ea3-d465-503c-88f0-78920f610b5e`；语种：中文；来源组：`zh_exam_case:5fa3818d38ee77a0d1534854`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "opa": "麻疹",
        "opb": "风疹",
        "opc": "水痘",
        "opd": "猩红热",
        "ope": "肺炎"
      },
      "instructions": "从给定诊断候选中选择最符合病例者。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "女，2岁，发热3天，体温39度，流涕，咳嗽。皮肤出现红色斑丘疹，体温升至40度。颊黏膜粗糙，可见白色斑点。最可能的诊断是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `opa`，对应选项：

```json
"麻疹"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "diagnosis_choice:cnmleqa:70b95ea3-d465-503c-88f0-78920f610b5e", "choice": "opa"}
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
    "json_index": 8035,
    "original_source": "pubmed-38684792;github-llm-for-clinical",
    "question_id": "70b95ea3-d465-503c-88f0-78920f610b5e"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cnmleqa__CNMLEQA-10k.json",
  "resource_sha256": "c6a87366474b6ef638df7d093f4f004f726cb859d5c9d1c8784185d9d2029275",
  "resource_url": "https://zenodo.org/api/records/18951465/files/CNMLEQA-10k.json/content",
  "source_id": "cnmleqa",
  "source_url": "https://doi.org/10.5281/zenodo.18951465",
  "split": "published_benchmark_no_official_split",
  "upstream_group": "70b95ea3-d465-503c-88f0-78920f610b5e",
  "upstream_id": "70b95ea3-d465-503c-88f0-78920f610b5e",
  "version": "zenodo.18951465"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[病例诊断选择：考试病例子集](../tasks/diagnosis_choice.md)。

## 相关任务调研

以下为曾考虑使用此来源的任务，不代表已采用：

| 任务说明 | 任务内容 |
| --- | --- |
| [护理措施选择](../tasks/nursing_priority.md) | 根据病例从原选项中选择正确、首要或最合适的护理措施；不生成护理文书。 |
| [病情监测与疗效判断](../tasks/monitoring_target.md) | 根据病例选择当前最应监测的变量或观察重点，不进行新诊断。 |
| [康复训练方案选择](../tasks/rehabilitation_choice.md) | 根据功能状态或术后阶段选择原题中的训练方案。 |
| [健康教育与沟通行动选择](../tasks/patient_counseling.md) | 根据情境选择教育重点、教育方式或沟通表达；仅选择上游选项，不生成话术。 |

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
