# Round 1 Devil's Advocate report

**Submission manifest:** `299a0326b8dd7d30d2dae9619745f57c7452608814e0fe615e22d5540388cfa2`  
**Role:** adversarial algebraic-geometry and computer-assisted-proof reviewer  
**Independence:** read-only review of submission; no other role report consulted  
**Decision:** **MINOR REVISION / HOLD_FOR_REPAIR**  
**Issue inventory:** Critical 0; Major 0; Minor 1; Observations 4

## Strongest case against acceptance

The strongest global objection is that the P7a theorem rests on several
bridges of different kinds: a published specialization theorem, a normalized
coefficient identity, a limiting Fourier zero, a finite interval ledger, and
an analytic eventual tail.  A successful same-source replay cannot repair an
incorrect bridge.  I therefore tried to break the coverage endpoints, signs,
tail decomposition, domain assumptions and claim boundary rather than merely
checking receipts.

The residue and endpoint partition is complete.  The weighted-Euler sign in
Proposition 2.1 is consistent.  The exact `r=1` branch supplies three zero rows,
an invertible diagonal derivative and a nonzero wrapped fourth row.  The finite
ledger contains every `(m,r)` in the advertised range, and the eventual proof
starts at the next integer.  The universal-ring cancellation in P7b occurs
only in an integral domain and is followed by explicit specialization.  The
boundary norm proof cancels the affine-line cover degree legitimately, and
the conditional geometry is not promoted to a universal Keller-map theorem.

One written-proof defect remains.

## Minor issue DA-1: undefined radius in the direct high-degree tail

**Location:** P7a manuscript, Section 5.2, p. 8, paragraph beginning “For
`u>m`”; corresponding comment in `e4_eventual_envelope.py` near the direct
high-degree bound.

The paper says that the direct finite level is below `(13/1000)^u` “using
`e<3` and `3R<=3`,” but Section 5 has not defined `R`.  Section 6 later defines
`R=4/5` for a different finite-certificate tail, so a reader cannot safely
infer which radius is meant.  The executable then jumps directly to

`45/u + 9/m + 72/(mu)`.

This does not appear theorem-breaking: on the Section 5 polydisc the coordinate
moduli in (5.2) are all at most one, so defining
`R_X=max_s |X_s| <= 1` gives `3R_X<=3` and recovers the displayed base.  The
checker already tests the explicit rational endpoint at `m=5000,u=5001`.
Nevertheless, the current article leaves a symbol undefined in a proof-critical
tail argument and therefore is not yet presentation-ready.

**Required repair:** define `R_X` at this point (or expand the inequality
without a new symbol), explain that it is the common coordinate-radius
majorant from (5.2), and update the source comment.  Rebuild the paper and
regenerate every receipt and manifest transitively bound to the changed bytes.

## Adversarial observations that did not become issues

1. The normalization audit samples `m=2,...,12`, but the manuscript derives
   the coefficient formula algebraically for general `m`; the audit is a
   regression check, not the sole proof.
2. The normal/optimized ledgers share code and Arb, but the paper calls this
   replay rather than independent reproduction.  The trust claim is accurate.
3. The six-sheet application depends on a large accepted companion chain,
   but the full chain and its exact manuscript hash are included and the new
   article states the dependence.
4. The literature audit cannot establish priority, but the external wording
   explicitly forbids “first” and “world-leading.”

## Final recommendation

`HOLD_FOR_REPAIR`.  There is no Critical or Major objection and no identified
counterexample to a theorem, but DA-1 is a Minor written-proof defect.  A fresh
review must examine new manifested bytes after repair.
