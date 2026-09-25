# 公共卫生核查：仅论断：逐案例结果

100 个案例，共 100 条测试记录。案例口径：来源分组中的不同病例、文档或题目；不等于患者数。同一案例内的多条记录不重复算案例。

下表列出每个案例的输入片段和两家模型成绩。完整输入、问题、原始答案及样本 ID 见 [samples.jsonl](samples.jsonl)，响应见 [Jev](responses.jsonl) 和 [DeepSeek](comparison/deepseek_responses.jsonl)。F1 综合考虑选对、漏选和误选，满分 100。


## 案例明细

| 案例 ID | 输入片段 | 测试记录 | Jev | DeepSeek |
| --- | --- | ---: | ---: | ---: |
| 25662 | {"claim": "Steve Scalise Says Ady Barkan asked Joe Biden, “Do we agree that we can redirect some of the fundin… | 1 | 0.0% | 0.0% |
| 9093 | {"claim": "Small increases in physical activity reduce immobility, disability risks in older adults", "publica… | 1 | 0.0% | 0.0% |
| 26263 | {"claim": "Facebook post Says a warning label on a box of disposable masks shows that they are ineffective at … | 1 | 100.0% | 100.0% |
| 8380 | {"claim": "Airlines rush to boost demand as coronavirus shreds playbook for crisis management.", "publication_… | 1 | 0.0% | 100.0% |
| 27477 | {"claim": "Black and white caterpillars can cause severe allergic reactions in some people who touch them.", "… | 1 | 0.0% | 100.0% |
| 10229 | {"claim": "Lung Cancer Breath ‘Signature’ Presents Promise for Earlier Diagnosis", "publication_date": "June 1… | 1 | 0.0% | 0.0% |
| 9034 | {"claim": "FDA authorizes marketing of first blood test to aid in the evaluation of concussion in adults", "pu… | 1 | 0.0% | 0.0% |
| 2894 | {"claim": "China reports one more H7N9 bird flu death.", "publication_date": "January 10, 2014"}… | 1 | 0.0% | 100.0% |
| 8665 | {"claim": "Thailand reports new coronavirus death as total cases reach 1,245.", "publication_date": "March 28,… | 1 | 0.0% | 100.0% |
| 38078 | {"claim": " Pope Francis bestowed the Pontifical Medal upon Lilianne Ploumen, a Dutch pro-abortion activist. "… | 1 | 0.0% | 0.0% |
| 3854 | {"claim": "3 Nebraska Medicaid providers honored for serving patients.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 24588 | {"claim": "Preventive care does not save the government money.", "publication_date": "August 17, 2009"}… | 1 | 0.0% | 100.0% |
| 1592 | {"claim": "Brazil's mothers left to raise microcephaly babies alone.", "publication_date": "March 11, 2016"}… | 1 | 0.0% | 100.0% |
| 2396 | {"claim": "Lose weight with skin cream? Fat chance, says U.S. govt.", "publication_date": "January 7, 2014"}… | 1 | 100.0% | 100.0% |
| 35599 | {"claim": "In July 2020, U.S. Education Secretary Betsy DeVos said \"only\" .02% of the country's K-12 school … | 1 | 100.0% | 0.0% |
| 31320 | {"claim": "Covfefe\" means something, anything.", "publication_date": "June 2, 2017"}… | 1 | 100.0% | 0.0% |
| 21840 | {"claim": "For every dollar we invest in Head Start, we get $5 to $7 back into our economy.", "publication_dat… | 1 | 0.0% | 0.0% |
| 17064 | {"claim": "A lot of the problems with forest fires ... is because of bad policy (not to clear out the forests)… | 1 | 0.0% | 0.0% |
| 34562 | {"claim": "The new supplement InteliGEN can boost brain function.", "publication_date": "September 30, 2016"}… | 1 | 100.0% | 100.0% |
| 16065 | {"claim": "We've caught Iran cheating on the interim (nuclear) deal.", "publication_date": "December 31, 2014"… | 1 | 0.0% | 0.0% |
| 3295 | {"claim": "Christmas miracle for Florida dog whose heart stopped.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 41932 | {"claim": "Obama Administration legalized bump stocks.", "publication_date": "April 3, 2018"}… | 1 | 0.0% | 0.0% |
| 23278 | {"claim": "The Chilean \"privatization scheme\" that Sharron Angle supports \"has resulted in hidden fees, few… | 1 | 0.0% | 0.0% |
| 3927 | {"claim": "Chicago’s mayor says top cop drinking before incident in car.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 23913 | {"claim": "Two-thirds of the top-rated hospitals in Florida were our hospitals.", "publication_date": "June 4,… | 1 | 0.0% | 0.0% |
| 11485 | {"claim": "New Portable Scanner for Breast Cancer", "publication_date": "October 28, 2010"}… | 1 | 0.0% | 0.0% |
| 5777 | {"claim": "Nebraska Sen. Bolz to run for 1st Congressional District.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 3744 | {"claim": "US regulators OK updated version of decades-old antibiotic.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 27974 | {"claim": "An anti-seat belt law advocate was killed in automobile accident.", "publication_date": "June 12, 2… | 1 | 0.0% | 100.0% |
| 37855 | {"claim": "United States President Donald Trump tweeted \"\"it is unbelievable that President Obama criticized… | 1 | 0.0% | 0.0% |
| 23732 | {"claim": "Under President George W. Bush, the U.S. had \"52 months of ... uninterrupted job creation\" and \"… | 1 | 0.0% | 0.0% |
| 8912 | {"claim": "'What choice do I have?' Lock-down strands millions in China's Wuhan.", "publication_date": "Januar… | 1 | 100.0% | 100.0% |
| 33361 | {"claim": "HIV-positive basketball star Earvin \"Magic\" Johnson donated blood to patients with leukemia. ", "… | 1 | 100.0% | 100.0% |
| 6014 | {"claim": "NFL suspends Patriots’ Gordon for substance abuse violation.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 7832 | {"claim": "Fitness experts separate folklore from fact.", "publication_date": "March 4, 2013"}… | 1 | 0.0% | 0.0% |
| 16799 | {"claim": "Expanding Medicaid would create 63k jobs.", "publication_date": "July 9, 2014"}… | 1 | 0.0% | 0.0% |
| 7357 | {"claim": "Democrats push new $3T coronavirus relief bill through House.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 4927 | {"claim": "Utah bans abortions after 18 weeks, teeing up legal showdown.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 36264 | {"claim": "An image shows reported cases of \"flesh eating bacteria\" in 2019.", "publication_date": "August 8… | 1 | 0.0% | 0.0% |
| 3995 | {"claim": "Chronic wasting disease found in buck on Winona County farm.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 12523 | {"claim": "In the House Republican health care bill, \"we’re expanding women’s access to health services by re… | 1 | 0.0% | 0.0% |
| 22819 | {"claim": "House Speaker Dean Cannon says that freshmen lawmakers account for one-third of the 120-member Hous… | 1 | 0.0% | 100.0% |
| 28726 | {"claim": "Donald Trump raped his former wife and a young woman, and his modeling agency was found to be traff… | 1 | 0.0% | 0.0% |
| 41819 | {"claim": "Three border agents in San Diego \"were very badly hurt through getting hit with rocks and stones.”… | 1 | 100.0% | 0.0% |
| 25301 | {"claim": "In the Illinois Legislature, Barack Obama \"voted 'present,' instead of yes or no\" on seven votes … | 1 | 0.0% | 100.0% |
| 11043 | {"claim": "Statin Drugs May Cut Risk of Kidney Trouble After Surgery", "publication_date": "April 14, 2011"}… | 1 | 0.0% | 0.0% |
| 15085 | {"claim": "HIV/AIDS among women is skyrocketing in Austin.", "publication_date": "October 2, 2015"}… | 1 | 0.0% | 0.0% |
| 30280 | {"claim": "The University of Louisville Hospital confirmed the deaths of 16 people from a rare strain of the \… | 1 | 100.0% | 100.0% |
| 24592 | {"claim": "I just want to assure [you] we're not talking about cutting Medicare benefits.", "publication_date"… | 1 | 0.0% | 0.0% |
| 1532 | {"claim": "Hate daylight saving time? You may have a point, researchers say.", "publication_date": "March 11, … | 1 | 0.0% | 100.0% |
| 1245 | {"claim": "Britain to complete plan next year to reach net zero transport emissions.", "publication_date": "Oc… | 1 | 0.0% | 0.0% |
| 18510 | {"claim": "In 2010 alone, 1,270 infants were reported to have died following attempted abortions and notably t… | 1 | 0.0% | 0.0% |
| 9653 | {"claim": "Tracking the risks and rewards of transcranial magnetic stimulation", "publication_date": "April 21… | 1 | 0.0% | 0.0% |
| 4047 | {"claim": "Survey finds many ticks carry disease in North Dakota.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 4768 | {"claim": "Tumor-free flounder: Study underscores Boston Harbor rebirth.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 3339 | {"claim": "Idaho officials say cat has rabies, first case in decades.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 27274 | {"claim": "Arizona State Senate candidate Bobby Wilson fatally shot his mother in 1963.", "publication_date": … | 1 | 0.0% | 0.0% |
| 10041 | {"claim": "Estrogen Lowers Breast Cancer and Heart Attack Risk in Some", "publication_date": "April 5, 2011"}… | 1 | 0.0% | 0.0% |
| 625 | {"claim": "Trading tires: How the West fuels a waste crisis in Asia.", "publication_date": "March 17, 2015"}… | 1 | 0.0% | 0.0% |
| 35674 | {"claim": "A video shows a piece of 5G equipment with \"COV-19\" inscribed on it. ", "publication_date": "May … | 1 | 0.0% | 100.0% |
| 10711 | {"claim": "Millions face risk from drug-coated stents", "publication_date": "November 28, 2006"}… | 1 | 0.0% | 0.0% |
| 13894 | {"claim": "African-Americans don't use drugs at a higher level than whites but \"wind up going to prison six t… | 1 | 0.0% | 100.0% |
| 9692 | {"claim": "Cortisol levels in children's hair may reveal future mental health risk", "publication_date": "Janu… | 1 | 0.0% | 0.0% |
| 9303 | {"claim": "The Baseball Diet Is Proving To Be A Heavy Favorite For Shedding Pounds In 2015", "publication_date… | 1 | 0.0% | 0.0% |
| 13565 | {"claim": "Mike Pence Says Hillary Clinton \"wants to increase Syrian refugees to this country by 550 percent.… | 1 | 0.0% | 100.0% |
| 10983 | {"claim": "Report: 20-somethings can go 2 years between Paps", "publication_date": "November 20, 2009"}… | 1 | 100.0% | 100.0% |
| 22480 | {"claim": "Phyllis Schlafly Says broken compact fluorescent light bulbs \"allegedly cause migraines and epilep… | 1 | 0.0% | 0.0% |
| 28438 | {"claim": "People who undergo amputations can sign paperwork allowing them to take the removed limbs home afte… | 1 | 0.0% | 0.0% |
| 10173 | {"claim": "An implant that hits a nerve", "publication_date": "December 2, 2008"}… | 1 | 0.0% | 0.0% |
| 36020 | {"claim": "South Dakota launched a campaign against methamphetamine addiction with the tagline \"Meth. We're O… | 1 | 0.0% | 100.0% |
| 14799 | {"claim": "Since 2004, more than 2,000 suspected terrorists have legally purchased weapons in the United State… | 1 | 0.0% | 100.0% |
| 24475 | {"claim": "The Baucus health care bill \"could be used to ban guns in home self-defense.", "publication_date":… | 1 | 100.0% | 100.0% |
| 39802 | {"claim": " A polio vaccination campaign headed by the Bill and Melinda Gates Foundation in India led to 47,50… | 1 | 100.0% | 100.0% |
| 25742 | {"claim": "A photo shows Kamala Harris is “listed as Caucasian on her birth certificate.”", "publication_date"… | 1 | 100.0% | 100.0% |
| 36851 | {"claim": " Hillary Clinton was forced to cancel a campaign event after a video showed her making lizard-like … | 1 | 100.0% | 100.0% |
| 33267 | {"claim": "Canine Carry Outs dog treats contain anti-freeze and are therefore dangerous to dogs.", "publicatio… | 1 | 100.0% | 100.0% |
| 4810 | {"claim": "Chicago receives $6.7M to help people living with HIV/AIDS.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 6165 | {"claim": "Philippines to cull 200,000 fowl after bird flu outbreak.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 4039 | {"claim": "Proposal for Lyme prevention included in appropriations deal.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 9316 | {"claim": "Five-minute neck scan can spot dementia 10 years earlier, say scientists", "publication_date": "Nov… | 1 | 0.0% | 0.0% |
| 4925 | {"claim": "Utah governor criticizes federal marijuana reform inaction.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 18217 | {"claim": "As a student at Occidental College in Los Angeles from 1979 to 1981, \"there were days where folks … | 1 | 0.0% | 100.0% |
| 26382 | {"claim": "The existence of a canine coronavirus vaccine casts doubt on statements that there isn’t one for hu… | 1 | 100.0% | 0.0% |
| 13872 | {"claim": "Illegal tobacco sales, price driven too high, has been connected to at least several cases of fundi… | 1 | 0.0% | 0.0% |
| 28777 | {"claim": "During a radio interview, Rosie O'Donnell said, \"I'd like to take my period blood and smear it all… | 1 | 0.0% | 0.0% |
| 40590 | {"claim": " It’s common around Christmas time for people to warn one another about the alleged toxicity of poi… | 1 | 0.0% | 0.0% |
| 5780 | {"claim": "Massachusetts lawmakers weigh ‘Medicare for all’ bill.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
| 40946 | {"claim": "Italy has concluded Covid-19 is not a virus, and people are actually dying of amplified global 5G e… | 1 | 100.0% | 100.0% |
| 2045 | {"claim": "Baby illness can be scanned in mother's blood: study.", "publication_date": "December 9, 2010"}… | 1 | 0.0% | 100.0% |
| 10794 | {"claim": "Stem cells reverse blindness caused by burns", "publication_date": "June 23, 2010"}… | 1 | 0.0% | 0.0% |
| 9298 | {"claim": "Metformin may lower lung cancer risk in diabetic nonsmokers", "publication_date": "April 30, 2015"}… | 1 | 0.0% | 0.0% |
| 2530 | {"claim": "Swiss police arrest \"healer\" accused of infecting 16 with HIV.", "publication_date": "March 15, 2… | 1 | 0.0% | 100.0% |
| 14779 | {"claim": "Hillary Clinton Says Bernie Sanders \"voted for regime change with respect to Libya.", "publication… | 1 | 100.0% | 100.0% |
| 6637 | {"claim": "Recall: Nearly 57 tons of ground beef for possible E coli.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 4797 | {"claim": "US senators ask federal government to address youth vaping.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 26027 | {"claim": "“Four kids who took the coronavirus vaccine died immediately.”", "publication_date": "July 1, 2020"… | 1 | 100.0% | 100.0% |
| 10720 | {"claim": "Colonoscopies Miss Many Cancers, Study Finds", "publication_date": "December 15, 2008"}… | 1 | 0.0% | 100.0% |
| 33675 | {"claim": "Muslim girls buried alive by their father are fed and comforted by Jesus until rescuers come for th… | 1 | 100.0% | 0.0% |
| 4062 | {"claim": "Ohio officials say tick-borne Lyme Disease still a threat.", "publication_date": ""}… | 1 | 0.0% | 100.0% |
| 4035 | {"claim": "2007 mass shooting survivor copes with 300 pellets of lead.", "publication_date": ""}… | 1 | 0.0% | 0.0% |
