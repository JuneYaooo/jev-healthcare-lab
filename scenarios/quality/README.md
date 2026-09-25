# 医疗质控、幻觉识别与请求安全

**11 个任务条件，1,157 条主评测记录。** [全部场景](../../README.md)

错误检出、错误定位、回答幻觉和请求安全是不同任务；MedSafety 的正常／有害来源存在混杂。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [医疗叙述错误检出](medec_error_detection/README.md) | 错误检出 | 100 | Accuracy | 65.0% | 60.0% |
| [医疗叙述错误定位](medec_error_localization/README.md) | 错误定位 | 100 | Accuracy | 72.0% | 70.0% |
| [阿拉伯文医疗文本错误检出](mederrbench_ARA/README.md) | 错误检出 | 97 | Accuracy | 69.1% | 59.8% |
| [中文医疗文本错误检出](mederrbench_CN/README.md) | 错误检出 | 100 | Accuracy | 73.0% | 74.0% |
| [英文医疗文本错误检出](mederrbench_EN/README.md) | 错误检出 | 100 | Accuracy | 81.0% | 79.0% |
| [医学回答幻觉识别：有证据](medhallu_with_evidence/README.md) | 幻觉识别 | 200 | Accuracy | 82.0% | 82.5% |
| [医学回答幻觉识别：无证据](medhallu_without_evidence/README.md) | 幻觉识别 | 200 | Accuracy | 60.0% | 69.5% |
| [医疗有害请求筛查](medsafety_request_gate/README.md) | 请求安全分类 | 200 | Accuracy | 93.5% | 96.0% |
| [边界挑战：病历矛盾](challenge_contradiction/README.md) | 矛盾检测 | 20 | Accuracy | 100.0% | 95.0% |
| [边界挑战：隐私信息候选](challenge_phi_candidate/README.md) | 隐私信息识别 | 20 | Accuracy | 95.0% | 95.0% |
| [边界挑战：提示注入](challenge_prompt_injection/README.md) | 提示注入抵抗 | 20 | Accuracy | 100.0% | 100.0% |
