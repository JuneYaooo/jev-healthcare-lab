# 病例诊断选择：考试病例子集

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 方向适合主评测；与模拟诊断合并报告上层任务，不能仅因来源不同当作两个独立临床能力。

本页为来源子集，统一并入 [病例诊断选择](diagnosis.md) 计分，不另增加任务权重。

## 任务是什么

从给定诊断候选中选择最符合病例者。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `diagnosis_choice` |
| 医疗场景 | 诊断与鉴别 |
| 能力维度 | 临床候选方案 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 100 |
| 语种 | 中文 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 50 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 50 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下为合并后的病例诊断任务成绩，两个来源子集共 200 题；逐来源结果保存在评分文件中。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

| 模型 | 准确率 | 有效回答 / 题数 | 平均秒 | P50 秒 | P95 秒 | 任务总秒 | 超时 / 请求失败 / 无效回答 | 重试次数 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | 79.50% | 200 / 200 | 1.047 | 0.990 | 1.377 | 26.649 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/jev-1.13.0/config.json) · [响应](../../results/clinical-20261012/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-20261012/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 84.00% | 200 / 200 | 0.586 | 0.473 | 0.777 | 24.209 | 0 / 0 / 0 | 1 | [配置](../../results/clinical-20261012/deepseek-flash/config.json) · [响应](../../results/clinical-20261012/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-20261012/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 81.00% | 200 / 200 | 0.994 | 0.961 | 1.323 | 25.291 | 0 / 0 / 0 | 4 | [配置](../../results/clinical-20261012/deepseek-v4-pro/config.json) · [响应](../../results/clinical-20261012/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-20261012/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 66.00% | 200 / 200 | 1.283 | 0.821 | 4.233 | 33.379 | 0 / 0 / 0 | 1 | [配置](../../results/clinical-20261012/qwen3.5-9b/config.json) · [响应](../../results/clinical-20261012/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-20261012/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 77.00% | 200 / 200 | 3.025 | 2.486 | 6.496 | 76.025 | 0 / 0 / 0 | 1 | [配置](../../results/clinical-20261012/qwen3.8-27b/config.json) · [响应](../../results/clinical-20261012/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-20261012/qwen3.8-27b/scores.json) |

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`diagnosis_choice:cmb:9865`；语种：中文；来源组：`zh_exam_case:462c68717b08a15194bac182`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "肠结核",
        "B": "溃疡性结肠炎",
        "C": "克罗恩病",
        "D": "结肠癌",
        "E": "结肠息肉"
      },
      "instructions": "从给定诊断候选中选择最符合病例者。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "男性，36岁。黏液脓血便1年，无发热，常伴里急后重。查体：左下腹轻压痛，未触及包块。胸部X线检查：未见异常。最可能的诊断是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `B`，对应选项：

```json
"溃疡性结肠炎"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "diagnosis_choice:cmb:9865", "choice": "B"}
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
    "answer_json_index": 9864,
    "json_index": 9864,
    "question_id": 9865,
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
  "upstream_group": "9865",
  "upstream_id": "9865",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 10 题、B 10 题、C 10 题、D 10 题、E 10 题、opa 10 题、opb 10 题、opc 10 题、opd 10 题、ope 10 题。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [CMExam](../datasets/cmexam.md) | Apache 标识与 README 学术/研究限制并存，先澄清数据授权范围；病例题也需筛选。 |
| [MedJourney](../datasets/medjourney.md) | 未见明确数据许可；部分任务共用 CMB/CMExam 上游 |
| [MedMCQA](../datasets/medmcqa.md) | 本任务暂无收录，是否适用需按任务定义核验。 |
| [MedXpertQA](../datasets/medxpertqa.md) | 论文附录提出不在线分享题例；在与 MIT 数据卡的适用范围澄清前仅引用，不在本仓库再分发题目。 |
| [MLEC-QA](../datasets/mlec_qa.md) | 需下载官方包核对独立数据许可、测试划分和共享题干；仅收病例决策单选。 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/diagnosis_choice/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/diagnosis_choice/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
