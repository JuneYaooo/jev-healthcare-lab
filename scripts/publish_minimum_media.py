"""Archive only evaluated audio/image assets, preserving original media manifests."""
import argparse,hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def info(path):return {'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepared',type=Path,required=True);a=ap.parse_args();export=[]
 for name,source in [('ocr',a.prepared/'media'),('audio',a.prepared/'aligned-media')]:
  for r in json.loads((a.prepared/(name+'_assets.json')).read_text()):
   path=source/r['path'];assert info(path)=={k:r[k] for k in ['bytes','sha256']};folder=ROOT/'scenarios/multimodal'/r['task'];target=folder/'upstream/minimum20'/r['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
   entry={'file':str(target.relative_to(folder)),'source':r['source'],**info(target)};manifest=folder/'upstream/manifest.json';entries=json.loads(manifest.read_text());entries=[e for e in entries if e['file']!=entry['file']]+[entry];manifest.write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n');export.append({'path':str(target.relative_to(ROOT)),**info(target)})
 audio=ROOT/'scenarios/multimodal/primock_asr_fields/upstream/minimum20'
 for name in ['locked_targets.json','execution.json']:
  shutil.copyfile(a.prepared/'aligned-media'/name,audio/name);export.append({'path':str((audio/name).relative_to(ROOT)),**info(audio/name)})
 rows=[json.loads(l) for name in ['initial.jsonl','tcm-rest.jsonl','audio.jsonl'] for l in (a.prepared/name).read_text().splitlines()]
 report={'added_records':len(rows),'tasks':{},'assets':export,'source_files':{name:info(a.prepared/name) for name in ['tcm-single.json','tcm-multi.json']}}
 for r in rows:report['tasks'].setdefault(r['task'],[]).append({'id':r['id'],'group':r['group'],'request_sha256':r['request_sha256'],'cohort':r['metadata']['cohort']})
 (ROOT/'results/minimum_case_expansion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Published',len(export),'verified media artifacts for',len(rows),'new paired records')
if __name__=='__main__':main()
