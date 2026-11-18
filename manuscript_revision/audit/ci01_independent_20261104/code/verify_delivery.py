"""Independent arithmetic, deterministic replay, input guard, and delivery QA."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,importlib.metadata,json,math,subprocess,sys
import numpy as np
import pandas as pd
from reconstruct import OUT,SNAP,COLS,dump
ROOT=OUT.parents[2]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def exact_dp(h,k=3):
    x=np.sort(h);n=len(x);a=np.r_[0,np.cumsum(x)];b=np.r_[0,np.cumsum(x*x)]
    dp=np.full((k+1,n+1),np.inf);dp[0,0]=0
    for c in range(1,k+1):
        for end in range(c,n+1):
            dp[c,end]=min(dp[c-1,start]+b[end]-b[start]-(a[end]-a[start])**2/(end-start) for start in range(c-1,end))
    return float(dp[k,n])

def main():
    report={};manifest=json.loads((OUT/'logs/frozen_inputs_manifest.json').read_text())
    changed=[r['path'] for r in manifest if sha(ROOT/r['path'])!=r['sha256'] or sha(OUT/r['snapshot'])!=r['sha256']]
    report['frozen_input_guard']=dict(files=len(manifest),changed=changed,unchanged=not changed)
    assert not changed
    inv=pd.read_csv(OUT/'Candidate_Event_Inventory.csv');audit=pd.read_csv(OUT/'Inclusion_Exclusion_Audit.csv')
    comp=pd.read_csv(OUT/'Original23_vs_Reconstructed.csv');data=pd.read_csv(OUT/'analysis/reconstructed_model_input.csv')
    assert inv.candidate_id.is_unique and audit.candidate_id.is_unique and comp.candidate_id.is_unique
    assert set(inv.candidate_id)==set(audit.candidate_id)==set(comp.candidate_id)
    assert len(inv)==63 and inv.hko_warning_group_id.nunique()==62
    assert len(data)==60 and len(audit[audit.screening_status.eq('PENDING_DATA')])==3
    assert set(data.event_id)==set(audit.loc[audit.model_eligible,'candidate_id'])
    assert not audit.is_entity_exclusion.any()
    assert audit.loc[~audit.model_eligible,['model_R_mm_day','model_W_mCD','model_S_m']].isna().all().all()
    assert audit.loc[audit.secondary_source_QC.eq('PENDING_SOURCE_CONFLICT'),'screening_status'].eq('PENDING_DATA').all()
    assert audit.loc[audit.secondary_source_QC.eq('PEAK_TIME_CONFLICT_UNRESOLVED'),'model_eligible'].all()
    originals=comp[comp.comparison_type.eq('ORIGINAL_EVENT')]
    assert len(originals)==23 and originals.original_event_id.nunique()==23
    assert originals[['delta_R_mm_day','delta_W_mCD','delta_S_m']].eq(0).all().all()
    assert originals.reconstructed_status.eq('INCLUDE').all()
    checks=json.loads((OUT/'evidence/Candidate_Completeness_Check.json').read_text())
    assert len(checks)==9 and all(r['exact_segment_match'] for r in checks)
    report['candidate_integrity']=dict(candidate_cyclones=63,warning_groups=62,warning_segments=sum(r['database_segments'] for r in checks),crosscheck_years=9,final_analysis_N=60,pending=3,entity_exclusions=0,original23_vectors_unchanged=True)
    impact=json.loads((OUT/'analysis/scenario_impact.json').read_text());mainfit=impact['fits'][impact['main_fit']]
    arithmetic=[]
    for name,matrix in [('original23_frozen',pd.read_csv(SNAP/'01_Data/Events/model_input.csv')),(impact['main_fit'],data)]:
        x=matrix[COLS].values;z=(x-x.min(0))/np.ptp(x,axis=0)
        information=z.std(0,ddof=0)*np.sum(1-np.corrcoef(z,rowvar=False),axis=1);w=information/information.sum()
        saved=impact['fits'][name];assert np.allclose(w,saved['weights'],rtol=0,atol=1e-14)
        sse=exact_dp(z@w);assert abs(sse-saved['kmeans_sse'])<1e-10
        arithmetic.append(dict(dataset=name,max_weight_error=float(np.max(abs(w-saved['weights']))),independent_DP_SSE=sse,reported_SSE=saved['kmeans_sse'],nonempty_contiguous_K3_partitions=math.comb(len(matrix)-1,2)))
    report['independent_arithmetic']=arithmetic
    # Stable scenario outputs and all data-evidence tables must reproduce byte-for-byte.
    targets=[OUT/f for f in ['Candidate_Event_Inventory.csv','Inclusion_Exclusion_Audit.csv','Original23_vs_Reconstructed.csv','Supplemental_TaiO_Observations.csv']]
    targets += [p for folder in ['analysis','evidence'] for p in (OUT/folder).rglob('*') if p.is_file()]
    hashes={str(p.relative_to(OUT)):sha(p) for p in targets}
    for script in ['reconstruct.py','assess_scenarios.py','verify_tides_and_spatial.py']:
        log=OUT/'logs'/('replay_'+script.replace('.py','.log'))
        with log.open('w') as f:subprocess.run([sys.executable,str(OUT/'code'/script)],stdout=f,stderr=subprocess.STDOUT,check=True)
    changed_replay=[rel for rel,digest in hashes.items() if sha(OUT/rel)!=digest]
    assert not changed_replay,changed_replay
    report['offline_deterministic_replay']=dict(files_compared=len(hashes),byte_identical=True,changed=changed_replay)
    first=OUT/'backend_probability60/summary.csv';repeat=OUT/'backend_probability60_replay/summary.csv'
    assert first.read_bytes()==repeat.read_bytes()
    backend=json.loads((OUT/'backend_probability60/validation.json').read_text());repeat_validation=json.loads((OUT/'backend_probability60_replay/validation.json').read_text())
    assert backend['configurations']==repeat_validation['configurations']==555
    for r in [backend,repeat_validation]:assert r['all_recorded_solver_statuses_optimal'] and r['all_existing_feasibility_and_information_value_checks_passed']
    ev=json.loads((OUT/'backend_probability60/ev_tie_verification.json').read_text());assert ev['status']=='PASS'
    report['backend_replay']=dict(configurations_per_run=555,all_555_summary_rows_byte_identical=True,summary_sha256=sha(first),solver_audit_rows_per_run=backend['solver_audit_rows'],EV_tie_audit=ev,scope='probability-only conditional sensitivity; no empirical remapping of scenario coefficients')
    pdfs=[]
    for path in list((OUT/'sources/pdf').glob('*.pdf'))+list((OUT/'sources/prior_fix/sources').glob('HKO_MWS*.pdf')):
        rec=json.loads(path.with_suffix('.preflight.json').read_text())
        assert rec['verdict']=='PASS' and rec['sha256']==sha(path)
        pdfs.append(dict(path=str(path.relative_to(OUT)),pages=rec['reader_page_count'],sha256=sha(path),verdict=rec['verdict']))
    report['PDF_integrity']=pdfs
    report['final_status']='PASS_WITH_EXPLICIT_UNRESOLVED_CI01_ITEMS'
    report['CI01_fully_closed']=False
    report['timestamp_utc']=datetime.now(timezone.utc).isoformat()
    dump('logs/Final_Verification.json',report)
    versions={name:importlib.metadata.version(name) for name in ['numpy','pandas','scipy','scikit-learn','threadpoolctl','PyYAML','openpyxl','pypdf','gurobipy']}
    dump('logs/exact_environment_versions.json',dict(python=sys.version,packages=versions))
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
