#!/usr/bin/env python3
"""Require release verifiers to reject three representative corruptions."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def run_failure(command: list[str], cwd: Path, label: str) -> None:
    completed = subprocess.run(command, cwd=cwd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if completed.returncode == 0:
        raise SystemExit(f"negative control unexpectedly passed: {label}")
    print(f"REJECTED {label}: exit={completed.returncode}")


def copy(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".lake", ".git", "__pycache__"))


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="e4-negative-") as temporary:
        base = Path(temporary)

        p7 = base / "p7"
        copy(ROOT / "p7a_effectivity", p7 / "p7a_effectivity")
        copy(ROOT / "manuscripts/polydegree_e4_effective", p7 / "manuscripts/polydegree_e4_effective")
        ledger = p7 / "p7a_effectivity/e4_finite_cases_v2_m0005_m4999.jsonl"
        data = ledger.read_bytes()
        ledger.write_bytes((b"0" if data[:1] != b"0" else b"1") + data[1:])
        run_failure([sys.executable, "p7a_effectivity/verify_release.py"], p7, "p7a-ledger-byte")

        formal = base / "formal"
        copy(ROOT / "formal/BorderedJacobianUniversal", formal)
        source = formal / "BorderedJacobianUniversal/Universal.lean"
        source.write_text(source.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        run_failure([sys.executable, "verify_release.py"], formal, "lean-source-byte")

        boundary = base / "boundary"
        copy(ROOT / "theorems", boundary / "theorems")
        theorem = boundary / "theorems/BOUNDARY_NORM_TRANSFER_THEOREM.md"
        theorem.write_text(theorem.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        run_failure([sys.executable, "theorems/verify_boundary_norm_release.py"], boundary, "boundary-theorem-byte")

    print("NEGATIVE CONTROLS PASS: 3/3 corruptions rejected")


if __name__ == "__main__":
    main()
