# ASR 转写病史字段判断：逐案例结果

20 个案例，共 37 条测试记录。案例口径：不同公开演绎会话。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。

## 不同来源的表现

| 来源分组 | 案例 | 测试记录 | Jev | DeepSeek |
| --- | ---: | ---: | ---: | ---: |
| 原归档样本 | 3 | 20 | 95.0% | 95.0% |
| PriMock57 新增独立会话片段 | 17 | 17 | 88.2% | 82.4% |

## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| day1_consultation01 | Hello, hi. Hi, I just had some diarrhea for the last three days and it's been affecting me. I need to stay clo… | 12 | 91.7% | 91.7% |
| day1_consultation02 | Hello, can you hear me well? Okay. Yes, so it's been a few days now. I have like your soul and the red skin. I… | 4 | 100.0% | 100.0% |
| day1_consultation03 | Hello. Oh, I just got terrible headaches since midday. On the left side, just making me feel so ill. I just fe… | 4 | 100.0% | 100.0% |
| day1_consultation04 | I've been feeling kind of under the weather for the past four days. It started with the sore throat and runnin… | 1 | 100.0% | 100.0% |
| day1_consultation05 | I'm not going to get to the next one. I'm not going to get to the next one. I'm not going to get to the next o… | 1 | 0.0% | 0.0% |
| day1_consultation06 | Well, I've got heart failure. I was told that a while ago, and I got a bit breathless when I was first diagnos… | 1 | 100.0% | 100.0% |
| day1_consultation07 | Yeah, yeah, mostly dry as a, you know, so we, but in the morning it's a bit worse. But, you know, it's fairly,… | 1 | 100.0% | 100.0% |
| day1_consultation08 | All over my arms and my hands mainly. I know.… | 1 | 100.0% | 100.0% |
| day1_consultation09 | It's not too bad. It's like a stinging kind of pain. It's not like unbearable, but it's definitely bothering m… | 1 | 0.0% | 0.0% |
| day1_consultation10 | Yeah, I think going on for a little bit longer than three days I think actually maybe just under a week. Sorry… | 1 | 100.0% | 100.0% |
| day1_consultation11 | I guess it's been a little while now and I've just been feeling not so great and it's all come from like it's … | 1 | 100.0% | 100.0% |
| day1_consultation12 | Yeah, around 5 to 6 times a day. Yes, it's definitely… | 1 | 100.0% | 100.0% |
| day1_consultation13 | around three days ago, maybe? It's basically like, it kind of feels over my head, but like mainly around my ri… | 1 | 100.0% | 100.0% |
| day1_consultation14 | I've just been super annoying and it's not going away. I think it started like maybe a bit less than a week ag… | 1 | 100.0% | 100.0% |
| day1_consultation15 | not severe is just, you know, I don't hydrate very much so yeah, it's very bad in my hibes. Yeah, I mean, it's… | 1 | 100.0% | 0.0% |
| day2_consultation01 | I occasionally get like a ringing in my left ear just on the one side and there's actually been a few times wh… | 1 | 100.0% | 100.0% |
| day2_consultation02 | I have a weird swelling on my elbow. I noticed that when I was in the shower. It's not painful at all. I feel … | 1 | 100.0% | 100.0% |
| day2_consultation03 | just one five just to my left side and notice that the hearing is kind of gone down a bit yeah so again it's t… | 1 | 100.0% | 100.0% |
| day2_consultation04 | Well, I've got a bit of a slight fever and I've got a bit of blood on two occasions. [BLANK_AUDIO]… | 1 | 100.0% | 100.0% |
| day2_consultation05 | Get up, correct. If I right hand? Yeah.… | 1 | 100.0% | 100.0% |
