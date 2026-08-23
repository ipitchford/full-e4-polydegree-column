# Round 1 replay transcript

**Bound submission manifest:**
`299a0326b8dd7d30d2dae9619745f57c7452608814e0fe615e22d5540388cfa2`

## Byte and transitive-receipt gate

- Status: PASS
- Subject files: 375
- Parent round-4 manifest:
  `f28a6bafbe34c08aa16ad7f18d3f68550b271af43a1ff83b68c1da3cbf8d0f64`
- Manuscript build receipt:
  `fdb8ffbc405af81f0a269a0340ff8f939418405ef792c26cd061b0d6f67926b2`
- PDF pages: 14, 5, 6
- Overfull boxes: 0, 0, 0

## P7a replay

- Normal mode: PASS
- Optimized mode: PASS
- Receipts byte-identical
- Integrated receipt:
  `cc5a15ff407173d02bbfd685a111c8c60f8ac50d947eb089ad84c5b9ecde3e87`
- Finite cases scanned: 14,985
- Normal/optimized finite ledgers byte-identical

## P7b replay

- Lean 4.32.1 / Lake 5.0.0 / Mathlib commit
  `520045ab14e26149ee970e2e617ca04b09bde5d6`
- Exact 14-file formal source set matches the frozen candidate
- Source scan: PASS
- Build: PASS without warnings or `sorryAx`
- Formal receipt:
  `bc57d920fe4f6679a2b8fa871209f43de99de146c1c012b4a8a81dcadeb494a9`

## Boundary-norm finite specialization

- Normal mode: PASS
- Optimized mode: PASS
- Receipts byte-identical
- Positive pencil systems: nullity 0 for degrees 0, 1, 2
- Negative control: nullity 1 for degrees 0, 1
- Receipt:
  `1f627c7f8cb30dcf4c978db183f0af6b0d2c2c039b70efc025a52fabbf8fcd2f`

These are replay results, not independent reproduction and not external peer
review.
