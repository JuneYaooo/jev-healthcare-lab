"""Extract aligned PriMock57 patient-channel excerpts and transcribe with Whisper.cpp."""
import argparse,hashlib,json,re,time,wave
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--audio-dir',type=Path,required=True);ap.add_argument('--model',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 from pywhispercpp.model import Model
 a.output.mkdir(parents=True,exist_ok=True);model=Model(str(a.model),n_threads=4,language='en',print_progress=False,print_realtime=False,redirect_whispercpp_logs_to=str(a.output/'whisper.log'));evidence=[]
 for case in ['day1_consultation02','day1_consultation03']:
  audio=a.audio_dir/(case+'_patient.wav');grid=a.source/'transcripts'/(case+'_patient.TextGrid');clip=a.output/(case+'-clip.wav')
  with wave.open(str(audio)) as w:
   params=w.getparams();frames=90*w.getframerate();raw=w.readframes(frames)
   if len(raw)!=frames*w.getsampwidth()*w.getnchannels():raise ValueError('Source does not contain the complete excerpt')
  with wave.open(str(clip),'wb') as w:w.setparams(params);w.writeframes(raw)
  blocks=re.findall(r'xmin = ([\d.]+)\s+xmax = ([\d.]+)\s+text = "(.*)"',grid.read_text())
  reference=' '.join(re.sub('<[^>]+>','',text) for start,end,text in blocks if float(end)<=90 and text)
  (a.output/(case+'-reference.txt')).write_text(reference)
  start=time.perf_counter();segments=model.transcribe(str(clip));elapsed=time.perf_counter()-start
  (a.output/(case+'-asr.txt')).write_text(' '.join(s.text for s in segments))
  evidence.append({'case':case,'excerpt_seconds':[0,90],'reference_textgrid_sha256':hashlib.sha256(grid.read_bytes()).hexdigest(),'clip_sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'asr_elapsed_s':elapsed})
 (a.output/'asr_execution.json').write_text(json.dumps({'model':'Whisper.cpp tiny.en-q5_1','model_sha256':hashlib.sha256(a.model.read_bytes()).hexdigest(),'language':'en','threads':4,'excerpts':evidence},indent=2)+'\n')
if __name__=='__main__':main()
