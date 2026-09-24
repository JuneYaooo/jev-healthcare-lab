import benchmark as b
import xml.etree.ElementTree as E,json,collections
root=E.parse(b.DATA/'more/bioscope-abstracts.xml').getroot();pool=[];rows=[]
for doc in root.findall('.//Document'):
 pid=doc.findtext('DocID')
 for s in doc.findall('.//sentence'):
  labs={c.attrib['type'] for c in s.findall('.//cue')};lab='both' if len(labs)>1 else next(iter(labs),'neither');pool.append(dict(id=pid+':'+s.attrib['id'],group=pid,text=''.join(s.itertext()),gold=lab))
for lab in ['negation','speculation','both','neither']:
 for x in b.sample([r for r in pool if r['gold']==lab],25,'bioscope'+lab):
  req=b.choice(x['text'],'Which explicitly expressed linguistic cues occur in this biomedical sentence? Negation denies an event; speculation expresses uncertainty or hypothesis. Classify presence of either kind, not whether the main conclusion is true.',{'negation':'Negation cue only','speculation':'Speculative cue only','both':'Both negation and speculation cues','neither':'Neither'})
  r=b.record('bioscope_sentence_cues',x['id'],x['group'],req,x['gold'],source='BioScope abstracts XML official public download,25/class; sentence cue presence derived from gold cue tags; NOT cue/span localization or clinical assertions');r['request_sha256']=b.sha(req);rows.append(r)
(b.DATA/'bioscope_prepared.jsonl').write_text(''.join(b.dumps(r)+'\n' for r in rows));print(len(rows),collections.Counter(x['gold'] for x in pool))
