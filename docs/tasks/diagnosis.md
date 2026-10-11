# 病例诊断选择

[返回首页](../../README.md) · [临床主评测任务](README.md)

根据给定病例资料，从候选中选择诊断。考试病例与模拟病例作为同一个评测任务的来源子集；题目和原答案保留，不因拆分来源重复增加任务权重。

共 200 题。合并后按全部题目计算任务准确率，并保留每个来源子集的结果。选项含义随题变化，不计算临床类别 F1。

| 来源子集与完整样例 | 题数 |
| --- | --- |
| [病例诊断选择：模拟病例子集](../tasks/synthetic_diagnosis.md) | 100 |
| [病例诊断选择：考试病例子集](../tasks/diagnosis_choice.md) | 100 |

## 样例与来源

两个来源子集的说明页分别给出完整输入、原选项、标准答案和溯源。以下为考试病例子集中的一题：

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

## 模型结果

两个诊断来源合并为 200 题。有效回答不代表答对；任务总秒为墙钟时间，单题平均值与分位数包含失败耗时。响应链接包含该模型全部题目。

| 模型 | 准确率 | 有效回答 / 题数 | 平均秒 | P50 秒 | P95 秒 | 任务总秒 | 超时 / 请求失败 / 无效回答 | 重试次数 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | 79.50% | 200 / 200 | 1.047 | 0.990 | 1.377 | 26.649 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/jev-1.13.0/config.json) · [响应](../../results/clinical-20261012/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-20261012/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 84.00% | 200 / 200 | 0.586 | 0.473 | 0.777 | 24.209 | 0 / 0 / 0 | 1 | [配置](../../results/clinical-20261012/deepseek-flash/config.json) · [响应](../../results/clinical-20261012/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-20261012/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 81.00% | 200 / 200 | 0.994 | 0.961 | 1.323 | 25.291 | 0 / 0 / 0 | 4 | [配置](../../results/clinical-20261012/deepseek-v4-pro/config.json) · [响应](../../results/clinical-20261012/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-20261012/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 66.00% | 200 / 200 | 1.283 | 0.821 | 4.233 | 33.379 | 0 / 0 / 0 | 1 | [配置](../../results/clinical-20261012/qwen3.5-9b/config.json) · [响应](../../results/clinical-20261012/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-20261012/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 77.00% | 200 / 200 | 3.025 | 2.486 | 6.496 | 76.025 | 0 / 0 / 0 | 1 | [配置](../../results/clinical-20261012/qwen3.8-27b/config.json) · [响应](../../results/clinical-20261012/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-20261012/qwen3.8-27b/scores.json) |

[完整得分、耗时与运行条件](../MODEL_RESULTS.md)

## 评测边界

考试病例与模拟病例分别报告，不能把模拟患者当成真实患者。候选数量与题型不同，比较模型时冻结同一批题目和选项。

[返回首页](../../README.md)
