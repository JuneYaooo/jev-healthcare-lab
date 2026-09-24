"""Archive the exact medical requests and responses selected by the published index."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import shutil

import benchmark as b

ROOT = Path(__file__).resolve().parents[1]


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', required=True, type=Path, help='Original medical-bench work directory')
    args = ap.parse_args()
    source = args.source.resolve()
    index = {(r['task'], r['id']): r for r in map(json.loads, (ROOT/'results/evaluation_index.jsonl').read_text().splitlines())}
    scenes = json.loads((ROOT/'results/scenario_manifest.json').read_text())['scenes']
    paths = {t: ROOT/'scenarios'/s['id']/t for s in scenes for t in s['task_ids']}
    methods = json.loads((ROOT/'results/task_methods.json').read_text())
    metrics = json.loads((ROOT/'results/all_results.json').read_text())['tasks']
    catalog = json.loads((ROOT/'results/medical_catalog.json').read_text())
    selected = defaultdict(list)
    seen = set()
    # Read only prepared shards; do not recursively copy private configuration or unrelated datasets.
    for file in sorted(source.glob('*prepared.jsonl')):
        for line in file.read_bytes().splitlines():
            row = json.loads(line)
            key = (row['task'], row['id'])
            if key not in index:
                continue
            if key in seen:
                raise ValueError(f'Duplicate selected sample: {key}')
            digest = b.sha(row['request'])
            if digest != index[key]['request_sha256'] or digest != row['request_sha256']:
                raise ValueError(f'Request hash mismatch: {key}')
            response_path = source/'runs/jev-1.13.0'/(b.sha([*key, digest])+'.json')
            raw_response = response_path.read_bytes()
            if b'\n' in raw_response:
                raise ValueError('Response must be one line to preserve its exact file hash in JSONL')
            if hashlib.sha256(raw_response).hexdigest() != index[key]['response_sha256']:
                raise ValueError(f'Response hash mismatch: {key}')
            response = json.loads(raw_response)
            if response['status'] != 'ok':
                raise ValueError(f'Non-successful selected response: {key}')
            b.validate_response(row['request'], response['response'])
            selected[row['task']].append((line, raw_response, row, file.name))
            seen.add(key)
    if seen != set(index):
        raise ValueError(f'Missing samples: {len(set(index)-seen)}')
    for task, samples in sorted(selected.items()):
        if task.startswith('robust_'):
            _, variant, parent = task.split('_', 2)
            dest = paths[parent]/'robustness'/variant
        else:
            parent = task
            dest = paths[task]
        dest.mkdir(parents=True, exist_ok=True)
        (dest/'samples.jsonl').write_bytes(b'\n'.join(x[0] for x in samples)+b'\n')
        (dest/'responses.jsonl').write_bytes(b'\n'.join(x[1] for x in samples)+b'\n')
        (dest/'index.jsonl').write_text(''.join(b.dumps(index[(task, x[2]['id'])])+'\n' for x in samples))
        prompts = {}
        for _, _, row, _ in samples:
            for question in row['request']['questions'].values():
                digest = b.sha(question)
                if digest not in prompts:
                    prompts[digest] = {'question': question, 'occurrences': 0, 'example_sample_id': row['id']}
                prompts[digest]['occurrences'] += 1
        dump(dest/'prompts.json', {'origin': 'Exact question objects from the archived requests; no rewritten prompts.', 'variants': list(prompts.values())})
        dump(dest/'example.json', {'sample': samples[0][2], 'response': json.loads(samples[0][1])})
        sources = [{k:r[k] for k in ('resource','source','completion_note')} for r in catalog if parent in r['tested_tasks']]
        provenance = {'task': task, 'model': 'jev-1.13.0', 'date': '2026-09-24',
                      'prepared_shards': sorted({x[3] for x in samples}),
                      'original_shard_sha256': {name: hashlib.sha256((source/name).read_bytes()).hexdigest() for name in sorted({x[3] for x in samples})},
                      'sample_count': len(samples),
                      'groups': len({x[2]['group'] for x in samples}), 'resources': sources,
                      'adapter': methods[parent]['adapter'], 'request_payload': 'sample.request plus model; gold and metadata are not sent',
                      'response_hash_format': 'SHA256 of each responses.jsonl line, excluding the added line separator; identical to original response file bytes',
                      'files': {name: {'bytes': (dest/name).stat().st_size, 'sha256': hashlib.sha256((dest/name).read_bytes()).hexdigest()} for name in ('samples.jsonl','responses.jsonl','index.jsonl','prompts.json','example.json')}}
        dump(dest/'provenance.json', provenance)
        if not task.startswith('robust_'):
            dump(dest/'results.json', metrics[task])
        else:
            ab = json.loads((ROOT/'results/ablations.json').read_text())
            dump(dest/'results.json', ab['robustness']['tasks'][parent+':'+variant])

    def attach(task, name, value):
        dump(paths[task]/name, value)
    ab = json.loads((ROOT/'results/ablations.json').read_text())
    offline = json.loads((ROOT/'results/offline_baselines.json').read_text())
    for t, result in offline['tasks'].items():
        attach(t, 'baseline.json', result)
    attach('ncbi_medspacy_jev_ner','baseline.json',json.loads((ROOT/'results/medspacy_results.json').read_text()))
    attach('cdrugred_discharge_candidate_pipeline','baseline.json',ab['cdrugred_baseline'])
    attach('bmi_weight_selection','hybrid.json',ab['bmi_hybrid'])
    attach('medcalc_verified_bounded_score','source_verification.json',json.loads((ROOT/'results/medcalc_verified_source.json').read_text()))
    attach('ddxplus_synthetic_primary','source_verification.json',json.loads((ROOT/'results/ddxplus_source.json').read_text()))
    attach('evidencebench_sentence_selection','hash_audit.json',json.loads((ROOT/'results/hash_normalization_audit.json').read_text()))
    # Actual upstream media and transcriptions used in the two propagation experiments.
    def copy_input(task, relative, target):
        path = source/relative
        dest = paths[task]/'upstream'/target
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        return {'file': str(dest.relative_to(paths[task])), 'source': str(relative), 'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    media = []
    for name in ('primock-patient-complete.wav','primock-reference.txt','primock-asr.txt'):
        media.append(copy_input('primock_asr_fields', Path('more')/name, name))
    attach('primock_asr_fields','upstream/manifest.json',media)
    attach('primock_asr_fields','upstream/results.json',json.loads((ROOT/'results/asr_results.json').read_text()))
    media = []
    selected_ocr = json.loads((source/'more/ocr_selected.json').read_text())
    for r in selected_ocr:
        for relative in (r['image'],r['ground_truth'],r['doc_id']+'-ocr.txt'):
            media.append(copy_input('clinocr_ocr_doctype',Path('more/ocr-eval')/relative,relative))
    attach('clinocr_ocr_doctype','upstream/manifest.json',media)
    attach('clinocr_ocr_doctype','upstream/selection.json',selected_ocr)
    attach('clinocr_ocr_doctype','upstream/results.json',json.loads((ROOT/'results/ocr_results.json').read_text()))
    # The original authored challenge panel was missing from the earlier export.
    original_outputs = source.parents[1]/'outputs/jev-medical-bench'
    shutil.copyfile(original_outputs/'challenge_cases.json',ROOT/'results/challenge_cases.json')
    dump(ROOT/'results/archive_summary.json',{'scenarios':len(scenes),'main_tasks':len(paths),'main_rows':sum(len(v) for t,v in selected.items() if not t.startswith('robust_')),'robustness_variants':sum(t.startswith('robust_') for t in selected),'robustness_rows':sum(len(v) for t,v in selected.items() if t.startswith('robust_')),'verified_request_response_pairs':len(seen),'original_index':'results/evaluation_index.jsonl','raw_scope':'The exact evaluated text inputs, labels, prompts and cached responses; upstream ASR audio and six OCR scans. Not the full source datasets.'})
    print(f'Archived {len(paths)} main tasks and {len(seen)} verified sample/response pairs.')


if __name__ == '__main__':
    main()
