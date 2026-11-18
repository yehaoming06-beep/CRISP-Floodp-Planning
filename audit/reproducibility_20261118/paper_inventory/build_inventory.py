from pathlib import Path
import subprocess,csv,json,hashlib,re,collections,urllib.parse
REPO=Path(__file__).resolve().parents[3]
SOURCE=Path('/Users/yehaoming/Desktop/climate_Devin')
OUT=Path(__file__).resolve().parent

def files(root):
 return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in {'.venv','.git','__pycache__','.pytest_cache','.DS_Store'} for x in p.relative_to(root).parts))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def csvout(name,rows):
 if not rows:return
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
tracked=set(subprocess.check_output(['git','ls-files','-z'],cwd=REPO).decode().split('\0'))-{''}
source_files=files(SOURCE)
rels=[p.relative_to(SOURCE).as_posix() for p in source_files]
r=subprocess.run(['git','check-ignore','--stdin','-z'],cwd=REPO,input='\0'.join(rels).encode()+b'\0',stdout=subprocess.PIPE)
ignored=set(r.stdout.decode().split('\0'))-{''}
rows=[]
for p,rel in zip(source_files,rels):
 rp=REPO/rel
 core=(rel.startswith(('01_Data/','02_Model/','03_Experiments/','05_Code/')) or rel in {'requirements-lock.txt','manuscript_revision/Supplementary_Methods_and_Results.md','manuscript_revision/CRISP_Merged_Manuscript.docx','manuscript_revision/audit/ci01_independent_20261104/analysis/reconstructed_model_input.csv'})
 s=sha(p) if core else ''
 rr=sha(rp) if core and rp.is_file() else ''
 rows.append({'source_relative_path':rel,'source_bytes':p.stat().st_size,'repo_present':rp.is_file(),'git_state':'TRACKED' if rel in tracked else 'IGNORED' if rel in ignored else 'UNTRACKED' if rp.is_file() else 'ABSENT_FROM_REPO','source_sha256_if_core':s,'repo_sha256_if_core':rr,'core_bytes_equal':s==rr if s and rr else ''})
csvout('source_to_repository_inventory.csv',rows)
csvout('original_only_files.csv',[r for r in rows if not r['repo_present']])
csvout('core_input_code_fingerprints.csv',[r for r in rows if r['source_sha256_if_core']])
summary={'source_root':str(SOURCE),'repo_root':str(REPO),'excluded_from_walk':['.venv','.git','__pycache__','.pytest_cache','.DS_Store'],'source_files':len(rows),'repo_counterparts':sum(r['repo_present'] for r in rows),'source_only':sum(not r['repo_present'] for r in rows),'source_repo_git_state':dict(collections.Counter(r['git_state'] for r in rows)),'tracked_repository_files':sorted(tracked),'fingerprinted_files':sum(bool(r['source_sha256_if_core']) for r in rows),'fingerprinted_equal':sum(r['core_bytes_equal'] is True for r in rows),'fingerprinted_mismatch':[r['source_relative_path'] for r in rows if r['core_bytes_equal'] is False]}
(OUT/'inventory_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
sections=[];linkrows=[]
for name in ['manuscript_revision/Supplementary_Methods_and_Results.md','supplementary/Supplementary_Methods_and_Results.md']:
 p=REPO/name;text=p.read_text();last=None
 for ln,line in enumerate(text.splitlines(),1):
  if m:=re.match(r'^## (S\d+) (.*)',line):
   last=m.group(1)
   if name.startswith('manuscript_revision'):sections.append({'section':last,'heading':m.group(2),'line':ln})
  for m in re.finditer(r'!?\[([^\]]*)\]\(([^)]+)\)',line):
   target=m.group(2)
   if re.match(r'^https?://',target):continue
   dest=target.split('#')[0]
   resolved=(p.parent/urllib.parse.unquote(dest)).resolve() if dest else p
   rel=resolved.relative_to(REPO).as_posix() if resolved.is_relative_to(REPO) else str(resolved)
   ir=subprocess.run(['git','check-ignore','-q',rel],cwd=REPO).returncode==0
   linkrows.append({'document':name,'section':last,'line':ln,'label':m.group(1),'target':target,'resolved':rel,'exists':resolved.exists(),'git_state':'TRACKED' if rel in tracked else 'IGNORED' if ir else 'UNTRACKED' if resolved.exists() else 'MISSING'})
 if name.startswith('manuscript_revision'):
  summary['supplement_sections']=len(sections)
  summary['supplement_table_numbers']=sorted(set(int(x) for x in re.findall(r'\*\*Table S(\d+)\.',text)))
  summary['supplement_figure_numbers']=sorted(set(int(x) for x in re.findall(r'\*\*Figure S(\d+)\.',text)))
csvout('supplement_sections.csv',sections);csvout('supplement_local_links.csv',linkrows)
summary['supplement_local_links']=len(linkrows);summary['supplement_missing_local_links']=[r for r in linkrows if not r['exists']]
(OUT/'inventory_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2))
