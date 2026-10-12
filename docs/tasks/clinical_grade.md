# 疾病分期与严重程度判断

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 根据病例作出临床分级，方向适合主评测；不同分期体系应分层，考试金标不证明现行临床有效性。

## 任务是什么

根据病例从原选项中选择疾病分期、严重程度分度或功能分级。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `clinical_grade` |
| 医疗场景 | 诊断与鉴别 |
| 能力维度 | 规则与数值 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 100 / 100 |
| 来源组数 | 99 |
| 语种 | 中文 100 题 |
| 数据范围 | 开放许可部分 100 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 70 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 30 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

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
| JEV 1.13 | **62.00%** | 100 / 100 | 1.336 | 0.972 | 3.372 | 17.204 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | 50.00% | 95 / 100 | **0.470** | **0.455** | **0.708** | **6.229** | 0 / 0 / 5 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 53.00% | 100 / 100 | 0.949 | 0.940 | 1.271 | 12.427 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 34.00% | 97 / 100 | 1.469 | 0.807 | 4.640 | 20.693 | 0 / 0 / 3 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 43.00% | 100 / 100 | 2.685 | 2.488 | 5.411 | 40.294 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

本轮多题结果（固定最大打包档，对比 Flash）：JEV 60.42%，Flash 34.38%；JEV 耗时少 56.0%；JEV 成本低 47.4%–73.7%。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

固定本任务 32 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 65.62% | 8.865 | 3.61 / 2.37 | 96 / 96 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 46.88% | 20.762 | 1.40 / 0.72 | 87 / 96 | 9 |
| 逐题 | 8 | 1 | JEV 1.13 | 65.62% | 1.313 | 24.38 / 16.00 | 96 / 96 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 46.88% | 2.880 | 10.19 / 5.21 | 88 / 96 | 8 |
| 逐题 | 32 | 1 | JEV 1.13 | 65.62% | 1.157 | 27.65 / 18.15 | 96 / 96 | 0 |
| 逐题 | 32 | 1 | DeepSeek V4.1 Flash | 46.88% | 1.095 | 26.18 / 13.70 | 86 / 96 | 10 |
| 多题打包 | 1 | 8 | JEV 1.13 | 61.46% | 1.522 | 21.03 / 12.92 | 12 / 12 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 48.96% | 3.446 | 9.00 / 4.55 | 9 / 12 | 3 |
| 多题打包 | 1 | 32 | JEV 1.13 | 60.42% | 0.551 | 58.11 / 35.11 | 3 / 3 | 0 |
| 多题打包 | 1 | 32 | DeepSeek V4.1 Flash | 34.38% | 1.252 | 25.57 / 8.79 | 3 / 3 | 0 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 8.139–9.945 | 0.259 | 0.324 | 1.262 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-181.jsonl) · [轮2](../../results/task-performance-v1/cell-291.jsonl) · [轮3](../../results/task-performance-v1/cell-569.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 19.528–22.520 | 0.629 | 1.031 | 1.169 | 0 | 0 / 0 / 9 | [轮1](../../results/task-performance-v1/cell-154.jsonl) · [轮2](../../results/task-performance-v1/cell-243.jsonl) · [轮3](../../results/task-performance-v1/cell-603.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 1.188–1.480 | 0.286 | 0.336 | 0.723 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-114.jsonl) · [轮2](../../results/task-performance-v1/cell-273.jsonl) · [轮3](../../results/task-performance-v1/cell-659.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 2.737–3.124 | 0.661 | 0.913 | 1.440 | 0 | 0 / 0 / 8 | [轮1](../../results/task-performance-v1/cell-127.jsonl) · [轮2](../../results/task-performance-v1/cell-297.jsonl) · [轮3](../../results/task-performance-v1/cell-496.jsonl) |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.902–1.640 | 0.772 | 0.896 | 1.640 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-067.jsonl) · [轮2](../../results/task-performance-v1/cell-405.jsonl) · [轮3](../../results/task-performance-v1/cell-691.jsonl) |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.874–1.243 | 0.677 | 1.030 | 1.234 | 0 | 0 / 0 / 10 | [轮1](../../results/task-performance-v1/cell-035.jsonl) · [轮2](../../results/task-performance-v1/cell-324.jsonl) · [轮3](../../results/task-performance-v1/cell-639.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 1.329–1.785 | 0.375 | 样本不足 | 0.754 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-103.jsonl) · [轮2](../../results/task-performance-v1/cell-454.jsonl) · [轮3](../../results/task-performance-v1/cell-625.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 3.216–3.850 | 0.849 | 样本不足 | 1.143 | 0 | 0 / 0 / 3 | [轮1](../../results/task-performance-v1/cell-110.jsonl) · [轮2](../../results/task-performance-v1/cell-396.jsonl) · [轮3](../../results/task-performance-v1/cell-514.jsonl) |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.319–0.909 | 0.424 | 样本不足 | 0.909 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-017.jsonl) · [轮2](../../results/task-performance-v1/cell-290.jsonl) · [轮3](../../results/task-performance-v1/cell-677.jsonl) |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.925–1.487 | 1.343 | 样本不足 | 1.487 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-071.jsonl) · [轮2](../../results/task-performance-v1/cell-444.jsonl) · [轮3](../../results/task-performance-v1/cell-703.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0319 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0770–0.1540 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0319 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0770–0.1540 | 0 |
| 逐题 B≤1 / C32 | JEV 1.13 | 0.0319 | 0 |
| 逐题 B≤1 / C32 | DeepSeek V4.1 Flash | 0.0770–0.1541 | 0 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0211 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0250–0.0500 | 0 |
| 多题打包 B≤32 / C1 | JEV 1.13 | 0.0197 | 0 |
| 多题打包 B≤32 / C1 | DeepSeek V4.1 Flash | 0.0374–0.0749 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`clinical_grade:cmb:official_test:850`；语种：中文；来源组：`zh_exam_case:5f0dac8dcc1b92625d5bc576`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "Ⅰ期",
        "B": "Ⅱa",
        "C": "Ⅱb",
        "D": "Ⅲa",
        "E": "Ⅲb"
      },
      "instructions": "根据病例从原选项中选择疾病分期、严重程度分度或功能分级。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "患者23岁，停经3个月，阴道流血2周，查子宫大小超过妊周，阴道可见2cm×2cm紫蓝结节，宫旁无异常，侵葡的分期为（ ）。"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `C`，对应选项：

```json
"Ⅱb"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "clinical_grade:cmb:official_test:850", "choice": "C"}
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
    "answer_json_index": 850,
    "json_index": 850,
    "question_id": 851,
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
  "upstream_group": "5f0dac8dcc1b92625d5bc576",
  "upstream_id": "official_test:850",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 5 题、B 11 题、C 23 题、D 23 题、E 8 题、opa 5 题、opb 6 题、opc 5 题、opd 9 题、ope 5 题。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 调研过的其他来源

这些来源尚未为本任务提供题目；不能据此计入覆盖数量或视为已授权分发。

| 来源说明 | 登记情况 |
| --- | --- |
| [CMedCalc-Bench](../datasets/cmedcalc.md) | 公开仓库未见明确数据许可；原文与合成混合 |

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/clinical_grade/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/clinical_grade/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
