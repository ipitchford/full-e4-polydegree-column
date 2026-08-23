# Effective Fourier certificates for the full (e=4) Polydegree column

**Candidate research article, 23 August 2026**  
**Status:** computer-assisted theorem candidate; internally replayed; not externally peer reviewed

## Abstract

Let \(\mathcal G_{\mathbf d}\) denote the polydegree stratum of plane
polynomial automorphisms over \(\mathbb C\). Lewis, Perry and Straub gave an
explicit coefficient-polynomial criterion implying

\[
\mathcal G_{(d+4)}\subseteq\overline{\mathcal G_{(d,5)}}
\]

and verified it for \(2\le d<20\). We prove the containment for every
\(d\ge2\). The proof makes a previously qualitative Fourier-limit argument
effective. After writing \(d=4m+r\), one residue class has an exact solution
at the origin. For the other three classes, exact rational coefficient bounds
and complex interval Newton estimates certify all \(14{,}985\) cases
\(5\le m<5000\). A uniform analytic envelope proves every \(m\ge5000\).
The finite ledger was recomputed under normal and optimized Python, producing
byte-identical 17 MB certificates, and a separate fail-closed audit checks
coverage, ordering, hashes and explicit outward-rounded interval endpoints.
The uniform certificate uses exact rational arithmetic together with 256-bit
Arb evaluation only for cancellation-sensitive Fourier constants. This is a
computer-assisted proof of one Polydegree-containment column; it is not a
result about the Jacobian or Hessian conjectures.

## 1. Statement and relation to earlier work

For \(e\ge1\), write \(\mathbf x=(x_1,\ldots,x_e)\). If
\(\mathbf a\in\mathbb Z_{\ge0}^e\), put

\[
|\mathbf a|=\sum_{s=1}^e a_s,
\qquad
\mathbf a\cdot\mathbf N=\sum_{s=1}^e s a_s.
\]

Following Lewis--Perry--Straub [1], define

\[
g_{n,e}=\frac1{n+1}
\sum_{\mathbf a\cdot\mathbf N=n}(-1)^{|\mathbf a|}
\binom{n+|\mathbf a|}{a_1,\ldots,a_e,n}\mathbf x^{\mathbf a}.
\tag{1.1}
\]

Their Theorem 4 implies the following specialization criterion.

### Published input 1.1 (Lewis--Perry--Straub)

If there is \(P\in\mathbb C^e\) satisfying

\[
g_{d,e}(P)=\cdots=g_{d+e-2,e}(P)=0,
\quad
g_{d+e-1,e}(P)\ne0,
\quad
a_{d,e}(P)\ne0,
\tag{1.2}
\]

where \(a_{d,e}\) is their determinant polynomial, then

\[
\mathcal G_{(d+e)}\subseteq
\overline{\mathcal G_{(d,e+1)}}.
\tag{1.3}
\]

They verified (1.2) for \(e=4\) and \(2\le d<20\) [1, Theorem 13(b)].
Perry's earlier dissertation verifies a different, weaker intersection
statement through \(d=45\) [2]; it must not be read as the containment in
(1.3).

Our main result is as follows.

### Theorem A

For every integer \(d\ge2\),

\[
\boxed{\mathcal G_{(d+4)}\subseteq
\overline{\mathcal G_{(d,5)}}.}
\tag{1.4}
\]

The new range is \(d\ge20\). Its proof is computer-assisted only on the
finite interval \(20\le d<20000\); an analytic certificate covers all larger
degrees. The residue class \(d\equiv1\pmod4\) also follows from Edo's known
divisibility theorem [4]; the new work is in the other three residue classes.

The literature audit accompanying this article did not locate an earlier
all-\(d\) proof of (1.4), but that is an absence finding rather than a priority
theorem. We therefore make no claim of being first until specialists have
checked the result and its historical positioning.

## 2. Reduction to a smooth common zero

Lewis--Perry--Straub define polynomials \(\alpha_{i,j,e}\) and

\[
a_{d,e}=\det(\alpha_{i,j,e})_{
0\le i\le e-1,\ d-1\le j\le d+e-2}.
\]

Direct coefficient differentiation gives

\[
\alpha_{i,j,e}=-\frac{\partial g_{j+1,e}}{\partial x_{i+1}}.
\tag{2.1}
\]

Let

\[
D_{d,e}=\left(\frac{\partial g_{d+r,e}}{\partial x_s}\right)_ {
0\le r\le e-1,\ 1\le s\le e}.
\]

Then \(a_{d,e}=(-1)^e\det D_{d,e}\). Let \(J_s\) be the minor of the first
\(e-1\) rows obtained by deleting column \(s\).

### Proposition 2.1 (Jacobian--Euler identity)

In \(\mathbb Z[x_1,\ldots,x_e]\),

\[
s x_s a_{d,e}=
\sum_{r=0}^{e-1}(-1)^{e+r+s-1}(d+r)g_{d+r,e}M_{r,s},
\tag{2.2}
\]

where \(M_{r,s}\) deletes row \(r\) and column \(s\) from \(D_{d,e}\). On
the zero locus of the first \(e-1\) rows,

\[
s x_s a_{d,e}=(-1)^s(d+e-1)g_{d+e-1,e}J_s.
\tag{2.3}
\]

#### Proof

The polynomial \(g_{n,e}\) is weighted homogeneous of weight \(n\) for
\(\operatorname{wt}(x_s)=s\), hence

\[
\sum_{s=1}^e sx_s\frac{\partial g_{n,e}}{\partial x_s}=ng_{n,e}.
\]

Replace column \(s\) of \(D_{d,e}\) by the weighted sum of all columns.
Multilinearity kills every summand except the original \(s\)-column. Expanding
the resulting determinant along that column and using
\(a_{d,e}=(-1)^e\det D_{d,e}\) proves (2.2). Equation (2.3) follows after
the first \(e-1\) rows vanish. \(\square\)

For \(e=4\), we work on \(x_4=1\) and use \(s=4\). It therefore suffices to
find a common zero of \(g_{d,4},g_{d+1,4},g_{d+2,4}\) at which their anchored
\(3\times3\) Jacobian and \(g_{d+3,4}\) are nonzero.

## 3. Exact rescaling

Write

\[
d=4m+r,\qquad 0\le r\le3.
\]

For each \(n\in\{d,d+1,d+2,d+3\}\), write \(n=4M+q\), where
\(M\in\{m,m+1\}\) and \(0\le q\le3\). Put

\[
C_{M,q}=\frac{(-1)^M}{4M+q+1}
\frac{(5M+q)!}{(4M+q)!M!}
\tag{3.1}
\]

and define the row used by the verifier,

\[
P^{(m)}_{M,q}(X)=
\frac{g_{4M+q,4}(X_1/m,X_2/m,X_3/m,1)}{C_{M,q}}.
\tag{3.2}
\]

For \(\mathbf a=(a_1,a_2,a_3)\), set

\[
u=a_1+a_2+a_3,\quad
w=a_1+2a_2+3a_3,\quad
t=\frac{w-q}{4},\quad
\ell=u-t.
\]

A term occurs precisely when \(w\equiv q\pmod4\) and \(0\le t\le M\).
Its coefficient before \(X_1^{a_1}X_2^{a_2}X_3^{a_3}/(a_1!a_2!a_3!)\)
is exactly

\[
c^{(m)}_{M,q}(\mathbf a)=
\frac{(-1)^\ell}{m^u}
\prod_{i=1}^{\ell}(5M+q+i)
\prod_{i=0}^{t-1}(M-i).
\tag{3.3}
\]

Choose

\[
\rho=5^{1/4}e^{\pi i/4},
\qquad \rho^4=-5.
\]

Since

\[
4\ell-q=3a_1+2a_2+a_3,
\]

the limiting coefficient is

\[
c^\infty_q(\mathbf a)=(-5)^\ell=\rho^q
\rho^{3a_1+2a_2+a_3}.
\tag{3.4}
\]

The exact finite-to-limit ratio is

\[
R^{(m)}_{M,q}(\mathbf a)=
\prod_{i=1}^{\ell}\left(1+\frac{q+i}{5M}\right)
\prod_{i=0}^{t-1}\left(1-\frac{i}{M}\right)
\left(\frac Mm\right)^u.
\tag{3.5}
\]

All analytic and finite bounds below start from (3.3) or (3.5); no fitted
coefficient model is used.

## 4. Fourier limit and simple zeros

Define

\[
H_q(X)=\frac14\sum_{j=0}^3 i^{-qj}
\exp\!\left(\rho^3i^jX_1+\rho^2i^{2j}X_2+\rho i^{3j}X_3\right),
\tag{4.1}
\]

and \(L_q=\rho^qH_q\). The root-of-unity filter shows that \(L_q\) has
the coefficients (3.4), so the four finite rows converge to the corresponding
\(L_q\).

Put

\[
E_j=\exp\!\left(\rho^3i^jX_1+\rho^2i^{2j}X_2+\rho i^{3j}X_3\right).
\]

For residue \(r\), choose \(C_r\) with \(C_r^4=(-1)^{r-1}\) and impose

\[
E_j=C_ri^{(r-1)j}.
\tag{4.2}
\]

The compatibility equation is \(\prod_jE_j=1\). Choose logarithms
\(\Lambda_{j,r}\) summing to zero and set

\[
X^*_{s,r}=\frac1{4\rho^{4-s}}
\sum_{j=0}^3\Lambda_{j,r}i^{-sj},\qquad s=1,2,3.
\tag{4.3}
\]

We use the following exact phase choices, specified by their logarithms divided
by \(\pi i\):

| \(r\) | \((\Lambda_{0,r},\ldots,\Lambda_{3,r})/(\pi i)\) |
|---:|---|
| 0 | \((1/4,-1/4,-3/4,3/4)\) |
| 2 | \((1/4,3/4,-3/4,-1/4)\) |
| 3 | \((-1/2,1/2,-1/2,1/2)\) |

The residue \(r=1\) is treated exactly in Section 7. Fourier inversion gives

\[
H_r(X_r^*)=H_{r+1}(X_r^*)=H_{r+2}(X_r^*)=0,
\qquad H_{r-1}(X_r^*)=C_r\ne0.
\tag{4.4}
\]

Moreover,

\[
\frac{\partial H_q}{\partial X_s}=\rho^{4-s}H_{q-s}.
\tag{4.5}
\]

Thus the first-three-row limit Jacobian is diagonal after accounting for the
row normalizations. The diagonal moduli and the fourth-row modulus are:

| \(r\) | first-three-row diagonal moduli | fourth-row modulus |
|---:|---|---:|
| 0 | \((|\rho|^3,|\rho|^3,|\rho|^3)\) | \(|\rho|^3\) |
| 2 | \((|\rho|^5,|\rho|^5,|\rho|)\) | \(|\rho|\) |
| 3 | \((|\rho|^6,|\rho|^2,|\rho|^2)\) | \(|\rho|^2\) |

Consequently the inverse row-sum norm is at most

\[
|\rho|^{-1}<\frac{67}{100}.
\tag{4.6}
\]

The fourth-row limit modulus is at least

\[
|\rho|>\frac{149}{100}.
\tag{4.7}
\]

A 256-bit Arb evaluation proves

\[
|X^*_{1,r}|\le\frac13,\qquad
|X^*_{2,r}|\le\frac{71}{100},\qquad
|X^*_{3,r}|\le\frac34
\tag{4.8}
\]

for \(r=0,2,3\). These enclosures are reproduced by the uniform verifier.

## 5. Uniform effectivity for \(m\ge5000\)

This section proves an explicit analytic handoff. Let

\[
\Delta^{(m)}_{M,q}=P^{(m)}_{M,q}-L_q.
\]

We bound \(\Delta\) on the closed polydisc

\[
\|X-X_r^*\|_\infty\le\frac14.
\tag{5.1}
\]

By (4.8), its coordinate moduli are at most

\[
\left(\frac7{12},\frac{24}{25},1\right).
\tag{5.2}
\]

### 5.1 Head expansion through degree 50

Let \(\omega=M-m\in\{0,1\}\). Expanding (3.5) gives

\[
R^{(m)}_{M,q}(\mathbf a)
=1+\frac{A_{q,\omega}(\mathbf a)}m+O(m^{-2}),
\tag{5.3}
\]

where

\[
A_{q,\omega}(\mathbf a)=
\frac{q\ell}{5}+\frac{\ell(\ell+1)}{10}
-\frac{t(t-1)}2+\omega u.
\tag{5.4}
\]

The corresponding exponential differential operator can be evaluated by the
four Fourier modes. More explicitly, for mode \(j\), put

\[
z_s=\rho^{4-s}i^{sj}X_s,
\]

\[
p_t=-\frac q4+\sum_{s=1}^3\frac{s}{4}z_s,
\qquad
d_t=\sum_{s=1}^3\frac{s^2}{16}z_s,
\]

\[
p_\ell=\frac q4+\sum_{s=1}^3\frac{4-s}{4}z_s,
\qquad
d_\ell=\sum_{s=1}^3\frac{(4-s)^2}{16}z_s,
\qquad
p_u=\sum_{s=1}^3z_s.
\]

The multiplier corresponding to (5.4) is

\[
\mathcal A_{q,\omega,j}=
\frac q5p_\ell+
\frac{p_\ell^2+d_\ell+p_\ell}{10}
-\frac{p_t^2+d_t-p_t}{2}+\omega p_u,
\tag{5.4a}
\]

and therefore

\[
G_{q,\omega}(X)=\frac{\rho^q}{4}
\sum_{j=0}^3i^{-qj}\mathcal A_{q,\omega,j}E_j.
\tag{5.4b}
\]

At each \(X_r^*\), 256-bit Arb arithmetic proves that the largest first-order
row defect is

\[
1.884955592153876\ldots<2.
\tag{5.5}
\]

On (5.1), an exact rational triangle calculation gives

\[
\|G\|_\infty\le
\frac{51944278023}{204800000}
=253.6341700\ldots<254.
\tag{5.6}
\]

For the second-order remainder, let

\[
A^+=\frac{q\ell}{5}+\frac{\ell(\ell+1)}{10}
+\frac{t(t-1)}2+\omega u.
\]

The elementary product estimate

\[
\left|\prod_j(1+\delta_j)-1-\sum_j\delta_j\right|
\le\frac12\left(\sum_j|\delta_j|\right)^2
\exp\!\left(\sum_j|\delta_j|\right)
\tag{5.7}
\]

together with the difference between \(1/M\) and \(1/m\) gives the exact
coefficient remainder

\[
\left|R^{(m)}_{M,q}-1-\frac{A_{q,\omega}}m\right|
\le \frac{\frac65(A^+)^2/2+A^+}{m^2}
\tag{5.8}
\]

for \(u\le50\) and \(m\ge5000\). Summing (5.8) exactly over all admissible
head monomials gives

\[
K_{2,\mathrm{ball}}<15374,
\qquad
K_{2,\mathrm{centre}}<1105.
\tag{5.9}
\]

The verifier checks the stronger exact rational values
\(15373.3723513\ldots\) and \(1104.3997874\ldots\).

### 5.2 Tail above degree 50

On (5.1), the absolute limit level of total degree \(u\) is bounded by

\[
B_u=\frac{15^u}{u!}.
\tag{5.10}
\]

Indeed, after dropping the congruence restriction, the multinomial theorem
bounds the level by

\[
\frac{|\rho|^q}{u!}
\left(|\rho|^3|X_1|+|\rho|^2|X_2|+|\rho||X_3|\right)^u.
\]

The bounds \(|\rho|<3/2\) and (5.2) make this smaller than (5.10) for
\(u\ge51\). For a finite coefficient, the falling-factor product in (3.5)
is at most one, while

\[
\prod_{i=1}^{\ell}\left(1+\frac{q+i}{5M}\right)
\left(\frac Mm\right)^u
\le
\exp\!\left(\frac{(u+3)^2}{2m}\right).
\]

This proves the finite majorant used below.

For \(u\ge51\), the first-order multiplier in (5.4) is at most \(u^2\).
Indeed,

\[
A^+\le \frac{61}{160}u^2+\frac{17}{10}u\le u^2.
\tag{5.11}
\]

Here we used \(q\le3\), \(\ell\le u\), \(t\le3u/4\) and
\(\omega\le1\). The last inequality already holds for \(u\ge3\).

For \(u\le m\), the finite level is bounded by

\[
B_u\exp\!\left(\frac{(u+3)^2}{2m}\right).
\tag{5.12}
\]

The verifier sums the finite, limit and \(m^{-1}\)-scaled first-order levels
exactly for \(51\le u\le400\). Starting at \(u=401\), the limit and
first-order successive ratios are bounded by \(1/20\); the same is true for
the finite majorant while \(u\le m\). Its successive ratio is

\[
\frac{15}{u+1}
\exp\!\left(\frac{2u+7}{2m}\right),
\]

which decreases on this range. The three first-ratio inequalities are checked
in exact rational arithmetic, with a rational Taylor upper bound for the one
exponential. For \(u>m\), use \(u!\ge(u/e)^u\), \(M\le m+1\) and
\(q\le3\). On the polydisc (5.1), put
\(R_X=\max_s|X_s|\); (5.2) gives \(R_X\le1\), hence
\(3R_X\le3\). For every \(m\ge5000\) and \(u\ge5001\), the direct finite
level is below \((13/1000)^u\): using \(e<3\), its level base is strictly
smaller than

\[
\frac{45}{u}+\frac9m+\frac{72}{mu}<\frac{13}{1000}.
\]

Consequently the complete omitted contribution is

\[
T=2.482176974351622\ldots\times10^{-6}
<\frac1{400000}.
\tag{5.13}
\]

The exact fraction for \(T\) is recomputed by the verifier; its canonical
numerator/denominator text is bound into the receipt by SHA-256.

### 5.3 Quantitative Newton lemma

We use the following standard form of the Newton--Kantorovich theorem.

### Lemma 5.1

Let \(F\) be holomorphic on a convex neighbourhood of \(x_0\) in
\(\mathbb C^n\). Suppose \(DF(x_0)\) is invertible and

\[
\|DF(x_0)^{-1}\|\le\beta,
\qquad
\|F(x_0)\|\le\delta,
\]

and suppose \(DF\) is Lipschitz with constant \(L\) on the ball of radius
\(2\eta\), where \(\eta=\beta\delta\). If

\[
h=\beta L\eta\le\frac12,
\]

then \(F\) has a zero in that ball. The zero lies within

\[
t_* = \frac{1-\sqrt{1-2h}}{\beta L}\le2\eta
\]

of \(x_0\). If \(2\beta L\eta<1\), its Jacobian is invertible.

#### Proof

This is the Newton--Kantorovich majorant theorem applied to the scalar
majorant \(\beta\delta-t+(\beta L/2)t^2\). Its smaller root is \(t_*\).
The inequality \(t_*\le2\eta\) follows from
\(1-\sqrt{1-2h}\le2h\). Finally,

\[
\|DF(x_0)^{-1}(DF(x)-DF(x_0))\|
\le2\beta L\eta<1
\]

on the root enclosure, so Neumann inversion proves nonsingularity. \(\square\)

### 5.4 Cauchy and Newton constants

Equations (5.5)--(5.13) give, for every row and every \(m\ge5000\),

\[
\epsilon_m:=\sup_{(5.1)}|\Delta^{(m)}_{M,q}|
\le\frac{254}{m}+\frac{15374}{m^2}+\frac1{400000},
\tag{5.14}
\]

and at the first-three-row centre,

\[
\delta_m:=\max|P^{(m)}_{M,q}(X_r^*)|
\le\frac2m+\frac{1105}{m^2}+\frac1{400000}.
\tag{5.15}
\]

At \(m=5000\),

\[
\epsilon_m\le0.05141746,
\qquad
\delta_m\le0.0004467.
\tag{5.16}
\]

The first-derivative Cauchy row-sum coefficient at the centre is \(12\), for
which we use \(15\). On the inner ball of radius \(1/100\), the distance to
the boundary of (5.1) is \(6/25\). The second-derivative Cauchy row-sum
coefficient is

\[
\frac{12}{(6/25)^2}=\frac{625}{3}<300.
\tag{5.17}
\]

The limit Hessian row sum is at most \(188.468<258\), and the fourth-row
gradient is at most \(27.095<37\). All four comparisons are derived and
checked in the executable receipt.

Let \(\beta_0=67/100\). Neumann inversion gives

\[
\beta_m\le\frac{\beta_0}{1-15\beta_0\epsilon_m}.
\tag{5.18}
\]

Let

\[
L_m=258+300\epsilon_m,
\quad
\eta_m=\beta_m\delta_m,
\quad
h_m=\beta_mL_m\eta_m.
\tag{5.19}
\]

At the endpoint \(m=5000\), exact rational evaluation gives

| predicate | certified bound |
|---|---:|
| \(15\beta_0\epsilon_m\) | \(0.516745473<1\) |
| \(\beta_m\) | \(1.386432952\) |
| \(L_m\) | \(273.425238\) |
| \(h_m\) | \(0.234775241<1/2\) |
| \(2\eta_m\) | \(0.001238640<1/100\) |
| fourth-row margin | \(1.392752889>0\) |
| transported Jacobian margin | \(0.530449518>0\) |

The Newton--Kantorovich theorem therefore supplies a zero of the first three
finite rows within \(2\eta_m\) of \(X_r^*\). The last two margins show that
the fourth row and the first-three-row Jacobian remain nonzero at that zero.
Every defect expression decreases with \(m\), so the endpoint proves all
\(m\ge5000\).

### Theorem 5.2 (uniform analytic branch)

For every \(m\ge5000\) and \(r\in\{0,2,3\}\), the first three rows associated
with \(d=4m+r\) have a common zero at which their anchored Jacobian and the
fourth row are nonzero.

## 6. Finite interval certificates

It remains to cover \(5\le m<5000\) in residues \(0,2,3\).

### 6.1 Exact coefficient evaluation and rigorous tails

For \(m\le30\), the checker evaluates every coefficient in (3.3). For
\(m\ge31\), it evaluates all monomials of total degree at most \(50\). Let
\(R=4/5\), let \(U=51\), and put

\[
E_{k,u}=
\frac{(5m+8+u)^u(3R)^u u^k}{m^u u!R^k},
\qquad k=0,1,2.
\tag{6.1}
\]

This bounds respectively the omitted value, gradient row sum and Hessian row
sum at level \(u\). Support gives \(u\le d+3\le4m+6\), so

\[
\frac{u}{5m+8+u}<\frac12.
\]

Hence, with an Arb upper bound for \(e^{1/2}\), the first omitted ratio is

\[
q_{k,U}=
\frac{3R(5m+9+U)e^{1/2}}{m(U+1)}
\left(\frac{U+1}{U}\right)^k<1.
\tag{6.2}
\]

The right side decreases at later levels, so the complete tail is bounded by

\[
\frac{E_{k,U}}{1-q_{k,U}}.
\tag{6.3}
\]

For completeness, after removing constants the \(u\)-dependent factors in
the ratio majorant are respectively

\[
\frac{5m+9+u}{u+1},\qquad
\frac{5m+9+u}{u},\qquad
\frac{(5m+9+u)(u+1)}{u^2}
\]

for \(k=0,1,2\). Each is decreasing, which justifies using the first omitted
ratio for the complete supported tail.

### 6.2 Interval-Newton gate

Proposed centres are exact rational decimal points. For \(5\le m\le16\),
they are stored explicitly; for \(m\ge17\), the checker uses one fixed formula

\[
X_{m,r}^{\mathrm{loc}}=X_r^*+\frac{Y_r}{m},
\tag{6.4}
\]

where the decimal rational vectors \(Y_r\) are part of the hashed source.
Their numerical origin is irrelevant to acceptance.

The checker evaluates each truncated row, all first derivatives and all second
derivatives in 128-bit complex Arb arithmetic. The derivative box is the
coordinate rectangle of real and imaginary radius \(1/100\). Its maximum
complex displacement is therefore \(\sqrt2/100\), and the checker proves that
the whole rectangle lies in \(|X_s|<4/5\), the domain used by (6.1).

Let \(J_0\) be the truncated centre Jacobian and let
\(\beta_{\rm tr}=\|J_0^{-1}\|_\infty\). If \(T_1\) is the gradient-tail
bound, Neumann inversion gives

\[
\beta=\frac{\beta_{\rm tr}}{1-\beta_{\rm tr}T_1}.
\tag{6.5}
\]

Let \(\delta\) be the first-three-row residual including \(T_0\), and let
\(L\) be the Hessian row-sum bound on the box including \(T_2\). Each case is
accepted only if the explicit outward-rounded endpoints prove

\[
h=\beta L(\beta\delta)<\frac12,
\qquad
2\beta\delta<\frac1{100},
\tag{6.6}
\]

and if interval transport proves both the fourth row and the Jacobian nonzero
throughout the resulting root enclosure.

### 6.3 Coverage and worst case

The ledger contains exactly

\[
4995\times3=14985
\]

records, ordered lexicographically by \(m=5,\ldots,4999\) and
\(r=0,2,3\). Thirty-six cases use stored centres and \(14949\) use (6.4).
The independent structural auditor reports the following worst endpoints:

| quantity | certified endpoint | case |
|---|---:|---:|
| maximum \(h\) | \(0.465782636<1/2\) | \(m=17,r=2\) |
| maximum root radius | \(0.006955535<1/100\) | \(m=17,r=2\) |
| minimum fourth-row margin | \(1.475688755>0\) | \(m=17,r=2\) |
| minimum Jacobian margin | \(0.068434729>0\) | \(m=17,r=2\) |

The normal and optimized runs produce byte-identical ledgers with SHA-256

```text
a106c2df4bf6b771b0ee3245d6e0f5c95d1a1cb5485e9b03e93d942f77ccc3a1
```

The independent audit receipt has SHA-256

```text
d4702c869d6d735a3736ece0a19c61232e667b8dca6ba0c7277e1b5cd89923b6
```

### Theorem 6.1 (finite bridge)

For every \(5\le m<5000\) and \(r\in\{0,2,3\}\), the first three rows
associated with \(d=4m+r\) have a common zero at which their anchored Jacobian
and the fourth row are nonzero.

## 7. Exact residue \(r=1\)

Let \(d=4m+1\) and set \(X=(0,0,0)\). Congruence excludes a constant term
from rows \(q=1,2,3\), so the first three rows vanish. Their only linear
monomials are respectively \(X_1,X_2,X_3\), and their Jacobian is diagonal:

\[
\operatorname{diag}\left(
-\frac{5m+2}{m},
-\frac{5m+3}{m},
-\frac{5m+4}{m}
\right).
\tag{7.1}
\]

Its determinant is nonzero for every \(m\ge1\). The wrapped fourth row has
\(q=0,M=m+1\) and constant term exactly \(1\). Thus this residue class is
algebraic and needs no interval computation. This specialization recovers the
\(e=4\), \(d-1\equiv0\pmod4\) case of Edo's divisibility theorem [4].

## 8. Proof of Theorem A

Lewis--Perry--Straub prove (1.4) for \(2\le d<20\). For \(d\ge20\), write
\(d=4m+r\), so \(m\ge5\). Section 7 proves the required specialization when
\(r=1\). Theorem 6.1 proves it for \(r=0,2,3\) and \(m<5000\), while
Theorem 5.2 proves it for \(m\ge5000\).

Unscaling gives

\[
P=(X_1/m,X_2/m,X_3/m,1).
\]

All row-normalization factors \(C_{M,q}\) are nonzero. Coordinate scaling and
row normalization multiply the anchored Jacobian by nonzero factors, so the
certified normalized determinant is nonzero exactly when the anchored minor
in Proposition 2.1 is nonzero. Proposition 2.1 then supplies the full
determinant condition in Published input 1.1. Applying the Lewis--Perry--Straub
implication proves (1.4). \(\square\)

## 9. Reproducibility and trust boundary

The proof package pins Python 3.14.6, python-flint 0.8.0 and the Arb precision
used by each checker. Its proof-critical parts are:

1. `e4_eventual_envelope.py`, which recomputes the exact head/tail bounds,
   the 256-bit Fourier enclosures and the threshold inequalities;
2. `e4_certify_prototype.py`, the coefficient/evaluation/interval-Newton core;
3. `e4_finite_bridge.py`, the ordered finite producer;
4. `verify_finite_ledger.py`, the separate structural and endpoint auditor;
5. `verify_normalization.py`, which independently reconstructs 78,144
   admissible normalized coefficients from the multinomial definition and
   checks 1,446,940 rejected support triples;
6. the exact locator file; and
7. the normal and optimized finite ledgers and receipts.

The proof-critical frozen digests are listed in four 16-character groups;
spaces are typographical only:

- eventual receipt:
  `747cd56f4a297774 0ac0786055d2cdf0 7ed9e7b89521ed91 0ad736d6eaf5daa9`;
- normalization receipt:
  `b82f1709aeee6e1f cc58a8091125c11d cb3ff5b0b9095fc9 85c2bf516a62d47e`;
- finite v2 ledger:
  `a106c2df4bf6b771 b0ee3245d6e0f5c9 5d1a1cb5485e9b03 e93d942f77ccc3a1`;
- finite v2 production receipt:
  `4e14868e1531fb85 509dc017533b9261 21c130d31ef1eb1b 41195d5cfddb5b54`;
- independent ledger audit:
  `d4702c869d6d735a 3736ece0a19c6123 2e667b8dca6ba0c7 277e1b5cd89923b6`.

The decimal locators are not trusted as solutions. The finite proof depends on
the interval gates in (6.6), exact coefficient formulas, and rigorous omitted
tails. Likewise, the finite ledger is not independent reproduction: both runs
use the same source and arithmetic library. Its evidential role is exhaustive
replay and optimization-sensitivity detection.

Arb midpoint-radius arithmetic is described in [3]. A specialist verifier can
replace the implementation while preserving the mathematical certificate
conditions in Sections 5 and 6.

## 10. Limitations and claim boundary

- The finite range is a computer-assisted proof, not a hand enumeration.
- The implication from the coefficient specialization to the stratum
  containment is the published theorem of Lewis--Perry--Straub; it is not
  re-formalized in a proof assistant here.
- The package has been internally replayed, but not independently reproduced
  or externally peer reviewed.
- The search found no earlier all-degree \(e=4\) proof, but this does not
  establish priority.
- The theorem concerns plane polynomial automorphism strata. It neither proves
  nor refutes the two-dimensional Jacobian conjecture, the quartic Hessian
  conjecture in dimension four, or any other open Jacobian/Hessian case.

## References

[1] D. Lewis, K. Perry and A. Straub, “An algorithmic approach to the
Polydegree Conjecture for plane polynomial automorphisms,” *Journal of Pure
and Applied Algebra* **223** (2019), 5346--5359.
<https://doi.org/10.1016/j.jpaa.2019.04.002>.

[2] K. A. Perry, *Polydegree properties of polynomial automorphisms*, PhD
dissertation, The University of Alabama, 2016.
<https://ir.ua.edu/handle/123456789/2587>.

[3] F. Johansson, “Arb: efficient arbitrary-precision midpoint-radius interval
arithmetic,” *IEEE Transactions on Computers* **66** (2017), 1281--1292.
<https://doi.org/10.1109/TC.2017.2690633>.

[4] E. Edo, “Some families of polynomial automorphisms II,” *Acta
Mathematica Vietnamica* **32** (2007), 155--168.

## Declarations

**Data and code availability.** The exact frozen successor archive, manifest,
source files, ledgers and receipts accompany the candidate release.

**Author responsibility.** The submitting author is responsible for the
mathematical claims, computational evidence and source selection.

**Funding.** No dedicated external funding is declared.

**Competing interests.** No competing interests are declared.

**AI-use disclosure.** AI systems contributed to source discovery, proof
exploration, software construction, replay, review and drafting. The author
must inspect and approve the final submission. Internal AI review is not
external peer review.
