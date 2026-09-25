"""Verify supplemental questions and explicit gold mappings against source records."""
import argparse,csv,json,re
from pathlib import Path
from prepare_minimum_cases import quiz

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--prepared',type=Path,required=True);a=ap.parse_args();root=Path(__file__).resolve().parents[1]
 multi=json.loads((a.prepared/'tcm-multi.json').read_text());single=json.loads((a.prepared/'tcm-single.json').read_text());exam=list(csv.DictReader((a.source/'CMExam/data/test_with_annotations.csv').open()));sdt={str(r['id']):r for r in json.loads((a.source/'TCM-BEST4SDT/TCM-BEST4SDT.json').read_text())}
 n=0
 for p in root.glob('scenarios/*/*/samples.jsonl'):
  for line in p.read_text().splitlines():
   r=json.loads(line);m=r['metadata'];cohort=m.get('cohort','')
   if cohort=='TCM-QA':
    src=(multi if m['source_file'].endswith('MULITPLE.json') else single)[m['source_index']];question,opts=quiz(src);assert r['request']['state']==question
    assert r['gold']==(list(src['answer'].strip()) if isinstance(r['gold'],list) else src['answer'].strip());n+=1
   elif cohort=='CMExam 公卫法律伦理':
    src=exam[m['source_index']];assert src['Area of Competency']=='公卫法律伦理';assert r['request']['state']==src['Question'];assert r['gold']==list(src['Answer'].strip());n+=1
   elif cohort=='TCM-BEST 病性要素拆分':
    src=sdt[r['group']];values=dict(s.split('：',1) for s in src['output'] if '：' in s);assert r['request']['state']==src['instruction'];assert m['source_original_nature']==values['病性'];assert r['gold']==m['source_gold_mapping'][values['病性']];n+=1
   elif cohort=='PriMock57 新增独立会话片段':
    kind='asr' if r['task']=='primock_asr_fields' else 'reference';base=root/'scenarios/multimodal/primock_asr_fields/upstream/minimum20';assert r['request']['state']==(base/(r['group']+'-'+kind+'.txt')).read_text();assert m['gold_evidence'].lower() in (base/(r['group']+'-reference.txt')).read_text().lower();n+=1
 assert n==93,n
 print('Verified 93 supplemental TCM and audio source bindings; OCR assets verified in publication manifest')
if __name__=='__main__':main()
