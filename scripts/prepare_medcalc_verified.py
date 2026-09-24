import benchmark as b
import csv,json,hashlib
p=b.DATA/'more/medcalc-verified-test.csv';tree=json.loads((b.DATA/'more/medcalc-tree.json').read_text());entry=next(x for x in tree if x['path']=='test_data.csv');data=p.read_bytes();assert len(data)==entry['size'];assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['oid']
limits={'Glasgow Coma Score (GCS)':(3,15),'CURB-65 Score for Pneumonia Severity':(0,5),'SIRS Criteria':(0,4),'CHA2DS2-VASc Score for Atrial Fibrillation Stroke Risk':(0,9),'FeverPAIN Score for Strep Pharyngitis':(0,5)};rows=[]
for r in csv.DictReader(p.open()):
 if r['Calculator Name'] not in limits:continue
 low,high=limits[r['Calculator Name']];gold=str(int(float(r['Ground Truth Answer'])));criteria={str(i):str(i) for i in range(low,high+1)};criteria['unknown']='The patient note lacks information necessary to determine the score';assert gold in criteria
 req=b.choice({'patient_note':r['Patient Note'],'question':r['Question']},'Determine the requested clinical score from this patient note. Select its numeric value from the fixed full score range. No reference parameters or explanation are supplied. If essential information is missing, select unknown.',criteria)
 x=b.record('medcalc_verified_bounded_score',r['Row Number'],r['Note ID'],req,gold,indicator=r['Calculator Name'],source='MedCalc-Bench-Verified published test CSV via publisher HF mirror;5 full bounded-score calculators x20; converted to closed numeric choice, NOT full55-calculator numerical generation benchmark');x['request_sha256']=b.sha(req);rows.append(x)
(b.DATA/'medcalc_verified_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print(len(rows))
(b.OUT/'medcalc_verified_source.json').write_text(json.dumps({'file':'test_data.csv','git_blob':entry['oid'],'sha256':hashlib.sha256(data).hexdigest(),'source':'https://huggingface.co/datasets/nsk7153/MedCalc-Bench-Verified','transport':'hf-mirror.com','verification':'Matches Git blob from mirror metadata; not independently checked against primary-host byte stream','scope':limits},indent=2))
