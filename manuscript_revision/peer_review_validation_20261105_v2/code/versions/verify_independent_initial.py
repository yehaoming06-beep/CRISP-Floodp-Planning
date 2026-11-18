"""Independent v2 numerical audit: raw JSON -> matrices -> SciPy/HiGHS.

No project model, parameter loader, or primary runner is imported.  Primary
solutions are evidence to test, never a source of EV construction or optima.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import itertools
import json
import math
import platform
import re
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csc_matrix

BASE = Path(__file__).resolve().parents[1]
PRIMARY = BASE / "runs" / "primary"
OUT = BASE / "independent_validation"
TOL = 1e-6
RESOURCE = (("deploy_cost", "operating_budget"), ("labour", "labour_capacity"),
            ("equipment", "equipment_capacity"), ("supply", "supply_capacity"))
TRIPLE_FIELDS = ("deploy_cost", "labour", "equipment", "supply", "upper_bound", "benefit")
CHECKS = []
SOLVE_COUNT = 0


def read(path):
    return json.loads(Path(path).read_text())


def dump(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False))


def table(path, rows):
    if not rows:
        return
    with Path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1048576), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition, label, detail=None):
    if not condition:
        raise AssertionError(f"{label}: {detail}")


def close(a, b, label):
    require(abs(float(a) - float(b)) <= TOL, label, {"left": a, "right": b})


def decode(raw):
    """Parse only JSON; preserve the declared pair order for binary masks."""
    p = {"scenarios": list(raw["probabilities"]),
         "probabilities": dict(raw["probabilities"]), "setup_budget": raw["setup_budget"]}
    p["setup_cost"] = {(r["location"], r["intervention"]): r["value"] for r in raw["setup_cost"]}
    p["pairs"] = list(p["setup_cost"])
    p["locations"] = list(dict.fromkeys(j for j, _ in p["pairs"]))
    p["interventions"] = list(dict.fromkeys(i for _, i in p["pairs"]))
    for _, capacity in RESOURCE:
        p[capacity] = dict(raw[capacity])
    for field in TRIPLE_FIELDS:
        p[field] = {(r["scenario"], r["location"], r["intervention"]): r["value"]
                    for r in raw[field]}
    return p


def resource_bound(p, scenario, location, intervention):
    ratios = [p[capacity][scenario] / p[coefficient][scenario, location, intervention]
              for coefficient, capacity in RESOURCE
              if p[coefficient][scenario, location, intervention] > 0]
    require(bool(ratios), "At least one positive resource coefficient")
    return math.floor(min(ratios) + 1e-10)


def expected_from_raw(q, convention):
    """A averages individually floored bounds; B derives new bounds after averaging."""
    p = copy.deepcopy(q)
    p["scenarios"] = ["EV"]
    p["probabilities"] = {"EV": 1.0}
    for _, capacity in RESOURCE:
        p[capacity] = {"EV": sum(q["probabilities"][s] * q[capacity][s] for s in q["scenarios"])}
    for field in TRIPLE_FIELDS:
        p[field] = {("EV", j, i): sum(q["probabilities"][s] * q[field][s, j, i]
                                       for s in q["scenarios"])
                    for j, i in q["pairs"]}
    if convention == "B":
        p["upper_bound"] = {("EV", j, i): resource_bound(p, "EV", j, i) for j, i in q["pairs"]}
    return p


def compare_parameters(saved, expected, tag):
    require(saved["scenarios"] == expected["scenarios"], f"{tag} scenarios")
    require(saved["pairs"] == expected["pairs"], f"{tag} ordered pairs")
    for field in ("setup_budget", "setup_cost", "probabilities") + tuple(b for _, b in RESOURCE) + TRIPLE_FIELDS:
        left, right = saved[field], expected[field]
        if isinstance(left, dict):
            require(set(left) == set(right), f"{tag}/{field} key equality")
            for key in left:
                close(left[key], right[key], f"{tag}/{field}/{key}")
        else:
            close(left, right, f"{tag}/{field}")


def base_config(model):
    return {"stock": "none" if model == "legacy" else "shared", "integer_n": True,
            "existing_stock": 0, "capital_budget_hkd": 0 if model == "legacy" else 2000000,
            "purchase_price_hkd": 1000000, "accessible_locations": ["Tai O1", "Tai O2"],
            "coverage_each_location_each_scenario": 0}


def expected_spec(tag, q):
    """Derive each specification from its declared design, not saved parameter files."""
    p = copy.deepcopy(q)
    parts = tag.split("_")
    if parts[1] in ("legacy", "mobile"):
        c = base_config(parts[1])
        if parts[2] == "ws":
            scenario = "_".join(parts[3:])
            p["scenarios"], p["probabilities"] = [scenario], {scenario: 1.0}
        elif parts[2] in ("A", "B") and parts[-1] == "ev":
            p = expected_from_raw(q, parts[2])
    elif parts[1] == "coverage":
        c = base_config("mobile")
        c["coverage_each_location_each_scenario"] = int(parts[2])
    elif parts[1].startswith("budget"):
        c = base_config("mobile")
        c["capital_budget_hkd"] = int(parts[1][6:])
        case = parts[2]
        c["integer_n"] = case not in ("F0", "F1", "F2")
        if case == "F0":
            c["stock"] = "none"
        elif case == "F1":
            c["stock"] = "replicated"
        elif case == "A1":
            c["accessible_locations"] = ["Tai O1"]
        elif case == "A2":
            c["accessible_locations"] = ["Tai O2"]
    else:
        raise AssertionError(f"Unknown specification: {tag}")
    return p, c


def matrix(p, c, fixed=None):
    pairs, scenarios = p["pairs"], p["scenarios"]
    triples = [(s, j, i) for s in scenarios for j, i in pairs]
    ny, nx = len(pairs), len(triples)
    total, ni = ny + nx + 1, ny + nx
    yindex = {key: index for index, key in enumerate(pairs)}
    xindex = {key: ny + index for index, key in enumerate(triples)}
    names = [f"ready_{i}" for i in range(ny)] + [f"deploy_{i}" for i in range(nx)] + ["new_pumps"]
    integrality = np.ones(total, dtype=np.uint8)
    integrality[ni] = int(c["integer_n"])
    lower, upper = np.zeros(total), np.full(total, np.inf)
    upper[:ny] = 1
    upper[ni] = c["capital_budget_hkd"] / c["purchase_price_hkd"]
    objective = np.zeros(total)
    for key, idx in xindex.items():
        objective[idx] = p["probabilities"][key[0]] * p["benefit"][key]
    rows, lb, ub, labels = [], [], [], []

    def row(label, entries, low=-np.inf, high=np.inf):
        vector = np.zeros(total)
        for index, coefficient in entries:
            vector[index] += coefficient
        rows.append(vector)
        labels.append(label)
        lb.append(low)
        ub.append(high)

    row("readiness", [(yindex[k], p["setup_cost"][k]) for k in pairs], high=p["setup_budget"])
    row("capital", [(ni, c["purchase_price_hkd"])], high=c["capital_budget_hkd"])
    if fixed is not None:
        require(len(fixed["y"]) == ny, "All readiness decisions fixed")
        for index, value in enumerate(fixed["y"]):
            row(f"fixed_y_{index}", [(index, 1)], low=value, high=value)
        row("fixed_n", [(ni, 1)], low=fixed["n"], high=fixed["n"])
    for s in scenarios:
        for coefficient, capacity in RESOURCE:
            row(f"{s}/{capacity}", [(xindex[s, j, i], p[coefficient][s, j, i]) for j, i in pairs],
                high=p[capacity][s])
        for j, i in pairs:
            row(f"{s}/{j}/{i}/link", [(xindex[s, j, i], 1), (yindex[j, i], -p["upper_bound"][s, j, i])], high=0)
        if c["stock"] == "shared":
            row(f"{s}/shared", [(xindex[s, j, "Drainage"], 1) for j in p["locations"]] + [(ni, -1)], high=c["existing_stock"])
        elif c["stock"] == "replicated":
            for j in p["locations"]:
                row(f"{s}/{j}/replicated", [(xindex[s, j, "Drainage"], 1), (ni, -1)], high=c["existing_stock"])
        else:
            require(c["stock"] == "none", "Recognized inventory rule")
        for j in p["locations"]:
            if j not in c["accessible_locations"]:
                row(f"{s}/{j}/access", [(xindex[s, j, "Drainage"], 1)], low=0, high=0)
            k = c["coverage_each_location_each_scenario"]
            if k:
                row(f"{s}/{j}/coverage", [(xindex[s, j, i], 1) for i in p["interventions"]], low=k)
    return {"c": objective, "A": np.array(rows), "lb": np.array(lb), "ub": np.array(ub),
            "lower": lower, "upper": upper, "integrality": integrality, "names": names,
            "labels": labels, "triples": triples, "nindex": ni}


def check_vector(m, vector):
    vector = np.asarray(vector, dtype=float)
    lhs = m["A"] @ vector
    violation = max(0.0, float(np.max(m["lb"] - lhs)), float(np.max(lhs - m["ub"])),
                    float(np.max(m["lower"] - vector)), float(np.max(vector - m["upper"])))
    domain = float(np.max(np.abs(vector[m["integrality"] > 0] - np.rint(vector[m["integrality"] > 0]))))
    return {"max_constraint_or_bound_violation": violation, "max_integrality_error": domain,
            "objective_reconstructed": float(m["c"] @ vector)}


def solve(p, c, fixed=None):
    global SOLVE_COUNT
    m = matrix(p, c, fixed)
    answer = milp(c=-m["c"], integrality=m["integrality"],
                  bounds=Bounds(m["lower"], m["upper"]),
                  constraints=LinearConstraint(csc_matrix(m["A"]), m["lb"], m["ub"]),
                  options={"mip_rel_gap": 0, "time_limit": 60, "presolve": True})
    SOLVE_COUNT += 1
    require(answer.status in (0, 2), "HiGHS terminated definitively", answer.message)
    result = {"status": "OPTIMAL" if answer.status == 0 else "INFEASIBLE",
              "status_code": int(answer.status), "message": answer.message,
              "objective": None, "solution": None}
    if answer.status == 0:
        checked = check_vector(m, answer.x)
        require(checked["max_constraint_or_bound_violation"] <= TOL, "Independent solution feasibility", checked)
        require(checked["max_integrality_error"] <= TOL, "Independent solution domains", checked)
        result.update(objective=float(-answer.fun), solution=answer.x.tolist(), validation=checked,
                      primary_mip_dual_bound=float(-answer.mip_dual_bound), primary_mip_gap=float(answer.mip_gap))
    return m, result


def vector_from_saved(p, saved):
    lookup = {(r["scenario"], r["location"], r["intervention"]): r["x"] for r in saved["x"]}
    require(set(lookup) == {(s, j, i) for s in p["scenarios"] for j, i in p["pairs"]}, "Saved deployment keys complete")
    return saved["policy"]["y"] + [lookup[s, j, i] for s in p["scenarios"] for j, i in p["pairs"]] + [saved["policy"]["n"]]


def fixed_from_tag(tag, saved):
    if "_enum_" in tag:
        fragment = tag.split("_enum_", 1)[1].split("_")
        mask, n = int(fragment[0]), int(fragment[1])
        expected = {"y": [int(bool(mask & (1 << k))) for k in range(6)], "n": n}
        require(saved["fixed_policy"] == expected, f"{tag} full fixed policy matches identifier")
        return expected
    if tag.endswith("_eev"):
        ev_tag = tag[:-4] + "_ev"
        expected = read(PRIMARY / "solutions" / f"{ev_tag}.json")["policy"]
        require(saved["fixed_policy"] == expected, f"{tag} all y and n fixed from selected EV")
        return expected
    require(saved["fixed_policy"] is None, f"{tag} no undeclared fixed stage")
    return None


def save_model_evidence(m, tag):
    directory = OUT / "matrices"
    directory.mkdir(exist_ok=True)
    np.savez_compressed(directory / f"{tag}.npz", objective=m["c"], A=m["A"],
                        row_lower=m["lb"], row_upper=m["ub"], variable_lower=m["lower"],
                        variable_upper=m["upper"], integrality=m["integrality"],
                        variable_names=np.array(m["names"]), row_names=np.array(m["labels"]))


def raw_sources():
    old = read(BASE / "snapshots/04_Results/Optimization/baseline_inputs.json")
    new = read(BASE / "snapshots/manuscript_revision/audit/ci01_independent_20261104/backend_probability60/inputs.json")
    require({k: v for k, v in old.items() if k != "probabilities"} ==
            {k: v for k, v in new.items() if k != "probabilities"}, "Frequency-only replacement")
    p23, p60 = decode(old), decode(new)
    for p, counts in ((p23, (9, 9, 5)), (p60, (35, 19, 6))):
        for s, count in zip(p["scenarios"], counts):
            close(p["probabilities"][s], count / sum(counts), "Raw event frequency")
        close(sum(p["probabilities"].values()), 1, "Probability normalization")
        for s, j, i in itertools.product(p["scenarios"], p["locations"], p["interventions"]):
            close(p["upper_bound"][s, j, i], resource_bound(p, s, j, i), "Raw U independently derived from resources")
    return {"23": p23, "60": p60}


def audit_saved_specs(qs):
    all_saved = sorted((PRIMARY / "solutions").glob("*.json"))
    require(bool(all_saved), "Primary output exists")
    rows, inventory, results = [], [], {}
    unique_parameters = set()
    for number, path in enumerate(all_saved, 1):
        saved = read(path)
        tag = saved["tag"]
        require(path.stem == tag, "Consistent solution filename")
        freq = tag.split("_")[0][1:]
        expected, expected_c = expected_spec(tag, qs[freq])
        require(saved["config"] == expected_c, f"{tag} declared configuration")
        parameter_path = PRIMARY / "parameters" / f'{saved["parameter_id"]}.json'
        raw = read(parameter_path)
        expected_id = hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest()[:20]
        require(saved["parameter_id"] == expected_id, f"{tag} parameter content identifier")
        unique_parameters.add(parameter_path)
        compare_parameters(decode(raw), expected, tag)
        fixed = fixed_from_tag(tag, saved)
        m, answer = solve(expected, expected_c, fixed)
        require(answer["status"] == saved["status"], f"{tag} status agreement", answer)
        require(saved["status_code"] == (2 if saved["status"] == "OPTIMAL" else 3), f"{tag} primary numeric status")
        delta = None
        checked = {"max_constraint_or_bound_violation": None, "max_integrality_error": None}
        required = [("solution_json", path), ("parameters_json", parameter_path),
                    ("lp", PRIMARY / "models" / f"{tag}.lp"), ("log", PRIMARY / "logs" / f"{tag}.log")]
        log = (PRIMARY / "logs" / f"{tag}.log").read_text()
        # Stored numeric status plus independent optimization determines pass;
        # no exact English 'Optimal solution found' phrase is required.
        log_multi_solved = bool(re.search(r"Multi-objectives\s*:\s*solved", log, re.I))
        log_presolve_all_fixed = bool(re.search(r"All rows and columns removed", log, re.I))
        if saved["status"] == "OPTIMAL":
            require(saved["solution_count"] >= 1, f"{tag} incumbent exists")
            close(answer["objective"], saved["objective"], f"{tag} primary objective")
            close(saved["primary_value_from_solver"], saved["objective"], f"{tag} recorded solver primary objective")
            vector = vector_from_saved(expected, saved)
            checked = check_vector(m, vector)
            require(checked["max_constraint_or_bound_violation"] <= TOL, f"{tag} saved feasibility", checked)
            require(checked["max_integrality_error"] <= TOL, f"{tag} saved variable domains", checked)
            close(checked["objective_reconstructed"], saved["objective"], f"{tag} saved objective reconstruction")
            if fixed is not None:
                require(saved["policy"]["y"] == fixed["y"], f"{tag} readiness fixed")
                close(saved["policy"]["n"], fixed["n"], f"{tag} procurement fixed")
            sol_path = PRIMARY / "sol" / f"{tag}.sol"
            required.append(("gurobi_sol", sol_path))
            raw_values = {}
            for line in sol_path.read_text().splitlines():
                if line.strip() and not line.lstrip().startswith("#"):
                    name, value = line.split()
                    raw_values[name] = float(value)
            require(set(m["names"]) == set(raw_values), f"{tag} raw SOL variable completeness")
            sol_vector = [raw_values[name] for name in m["names"]]
            sol_checks = check_vector(m, sol_vector)
            require(sol_checks["max_constraint_or_bound_violation"] <= TOL and sol_checks["max_integrality_error"] <= TOL,
                    f"{tag} unrounded SOL feasible and in domain", sol_checks)
            require(float(np.max(np.abs(np.array(sol_vector) - vector))) <= TOL, f"{tag} SOL/JSON agreement")
            require(log_multi_solved, f"{tag} multiobjective log completion marker")
            delta = abs(answer["objective"] - saved["objective"])
        else:
            require(saved["objective"] is None and saved["solution_count"] == 0, f"{tag} infeasible is never zero-filled")
            required.append(("iis", PRIMARY / "models" / f"{tag}.ilp"))
        for kind, artifact in required:
            require(artifact.is_file() and artifact.stat().st_size > 0, f"{tag} nonempty {kind}")
            inventory.append({"tag": tag, "kind": kind, "path": str(artifact.relative_to(BASE)),
                              "bytes": artifact.stat().st_size, "sha256": sha(artifact)})
        save_model_evidence(m, tag)
        answer.update(tag=tag, saved_objective=saved["objective"], absolute_objective_error=delta,
                      saved_solution_validation=checked, all_y_and_n_fixed=fixed is not None,
                      log_multiobjective_solved=log_multi_solved, log_presolve_all_fixed=log_presolve_all_fixed)
        dump(OUT / "solutions" / f"{tag}.json", answer)
        row = {"tag": tag, "status": answer["status"], "primary_objective": saved["objective"],
               "independent_objective": answer["objective"], "absolute_error": delta,
               "saved_feasibility_violation": checked["max_constraint_or_bound_violation"],
               "saved_integrality_error": checked["max_integrality_error"], "all_y_n_fixed": fixed is not None,
               "multiobjective_log_solved": log_multi_solved, "presolve_all_fixed": log_presolve_all_fixed}
        rows.append(row)
        results[tag] = answer
        if number % 50 == 0:
            print(f"Independently verified {number}/{len(all_saved)} saved specifications", flush=True)
    require(set(path.stem for path in (PRIMARY / "models").glob("*.lp")) == set(results), "LP/solution inventory equality")
    require(set(path.stem for path in (PRIMARY / "logs").glob("*.log")) == set(results), "Log/solution inventory equality")
    require(set(path.stem for path in (PRIMARY / "sol").glob("*.sol")) ==
            {tag for tag, r in results.items() if r["status"] == "OPTIMAL"}, "SOL/optimal inventory equality")
    require(set((PRIMARY / "parameters").glob("*.json")) == unique_parameters, "No unreferenced or missing parameter JSON")
    audit = csv_rows(PRIMARY / "solver_audit.csv")
    require(set(r["tag"] for r in audit) == set(results) and len(audit) == len(results), "Audit table covers each solve once")
    validation = read(PRIMARY / "validation.json")
    require(validation["solves"] == len(results), "Primary validation count")
    require(validation["optimal"] == sum(r["status"] == "OPTIMAL" for r in results.values()), "Primary optimal count")
    require(validation["infeasible_expected"] == sum(r["status"] == "INFEASIBLE" for r in results.values()), "Primary infeasible count")
    table(OUT / "all_saved_specifications.csv", rows)
    table(OUT / "primary_artifact_inventory.csv", inventory)
    return results, rows


def audit_ev(qs, saved_results):
    summaries, trials, ties, bounds = [], [], [], []
    primary_summaries = {(r["frequency"], r["model"], r["convention"]): r for r in csv_rows(PRIMARY / "ev_summary.csv")}
    primary_trials = {(r["frequency"], r["model"], r["convention"], int(r["mask"]), int(r["n"])): r
                      for r in csv_rows(PRIMARY / "ev_all_policy_trials.csv")}
    primary_ties = {(r["frequency"], r["model"], r["convention"], int(r["mask"]), int(r["n"])): r
                    for r in csv_rows(PRIMARY / "ev_optimal_policies.csv")}
    for frequency, q in qs.items():
        masks = [mask for mask in range(1 << len(q["pairs"]))
                 if sum(q["setup_cost"][pair] * bool(mask & (1 << k)) for k, pair in enumerate(q["pairs"])) <= q["setup_budget"] + TOL]
        require(len(masks) == 26, "Budget-feasible readiness set count")
        for model in ("legacy", "mobile"):
            c = base_config(model)
            rp = saved_results[f"f{frequency}_{model}_rp"]["objective"]
            ws = sum(q["probabilities"][s] * saved_results[f"f{frequency}_{model}_ws_{s}"]["objective"] for s in q["scenarios"])
            for convention in ("A", "B"):
                p = expected_from_raw(q, convention)
                collected = []
                for j, i in q["pairs"]:
                    bounds.append({"frequency": frequency, "model": model, "convention": convention,
                                   "location": j, "intervention": i, "upper_bound": p["upper_bound"]["EV", j, i],
                                   "effective_integer_upper_bound": math.floor(p["upper_bound"]["EV", j, i] + 1e-10)})
                for mask in masks:
                    yy = [int(bool(mask & (1 << k))) for k in range(len(q["pairs"]))]
                    for n in range(1 if model == "legacy" else 3):
                        fixed = {"y": yy, "n": n}
                        _, ev = solve(p, c, fixed)
                        require(ev["status"] == "OPTIMAL", "EV fixed policy feasible")
                        key = (frequency, model, convention, mask, n)
                        require(key in primary_trials, "Primary EV trials complete")
                        close(ev["objective"], primary_trials[key]["ev"], f"Raw-derived fixed EV {key}")
                        collected.append({"frequency": frequency, "model": model, "convention": convention,
                                          "mask": mask, "n": n, "ev": ev["objective"]})
                best = max(r["ev"] for r in collected)
                optima = [r for r in collected if abs(r["ev"] - best) <= TOL]
                for item in collected:
                    item["is_primary_ev_optimum"] = abs(item["ev"] - best) <= TOL
                    key = (frequency, model, convention, item["mask"], item["n"])
                    require((primary_trials[key]["is_primary_ev_optimum"] == "True") == item["is_primary_ev_optimum"], "All EV optimum flags agree")
                    trials.append(dict(item))
                selected = min(optima, key=lambda r: (r["n"], sum(q["setup_cost"][pair] * bool(r["mask"] & (1 << k))
                                                                 for k, pair in enumerate(q["pairs"])), r["mask"]))
                ev_saved = read(PRIMARY / "solutions" / f"f{frequency}_{model}_{convention}_ev.json")
                require(ev_saved["policy"]["y"] == [int(bool(selected["mask"] & (1 << k))) for k in range(len(q["pairs"]))], "EV lexicographic selected y")
                close(ev_saved["policy"]["n"], selected["n"], "EV lexicographic selected n")
                for item in optima:
                    fixed = {"y": [int(bool(item["mask"] & (1 << k))) for k in range(len(q["pairs"]))], "n": item["n"]}
                    _, eev = solve(q, c, fixed)
                    require(eev["status"] == "OPTIMAL", "Every EV optimum has feasible EEV")
                    item.update(eev=eev["objective"], vss=rp - eev["objective"])
                    key = (frequency, model, convention, item["mask"], item["n"])
                    require(key in primary_ties, "Primary ties include every independently identified optimum")
                    close(item["eev"], primary_ties[key]["eev"], f"Independent EEV {key}")
                    close(item["vss"], primary_ties[key]["vss"], f"Independent VSS {key}")
                    ties.append(dict(item))
                summary = {"frequency": frequency, "model": model, "convention": convention, "rp": rp, "ws": ws,
                           "ev": best, "selected_mask": selected["mask"], "selected_ev_n": selected["n"],
                           "selected_eev": selected["eev"], "selected_vss": selected["vss"], "evpi": ws-rp,
                           "feasible_policies_enumerated": len(collected), "ev_optimal_policy_count": len(optima),
                           "eev_min": min(r["eev"] for r in optima), "eev_max": max(r["eev"] for r in optima),
                           "vss_min": min(r["vss"] for r in optima), "vss_max": max(r["vss"] for r in optima)}
                other = primary_summaries[frequency, model, convention]
                for field in summary:
                    if field not in ("frequency", "model", "convention", "selected_mask"):
                        close(summary[field], other[field], f"EV summary {frequency}/{model}/{convention}/{field}")
                require(ws + TOL >= rp >= summary["eev_max"] - TOL, "WS >= RP >= every EEV")
                summaries.append(summary)
    require(len(trials) == len(primary_trials), "No extra or missing primary EV policy trials")
    require(len(ties) == len(primary_ties), "Exact EV primary-optimal policy set equality")
    divergence = []
    trial_lookup = {(r["frequency"], r["model"], r["convention"], r["mask"], r["n"]): r["ev"] for r in trials}
    for frequency, model in itertools.product(qs, ("legacy", "mobile")):
        differences = [abs(r["ev"] - trial_lookup[frequency, model, "B", r["mask"], r["n"]])
                       for r in trials if r["frequency"] == frequency and r["model"] == model and r["convention"] == "A"]
        divergence.append({"frequency": frequency, "model": model, "fixed_policy_count": len(differences),
                           "A_B_different_value_policy_count": sum(d > TOL for d in differences),
                           "maximum_fixed_policy_value_difference": max(differences)})
    table(OUT / "ev_summary.csv", summaries)
    table(OUT / "ev_all_policy_trials.csv", trials)
    table(OUT / "ev_optimal_policies.csv", ties)
    table(OUT / "ev_reconstructed_bounds.csv", bounds)
    table(OUT / "ev_fixed_policy_convention_differences.csv", divergence)
    return summaries, trials, ties, divergence


def audit_structure_and_coverage(qs, results):
    component = []
    for frequency, budget in itertools.product(qs, (2000000, 6500000)):
        stem = f"f{frequency}_budget{budget}_"
        keys = ("F0_no_stock", "F1_replicated_continuous", "F2_shared_continuous", "F3_shared_integer", "A1_access_O1_only", "A2_access_O2_only")
        values = [results[stem + key]["objective"] for key in keys]
        require(values[0] + TOL >= values[1] >= values[2] - TOL, "Inventory nesting F0/F1/F2")
        require(values[2] + TOL >= values[3], "Continuous contains integer n")
        close(values[2], values[3], "F2/F3 primary equality for current inputs")
        require(values[3] + TOL >= max(values[4:]), "Restricted access contained in F3")
        for key, value in zip(keys, values):
            component.append({"frequency": frequency, "capital_budget_hkd": budget, "case": key, "rp": value})
    certificate, coverage = [], []
    for frequency, q in qs.items():
        previous = math.inf
        for k in (0, 1, 2, 6):
            answer = results[f"f{frequency}_coverage_{k}"]
            if k < 6:
                require(answer["status"] == "OPTIMAL" and answer["objective"] <= previous + TOL, "Coverage monotonicity")
                previous = answer["objective"]
            else:
                require(answer["status"] == "INFEASIBLE", "Coverage negative control infeasible")
                count = 0
                for s, (coefficient, capacity) in itertools.product(q["scenarios"], RESOURCE):
                    per_location = {j: min(q[coefficient][s, j, i] for i in q["interventions"]) for j in q["locations"]}
                    required = k * sum(per_location.values())
                    available = q[capacity][s]
                    if required > available + TOL:
                        count += 1
                        certificate.append({"frequency": frequency, "scenario": s, "coverage_k": k,
                                            "resource": coefficient, "minimal_resource_required": required,
                                            "resource_capacity": available, "strict_shortfall": required - available,
                                            "logic": "sum_j min_i(resource_sji) * k > scenario capacity"})
                require(count > 0, "At least one explicit resource contradiction proves infeasibility")
            row = {"frequency": frequency, "k": k, "status": answer["status"], "rp": answer["objective"],
                   "opportunity_cost": None if k == 6 else results[f"f{frequency}_coverage_0"]["objective"] - answer["objective"]}
            coverage.append(row)
    # A feasible replicated-stock point violating shared-stock accounting.
    q = qs["23"]
    c = base_config("mobile")
    c["stock"] = "replicated"
    m = matrix(q, c)
    vector = [int(i == "Drainage") for j, i in q["pairs"]] + [2 if i == "Drainage" else 0 for s, j, i in m["triples"]] + [2]
    checked = check_vector(m, vector)
    require(checked["max_constraint_or_bound_violation"] <= TOL, "Replicated-stock witness feasible")
    c["stock"] = "shared"
    shared_m = matrix(q, c)
    shared_lhs = shared_m["A"] @ vector
    violated = [{"constraint": label, "lhs": float(shared_lhs[k]), "upper": float(shared_m["ub"][k])}
                for k, label in enumerate(shared_m["labels"]) if shared_lhs[k] > shared_m["ub"][k] + TOL]
    require(len(violated) == len(q["scenarios"]) and all(r["constraint"].endswith("/shared") for r in violated), "Only shared rows violated by stock witness")
    witness_rows = [{"constraint": label, "lhs": float((m["A"] @ vector)[k]),
                     "lower": None if not np.isfinite(m["lb"][k]) else float(m["lb"][k]),
                     "upper": None if not np.isfinite(m["ub"][k]) else float(m["ub"][k])}
                    for k, label in enumerate(m["labels"])]
    dump(OUT / "inventory_feasible_set_witness.json", {"y": vector[:6], "n": 2, "drainage_each_location_each_scenario": 2,
                                                      "replicated_validation": checked, "all_replicated_rows": witness_rows,
                                                      "shared_violations": violated})
    table(OUT / "component_independent.csv", component)
    table(OUT / "coverage_independent.csv", coverage)
    table(OUT / "coverage_infeasibility_certificates.csv", certificate)
    dump(OUT / "coverage_infeasibility_certificates.json", certificate)
    return component, coverage, certificate


def main():
    started = time.monotonic()
    require((PRIMARY / "validation.json").exists(), "Wait until primary run finishes")
    OUT.mkdir(parents=True, exist_ok=False)
    try:
        qs = raw_sources()
        results, rows = audit_saved_specs(qs)
        summaries, trials, ties, divergence = audit_ev(qs, results)
        component, coverage, certificates = audit_structure_and_coverage(qs, results)
        manifest = {"status": "PASS", "python": sys.version, "platform": platform.platform(),
                    "numpy_version": np.__version__, "scipy_version": scipy.__version__,
                    "solver": "SciPy milp / bundled HiGHS, primary objective maximization by minimization of its negative",
                    "code_sha256": sha(Path(__file__)), "primary_run_manifest_sha256": sha(PRIMARY / "run_manifest.json"),
                    "independent_saved_specifications": len(results), "solves_compared": len(results),
                    "optimal": sum(r["status"] == "OPTIMAL" for r in results.values()),
                    "infeasible": sum(r["status"] == "INFEASIBLE" for r in results.values()),
                    "independent_milp_calls": SOLVE_COUNT, "raw_derived_EV_specifications": len(summaries),
                    "raw_derived_EV_fixed_policy_trials": len(trials), "raw_derived_EV_optimal_policies": len(ties),
                    "component_cases": len(component), "coverage_cases": len(coverage),
                    "resource_infeasibility_certificates": len(certificates),
                    "maximum_primary_objective_error": max(r["absolute_error"] or 0 for r in rows),
                    "max_objective_error": max(r["absolute_error"] or 0 for r in rows),
                    "maximum_saved_feasibility_violation": max(r["saved_feasibility_violation"] or 0 for r in rows),
                    "max_constraint_violation": max(r["saved_feasibility_violation"] or 0 for r in rows),
                    "maximum_saved_integrality_error": max(r["saved_integrality_error"] or 0 for r in rows),
                    "max_integrality_error": max(r["saved_integrality_error"] or 0 for r in rows),
                    "full_EEV_y_n_fixation_checked": True, "EV_tie_sets_and_secondary_selection_checked": True,
                    "raw_snapshot_parameter_reconstruction_checked": True,
                    "no_runner_helpers_imported": True, "seconds": time.monotonic() - started}
        dump(OUT / "validation.json", manifest)
        dump(OUT / "verification.json", manifest)
        note = ("# 独立数值核验\n\n"
                f"结论：PASS。独立从 v2 原始 JSON 快照构造矩阵，用 SciPy {scipy.__version__}/HiGHS 重求全部 {len(results)} 个保存规格的主目标，"
                f"状态为 {manifest['optimal']} 个最优、{manifest['infeasible']} 个不可行，与主求解一致。"
                f"最大目标差 {manifest['maximum_primary_objective_error']:.3g}；最大保存解可行性残差 {manifest['maximum_saved_feasibility_violation']:.3g}。\n\n"
                f"从原始资源与概率重建 A/B 的 {len(summaries)} 个 EV 规格，独立枚举 {len(trials)} 个预算可行的一阶段政策，"
                f"复核全部 {len(ties)} 个并列最优政策、EEV/VSS 范围及采购量→readiness 费用→二进制 mask 的次目标选择。"
                "EEV 的全部 y 和 n 固定约束逐项检查；固定政策值差异见 ev_fixed_policy_convention_differences.csv。\n\n"
                "24 个组件规格满足预先声明的可行域包含关系；复制库存与共享库存的区分另有逐行可行点见证。"
                "8 个覆盖规格的结果与单调性一致；k=6 的两个不可行实例有独立资源下界矛盾证书，不把不可行值填为零。\n\n"
                "全部 LP、日志、参数、JSON 和最优 SOL 的存在性、完整性与哈希已检查。日志检查采用多目标求解完成标记、数值状态及独立优化；"
                "允许 presolve 固定全部变量，不要求某一句英文最优提示。独立矩阵保存在 matrices，各规格复核解保存在 solutions。\n\n"
                "这是所声明抽象优化模型的数值一致性核验，不是现场效益、实证公平或水力验证。\n")
        (OUT / "Independent_Validation.md").write_text(note)
        print(json.dumps(manifest, ensure_ascii=False), flush=True)
    except BaseException as exc:
        dump(OUT / "failure.json", {"status": "FAIL", "exception": type(exc).__name__, "message": str(exc),
                                    "independent_milp_calls": SOLVE_COUNT, "seconds": time.monotonic() - started})
        dump(OUT / "verification.json", {"status": "FAIL", "exception": type(exc).__name__, "message": str(exc),
                                         "solves_compared": SOLVE_COUNT})
        raise


if __name__ == "__main__":
    main()
