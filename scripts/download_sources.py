"""Fetch only the pinned public benchmark files. No gated datasets or mirrors.
Existing files are accepted only when their Git blob hashes match.
"""
import base64
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
FILES=[
 ('lemuria-wchen/imcs21','e4b5c380544488c5a409ffd84a5e8573fa77ab2c','imcs-dev.json'),
 ('lemuria-wchen/imcs21','501a3f6008980cd96eeffd58ba0090d27101675a','imcs-train.json'),
 ('lemuria-wchen/imcs21','4e61784d2d51bfa95a61cd65355cd2eb47acdc00','imcs-symptom_norm.csv'),
 ('microsoft/clinical_visit_note_summarization_corpus','6a87218334f321eda481a0845dfe13077ba1aea0','MTS_Dataset_ValidationSet.csv'),
 ('abachaa/MEDEC','8bddb55ca19e09399913544ab42602465321b339','MEDEC-MS-ValidationSet-with-GroundTruth-and-ErrorType.csv'),
 ('pubmedqa/pubmedqa','38db7750761c78950ed32303e7545bdaa513390c','pubmedqa.json'),
 ('Franck-Dernoncourt/pubmed-rct','30b4dabf34ef8a47d19363e86f5cb1308222c43d','rct-dev.txt'),
 ('Zhihong-Zhu/CMedCalc-Bench','fd9a8d8b05bf18fd20543926a25dc13f665195bf','cmedcalc-semantic.json'),
 ('Zhihong-Zhu/CMedCalc-Bench','bf7b07bcb72627e0b5495278a195327aab12ad8a','cmedcalc-faithful.json'),
 ('Zhihong-Zhu/CMedCalc-Bench','aa291e900087014cfd6f70158e0e9dde51304124','cmedcalc-equation.json'),
 ('Zhihong-Zhu/CMedCalc-Bench','cca36eb981e81a7991284405b9ba650d9f0a9562','cmedcalc-score.json'),
 ('isegura/DDICorpus','843a06b12c0d1e9448436eceba6efa6a9f63592d','ddi2013.zip'),
 ('kbressem/LongHealth','76bf80d37f321408a0e3f421a2e2d7ef59e97c1e','longhealth.json'),
 ('Medical-AI-Learning/MedJourney','c3c8432957d32a9dff12aec9ae8a71f687c96f2a','medjourney-dr.json'),
 ('borororo/zy-bert','4ad8f687eaf95de7b335c4370ea5e14f12b5efa7','tcm-train-dev.zip'),
 ('borororo/zy-bert','1334879e6eccacd0de4a6711d08eab6dde0c74b0','tcm-test.json'),
]
def blobsha(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'medical-benchmark-research'}),timeout=120) as r:return r.read()
def main():
 DATA.mkdir(parents=True,exist_ok=True)
 for repo,digest,name in FILES:
  dest=DATA/name
  if dest.exists() and blobsha(dest.read_bytes())==digest:
   print(name,'verified existing');continue
  obj=json.loads(fetch(f'https://api.github.com/repos/{repo}/git/blobs/{digest}'))
  raw=base64.b64decode(obj['content']);assert blobsha(raw)==digest
  temp=dest.with_suffix('.partial');temp.write_bytes(raw);temp.replace(dest);print(name,'downloaded verified')
 # Organizer's pinned ZIP member; no extraction to arbitrary paths.
 dest=DATA/'nli4ct.zip'
 manifest=Path(__file__).with_name('manifest.json')
 expected=json.loads(manifest.read_text())['source_files']['nli4ct.zip']['sha256']
 if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest()==expected:
  print('nli4ct.zip verified existing');return
 repo='https://codeload.github.com/ai-systems/nli4ct/zip/8e8e5fc506b916984011873403b9ea5ed6dd96c2'
 with zipfile.ZipFile(io.BytesIO(fetch(repo))) as archive:
  members=[n for n in archive.namelist() if n.endswith('Complete_dataset.zip')]
  if len(members)!=1:raise ValueError('Unexpected NLI4CT archive members')
  raw=archive.read(members[0])
 assert hashlib.sha256(raw).hexdigest()==expected
 dest.write_bytes(raw);print('nli4ct.zip downloaded verified')
if __name__=='__main__':main()
