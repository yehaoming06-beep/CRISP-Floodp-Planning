#!/usr/bin/env python3
"""Read the current CRISP workbook and calculate resource-derived bounds.

The original CU/score block is illustrative. Mobile stock and census metadata
are maintained in separate workbook sheets and read by the current model.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

from openpyxl import load_workbook


SCENARIO_ORDER = ("Moderate", "Severe", "Extreme")
TOLERANCE = 1e-6


@dataclass(frozen=True)
class Parameters:
    scenarios: Tuple[str, ...]
    locations: Tuple[str, ...]
    interventions: Tuple[str, ...]
    probabilities: Mapping[str, float]
    setup_budget: float
    operating_budget: Mapping[str, float]
    labour_capacity: Mapping[str, float]
    equipment_capacity: Mapping[str, float]
    supply_capacity: Mapping[str, float]
    benefit_weights: Mapping[str, float]
    setup_cost: Mapping[Tuple[str, str], float]
    deploy_cost: Mapping[Tuple[str, str, str], float]
    labour: Mapping[Tuple[str, str, str], float]
    equipment: Mapping[Tuple[str, str, str], float]
    supply: Mapping[Tuple[str, str, str], float]
    upper_bound: Mapping[Tuple[str, str, str], int]
    life_score: Mapping[str, float]
    property_score: Mapping[str, float]
    recovery_score: Mapping[str, float]
    alpha: Mapping[Tuple[str, str], float]
    beta: Mapping[str, float]
    benefit: Mapping[Tuple[str, str, str], float]

    def with_recomputed_bounds(self) -> "Parameters":
        """Rebuild derived linking bounds after a budget, resource or cost change.

        These bounds are mathematical consequences of the four resource rows,
        not independently observed inventory limits. Separate inventory limits
        belong in explicit model constraints (see crisp_mobile_pump_model.py).
        """
        return replace(self, upper_bound=derive_upper_bounds(self))


def derive_upper_bounds(parameters: Parameters) -> Dict[Tuple[str, str, str], int]:
    bounds = {}
    for key in parameters.benefit:
        ratios = []
        for coefficient, capacity in (("deploy_cost", "operating_budget"),
                                      ("labour", "labour_capacity"),
                                      ("equipment", "equipment_capacity"),
                                      ("supply", "supply_capacity")):
            use = float(getattr(parameters, coefficient)[key])
            available = float(getattr(parameters, capacity)[key[0]])
            if not math.isfinite(use) or use < 0 or not math.isfinite(available) or available < 0:
                raise ValueError(f"Invalid {coefficient}/{capacity} value for {key}")
            if use > 0:
                ratios.append(available / use)
        if not ratios:
            raise ValueError(f"No finite resource-derived upper bound for {key}")
        bounds[key] = math.floor(min(ratios) + 1e-10)
    return bounds


def _require_number(value: Any, label: str) -> float:
    if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Missing or non-numeric workbook value for {label}: {value!r}")
    if not math.isfinite(float(value)):
        raise ValueError(f"Non-finite workbook value for {label}: {value!r}")
    return float(value)


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing or non-text workbook value for {label}: {value!r}")
    return value.strip()


def _close(a: float, b: float, tol: float = TOLERANCE) -> bool:
    return abs(a - b) <= tol


def load_inputs(workbook_path: Path) -> Parameters:
    """Read all model inputs directly from the four required workbook sheets."""
    wb = load_workbook(workbook_path, data_only=True, read_only=True)
    required_sheets = {"Scenario", "Baseline_Settings", "Intervention_Params", "Benefit_Params"}
    missing = required_sheets.difference(wb.sheetnames)
    if missing:
        raise ValueError(f"Required input sheets missing: {sorted(missing)}")

    ws_scenario = wb["Scenario"]
    probabilities: Dict[str, float] = {}
    for row in range(4, 7):
        scenario = _require_text(ws_scenario.cell(row, 1).value, f"Scenario!A{row}")
        probabilities[scenario] = _require_number(ws_scenario.cell(row, 2).value, f"Scenario!B{row}")
    if tuple(probabilities) != SCENARIO_ORDER:
        raise ValueError(f"Unexpected scenario order/names: {tuple(probabilities)}")

    ws_base = wb["Baseline_Settings"]
    operating_budget: Dict[str, float] = {}
    labour_capacity: Dict[str, float] = {}
    equipment_capacity: Dict[str, float] = {}
    supply_capacity: Dict[str, float] = {}
    for row in range(5, 8):
        scenario = _require_text(ws_base.cell(row, 1).value, f"Baseline_Settings!A{row}")
        operating_budget[scenario] = _require_number(ws_base.cell(row, 2).value, f"Baseline_Settings!B{row}")
        labour_capacity[scenario] = _require_number(ws_base.cell(row, 3).value, f"Baseline_Settings!C{row}")
        equipment_capacity[scenario] = _require_number(ws_base.cell(row, 4).value, f"Baseline_Settings!D{row}")
        supply_capacity[scenario] = _require_number(ws_base.cell(row, 5).value, f"Baseline_Settings!E{row}")
    setup_budget = _require_number(ws_base["B11"].value, "Baseline_Settings!B11")
    benefit_weights = {
        "w_L": _require_number(ws_base["B15"].value, "Baseline_Settings!B15"),
        "w_P": _require_number(ws_base["B16"].value, "Baseline_Settings!B16"),
        "w_R": _require_number(ws_base["B17"].value, "Baseline_Settings!B17"),
    }

    ws_intervention = wb["Intervention_Params"]
    setup_cost: Dict[Tuple[str, str], float] = {}
    deploy_cost: Dict[Tuple[str, str, str], float] = {}
    labour: Dict[Tuple[str, str, str], float] = {}
    equipment: Dict[Tuple[str, str, str], float] = {}
    supply: Dict[Tuple[str, str, str], float] = {}
    upper_bound: Dict[Tuple[str, str, str], int] = {}
    seen_locations = []
    seen_interventions = []
    for row in range(4, 22):
        scenario = _require_text(ws_intervention.cell(row, 1).value, f"Intervention_Params!A{row}")
        location = _require_text(ws_intervention.cell(row, 2).value, f"Intervention_Params!B{row}")
        intervention = _require_text(ws_intervention.cell(row, 3).value, f"Intervention_Params!C{row}")
        if location not in seen_locations:
            seen_locations.append(location)
        if intervention not in seen_interventions:
            seen_interventions.append(intervention)
        key = (scenario, location, intervention)
        pair = (location, intervention)
        row_setup = _require_number(ws_intervention.cell(row, 4).value, f"Intervention_Params!D{row}")
        if pair in setup_cost and not _close(setup_cost[pair], row_setup):
            raise ValueError(f"Inconsistent setup cost for {pair}: {setup_cost[pair]} vs {row_setup}")
        setup_cost[pair] = row_setup
        deploy_cost[key] = _require_number(ws_intervention.cell(row, 5).value, f"Intervention_Params!E{row}")
        labour[key] = _require_number(ws_intervention.cell(row, 6).value, f"Intervention_Params!F{row}")
        equipment[key] = _require_number(ws_intervention.cell(row, 7).value, f"Intervention_Params!G{row}")
        supply[key] = _require_number(ws_intervention.cell(row, 8).value, f"Intervention_Params!H{row}")
        u_value = _require_number(ws_intervention.cell(row, 13).value, f"Intervention_Params!M{row}")
        if not _close(u_value, round(u_value)) or u_value < 0:
            raise ValueError(f"Derived U_ijs must be a nonnegative integer at row {row}: {u_value}")
        upper_bound[key] = int(round(u_value))
        row_caps = (
            _require_number(ws_intervention.cell(row, 9).value, f"Intervention_Params!I{row}"),
            _require_number(ws_intervention.cell(row, 10).value, f"Intervention_Params!J{row}"),
            _require_number(ws_intervention.cell(row, 11).value, f"Intervention_Params!K{row}"),
            _require_number(ws_intervention.cell(row, 12).value, f"Intervention_Params!L{row}"),
        )
        expected_caps = (
            operating_budget[scenario], labour_capacity[scenario],
            equipment_capacity[scenario], supply_capacity[scenario],
        )
        if any(not _close(a, b) for a, b in zip(row_caps, expected_caps)):
            raise ValueError(f"Capacity mismatch between source sheets for {key}")

    ws_benefit = wb["Benefit_Params"]
    life_score: Dict[str, float] = {}
    property_score: Dict[str, float] = {}
    recovery_score: Dict[str, float] = {}
    alpha: Dict[Tuple[str, str], float] = {}
    beta: Dict[str, float] = {}
    benefit: Dict[Tuple[str, str, str], float] = {}
    for row in range(4, 22):
        scenario = _require_text(ws_benefit.cell(row, 1).value, f"Benefit_Params!A{row}")
        location = _require_text(ws_benefit.cell(row, 2).value, f"Benefit_Params!B{row}")
        intervention = _require_text(ws_benefit.cell(row, 3).value, f"Benefit_Params!C{row}")
        key = (scenario, location, intervention)
        scores = (
            _require_number(ws_benefit.cell(row, 4).value, f"Benefit_Params!D{row}"),
            _require_number(ws_benefit.cell(row, 5).value, f"Benefit_Params!E{row}"),
            _require_number(ws_benefit.cell(row, 6).value, f"Benefit_Params!F{row}"),
        )
        for target, value, label in zip(
            (life_score, property_score, recovery_score), scores, ("life", "property", "recovery")
        ):
            if intervention in target and not _close(target[intervention], value):
                raise ValueError(f"Inconsistent {label} score for {intervention}")
            target[intervention] = value
        alpha_value = _require_number(ws_benefit.cell(row, 7).value, f"Benefit_Params!G{row}")
        alpha_key = (scenario, intervention)
        if alpha_key in alpha and not _close(alpha[alpha_key], alpha_value):
            raise ValueError(f"Inconsistent alpha for {alpha_key}")
        alpha[alpha_key] = alpha_value
        beta_value = _require_number(ws_benefit.cell(row, 8).value, f"Benefit_Params!H{row}")
        if location in beta and not _close(beta[location], beta_value):
            raise ValueError(f"Inconsistent beta for {location}")
        beta[location] = beta_value
        benefit[key] = _require_number(ws_benefit.cell(row, 10).value, f"Benefit_Params!J{row}")

    wb.close()

    scenarios = tuple(probabilities)
    locations = tuple(seen_locations)
    interventions = tuple(seen_interventions)
    expected_keys = {(s, j, i) for s in scenarios for j in locations for i in interventions}
    for name, mapping in {
        "deploy_cost": deploy_cost,
        "labour": labour,
        "equipment": equipment,
        "supply": supply,
        "upper_bound": upper_bound,
        "benefit": benefit,
    }.items():
        if set(mapping) != expected_keys:
            raise ValueError(f"{name} keys differ from the required 18 combinations")
    expected_pairs = {(j, i) for j in locations for i in interventions}
    if set(setup_cost) != expected_pairs:
        raise ValueError("Setup-cost keys differ from the required location-intervention pairs")
    if len(expected_keys) != 18:
        raise ValueError(f"Expected exactly 18 scenario-location-intervention combinations, found {len(expected_keys)}")
    probability_sum = sum(probabilities.values())
    if not _close(probability_sum, 1.0):
        raise ValueError(f"Scenario probabilities sum to {probability_sum}, not 1")

    return Parameters(
        scenarios=scenarios,
        locations=locations,
        interventions=interventions,
        probabilities=probabilities,
        setup_budget=setup_budget,
        operating_budget=operating_budget,
        labour_capacity=labour_capacity,
        equipment_capacity=equipment_capacity,
        supply_capacity=supply_capacity,
        benefit_weights=benefit_weights,
        setup_cost=setup_cost,
        deploy_cost=deploy_cost,
        labour=labour,
        equipment=equipment,
        supply=supply,
        upper_bound=upper_bound,
        life_score=life_score,
        property_score=property_score,
        recovery_score=recovery_score,
        alpha=alpha,
        beta=beta,
        benefit=benefit,
    )


def _parameters_to_json(parameters: Parameters) -> Dict[str, Any]:
    def rows(mapping: Mapping[Tuple[str, ...], Any], labels: Iterable[str]) -> list[Dict[str, Any]]:
        label_list = list(labels)
        return [{**dict(zip(label_list, key)), "value": value} for key, value in mapping.items()]

    return {
        "probabilities": dict(parameters.probabilities), "setup_budget": parameters.setup_budget,
        "operating_budget": dict(parameters.operating_budget),
        "labour_capacity": dict(parameters.labour_capacity),
        "equipment_capacity": dict(parameters.equipment_capacity),
        "supply_capacity": dict(parameters.supply_capacity),
        "benefit_weights": dict(parameters.benefit_weights),
        "setup_cost": rows(parameters.setup_cost, ("location", "intervention")),
        "deploy_cost": rows(parameters.deploy_cost, ("scenario", "location", "intervention")),
        "labour": rows(parameters.labour, ("scenario", "location", "intervention")),
        "equipment": rows(parameters.equipment, ("scenario", "location", "intervention")),
        "supply": rows(parameters.supply, ("scenario", "location", "intervention")),
        "upper_bound": rows(parameters.upper_bound, ("scenario", "location", "intervention")),
        "life_score": dict(parameters.life_score), "property_score": dict(parameters.property_score),
        "recovery_score": dict(parameters.recovery_score),
        "alpha": rows(parameters.alpha, ("scenario", "intervention")),
        "beta": dict(parameters.beta),
        "benefit": rows(parameters.benefit, ("scenario", "location", "intervention")),
    }

