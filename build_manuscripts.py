#!/usr/bin/env python3
"""Typeset and inspect the three HC4JC2 successor manuscripts."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Manuscript:
    directory: str
    title: str
    required_text: tuple[str, ...]


MANUSCRIPTS = (
    Manuscript(
        "polydegree_e4_effective",
        "Effective Fourier certificates for the full (e=4) Polydegree column",
        ("Theorem A", "For every integer d", "Lewis", "Arb"),
    ),
    Manuscript(
        "bordered_jacobian_formal",
        "Formal verification of a universal bordered Jacobian identity over arbitrary commutative rings",
        ("Theorem 1.1", "arbitrary commutative ring", "Lean 4.32.1"),
    ),
    Manuscript(
        "boundary_norm_transfer",
        "A finite pencil criterion for boundary-norm graph obstructions",
        ("Theorem 5.1", "cover-degree-free norm lemma", "finite pencil"),
    ),
)


class BuildError(RuntimeError):
    """A typesetting or PDF inspection condition failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise BuildError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stdout[-8000:]}\n{completed.stderr[-8000:]}"
        )
    return completed.stdout + completed.stderr


def source_without_duplicate_title(source: Path, expected_title: str) -> str:
    text = source.read_text(encoding="utf-8")
    lines = text.splitlines()
    require(lines and lines[0].startswith("# "), f"missing H1 title in {source}")
    actual_title = lines[0][2:].strip()
    require(actual_title == expected_title, f"unexpected title in {source}: {actual_title!r}")
    remainder = lines[1:]
    if remainder and remainder[0] == "":
        remainder = remainder[1:]
    return "\n".join(remainder) + "\n"


def pandoc_command(source: Path, tex_output: Path, title: str) -> list[str]:
    return [
        "pandoc",
        str(source),
        "--from=markdown+tex_math_dollars+tex_math_single_backslash+raw_tex",
        "--to=latex",
        "--standalone",
        f"--metadata=title:{title}",
        "--metadata=date:23 August 2026",
        "-V",
        "papersize:a4",
        "-V",
        "geometry:margin=24mm",
        "-V",
        "fontsize=11pt",
        "-V",
        "colorlinks=true",
        "-V",
        "linkcolor=blue",
        "-V",
        "urlcolor=blue",
        "-V",
        r"header-includes=\usepackage{mathtools}",
        "-V",
        r"header-includes=\allowdisplaybreaks",
        "-V",
        r"header-includes=\setlength{\emergencystretch}{6em}",
        "-V",
        r"header-includes=\DeclareUnicodeCharacter{2084}{\ensuremath{_4}}",
        f"--output={tex_output}",
    ]


def inspect_log(log_path: Path) -> dict[str, object]:
    log = log_path.read_text(encoding="utf-8", errors="replace")
    forbidden = (
        "Undefined control sequence",
        "LaTeX Error",
        "Citation `",
        "Reference `",
        "There were undefined references",
    )
    for marker in forbidden:
        require(marker not in log, f"{log_path.name} contains {marker!r}")
    overfull_values = [
        float(value)
        for value in re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide\)", log)
    ]
    maximum = max(overfull_values, default=0.0)
    require(maximum <= 2.0, f"{log_path.name} has an overfull box of {maximum:.3f}pt")
    return {
        "overfull_box_count": len(overfull_values),
        "maximum_overfull_pt": maximum,
        "underfull_box_count": log.count("Underfull \\hbox"),
    }


def build_one(item: Manuscript) -> dict[str, object]:
    directory = ROOT / "manuscripts" / item.directory
    markdown = directory / "manuscript.md"
    tex = directory / "manuscript.tex"
    pdf = directory / "manuscript.pdf"
    text_output = directory / "manuscript.txt"
    require(markdown.is_file(), f"missing manuscript: {markdown}")

    transformed = source_without_duplicate_title(markdown, item.title)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".md",
        dir=directory,
        prefix=".typeset-",
        delete=False,
    ) as handle:
        handle.write(transformed)
        temporary_source = Path(handle.name)
    try:
        run(pandoc_command(temporary_source, tex, item.title), directory)
    finally:
        temporary_source.unlink(missing_ok=True)

    run(
        [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            tex.name,
        ],
        directory,
    )
    run(["pdftotext", "-layout", pdf.name, text_output.name], directory)

    extracted = text_output.read_text(encoding="utf-8", errors="replace")
    normalized_text = re.sub(r"\s+", " ", extracted)
    require(item.title in normalized_text, f"PDF text does not contain title: {item.title}")
    for phrase in item.required_text:
        require(phrase in normalized_text, f"PDF text is missing required phrase {phrase!r}")
    require("textbackslash" not in normalized_text, "PDF exposes a mangled TeX backslash")

    metrics = inspect_log(directory / "manuscript.log")
    page_output = run(["pdfinfo", pdf.name], directory)
    page_match = re.search(r"^Pages:\s+(\d+)$", page_output, flags=re.MULTILINE)
    require(page_match is not None, f"cannot read page count for {pdf}")
    return {
        "directory": item.directory,
        "title": item.title,
        "pages": int(page_match.group(1)),
        "sha256": {
            "markdown": sha256(markdown),
            "tex": sha256(tex),
            "pdf": sha256(pdf),
            "text": sha256(text_output),
        },
        "log_metrics": metrics,
        "pdf_text_gate": "PASS",
    }


def atomic_write(path: Path, payload: dict[str, object]) -> None:
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
        results = [build_one(item) for item in MANUSCRIPTS]
        receipt = {
            "schema": "hc4jc2.successor-manuscript-build.v1",
            "status": "PASS",
            "pandoc": run(["pandoc", "--version"], ROOT).splitlines()[0],
            "latexmk": run(["latexmk", "-v"], ROOT).splitlines()[0],
            "manuscripts": results,
        }
        receipt_path = ROOT / "MANUSCRIPT_BUILD_RECEIPT.json"
        atomic_write(receipt_path, receipt)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "receipt": receipt_path.name,
                    "receipt_sha256": sha256(receipt_path),
                },
                sort_keys=True,
            )
        )
        return 0
    except BuildError as exc:
        print(json.dumps({"status": "FAIL", "message": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
