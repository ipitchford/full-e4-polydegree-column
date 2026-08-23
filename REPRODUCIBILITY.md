# Reproducibility instructions

Run commands from the submission root.  Verification is fail-closed: a
timeout, missing dependency, changed byte, or nonzero exit is not a pass.

## 1. Verify the frozen file set and receipt bindings

```sh
python3 verify_package.py
```

This verifies every subject-file SHA-256, the exact file set, the parent
round-4 manifest, all manuscript build bindings, and the three project
receipts.  It does not execute third-party proof engines.

## 2. Replay the effective Polydegree package

Pinned environment used for the release: CPython 3.14.6,
`python-flint==0.8.0`, `mpmath==1.3.0`.

```sh
python p7a_effectivity/verify_release.py
python -O p7a_effectivity/verify_release.py
```

Each command scans all 14,985 finite cases.  The wrapper checks the stored
normal/optimized ledger identity and replays the normalization and eventual
certificates.  Full ledger regeneration is documented in
`p7a_effectivity/README.md` and should target fresh paths.

## 3. Replay the formal proof

Pinned toolchain: Lean 4.32.1, Lake 5.0.0, Mathlib v4.32.1 at commit
`520045ab14e26149ee970e2e617ca04b09bde5d6`.

```sh
cd formal/BorderedJacobianUniversal
lake update
python3 verify_release.py
```

The verifier checks the exact source set, pinned dependency commit, forbidden
constructs, a warning-free build, the theorem/axiom report, and the
zero-divisor test.

## 4. Replay the finite-pencil specialization

Pinned environment used for the release: CPython 3.14.6 and `sympy==1.14.0`.

```sh
python3 theorems/verify_boundary_norm_release.py
python3 -O theorems/verify_boundary_norm_release.py
```

This checks the exact six-sheet pencil calculation and negative control.  The
abstract norm and transfer lemmas remain mathematical-text obligations.

## 5. Rebuild the articles

The release used Pandoc 3.9, Latexmk 4.88, and a TeX Live installation.

```sh
python3 build_manuscripts.py
```

The build gate checks required extracted text, page counts, LaTeX errors, and
overfull boxes.  Regeneration changes derived PDF bytes if the external TeX
stack is not byte-reproducible; verify semantics and layout, then record the
new environment rather than overwriting the frozen receipt.

## Evidence boundary

Exact replay is not independent reproduction.  A strong external audit would
separately rederive the normalization/tail bounds, implement the finite
certificate predicates independently, inspect the Lean theorem statements,
and review the geometric hypotheses of the boundary transfer.
