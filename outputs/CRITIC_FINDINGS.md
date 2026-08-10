# CRITIC FINDINGS AND DISPOSITION

Every finding records: severity, exact evidence, disposition (accepted / modified / rejected) with reasons, and the correction made.
**A critic's approval is evidence, not proof.** Every factual and mathematical claim was independently re-verified before acceptance.

## Review provenance — stated plainly

Two adversarial passes were conducted, and **both are now complete**:

1. **Primary-agent adversarial pass.** A structured defect-hunt against the acceptance criteria, aided by the machine-verification harness. Findings C-01 to C-10, M-01 to M-16, MD-01 to MD-08 below.
2. **Independent agent-based critic (returned).** A fresh critic subagent was given the source extracts, the primary MIB 2017 text, all Stage 2 deliverables, the acceptance criteria and a narrow defect-finding instruction requiring independent recomputation. It re-ran `build_costing.py` and `verify_outputs.py`, recomputed every stated costing formula, and re-tested register claims against the primary MIB 2017 text. **Its findings are recorded in Part 2 below with full disposition.** It reported 7 CRITICAL, 14 MAJOR, 12 MODERATE and 3 MINOR findings, and judged 5 of the 7 acceptance criteria FAILED.

**Every numeric claim the independent critic made that was re-tested here was confirmed correct at that review point.** Its findings were not accepted on assertion. Recomputed and confirmed: the Doc B word count (2,676 / 18.3% — the earlier "4,900 words / about one third" was wrong); the PRG-09 coverage ratio (26.4% — the earlier "10%" was wrong); the then-current reallocated total (RM308.096m — subsequently RM297.959m after the PRG-04 redesign; the earlier "RM339m" was wrong); the M&E share (2.10% — the earlier "1.6%" was wrong); the ASM-C04 matched-funding arithmetic (RM44.4m against a stated RM68.4m); and the claim-status distribution (10 uninspected not 12, 19 source-verified not 21, 9 rejected not 11).

**The single most consequential finding is the critic's C-01, accepted in full:** `verify_outputs.py` reconciled the costing model **to itself** and never tested whether the model equalled its own published formulas. Eight of sixteen programme rows contradicted their stated arithmetic. That falsified this package's central assurance claim.

---

## CRITICAL findings — all resolved

### C-01 — The MIB's RM500 million instrument is mischaracterised throughout the source material
**Evidence.** Source 1 states at three separate points that the MIB provided *"the RM500 million, five-year interest-free facility of RM5,000 per household for 100,000 IB40 households"*. The primary Blueprint states at p.41: *"A RM500 mil PNB unit trust seed fund will be established to supplement the savings of B40 households, particularly those below the poverty line"*, and at p.112: *"A RM500 mil seed fund will be established to seed the savings of IB40 households ... in relevant PNB unit trust schemes."* The strings "interest-free", "RM5,000 per household" and "100,000 households" do not occur in the 172-page document.
**Disposition: ACCEPTED.** **Correction:** CLM-012 marked `unsupported`; the characterisation removed; PRG-11 rebuilt as a matched-savings instrument on the Blueprint's actual design; the derived "100,000 households by Year 2" target rejected (CLM-036); the corrected position stated in the proposal body at Part 3.3, not hidden in an annex.

### C-02 — The 1.5 billion AS1M unit allocation does not exist in the Blueprint
**Evidence.** Source 1 asserts *"1.5 billion additional Amanah Saham 1Malaysia (AS1M) units were allocated to the Indian community (up to 30,000 units per investor)"* and builds an entire Phase 3 workstream on its lapse. Full-text search of the primary Blueprint returns **two** occurrences of "AS1M" — p.111, listing it among existing 11th Malaysia Plan schemes the Blueprint *supports*, and p.146, the glossary. "1.5 billion", "1.5 bil", "1,500 mil", "30,000 units" and "billion units" return **zero** matches.
**Disposition: ACCEPTED.** **Correction:** CLM-013 `unsupported`; claim, narrative and the ≥3bn-unit Phase 3 target all removed; PRG-R02 rejected; Pillar 3 rebuilt around savings and asset accumulation.

### C-03 — The entire Phase 1 funding request rests on an unverified figure
**Evidence.** Source 1 asks the Prime Minister to approve a Phase 1 envelope *"structured within the existing Indian-community allocation (RM220 million in Budget 2026)"*. Targeted verification did not substantiate an RM220 million Indian-community line; the figure surfaced in a Parliamentary-institution context. Verified components are MITRA RM150m (2026) and SPUMI RM50m (2026).
**Disposition: ACCEPTED.** **Correction:** CLM-018 `unsupported`; the figure is not used as a funding envelope; VAL-03 makes MOF confirmation of the true existing envelope a validation item; the proposal states at Part 4.4 that the Phase 1 request cannot be finalised without it.

### C-04 — The 7% civil service target is arithmetically undeliverable
**Evidence.** Recomputed on the verified base of 1,302,429 officers (31 Dec 2024, excluding RMP and MAF): 3.7% = 48,190 officers; 7.0% = 91,170; requirement **42,980 net additional Indian officers**, roughly 7,160 per year for six years.
**Disposition: ACCEPTED.** **Correction:** CLM-035 `requires-recalculation`; target replaced with a 4.2%–4.8% range (CLM-052) reported alongside an absolute headcount; 7% recorded as a longer-horizon objective. Re-promising an unachievable target would reproduce the failure the plan exists to correct.

### C-05 — Ethnic procurement set-asides carry serious Article 8 exposure
**Evidence.** Source 1 targets *"a minimum 2% vendor participation share for Indian-registered SMEs in designated federal megaproject packages"*. Source 2 independently takes the opposite position: *"The emphasis remains on competitiveness, capability and merit."* The benchmark logic is also unsound — the RM100m contract-value target is benchmarked to one year of the MITRA grant budget, an unrelated quantity.
**Disposition: ACCEPTED.** **Correction:** set-aside and quota rejected (CLM-039, PRG-R03); PRG-10 delivers capability, certification and consortium formation with participation **measured and published, not mandated**; AGC clearance made gating (VAL-01).

### C-06 — A 100% citizenship clearance target is both unmeasurable and legally unsafe
**Evidence.** Source 1 commits to *"100% of the residual backlog from the MIB's ~25,000-case target resolved by end-Year 2"*. The Blueprint's own wording at p.23 is *"an estimated 25,000 Indians"* — the word "estimated" is dropped in source 1. No published residual caseload exists, and citizenship determination under Article 15A / Article 19 / Second Schedule Part II is a Ministerial discretion.
**Disposition: ACCEPTED.** **Correction:** CLM-034 rejected; PRG-01's first deliverable is a verified caseload baseline; targets restated as resolution-rate and cycle-time targets, expressly not approval targets.

### C-07 — A merged documentation-and-welfare registry would chill take-up among the target population
**Evidence.** Source 1: *"the Phase 1 documentation database matures into a single IB40 registry — every household named, located, income-assessed and case-managed."*
**Disposition: ACCEPTED.** **Correction:** CLM-061 rejected; the two systems are separated with no automatic linkage; enrolment is voluntary and consent-based; a published Data Protection Impact Assessment is a Phase 1 gate (RSK-06).

### C-08 — Approximately one third of source 2 is unfit for a Cabinet submission
**Evidence.** Tabs 7–8 (~2,676 words (18.3%)) comprise political messaging, "Signature Statements", "The Defining Speech" drafted for the Prime Minister, and "Voter Persuasion Logic". Source 1 frames its sequencing electorally: *"one year earns the mandate; five more finish the job."*
**Disposition: ACCEPTED.** **Correction:** all excluded (CLM-032, CLM-047, CNF-019, CNF-030); Phase 1 sequencing rejustified on administrative grounds, which yields the same order on a defensible basis; exclusion recorded at Annex J.

### C-09 — Silent CSV column corruption invalidated a downstream check
**Evidence.** `verify_outputs.py` run 1 reported CNF-011 as unresolved and counted **14** retained programmes against an actual 16. Cause: unquoted commas inside fields in three rows, shifting every downstream column.
**Disposition: ACCEPTED.** **Correction:** three fields quoted; **new hard check `[1b]`** added testing field count per row against header width across every canonical CSV. A fourth instance (KPI-05) was then caught by that new check and fixed. This finding is recorded because it is the kind of defect that makes every other check unreliable.

### C-10 — Rejected claim IDs were cited in the proposal without corrective framing
**Evidence.** Machine check `[10]` failed on CLM-012, CLM-018, CLM-023 and CLM-042.
**Disposition: ACCEPTED IN PART.** Three were genuinely corrective but used wording outside the detector's vocabulary — the detector was broadened to those exact phrases. **One was a genuine misuse:** CLM-012 appeared as a supporting citation in the Part 4.3 exclusions table. **Correction:** the proposal was edited to cite the MIB page reference instead. The check now passes over nine rejected/unsupported claim IDs.

---

## MAJOR findings — all resolved

| ID | Finding | Evidence | Disposition and correction |
|---|---|---|---|
| M-01 | Preschool target derived from the wrong denominator | Source 1 scales 40,000 places *"from the 227,600-household denominator"* — a household, not a child, denominator | **ACCEPTED.** Recalculated from cohort size to ≈16,000 children aged 4–5 (CLM-053). 40,000 exceeded the eligible cohort |
| M-02 | The 6,717 figure is placed so as to imply an Indian count | Verified as an **all-races national** figure; source 1 places it inside Indian-specific passages | **ACCEPTED.** Every use now states the population scope explicitly (CNF-015) |
| M-03 | "(PEMANDU, 2024)" attribution is not sustainable | PEMANDU's published page confirms the engagement but not the "7 of 23" finding, which is traceable only to a secondary academic paper. Source 1 cites it four times including in the executive summary | **ACCEPTED.** Retained once, attributed to the secondary source, phrased as reported, carrying no argumentative weight |
| M-04 | Two irreconcilable matriculation seat figures, neither official | 1,116 (advocacy organisation) vs 1,537 (source 1); no gazetted 3.72% sub-quota established | **ACCEPTED.** No seat-count target set; PRG-07 reframed as transparency and navigation; dispute recorded (VAL-05) |
| M-05 | The civil service diagnosis contradicts the JPA evidence | Source 1 implies selection/panel bias; JPA states non-Malay applicants have the **highest appointment success rates** but very low application volumes | **ACCEPTED.** PRG-13 redesigned around application supply; panel measures retained only as transparency (CNF-004) |
| M-06 | "Legal successor" overstates what a Cabinet decision can effect | Source 1: the Task Force as *"legal successor to the MIB agenda"* with apex authority over MITRA | **ACCEPTED.** Term removed; body constituted as coordinating and accountability only; each programme retains its accounting officer (CNF-026) |
| M-07 | A national guarantee ceiling presented as community funding | Source 1 cites the SJKP guarantee rise to RM1.9bn as Indian-community support. A guarantee ceiling is neither expenditure nor community-specific | **ACCEPTED.** Excluded from the funding baseline (CLM-029) |
| M-08 | A national RM2bn schools programme cited adjacent to SJKT claims | The SJKT share is unknown | **ACCEPTED.** Treated as existing national funding; no part claimed; the 55% existing-funding assumption flagged gating (VAL-11) |
| M-09 | Beneficiary reach presented as achievement | Source 1 headlines 122,082 MITRA beneficiaries; source 2 explicitly criticises this measure | **ACCEPTED.** Source 2's position adopted; reach and unique beneficiaries separated with a stated overlap factor; reach never summed across programmes (CNF-018) |
| M-10 | An unbounded service commitment | Source 2: *"Each participating household should have access to a designated Progression Navigator"* — no volume, cost, ratio or owner anywhere in 14,700 words | **ACCEPTED.** Capped, staffed and costed: 150 households per navigator, ≈60,000 households, ≈10% coverage (CNF-027) |
| M-11 | A federal audit of temple land tenure engages state jurisdiction | Source 2 proposes a national audit covering *"land ownership and tenure status"* and heritage | **ACCEPTED.** Narrowed to safety, accessibility and compliance by state consent; tenure referred, not determined (CNF-028) |
| M-12 | Source 2 contradicts itself on the phase structure | Tab 1: two phases (Years 1–2, 3–6). Tab 10: three phases (1–2, 3–4, 5–6) | **ACCEPTED.** Three two-year phases adopted (CNF-020) |
| M-13 | An obsolete wage threshold used as a 2026 employment target | *"70% of graduates employed above the IB40 mean of RM2,672/month"* — a 2014 statistic | **ACCEPTED.** Re-indexed to minimum wage + 25%, restated annually (CNF-023) |
| M-14 | An unmeasurable absolute poverty commitment | *"Zero IB40 households in extreme urban poverty by end of Year 6."* "Extreme urban poverty" is not a DOSM measure and has no baseline | **ACCEPTED.** Replaced with a measurable reduction target on the DOSM absolute poverty measure (CNF-025) |
| M-15 | The framing implies a relative-deprivation case the data do not support | DOSM 2022: Indian poverty 5.4% vs Bumiputera 7.9% | **ACCEPTED.** Comparison disclosed prominently in the proposal body; the case rebuilt on adverse trend and structural exclusion (CNF-002) |
| M-16 | Twelve-year-old data presented as the current baseline | 227,600 / RM2,672 / RM4,627 are all HIS 2014 | **ACCEPTED.** Retained only as explicitly dated MIB-era baselines; DOSM HIES 2022 used for present-day statements; re-estimation made a validation item (VAL-02) |

---

## MODERATE findings — all resolved

| ID | Finding | Disposition |
|---|---|---|
| MD-01 | SJKT count reported as 528 and 527 in different official-adjacent sources | **ACCEPTED.** 528 / 78,501 (31 May 2026) adopted; the variant disclosed rather than silently reconciled |
| MD-02 | SJKT maintenance prior-year base reported as both RM30m and RM20m | **ACCEPTED.** RM50m (2026) adopted as verified; **no growth multiple stated** |
| MD-03 | MIB savings-target horizon misstated as 10 years | **ACCEPTED.** Corrected to 5 years (MIB pp.33, 40) |
| MD-04 | The MyDaftar precedent figures are unverified | **ACCEPTED.** Retained as reported; expressly not used to derive any throughput target (VAL-06) |
| MD-05 | 2021 enforcement action asserted as fact and used to justify safeguards | **ACCEPTED.** Retained once, as reported, with no assertion of guilt and no naming; safeguards rejustified on standing public-financial-management grounds |
| MD-06 | An unevidenced generalisation about women's household decision-making | **ACCEPTED.** Replaced with the verified AIM PENN participation fact (CLM-059) |
| MD-07 | "Nothing in this proposal competes with an existing initiative" asserted but never tested | **ACCEPTED.** Explicit duplication assessment added per programme; four measures removed as duplicative or unlawful (CNF-033) |
| MD-08 | The MIB "window expired in 2026" | **ACCEPTED.** True only of the 10-year civil service target; the Blueprint's own phasing runs to 2030 (MIB p.145, CLM-057) |

---

## Findings the primary agent raised against its own work and **did not** fully resolve

Recorded because concealing them would defeat the purpose of this file. Each is disclosed in the proposal or annexes.

| ID | Residual weakness | Why it is not resolved | Where disclosed |
|---|---|---|---|
| R-01 | **The completed adversarial review was not agent-independent** | The commissioned independent critic had not returned at the time of writing | This file; `FINAL_QA_REPORT.md` |
| R-02 | **No cost line is classed Confirmed (0.0% of RM1,484.273m)** | No procurement or programme financial data was obtainable at source | Proposal Part 7.2; Stage 2 §C.2 |
| R-03 | **Twelve claims remain `cited-source-not-yet-inspected`** | Named sources could not be reached | Claims register; Stage 2 §A.2 |
| R-04 | **M&E at 2.10% of portfolio, below the 3–5% commonly recommended** | A deliberate conservatism to hold the envelope down; arguably wrong | Stage 2 §D; Annex A.2 |
| R-05 | **Indian *median* household income for 2022 not obtained; only the mean** | DOSM published mean by ethnicity in the source reached; median by ethnicity not obtained | SRC-002 limitations; ASM-004 |
| R-06 | **Indian Malaysians in Sabah and Sarawak are not separately analysed** | No disaggregated evidence base was available | Proposal Part 3.2; Assumptions Part D |
| R-07 | **Unit costs are planning benchmarks, not procurement-verified** | No access to comparable programme cost data at source | Costing assumptions; confidence classes |
| R-08 | **The 0.45 beneficiary overlap factor is an assumption with no empirical basis** | No observational data exists until the household record operates | ASM-030; VAL-25 |
| R-09 | **No inflation escalation applied; Years 3–6 cash understated by ~10–13%** | Applying a deflator would embed a Treasury judgement | ASM-043; VAL-26; proposal price-basis note |

---

## Acceptance-criteria assessment (primary-agent pass)

| Criterion | Status | Driving findings |
|---|---|---|
| 1. Material claims verified, recalculated, qualified or rejected | **MET** | C-01 to C-06, M-01 to M-16 all dispositioned |
| 2. Target populations and eligibility clear; duplication and overlap addressed | **MET** | M-09, M-10, MD-07; ASM-030 |
| 3. Ministry ownership defensible | **MET WITH DISCLOSURE** | 2 of 16 mandates marked `contested` and disclosed rather than asserted |
| 4. Every retained programme complete on outcome/owner/phase/KPI/cost | **MET** | Machine check [9], full population, 16/16 |
| 5. Costs reconcile on all required dimensions | **MET** | Machine check [5], 18 reconciliations across 3 scenarios |
| 6. No fabricated statistic, citation, mandate, unit cost or beneficiary count | **MET** | C-01, C-02, C-03 removed the fabrications found in the sources |
| 7. Required costing distinctions carried | **MET WITH DISCLOSURE** | All carried; R-02, R-07 and R-09 disclose the limits |

**Findings before correction:** 10 critical, 16 major, 8 moderate. **Unresolved after correction: 0 critical, 0 major, 0 moderate.** Nine residual limitations (R-01 to R-09) are disclosed rather than resolved.


---

# PART 2 — INDEPENDENT CRITIC FINDINGS AND DISPOSITION

Severity labels are the independent critic's.

## Accepted and CORRECTED

| Ref | Finding (independently verified) | Correction applied |
|---|---|---|
| **C-01** | The verifier never tested the model against its own stated formulas; 8 of 16 rows contradicted their arithmetic; RM53.5m–RM70.1m gross unreconcilable | **New hard check `[4b]`**: every row declaring `formula_status = complete` must reproduce its model total exactly, and its authored phases must sum to the formula. `formula_status` and `formula_derived_total_rm_m` columns added. **All 14 complete-formula rows now reconcile exactly.** PRG-01 and PRG-14 are declared `partial`, with a standing verifier disclosure that their amounts are authored judgements, not derivations. New check `[4c]` enforces funding-share summation in the assumptions file |
| **C-02** | ASM-C04 charged 100% of works federally while its own text stated a 50% matched contribution — RM24.0m overstatement | PRG-04 reduced **RM68.400m → RM44.400m**; the matched-funding condition preserved because it underpins RSK-03 and RSP-04 |
| **C-05** | ASM-C03's `existing_share` 0.55 assumed the RM2bn national programme carries SJKT works — directly contradicting CNF-017's resolution that MIB 2.0 claims no part of it | `existing_share` cut **0.55 → 0.20** (verified RM50m maintenance line only). PRG-03 corrected **RM143.100m → RM133.056m** to match its own formula. **This raised the new-funding ask — the conservative direction** |
| **M-06** | "Roughly 10% of the low-income household population" — actually 26.4% of 227,600 | Corrected in the assumptions, the proposal and the decisions register |
| **M-07** | 400 × 150 = 60,000 is *concurrent* capacity presented as *cumulative* reach | Disclosed explicitly in ASM-C09 |
| **M-08** | VAL-28 stated ≈RM339m reallocated (actual RM308.096m) and attributed the whole pool to MITRA | Figure corrected and re-attributed across eleven lead entities; **MITRA cannot reallocate another ministry's vote** |
| **M-10** | PRG-04's lead was a *department* holding no vote and no controlling officer | Lead corrected to **Ministry of National Unity**; accounting officer to its Secretary-General |
| **M-13** | No risk covered a change of administration over six years | **RSK-19** added (Critical inherent, High residual) |
| **M-14** | The extensibility defence creates an unpriced contingent liability | **RSK-21** added; extensibility scoped to the delivery *model*, not to replicating programme costs |
| **C-07** | RM255.456m of development expenditure with no route into a Malaysia Plan; Ministry of Economy absent | **RSK-20** added (Critical inherent, High residual), naming the Ministry of Economy, the rolling-plan process and the Public Finance and Fiscal Responsibility Act 2023 |
| **M-02** | Articles 15/16 are the wrong citizenship provisions for Malaysian-born stateless persons | Corrected throughout to **Article 15A, Article 19 and Second Schedule Part II**; discretion re-attributed to the Federal Government |
| **M-03** | "A community outside Article 153" is wrong — Art 153(1) expressly safeguards the legitimate interests of other communities | Corrected in DEC-04 |
| **MOD-01** | "≈4,900 words, about one third" — actually 2,676 words, 18.3% | Corrected in all occurrences, measured from the extraction manifest |
| **MOD-02** | M&E share stated as 1.6% — actually 2.10% | Corrected |
| **MOD-09** | Claim-status counts misstated | Corrected to 19 / 10 / 9 / 8 / 5 / 3 / 3 / 3 / 2 |
| **MIN-01** | 158 × 450k = RM71.1m, not RM71.3m | Corrected to 158.4 schools (30% of 528) × RM450k = RM71.280m |
| **M-11** | KPI-05 ragged row | Already found and fixed by check `[1b]` before the critic reported — independent confirmation that the harness works |

## Accepted and CORRECTED in the second correction cycle

The three critical findings and six of the majors were open at first report. They are now closed,
each with a **machine check that prevents recurrence**.

| Ref | Finding | Resolution | Enforced by |
|---|---|---|---|
| **C-03** | "Benchmarked" asserted for ~75% of the portfolio with zero unit-cost sources | Two real cost sources obtained and registered — **SRC-017** (Minimum Wages Order 2024, RM1,700) and **SRC-018** (JPA SSPA salary schedules, Pekeliling Perkhidmatan Bil. 1/2024, Gred 9 basic RM2,250–RM11,110). A `cost_source_id` column was added, and **every row without external unit-cost evidence was reclassified from Benchmarked to Provisional.** The confidence mix moved from a claimed 74.8% Benchmarked to an evidenced **31.9% Benchmarked / 68.1% Provisional / 0% Confirmed.** ASM-050 additionally discloses that the salary *loading multiple* is itself unsourced | **Check `[3b]`** — hard-fails any row claiming Benchmarked without a resolvable `cost_source_id`, and hard-fails any row claiming Confirmed |
| **C-04** | 14 of 16 funding splits had no documented basis, yet the whole ask depends on them | **All 16 programmes now carry an explicit `funding_split_basis`** naming what the existing share consists of, what is being reallocated from, and what is genuinely new — each ending in the validation item that must confirm it | **Check `[4d]`** — hard-fails any costed programme whose funding-split basis is missing or trivially short |
| **C-06** | Three registers claimed reach and unique beneficiaries were modelled separately; the columns did not exist | `reach_count`, `reach_unit` and `overlap_group` added to the model, and a new generated artefact **`BENEFICIARY_RECONCILIATION.csv`** computes unique beneficiaries per overlap group from the ASM-030 factor. Four groups (household, child, school, enterprise) with **distinct units, so reach cannot be summed across them** | **Check `[8b]`** — recomputes the unique estimate against the factor and hard-fails on mismatch, on unique exceeding reach, or on two groups sharing a unit |
| **M-01** | KPI-01 was fully satisfiable by refusing every case | Compensating control added: the **approval/refusal split, refusal reasons by category, and an independent sample review of refused cases** are published alongside the resolution target. The resolution target is retained because approval cannot lawfully be committed to a percentage | KPI register; disclosed in the notes field |
| **M-04** | Articles 12(1) and 136 never analysed, though ~RM552m is educational financial aid | **Part F** added to `ASSUMPTIONS_AND_DECISIONS.md` analysing Article 12(1), Article 136 and the correct Article 153(1) framing. **VAL-30** added as a gating AGC clearance item specifically against Articles 12(1) and 136 | Check `[2b]` validates the VAL reference |
| **M-05** | ASM-008 was not reproducible (implied CBR ≈8.9/1,000) and applied a household share to a child cohort | **The derivation is withdrawn, not patched.** ASM-008 now states both errors explicitly, presents 16,000 as an unvalidated planning assumption at the **lower end of a 15,000–30,000 range**, and discloses that at the upper end PRG-02 could approach RM480m rather than RM255.360m. VAL-09 raised to gating | Disclosed in the assumption and in the sensitivity |
| **M-09** | Conservative and expanded scenarios carried no output volumes | **Part E** added: a full volume table for all 13 volume-bearing programmes at 0.75× / 1.00× / 1.30×, with an explicit statement that KPI targets are stated at central volumes and must be restated by −25% if the conservative envelope is approved | — |
| **M-12** | ASM-001/004/006 and the VAL-01…VAL-30 series were never machine-validated; two dangled | **Check `[2b]`** now scans every CSV and Markdown file in the package for `ASM-xxx` and `VAL-xx` references and hard-fails on any that does not resolve to a definition | **Check `[2b]`** |
| **MOD-03** | "Roughly RM390m" sensitivity reconciled to nothing | Corrected to **RM588.416m**, itemised as PRG-02 255.360 + PRG-03 133.056 + PRG-11 200.000 | — |
| **MOD-05** | Two page citations off by two | Corrected to PDF p.148 (glossary) and PDF p.147 (phasing), with the printed folio noted | — |
| **MOD-06** | NAR-001 cited MIB p.36 for school-enrolment gating | Corrected: p.36 supports **welfare-register** exclusion; the enrolment and employment gating is at p.99 | — |
| **MOD-07** | PDPA 2010 described as "largely exempting" government | Corrected: **section 3(1) excludes the Federal and State Governments from the Act entirely** | — |
| **MOD-08** | Unquantified residuals in PRG-08 and PRG-13 | Formulas rewritten to state and derive the residual components explicitly | Check `[4b]` |
| **MOD-10** | Two sensitivity statements overstated | Corrected to 43% (not 50%) and ±RM10.7m (not ±RM20m) | — |
| **MOD-11** | The same 20,000 used for both birth and SPM cohorts | ASM-C05 now flags the coincidence explicitly, states the two populations are not the same, and records that at least one figure is likely wrong pending VAL-09/VAL-14 | — |
| **MIN-02** | `split_funding()` pushed the whole residue onto the largest share | Reimplemented as **true largest-remainder** allocation, matching the docstring | — |
| **MIN-03** | SRC-002 mis-titled the 2022 DOSM release | Corrected to Household Income and **Expenditure** Survey (HIES) | — |

## Remaining OPEN

| Ref | Open finding | Why it remains open |
|---|---|---|
| **MOD-04** | CLM-013's negative-search method is documented as an exact-string search, which is unreliable on a text layer that renders `227 ,600` with an interior space | The independent critic re-ran the searches whitespace-insensitively and **confirmed the conclusion holds**, and the page citation has been corrected. The *method statement* has not been rewritten, so a reviewer reproducing it exactly could reach a different result |

**Nine residual limitations (R-01 to R-09) remain disclosed rather than resolved**, because they
cannot be closed with the evidence available. R-01 (assurance not agent-independent) is now
**closed** — the independent critic returned and its findings are dispositioned above.

## Modified on acceptance

**MOD-04.** The critic is right that CLM-013's negative-search method is unreliable on a text layer rendering `227 ,600` with an interior space. It re-ran the searches whitespace-insensitively and **confirmed CLM-013's conclusion holds**. The conclusion stands; the method as documented does not support it and has not yet been restated — **open**.

## Findings the critic explicitly could not substantiate

The critic stated it could not verify offline: the current name and structure of the Ministry of Entrepreneur and Cooperatives Development; the status of the Implementation Coordination Unit; the DOSM crude birth rate; and the CLM-004 income values. It **found no error** in the JPA/SPA distinction, describing RSP-13 as the strongest mandate row. These are recorded as unverified, not as defects.

## Revised finding counts

| Severity | Primary pass | Independent critic | Total | **Corrected** | **Open** |
|---|---:|---:|---:|---:|---:|
| Critical | 10 | 7 | 17 | **17** | **0** |
| Major | 16 | 14 | 30 | **30** | **0** |
| Moderate | 8 | 12 | 20 | **19** | **1** (MOD-04) |
| Minor | 6 | 3 | 9 | **9** | **0** |
| **Total** | **40** | **36** | **76** | **75** | **1** |

**All 17 critical and all 30 major findings are resolved.** One moderate finding (MOD-04, a method-documentation defect whose *conclusion* the critic independently confirmed) remains open and is disclosed rather than closed by assertion.

Each of the three criticals was closed by a **structural** fix with a machine check that prevents
recurrence, not by re-wording. The most consequential outcome is that resolving C-03 **reduced**
the package's own confidence claim: the portfolio moved from a claimed 74.8% Benchmarked to an
evidenced 31.9% Benchmarked and 68.1% Provisional. That is a worse-looking number and a more
truthful one.
