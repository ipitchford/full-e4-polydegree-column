#!/usr/bin/env python3
"""Replay and bind the boundary-norm finite-pencil certificate.

The proof of the abstract norm and pencil lemmas is mathematical text.  This
wrapper checks the exact six-sheet specialization in normal and optimized
Python, requires identical semantic output, and records hashes for the source
and both theorem statements.  No Python ``assert`` is used for a release gate.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "theorems" / "verify_six_sheet_pencil.py"
THEOREM_NOTE = ROOT / "theorems" / "BOUNDARY_NORM_TRANSFER_THEOREM.md"
MANUSCRIPT = ROOT / "manuscripts" / "boundary_norm_transfer" / "manuscript.md"
DEFAULT_RECEIPT = ROOT / "theorems" / "BOUNDARY_NORM_RECEIPT.json"


class VerificationError(RuntimeError):
    """A release condition failed."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run_checker(optimized: bool) -> dict[str, object]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.append(str(CHECKER))
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise VerificationError(
            f"checker failed in {'optimized' if optimized else 'normal'} mode: "
            f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
        )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise VerificationError(f"expected one JSON output line, got {len(lines)}")
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise VerificationError(f"checker output is not JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise VerificationError("checker JSON is not an object")
    return payload


def require_payload(payload: dict[str, object]) -> None:
    expected = {
        "status": "PASS",
        "field": "Q(sqrt(-15))",
        "alpha_relation": "alpha^2 + 3*alpha + 6 = 0",
        "kappa": 2,
        "gcd_degree": 0,
        "resultant": "2*alpha",
        "optimized_python_safe": True,
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            raise VerificationError(
                f"unexpected payload field {key!r}: "
                f"expected {value!r}, got {payload.get(key)!r}"
            )
    pencil = payload.get("pencil_tests")
    if not isinstance(pencil, list) or len(pencil) != 3:
        raise VerificationError("expected exactly three finite pencil tests")
    for target_degree, row in enumerate(pencil):
        if not isinstance(row, dict):
            raise VerificationError("pencil-test entry is not an object")
        if row.get("target_degree") != target_degree:
            raise VerificationError("pencil-test degrees are not ordered 0,1,2")
        if row.get("solution_nullity") != 0:
            raise VerificationError("a forbidden low monomial occurs")
    control = payload.get("negative_control")
    if not isinstance(control, list) or len(control) != 2:
        raise VerificationError("expected two negative-control tests")
    for target_degree, row in enumerate(control):
        if not isinstance(row, dict):
            raise VerificationError("negative-control entry is not an object")
        if row.get("target_degree") != target_degree:
            raise VerificationError("negative-control degrees are not ordered 0,1")
        if row.get("solution_nullity") != 1:
            raise VerificationError("negative control failed to expose a monomial")


def atomic_json_write(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as handle:
        handle.write(data)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def main() -> int:
    try:
        for path in (CHECKER, THEOREM_NOTE, MANUSCRIPT):
            if not path.is_file():
                raise VerificationError(f"required artifact is missing: {path.relative_to(ROOT)}")
        normal = run_checker(optimized=False)
        optimized = run_checker(optimized=True)
        require_payload(normal)
        require_payload(optimized)
        if normal != optimized:
            raise VerificationError("normal and optimized semantic outputs differ")

        receipt: dict[str, object] = {
            "schema": "hc4jc2.boundary-norm-pencil.v1",
            "status": "PASS",
            "claim_boundary": (
                "Exact finite-pencil specialization only; the norm lemma and "
                "BN transfer theorem remain mathematical-text obligations."
            ),
            "normal_optimized_semantic_identity": True,
            "result": normal,
            "source_hashes": {
                str(CHECKER.relative_to(ROOT)): sha256(CHECKER),
                str(THEOREM_NOTE.relative_to(ROOT)): sha256(THEOREM_NOTE),
                str(MANUSCRIPT.relative_to(ROOT)): sha256(MANUSCRIPT),
            },
            "environment": {
                "python": sys.version.split()[0],
                "sympy": normal.get("sympy_version"),
            },
        }
        atomic_json_write(DEFAULT_RECEIPT, receipt)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "receipt": str(DEFAULT_RECEIPT.relative_to(ROOT)),
                    "receipt_sha256": sha256(DEFAULT_RECEIPT),
                },
                sort_keys=True,
            )
        )
        return 0
    except VerificationError as exc:
        print(json.dumps({"status": "FAIL", "message": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
