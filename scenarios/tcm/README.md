# 中医知识、辨证与安全

**14 个任务条件，800 条主评测记录。** [全部场景](../../README.md)

单选 Accuracy 与多选 micro-F1 分列；TCM-BEST 安全项为标签一致率，部分标签存在过度拒绝倾向。

| 任务（点击查看完整方法与数据） | 任务类型 | 记录数 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [中医病历证型分类](tcm_syndrome/README.md) | 证型分类 | 100 | Accuracy | 33.0% |
| [医学伦理单选](tcm_best_ethics/README.md) | 单选问答 | 97 | Accuracy | 89.7% |
| [医学伦理多选](tcm_best_ethics_multi/README.md) | 多选问答 | 3 | micro-F1 | 81.8% |
| [中医基础知识单选](tcm_best_knowledge/README.md) | 单选问答 | 89 | Accuracy | 91.0% |
| [中医基础知识多选](tcm_best_knowledge_multi/README.md) | 多选问答 | 11 | micro-F1 | 79.3% |
| [中医病位单选](tcm_best_location/README.md) | 单选问答 | 21 | Accuracy | 81.0% |
| [中医病位多选](tcm_best_location_multi/README.md) | 多选问答 | 79 | micro-F1 | 64.8% |
| [中医病性单选](tcm_best_nature/README.md) | 单选问答 | 99 | Accuracy | 69.7% |
| [中医病性多选](tcm_best_nature_multi/README.md) | 多选问答 | 1 | micro-F1 | 80.0% |
| [中医治则治法单选](tcm_best_principles/README.md) | 单选问答 | 3 | Accuracy | 100.0% |
| [中医治则治法多选](tcm_best_principles_multi/README.md) | 多选问答 | 97 | micro-F1 | 70.3% |
| [中医证型单选](tcm_best_syndrome/README.md) | 单选问答 | 68 | Accuracy | 80.9% |
| [中医证型多选](tcm_best_syndrome_multi/README.md) | 多选问答 | 32 | micro-F1 | 52.8% |
| [中医安全问题标签一致性](tcm_best_安全问题/README.md) | 安全标签分类 | 100 | Accuracy | 27.0% |
