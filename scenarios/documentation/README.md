# 病历章节、文书质控与随访记录

**5 个任务条件，212 条主评测记录。** [全部场景](../../README.md)

已测章节分类；尚未验证从医患对话生成完整病历或真实交接班质量。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [问诊对话对应病历章节](mts_section_classification/README.md) | 章节分类 | 100 | Accuracy | 76.0% | 73.0% |
| [已分段病历章节分类](aci_note_section/README.md) | 章节分类 | 100 | Accuracy | 99.0% | 100.0% |
| [边界挑战：文档类型](challenge_document_type/README.md) | 文档类型分类 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：文书缺项](challenge_documentation/README.md) | 文书缺项判断 | 4 | Accuracy | 100.0% | 100.0% |
| [边界挑战：随访行动](challenge_followup_action/README.md) | 行动项识别 | 4 | Accuracy | 100.0% | 100.0% |
