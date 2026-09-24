from pywhispercpp.model import Model
from pathlib import Path
import time,json,re
from rapidfuzz.distance import Levenshtein
D=Path('data/more');t=time.perf_counter();m=Model(str(D/'ggml-tiny.en-q5_1.bin'),n_threads=4,language='en',print_progress=False,print_realtime=False,redirect_whispercpp_logs_to=str(D/'whisper.log'));segs=m.transcribe(str(D/'primock-patient-complete.wav'));elapsed=time.perf_counter()-t;text=' '.join(s.text for s in segs);(D/'primock-asr.txt').write_text(text)
norm=lambda s:re.findall(r"[a-z]+(?:'[a-z]+)?|\d+",re.sub(r'<[^>]+>', '', s).lower());gold=norm((D/'primock-reference.txt').read_text());pred=norm(text);out=dict(model='whisper.cpp tiny.en-q5_1',audio='PriMock57 day1 consultation01 patient channel',duration_seconds=457.92,elapsed_seconds=elapsed,reference_words=len(gold),hypothesis_words=len(pred),word_error_rate=Levenshtein.distance(gold,pred)/len(gold),segments=[dict(start=s.t0/100,end=s.t1/100,text=s.text) for s in segs]);Path('results/asr_results.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k!='segments'})
