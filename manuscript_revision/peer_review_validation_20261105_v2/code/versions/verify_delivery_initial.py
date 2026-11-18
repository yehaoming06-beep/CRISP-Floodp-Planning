"""Final scientific-table, evidence-link and frozen-source delivery checks. No solving."""
import csv,hashlib,json,re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]
REPORTS=['Peer_Review_Issues.md','EV_Convention_Sensitivity.md','Controlled_Model_Ablation.md',
         'Methodological_Contribution_Matrix.md','Revised_Experiment_Recommendations.md']
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def read(p):return json.loads(p.read_text())
def csvrows(name):return list(csv.DictReader((BASE/'runs/primary'/name).open(encoding='utf-8-sig')))
def mdrows(name):
    return [[c.strip() for c in line.strip().strip('|').split('|')]
            for line in (BASE/name).read_text().splitlines() if line.startswith('|')]
def near(a,b):assert abs(float(a)-float(b))<=0.00000051,(a,b)

primary=read(BASE/'runs/primary/validation.json');ind=read(BASE/'independent_validation/verification.json')
assert primary['status']==ind['status']=='PASS'
assert primary['solves']==ind['solves_compared']==500 and primary['optimal']==ind['optimal']==498
assert ind['infeasible']==2 and ind['max_objective_error']<1e-6
assert read(BASE/'runs/primary/model_readback_verification.json')['models_read_successfully']==500
assert read(BASE/'assessment/Scenario_Chain_Audit.json')['status']=='PASS'
assert 'RESULTS_AND_SCOPE_PASS' in (BASE/'assessment/Post_Result_Review.md').read_text()

numeric_cells=0
ev=csvrows('ev_summary.csv')
for row in mdrows('EV_Convention_Sensitivity.md'):
    if not re.fullmatch(r'(23|60) (legacy|mobile)',row[0]):continue
    freq,model=row[0].split()
    pair=[r for r in ev if r['frequency']==freq and r['model']==model]
    assert len(pair)==2 and row[1]=='A=B'
    keys=['rp','ws','ev','selected_ev_n','selected_eev','selected_vss','ev_optimal_policy_count']
    for r in pair:
        for cell,key in zip(row[2:9],keys):near(cell,r[key]);numeric_cells+=1
        for cell,keys2 in zip(row[9:11],[('eev_min','eev_max'),('vss_min','vss_max')]):
            for value,key in zip(cell.split('–'),keys2):near(value,r[key]);numeric_cells+=1

component=csvrows('component_summary.csv')
prefixes={'F0':'F0_no_stock','F1':'F1_replicated_continuous','F2':'F2_shared_continuous',
          'F3':'F3_shared_integer','A1':'A1_access_O1_only','A2':'A2_access_O2_only'}
for row in mdrows('Controlled_Model_Ablation.md'):
    prefix=row[0].split()[0] if row else ''
    if prefix in prefixes and len(row)==5:
        for cell,(freq,budget) in zip(row[1:],[('23','2000000'),('60','2000000'),('23','6500000'),('60','6500000')]):
            r=next(r for r in component if r['frequency']==freq and r['capital_budget_hkd']==budget and r['case']==prefixes[prefix])
            near(cell,r['rp']);numeric_cells+=1
coverage=csvrows('coverage_summary.csv')
for row in mdrows('Controlled_Model_Ablation.md'):
    if row[0] not in ('23','60') or len(row)!=6:continue
    r=next(r for r in coverage if r['frequency']==row[0] and r['minimum_packages_each_location_each_scenario']==row[1])
    assert row[2]==r['status']
    if r['status']=='OPTIMAL':
        for cell,key in zip(row[3:],['rp','delta_vs_no_coverage','n']):near(cell,r[key]);numeric_cells+=1
    else:assert row[3:]==['不存在','不适用','不适用']

broken=[];link_count=0
for filename in REPORTS+['README.md']:
    content=(BASE/filename).read_text()
    for link in re.findall(r'\]\(([^)]+)\)',content):
        if re.match(r'https?://',link):continue
        target=link.split('#')[0]
        if not target:continue
        link_count+=1
        if not (BASE/target).exists():broken.append({'report':filename,'target':target})
assert not broken,broken

gate=read(BASE/'assessment/Execution_Gate_Record.json')
for path,h in gate['sha256'].items():assert sha(ROOT/path)==h,path
assert sha(BASE/'code/run_validation.py')==read(BASE/'runs/primary/run_manifest.json')['code_sha256']
assert sha(BASE/'code/verify_independent.py')==ind['code_sha256']
assert sha(BASE/'code/versions/verify_independent_initial.py')==ind['initial_numerical_audit_code_sha256']
old=read(BASE/'frozen_manifest_before.json')
assert not any('peer_review_validation_20261105_v1/' in p for p in old)
changed=[p for p,h in old.items() if not (ROOT/p).exists() or sha(ROOT/p)!=h]
assert not changed,changed
summary={'status':'PASS','date_time':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
    'required_reports':REPORTS,'table_numeric_cells_checked':numeric_cells,'local_report_links_checked':link_count,
    'broken_links':broken,'original_scientific_files_hashed':len(old),'changed_or_missing_original_files':changed,
    'v1_results_read_or_used':False,'primary_solver_calls':500,'independent_solver_calls':ind['independent_milp_calls'],
    'primary_optimal':498,'primary_expected_infeasible':2,'max_cross_solver_objective_error':ind['max_objective_error'],
    'all_execution_gate_code_hashes_match':True,'post_result_review':'PASS','empirical_calibration':False,
    'CI-01':'PARTIALLY RESOLVED / NOT FULLY CLOSED','CI-06':'OPEN'}
(BASE/'Final_Delivery_Verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
excluded={'Artifact_Manifest.json','Final_Delivery_Verification.json'}
inventory={str(p.relative_to(BASE)):{'sha256':sha(p),'bytes':p.stat().st_size}
           for p in sorted(BASE.rglob('*')) if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts}
(BASE/'Artifact_Manifest.json').write_text(json.dumps({'files':inventory,'metadata_excluded_from_self_hash':sorted(excluded)},ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False))
