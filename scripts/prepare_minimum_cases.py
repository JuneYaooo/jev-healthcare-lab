"""Prepare independent source-labeled examples for previously small tasks."""
import argparse,json,re,hashlib,subprocess,csv
from pathlib import Path
import benchmark as b
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/minimum20'
def add(rows,task,id_,state,choices,gold,instruction,group=None,**meta):
 if isinstance(gold,list):
  req={'state':state,'questions':{k:{'type':'noul','instructions':instruction+' 候选：'+v} for k,v in choices.items()}};meta['scoring']='multi_question_keys';assert set(gold)<=set(choices)
 else:req=b.choice(state,instruction,choices);assert gold in choices
 r=b.record(task,id_,group or id_,req,gold,**meta);r['request_sha256']=b.sha(req);rows.append(r)
def quiz(r):
 parts=re.split(r'\n\s*([A-E])[.、．]\s*',r['question']);assert len(parts)>=9
 q=re.sub(r'^\d+[.、．]\s*','',parts[0]);pairs=list(zip(parts[1::2],parts[2::2]));assert len({k for k,v in pairs})==len(pairs)
 return q,{k:v.strip() for k,v in pairs}
def tcm():
 old=[json.loads(l) for p in (ROOT/'scenarios').glob('*/*/samples.jsonl') for l in p.read_text().splitlines() if not json.loads(l)['metadata'].get('cohort')];used={r['request']['state'] for r in old if isinstance(r['request']['state'],str)};rows=[];pool=[]
 for i,r in enumerate(json.loads((OUT/'tcm-multi.json').read_text())):
  try:q,opt=quiz(r)
  except AssertionError:continue
  if len(r['answer'].strip())>1 and q not in used:pool.append((i,q,opt,list(r['answer'].strip())))
 for i,q,opt,gold in sorted(pool,key=lambda x:b.sha(['minimum20-knowledge',x[0]]))[:9]:
  add(rows,'tcm_best_knowledge_multi','tcmqa:multi:'+str(i),q,opt,gold,'判断该候选是否为此多选题的正确答案。',source='TCM-QA original multiple-choice question and published answer',source_url='https://github.com/yizhen-buaa/TCM-QA-datasets',source_file='Q&A datasets-MULITPLE.json',source_index=i,cohort='TCM-QA',source_case_id='tcmqa:multi:'+str(i))
 pool=[]
 for i,r in enumerate(json.loads((OUT/'tcm-single.json').read_text())):
  try:q,opt=quiz(r)
  except AssertionError:continue
  if len(r['answer'].strip())==1 and '治法' in q and ('患者' in q or '患儿' in q) and q not in used:pool.append((i,q,opt,r['answer'].strip()))
 assert len(pool)>=15
 for i,q,opt,gold in sorted(pool,key=lambda x:b.sha(['minimum20-treatment',x[0]]))[:15]:
  add(rows,'tcm_best_principles','tcmqa:single:'+str(i),q,opt,gold,'根据病例选择治则治法的最佳选项。',source='TCM-QA original clinical treatment-principle MCQ and published answer',source_url='https://github.com/yizhen-buaa/TCM-QA-datasets',source_file='Q&A datasets-SINGLE.json',source_index=i,cohort='TCM-QA',source_case_id='tcmqa:single:'+str(i))
 (OUT/'tcm-basic.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print('Prepared',len(rows),'original TCM-QA questions')
def ocr():
 import duckdb
 old=[json.loads(l) for l in (ROOT/'scenarios/multimodal/clinocr_reference_doctype/samples.jsonl').read_text().splitlines() if not json.loads(l)['metadata'].get('cohort')];texts={r['request']['state'] for r in old};pool=[]
 for p in (ROOT/'data/expansion').glob('ocr-*.parquet'):
  q=duckdb.sql(f"SELECT * FROM read_parquet('{p}')");pool += [dict(zip(q.columns,r)) for r in q.fetchall()]
 # Four distinct source documents with the already established template-purpose mapping.
 selected=[]
 for template in [1,2,3,8]:
  r=next(r for r in sorted(pool,key=lambda r:r['doc_id']) if int(r['template'])==template and r['ground_truth'] not in texts);selected.append(r)
 labels={1:'radiology',2:'lab',3:'discharge',8:'referral'};opts={'radiology':'Radiology report','medication_list':'Medication list/reconciliation','lab':'Laboratory or pathology report','discharge':'Discharge summary or post-procedure discharge instructions','referral':'Referral letter','billing':'Billing/insurance document','unknown':'Other clinical note, assessment, questionnaire, daily report, or unreadable'}
 media=OUT/'media';media.mkdir(exist_ok=True);rows=[];assets=[]
 for r in selected:
  name=r['doc_id'];image=media/(name+'.jpg');image.write_bytes(r['image']['bytes']);ref=r['ground_truth'];(media/(name+'-reference.txt')).write_text(ref)
  result=subprocess.run(['tesseract',str(image),'stdout','-l','eng','--psm','3'],capture_output=True,text=True,check=True,timeout=40);(media/(name+'-ocr.txt')).write_text(result.stdout)
  for kind,text in [('reference',ref),('ocr',result.stdout)]:add(rows,'clinocr_'+kind+'_doctype','minimum20:'+name,text,opts,labels[int(r['template'])],'Classify this document by its primary clinical purpose.',group='template_'+str(r['template']),source='ClinOCR-Bench official distinct scan; purpose mapped from original reference',source_dataset='https://huggingface.co/datasets/ClinOCR-Bench/ClinOCR-Bench',source_case_id=re.search(r't\d+_s\d+',name)[0],cohort='ClinOCR-Bench supplement',template=int(r['template']),indicator=r['subset'])
  for suffix in ['.jpg','-reference.txt','-ocr.txt']:
   p=media/(name+suffix);assets.append({'task':'clinocr_ocr_doctype','path':p.name,'source':'ClinOCR-Bench '+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (OUT/'ocr.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));(OUT/'ocr_assets.json').write_text(json.dumps(assets,indent=2));print('Prepared OCR pairs:',len(rows),'records, four new source documents')
def ethics(source):
 old=[json.loads(l) for p in (ROOT/'scenarios').glob('*/*/samples.jsonl') for l in p.read_text().splitlines() if not json.loads(l)['metadata'].get('cohort')];states={r['request']['state'] for r in old if isinstance(r['request']['state'],str)};pool=[];rows=[]
 for i,r in enumerate(csv.DictReader((source/'CMExam/data/test_with_annotations.csv').open())):
  gold=list(r['Answer'].strip());opts=dict(re.findall(r'^([A-Z])\s+(.+)$',r['Options'],re.M))
  if len(gold)>1 and set(gold)<=set(opts) and r['Area of Competency']=='公卫法律伦理' and r['Question'] not in states:pool.append((i,r,opts,gold))
 assert len(pool)>=17
 for i,r,opts,gold in sorted(pool,key=lambda x:b.sha(['minimum20-ethics',x[0]]))[:17]:
  add(rows,'tcm_best_ethics_multi','cmexam:ethics:'+str(i),r['Question'],opts,gold,'判断该候选是否为此多选题的正确答案。',source='CMExam official test; original public-health law and ethics category; published exam answer, not current legal guidance',source_url='https://github.com/williamliujl/CMExam',source_index=i,cohort='CMExam 公卫法律伦理',source_case_id='cmexam:'+str(i))
 (OUT/'ethics.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print('Prepared',len(rows),'original law/ethics multi-answer questions')
def nature(source):
 old={str(r['group']) for p in (ROOT/'scenarios/tcm').glob('tcm_best_*/samples.jsonl') for l in p.read_text().splitlines() for r in [json.loads(l)] if not r['metadata'].get('cohort')};pool=[];rows=[]
 mapping={'实热证':['excess','heat'],'虚寒证':['deficiency','cold'],'虚热证':['deficiency','heat'],'本虚标实':['deficiency','excess'],'虚实夹杂':['deficiency','excess'],'虚实夹杂证':['deficiency','excess']}
 quotas={'实热证':6,'虚寒证':4,'虚热证':2,'mixed':6};choices={'cold':'寒性要素','heat':'热性要素','deficiency':'虚性要素','excess':'实性要素'}
 for r in json.loads((source/'TCM-BEST4SDT/TCM-BEST4SDT.json').read_text()):
  if 'question' in r or str(r['id']) in old:continue
  vals=dict(s.split('：',1) for s in r['output'] if '：' in s);label=vals['病性']
  if label in mapping:pool.append((r,label,'mixed' if label in ['本虚标实','虚实夹杂','虚实夹杂证'] else label))
 for bucket,n in quotas.items():
  candidates=sorted([x for x in pool if x[2]==bucket],key=lambda x:b.sha(['minimum20-nature',x[0]['id']]))[:n];assert len(candidates)==n
  for r,label,_ in candidates:
   add(rows,'tcm_best_nature_multi','best-elements:'+str(r['id']),r['instruction'],choices,mapping[label],'根据病例判断该病性要素是否属于主要病性；可同时包含多个要素。',group=str(r['id']),source='TCM-BEST4SDT original distinct SDT case; cold/heat/deficiency/excess factors deterministically split from an explicit compound source nature label',source_url='https://github.com/DYJG-research/TCM-BEST4SDT',source_case_id='best:'+str(r['id']),source_original_nature=label,source_gold_mapping=mapping,cohort='TCM-BEST 病性要素拆分',scope='Derived factor-selection adaptation; original two multi-answer option items retained and scored separately; no generated clinical gold')
 (OUT/'nature.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print('Prepared',len(rows),'distinct source cases with explicit compound nature labels')
def audio(source):
 rows=[];assets=[];targets=json.loads((source/'locked_targets.json').read_text());assert len(targets)==17
 for r in targets:
  case=r['case'];ref=(source/(case+'-reference.txt')).read_text();assert r['gold_evidence'].lower() in ref.lower()
  for kind in ['reference','asr']:
   text=(source/(case+'-'+kind+'.txt')).read_text()
   add(rows,'primock_'+kind+'_fields','minimum20:'+case,text,r['choices'],r['gold'],r['question']+' Only use what this transcript says.',group=case,source='PriMock57 original acted consultation; aligned excerpt; manually specified field question and gold evidenced by original reference before model calls',source_url='https://github.com/babylonhealth/primock57',source_audio_url='https://media.githubusercontent.com/media/babylonhealth/primock57/main/audio/'+case+'_patient.wav',source_case_id=case,audio_excerpt_seconds=r['excerpt_seconds'],gold_evidence=r['gold_evidence'],source_textgrid_sha256=r['textgrid_sha256'],cohort='PriMock57 新增独立会话片段')
  for suffix in ['-clip.wav','-reference.txt','-asr.txt']:
   p=source/(case+suffix);assets.append({'task':'primock_asr_fields','path':p.name,'source':'PriMock57 '+case+' patient channel; seconds '+str(r['excerpt_seconds']),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (OUT/'audio.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));(OUT/'audio_assets.json').write_text(json.dumps(assets,indent=2));print('Prepared',len(rows),'ASR/reference records from 17 distinct consultations')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('part',choices=['tcm','ocr','ethics','nature','audio']);ap.add_argument('--source',type=Path);a=ap.parse_args()
 if a.part in ['ethics','nature','audio']:assert a.source is not None;globals()[a.part](a.source)
 else:globals()[a.part]()
