# P7b manuscript--Lean concordance

## Source bound

This concordance compares the Lean package with:

```text
HC4JC2_ACTIONS_1_TO_7_ACCEPTED_2026-08-23/submission/
  built-round4-author/bordered-jacobian/manuscript.md
```

The frozen parent submission has manifest SHA-256
`f28a6bafbe34c08aa16ad7f18d3f68550b271af43a1ff83b68c1da3cbf8d0f64`.
The successor does not mutate that submission.

## Exact object map

| Manuscript object | Lean object | Concordance |
|---|---|---|
| Ring `R` | `{R : Type*} [CommRing R]` | Exact; final results allow zero divisors and all characteristics. |
| Degrees `r,s >= 0` | `(r s : Nat)` | Exact, including `r=s=0`. |
| `A=sum a_i X^i` | `polyOfCoeffs r a` | Exact; `polyOfCoeffs_coeff` proves the coefficient convention. |
| `B=sum b_j X^j` | `polyOfCoeffs s b` | Exact. |
| Source order `a_0,...,a_r,b_0,...,b_s` | `Fin (r+s+2)` in `mulJac` | Exact; `coeffOrderEquiv` proves equivalence with the disjoint-sum indexing used in the convolution proof. |
| `M_{k,a_i}=b_{k-i}`, `M_{k,b_j}=a_{k-j}` | `mulJac r s a b` | Exact, with `coeffExt` equal to zero out of range. |
| `kappa=(a_0,...,a_r,-b_0,...,-b_s)` | `kappa r s a b` | Exact. |
| `R_{r,s}(A,B)=Res(B,A)` | `resultantBA r s a b` | Exact argument order and increasing-power coefficient convention. |
| Append row `v` | `border M v` | Exact; `v` is the last row. |
| Delete column `k` | `M.submatrix id k.succAbove` | Exact order-preserving deletion. |

## Theorem map

### Kernel identity

Manuscript Lemma 2.1 states `M kappa = 0`.
`mulJac_mulVec_kappa` proves the same identity over every commutative ring.
The proof is first carried out with sum-type column indices and then transported
to the manuscript's single ordered index.

### Anchored minor

Manuscript Lemma 3.1 gives

\[
\det M_{\widehat{a_r}}
=(-1)^{rs}\operatorname{Res}(B,A)a_r.
\]

`det_anchorMinor` proves exactly

```text
det(anchorMinor r s a b)
  = (-1)^(r*s) * resultantBA r s a b * a (Fin.last r).
```

The preceding theorem `anchorCore_eq_sylvester` identifies the core matrix
entrywise with `Polynomial.sylvester`; the proof does not treat positive
degrees as an implicit precondition.

### Universal maximal minors

Manuscript equation (4.2), extended globally by Theorem 5.1, is

\[
(-1)^k\det M_{\widehat k}
=(-1)^{r(s+1)}\operatorname{Res}(B,A)\kappa_k.
\]

`universal_cofactorVec` first proves this in
`MvPolynomial (Fin (r+s+2)) Z`.  Its only cancellation uses
`MvPolynomial.X_ne_zero` for the universal `a_r` variable in this integral
domain.  `cofactorVec_mulJac` then obtains the identity over an arbitrary
commutative ring solely by applying the specialization homomorphism.
`det_mulJac_submatrix` expands the `cofactorVec` definition and is literally
the displayed manuscript formula.

### Bordered determinant

Manuscript equation (4.1), extended globally by Theorem 5.1, is

\[
\det\operatorname{border}(M,v)
=(-1)^{s(r+1)+1}\operatorname{Res}(B,A)\sum_k\kappa_kv_k.
\]

`det_bordered` proves

```text
det(border (mulJac r s a b) v)
  = (-1)^(s*(r+1)+1) * resultantBA r s a b
      * sum i, v i * kappa r s a b i.
```

The factor order inside the finite sum is reversed, but is equal because `R`
is commutative.  The exponent is textually identical.

## Relationship to the parent proof

The parent manuscript's chart proof assumes an integral domain and `a_r != 0`,
then Theorem 5.1 removes those hypotheses by universal specialization.  The
Lean package formalizes that strategy but strengthens its abstract bridge:
`kernel_cofactor_proportional` proves the cross-multiplied cofactor relation

\[
x_p C_k=x_k C_p
\]

over any commutative ring, using a selector border and the adjugate identity.
Consequently no division, generic-rank assumption, or cancellation occurs in
the arbitrary-ring part.

The Lean universal ring contains only the coefficient variables, not border
variables.  This is equivalent to the parent Theorem 5.1 because the universal
maximal-minor formula is specialized first and `det_border` then supplies an
arbitrary row.  It is not a weakening of either (4.1) or (4.2).

## Tests and limitations

- `det_bordered_zero_zero` checks the `2 x 2` matrix and sign at `r=s=0` by
  definitional reduction.
- `zmod_six_one_one_control` checks a nonzero concrete determinant over
  `ZMod 6`, so the executable test is not confined to domains or fields.
- The package proves only the coefficient-multiplication identities above.
  It makes no claim about invertibility of polynomial maps, `JC_2`, `HC_4`, or
  novelty of the classical resultant ingredients.
- A successful replay is formal verification relative to the pinned Lean
  kernel and Mathlib dependency, not independent peer review or a priority
  determination.
