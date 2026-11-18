"""Adapt the frozen EV policy enumeration to the new61 probability vector."""
from dataclasses import replace
import argparse,importlib.util,json,sys
from reconstruct import OUT,SNAP

sys.path.insert(0,str(SNAP/'02_Model'))
spec=importlib.util.spec_from_file_location('saved_ev_tie_audit',SNAP/'03_Experiments/Optimization/code/audit_ev_ties.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
original_load=module.load_inputs
update=json.loads((OUT/'analysis/backend_probability_update.json').read_text())
prob=update['probabilities']
ap=argparse.ArgumentParser();ap.add_argument('--run-name');args=ap.parse_args()
module.load_inputs=lambda path:replace(original_load(path),probabilities=prob)
sys.argv=['audit_backend_ev_ties.py',str(OUT/(args.run_name or f'backend_probability{update["N"]}'))]
module.main()
