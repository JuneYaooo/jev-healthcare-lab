# 参考转写病史字段判断：逐案例结果

20 个案例，共 37 条测试记录。案例口径：不同公开演绎会话。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。

## 不同来源的表现

| 来源分组 | 案例 | 测试记录 | Jev | DeepSeek |
| --- | ---: | ---: | ---: | ---: |
| 原归档样本 | 3 | 20 | 100.0% | 100.0% |
| PriMock57 新增独立会话片段 | 17 | 17 | 100.0% | 100.0% |

## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| day1_consultation01 | Hello, how are you? Oh hey, um, I've just had some diarrhea for the last three days, um, and it's been affecti… | 12 | 100.0% | 100.0% |
| day1_consultation02 | Hello. Can you hear me well? OK. Yes. So, it's been a few days now. I have like a sore, and a red skin. It's k… | 4 | 100.0% | 100.0% |
| day1_consultation03 | Hello. Ohh, I just got a terrible headache since mid-day. Um on the left side. It's just making me feel so ill… | 4 | 100.0% | 100.0% |
| day1_consultation04 | Alright, so I've been feeling, I've been feeling kind of uh under the weather for the past four days. Um it st… | 1 | 100.0% | 100.0% |
| day1_consultation05 | Uh, like below my belly button, it's like quite, sore when I press on it.… | 1 | 100.0% | 100.0% |
| day1_consultation06 | Um, well, I've, I've uh, I've got um, heart failure. Uh, I was told that, uh, a while ago.… | 1 | 100.0% | 100.0% |
| day1_consultation07 | Uh, yeah, yeah, mean, mostly, dry it's a , you know it's a wee bit in the morning it's a bit worse uh, but , a… | 1 | 100.0% | 100.0% |
| day1_consultation08 | All over my arms, um, and my hands mainly. Uh, no. Never had .… | 1 | 100.0% | 100.0% |
| day1_consultation09 | Um, it's, it's not too bad, it's sort of like a stinging kind of pain. Um. It's not like unbearable, but uh, i… | 1 | 100.0% | 100.0% |
| day1_consultation10 | Uh, yeah it's been going on for a little bit longer than three days I think actually, maybe just under a week.… | 1 | 100.0% | 100.0% |
| day1_consultation11 | It's all come from like, uh it's like basically I think it's diarrhoea. And it's like just coming out, like lo… | 1 | 100.0% | 100.0% |
| day1_consultation12 | Yeah, around, five to six times a day.… | 1 | 100.0% | 100.0% |
| day1_consultation13 | Um, it's basically like, it kind of feels all over my head, but like mainly, um, around my right eye. Um… | 1 | 100.0% | 100.0% |
| day1_consultation14 | Uh I think it started like maybe, a bit less than a week ago. Like maybe, maybe five or six days ago.… | 1 | 100.0% | 100.0% |
| day1_consultation15 | Yeah. Like it's very, it's very bad in my hands.… | 1 | 100.0% | 100.0% |
| day2_consultation01 | Um, I occasionally get like a ringing in my left ear, uh just on the one side and um there's actually been a f… | 1 | 100.0% | 100.0% |
| day2_consultation02 | It's not painful at all, or like, I I feel fine. But it's just, just a bit, a bit weird, to see that.… | 1 | 100.0% | 100.0% |
| day2_consultation03 | Just one side, just on my left side, I've noticed that the hearing's kind of gone down a bit.… | 1 | 100.0% | 100.0% |
| day2_consultation04 | Um, well I've had a , I've got a bit of slight fever, um, and, and, uh, well like, I coughed up a bit of blood… | 1 | 100.0% | 100.0% |
| day2_consultation05 | Yeah, that's correct. My right hand. Yes.… | 1 | 100.0% | 100.0% |
