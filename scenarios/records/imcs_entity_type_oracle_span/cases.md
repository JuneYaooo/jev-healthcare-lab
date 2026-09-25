# 中文给定实体类型识别：逐案例结果

95 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 10308783 | {"end_exclusive": 10, "sentence": "昨天医院开的蒙脱石散和妈咪爱", "start": 6, "target_span": "蒙脱石散"}… | 1 | 100.0% | 100.0% |
| 10671430 | {"end_exclusive": 47, "sentence": "如果治疗方案不能缓解，甚至加重，尤其是孩子精神状态不好，需要携带最近的检查和就诊记录去医院复诊！", "start": 45, "target_spa… | 1 | 0.0% | 100.0% |
| 10536340 | {"end_exclusive": 3, "sentence": "益生菌是不是就是双歧杆菌呢？", "start": 0, "target_span": "益生菌"}… | 1 | 100.0% | 100.0% |
| 10361156 | {"end_exclusive": 16, "sentence": "有点儿便秘，我看看有没有消化不良", "start": 12, "target_span": "消化不良"}… | 1 | 100.0% | 100.0% |
| 10143642 | {"end_exclusive": 21, "sentence": "一般如果生理性黄疸的话，主要出现为面部发黄，手脚一般不会黄的。", "start": 17, "target_span": "面部发黄"}… | 1 | 100.0% | 100.0% |
| 10794066 | {"end_exclusive": 9, "sentence": "孩子出现鼻塞，咳嗽，很可能是感冒的表现", "start": 7, "target_span": "咳嗽"}… | 1 | 100.0% | 100.0% |
| 10563580 | {"end_exclusive": 14, "sentence": "嗯嗯知道啦,谢谢医生,吃护彤没什么副作用是吗,从来没吃过", "start": 12, "target_span": "护彤"}… | 1 | 100.0% | 100.0% |
| 10763697 | {"end_exclusive": 23, "sentence": "注意观察咳嗽情况，如果治疗后出现咳嗽频繁，有痰，建议就医小儿科，让医生听诊，检查看气管里的情况，再做进一步处理。", "start": 22, "ta… | 1 | 100.0% | 100.0% |
| 10306738 | {"end_exclusive": 7, "sentence": "一般微生态药物包括双歧杆菌，布拉氏菌酵母散等", "start": 2, "target_span": "微生态药物"}… | 1 | 100.0% | 100.0% |
| 10146044 | {"end_exclusive": 39, "sentence": "相对来讲，如果不是说发展到支气管炎，肺炎之类的，或者明显的细菌感染，那么抗生素的使用我也是提倡使用要注意", "start": 36, "target… | 2 | 100.0% | 100.0% |
| 10618477 | {"end_exclusive": 24, "sentence": "至于你说的感冒药一点儿变化纳米颗粒那个，讨厌感冒，", "start": 22, "target_span": "感冒"}… | 1 | 100.0% | 100.0% |
| 10395962 | {"end_exclusive": 7, "sentence": "可以吃上妈咪爱和思密达", "start": 4, "target_span": "妈咪爱"}… | 1 | 100.0% | 100.0% |
| 10126831 | {"end_exclusive": 14, "sentence": "您好，宝宝咳嗽多久了？有发热喘憋吗？", "start": 12, "target_span": "发热"}… | 1 | 100.0% | 100.0% |
| 10409100 | {"end_exclusive": 11, "sentence": "宝宝肚子咕噜响吗？放屁多吗？还有其他症状吗？", "start": 9, "target_span": "放屁"}… | 1 | 100.0% | 100.0% |
| 10113334 | {"end_exclusive": 6, "sentence": "你感觉有奶瓣吗？", "start": 4, "target_span": "奶瓣"}… | 1 | 100.0% | 100.0% |
| 10153677 | {"end_exclusive": 21, "sentence": "那宝宝应该是感冒引起的鼻炎给他一直在流鼻涕，嗯现在要去看一遍的话那就不用给他吃抗生素了，接着给他吃抗过敏的药，", "start": 18, "tar… | 1 | 100.0% | 100.0% |
| 10204965 | {"end_exclusive": 4, "sentence": "还有头孢", "start": 2, "target_span": "头孢"}… | 1 | 100.0% | 0.0% |
| 10490091 | {"end_exclusive": 16, "sentence": "不用谢！晚上被一些退热贴或者退热栓，如果大便不出来，还是会出现发热", "start": 14, "target_span": "退热"}… | 1 | 0.0% | 100.0% |
| 10358876 | {"end_exclusive": 13, "sentence": "先给宝宝口服小儿氨酚黄那敏。", "start": 6, "target_span": "小儿氨酚黄那敏"}… | 1 | 100.0% | 100.0% |
| 10742145 | {"end_exclusive": 7, "sentence": "可以吃点茵栀黄，培菲康调节一下胃肠道", "start": 4, "target_span": "茵栀黄"}… | 1 | 100.0% | 100.0% |
| 10372140 | {"end_exclusive": 10, "sentence": "在家吃的化痰止咳颗粒，今天又喝的氨溴索口服液。还用去点儿头孢类的炫耀吗？", "start": 4, "target_span": "化痰止咳颗粒"}… | 1 | 100.0% | 100.0% |
| 10201880 | {"end_exclusive": 11, "sentence": "宝宝三个月以内容易吐奶", "start": 9, "target_span": "吐奶"}… | 1 | 100.0% | 100.0% |
| 10365840 | {"end_exclusive": 40, "sentence": "他的这个白细胞是在正常范围。支持一个病毒性的感染。你的那个药物主要就是对症抗病毒所以是对症的。", "start": 37, "target_span… | 1 | 100.0% | 100.0% |
| 10691361 | {"end_exclusive": 15, "sentence": "现在咳嗽还厉害吗，有痰还是干咳？", "start": 13, "target_span": "干咳"}… | 1 | 100.0% | 100.0% |
| 10405518 | {"end_exclusive": 3, "sentence": "没有痰也不流鼻涕", "start": 2, "target_span": "痰"}… | 2 | 100.0% | 100.0% |
| 10219090 | {"end_exclusive": 7, "sentence": "到医院只做雾化给做吗", "start": 5, "target_span": "雾化"}… | 1 | 100.0% | 100.0% |
| 10692933 | {"end_exclusive": 4, "sentence": "37.7", "start": 0, "target_span": "37.7"}… | 1 | 100.0% | 0.0% |
| 10115296 | {"end_exclusive": 8, "sentence": "这次还要注意咳嗽会不会反复", "start": 6, "target_span": "咳嗽"}… | 1 | 100.0% | 100.0% |
| 10672500 | {"end_exclusive": 16, "sentence": "说明书说长期过量的服用会出现发热，但是宝宝第一次服用，我觉得可能性不大，但仍然也要考虑。谨慎起见，暂时不再服用维生素d滴剂啦。", "start": … | 1 | 100.0% | 100.0% |
| 10287846 | {"end_exclusive": 14, "sentence": "这个宝贝这么小，最好给宝贝查个血常规胸片", "start": 13, "target_span": "查"}… | 1 | 100.0% | 100.0% |
| 10420315 | {"end_exclusive": 33, "sentence": "问题宝宝两岁了，早晨发烧，去看了是扁桃体发炎，推的药。开了点消炎药，宝宝这会有点咳嗽，有点呕吐", "start": 30, "target_span… | 1 | 100.0% | 100.0% |
| 10154935 | {"end_exclusive": 10, "sentence": "也应该注意是否是感冒引起的肠系膜淋巴结炎？", "start": 8, "target_span": "感冒"}… | 1 | 100.0% | 100.0% |
| 10075507 | {"end_exclusive": 4, "sentence": "对于腹泻的孩子，推拿是相当管用的。在感染控制以后，腹泻的症状会逐渐的缓解", "start": 2, "target_span": "腹泻"}… | 1 | 100.0% | 100.0% |
| 10117415 | {"end_exclusive": 4, "sentence": "咳嗽没痰", "start": 3, "target_span": "痰"}… | 1 | 100.0% | 100.0% |
| 10619691 | {"end_exclusive": 12, "sentence": "假如出现腹泻加重，精神差，出现呕吐了，就建议去医院儿科看看了", "start": 9, "target_span": "精神差"}… | 1 | 100.0% | 100.0% |
| 10041940 | {"end_exclusive": 21, "sentence": "但是粪便隐性阳性还是要注意有没有病毒性肠炎", "start": 16, "target_span": "病毒性肠炎"}… | 1 | 100.0% | 0.0% |
| 10362641 | {"end_exclusive": 5, "sentence": "咳嗽流鼻涕吗？", "start": 2, "target_span": "流鼻涕"}… | 1 | 100.0% | 100.0% |
| 10304053 | {"end_exclusive": 8, "sentence": "对了，他哥哥感冒了，是不是他哥哥传染的啊，他哥哥4岁半了，", "start": 6, "target_span": "感冒"}… | 1 | 100.0% | 100.0% |
| 10335063 | {"end_exclusive": 5, "sentence": "各种消化药都吃了", "start": 2, "target_span": "消化药"}… | 1 | 100.0% | 100.0% |
| 10777965 | {"end_exclusive": 10, "sentence": "吃了小儿柴桂退烧颗粒", "start": 2, "target_span": "小儿柴桂退烧颗粒"}… | 1 | 100.0% | 100.0% |
| 10042920 | {"end_exclusive": 15, "sentence": "频繁的呕吐，最容易导致支气管炎和鼻塞。", "start": 11, "target_span": "支气管炎"}… | 1 | 100.0% | 100.0% |
| 10243045 | {"end_exclusive": 62, "sentence": "就是不严重，我媳妇非说要自愈，然后过两天去医院开了感冒药咳嗽药，然后吃了一天，又去看中医，吃的中药，然后又严重了，就开始雾化", "start": 6… | 1 | 100.0% | 100.0% |
| 10675602 | {"end_exclusive": 8, "sentence": "有没有进行肝功能的检查", "start": 5, "target_span": "肝功能"}… | 1 | 100.0% | 100.0% |
| 10603433 | {"end_exclusive": 33, "sentence": "那目前看大便情况，主要还是发烧，感冒，引起的消化不良，胃肠功能紊乱，继续服用益生菌就可以了。", "start": 27, "target_span"… | 2 | 100.0% | 100.0% |
| 10566119 | {"end_exclusive": 12, "sentence": "有点绿色，多伴有消化不好，加上金双歧促进消化看看", "start": 8, "target_span": "消化不好"}… | 1 | 100.0% | 100.0% |
| 10303236 | {"end_exclusive": 4, "sentence": "积食化验不出", "start": 2, "target_span": "化验"}… | 1 | 100.0% | 100.0% |
| 10398220 | {"end_exclusive": 15, "sentence": "嗯嗯，这个病毒感染是主要抗病毒及保肝，对症治疗", "start": 12, "target_span": "抗病毒"}… | 1 | 100.0% | 100.0% |
| 10359262 | {"end_exclusive": 28, "sentence": "吃了好多药都不管用，这几天感冒了，拉的更严重了，都成水样的了", "start": 26, "target_span": "水样"}… | 1 | 100.0% | 100.0% |
| 10841074 | {"end_exclusive": 5, "sentence": "现在是输液治疗了吗？用的什么药物，发我看一下吧。", "start": 3, "target_span": "输液"}… | 2 | 100.0% | 100.0% |
| 10642754 | {"end_exclusive": 23, "sentence": "目前建议继续在新生儿科住院治疗，积极的照射蓝光，尽快的把黄疸降到安全范围，以防产生脑神经损伤，引起胆红素脑病。", "start": 19, "tar… | 1 | 100.0% | 100.0% |
| 10339599 | {"end_exclusive": 2, "sentence": "头疼，昨天刚吃早饭就吐了，去门诊医生检查口腔又吐了", "start": 0, "target_span": "头疼"}… | 1 | 100.0% | 100.0% |
| 10658064 | {"end_exclusive": 2, "sentence": "发热", "start": 0, "target_span": "发热"}… | 1 | 100.0% | 100.0% |
| 10489811 | {"end_exclusive": 42, "sentence": "好的，先观察宝宝状态吧，暂时不用药，低热持续三天考虑随时去医院检查。另外消化不良腹泻也可以导致低热", "start": 40, "target_sp… | 1 | 100.0% | 100.0% |
| 10747362 | {"end_exclusive": 20, "sentence": "是先吃蒙脱石散再吃别的，还是后吃蒙脱石散", "start": 16, "target_span": "蒙脱石散"}… | 1 | 100.0% | 100.0% |
| 10849488 | {"end_exclusive": 2, "sentence": "雾化排痰治疗", "start": 0, "target_span": "雾化"}… | 1 | 100.0% | 100.0% |
| 10340157 | {"end_exclusive": 9, "sentence": "减轻点，还是有点咳，咳的时候听着有痰", "start": 8, "target_span": "咳"}… | 1 | 100.0% | 100.0% |
| 10293386 | {"end_exclusive": 9, "sentence": "桔贝合剂，匹多莫德，阿奇霉素干混悬剂", "start": 5, "target_span": "匹多莫德"}… | 1 | 100.0% | 100.0% |
| 10097362 | {"end_exclusive": 30, "sentence": "从你发的图片看着孩子大便当中奶瓣比较多，应该考虑消化功能不好", "start": 24, "target_span": "消化功能不好"}… | 1 | 100.0% | 100.0% |
| 10644554 | {"end_exclusive": 6, "sentence": "现在小孩化验过乙肝五项吗？有没有感染到？", "start": 4, "target_span": "化验"}… | 1 | 100.0% | 100.0% |
| 10854835 | {"end_exclusive": 2, "sentence": "克洛行不", "start": 0, "target_span": "克洛"}… | 1 | 100.0% | 100.0% |
| 10517882 | {"end_exclusive": 14, "sentence": "根据你叙述的情况，孩子的发烧原因现在还不清楚，两岁宝宝最常见的发烧原因，感冒，积食这些，需要观察孩子的情况来进一步判断！", "start": 12,… | 1 | 100.0% | 100.0% |
| 10172036 | {"end_exclusive": 33, "sentence": "血常规和胸片必须要查的，这个孩子咳嗽时间比较长，另外还需要进行肺炎支原体的检查", "start": 31, "target_span": "肺炎"}… | 1 | 0.0% | 0.0% |
| 10144895 | {"end_exclusive": 59, "sentence": "注意腹部保暖，妈妈饮食要清淡一点，不要吃易过敏、不易消化、油腻的食物。再按上述用法吃2天，如果还没有任何好转，需要化验大便", "start": 57… | 1 | 100.0% | 100.0% |
| 10799495 | {"end_exclusive": 6, "sentence": "去医院做检查没有什么问题，但是现在就是偶尔咳下", "start": 4, "target_span": "检查"}… | 1 | 100.0% | 100.0% |
| 10300622 | {"end_exclusive": 4, "sentence": "或者头孢己新加易坦静？", "start": 2, "target_span": "头孢"}… | 1 | 0.0% | 0.0% |
| 10880605 | {"end_exclusive": 18, "sentence": "我看孩子那个大便有绿色的，而且比较稀。考虑，腹泻病可能性大。", "start": 17, "target_span": "稀"}… | 1 | 100.0% | 100.0% |
| 10314181 | {"end_exclusive": 19, "sentence": "小儿抵抗力差，感冒以后很容易引起气管炎和肺炎的。", "start": 16, "target_span": "气管炎"}… | 2 | 100.0% | 100.0% |
| 10511143 | {"end_exclusive": 5, "sentence": "宝宝流鼻涕？鼻塞吗？", "start": 2, "target_span": "流鼻涕"}… | 1 | 100.0% | 100.0% |
| 10069596 | {"end_exclusive": 4, "sentence": "没有发热，呕吐", "start": 2, "target_span": "发热"}… | 1 | 100.0% | 100.0% |
| 10458540 | {"end_exclusive": 21, "sentence": "宝宝目前的主要症状大便次数增多，黄色稀水样的大便，还伴有一个低烧。考虑腹泻待查。具体的原因有可能是消化不良，病毒感染或者细菌感染等等。", "star… | 1 | 100.0% | 100.0% |
| 10853857 | {"end_exclusive": 31, "sentence": "注意环境安静，室温合适，衣物要宽松，出生后半个月开始补充维生素d滴剂", "start": 28, "target_span": "维生素"}… | 1 | 100.0% | 0.0% |
| 10864960 | {"end_exclusive": 26, "sentence": "推荐，小儿咽扁颗粒。每次13包，一天两次。治疗嗓子哑。", "start": 23, "target_span": "嗓子哑"}… | 1 | 100.0% | 100.0% |
| 10236687 | {"end_exclusive": 10, "sentence": "从什么时间开始拉肚子了，一发热就有拉肚子的情况？", "start": 7, "target_span": "拉肚子"}… | 1 | 100.0% | 100.0% |
| 10505115 | {"end_exclusive": 6, "sentence": "因为长期腹泻影响孩子营养的吸收，可能会出现贫血，电解质紊乱，肠壁黏膜脱落，便血等", "start": 4, "target_span": "腹泻"}… | 1 | 100.0% | 100.0% |
| 10003026 | {"end_exclusive": 2, "sentence": "咳嗽频率较前有加重没有", "start": 0, "target_span": "咳嗽"}… | 1 | 100.0% | 100.0% |
| 10583167 | {"end_exclusive": 5, "sentence": "宝宝拉肚子几天了？", "start": 2, "target_span": "拉肚子"}… | 1 | 100.0% | 100.0% |
| 10342476 | {"end_exclusive": 5, "sentence": "查胃肠彩超，排除巨结肠的胃肠发育原因", "start": 1, "target_span": "胃肠彩超"}… | 1 | 100.0% | 100.0% |
| 10141488 | {"end_exclusive": 14, "sentence": "从化验结果分析，宝宝细菌感染", "start": 10, "target_span": "细菌感染"}… | 1 | 100.0% | 100.0% |
| 10602664 | {"end_exclusive": 9, "sentence": "是的，总是反复发烧，很着急", "start": 7, "target_span": "发烧"}… | 1 | 100.0% | 100.0% |
| 10291187 | {"end_exclusive": 2, "sentence": "头孢过敏不", "start": 0, "target_span": "头孢"}… | 1 | 100.0% | 0.0% |
| 10132419 | {"end_exclusive": 20, "sentence": "鼻涕流的不算很多,偶尔出来一点,没有咳嗽", "start": 18, "target_span": "咳嗽"}… | 1 | 100.0% | 100.0% |
| 10471321 | {"end_exclusive": 2, "sentence": "咳嗽呼噜流鼻涕", "start": 0, "target_span": "咳嗽"}… | 1 | 100.0% | 100.0% |
| 10298891 | {"end_exclusive": 8, "sentence": "没有，就是咳嗽痰多", "start": 7, "target_span": "痰"}… | 1 | 100.0% | 100.0% |
| 10412723 | {"end_exclusive": 5, "sentence": "吃的止咳药", "start": 2, "target_span": "止咳药"}… | 1 | 100.0% | 0.0% |
| 10556801 | {"end_exclusive": 6, "sentence": "现在除了咳嗽，还有别的其他症状吗？", "start": 4, "target_span": "咳嗽"}… | 1 | 100.0% | 100.0% |
| 10732886 | {"end_exclusive": 10, "sentence": "额一般来说拿这种感冒的话，量体发炎需要反复发这个两到三天的，", "start": 8, "target_span": "感冒"}… | 1 | 100.0% | 100.0% |
| 10787762 | {"end_exclusive": 14, "sentence": "孩子可能是水土不服引起的感冒", "start": 12, "target_span": "感冒"}… | 1 | 100.0% | 100.0% |
| 10217465 | {"end_exclusive": 9, "sentence": "昨天没有查，以前查过", "start": 8, "target_span": "查"}… | 1 | 100.0% | 100.0% |
| 10520085 | {"end_exclusive": 5, "sentence": "布洛芬颗粒,一天可以吃多少吗", "start": 0, "target_span": "布洛芬颗粒"}… | 1 | 100.0% | 100.0% |
| 10295503 | {"end_exclusive": 14, "sentence": "可以在空腹时吃复方凝乳酶胶囊或硫糖铝凝胶，保护胃黏膜，吃思密达止泻，饭后吃益生菌和乳酶生帮助消化。", "start": 7, "target_spa… | 1 | 100.0% | 100.0% |
| 10114255 | {"end_exclusive": 9, "sentence": "那现在家里有氨溴索，四季抗病毒，开喉剑可以给他用吗？", "start": 6, "target_span": "氨溴索"}… | 1 | 100.0% | 100.0% |
| 10846852 | {"end_exclusive": 24, "sentence": "因为两个的宝宝的受很多的因素的影响，比如说：过敏", "start": 22, "target_span": "过敏"}… | 1 | 100.0% | 100.0% |
| 10405628 | {"end_exclusive": 2, "sentence": "发热几天了？之前吃了很多奶吗", "start": 0, "target_span": "发热"}… | 1 | 100.0% | 100.0% |
| 10116314 | {"end_exclusive": 89, "sentence": "问题八个月的宝宝反复发烧两次了，刚给他吃了复方锌布颗粒，妈咪爱，头孢克洛干混悬剂，抗病毒口服液乳酸菌素颗粒。。。现在的症状流鼻涕，有点闹肚子水样的，，… | 1 | 100.0% | 100.0% |
| 10489130 | {"end_exclusive": 6, "sentence": "止咳化痰药物如氨溴特罗。", "start": 0, "target_span": "止咳化痰药物"}… | 1 | 100.0% | 100.0% |
