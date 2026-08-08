# AUDIT LOG

Chronological record of what was checked, what failed, what changed, and the result. Original session date: 2026-08-05; latest amendment: 2026-08-08.

---

## Post-release amendment — PRG-04 multi-faith redesign (2026-08-08)

| # | Check | Result |
|---|---|---|
| A.1 | Inclusive scope | PRG-04 expressly includes Hindu temples, mosques and surau serving Indian Muslim communities, churches, Sikh gurdwaras, Baha'i facilities and other eligible institutions through an open-ended definition |
| A.2 | Common eligibility | Needs-based criteria, documented public-interest community service, and state, institutional and any applicable religious-authority consent replace fixed allocations by religion |
| A.3 | Differentiated structural response | Temple and estate-legacy tenure, relocation and registration cases retain a separate documentation-and-state-referral pathway; no federal adjudicative power is asserted |
| A.4 | Public-funding boundary | Support is limited to life safety, accessibility, compliance and eligible community-service spaces; worship, proselytisation, ceremonies, devotional fixtures and doctrinal activity are excluded |
| A.5 | Cost discipline | RM44.400m remains a provisional planning cap, not an expanded coverage commitment; the 1,200-institution assumption, faith-type distribution, partner capacity and fiscal envelope require recalibration after the multi-faith facility map |
| A.6 | Cross-register consistency | Programme, responsibility, KPI, risk, conflict, claim, costing and executive-proposal records updated; `COSTING_MODEL.csv` regenerated from `COSTING_ASSUMPTIONS.csv` |
| A.7 | Regression verification | `verify_outputs.py`: **PASS — 76 checks, 0 hard failures, 1 standing disclosure warning**; Next.js production build: **PASS — 29 static pages generated** |

**Amendment result: PASS.** No numerical target or additional appropriation was invented. The broadened eligibility is explicitly gated by VAL-13 baseline, jurisdictional and fiscal validation.

---

## Stage 0 — Access and extraction validation

| # | Check | Method | Result |
|---|---|---|---|
| 0.1 | Both source documents located | Directory listing of `inputs/` | PASS — 2 `.docx`, 41,308 and 80,374 bytes |
| 0.2 | Full content extracted | Custom OOXML walker `extract_sources.py` traversing body, tables, text boxes, `AlternateContent`, `sdt`, headers/footers, footnotes, endnotes | PASS — 67,475 and 105,692 chars |
| 0.3 | Image-only / truncated / omitted content | Machine count of `a:blip`, `v:imagedata`, `w:object`, `w:drawing`, `word/media/*`, chart parts, embeddings | PASS — **all zero in both files**; no OCR or alternative rendering needed |
| 0.4 | Tables captured | Row/cell traversal | PASS — 4 tables in source 1, 0 in source 2 |
| 0.5 | Metadata reliability | `docProps/app.xml` vs extracted text | **DEFECT (minor):** source 1 declares `Pages: 1, Words: 83` against 10,000 extracted words. Metadata is stale. **Correction:** extracted text treated as authoritative; page counts not used as a completeness measure |
| 0.6 | Citation infrastructure | Footnote/endnote/hyperlink relationship count | **DEFECT (major, in the sources):** zero footnotes, endnotes or hyperlinks in either document. No figure carries a page, table or URL. **Correction:** no claim attributed to a named source accepted without direct inspection of that source. Registered as CNF-014 context |

**Gate: PASS.** Blocker policy not triggered.

---

## Stage 1 — Comparative diagnostic

### Cycle 1
| Defect | Severity | Finding |
|---|---|---|
| S1-D01 | Major | 11 claims rows lacked `population_scope` and `reference_period` |
| S1-D02 | Major | 2 programmes carried no `outcome` |
| S1-D03 | Major | Draft architecture permitted a Phase 3 commitment with no Phase 2 gate |
| S1-D04 | Moderate | Narrative register lacked an `exaggeration_risk` field |
| S1-D05 | Moderate | Conflict register lacked `adopted_resolution`, recording only a method |
| S1-D06 | Moderate | Programme register lacked an explicit duplication assessment |
| S1-D07 | Moderate | Source register lacked a `supports_directly_or_inference` field |
| S1-D08 | Moderate | Claims register had no link to conflict IDs |
| S1-D09 | Moderate | No record of which source-2 content was excluded and why |

### Cycle 2 — corrections and regression
All nine corrected. Fields added; the Phase 3 gate written in (independent mid-term evaluation at end-Year 3 gates Phase 3 funding); `duplication_assessment`, `adopted_resolution`, `exaggeration_risk`, `supports_directly_or_inference` and `conflict_id` columns added; exclusions recorded at CLM-047 and CNF-030.
**Regression check:** field-completeness re-tested over the full population of rows in all five Stage 1 registers — **0 failures**.

**Gate: PASS.** Scores in `STATUS.md`. Zero critical findings.

---

## Stage 2 — Evidence reconciliation, programme validation, costing

### Source verification actions
| # | Action | Result |
|---|---|---|
| 2.1 | Obtained the **primary MIB 2017 blueprint** (172 pp) and extracted 287,956 chars | Decisive — enabled direct testing of every MIB-attributed claim |
| 2.2 | Full-text search for `227,600`, `2,672`, `4,627` | **Verified** at MIB pp.16, 18, 94, 95 |
| 2.3 | Full-text search for `RM500`, `AS1M`, `1.5 billion`, `30,000 units` | **CRITICAL DEFECT FOUND** — RM500m is a *PNB unit-trust seed fund* (pp.41, 112), not a loan scheme; AS1M appears twice, both incidental; the 1.5bn figure returns **zero matches** |
| 2.4 | Full-text search for `25,000`, civil service `7%`, savings target | **Verified** at pp.23, 36, 118, 129, 33, 40 — and the savings horizon is **5 years, not 10** as the source draft states |
| 2.5 | DOSM HIES 2022, Poverty in Malaysia 2022, Current Population Estimates 2026 | Verified; **Indian poverty 5.4% (2022) is below Bumiputera 7.9%** — materially reframes the justification |
| 2.6 | JPA/HRMIS civil service composition | Verified: 3.7% of 1,302,429 excluding RMP and MAF; **and JPA attributes the gap to application volume, not selection** |
| 2.7 | The Star, 29 July 2026 PM announcement | Verified at source |
| 2.8 | MITRA RM150m (2026) | Verified (BERNAMA / The Star / The Edge) |
| 2.9 | SJKT 528 / 78,501 (31 May 2026) | Verified — **conflict found:** The Star refers to 527, and the prior-year maintenance base is reported as both RM30m and RM20m |
| 2.10 | 6,717 matriculation offers (April 2026) | Verified — **and confirmed to be an all-races national figure**, not an Indian count |
| 2.11 | RM220m Budget 2026 Indian-community line | **NOT SUBSTANTIATED.** The source draft's entire Phase 1 funding request rests on it |
| 2.12 | PEMANDU "7 of 23 PTMI reforms" | PEMANDU's own page confirms the engagement but **not the finding**; traceable only to a secondary academic paper |
| 2.13 | 3.72% matriculation sub-quota | **NOT ESTABLISHED** as an instrument; two irreconcilable seat figures (1,116 vs 1,537) circulate |

**Disposition:** 5 claims marked unsupported, 3 inconsistent, 11 targets rejected, 12 marked cited-source-not-yet-inspected.

### Numerical verification
| # | Check | Result |
|---|---|---|
| 2.14 | Costing built from assumptions by script, not by hand | `build_costing.py` → 54 cost lines, no hand-entered figures |
| 2.15 | Funding shares sum to 1.0 per programme | Enforced in the builder; raises `SystemExit` otherwise |
| 2.16 | Funding split sums exactly to line total | Largest-remainder allocation; no rounding residue possible |
| 2.17 | Civil service 7% feasibility recomputed | 42,980 net additions required → **target rejected** |
| 2.18 | Preschool cohort recomputed from cohort size not household count | 40,000 places **exceeded the eligible cohort** → recalculated to ≈16,000 children |
| 2.19 | Full machine verification | `verify_outputs.py` — see below |

### Machine verification cycles
| Cycle | Command | Result |
|---|---|---|
| 1 | `python outputs/verify_outputs.py` | **50 passed, 0 hard failures, 3 warnings.** Warnings: proposal not yet written; CNF-011 reported unresolved; 9 canonical files not yet written |
| — | Investigation of the CNF-011 warning | **DEFECT FOUND (major):** three CSV rows contained **unquoted commas inside a field**, silently shifting every downstream column. Affected: `CONFLICT_AND_DUPLICATION_REGISTER.csv` CNF-011, and `PROGRAMME_REGISTER.csv` PRG-09 and PRG-10. Effect: the retained-programme count read 14 instead of 16, and CNF-011's status read as its resolution method. **This is exactly the class of silent corruption that would have invalidated downstream checks** |
| — | Correction | Three fields quoted. **New hard check `[1b]` added to `verify_outputs.py`**: field-count integrity per row against header width, across every canonical CSV, so this class of defect can never again pass silently |
| 2 | Re-run after correction and all remaining files written | Recorded in `VERIFICATION_RESULTS.md` |

### Independent adversarial review
A fresh critic subagent was commissioned with the source extracts, the primary MIB 2017 text, all Stage 2 deliverables, the acceptance criteria, and a narrow instruction to find defects and to independently recompute at least six programme phase figures against the stated formulas. Findings and their disposition — accepted, modified or rejected, with reasons — are recorded in `CRITIC_FINDINGS.md`. Every factual and mathematical claim made by the critic was independently re-verified before acceptance; a critic's approval is treated as evidence, not proof.

**Gate: PASS.**

---

## Stage 3 — Integrated executive proposal

| # | Check | Result |
|---|---|---|
| 3.1 | No number in the proposal without a claim ID or register mapping | Enforced by machine check [10] |
| 3.2 | No rejected/unsupported claim used as live evidence | Machine check [10] scans a ±600-character window around every rejected claim ID for corrective language and fails if absent |
| 3.3 | Ten Cabinet objections explicitly answered | Part 10 of the proposal |
| 3.4 | Preliminary endorsement distinguished from appropriation | Stated in the status note, in the D1–D6 table's "does not authorise" column, and in Part 12 |
| 3.5 | Body–annex agreement | Annex A totals equal the proposal's Part 7 figures; both derive from the same generated CSV |
| 3.6 | Electoral and messaging content excluded | Verified absent; recorded at Annex J |
| 3.7 | Heterogeneity requirement | Part 3.2 distinguishes by documentation status, life stage, household composition, geography and gender, and records the Sabah/Sarawak analytical gap rather than concealing it |
| 3.8 | British spelling and formal register | Applied throughout |

---

## Stage 4 — Final assurance

Recorded in `FINAL_QA_REPORT.md`.
