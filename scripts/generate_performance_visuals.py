"""Render performance curves from verified comparison.json; matplotlib required."""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    rows = json.loads((ROOT / 'results/performance-v1/comparison.json').read_text())
    colors = {'jev-1.13.0': '#187a61', 'deepseek-flash': '#386cb0'}
    names = {'jev-1.13.0': 'JEV 1.13', 'deepseek-flash': 'DeepSeek V4.1 Flash'}
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.hashsalt': 'jev-performance-v1'})
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))
    fig.set_facecolor('#fafaf7')
    fig.suptitle('Decision API performance — 3 repeated runs', fontsize=17, weight='bold')
    for model in colors:
        c = sorted([r for r in rows if r['suite'] == 'concurrency' and r['model'] == model], key=lambda r:r['level'])
        q = sorted([r for r in rows if r['suite'] == 'fanout' and r['model'] == model], key=lambda r:r['level'])
        axes[0].plot([r['level'] for r in c], [r['valid_decisions_per_s'] for r in c], 'o-', color=colors[model], label=names[model])
        axes[0].fill_between([r['level'] for r in c], [min(r['throughput_per_repeat']) for r in c], [max(r['throughput_per_repeat']) for r in c], color=colors[model], alpha=.12)
        axes[1].plot([r['level'] for r in q], [r['p50_s'] for r in q], 'o-', color=colors[model], label=names[model])
    axes[0].set(title='128 clinical questions per batch', xlabel='Concurrent requests', ylabel='Valid decisions / second', xticks=[1,8,16,32,64])
    axes[1].set(title='Fixed synthetic state, increasing questions', xlabel='Questions in one request', ylabel='Median full response time (seconds)', xticks=[1,10,50,100,200])
    for ax in axes:
        ax.set_facecolor('#fafaf7')
        ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y', alpha=.18)
        ax.set_ylim(bottom=0)
        ax.legend(frameon=False, fontsize=10)
    fig.subplots_adjust(left=.065, right=.985, bottom=.23, top=.79, wspace=.25)
    fig.text(.02,.055,'Shading: min–max throughput across runs. HTTP connections reused within workers; no retries.', fontsize=9, color='#555555')
    fig.text(.02,.02,'Finite batches, not sustained capacity. Synthetic routing rules do not measure clinical competence.  Source: JuneYaooo/jev-healthcare-lab', fontsize=8.5, color='#555555')
    out=ROOT/'assets/performance'
    out.mkdir(parents=True,exist_ok=True)
    svg = out/'performance-v1.svg'
    fig.savefig(svg,metadata={'Date':None})
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
    fig.savefig(out/'performance-v1.png',dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    main()
