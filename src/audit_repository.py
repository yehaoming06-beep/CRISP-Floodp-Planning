#!/usr/bin/env python3
"""Audit the organized package without importing or executing research code.

Uses only the Python standard library. Historical scientific validators are
preserved as evidence and are not invoked by this utility.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CI01 = "manuscript_revision/audit/ci01_independent_20261104"
PEER = "manuscript_revision/peer_review_validation_20261105_v2"
DOCUMENTS = (
    "README.md", "data/README.md", "src/README.md", "results/README.md",
    "supplementary/README.md", "supplementary/Supplementary_Methods_and_Results.md",
    "audit/Repository_Organization_Report.md", "audit/Manuscript_Alignment.md",
    "audit/Data_Rights_and_Access.md", "audit/Dependency_Evidence.md",
    "manuscript_revision/Supplementary_Methods_and_Results.md",
)
SECTION_TITLES = (
    "Scope and evidence versions",
    "EV conventions and complete baseline policy comparisons",
    "Controlled model components",
    "Hypothetical minimum geographic coverage",
    "Frozen spatial heterogeneity",
    "Frozen intervention subsets and one factor perturbations",
    "Frozen joint parameter stress tests",
    "Frozen legacy bounds and capacity grids",
    "Detailed procurement and inventory sensitivity",
    "Original event data and source ledger",
    "Scenario dependent illustrative requirements",
    "Reconstructed local warning frame and provenance",
    "Verification scope and source-reading boundaries",
)
# Inline links and images, including angle-bracket destinations and titles.
LINK = re.compile(r'(!?\[[^\]\n]*\]\()(<[^>\n]+>|[^\s)]+)([^)\n]*\))')
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai_token": re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b"),
    "github_token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})\b"),
    "aws_access_key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
}


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def contained_path(relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Expected a repository-relative path")
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError("Path resolves outside repository")
    return resolved


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        return list(reader)


def run_audit(submission_policy: bool = False) -> dict:
    errors: list[dict] = []
    advisories: list[dict] = []
    checks: dict = {}
    submission_inputs = {
        "01_Data/CRISP_Master_Data.xlsx", "01_Data/Events/model_input.csv",
        "01_Data/Events/event_metadata.csv", "01_Data/Controls/capacity_bound_reference.json",
        "01_Data/Controls/pre_cleanup_metrics.json", "01_Data/Controls/pre_cleanup_report_verification.json",
    } if submission_policy else set()
    if submission_policy:
        advisories.append({"check": "submission_policy", "detail":
            "Six reviewed numerical inputs and numerical audit execution logs are candidates. "
            "This is not redistribution clearance; THIRD_PARTY_NOTICES and the submission checklist still apply."})

    def error(check: str, path: str, detail: str) -> None:
        errors.append({"check": check, "path": path, "detail": detail})

    manifest_path = "audit/import_manifest.csv"
    imported: list[dict[str, str]] = []
    try:
        imported = csv_rows(ROOT / manifest_path)
        required = {"source_path", "repository_path", "sha256", "bytes", "git_policy"}
        if not imported or not required.issubset(imported[0]):
            raise ValueError("Import manifest is empty or lacks required columns")
        seen: set[str] = set()
        verified = 0
        for row in imported:
            rel = row["repository_path"]
            try:
                if rel in seen:
                    raise ValueError("Duplicate manifest destination")
                seen.add(rel)
                path = contained_path(rel)
                if not path.is_file():
                    raise ValueError("Imported file is missing")
                if path.stat().st_size != int(row["bytes"]):
                    raise ValueError("Byte count differs from import manifest")
                if digest(path) != row["sha256"].lower():
                    raise ValueError("SHA-256 differs from import manifest")
                verified += 1
            except (OSError, ValueError) as exc:
                error("import_integrity", rel, str(exc))
        checks["import_integrity"] = {"listed": len(imported), "verified": verified}
    except (OSError, ValueError) as exc:
        error("import_integrity", manifest_path, str(exc))

    # Parse every packaged Python file, including ignored imported files, but do
    # not traverse local environments/caches and never import research modules.
    excluded = {".git", ".venv", "venv", "env", "__pycache__", "node_modules"}
    parsed = 0
    for path in ROOT.rglob("*.py"):
        if excluded.intersection(path.relative_to(ROOT).parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            # ast.parse accepts bytes and respects a Python encoding declaration.
            ast.parse(path.read_bytes(), filename=rel)
            parsed += 1
        except (OSError, SyntaxError, ValueError) as exc:
            error("python_syntax", rel, str(exc))
    checks["python_syntax"] = {"parsed_without_execution": parsed}

    checked_links = 0
    for rel in DOCUMENTS:
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for match in LINK.finditer(text):
                target = match.group(2).strip("<>")
                parts = urlsplit(target)
                if parts.scheme or parts.netloc or not parts.path:
                    continue
                checked_links += 1
                resolved = ((ROOT / rel).parent / unquote(parts.path)).resolve()
                if not resolved.is_relative_to(ROOT):
                    error("local_links", rel, "Link escapes repository: " + target)
                elif not resolved.exists():
                    error("local_links", rel, "Missing link target: " + target)
        except (OSError, UnicodeError, ValueError) as exc:
            error("local_links", rel, str(exc))
    checks["local_links"] = {"documents": len(DOCUMENTS), "local_targets_checked": checked_links}

    supplement = "supplementary/Supplementary_Methods_and_Results.md"
    original = "manuscript_revision/Supplementary_Methods_and_Results.md"
    try:
        relocated = (ROOT / supplement).read_text(encoding="utf-8")
        source = (ROOT / original).read_text(encoding="utf-8")
        headings = re.findall(r"^## (S\d+) (.+)$", relocated, re.MULTILINE)
        expected = [(f"S{i}", title) for i, title in enumerate(SECTION_TITLES, 1)]
        if headings != expected:
            error("supplement_sections", supplement, "S1-S13 headings/order differ from the audited source")
        # Preserve labels, titles, prose, numbers, whitespace and external links.
        # Only destination strings are omitted for this relocation comparison.
        def omit_destinations(text: str) -> str:
            return LINK.sub(lambda match: match.group(1) + "LINK_TARGET" + match.group(3), text)
        same = omit_destinations(relocated) == omit_destinations(source)
        if not same:
            error("supplement_text", supplement, "Text differs beyond Markdown link destinations")
        checks["supplement"] = {"section_headings": headings, "text_unchanged_except_link_destinations": same}
    except (OSError, UnicodeError) as exc:
        error("supplement", supplement, str(exc))

    expected_tables = {
        "04_Results/Optimization/summary.csv": 555,
        "04_Results/Optimization/solver_audit.csv": 3875,
        CI01 + "/backend_probability60/summary.csv": 555,
        CI01 + "/backend_probability60/solver_audit.csv": 3888,
        PEER + "/runs/primary/solver_audit.csv": 500,
        PEER + "/runs/primary/ev_all_policy_trials.csv": 416,
        PEER + "/runs/primary/component_summary.csv": 24,
        PEER + "/runs/primary/coverage_summary.csv": 8,
    }
    counts: dict = {}
    for rel, expected in expected_tables.items():
        try:
            rows = csv_rows(ROOT / rel)
            counts[rel] = {"expected": expected, "observed": len(rows)}
            if len(rows) != expected:
                error("experiment_counts", rel, f"Expected {expected} records; found {len(rows)}")
            if rel == PEER + "/runs/primary/solver_audit.csv":
                states = dict(Counter(row.get("status", "") for row in rows))
                counts[rel]["status_counts"] = states
                if states != {"OPTIMAL": 498, "INFEASIBLE": 2}:
                    error("experiment_counts", rel, "Expected 498 OPTIMAL and 2 INFEASIBLE")
        except (OSError, ValueError) as exc:
            error("experiment_counts", rel, str(exc))
    checks["experiment_counts"] = counts

    # Historical whole-workspace guards are not portable subset certificates.
    # Report absent original paths as an advisory, never as a new scientific PASS.
    guard_rel = PEER + "/frozen_manifest_before.json"
    try:
        historical = json.loads((ROOT / guard_rel).read_text(encoding="utf-8"))
        if not isinstance(historical, dict):
            raise ValueError("Expected historical guard mapping")
        missing = 0
        different = 0
        matching = 0
        for rel, expected_hash in historical.items():
            path = contained_path(rel)
            if not path.is_file():
                missing += 1
            elif digest(path) != expected_hash:
                different += 1
            else:
                matching += 1
        advisories.append({
            "check": "historical_workspace_guard", "path": guard_rel,
            "original_paths": len(historical), "absent_in_organized_package": missing,
            "present_with_different_hash": different,
            "present_with_matching_hash": matching,
            "detail": "Archived whole-workspace guard was not reexecuted; subset integrity does not establish historical guard completeness or numerical reproducibility.",
        })
    except (OSError, ValueError, TypeError) as exc:
        advisories.append({"check": "historical_workspace_guard", "path": guard_rel, "detail": str(exc)})

    candidates: list[str] = []
    try:
        command = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        candidates = sorted(set(command.stdout.decode("utf-8").split("\0")) - {""})
        unsafe_parts = {".venv", "venv", "env", "__pycache__", ".cache", ".pytest_cache", "node_modules"}
        unsafe_names = {".ds_store", ".envrc", "credentials", "credentials.json", "secrets.toml", "gurobi.lic"}
        for rel in candidates:
            path = contained_path(rel)
            parts = {part.lower() for part in Path(rel).parts}
            name = path.name.lower()
            execution_log = submission_policy and path.suffix.lower() == ".log" and (
                rel.startswith("audit/reproducibility_20261118/") or
                rel.startswith("audit/submission_20261118/clean_run/"))
            if (parts & unsafe_parts or name in unsafe_names or name == ".env"
                    or name.startswith(".env.") or path.suffix.lower() in {".zip", ".key", ".pem", ".p12", ".headers"}
                    or (path.suffix.lower() == ".log" and not execution_log)
                    or name == "network_probe_headers.txt"):
                error("git_safety", rel, "Environment, cache, credential, raw-log or archive path is a Git candidate")
            if "sources" in parts and name not in {"readme.md", "index.md"}:
                error("git_safety", rel, "Raw third-party source archive is a Git candidate")
            if path.is_file() and path.stat().st_size <= 5 * 1024 * 1024:
                data = path.read_bytes()
                if b"\0" in data:
                    continue
                text = data.decode("utf-8", errors="replace")
                for label, pattern in SECRET_PATTERNS.items():
                    match = pattern.search(text)
                    if match:
                        error("credential_scan", rel, f"Possible {label} at line {text.count(chr(10), 0, match.start()) + 1}; value withheld")
        # Explicitly withheld import rows must not enter a future default add.
        candidate_set = set(candidates)
        for row in imported:
            policy = row["git_policy"].lower().replace("_", "-")
            if any(word in policy for word in ("local", "withheld", "restricted", "exclude")):
                if row["repository_path"] in candidate_set and row["repository_path"] not in submission_inputs:
                    error("git_policy", row["repository_path"], "Manifest marks this import as withheld/local but Git considers it a candidate")
        checks["git_safety"] = {"candidate_files": len(candidates), "submission_policy": submission_policy, "credential_scan": "Recognizable token patterns in UTF-8-like candidate files <=5 MiB; not an exhaustive secret detector"}
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        error("git_safety", ".", str(exc))

    return {
        "status": "PASS" if not errors else "FAIL",
        "scope": "Package integrity, source syntax, selected links, section structure, archived table counts and Git candidate hygiene; no research code executed",
        "audited_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks, "errors": errors, "advisories": advisories,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Also save JSON inside results/repository_audit/ only")
    parser.add_argument("--submission-policy", action="store_true",
                        help="Use reviewed minimal-input/execution-log exceptions without implying release clearance")
    args = parser.parse_args()
    output = None
    if args.output is not None:
        output = args.output.resolve()
        allowed = (ROOT / "results/repository_audit").resolve()
        if output == allowed or not output.is_relative_to(allowed) or output.suffix.lower() != ".json":
            parser.error("--output must be a .json file inside results/repository_audit/")
    result = run_audit(args.submission_policy)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
