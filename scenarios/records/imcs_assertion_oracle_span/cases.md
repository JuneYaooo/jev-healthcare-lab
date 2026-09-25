# 中文症状肯否定状态：逐案例结果

91 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 10626577 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "咳嗽半月了。大夫听诊是支气管炎吗？", "sent… | 1 | 100.0% | 100.0% |
| 10313998 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10089127 | {"dialogue": [{"sentence": "孩子干咳还是有痰？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "好像是干咳，前两天感冒，感冒好了就开… | 1 | 100.0% | 100.0% |
| 10727119 | {"dialogue": [{"sentence": "你好，宝贝还在母乳喂养吗？最近吃奶咋么样？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "宝贝最近有没… | 1 | 100.0% | 100.0% |
| 10301480 | {"dialogue": [{"sentence": "你好！", "sentence_id": "1", "speaker": "医生"}, {"sentence": "发烧吗？", "sentence_id": "2… | 1 | 100.0% | 100.0% |
| 10846852 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10835516 | {"dialogue": [{"sentence": "孩子咳嗽总共几天了呢", "sentence_id": "1", "speaker": "医生"}, {"sentence": "快20天了", "sentence… | 2 | 100.0% | 100.0% |
| 10603433 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 2 | 100.0% | 50.0% |
| 10847829 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "37度5以上可以贴退热贴，多饮水，38.5度以上用… | 1 | 100.0% | 100.0% |
| 10658064 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10600006 | {"dialogue": [{"sentence": "您好！", "sentence_id": "1", "speaker": "医生"}, {"sentence": "舌头上有泡，孩子可能是病毒性的，反复发热和病毒感… | 1 | 0.0% | 0.0% |
| 10501977 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "目前咳嗽，看过医生吗，具体确诊了什么疾病", "s… | 1 | 100.0% | 100.0% |
| 10778228 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "咳嗽是干咳，还是有痰？", "sentence_i… | 1 | 100.0% | 0.0% |
| 10264160 | {"dialogue": [{"sentence": "你好！", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2",… | 1 | 100.0% | 100.0% |
| 10768005 | {"dialogue": [{"sentence": "您好！很高兴为您服务", "sentence_id": "1", "speaker": "医生"}, {"sentence": "为了更好的提供服务，我需要询问您几… | 1 | 100.0% | 100.0% |
| 10110161 | {"dialogue": [{"sentence": "你好，小孩现在咳嗽程度怎么样", "sentence_id": "1", "speaker": "医生"}, {"sentence": "咳嗽到是不太厉害了", "… | 1 | 0.0% | 0.0% |
| 10242702 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10399296 | {"dialogue": [{"sentence": "您好，我是您的辅诊医生，需要询问几个问题，才能更好的评估孩子情况，您还在吗？", "sentence_id": "1", "speaker": "医生"}, {"s… | 1 | 100.0% | 100.0% |
| 10342476 | {"dialogue": [{"sentence": "您好，我是您的辅诊医生，需要询问几个问题，才能更好的评估孩子情况，您还在吗？", "sentence_id": "1", "speaker": "医生"}, {"s… | 1 | 100.0% | 100.0% |
| 10315619 | {"dialogue": [{"sentence": "您好，请问您家孩子多大了", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_… | 1 | 100.0% | 100.0% |
| 10175834 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10400405 | {"dialogue": [{"sentence": "你好，就今天摔的吗？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "您好", "sentence_id… | 1 | 100.0% | 100.0% |
| 10214268 | {"dialogue": [{"sentence": "你好！", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2",… | 1 | 100.0% | 100.0% |
| 10361156 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 0.0% | 0.0% |
| 10190259 | {"dialogue": [{"sentence": "你好，很高兴能够帮助您。", "sentence_id": "1", "speaker": "医生"}, {"sentence": "您好", "sentence_… | 1 | 100.0% | 100.0% |
| 10412723 | {"dialogue": [{"sentence": "咳嗽多久了", "sentence_id": "1", "speaker": "医生"}, {"sentence": "两天", "sentence_id": "2… | 1 | 100.0% | 0.0% |
| 10618477 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10224684 | {"dialogue": [{"sentence": "你好！", "sentence_id": "1", "speaker": "医生"}, {"sentence": "在呢", "sentence_id": "2",… | 2 | 100.0% | 100.0% |
| 10594957 | {"dialogue": [{"sentence": "你好，小孩有流鼻涕鼻塞吗？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "没有", "sentence… | 2 | 50.0% | 50.0% |
| 10309191 | {"dialogue": [{"sentence": "您好，我是您的辅诊医生，需要询问几个问题，才能更好的评估孩子情况，您还在吗？", "sentence_id": "1", "speaker": "医生"}, {"s… | 1 | 0.0% | 100.0% |
| 10517361 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "目前看过医生吗，具体确诊了什么疾病", "sent… | 1 | 100.0% | 0.0% |
| 10515944 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "目前看过医生吗，具体确诊了什么疾病", "sent… | 2 | 50.0% | 50.0% |
| 10286582 | {"dialogue": [{"sentence": "为了更好的提供服务，我需要询问您几个与病症相关的问题，感谢您配合。", "sentence_id": "1", "speaker": "医生"}, {"senten… | 1 | 0.0% | 0.0% |
| 10608836 | {"dialogue": [{"sentence": "你好，这个化验说明小孩有缺锌缺钙缺铁。", "sentence_id": "1", "speaker": "医生"}, {"sentence": "可能和小孩便秘有… | 1 | 100.0% | 100.0% |
| 10268297 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "嗯嗯", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10358398 | {"dialogue": [{"sentence": "你好，目前除了反复发热，还有别的症状吗", "sentence_id": "1", "speaker": "医生"}, {"sentence": "大夫您好，孩子一… | 1 | 100.0% | 100.0% |
| 10284675 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好医生", "sentence_id": "2"… | 1 | 100.0% | 100.0% |
| 10864960 | {"dialogue": [{"sentence": "您好。", "sentence_id": "1", "speaker": "医生"}, {"sentence": "孩子最近有没有剧烈的哭闹？", "sentenc… | 2 | 100.0% | 100.0% |
| 10503107 | {"dialogue": [{"sentence": "您好，本次发热2天，除发热有其他不适症状吗？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "没有", … | 2 | 50.0% | 50.0% |
| 10372608 | {"dialogue": [{"sentence": "你好，目前孩子咳嗽厉害吗", "sentence_id": "1", "speaker": "医生"}, {"sentence": "近几天下午咳嗽，有时还不咳嗽"… | 1 | 100.0% | 100.0% |
| 10656651 | {"dialogue": [{"sentence": "你好我是您的接诊医生", "sentence_id": "1", "speaker": "医生"}, {"sentence": "宝贝最近家里有人感冒吗", "se… | 1 | 0.0% | 0.0% |
| 10579421 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 0.0% | 0.0% |
| 10602635 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 0.0% | 0.0% |
| 10063127 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 0.0% | 0.0% |
| 10303236 | {"dialogue": [{"sentence": "您好，宝宝有呕吐腹痛吗？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "没有呕吐，腹部有点胀", "s… | 1 | 100.0% | 100.0% |
| 10043402 | {"dialogue": [{"sentence": "您好，孩子发烧几天了？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "下午发的热", "sentenc… | 1 | 100.0% | 100.0% |
| 10042920 | {"dialogue": [{"sentence": "首先很乐意为您解答！我需咨询相关信息，请如实作答。", "sentence_id": "1", "speaker": "医生"}, {"sentence": "您好… | 1 | 100.0% | 100.0% |
| 10039491 | {"dialogue": [{"sentence": "为了更好的提供服务，我需要询问您几个与病症相关的问题，感谢您配合。", "sentence_id": "1", "speaker": "医生"}, {"senten… | 1 | 100.0% | 100.0% |
| 10251585 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "在吗", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10509950 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "目前看过医生吗，具体确诊了什么疾病", "sent… | 1 | 100.0% | 0.0% |
| 10063352 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "您好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10597189 | {"dialogue": [{"sentence": "你好我是您的接诊医生", "sentence_id": "1", "speaker": "医生"}, {"sentence": "宝贝最近家里有人感冒吗？", "s… | 1 | 100.0% | 100.0% |
| 10290786 | {"dialogue": [{"sentence": "你好，目前咳嗽还频繁吗", "sentence_id": "1", "speaker": "医生"}, {"sentence": "还好，一般就刚睡醒咳，睡觉不咳，… | 1 | 100.0% | 100.0% |
| 10405223 | {"dialogue": [{"sentence": "你好，目前的发烧属于中度烧，当前可以物理降温", "sentence_id": "1", "speaker": "医生"}, {"sentence": "物理降温"… | 1 | 100.0% | 100.0% |
| 10154080 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10294549 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "您好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10282417 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "宝宝是母乳喂养吗？", "sentence_id"… | 1 | 100.0% | 100.0% |
| 10696790 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "孩子经常几天一次大便？", "sentence_i… | 1 | 100.0% | 100.0% |
| 10429448 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "除了咳嗽宝宝还有别的不舒服吗？", "senten… | 1 | 100.0% | 100.0% |
| 10127215 | {"dialogue": [{"sentence": "你好，孩子现在状态好不好有没有拉肚子", "sentence_id": "1", "speaker": "医生"}, {"sentence": "暂时没拉肚子", … | 1 | 100.0% | 100.0% |
| 10201439 | {"dialogue": [{"sentence": "你好，很高兴能够帮助你。", "sentence_id": "1", "speaker": "医生"}, {"sentence": "儿子反复发烧，怎么办", "s… | 1 | 100.0% | 100.0% |
| 10037162 | {"dialogue": [{"sentence": "孩子一个多月的时间大便一直这样吗？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "对呀，有时候好了过两… | 1 | 100.0% | 100.0% |
| 10762750 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "宝宝发了几天了？", "sentence_id":… | 1 | 100.0% | 0.0% |
| 10141745 | {"dialogue": [{"sentence": "你好，很高兴帮助你。", "sentence_id": "1", "speaker": "医生"}, {"sentence": "宝宝咳嗽主要以白天为主还是晚上为主… | 1 | 100.0% | 100.0% |
| 10409100 | {"dialogue": [{"sentence": "您好，我是您的辅诊医生，需要询问几个问题，才能更好的评估孩子情况，您还在吗？", "sentence_id": "1", "speaker": "医生"}, {"s… | 2 | 50.0% | 50.0% |
| 10129820 | {"dialogue": [{"sentence": "您好，我是儿科主治医师张姣姣，同时也是一位宝妈，下面由我来帮您解答咨询，接下来就开始问诊、分析！", "sentence_id": "1", "speaker": … | 1 | 100.0% | 100.0% |
| 10160595 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "梨卡到之后有吐出来吗", "sentence_id… | 1 | 100.0% | 100.0% |
| 10742145 | {"dialogue": [{"sentence": "用什么草药洗的？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "不知道", "sentence_id"… | 1 | 100.0% | 100.0% |
| 10025885 | {"dialogue": [{"sentence": "你好,孩子咳嗽多长时间了?", "sentence_id": "1", "speaker": "医生"}, {"sentence": "半年多了", "senten… | 1 | 100.0% | 0.0% |
| 10306738 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "在吗", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10125134 | {"dialogue": [{"sentence": "你好，很高兴为你服务！", "sentence_id": "1", "speaker": "医生"}, {"sentence": "谢谢帮忙解答", "senten… | 1 | 0.0% | 100.0% |
| 10209199 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 0.0% | 0.0% |
| 10115288 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "在吗", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10587056 | {"dialogue": [{"sentence": "您好，宝宝发热几天了？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "体温最高多少？", "sente… | 1 | 100.0% | 100.0% |
| 10852486 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10223952 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10595871 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 0.0% | 0.0% |
| 10053788 | {"dialogue": [{"sentence": "您好，我是您这次的咨询医生", "sentence_id": "1", "speaker": "医生"}, {"sentence": "为了更准确的判断病情，我需要… | 1 | 0.0% | 0.0% |
| 10075507 | {"dialogue": [{"sentence": "目前孩子的精神状态怎么样", "sentence_id": "1", "speaker": "医生"}, {"sentence": "今天晚上发热37.8咳嗽", … | 1 | 100.0% | 100.0% |
| 10143338 | {"dialogue": [{"sentence": "你好，宝宝是足月出生吗？生的时候有没有异常。", "sentence_id": "1", "speaker": "医生"}, {"sentence": "38周加三… | 1 | 100.0% | 100.0% |
| 10221248 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "为了更好的提供服务，我需要询问您几个与病症相关的问… | 2 | 100.0% | 100.0% |
| 10798209 | {"dialogue": [{"sentence": "孩子什么时候打的疫苗呢", "sentence_id": "1", "speaker": "医生"}, {"sentence": "今天打的", "sentence… | 1 | 100.0% | 0.0% |
| 10163114 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10460319 | {"dialogue": [{"sentence": "你好，血常规化验怎么样？", "sentence_id": "1", "speaker": "医生"}, {"sentence": "这个阴影，最好做一个肺部CT检… | 1 | 0.0% | 0.0% |
| 10018726 | {"dialogue": [{"sentence": "您好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "宝宝现在晚上睡觉咳嗽不", "sentence_i… | 1 | 0.0% | 0.0% |
| 10491362 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 0.0% | 0.0% |
| 10219090 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "嗯你好", "sentence_id": "2",… | 1 | 100.0% | 100.0% |
| 10788046 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好", "sentence_id": "2", … | 1 | 100.0% | 100.0% |
| 10155990 | {"dialogue": [{"sentence": "您好，明显的疫苗反应，做好护理就可，注意腹部保暖，可以口服布拉氏酵母菌观察。", "sentence_id": "1", "speaker": "医生"}, {"s… | 1 | 100.0% | 100.0% |
| 10467781 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "你好我家宝宝之前干咳不是很厉害，大概每天白天也就平… | 1 | 100.0% | 100.0% |
| 10236687 | {"dialogue": [{"sentence": "你好", "sentence_id": "1", "speaker": "医生"}, {"sentence": "医生你好", "sentence_id": "2"… | 1 | 0.0% | 0.0% |
