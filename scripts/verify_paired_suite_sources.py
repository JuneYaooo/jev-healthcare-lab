"""Check frozen suite texts and gold labels against local original source files."""
import argparse,json,tarfile
from pathlib import Path
import benchmark as b
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--original-data',type=Path,required=True);ap.add_argument('--pubmed-file',type=Path,required=True);a=ap.parse_args()
 pubmed={}
 for block in a.pubmed_file.read_text().split('\n\n')[:-1][:300]:
  ls=block.strip().splitlines();pubmed[ls[0][3:]]=[l.split('\t',1) for l in ls[1:]]
 imcs=json.loads((a.original_data/'imcs-dev.json').read_text())
 with tarfile.open(a.original_data/'more/scifact-data.tar.gz') as t:
  claims={str(r['id']):r for line in t.extractfile('data/claims_train.jsonl').read().decode().splitlines() for r in [json.loads(line)]}
  corpus={str(r['doc_id']):r for line in t.extractfile('data/corpus.jsonl').read().decode().splitlines() for r in [json.loads(line)]}
 manifest=json.loads((ROOT/'comparisons/paired-suite/manifest.json').read_text());old=[json.loads(l) for p in (ROOT/'scenarios').glob('*/*/samples.jsonl') for l in p.read_text().splitlines()];previous=[json.loads(l) for l in (ROOT/'scenarios/evidence/pubmed_rct_section/paired-new/inputs.jsonl').read_text().splitlines()]
 oldids={str(r.get('group',r['id'])) for r in old+previous};oldtext='\n'.join(json.dumps(r['request']['state'],ensure_ascii=False) for r in old+previous)
 total=0
 for e in manifest['experiments']:
  rows=[json.loads(l) for l in (ROOT/e['path']/'inputs.jsonl').read_text().splitlines()];assert b.sha(rows)==e['selection_sha256'];assert len({r['id'] for r in rows})==e['materials']
  for r in rows:
   state=r['request']['state'];ix=r['metadata']['selected_indices']
   if e['id']=='pubmed':
    assert r['id'] not in oldids
    sentences=pubmed[r['id']];assert state=={'sentences':{f's{i+1:02}':text for i,(_,text) in enumerate(sentences)}};gold={f's{i+1:02}':sentences[i][0] for i in ix}
    assert all(json.dumps(t,ensure_ascii=False)[1:-1] not in oldtext for _,t in sentences)
   elif e['id']=='imcs':
    assert r['id'] not in {str(x['group']) for x in old if x['task'].startswith('imcs_')}
    dialogue=imcs[r['id']]['dialogue'];assert state=={'dialogue':{f'u{i+1:02}':{'speaker':u['speaker'],'text':u['sentence']} for i,u in enumerate(dialogue)}};gold={f'u{i+1:02}':dialogue[i]['dialogue_act'] for i in ix}
   else:
    claim_id,doc_id=r['id'].split(':');claim=claims[claim_id];abstract=corpus[doc_id]['abstract'];assert state=={'claim':claim['claim'],'abstract':{f's{i+1:02}':s for i,s in enumerate(abstract)}}
    positive={i for annotation in claim['evidence'][doc_id] for i in annotation['sentences']};assert positive<=set(ix);gold={f's{i+1:02}':'evidence' if i in positive else 'not_evidence' for i in ix}
    assert all(json.dumps(t,ensure_ascii=False)[1:-1] not in oldtext for t in [claim['claim'],*abstract])
   assert r['gold']==gold and set(r['request']['questions'])==set(gold);total+=len(gold)
 print('Original source text and gold labels verified:',total,'judgments; prior materials excluded')
if __name__=='__main__':main()
