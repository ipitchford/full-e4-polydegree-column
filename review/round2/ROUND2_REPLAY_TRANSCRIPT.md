# Round 2 replay transcript

**Submission manifest:**
`867bff8d9b092a133194cf57a53d06dc3824d8aeb47508c5e5eec614bb8fc4a7`

## Exact package gate

- Status: PASS
- Verified subject files: 375
- Parent manifest:
  `f28a6bafbe34c08aa16ad7f18d3f68550b271af43a1ff83b68c1da3cbf8d0f64`
- Manuscript build receipt:
  `d09bd4a04e73d10907700fb0daa1e04ccc2373f35d2f2b194ff9b3370ab4ff60`
- Pages: 14, 5, 6; overfull boxes: 0, 0, 0

## P7a

- Normal integrated replay: PASS
- Optimized integrated replay: PASS
- Receipts byte-identical
- Integrated receipt:
  `87961565b7aa3584b8ea7313b49309d3ad53e56e5e9adcd1ce8cd747a0da94dc`
- Eventual receipt after DA-1 clarification:
  `e9d151f80c138f58db73af2fdc88347afb8ff6c3c0f39c47b849efa2d047602b`
- 14,985 finite cases; normal/optimized ledgers byte-identical
- Endpoint at `m=5000`: `h=0.23477524073436623`, root radius
  `0.0012386391985108088`

## P7b

- Exact 14-file formal set matches candidate
- Lean 4.32.1 / Lake 5.0.0 / Mathlib
  `520045ab14e26149ee970e2e617ca04b09bde5d6`
- Source scan: PASS
- Build: PASS without warnings or `sorryAx`
- Receipt:
  `bc57d920fe4f6679a2b8fa871209f43de99de146c1c012b4a8a81dcadeb494a9`

## Boundary-norm specialization

- Normal and optimized replays: PASS; receipts byte-identical
- Three prohibited pencil degrees have nullity 0
- Two negative-control degrees have nullity 1
- Receipt:
  `1f627c7f8cb30dcf4c978db183f0af6b0d2c2c039b70efc025a52fabbf8fcd2f`

These are exact replays, not independent reproduction or external peer review.
