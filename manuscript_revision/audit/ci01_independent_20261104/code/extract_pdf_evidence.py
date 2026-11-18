"""Preflight, extract, and render complete 2025 official monthly evidence."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
from pypdf import PdfReader

OUT=Path(__file__).resolve().parents[1]
PREFLIGHT=Path(__file__).resolve().parent/'vendor/pdf_read_preflight.py'
def main():
    all_pages=[]
    for month in [6,7,8,9,10,11]:
        stem=f'HKO_MWS2025{month:02}'
        path=OUT/'sources/pdf'/f'{stem}.pdf'
        if not path.exists():path=OUT/'sources/prior_fix/sources'/f'{stem}.pdf'
        sidecar=path.with_suffix('.preflight.json')
        if not sidecar.exists():subprocess.run([sys.executable,str(PREFLIGHT),str(path),'--output',str(sidecar)],check=True)
        pre=json.loads(sidecar.read_text());assert pre['verdict']=='PASS' and pre['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
        doc=PdfReader(path)
        targets=[]
        for i,page in enumerate(doc.pages,1):
            text=page.extract_text()
            dest=OUT/'sources/pdf_text'/f'{stem}_p{i:03}.txt';dest.parent.mkdir(exist_ok=True);dest.write_text(text)
            if re.search(r'Shek\s+Pik',text,re.I) and re.search(r'(storm\s+surge|sea\s+level\s+rise)',text,re.I):
                lines=text.splitlines()
                sp=[s.strip() for s in lines if re.search(r'Shek\s+Pik',s,re.I)]
                rec=dict(month=month,pdf=str(path.relative_to(OUT)),sha256=pre['sha256'],pdf_page=i,printed_page=lines[-1].strip() if lines else '',Shek_Pik_lines=sp,text_file=str(dest.relative_to(OUT)),url=f'https://www.hko.gov.hk/en/publica/mws/files/mws2025{month:02}.pdf#page={i}')
                image=OUT/'sources/page_images'/f'{stem}_p{i:03}';image.parent.mkdir(exist_ok=True)
                subprocess.run(['pdftoppm','-f',str(i),'-l',str(i),'-scale-to','1500','-png','-singlefile',str(path),str(image)],check=True,capture_output=True)
                rec['image']=str(image.with_suffix('.png').relative_to(OUT));targets.append(rec)
        all_pages+=targets;print(stem,'pages',len(doc.pages),'target tables',len(targets),flush=True)
    (OUT/'sources/pdf_table_pages.json').write_text(json.dumps(all_pages,ensure_ascii=False,indent=2))
    for r in all_pages:print(r['month'],r['pdf_page'],r['Shek_Pik_lines'],flush=True)

if __name__=='__main__':main()
