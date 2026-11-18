"""Fixed design for the current spatial, ablation and uncertainty experiments."""
from dataclasses import replace
import dataclasses,math
import numpy as np
from typing import Any

def derived_u(p):
    return {k: math.floor(min(p.operating_budget[k[0]] / p.deploy_cost[k],
                             p.labour_capacity[k[0]] / p.labour[k],
                             p.equipment_capacity[k[0]] / p.equipment[k],
                             p.supply_capacity[k[0]] / p.supply[k]) + 1e-10)
            for k in p.benefit}


def benefit(p, intervention_factors=None, beta_ji=None):
    factors = intervention_factors or {}
    return {(s, j, i): (p.benefit_weights["w_L"] * p.life_score[i]
                        + p.benefit_weights["w_P"] * p.property_score[i]
                        + p.benefit_weights["w_R"] * p.recovery_score[i])
            * p.alpha[s, i] * (beta_ji[j, i] if beta_ji else p.beta[j]) * factors.get(i, 1.0)
            for s, j, i in p.benefit}


def normalize(d):
    total = sum(d.values())
    return {k: v / total for k, v in d.items()}

def spatial(base):
    for a, d in enumerate((-.2, -.1, 0., .1, .2)):
        for b, c in enumerate((.8, .9, 1., 1.1, 1.2)):
            q = replace(base, beta=dict(zip(base.locations, (1 + d, 1 - d))),
                        setup_cost={(j, i): v * (c if j == base.locations[0] else 2 - c) for (j, i), v in base.setup_cost.items()},
                        deploy_cost={(s, j, i): v * (c if j == base.locations[0] else 2 - c) for (s, j, i), v in base.deploy_cost.items()})
            q = replace(q, benefit=benefit(q), upper_bound=derived_u(q))
            yield q, {"id": f"spatial_{a}_{b}", "experiment": "spatial", "delta": d, "cost1": c}
    beta_ji = {(j, i): ((1.1 if j == base.locations[0] else .9) if i == "Drainage" else
                        (.9 if j == base.locations[0] else 1.1) if i == "Barrier" else 1.)
               for j in base.locations for i in base.interventions}
    yield replace(base, benefit=benefit(base, beta_ji=beta_ji)), {
        "id": "spatial_cross", "experiment": "spatial", "beta_ji_override":
        [{"location": j, "intervention": i, "value": v} for (j, i), v in beta_ji.items()],
        "note": "beta_ji_override replaces scalar beta in benefit construction"}


FACTORS = ("benefit_Drainage", "benefit_Barrier", "benefit_Warning", "weight_w_L", "weight_w_P", "weight_w_R",
           "setup_cost", "deploy_cost", "probability_Extreme", "beta_location2", "availability_U",
           "both_costs", "deploy_cost_fixed_U", "alpha_all")


def oat(base, factor, level):
    q = base
    if factor.startswith("weight_"):
        key = factor.removeprefix("weight_")
        q = replace(q, benefit_weights=normalize({k: v * (level if k == key else 1) for k, v in q.benefit_weights.items()}))
    if factor in ("setup_cost", "both_costs"):
        q = replace(q, setup_cost={k: v * level for k, v in q.setup_cost.items()})
    if factor in ("deploy_cost", "both_costs", "deploy_cost_fixed_U"):
        q = replace(q, deploy_cost={k: v * level for k, v in q.deploy_cost.items()})
    if factor == "probability_Extreme":
        q = replace(q, probabilities=normalize({k: v * (level if k == "Extreme" else 1) for k, v in q.probabilities.items()}))
    if factor == "beta_location2":
        q = replace(q, beta={k: v * (level if k == q.locations[1] else 1) for k, v in q.beta.items()})
    if factor == "alpha_all":
        q = replace(q, alpha={k: v * level for k, v in q.alpha.items()})
    factors = {factor.removeprefix("benefit_"): level} if factor.startswith("benefit_") else None
    q = replace(q, benefit=benefit(q, factors))
    u = dict(base.upper_bound) if factor == "deploy_cost_fixed_U" else derived_u(q)
    if factor == "availability_U":
        u = {k: min(v, math.floor(base.upper_bound[k] * level + 1e-10)) for k, v in u.items()}
    return replace(q, upper_bound=u)


def joint(base, n=200):
    rng = np.random.Generator(np.random.PCG64(20261103))
    for draw in range(n):
        raw = {name: dict(zip(keys, rng.uniform(.8, 1.2, len(keys)).tolist())) for name, keys in (
            ("benefit", base.interventions), ("setup_cost", base.interventions),
            ("deploy_cost", base.interventions), ("availability", base.interventions),
            ("weights", tuple(base.benefit_weights)), ("beta", base.locations), ("probabilities", base.scenarios))}
        q = replace(base, setup_cost={(j, i): v * raw["setup_cost"][i] for (j, i), v in base.setup_cost.items()},
                    deploy_cost={(s, j, i): v * raw["deploy_cost"][i] for (s, j, i), v in base.deploy_cost.items()},
                    benefit_weights=normalize({k: v * raw["weights"][k] for k, v in base.benefit_weights.items()}),
                    beta={k: v * raw["beta"][k] for k, v in base.beta.items()},
                    probabilities=normalize({k: v * raw["probabilities"][k] for k, v in base.probabilities.items()}))
        q = replace(q, benefit=benefit(q, raw["benefit"]), upper_bound=derived_u(q))
        for mode in ("derived", "availability"):
            u = q.upper_bound if mode == "derived" else {k: min(v, math.floor(base.upper_bound[k] * raw["availability"][k[2]]))
                                                        for k, v in q.upper_bound.items()}
            yield replace(q, upper_bound=u), {"id": f"joint_{draw:03}_{mode}", "experiment": "joint",
                                             "draw": draw, "u_mode": mode, "multipliers": raw}


SETUP_LEVELS = (0.50, 0.75, 1.00, 1.25, 1.50, 2.00)
RESOURCE_LEVELS = (0.50, 0.75, 1.00, 1.25, 1.50)
RESOURCE_FIELDS = {
    "Labour": "labour_capacity",
    "Equipment": "equipment_capacity",
    "Supply": "supply_capacity",
}

def scaled_parameters(parameters: Any, parameter: str, multiplier: float) -> Any:
    """Change one capacity and recompute its mathematically derived bounds."""
    if not math.isfinite(multiplier) or multiplier < 0:
        raise ValueError("Capacity multiplier must be finite and nonnegative")
    if parameter == "Setup Budget":
        return dataclasses.replace(
            parameters, setup_budget=float(parameters.setup_budget) * multiplier
        )
    field = RESOURCE_FIELDS[parameter]
    baseline = getattr(parameters, field)
    changed = dataclasses.replace(
        parameters,
        **{field: {scenario: float(value) * multiplier for scenario, value in baseline.items()}},
    )
    return changed.with_recomputed_bounds()
