# 病例并发症判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 根据新表现判断并发症，适合主评测；按诊断相关子类汇总。

## 任务是什么

根据病例从原选项中选择最可能的并发症；不是主诊断任务。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `case_complication` |
| 医疗场景 | 住院与护理 |
| 能力维度 | 风险与升级 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 96 |
| 语种 | 中文 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 64 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 36 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

## 如何作答与评分

根据材料从 `request.questions.decision.criteria` 选择一个选项键。`gold` 不向模型发送。缺失或无效回答按错计。按各题候选独立评分，只报告准确率和来源组结果；不对局部选项键计算临床类别 F1。

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | **93.00%** | 100 / 100 | 1.018 | 0.884 | 1.357 | 15.615 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 89.00% | 100 / 100 | **0.439** | **0.433** | **0.579** | **5.669** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 89.00% | 100 / 100 | 0.960 | 0.917 | 1.325 | 12.224 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 70.00% | 100 / 100 | 1.173 | 0.669 | 4.746 | 16.190 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 84.00% | 100 / 100 | 2.439 | 1.950 | 6.121 | 31.068 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

本轮多题结果（固定最大打包档，对比 Flash）：JEV 93.75%，Flash 57.29% ⚠；JEV 耗时少 71.5%；JEV 成本低 40.5%–70.3%。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 94.79% | 8.324 | 3.84 / 3.64 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 90.62% | 20.166 | 1.59 / 1.44 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 93.75% | 1.622 | 19.73 / 18.49 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 90.62% | 2.876 | 11.13 / 10.08 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | JEV 1.13 | 93.75% | 0.587 | 54.54 / 51.13 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 89.58% | 1.055 | 30.32 / 27.16 | 96 / 96 | 0 |
| 多题打包 | 1 | 8 | JEV 1.13 | 95.83% | 1.698 | 18.85 / 18.07 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 67.71% | 3.370 | 8.21 / 6.43 | 7 / 12 | 5 |
| 多题打包 | 1 | 32 | JEV 1.13 | 93.75% | 0.334 | 95.74 / 89.76 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 57.29% | 1.174 | 18.74 / 15.62 | 0 / 3 | 3 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 7.650–9.081 | 0.257 | 0.306 | 0.353 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-024.jsonl) · [轮2](../../results/task-performance-v1/cell-421.jsonl) · [轮3](../../results/task-performance-v1/cell-673.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 19.298–21.310 | 0.642 | 0.854 | 1.100 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-224.jsonl) · [轮2](../../results/task-performance-v1/cell-315.jsonl) · [轮3](../../results/task-performance-v1/cell-622.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.574–1.680 | 0.263 | 0.838 | 0.969 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-133.jsonl) · [轮2](../../results/task-performance-v1/cell-458.jsonl) · [轮3](../../results/task-performance-v1/cell-650.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.815–2.933 | 0.647 | 0.814 | 1.055 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-066.jsonl) · [轮2](../../results/task-performance-v1/cell-446.jsonl) · [轮3](../../results/task-performance-v1/cell-591.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.323–1.055 | 0.272 | 0.993 | 1.055 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-111.jsonl) · [轮2](../../results/task-performance-v1/cell-342.jsonl) · [轮3](../../results/task-performance-v1/cell-578.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.912–1.150 | 0.754 | 1.048 | 1.140 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-164.jsonl) · [轮2](../../results/task-performance-v1/cell-330.jsonl) · [轮3](../../results/task-performance-v1/cell-486.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.160–2.666 | 0.287 | 样本不足 | 1.681 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-203.jsonl) · [轮2](../../results/task-performance-v1/cell-261.jsonl) · [轮3](../../results/task-performance-v1/cell-574.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 2.826–3.787 | 0.735 | 样本不足 | 1.065 | 0 | 0 / 0 / 5 | [轮1](../../results/task-performance-v1/cell-027.jsonl) · [轮2](../../results/task-performance-v1/cell-365.jsonl) · [轮3](../../results/task-performance-v1/cell-566.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.286–0.427 | 0.290 | 样本不足 | 0.427 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-001.jsonl) · [轮2](../../results/task-performance-v1/cell-388.jsonl) · [轮3](../../results/task-performance-v1/cell-588.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.998–1.350 | 1.173 | 样本不足 | 1.350 | 0 | 0 / 0 / 3 | [轮1](../../results/task-performance-v1/cell-016.jsonl) · [轮2](../../results/task-performance-v1/cell-236.jsonl) · [轮3](../../results/task-performance-v1/cell-543.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0224 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0384–0.0768 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0226 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0384–0.0768 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0226 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.0388–0.0777 | 0 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0138 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0214–0.0429 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0130 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0218–0.0436 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`case_complication:cmb:upstream_train_reserved_for_local_evaluation:172790`；语种：中文；来源组：`zh_exam_case:34036ad9d199c7abae3ebdb9`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "脓胸",
        "B": "支气管扩张",
        "C": "休克",
        "D": "DIC",
        "E": "中毒性脑病"
      },
      "instructions": "根据病例从原选项中选择最可能的并发症；不是主诊断任务。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "患儿，男，2岁。在因肺炎住院期间，突然出现自觉呼吸困难，全身中毒症状加重，频繁咳嗽，血压正常。此时考虑患儿出现的并发症是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `A`，对应选项：

```json
"脓胸"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "case_complication:cmb:upstream_train_reserved_for_local_evaluation:172790", "choice": "A"}
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
    "json_index": 172790,
    "zip_member": "CMB/CMB-Exam/CMB-train/CMB-train-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "upstream_train_reserved_for_local_evaluation",
  "upstream_group": "34036ad9d199c7abae3ebdb9",
  "upstream_id": "upstream_train_reserved_for_local_evaluation:172790",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 7 题、B 13 题、C 14 题、D 19 题、E 11 题、opa 5 题、opb 4 题、opc 9 题、opd 10 题、ope 8 题。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/case_complication/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/case_complication/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
