"""Archive public HKO evidence; never write outside this independent audit."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse, hashlib, json, shutil, subprocess, urllib.parse

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[2]
WEB = OUT / 'sources/web'
LOG = OUT / 'logs/retrieval.jsonl'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def snapshot():
    manifest = []
    for folder in ['01_Data','02_Model','03_Experiments','04_Results','05_Code','06_Manuscript']:
        for src in sorted((ROOT/folder).rglob('*')):
            if not src.is_file() or '__pycache__' in src.parts or src.name == '.DS_Store': continue
            rel = src.relative_to(ROOT); dest = OUT/'snapshots'/rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists(): shutil.copy2(src, dest)
            assert sha(src) == sha(dest), rel
            manifest.append(dict(path=str(rel),snapshot=str(dest.relative_to(OUT)),bytes=src.stat().st_size,sha256=sha(src)))
    for src in sorted((ROOT/'manuscript_revision').glob('*')):
        if not src.is_file() or src.name == '.DS_Store': continue
        rel=src.relative_to(ROOT);dest=OUT/'snapshots'/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():shutil.copy2(src,dest)
        assert sha(src)==sha(dest)
        manifest.append(dict(path=str(rel),snapshot=str(dest.relative_to(OUT)),bytes=src.stat().st_size,sha256=sha(src)))
    (OUT/'logs/frozen_inputs_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    previous=ROOT/'manuscript_revision/audit/fixes_20261104'
    for name in ['sources','source_pages']:
        shutil.copytree(previous/name,OUT/'sources/prior_fix'/name,dirs_exist_ok=True)
    for name in ['retrieval_log.json','range_download_log.json','Event_Source_Updates.csv','tide_source_checks_current.json','monthly_table_extraction.json']:
        shutil.copy2(previous/name,OUT/'sources/prior_fix'/name)
    old=ROOT/'manuscript_revision/audit/evidence_consistency_20261104'
    for name in ['primary_fetch_log.json','rainfall_recalculation.json','station_substitution_evidence.json','tide_source_checks.json']:
        shutil.copy2(old/name,OUT/'sources'/('prior_'+name))
    print('Frozen input snapshots:',len(manifest),flush=True)

def fetch(job):
    name,url=job
    if urllib.parse.urlsplit(url).hostname not in {'www.hko.gov.hk','www.weather.gov.hk','data.weather.gov.hk'}:
        raise ValueError('Only public HKO sources are permitted')
    dest=WEB/name;dest.parent.mkdir(parents=True,exist_ok=True)
    record=dict(name=name,url=url,retrieved_utc=datetime.now(timezone.utc).isoformat())
    previous=[json.loads(s) for s in LOG.read_text().splitlines() if s.strip()] if LOG.exists() else []
    verified=any(r.get('name')==name and r.get('http_status')=='200' and r.get('sha256')==sha(dest) for r in previous) if dest.exists() else False
    if dest.exists() and dest.stat().st_size>0 and verified:
        record.update(status='REUSE_EXISTING_SNAPSHOT',path=str(dest.relative_to(OUT)),bytes=dest.stat().st_size,sha256=sha(dest))
        return record
    if dest.exists():
        historic=WEB/'history'/(name+'.'+sha(dest));historic.parent.mkdir(exist_ok=True)
        if not historic.exists():shutil.copy2(dest,historic)
    headers=OUT/'logs'/(name.replace('/','_')+'.headers')
    proc=subprocess.run(['/usr/bin/curl','--location','--max-time','30','--silent','--show-error','--dump-header',str(headers),'--output',str(dest),'--write-out','%{http_code}\n%{url_effective}\n%{size_download}',url],capture_output=True,text=True)
    parts=proc.stdout.splitlines()
    record.update(returncode=proc.returncode,stderr=proc.stderr,headers=str(headers.relative_to(OUT)))
    if parts:record['http_status']=parts[0]
    if len(parts)>1:record['final_url']=parts[1]
    if dest.exists():record.update(path=str(dest.relative_to(OUT)),bytes=dest.stat().st_size,sha256=sha(dest))
    record['status']='COMPLETE_TRANSFER' if proc.returncode==0 and parts and parts[0]=='200' else 'UNAVAILABLE'
    return record

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--snapshot',action='store_true');ap.add_argument('--jobs',type=Path);args=ap.parse_args()
    if args.snapshot:snapshot()
    if args.jobs:jobs=json.loads(args.jobs.read_text())
    else:
        jobs=[(f'HKO_{y}_{page}.html',f'https://www.hko.gov.hk/en/publica/tc/tc{y}/{page}.html') for y in range(2017,2026) for page in ['table41','table42','table43','section3','content']]
        jobs += [('HKO_2025.htm','https://www.hko.gov.hk/en/informtc/tc2025.htm'),('HKO_warning_database.html','https://www.hko.gov.hk/en/wxinfo/climat/warndb/warndb1.shtml'),('HKO_daily_R11_2025.xml','https://www.hko.gov.hk/cis/aws/individual_day/daily_R11_2025.xml'),('HKO_daily_R11_2025.htm','https://www.hko.gov.hk/en/cis/dailyExtract.htm?y=2025&m=1')]
    with ThreadPoolExecutor(max_workers=5) as pool:
        for rec in pool.map(fetch,jobs):
            with LOG.open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
            print(rec['name'],rec['status'],rec.get('http_status'),rec.get('bytes'),flush=True)

if __name__=='__main__':main()
