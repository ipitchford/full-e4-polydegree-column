# Effective e=4 Polydegree certificate package

This directory supports the candidate theorem

\[
\mathcal G_{(d+4)}\subseteq\overline{\mathcal G_{(d,5)}}
\qquad(d\ge2).
\]

Read `../manuscripts/polydegree_e4_effective/manuscript.pdf` first. The proof
uses the published Lewis--Perry--Straub implication for `2 <= d < 20`, an
exact residue-1 branch, 14,985 finite FLINT/Arb certificates, and a uniform
analytic certificate from `m=5000`.

## Fast release replay

In the pinned Python environment:

```sh
python verify_release.py
```

The wrapper performs all inexpensive proof checks under normal and optimized
Python, scans the entire finite ledger, verifies the stored and formula-based
case coverage, compares the two 17 MB ledgers byte-for-byte, and writes
`P7A_RELEASE_RECEIPT.json`. It does not regenerate the expensive finite
ledger.

## Full finite regeneration

To reproduce every interval case into fresh paths:

```sh
python e4_finite_bridge.py \
  --ledger /fresh/path/e4_finite_cases.jsonl \
  --receipt /fresh/path/e4_finite_receipt.json
```

Then point a copied auditor at the new receipt or independently implement the
certificate predicates in Sections 5--6 of the manuscript. Replaying the
same source and Arb library is exhaustive replay, not independent
reproduction.

## Artifact roles

- `e4_eventual_envelope.py`: exact-rational and 256-bit Arb eventual proof.
- `e4_certify_prototype.py`: proof-critical coefficient and interval-Newton
  core used by every finite case.
- `e4_finite_bridge.py`: deterministic ordered producer.
- `verify_finite_ledger.py`: separate fail-closed structural/endpoints audit.
- `verify_normalization.py`: exact direct-multinomial/product-formula audit.
- `small_locators_5_12.jsonl`: exact decimal locator data for `m=5,...,16`.
  The filename is a preserved legacy name; changing it would detach the
  frozen finite receipt from its source hash.
- `e4_finite_cases_v2_m0005_m4999.jsonl`: authoritative finite ledger.
- `e4_finite_cases_v2_m0005_m4999_optimized_replay.jsonl`: byte-identical
  optimized replay.

The core file retains a historical “prototype” filename and introductory
docstring even though it now handles the full finite range. Its executable
logic and frozen source hash, not that historical label, define the
certificate.

## Trust boundary

The package verifies its stated inequalities relative to Python,
python-flint and Arb. The coefficient normalization and tail derivations are
also written mathematically in the manuscript. The package does not verify
the FLINT/Arb implementation, independently reproduce the computation, or
formalize the Lewis--Perry--Straub implication. It says nothing about JC2 or
HC4.
