# Formal verification of a universal bordered Jacobian identity over arbitrary commutative rings

**Formalization companion article, 23 August 2026**  
**Status:** kernel-checked Lean 4 development; internally replayed; not externally peer reviewed

## Abstract

Let $A=\sum_{i=0}^r a_iX^i$ and $B=\sum_{j=0}^s b_jX^j$ over a
commutative ring, and let $M$ be the Jacobian of the coefficient
multiplication map $(A,B)\mapsto AB$. We give a Lean 4 formalization of all
signed maximal minors of $M$ and of the determinant obtained by appending an
arbitrary row. The final theorems hold over every commutative ring, including
rings with zero divisors and the boundary cases $r=0$ or $s=0$. The proof
avoids division and rank assumptions. It first proves an abstract
cross-multiplied cofactor relation over arbitrary rings, identifies one
anchored minor with a Sylvester resultant, cancels a single coefficient only
in a universal polynomial integral domain, and then specializes the universal
identity to the target ring. The pinned package builds without warnings or
unproved placeholders under Lean 4.32.1 and Mathlib v4.32.1. This is a formal
verification of the stated determinant identities, not a result on the
Jacobian or Hessian conjectures and not a priority claim for the classical
identity.

## 1. Statement

Fix $r,s\ge0$ and a commutative ring $R$. Put

\[
A(X)=\sum_{i=0}^r a_iX^i,
\qquad
B(X)=\sum_{j=0}^s b_jX^j.
\]

Order the coefficient variables as

\[
a_0,\ldots,a_r,b_0,\ldots,b_s.
\]

The coefficient multiplication map has $r+s+1$ output coordinates and
$r+s+2$ input coordinates. Its Jacobian is therefore a rectangular matrix

\[
M\in\operatorname{Mat}_{r+s+1,r+s+2}(R),
\]

with entries

\[
M_{k,a_i}=b_{k-i},\qquad M_{k,b_j}=a_{k-j},
\tag{1.1}
\]

where out-of-range coefficients are zero. Define

\[
\kappa=(a_0,\ldots,a_r,-b_0,\ldots,-b_s)
\tag{1.2}
\]

and use the resultant convention

\[
\mathcal R_{r,s}(A,B)=\operatorname{Res}(B,A).
\tag{1.3}
\]

For a column $k$, let $M_{\widehat k}$ denote the order-preserving
submatrix obtained by deleting that column.

### Theorem 1.1 (signed maximal minors)

For every commutative ring $R$, all $r,s\ge0$, every coefficient family,
and every column $k$,

\[
\boxed{
(-1)^k\det M_{\widehat k}
=(-1)^{r(s+1)}\mathcal R_{r,s}(A,B)\kappa_k.}
\tag{1.4}
\]

### Theorem 1.2 (bordered determinant)

Append an arbitrary row $v=(v_0,\ldots,v_{r+s+1})$ below $M$. Then

\[
\boxed{
\det\operatorname{border}(M,v)
=(-1)^{s(r+1)+1}\mathcal R_{r,s}(A,B)
\sum_kv_k\kappa_k.}
\tag{1.5}
\]

The Lean theorems are respectively
`BorderedJacobianUniversal.det_mulJac_submatrix` and
`BorderedJacobianUniversal.det_bordered`.

## 2. The ring-general cofactor mechanism

The identity

\[
M\kappa=0
\tag{2.1}
\]

is the differential form of $AB-AB=0$. In coordinates, each output row is
the difference of the same convolution sum in opposite orders. The formal
proof first uses a sum-type index separating the $a$- and $b$-columns,
then transports the result along an explicit equivalence to the manuscript
order (1.1). This separation prevents an indexing convention from being
hidden inside simplification.

For a general $n\times(n+1)$ matrix $N$, define its signed cofactor vector

\[
C_k=(-1)^k\det N_{\widehat k}.
\]

The familiar field argument would say that two kernel vectors are
proportional when the kernel is one-dimensional. That argument is unusable
over a ring with zero divisors: rank and division need not behave as required.
Instead the formalization proves the cross-multiplied identity

\[
x_pC_k=x_kC_p
\tag{2.2}
\]

for every $x$ with $Nx=0$. The proof appends a selector row to $N$,
uses the adjugate identity, and expands the resulting determinants. It is
valid over an arbitrary commutative ring and assumes neither generic rank nor
the invertibility of any coefficient.

The same abstract file proves Laplace expansion of an arbitrary border:

\[
\det\operatorname{border}(N,v)=(-1)^n\sum_kv_kC_k.
\tag{2.3}
\]

Thus Theorem 1.2 becomes a formal consequence of Theorem 1.1 once its signs
are reconciled.

## 3. The anchored Sylvester minor

Delete the column corresponding to $a_r$. After separating its last row,
the remaining core is identified entry by entry with Mathlib's Sylvester
matrix. The formal theorem is

\[
\det M_{\widehat{a_r}}
=(-1)^{rs}\operatorname{Res}(B,A)a_r.
\tag{3.1}
\]

No positive-degree side condition is inserted: the proof includes $r=0$,
$s=0$, and $r=s=0$. Combining (3.1) with the cofactor sign gives

\[
C_{a_r}=(-1)^{r(s+1)}\operatorname{Res}(B,A)a_r.
\tag{3.2}
\]

The use of $\operatorname{Res}(B,A)$, rather than
$\operatorname{Res}(A,B)$, is part of the theorem statement and is tested
throughout the concordance. This avoids absorbing a degree-dependent sign in
informal notation.

## 4. Universal cancellation and specialization

Equation (2.2), with $x=\kappa$ and $p=a_r$, gives

\[
a_rC_k
=\kappa_k(-1)^{r(s+1)}\operatorname{Res}(B,A)a_r.
\tag{4.1}
\]

It is generally invalid to cancel $a_r$ in $R$. The proof therefore moves
to the universal ring

\[
U=\mathbb Z[A_0,\ldots,A_r,B_0,\ldots,B_s],
\]

an integral domain in which the universal variable $A_r$ is nonzero. The
single cancellation in (4.1) is made only in $U$, yielding the universal
cofactor identity (1.4).

For an arbitrary commutative ring $R$, the coefficient assignment defines
a ring homomorphism $U\to R$. The formal specialization layer proves that
this map commutes with every relevant matrix entry, polynomial coefficient,
resultant, determinant and cofactor. Mapping the universal theorem into $R$
therefore gives (1.4) without cancellation in $R$. Finally (2.3) gives
(1.5).

This architecture is the central assurance gain of the formalization. The
arbitrary-ring theorem is not extrapolated from a generic-field calculation;
it is obtained by an explicit universal identity and functorial
specialization.

## 5. Formal object and theorem map

| Mathematical object | Lean declaration |
|---|---|
| coefficient extension by zero | `coeffExt` |
| multiplication Jacobian $M$ | `mulJac` |
| kernel vector $\kappa$ | `kappa` |
| abstract border | `border` |
| signed cofactor vector | `cofactorVec` |
| kernel identity (2.1) | `mulJac_mulVec_kappa` |
| cross relation (2.2) | `kernel_cofactor_proportional` |
| anchored minor (3.1) | `det_anchorMinor` |
| universal cofactor formula | `universal_cofactorVec` |
| arbitrary-ring maximal minors | `det_mulJac_submatrix` |
| arbitrary-ring border formula | `det_bordered` |

The detailed file-by-file and sign concordance is distributed as
`FORMALIZATION_CONCORDANCE.md`.

## 6. Boundary and zero-divisor tests

Two executable formal tests address common failure modes.

1. `det_bordered_zero_zero` reduces the $r=s=0$ theorem to the explicit
   $2\times2$ determinant, checking the smallest dimension and its sign.
2. `zmod_six_one_one_control` instantiates a nonzero bordered determinant in
   $\mathbb Z/6\mathbb Z$. It confirms that the released theorem is not
   accidentally restricted to domains or fields.

Tests do not replace the general proof, but they expose off-by-one indexing,
sign and hidden-domain regressions at inexpensive concrete points.

## 7. Reproducibility receipt

The package pins:

- Lean 4.32.1, commit
  `f054605aea4b840552cca2e725580bffd1e1b704`;
- Lake 5.0.0;
- Mathlib v4.32.1, commit
  `520045ab14e26149ee970e2e617ca04b09bde5d6`.

The accepted clean build processed 1,966 jobs with no warnings. A fail-closed
source scan found no `sorry`, `admit`, custom `axiom`, `sorryAx`,
`native_decide`, `unsafe`, or `simp?`. The release-critical `#print axioms`
output contains only the standard Lean/Mathlib dependencies `propext`,
`Classical.choice`, and `Quot.sound`. The formal receipt has SHA-256

```text
bc57d920fe4f6679a2b8fa871209f43de99de146c1c012b4a8a81dcadeb494a9
```

and binds every source, toolchain and concordance file by SHA-256. A clean
replay is

```sh
python3 verify_release.py
```

from the formal package directory after fetching the pinned dependencies.

## 8. Trust and claim boundary

The successful build means that the stated Lean theorems elaborate and are
accepted by the pinned Lean kernel relative to Mathlib. It does not
independently verify the kernel, compiler, operating system or Mathlib. The
package has been internally replayed, not independently reproduced or
externally peer reviewed.

The formalization establishes only the determinant identities (1.4)--(1.5).
It does not prove invertibility of a polynomial map, the two-dimensional
Jacobian conjecture, the quartic Hessian conjecture, or originality of the
classical algebraic ingredients.

## Declarations

**Code availability.** Lean source, lockfiles, concordance, verifier and the
exact receipt accompany the successor package under the Apache-2.0 license.

**Author responsibility.** The submitting author is responsible for the
mathematical statement, sign conventions and interpretation of the formal
result.

**AI-use disclosure.** AI systems contributed to proof architecture, Lean
implementation, replay, review and drafting. Internal AI review is not
external peer review.
