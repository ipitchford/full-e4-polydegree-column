#!/usr/bin/env python3
"""Exact certificate for the finite pencil test in Theorem 4.1.

This checks the Kistner--Shaska residual pair over Q(sqrt(-15)).  It uses
explicit failure returns rather than assertions so `python -O` preserves all
checks.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def fail(message: str, details: object | None = None) -> int:
    payload = {"status": "FAIL", "message": message}
    if details is not None:
        payload["details"] = details
    print(json.dumps(payload, sort_keys=True))
    return 1


def main() -> int:
    s = sp.Symbol("s")
    delta = sp.sqrt(-15)
    alpha = (-3 + delta) / 2
    beta = 1 - alpha

    relation = sp.simplify(alpha**2 + 3 * alpha + 6)
    if relation != 0:
        return fail("quadratic field relation did not reduce to zero", str(relation))

    A = sp.Poly(alpha + beta * s, s, extension=delta)
    B = sp.Poly(
        s
        * (
            sp.Rational(8, 3) * alpha**2
            + sp.Rational(9, 2) * alpha * beta * s
            + sp.Rational(9, 5) * beta**2 * s**2
        ),
        s,
        extension=delta,
    )

    gcd = sp.gcd(A, B)
    if gcd.degree() != 0:
        return fail("residual polynomials are not coprime", str(gcd.as_expr()))

    resultant = sp.simplify(sp.resultant(A.as_expr(), B.as_expr(), s))
    expected_resultant = sp.simplify(2 * alpha)
    if sp.simplify(resultant - expected_resultant) != 0:
        return fail(
            "residual resultant does not equal 2*alpha",
            {"actual": str(resultant), "expected": str(expected_resultant)},
        )

    coefficient_vectors = []
    for degree in range(4):
        coefficient_vectors.append(
            [A.nth(degree), B.nth(degree)]
        )

    pencil_rows = []
    for target_degree in range(3):
        constraints = sp.Matrix(
            [
                coefficient_vectors[degree]
                for degree in range(4)
                if degree != target_degree
            ]
        )
        rank = constraints.rank()
        nullity = 2 - rank
        row = {
            "target_degree": target_degree,
            "constraint_rank": rank,
            "solution_nullity": nullity,
        }
        pencil_rows.append(row)
        if nullity != 0:
            return fail("a forbidden low monomial occurs in the pencil", row)

    # Negative controls: span(1,s) must contain both degree-zero and
    # degree-one monomials, so the corresponding constraint nullities are 1.
    A_bad = sp.Poly(1, s, domain=sp.QQ)
    B_bad = sp.Poly(s, s, domain=sp.QQ)
    bad_vectors = [[A_bad.nth(d), B_bad.nth(d)] for d in range(2)]
    negative_control = []
    for target_degree in range(2):
        constraints = sp.Matrix(
            [bad_vectors[d] for d in range(2) if d != target_degree]
        )
        nullity = 2 - constraints.rank()
        negative_control.append(
            {"target_degree": target_degree, "solution_nullity": nullity}
        )
        if nullity != 1:
            return fail("negative control did not expose a monomial", negative_control)

    payload = {
        "status": "PASS",
        "field": "Q(sqrt(-15))",
        "alpha_relation": "alpha^2 + 3*alpha + 6 = 0",
        "kappa": 2,
        "gcd_degree": gcd.degree(),
        "resultant": "2*alpha",
        "pencil_tests": pencil_rows,
        "negative_control": negative_control,
        "sympy_version": sp.__version__,
        "optimized_python_safe": True,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
