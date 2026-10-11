# CMB-Exam（中文病例单选子集）

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `cmb` |
| 上游入口 | [发布方页面](https://github.com/FreedomIntelligence/CMB) |
| 收录情况 | 454 题 / 20 个任务 |
| 使用范围 | 开放许可核心集 |
| 登记的数据许可 | Apache-2.0 |
| 收录语种 | 中文 454 题 |

## 来源与引用

Wang et al., CMB (NAACL 2024)

[论文或项目引用](https://arxiv.org/abs/2308.08833) · [数据许可](https://www.apache.org/licenses/LICENSE-2.0)

许可与说明快照：[LICENSE](../../benchmarks/medical_decision_v1/sources/cmb/LICENSE) · [README.md](../../benchmarks/medical_decision_v1/sources/cmb/README.md) · [HF_DATA_CARD.md](../../benchmarks/medical_decision_v1/sources/cmb/HF_DATA_CARD.md)

## 用于哪些任务

| 任务说明 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- |
| [给药途径与方法选择](../tasks/administration_route_choice.md) | 3 | 根据给药情境选择途径或实施方法；不等同从原文提取给药途径。 |
| [病例并发症判断](../tasks/case_complication.md) | 64 | 根据病例从原选项中选择最可能的并发症；不是主诊断任务。 |
| [病例病因与原因判断](../tasks/case_etiology.md) | 50 | 根据病例从原选项中选择导致所述疾病、症状或事件的最可能原因。 |
| [临床分级与分期选择](../tasks/clinical_grade.md) | 70 | 根据病例从原选项中选择疾病分期、严重程度分度或功能分级。 |
| [知情与隐私处置选择](../tasks/consent_action.md) | 1 | 根据情境选择知情同意、隐私披露或尊重患者意愿的具体行动；不评价伦理原则名称。 |
| [临床病例候选诊断](../tasks/diagnosis_choice.md) | 50 | 从给定诊断候选中选择最符合病例者。 |
| [检查方案选择](../tasks/examination_choice.md) | 19 | 根据病例从给定候选中选择检查。 |
| [补液方案选择](../tasks/fluid_plan.md) | 9 | 根据病例从原选项中选择补液量、溶液或补液方案。 |
| [随访方案选择](../tasks/followup_plan.md) | 3 | 根据完整病例选择复查项目或随访时机；不等同待办是否完成或逾期。 |
| [感染防控措施选择](../tasks/infection_precaution.md) | 4 | 根据患者或病区情境选择隔离、无菌操作、消毒或阻断传播措施。 |
| [用药方案选择](../tasks/medication_choice.md) | 12 | 根据病例从给定候选中选择用药。 |
| [病情监测指标选择](../tasks/monitoring_target.md) | 5 | 根据病例选择当前最应监测的变量或观察重点，不进行新诊断。 |
| [护理措施选择](../tasks/nursing_priority.md) | 42 | 根据病例从原选项中选择正确、首要或最合适的护理措施；不生成护理文书。 |
| [病例营养方案选择](../tasks/nutrition_plan.md) | 10 | 根据病例选择原题要求的饮食或营养支持方案；保留上游选项及答案，不生成食谱。 |
| [患者特异性禁忌选择](../tasks/patient_contraindication.md) | 33 | 根据病例从原选项中选择不宜使用或禁忌的药物、检查或治疗方案。 |
| [患者教育与沟通选择](../tasks/patient_counseling.md) | 11 | 根据情境选择教育重点、教育方式或沟通表达；仅选择上游选项，不生成话术。 |
| [护理体位选择](../tasks/positioning_choice.md) | 8 | 根据患者病情或操作情境，从原始选项中选择合适体位。 |
| [个体预防方案选择](../tasks/prevention_choice.md) | 10 | 根据病例、暴露或复发风险，选择预防行动；不评价预防等级概念。 |
| [康复训练方案选择](../tasks/rehabilitation_choice.md) | 4 | 根据功能状态或术后阶段选择原题中的训练方案。 |
| [治疗方案选择](../tasks/treatment_choice.md) | 46 | 根据病例从给定候选中选择治疗。 |

## 答案与格式转换

固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`medication_choice:cmb:484`；语种：中文；来源组：`zh_exam_case:8a058cac7751eb24e2eaf744`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "止带方",
        "B": "知柏地黄丸",
        "C": "完带汤",
        "D": "六味地黄丸",
        "E": "内补丸"
      },
      "instructions": "根据病例从给定候选中选择用药。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "患者，女，30岁，已婚。近感带下量增多，伴阴道灼热、干涩，腰膝酸软，头晕耳鸣，五心烦热，舌红苔黄，脉细数。治疗首选方剂为"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `B`，对应选项：

```json
"知柏地黄丸"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "medication_choice:cmb:484", "choice": "B"}
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
    "answer_json_index": 483,
    "json_index": 483,
    "question_id": 484,
    "supporting_resources": [
      "cmb__CMB-test-choice-answer.json"
    ],
    "zip_member": "CMB/CMB-Exam/CMB-test/CMB-test-choice-question-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "official_test",
  "upstream_group": "484",
  "upstream_id": "484",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[用药方案选择](../tasks/medication_choice.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
