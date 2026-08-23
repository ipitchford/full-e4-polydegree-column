#!/usr/bin/env python3
"""Independent exact audit of the e=4 normalized coefficient formula."""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import platform
import sys
from fractions import Fraction


HERE = pathlib.Path(__file__).resolve().parent
RECEIPT_PATH = HERE / "e4_normalization_receipt.json"


class NormalizationError(RuntimeError):
    """Raised when the direct and product coefficient formulas disagree."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise NormalizationError(message)


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalization_constant(big_m: int, q: int) -> Fraction:
    n = 4 * big_m + q
    sign = -1 if big_m % 2 else 1
    return Fraction(
        sign * math.factorial(5 * big_m + q),
        (n + 1) * math.factorial(n) * math.factorial(big_m),
    )


def direct_coefficient(
    n: int, m: int, a1: int, a2: int, a3: int
) -> Fraction | None:
    big_m, q = divmod(n, 4)
    weight = a1 + 2 * a2 + 3 * a3
    if (weight - q) % 4:
        return None
    t = (weight - q) // 4
    if t < 0 or t > big_m:
        return None
    a4 = big_m - t
    total = a1 + a2 + a3 + a4
    sign = -1 if total % 2 else 1
    coefficient_g = Fraction(
        sign * math.factorial(n + total),
        (n + 1)
        * math.factorial(n)
        * math.factorial(a1)
        * math.factorial(a2)
        * math.factorial(a3)
        * math.factorial(a4),
    )
    return coefficient_g / normalization_constant(big_m, q) / m ** (a1 + a2 + a3)


def product_coefficient(
    n: int, m: int, a1: int, a2: int, a3: int
) -> Fraction | None:
    big_m, q = divmod(n, 4)
    weight = a1 + 2 * a2 + 3 * a3
    if (weight - q) % 4:
        return None
    t = (weight - q) // 4
    if t < 0 or t > big_m:
        return None
    degree = a1 + a2 + a3
    ell = degree - t
    numerator = -1 if ell % 2 else 1
    for index in range(1, ell + 1):
        numerator *= 5 * big_m + q + index
    for index in range(t):
        numerator *= big_m - index
    denominator = (
        m**degree
        * math.factorial(a1)
        * math.factorial(a2)
        * math.factorial(a3)
    )
    return Fraction(numerator, denominator)


def audit() -> dict[str, object]:
    admissible_count = 0
    rejected_count = 0
    window_count = 0
    for m in range(2, 13):
        for residue in range(4):
            d = 4 * m + residue
            for offset in range(4):
                n = d + offset
                window_count += 1
                for a1 in range(n + 1):
                    for a2 in range(n + 1 - a1):
                        for a3 in range(n + 1 - a1 - a2):
                            direct = direct_coefficient(n, m, a1, a2, a3)
                            product = product_coefficient(n, m, a1, a2, a3)
                            require(
                                (direct is None) == (product is None),
                                f"support mismatch m={m}, r={residue}, n={n}, a={(a1,a2,a3)}",
                            )
                            if direct is None:
                                rejected_count += 1
                            else:
                                admissible_count += 1
                                require(
                                    direct == product,
                                    f"coefficient mismatch m={m}, r={residue}, n={n}, a={(a1,a2,a3)}",
                                )
    require(window_count == 176, "unexpected number of four-row windows")
    require(admissible_count > 0 and rejected_count > 0, "degenerate audit coverage")
    return {
        "schema": "hc4jc2.polydegree-e4-normalization-audit.v1",
        "status": "PASS",
        "range": "m=2,...,12; residues 0,1,2,3; offsets 0,1,2,3",
        "row_count": window_count,
        "admissible_coefficients": admissible_count,
        "rejected_support_triples": rejected_count,
        "arithmetic": "Python Fraction exact rational arithmetic",
        "python": platform.python_version(),
        "script_sha256": sha256(pathlib.Path(__file__).resolve()),
    }


def main() -> None:
    require(not RECEIPT_PATH.exists(), f"refusing to overwrite receipt: {RECEIPT_PATH}")
    receipt = audit()
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"NORMALIZATION PASS: {receipt['admissible_coefficients']} coefficients; "
        f"receipt_sha256={sha256(RECEIPT_PATH)}"
    )


if __name__ == "__main__":
    try:
        main()
    except NormalizationError as error:
        print(f"NORMALIZATION FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
