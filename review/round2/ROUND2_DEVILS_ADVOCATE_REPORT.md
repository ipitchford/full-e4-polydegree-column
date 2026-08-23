# Round 2 Devil's Advocate report

**Submission manifest:** `867bff8d9b092a133194cf57a53d06dc3824d8aeb47508c5e5eec614bb8fc4a7`  
**Role:** adversarial algebraic geometry and computer-assisted proof  
**Independence:** fresh read-only attack; no other Round 2 report consulted  
**Decision:** **ACCEPT**  
**Issue inventory:** Critical 0; Major 0; Minor 0; Observations 5

## Strongest counterargument

The best case against release is that P7a could be an impressive but
non-binding computation: an unproved normalization might feed the wrong rows;
the ledger might miss degrees; the eventual estimate might omit the very high
finite coefficients; or a smooth zero of normalized rows might fail to imply
the published determinant condition.  P7b could hide an illegal cancellation
when specialized to zero divisors.  The boundary theorem could smuggle in the
conclusion through an overstrong “boundary package” or misuse norms when the
boundary curve is not rational.  Finally, a negative literature search could
be misrepresented as priority.

I attacked each route.

## P7a adversarial audit

1. **Wrong polynomial or sign.**  The normalized coefficient formula is
   derived from the multinomial definition with the exact support congruence,
   and a separate exact audit reconstructs admitted and rejected terms.  Row
   and coordinate scalings are nonzero.  Weighted Euler expansion gives the
   correct sign and shows that the anchored minor plus fourth row controls the
   determinant required by Lewis--Perry--Straub.
2. **Coverage hole.**  The ranges are exhaustive: `2<=d<20` published;
   `d>=20` has `m>=5`; residue one is exact; the other residues are certified
   for `5<=m<5000` and proved analytically for `m>=5000`.  The finite auditor
   enforces all 14,985 ordered pairs and rejects trailing or missing rows.
3. **Locator masquerading as proof.**  Locators are only centres.  Acceptance
   uses outward interval residual, inverse, Hessian, root-radius, fourth-row
   and transported-Jacobian inequalities.  The worst margins are positive.
4. **Eventual tail hole.**  The repaired direct high-degree estimate is now
   complete.  On (5.1), `R_X=max_s|X_s|<=1`.  The coefficient/multinomial
   level and `u!>=(u/e)^u` give base
   `e(3R_X)(5m+8+u)/(mu)`, strictly below
   `9(5m+8+u)/(mu)`.  For `m>=5000,u>m`, the explicit expression
   `45/u+9/m+72/(mu)` is maximized at `(5000,5001)` and is below
   `13/1000`; summing from degree 5001 therefore safely overbounds every
   direct high-degree tail.  The `u<=m` majorant may be extended as a positive
   infinite geometric sum solely to overbound its valid truncated range, and
   the `u>m` contribution is then added separately—there is no omitted band.
5. **Threshold-only numerics.**  The analytic expressions are monotone in the
   required direction after replacing `m` by its minimum.  Exact rational
   gates, not displayed floats, decide the endpoint.  Normal and optimized
   replays are identical, while the paper does not call them independent.

I find no counterexample or unclosed bridge in P7a.

## P7b adversarial audit

The usual kernel-proportionality proof would fail over a general ring, but the
formal proof uses the cross-multiplied identity instead.  Cancellation of
`a_r` occurs only in the universal `Z`-polynomial domain where that variable
is nonzero; the whole polynomial identity is then mapped to the target ring.
The anchored resultant convention and border signs are kernel-checked for all
degrees, including `r=s=0`, and a non-domain `ZMod 6` instance passes.  No
forbidden placeholder or unexpected axiom is present.  The formal trust claim
is relative to the pinned kernel/Mathlib, exactly as it must be.

## Boundary theorem adversarial audit

The norm lemma does not assume the boundary curve itself is an affine line.
It assumes a finite affine-line cover on which `s,ell,h` are polynomials.
This makes `h` integral over `k[s]`; the tower norm exponent contains the same
cover degree in numerator and denominator, so its cancellation is legitimate.
The finite-pencil equivalence is a UFD consequence of factorization of a
homogeneous binary form.  The transfer theorem is conditional on explicit
saturation, factor, residue and domination obligations and therefore is not
circular: it proves what follows after those geometric facts are established.
The six-sheet application includes the entire companion chain and states that
the three-system pencil computation alone is insufficient.  The failure
example is limited to the method and is not advertised as a Keller map.

## Priority and overclaim attack

The audit is bounded and cannot rule out unpublished or unindexed work.  The
package explicitly says so and prohibits “first” and “world-leading” as public
claims.  It distinguishes Orevkov/Borisov geometry and the current unrefereed
Kistner--Shaska source.  No JC2 or HC4 implication is stated.

## Issues

No Critical, Major, or Minor issues are identified.  In particular, the
Round-entry radius defect is resolved mathematically and transitively in the
new receipts, not merely cosmetically.

## Observations (non-blocking, not defects)

1. Same-library replay leaves FLINT/Arb implementation trust; the manuscript
   discloses this.
2. The published Lewis--Perry--Straub implication is not re-formalized; it is
   accurately identified as an external theorem input.
3. The densest risk remains human review of the P7a tail and first-order
   operator, so external refereeing is indispensable.
4. The boundary result is only as portable as future proofs of `BN`; its
   significance is not overstated.
5. Priority remains provisional until specialists search and cite the result.

## Final recommendation

Accept.  I cannot sustain a Critical, Major or Minor objection to the exact
Round 2 bytes.  This is an internal acceptance recommendation, not external
peer review.
