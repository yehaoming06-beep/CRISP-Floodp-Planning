"""Archive complete public HKO monthlies using verified HTTP byte ranges."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import argparse,hashlib,json,re,subprocess

OUT=Path(__file__).resolve().parents[1]
PDF=OUT/'sources/pdf';PDF.mkdir(exist_ok=True)
RANGES=OUT/'sources/ranges';RANGES.mkdir(exist_ok=True)
BLOCK=1048576

def get(job):
    name,url,start,end,total=job
    path=RANGES/f'{name}_{start}_{end}.part';header=path.with_suffix('.headers')
    attempts=[]
    for attempt in range(1,4):
        r=dict(name=name,url=url,start=start,end=end,attempt=attempt,retrieved_utc=datetime.now(timezone.utc).isoformat())
        p=subprocess.run(['/usr/bin/curl','-L','--max-time','30','--silent','--show-error','--range',f'{start}-{end}','--dump-header',str(header),'--output',str(path),'--write-out','%{http_code}',url],capture_output=True,text=True)
        text=header.read_text() if header.exists() else ''
        match=re.findall(r'content-range:\s*bytes (\d+)-(\d+)/(\d+)',text,re.I)
        lm=re.findall(r'last-modified:\s*([^\r\n]+)',text,re.I)
        r.update(http_status=p.stdout,returncode=p.returncode,stderr=p.stderr,content_range=match[-1] if match else None,last_modified=lm[-1] if lm else None)
        ok=p.returncode==0 and p.stdout=='206' and match and tuple(map(int,match[-1][:2]))==(start,end)
        ok=ok and (total is None or int(match[-1][2])==total) and path.stat().st_size==end-start+1
        r.update(status='VALID_RANGE' if ok else 'FAILED',bytes=path.stat().st_size if path.exists() else 0)
        if path.exists():r['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        attempts.append(r)
        if ok:return r,path,attempts
    return r,None,attempts

def main():
    logs=[];results=[]
    ap=argparse.ArgumentParser();ap.add_argument('--period',action='append');args=ap.parse_args()
    periods=args.period or ['202506','202508','202510','202511']
    for period in periods:
        assert re.fullmatch(r'20\d{4}',period)
        name=f'HKO_MWS{period}';url=f'https://www.hko.gov.hk/en/publica/mws/files/mws{period}.pdf'
        final=PDF/f'{name}.pdf'
        if final.exists():print(name,'existing complete file',flush=True);continue
        first,path,attempts=get((name,url,0,BLOCK-1,None));logs+=attempts
        if path is None:results.append(dict(name=name,status='UNAVAILABLE'));continue
        total=int(first['content_range'][2]);parts={0:path};records=[first]
        jobs=[(name,url,start,min(start+BLOCK-1,total-1),total) for start in range(BLOCK,total,BLOCK)]
        with ThreadPoolExecutor(max_workers=6) as pool:
            for fut in as_completed([pool.submit(get,job) for job in jobs]):
                rec,p,ats=fut.result();logs+=ats;records.append(rec)
                if p:parts[rec['start']]=p
        ok=len(parts)==1+len(jobs) and len({r['last_modified'] for r in records})==1 and all(r['status']=='VALID_RANGE' for r in records)
        result=dict(name=name,url=url,complete=ok,total_bytes=total)
        if ok:
            payload=b''.join(parts[k].read_bytes() for k in sorted(parts));assert len(payload)==total and payload.startswith(b'%PDF-') and b'%%EOF' in payload[-2048:]
            final.write_bytes(payload);result.update(path=str(final.relative_to(OUT)),sha256=hashlib.sha256(payload).hexdigest())
        results.append(result)
        logname='pdf_download_'+'_'.join(periods)+'.json'
        (OUT/'logs'/logname).write_text(json.dumps(dict(snapshots=results,attempts=logs),indent=2))
        print(name,ok,total,flush=True)
    print(json.dumps(results,indent=2),flush=True)

if __name__=='__main__':main()
