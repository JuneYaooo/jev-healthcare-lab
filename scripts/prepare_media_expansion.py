"""Prepare additional public audio excerpts and OCR documents from real upstream files."""
import argparse,json,re,subprocess,hashlib,wave
from pathlib import Path
import duckdb
import benchmark as b
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data/expansion';MEDIA=D/'media'

def main():
 rows=[];assets=[]
 def add(task,id_,group,state,q,opts,gold,**meta):
  r=b.record(task,id_,group,b.choice(state,q,opts),gold,**meta);r['request_sha256']=b.sha(r['request']);rows.append(r)
 targets={
 'day1_consultation02':[
 ('itching','Does the patient report current itching?',{'yes':'Reports itching','no':'Explicitly denies itching','unknown':'Not documented'},'yes','really itchy'),
 ('red_skin','Does the patient report red skin?',{'yes':'Reports red skin','no':'Explicitly denies red skin','unknown':'Not documented'},'yes','a red skin'),
 ('location','Which set of affected locations does the patient explicitly mention?',{'chest_hands_arms':'Chest, hands and arms','face_feet':'Face and feet','unknown':'Not documented'},'chest_hands_arms','my chest, my, my hands, my arms'),
 ('sleep','What effect on sleep is reported?',{'impaired':'Cannot sleep at night','normal':'No effect on sleep','unknown':'Not documented'},'impaired',"can't even sleep at night")],
 'day1_consultation03':[
 ('onset','When did this headache start?',{'midday':'Since mid-day','yesterday':'Yesterday','unknown':'Not documented'},'midday','since mid-day'),
 ('side','Which side is the headache on?',{'left':'Left','right':'Right','unknown':'Not documented'},'left','left side'),
 ('vision','When were zig-zag visual lines noticed relative to the headache?',{'before':'A few minutes before','after':'After','unknown':'Not documented'},'before','a few minutes before the headache started'),
 ('movement','What happens to the headache when moving or leaning forward?',{'worse':'It gets worse','better':'It improves','unknown':'Not documented'},'worse','headache gets worse')]
 }
 for case,items in targets.items():
  ref=(MEDIA/(case+'-reference.txt')).read_text()
  for name,q,opts,gold,evidence in items:
   assert evidence in ref
   for kind in ['reference','asr']:
    add('primock_'+kind+'_fields',case+':'+name,case,(MEDIA/(case+'-'+kind+'.txt')).read_text(),q+' Only use what this transcript says.',opts,gold,source='PriMock57 public acted consultation; first 90 seconds of patient channel; gold annotated from reference before model calls',gold_evidence=evidence,audio_excerpt_seconds=[0,90],source_audio_url='https://media.githubusercontent.com/media/babylonhealth/primock57/main/audio/'+case+'_patient.wav')
  for suffix in ['-clip.wav','-reference.txt','-asr.txt']:assets.append({'task':'primock_asr_fields','path':case+suffix,'source':'PriMock57 '+case+' patient channel, 0–90 seconds; tiny.en-q5_1 ASR for the asr text'})
 # Cover the fourteen additional template types; the first archive already used templates 1 and 9.
 labels={2:'lab',3:'discharge',4:'unknown',5:'unknown',6:'lab',7:'unknown',8:'referral',10:'unknown',11:'lab',12:'lab',13:'unknown',14:'unknown',15:'lab',16:'unknown'}
 opts={'radiology':'Radiology report','medication_list':'Medication list/reconciliation','lab':'Laboratory or pathology report','discharge':'Discharge summary or post-procedure discharge instructions','referral':'Referral letter','billing':'Billing/insurance document','unknown':'Other clinical note, assessment, questionnaire, daily report, or unreadable'}
 pool=[]
 for p in [D/'ocr-normal.parquet',D/'ocr-tables.parquet']:
  q=duckdb.sql(f"SELECT * FROM read_parquet('{p}')");pool += [dict(zip(q.columns,r)) for r in q.fetchall()]
 for template,gold in labels.items():
  selected=sorted([r for r in pool if int(r['template'])==template],key=lambda r:r['doc_id'])[0];name=selected['doc_id'];img=MEDIA/(name+'.jpg')
  img.write_bytes(selected['image']['bytes']);ref=selected['ground_truth'];(MEDIA/(name+'-reference.txt')).write_text(ref)
  result=subprocess.run(['tesseract',str(img),'stdout','-l','eng','--psm','3'],capture_output=True,text=True,check=True,timeout=40);(MEDIA/(name+'-ocr.txt')).write_text(result.stdout)
  for kind,text in [('reference',ref),('ocr',result.stdout)]:
   add('clinocr_'+kind+'_doctype',name,'template_'+str(template),text,'Classify this document by its primary clinical purpose.',opts,gold,source='ClinOCR-Bench official test, one additional scan for each previously unrepresented template; doc-type gold manually mapped from reference purpose',template=template,indicator=selected['subset'],source_dataset='https://huggingface.co/datasets/ClinOCR-Bench/ClinOCR-Bench',category_note='Expanded descriptions clarify pathology under lab and post-procedure instructions under discharge; other notes use unknown')
  for suffix in ['.jpg','-reference.txt','-ocr.txt']:assets.append({'task':'clinocr_ocr_doctype','path':name+suffix,'source':'ClinOCR-Bench official '+selected['subset']+' test '+name})
 for a in assets:
  p=MEDIA/a['path'];a.update(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 (D/'media_additions.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));(D/'media_assets.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
 print('Prepared',len(rows),'real-media derived records,',len(assets),'source assets.')

if __name__=='__main__':main()
