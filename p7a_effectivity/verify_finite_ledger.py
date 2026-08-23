#!/usr/bin/env python3
"""Fail-closed structural and interval audit of the finite e=4 ledger."""

from __future__ import annotations

import hashlib
import json
import pathlib
import platform
import sys

import flint
from flint import arb


HERE = pathlib.Path(__file__).resolve().parent
RECEIPT_PATH = HERE / "e4_finite_receipt_v2_m0005_m4999.json"
AUDIT_PATH = HERE / "e4_finite_audit_v2.json"
RESIDUES = (0, 2, 3)


class AuditError(RuntimeError):
    """Raised when the ledger or its provenance is inconsistent."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_paths() -> dict[str, pathlib.Path]:
    return {
        "driver": HERE / "e4_finite_bridge.py",
        "certification_core": HERE / "e4_certify_prototype.py",
        "locators": HERE / "small_locators_5_12.jsonl",
    }


def audit() -> dict[str, object]:
    require(RECEIPT_PATH.is_file(), f"missing receipt: {RECEIPT_PATH}")
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    require(receipt["status"] == "CERTIFIED", "producer receipt is not certified")
    start = receipt["m_range"]["start_inclusive"]
    stop = receipt["m_range"]["stop_exclusive"]
    require((start, stop) == (5, 5_000), "unexpected finite-bridge range")
    ledger_path = HERE / receipt["ledger"]["name"]
    require(ledger_path.is_file(), f"missing ledger: {ledger_path}")
    require(sha256(ledger_path) == receipt["ledger"]["sha256"], "ledger hash mismatch")

    for name, path in source_paths().items():
        require(path.is_file(), f"missing source: {path}")
        require(sha256(path) == receipt["sources"][name], f"source hash mismatch: {name}")

    maximum_upper = {"h": None, "root_radius": None, "tail0": None, "tail1": None, "tail2": None}
    minimum_lower = {"next_margin": None, "jacobian_margin": None}
    maximum_case: dict[str, dict[str, int] | None] = {name: None for name in maximum_upper}
    minimum_case: dict[str, dict[str, int] | None] = {name: None for name in minimum_lower}
    stored_count = 0
    formula_count = 0
    line_count = 0

    with ledger_path.open("r", encoding="utf-8") as stream:
        for m in range(start, stop):
            for residue in RESIDUES:
                line = stream.readline()
                require(line != "", f"ledger ended before m={m}, r={residue}")
                line_count += 1
                record = json.loads(line)
                require((record["m"], record["r"]) == (m, residue), "case order mismatch")
                require(record["d"] == 4 * m + residue, "degree field mismatch")
                require(record["maximum_degree"] == record["d"] + 3, "maximum degree mismatch")
                expected_cutoff = record["maximum_degree"] if m <= 30 else 50
                require(record["cutoff"] == expected_cutoff, "cutoff mismatch")
                require(record["ok"] is True, "case-level status is not true")
                require(
                    set(record["checks"])
                    == {"h_lt_half", "root_in_domain", "next_row_nonzero", "jacobian_nonzero"},
                    "proof-predicate key mismatch",
                )
                require(all(value is True for value in record["checks"].values()), "false predicate")
                if record["locator"] == "stored_decimal":
                    stored_count += 1
                elif record["locator"] == "asymptotic_formula":
                    formula_count += 1
                else:
                    raise AuditError("unknown locator class")

                endpoint_fields = record["certified_endpoints"]
                upper_names = {
                    "h": "h_upper",
                    "root_radius": "root_radius_upper",
                    "tail0": "tail0_upper",
                    "tail1": "tail1_upper",
                    "tail2": "tail2_upper",
                }
                lower_names = {
                    "next_margin": "next_margin_lower",
                    "jacobian_margin": "jacobian_margin_lower",
                }
                require(
                    set(endpoint_fields) == set(upper_names.values()) | set(lower_names.values()),
                    "certified-endpoint key mismatch",
                )
                for name, endpoint_name in upper_names.items():
                    endpoint = arb(endpoint_fields[endpoint_name]).upper()
                    if maximum_upper[name] is None or maximum_upper[name] < endpoint:
                        maximum_upper[name] = endpoint
                        maximum_case[name] = {"m": m, "r": residue}
                for name, endpoint_name in lower_names.items():
                    endpoint = arb(endpoint_fields[endpoint_name]).lower()
                    if minimum_lower[name] is None or endpoint < minimum_lower[name]:
                        minimum_lower[name] = endpoint
                        minimum_case[name] = {"m": m, "r": residue}
        require(stream.readline() == "", "ledger contains trailing cases")

    expected_count = 3 * (stop - start)
    require(line_count == expected_count == receipt["case_count"], "case-count mismatch")
    require(
        {"stored_decimal": stored_count, "asymptotic_formula": formula_count}
        == receipt["locator_counts"],
        "locator-count mismatch",
    )
    require(maximum_upper["h"] < arb(1) / 2, "audited h ceiling is not below 1/2")
    require(maximum_upper["root_radius"] < arb(1) / 100, "audited root radius is too large")
    require(minimum_lower["next_margin"] > 0, "audited fourth-row margin is not positive")
    require(minimum_lower["jacobian_margin"] > 0, "audited Jacobian margin is not positive")

    return {
        "schema": "hc4jc2.polydegree-e4-finite-audit.v2",
        "status": "PASS",
        "producer_receipt": {"name": RECEIPT_PATH.name, "sha256": sha256(RECEIPT_PATH)},
        "ledger": {"name": ledger_path.name, "sha256": sha256(ledger_path)},
        "case_count": line_count,
        "coverage": "m=5,...,4999 in residues 0,2,3, in canonical order",
        "locator_counts": {"stored_decimal": stored_count, "asymptotic_formula": formula_count},
        "maximum_upper_endpoints": {
            name: {"value": str(value), "case": maximum_case[name]}
            for name, value in maximum_upper.items()
        },
        "minimum_lower_endpoints": {
            name: {"value": str(value), "case": minimum_case[name]}
            for name, value in minimum_lower.items()
        },
        "environment": {
            "python": platform.python_version(),
            "python_flint": flint.__version__,
            "precision_bits": flint.ctx.prec,
        },
        "auditor_sha256": sha256(pathlib.Path(__file__).resolve()),
    }


def main() -> None:
    require(not AUDIT_PATH.exists(), f"refusing to overwrite audit: {AUDIT_PATH}")
    result = audit()
    AUDIT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"AUDIT PASS: {result['case_count']} cases; sha256={sha256(AUDIT_PATH)}")


if __name__ == "__main__":
    try:
        main()
    except AuditError as error:
        print(f"AUDIT FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
