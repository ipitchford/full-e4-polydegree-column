# A seed-independent boundary-norm transfer criterion

**Status:** new working theorem candidate; not yet independently reviewed  
**Date:** 23 August 2026  
**Scope:** conditional transfer theorem for polynomial graph sections over
`k = C`; no assertion of `JC_2`

## 1. Why this is an extension

The accepted parent P5 proves a graph obstruction for one fixed six-sheeted
graded Keller seed. Its norm step depends only on a much smaller set of data:
a one-parameter horizontal boundary, an affine-line dicritical covering each
boundary factor, and a coprime residual pencil. This note isolates those data
and turns the seed calculation into a reusable theorem.

The main simplification is finite. Although graph equations have arbitrary
degree, the terminal obstruction is equivalent to checking whether a
two-dimensional polynomial pencil contains one of finitely many monomials.

## 2. Algebraic norm lemma

Let `k = C`, let `s` be an indeterminate, and let `kappa >= 0`. Let

\[
F_i(s,l)\in k[s,l]
\]

be irreducible and monic of positive `l`-degree `n_i`, and put

\[
f_i(s)=F_i(s,0)\ne0,
\qquad
K_i=\operatorname{Frac}(k[s,l]/(F_i)).
\]

Assume that there is a finite extension

\[
K_i\hookrightarrow L_i=k(t)
\]

of degree `e_i` such that:

1. the image `s(t)` is a nonconstant polynomial;
2. the image `l(t)` is a polynomial; and
3. `h(t)=s(t)^kappa/l(t)` is a polynomial.

### Lemma 2.1 (cover-degree-free norm support)

Under these assumptions,

\[
f_i(s)=c_i s^{q_i},
\qquad c_i\in k^\times,
\qquad 0\le q_i\le \kappa n_i.
\tag{2.1}
\]

#### Proof

Because `s(t)` is a nonconstant polynomial, `t` is integral over `k[s]`:
divide the equation `s(T)-s=0` by the leading coefficient of `s(T)`. Hence
`k[t]` is finite integral over `k[s]`, and `h(t)` is integral over `k[s]`.
Its field norm to `k(s)` is therefore integral over `k[s]`. It also lies in
`k(s)`; normality of the PID `k[s]` gives

\[
N_{L_i/k(s)}(h)\in k[s].
\]

Monicity and irreducibility give `[K_i:k(s)]=n_i` and

\[
N_{K_i/k(s)}(l)=(-1)^{n_i}f_i(s).
\]

Since `h=s^kappa/l` belongs to `K_i`, the tower law gives

\[
N_{L_i/k(s)}(h)
=\pm\frac{s^{\kappa e_i n_i}}{f_i(s)^{e_i}}
\in k[s].
\tag{2.2}
\]

Thus `f_i(s)^{e_i}` divides a power of `s` in the UFD `k[s]`. Every
irreducible factor of `f_i` is therefore associated to `s`, which proves the
monomial form. Comparing exponents in (2.2) gives
`e_i q_i <= kappa e_i n_i`, and the covering degree cancels. This proves
(2.1). `square`

## 3. The finite pencil criterion

Let `A,B in k[s]` be nonzero coprime polynomials. Define the low-monomial
set

\[
\mathcal M_\kappa=\{c s^q:c\in k^\times,\ 0\le q\le\kappa\}.
\]

### Lemma 3.1 (all homogeneous degrees reduce to the pencil)

The following are equivalent.

1. The pencil `kA+kB` is disjoint from `M_kappa`.
2. For every `m>=1` and every nonzero homogeneous
   `H_m in k[X,Y]` of degree `m`,

   \[
   H_m(A(s),B(s))\notin\mathcal M_\kappa.
   \tag{3.1}
   \]

#### Proof

The implication 2 to 1 is the degree-one case. Conversely, factor over the
algebraically closed field:

\[
H_m(X,Y)=c\prod_{j=1}^m(a_jX+b_jY).
\]

If `H_m(A,B)=c' s^q` with `q<=kappa`, unique factorization in `k[s]`
forces every nonzero factor `a_jA+b_jB` to be a scalar times `s^{q_j}`,
where `0<=q_j<=q<=kappa`. At least one such pencil element therefore lies
in `M_kappa`, contradicting 1. `square`

This lemma is sharp as an algebraic criterion. For `A=1`, `B=s`, and
`kappa>=1`, the pencil contains both `1` and `s`; the degree-one forms `X`
and `Y` attain the forbidden monomials. This is a counterexample to weakening
the pencil hypothesis, not a Keller-map counterexample.

## 4. Boundary-chart transfer theorem

Let `H in k[U,V]` be nonzero, with `H(0,0)=0`, degree `m`, and top homogeneous
part `H_m`. Suppose that, under a hypothetical identification of a selected
graph preimage component with `A^2`, the following data have been proved.

### Transfer hypotheses `BN(kappa;A,B)`

1. There is an integral partial boundary chart with parameters `(s,epsilon,l)`
   whose graph closure is saturated and whose special fibre at `epsilon=0`
   is the monic polynomial

   \[
   C_H(s,l)=\prod_iF_i(s,l)^{r_i},
   \qquad \sum_i r_i n_i=m+1.
   \tag{4.1}
   \]

   Each `F_i` is distinct, irreducible, and monic of `l`-degree `n_i>=1`.

2. Its constant term is exactly

   \[
   C_H(s,0)=H_m(s^\kappa A(s),s^\kappa B(s))\ne0.
   \tag{4.2}
   \]

3. Every reduced horizontal factor is a genuine boundary prime, dominates
   the `s`-line, and has regular nonconstant affine target residues

   \[
   U=\frac{s^\kappa A(s)}{l},
   \qquad
   V=\frac{s^\kappa B(s)}{l}.
   \tag{4.3}
   \]

4. Chart--dicritical domination supplies, for every factor, a finite
   dominant affine-line dicritical `A^1_t -> V(F_i)` on which `s(t)` and
   `l(t)` are polynomials.

5. `gcd(A,B)=1`. Consequently Bezout gives `aA+bB=c`, and (4.3) makes

   \[
   h=\frac{s^\kappa}{l}=c^{-1}(aU+bV)
   \]

   a polynomial on every affine-line dicritical.

### Theorem 4.1 (boundary-norm transfer)

If `BN(kappa;A,B)` holds and

\[
(kA+kB)\cap\mathcal M_\kappa=\varnothing,
\tag{4.4}
\]

then the selected graph component cannot be isomorphic to `A^2`.

#### Proof

Apply Lemma 2.1 to every factor in (4.1). Writing
`f_i(s)=F_i(s,0)`, one gets

\[
f_i(s)=c_i s^{q_i},
\qquad q_i\le\kappa n_i.
\]

Taking constant terms in (4.1) and using (4.2),

\[
s^{\kappa m}H_m(A,B)
=c s^Q,
\qquad
Q=\sum_i r_iq_i
\le\kappa\sum_i r_in_i
=\kappa(m+1).
\]

Because the left side is nonzero and divisible by `s^{kappa m}`, this gives

\[
H_m(A,B)=c s^q,
\qquad 0\le q=Q-\kappa m\le\kappa.
\]

Lemma 3.1 contradicts (4.4). `square`

### Corollary 4.2 (finite verification burden)

For any new seed satisfying the geometric transfer hypotheses, the all-degree
top-form condition requires only a finite linear-algebra calculation: solve

\[
uA(s)+vB(s)=c s^q
\]

for `q=0,...,kappa`. No enumeration over graph degrees `m` is necessary.

## 5. Recovery of the accepted six-sheet theorem

For the Kistner--Shaska six-sheet seed, the accepted boundary chart has
`kappa=2` and

\[
A(s)=\alpha+(1-\alpha)s,
\]

\[
B(s)=s\left(
\frac83\alpha^2+
\frac92\alpha(1-\alpha)s+
\frac95(1-\alpha)^2s^2
\right),
\qquad \alpha^2+3\alpha+6=0.
\]

These polynomials are coprime; the accepted exact resultant is `2 alpha !=0`.
If `uA+vB` were a monomial of degree at most two, its cubic coefficient would
force `v=0`, because `(9/5)(1-alpha)^2 != 0`. The remaining polynomial `uA`
has both nonzero constant and linear coefficients unless `u=0`. Hence the
pencil contains none of `c`, `cs`, `cs^2`, and Theorem 4.1 recovers the
all-degree graph obstruction.

The gain is not a stronger conclusion for this one seed. It is a transfer
theorem: every seed with the same boundary architecture can now be screened
by a finite pencil computation.

## 6. Claim boundary and open obligations

This working theorem does **not** prove that an arbitrary graded Keller seed
has `BN(kappa;A,B)`. Saturation, horizontal-boundary exhaustion, nonconstant
affine residues, and affine-line dicritical domination remain geometric proof
obligations for each application. It also does not cover non-graph surfaces,
nontriangular target coordinates, or native plane constructions.

Before release it requires:

1. an independent line-by-line mathematical review;
2. theorem-level literature screening for equivalent UFD/norm-transfer
   statements;
3. exact reconciliation with the parent P4 chart--dicritical lemma;
4. a source-specific application beyond the original seed, or explicit
   labelling as a conditional generalization; and
5. integration into the successor manuscript and frozen package.

