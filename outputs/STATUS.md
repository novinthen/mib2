# MIB 2.0 — STATUS

**Assignment:** Reconcile two source drafts into one evidence-led executive proposal for preliminary Cabinet consideration.
**Working directory:** `C:\Users\Admin1\Desktop\MIB 2.0`
**Price basis for all costs:** 2026 nominal ringgit (RM), price base year 2026.

> `STATUS.md` is a progress record, not proof of correctness. Gate evidence lives in `AUDIT_LOG.md`, `VERIFICATION_RESULTS.md` and `FINAL_QA_REPORT.md`.

---

## Stage 0 — Access and extraction validation — **PASS**

**Timestamp:** 2026-08-05

### Deliverables completed
| Item | Result |
|---|---|
| Source 1 located | `inputs/Malaysian_Indian_6Year_Action_Plan.docx` (41,308 bytes) |
| Source 2 located | `inputs/MIB_2.0_V2.docx` (80,374 bytes) |
| Extraction tool built | `outputs/extract_sources.py` (zipfile + OOXML walker, python-docx installed but not required) |
| Full text extracted | `outputs/extracted/Malaysian_Indian_6Year_Action_Plan.txt` (67,475 chars / 10,000 words) |
| Full text extracted | `outputs/extracted/MIB_2.0_V2.txt` (105,692 chars / 14,663 words) |
| Manifests written | `outputs/extracted/*_manifest.json` |
| Third source acquired | MIB 2017 blueprint PDF, 172 pp, extracted to `outputs/extracted/MIB_2017_blueprint.txt` (287,956 chars) |

### Extraction completeness test (machine-counted)
| Element | Action Plan | MIB 2.0 V2 |
|---|---:|---:|
| Paragraphs with text | 359 | 1,964 |
| Headings | 74 | 266 |
| Tables | 4 | 0 |
| Text boxes | 0 | 0 |
| Images / drawings | 0 | 0 |
| VML images | 0 | 0 |
| Embedded objects (OLE) | 0 | 0 |
| Charts | 0 | 0 |
| `word/media/` entries | 0 | 0 |
| Footnotes / endnotes | 0 | 0 |
| Hyperlink relationships | 0 | 0 |

### Limitations recorded
1. Neither `.docx` contains any image, chart, drawing, embedded object or media part. **No content is image-only, and therefore nothing required OCR or an alternative rendering path.** Extraction is complete.
2. Neither document carries footnotes, endnotes, or hyperlink relationships. All citations in the Action Plan are inline parenthetical references plus a prose "Appendix A: Key Sources" list; none carries a URL, page or table reference. This is itself a material evidence weakness, recorded in the limitations field of SRC-016.
3. `MIB_2.0_V2.docx` has no `docProps` (no page count available). Page counts are therefore not used as a completeness measure; word and paragraph counts are used instead.
4. `Malaysian_Indian_6Year_Action_Plan.docx` declares `Pages: 1`, `Words: 83` in `docProps/app.xml` — these are stale authoring metadata inconsistent with the extracted 10,000 words. Extracted text, not metadata, is treated as authoritative.
5. `MIB_2.0_V2.docx` body is organised as "Tab 1"–"Tab 10" markers rather than numbered chapters; chapter numbers appear inconsistently inside the tabs.

### Gate decision
**PASS.** Both documents were read in full. Machine counts confirm zero non-text objects, so no material content can be hidden from extraction. Blocker policy not triggered.

**Next action:** Stage 1 — comparative diagnostic, registers, unified architecture.

---

## Stage 1 — Comparative diagnostic and unified architecture — **PASS (cycle 2)**

**Timestamp:** 2026-08-05

### Deliverables completed
`STAGE_1_DIAGNOSTIC.md`, `CLAIMS_AND_FIGURES_REGISTER.csv` (62 claims), `PROGRAMME_REGISTER.csv` (16 retained programmes + 5 rejected/merged), `NARRATIVE_REGISTER.csv` (18 entries), `CONFLICT_AND_DUPLICATION_REGISTER.csv` (34 conflicts), `ASSUMPTIONS_AND_DECISIONS.md` (12 decisions).

### Audit cycles
- **Cycle 1:** 9 defects found (3 major, 6 moderate) — chiefly: claims register initially lacked `population_scope` and `reference_period` on 11 rows; two programmes carried no outcome; phase logic in the draft architecture allowed an unfunded Phase 3 commitment.
- **Cycle 2:** all 9 corrected; regression check re-ran the field-completeness test over the full population of rows — 0 failures.

### Rubric (applicable dimensions only)
| Dimension | Score | Evidence |
|---|---:|---|
| Factual accuracy | 4.4 | 62/62 claims classified; 5 claims reclassified `unsupported` after MIB 2017 PDF inspection |
| Evidence quality | 4.3 | Primary MIB 2017 PDF obtained and text-extracted; DOSM/Bernama/The Star inspected at source |
| Internal consistency | 4.4 | 24 conflicts registered with resolution method; 0 silently reconciled |
| Policy logic | 4.3 | Every retained programme carries problem → cause → response → outcome |
| Completeness | 4.5 | All Stage 1 required registers present and field-complete |
| Numerical integrity | N/A | No costing built at Stage 1 (built and tested at Stage 2) |
| Delivery feasibility | N/A | Assessed at Stage 2 |
| Fiscal credibility | N/A | Assessed at Stage 2 |
| Narrative–evidence alignment | N/A | Assessed at Stage 3 |
| Cabinet readiness | N/A | Assessed at Stage 3 |
| **Average (5 applicable)** | **4.38** | Threshold 4.3 — pass |

### Gate decision
**PASS.** Zero critical findings; zero unresolved major/moderate findings. Both documents comprehensively inventoried. No merged drafting begun.

**Next action:** Stage 2 — evidence reconciliation, programme validation, costing.

---

## Stage 2 — Evidence reconciliation, programme validation and costing — **PASS (cycle 3)**

**Timestamp:** 2026-08-05

**Deliverables:** `SOURCE_REGISTER.csv` (16), `RESPONSIBILITY_MATRIX.csv` (16), `KPI_REGISTER.csv` (16), `RISK_AND_SAFEGUARD_REGISTER.csv` (18), `COSTING_ASSUMPTIONS.csv` (24), `COSTING_MODEL.csv` (54, generated), `build_costing.py`, `verify_outputs.py`, `VERIFICATION_RESULTS.md`, `STAGE_2_RECONCILIATION.md`.

**Audit cycles:** Cycle 1 — obtained and extracted the primary MIB 2017 blueprint (172 pp); 5 claims failed primary-source inspection. Cycle 2 — machine verification exposed silent CSV column corruption in 3 rows; new hard check `[1b]` added. Cycle 3 — `[1b]` then caught a 4th corrupted row, and `[10]` caught a rejected claim ID used as a supporting citation; both corrected. Final run: exit 0.

**Rubric:** Factual accuracy 4.5 · Evidence quality 4.2 · Numerical integrity 4.7 · Internal consistency 4.6 · Policy logic 4.4 · Delivery feasibility 4.3 · Fiscal credibility 4.3 · Completeness 4.6 — **average 4.45** (Narrative–evidence alignment and Cabinet readiness scored at Stage 3/4).

**Defects:** 10 critical, 16 major, 8 moderate found; **0 unresolved**. R-01 later closed when the independent critic returned; eight residual limitations (R-02 to R-09) remain disclosed.

**Gate: PASS.** Costs reconcile on all six required dimensions across all three scenarios; machine verification passes with no hard failures.

---

## Stage 3 — Integrated executive proposal — **PASS**

**Timestamp:** 2026-08-05
**Deliverables:** `MIB_2.0_EXECUTIVE_PROPOSAL.md`, `TECHNICAL_ANNEXES.md`.
**Evidence:** 36 distinct claim IDs cited and all resolving; 9 rejected/unsupported claims verified as appearing only in corrective context; body and annex figures identical by construction; 10 Cabinet objections answered; operative approval, conditional endorsement and express deferral separated through a canonical decision register; all electoral and messaging content excluded.
**Rubric:** Narrative–evidence alignment 4.4 · Cabinet readiness 4.4 · Internal consistency 4.6 · Policy logic 4.4 · Completeness 4.6 — **average 4.48**.
**Gate: PASS.**

---

## Stage 4 — Final assurance and release — **PASS**

**Timestamp:** 2026-08-05
**Deliverable:** `FINAL_QA_REPORT.md`.
**Machine verification:** exit 0 — **91 checks passed, 0 hard failures**, 1 standing disclosure warning.
**Findings:** **76 across two adversarial passes** (17 critical, 30 major, 20 moderate, 9 minor) → **76 resolved, 0 open**. The independent critic returned and its findings drove a second correction cycle; Stage 9 closed MOD-04 by documenting the reproducible whitespace-normalised search method for CLM-013.
**Rubric average across all 10 applicable dimensions: 4.44**, every dimension ≥ 4.0.
**Material caveat:** 0% of the portfolio is Confirmed and 68.1% is Provisional. That classification is now evidence-based and machine-enforced (check `[3b]`), having been corrected downward from a previously claimed 74.8% Benchmarked.
**Gate: PASS.**

---

## Submission-readiness Stage 1 — Repair document integrity — **PASS**

**Timestamp:** 2026-08-10

Proposal and annex figures now derive from the canonical registers; repeated financial and phase sections regenerate deterministically; portfolio counts and the Year 2 and Year 3 gates are reconciled; and the verifier detects narrative, reference and financial drift. The implementation was merged through PR #2 at merge commit `9a87816ff3eda217d05b9f1cd66eac6e8042ee82`.

**Gate: PASS for internal document integrity.** This stage does not supply external legal, fiscal, agency or Cabinet approval.

---

## Submission-readiness Stage 2 — Tighten the decision sought — **PASS**

**Timestamp:** 2026-08-10

The Cabinet ask is now divided into **5 approve-now decisions**, **4 conditional endorsements** and **7 express deferrals**. The six-year architecture and programme directions may guide validation, but the RM1,484.273m central scenario is not an approved envelope; no appropriation, reallocation, programme launch, permanent establishment, PNB participation, state-dependent commitment or unverified target is authorised. Parts 2 and 12 are generated from `DECISION_REGISTER.csv`, and verifier check `[12a]` fails on decision-category, fiscal-figure or excluded-subject drift.

**Gate: PASS.**

---

## Submission-readiness Stage 3 — Reclassify and control validation items — **PASS**

**Timestamp:** 2026-08-10

All 30 validation items now reside in `VALIDATION_REGISTER.csv` and are classified by the earliest decision they may block: **12 pre-submission gates, 8 programme-launch gates, 2 phase-expansion gates, 5 operational baselines and 3 deferrable validation matters**. The six strict gates are preserved. VAL-03, VAL-24, VAL-27 and VAL-28 are marked decision-dependent critical. Every row carries one accountable owner, supporting agencies, required evidence, a control deadline, escalation route, financial consequence, affected Stage 2 decision IDs and one of five controlled statuses.

The proposal and detailed assumptions register are generated from the canonical CSV. The no-cascade rule prevents one unresolved partner- or jurisdiction-specific item from blocking unrelated work. Verifier checks `[13]`–`[13b]` enforce schema completeness, classification coverage, criticality, decision references and status vocabulary.

**Gate: PASS.**

---

## Submission-readiness Stage 4 — Legal and jurisdictional clearance matrix — **PASS (design complete; official clearances open)**

**Timestamp:** 2026-08-10

`LEGAL_ISSUES_REGISTER.csv` now controls **18 legal issues**: **10 pre-submission clearances** and **8 programme-launch clearances**. All 16 retained programmes are covered. The matrix identifies the legal authority and primary-source IDs, precise question, provisional design boundary, required written clearance, competent owner, consulted bodies, affected programmes and Stage 2 decisions, related validation controls, unresolved consequence, clearance stage and status.

All 18 issues remain `open`; this drafting exercise has obtained no AGC or other competent-authority clearance. A disposition cannot be recorded without both a written evidence reference and acceptance date. The six PRG-04 pathways are separated, and the newly listed Government Procurement Act 2026 [Act 882] is treated as requiring confirmation of commencement, subsidiary and transitional instruments rather than presumed application.

Verifier checks `[14]`–`[14c]` enforce schema completeness, source/programme/decision/validation linkage, all-programme coverage, authority coverage, status discipline and the six PRG-04 pathways. Final regression: **98 checks passed, 0 hard failures**; deterministic regeneration, production build (29 pages) and targeted website lint passed.

**Gate: PASS for submission-design readiness. Official legal clearance remains an external precondition and is not represented as complete.**

---

## Submission-readiness Stage 5 — Phase 1 fiscal validation architecture — **PASS (design complete; Treasury validation open)**

**Timestamp:** 2026-08-10

`FISCAL_VALIDATION_REGISTER.csv` now controls **10 fiscal questions**: **5 Phase 1 ceiling gates, 4 programme-cost gates and 1 later-phase gate**. Together they cover confirmed existing allocations, lawful reallocations, the true incremental Phase 1 requirement, establishment and fully loaded staffing cost, unit-cost evidence, inflation and annual cash flow, official expenditure and vote classification, procurement and disbursement routes, contingent and matched exposure, and output-defined affordability options.

The generated Phase 1 schedule exposes all 18 central cost lines and reconciles to **RM355.255m gross**. Conservative RM283.359m and expanded RM441.532m figures remain cost sensitivities; none is an output package, fallback envelope or appropriation request. The six-year funding shares are not mechanically apportioned to Phase 1 because no ministry or Treasury has confirmed that split.

All 10 controls remain `open`. A control cannot be recorded as validated without both a Ministry of Finance evidence reference and acceptance date. A verified Phase 1 ceiling exists only after the core funding and classification controls clear and every included component clears its applicable programme-cost gates.

Verifier checks `[15]`–`[15f]` enforce completeness, staging, programme coverage, status discipline, model-derived Phase 1 figures and the prohibition on fabricated funding splits. Current regression: **108 checks passed, 0 hard failures**.

**Gate: PASS for Treasury-review design. Official fiscal confirmation remains external; no Phase 1 ceiling or appropriation is represented as complete.**

---

## Submission-readiness Stage 6 — Programme delivery feasibility — **PASS (design complete; agency confirmation open)**

**Timestamp:** 2026-08-10

`PROGRAMME_DESIGN_REGISTER.csv` now controls **16 programme design sheets**, one for every retained substantive programme. The generated `PROGRAMME_DESIGN_SHEETS.md` joins each design to its programme logic, accounting officer, mandate route, supporting agencies, KPI, central Phase 1 and six-year cost, legal issues and fiscal controls. Every sheet also contains exclusions, delivery channel, geographic coverage, annual or phase volume, complaint and review mechanism, dataset and retention rule, dependencies and stop, redesign and expansion criteria.

All 16 sheets remain `draft_pending_agency_confirmation`; **0 of 16 has written accounting-officer acceptance**. The sheets are therefore internally complete instructions for agency feasibility review, not signed delivery commitments. Acceptance requires an evidence reference and date, and implementation still depends on the mapped legal, fiscal, validation, capacity, state and partner gates.

Stage 6 also corrected three latent service-volume defects: PRG-05 is 120,000 students over six years under its current formula, not 60,000; PRG-09 is a concurrent-capacity model rather than cumulative reach; and PRG-10 supports 5,000 enterprises, not the stale 6,000 narrative. PRG-07's 20,000-applicant-per-phase duration now matches its formula.

Verifier checks `[16]`–`[16f]` enforce design completeness, full programme joins, evidence-backed acceptance, exact generated sheets, required two-part structure and volume reconciliation. Current regression: **118 checks passed, 0 hard failures**.

**Gate: PASS for internal programme-design completeness. Official authority, capacity and accounting-officer confirmation remain external and open.**

---

## Submission-readiness Stage 7 — Concrete service commitments — **PASS (design complete; agency adoption open)**

**Timestamp:** 2026-08-10

`SERVICE_COMMITMENT_REGISTER.csv` now controls seven household-visible minimum service commitments: named case ownership; acknowledgement and status visibility; written reasons or referral records; no-wrong-door referral; published eligibility and waiting-list rules; quarterly service-performance reporting; and a defined escalation and complaint route.

The commitments use observable process events rather than invented day counts. Numeric acknowledgement, processing, referral, waiting-list and complaint-resolution standards remain unset until the responsible agencies validate workflow, caseload, systems and staffing. Quarterly reporting is retained as a portfolio governance cadence, with exact cut-off, assurance and publication dates still subject to PRG-15 and PRG-16 capacity confirmation.

All seven remain `draft_pending_agency_confirmation`; **0 of 7 has written agency adoption evidence**. They control administrative service and remedy only. They do not guarantee citizenship, admission, certification, employment, procurement awards, finance, investment returns, housing or other statutory or third-party outcomes.

Verifier checks `[17]`–`[17g]` enforce the exact seven-commitment set, complete fields, full portfolio coverage, adoption evidence, prohibition on invented numeric deadlines, exclusion of outcome guarantees, deterministic generation and exact programme-sheet mappings. Check `[12f]` also prevents recurrence of the conservative-funding narrative drift found during final review. Current regression: **130 checks passed, 0 hard failures**.

**Gate: PASS for internal service-standard design. Responsible-agency adoption and precise elapsed-time standards remain external and open.**

---

## Submission-readiness Stage 8 — Governance continuity below the Prime Minister — **PASS (design complete; Cabinet adoption open)**

**Timestamp:** 2026-08-10

`GOVERNANCE_CONTINUITY_REGISTER.csv` now controls eight mechanisms: Prime Ministerial sponsorship and strategic review; a designated responsible minister between reviews; a Chief Secretary-chaired or Cabinet-authorised equivalent senior-officials committee; named ministry delivery officers and alternates with commitments in ministry planning; bounded secretariat reporting authority; automatic milestone escalation; meeting-independent quarterly publication; and office-based succession and handover.

The Prime Minister is no longer the daily operating dependency. KPI-15 tests whether delegated reviews, returns, exception handling, reporting and handover continue. Every programme's responsibility record now uses the GC-06 escalation chain. RSK-01 falls from High to Moderate residual risk only if the controls are adopted and maintained; RSK-19 remains High because a successor Cabinet may lawfully change or discontinue policy.

All eight controls remain `draft_pending_cabinet_confirmation`; **0 of 8 is adopted**. They do not create a permanent body, delegate statutory authority, transfer votes or procurement power, displace accounting officers, bind states or independent bodies, or authorise expenditure.

Verifier checks `[18]`–`[18f]` enforce the exact control set, required fields, full portfolio coverage, adoption evidence, deterministic generation, removal of the personal-chair dependency and programme-level escalation. Final regression: **140 checks passed, 0 hard failures**; deterministic double regeneration, targeted website lint and the 29-page production build pass.

**Gate: PASS for internal continuity design. Cabinet terms, delegations, nominations, reporting authority and succession instruments remain external and open.**

---

## Submission-readiness Stage 9 — Cross-stage assurance repair — **PASS (internal release assurance; external approvals open)**

**Timestamp:** 2026-08-10

Stage 9 adds reconstructed, explicitly non-verbatim Stage 1-8 requirements; requirement-to-file-to-test-to-commit traceability; assurance-history corrections; partial-formula ceiling exclusions; GitHub Actions for policy, deterministic, lint and build checks; a classified cross-stage assurance report; and rendered Cabinet-facing DOCX/PDF outputs tied to the canonical Markdown by hash.

The workflow can be made available as a required status check, but repository branch-protection configuration remains a separate administrator setting. Stage 9 does not claim that the workflow file alone enforces merge protection.

Final validation: **161 machine checks passed, 0 warnings, 0 hard failures**; deterministic double regeneration passed; website lint and 29-page production build passed; DOCX accessibility audit returned 0 findings; the 37-page PDF passed structure, text, page-count and visual inspection. **Gate: PASS for internal repository release. Legal, Treasury, agency and Cabinet approvals remain external and open.**

---

## Headline result

| | Central | Conservative | Expanded |
|---|---:|---:|---:|
| Six-year gross cost (2026 prices) | **RM1,484.273m** | RM1,158.487m | RM1,875.220m |
| Incremental new funding | **RM847.677m** | RM662.217m | RM1,070.229m |

Confidence mix (central): **Confirmed 0.0%** · Benchmarked 31.9% · Provisional 68.1%.
**30 validation items, 18 legal issues and 10 fiscal controls remain open. All 16 programme design sheets await agency acceptance, all seven service commitments await agency adoption, and all eight governance continuity controls await Cabinet confirmation. Six validation items are strict gates: VAL-01, VAL-09, VAL-11, VAL-19, VAL-23 and VAL-30. Four are decision-dependent critical: VAL-03, VAL-24, VAL-27 and VAL-28. An unresolved item blocks only its mapped decision, programme or fiscal component.**
