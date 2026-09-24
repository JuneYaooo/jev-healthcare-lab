# 患者入组预筛与临床试验匹配

**3 个任务条件，350 条主评测记录。** [全部场景](../../README.md)

NLI4CT 测证据材料上的判断与定位；TrialGPT 为直接三分类，不是完整检索排序和逐条纳排推理。

| 任务（点击查看完整方法与数据） | 任务类型 | 记录数 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [临床试验证据支持判断](nli4ct_entailment/README.md) | 文本蕴含判断 | 100 | Accuracy | 88.0% |
| [临床试验证据句定位](nli4ct_evidence/README.md) | 证据句筛选 | 100 | micro-F1 | 49.9% |
| [患者与临床试验入组预筛](trialgpt_sigir_referral/README.md) | 入组适配分类 | 150 | Accuracy | 48.0% |
