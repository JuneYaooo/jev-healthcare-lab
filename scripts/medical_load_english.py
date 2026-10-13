"""English copy for the medical benchmark README and figures."""
import re

TASK_TITLES = {
    'triage_urgency': 'Triage and urgency assessment',
    'message_urgency_pair': 'Patient message prioritization',
    'examination_choice': 'Diagnostic test selection',
    'clinical_grade': 'Disease staging and severity assessment',
    'diagnosis': 'Case diagnosis selection',
    'tcm_syndrome': 'TCM syndrome classification',
    'case_etiology': 'Case etiology assessment',
    'tcm_pathogenesis_candidate': 'TCM candidate pathogenesis assessment',
    'patient_contraindication': 'Patient-specific contraindication assessment',
    'treatment_choice': 'Treatment selection',
    'medication_choice': 'Medication selection',
    'fluid_plan': 'Fluid therapy selection',
    'pgx_guideline_recommendation': 'Pharmacogenomic guideline recommendation selection',
    'administration_route_choice': 'Administration route and method selection',
    'case_complication': 'Case complication assessment',
    'nursing_priority': 'Nursing intervention selection',
    'nutrition_plan': 'Nutrition and diet selection',
    'positioning_choice': 'Patient positioning selection',
    'monitoring_target': 'Clinical monitoring and treatment response assessment',
    'infection_precaution': 'Infection prevention measures',
    'followup_plan': 'Follow-up testing and timing',
    'rehabilitation_choice': 'Rehabilitation plan selection',
    'prevention_choice': 'Preventive intervention selection',
    'patient_counseling': 'Patient education and communication',
    'trial_referral': 'Clinical trial prescreening and referral',
    'trial_shared_patient': 'Multiple trial referrals for one patient',
    'consent_action': 'Informed consent and privacy decisions',
}

COPY = {
    '从接口设计和本次任务表现看，JEV 很适合高频、结构化、边界明确的决策场景：将上下文转为明确选项上的判断，再由程序组合成筛选、分流或审核流程。它在具体医疗任务上的适用程度，仍需结合各任务的准确率与错误类型判断。': 'JEV’s interface design and the task results here make it well suited to frequent, structured decisions with clearly defined scope: turning context into judgments over explicit options that software can combine into screening, routing, or review workflows. Its suitability for a specific healthcare task still depends on that task’s accuracy and error patterns.',
    '**简体中文** | [English](README.en.md)': '[简体中文](README.md) | **English**',
    '**评估 JEV 在医疗场景中的表现**：围绕分诊、诊断、用药、护理与临床试验筛选等具体任务，考察它的判断准确率、持续吞吐和使用成本，并与 DeepSeek Flash、Qwen 对照。': '**Evaluating JEV in healthcare scenarios**: measure decision accuracy, sustained throughput, and usage cost across triage, diagnosis, medication, nursing, and clinical trial screening, with DeepSeek Flash and Qwen as comparison models.',
    '项目背景与目的': 'Background and purpose',
    'JEV 是 TypeSafe 推出的旗舰模型，官方将其定位为面向软件决策的 System One 模型：输入上下文（state）和类型化问题，直接返回程序可使用的结构化结果。其接口提供 Choice、Score、Noul 三类问题，并支持围绕同一份上下文并行处理多个独立判断。[官方介绍](https://docs.typesafe.ai/introduction)': 'JEV is TypeSafe’s flagship model, described by its developers as a System One model for decisions inside software. It accepts context (state) and typed questions, then returns structured results that code can consume directly. Its API offers Choice, Score, and Noul questions and supports multiple independent judgments over the same context in parallel. [Official introduction](https://docs.typesafe.ai/introduction)',
    '医疗工作流包含许多范围明确的判断，例如识别就医紧急程度、判断方案禁忌、选择下一步检查，以及筛选患者可能适合的临床试验。这些任务为检验 JEV 的结构化决策能力提供了具体场景：输出能否直接被程序读取，以及判断本身是否正确，都需要通过医疗题目验证。': 'Healthcare workflows involve many narrowly scoped judgments: assessing urgency, checking contraindications, choosing the next diagnostic test, or screening trials that may suit a patient. These tasks provide concrete settings for evaluating JEV’s structured decisions. Both machine-readable output and the correctness of the underlying judgment need to be tested on medical questions.',
    '本项目希望回答三个问题：JEV 在哪些医疗任务上表现较好，在哪些任务上仍有短板；多题处理与持续并发时，准确率、吞吐和成本如何取舍；同一患者材料供多个问题共享的处理方式，在医疗筛选任务中表现如何。为此，项目公开固定题集、数据来源、评分方法与原始结果，便于复算和比较。': 'This project asks three questions: which healthcare tasks JEV handles well and where it falls short; how accuracy, throughput, and cost trade off when processing multiple questions under sustained concurrency; and how sharing one patient’s context across multiple questions performs in medical screening. Frozen question sets, data provenance, scoring methods, and raw results are available for reproduction and comparison.',
    '当前评测聚焦有明确选项与标准答案的 Choice 任务；Score、Noul 和置信度校准尚未纳入验证。结果用于研究与原型选型，不构成临床有效性验证。': 'The current evaluation covers Choice tasks with explicit options and reference answers. Score, Noul, and confidence calibration have not been evaluated. Results support research and prototype selection; they do not establish clinical validity.',
    '评测结果': 'Evaluation results',
    '医疗决策准确率、成本与吞吐对比': 'Medical decision accuracy, cost, and throughput',
    '本轮覆盖 26 个既有医疗任务的 1,514 项判断，另加 8 位模拟患者的 64 项试验转介判断。数据包含考试病例、模拟患者与公开标注，尚非临床部署验证。': 'This round covers 1,514 decisions across 26 existing medical tasks, plus 64 trial referral decisions for eight simulated patients. Data include exam cases, simulated patients, and public annotations; this is not a clinical deployment validation.',
    '本轮尚未完成：': 'Incomplete in this round: ',
    '。** 相应成绩留空，当前尚不能完成四模型对比。[既有 JEV／Flash 阶段性测试](results/sustained-throughput-v1/README.md)另行保留。': '.** Results are left blank, so a complete four-model comparison is not yet available. [Earlier JEV/Flash tests](results/sustained-throughput-v1/README.md) remain available.',
    '完整题集已完成的模型：': 'Models that completed the full question set: ',
    '三项任务体现出不同取舍（完整速度、成本及 Qwen 对比见表 1）：': 'Three tasks illustrate different tradeoffs (see Table 1 for full throughput, cost, and Qwen comparisons):',
    '准确率按模型原样输出计分，非法选项也算错；它同时反映判断与输出可用性。吞吐表示每秒收到的合法判断数，**不等于每秒正确判断数**。成本按新病例、无缓存折扣的输入与输出用量折算，单位为人民币；Flash 区间对应闲时与高峰标价。': 'Accuracy is scored from unmodified model outputs, with invalid options counted as errors; it reflects both judgment and output usability. Throughput counts valid decisions received per second, **not correct decisions per second**. Cost is estimated in CNY from input and output usage for fresh cases without cache discounts; Flash ranges reflect off-peak and peak list prices.',
    '**测试账户限制：本次测试受账户额度、请求限流及共享服务条件影响，部分性能指标可能无法充分反映模型能力，尤其是响应速度和吞吐量。** 表中数值是当前测试条件下的观测结果，不代表模型的性能上限，模型间的速度差距也不能直接外推到其他部署条件。Qwen 本次账户上限分别为 8 万／4 万 token 每分钟；网络与供应商缓存也会影响结果。': '**Test account limitations: account quotas, request rate limits, and shared service conditions may prevent some performance metrics—especially response speed and throughput—from fully reflecting model capabilities.** The values shown are observations under the tested conditions, not model performance ceilings; speed differences between models should not be extrapolated directly to other deployment conditions. The two Qwen accounts were limited to 80,000 and 40,000 tokens per minute, respectively. Network conditions and provider caching also affect results.',
    '**表 1｜医疗任务总览。准确率与成本来自完整题集的 8 并发多题测试；吞吐取预先指定的 32 并发档、两轮持续负载结果。点击任务进入详细结果。**': '**Table 1 | Healthcare task overview. Accuracy and cost use the full question set at concurrency 8; throughput uses two sustained-load rounds at the prespecified concurrency of 32. Select a task for details.**',
    '粗体表示同一任务、同一并发档内已测模型的最优观测值，并列最优均加粗；不表示统计显著性。成本区间重叠、无法确定最低者时不加粗。': 'Bold indicates the best observed value among tested models for the same task and concurrency, including ties; it does not imply statistical significance. Overlapping cost intervals are not highlighted when the cheapest model cannot be determined.',
    '“—”表示本轮未获得完整数据或样本不足。独立题量指不重复的判断项，不表示统计独立，也不等于独立患者数；患者／来源组数见每个任务表题。少于 20 题仅作探索性比较。三个空任务（剂量适宜性、危急值升级、就诊科室分流）暂不计分。': '“—” denotes incomplete data or insufficient samples. Unique decisions are deduplicated items, not statistically independent observations or unique patients; patient/source group counts appear in each task caption. Tasks with fewer than 20 items are exploratory. Three empty tasks (dose appropriateness, critical-value escalation, and department routing) are not scored.',
    '样本覆盖有限，只作探索性比较，尤其不能据此稳定估计临床可靠性。': 'Limited sample coverage makes this an exploratory comparison; it cannot provide a robust estimate of clinical reliability.',
    '8 位模拟患者各对应 8 项真实注册试验。患者材料放在共享 state 中，只传一次；每个问题对应一项候选试验。金标为上游的“不相关／可能适合／很可能适合转介”，不是逐条入排标准的专家判定。与原试验转介题集可能重合，不另计入总体图。': 'Each of eight simulated patients is paired with eight registered trials. Patient context is sent once in a shared state, with one question per candidate trial. Reference labels are the upstream categories “irrelevant / potentially suitable / likely suitable for referral,” not expert assessments of individual eligibility criteria. This panel may overlap with the original trial referral set and is excluded from the overview chart.',
    '三类金标分别为 49、9、6 项；全部回答“不相关”的多数类基线为准确率 76.56%、Macro-F1 28.91%。因此需结合 Macro-F1 判断模型是否识别了较少见的适合转介案例，不能仅看准确率。': 'The three reference classes contain 49, 9, and 6 items. Always predicting “irrelevant” yields 76.56% accuracy and 28.91% Macro-F1. Read accuracy alongside Macro-F1 to assess whether a model identifies the less common suitable referral cases.',
    'Macro-F1 对本任务金标中出现的类别等权平均；没有金标样本的候选类别不另加零分项，各模型使用相同类别集合。': 'Macro-F1 equally weights classes present in this task’s reference labels. Candidate classes without reference examples do not receive additional zero-score entries; all models use the same class set.',
    '这是候选病机的判断任务，按既有标注计分；不能由此推导自由生成辨证与处方的能力。': 'This task scores judgments about candidate TCM pathogenesis against existing annotations; it does not establish the ability to generate syndrome analyses or prescriptions freely.',
    '本任务严格区分原始选项键，例如 `Patient #1` 不能改写成 `Patient_1`。这类输出合约错误也按错计，因此成绩同时反映判断和接口可直接使用的程度，不能全部归因于医学推理差异。': 'Original option keys must match exactly: for example, `Patient #1` cannot be rewritten as `Patient_1`. Such output-contract errors count as incorrect, so scores reflect both judgment and direct API usability, not solely differences in medical reasoning.',
    '配置并发是工作器上限；实际在途请求可能因账户额度更少。P95 不含客户端额度等待；不足 20 个完整响应时不报告 P95。': 'Configured concurrency is a worker limit; account quotas may reduce requests in flight. P95 excludes client-side quota waiting and is omitted when fewer than 20 complete responses are available.',
    '查看本任务的两个并发档': 'View both concurrency settings',
    '医疗场景': 'Healthcare scenario', '具体任务': 'Task', '独立题量': 'Unique decisions',
    '模型': 'Model', '准确率 (%) ↑': 'Accuracy (%) ↑', '吞吐量 (判断/秒) ↑': 'Throughput (decisions/s) ↑',
    '成本 (元/千项判断) ↓': 'Cost (CNY/1,000 decisions) ↓', '完整响应 P95 (秒) ↓': 'Full-response P95 (s) ↓',
    '配置并发': 'Configured concurrency', '实际平均同时请求数': 'Mean requests in flight',
    '接诊与分诊': 'Intake and triage', '检查与检验': 'Examinations and tests', '诊断与鉴别': 'Diagnosis and differential diagnosis',
    '治疗与用药': 'Treatment and medication', '住院与护理': 'Inpatient care and nursing', '出院与随访': 'Discharge and follow-up',
    '临床试验筛选': 'Clinical trial screening', '病历与医疗质量控制': 'Medical records and quality assurance',
    '评估方法与适用边界': 'Methods and scope', '数据集与许可': 'Datasets and licenses', '原始响应与复算': 'Raw responses and reproduction',
    '任务定义与数据': 'Task definition and data', '评估方法': 'Evaluation methods', '原始记录与计价依据': 'Raw records and pricing',
    '的并发吞吐对比': ': throughput by concurrency',
}


def translate(text, report):
    # Replace complete copy before shorter labels so shared terms stay intact.
    mapping = {**COPY, **{f['title']: TASK_TITLES[fid] for fid, f in report['families'].items()}}
    text = re.sub(r'\*\*表 (\d+)｜(.+?)：(\d+) 项独立判断，(\d+) 个来源组；每请求最多 (\d+) 项。准确率测试配置 8 并发，负载测试配置 32 并发。\*\*',
                  r'**Table \1 | \2: \3 unique decisions from \4 source groups; up to \5 decisions per request. Accuracy uses concurrency 8; load testing uses concurrency 32.**', text)
    text = re.sub(r'\*\*表 (\d+)a｜(.+?)：每请求最多 (\d+) 项，负载题集 (\d+) 项，各档两轮。\*\*',
                  r'**Table \1a | \2: up to \3 decisions per request, \4 load-test decisions, two rounds per setting.**', text)
    text = re.sub(r'准确率和成本来自完整的 (\d+) 项固定题集；吞吐与 P95 来自其中预先选定的 (\d+) 项判断，持续循环施压两轮。重复调用不增加独立题量。P95 从实际发出计时，不含额度排队；不足 20 个响应时留空。',
                  r'Accuracy and cost use all \1 fixed decisions. Throughput and P95 use a prespecified subset of \2 decisions, repeated over two sustained-load rounds. Repeated calls do not increase the unique sample count. P95 starts at HTTP dispatch, excludes quota waiting, and is omitted below 20 responses.', text)
    text = re.sub(r'：JEV 准确率 ([\d.]+)%，Flash 为 ([\d.]+)%；本次 JEV 的 32 并发吞吐(更高|更低|相同)。',
                  lambda m: f': JEV accuracy is {m[1]}% versus {m[2]}% for Flash; JEV throughput at concurrency 32 is ' + {'更高':'higher', '更低':'lower', '相同':'the same'}[m[3]] + ' in this run.', text)
    for source in sorted(mapping, key=len, reverse=True):
        text = text.replace(source, mapping[source])
    text = re.sub(r'(Models that completed the full question set: [^\n]+)。', lambda m: m[1].replace('、', ', ') + '.', text)
    text = re.sub(r'(Incomplete in this round: [^\n]+?)\.\*\*', lambda m: m[1].replace('、', ', ') + '.**', text)
    remaining = re.findall(r'[^\n]*[\u4e00-\u9fff][^\n]*', text.replace('[简体中文](README.md)', ''))
    if remaining:
        raise ValueError('Missing English README translations: ' + '\n'.join(remaining))
    return text


def render(report, chinese):
    text = translate(chinese, report)
    directory = 'docs/assets/' + report.get('gateway', {}).get('archive', 'results/medical-load-v2').split('/')[-1]
    text = text.replace(f'{directory}/overview.png', f'{directory}/en/overview.png')
    for fid in report['families']:
        text = text.replace(f'{directory}/{fid}.svg', f'{directory}/en/{fid}.svg')
    return text


def chart_text(text, report):
    labels = {
        **{f['title']: TASK_TITLES[fid] for fid, f in report['families'].items()},
        '点：两轮合并吞吐；竖线：两轮范围': 'Points: pooled throughput; bars: range across two rounds',
        '配置并发（账户额度可能限制实际并发）': 'Configured concurrency (subject to account quotas)',
        '吞吐量（判断/秒）': 'Throughput (decisions/s)',
        '任务平均准确率（%）↑': 'Mean task accuracy (%) ↑',
        '每千项判断成本（元）↓\nFlash 横线：闲时至高峰标价': 'Cost (CNY/1,000 decisions) ↓\nFlash line: off-peak to peak prices',
        '等任务量吞吐（判断/秒）↑\n32 配置并发，受平台与账户额度影响\n未形成完整可汇总数据的模型不绘制': 'Equal-task throughput (decisions/s) ↑\nConcurrency 32; platform and account limits apply\nModels with incomplete aggregate data omitted',
        '医疗多项决策：质量 × 成本 × 吞吐': 'Medical decisions: accuracy × cost × throughput',
        '完整结果尚未齐备': 'Complete results not yet available',
        ' / 千项': ' / 1,000', ' 判断/秒': ' decisions/s',
    }
    for source in sorted(labels, key=len, reverse=True):
        text = text.replace(source, labels[source])
    text = re.sub(r'（负载题集 (\d+) 项）', r' (\1 load-test decisions)', text)
    text = re.sub(r'(\d+) 个至少 20 题的既有任务；两轮持续负载', r'\1 existing tasks with at least 20 items; two sustained-load rounds', text)
    if re.search(r'[\u4e00-\u9fff]', text):
        raise ValueError('Missing English chart translation: ' + text)
    return text
