"""Audit frequency-only contract and existing scenario evidence; no refitting/solving."""
import csv,hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]; SNAP=BASE/'snapshots'
PREFIX='manuscript_revision/audit/ci01_independent_20261104/'
def read(rel): return json.loads((SNAP/rel).read_text())
old=read('04_Results/Optimization/baseline_inputs.json'); new=read(PREFIX+'backend_probability60/inputs.json')
diff=[k for k in old if old[k]!=new[k]]
assert diff==['probabilities']
impact=read(PREFIX+'analysis/scenario_impact.json')
with (SNAP/PREFIX/'analysis/Original23_Label_Migration.csv').open(encoding='utf-8-sig') as f:
    migration=list(csv.DictReader(f))
changed=[r['original_event_id'] for r in migration if r['old_class']!=r['new_class']]
assert len(changed)==impact['original23_class_changes']==6
fits=impact['fits']
assert fits['original23_frozen']['counts']==[9,9,5]
assert fits['reconstructed60_adjudicated']['counts']==[35,19,6]
assert impact['main_fit']=='reconstructed60_adjudicated' and impact['main_N']==60
assert impact['main_old_projection_counts']==[43,12,5]
sources=['04_Results/Optimization/baseline_inputs.json',PREFIX+'backend_probability60/inputs.json',
         PREFIX+'analysis/scenario_impact.json',PREFIX+'analysis/Original23_Label_Migration.csv',PREFIX+'code/run_backend.py']
result={'status':'PASS','audit_type':'existing-evidence consistency, not new clustering experiment',
    'only_changed_backend_parameter_field':diff,'unchanged_backend_fields':[k for k in old if k not in diff],
    'old_frequencies':old['probabilities'],'new_frequencies':new['probabilities'],
    'old_class_counts':fits['original23_frozen']['counts'],'new_class_counts':fits['reconstructed60_adjudicated']['counts'],
    'changed_original_labels':changed,'fixed_old_projection_counts':impact['main_old_projection_counts'],
    'old_representatives':fits['original23_frozen']['representatives'],
    'new_representatives':fits['reconstructed60_adjudicated']['representatives'],
    'old_thresholds':fits['original23_frozen']['thresholds'],'new_thresholds':fits['reconstructed60_adjudicated']['thresholds'],
    'empirical_response_recalibration':False,'full_observation_to_decision_propagation':False,
    'source_sha256':{r:hashlib.sha256((SNAP/r).read_bytes()).hexdigest() for r in sources}}
(BASE/'assessment/Scenario_Chain_Audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps({'status':'PASS','changed_field':diff,'changed_original_labels':changed}))
