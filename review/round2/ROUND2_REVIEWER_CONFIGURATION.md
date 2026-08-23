# Round 2 reviewer configuration

**Object under review:** `release_candidate/submission`  
**Submission manifest SHA-256:** `867bff8d9b092a133194cf57a53d06dc3824d8aeb47508c5e5eec614bb8fc4a7`  
**Review date:** 23 August 2026  
**Submission state:** immutable-by-manifest; reviewers are read-only

## Round entry condition

Round 1 held manifest `299a0326...8cfa2` for one Minor finding: an
undefined common radius in the P7a direct high-degree tail.  The new bytes
define `R_X=max_s |X_s|<=1`, update the bound source comment, and regenerate
the eventual, integrated P7a, manuscript-build and submission receipts.
No Round 1 acceptance report is carried forward.

## Decision rule

Each reviewer independently returns Accept, Minor Revision, Major Revision or
Reject, with Critical/Major/Minor/Observation counts.  Any Critical, Major or
Minor issue means `HOLD_FOR_REPAIR`.  A Critical Devil's Advocate finding
forbids acceptance.  Unanimous Accept with zero unresolved Critical, Major and
Minor issues is required.

## Roles

1. Editor-in-Chief: contribution, fit, priority calibration, separation and
   presentation.
2. Methodology and Evidence: exact/interval/analytic/formal proof chain,
   receipts, coverage and reproducibility.
3. Domain Mathematics: Polydegree bridge, signs and scaling, universal
   bordered identity, norm and pencil theorems, conditional geometry.
4. Applications and Cross-Disciplinary: reuse, artifact usability and impact
   discipline.
5. Devil's Advocate: strongest attack on all bridges, with explicit re-audit
   of the repaired high-degree tail.

The reports are simulated independent internal AI roles, not external peer
review.  The synthesizer may use only findings actually present in the five
reports.
