# Effective Fourier certificates for the full e=4 Polydegree column

**Version:** 0.1.0-candidate. **Status:** anonymous unrefereed candidate.

**DOI:** [10.5281/zenodo.22072044](https://doi.org/10.5281/zenodo.22072044)

**Repository:** <https://github.com/ipitchford/full-e4-polydegree-column>

This repository releases three separable mathematical candidate papers and
their replayable evidence:

1. **Full e=4 Polydegree column.** For every integer \(d\ge2\),
   \[
   \mathcal G_{(d+4)}\subseteq\overline{\mathcal G_{(d,5)}}.
   \]
   The proof combines the published range \(2\le d<20\), an exact residue
   class, 14,985 FLINT/Arb finite certificates, and a uniform analytic branch
   for \(m\ge5000\).
2. **Universal bordered-Jacobian identity.** Lean 4.32.1 checks the signed
   maximal-minor and bordered-determinant identities over every commutative
   ring, including zero divisors and the degree-zero boundary.
3. **Finite-pencil boundary-norm transfer.** A short companion proves a
   cover-degree-free norm lemma, finite-pencil equivalence, conditional
   transfer theorem, six-sheet application, and a sharp limitation of the
   method.

These results do **not** solve Furter's R(3), prove monotone
\(R(3,n)\Rightarrow R(3,n+1)\) rigidity, solve the two-dimensional Jacobian
conjecture, or solve the quartic Hessian conjecture in dimension four.

## Start here

- Main paper: [papers/01-full-e4-polydegree-column.pdf](papers/01-full-e4-polydegree-column.pdf)
- Lean companion: [papers/02-universal-bordered-jacobian-formalization.pdf](papers/02-universal-bordered-jacobian-formalization.pdf)
- Boundary companion: [papers/03-boundary-norm-finite-pencil.pdf](papers/03-boundary-norm-finite-pencil.pdf)
- Exact status and limitations: [STATUS.md](STATUS.md) and [ASSURANCE.md](ASSURANCE.md)
- Machine-readable claims: [CLAIMS.json](CLAIMS.json)
- Replay: [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md)
- Internal reviews: [review/round2/ROUND2_ACCEPTANCE_SYNTHESIS.md](review/round2/ROUND2_ACCEPTANCE_SYNTHESIS.md)

## Fast replay

Create an environment with the versions in `requirements.txt`, then run:

```sh
python3 verification/verify_public_release.py
python3 p7a_effectivity/verify_release.py
python3 -O p7a_effectivity/verify_release.py
python3 theorems/verify_boundary_norm_release.py
python3 -O theorems/verify_boundary_norm_release.py
python3 verification/negative_controls.py

cd formal/BorderedJacobianUniversal
lake update
python3 verify_release.py
```

The public repository and its eventual DOI establish availability and byte
identity. They do not by themselves establish theorem truth, priority,
independent reproduction, specialist review, or journal peer review.
