# 预防措施选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 13 题混合个体、接触者及群体防控措施；原个体预防名称偏窄，需按作用对象分层。

## 任务是什么

根据病例、暴露或复发风险，选择预防行动；不评价预防等级概念。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `prevention_choice` |
| 医疗场景 | 出院与随访 |
| 能力维度 | 临床候选方案、流程与下一步行动 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 13 / 100 |
| 来源组数 | 13 |
| 语种 | 英语 1 题、中文 12 题 |
| 数据范围 | 开放许可部分 13 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 10 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 2 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |
| [MedMCQA](../datasets/medmcqa.md) | 1 | [原始来源](https://huggingface.co/datasets/openlifescienceai/medmcqa) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，在本次所选许可范围内少于 20 题的任务仅给探索性结果，不进入汇总。20 题是最低汇总门槛，不是统计充分性或临床有效性保证。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

| 模型 | 准确率 | 有效回答 / 题数 | 平均秒 | P50 秒 | P95 秒 | 任务总秒 | 超时 / 请求失败 / 无效回答 | 重试次数 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | 84.62% | 13 / 13 | 0.898 | 0.898 | 1.011 | 1.849 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/jev-1.13.0/config.json) · [响应](../../results/clinical-20261012/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-20261012/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 84.62% | 13 / 13 | 0.432 | 0.406 | 0.831 | 0.994 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/deepseek-flash/config.json) · [响应](../../results/clinical-20261012/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-20261012/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 84.62% | 13 / 13 | 0.881 | 0.924 | 1.128 | 1.911 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/deepseek-v4-pro/config.json) · [响应](../../results/clinical-20261012/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-20261012/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 76.92% | 13 / 13 | 0.720 | 0.606 | 1.732 | 1.735 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/qwen3.5-9b/config.json) · [响应](../../results/clinical-20261012/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-20261012/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 92.31% | 13 / 13 | 1.407 | 1.634 | 1.835 | 2.815 | 0 / 0 / 0 | 0 | [配置](../../results/clinical-20261012/qwen3.8-27b/config.json) · [响应](../../results/clinical-20261012/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-20261012/qwen3.8-27b/scores.json) |

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`prevention_choice:cmb:upstream_train_reserved_for_local_evaluation:17553`；语种：中文；来源组：`zh_exam_case:3f7ba69a1d52e9d79c26aef0`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "避免关节损伤",
        "B": "忌海鲜",
        "C": "减少体育运动",
        "D": "长效青霉素肌注",
        "E": "激素吸入维持"
      },
      "instructions": "根据病例、暴露或复发风险，选择预防行动；不评价预防等级概念。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "10岁男孩，因发热，关节肿痛，皮肤出现环行红斑，心率快出现奔马律，血沉增快，经治疗上述症状、体征消失后。需继发性预防的方法是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `D`，对应选项：

```json
"长效青霉素肌注"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "prevention_choice:cmb:upstream_train_reserved_for_local_evaluation:17553", "choice": "D"}
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
    "json_index": 17553,
    "zip_member": "CMB/CMB-Exam/CMB-train/CMB-train-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "upstream_train_reserved_for_local_evaluation",
  "upstream_group": "3f7ba69a1d52e9d79c26aef0",
  "upstream_id": "upstream_train_reserved_for_local_evaluation:17553",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 1 题、B 5 题、D 3 题、E 1 题、opb 1 题、opc 1 题、opd 1 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

**[MedMCQA](../datasets/medmcqa.md)**：印度医学考试题；不是患者观察队列。 答案依据：仅用官方 validation、choice_type=single；cop 的 0–3 原样映射 opa–opd。

采用数据卡 Apache-2.0，而非代码仓库许可。仅固定范围清单病例题，未独立核验现行临床规范。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/prevention_choice/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/prevention_choice/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
