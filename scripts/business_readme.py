"""Render the research overview and full task comparison from archived evidence."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text())


def score(q):return q.get('accuracy',q.get('micro_f1'))
def display(q):
    if not q:return '待完成'
    return f'{score(q)*100:.1f}'+('% 正确率' if 'accuracy' in q else ' 分·抽取综合分')
def money(v):return f'${v:.3f}'

def research_extensions():
    """Preserve the explicitly maintained extension block during report rebuilds."""
    path = ROOT / 'README.md'
    content = path.read_text() if path.exists() else ''
    start, end = '<!-- research-extensions:start -->', '<!-- research-extensions:end -->'
    if start not in content and end not in content:
        return []
    if content.count(start) != 1 or content.count(end) != 1 or content.index(start) > content.index(end):
        raise ValueError('README research extension markers must form one ordered pair')
    block = content[content.index(start) + len(start):content.index(end)].strip()
    return ['### 研究扩展', '', start, '', block, '', end, '']


# Illustrative examples selected after analysis, including favorable and unfavorable results.
RESULT_EXAMPLES = [
    ('imcs_entity_type_oracle_span', '给定实体的类型分类'),
    ('aci_note_section', '已分段病历章节分类'),
    ('longhealth_full_context', '长病历选择题问答'),
    ('medec_error_detection', '医疗文本错误检出'),
    ('trialgpt_sigir_referral', '患者与试验入组预筛'),
    ('medcalc_verified_bounded_score', '五种量表闭集评分'),
]

DOMAIN_EXAMPLES = {
    'service': '咨询意图、科室推荐、规则分诊',
    'records': '实体、断言、术语、章节、长病历问答与质控',
    'reports': '检验值关联、单位等价、报告文本断言',
    'medication': '药物关系、用药变更、出院带药与用药选择题',
    'clinical': '诊断、检查与治疗选择题、临床计算、医学及中医知识',
    'followup': '随访行动识别',
    'research': 'PICO、研究证据、患者入组与公共卫生论断核查',
    'governance': '编码证据、隐私候选、幻觉、请求安全与伦理',
}


def render():
    comparison = load('comparisons/deepseek-flash/summary.json')
    if not comparison['summary']['complete']:
        raise ValueError('Do not publish an incomplete comparison as final')
    audit = load('results/evidence_audit.json')['tasks']
    taxonomy = load('results/task_taxonomy.json')
    families = {f['id']: f for f in taxonomy['families']}
    counts = Counter(families[r['family']]['domain'] for r in taxonomy['benchmark_tasks'].values())
    scenes = load('results/scenario_manifest.json')['scenes']
    owner = {t: s['id'] for s in scenes for t in s['task_ids']}
    total = comparison['summary']['planned_rows']
    n_tasks = len(taxonomy['benchmark_tasks'])
    public_tasks = sum(not t.startswith('challenge_') for t in taxonomy['benchmark_tasks'])
    j, d = (comparison['summary'][provider] for provider in ('jev', 'deepseek'))
    timing = {provider: load(f'comparisons/batch-time/{provider}/summary.json') for provider in ('jev', 'deepseek')}
    replay_total = timing['jev']['rows']
    if replay_total != timing['deepseek']['rows']:
        raise ValueError('Timing comparison uses different cohorts')
    long_case = audit['longhealth_full_context']['case_all_correct']['jev']
    harmful = audit['medsafety_request_gate']['safety_events']['harmful_allowed']['jev']
    missed = audit['medec_error_detection']['safety_events']['error_missed']['jev']
    out = [
        '# Jev Healthcare Lab', '',
        '**医疗文本结构化判断的回顾性评测：任务表现、错误分析与调用成本**', '',
        '[任务目录](docs/医疗任务总目录.md) · [完整结果](docs/任务对比.md) · [评测方法](docs/EVALUATION.md) · [复现说明](docs/REPRODUCING.md)', '',
        '## 研究概述', '',
        '本项目研究 Jev 在医疗文本分类、候选筛选与证据判断中的表现，并与接收相同材料和问题的 DeepSeek Flash 比较。研究使用公开评测材料、人工边界题及归档 API 响应，属于离线探索性评测。', '',
        f'主分析包含 **{n_tasks} 个任务条件、{total:,} 条输入**。结果显示，表现取决于任务及输入条件：给定实体或章节边界的分类任务得分较高，完整抽取、入组预筛和数值评分仍有明显错误。现有证据支持进一步验证具体组件，尚未证明完整诊疗流程的可靠性或患者获益。', '',
        '## 任务范围', '',
        f'任务按 {len(taxonomy["domains"])} 个业务领域浏览；每个评测条件只计入一个主要领域。下表只描述已有实验，完整任务定义、未测能力和覆盖边界见[医疗任务总目录](docs/医疗任务总目录.md)。', '',
        '| 业务领域 | 已测内容示例 | 任务条件数 |',
        '| --- | --- | ---: |',
    ]
    for domain, title in taxonomy['domains'].items():
        out.append(f'| [{title}](docs/医疗任务总目录.md#{domain}) | {DOMAIN_EXAMPLES[domain]} | {counts[domain]} |')
    out += [
        '',
        f'{public_tasks} 项条件来自公开材料适配，{n_tasks-public_tasks} 项为自编边界挑战。有无证据、语言、选择题形式及 OCR／ASR 转写条件可分别计数，因此 **{n_tasks} 项不等于 {n_tasks} 种独立医疗工作，{total:,} 条输入也不等于独立患者数**。中医是专业标签；OCR／ASR 是输入链路，均不单列为业务领域。', '',
        '## 研究设计', '',
        '- **模型与对照**：Jev 使用 `jev-1.13.0` 的历史响应；对照请求模型为 `deepseek-flash`，归档配置记为 DeepSeek V4.1 Flash，关闭思考模式、temperature=0。两者接收相同材料与判断目标，通过各自接口输出答案；效果评测不是同期测速。',
        '- **分析单位与指标**：单选判断报告准确率，集合抽取报告 micro-F1，不合并成一个“医疗总分”。同一来源病例或文档的多个字段按来源聚合；另报告病例全部正确率及错误方向。',
        '- **统计与失败处理**：配对区间按来源案例重采样 2,000 次，报告探索性 95% 区间，未校正多重比较。失败记录保留在分母中；43 条无实体候选记录按规则输出空集，未调用 API，仍参与评分。', '',
        '具体抽样、任务适配、提示词、评分及来源见各任务方法页；统计定义见[评测方法](docs/EVALUATION.md)，模型配置与输出适配见[同题对比方法](comparisons/deepseek-flash/README.md)。', '',
        '## 主要结果', '',
        '下表为分析后选取的示例，包含不同表现方向，用于说明输入条件与任务差异；不作为预先指定的主要终点或总体能力排名。全部任务见[完整结果](docs/任务对比.md)。', '',
        '| 评测条件 | 输入数／来源案例数 | Jev 准确率 | DeepSeek 准确率 | 差值［95% 区间］ |',
        '| --- | ---: | ---: | ---: | ---: |',
    ]
    for task, label in RESULT_EXAMPLES:
        r = audit[task]
        pair = r['paired']
        ci = pair['ci95']['difference']
        out.append(f'| [{label}](scenarios/{owner[task]}/{task}/README.md) | {r["records"]}／{r["cases"]} | {pair["jev"]:.1%} | {pair["deepseek"]:.1%} | {pair["difference"]*100:+.1f} ［{ci["lower"]*100:.1f}, {ci["upper"]*100:.1f}］ |')
    out += [
        '',
        '差值为 Jev 减 DeepSeek，单位为百分点。来源案例可能是患者材料、文档或题目；不同任务的来源案例数不能直接相加。区间跨零时，当前样本不能清楚区分两者。', '',
        f'**错误与风险。** 长病历问答中，Jev 有 {long_case["correct"]}/{long_case["total"]} 个来源病例的题目全部答对；请求安全筛查漏过 {harmful["events"]}/{harmful["eligible"]} 条有害请求，医疗错误检出漏掉 {missed["events"]}/{missed["eligible"]} 条错误文本。这些是按数据标签统计的事件，尚未经过医生严重度仲裁。逐类错误、置信度与人工复核量见[证据审计](docs/医疗适用性审计.md)。', '',
        f'**成本与耗时。** 主效果评测每千条输入的费用估算为 Jev {money(j["cost_per_1000_usd"])}、DeepSeek {money(d["cost_per_1000_usd"])}；独立的 {replay_total:,} 条重复输入测速中分别为 {money(timing["jev"]["cost_usd"]/replay_total*1000)}、{money(timing["deepseek"]["cost_usd"]/replay_total*1000)}，8 并发整批耗时分别为 {timing["jev"]["batch_elapsed_s"]/60:.1f}、{timing["deepseek"]["batch_elapsed_s"]/60:.1f} 分钟。费用按归档费率估算，仅含可核验模型调用；缓存、重试和队列条件影响结果。详见[独立测速](comparisons/batch-time/README.md)。', '',
        '另有 [140 份新材料的逐项／合并处理对照](comparisons/paired-suite/README.md)，包含 1,400 个不同判断；该实验与主分析、15 组扰动实验分别报告，不重复累计为独立病例。', '',
        '## 局限性', '',
        '- **代表性**：公开材料、自编题、合成病例和给定候选占有较大比重；闭源模型的预训练接触情况未知，尚缺跨机构、专科和人群的充分验证。',
        '- **任务边界**：给定实体分类不能替代完整病历抽取；选择题不能替代临床决策；转写后文本成绩不能证明原生读图或音频理解能力。',
        '- **证据强度**：结果为历史样本上的探索性分析；没有前瞻性医院试验、独立医生全量审核或真实工时和患者结局评估。高置信度不等于低临床风险。', '',
        '## 快速复现', '',
        '以下步骤核验已归档的数据与评分，不调用模型 API。需要 Git 和 Python 3.10+；这些命令仅使用 Python 标准库，无需 GPU、API 密钥或额外安装包。', '',
        '```sh',
        'git clone https://github.com/JuneYaooo/jev-healthcare-lab.git',
        'cd jev-healthcare-lab',
        'python3 scripts/build_task_catalog.py --check',
        'python3 scripts/verify_experiments.py',
        '```', '',
        '目录检查核对任务映射与生成页面；归档检查核验输入／响应哈希并重新计算指标。预期得到 96 个主任务、7,133 条主记录、300 条扰动记录，主指标与扰动指标均为 `all matched`。', '',
        '完整核验、测试、环境记录和 API 重跑说明见[复现文档](docs/REPRODUCING.md)。重新调用服务需要相应账户与凭据，可能产生费用；服务版本变化也可能改变结果。', '',
        '## 数据与代码可用性', '',
        '**评测数据。** `scenarios/<归档分组>/<任务>/` 保存实际评测子集，包括输入、金标、提示词、模型响应、评分和来源信息；不是上游数据集的完整副本。语音与 OCR 子集另附使用的媒体和转写。索引见[实验归档](scenarios/README.md)，来源和使用条件见[第三方说明](THIRD_PARTY_NOTICES.md)。', '',
        '**代码与版本。** 数据适配、调用、评分和核验代码位于 `scripts/`，仓库代码使用 [MIT 许可证](LICENSE)。第三方数据、标注、媒体与服务输出遵循各自许可，不随代码重新授权。复用或引用结果时应记录 Git 提交号、任务 ID 和归档模型版本。', '',
        '**训练扩展。** [逐项映射](docs/医疗任务映射.md#训练任务统计快照)另列 v0.5 中文训练包的 27 类、5,007 条统计快照；原训练包不属于主评测归档，其样本数和其他模型审计不计入本页 Jev 成绩。', '',
    ]
    extensions = research_extensions()
    if extensions:
        out += ['<details>', '<summary>研究扩展导航</summary>', '', *extensions, '</details>', '']
    return '\n'.join(out)


def render_task_table():
    comparison=load('comparisons/deepseek-flash/summary.json')
    if not comparison['summary']['complete']:
        raise ValueError('Do not publish an incomplete comparison as final')
    tasks=comparison['tasks']
    inventory=load('results/case_inventory.json')['tasks']
    scenes=load('results/scenario_manifest.json')['scenes']
    lines=['', '',
           '以下按场景列出全部 96 项任务。正确率表示答对比例；抽取综合分兼顾漏检和误报，满分 100。费用为每千条同类输入的美元估算。', '',
           '案例按来源中的病例、会话、文档、临床片段或题目计数；同一案例的多个字段不重复算案例，自编测试另有标注。点击案例数可查看逐案例成绩及来源分组，点击任务名称可查看评测方法。', '']
    methods=json.loads((ROOT/'results/task_methods.json').read_text())
    for scene in scenes:
        lines += [f'### {scene["title"]}', '',
                  '| 任务 | 任务类型 | 案例数 | 测试记录 | Jev | DeepSeek | 每千条费用：Jev / DeepSeek |',
                  '| --- | --- | ---: | ---: | ---: | ---: | ---: |']
        for task in scene['task_ids']:
            r=tasks[task];method=methods[task]
            lines.append(f'| [{method["title"]}](scenarios/{scene["id"]}/{task}/README.md) | {method["task_type"]} | [{inventory[task]['cases']}](scenarios/{scene['id']}/{task}/cases.md) | {r["planned"]} | {display(r["jev"]["quality"])} | {display(r["deepseek"]["quality"])} | {money(r["jev"]["cost_per_1000_usd"])} / {money(r["deepseek"]["cost_per_1000_usd"])} |')
        lines.append('')
    lines += ['[原始实验统计](docs/完整任务统计.md) · [对比实验详情](comparisons/deepseek-flash/README.md)', '']
    body='\n'.join(lines)
    return '# 全部任务的对比表现\n\n[首页](../README.md) · [统计与风险审计](医疗适用性审计.md)\n'+body.replace('](scenarios/', '](../scenarios/').replace('](docs/', '](').replace('](comparisons/', '](../comparisons/')
