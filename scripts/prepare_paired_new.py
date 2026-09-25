"""Lock fresh PubMed RCT documents and a paired request-grouping protocol."""
import argparse,json,hashlib,random
from pathlib import Path
import benchmark as b
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'scenarios/evidence/pubmed_rct_section/paired-new'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);a=ap.parse_args()
 assert not (BASE/'protocol.json').exists(),'Protocol already locked'
 # First 300 complete abstracts define the source pool independently of download length.
 blocks=a.source.read_text().split('\n\n')[:-1][:300];assert len(blocks)==300
 pool=[]
 for block in blocks:
  lines=block.strip().splitlines();assert lines[0].startswith('###')
  sentences=[line.split('\t',1) for line in lines[1:]];assert all(len(x)==2 for x in sentences)
  pool.append({'id':lines[0][3:],'sentences':sentences})
 old=[json.loads(l) for p in (ROOT/'scenarios').glob('*/*/samples.jsonl') for l in p.read_text().splitlines()]
 old_ids={str(r['group']) for r in old};old_text='\n'.join(json.dumps(r['request']['state'],ensure_ascii=False) for r in old)
 candidates=[r for r in pool if 10<=len(r['sentences'])<=24 and r['id'] not in old_ids and not any(json.dumps(text,ensure_ascii=False)[1:-1] in old_text for _,text in r['sentences'])]
 chosen=sorted(candidates,key=lambda r:b.sha(['paired-new-v1',r['id']]))[:20];assert len(chosen)==20
 criteria={'BACKGROUND':'Background and motivation','OBJECTIVE':'Study objective','METHODS':'Study methods','RESULTS':'Study results','CONCLUSIONS':'Conclusions'}
 rows=[]
 for r in chosen:
  selected=sorted(sorted(range(len(r['sentences'])),key=lambda i:b.sha([r['id'],i,'questions']))[:10])
  state={'sentences':{f's{i+1:02}':text for i,(_,text) in enumerate(r['sentences'])}}
  questions={f's{i+1:02}':{'type':'choice','instructions':f'Classify the rhetorical role of sentence s{i+1:02} in this clinical trial abstract. Use the surrounding abstract for context.','criteria':criteria} for i in selected}
  row={'id':r['id'],'request':{'state':state,'questions':questions},'gold':{f's{i+1:02}':r['sentences'][i][0] for i in selected},'source':'PubMed_20k_RCT/test.txt','selected_sentence_indices':selected}
  row['request_sha256']=b.sha(row['request']);assert all(g in criteria for g in row['gold'].values());rows.append(row)
 conditions=[(p,n) for p in ['jev','deepseek'] for n in [1,5,10]];random.Random(417).shuffle(conditions)
 protocol={'dataset':'PubMed 20k RCT test; fresh documents excluded from all existing main-task inputs','source_url':'https://github.com/Franck-Dernoncourt/pubmed-rct/blob/master/PubMed_20k_RCT/test.txt','source_pool':'First 300 complete test abstracts; retain 10–24 sentences, exclude prior IDs and any exact sentence overlap, choose 20 by fixed SHA256 order.','source_pool_sha256':b.sha(pool),'eligible_documents':len(candidates),'documents':20,'questions_per_document':10,'unique_decisions':200,'group_sizes':[1,5,10],'repetitions':2,'workers':4,'connect_timeout_s':10,'read_timeout_s':30,'retry_limit':1,'retry_delay_s':1,'http_client':'httpx persistent per-provider connection pool, HTTP/1.1; no local response cache','order':[{'round':rep,'provider':p,'group_size':n} for rep,seq in [(1,conditions),(2,list(reversed(conditions)))] for p,n in seq],'selection_sha256':b.sha(rows),'quality':'Each question scored against original source label; terminal missing outputs counted wrong; all groups use identical full state, questions and labels.','cost':'Actual reported usage at submission-time tariff, including recorded retries. Cache hit/miss retained; cache is not controlled.','scope':'Same ten questions per document, partitioned into groups of 1, 5 or 10. Four documents at a time; groups within each document execute sequentially. Paired workflow latency, not pure inference or unrestricted maximum throughput.'}
 BASE.mkdir(parents=True,exist_ok=True)
 (BASE/'inputs.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));(BASE/'protocol.json').write_text(json.dumps(protocol,ensure_ascii=False,indent=2)+'\n')
 print('Locked',len(rows),'new documents and',sum(len(r['gold']) for r in rows),'source-labeled decisions; eligible pool',len(candidates))
if __name__=='__main__':main()
