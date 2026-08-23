# Claim boundary

## What is claimed

### P7a: full effective \(e=4\) Polydegree column

For every integer \(d\ge2\),
\[
\mathcal G_{(d+4)}\subseteq\overline{\mathcal G_{(d,5)}}.
\]
The proof boundary is explicit: published mathematics covers \(2\le d<20\);
an exact construction covers \(d\equiv1\pmod4\); a frozen Arb ledger covers
the other residues for \(5\le m<5000\); and a written analytic envelope covers
\(m\ge5000\).

### P7b: universal bordered-Jacobian identity

The Lean development proves the displayed signed-minor and bordered
determinant identities for the binary-form multiplication Jacobian over every
commutative ring.  Cancellation occurs only in the universal polynomial ring;
the resulting identity is then specialized to arbitrary rings.

### Boundary-norm transfer

The norm lemma and finite-pencil criterion are unconditional algebraic
statements under their hypotheses.  The transfer theorem is conditional on a
specified geometric boundary package.  The six-sheet application inherits
that package from the accepted companion proof.  The example \(A=1,B=s\)
shows that the finite-pencil hypothesis is necessary for this method.

## What is not claimed

- No proof or refutation of JC2.
- No proof or refutation of HC4.
- No extension of a finite degree-four JC2 analysis to arbitrary degrees.
- No claim that computation alone proves the Polydegree theorem: the
  normalization, interval predicates, coverage split, and eventual bridge are
  mathematical proof obligations written in the article.
- No independent reproduction of FLINT/Arb, Mathlib, Lean, Python, or Sympy.
- No external peer review, journal acceptance, or unconditional priority
  declaration.
- No claim that every polynomial Keller map satisfies the boundary package
  used by the conditional transfer theorem.

## Calibrated significance assessment

The source audit supports presenting P7a as the strongest and most plausibly
original result in the corpus, subject to specialist priority review.  P7b is
a substantial formal-assurance contribution.  The boundary-norm result is a
reusable conceptual extraction with a sharp method boundary.  The audit did
not locate a close precursor, but absence from a bounded search is not a
proof of priority.
