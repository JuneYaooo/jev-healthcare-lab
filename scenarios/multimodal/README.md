# 语音病历、医疗文档 OCR 与报告断言

**5 个任务条件，142 条主评测记录。** [实验归档](../README.md) · [业务任务总目录](../../docs/医疗任务总目录.md)

已归档 ASR／参考转写各 37 条字段判断，OCR／参考文本各 24 条文档分类，以及 20 条报告文本断言。早期病例与后续片段扩展分别说明；记录和来源分组数不等于独立患者数。医学影像和 ECG 原始输入尚未测。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [ASR 转写病史字段判断](primock_asr_fields/README.md) | 病史字段判断 | 37 | Accuracy | 91.9% | 89.2% |
| [参考转写病史字段判断](primock_reference_fields/README.md) | 病史字段判断 | 37 | Accuracy | 100.0% | 100.0% |
| [OCR 文本医疗文档类型识别](clinocr_ocr_doctype/README.md) | 文档类型分类 | 24 | Accuracy | 95.8% | 87.5% |
| [参考文本医疗文档类型识别](clinocr_reference_doctype/README.md) | 文档类型分类 | 24 | Accuracy | 95.8% | 95.8% |
| [边界挑战：影像报告断言](challenge_radiology_assertion/README.md) | 报告断言判断 | 20 | Accuracy | 100.0% | 100.0% |
