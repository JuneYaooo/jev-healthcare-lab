"""Download aligned public acted-consultation excerpts and run local ASR."""
import argparse,concurrent.futures as cf,hashlib,json,math,re,struct,time,wave
from pathlib import Path
import httpx

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--targets',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--model',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 targets=json.loads(a.targets.read_text());locked=[]
 for case,q,options,gold,evidence in targets:
  grid=a.source/(case+'_patient.TextGrid');blocks=[(float(start),float(end),re.sub('<[^>]+>','',t)) for start,end,t in re.findall(r'xmin = ([\d.]+)\s+xmax = ([\d.]+)\s+text = "(.*)"',grid.read_text())];match=next((start,end) for start,end,t in blocks if evidence.lower() in t.lower() and end<=90)
  start=max(0,math.floor(match[0])-5);end=max(start+20,math.ceil(match[1])+5);reference=' '.join(t for s,e,t in blocks if s>=start and e<=end and t);assert evidence.lower() in reference.lower()
  locked.append({'case':case,'question':q,'choices':options,'gold':gold,'gold_evidence':evidence,'excerpt_seconds':[start,end],'reference':reference,'textgrid_sha256':hashlib.sha256(grid.read_bytes()).hexdigest()})
 (a.output/'locked_targets.json').write_text(json.dumps(locked,ensure_ascii=False,indent=2))
 def fetch(item):
  case=item['case'];clip=a.output/(case+'-clip.wav')
  if clip.exists():return
  url='https://media.githubusercontent.com/media/babylonhealth/primock57/main/audio/'+case+'_patient.wav';start,end=item['excerpt_seconds']
  with httpx.Client(timeout=httpx.Timeout(30,connect=12)) as client:
   header=client.get(url,headers={'Range':'bytes=0-43'});header.raise_for_status();raw=header.content;assert raw[:4]==b'RIFF' and raw[36:40]==b'data' and struct.unpack('<HHIIHH',raw[20:36])==(1,1,16000,32000,2,16)
   lo=44+start*32000;hi=44+end*32000-1;response=client.get(url,headers={'Range':f'bytes={lo}-{hi}'});response.raise_for_status();assert response.status_code==206 and response.headers['content-range'].startswith(f'bytes {lo}-{hi}/');frames=response.content;assert len(frames)==(end-start)*32000
  with wave.open(str(clip),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(frames)
  print('Downloaded aligned excerpt',case,end-start,'seconds',flush=True)
 def fetch_retry(item):
  for attempt in range(4):
   try:return fetch(item)
   except (httpx.HTTPError,AssertionError) as error:
    print('Download retry',item['case'],type(error).__name__,attempt+1,flush=True)
    if attempt==3:raise
    time.sleep(1)
 with cf.ThreadPoolExecutor(4) as pool:list(pool.map(fetch_retry,locked))
 from pywhispercpp.model import Model
 model=Model(str(a.model),n_threads=4,language='en',print_progress=False,print_realtime=False,redirect_whispercpp_logs_to=str(a.output/'whisper.log'));runs=[]
 for r in locked:
  case=r['case'];(a.output/(case+'-reference.txt')).write_text(r['reference']);t=time.perf_counter();segments=model.transcribe(str(a.output/(case+'-clip.wav')));(a.output/(case+'-asr.txt')).write_text(' '.join(s.text for s in segments));runs.append({'case':case,'elapsed_s':time.perf_counter()-t,'excerpt_seconds':r['excerpt_seconds']});print('Transcribed',case,flush=True)
 (a.output/'execution.json').write_text(json.dumps({'model':'Whisper.cpp tiny.en-q5_1','model_sha256':hashlib.sha256(a.model.read_bytes()).hexdigest(),'runs':runs},indent=2))
if __name__=='__main__':main()
