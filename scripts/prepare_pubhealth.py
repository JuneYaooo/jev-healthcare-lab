import benchmark as b
import duckdb,json,hashlib
p=b.DATA/'more/pubhealth-test.parquet';digest=hashlib.sha256(p.read_bytes()).hexdigest();assert digest=='ccbb9040748d73db51cb2fd9e78fa18e69e5afc79b3d90697a62e7aaab579096'
c=duckdb.sql(f"select * from read_parquet('{p}')");pool=[dict(zip(c.columns,x)) for x in c.fetchall()];pool=[dict(r,id=r['claim_id']) for r in pool if r['label'] in range(4) and r['claim'] and r['main_text'] and len(r['main_text'])<70000];rows=[]
for r in b.sample(pool,100,'pubhealth'):
 for condition in ['with_article','claim_only']:
  state={'claim':r['claim'],'publication_date':r['date_published']}
  if condition=='with_article':state['fact_check_article']=r['main_text']
  req=b.choice(state,'Classify this historical public-health claim as of the publication date.'+(' Use the supplied fact-checking article, which may directly state its conclusion.' if condition=='with_article' else ' No retrieval evidence is supplied.'),{'0':'False','1':'Mixture of true and false','2':'True','3':'Unproven'})
  x=b.record('pubhealth_'+condition,r['id'],r['id'],req,str(r['label']),source='official publisher HF converted test mirrored via hf-mirror,100 paired claims; main_text is a fact-check article not independent raw evidence; explanation excluded; historical labels not current clinical guidance');x['request_sha256']=b.sha(req);rows.append(x)
(b.DATA/'pubhealth_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print(len(rows))
