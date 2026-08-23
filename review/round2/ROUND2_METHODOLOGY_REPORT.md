# Round 2 Methodology and Evidence report

**Submission manifest:** `867bff8d9b092a133194cf57a53d06dc3824d8aeb47508c5e5eec614bb8fc4a7`  
**Role:** rigorous numerics, formal verification and reproducibility  
**Independence:** fresh read-only review and replay inspection; no other Round 2 report consulted  
**Decision:** **ACCEPT**  
**Issue inventory:** Critical 0; Major 0; Minor 0; Observations 4

## P7a evidence chain

The proof has five separately auditable links: the published specialization
criterion, exact normalized coefficients, a simple Fourier-limit zero, a
finite interval bridge, and an eventual analytic bridge.  The integer coverage
is complete: published `2<=d<20`; exact residue `r=1`; finite
`5<=m<5000, r in {0,2,3}`; eventual `m>=5000` in those residues.

The normalization auditor uses exact factorial/Fraction formulas and checks
both support and coefficient equality.  The 14,985-record auditor checks
ordered coverage, absence of trailing records, source/producer hashes, cutoff
policy, outward endpoints, and all four strict interval-Newton predicates.
The finite worst case remains strictly within every gate.  Optimized and
normal ledgers and integrated receipts are byte-identical, while the article
correctly says this is replay rather than independent implementation.

The repaired direct high-degree tail is now fully stated.  With
`R_X=max_s|X_s|<=1`, multinomial majorization contributes at most
`(3R_X)^u`; the coefficient bound contributes `(5m+8+u)^u/m^u`; and
`u! >= (u/e)^u`, `e<3` give a base strictly below

`9(5m+8+u)/(mu) = 45/u + 9/m + 72/(mu)`.

For `m>=5000,u>m`, this decreases in both variables and is below `13/1000`
at `(5000,5001)`.  Summing the resulting geometric tail is therefore valid.
The repaired source comment states the same derivation, and the regenerated
eventual receipt tests the exact rational endpoint.  The rest of the eventual
certificate exposes exact head bounds, a rational Taylor exponential upper
bound, Cauchy derivative constants, Newton--Kantorovich inequalities and
transport margins.  Decimal conversions are display-only.

## P7b formal chain

The exact candidate source set matches the formal receipt.  The verifier pins
Lean/Lake/Mathlib, scans for placeholders and unsafe constructs, checks the
Mathlib commit, builds without warnings, and rejects unexpected axioms.  The
theorem map covers the ring-general cofactor relation, anchored resultant
minor, universal cancellation, specialization, maximal minors and border.
The zero-degree and `ZMod 6` controls exercise boundary and zero-divisor scope.

## Boundary finite calculation

The exact SymPy computation verifies the quadratic relation, gcd, resultant
and ranks of the three prohibited monomial systems over the stated quadratic
field.  Its `span(1,s)` negative control has the expected nonzero nullities.
Explicit failures survive optimized Python.  The package does not mistake this
small exact calculation for a proof of the conditional geometric interface.

## Package integrity

The outer gate verifies exactly 375 subject files, transitive manuscript and
receipt hashes, and the frozen parent manifest.  Semantic replays are split by
environment and all passed.  PDF generation reports 14/5/6 pages and no
overfull boxes.

## Issues

No Critical, Major, or Minor issues are identified.

## Observations (non-blocking, not defects)

1. A second interval-arithmetic implementation remains the best next
   assurance improvement.
2. External reviewers should audit the handwritten derivation of the finite
   tail majorant and monotonicity, not only run the verifier.
3. A clean Lean build verifies P7b relative to the pinned kernel/dependency;
   it does not formalize P7a or the boundary geometry, exactly as stated.
4. Preserve the manifest and both finite ledgers in any archival release.

## Final recommendation

Accept.  The repaired proof/evidence interface is complete, deterministic and
accurately bounded.
