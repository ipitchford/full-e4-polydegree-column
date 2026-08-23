# BorderedJacobianUniversal

This Lean 4 package formalizes the signed maximal-minor and bordered-determinant
identities for the coefficient multiplication map

\[
(A,B) \longmapsto AB,
\]

including degree-zero boundary cases and specialization to every commutative
ring.  It is a formalization of P7b in the frozen HC4JC2 Actions 1--7 package;
it does not prove the Jacobian conjecture, the Hessian conjecture, or a new
resultant theorem.

## Main result

For coefficient vectors `a = (a_0,...,a_r)` and `b = (b_0,...,b_s)`, let
`mulJac r s a b` be the Jacobian of coefficient multiplication, with columns
ordered `a_0,...,a_r,b_0,...,b_s`.  Let

```text
kappa = (a_0,...,a_r,-b_0,...,-b_s)
resultantBA = Res(B,A).
```

`BorderedJacobianUniversal.det_bordered` proves, over an arbitrary
commutative ring,

\[
\det \operatorname{border}(M,v)
=(-1)^{s(r+1)+1}\operatorname{Res}(B,A)
\sum_i v_i\kappa_i.
\]

`BorderedJacobianUniversal.det_mulJac_submatrix` proves every signed maximal
minor:

\[
(-1)^k\det M_{\widehat k}
=(-1)^{r(s+1)}\operatorname{Res}(B,A)\kappa_k.
\]

## Proof architecture

1. `General.lean` proves abstract rectangular-cofactor, kernel, and bordered
   determinant identities over commutative rings without division.
2. `Multiplication.lean` defines the manuscript-ordered multiplication
   Jacobian and proves that `kappa` lies in its right kernel.
3. `Anchor.lean` identifies the anchored maximal minor with Mathlib's
   Sylvester matrix, including `r = 0` or `s = 0`.
4. `Universal.lean` works in the integral domain
   `Z[A_0,...,A_r,B_0,...,B_s]`.  Cancellation of the universal variable
   `A_r` occurs only here.
5. `Specialization.lean` evaluates that universal identity into an arbitrary
   commutative ring and derives the final bordered formula.
6. `Tests.lean` checks `(r,s) = (0,0)` definitionally and gives a concrete
   zero-divisor-ring control over `ZMod 6`.

The universal ring does not need variables for the border row: the universal
maximal-minor identity is specialized first, and the abstract bordered
determinant lemma then supplies every row `v`.

## Rebuild

The package pins Lean and Mathlib in `lean-toolchain` and
`lake-manifest.json`.

```sh
lake update
lake exe cache get
lake build
```

The accepted build environment was Lean 4.32.1, Lake 5.0.0, and Mathlib
commit `520045ab14e26149ee970e2e617ca04b09bde5d6`.

To inspect the logical dependencies, rebuild normally.  Each proof module
ends with `#print axioms` commands for its release-critical theorems.  The
expected output contains only Lean/Mathlib's standard logical dependencies
`propext`, `Classical.choice`, and `Quot.sound` (some elementary indexing
lemmas need fewer).  The source tree contains no `sorry`, `admit`, custom
`axiom`, `unsafe`, `native_decide`, or `simp?` declaration/tactic.

## Trust and claim boundary

The replay checks elaboration and kernel verification of the stated Lean
theorems against the pinned Lean/Mathlib sources.  It does not independently
verify the Lean kernel, compiler, operating system, or the mathematical
priority of the identity.  `FORMALIZATION_CONCORDANCE.md` maps the formal
objects to the frozen manuscript and records the exact sign conventions.

Copyright 2026 HC4JC2 successor project contributors.  Licensed under
Apache-2.0; see `LICENSE`.
