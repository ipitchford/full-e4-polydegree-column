#!/usr/bin/env python3
"""Deterministic Arb ledger for the finite e=4 Polydegree bridge.

For every requested m, this driver certifies residues 0, 2, and 3 using the
interval-Newton core in ``e4_certify_prototype.py``.  Residue 1 is covered by
an exact symbolic branch recorded in the aggregate receipt.  The default
half-open range 5 <= m < 5000 meets the uniform analytic certificate at 5000.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing
import os
import pathlib
import platform
import sys
import time
from typing import Iterable

import flint

import e4_certify_prototype as core


HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_START = 5
DEFAULT_STOP = 5_000
RESIDUES = (0, 2, 3)


class BridgeError(RuntimeError):
    """Raised when a finite-bridge acceptance condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BridgeError(message)


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_residue_one_branch() -> dict[str, object]:
    """Record the all-m algebraic solution for d = 4m+1.

    At X=(0,0,0), congruence leaves no constant term in rows q=1,2,3.
    Their only linear monomials are respectively X1, X2, X3, giving the
    displayed diagonal Jacobian.  The wrapped q=0 fourth row has constant 1.
    """
    return {
        "residue": 1,
        "range": "every integer m>=1",
        "point": ["0", "0", "0"],
        "first_three_rows": ["0", "0", "0"],
        "jacobian": {
            "shape": "diagonal",
            "diagonal": ["-(5m+2)/m", "-(5m+3)/m", "-(5m+4)/m"],
            "determinant": "-(5m+2)(5m+3)(5m+4)/m^3",
            "nonzero_for": "every integer m>=1",
        },
        "fourth_row_at_point": "1",
        "status": "EXACT",
    }


def preflight(m_start: int, m_stop: int) -> None:
    require(m_start >= DEFAULT_START, "finite bridge starts at m=5")
    require(m_stop > m_start, "m-stop must exceed m-start")
    require(m_stop <= DEFAULT_STOP, "m-stop must not pass the analytic handoff m=5000")
    require(core.ROOT_RADIUS_LIMIT == core.Fraction(1, 100), "unexpected root radius")
    require(core.DOMAIN_BOUND == core.Fraction(4, 5), "unexpected proof domain")
    for m in range(max(m_start, 5), min(m_stop, 17)):
        for residue in RESIDUES:
            require((m, residue) in core.SMALL_LOCATORS, f"missing stored locator m={m}, r={residue}")


def certify_m(m: int) -> list[dict[str, object]]:
    records = []
    for residue in RESIDUES:
        record = core.certify_case(m, residue)
        require(record["ok"] is True, f"case did not certify: m={m}, r={residue}")
        records.append(record)
    return records


def iter_certificates(
    values: Iterable[int], workers: int
) -> Iterable[list[dict[str, object]]]:
    if workers == 1:
        for value in values:
            yield certify_m(value)
        return
    context = multiprocessing.get_context("spawn")
    with context.Pool(processes=workers, maxtasksperchild=250) as pool:
        yield from pool.imap(certify_m, values, chunksize=1)


def default_workers() -> int:
    available = os.cpu_count() or 1
    return max(1, min(available, 12))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--m-start", type=int, default=DEFAULT_START)
    parser.add_argument("--m-stop", type=int, default=DEFAULT_STOP)
    parser.add_argument("--workers", type=int, default=default_workers())
    parser.add_argument("--ledger", type=pathlib.Path)
    parser.add_argument("--receipt", type=pathlib.Path)
    return parser.parse_args()


def chosen_paths(arguments: argparse.Namespace) -> tuple[pathlib.Path, pathlib.Path]:
    stem = f"m{arguments.m_start:04d}_m{arguments.m_stop - 1:04d}"
    ledger = arguments.ledger or HERE / f"e4_finite_cases_v2_{stem}.jsonl"
    receipt = arguments.receipt or HERE / f"e4_finite_receipt_v2_{stem}.json"
    return ledger.resolve(), receipt.resolve()


def source_hashes() -> dict[str, str]:
    paths = {
        "driver": pathlib.Path(__file__).resolve(),
        "certification_core": pathlib.Path(core.__file__).resolve(),
        "locators": pathlib.Path(core.LOCATOR_PATH).resolve(),
    }
    return {name: sha256(path) for name, path in paths.items()}


def run(arguments: argparse.Namespace) -> dict[str, object]:
    preflight(arguments.m_start, arguments.m_stop)
    require(arguments.workers >= 1, "workers must be positive")
    ledger_path, receipt_path = chosen_paths(arguments)
    require(not ledger_path.exists(), f"refusing to overwrite ledger: {ledger_path}")
    require(not receipt_path.exists(), f"refusing to overwrite receipt: {receipt_path}")
    partial_path = ledger_path.with_suffix(ledger_path.suffix + ".partial")
    require(not partial_path.exists(), f"remove or preserve existing partial ledger: {partial_path}")
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)

    started = time.monotonic()
    case_count = 0
    stored_count = 0
    formula_count = 0
    with partial_path.open("x", encoding="utf-8") as stream:
        for index, records in enumerate(
            iter_certificates(range(arguments.m_start, arguments.m_stop), arguments.workers),
            start=1,
        ):
            for record in records:
                stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
                case_count += 1
                if record["locator"] == "stored_decimal":
                    stored_count += 1
                else:
                    formula_count += 1
            if index % 100 == 0:
                elapsed = time.monotonic() - started
                print(
                    f"progress m={records[-1]['m']}: {case_count} cases; {elapsed:.1f}s",
                    file=sys.stderr,
                    flush=True,
                )
        stream.flush()
        os.fsync(stream.fileno())
    partial_path.replace(ledger_path)

    expected_count = 3 * (arguments.m_stop - arguments.m_start)
    require(case_count == expected_count, "case count does not match requested range")
    elapsed = time.monotonic() - started
    receipt = {
        "schema": "hc4jc2.polydegree-e4-finite-bridge.v2",
        "status": "CERTIFIED",
        "m_range": {"start_inclusive": arguments.m_start, "stop_exclusive": arguments.m_stop},
        "residues_certified_by_arb": list(RESIDUES),
        "case_count": case_count,
        "locator_counts": {"stored_decimal": stored_count, "asymptotic_formula": formula_count},
        "residue_one_exact_branch": exact_residue_one_branch(),
        "proof_predicates_per_case": [
            "Kantorovich h < 1/2",
            "certified root radius < 1/100",
            "fourth row nonzero throughout the root enclosure",
            "Jacobian nonzero throughout the root enclosure",
        ],
        "interval_serialization": (
            "Human-readable Arb intervals plus separately stored outward-rounded "
            "upper/lower endpoints; acceptance uses the endpoints."
        ),
        "ledger": {"name": ledger_path.name, "sha256": sha256(ledger_path)},
        "sources": source_hashes(),
        "environment": {
            "python": platform.python_version(),
            "python_flint": flint.__version__,
            "precision_bits": flint.ctx.prec,
            "workers": arguments.workers,
        },
        "elapsed_seconds_nonsemantic": round(elapsed, 3),
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"CERTIFIED: {case_count} Arb cases plus the exact residue-1 branch; "
        f"ledger_sha256={receipt['ledger']['sha256']}"
    )
    print(f"receipt: {receipt_path.name} sha256={sha256(receipt_path)}")
    return receipt


def main() -> None:
    arguments = parse_args()
    run(arguments)


if __name__ == "__main__":
    try:
        main()
    except (BridgeError, core.CertificationError) as error:
        print(f"CERTIFICATION FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
