"""Re-execute frozen offline screening logic in an independent output stage.
No network requests, source edits, QC adjudications, PDF extraction or visual review.
"""
from pathlib import Path
import sys,subprocess,importlib.util,hashlib,csv,json,shutil,platform,contextlib,io,time,math
sys.dont_write_bytecode=True
REPO=Path(__file__).resolve().parents[3]
BASE=REPO/'manuscript_revision/audit/ci01_independent_20261104'
ROOT=Path(__file__).resolve().parent
STAGE=ROOT/'stage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,x):
 (ROOT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
def writecsv(name,rows):
 if not rows:return
 with (ROOT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if STAGE.exists():raise RuntimeError('Refusing to overwrite an existing reconstruction stage')
STAGE.mkdir()
files=[p.relative_to(BASE).as_posix() for p in sorted((BASE/'sources/web').rglob('*')) if p.is_file()]
files += [p.relative_to(BASE).as_posix() for p in sorted((BASE/'snapshots/01_Data/Sources/HKO/r11_daily').glob('*.json'))]
files += ['snapshots/01_Data/Events/event_metadata.csv','Screening_Protocol.md','Source_Conflict_Adjudication.md','logs/protocol_freeze.json','logs/qc_protocol_freeze.json','evidence/QC_Adjudication.json','sources/pdf_table_pages.json']
pages=json.loads((BASE/'sources/pdf_table_pages.json').read_text())
files += [r['pdf'] for r in pages]+[r['text_file'] for r in pages]
files=sorted(set(files))
manifest=[]
for rel in files:
 s=BASE/rel;t=STAGE/rel
 if not s.is_file():raise FileNotFoundError(s)
 if s.is_symlink():raise RuntimeError(f'Symlink source not accepted: {s}')
 t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(s,t)
 actual=sha(t);expected=sha(s)
 if actual!=expected:raise RuntimeError(f'Copy checksum mismatch: {rel}')
 manifest.append({'relative_path':rel,'source_path':str(s),'stage_path':str(t),'bytes':s.stat().st_size,'source_sha256':expected,'copied_sha256':actual,'same':True})
writecsv('copied_input_manifest.csv',manifest)
code_paths=[BASE/'code/reconstruct.py',BASE/'code/hko_parse.py',Path(__file__).resolve()]
dump('code_manifest.json',[{'path':str(p),'sha256':sha(p)} for p in code_paths])
outputs=['Candidate_Event_Inventory.csv','Inclusion_Exclusion_Audit.csv','Original23_vs_Reconstructed.csv','analysis/reconstructed_model_input.csv','analysis/screening_summary.json','evidence/Warning_Segments.csv','evidence/Candidate_Completeness_Check.json','evidence/Overlapping_Windows.csv','evidence/Rainfall_Station_Window_Details.json','evidence/Tide_Table_Extraction.json','evidence/Rainfall_Redownload_Comparison.json']
reference_before={rel:sha(BASE/rel) for rel in outputs}
dump('reference_output_hashes_before.json',reference_before)
env={'python_executable':sys.executable,'python_version':sys.version,'platform':platform.platform(),'working_directory':str(REPO),'command':[sys.executable,str(Path(__file__).resolve())],'network':'No network calls in original reconstruct.py or hko_parse.py; archived source replay only','copied_inputs':len(manifest),'copied_bytes':sum(r['bytes'] for r in manifest),'pdf_files_copied':len(set(r['pdf'] for r in pages)),'pdf_page_texts_copied':len(set(r['text_file'] for r in pages)),'images_copied':0,'portability_adaptation':'Import unchanged original reconstruct.py and hko_parse.py; rebind only OUT/SNAP/WEB to isolated stage. Source content and algorithm unchanged.','inherited_content_caveat':'Generated Tide_Table_Extraction.json includes historical visual_check text dated 2026-11-04. This run inherits those fields and historical extracted page text; no new PDF extraction, image inspection, live download, independent QC decision, or resolution of pending conflicts is claimed.'}
dump('execution_environment.json',env)
sys.path.insert(0,str(BASE/'code'))
spec=importlib.util.spec_from_file_location('crisp_offline_reconstruction_original',BASE/'code/reconstruct.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.OUT=STAGE;m.SNAP=STAGE/'snapshots';m.WEB=STAGE/'sources/web'
stdout=io.StringIO();started=time.perf_counter()
try:
 with contextlib.redirect_stdout(stdout):m.main()
except BaseException as exc:
 (ROOT/'execution_stdout.log').write_text(stdout.getvalue())
 dump('execution_failure.json',{'status':'BLOCKED','exception':repr(exc),'elapsed_seconds':time.perf_counter()-started})
 raise
elapsed=time.perf_counter()-started
(ROOT/'execution_stdout.log').write_text(stdout.getvalue())
comparisons=[];diffs=[]
for rel in outputs:
 a=BASE/rel;b=STAGE/rel
 row={'relative_path':rel,'reference_sha256':sha(a),'rerun_sha256':sha(b),'byte_identical':a.read_bytes()==b.read_bytes(),'reference_rows':None,'rerun_rows':None,'row_order_identical':None,'different_cells':0,'max_numeric_absolute_error':0.0,'parsed_equal':False}
 if a.suffix=='.csv':
  ar=list(csv.DictReader(a.open(encoding='utf-8-sig')));br=list(csv.DictReader(b.open(encoding='utf-8-sig')))
  row['reference_rows']=len(ar);row['rerun_rows']=len(br);row['row_order_identical']=ar==br;row['parsed_equal']=ar==br
  if len(ar)!=len(br):diffs.append({'relative_path':rel,'row':None,'column':'ROW_COUNT','reference':len(ar),'rerun':len(br),'numeric_absolute_error':None})
  for i,(aa,bb) in enumerate(zip(ar,br),1):
   for k in dict.fromkeys(list(aa)+list(bb)):
    v,w=aa.get(k),bb.get(k)
    try:err=abs(float(v)-float(w)) if math.isfinite(float(v)) and math.isfinite(float(w)) else None
    except (ValueError,TypeError):err=None
    if err is not None:row['max_numeric_absolute_error']=max(row['max_numeric_absolute_error'],err)
    if v!=w:
     row['different_cells']+=1;diffs.append({'relative_path':rel,'row':i,'column':k,'reference':v,'rerun':w,'numeric_absolute_error':err})
 elif a.suffix=='.json':row['parsed_equal']=json.loads(a.read_text())==json.loads(b.read_text())
 comparisons.append(row)
writecsv('output_comparison.csv',comparisons)
if diffs:writecsv('cell_differences.csv',diffs)
else:(ROOT/'cell_differences.csv').write_text('relative_path,row,column,reference,rerun,numeric_absolute_error\n')
source_unchanged=all(sha(BASE/r['relative_path'])==r['source_sha256'] for r in manifest)
reference_unchanged=all(sha(BASE/rel)==h for rel,h in reference_before.items())
summary=json.loads((STAGE/'analysis/screening_summary.json').read_text())
result={'status':'REPRODUCED_FROZEN_OFFLINE_RECONSTRUCTION' if all(r['parsed_equal'] for r in comparisons) and source_unchanged and reference_unchanged else 'FAIL','elapsed_seconds':elapsed,'copied_input_count':len(manifest),'copied_input_bytes':sum(r['bytes'] for r in manifest),'all_11_outputs_byte_identical':all(r['byte_identical'] for r in comparisons),'all_11_outputs_parsed_equal':all(r['parsed_equal'] for r in comparisons),'core_target_rows':{r['relative_path']:r['rerun_rows'] for r in comparisons if r['relative_path'] in {'Candidate_Event_Inventory.csv','Inclusion_Exclusion_Audit.csv','analysis/reconstructed_model_input.csv'}},'different_cells':len(diffs),'maximum_numeric_absolute_error':max(r['max_numeric_absolute_error'] for r in comparisons),'source_copies_unchanged_after_run':source_unchanged,'reference_outputs_unchanged_after_run':reference_unchanged,'screening_summary':summary,'interpretation_limit':env['inherited_content_caveat']}
dump('validation.json',result)
print(json.dumps(result,ensure_ascii=False,indent=2))
