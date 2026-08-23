# Research-question brief

## Programme question

Starting from the exact accepted HC4JC2 parent, can one produce a successor
release that adds a rigorously verified formal theorem and at least one genuine
mathematical extension, while determining current priority accurately and
without making success depend on solving JC2 or unrestricted HC4?

## Primary research questions

### RQ-P7a: effective Fourier persistence

Can the qualitative compact-`C^1` argument for the `e=4` Polydegree column be
made effective by deriving exact or interval-certified bounds for:

1. the finite-to-limit coefficient defect and its first derivatives on an
   explicit polydisc or norm ball;
2. variation of the limiting Jacobian and a norm bound for its inverse;
3. the residual of each finite row at a chosen limit zero;
4. nonvanishing of the fourth row throughout the validated neighbourhood; and
5. exact finite coverage of every degree between the published `2 <= d < 20`
   range and the resulting analytic threshold?

The preferred outcome is an explicit `D_0(4)` and full finite stitch. A valid
fallback is a nontrivial effective partial theorem together with a
machine-checkable minimal-obstruction dossier that identifies the first bound
or finite case that cannot be closed.

### RQ-P7b: universal formalization

Can the signed all-maximal-minor and arbitrary-border identity for binary-form
multiplication be formalized afresh in Lean 4/Mathlib, with:

1. audited definitions matching the accepted coefficient and sign conventions;
2. a theorem in a universal integer-coefficient polynomial ring;
3. a proved evaluation/specialization theorem to every commutative ring;
4. boundary degrees `r=0` or `s=0` included;
5. no `sorry`, `admit`, unsafe axiom, or unreported statement weakening; and
6. an axiom and source-to-statement audit that distinguishes kernel/minor,
   resultant, border, and specialization claims?

### RQ-P4/P5: transfer of the boundary-norm obstruction

Which hypotheses on an étale seed, chart boundary, dicritical cover, and graph
equation are sufficient for the covering degree to cancel in the norm argument?
Can those hypotheses be verified for a broader class than the accepted fixed
six-sheet triangular family, or can one prove sharp counterexamples/no-go
results showing exactly where transfer fails?

## Secondary questions

1. Does equality in the P4 sheet inequality `mu_w >= e_alpha a_c` force all
   local sheets supported at `w` to come from the selected boundary branch?
2. Can a finite global sheet partition convert the local inequality into a
   usable classification for low-degree seeds?
3. Is P5's monomial conclusion a special case of a general UFD norm-support
   lemma independent of the Kistner–Shaska formula?
4. Which terms and aliases in the Polydegree, dicritical/valuation,
   compactification, resultant-minor, and bordered-determinant literatures must
   be searched before any novelty statement is permitted?

## Scope

### In scope

- the accepted P7a, P7b, P4 and P5 statements and their exact parent artifacts;
- peer-reviewed papers, authoritative preprints, books and primary formal
  library sources needed for claim and priority verification;
- exact symbolic algebra, interval arithmetic and proof-assistant checking;
- new theorems, counterexamples and negative-result dossiers with explicit
  hypotheses;
- article-quality manuscripts and reproducibility packages.

### Out of scope as completion requirements

- solving or refuting JC2;
- solving unrestricted HC4;
- claiming global priority from a non-exhaustive search;
- treating numerical convergence, exact finite replay or an internal review as
  proof of an unrestricted theorem;
- repairing the accepted parent in place.

## FINER assessment

| Criterion | Score (1–5) | Reason |
|---|---:|---|
| Feasible | 4 | P7b formalization and an abstract P5 norm lemma are bounded; P7a has an explicit negative-result fallback |
| Interesting | 5 | P7a could close a published Polydegree column; P4/P5 bear directly on finite-sheet architectures |
| Novel | 4 | Plausible but must remain provisional until the specialist search is complete |
| Ethical | 5 | No human/animal data; attribution, AI disclosure and claim boundaries are explicit |
| Relevant | 5 | Directly extends the strongest accepted outputs and improves external auditability |

**Total:** 23/25. The programme is suitable for full investigation, with
effectivity and priority treated as open rather than presumed.

