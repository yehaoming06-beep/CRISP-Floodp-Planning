"""Portable orchestration of the frozen core and two 555-case experiments."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=("core", "suite23", "suite60", "all"))
    parser.add_argument("--output", type=Path, required=True,
                        help="New directory within the checkout; existing directories are refused")
    args = parser.parse_args()
    out = args.output.resolve()
    out.relative_to(ROOT)
    out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1",
               OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONHOME", None)
    steps = []
    report = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "target": args.target, "python": sys.version, "executable": sys.executable,
        "platform": platform.platform(), "steps": steps,
        "packages": {p: metadata.version(p) for p in
                     ("gurobipy", "numpy", "pandas", "scipy", "scikit-learn", "openpyxl")},
        "scope": "Frozen experiments only; no source re-adjudication or empirical calibration",
    }

    def save():
        (out / "execution.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(name, script, *arguments):
        command = [sys.executable, script, *map(str, arguments)]
        entry = {"name": name, "command": command,
                 "started_utc": datetime.now(timezone.utc).isoformat(),
                 "log": f"{name}.txt"}
        steps.append(entry)
        save()
        print(f"Running {name}", flush=True)
        with (out / entry["log"]).open("w") as log:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=log,
                                    stderr=subprocess.STDOUT)
        entry.update(exit_code=result.returncode,
                     ended_utc=datetime.now(timezone.utc).isoformat())
        save()
        if result.returncode:
            raise RuntimeError(f"{name} failed; see {out / entry['log']}")

    try:
        scenarios = out / "scenarios"
        if args.target in ("core", "suite60", "all"):
            run("scenarios", "src/submission/scenarios.py", "--output", scenarios)
        counts = scenarios / "scenario_reproduction_summary.json"
        if counts.exists():
            scenario_status = json.loads(counts.read_text())
            assert scenario_status["status"] == "PASS", "Scenario cross-check failed"
        if args.target in ("core", "all"):
            run("core", "audit/reproducibility_20261118/optimization/run_core.py",
                "--counts-file", counts, "--output", out / "core")
        if args.target in ("suite23", "all"):
            run("suite23", "03_Experiments/Optimization/code/run_experiments.py",
                "--run-id", "submission23", "--output", out / "suite23")
            run("verify23", "03_Experiments/Optimization/code/verify_results.py",
                out / "suite23")
        if args.target in ("suite60", "all"):
            run("suite60", "src/submission/suite60.py", "--counts-file", counts,
                "--output", out / "suite60")
            run("verify60", "src/submission/verify60.py", out / "suite60")
        # Comparison references are never used to build model parameters.
        import pandas as pd
        comparisons = []
        for suite, reference in (
            ("suite23", "04_Results/Optimization/summary.csv"),
            ("suite60", "manuscript_revision/audit/ci01_independent_20261104/backend_probability60/summary.csv"),
        ):
            if not (out / suite).exists():
                continue
            fresh = pd.read_csv(out / suite / "summary.csv").set_index("id")
            old = pd.read_csv(ROOT / reference).set_index("id")
            assert len(fresh) == len(old) == 555 and set(fresh.index) == set(old.index)
            for key in ("rp", "ws", "ev", "eev", "vss", "evpi", "new_pumps", "setup_used"):
                delta = float((fresh[key] - old.loc[fresh.index, key]).abs().max())
                assert delta < 1e-9, (suite, key, delta)
                comparisons.append({"suite": suite, "field": key, "max_abs_error": delta})
            assert fresh.plan.equals(old.loc[fresh.index].plan)
        report.update(status="PASS", historical_comparisons=comparisons)
    except Exception as exc:
        report.update(status="FAIL", error=str(exc))
        raise
    finally:
        report["ended_utc"] = datetime.now(timezone.utc).isoformat()
        save()
    print(f"PASS: {args.target}; records: {out / 'execution.json'}", flush=True)


if __name__ == "__main__":
    main()
