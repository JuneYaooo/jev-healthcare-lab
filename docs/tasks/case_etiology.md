# 病例病因判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 根据病例在原候选中判断原因，属于临床推断；与文本 Causes 标注不同。

## 任务是什么

根据病例从原选项中选择导致所述疾病、症状或事件的最可能原因。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `case_etiology` |
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

合并任务后，本次所选许可范围内所有有题任务均计入所属范围的汇总分。少于 20 题标记为小样本，成绩可能波动较大；该标记不影响计分，辅助任务不计入临床主分数。

本轮各模型使用相同题目进行测试；完整计时与失败明细见 [模型对比](../MODEL_RESULTS.md)。

## 模型结果

以下成绩使用本页全部已收录题目；耗时包括请求、响应处理及重试等待。

有效回答表示返回合法选项，不代表正确；平均值和分位数包含已启动题目的失败耗时。任务总秒为含并发调度的墙钟时间，不是单题耗时之和。响应链接包含该模型全部题目，可按本页任务的题目 ID 查找。

加粗表示本任务的最高准确率或最短用时；按显示精度并列时同时加粗，全部相同则不标记。

| 模型 | 准确率 ↑ | 有效回答 / 题数 | 平均秒 ↓ | P50 秒 ↓ | P95 秒 ↓ | 任务总秒 ↓ | 超时 / 请求失败 / 无效回答 | 原始记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JEV 1.13 | **84.00%** | 100 / 100 | 3.744 | 3.054 | 7.832 | 52.541 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | **84.00%** | 100 / 100 | **0.478** | **0.475** | **0.698** | **6.236** | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | **84.00%** | 100 / 100 | 1.012 | 0.996 | 1.462 | 13.448 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 66.00% | 100 / 100 | 1.585 | 0.708 | 3.783 | 42.321 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 81.00% | 100 / 100 | 1.808 | 1.780 | 2.703 | 23.571 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

持续多题并发尚未测试。以下为历史有限批次结果，不作为高并发高吞吐证据。

### 历史有限批次测试

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

历史多题结果（固定最大打包档，对比 Flash）：JEV 73.96%，Flash 80.21% ⚠；JEV 耗时少 56.3%；取决于 Flash 闲时／高峰价格。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 78.12% | 9.212 | 3.47 / 2.71 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 78.12% | 20.631 | 1.55 / 1.21 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | JEV 1.13 | 77.08% | 4.383 | 7.22 / 5.63 | 95 / 96 | 1 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 82.29% | 2.768 | 11.56 / 9.51 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | JEV 1.13 | 78.12% | 0.353 | 90.77 / 70.91 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 84.38% | 1.026 | 31.19 / 26.32 | 96 / 96 | 0 |
| 多题打包 | 1 | 8 | JEV 1.13 | 73.96% | 1.585 | 20.19 / 14.93 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 71.88% | 3.474 | 8.64 / 6.62 | 7 / 12 | 5 |
| 多题打包 | 1 | 32 | JEV 1.13 | 73.96% | 0.595 | 53.80 / 39.79 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 80.21% | 1.360 | 23.28 / 18.87 | 2 / 3 | 1 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 7.884–10.367 | 0.270 | 0.451 | 0.902 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-229.jsonl) · [轮2](../../results/task-performance-v1/cell-270.jsonl) · [轮3](../../results/task-performance-v1/cell-483.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 19.641–22.275 | 0.635 | 0.883 | 1.422 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-107.jsonl) · [轮2](../../results/task-performance-v1/cell-354.jsonl) · [轮3](../../results/task-performance-v1/cell-581.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.082–10.034 | 0.259 | 1.081 | 10.031 | 0 | 0 / 1 / 0 | [轮1](../../results/task-performance-v1/cell-106.jsonl) · [轮2](../../results/task-performance-v1/cell-371.jsonl) · [轮3](../../results/task-performance-v1/cell-551.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.568–2.939 | 0.606 | 0.949 | 1.064 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-199.jsonl) · [轮2](../../results/task-performance-v1/cell-379.jsonl) · [轮3](../../results/task-performance-v1/cell-506.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.327–0.392 | 0.259 | 0.318 | 0.391 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-198.jsonl) · [轮2](../../results/task-performance-v1/cell-385.jsonl) · [轮3](../../results/task-performance-v1/cell-523.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.883–1.128 | 0.646 | 0.981 | 1.127 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-188.jsonl) · [轮2](../../results/task-performance-v1/cell-448.jsonl) · [轮3](../../results/task-performance-v1/cell-697.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.266–1.787 | 0.301 | 样本不足 | 0.873 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-148.jsonl) · [轮2](../../results/task-performance-v1/cell-252.jsonl) · [轮3](../../results/task-performance-v1/cell-641.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 3.143–3.639 | 0.800 | 样本不足 | 1.242 | 0 | 0 / 0 / 5 | [轮1](../../results/task-performance-v1/cell-232.jsonl) · [轮2](../../results/task-performance-v1/cell-343.jsonl) · [轮3](../../results/task-performance-v1/cell-546.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.294–1.081 | 0.409 | 样本不足 | 1.081 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-013.jsonl) · [轮2](../../results/task-performance-v1/cell-319.jsonl) · [轮3](../../results/task-performance-v1/cell-538.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 1.081–1.560 | 1.439 | 样本不足 | 1.560 | 0 | 0 / 0 / 1 | [轮1](../../results/task-performance-v1/cell-080.jsonl) · [轮2](../../results/task-performance-v1/cell-424.jsonl) · [轮3](../../results/task-performance-v1/cell-684.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0274 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0449–0.0898 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | — | 1 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0426–0.0853 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0274 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.0416–0.0832 | 0 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0180 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0200–0.0401 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0166 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0160–0.0320 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`case_etiology:cmb:upstream_train_reserved_for_local_evaluation:120835`；语种：中文；来源组：`zh_exam_case:92bde96d7d6dc028443287d6`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "食管胃底静脉曲张破裂",
        "B": "胃癌",
        "C": "消化性溃疡",
        "D": "反流性食管炎",
        "E": "食管憩室"
      },
      "instructions": "根据病例从原选项中选择导致所述疾病、症状或事件的最可能原因。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "女性，48岁，3年前确诊肝硬化，常有上腹隐痛，纳差。1日前突然呕吐棕褐色胃内容物一次，量约200ml。最可能的出血原因是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `C`，对应选项：

```json
"消化性溃疡"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "case_etiology:cmb:upstream_train_reserved_for_local_evaluation:120835", "choice": "C"}
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
    "json_index": 120835,
    "zip_member": "CMB/CMB-Exam/CMB-train/CMB-train-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "upstream_train_reserved_for_local_evaluation",
  "upstream_group": "92bde96d7d6dc028443287d6",
  "upstream_id": "upstream_train_reserved_for_local_evaluation:120835",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 10 题、B 10 题、C 10 题、D 10 题、E 10 题、opa 10 题、opb 10 题、opc 10 题、opd 10 题、ope 10 题。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/case_etiology/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/case_etiology/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
