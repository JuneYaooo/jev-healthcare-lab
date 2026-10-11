# LongHealth

[返回首页](../../README.md) · [全部数据集与参考来源](README.md) · [任务目录](../tasks/README.md)

## 这是什么数据

20 个虚构患者；100 道题不是 100 个患者。

| 项目 | 说明 |
| --- | --- |
| 来源 ID | `longhealth` |
| 上游入口 | [发布方页面](https://github.com/kbressem/LongHealth) |
| 收录情况 | 200 题 / 2 个任务 |
| 评测用途 | 辅助评测（不计临床主分数） 100 题、暂停使用（不导出、不评分） 100 题 |
| 使用范围 | 开放许可部分 |
| 登记的数据许可 | Apache-2.0 |
| 收录语种 | 英语 200 题 |

## 来源与引用

Bressem et al., LongHealth

[论文或项目引用](https://github.com/kbressem/LongHealth) · [数据许可](https://www.apache.org/licenses/LICENSE-2.0)

许可与说明快照：[longhealth__README.md](../../benchmarks/medical_decision_v1/sources/longhealth/longhealth__README.md) · [longhealth__LICENSE](../../benchmarks/medical_decision_v1/sources/longhealth/longhealth__LICENSE)

### 使用限制

信息充分性子集使用固定的两个异患者干扰文档和完整证据文档；不同于原始随机十次、token 截断协议。100 个问题共享 20 个虚构患者及干扰材料，应按患者分组，不能声称 100 个独立患者。

## 用于哪些任务

| 任务或来源子集 | 用途 | 此来源贡献题数 | 评测内容 |
| --- | --- | --- | --- |
| [目标患者回答证据是否出现（需重建）](../tasks/input_sufficiency.md) | 暂停使用（不导出、不评分） | 100 | 判断给定临床记录是否包含回答目标问题的证据；当前以 LongHealth 缺失证据协议覆盖记录信息充分性，不覆盖计算缺项或冲突消解。 |
| [长病历事实检索问答](../tasks/long_record_evidence.md) | 辅助评测（不计临床主分数） | 100 | 根据完整病例文书，在原始选项中选择有依据的答案。 |

## 答案与格式转换

沿用发布问题、五个选项和 correct 字段。 信息充分性来自同版本 task2.py 的 answer_docs 有/无协议，机械投影为 yes/no，不创作临床答案。

这里只采用可明确计分的判断任务。下方样例是本仓库适配后的评测记录，未将上游原格式冒充为统一请求格式；原始定位与资源链接随样例保留。尚未经过本项目独立医生逐题复核。

## 收录样例

以下为当前评测集中实际收录的一题，展示适配后的请求格式。为便于阅读，选取较短记录；样例不代表全任务的难度或类别分布，材料与选项未截断或改写。

题目 ID：`input_sufficiency:longhealth:patient_06:0:0`；语种：英语；来源组：`longhealth:patient_06`。

### 模型输入

只把以下 `request` 对象发送给模型。`state` 是输入材料，`questions.decision` 包含问题、选项和输出类型。

```json
{
  "questions": {
    "decision": {
      "criteria": {
        "no": "Required patient evidence is absent",
        "yes": "Evidence needed to answer is present"
      },
      "instructions": "判断给定临床记录是否包含回答目标问题的证据；当前以 LongHealth 缺失证据协议覆盖记录信息充分性，不覆盖计算缺项或冲突消解。",
      "type": "choice"
    }
  },
  "state": {
    "documents": [
      {
        "document": 1,
        "text": "**Dear colleague, **\n\nWe are reporting on our patient, John Havers, born on 05/29/1953, who\nreceived an MRI of the right proximal thigh for further clarification of\na potential tumor.\n\n**MRI of the right thigh, plain and with contrast agent, on\n02/19/2017:**\n\n[Technique]{.underline}: Surface coil, localization scan, coronal T1 SE,\ntransverse, coronal, sagittal T2 TSE with fat suppression. After\nintravenous contrast administration, T1-TSE transverse and T1-TSE FS\n(coronal, T2 TSE FS coronal as an additional fat-saturated sequence in\nthe same section level for exploring relevant edema).\n\n[Findings]{.underline}: Normal bone marrow signal consistent with age.\nNo signs of fractures. Coexistence of moderate degenerative changes in\nthe hip joints, more pronounced on the right than on the left. Mild\nactivation of the muscles in the left proximal adductor region. Ventral\nto the gracilis muscle and dorsal to the sartorius muscle at the level\nof the middle third of the right thigh is a subfascial intermuscular\noval mass lesion with a high-signal appearance on T2-weighted images and\na low-signal appearance on T1-weighted images. It is partially septated,\nwell-demarcated, and shows strong contrast enhancement. No evidence of\nblood degradation products. Dimensions are 35 x 45 x 40 mm. No evidence\nof suspiciously enlarged lymph nodes. Other assessed soft tissues are\nunremarkable for the patient\\'s age.\n\n[Assessment]{.underline}: Overall, a high suspicion of a mucinous mass\nlesion in the region of the right adductor compartment. Differential\nDiagnosis: Mucinous liposarcoma. Further histological evaluation is\nstrongly recommended.\n\n**Current Recommendations:** Presentation at the clinic for surgery for\nfurther differential diagnostic clarification.\n\n"
      },
      {
        "document": 2,
        "text": "**Dear colleague, **\n\n\nWe are writing to report on the outpatient treatment of Mrs. Laura\nMiller, born on 04/03/1967, on 05/22/2020.\n\n**Diagnosis**: Osteoporotic vertebral body sintering (lumbar vertebra 2\nand thoracic vertebra 8).\n\n**Medical History**: Mrs. Miller presents with pain in her back, legs\nradiating, after fall on the back 6 weeks ago. The complaints were\nprogressive with intermittent paresthesia in both legs.\n\n**Other Diagnoses** (not fully collectible):\n\n-   Status post apoplexy\n\n**Current Medication (**not ascertainable):\n\n-   Blood pressure medication\n\n-   Osteoporosis medication\n\n-   No anticoagulation.\n\n**Physical Examination: Lumbar spine:** Skin without pathological\nfindings. No redness, no evidence of infection.\n\nTapping pain over thoracic spine/lumbar spine, no compression pain, no\ntorsion pain, no pressure pain over spinous process.\n\nRadiation of pain into the right and left leg, paravertebral muscle\nhardness.\n\nNo paresthesias in the genital area, no breech anesthesia, no peripheral\nneurologic deficits, No bladder or rectal dysfunction.\n\nPeripheral Circulation/Motor function/Sensitivity intact.\n\nStrength grade on all sides: Hip Flex/Ex: 5/5, Knee Flex/Ex: 5/5,\n\nFoot extensor muscles of the lower leg/flexor muscles of the lower leg:\n3/5.\n\nBig toe extensor muscles of the lower leg/big toe flexor muscles of the\nlower leg: 2/5.\n\n**Thoracic Spine 2 levels from 05/22/2020, Lumbar spine in 2 planes from\n05/22/2020:**\n\nClinical indication: Status post fall\n\nQuestion: new fracture?\n\nPreliminary images: none comparable\n\n**Findings**\n\n1\\) [Thoracic Spine]{.underline}: Multiple thoracic vertebral bodies\nexhibit decreased height, most notably at the central region where a\nmeasurement of approximately 17 mm suggests significant height loss and\npotential acute fracture. Additionally, there are endplate impressions\nin individual vertebrae of the lower thoracic spine. Aortic sclerosis is\npresent, along with degenerative changes throughout the thoracic\nvertebrae. The osseous structure presents osteoporotic features. A\nsuspected hemangioma is identified in a vertebral body of the lower\nthoracic spine.\n\n2\\) [Lumbar Spine]{.underline}: In a presumed five-segment lumbar spine,\nthe L1 vertebra shows a subtle reduction in height with a questionable\nendplate impression. Osteoporotic features are evident in the bony\nstructure.\n\n**Assessment:** Multiple fractures are evident in both thoracic\nvertebrae and the first lumbar vertebra, some of which may be acute. MRI\nis recommended for further evaluation. Osseous structure displays\npronounced osteoporotic features.\n\nGrade III esophageal varices present without definitive high-risk\nstigmata. Varices also noted at the gastroesophageal junction,\nclassified as GOV 1 according to Sarin\\'s classification. Band ligation\nof the varices is not performed, as no unambiguous source of bleeding is\nidentifiable and a significant portion of the stomach remains outside\nthe field of view.\n\n**Recommendation**: Terlipressin, monitor surveillance, Erythromycin\n\n**Computed Tomography Thoracic spine from 05/22/2020:**\n\nFracture at the base plate of lumbar vertebra 2 with involvement of the\nposterior margin. Left lateral, no significant reduction in height of\nthe vertebral body. No tension of the spine.\n\nSuspicion of new small fracture also at the cover plate at thoracic\nvertebra 8.\n\nMultiple, older, osteoporotic compression fractures at the thoracic\nspine and\n\nupper lumbar spine.\n\n**Additional Finding:**\n\nLiver cirrhosis with multiple nodules, low ascites, and portal vein\ncongestion. Splenomegaly. If not already known, further workup of liver\nlesions is recommended. Hydrops of the gallbladder.\n\n**Current Recommendations**: There is a general indication for admission\nof the patient and further diagnostics before surgical treatment of the\nfractures. Mrs. Miller is generally opposed to surgical care. She was\nthoroughly informed about the risks (progression, cross-section, death).\n\nRe-presentation with current bone densitometry and update of\nosteoporosis medication, as well as current holospinal MRI. In the\nmeantime, analgesia as needed using Acetaminophen 500mg 1-1-1 under\ngastric protection.\n\n**Esophagogastroduodenoscopy from 05/22/2020:**\n\n[Esophagus]{.underline}: Unobstructed intubation of the esophageal\nopening was achieved under direct visualization. In the upper third of\nthe esophagus, multiple prominent varices protrude into the lumen,\nunaltered by air insufflation. In the middle third, there are areas with\nwhitish overlying material that do not resemble the typical white nipple\nsign. Despite meticulous inspection, no active bleeding sites were\nidentified. The Z-line reveals isolated minor erosions. Cardiac\nsphincter closure is complete.\n\n[Stomach]{.underline}: Full distension of the gastric lumen was\naccomplished with air insufflation. The major curvature of the stomach\ncontained food mixed with hematin. The mucosal surface was similarly\ncoated with hematin, but no active bleeding was discernible in the\nvisualized areas. Peristaltic movement was widespread. Upon\nretroflexion, pronounced varices were noted near the cardiac region on\nthe lesser curvature. The pylorus was unremarkable and easily\ntraversable.\n\n[Duodenum]{.underline}: Adequate distension of the duodenal bulb was\nachieved, providing a clear view up to the descending part of the\nduodenum. Overall, the mucosa appeared normal with minor remnants of\nhematin, and no source of bleeding was identified.\n\n"
      }
    ],
    "question": "The carcinoma is located in which area of the tongue?",
    "target_patient": "Paul Doe"
  }
}
```

### 标准答案与预测格式

原始标注映射后的正确选项键为 `no`，对应选项：

```json
"Required patient evidence is absent"
```

评分用预测文件每行包含题目 ID 与模型选择的选项键。下面使用标准答案演示文件格式，不是模型运行结果：

```json
{"id": "input_sufficiency:longhealth:patient_06:0:0", "choice": "no"}
```

### 样例溯源

[上游资源](https://raw.githubusercontent.com/kbressem/LongHealth/479922279ce8fa528fe2cd87d854c6a2f8365d21/data/benchmark_v5.json) · [数据集说明](../datasets/longhealth.md)

以下信息用于追溯材料、划分和答案来源，不作为模型输入。`locator` 是原文件中的定位信息：

```json
{
  "data_license": "Apache-2.0",
  "distribution": "open",
  "gold_origin": "upstream_annotation",
  "independent_clinical_review": false,
  "locator": {
    "answer_location_keys": [
      "text_5"
    ],
    "display_document_keys": [
      "patient_14/text_0",
      "patient_08/text_0"
    ],
    "evidence_included": false,
    "patient_key": "patient_06",
    "question_No": 0,
    "supporting_resources": [
      "longhealth__task2.py"
    ]
  },
  "material_kind": "fictional_longitudinal_records",
  "resource": "longhealth__data_benchmark_v5.json",
  "resource_sha256": "82d34d9da47ab279d7aa89a6bdf298c0ac79f1e506e1dd0a3ea69a1ad5e2cb45",
  "resource_url": "https://raw.githubusercontent.com/kbressem/LongHealth/479922279ce8fa528fe2cd87d854c6a2f8365d21/data/benchmark_v5.json",
  "source_id": "longhealth",
  "source_url": "https://github.com/kbressem/LongHealth",
  "split": "published_benchmark_controlled_evidence_ablation",
  "upstream_group": "patient_06",
  "upstream_id": "patient_06:0:0",
  "version": "479922279ce8fa528fe2cd87d854c6a2f8365d21"
}
```

更多样例、数据文件和任务边界见上方各任务说明页。样例所属任务：[目标患者回答证据是否出现（需重建）](../tasks/input_sufficiency.md)。

## 追溯与使用

来源元数据保存在 [来源登记文件](../../benchmarks/medical_decision_v1/sources.json)，已收录题目的原始文件版本与哈希见 [资源锁定文件](../../benchmarks/medical_decision_v1/sources.lock.json)。原始数据各自的许可独立适用。

[返回首页](../../README.md)
