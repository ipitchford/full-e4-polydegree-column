# Specialist literature and priority search protocol

**Protocol date:** 23 August 2026  
**Search end date:** current execution date; record exact timestamps per query

## Questions

1. What prior work proves or approximates the `e=4` Polydegree containment,
   Fourier/asymptotic coefficient persistence, or effective smooth-point
   criteria for the Lewis–Perry–Straub coefficient system?
2. What prior work identifies finite normalization, Stein contraction,
   dicritical sheet budgets, or inequalities equivalent to `mu >= e a` for
   plane Keller maps?
3. What prior work uses field norms from affine-line dicriticals to obstruct
   graph sections or embeddings, including results not phrased as a
   “six-sheet graph obstruction”?
4. Which parts of the bordered-Jacobian/minor identity are classical or already
   formalized? This question informs attribution even though P7b is not the
   primary priority target.

## Primary source channels

- Crossref and DOI landing pages for metadata resolution;
- arXiv API/abstract pages and source/PDF versions;
- journal and publisher pages;
- zbMATH Open, MathSciNet where locally accessible, and Google Scholar for
  citation chaining and alias discovery;
- EuDML, Numdam, Project Euclid, SpringerLink and institutional repositories
  for older primary texts;
- Mathlib source and documentation for formal precedents.

Search-result snippets are discovery evidence only. Claim verification requires
the paper, book chapter, or formal source itself.

## Query families

### P7a / Polydegree

- `"Polydegree Conjecture" e=4`
- `polydegree plane polynomial automorphisms closure G_(d,e)`
- `Lewis Perry Straub coefficient polynomials g_n,e smooth point`
- `polydegree containment effective threshold`
- `Fourier limit coefficient polynomial automorphisms`
- `Jacobian Euler identity polydegree`
- citations to DOI `10.1016/j.jpaa.2019.04.002`
- citations to arXiv `1809.09681`

### P4 / finite normalization and sheet budget

- `Keller map Stein factorization dicritical divisor local degree`
- `polynomial map C2 nonproperness dicritical local multiplicity`
- `Orevkov three-sheeted polynomial mappings boundary chain`
- `normal ramification tangential degree local multiplicity finite map`
- `finite normalization affine target plane Jacobian conjecture`
- citations to DOI `10.1070/IM1987v029n03ABEH000984`

### P5 / norm obstruction

- `Jacobian conjecture field norm dicritical affine line`
- `Keller map graph section boundary obstruction`
- `six sheeted graded Keller map Kistner Shaska`
- `noninjective étale map A3 graph hypersurface affine plane`
- `dicritical valuation norm polynomial graph`
- `top homogeneous monomial obstruction polynomial embedding`
- citations to the seed paper and to Żołądek's degree-at-most-five result

### P7b attribution/formal precedents

- `Jacobian polynomial multiplication maximal minors resultant`
- `bordered determinant Sylvester resultant kernel vector`
- `binary form multiplication differential Sylvester matrix`
- `resultant gradient maximal minors`
- citations to Chipalkatti Lemma 5.7 and Bhargava–Cremona–Fisher–Gajović
  Lemma 2.6
- Mathlib searches for `Polynomial.resultant`, determinant specialization,
  `Matrix.det`, and `MvPolynomial.eval₂Hom`

## Screening

### Include

- primary research papers, authoritative monographs and formal-library source;
- any language or date when the mathematical claim overlaps;
- theses or preprints when they contain a potentially priority-defeating result;
- correction, erratum and retraction records.

### Exclude from claim support

- search snippets, unsourced summaries and AI answers;
- papers whose full relevant statement cannot be inspected;
- citations that mention the topic without proving the compared claim.

Excluded items remain in the search log with a reason, preventing silent
selection bias.

## Per-source verification record

For every included source record:

1. exact title, authors, year, venue, DOI/arXiv/version;
2. authoritative URLs and access date;
3. exact theorem/lemma/section/page supporting the compared claim;
4. a neutral paraphrase and a short quotation only when necessary;
5. relationship to the successor claim: same, stronger, weaker, orthogonal, or
   only methodological;
6. source quality and version discrepancies;
7. priority effect: `KNOWN`, `CLOSE_PRECURSOR`, `PLAUSIBLY_NEW`, `UNRESOLVED`;
8. independent second-pass verification status.

## Search stopping rule

The internal search can stop when every query family has been run in at least
two independent databases, backward and forward citation chains of all close
precursors have been inspected, three consecutive alias-expansion rounds add
no new close precursor, and all included sources have claim-level verification.
This supports a provisional internal priority assessment only; external
specialist review remains required for a strong priority claim.

