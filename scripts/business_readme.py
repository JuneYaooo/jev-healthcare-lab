"""Render a task-first project homepage and full comparison from archived evidence."""
import json
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


# Concrete task examples; full results remain linked alongside the selection.
TASK_EXAMPLES = [
    ('aci_note_section', '把病历内容归入对应章节', '已给定章节边界'),
    ('longhealth_full_context', '读长病历，回答指定问题', '20 个虚构患者的 100 道选择题'),
    ('trialgpt_sigir_referral', '判断患者是否适配临床试验', '给定患者与试验材料，直接三分类'),
    ('medcalc_verified_bounded_score', '给临床量表选出数值评分', '5 种量表，答案来自给定选项'),
]

DOMAIN_EXAMPLES = {
    'service': '给患者提问分类、推荐科室、按规则分流',
    'records': '整理病历、识别肯否定、统一术语、查找错误',
    'reports': '把检验数值对上项目、读懂报告里的肯否定',
    'medication': '识别药物关系、用药变更、剂量与频次',
    'clinical': '比较诊断、检查、治疗、量表及中医相关题目',
    'followup': '识别复诊、复查等后续行动',
    'research': '筛选研究证据、整理 PICO、做患者入组预筛',
    'governance': '核对编码依据、识别隐私候选和有害请求',
}


def render():
    comparison = load('comparisons/deepseek-flash/summary.json')
    if not comparison['summary']['complete']:
        raise ValueError('Do not publish an incomplete comparison as final')
    audit = load('results/evidence_audit.json')['tasks']
    taxonomy = load('results/task_taxonomy.json')
    scenes = load('results/scenario_manifest.json')['scenes']
    owner = {t: s['id'] for s in scenes for t in s['task_ids']}
    total = comparison['summary']['planned_rows']
    n_tasks = len(taxonomy['benchmark_tasks'])
    j, d = (comparison['summary'][provider] for provider in ('jev', 'deepseek'))
    timing = {provider: load(f'comparisons/batch-time/{provider}/summary.json') for provider in ('jev', 'deepseek')}
    replay_total = timing['jev']['rows']
    if replay_total != timing['deepseek']['rows']:
        raise ValueError('Timing comparison uses different cohorts')
    long_case = audit['longhealth_full_context']['case_all_correct']['jev']
    out = [
        '# 医疗 AI，哪些任务值得先做？', '',
        'Jev Healthcare Lab · Jev × DeepSeek 医疗任务实测', '',
        '**一个帮你选医疗 AI 场景、比较模型效果和成本的开源评测仓库。**', '',
        '我们让 Jev 和 DeepSeek 回答同一批医疗题目：整理病历、识别用药变更、筛选科研证据……看它们能做对多少、花多少、等多久。测试材料、模型回答和评分脚本都在这里，做医疗产品或应用开发时可以直接查阅、复验。', '',
        f'**{len(taxonomy["domains"])} 个业务领域 · {n_tasks} 个评测条件 · {total:,} 条测试输入**', '',
        '**[找你的场景 →](docs/医疗任务总目录.md)　[看两家成绩 →](docs/任务对比.md)　[查看测试原题 →](scenarios/README.md)**', '',
        '## 99% 与 25%：同一个模型的两种表现', '',
        'Jev 给已分段的病历归类时答对 99/100；从给定选项中选出临床量表分数时，答对 25/100。具体任务和输入条件，决定了成绩该怎么读。', '',
        '| 交给 AI 的工作 | Jev 准确率 | DeepSeek 准确率 | 实际测的是什么 |',
        '| --- | ---: | ---: | --- |',
    ]
    for task, title, boundary in TASK_EXAMPLES:
        pair = audit[task]['paired']
        out.append(f'| [{title}](scenarios/{owner[task]}/{task}/README.md) | {pair["jev"]:.1%} | {pair["deepseek"]:.1%} | {boundary} |')
    out += [
        '',
        f'这些是全部 {n_tasks} 项中的四个例子。长病历问答虽然答对 95/100 道题，但只有 {long_case["correct"]}/{long_case["total"]} 个来源病例的题目全部答对。用来选场景时，还要看错在哪里、会漏掉什么，以及需要多少人工复核。[完整成绩](docs/任务对比.md) · [错误、区间与复核量](docs/医疗适用性审计.md)', '',
        '## 从你正在做的工作开始', '',
        '| 你关心的方向 | 仓库里可以看什么 |',
        '| --- | --- |',
    ]
    for domain, title in taxonomy['domains'].items():
        out.append(f'| [{title} →](docs/医疗任务总目录.md#{domain}) | {DOMAIN_EXAMPLES[domain]} |')
    out += [
        '',
        '每个方向都标明哪些已做有限实测、哪些只有训练扩展、哪些还没测。中医、OCR 和 ASR 等条件也有单独标记。[查看任务与实验的对应关系](docs/医疗任务映射.md)', '',
        '## 便宜多少，也要看怎么用', '',
        '相同模型，换一批调用条件，费用排序也会改变：', '',
        f'- **主效果评测**：每千条输入，Jev **{money(j["cost_per_1000_usd"])}**，DeepSeek **{money(d["cost_per_1000_usd"])}**。',
        f'- **独立重复输入测速**：每千条输入，Jev **{money(timing["jev"]["cost_usd"]/replay_total*1000)}**，DeepSeek **{money(timing["deepseek"]["cost_usd"]/replay_total*1000)}**。', '',
        f'以上为美元估算，按归档费率和可核验用量计算。重复输入可能提高缓存命中；两组分别为 {total:,} 条和 {replay_total:,} 条输入，费用也不含 OCR、语音转写、系统接入和人工复核。[费用、耗时与调用条件](comparisons/batch-time/README.md)', '',
        '如果你的产品需要对一份材料连续做多个判断，还可以看 [140 份新材料的逐项／合并处理实验](comparisons/paired-suite/README.md)：每次处理 1 项、5 项、10 项，对比准确率、总耗时和费用。', '',
        '## 看完分数，可以接着做什么', '',
        '1. **挑一个值得试的任务。** 在[任务目录](docs/医疗任务总目录.md)里确认输入、输出和覆盖边界，找到与你业务最接近的实验。',
        '2. **打开原题，检查模型怎么答。** 例如[长病历问答](scenarios/records/longhealth_full_context/README.md)，可以一路查看测试材料、提示词、标准答案、模型响应和逐案例成绩。',
        '3. **核验结果，再设计自己的测试。** 仓库保留评分和验证脚本；用自己的材料开展新实验，方法见[复现与实验说明](docs/REPRODUCING.md)。', '',
        '先在本地核验归档，无需 API 密钥或 GPU，使用 Git 和 Python 3.10+ 即可：', '',
        '```sh',
        'git clone https://github.com/JuneYaooo/jev-healthcare-lab.git',
        'cd jev-healthcare-lab',
        'python3 scripts/verify_experiments.py',
        '```', '',
        '成功时会核验 7,133 条主记录和 300 条扰动记录，并输出重算指标 `all matched`。这一步使用已保存的响应；重新调用模型需要相应服务账户。', '',
        '<details>',
        '<summary><strong>评测口径、模型版本与使用边界</strong></summary>', '',
        '- **测了什么**：72 项公开材料适配条件、24 项自编边界挑战。条件数不等于独立医疗工作数，输入数不等于患者数；给定实体、候选或章节边界的任务要按原条件理解。',
        '- **怎么比较**：Jev 为 `jev-1.13.0`；DeepSeek 请求名为 `deepseek-flash`，归档配置记为 V4.1 Flash、关闭思考模式。两者使用相同材料与判断目标；主效果评测不是同期测速。',
        '- **怎么计分**：首页四个例子在分析后选取，全部任务另表公开。分类报告准确率，集合抽取报告 micro-F1，不混成一个总分。失败留在分母；配对区间按来源案例聚合，属于探索性分析，未校正多重比较。',
        '- **能得出什么**：公开材料、合成病例和小样本测试可帮助筛选下一步验证方向。当前没有真实医院的前瞻性流程验证、独立医生全量审核或患者结局证据。',
        '- **哪些另算**：批处理与扰动实验分别报告；27 类训练任务只作为独立扩展映射，不计入主评测成绩。', '',
        '[详细方法](docs/EVALUATION.md) · [同题对比配置](comparisons/deepseek-flash/README.md) · [来源与未完成项](docs/覆盖与阻塞账本.md)', '',
        '</details>', '',
        '代码使用 [MIT 许可证](LICENSE)；评测文本、标注、媒体和服务输出遵循各自的[第三方使用条件](THIRD_PARTY_NOTICES.md)。引用结果时请记录提交号、任务 ID 和模型版本。', '',
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
