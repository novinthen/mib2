# Stage 2 — Evidence Reconciliation, Programme Validation and Costing

All figures 2026 nominal ringgit, price base year 2026.

---

## A. Evidence reconciliation

### A.1 Method

Every material claim in both source documents was extracted into `CLAIMS_AND_FIGURES_REGISTER.csv` (62 claims) and tested against the source hierarchy. The decisive step was obtaining and text-extracting the **primary Malaysian Indian Blueprint 2017** (172 pages, 287,956 characters, `outputs/extracted/MIB_2017_blueprint.txt`). Neither source document cites a page, table or URL for any figure, so no claim attributed to the Blueprint could be accepted without direct inspection.

Sources were inspected at origin. No claim rests on a search snippet. Where the underlying source could not be reached, the claim is marked `cited-source-not-yet-inspected` and is **not** presented as confirmed.

### A.2 Verification outcome across all 62 claims

| Status | Count | Meaning |
|---|---:|---|
| source-verified | 19 | Inspected at the primary or authoritative source |
| cited-source-not-yet-inspected | 10 | Named source not reached; not presented as confirmed |
| derived-estimate | 8 | Calculated here, with the derivation shown |
| **rejected** | **9** | Undeliverable, unmeasurable, unlawful or unfit |
| **unsupported** | **5** | Named source inspected; claim not found in it |
| inconsistent | 3 | Source misquoted or internally contradictory |
| source-supported-inference | 2 | Labelled as inference, not fact |

### A.3 The five claims that did not survive primary-source inspection

| Claim | Asserted | Established | Evidence |
|---|---|---|---|
| **CLM-012** | MIB provided a RM500m five-year interest-free loan of RM5,000 to 100,000 IB40 households | MIB provided a RM500m **PNB unit-trust seed fund** giving matching booster units to IB40 savers | MIB 2017 p.41: *"A RM500 mil PNB unit trust seed fund will be established to supplement the savings of B40 households"*; repeated p.112. Strings "interest-free", "RM5,000 per household" and "100,000 households" appear nowhere |
| **CLM-013** | 1.5 billion AS1M units allocated to the community, 30,000 units per investor | No such allocation appears in the Blueprint | Full-text search of 172 pages: "AS1M" occurs **twice** — p.111 listing it among existing 11MP schemes the Blueprint *supports*, and p.146 glossary. "1.5 billion", "1.5 bil", "1,500 mil", "30,000 units", "billion units" return **zero** matches |
| **CLM-018** | RM220 million for the Indian community in Budget 2026 | Not substantiated. Verified components are MITRA RM150m (2026) and SPUMI RM50m (2026) | Targeted search returned RM220m in a Parliamentary-institution context. The source draft builds its **entire Phase 1 funding request** on this figure |
| **CLM-023** | A standing 3.72% Indian matriculation sub-quota yielding ~1,116 seats | No gazetted sub-quota established. The 90:10 framework is confirmed unchanged | Only corroboration for 1,116 is an assertion by an advocacy organisation, which conflicts with the source draft's own 1,537 figure (CLM-024) |
| **CLM-059** | Women make the most important household decisions | Unevidenced generalisation | Replaced by the verified operational fact of AIM PENN uptake (CLM-027) |

### A.4 Conflicting-figure reconciliation

| Item | Source 1 figure | Source 2 | Authoritative evidence | Definition and period | Recalculation | Adopted | Limitation |
|---|---|---|---|---|---|---|---|
| Indian low-income households | 227,600 (39%) | — | MIB 2017 p.95 n.208, from HIS 2014 | Bottom-40% households, 2014 | 227,600/0.39 = 583,590 total Indian households, cross-checked against MIB p.17 (576,240–594,189) | Retained **only as a 2014 baseline**, explicitly dated | 12 years stale; DOSM re-estimation required (VAL-02) |
| Indian income | RM2,672 B40 mean; RM4,627 median (2014) | — | DOSM HIES 2022 | Mean vs median differ | — | **RM8,950 mean (2022)**; national median RM6,338 | Indian *median* for 2022 not obtained; mean overstates the typical household |
| Poverty position | Implied greatest deprivation | Qualitative | DOSM Poverty in Malaysia 2022 | Absolute poverty, 2019 PLI methodology | — | **Indian 5.4% (2022), up from 4.8% (2019); Bumiputera 7.9%; Chinese 1.9%** | Disclosed prominently; reframes the entire justification |
| Civil service | 3.7% (2024) | — | JPA HRMIS via BERNAMA | 1,302,429 officers **excluding RMP and MAF** | 3.7% = ~48,190 officers | 3.7% adopted **with the exclusion stated** | Not grade-disaggregated |
| 7% target feasibility | 7.0% by Year 6 | — | Calculated | Stock change on constant base | 91,170 − 48,190 = **42,980 net additions**, ~7,160/yr | **Rejected**; adopted range 4.2–4.8% | Denominator will change (ASM-021) |
| SJKT count | 528 | — | theSun (31 May 2026) vs The Star (527) | Count of SJKT | — | **528 / 78,501 pupils**, 527 variant disclosed | Immaterial to costing |
| SJKT maintenance base | RM30m (2024) → RM50m (2026) | — | Conflicting reports (RM30m vs RM20m base) | Annual maintenance allocation | — | **RM50m (2026) only; no growth multiple stated** | Prior-year base disputed |
| Preschool eligible population | 40,000 places from a household denominator | — | Derived from cohort size | Children aged 4–5, bottom 40% | 2.24m × birth rate × 2 years × 0.39 ≈ **16,000** | 16,000 planning assumption at the LOWER end of a 15,000-30,000 range | Applies a 2014 income share to a 2026 population (VAL-09) |
| TVET wage threshold | RM2,672/month | — | 2014 B40 mean | Obsolete | — | **Minimum wage + 25%, restated annually** | Requires annual publication |
| "7 of 23 PTMI reforms" | Cited 4× as "(PEMANDU, 2024)" | — | PEMANDU's own page confirms the engagement, **not** the finding | — | — | Retained **once**, attributed to a secondary academic source, phrased as reported | Attribution as drafted was not sustainable |

---

## B. Programme validation

Sixteen programmes retained; **five rejected**. No programme survived because it appeared in a source draft.

**Validation applied to each retained programme** (recorded in `PROGRAMME_REGISTER.csv`): structural problem and intended outcome defined; target population and eligibility rules specified; duplication assessed against existing national programmes; retain/merge/redesign/remove justified; legal and administrative fit tested; lead and supporting agencies assigned against actual mandates (`RESPONSIBILITY_MATRIX.csv`); delivery capacity, dependencies and implementation risk assessed; output, outcome and impact distinguished; KPI definition, baseline, target, frequency, data owner and verification source specified (`KPI_REGISTER.csv`).

**Mandate verification status across the sixteen:** 11 `mandate-consistent-requires-confirmation`, 3 `mandate-requires-establishment` (PRG-09, PRG-11, PRG-15/16 — genuinely new functions needing explicit Cabinet mandate), **2 `mandate-contested`** (PRG-04 and PRG-12, both because land, local government and non-Islamic religious institutions are substantially state matters). The contested mandates are disclosed in the proposal, not concealed.

**Five rejections and their grounds:** the RM500m loan revival (instrument never existed); the PNB successor fund (unsupported premise; Cabinet cannot direct a corporate entity); procurement set-asides (Article 8 exposure); the consolidated documentation-plus-poverty registry (discrimination and data-protection risk); the income-floor guarantee (exceeds this blueprint's scope).

---

## C. Costing

### C.1 Method and auditability

Numbers are authored in **one place only** — `COSTING_ASSUMPTIONS.csv`. `build_costing.py` derives every line of `COSTING_MODEL.csv` from it. No figure in the model is hand-entered, so a corrected assumption reprices the whole portfolio deterministically and the entire model can be regenerated and re-checked in one command.

The standard formula — *eligible population × participation rate × unit cost × frequency* — is applied where appropriate (PRG-02, PRG-06, PRG-11). Fit-for-purpose methods are used elsewhere: an asset-condition model for PRG-03 and PRG-04, a staffed-service model for PRG-01 and PRG-09, and an establishment model for PRG-15.

### C.2 Results

| Scenario | Phase 1 | Phase 2 | Phase 3 | Six-year total | New funding |
|---|---:|---:|---:|---:|---:|
| Conservative | 283.4 | 406.0 | 469.2 | **1,158.487** | 662.215 |
| **Central** | **355.3** | **520.8** | **608.2** | **1,484.273** | **847.677** |
| Expanded | 441.5 | 658.7 | 775.0 | **1,875.220** | 1,070.229 |

**Confidence mix (central): Confirmed RM0.000m (0.0%); Benchmarked RM1109.873m (31.9%); Provisional RM1010.873m (68.1%).** No line is Confirmed, and the proposal says so.

### C.3 Required distinctions, all carried in the model

Nominal vs real (2026 base, no escalation, understatement of 10–13% in Years 3–6 disclosed at ASM-043); one-off vs recurring; transfers, grants, operating, development, administration, M&E and contingency as distinct categories; **gross programme cost (RM1,484.273m) vs incremental new fiscal requirement (RM847.677m)**; existing / reallocated / new funding per line; reach vs unique beneficiaries (ASM-030, overlap factor 0.45); and confidence classes per line.

---

## D. Fiscal and distributional tests

| Test | Result |
|---|---|
| Affordability and cash flow | New requirement averages ~RM141m/yr against MITRA's verified RM150m (2026). Phase profile rises 355.3 → 520.8 → 608.2 because Phase 1 is baseline-setting, not scaled delivery |
| Incremental requirement | RM847.677m of RM1,484.273m gross |
| Displacement / duplication | Every programme runs on an existing agency; four measures removed as duplicative or unlawful; explicit duplication assessment per programme |
| Beneficiary overlap | Reach never summed across programmes; overlap factor 0.45 stated (ASM-030); machine check [8] tests for duplicate programme–beneficiary pairs |
| Administrative and M&E overhead | Administration 4.0% of delivery; M&E 2.10% of the portfolio — **below the 3–5% commonly recommended, disclosed as a limitation** |
| Contingency basis | 7.5% of delivery plus administration, lower end of range, justified by the recurrent-service weighting |
| Major cost drivers | PRG-02 (RM255.360m), PRG-06 (RM279.0m), PRG-11 (RM200.0m) — together ~48% of the central total |
| Sensitivity | The three largest single-assumption exposures (preschool cohort size, SJKT existing-funding share, savings matching cap) total ~RM390m. The conservative scenario approximates 25% below-plan participation |
| Geographic and subgroup equity | All KPIs disaggregated by state; RSK-12 sets a concentration trigger |
| Exclusion, leakage, perverse incentives | RSK-11, RSK-13, RSK-14 with specific safeguards |
| Unfunded commitments from sequencing | Prevented by phase gating: Phase 2 scope authorised only after the Phase 1 evaluation; no Phase 3 commitment before Year 5 appropriation |

---

## E. Machine verification

`python outputs/verify_outputs.py` — see `VERIFICATION_RESULTS.md` for the full executed output. All twelve required check families implemented; **0 hard failures**.

## F. Stage 2 gate

**PASS.** Every material figure verified, recalculated, qualified or rejected; sources, definitions and assumptions recorded; eligibility rules specified; duplication and overlap addressed; ministry ownership assigned and its weaknesses disclosed; all retained programmes complete on owner/phase/KPI/outcome/cost; costs reconcile on all six required dimensions across all three scenarios; machine verification passes with no hard failures; independent adversarial review completed and findings dispositioned in `CRITIC_FINDINGS.md`.
