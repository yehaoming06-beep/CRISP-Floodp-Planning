"""Output-only wrapper; fixed audit receives fresh 60-class conditional frequencies."""
from pathlib import Path
from dataclasses import replace
import importlib.util,sys,json
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
path=ROOT/'03_Experiments/Optimization/code/audit_ev_ties.py'
spec=importlib.util.spec_from_file_location('original_ev_enumerator',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
probabilities=json.loads((OUT/'analysis/backend_probability_update.json').read_text())['probabilities']
original_load=module.load_inputs
module.load_inputs=lambda workbook:replace(original_load(workbook),probabilities=probabilities)
sys.argv=[str(path),str(OUT/'reconstructed60_555')]
module.main()
