# 中文问诊对话行为分类：逐案例结果

95 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 10109679 | {"context": [{"sentence": "你好，很高兴为你服务！", "sentence_id": "1", "speaker": "医生"}], "target": {"sentence": "就今天去小医… | 1 | 0.0% | 0.0% |
| 10489096 | {"context": [{"sentence": "老是出现鼻塞现象", "sentence_id": "14", "speaker": "患者"}, {"sentence": "有时候晚上睡着的时候拿镊子，把鼻屎抠出… | 1 | 100.0% | 100.0% |
| 10579421 | {"context": [{"sentence": "肚子", "sentence_id": "8", "speaker": "患者"}, {"sentence": "还有没消化的东西", "sentence_id": … | 1 | 100.0% | 100.0% |
| 10231105 | {"context": [{"sentence": "医生没有调整药物吗", "sentence_id": "41", "speaker": "医生"}, {"sentence": "晚上睡不好总是哭闹.叫唤", "se… | 1 | 100.0% | 100.0% |
| 10299631 | {"context": [{"sentence": "嗯嗯", "sentence_id": "14", "speaker": "医生"}, {"sentence": "宝宝睡觉打呼噜吗", "sentence_id":… | 1 | 100.0% | 100.0% |
| 10293983 | {"context": [{"sentence": "可以适当给孩子口服免疫调节剂，增加孩子的抵抗力", "sentence_id": "6", "speaker": "医生"}, {"sentence": "小儿热速清… | 1 | 100.0% | 100.0% |
| 10668558 | {"context": [{"sentence": "如果孩子出现呛奶，或者吐奶的时候，要及时的把脸侧向一侧，防止呛到气管里。反复的呛奶，可能会加重呼吸道的炎症。", "sentence_id": "25", "spea… | 2 | 100.0% | 100.0% |
| 10228814 | {"context": [{"sentence": "8.1，9.2", "sentence_id": "18", "speaker": "医生"}, {"sentence": "用这个值17.1", "sentence… | 2 | 50.0% | 50.0% |
| 10295434 | {"context": [{"sentence": "一起犯小脾气引起重视，", "sentence_id": "21", "speaker": "医生"}, {"sentence": "好的谢谢医生", "senten… | 1 | 100.0% | 100.0% |
| 10557134 | {"context": [{"sentence": "为什么前几天开塞露打得多，然后接下来两天她自己都能排出来，还不干了，后来我家了点米粉接下来就走开始便秘了？", "sentence_id": "32", "speak… | 1 | 0.0% | 0.0% |
| 10120528 | {"context": [{"sentence": "着凉怎么样？", "sentence_id": "7", "speaker": "医生"}, {"sentence": "有没有明显着凉冻肚子或者接触感冒的人？", … | 1 | 0.0% | 100.0% |
| 10223933 | {"context": [{"sentence": "还有什么问题吗？没有我就关闭对话框了，好吗？", "sentence_id": "25", "speaker": "医生"}, {"sentence": "小儿咳喘灵… | 1 | 100.0% | 100.0% |
| 10603433 | {"context": [{"sentence": "看目前有流鼻涕，发烧症状，同时有吐奶，腹泻。考虑确实是小儿胃肠型感冒，一般是病毒感染引起的。", "sentence_id": "11", "speaker": "医… | 1 | 100.0% | 100.0% |
| 10420275 | {"context": [{"sentence": "还有小儿百步糖浆", "sentence_id": "24", "speaker": "患者"}, {"sentence": "一般小孩儿多见的是病毒感染引起", "… | 1 | 100.0% | 100.0% |
| 10324582 | {"context": [], "target": {"sentence": "你好，孩子有没有鼻塞，流涕呢", "sentence_id": "1", "speaker": "医生"}}… | 1 | 100.0% | 100.0% |
| 10125134 | {"context": [{"sentence": "孩没有流鼻涕", "sentence_id": "45", "speaker": "患者"}, {"sentence": "我认为首先应该进行肺炎支原体检查，因为支原… | 1 | 100.0% | 100.0% |
| 10286786 | {"context": [{"sentence": "口唇干尿也少", "sentence_id": "15", "speaker": "患者"}, {"sentence": "是不轮状病毒肠炎？", "sentence… | 1 | 100.0% | 100.0% |
| 10563580 | {"context": [{"sentence": "好滴,像我宝宝这种吃三天就行还是需要更久", "sentence_id": "32", "speaker": "患者"}, {"sentence": "一般吃三天就可… | 2 | 100.0% | 100.0% |
| 10296832 | {"context": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "在吗", "sentence_id": "2", "… | 1 | 100.0% | 100.0% |
| 10023928 | {"context": [{"sentence": "白细胞数明显的升高，应该考虑细菌感染，细菌感染的孩子是需要应用抗生素的，对孩子影响不大。抗生素是有副作用的，我们需要看的是抗生素的治疗作用大还是副作用大，显然这个孩子… | 1 | 0.0% | 0.0% |
| 10113847 | {"context": [{"sentence": "好的。谢谢医生。节日快乐。我没有问题了", "sentence_id": "29", "speaker": "患者"}, {"sentence": "再见", "se… | 1 | 100.0% | 100.0% |
| 10079995 | {"context": [], "target": {"sentence": "你好，发热有多久了呢", "sentence_id": "1", "speaker": "医生"}}… | 1 | 100.0% | 100.0% |
| 10029209 | {"context": [{"sentence": "有时拉的屎很稀，有时屎很黏", "sentence_id": "5", "speaker": "患者"}, {"sentence": "次数正常不，饮食正常不，精神状… | 1 | 0.0% | 0.0% |
| 10011151 | {"context": [{"sentence": "发烧39度现在", "sentence_id": "8", "speaker": "患者"}, {"sentence": "喝了布洛芬也不退", "sentence_… | 1 | 100.0% | 100.0% |
| 10722230 | {"context": [{"sentence": "消化功能不良的原因", "sentence_id": "33", "speaker": "医生"}, {"sentence": "好的", "sentence_id"… | 1 | 100.0% | 100.0% |
| 10185504 | {"context": [{"sentence": "好的，知道了", "sentence_id": "31", "speaker": "患者"}, {"sentence": "嗯嗯", "sentence_id": "… | 1 | 100.0% | 100.0% |
| 10675602 | {"context": [{"sentence": "孩子出生以后多长时间了", "sentence_id": "8", "speaker": "医生"}, {"sentence": "今天第十一天", "sentenc… | 1 | 100.0% | 0.0% |
| 10649219 | {"context": [{"sentence": "用不用化验微量元素了，哦，一直到现在补锌还补钙", "sentence_id": "37", "speaker": "患者"}, {"sentence": "嗯，一般… | 1 | 100.0% | 100.0% |
| 10288543 | {"context": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", "… | 1 | 0.0% | 0.0% |
| 10172036 | {"context": [{"sentence": "你好", "sentence_id": "2", "speaker": "患者"}, {"sentence": "有几个具体的细节问题，我需要向你询问一下，希望你能配… | 1 | 100.0% | 100.0% |
| 10348914 | {"context": [{"sentence": "昨天发热了，给他扭莎了烧今天腿了", "sentence_id": "23", "speaker": "患者"}, {"sentence": "感冒发热，吃药了吗？吃… | 1 | 100.0% | 100.0% |
| 10296238 | {"context": [{"sentence": "你好", "sentence_id": "2", "speaker": "患者"}, {"sentence": "孩子大便鼻涕样粘稠物是肠道分泌液", "senten… | 1 | 0.0% | 0.0% |
| 10471721 | {"context": [{"sentence": "这个孩子精神状态怎么样", "sentence_id": "3", "speaker": "医生"}, {"sentence": "不好", "sentence_id… | 1 | 100.0% | 100.0% |
| 10406010 | {"context": [{"sentence": "好的", "sentence_id": "24", "speaker": "患者"}, {"sentence": "平时可以让宝宝多喝水，咳嗽厉害时候拍背促进痰液排出… | 1 | 100.0% | 100.0% |
| 10119218 | {"context": [{"sentence": "建议复查，最好拍一下胸片检查", "sentence_id": "45", "speaker": "医生"}, {"sentence": "必要时建议雾化治疗", "… | 2 | 100.0% | 100.0% |
| 10800956 | {"context": [{"sentence": "哦，根据您说的情况分析，这应该是正常现象", "sentence_id": "10", "speaker": "医生"}, {"sentence": "是什么原因呢"… | 1 | 100.0% | 100.0% |
| 10473083 | {"context": [{"sentence": "口服药物三天，观察变化。", "sentence_id": "39", "speaker": "医生"}, {"sentence": "如果咳嗽消失可以停止药物。",… | 1 | 0.0% | 0.0% |
| 10351608 | {"context": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "您好", "sentence_id": "2", "… | 1 | 100.0% | 100.0% |
| 10524178 | {"context": [{"sentence": "喝一支可以吗", "sentence_id": "23", "speaker": "患者"}, {"sentence": "我看痰还是比较多，医生有没有给开专门的化痰… | 1 | 0.0% | 0.0% |
| 10261841 | {"context": [{"sentence": "每天五六次", "sentence_id": "9", "speaker": "患者"}, {"sentence": "没有", "sentence_id": "10… | 1 | 0.0% | 0.0% |
| 10199090 | {"context": [{"sentence": "先看看是不是有鼻炎", "sentence_id": "33", "speaker": "医生"}, {"sentence": "有鼻炎的话，先治疗鼻炎", "sen… | 1 | 0.0% | 0.0% |
| 10268861 | {"context": [{"sentence": "好", "sentence_id": "42", "speaker": "患者"}, {"sentence": "谢谢", "sentence_id": "43", … | 1 | 100.0% | 100.0% |
| 10011048 | {"context": [{"sentence": "精灵蓓蓓上面都没有说明的五个月宝宝一天吃多少都没有的，我还以为吃杂牌", "sentence_id": "40", "speaker": "患者"}, {"sente… | 1 | 100.0% | 100.0% |
| 10342587 | {"context": [{"sentence": "嗯", "sentence_id": "31", "speaker": "医生"}, {"sentence": "因为我听说母亲咳嗽，小孩吃奶不好，会加重病情是吗",… | 1 | 0.0% | 0.0% |
| 10425533 | {"context": [{"sentence": "一直都在吃", "sentence_id": "9", "speaker": "患者"}, {"sentence": "嗯嗯，现在大便几天一次？", "sentenc… | 1 | 100.0% | 100.0% |
| 10154935 | {"context": [{"sentence": "有没有呕吐？", "sentence_id": "4", "speaker": "医生"}, {"sentence": "六点半的时候吐了一次，要舒服一点。头晕", … | 1 | 100.0% | 100.0% |
| 10799495 | {"context": [{"sentence": "是的", "sentence_id": "43", "speaker": "医生"}, {"sentence": "拿单子给你看？", "sentence_id": … | 1 | 0.0% | 0.0% |
| 10201880 | {"context": [{"sentence": "和自身胃比较浅有关系", "sentence_id": "34", "speaker": "医生"}, {"sentence": "会影响宝宝", "sentence… | 1 | 100.0% | 100.0% |
| 10236687 | {"context": [{"sentence": "拉肚子拉了几天了，也是一个周？", "sentence_id": "28", "speaker": "医生"}, {"sentence": "这个孩子不是38.7度的… | 1 | 100.0% | 100.0% |
| 10089522 | {"context": [{"sentence": "宝宝精神好吗", "sentence_id": "3", "speaker": "医生"}, {"sentence": "精神很好", "sentence_id": … | 1 | 100.0% | 100.0% |
| 10075507 | {"context": [{"sentence": "现在还是有咳嗽的症状，需要口服抗过敏的药物，可以选择开瑞坦", "sentence_id": "39", "speaker": "医生"}, {"sentence":… | 2 | 100.0% | 100.0% |
| 10045489 | {"context": [{"sentence": "哦，很难避免", "sentence_id": "34", "speaker": "患者"}, {"sentence": "如果白细胞数继续增加，需要口服消炎药", … | 1 | 0.0% | 100.0% |
| 10108555 | {"context": [{"sentence": "丝丝的", "sentence_id": "10", "speaker": "患者"}, {"sentence": "这个是喘息", "sentence_id": "… | 1 | 100.0% | 100.0% |
| 10358398 | {"context": [{"sentence": "能退到多少度", "sentence_id": "9", "speaker": "医生"}, {"sentence": "（空）", "sentence_id": "… | 1 | 0.0% | 0.0% |
| 10087556 | {"context": [{"sentence": "4天", "sentence_id": "6", "speaker": "患者"}, {"sentence": "1岁", "sentence_id": "7", "… | 1 | 100.0% | 100.0% |
| 10311103 | {"context": [{"sentence": "头痛时有没有呕吐", "sentence_id": "13", "speaker": "医生"}, {"sentence": "没有", "sentence_id":… | 1 | 100.0% | 0.0% |
| 10498471 | {"context": [{"sentence": "好的", "sentence_id": "13", "speaker": "医生"}, {"sentence": "后面那个医生开了2开雾化，叫我也输液，但宝宝作天才… | 1 | 0.0% | 0.0% |
| 10788046 | {"context": [{"sentence": "嗯嗯，那我如果下星期去影响大吗？还是明天去啊？", "sentence_id": "37", "speaker": "患者"}, {"sentence": "建议明天… | 1 | 100.0% | 0.0% |
| 10208054 | {"context": [{"sentence": "吃药有时吃一个月，过不了多长时间就又拉", "sentence_id": "24", "speaker": "患者"}, {"sentence": "如果孩子从小时候… | 1 | 0.0% | 0.0% |
| 10605041 | {"context": [{"sentence": "就是晚上咳", "sentence_id": "11", "speaker": "患者"}, {"sentence": "有过肺部听诊吗？目前有服用药物吗？", "s… | 1 | 0.0% | 0.0% |
| 10746036 | {"context": [{"sentence": "请问什么时候开始发烧？", "sentence_id": "3", "speaker": "医生"}, {"sentence": "昨天中午打的疫苗.晚上八点左右就烧… | 1 | 0.0% | 100.0% |
| 10484596 | {"context": [{"sentence": "桔梗止咳片可以吃多少", "sentence_id": "27", "speaker": "患者"}, {"sentence": "一般一次一片，一天3次即可", "… | 1 | 100.0% | 0.0% |
| 10787762 | {"context": [{"sentence": "推荐氯雷他定片，每次三分之一片，一天一次就可以", "sentence_id": "24", "speaker": "医生"}, {"sentence": "感冒治疗… | 1 | 100.0% | 100.0% |
| 10556801 | {"context": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}], "target": {"sentence": "你好，医生", "senten… | 1 | 100.0% | 100.0% |
| 10769238 | {"context": [{"sentence": "如果是肺结核，要吃抗痨药才有效", "sentence_id": "18", "speaker": "医生"}, {"sentence": "通常小儿很少肺纤维灶",… | 1 | 0.0% | 0.0% |
| 10228006 | {"context": [{"sentence": "除了头孢拉定和拉宗", "sentence_id": "35", "speaker": "医生"}, {"sentence": "这两个药容易引起血尿，不可以吃", … | 1 | 0.0% | 0.0% |
| 10619691 | {"context": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}], "target": {"sentence": "你好，", "sentence… | 1 | 100.0% | 100.0% |
| 10222259 | {"context": [{"sentence": "可以用温毛巾热敷鼻子", "sentence_id": "32", "speaker": "医生"}, {"sentence": "多喝温水", "sentence_… | 1 | 100.0% | 100.0% |
| 10411703 | {"context": [{"sentence": "最近小便量和平时一样吗", "sentence_id": "18", "speaker": "医生"}, {"sentence": "她要喝奶粉", "sentenc… | 1 | 0.0% | 0.0% |
| 10283358 | {"context": [{"sentence": "（空）", "sentence_id": "18", "speaker": "患者"}, {"sentence": "检查了", "sentence_id": "19… | 1 | 0.0% | 0.0% |
| 10443740 | {"context": [{"sentence": "宝贝目前的话主要是一个支气管炎的表现，这个可能受凉或者感染引起来的，治疗的原则一般就是消炎止咳化痰治疗的奥！", "sentence_id": "31", "spea… | 1 | 100.0% | 100.0% |
| 10846933 | {"context": [{"sentence": "注意观察体温情况，咳嗽轻重，以及声音嘶哑的情况。如果出现发烧，咳嗽加重，建议就医公立二甲医院小儿内科，让医生检查，进一步听诊，明确情况。", "sentence_id… | 1 | 100.0% | 100.0% |
| 10154237 | {"context": [{"sentence": "祝宝宝健康成长", "sentence_id": "30", "speaker": "医生"}, {"sentence": "还有其他问题吗？", "sentence… | 1 | 100.0% | 0.0% |
| 10170854 | {"context": [{"sentence": "有一点", "sentence_id": "7", "speaker": "患者"}, {"sentence": "您用的是什么退黄？茵栀黄颗粒吗？", "sente… | 1 | 100.0% | 100.0% |
| 10743738 | {"context": [{"sentence": "您好", "sentence_id": "2", "speaker": "患者"}, {"sentence": "宝贝最近家里有人感冒吗？", "sentence_i… | 1 | 0.0% | 0.0% |
| 10520085 | {"context": [{"sentence": "（空）", "sentence_id": "18", "speaker": "患者"}, {"sentence": "目前这个体温物理降温就可以了，可以温水擦身，冷毛… | 1 | 0.0% | 100.0% |
| 10864720 | {"context": [{"sentence": "不是，是说益生菌在喂奶前或喂奶时喂每次都会呕吐？", "sentence_id": "44", "speaker": "医生"}, {"sentence": "没有,… | 1 | 0.0% | 0.0% |
| 10116314 | {"context": [{"sentence": "流涕考虑上呼吸道感染，您用抗病毒的就可以了。", "sentence_id": "40", "speaker": "医生"}, {"sentence": "退热贴在发… | 1 | 100.0% | 100.0% |
| 10320588 | {"context": [{"sentence": "嗯，好的", "sentence_id": "36", "speaker": "患者"}, {"sentence": "谢谢医生", "sentence_id": "… | 1 | 100.0% | 100.0% |
| 10594957 | {"context": [{"sentence": "早上起他老吸鼻子，也扣", "sentence_id": "5", "speaker": "患者"}, {"sentence": "现在的情况，有可能是鼻炎引起鼻涕倒… | 1 | 100.0% | 100.0% |
| 10659024 | {"context": [{"sentence": "目前就这个状态，睡着，我们也没敢去碰她", "sentence_id": "23", "speaker": "患者"}, {"sentence": "好的医生，会不会… | 1 | 100.0% | 0.0% |
| 10578867 | {"context": [{"sentence": "到刚他醒了，感觉喉咙有些痰的感觉", "sentence_id": "37", "speaker": "患者"}, {"sentence": "是的，咳嗽刚开始一般是… | 1 | 100.0% | 100.0% |
| 10161079 | {"context": [{"sentence": "孩子食欲精神都挺好吗？", "sentence_id": "7", "speaker": "医生"}, {"sentence": "白天睡觉鼻子里有鼻涕，呼哧呼哧的，… | 1 | 100.0% | 100.0% |
| 10278593 | {"context": [{"sentence": "用阿莫西林，或者头孢类药物，庆大霉素对耳朵不好，不要吃", "sentence_id": "9", "speaker": "医生"}, {"sentence": "好… | 1 | 100.0% | 100.0% |
| 10747362 | {"context": [{"sentence": "没了", "sentence_id": "49", "speaker": "患者"}, {"sentence": "好的，有问题随时再联络。", "sentence_… | 1 | 100.0% | 100.0% |
| 10309191 | {"context": [{"sentence": "嗯嗯", "sentence_id": "30", "speaker": "医生"}, {"sentence": "体温在38.5以上可以吃点退热药，手脚热的话可以用… | 1 | 100.0% | 100.0% |
| 10357202 | {"context": [{"sentence": "拍照给你看一下嘛", "sentence_id": "16", "speaker": "患者"}, {"sentence": "好", "sentence_id": … | 1 | 100.0% | 100.0% |
| 10642754 | {"context": [{"sentence": "现在孩子精神状态怎样，吃奶情况怎样？如果有胆红素脑病的孩子，经常会精神不好，嗜睡，反应差，活动减少。", "sentence_id": "13", "speaker"… | 1 | 0.0% | 0.0% |
| 10026624 | {"context": [{"sentence": "轮状病毒肠炎的孩子，大便次数都很多，不可能一天一两次的", "sentence_id": "16", "speaker": "医生"}, {"sentence": "… | 1 | 0.0% | 0.0% |
| 10294841 | {"context": [{"sentence": "就正常状态下会疼吗", "sentence_id": "26", "speaker": "医生"}, {"sentence": "精神不好,总哭闹", "senten… | 1 | 100.0% | 100.0% |
| 10243045 | {"context": [{"sentence": "这个打点滴对宝宝会不会有很大的影响", "sentence_id": "15", "speaker": "患者"}, {"sentence": "是吧，得肺炎也是对肺… | 1 | 0.0% | 0.0% |
| 10256634 | {"context": [{"sentence": "是一直发紫还是有时候会？", "sentence_id": "15", "speaker": "医生"}, {"sentence": "一直", "sentence_… | 1 | 100.0% | 100.0% |
| 10284638 | {"context": [{"sentence": "关系不大的，注意腹部保暖", "sentence_id": "19", "speaker": "医生"}, {"sentence": "好的～～谢谢", "sente… | 1 | 100.0% | 100.0% |
| 10034499 | {"context": [{"sentence": "您好，在吗？", "sentence_id": "1", "speaker": "医生"}], "target": {"sentence": "嗯，在呢", "sen… | 1 | 100.0% | 100.0% |
| 10171923 | {"context": [{"sentence": "在吗", "sentence_id": "2", "speaker": "医生"}, {"sentence": "为了更好的提供服务，我需要询问您几个与病症相关的问题… | 1 | 100.0% | 100.0% |
