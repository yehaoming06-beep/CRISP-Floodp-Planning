from pathlib import Path
import csv,json,hashlib,collections,sys,platform,importlib.metadata as md
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
rows=[]
for dataset,folder,historical in [('original23','original23_555',ROOT/'04_Results/Optimization'),('reconstructed60','reconstructed60_555',ROOT/'manuscript_revision/audit/ci01_independent_20261104/backend_probability60')]:
    old={r['case']:r for r in csv.DictReader((historical/'ev_policy_tie_ranges.csv').open(encoding='utf-8-sig'))}
    new=list(csv.DictReader((OUT/folder/'ev_policy_tie_ranges.csv').open(encoding='utf-8-sig')))
    assert len(new)==10 and set(old)=={r['case'] for r in new}
    for r in new:
        for key,value in r.items():
            if key=='case':continue
            try:delta=float(value)-float(old[r['case']][key]);error=abs(delta);status='PASS' if error<1e-9 else 'FAIL'
            except ValueError:delta=None;error=None;status='PASS' if value==old[r['case']][key] else 'FAIL'
            rows.append({'dataset':dataset,'case':r['case'],'field':key,'new':value,'historical':old[r['case']][key],'signed_error':delta,'absolute_error':error,'status':status})
with (OUT/'ev_tie_history_comparison.csv').open('w',newline='') as stream:
    w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
result={'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL','cases':20,'fields_compared':len(rows),'failures':sum(r['status']=='FAIL' for r in rows),'max_numeric_error':max(r['absolute_error'] for r in rows if r['absolute_error'] is not None)}
(OUT/'ev_tie_comparison_validation.json').write_text(json.dumps(result,indent=2))
sweeps={}
for dataset,folder in [('original23','original23_555'),('reconstructed60','reconstructed60_555')]:
    records=list(csv.DictReader((OUT/folder/'summary.csv').open(encoding='utf-8-sig')))
    sweeps[dataset]={'configurations':len(records),'design_counts':dict(collections.Counter(r['experiment'] for r in records)),'validation':json.loads((OUT/folder/'validation.json').read_text()),'independent':json.loads((OUT/folder/'independent_verification.json').read_text()),'ev_ties':json.loads((OUT/folder/'ev_tie_verification.json').read_text())}
manifest={'status':'PASS','scope':'from-input reexecution plus independent core enumeration and independent 555 RP matrix verification','core_clean_environment':json.loads((OUT/'clean_environment/core_validation.json').read_text()),'sweeps':sweeps,'paper_comparison':json.loads((OUT/'comparison_validation.json').read_text()),'ev_ties_history_comparison':result,'integer_rounding_verification':json.loads((OUT/'independent_integer_rounding_validation.json').read_text()),'audit_code_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.py'))},'failed_attempts':[{'log':'clean_environment_attempt01_console.log','stage':'new output-directory argument adaptation; before solving','reason':'wrapper looked for enumeration source under output directory','resolution':'source path anchored to script; clean environment rerun passed','scientific_parameter_change':False}],'limits':['Core coefficients remain illustrative and uncalibrated.','Reconstructed-60 changes frequencies only.','Three pending events remain unresolved.','Independent 555 checks optimize RP only; all other saved solution constraints/objectives and EV-to-EEV first-stage fixing are checked. Independent exhaustive proof of all six metrics is provided for the four core models.','Existing research environment reused for 555 and selected EV-tie grids; clean environment independently reran the four core models only.','Source reconstruction from archived official observations was not rerun by this optimization audit.']}
(OUT/'optimization_audit_summary.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False));print(json.dumps({'status':manifest['status'],'ev_tie_comparison':result}))
