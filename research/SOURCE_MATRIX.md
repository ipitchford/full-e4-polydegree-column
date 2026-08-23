# Source-to-claim comparison matrix

**Status:** final claim-level matrix for the 2026-08-23 successor candidate

| Source | Exact result inspected | Parent/successor relationship | Quality/version | Provisional priority effect |
|---|---|---|---|---|
| Perry, *Polydegree properties of polynomial automorphisms* (PhD, 2016), Thms. 1.3.2, 3.0.1 | e=4 **intersection** through `d=45`; Mathematica Groebner-basis assertion | Weaker than P7a's desired full e=4 containment but a direct computational antecedent | Primary dissertation; exact artifacts not supplied in the PDF | `CLOSE_PRECURSOR`; narrows historical narrative |
| Lewis--Perry--Straub, JPAA 223 (2019), DOI `10.1016/j.jpaa.2019.04.002`, Thms. 4, 11, 13(b) | specialization criterion, decidability, e=4 containment for `2 <= d < 20` | Baseline source of the coefficient system and finite range; P7a aims for an effective all-degree continuation | Peer-reviewed primary paper; frozen author PDF | `KNOWN_BASELINE` |
| Furter, *Plane polynomial automorphisms of fixed multidegree*, Math. Ann. 343 (2009), DOI `10.1007/s00208-008-0296-2` | fixed-multidegree strata are smooth and locally closed; closure results within the fixed-length framework | Important surrounding geometry but not the length-one-to-length-two all-`d` e=4 containment | Peer-reviewed primary paper; author PDF inspected online | `ORTHOGONAL_CLOSE_CONTEXT` |
| Orevkov, Izvestiya 50 (1986)/Math. USSR-Izv. 29 (1987), DOI `10.1070/IM1987v029n03ABEH000984`, Lemma 2.1, Section 4 | one-ended chain and topological multiplicity/defect budget | Foundational input to P4/P5 | Peer-reviewed primary paper | `KNOWN_BASELINE` |
| Borisov, *On the Stein factorization of resolutions of Jacobian self-maps of P2*, DOI `10.1007/s13366-014-0208-4`, Thms. 3.4--3.5 | affine-plane complement; exceptional-curve intersection and normalization geometry; power-map description | Same or stronger than several global-geometric clauses of parent P4; not the exact local-algebra inequality | Peer-reviewed primary paper; author PDF | `CLOSE_PRECURSOR`; P4 novelty must be narrowed |
| Borisov, *Frameworks for two-dimensional Keller maps*, EJC 27 (2020), DOI `10.37236/9210` | combinatorial framework for boundary types and ramification data | Broad P4 context; no finite-pencil graph-norm transfer theorem located | Peer-reviewed primary paper | `CLOSE_CONTEXT`; no P4 package-priority claim |
| Żołądek, *An application of Newton--Puiseux charts to the Jacobian problem*, Topology 47 (2008), DOI `10.1016/j.top.2008.04.001` | publisher abstract confirms the Jacobian Conjecture for maps of topological degree at most five | Input only to the parent/companion six-sheet reduction; not used in the abstract transfer theorem | Peer-reviewed primary publisher record; complete bytes not frozen here | `KNOWN_COMPANION_INPUT` |
| Shaska, arXiv `2607.20210` | graded Keller formalism; dimension-two equivariant maps invertible; three-dimensional examples/parameter spaces | Immediate context and terminology for P5, not its graph obstruction | Current record v2 (25 July 2026); frozen local PDF is v1 | `CONTEXT`, version difference disclosed |
| Kistner--Shaska, arXiv `2608.02863v1`, Thm. 3.19 and Prop. 3.21 | fixed six-sheet seed; direct two-variable non-descent from a negative Lambda exponent | Parent P5 uses this seed but proves a different graph-section obstruction; the source already contains a narrower direct non-descent result | Very recent unrefereed v1 | `KNOWN_SEED`; P5 phrasing must distinguish the two obstructions |
| Arzhantsev et al. infinite-transitivity works (2019, 2023) | application/context, no inspected e=4 effectivity theorem | Orthogonal to P7a's analytic/effective step | Peer-reviewed primary works | `ORTHOGONAL` |
| Current GitHub degree-six/Jacobian research notes returned by phrase searches | finite-normalization and monodromy research; no matching theorem in indexed snippets | Gray literature was discovery-only and is not a scholarly authority for the successor | Public mutable repositories | `EXCLUDED_FROM_PRIORITY_EVIDENCE` |

## Current calibrated assessments

### P7a

The effective all-degree e=4 containment is **submission-worthy and plausibly
new on the completed public-record audit**, not priority-established. Perry is
a direct predecessor and must be cited, but her wider numerical range is
intersection-only. LPS is the controlling full-containment source. Furter's
fixed-multidegree geometry is close context rather than a theorem collision.

### P4

The parent manuscript's broad global-boundary presentation is **not safely
new as a package** because Borisov's published Stein-factor theorem is a close
precursor. A defensible successor must isolate genuinely additional clauses
and explicitly compare them with Borisov Theorems 3.4--3.5.

### P5

The finite-pencil boundary-norm transfer theorem is **plausibly new on the
completed public-record audit**, but it is narrower in scope than the seed
paper's surrounding graded programme. It is defensible as a conditional
generalization, with the seed recovered as one verified instance and with a
proved sharp limitation of the method.

No row authorizes “world-leading,” “first,” or comprehensive-priority claims.
Those labels require specialist external assessment and a broader priority
search than an internal candidate-release audit can supply.
