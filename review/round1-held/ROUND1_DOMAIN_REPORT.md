# Round 1 Domain Mathematics report

**Submission manifest:** `299a0326b8dd7d30d2dae9619745f57c7452608814e0fe615e22d5540388cfa2`  
**Role:** plane polynomial automorphisms, elimination theory and Keller geometry reviewer  
**Independence:** read-only review of submission and cited source snapshots; no other role report consulted  
**Decision:** **ACCEPT**  
**Issue inventory:** Critical 0; Major 0; Minor 0; Observations 4

## Polydegree theorem

The published bridge is represented accurately.  Lewis--Perry--Straub
Theorem 4 gives the required specialization implication, and Theorem 13(b)
gives the full containment for exactly `2 <= d < 20`.  Perry's dissertation
Theorem 3.0.1 instead gives a nonempty intersection involving
`G_(d+3)` and `closure(G_(d,4))` through degree 45; the manuscript correctly
does not use it as the desired containment.

Proposition 2.1 (paper pp. 2--3) is algebraically sound.  Weighted Euler
homogeneity supplies the replacement column; determinant multilinearity
kills every duplicated-column term; and Laplace expansion yields the displayed
sign.  On the first-three-row zero locus at `e=4`, nonvanishing of the
anchored minor and fourth row indeed supplies the full determinant condition.

The coefficient normalization in Section 3 follows from the multinomial
definition with the support congruence and wrapped `(M,q)` convention.  The
root-of-unity filter in Section 4 produces the stated limiting rows.  The
phase choices annihilate three consecutive Fourier components, derivative
shifts make the limiting Jacobian diagonal, and the fourth component is
nonzero.  Section 5 then gives explicit perturbation bounds rather than a
bare convergence argument.  The finite and analytic branches meet exactly at
`m=5000`; Section 7 treats the missing residue class at the origin; and the
unscaling argument on p. 12 preserves all nonvanishing conditions.  The proof
therefore covers every integer `d >= 2` without a residue or endpoint gap.

## Bordered-Jacobian formal theorem

The mathematical architecture is valid.  For an `n x (n+1)` matrix, the
signed cofactor vector is in the kernel, and the selector-border/adjugate
argument gives the cross-multiplied proportionality without division.  The
anchored multiplication-Jacobian minor is a Sylvester determinant with the
stated `Res(B,A)` convention.  Cancelling `a_r` only in the universal
integer polynomial domain and then mapping to an arbitrary commutative ring
is the correct way to obtain the zero-divisor-general identity.  The border
sign follows by Laplace expansion.  The Lean theorem map and concrete
`r=s=0`, `ZMod 6` tests address the likely sign/scope failure modes.

## Boundary-norm theorem

Lemma 2.1 (paper p. 2) is correct.  A nonconstant polynomial `s(t)` makes
`k[t]` integral over `k[s]`; hence the norm of the polynomial `h(t)` lies in
the integrally closed ring `k[s]`.  Monicity in `ell` gives
`[K:k(s)]=n` and `N(ell)=(-1)^n F(s,0)`.  The tower norm then forces
`F(s,0)^e` to divide a power of `s`; unique factorization yields a monomial,
and the exponent comparison cancels the cover degree `e`.

Lemma 3.1 (p. 3) uses algebraic closure to factor the top form into linear
forms; UFD factorization then proves both directions of the finite-pencil
equivalence.  In Theorem 5.1 (p. 4), multiplying factor constant terms gives
`Q <= kappa(m+1)`, while the explicit `s^(kappa m)` factor gives
`Q >= kappa m`; the residual exponent is therefore between zero and
`kappa`, exactly the range ruled out by the pencil hypothesis.

For the six-sheet seed (p. 5), the cubic coefficient of `B` forces its pencil
coefficient to vanish in any monomial of degree at most two; the remaining
linear `A` has nonzero constant and linear terms.  The exact resultant and
pencil checker agree.  The article correctly treats the full boundary package
as a companion theorem, not as a consequence of the small pencil calculation.
The `A=1,B=s` example is a sharp counterexample to weakening this algebraic
method, and is not misrepresented as a Keller counterexample.

## Priority and scope

The search record identifies the closest published results and avoids a new
claim for Orevkov/Borisov boundary geometry.  No reviewed theorem is stated as
a JC2 or HC4 advance.  The all-`d` Polydegree theorem is mathematically
substantial and plausibly new on the documented search, but the manuscript
appropriately defers priority to external specialists.

## Issues

No Critical, Major, or Minor issues are identified.

## Observations (non-blocking, not defects)

1. P7a should receive a referee who will rederive the Section 5 tail and
   monotonicity estimates line by line; these are the densest hand-proof
   obligations despite the executable receipt.
2. The formal theorem is useful independently of its original chart context
   and can be released as a reusable Mathlib-adjacent development.
3. The boundary transfer theorem may become more significant if further
   graded seeds can be shown to satisfy `BN(kappa;A,B)`.
4. The package's separate-paper strategy is mathematically preferable: none
   of the three theorems needs an unsupported JC2/HC4 narrative to be valuable.

## Final recommendation

Accept for specialist submission as candidate research, with the existing
external-review and priority qualifications retained verbatim.
