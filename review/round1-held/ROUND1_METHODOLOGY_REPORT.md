# Round 1 Methodology and Evidence report

**Submission manifest:** `299a0326b8dd7d30d2dae9619745f57c7452608814e0fe615e22d5540388cfa2`  
**Role:** computer-assisted proof, formal methods and reproducibility reviewer  
**Independence:** read-only review of submission and replay transcript; no other role report consulted  
**Decision:** **ACCEPT**  
**Issue inventory:** Critical 0; Major 0; Minor 0; Observations 4

## Scope and evidence model

The submission correctly separates theorem text, published input, finite
computation, analytic handoff, formal proof, and exact replay.  It explicitly
states that same-source replay is not independent reproduction.  I reviewed
the P7a manuscript Sections 3--9 (pp. 3--13), all proof-critical P7a scripts
and receipts, the full Lean receipt/concordance, the boundary checker and
negative control, `REPRODUCIBILITY.md`, and the package verifier.

## P7a computer-assisted proof

The coverage partition is complete and nonoverlapping:

- published input covers `2 <= d < 20`;
- for `d >= 20`, writing `d=4m+r` gives `m >= 5`;
- Section 7 handles `r=1` exactly for every `m`;
- the ledger handles `5 <= m < 5000` for `r=0,2,3`;
- the analytic certificate handles `m >= 5000` for `r=0,2,3`.

The normalization audit reconstructs the multinomial formula using exact
`Fraction` arithmetic and checks both admitted and rejected support triples.
The finite auditor reads exactly 14,985 records in canonical order, rejects
trailing cases, checks the producer and source hashes, reconstructs Arb
endpoints, and gates the four strict predicates.  Worst margins are reported,
not hidden: the limiting finite case has `h < 0.465783`, root radius below
`0.006956`, fourth-row margin above `1.475688`, and Jacobian margin above
`0.068434` (paper p. 11).

The eventual proof is materially more than numerical evaluation.  Sections
5.1--5.4 (pp. 5--10) expose the exact first-order operator, rational
second-order majorants, factorial/geometric tail split, Cauchy bounds, and
Newton--Kantorovich inequalities.  The executable certificate uses rational
objects for gates; the one conversion to `float` is only a decimal display
field, while exact numerators/denominators or their canonical-text hashes are
recorded.  The threshold is tested at `m=5000` and monotonicity is explicitly
argued.  Normal and optimized integrated replays produce the same receipt,
and the two finite ledgers are byte-identical.

## Lean formal assurance

The formal receipt binds 14 source/configuration files, Lean 4.32.1, Lake
5.0.0 and an exact Mathlib commit.  The replay checks the exact file set,
forbidden constructs, dependency commit and warning-free `lake build`.
The theorem architecture matches the manuscript: arbitrary-ring kernel and
cofactor lemmas, a universal polynomial-ring cancellation, explicit
specialization, then the border theorem.  The zero-degree and `ZMod 6` tests
exercise the most likely scope regressions.  Only standard `propext`,
`Classical.choice` and `Quot.sound` dependencies are reported; no `sorryAx` or
unexpected axiom occurs.

## Boundary finite checker

The SymPy script uses exact rationals and the algebraic extension
`Q(sqrt(-15))`.  It checks the defining relation, gcd, resultant and ranks of
all three forbidden pencil systems.  The `A=1,B=s` negative control forces
nullity one in degrees zero and one.  All failure gates use explicit branches,
so optimized Python cannot erase them.  The wrapper binds the checker,
mathematical theorem note and article and is deterministic in normal and
optimized modes.

## Package and replay integrity

The outer verifier checks the exact 375-file set, every manifest digest, the
accepted parent manifest, the P7a and boundary source bindings, the Lean
source receipt, and all three manuscript build bindings.  Semantic replay is
kept separate because the Python/Arb, SymPy and Lean environments differ.
That is a sound trust design rather than a weakness.

## Issues

No Critical, Major, or Minor issues are identified.

## Observations (non-blocking, not defects)

1. An external P7a referee should independently rederive the estimates in
   Sections 5--6 rather than treating a successful replay as sufficient.
2. Independent reimplementation of the interval predicates would be the most
   valuable next assurance gain; the current normal/optimized comparison is
   optimization-sensitivity evidence, not implementation independence.
3. A public archive should preserve the pinned dependency metadata and both
   ledgers even if a smaller convenience download is also offered.
4. The Lean development formalizes P7b only; the package accurately avoids
   describing the analytic P7a or geometric boundary theorem as formally
   verified.

## Final recommendation

Accept.  The computational and formal claims are auditable, fail-closed and
appropriately bounded, and the exact frozen bytes passed every stated replay.
