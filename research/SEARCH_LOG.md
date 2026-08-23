# Specialist search log

**Project:** HC4JC2 successor  
**Protocol:** `SEARCH_PROTOCOL.md`  
**Status:** claim-level audit closed on 2026-08-23; absence findings remain
bounded public-record findings, not proofs of priority

## Frozen primary-source bytes

Downloaded from the authoritative repository, author, or arXiv URL on
2026-08-23 at 15:28:49 UTC.

| Local file | Source URL | SHA-256 |
|---|---|---|
| `sources/perry_2016_dissertation.pdf` | <https://ir-api.ua.edu/api/core/bitstreams/e9dc277b-9b56-47c9-8c00-bd4de9bab2fc/content> | `7c32c5dfc29111d07fff196ba0a26ecd905b957676e7d1a700a03c24150c6f15` |
| `sources/lewis_perry_straub_2019.pdf` | <https://arminstraub.com/downloads/pub/polydegree-conjecture.pdf> | `e49949a5ff90d81d3e4483c8c93cf45b8009a9c6bb62d837053b3575d3279c1c` |
| `sources/orevkov_1987.pdf` | <https://www.math.univ-toulouse.fr/~orevkov/jc86.pdf> | `f80d4a7d7e04987ce7dece58f33cff20ea9210183ca3ffd4488f39a2147532db` |
| `sources/borisov_stein.pdf` | <https://people.math.binghamton.edu/borisov/documents/papers/ampleramification.pdf> | `dc63edc476dcd8f2b9b35329bc3bbb415bfb15496fb8fa384ff22cfae24271f4` |
| `sources/kistner_shaska_2608.02863v1.pdf` | <https://arxiv.org/pdf/2608.02863v1> | `3cd7e239d8b01c79239789a97c26e466208d9cb216d9773574562c468c915a2e` |
| `sources/shaska_2607.20210v1.pdf` | <https://arxiv.org/pdf/2607.20210v1> | `e35686af71d078e509142331e017b7168ace885c88d400e7bc8b68e0d25fc12f` |

## Query register

### 2026-08-23T15:29:21Z — P7a exact-title and alias pass

1. **Crossref REST:** `query.title=Polydegree Conjecture`, `rows=20`.
   The meaningful exact-topic record was Lewis--Perry--Straub, DOI
   `10.1016/j.jpaa.2019.04.002`; the remaining returned records were generic
   “conjecture” false positives.
2. **OpenAlex:** search for the exact LPS title, `per-page=20`. Returned the
   journal and arXiv duplicates, the 2026 Evidence Press e=3 candidate, and
   several infinite-transitivity works that cite or discuss the surrounding
   application. No independent e=4 effectivity theorem was returned.
3. **arXiv API:** `all:"Polydegree Conjecture"`, `max_results=50`. Returned
   only “An algorithmic approach to the Polydegree Conjecture for plane
   polynomial automorphisms.”

This is an alias-sensitive database absence result, not proof of priority.

### 2026-08-23T15:29:30Z — LPS forward-chain pass

OpenAlex filter `cites:W2893174753`, `per-page=200`, returned two records:

- Arzhantsev--Kuyumzhiyan--Zaidenberg, *Infinite transitivity, finite
  generation, and Demazure roots*, DOI `10.1016/j.aim.2019.05.006`;
- Arzhantsev, *Automorphisms of algebraic varieties and infinite
  transitivity*, DOI `10.1090/spmj/1749`, arXiv `2212.13616`.

Their inspected topics are infinite transitivity/flexibility. Neither source
states an e=4 Polydegree containment or an effective Fourier/smooth-point
bound. The OpenAlex direction may mix later-version reference chronology, so
this result is used only for discovery.

### 2026-08-23 — primary theorem extraction: Perry and LPS

- Perry dissertation, Theorem 1.3.2 / Theorem 3.0.1: for
  `2 <= d <= 45`, only
  `G_(d+3) intersect closure(G_(d,4)) != empty` is asserted. Page 43 says the
  range was checked using a Mathematica Groebner basis; the dissertation does
  not provide the complete machine artifacts. The example at `d=5` then uses
  approximate roots.
- LPS, Theorem 13(b): for `2 <= d < 20`, the stronger full containment
  `G_(d+4) subset closure(G_(d,5))` is asserted. The paper reports Sage plus
  Magma and partial independent Mathematica checking.
- These are different e-index conventions and, more importantly, different
  logical strengths. The successor must never present Perry's range 45 as a
  containment range.

### 2026-08-23 — P4 primary-source chain

- Orevkov (1987), Lemma 2.1 and Section 4: one-ended finite-image boundary
  chains and a finite sheet/multiplicity budget for locally invertible plane
  polynomial maps.
- Borisov, *On the Stein factorization of resolutions of Jacobian self-maps
  of P2*, Theorems 3.4--3.5: the Stein surface has affine-plane complement;
  its exceptional curves meet only over target infinity; away from that point
  their normalizations are affine lines or once-punctured affine lines; and
  the map on normalizations is either degree one or a power map followed by
  normalization of the target curve.
- Consequence for the parent P4 priority claim: the global boundary geometry
  is a close published precursor and cannot be claimed wholesale as new. The
  exact analytic/algebraic Stein comparison, finite-local-algebra
  interpretation, valuation transport, and the inequality `mu >= e a` remain
  candidates for narrower novelty checking.

### 2026-08-23 — P5 seed and phrase pass

- Kistner--Shaska arXiv `2608.02863v1`, Proposition 3.21, already proves that
  its cyclic-cone members do not directly descend to two-variable polynomial
  Keller pairs: a single top coefficient has a negative Lambda exponent.
  It does not discuss graph sections `W+H(U,V)=0`, finite-normalization
  dicritical covers, or the field-norm compression used in parent P5.
- Exact/near-exact web queries for “boundary-norm obstruction”, “field norm”
  plus “dicritical”, and “graph sections” plus “graded Keller” found no
  journal or arXiv theorem with the parent P5 statement. They did return
  current GitHub research notes on degree-six finite-normalization programmes;
  these are queued as gray literature and are not used as authority without
  commit/provenance inspection.
- Author correction: the authoritative arXiv record gives **Kyle Kistner**
  and **Tanush Shaska**. Any “Jonas Kistner” / “Tony Shaska” string inherited
  from an older audit is erroneous and must not propagate.

### 2026-08-23 — version and dependency reconciliation

- The current arXiv record for Shaska, `2607.20210`, is v2, revised
  25 July 2026. The frozen local source is explicitly v1. The source is used
  only for current graded-Keller context, not as a proof input, and the
  version difference is therefore disclosed rather than silently erased.
- Kistner--Shaska `2608.02863` remains v1, submitted 3 August 2026. Its
  current HTML was searched for `graph`, `field norm`, and the exact transfer
  vocabulary; no equivalent result was located. Proposition 3.21 is still the
  relevant direct non-descent comparison.
- The publisher record for Żołądek, DOI
  `10.1016/j.top.2008.04.001`, confirms the theorem for topological degree at
  most five. This theorem is a dependency of the companion six-sheet
  reduction, not of the abstract boundary-norm transfer theorem. The complete
  article bytes were not frozen here, so no more detailed theorem extraction
  is claimed.

### 2026-08-23 — three alias rounds and orthogonal precursor screen

The stopping-rule rounds were completed separately for the two new claims.

1. **Exact wording:** `e=4 Polydegree containment`, `boundary-norm
   obstruction`, `field norm dicritical graph section`.
2. **Structural wording:** `smooth point coefficient system plane polynomial
   automorphism strata`, `finite pencil homogeneous form monomial`,
   `affine-line dicritical norm exponent`.
3. **Neighbouring vocabulary:** `fixed multidegree closure`, `Stein
   factorization Keller boundary`, `nonproper value valuation transfer`, and
   `graded Keller graph hypersurface`.

The searches used arXiv plus at least one of Crossref, OpenAlex, publisher
pages, author pages, and forward/backward reference chains. The third round
rediscovered Furter's *Plane polynomial automorphisms of fixed multidegree*.
Its theorems concern smooth locally closed fixed-multidegree strata and
closure order among strata of the same length; they do not give the
length-one-to-length-two all-`d` e=4 containment. No close P7a or finite-pencil
boundary-norm theorem emerged in the final round.

## Residual boundaries of the audit

1. The public-record search cannot exclude unpublished, private, differently
   indexed, or future work. It therefore supports only “no close precursor
   located,” never “first” or comprehensive priority.
2. Borisov and Orevkov already cover much of P4's global geometry. The
   successor makes no broad P4 novelty claim and therefore does not require an
   exhaustive priority verdict on every valuation formulation.
3. Mutable GitHub research notes were excluded from scholarly authority.
   Their snippets disclosed no matching theorem; chronology and independent
   authorship were not relied upon.
4. P7b's Lean packaging is a formal-verification contribution, not a claimed
   new classical determinant identity. A separate classical-priority claim is
   intentionally not made.
