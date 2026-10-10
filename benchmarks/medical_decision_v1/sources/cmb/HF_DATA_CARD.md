---
license: apache-2.0
task_categories:
- question-answering
- text-generation
language:
- zh
tags:
- medical
- biology
- chemistry
size_categories:
- 100K<n<1M
configs:
  - config_name: CMB-Clin
    data_files:
      - split: test
        path: CMB-Clin/CMB-Clin-qa.json
  - config_name: CMB-Exam
    data_files:
      - split: test
        path: CMB-Exam/CMB-test/CMB-test-choice-question-merge.json
      - split: train
        path: CMB-Exam/CMB-train/CMB-train-merge.json
      - split: val
        path: CMB-Exam/CMB-val/CMB-val-merge.json
---

# CMB: A Comprehensive  Medical Benchmark in Chinese
![CMB](assets/title.png)
<p align="center">
   🌐 <a href="https://github.com/FreedomIntelligence/CMB" target="_blank">Github</a> • 🌐 <a href="https://cmedbenchmark.llmzoo.com/#home" target="_blank">Website</a> • 🤗 <a href="https://huggingface.co/datasets/FreedomIntelligence/CMB" target="_blank">HuggingFace</a>

## 🌈 Update
* **[2024.02.21]** The [answers](https://github.com/FreedomIntelligence/CMB/tree/main/data) to the CMB-Exam test has been updated and some errors caused by omissions in version management have been fixed.
* **[2024.01.08]** In order to facilitate testing, we disclose the [answers](https://github.com/FreedomIntelligence/CMB/tree/main/data) to the CMB-Exam test
* **[2023.09.22]** CMB is included in [OpenCompass](https://github.com/open-compass/opencompass).
* **[2023.08.21]** [Paper](https://arxiv.org/abs/2308.08833) released.
* **[2023.08.01]** 🎉🎉🎉 CMB is published！🎉🎉🎉


## 🌐 Download Data

- (Recommended) Download the [zip file](https://github.com/FreedomIntelligence/CMB/tree/main/data) and unzip:
    ```bash
    git clone "https://github.com/FreedomIntelligence/CMB.git" && cd CMB && unzip "./data/CMB.zip" -d "./data/" && rm "./data/CMB.zip"
    ```
- Or  load our data as follows:
    ```python
    from datasets import load_dataset
    # CMB-Exam datasets （multiple-choice and multiple-answer questions）
    exam_datasets = load_dataset('FreedomIntelligence/CMB','exam')
    # CMB-Clin datasets
    clin_datasets = load_dataset('FreedomIntelligence/CMB','clin')
    ```

  

## 🥇 Leaderboard 

Please Check [Leaderboard](https://cmedbenchmark.llmzoo.com/static/leaderboard.html).



## 🥸 Dataset intro
![CMB](assets/CMB-2.svg)
### Components

- CMB-Exam: Comprehensive multi-level assessment for medical knowledge
   - Structure: 6 major categories and 28 subcategories, [View Catalog](catalog.md)
   - CMB-test: 400 questions per subcategories, 11200 questions in total
   - CMB-val: 280 questions with solutions and explanations; used as source for CoT and few-shot
   - CMB-train: 269359 questions for medical knowledge injection
    
- CMB-Clin: 74 cases of complex medical inquires 


### CMB-Exam Item 
```json
{
    "exam_type": "医师考试",
    "exam_class": "执业医师",
    "exam_subject": "口腔执业医师",
    "question": "患者，男性，11岁。近2个月来时有低热（37～38℃），全身无明显症状。查体无明显阳性体征。X线检查发现右肺中部有一直径约0.8cm类圆形病灶，边缘稍模糊，肺门淋巴结肿大。此男孩可能患",
    "answer": "D",
    "question_type": "单项选择题",
    "option": {
        "A": "小叶型肺炎",
        "B": "浸润性肺结核",
        "C": "继发性肺结核",
        "D": "原发性肺结核",
        "E": "粟粒型肺结核"
    }
},
```
- exam_type: major category
- exam_class: sub-category
- exam_subject: Specific departments or subdivisions of disciplines 
- question_type: *multiple-choice (单项选择题)* or *multiple-answer (多项选择题)*


### CMB-Clin Item 
```json
{
    "id": 0,
    "title": "案例分析-腹外疝",
    "description": "现病史\n（1）病史摘要\n     病人，男，49岁，3小时前解大便后出现右下腹疼痛，右下腹可触及一包块，既往体健。\n（2）主诉\n     右下腹痛并自扪及包块3小时。\n\n体格检查\n体温： T 37.8℃，P 101次／分，呼吸22次/分，BP 100/60mmHg，腹软，未见胃肠型蠕动波，肝脾肋下未及，于右侧腹股沟区可扪及一圆形肿块，约4cm×4cm大小，有压痛、界欠清，且肿块位于腹股沟韧带上内方。\n\n辅助检查\n（1）实验室检查\n     血常规：WBC 5.0×109／L，N 78％。\n     尿常规正常。\n（2）多普勒超声检查\n     沿腹股沟纵切可见一多层分布的混合回声区，宽窄不等，远端膨大，边界整齐，长约4～5cm。\n（3）腹部X线检查\n     可见阶梯状液气平。",
    "QA_pairs": [
        {
            "question": "简述该病人的诊断及诊断依据。",
            "solution": "诊断：嵌顿性腹股沟斜疝合并肠梗阻。\n诊断依据：\n①右下腹痛并自扪及包块3小时；\n②有腹胀、呕吐，类似肠梗阻表现；腹部平片可见阶梯状液平，考虑肠梗阻可能；腹部B超考虑，\n腹部包块内可能为肠管可能；\n③有轻度毒性反应或是中毒反应，如 T 37.8℃，P 101次／分，白细胞中性分类78％；\n④腹股沟区包块位于腹股沟韧带上内方。"
        },
        {
            "question": "简述该病人的鉴别诊断。",
            "solution": "（1）睾丸鞘膜积液：鞘膜积液所呈现的肿块完全局限在阴囊内，其上界可以清楚地摸到；用透光试验检查肿块，鞘膜积液多为透光（阳性），而疝块则不能透光。\n（2）交通性鞘膜积液：肿块的外形与睾丸鞘膜积液相似。于每日起床后或站立活动时肿块缓慢地出现并增大。平卧或睡觉后肿块逐渐缩小，挤压肿块，其体积也可逐渐缩小。透光试验为阳性。\n（3）精索鞘膜积液：肿块较小，在腹股沟管内，牵拉同侧睾丸可见肿块移动。\n（4）隐睾：腹股沟管内下降不全的睾丸可被误诊为斜疝或精索鞘膜积液。隐睾肿块较小，挤压时可出现特有的胀痛感觉。如患侧阴囊内睾丸缺如，则诊断更为明确。\n（5）急性肠梗阻：肠管被嵌顿的疝可伴发急性肠梗阻，但不应仅满足于肠梗阻的诊断而忽略疝的存在；尤其是病人比较肥胖或疝块较小时，更易发生这类问题而导致治疗上的错误。\n（6）此外，腹股沟区肿块还应与以下疾病鉴别:肿大的淋巴结、动（静）脉瘤、软组织肿瘤、脓肿、\n圆韧带囊肿、子宫内膜异位症等。"
        },
        {
            "question": "简述该病人的治疗原则。",
            "solution": "嵌顿性疝原则上需要紧急手术治疗，以防止疝内容物坏死并解除伴发的肠梗阻。术前应做好必要的准备，如有脱水和电解质紊乱，应迅速补液加以纠正。手术的关键在于正确判断疝内容物的活力，然后根据病情确定处理方法。在扩张或切开疝环、解除疝环压迫的前提下，凡肠管呈紫黑色，失去光泽和弹性，刺激后无蠕动和相应肠系膜内无动脉搏动者，即可判定为肠坏死。如肠管尚未坏死，则可将其送回腹腔，按一般易复性疝处理，即行疝囊高位结扎+疝修补术。如肠管确已坏死或一时不能肯定肠管是否已失去活力时，则应在病人全身情况允许的前提下，切除该段肠管并进行一期吻合。凡施行肠切除吻合术的病人，因手术区污染，在高位结扎疝囊后，一般不宜作疝修补术，以免因感染而致修补失败。"
        }
    ]
},
```
- title: name of disease
- description: information of patient
- QA_pairs: a series of questions and their solutions based on the description



## ℹ️ How to evaluate and submit refer to [link](https://github.com/FreedomIntelligence/CMB)

## 😘  Citation
Please use the following citation if you intend to use our dataset for training or evaluation:

```
@misc{cmedbenchmark,
  title={CMB: Chinese Medical Benchmark},
  author={Xidong Wang*, Guiming Hardy Chen*, Dingjie Song*, Zhiyi Zhang*, Qingying Xiao, Xiangbo Wu, Feng Jiang, Jianquan Li, Benyou Wang},
  note={Xidong Wang, Guiming Hardy Chen, Dingjie Song, and Zhiyi Zhang contributed equally to this github repo.},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/FreedomIntelligence/CMB}},
}
```

## Acknowledgement 
- We thank [Shenzhen Research Institute of Big Data](http://www.sribd.cn/) for their enormous support for this project.

- We thank the following doctors for participating in the human evaluation of CMB-Clin:
    
    - 林士军 (香港中文大学（深圳）附属第二医院)
    - 常河
    - 许晓爽
