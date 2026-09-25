# 语音病历、医疗文档 OCR 与报告断言

**5 个任务条件，142 条主评测记录。** [全部场景](../../README.md)

语音字段测试来自 3 个扮演患者病例，OCR 类型测试来自 20 张扫描图、16 个模板。影像和 ECG 尚未运行。

| 任务（点击查看方法与费用） | 任务类型 | 记录数 | 指标 | Jev | DeepSeek |
| --- | --- | ---: | --- | ---: | ---: |
| [ASR 转写病史字段判断](primock_asr_fields/README.md) | 病史字段判断 | 37 | Accuracy | 91.9% | 89.2% |
| [参考转写病史字段判断](primock_reference_fields/README.md) | 病史字段判断 | 37 | Accuracy | 100.0% | 100.0% |
| [OCR 文本医疗文档类型识别](clinocr_ocr_doctype/README.md) | 文档类型分类 | 24 | Accuracy | 95.8% | 87.5% |
| [参考文本医疗文档类型识别](clinocr_reference_doctype/README.md) | 文档类型分类 | 24 | Accuracy | 95.8% | 95.8% |
| [边界挑战：影像报告断言](challenge_radiology_assertion/README.md) | 报告断言判断 | 20 | Accuracy | 100.0% | 100.0% |
