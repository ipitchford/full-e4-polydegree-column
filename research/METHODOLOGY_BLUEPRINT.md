# Methodology blueprint

## Research design

The programme uses a proof-first mixed method: conventional mathematics,
formal proof, exact/interval computation, and reproducible literature audit.
Each method has a separate claim class and acceptance test.

## Evidence classes

| Class | What it can establish | What it cannot establish |
|---|---|---|
| Conventional proof | The stated theorem, if externally checked and correct | Formal kernel acceptance or historical priority |
| Lean proof | The encoded statement from declared axioms | Faithfulness of the encoding to the manuscript |
| Exact symbolic computation | Finite identities and enumerated cases | An unencoded infinite theorem |
| Interval certificate | Validated numerical inequalities on its covered domain | Cases outside the certified domain |
| Literature/source audit | Source-backed existence, wording and provisional priority assessment | Mathematical truth of the new proof |
| Internal five-role review | A documented internal release decision on frozen bytes | External peer review or independent reproduction |

## Work packages and gates

### WP0 — immutable parent

- Verify all 200 parent manifest entries.
- Record hashes of P7a, P7b, P4 and P5.
- Never modify the parent release.

**Gate:** exact manifest passes. **Current result:** PASS.

### WP1 — literature and priority audit

- Execute the documented search protocol.
- Verify every bibliographic field against a DOI registry, publisher, arXiv or
  authoritative catalogue.
- Verify every claim at page/theorem/section level from the source itself.
- Search adverse formulations and aliases, not only title phrases copied from
  the candidate manuscripts.
- Classify novelty as `KNOWN`, `CLOSE_PRECURSOR`, `PLAUSIBLY_NEW`, or
  `UNRESOLVED`; never as globally first without external specialist review.

**Gate:** 100% of citations and source-backed statements verified; unresolved
items visibly marked.

### WP2 — P7b formalization

- Create a new pinned Lean project under this successor workspace.
- Transcribe and audit definitions independently from the accepted manuscript.
- Prove small-degree tripwires before the general theorem.
- Prove the universal identity and the evaluation theorem separately.
- Run `lake build`, a forbidden-token scan, `#print axioms` on every public
  theorem, and a statement-diff audit against the manuscript.
- Treat any old local Lean repository as non-authoritative provenance only.

**Gate:** no `sorryAx`, `sorry`, `admit`, unsafe declaration or hidden
hypothesis; public theorem statements match the accepted mathematical claim.

### WP3 — P7a effectivity

Use four residue classes separately. For each selected limit zero and explicit
closed ball:

1. bound coefficient-ratio defects by splitting low levels from a factorial
   tail;
2. bound function and first-derivative errors uniformly;
3. bound limit-Jacobian variation using explicit exponential formulas;
4. apply a stated Newton–Kantorovich, contraction or interval-Newton theorem
   with all norms and constants fixed;
5. certify fourth-row nonvanishing and the anchored minor;
6. convert the threshold in `m` to degrees `d=4m+r`;
7. certify the remaining finite degrees by exact algebra or validated numerics
   whose source-to-theorem bridge is independently audited.

Every bound script must use exact rationals or outward-rounded intervals for
the proof path; ordinary floating point is exploratory only.

**Gate A:** explicit all-residue analytic threshold.  
**Gate B:** exact finite coverage to the published initial range.  
**Fallback gate:** a verifier-backed obstruction dossier identifies the first
failed inequality/case and proves all earlier reductions.

### WP4 — P4/P5 transfer or sharp limitation

First isolate an abstract norm-compression lemma with hypotheses on:

- a finite function-field extension `K/k(s)` presented by a monic boundary
  factor;
- a finite cover `L/K` coming from a dicritical affine line;
- polynomiality/integrality of the pulled-back quotient `h`;
- a relation `h=s^N/ell`; and
- normality of `k[s]`.

Then determine which hypotheses are seed-independent. Test candidate extensions
one architecture at a time: other graded seeds, controlled affine/triangular
coordinate changes, then selected nontriangular coordinates. A failed extension
must yield an explicit counterexample or a proved missing-hypothesis theorem,
not an impressionistic negative result.

**Gate:** at least one theorem or sharp counterexample/no-go result not already
in the parent package.

### WP5 — manuscripts, integrity and review

- Maintain claim–evidence and source–claim matrices during writing.
- Build manuscript PDFs from versioned source.
- Run pre-review reference, claim, computation, originality and AI-failure-mode
  integrity checks.
- Freeze exact successor bytes before review.
- Obtain independent Editor-in-Chief, Methodology/Evidence, Domain Mathematics,
  Cross-disciplinary/Applications and Devil's Advocate reports.
- Resolve every Critical, Major and Minor issue, then re-review and perform an
  independent final integrity check from scratch.

**Gate:** unanimous `ACCEPT` on the exact final bytes with zero unresolved
Critical, Major or Minor findings.

## Reproducibility policy

- Pin toolchains and dependency manifests.
- Store commands, exit codes, stdout/stderr receipts, wall time and hashes.
- Add negative and mutation controls to certificate verifiers.
- A timeout or missing terminal receipt is incomplete evidence, never PASS.
- Preserve failed research branches as timestamped records; do not edit them
  into apparent successes.

## Terminal success conditions

Completion requires all of the following:

1. verified priority audit for P7a and P4/P5;
2. accepted fresh P7b formal proof through arbitrary-ring specialization;
3. a P7a full theorem, effective partial theorem, or minimal-obstruction
   dossier meeting its stated verification gate;
4. at least one new P4/P5 theorem or sharp limitation/counterexample;
5. article-quality frozen successor artifacts; and
6. unanimous five-role internal acceptance of those exact bytes.

