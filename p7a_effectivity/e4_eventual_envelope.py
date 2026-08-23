#!/usr/bin/env python3
"""Rigorous eventual certificate for the effective e=4 Fourier branch.

The script combines exact rational coefficient bounds with Arb verification of
the only cancellation-sensitive constant, the first-order defect at the exact
Fourier zeros.  It proves the interval-Newton inequalities uniformly for
every m >= 5000 in residues 0, 2, and 3.  Residue 1 is an exact branch.
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import platform
import sys
from fractions import Fraction

import flint
from flint import acb, arb, fmpq


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

flint.ctx.prec = 256
M_THRESHOLD = 5_000
HEAD_CUTOFF = 50
PAIR_TYPES = ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0))
CENTRE_BOUNDS = (Fraction(1, 3), Fraction(71, 100), Fraction(3, 4))
QUARTER_BALL_BOUNDS = (Fraction(7, 12), Fraction(24, 25), Fraction(1))
K1_BALL_CEILING = Fraction(254)
K1_CENTRE_CEILING = Fraction(2)
K2_BALL_CEILING = Fraction(15_374)
K2_CENTRE_CEILING = Fraction(1_105)
TAIL_CEILING = Fraction(1, 400_000)
SOURCE_POLYDISC_RADIUS = Fraction(1, 4)
ROOT_BALL_RADIUS = Fraction(1, 100)
CAUCHY_MARGIN = SOURCE_POLYDISC_RADIUS - ROOT_BALL_RADIUS
JACOBIAN_DEFECT_CEILING = Fraction(15)
LIMIT_HESSIAN_CEILING = Fraction(258)
HESSIAN_DEFECT_CEILING = Fraction(300)
NEXT_GRADIENT_CEILING = Fraction(37)


class CertificationError(RuntimeError):
    """Raised when an advertised bound cannot be proved."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificationError(message)


def exp_ub(x: Fraction, terms: int | None = None) -> Fraction:
    """Exact rational upper bound for exp(x), x >= 0."""
    require(x >= 0, "exp_ub requires a nonnegative argument")
    if terms is None:
        terms = max(40, x.numerator // x.denominator + 2)
    terms = max(terms, x.numerator // x.denominator + 2)
    require(Fraction(terms) > x, "Taylor remainder denominator is not positive")
    total = Fraction(1)
    term = Fraction(1)
    for index in range(1, terms):
        term *= x / index
        total += term
    remainder = term * x / terms * Fraction(terms, terms - x)
    require(remainder >= 0, "Taylor remainder is negative")
    return total + remainder


def head_second_order(bounds: tuple[Fraction, Fraction, Fraction]) -> dict[tuple[int, int], Fraction]:
    """Sum the O(m^-2) product remainder through total degree 50."""
    result: dict[tuple[int, int], Fraction] = {}
    exponential_ceiling = Fraction(6, 5)
    maximum_absolute_sum = Fraction(0)
    for q, wrap in PAIR_TYPES:
        total = Fraction(0)
        for a1 in range(HEAD_CUTOFF + 1):
            for a2 in range(HEAD_CUTOFF + 1 - a1):
                for a3 in range(HEAD_CUTOFF + 1 - a1 - a2):
                    weight = a1 + 2 * a2 + 3 * a3
                    if (weight - q) % 4:
                        continue
                    t = (weight - q) // 4
                    if t < 0:
                        continue
                    degree = a1 + a2 + a3
                    if degree == 0:
                        continue
                    ell = degree - t
                    absolute_sum = (
                        Fraction(q * ell, 5)
                        + Fraction(ell * (ell + 1), 10)
                        + Fraction(t * (t - 1), 2)
                        + wrap * degree
                    )
                    maximum_absolute_sum = max(maximum_absolute_sum, absolute_sum)
                    coefficient_weight = (
                        Fraction(5**ell)
                        * bounds[0] ** a1
                        * bounds[1] ** a2
                        * bounds[2] ** a3
                        / (
                            math.factorial(a1)
                            * math.factorial(a2)
                            * math.factorial(a3)
                        )
                    )
                    # Product remainder plus conversion P/M -> P/m when M=m+1.
                    total += coefficient_weight * (
                        exponential_ceiling * absolute_sum**2 / 2 + absolute_sum
                    )
        result[(q, wrap)] = total
    require(
        exp_ub(maximum_absolute_sum / M_THRESHOLD) <= Fraction(6, 5),
        "configured exponential ceiling is too small",
    )
    return result


def tail_bound() -> Fraction:
    """Uniform C0 tail for finite, limit, and first-order series above degree 50."""
    # For u >= 51 the absolute first-order multiplier is bounded by
    # (61/160)u^2 + (17/10)u <= u^2.  The two summands come respectively
    # from the quadratic and linear parts of the product expansion.
    first_tail_degree = HEAD_CUTOFF + 1
    leading_multiplier_bound = (
        Fraction(61, 160) * first_tail_degree**2
        + Fraction(17, 10) * first_tail_degree
    )
    require(
        leading_multiplier_bound <= first_tail_degree**2,
        "u^2 does not dominate the first-order tail multiplier",
    )
    finite = Fraction(0)
    limit = Fraction(0)
    leading = Fraction(0)
    for degree in range(HEAD_CUTOFF + 1, 401):
        limit_level = Fraction(15**degree, math.factorial(degree))
        limit += limit_level
        leading += Fraction(degree**2, M_THRESHOLD) * limit_level
        finite += limit_level * exp_ub(
            Fraction((degree + 3) ** 2, 2 * M_THRESHOLD)
        )

    ratio = Fraction(1, 20)
    degree = 401
    require(Fraction(15, degree + 1) <= ratio, "limit-tail ratio exceeds 1/20")
    require(
        Fraction(15 * (degree + 1), degree**2) <= ratio,
        "leading-tail ratio exceeds 1/20",
    )
    finite_first_ratio = Fraction(15, degree + 1) * exp_ub(
        Fraction(2 * degree + 7, 2 * M_THRESHOLD)
    )
    require(
        finite_first_ratio <= ratio,
        "finite-tail ratio at the first omitted level exceeds 1/20",
    )
    limit_level = Fraction(15**degree, math.factorial(degree))
    finite_level = limit_level * exp_ub(
        Fraction((degree + 3) ** 2, 2 * M_THRESHOLD)
    )
    leading_level = Fraction(degree**2, M_THRESHOLD) * limit_level
    finite += finite_level / (1 - ratio)
    limit += limit_level / (1 - ratio)
    leading += leading_level / (1 - ratio)

    # Direct high-degree finite terms for every u > M_THRESHOLD, uniformly in
    # m >= M_THRESHOLD.  On the manuscript polydisc,
    # R_X = max_s |X_s| <= 1, so 3 R_X <= 3.  Together with e < 3, the level
    # base is less than 9(5m+8+u)/(mu) = 45/u + 9/m + 72/(mu).
    high_ratio = Fraction(13, 1000)
    first_high_degree = M_THRESHOLD + 1
    high_ratio_actual = (
        Fraction(45, first_high_degree)
        + Fraction(9, M_THRESHOLD)
        + Fraction(72, M_THRESHOLD * first_high_degree)
    )
    require(
        high_ratio_actual <= high_ratio,
        "direct high-degree ratio exceeds 13/1000",
    )
    high_finite = high_ratio ** (M_THRESHOLD + 1) / (1 - high_ratio)
    total = finite + limit + leading + high_finite
    require(total <= TAIL_CEILING, "tail exceeds the configured ceiling")
    return total


def arb_fourier_data() -> dict[str, object]:
    """Verify limit-point coordinates and first-order defect cancellation."""
    imaginary = acb(0, 1)
    pi = arb.pi()
    sqrt_two = arb(2).sqrt()
    rho_abs = arb(5).sqrt().sqrt()
    rho = acb(rho_abs / sqrt_two, rho_abs / sqrt_two)
    log_coefficients = {
        0: (Fraction(1, 4), Fraction(-1, 4), Fraction(-3, 4), Fraction(3, 4)),
        2: (Fraction(1, 4), Fraction(3, 4), Fraction(-3, 4), Fraction(-1, 4)),
        3: (Fraction(-1, 2), Fraction(1, 2), Fraction(-1, 2), Fraction(1, 2)),
    }
    phases = {
        0: acb(1 / sqrt_two, 1 / sqrt_two),
        2: acb(1 / sqrt_two, 1 / sqrt_two),
        3: -imaginary,
    }
    maximum_first_order = arb(0)
    points: dict[str, list[str]] = {}
    first_order_values: dict[str, list[str]] = {}

    for residue in (0, 2, 3):
        logs = [imaginary * pi * fmpq(value.numerator, value.denominator) for value in log_coefficients[residue]]
        point = []
        for coordinate in range(1, 4):
            numerator = sum(
                (logs[index] * imaginary ** (-coordinate * index) for index in range(4)),
                acb(0),
            )
            point.append(numerator / (4 * rho ** (4 - coordinate)))
        require(abs(point[0]) <= arb(fmpq(1, 3)), "X1 limit-point bound failed")
        require(abs(point[1]) <= arb(fmpq(71, 100)), "X2 limit-point bound failed")
        require(abs(point[2]) <= arb(fmpq(3, 4)), "X3 limit-point bound failed")
        points[str(residue)] = [str(value) for value in point]

        row_values = []
        for offset in range(3):
            q = (residue + offset) % 4
            wrap = (residue + offset) // 4
            total = acb(0)
            for index in range(4):
                z = [
                    rho ** (4 - coordinate)
                    * imaginary ** (coordinate * index)
                    * point[coordinate - 1]
                    for coordinate in range(1, 4)
                ]
                p_t = -fmpq(q, 4) + sum(
                    (fmpq(coordinate, 4) * z[coordinate - 1] for coordinate in range(1, 4)),
                    acb(0),
                )
                d_t = sum(
                    (fmpq(coordinate**2, 16) * z[coordinate - 1] for coordinate in range(1, 4)),
                    acb(0),
                )
                p_l = fmpq(q, 4) + sum(
                    (fmpq(4 - coordinate, 4) * z[coordinate - 1] for coordinate in range(1, 4)),
                    acb(0),
                )
                d_l = sum(
                    (fmpq((4 - coordinate) ** 2, 16) * z[coordinate - 1] for coordinate in range(1, 4)),
                    acb(0),
                )
                p_u = sum(z, acb(0))
                multiplier = (
                    fmpq(q, 5) * p_l
                    + (p_l**2 + d_l + p_l) / 10
                    - (p_t**2 + d_t - p_t) / 2
                    + wrap * p_u
                )
                exponential = phases[residue] * imaginary ** (((residue - 1) % 4) * index)
                total += (
                    rho**q
                    * imaginary ** (-q * index)
                    * multiplier
                    * exponential
                    / 4
                )
            row_values.append(str(total))
            require(
                abs(total) <= arb(2),
                f"first-order centre defect exceeds 2 for residue {residue}, offset {offset}",
            )
            if maximum_first_order < abs(total):
                maximum_first_order = abs(total)
        first_order_values[str(residue)] = row_values

    require(maximum_first_order <= arb(2), "first-order centre defect exceeds 2")
    require(1 / rho_abs <= arb(fmpq(67, 100)), "inverse limit Jacobian bound failed")
    require(rho_abs >= arb(fmpq(149, 100)), "next-row base margin failed")
    return {
        "points": points,
        "first_order_values": first_order_values,
        "maximum_first_order": str(maximum_first_order),
        "rho_abs": str(rho_abs),
    }


def first_order_ball_bound() -> Fraction:
    """Rational triangle bound for G on the quarter-polydisc."""
    require(Fraction(5) < Fraction(3, 2) ** 4, "configured |rho| bound failed")
    require(
        exp_ub(Fraction(57, 32)) <= 6,
        "Fourier exponential on the quarter-polydisc exceeds 6",
    )
    z = (
        Fraction(27, 8) * Fraction(7, 12),
        Fraction(9, 4) * Fraction(24, 25),
        Fraction(3, 2),
    )
    maximum = Fraction(0)
    for q, wrap in PAIR_TYPES:
        p_t = Fraction(q, 4) + sum(
            Fraction(coordinate, 4) * z[coordinate - 1]
            for coordinate in range(1, 4)
        )
        d_t = sum(
            Fraction(coordinate**2, 16) * z[coordinate - 1]
            for coordinate in range(1, 4)
        )
        p_l = Fraction(q, 4) + sum(
            Fraction(4 - coordinate, 4) * z[coordinate - 1]
            for coordinate in range(1, 4)
        )
        d_l = sum(
            Fraction((4 - coordinate) ** 2, 16) * z[coordinate - 1]
            for coordinate in range(1, 4)
        )
        p_u = sum(z)
        multiplier = (
            Fraction(q, 5) * p_l
            + (p_l**2 + d_l + p_l) / 10
            + (p_t**2 + d_t + p_t) / 2
            + wrap * p_u
        )
        # |rho|^q < (3/2)^q and exp(sum |rho|^(4-s)/4) < 6.
        bound = Fraction(3, 2) ** q * 6 * multiplier
        maximum = max(maximum, bound)
    require(maximum <= K1_BALL_CEILING, "first-order quarter-ball bound exceeds 254")
    return maximum


def analytic_derivative_bounds(epsilon_ball: Fraction) -> dict[str, Fraction]:
    """Derive every Cauchy and limit-system derivative constant used below."""
    require(CAUCHY_MARGIN == Fraction(6, 25), "unexpected Cauchy margin")
    spectral_sum = Fraction(57, 8)
    limit_exponential = exp_ub(spectral_sum * ROOT_BALL_RADIUS)
    limit_exponential_ceiling = Fraction(11, 10)
    require(
        limit_exponential <= limit_exponential_ceiling,
        "limit exponential exceeds 11/10 on the root ball",
    )

    # Three first derivatives, each bounded by epsilon/R at the centre.
    jacobian_defect = Fraction(3) / SOURCE_POLYDISC_RADIUS
    require(
        jacobian_defect <= JACOBIAN_DEFECT_CEILING,
        "Jacobian Cauchy coefficient exceeds 15",
    )

    # Three pure second derivatives carry the one-variable factor 2; the six
    # ordered mixed derivatives carry factor 1.
    hessian_defect = Fraction(12) / CAUCHY_MARGIN**2
    require(
        hessian_defect <= HESSIAN_DEFECT_CEILING,
        "Hessian Cauchy coefficient exceeds 300",
    )

    # |rho|^q <= (3/2)^3 and sum_s |rho|^(4-s) <= 57/8.
    limit_hessian = (
        Fraction(3, 2) ** 3
        * spectral_sum**2
        * limit_exponential_ceiling
    )
    require(
        limit_hessian <= LIMIT_HESSIAN_CEILING,
        "limit Hessian row sum exceeds 258",
    )
    limit_gradient = (
        Fraction(3, 2) ** 3
        * spectral_sum
        * limit_exponential_ceiling
    )
    defect_gradient = Fraction(3) / CAUCHY_MARGIN * epsilon_ball
    next_gradient = limit_gradient + defect_gradient
    require(
        next_gradient <= NEXT_GRADIENT_CEILING,
        "fourth-row gradient exceeds 37",
    )
    return {
        "spectral_sum": spectral_sum,
        "limit_exponential_actual": limit_exponential,
        "limit_exponential_used": limit_exponential_ceiling,
        "jacobian_defect_coefficient_actual": jacobian_defect,
        "jacobian_defect_coefficient_used": JACOBIAN_DEFECT_CEILING,
        "hessian_defect_coefficient_actual": hessian_defect,
        "hessian_defect_coefficient_used": HESSIAN_DEFECT_CEILING,
        "limit_hessian_actual": limit_hessian,
        "limit_hessian_used": LIMIT_HESSIAN_CEILING,
        "limit_gradient_actual": limit_gradient,
        "defect_gradient_at_threshold": defect_gradient,
        "next_gradient_actual_at_threshold": next_gradient,
        "next_gradient_used": NEXT_GRADIENT_CEILING,
    }


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("ascii")).hexdigest()


def fraction_record(value: Fraction) -> dict[str, str]:
    numerator = str(value.numerator)
    denominator = str(value.denominator)
    record = {"decimal": f"{float(value):.17g}"}
    if len(numerator) + len(denominator) <= 256:
        record["numerator"] = numerator
        record["denominator"] = denominator
    else:
        exact_text = numerator + "/" + denominator
        record["exact_fraction_sha256"] = sha256_text(exact_text)
        record["numerator_digits"] = str(len(numerator))
        record["denominator_digits"] = str(len(denominator))
    return record


def certify() -> dict[str, object]:
    k1_ball = first_order_ball_bound()
    k2_ball_by_pair = head_second_order(QUARTER_BALL_BOUNDS)
    k2_centre_by_pair = head_second_order(CENTRE_BOUNDS)
    k2_ball = max(k2_ball_by_pair.values())
    k2_centre = max(k2_centre_by_pair.values())
    require(k2_ball <= K2_BALL_CEILING, "second-order quarter-ball ceiling failed")
    require(k2_centre <= K2_CENTRE_CEILING, "second-order centre ceiling failed")
    tail = tail_bound()
    fourier = arb_fourier_data()

    m = Fraction(M_THRESHOLD)
    epsilon_ball = K1_BALL_CEILING / m + K2_BALL_CEILING / m**2 + TAIL_CEILING
    residual = K1_CENTRE_CEILING / m + K2_CENTRE_CEILING / m**2 + TAIL_CEILING
    derivative_bounds = analytic_derivative_bounds(epsilon_ball)
    beta_zero = Fraction(67, 100)
    derivative_error = JACOBIAN_DEFECT_CEILING * epsilon_ball
    neumann = beta_zero * derivative_error
    require(neumann < 1, "eventual Jacobian Neumann condition failed")
    beta = beta_zero / (1 - neumann)
    lipschitz = LIMIT_HESSIAN_CEILING + HESSIAN_DEFECT_CEILING * epsilon_ball
    eta = beta * residual
    h = beta * lipschitz * eta
    root_radius = 2 * eta
    next_margin = (
        Fraction(149, 100)
        - NEXT_GRADIENT_CEILING * root_radius
        - epsilon_ball
    )
    jacobian_margin = 1 - beta * lipschitz * root_radius
    require(h < Fraction(1, 2), "eventual Kantorovich h condition failed")
    require(root_radius < Fraction(1, 100), "eventual root radius exceeds 1/100")
    require(next_margin > 0, "eventual fourth-row margin failed")
    require(jacobian_margin > 0, "eventual Jacobian transport margin failed")

    return {
        "schema": "hc4jc2.polydegree-e4-eventual.v1",
        "status": "CERTIFIED",
        "m_threshold": M_THRESHOLD,
        "degree_coverage": "all d=4m+r with m>=5000 and r in {0,2,3}; r=1 is exact",
        "arithmetic": "Fraction exact rational bounds plus 256-bit FLINT/Arb Fourier evaluation",
        "constants": {
            "K1_ball_actual": fraction_record(k1_ball),
            "K1_ball_used": fraction_record(K1_BALL_CEILING),
            "K1_centre_used": fraction_record(K1_CENTRE_CEILING),
            "K2_ball_actual": fraction_record(k2_ball),
            "K2_ball_used": fraction_record(K2_BALL_CEILING),
            "K2_centre_actual": fraction_record(k2_centre),
            "K2_centre_used": fraction_record(K2_CENTRE_CEILING),
            "tail_actual": fraction_record(tail),
            "tail_used": fraction_record(TAIL_CEILING),
        },
        "endpoint_predicates": {
            "epsilon_ball": fraction_record(epsilon_ball),
            "residual": fraction_record(residual),
            "neumann_product": fraction_record(neumann),
            "beta": fraction_record(beta),
            "lipschitz": fraction_record(lipschitz),
            "h": fraction_record(h),
            "root_radius": fraction_record(root_radius),
            "next_margin": fraction_record(next_margin),
            "jacobian_margin": fraction_record(jacobian_margin),
        },
        "fourier_arb": fourier,
        "analytic_derivative_bounds": {
            name: fraction_record(value) for name, value in derivative_bounds.items()
        },
        "monotonicity": (
            "For m>=5000 the 1/m and 1/m^2 head terms decrease; the finite and "
            "leading tails were evaluated at m=5000 and the limit tail is constant. "
            "All acceptance expressions worsen monotonically with the two defect envelopes."
        ),
    }


def main() -> None:
    receipt_path = pathlib.Path(__file__).with_name("e4_eventual_receipt.json")
    receipt = certify()
    receipt["environment"] = {
        "python": platform.python_version(),
        "python_flint": flint.__version__,
        "precision_bits": flint.ctx.prec,
    }
    receipt["script_sha256"] = sha256(pathlib.Path(__file__))
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "CERTIFIED: m >= 5000; "
        f"h={receipt['endpoint_predicates']['h']['decimal']}; "
        f"root_radius={receipt['endpoint_predicates']['root_radius']['decimal']}"
    )
    print(f"receipt: {receipt_path.name} sha256={sha256(receipt_path)}")


if __name__ == "__main__":
    try:
        main()
    except CertificationError as error:
        print(f"CERTIFICATION FAILED: {error}", file=sys.stderr)
        raise SystemExit(1)
