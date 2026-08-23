# Final specialist priority and significance audit

**Candidate successor:** HC4JC2 Actions 1--7 extension  
**Audit date:** 23 August 2026  
**Scope:** P7a and P4/P5; current public scholarly record  
**Authority:** internal evidence audit, not external peer review

## Executive verdict

The successor contains one result that, if the manuscript and certificates
survive specialist external scrutiny, is capable of being a leading
contribution in its narrow area: the effective proof

\[
\mathcal G_{(d+4)}\subset\overline{\mathcal G_{(d,5)}}
\qquad(d\ge2).
\]

It completes the full `e=4` Polydegree column beyond the published
Lewis--Perry--Straub range. The advance is an infinite theorem, not merely a
larger computation: an explicit Fourier-limit branch and rigorous eventual
envelope reduce the problem to a finite interval certificate. The public
record search found no earlier all-degree or effective-e=4 theorem. This makes
the work submission-worthy and plausibly highly original and significant,
but does not establish priority or justify “first” or “world-leading” before
external specialists have assessed it.

The boundary-norm paper is also formally presentable. Its contribution is
smaller but clean: a cover-degree-free norm bound, an equivalence reducing
all homogeneous graph degrees to finitely many pencil systems, a conditional
transfer theorem, and a sharp counterexample to weakening the pencil method.
It should not be sold as new global geometry for plane Keller maps. Orevkov
and Borisov already provide close or stronger global boundary results.

The Lean P7b development is a rigorous and useful formal-verification
contribution: it proves the universal bordered-Jacobian identity and its
specialization to arbitrary commutative rings, including a zero-divisor test.
Its originality lies in the end-to-end formal package, not in claiming the
classical adjugate/resultant identity itself as new.

None of these results proves or materially reduces the two-dimensional
Jacobian conjecture or the quartic Hessian conjecture in dimension four.

## Claim-level decisions

| Item | Originality | Significance | Rigour at candidate stage | Release decision |
|---|---|---|---|---|
| Full effective `e=4` Polydegree column | High and plausibly new on bounded search | High within plane polynomial-automorphism strata | Computer-assisted proof with exact formulas, Arb enclosures, exhaustive ledger, independent structural auditor | **Prepare for specialist submission** |
| P7b arbitrary-ring Lean formalization | High implementation originality; classical identity priority not claimed | Moderate to high as reusable assurance infrastructure | Kernel-checked Lean build, pinned Mathlib, no `sorry`/custom axioms, specialization tests | **Release as companion formal artifact** |
| Finite-pencil boundary-norm transfer | Plausibly new on bounded search | Moderate; reusable when `BN` geometry is available | Hand proof plus exact algebra checker; six-sheet application depends on companion geometry | **Prepare as a separate short paper or companion note** |
| Broad predecessor P4 geometry | Not safely new | Potentially important but substantially anticipated | Internal manuscript may remain useful exposition | **Do not submit as an originality claim** |
| JC2/HC4 solution claims | None established | Would be exceptional if true, but unsupported here | Open obligations remain | **Prohibited** |

## Nearest sources and exact separations

1. Perry's 2016 dissertation reports, for `2 <= d <= 45`, a nonempty
   intersection involving `G_(d+3)` and `closure(G_(d,4))`. It is not the
   full containment proved here.
2. Lewis--Perry--Straub, Theorem 13(b), prove the relevant e=4 full
   containment only for `2 <= d < 20`. Their Theorem 4 is the published
   specialization implication used by the successor.
3. Furter's 2009 fixed-multidegree paper proves smoothness/local closedness
   and related closure structure, but not the all-`d` containment above.
4. Orevkov and Borisov substantially anticipate broad P4 boundary geometry.
   The successor therefore isolates only the algebraic transfer mechanism.
5. Kistner--Shaska Proposition 3.21 gives a direct negative-exponent
   non-descent argument. It does not give the graph-section field-norm theorem
   or finite-pencil equivalence.

Full queries, versions, source hashes and residual audit limits appear in
`SEARCH_LOG.md` and `SOURCE_MATRIX.md`.

## Safe external wording

The following language is supported if the exact package passes the final
review gate:

> We prove the e=4 Polydegree containment for every d >= 2. The proof combines
> the published Lewis--Perry--Straub specialization criterion with an explicit
> Fourier branch, a rigorous eventual estimate, and a finite Arb certificate.

> We also prove a conditional boundary-norm transfer theorem reducing all
> graph degrees to a finite pencil test, and provide a Lean formalization of
> the universal bordered-Jacobian identity through arbitrary commutative-ring
> specialization.

The following wording is not supported: “solution of JC2,” “solution of HC4,”
“first proof,” “world-leading,” “independently reproduced,” “peer reviewed,”
or “formally verified” when referring to the analytic and geometric papers.

## Audit limitations

The search covered exact and structural aliases in arXiv, Crossref, OpenAlex,
publisher and author sources, together with inspected backward/forward chains.
It cannot exclude unpublished work, private circulation, indexing failures or
future priority disputes. Very recent cited arXiv papers are unrefereed. The
final mathematical verdict must come from independent specialists who replay
the exact frozen bytes.
