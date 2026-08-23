#!/usr/bin/env python3
"""Fail-closed, read-only replay for the P7b Lean release."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent
RECEIPT = ROOT / "FORMAL_RECEIPT.json"
IGNORED_TOP_LEVEL = {".lake", ".git"}
FORBIDDEN_LEAN = re.compile(
    r"\bsorry\b|\badmit\b|\baxiom\b|sorryAx|native_decide|\bunsafe\b|simp\?"
)


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(*command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def release_files() -> set[str]:
    files: set[str] = set()
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[0] in IGNORED_TOP_LEVEL:
            continue
        files.add(relative.as_posix())
    return files


def fail(message: str, details: Any | None = None) -> None:
    result: dict[str, Any] = {"status": "FAIL", "message": message}
    if details is not None:
        result["details"] = details
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(1)


def main() -> None:
    try:
        receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail("cannot read FORMAL_RECEIPT.json", str(error))

    expected_hashes: dict[str, str] = receipt["files_sha256"]
    expected_files = set(expected_hashes) | {RECEIPT.name}
    actual_files = release_files()
    if actual_files != expected_files:
        fail(
            "release file set differs from receipt",
            {
                "missing": sorted(expected_files - actual_files),
                "unlisted": sorted(actual_files - expected_files),
            },
        )

    mismatches = {
        name: {"expected": expected, "actual": sha256(ROOT / name)}
        for name, expected in expected_hashes.items()
        if sha256(ROOT / name) != expected
    }
    if mismatches:
        fail("SHA-256 mismatch", mismatches)

    lean = run("lean", "--version")
    if lean.returncode != 0 or receipt["toolchain"]["lean_version"] not in lean.stdout:
        fail("Lean version mismatch", lean.stdout.strip())

    lake = run("lake", "--version")
    if lake.returncode != 0 or receipt["toolchain"]["lake_version"] not in lake.stdout:
        fail("Lake version mismatch", lake.stdout.strip())

    mathlib = run("git", "-C", ".lake/packages/mathlib", "rev-parse", "HEAD")
    if mathlib.returncode != 0:
        fail("cannot resolve local Mathlib commit", mathlib.stdout.strip())
    if mathlib.stdout.strip() != receipt["toolchain"]["mathlib_commit"]:
        fail("Mathlib commit mismatch", mathlib.stdout.strip())

    forbidden: dict[str, list[dict[str, Any]]] = {}
    project_sources = [ROOT / "BorderedJacobianUniversal.lean"]
    project_sources.extend(
        sorted((ROOT / "BorderedJacobianUniversal").rglob("*.lean"))
    )
    for source in project_sources:
        matches = []
        for line_number, line in enumerate(
            source.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for match in FORBIDDEN_LEAN.finditer(line):
                matches.append({"line": line_number, "token": match.group(0)})
        if matches:
            forbidden[source.relative_to(ROOT).as_posix()] = matches
    if forbidden:
        fail("forbidden Lean construct found", forbidden)

    build = run("lake", "build")
    if build.returncode != 0:
        fail("lake build failed", build.stdout[-12000:])
    if "warning:" in build.stdout:
        fail("lake build completed with warnings", build.stdout[-12000:])
    if "sorryAx" in build.stdout:
        fail("axiom receipt contains sorryAx", build.stdout[-12000:])
    if "Build completed successfully" not in build.stdout:
        fail("success marker missing from lake build", build.stdout[-12000:])

    print(
        json.dumps(
            {
                "status": "PASS",
                "receipt_schema": receipt["schema"],
                "verified_files": len(expected_hashes),
                "lean": lean.stdout.strip(),
                "lake": lake.stdout.strip(),
                "mathlib_commit": mathlib.stdout.strip(),
                "source_scan": "PASS",
                "build": "PASS_WITHOUT_WARNINGS_OR_SORRYAX",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
