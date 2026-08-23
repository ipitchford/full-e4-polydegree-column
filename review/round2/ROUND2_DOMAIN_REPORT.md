# Round 2 Domain Mathematics report

**Submission manifest:** `867bff8d9b092a133194cf57a53d06dc3824d8aeb47508c5e5eec614bb8fc4a7`  
**Role:** Polydegree, resultants and two-dimensional Keller geometry  
**Independence:** fresh read-only proof review; no other Round 2 report consulted  
**Decision:** **ACCEPT**  
**Issue inventory:** Critical 0; Major 0; Minor 0; Observations 4

## Full `e=4` Polydegree column

The source distinction is correct: Lewis--Perry--Straub Theorem 4 is the
specialization-to-containment implication and Theorem 13(b) establishes it
for `2<=d<20`; Perry's degree-45 statement is only a weaker stratum
intersection.  The new theorem therefore addresses the correct missing range.

The weighted Euler identity in Proposition 2.1 has the right determinant
signs.  On the first-three-row zero set at `e=4,x_4=1`, a nonzero anchored
minor and fourth row force the full determinant polynomial and required next
coefficient to be nonzero.  The exact row normalization and unscaling use only
nonzero factors.

The coefficient product formula, support congruence and wrap `M=m` or `m+1`
are consistent.  Root-of-unity filtering gives the four Fourier rows, the
chosen phases annihilate the required three, and the derivative shift makes
the limit Jacobian invertible with a nonzero fourth row.  The finite and
eventual perturbation arguments supply actual nearby simple zeros, not only
small residuals.  The residue-one origin calculation is exact.  The proof on
p. 12 consequently exhausts every `d>=2`.

The revised high-degree paragraph defines its common coordinate majorant
`R_X` directly from the Section 5 polydisc.  Its factorial-base estimate is
now self-contained and uses notation distinct from both the coefficient ratio
and the later finite radius.  I find no remaining gap at the analytic handoff.

## Universal bordered-Jacobian theorem

The signed cofactor relation over a commutative ring is correctly
cross-multiplied, so it avoids an unjustified rank-one kernel argument.  The
anchored minor matches the Sylvester resultant convention `Res(B,A)`.  The
only coefficient cancellation is performed in the universal polynomial
integral domain; all determinants, resultants and coefficients are then mapped
to an arbitrary commutative ring.  Laplace expansion yields the stated border
sign.  The Lean theorems cover all degrees including zero and a ring with zero
divisors.

## Boundary-norm transfer

For Lemma 2.1, nonconstant polynomial `s(t)` makes `t` integral over `k[s]`;
the norm of polynomial `h(t)` therefore lies in the integrally closed PID
`k[s]`.  Monicity gives the field degree and `N(ell)=(-1)^nF(s,0)`.
The tower norm forces `F(s,0)^e` to divide `s^(kappa en)`, yielding the
monomial and exponent bound with cancellation of `e`.

The finite-pencil lemma follows from homogeneous linear factorization over
`C` and unique factorization in `C[s]`.  In the transfer theorem, the total
factor degree `m+1` gives the upper exponent `kappa(m+1)`, while the top form
contributes `s^(kappa m)`; the remaining exponent lies in the forbidden finite
range.  The six-sheet pencil calculation is correct, and the article does not
omit its dependency on the companion geometric package.  `A=1,B=s` proves
sharpness only for this method, exactly as claimed.

## Novelty and conjecture boundary

The documented search supports specialist submission but not an unconditional
priority superlative.  Broad Orevkov/Borisov geometry is not reclaimed as new.
No theorem is converted into a JC2 or HC4 conclusion.

## Issues

No Critical, Major, or Minor issues are identified.

## Observations (non-blocking, not defects)

1. The P7a analytic estimates deserve independent expert reconstruction
   because they carry the new infinite range.
2. The bordered identity may be useful as general formal resultant
   infrastructure independently of this corpus.
3. The boundary theorem's future reach depends on finding further seeds with
   a provable `BN` package; the finite pencil test itself is cheap.
4. Keep all three contributions separated in external claims and submissions.

## Final recommendation

Accept the exact manifested mathematical candidate.
