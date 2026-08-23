#!/usr/bin/env python3
"""Fail-closed release verifier for the effective e=4 Polydegree package.

This wrapper replays the exact normalization and eventual certificates under
normal and optimized Python, recomputes the finite ledger audit without
rewriting the ledger, verifies the normal/optimized ledger identity, and
binds the mathematical manuscript to the exact evidence bytes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANUSCRIPT = ROOT / "manuscripts" / "polydegree_e4_effective" / "manuscript.md"
EVENTUAL_SCRIPT = HERE / "e4_eventual_envelope.py"
EVENTUAL_RECEIPT = HERE / "e4_eventual_receipt.json"
NORMALIZATION_SCRIPT = HERE / "verify_normalization.py"
NORMALIZATION_RECEIPT = HERE / "e4_normalization_receipt.json"
FINITE_AUDITOR = HERE / "verify_finite_ledger.py"
FINITE_AUDIT_RECEIPT = HERE / "e4_finite_audit_v2.json"
FINITE_PRODUCER_RECEIPT = HERE / "e4_finite_receipt_v2_m0005_m4999.json"
FINITE_LEDGER = HERE / "e4_finite_cases_v2_m0005_m4999.jsonl"
FINITE_OPTIMIZED_LEDGER = HERE / "e4_finite_cases_v2_m0005_m4999_optimized_replay.jsonl"
RELEASE_RECEIPT = HERE / "P7A_RELEASE_RECEIPT.json"


class ReleaseError(RuntimeError):
    """A release predicate failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def require_supported_python(payload: dict[str, object], label: str) -> None:
    """Accept the two Python minor lines exercised by the public CI matrix."""
    environment = payload.get("environment")
    if isinstance(environment, dict):
        version = environment.get("python")
    else:
        version = payload.get("python")
    require(isinstance(version, str), f"{label} Python version is missing")
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    require(match is not None, f"{label} Python version is malformed: {version!r}")
    minor_line = (int(match.group(1)), int(match.group(2)))
    require(
        minor_line in {(3, 12), (3, 14)},
        f"{label} used unsupported Python minor line: {version}",
    )


def proof_payload(payload: dict[str, object], label: str) -> dict[str, object]:
    """Remove only the non-mathematical Python patch string from a receipt."""
    require_supported_python(payload, label)
    normalized = json.loads(json.dumps(payload))
    environment = normalized.get("environment")
    if isinstance(environment, dict):
        environment.pop("python")
    else:
        normalized.pop("python")
    return normalized


def module_audit(module_name: str, optimized: bool) -> dict[str, object]:
    program = (
        "import json,sys;"
        f"sys.path.insert(0,{str(HERE)!r});"
        f"import {module_name} as m;"
        "print(json.dumps(m.audit(),sort_keys=True,separators=(',',':')))"
    )
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-c", program])
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    require(
        completed.returncode == 0,
        f"{module_name} failed in {'optimized' if optimized else 'normal'} mode: "
        f"stdout={completed.stdout!r} stderr={completed.stderr!r}",
    )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    require(len(lines) == 1, f"{module_name} emitted {len(lines)} nonempty lines")
    try:
        payload = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise ReleaseError(f"{module_name} output is not JSON: {exc}") from exc
    require(isinstance(payload, dict), f"{module_name} audit is not a JSON object")
    return payload


def replay_eventual(expected: dict[str, object], optimized: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="hc4jc2-eventual-") as temporary:
        temporary_script = Path(temporary) / EVENTUAL_SCRIPT.name
        shutil.copyfile(EVENTUAL_SCRIPT, temporary_script)
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.append(str(temporary_script))
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        require(
            completed.returncode == 0,
            f"eventual verifier failed in {'optimized' if optimized else 'normal'} mode: "
            f"stdout={completed.stdout!r} stderr={completed.stderr!r}",
        )
        generated_path = temporary_script.with_name(EVENTUAL_RECEIPT.name)
        require(generated_path.is_file(), "eventual verifier did not write its receipt")
        generated = json.loads(generated_path.read_text(encoding="utf-8"))
        require(isinstance(generated, dict), "generated eventual receipt is not an object")
        require(
            proof_payload(generated, "generated eventual receipt")
            == proof_payload(expected, "stored eventual receipt"),
            f"eventual proof payload changed in {'optimized' if optimized else 'normal'} replay",
        )


def validate_finite_producer() -> dict[str, object]:
    receipt = json.loads(FINITE_PRODUCER_RECEIPT.read_text(encoding="utf-8"))
    require(receipt.get("status") == "CERTIFIED", "finite producer is not certified")
    require(receipt.get("case_count") == 14_985, "finite producer case count is not 14985")
    require(
        receipt.get("m_range") == {"start_inclusive": 5, "stop_exclusive": 5000},
        "finite producer coverage is not m=5,...,4999",
    )
    ledger = receipt.get("ledger")
    require(isinstance(ledger, dict), "finite producer ledger record is malformed")
    require(ledger.get("name") == FINITE_LEDGER.name, "finite ledger name mismatch")
    require(ledger.get("sha256") == sha256(FINITE_LEDGER), "finite ledger hash mismatch")
    sources = receipt.get("sources")
    require(isinstance(sources, dict), "finite producer source record is malformed")
    source_paths = {
        "driver": HERE / "e4_finite_bridge.py",
        "certification_core": HERE / "e4_certify_prototype.py",
        "locators": HERE / "small_locators_5_12.jsonl",
    }
    for name, path in source_paths.items():
        require(sources.get(name) == sha256(path), f"finite source hash mismatch: {name}")
    return receipt


def verify() -> dict[str, object]:
    required = (
        MANUSCRIPT,
        EVENTUAL_SCRIPT,
        EVENTUAL_RECEIPT,
        NORMALIZATION_SCRIPT,
        NORMALIZATION_RECEIPT,
        FINITE_AUDITOR,
        FINITE_AUDIT_RECEIPT,
        FINITE_PRODUCER_RECEIPT,
        FINITE_LEDGER,
        FINITE_OPTIMIZED_LEDGER,
    )
    for path in required:
        require(path.is_file(), f"required release artifact is missing: {path.relative_to(ROOT)}")

    expected_eventual = json.loads(EVENTUAL_RECEIPT.read_text(encoding="utf-8"))
    require(isinstance(expected_eventual, dict), "stored eventual receipt is not an object")
    replay_eventual(expected_eventual, optimized=False)
    replay_eventual(expected_eventual, optimized=True)

    normalization_normal = module_audit("verify_normalization", optimized=False)
    normalization_optimized = module_audit("verify_normalization", optimized=True)
    normalization_stored = json.loads(NORMALIZATION_RECEIPT.read_text(encoding="utf-8"))
    require(isinstance(normalization_stored, dict), "stored normalization receipt is not an object")
    require(
        proof_payload(normalization_normal, "normal normalization audit")
        == proof_payload(normalization_optimized, "optimized normalization audit"),
        "normalization proof payloads differ by mode",
    )
    require(
        proof_payload(normalization_normal, "fresh normalization audit")
        == proof_payload(normalization_stored, "stored normalization receipt"),
        "fresh normalization proof payload differs from the stored receipt",
    )

    validate_finite_producer()
    finite_normal = module_audit("verify_finite_ledger", optimized=False)
    finite_optimized = module_audit("verify_finite_ledger", optimized=True)
    finite_stored = json.loads(FINITE_AUDIT_RECEIPT.read_text(encoding="utf-8"))
    require(isinstance(finite_stored, dict), "stored finite audit receipt is not an object")
    require(
        proof_payload(finite_normal, "normal finite audit")
        == proof_payload(finite_optimized, "optimized finite audit"),
        "finite ledger proof payloads differ by mode",
    )
    require(
        proof_payload(finite_normal, "fresh finite audit")
        == proof_payload(finite_stored, "stored finite audit receipt"),
        "fresh finite proof payload differs from the stored receipt",
    )
    require(
        sha256(FINITE_LEDGER) == sha256(FINITE_OPTIMIZED_LEDGER),
        "normal and optimized finite ledgers are not byte-identical",
    )

    artifacts = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in required
    }
    return {
        "schema": "hc4jc2.polydegree-e4-release.v1",
        "status": "PASS",
        "theorem": "G_(d+4) subset closure(G_(d,5)) for every integer d>=2",
        "coverage": {
            "published": "2<=d<20 (Lewis--Perry--Straub)",
            "finite_arb": "d=4m+r, 5<=m<5000, r in {0,2,3}",
            "eventual": "d=4m+r, m>=5000, r in {0,2,3}",
            "exact": "d=4m+1, every m>=1",
        },
        "normal_optimized_replays": {
            "normalization": True,
            "eventual": True,
            "finite_structural_audit": True,
            "finite_ledger_byte_identity": True,
        },
        "artifact_sha256": artifacts,
        "environment": {
            "python": platform.python_version(),
        },
        "claim_boundary": (
            "Computer-assisted Polydegree containment proof. It is not a JC2 or HC4 "
            "result, external peer review, or independent reproduction."
        ),
    }


def main() -> int:
    try:
        result = verify()
        require(RELEASE_RECEIPT.is_file(), "stored release receipt is missing")
        stored = json.loads(RELEASE_RECEIPT.read_text(encoding="utf-8"))
        require(isinstance(stored, dict), "stored release receipt is not an object")
        require(
            proof_payload(result, "fresh release receipt")
            == proof_payload(stored, "stored release receipt"),
            "fresh release proof payload differs from the stored receipt",
        )
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "receipt": RELEASE_RECEIPT.name,
                    "receipt_sha256": sha256(RELEASE_RECEIPT),
                },
                sort_keys=True,
            )
        )
        return 0
    except ReleaseError as exc:
        print(json.dumps({"status": "FAIL", "message": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
