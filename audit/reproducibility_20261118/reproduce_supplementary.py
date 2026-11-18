#!/usr/bin/env python3
"""Non-destructive adapter for the existing v2 supplementary verification.

The original primary runner is executed unchanged with --output. The existing
independent matrix verifier is imported without executing main(); only its
output destinations are rebound. No historical manifest is reinitialized and
no historical scientific parameter or result is changed.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent / 'supplementary'
SOURCE = Path('/Users/yehaoming/Desktop/climate_Devin/manuscript_revision/peer_review_validation_20261105_v2')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(independent_only=False):
    started = time.monotonic()
    OUT.mkdir(parents=True, exist_ok=True)
    primary = OUT / 'runs/primary'
    primary.parent.mkdir(exist_ok=True)
    runner = SOURCE / 'code/run_validation.py'
    verifier = SOURCE / 'code/verify_independent.py'
    command = [sys.executable, '-B', str(runner), '--output', str(primary)]
    meta = {'primary_command': command, 'runner_sha256': sha(runner),
            'independent_verifier_sha256': sha(verifier),
            'adaptation': 'Unchanged original primary CLI; independent verifier imported and PRIMARY/OUT rebound, then BASE rebound after raw_sources() solely for artifact relative-path serialization; main report-evidence check not invoked because original finalize_artifacts.py is fixed to historical primary.',
            'source_workspace': str(SOURCE), 'python': sys.version}
    (OUT / ('execution_corrected.json' if independent_only else 'execution.json')).write_text(json.dumps(meta, indent=2))
    if not independent_only:
        with (OUT / 'primary_console.txt').open('w') as f:
            answer = subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
        if answer.returncode:
            raise RuntimeError(f'Original primary runner exited {answer.returncode}; see primary_console.txt')
    spec = importlib.util.spec_from_file_location('crisp_v2_independent_audit_adapter', verifier)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module.PRIMARY = primary
    module.OUT = OUT / ('independent_corrected' if independent_only else 'independent')
    module.OUT.mkdir(exist_ok=False)
    qs = module.raw_sources()
    module.BASE = OUT  # Only the inventory's relative_to(BASE) uses BASE after raw_sources().
    results, rows = module.audit_saved_specs(qs)
    summaries, trials, ties, divergence = module.audit_ev(qs, results)
    component, coverage, certificates = module.audit_structure_and_coverage(qs, results)
    errors = [r['absolute_error'] or 0 for r in rows]
    report = {'status': 'PASS', 'new_primary_validation': json.loads((primary/'validation.json').read_text()),
              'independent_milp_calls': module.SOLVE_COUNT, 'new_specifications_checked': len(results),
              'independent_optimal': sum(r['status']=='OPTIMAL' for r in results.values()),
              'independent_infeasible': sum(r['status']=='INFEASIBLE' for r in results.values()),
              'max_primary_objective_error': max(errors),
              'max_saved_feasibility_violation': max(r['saved_feasibility_violation'] or 0 for r in rows),
              'max_saved_integrality_error': max(r['saved_integrality_error'] or 0 for r in rows),
              'ev_specifications': len(summaries), 'ev_fixed_policy_trials': len(trials),
              'ev_optimal_policies': len(ties), 'component_cases': len(component),
              'coverage_cases': len(coverage), 'resource_infeasibility_certificates': len(certificates),
              'elapsed_seconds': time.monotonic()-started,
              'scope': 'New Gurobi primary solves plus independent raw-JSON matrix/HiGHS re-solves; no field validation; historical fixed-output report finalizer and report-witness recheck not executed.',
              'adaptation': meta['adaptation']}
    (OUT / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--independent-only', action='store_true')
    args = parser.parse_args()
    try:
        main(args.independent_only)
    except BaseException as exc:
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT/'failure.json').write_text(json.dumps({'status':'FAIL','exception':type(exc).__name__,'message':str(exc)},indent=2))
        raise
