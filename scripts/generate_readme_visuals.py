"""Build README charts from archived results. Requires matplotlib and Pillow to render."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/readme'
SOURCES = ['results/clinical-v1/comparison.json',
           'benchmarks/medical_decision_v1/evaluation-summary.json',
           'benchmarks/medical_decision_v1/taxonomy.json']
BG, PANEL, INK, MUTED, GREEN = '#09121d', '#111f2e', '#edf5fa', '#a5b8ca', '#5de3ba'
COLORS = {'jev-1.13.0': GREEN, 'deepseek-flash': '#73b7ff',
          'deepseek-v4-pro': '#9aaff0', 'qwen3.8-27b': '#eda977', 'qwen3.5-9b': '#c49ade'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics():
    comparison, inventory, taxonomy = [json.loads((ROOT / p).read_text()) for p in SOURCES]
    clinical = inventory['clinical']
    models = sorted(comparison['models'].items(), key=lambda x: -x[1]['primary_clinical_score'])
    scenes = []
    for scene in taxonomy['scenarios']:
        families = [f for f in clinical['families'] if f['scenario'] == scene['id'] and f['records']]
        if not families:
            continue
        scenes.append({'title': scene['title'], 'records': sum(f['records'] for f in families),
                       'tasks': len(families), 'small_tasks': sum(f['small_sample'] for f in families),
                       'values': [sum(m['tasks'][f['id']]['accuracy'] for f in families) / len(families) * 100
                                  for _, m in models]})
    for i, (_, model) in enumerate(models):
        assert math.isclose(sum(s['values'][i] for s in scenes) / len(scenes),
                            model['primary_clinical_score'] * 100, abs_tol=1e-10)
    return {'records': clinical['records'], 'scenes': scenes, 'defined_tasks': clinical['defined_families'],
            'tested_tasks': clinical['populated_families'],
            'small_tasks': sum(f['small_sample'] for f in clinical['families']),
            'models': [{'id': key, 'label': m['label'], 'score': m['primary_clinical_score'] * 100,
                        'seconds': m['timing']['mean_elapsed_s']} for key, m in models]}


def font_path():
    candidates = [os.environ.get('JEV_CHART_FONT', ''),
                  '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
                  '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']
    for path in candidates:
        if path and Path(path).is_file():
            return path
    raise SystemExit('Set JEV_CHART_FONT to a Chinese-capable TTF/OTF font.')


def draw_charts(data, font):
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib import pyplot as plt, font_manager, colors
    from matplotlib.patches import Rectangle
    font_manager.fontManager.addfont(font)
    plt.rcParams.update({'font.family': font_manager.FontProperties(fname=font).get_name(),
                         'font.size': 13, 'text.color': INK, 'axes.labelcolor': MUTED,
                         'xtick.color': MUTED, 'ytick.color': INK, 'svg.fonttype': 'path',
                         'svg.hashsalt': 'jev-healthcare-v1', 'axes.unicode_minus': False})

    def canvas(title, subtitle):
        fig = plt.figure(figsize=(12, 6.8), dpi=150, facecolor=BG)
        fig.text(.045, .94, title, fontsize=24, weight='bold', va='top')
        fig.text(.045, .873, subtitle, fontsize=12, color=MUTED, va='top')
        return fig

    def save(fig, name):
        fig.savefig(OUT / (name + '.svg'), facecolor=BG, metadata={'Date': None})
        fig.savefig(OUT / (name + '.png'), facecolor=BG)
        plt.close(fig)

    models = data['models']
    best, runner_up = models[:2]
    fastest = min(models, key=lambda m: m['seconds'])
    fig = canvas('本轮结果：' + best['label'] + ' 主分数最高',
                 f"{data['records']:,} 道相同题目 · {data['tested_tasks']} 个有题任务 · {len(models)} 个模型")
    fig.text(.045, .785, f"{best['score']:.2f}%", fontsize=36, color=GREEN, weight='bold')
    fig.text(.285, .80, f"领先第二名 {best['score'] - runner_up['score']:.2f} 个百分点", fontsize=15)
    fig.text(.285, .759, f"平均用时最短：{fastest['label']} · {fastest['seconds']:.3f} 秒/题", fontsize=13, color=MUTED)
    for rect, field, limit, ticks, title in [
            ([.245, .205, .335, .44], 'score', 105, [0, 25, 50, 75, 100], '临床主分数 ↑'),
            ([.67, .205, .275, .44], 'seconds', 3.6, [0, 1, 2, 3], '平均用时 · 秒/题 ↓')]:
        ax = fig.add_axes(rect, facecolor=BG)
        values = [m[field] for m in models]
        bars = ax.barh(range(len(models)), values, height=.52, color=[COLORS[m['id']] for m in models])
        ax.invert_yaxis()
        ax.set_xlim(0, limit)
        ax.set_xticks(ticks)
        ax.set_yticks(range(len(models)), [m['label'] for m in models] if field == 'score' else [''] * len(models))
        ax.tick_params(axis='both', length=0, pad=12, labelsize=12)
        ax.set_title(title, loc='left', fontsize=15, pad=22, color=INK)
        ax.set_axisbelow(True)
        ax.grid(axis='x', color='#223448', linewidth=.7)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for bar, value in zip(bars, values):
            ax.text(value + limit * .02, bar.get_y() + bar.get_height()/2,
                    f'{value:.2f}%' if field == 'score' else f'{value:.3f}',
                    va='center', fontsize=12, color=INK)
    fig.text(.045, .093, '主分数：场景内任务等权，再对场景等权；全部小样本任务计入。', fontsize=12, color=MUTED)
    fig.text(.045, .052, '用时包含网络与等待，受平台条件影响。本轮差值不代表统计显著性或临床有效性。', fontsize=11, color=MUTED)
    save(fig, 'performance-v1')

    fig = canvas('场景表现：优势与差距分别看', '每格为场景内任务等权准确率（%） · 描边为最高值；并列均标记，全部相同不标记')
    ax = fig.add_axes([.30, .18, .64, .59], facecolor=BG)
    scenes = data['scenes']
    values = [s['values'] for s in scenes]
    cmap = colors.LinearSegmentedColormap.from_list('clinical', ['#142331', '#245774', '#68ddbd'])
    ax.imshow(values, cmap=cmap, vmin=0, vmax=100, aspect='auto')
    labels = ['JEV 1.13', 'DeepSeek\nV4.1 Flash', 'DeepSeek\nV4 Pro', 'Qwen\n3.8-27B', 'Qwen\n3.5-9B']
    by_id = dict(zip(['jev-1.13.0', 'deepseek-flash', 'deepseek-v4-pro', 'qwen3.8-27b', 'qwen3.5-9b'], labels))
    ax.set_xticks(range(len(models)), [by_id[m['id']] for m in models], fontsize=12)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(scenes)),
                  [f"{s['title']}\n{s['records']} 题 · {s['tasks']} 任务" +
                   (f" · {s['small_tasks']} 小样本" if s['small_tasks'] else '') for s in scenes], fontsize=11)
    ax.tick_params(length=0, pad=12)
    for i, scene in enumerate(scenes):
        rounded = [round(v, 1) for v in scene['values']]
        for j, value in enumerate(scene['values']):
            ax.text(j, i, f'{value:.1f}', ha='center', va='center', fontsize=16,
                    color=BG if value >= 65 else INK, weight='bold')
            if max(rounded) != min(rounded) and rounded[j] == max(rounded):
                ax.add_patch(Rectangle((j-.45, i-.43), .9, .86, fill=False, edgecolor=INK, linewidth=1.7))
    ax.set_xticks([i-.5 for i in range(len(models)+1)], minor=True)
    ax.set_yticks([i-.5 for i in range(len(scenes)+1)], minor=True)
    ax.grid(which='minor', color=BG, linewidth=5)
    ax.tick_params(which='minor', length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.text(.045, .10, '小样本 = 单任务不足 20 题。医疗质量控制仅 3 题，100% 不代表稳定的场景能力。', fontsize=12, color=MUTED)
    fig.text(.045, .056, '所有模型使用相同题目；最终请求失败与无效回答计错。完整样例、来源与结果见任务页。', fontsize=11, color=MUTED)
    save(fig, 'scenarios-v1')


def draw_motion(data, font):
    from PIL import Image, ImageDraw, ImageFont
    fonts = {size: ImageFont.truetype(font, size) for size in [15, 18, 22, 25, 32, 46]}
    base = Image.new('RGB', (1200, 400), BG)
    d = ImageDraw.Draw(base)
    for x in range(0, 1200, 40):
        d.line((x, 0, x, 400), fill='#102130')
    for y in range(0, 400, 40):
        d.line((0, y, 1200, y), fill='#102130')
    d.text((42, 26), 'JEV / HEALTHCARE LAB', font=fonts[18], fill=GREEN)
    d.text((42, 66), '让每一次医疗决策，都有据可查。', font=fonts[32], fill=INK)
    d.text((44, 116), '公开题目  /  同题比较  /  逐题溯源', font=fonts[18], fill=MUTED)
    xs, y = [125, 438, 751, 1064], 213
    labels = ['病例与规则', '候选决策', '模型作答', '评分与用时']
    for x, label in zip(xs, labels):
        d.rounded_rectangle((x-85, y-31, x+85, y+31), radius=12, fill=PANEL, outline='#355169', width=1)
        d.text((x, y), label, font=fonts[22], fill=INK, anchor='mm')
    for a, b in zip(xs, xs[1:]):
        d.line((a+85, y, b-85, y), fill='#2a5365', width=2)
    stats = [(str(len(data['scenes'])), '医疗场景'), (str(data['defined_tasks']), f"任务 / {data['tested_tasks']} 项有题"),
             (f"{data['records']:,}", '固定评测题'), (str(len(data['models'])), '同题对照模型')]
    for i, (number, label) in enumerate(stats):
        x = 45 + 295*i
        d.text((x, 280), number, font=fonts[46], fill=GREEN if i==0 else INK)
        d.text((x, 343), label, font=fonts[18], fill=MUTED)
    base.save(OUT / 'hero-v1.png')
    frames = []
    for frame in range(48):
        im = base.copy()
        draw = ImageDraw.Draw(im)
        for segment, (a, b) in enumerate(zip(xs, xs[1:])):
            t = (frame/48 - segment/3) % 1
            if t < .5:
                x = a+89 + (b-a-178)*(t*2)
                draw.ellipse((x-9, y-9, x+9, y+9), fill='#164b48')
                draw.ellipse((x-4, y-4, x+4, y+4), fill=GREEN)
        frames.append(im)
    # A shared palette avoids color flicker; motion never changes reported data.
    palette = frames[0].quantize(colors=128)
    indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT / 'hero-v1.gif', save_all=True, append_images=indexed[1:],
                    duration=100, loop=0, optimize=True, disposal=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = metrics()
    source_hashes = {p: sha(ROOT / p) for p in SOURCES}
    manifest_path = OUT / 'manifest-v1.json'
    if args.check:
        manifest = json.loads(manifest_path.read_text())
        assert manifest['inputs'] == source_hashes, 'Visual input changed; regenerate assets'
        assert manifest['generator_sha256'] == sha(Path(__file__)), 'Visual generator changed'
        assert json.loads((OUT / 'metrics-v1.json').read_text()) == data
        for name, digest in manifest['assets'].items():
            assert sha(OUT / name) == digest, name
        print('Verified README visual data and asset hashes.')
        return
    OUT.mkdir(parents=True, exist_ok=True)
    font = font_path()
    draw_charts(data, font)
    draw_motion(data, font)
    (OUT / 'metrics-v1.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    files = sorted(p for p in OUT.iterdir() if p.name != manifest_path.name)
    manifest_path.write_text(json.dumps({'inputs': source_hashes, 'generator_sha256': sha(Path(__file__)),
                                        'assets': {p.name: sha(p) for p in files}}, indent=2)+'\n')
    print('Wrote README animation, charts, static previews and source metrics.')


if __name__ == '__main__':
    main()
