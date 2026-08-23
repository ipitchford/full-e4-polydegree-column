#!/usr/bin/env python3
"""Prototype full-polynomial Arb certificates for the e=4 Polydegree rows.

This first-stage checker deliberately handles only small m, where the exact
finite polynomials fit below the selected cutoff.  It establishes the formula
and interval-Newton pipeline before analytic truncation tails are added.
"""

from __future__ import annotations

import math
import json
import pathlib
import sys
from functools import lru_cache
from fractions import Fraction

import flint
from flint import acb, acb_mat, acb_poly, arb, fmpq


flint.ctx.prec = 128
DOMAIN_BOUND = Fraction(4, 5)
ROOT_RADIUS_LIMIT = Fraction(1, 100)

# Exact decimal rationals used only as proposed centres.  Certification does
# not assume that they are exact limit points or exact asymptotic corrections.
CENTRES: dict[int, tuple[tuple[str, str], ...]] = {
    0: (
        (("0.33218297933418345", "0"), ("-0.16605473600852738", "0")),
        (("-0.35124073655203636", "0"), ("0.32357662908741813", "0")),
        (("0.7427837227596419", "0"), ("-0.43507077814192907", "0")),
    ),
    2: (
        (("0", "-0.33218297933418345"), ("0", "0.14951909435894695")),
        (("-0.35124073655203636", "0"), ("0.16816040208543284", "0")),
        (("0", "0.7427837227596419"), ("0", "-0.8648007366874441")),
    ),
    3: (
        (("0", "0"), ("0", "0")),
        (("-0.7024814731040727", "0"), ("0.8429777677248873", "0")),
        (("0", "0"), ("0", "0")),
    ),
}
LOCATOR_PATH = pathlib.Path(__file__).with_name("small_locators_5_12.jsonl")


class CertificationError(RuntimeError):
    """Raised when a proof predicate cannot be established."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificationError(message)


def to_fraction(decimal: str) -> Fraction:
    return Fraction(decimal)


def to_fmpq(value: Fraction) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def exact_complex(real: Fraction, imag: Fraction) -> acb:
    return acb(to_fmpq(real), to_fmpq(imag))


def asymptotic_centre(m: int, residue: int) -> tuple[acb, acb, acb]:
    require(residue in CENTRES, f"no nonexact centre for residue {residue}")
    result = []
    for (x_real, x_imag), (y_real, y_imag) in CENTRES[residue]:
        real = to_fraction(x_real) + to_fraction(y_real) / m
        imag = to_fraction(x_imag) + to_fraction(y_imag) / m
        result.append(exact_complex(real, imag))
    return result[0], result[1], result[2]


def load_small_locators() -> dict[tuple[int, int], tuple[acb, acb, acb]]:
    locators: dict[tuple[int, int], tuple[acb, acb, acb]] = {}
    for line in LOCATOR_PATH.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        coordinates = row["X"]
        point = tuple(
            exact_complex(Fraction(coordinates[2 * index]), Fraction(coordinates[2 * index + 1]))
            for index in range(3)
        )
        locators[(row["m"], row["r"])] = point
    return locators


SMALL_LOCATORS = load_small_locators()


@lru_cache(maxsize=64)
def coefficient_table(
    n: int, m: int, cutoff: int
) -> tuple[tuple[int, int, int, fmpq], ...]:
    """Exact coefficients of P_n = g_{n,4}(X/m,1) / C_{M,q}."""
    big_m, residue = divmod(n, 4)
    table: list[tuple[int, int, int, fmpq]] = []
    for a1 in range(cutoff + 1):
        for a2 in range(cutoff + 1 - a1):
            for a3 in range(cutoff + 1 - a1 - a2):
                weight = a1 + 2 * a2 + 3 * a3
                if (weight - residue) % 4:
                    continue
                t = (weight - residue) // 4
                if t < 0 or t > big_m:
                    continue
                degree = a1 + a2 + a3
                ell = degree - t
                numerator = 1
                for index in range(1, ell + 1):
                    numerator *= 5 * big_m + residue + index
                for index in range(t):
                    numerator *= big_m - index
                if ell % 2:
                    numerator = -numerator
                denominator = (
                    m**degree
                    * math.factorial(a1)
                    * math.factorial(a2)
                    * math.factorial(a3)
                )
                table.append((a1, a2, a3, fmpq(numerator, denominator)))
    return tuple(table)


def evaluate(
    table: tuple[tuple[int, int, int, fmpq], ...],
    x1: acb,
    x2: acb,
    x3: acb,
    cutoff: int,
) -> tuple[acb, acb, acb, acb, acb, acb, acb, acb, acb, acb]:
    """Evaluate a trivariate polynomial through all second derivatives."""
    by_a3: list[list[list[acb]]] = [
        [
            [acb(0) for _ in range(cutoff - a3 - a2 + 1)]
            for a2 in range(cutoff - a3 + 1)
        ]
        for a3 in range(cutoff + 1)
    ]
    for a1, a2, a3, coefficient in table:
        by_a3[a3][a2][a1] = acb(coefficient)

    values_x3: list[acb] = []
    dx1_x3: list[acb] = []
    dx2_x3: list[acb] = []
    dx11_x3: list[acb] = []
    dx12_x3: list[acb] = []
    dx22_x3: list[acb] = []
    for a3_rows in by_a3:
        values_x2: list[acb] = []
        dx1_x2: list[acb] = []
        dx11_x2: list[acb] = []
        for coefficients in a3_rows:
            polynomial = acb_poly(coefficients)
            values_x2.append(polynomial(x1))
            dx1_x2.append(polynomial.derivative()(x1))
            dx11_x2.append(polynomial.derivative().derivative()(x1))
        outer_x2 = acb_poly(values_x2)
        outer_dx1_x2 = acb_poly(dx1_x2)
        values_x3.append(outer_x2(x2))
        dx1_x3.append(outer_dx1_x2(x2))
        dx2_x3.append(outer_x2.derivative()(x2))
        dx11_x3.append(acb_poly(dx11_x2)(x2))
        dx12_x3.append(outer_dx1_x2.derivative()(x2))
        dx22_x3.append(outer_x2.derivative().derivative()(x2))

    outer_x3 = acb_poly(values_x3)
    outer_dx1_x3 = acb_poly(dx1_x3)
    outer_dx2_x3 = acb_poly(dx2_x3)
    return (
        outer_x3(x3),
        outer_dx1_x3(x3),
        outer_dx2_x3(x3),
        outer_x3.derivative()(x3),
        acb_poly(dx11_x3)(x3),
        acb_poly(dx12_x3)(x3),
        outer_dx1_x3.derivative()(x3),
        acb_poly(dx22_x3)(x3),
        outer_dx2_x3.derivative()(x3),
        outer_x3.derivative().derivative()(x3),
    )


def coefficient_moments(
    table: tuple[tuple[int, int, int, fmpq], ...], radius: arb
) -> tuple[arb, arb]:
    gradient = arb(0)
    hessian = arb(0)
    for a1, a2, a3, coefficient in table:
        degree = a1 + a2 + a3
        magnitude = abs(arb(coefficient))
        if degree:
            gradient += magnitude * degree * radius ** (degree - 1)
        if degree >= 2:
            hessian += magnitude * degree * (degree - 1) * radius ** (degree - 2)
    return gradient, hessian


def finite_tail_bounds(m: int, cutoff: int, maximum_degree: int) -> tuple[arb, arb, arb]:
    """Bound every omitted finite coefficient moment by one geometric tail."""
    if cutoff >= maximum_degree:
        return arb(0), arb(0), arb(0)
    first_degree = cutoff + 1
    radius = arb(to_fmpq(DOMAIN_BOUND))
    exp_half = arb(to_fmpq(Fraction(1, 2))).exp()
    coefficient_base = 5 * m + 8 + first_degree
    tails = []
    for moment in range(3):
        first = (
            arb(coefficient_base) ** first_degree
            * (3 * radius) ** first_degree
            * first_degree**moment
            / (arb(m) ** first_degree * math.factorial(first_degree) * radius**moment)
        )
        ratio = (
            3
            * radius
            * (5 * m + 9 + first_degree)
            * exp_half
            / (m * (first_degree + 1))
            * arb(to_fmpq(Fraction(first_degree + 1, first_degree))) ** moment
        )
        require(ratio < 1, f"finite-tail ratio is not contractive: {ratio}")
        tail = first / (1 - ratio)
        require(tail.is_finite() and tail >= 0, "finite tail is not a nonnegative finite ball")
        tails.append(tail)
    return tails[0], tails[1], tails[2]


def inverse_row_sum(jacobian: acb_mat) -> arb:
    determinant = jacobian.det()
    require(not determinant.contains(0), "centre Jacobian determinant contains zero")
    inverse = jacobian.inv()
    row_sums = [
        sum((abs(inverse[row, column]) for column in range(3)), arb(0))
        for row in range(3)
    ]
    bound = row_sums[0]
    for candidate in row_sums[1:]:
        if bound < candidate:
            bound = candidate
        elif not candidate <= bound:
            bound += candidate
    require(bound.is_finite(), "inverse row-sum bound is not finite")
    return bound


def max_ball(values: list[arb]) -> arb:
    require(values, "cannot bound an empty list")
    bound = values[0]
    for candidate in values[1:]:
        if bound < candidate:
            bound = candidate
        elif not candidate <= bound:
            bound += candidate
    return bound


def local_box(centre: tuple[acb, acb, acb], radius: Fraction) -> tuple[acb, acb, acb]:
    result = []
    radius_q = to_fmpq(radius)
    for coordinate in centre:
        real = coordinate.real + arb(0, radius_q)
        imag = coordinate.imag + arb(0, radius_q)
        result.append(acb(real, imag))
    return result[0], result[1], result[2]


def gradient_row_bound(value: tuple[acb, ...]) -> arb:
    return abs(value[1]) + abs(value[2]) + abs(value[3])


def hessian_row_bound(value: tuple[acb, ...]) -> arb:
    return (
        abs(value[4])
        + 2 * abs(value[5])
        + 2 * abs(value[6])
        + abs(value[7])
        + 2 * abs(value[8])
        + abs(value[9])
    )


def certify_case(m: int, residue: int) -> dict[str, object]:
    require(m >= 5, "prototype starts at m=5")
    require(residue in (0, 2, 3), "residue 1 is the separate exact branch")
    d = 4 * m + residue
    maximum_degree = d + 3
    cutoff = maximum_degree if m <= 30 else 50
    locator_key = (m, residue)
    centre = SMALL_LOCATORS.get(locator_key, asymptotic_centre(m, residue))
    root_limit = arb(to_fmpq(ROOT_RADIUS_LIMIT))
    domain = arb(to_fmpq(DOMAIN_BOUND))
    # An acb rectangular box permits independent real and imaginary
    # displacements of ROOT_RADIUS_LIMIT, hence a complex displacement of at
    # most sqrt(2) times that radius.
    rectangular_displacement = arb(2).sqrt() * root_limit
    for coordinate in centre:
        require(
            abs(coordinate) + rectangular_displacement < domain,
            "locator rectangle exits proof domain",
        )

    tables = [coefficient_table(d + offset, m, cutoff) for offset in range(4)]
    values = [evaluate(table, *centre, cutoff) for table in tables]
    box = local_box(centre, ROOT_RADIUS_LIMIT)
    box_values = [evaluate(table, *box, cutoff) for table in tables]
    tail0, tail1, tail2 = finite_tail_bounds(m, cutoff, maximum_degree)
    jacobian = acb_mat([[values[row][column + 1] for column in range(3)] for row in range(3)])
    beta_truncated = inverse_row_sum(jacobian)
    derivative_perturbation = beta_truncated * tail1
    require(
        derivative_perturbation.upper() < 1,
        "Jacobian tail defeats Neumann inversion",
    )
    beta = beta_truncated / (1 - derivative_perturbation)
    residual = max_ball([abs(values[row][0]) for row in range(3)]) + tail0
    lipschitz = max_ball([hessian_row_bound(box_values[row]) for row in range(3)]) + tail2
    eta = beta * residual
    h = beta * lipschitz * eta
    root_radius = 2 * eta
    next_gradient = gradient_row_bound(box_values[3]) + tail1
    next_margin = abs(values[3][0]) - tail0 - next_gradient * root_radius
    jacobian_margin = 1 - beta * lipschitz * root_radius

    checks = {
        "h_lt_half": h.upper() < arb(to_fmpq(Fraction(1, 2))),
        "root_in_domain": root_radius.upper() < root_limit,
        "next_row_nonzero": next_margin.lower() > 0,
        "jacobian_nonzero": jacobian_margin.lower() > 0,
    }
    return {
        "m": m,
        "r": residue,
        "d": d,
        "cutoff": cutoff,
        "maximum_degree": maximum_degree,
        "locator": "stored_decimal" if locator_key in SMALL_LOCATORS else "asymptotic_formula",
        "coefficient_counts": [len(table) for table in tables],
        "ok": all(checks.values()),
        "checks": checks,
        "h": str(h),
        "root_radius": str(root_radius),
        "tail0": str(tail0),
        "tail1": str(tail1),
        "tail2": str(tail2),
        "next_margin": str(next_margin),
        "jacobian_margin": str(jacobian_margin),
        "certified_endpoints": {
            "h_upper": h.upper().str(more=True),
            "root_radius_upper": root_radius.upper().str(more=True),
            "tail0_upper": tail0.upper().str(more=True),
            "tail1_upper": tail1.upper().str(more=True),
            "tail2_upper": tail2.upper().str(more=True),
            "next_margin_lower": next_margin.lower().str(more=True),
            "jacobian_margin_lower": jacobian_margin.lower().str(more=True),
        },
    }


def main() -> None:
    failures = []
    for m in range(5, 13):
        for residue in (0, 2, 3):
            result = certify_case(m, residue)
            print(result)
            if not result["ok"]:
                failures.append(result)
    require(not failures, f"{len(failures)} prototype cases failed")
    print("PROTOTYPE PASS: 24 full-polynomial Arb certificates")


if __name__ == "__main__":
    try:
        main()
    except CertificationError as error:
        print(f"CERTIFICATION FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
