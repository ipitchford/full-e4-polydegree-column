# A finite pencil criterion for boundary-norm graph obstructions

**Candidate research article, 23 August 2026**  
**Status:** theorem candidate; internally checked; not externally peer reviewed

## Abstract

Boundary arguments for polynomial graph sections often produce arbitrarily
high-degree homogeneous forms, apparently requiring a new obstruction in every
degree. We show that, under a precise dicritical-cover package, the entire
all-degree problem is equivalent to one finite calculation in a
two-dimensional polynomial pencil. The key field-norm lemma is independent of
the degree of the covering dicritical: if both \(s\) and \(\ell\) pull back to
polynomials on an affine-line cover and \(s^\kappa/\ell\) is polynomial, then
the boundary constant term is a monomial \(cs^q\) with
\(q\le\kappa\deg_\ell F\). Factoring a homogeneous form into linear factors
then reduces every graph degree to whether
\(\mathbb C A+\mathbb C B\) contains one of
\(1,s,\ldots,s^\kappa\), up to scalar. We formulate a conditional
boundary-norm transfer theorem, recover the graph obstruction for the
six-sheeted graded Keller seed of Kistner and Shaska, and prove that the pencil
hypothesis is sharp for this method. The theorem does not establish the
geometric boundary package for arbitrary maps and does not decide the
two-dimensional Jacobian conjecture.

## 1. Motivation and result

Let \(k=\mathbb C\). Consider a polynomial graph equation

\[
W+H(U,V)=0,
\qquad H(0,0)=0.
\]

In the six-sheeted graded Keller example of Kistner and Shaska [1], a
boundary chart for a hypothetical affine-plane inverse-image component has
residual target functions

\[
U=\frac{s^\kappa A(s)}{\ell},
\qquad
V=\frac{s^\kappa B(s)}{\ell},
\tag{1.1}
\]

with \(\kappa=2\). The accepted case-specific proof factors the special
fibre of the graph closure and applies field norms on covering affine-line
dicriticals. This article isolates the algebra that actually drives the final
contradiction.

The main conceptual result is that no enumeration over \(\deg H\) is needed.
Once the geometric boundary package has been proved for a seed, the
all-degree obstruction is equivalent to the finite condition

\[
(kA+kB)\cap
\{cs^q:c\in k^\times,\ 0\le q\le\kappa\}=\varnothing.
\tag{1.2}
\]

This is an extension of the fixed-seed proof, not a solution of a Jacobian
case. In particular, the hypotheses below are not asserted for every graded
Keller map.

## 2. A cover-degree-free norm lemma

Let \(s,\ell\) be indeterminates and let \(\kappa\ge0\). Let

\[
F(s,\ell)\in k[s,\ell]
\]

be irreducible and monic of positive \(\ell\)-degree \(n\). Put

\[
f(s)=F(s,0)\ne0,
\qquad
K=\operatorname{Frac}(k[s,\ell]/(F)).
\]

Assume there is a finite extension

\[
K\hookrightarrow L=k(t)
\]

of degree \(e\) such that the images \(s(t)\) and \(\ell(t)\) are
polynomials, \(s(t)\) is nonconstant, and

\[
h(t)=\frac{s(t)^\kappa}{\ell(t)}\in k[t].
\tag{2.1}
\]

### Lemma 2.1 (norm-support bound)

Under these assumptions,

\[
\boxed{f(s)=cs^q,\qquad c\in k^\times,\qquad0\le q\le\kappa n.}
\tag{2.2}
\]

#### Proof

Because \(s(t)\) is a nonconstant polynomial, \(t\) is integral over
\(k[s]\): divide \(s(T)-s\) by the nonzero constant leading coefficient of
\(s(T)\). Thus \(k[t]\) is finite integral over \(k[s]\), and the polynomial
\(h(t)\) is integral over \(k[s]\).

Its field norm \(N_{L/k(s)}(h)\) is integral over \(k[s]\) and lies in
\(k(s)\). Since the PID \(k[s]\) is integrally closed,

\[
N_{L/k(s)}(h)\in k[s].
\tag{2.3}
\]

Monicity and Gauss's lemma give \([K:k(s)]=n\), while

\[
N_{K/k(s)}(\ell)=(-1)^nf(s).
\]

Since \(h=s^\kappa/\ell\) belongs to \(K\), the tower law gives

\[
N_{L/k(s)}(h)
=\left(N_{K/k(s)}(h)\right)^e
=\pm\frac{s^{\kappa en}}{f(s)^e}
\in k[s].
\tag{2.4}
\]

Hence \(f(s)^e\) divides a power of \(s\) in the UFD \(k[s]\). Every
irreducible factor of \(f\) is therefore associated to \(s\), proving
\(f=cs^q\). Comparing exponents in (2.4) gives
\(eq\le\kappa en\), and the cover degree \(e\) cancels. \(\square\)

The cancellation of \(e\) is useful: the boundary curve itself need not have
affine-line normalization. It suffices to have a finite dominant affine-line
dicritical above it.

## 3. Every homogeneous degree reduces to one pencil

For coprime nonzero \(A,B\in k[s]\), define

\[
\mathcal M_\kappa=
\{cs^q:c\in k^\times,\ 0\le q\le\kappa\}.
\]

### Lemma 3.1 (finite pencil equivalence)

The following are equivalent.

1. \((kA+kB)\cap\mathcal M_\kappa=\varnothing\).
2. For every \(m\ge1\) and every nonzero homogeneous
   \(H_m\in k[X,Y]\) of degree \(m\),

   \[
   H_m(A(s),B(s))\notin\mathcal M_\kappa.
   \tag{3.1}
   \]

#### Proof

The second statement implies the first by taking \(m=1\). Conversely, factor
over the algebraically closed field:

\[
H_m(X,Y)=c\prod_{j=1}^m(a_jX+b_jY).
\]

Suppose \(H_m(A,B)=c's^q\) with \(q\le\kappa\). No factor
\(a_jA+b_jB\) is zero, since the product is nonzero. Unique factorization in
\(k[s]\) forces every factor to be \(c_js^{q_j}\), with
\(q_j\ge0\) and \(\sum_jq_j=q\). Thus at least one pencil element belongs
to \(\mathcal M_\kappa\), contradicting statement 1. \(\square\)

### Corollary 3.2 (finite algorithm)

Condition 1 is decided by the finite family of linear systems

\[
uA(s)+vB(s)=cs^q,
\qquad q=0,\ldots,\kappa.
\tag{3.2}
\]

No graph-degree cutoff is involved.

## 4. The geometric transfer package

The next theorem separates geometry from algebra. Let
\(H\in k[U,V]\setminus\{0\}\) satisfy \(H(0,0)=0\), put
\(m=\deg H\ge1\), and write \(H_m\) for its top homogeneous part. Suppose
that, under a hypothetical identification of a selected graph inverse-image
component with \(\mathbb A^2\), one has proved the following data.

### Boundary-norm hypotheses \(\mathrm{BN}(\kappa;A,B)\)

1. There is an integral saturated partial boundary chart with parameters
   \((s,\varepsilon,\ell)\). If \(m=\deg H\), its scheme-theoretic special
   fibre at \(\varepsilon=0\) is the monic polynomial

   \[
   C_H(s,\ell)=\prod_iF_i(s,\ell)^{r_i},
   \qquad \sum_i r_i n_i=m+1,
   \tag{4.1}
   \]

   where the \(F_i\) are distinct irreducible monic polynomials and
   \(n_i=\deg_\ell F_i\ge1\).

2. Its constant term is exactly

   \[
   C_H(s,0)=H_m(s^\kappa A(s),s^\kappa B(s))\ne0.
   \tag{4.2}
   \]

3. Every reduced factor is a genuine horizontal boundary prime and has
   regular nonconstant target residues

   \[
   U=\frac{s^\kappa A(s)}\ell,
   \qquad
   V=\frac{s^\kappa B(s)}\ell.
   \tag{4.3}
   \]

4. Every factor is dominated by a finite affine-line dicritical
   \(\mathbb A^1_t\to V(F_i)\) on which \(s(t)\) and \(\ell(t)\) are
   polynomials.

5. \(\gcd(A,B)=1\). Hence Bézout's identity and (4.3) make

   \[
   h=\frac{s^\kappa}{\ell}
   \]

   polynomial on each affine-line dicritical.

These hypotheses are deliberately explicit. Saturation, boundary exhaustion,
regular residues and dicritical domination are proof obligations, not
automatic consequences of writing down a chart.

## 5. Boundary-norm transfer

### Theorem 5.1

If \(\mathrm{BN}(\kappa;A,B)\) holds and

\[
(kA+kB)\cap\mathcal M_\kappa=\varnothing,
\tag{5.1}
\]

then the selected graph component cannot be isomorphic to \(\mathbb A^2\).

#### Proof

Put \(f_i(s)=F_i(s,0)\). Hypotheses 3--5 allow Lemma 2.1 to be applied to
every factor in (4.1). Thus

\[
f_i(s)=c_is^{q_i},
\qquad0\le q_i\le\kappa n_i.
\tag{5.2}
\]

Taking constant terms in (4.1) and using (4.2),

\[
s^{\kappa m}H_m(A,B)
=cs^Q,
\qquad
Q=\sum_i r_iq_i
\le\kappa\sum_i r_in_i
=\kappa(m+1).
\tag{5.3}
\]

The left side is nonzero and divisible by \(s^{\kappa m}\), so
\(Q\ge\kappa m\). Consequently

\[
H_m(A,B)=cs^q,
\qquad0\le q=Q-\kappa m\le\kappa.
\]

This contradicts Lemma 3.1 and (5.1). \(\square\)

The theorem is seed-independent but conditional. Its value is that after the
geometric package has been established, the unbounded family of graph degrees
collapses to the finite pencil test (3.2).

## 6. Six-sheeted application

For the Kistner--Shaska six-sheeted seed [1, Theorem 3.19], the companion
boundary-chart calculation gives \(\kappa=2\) and

\[
A(s)=\alpha+(1-\alpha)s,
\tag{6.1}
\]

\[
B(s)=s\left(
\frac83\alpha^2+
\frac92\alpha(1-\alpha)s+
\frac95(1-\alpha)^2s^2
\right),
\qquad
\alpha^2+3\alpha+6=0.
\tag{6.2}
\]

The full chart proof establishes \(\mathrm{BN}(2;A,B)\) for every nonzero
graph polynomial \(H\) with \(H(0,0)=0\); it is included byte-for-byte as the
accepted companion six-sheet graph manuscript in the same evidence package.
Its canonical Markdown SHA-256 is
`c7fc0e7ed904504e1b7a7ec01e4a22c867b9d9b2bfe9978bc23619c794240010`.
The required algebra is short:

\[
\operatorname{Res}_s(A,B)=2\alpha\ne0,
\]

so \(A\) and \(B\) are coprime. If \(uA+vB\) were a monomial of degree at
most two, its cubic coefficient would force \(v=0\), because
\((9/5)(1-\alpha)^2\ne0\). The remaining polynomial \(uA\) has both a
nonzero constant and a nonzero linear coefficient unless \(u=0\). Therefore

\[
(kA+kB)\cap\{c,cs,cs^2:c\in k^\times\}=\varnothing.
\tag{6.3}
\]

Theorem 5.1 recovers the all-degree graph obstruction. An exact SymPy checker
over \(\mathbb Q(\sqrt{-15})\) verifies the field relation, resultant, gcd and
all three pencil systems under both normal and optimized Python.

This application is distinct from Proposition 3.21 of [1]. That proposition
shows that the three-variable graded family does not directly become a
two-variable polynomial pair after the substitution \(T=\Lambda w\), because
a top term has a negative \(\Lambda\)-exponent. The present theorem concerns
polynomial graph sections, finite boundary normalizations and field norms.

## 7. Sharp limitation of the method

The pencil condition cannot be weakened within the norm/top-form argument.
Take

\[
A=1,\qquad B=s,\qquad\kappa\ge1.
\]

Then \(A\) and \(B\) are coprime, but the pencil contains both \(1\) and
\(s\). The degree-one homogeneous forms \(X\) and \(Y\) already produce
forbidden monomials. Thus condition (5.1) is necessary and sufficient for the
all-degree conclusion of Lemma 3.1.

This is a counterexample to weakening the algebraic method, not a Keller-map
counterexample and not a counterexample to Theorem 5.1. A seed whose pencil
meets \(\mathcal M_\kappa\) may still be obstructed by other geometry.

## 8. Literature position and limitations

Orevkov's boundary-chain and multiplicity arguments [2] and Borisov's Stein
factorization theorem [3] provide strong global restrictions on hypothetical
plane Keller maps. In particular, Borisov already proves much of the
one-point boundary and normalization geometry that appeared broadly in the
predecessor P4 manuscript. We do not claim those global facts as new.

The contribution isolated here is narrower: the cover-degree-free exponent
bound, the finite-pencil equivalence, and their conditional transfer through a
precise graph-boundary package. Current exact-phrase, citation-chain and arXiv
searches found no equivalent graph-section theorem, but this is not a proof of
priority.

The limitations are substantive:

- \(\mathrm{BN}(\kappa;A,B)\) must be proved for each application;
- the theorem does not cover arbitrary non-graph surfaces or arbitrary target
  coordinate changes;
- the six-sheet application depends on the companion chart-to-dicritical
  proof, not merely on the displayed pencil calculation;
- the Kistner--Shaska seed paper is a current unrefereed arXiv v1; and
- no conclusion about the two-dimensional Jacobian conjecture follows.

## References

[1] K. Kistner and T. Shaska, “Orbits and fields of definition for graded
Keller maps,” arXiv:2608.02863v1 (2026).
<https://arxiv.org/abs/2608.02863v1>.

[2] S. Yu. Orevkov, “On three-sheeted polynomial mappings of
\(\mathbb C^2\),” *Mathematics of the USSR-Izvestiya* **29** (1987),
409--430. <https://doi.org/10.1070/IM1987v029n03ABEH000984>.

[3] A. Borisov, “On the Stein factorization of resolutions of
two-dimensional Keller maps,” *Beiträge zur Algebra und Geometrie* **56**
(2015), 299--312. <https://doi.org/10.1007/s13366-014-0208-4>.

## Declarations

**Data and code availability.** The companion geometric proof, exact pencil
checker, receipts and frozen manifest accompany the candidate article.

**Author responsibility.** The submitting author is responsible for every
mathematical and historical claim.

**AI-use disclosure.** AI systems contributed to source discovery, theorem
extraction, proof exploration, exact checking, review and drafting. Internal
AI review is not external peer review.
