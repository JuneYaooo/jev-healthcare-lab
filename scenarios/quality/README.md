# 医疗质控、幻觉识别与请求安全

**11 个任务条件，1,109 条主评测记录。** [全部场景](../../README.md)

错误检出、错误定位、回答幻觉和请求安全是不同任务；MedSafety 的正常／有害来源存在混杂。

| 任务（点击查看完整方法与数据） | 类型 | 记录数 | 指标 | 结果 |
| --- | --- | ---: | --- | ---: |
| [医疗叙述错误检出](medec_error_detection/README.md) | 数据适配 | 100 | Accuracy | 65.0% |
| [医疗叙述错误定位](medec_error_localization/README.md) | 数据适配 | 100 | Accuracy | 72.0% |
| [阿拉伯文医疗文本错误检出](mederrbench_ARA/README.md) | 数据适配 | 97 | Accuracy | 69.1% |
| [中文医疗文本错误检出](mederrbench_CN/README.md) | 数据适配 | 100 | Accuracy | 73.0% |
| [英文医疗文本错误检出](mederrbench_EN/README.md) | 数据适配 | 100 | Accuracy | 81.0% |
| [医学回答幻觉识别：有证据](medhallu_with_evidence/README.md) | 数据适配 | 200 | Accuracy | 82.0% |
| [医学回答幻觉识别：无证据](medhallu_without_evidence/README.md) | 数据适配 | 200 | Accuracy | 60.0% |
| [医疗有害请求筛查](medsafety_request_gate/README.md) | 数据适配 | 200 | Accuracy | 93.5% |
| [边界挑战：病历矛盾](challenge_contradiction/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
| [边界挑战：隐私信息候选](challenge_phi_candidate/README.md) | 自编挑战 | 4 | Accuracy | 75.0% |
| [边界挑战：提示注入](challenge_prompt_injection/README.md) | 自编挑战 | 4 | Accuracy | 100.0% |
