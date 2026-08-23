#!/usr/bin/env python3
"""Fail-closed structural verifier for the public release projection."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
IGNORED_PARTS = {".git", ".lake", ".venv", "__pycache__"}
EXPECTED_REVIEW_MANIFEST = "867bff8d9b092a133194cf57a53d06dc3824d8aeb47508c5e5eec614bb8fc4a7"


class ReleaseError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    return (
        path.is_file()
        and path != MANIFEST
        and not any(part in IGNORED_PARTS for part in relative.parts)
        and path.suffix != ".pyc"
        and path.name != ".DS_Store"
    )


def parse_manifest() -> dict[str, str]:
    require(MANIFEST.is_file(), "MANIFEST.sha256 is missing")
    records: dict[str, str] = {}
    for number, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        digest, separator, relative = line.partition("  ")
        require(separator == "  " and re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"malformed manifest line {number}")
        require(relative not in records, f"duplicate manifest path: {relative}")
        require(relative != MANIFEST.name, "manifest must not hash itself")
        records[relative] = digest
    return records


def main() -> int:
    try:
        records = parse_manifest()
        actual = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if included(path)}
        require(actual == set(records), f"file-set mismatch: missing={sorted(set(records)-actual)!r}, unlisted={sorted(actual-set(records))!r}")
        mismatches = {name: {"expected": expected, "actual": sha256(ROOT / name)} for name, expected in records.items() if sha256(ROOT / name) != expected}
        require(not mismatches, f"SHA-256 mismatch: {mismatches!r}")

        aliases = {
            "papers/01-full-e4-polydegree-column.pdf": "manuscripts/polydegree_e4_effective/manuscript.pdf",
            "papers/02-universal-bordered-jacobian-formalization.pdf": "manuscripts/bordered_jacobian_formal/manuscript.pdf",
            "papers/03-boundary-norm-finite-pencil.pdf": "manuscripts/boundary_norm_transfer/manuscript.pdf",
        }
        for public, source in aliases.items():
            require((ROOT / public).read_bytes() == (ROOT / source).read_bytes(), f"paper alias differs: {public}")

        claims = json.loads((ROOT / "CLAIMS.json").read_text(encoding="utf-8"))
        require(claims.get("status") == "unrefereed-candidate", "claim status mismatch")
        require(claims.get("authors") == ["Anonymous"], "scholarly creator mismatch")
        require(len(claims.get("claims", [])) == 3, "expected three scoped claims")

        acceptance = json.loads((ROOT / "review/round2/INTERNAL_ACCEPTANCE.json").read_text(encoding="utf-8"))
        require(acceptance.get("submission_manifest_sha256") == EXPECTED_REVIEW_MANIFEST, "review target mismatch")
        require(acceptance.get("status") == "ACCEPT_INTERNAL_CANDIDATE_RELEASE", "internal review is not Accept")

        p7a = json.loads((ROOT / "p7a_effectivity/P7A_RELEASE_RECEIPT.json").read_text(encoding="utf-8"))
        boundary = json.loads((ROOT / "theorems/BOUNDARY_NORM_RECEIPT.json").read_text(encoding="utf-8"))
        formal = json.loads((ROOT / "formal/BorderedJacobianUniversal/FORMAL_RECEIPT.json").read_text(encoding="utf-8"))
        require(p7a.get("status") == "PASS" and boundary.get("status") == "PASS", "scientific receipt is not PASS")
        require(formal.get("verification", {}).get("build_exit_code") == 0, "formal build receipt is not successful")

        for path in ROOT.rglob("*"):
            if not included(path) or path.suffix.lower() not in {".md", ".txt", ".json", ".py", ".yml", ".yaml", ".toml", ".cff"} or path.stat().st_size > 5_000_000:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            private_prefix = "/Users" + "/admin"
            require(private_prefix not in text, f"private absolute path found: {path.relative_to(ROOT)}")
            zenodo_secret = "ZENODO" + "_ACCESS_TOKEN"
            openai_secret = "OPENAI" + "_API_KEY"
            require(zenodo_secret not in text and openai_secret not in text, f"secret variable found: {path.relative_to(ROOT)}")

        print(json.dumps({"status": "PASS", "manifestFiles": len(records), "reviewTarget": EXPECTED_REVIEW_MANIFEST, "claims": 3}, indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ReleaseError) as error:
        print(json.dumps({"status": "FAIL", "message": str(error)}, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
