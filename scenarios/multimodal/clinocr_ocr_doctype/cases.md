# OCR 文本医疗文档类型识别：逐案例结果

20 个案例，共 24 条测试记录。案例口径：不同原始文档（同一文档的扫描变体合并）。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。

## 不同来源的表现

| 来源分组 | 案例 | 测试记录 | Jev | DeepSeek |
| --- | ---: | ---: | ---: | ---: |
| 原归档样本 | 16 | 20 | 95.0% | 85.0% |
| ClinOCR-Bench supplement | 4 | 4 | 100.0% | 100.0% |

## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| t1_s2 | Patient: John Smith DOB: 05/20/1965 MRN: 789012 Accession #: A583920-25 Sunrise Diagnostics Phone: Patient: Jo… | 4 | 100.0% | 100.0% |
| t9_s2 | a RS re ‘hywuoo esau aco ／ (ow wm Ap am 08 ／ sur er eoaliub ene ae ‘vee i hong _uset ／ (une masa von ／ ／ ma ye… | 2 | 50.0% | 50.0% |
| t2_s2 | Patient Name: Jane Doe MRN: 987654321 LAKEWOOD PATHOLOGY REPORT HOSPITAL 831676002937 Patient Name: Jane Doe P… | 1 | 100.0% | 100.0% |
| t3_s2 | Patient Name: Johnathan A. Smith MRN: 78912345 Gastroenterology Associates of North RIVERSIDE America 123 Heal… | 1 | 100.0% | 100.0% |
| t4_s2 | Date of Visit: 06/21/2025 Attending Provider: Dr. Emily Carter, MD Location: General Internal Medicine Clinic … | 1 | 100.0% | 100.0% |
| t5_s2 | Northwood Community Hospital 789 Pine Street, Northwood, CA 90210 Phone: (310) 555-0101 Patient: Michael Johns… | 1 | 100.0% | 100.0% |
| t6_s2 | PRECISION 831676002937 DIAGNOSTIC Patient Name: Maria Garcia Ordering Physician: Dr. Angela _ i Date of Birth:… | 1 | 100.0% | 100.0% |
| t7_s2 | HOSPITAL Oakwood Community Clinic 450 North Main Street Madison, WI 53703 (608) 555-0102 Patient Name: Isabell… | 1 | 100.0% | 100.0% |
| t8_s2 | HOSPITAL FAX To: Dr. David Chen, Gastroenterology Facility: Metropolitan Digestive Health Institute Fax: (555)… | 1 | 100.0% | 100.0% |
| t10_s2 | 831676002937 Patient: Maria C. Delgado LAKEWOOD DOB: 03/28/1972 ae im March 10, 2026 SECTION A: Medical Histor… | 1 | 100.0% | 0.0% |
| t11_s2 | Michael B. Torres DOB: 11/03/1958 Age: ／ Acct#: 44712-B PRECISION 67 Sex:M Physician: Dr. James R. DIAGNOSTIC … | 1 | 100.0% | 100.0% |
| t12_s2 | Michael B. Torres DOB: 11/03/1958 Acct#: 44712-B PRECISION DIAGNOSTIC Age: 67 Physician: Dr. James R. Sex: M A… | 1 | 100.0% | 100.0% |
| t13_s2 | C) GENERALHOSPITAL HOSPITAL Full Name: Maria C. Delgado Date of Birth (MM/DD/YYYY): 03/28/1972 Patient ID / MR… | 1 | 100.0% | 0.0% |
| t14_s2 | ® RIVERSIDE HOSPITAL Proposed Procedure: Right total knee arthroplasty Surgical Pre-Operative Assessment Surge… | 1 | 100.0% | 100.0% |
| t15_s2 | ／ 03/15/2026 ／ Blue Ridge Medical Center — Laboratory Services ／ ENTER TIME: 06:30 ORDER TIME: 06:15 SPEC#: S-… | 1 | 100.0% | 100.0% |
| t16_s2 | Date: 04/14/2026 Therapist Names: Mr. David Osei, DAILY REPORT RBT / Ms. Julia Park, BCBA Patient: Ethan C. Br… | 1 | 100.0% | 100.0% |
| t1_s3 | Patient: Maria Garcia DOB: 09/15/1992 MRN: 654321 Accession #: B987654-25 OrthoSport Imaging Center Patient: M… | 1 | 100.0% | 100.0% |
| t2_s3 | Patient Name: John Smith MRN: 7890123 LAKEWOOD PATHOLOGY REPORT HOSPITAL 831676002937 Date of Dirty: 05/20/196… | 1 | 100.0% | 100.0% |
| t3_s3 | Patient Name: Maria E. Gonzalez MRN: 98765432 Cityside Gastroenterology Clinic RIVERSIDE 4500 Metro Parkway Me… | 1 | 100.0% | 100.0% |
| t8_s3 | HOSPITAL FAX To: Dr. Samantha Powell, Dermatology Facility: Skin Health Specialists, LLC Fax: (555) 999-8888 P… | 1 | 100.0% | 100.0% |
