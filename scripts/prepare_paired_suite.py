"""Freeze larger, non-overlapping paired cases across three medical tasks."""
import argparse,json,random,tarfile
from pathlib import Path
import benchmark as b
ROOT=Path(__file__).resolve().parents[1]
SUITE=ROOT/'comparisons/paired-suite'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--original-data',type=Path,required=True);ap.add_argument('--pubmed-file',type=Path,required=True);a=ap.parse_args();D=a.original_data
 assert not (SUITE/'manifest.json').exists(),'Suite is already frozen'
 prior=[json.loads(l) for p in (ROOT/'scenarios').glob('*/*/samples.jsonl') for l in p.read_text().splitlines()]
 paired=[json.loads(l) for p in (ROOT/'scenarios').rglob('inputs.jsonl') for l in p.read_text().splitlines()]
 prior_ids={str(r.get('group',r['id'])) for r in prior+paired};prior_text='\n'.join(json.dumps(r['request']['state'],ensure_ascii=False) for r in prior+paired)
 def overlap(text):return json.dumps(text,ensure_ascii=False)[1:-1] in prior_text
 def record(id_,state,questions,gold,**metadata):
  request={'state':state,'questions':questions};assert len(questions)==len(gold)==10
  return {'id':str(id_),'request':request,'request_sha256':b.sha(request),'gold':gold,'metadata':metadata}
 experiments=[]
 def freeze(key,title,path,rows,count,description,source_url,selection,source_hash,positive=None):
  assert len(rows)>=count,(key,len(rows));rows=rows[:count];folder=ROOT/path/'paired-expanded';assert not folder.exists()
  old=json.loads((ROOT/'scenarios/evidence/pubmed_rct_section/paired-new/protocol.json').read_text())
  order=[(p,n) for p in ['jev','deepseek'] for n in [1,5,10]];random.Random(913+len(experiments)).shuffle(order)
  protocol={**old,'dataset':title,'source_url':source_url,'source_pool':selection,'source_pool_sha256':source_hash,'eligible_documents':None,'documents':count,'unique_decisions':count*10,'selection_sha256':b.sha(rows),'order':[{'round':rep,'provider':p,'group_size':n} for rep,seq in [(1,order),(2,order[::-1])] for p,n in seq],'description':description,'positive_label':positive,'scope':'Ten fixed judgments per material, groups of 1/5/10; four material workers, sequential requests within material; two reversed-order rounds with persistent connections. Descriptive API/workflow measurement, not clinical validation.'}
  folder.mkdir(parents=True);(folder/'inputs.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));(folder/'protocol.json').write_text(json.dumps(protocol,ensure_ascii=False,indent=2)+'\n')
  experiments.append({'id':key,'title':title,'path':str(folder.relative_to(ROOT)),'materials':count,'unique_decisions':count*10,'selection_sha256':b.sha(rows)})
 # Extra independent abstracts: exclude the prior twenty paired abstracts as well.
 pool=[]
 for block in a.pubmed_file.read_text().split('\n\n')[:-1][:300]:
  ls=block.strip().splitlines();pool.append({'id':ls[0][3:],'sentences':[l.split('\t',1) for l in ls[1:]]})
 assert len(pool)==300
 criteria={'BACKGROUND':'Background and motivation','OBJECTIVE':'Study objective','METHODS':'Study methods','RESULTS':'Study results','CONCLUSIONS':'Conclusions'}
 rows=[]
 for r in sorted(pool,key=lambda x:b.sha(['paired-expanded',x['id']])):
  if r['id'] in prior_ids or not 10<=len(r['sentences'])<=24 or any(overlap(t) for _,t in r['sentences']):continue
  indices=sorted(sorted(range(len(r['sentences'])),key=lambda i:b.sha([r['id'],i,'questions']))[:10]);qs={f's{i+1:02}':{'type':'choice','instructions':f'Classify the rhetorical role of sentence s{i+1:02} in this clinical trial abstract. Use the surrounding abstract for context.','criteria':criteria} for i in indices}
  rows.append(record(r['id'],{'sentences':{f's{i+1:02}':t for i,(_,t) in enumerate(r['sentences'])}},qs,{f's{i+1:02}':r['sentences'][i][0] for i in indices},source='PubMed_20k_RCT/test.txt',selected_indices=indices))
 freeze('pubmed','临床试验摘要整理','scenarios/evidence/pubmed_rct_section',rows,60,'60 篇新摘要，每篇固定 10 句，使用原始背景／目的／方法／结果／结论标签。','https://github.com/Franck-Dernoncourt/pubmed-rct','First 300 complete test abstracts, 10–24 sentences; exclude all archived main and paired IDs and any exact sentence match, stable SHA256 order.',b.sha(pool))
 # New Chinese consultation cases with ten annotated dialogue acts.
 data=json.loads((D/'imcs-dev.json').read_text());rows=[]
 old_imcs={str(r['group']) for r in prior if r['task'].startswith('imcs_')}
 for id_,r in sorted(data.items(),key=lambda x:b.sha(['paired-imcs',x[0]])):
  dialogue=r['dialogue']
  if str(id_) in old_imcs or not 10<=len(dialogue)<=40:continue
  # Exclude exact whole-dialogue duplicates; short generic phrases may recur across patients.
  signature=''.join(u['sentence'] for u in dialogue)
  if any(signature==''.join(x['request']['state'].get('utterances',[])) for x in paired if isinstance(x['request']['state'],dict)):continue
  selected=sorted(sorted(range(len(dialogue)),key=lambda i:b.sha([id_,i,'acts']))[:10]);assert all(dialogue[i]['dialogue_act'] in b.ACT for i in selected)
  state={'dialogue':{f'u{i+1:02}':{'speaker':u['speaker'],'text':u['sentence']} for i,u in enumerate(dialogue)}}
  qs={f'u{i+1:02}':{'type':'choice','instructions':f'结合整段问诊上下文，判断 u{i+1:02} 这句话的主要对话行为，只选最符合的一类。','criteria':b.ACT} for i in selected}
  rows.append(record(id_,state,qs,{f'u{i+1:02}':dialogue[i]['dialogue_act'] for i in selected},source='IMCS21 dev',selected_indices=selected))
 freeze('imcs','中文问诊内容归类','scenarios/service/imcs_dialogue_act',rows,40,'40 段新的公开中文问诊对话，每段固定 10 句话，使用原始对话行为标注；任务是内容归类，不是给出诊疗建议。','https://github.com/lemuria-wchen/imcs21','IMCS21 dev; 10–40 utterances; exclude every patient ID in existing IMCS main tasks; stable SHA256 order, ten utterances selected without label balancing.',b.sha(data))
 # Evidence sentence identification using original SciFact rationale annotations.
 with tarfile.open(D/'more/scifact-data.tar.gz') as t:
  claims=[json.loads(l) for l in t.extractfile('data/claims_train.jsonl').read().decode().splitlines()];corpus={str(r['doc_id']):r for l in t.extractfile('data/corpus.jsonl').read().decode().splitlines() for r in [json.loads(l)]}
 rows=[];used_docs=set();old_claims={str(r['id']) for r in prior if r['task'].startswith('scifact')}
 for claim in sorted(claims,key=lambda r:b.sha(['paired-scifact',r['id']])):
  if str(claim['id']) in old_claims or overlap(claim['claim']):continue
  for doc_id,annotations in sorted(claim['evidence'].items()):
   abstract=corpus[doc_id]['abstract'];positive=set(i for ann in annotations for i in ann['sentences'])
   if doc_id in used_docs or not 10<=len(abstract)<=30 or not 1<=len(positive)<=5 or any(overlap(x) for x in abstract):continue
   negatives=sorted(set(range(len(abstract)))-positive,key=lambda i:b.sha([claim['id'],doc_id,i]))[:10-len(positive)];indices=sorted(positive|set(negatives));assert len(indices)==10
   state={'claim':claim['claim'],'abstract':{f's{i+1:02}':s for i,s in enumerate(abstract)}}
   qs={f's{i+1:02}':{'type':'choice','instructions':f'Is sentence s{i+1:02} part of the direct evidence supporting or refuting the supplied claim? Use the whole abstract for context. General background and merely related statements are not direct evidence.','criteria':{'evidence':'Direct evidence supporting or refuting the claim','not_evidence':'Not direct evidence for this claim'}} for i in indices}
   rows.append(record(str(claim['id'])+':'+doc_id,state,qs,{f's{i+1:02}':'evidence' if i in positive else 'not_evidence' for i in indices},source='SciFact claims_train.jsonl and corpus.jsonl',claim_id=claim['id'],doc_id=doc_id,positive_sentence_indices=sorted(positive),selected_indices=indices));used_docs.add(doc_id);break
 freeze('scifact','医学文献证据句筛选','scenarios/evidence/scifact_cited_abstract',rows,40,'40 组新的主张与摘要，每组筛选 10 个句子是否属于支持或反驳该主张的直接证据。答案取原始证据句标注；不是重新判断整项主张真假。','https://github.com/allenai/scifact','SciFact train (public gold); one claim per distinct document, 10–30 sentences; retain all 1–5 gold rationale sentences plus hash-selected negatives to ten; exclude exact archived claims or abstract sentences. Annotations may omit alternative valid rationale sentences.',b.sha({'claims':claims,'corpus':corpus}),'evidence')
 SUITE.mkdir(parents=True);(SUITE/'manifest.json').write_text(json.dumps({'experiments':experiments,'materials':sum(e['materials'] for e in experiments),'unique_decisions':sum(e['unique_decisions'] for e in experiments),'previous_paired_materials_excluded':20},ensure_ascii=False,indent=2)+'\n')
 print([(e['id'],e['materials']) for e in experiments])
if __name__=='__main__':main()
