# 补液方案选择

[返回首页](../../README.md) · [主评测任务](README.md) · [辅助与暂停任务](AUXILIARY.md) · [数据集目录](../datasets/README.md)

**当前用途：临床主评测。** 方向适合，仅 16 题；作为治疗方案子类并标明探索性，不当作稳定独立榜单。

## 任务是什么

根据病例从原选项中选择补液量、溶液或补液方案。

| 项目 | 说明 |
| --- | --- |
| 任务 ID | `fluid_plan` |
| 医疗场景 | 治疗与用药 |
| 能力维度 | 规则与数值 |
| 评测类别 | 临床判断与行动 |
| 当前题数 / 目标题数 | 16 / 100 |
| 来源组数 | 15 |
| 语种 | 中文 16 题 |
| 数据范围 | 开放许可部分 16 题 |

## 数据集来源

| 数据集说明 | 收录题数 | 上游入口 |
| --- | --- | --- |
| [CMB-Exam（中文病例单选子集）](../datasets/cmb.md) | 9 | [原始来源](https://github.com/FreedomIntelligence/CMB) |
| [CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md) | 7 | [原始来源](https://doi.org/10.5281/zenodo.18951465) |

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
| JEV 1.13 | 50.00% | 16 / 16 | 0.980 | 0.954 | 1.222 | 2.169 | 0 / 0 / 0 | [配置](../../results/clinical-v1/jev-1.13.0/config.json) · [响应](../../results/clinical-v1/jev-1.13.0/responses.jsonl) · [评分](../../results/clinical-v1/jev-1.13.0/scores.json) |
| DeepSeek V4.1 Flash | **56.25%** | 14 / 16 | **0.589** | **0.558** | **0.871** | **1.485** | 0 / 0 / 2 | [配置](../../results/clinical-v1/deepseek-flash/config.json) · [响应](../../results/clinical-v1/deepseek-flash/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-flash/scores.json) |
| DeepSeek V4 Pro | 50.00% | 16 / 16 | 0.910 | 0.902 | 1.134 | 2.025 | 0 / 0 / 0 | [配置](../../results/clinical-v1/deepseek-v4-pro/config.json) · [响应](../../results/clinical-v1/deepseek-v4-pro/responses.jsonl) · [评分](../../results/clinical-v1/deepseek-v4-pro/scores.json) |
| Qwen3.5-9B | 18.75% | 16 / 16 | 2.595 | 0.797 | 5.153 | 5.736 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.5-9b/config.json) · [响应](../../results/clinical-v1/qwen3.5-9b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.5-9b/scores.json) |
| Qwen3.8-27B | 31.25% | 16 / 16 | 1.992 | 1.793 | 2.554 | 4.241 | 0 / 0 / 0 | [配置](../../results/clinical-v1/qwen3.8-27b/config.json) · [响应](../../results/clinical-v1/qwen3.8-27b/responses.jsonl) · [评分](../../results/clinical-v1/qwen3.8-27b/scores.json) |

## 多问题与并发性能

持续多题并发尚未测试。以下为历史有限批次结果，不作为高并发高吞吐证据。

### 历史有限批次测试

固定本任务 16 道原题，每种模式、每个模型各运行三轮；各模式使用完全相同的题目与金标。单题原始输入保持不变，多题把不同原题材料放入各自记录，并要求逐题独立判断。这是同任务多病例／多材料批量判断，不是同一患者新增多项临床判断。

取样结果用于性能与批量准确率比较，不替代上方全题量的临床成绩。包含非商业材料的任务继承原来源许可。JEV 与 Flash 使用各自原生接口，Flash 关闭思考并返回题号到选项键的精简 JSON；其他三模型尚未进行本轮性能测试。

表中整组耗时为三轮完成整组题目的墙钟均值，吞吐为三轮有效／正确决策总数除以三轮墙钟总和，包含失败拖尾。单请求题数为实际值；超过上下文预算会拆包，材料不截断。并发是同时请求数，不是单请求问题数。

历史多题结果（固定最大打包档，对比 Flash）：JEV 70.83%，Flash 41.67% ⚠；JEV 耗时少 37.8%；JEV 成本低 32.3%–66.2%。具体准确率与费用仅对应下述性能子集，不代表全量成绩或其他调用方式。

**小样本任务：** 重复运行只观察性能波动，不增加独立题目数，不能据此稳定估计临床准确率或尾延迟。

| 模式 | 并发 | 每请求实际题数 | 模型 | 准确率 | 整组平均秒 | 有效 / 正确决策每秒 | 完整包 / 请求 | 失败或无效请求 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 | 1 | 1 | JEV 1.13 | 56.25% | 14.507 | 1.10 / 0.62 | 48 / 48 | 0 |
| 逐题 | 1 | 1 | DeepSeek V4.1 Flash | 56.25% | 9.756 | 1.50 / 0.92 | 44 / 48 | 4 |
| 逐题 | 8 | 1 | JEV 1.13 | 56.25% | 0.693 | 23.09 / 12.99 | 48 / 48 | 0 |
| 逐题 | 8 | 1 | DeepSeek V4.1 Flash | 56.25% | 1.778 | 8.43 / 5.06 | 45 / 48 | 3 |
| 逐题 | 16 | 1 | JEV 1.13 | 54.17% | 0.499 | 32.05 / 17.36 | 48 / 48 | 0 |
| 逐题 | 16 | 1 | DeepSeek V4.1 Flash | 56.25% | 0.875 | 16.76 / 10.28 | 44 / 48 | 4 |
| 多题打包 | 1 | 8 | JEV 1.13 | 70.83% | 0.805 | 19.88 / 14.08 | 6 / 6 | 0 |
| 多题打包 | 1 | 8 | DeepSeek V4.1 Flash | 47.92% | 1.605 | 7.69 / 4.78 | 0 / 6 | 6 |
| 多题打包 | 1 | 16 | JEV 1.13 | 70.83% | 0.476 | 33.62 / 23.82 | 3 / 3 | 0 |
| 多题打包 | 1 | 16 | DeepSeek V4.1 Flash | 41.67% | 0.765 | 19.60 / 8.71 | 0 / 3 | 3 |

<details>
<summary>重复波动、请求耗时、失败与原始响应</summary>

| 模式 | 模型 | 整组秒范围 | 请求 P50 秒 | 请求 P95 秒 | 最长请求秒 | 429 | 请求失败 / 超时 / 无效 | 原始响应 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 4.196–34.593 | 0.257 | 0.316 | 30.866 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-137.jsonl) · [轮2](../../results/task-performance-v1/cell-355.jsonl) · [轮3](../../results/task-performance-v1/cell-515.jsonl) |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 8.889–10.498 | 0.556 | 0.882 | 1.135 | 0 | 0 / 0 / 4 | [轮1](../../results/task-performance-v1/cell-167.jsonl) · [轮2](../../results/task-performance-v1/cell-420.jsonl) · [轮3](../../results/task-performance-v1/cell-660.jsonl) |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.514–1.019 | 0.261 | 0.365 | 0.816 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-099.jsonl) · [轮2](../../results/task-performance-v1/cell-414.jsonl) · [轮3](../../results/task-performance-v1/cell-580.jsonl) |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 1.555–2.224 | 0.644 | 0.853 | 1.510 | 0 | 0 / 0 / 3 | [轮1](../../results/task-performance-v1/cell-161.jsonl) · [轮2](../../results/task-performance-v1/cell-430.jsonl) · [轮3](../../results/task-performance-v1/cell-531.jsonl) |
| 逐题 B≤1 / C16 | JEV 1.13 | 0.275–0.934 | 0.259 | 0.869 | 0.921 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-200.jsonl) · [轮2](../../results/task-performance-v1/cell-347.jsonl) · [轮3](../../results/task-performance-v1/cell-561.jsonl) |
| 逐题 B≤1 / C16 | DeepSeek V4.1 Flash | 0.821–0.954 | 0.686 | 0.845 | 0.953 | 0 | 0 / 0 / 4 | [轮1](../../results/task-performance-v1/cell-134.jsonl) · [轮2](../../results/task-performance-v1/cell-272.jsonl) · [轮3](../../results/task-performance-v1/cell-615.jsonl) |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.502–1.286 | 0.260 | 样本不足 | 0.992 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-083.jsonl) · [轮2](../../results/task-performance-v1/cell-351.jsonl) · [轮3](../../results/task-performance-v1/cell-694.jsonl) |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 1.396–1.748 | 0.812 | 样本不足 | 1.070 | 0 | 0 / 0 / 6 | [轮1](../../results/task-performance-v1/cell-072.jsonl) · [轮2](../../results/task-performance-v1/cell-292.jsonl) · [轮3](../../results/task-performance-v1/cell-508.jsonl) |
| 多题打包 B≤16 / C1 | JEV 1.13 | 0.264–0.895 | 0.269 | 样本不足 | 0.895 | 0 | 0 / 0 / 0 | [轮1](../../results/task-performance-v1/cell-028.jsonl) · [轮2](../../results/task-performance-v1/cell-438.jsonl) · [轮3](../../results/task-performance-v1/cell-567.jsonl) |
| 多题打包 B≤16 / C1 | DeepSeek V4.1 Flash | 0.742–0.809 | 0.745 | 样本不足 | 0.809 | 0 | 0 / 0 / 3 | [轮1](../../results/task-performance-v1/cell-173.jsonl) · [轮2](../../results/task-performance-v1/cell-434.jsonl) · [轮3](../../results/task-performance-v1/cell-648.jsonl) |

请求耗时包含完整接收与校验，不含客户端排队；整组耗时包含排队。少于 20 次请求不展示 P95。

</details>

<details>
<summary>每千次正确决策成本</summary>

| 模式 | 模型 | 估算 USD / 千次正确决策 | 缺用量请求 |
| --- | --- | --- | --- |
| 逐题 B≤1 / C1 | JEV 1.13 | 0.0395 | 0 |
| 逐题 B≤1 / C1 | DeepSeek V4.1 Flash | 0.0565–0.1130 | 0 |
| 逐题 B≤1 / C8 | JEV 1.13 | 0.0395 | 0 |
| 逐题 B≤1 / C8 | DeepSeek V4.1 Flash | 0.0565–0.1130 | 0 |
| 逐题 B≤1 / C16 | JEV 1.13 | 0.0410 | 0 |
| 逐题 B≤1 / C16 | DeepSeek V4.1 Flash | 0.0565–0.1129 | 0 |
| 多题打包 B≤8 / C1 | JEV 1.13 | 0.0201 | 0 |
| 多题打包 B≤8 / C1 | DeepSeek V4.1 Flash | 0.0353–0.0706 | 0 |
| 多题打包 B≤16 / C1 | JEV 1.13 | 0.0191 | 0 |
| 多题打包 B≤16 / C1 | DeepSeek V4.1 Flash | 0.0282–0.0564 | 0 |

按归档价目与实际 usage 估算；Flash 含缓存命中与输出费用，区间对应闲时至高峰价格。缺用量时不填完整单位成本，非账单费用。

</details>

连接池显式预热并跨单元复用，网络与供应商缓存仍会影响结果；各模式是有限批次测试，不能外推持续服务容量。[完整协议](../TASK_PERFORMANCE.md) · [冻结题目](../../benchmarks/task_performance_v1/README.md) · [运行配置](../../results/task-performance-v1/config.json)

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`fluid_plan:cmb:upstream_train_reserved_for_local_evaluation:235546`；语种：中文；来源组：`zh_exam_case:df3934d55654c33876d589dc`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "A": "4250ml",
        "B": "3750ml",
        "C": "5750ml",
        "D": "3250ml",
        "E": "6500ml"
      },
      "instructions": "根据病例从原选项中选择补液量、溶液或补液方案。",
      "type": "choice"
    }
  },
  "state": {
    "clinical_question": "男性，25岁，体重60kg，烫伤双上肢，躯干及双臀部，均为深Ⅱ°，右大腿为Ⅰ°，急诊入院，其第2个24小时补液总量应该是"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `A`，对应选项：

```json
"4250ml"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "fluid_plan:cmb:upstream_train_reserved_for_local_evaluation:235546", "choice": "A"}
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
    "json_index": 235546,
    "zip_member": "CMB/CMB-Exam/CMB-train/CMB-train-merge.json"
  },
  "material_kind": "medical_examination_vignettes",
  "resource": "cmb__CMB.zip",
  "resource_sha256": "c2e4288127fa5e6c03cc3659d893b0bbb19e699f74fdadce8e7fa10ac5bfdd94",
  "resource_url": "https://raw.githubusercontent.com/FreedomIntelligence/CMB/6c8ece46097dae736c6805dd3b831e1a38c08971/data/CMB.zip",
  "source_id": "cmb",
  "source_url": "https://github.com/FreedomIntelligence/CMB",
  "split": "upstream_train_reserved_for_local_evaluation",
  "upstream_group": "df3934d55654c33876d589dc",
  "upstream_id": "upstream_train_reserved_for_local_evaluation:235546",
  "version": "6c8ece46097dae736c6805dd3b831e1a38c08971"
}
```

## 覆盖与使用边界

题数是决策问题数，来源组可能是病例、文档、句子或指南条目，不应一律视为独立患者。答案沿用上游标注或机械映射，尚未经过本项目独立医生逐题审核。

当前标准标签分布：A 1 题、D 2 题、E 6 题、opa 2 题、opb 1 题、opc 1 题、opd 3 题。

当前可用题目不足目标数量，保留实际题量；比较细小差异时须同时报告样本数。

**[CMB-Exam（中文病例单选子集）](../datasets/cmb.md)**：中文医疗考试病例题；不是医院原始病历。只选病例决策单选题，排除 CMB-Clin 自由生成任务。 答案依据：固定 GitHub 测试题与公开更正版答案按 id 连接，并核对考试类别、科目和题型；完整保留原选项及答案。任务归属按公开规则筛选，不新增临床金标。 新任务另使用官方验证和训练文件；上游训练划分明确标记为本地评测保留子集，不冒称官方测试。

**[CNMLEQA-10k（中文案例分析子集）](../datasets/cnmleqa.md)**：中文执业医师考试整编病例题；上游有案例/知识题型标注，不是真实就诊结果。 答案依据：只选原 question_type=案例分析的记录；沿用 opa—ope 和 answer，保留每题 source、年份与原始 UUID；没有官方训练/测试划分，不冒称官方测试。 增加病例分期、病因、并发症、禁忌、护理和补液相关单选子集；沿用原答案，不把生成任务转换为自造金标。

## 数据文件

[本任务全部记录](../../benchmarks/medical_decision_v1/tasks/fluid_plan/samples.jsonl) · [任务定义与统计](../../benchmarks/medical_decision_v1/tasks/fluid_plan/task.json) · [格式与使用方法](../REPRODUCING.md)

[返回首页](../../README.md)
