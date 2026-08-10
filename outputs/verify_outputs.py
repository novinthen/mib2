"""
Machine verification for the MIB 2.0 output package.

Implements the twelve minimum checks required by MASTER_PROMPT.md section 10.
Exits non-zero if any HARD check fails.

Usage: python outputs/verify_outputs.py
"""

import csv
import hashlib
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))

HARD_FAILURES = []
SOFT_WARNINGS = []
PASSED = []
TOL = Decimal("0.005")  # RM 5,000 tolerance on RM-million figures


def load(name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        HARD_FAILURES.append(f"[FILE] missing required file: {name}")
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check(cond, ok_msg, fail_msg, hard=True):
    if cond:
        PASSED.append(ok_msg)
    else:
        (HARD_FAILURES if hard else SOFT_WARNINGS).append(fail_msg)
    return cond


def D(x):
    try:
        return Decimal(str(x).strip() or "0")
    except Exception:
        return None


# --------------------------------------------------------------------------
REQUIRED = {
    "SOURCE_REGISTER.csv": ["source_id", "title", "issuing_institution", "url",
                            "access_date", "tier", "limitations",
                            "supports_directly_or_inference"],
    "CLAIMS_AND_FIGURES_REGISTER.csv": ["claim_id", "source_document", "source_location",
                                        "verbatim_or_close_claim", "claim_type",
                                        "population_scope", "geography", "reference_period",
                                        "cited_source", "verification_status",
                                        "adopted_treatment", "notes"],
    "PROGRAMME_REGISTER.csv": ["programme_id", "programme_name", "problem_addressed",
                               "structural_cause", "target_group", "eligibility",
                               "delivery_mechanism", "proposed_owner", "phase",
                               "output", "outcome", "kpi_id", "cost_status",
                               "duplication_assessment", "preliminary_feasibility",
                               "retain_decision"],
    "NARRATIVE_REGISTER.csv": ["narrative_id", "source_document", "narrative_element",
                               "evidence_status", "exaggeration_risk",
                               "recommended_treatment"],
    "CONFLICT_AND_DUPLICATION_REGISTER.csv": ["conflict_id", "item", "action_plan_position",
                                              "mib_v2_position", "conflict_type",
                                              "materiality", "evidence_needed",
                                              "resolution_method", "status",
                                              "adopted_resolution"],
    "RESPONSIBILITY_MATRIX.csv": ["responsibility_id", "programme_id", "lead_ministry_or_agency",
                                  "mandate_basis", "accounting_officer", "phase",
                                  "mandate_verification_status"],
    "KPI_REGISTER.csv": ["kpi_id", "programme_id", "kpi_name", "indicator_type", "definition",
                         "baseline_value", "baseline_year", "year_2_target",
                         "year_4_target", "year_6_target", "measurement_frequency",
                         "data_owner", "verification_source"],
    "RISK_AND_SAFEGUARD_REGISTER.csv": ["risk_id", "risk_category", "risk_description",
                                        "likelihood", "impact", "safeguard", "owner"],
    "COSTING_MODEL.csv": ["cost_line_id", "programme_id", "pillar", "lead_ministry",
                          "cost_category", "price_base_year", "scenario", "years_1_2",
                          "years_3_4", "years_5_6", "six_year_total", "existing_funding",
                          "reallocated_funding", "new_funding", "cost_method",
                          "assumption_ids", "confidence", "cost_source_id",
                          "funding_split_basis", "overlap_group"],
    "BENEFICIARY_RECONCILIATION.csv": ["overlap_group", "unit", "programmes",
                                       "summed_reach", "overlap_factor",
                                       "unique_estimate", "note"],
    "COSTING_ASSUMPTIONS.csv": ["assumption_id", "programme_id", "cost_category",
                                "price_base_year", "cost_method", "confidence",
                                "basis_and_benchmark", "formula_status",
                                "cost_source_id", "funding_split_basis",
                                "years_1_2_central_rm_m", "years_3_4_central_rm_m",
                                "years_5_6_central_rm_m", "existing_share",
                                "reallocated_share", "new_share"],
    "DECISION_REGISTER.csv": ["decision_id", "category", "decision_text",
                              "what_it_authorises", "what_it_does_not_authorise",
                              "dependency", "responsible_owner", "completion_evidence"],
    "VALIDATION_REGISTER.csv": ["validation_id", "item", "classification", "criticality",
                                "accountable_owner", "supporting_agencies", "required_evidence",
                                "deadline", "escalation_route", "financial_consequence",
                                "decision_affected_if_unresolved", "status"],
    "LEGAL_ISSUES_REGISTER.csv": ["legal_issue_id", "domain", "legal_authority",
                                  "authority_source_ids", "legal_question",
                                  "provisional_design_position", "required_written_clearance",
                                  "clearance_owner", "consulted_bodies", "affected_programmes",
                                  "affected_decisions", "related_validation_ids",
                                  "consequence_if_unresolved", "clearance_stage", "status",
                                  "evidence_reference", "acceptance_date"],
    "FISCAL_VALIDATION_REGISTER.csv": ["fiscal_control_id", "domain",
                                       "validation_question", "provisional_model_position",
                                       "required_evidence", "validation_owner",
                                       "supporting_bodies", "affected_programmes",
                                       "affected_decisions", "related_validation_ids",
                                       "validation_stage", "consequence_if_unresolved",
                                       "status", "evidence_reference", "acceptance_date"],
    "PROGRAMME_DESIGN_REGISTER.csv": ["programme_id", "design_status", "exclusions",
                                       "delivery_channel", "geographic_coverage", "annual_volume",
                                       "volume_status", "complaints_and_appeals", "data_collected",
                                       "retention_and_access_rule", "key_dependencies", "stop_criteria",
                                       "redesign_criteria", "expansion_criteria", "signoff_owner",
                                       "signoff_status", "evidence_reference", "acceptance_date"],
    "SERVICE_COMMITMENT_REGISTER.csv": ["commitment_id", "commitment_name",
                                         "controlled_commitment", "applicability_rule",
                                         "affected_programmes", "implementation_point",
                                         "service_timeline_status", "service_timeline",
                                         "capacity_evidence_required", "standard_owner",
                                         "performance_measure", "reporting_frequency",
                                         "escalation_and_remedy", "excluded_outcomes",
                                         "adoption_status", "evidence_reference", "acceptance_date"],
    "GOVERNANCE_CONTINUITY_REGISTER.csv": ["continuity_id", "component",
                                             "controlled_rule", "primary_owner",
                                             "delegated_owner", "activation_trigger",
                                             "operating_cadence", "required_instrument",
                                             "authority_boundary", "evidence_requirement",
                                             "affected_programmes", "related_decisions",
                                             "related_controls", "status",
                                             "evidence_reference", "acceptance_date"],
    "COST_FORMULA_CONTROL_REGISTER.csv": ["formula_control_id", "programme_id",
                                             "assumption_id", "formula_status",
                                             "central_phase_1_direct_rm_m",
                                             "central_six_year_direct_rm_m",
                                             "ceiling_treatment", "required_evidence",
                                             "status", "evidence_reference", "acceptance_date"],
    "STAGE_TRACEABILITY_REGISTER.csv": ["requirement_id", "stage_id", "stage_name",
                                           "controlled_requirement", "prompt_provenance",
                                           "prompt_fidelity", "evidence_files",
                                           "verifier_checks", "pr_number", "head_commit",
                                           "merge_commit", "internal_status", "external_status"],
    "RENDERED_SUBMISSION_MANIFEST.csv": ["artifact_id", "canonical_sources",
                                             "canonical_source_bundle_sha256", "docx_file",
                                             "docx_sha256", "pdf_file", "pdf_sha256",
                                             "pdf_page_count", "render_status", "visual_qa_status"],
}

data = {}
print("=" * 78)
print("MIB 2.0 MACHINE VERIFICATION")
print("=" * 78)

# ---- CHECK 1: required columns in every canonical CSV ---------------------
for fname, cols in REQUIRED.items():
    rows = load(fname)
    data[fname] = rows
    if not rows:
        continue
    missing = [c for c in cols if c not in rows[0]]
    check(not missing,
          f"[1] {fname}: all {len(cols)} required columns present ({len(rows)} rows)",
          f"[1] {fname}: MISSING COLUMNS {missing}")

# ---- CHECK 1b: field-count integrity (catches unquoted commas shifting
#      every downstream column, which silently corrupts an entire row) -----
for fname in REQUIRED:
    path = os.path.join(HERE, fname)
    if not os.path.exists(path):
        continue
    with open(path, newline="", encoding="utf-8") as fh:
        raw = list(csv.reader(fh))
    if not raw:
        continue
    width = len(raw[0])
    ragged = [(i + 1, len(r)) for i, r in enumerate(raw[1:], start=1) if len(r) != width]
    check(not ragged,
          f"[1b] {fname}: all {len(raw) - 1} data rows have exactly {width} fields",
          f"[1b] {fname}: RAGGED ROWS (line, field_count) vs header width {width}: {ragged[:10]} "
          f"- almost certainly an unquoted comma shifting downstream columns")

# ---- CHECK 2: duplicate IDs and broken foreign keys ----------------------
ID_COL = {"SOURCE_REGISTER.csv": "source_id",
          "CLAIMS_AND_FIGURES_REGISTER.csv": "claim_id",
          "PROGRAMME_REGISTER.csv": "programme_id",
          "NARRATIVE_REGISTER.csv": "narrative_id",
          "CONFLICT_AND_DUPLICATION_REGISTER.csv": "conflict_id",
          "RESPONSIBILITY_MATRIX.csv": "responsibility_id",
          "KPI_REGISTER.csv": "kpi_id",
          "RISK_AND_SAFEGUARD_REGISTER.csv": "risk_id",
          "COSTING_MODEL.csv": "cost_line_id",
          "COSTING_ASSUMPTIONS.csv": "assumption_id",
          "BENEFICIARY_RECONCILIATION.csv": "overlap_group",
          "DECISION_REGISTER.csv": "decision_id",
          "VALIDATION_REGISTER.csv": "validation_id",
          "LEGAL_ISSUES_REGISTER.csv": "legal_issue_id",
          "FISCAL_VALIDATION_REGISTER.csv": "fiscal_control_id"}
ID_COL["PROGRAMME_DESIGN_REGISTER.csv"] = "programme_id"
ID_COL["SERVICE_COMMITMENT_REGISTER.csv"] = "commitment_id"
ID_COL["GOVERNANCE_CONTINUITY_REGISTER.csv"] = "continuity_id"
ID_COL["COST_FORMULA_CONTROL_REGISTER.csv"] = "formula_control_id"
ID_COL["STAGE_TRACEABILITY_REGISTER.csv"] = "requirement_id"
ID_COL["RENDERED_SUBMISSION_MANIFEST.csv"] = "artifact_id"
for fname, col in ID_COL.items():
    rows = data.get(fname, [])
    if not rows:
        continue
    ids = [r[col] for r in rows]
    dupes = [i for i, c in Counter(ids).items() if c > 1]
    check(not dupes, f"[2] {fname}: {len(ids)} unique IDs, no duplicates",
          f"[2] {fname}: DUPLICATE IDs {dupes}")

prog_ids = {r["programme_id"] for r in data.get("PROGRAMME_REGISTER.csv", [])}
retained = {r["programme_id"] for r in data.get("PROGRAMME_REGISTER.csv", [])
            if r["retain_decision"].upper().startswith("RETAIN")}
src_ids = {r["source_id"] for r in data.get("SOURCE_REGISTER.csv", [])}
conf_ids = {r["conflict_id"] for r in data.get("CONFLICT_AND_DUPLICATION_REGISTER.csv", [])}
kpi_ids = {r["kpi_id"] for r in data.get("KPI_REGISTER.csv", [])}
asm_ids = {r["assumption_id"] for r in data.get("COSTING_ASSUMPTIONS.csv", [])}

broken = []
for r in data.get("CLAIMS_AND_FIGURES_REGISTER.csv", []):
    for sid in filter(None, re.split(r"[;,]", r.get("source_id", ""))):
        if sid.strip() and sid.strip() not in src_ids:
            broken.append(f"{r['claim_id']}->source {sid.strip()}")
    cid = r.get("conflict_id", "").strip()
    if cid and cid not in conf_ids:
        broken.append(f"{r['claim_id']}->conflict {cid}")
for r in data.get("KPI_REGISTER.csv", []):
    if r["programme_id"] not in prog_ids:
        broken.append(f"{r['kpi_id']}->programme {r['programme_id']}")
for r in data.get("RESPONSIBILITY_MATRIX.csv", []):
    if r["programme_id"] not in prog_ids:
        broken.append(f"{r['responsibility_id']}->programme {r['programme_id']}")
for r in data.get("COSTING_MODEL.csv", []):
    pid = r["programme_id"]
    if not pid.startswith("PRG-XX") and pid not in prog_ids:
        broken.append(f"{r['cost_line_id']}->programme {pid}")
    for a in filter(None, re.split(r"[;,]", r["assumption_ids"])):
        if a.strip() and a.strip() not in asm_ids:
            broken.append(f"{r['cost_line_id']}->assumption {a.strip()}")
check(not broken, f"[2] foreign keys: all references resolve across 5 register pairs",
      f"[2] BROKEN FOREIGN KEYS: {broken[:12]}")

# ---- CHECK 3: material claims carry a source or assumption reference -----
MATERIAL = {"baseline_statistic", "budget_claim", "institutional_claim",
            "derived-estimate", "derived_estimate", "calculated_estimate", "causal_claim"}
unsourced = []
for r in data.get("CLAIMS_AND_FIGURES_REGISTER.csv", []):
    if r["claim_type"] in MATERIAL and r["verification_status"] not in (
            "unsupported", "rejected", "cited-source-not-yet-inspected"):
        if not r.get("source_id", "").strip() and not r.get("cited_source", "").strip():
            unsourced.append(r["claim_id"])
check(not unsourced,
      "[3] every material claim not marked unsupported/rejected/uninspected carries a source reference",
      f"[3] MATERIAL CLAIMS WITHOUT SOURCE: {unsourced}")

# ---- CHECK 4: recompute programme totals from phase values --------------
bad = []
for r in data.get("COSTING_MODEL.csv", []):
    s = D(r["years_1_2"]) + D(r["years_3_4"]) + D(r["years_5_6"])
    if abs(s - D(r["six_year_total"])) > TOL:
        bad.append(f"{r['cost_line_id']}: {s} != {r['six_year_total']}")
check(not bad, f"[4] all {len(data.get('COSTING_MODEL.csv', []))} cost lines: phases sum to six_year_total",
      f"[4] PHASE SUM MISMATCH: {bad[:10]}")

bad = []
for r in data.get("COSTING_MODEL.csv", []):
    s = D(r["existing_funding"]) + D(r["reallocated_funding"]) + D(r["new_funding"])
    if abs(s - D(r["six_year_total"])) > TOL:
        bad.append(f"{r['cost_line_id']}: funding {s} != total {r['six_year_total']}")
check(not bad, "[4] all cost lines: existing + reallocated + new equals six_year_total",
      f"[4] FUNDING SPLIT MISMATCH: {bad[:10]}")

cm_all = data.get("COSTING_MODEL.csv", [])
# ---- CHECK 4b: the model must equal its OWN STATED FORMULA --------------
#      Without this, the model only reconciles to itself: a hand-edited or
#      mis-derived amount passes every other numeric check.
asm = {r["assumption_id"]: r for r in data.get("COSTING_ASSUMPTIONS.csv", [])}
central = {r["programme_id"]: r for r in cm_all if r["scenario"] == "central"}
mismatch, partial = [], []
for aid, a in asm.items():
    if a["formula_status"] == "complete":
        derived = D(a["formula_derived_total_rm_m"])
        row = central.get(a["programme_id"])
        if row is None:
            mismatch.append(f"{aid}: no central cost line")
            continue
        if abs(derived - D(row["six_year_total"])) > TOL:
            mismatch.append(f"{aid}/{a['programme_id']}: formula {derived} != model {row['six_year_total']}")
        phases = D(a["years_1_2_central_rm_m"]) + D(a["years_3_4_central_rm_m"]) + D(a["years_5_6_central_rm_m"])
        if abs(phases - derived) > TOL:
            mismatch.append(f"{aid}: authored phases {phases} != formula {derived}")
    elif a["formula_status"] == "partial":
        partial.append(a["programme_id"])
check(not mismatch,
      f"[4b] every 'complete' formula row reproduces its model total exactly "
      f"({sum(1 for a in asm.values() if a['formula_status'] == 'complete')} rows tested)",
      f"[4b] MODEL DOES NOT EQUAL ITS OWN STATED FORMULA: {mismatch[:10]}")
check(len(partial) <= 2,
      f"[4b] only {len(partial)} programme(s) carry an incomplete formula and are declared 'partial': {partial}",
      f"[4b] too many un-derived cost rows: {partial}")

# ---- CHECK 4c: funding shares in the assumptions must sum to exactly 1 ---
badshare = [a["assumption_id"] for a in asm.values()
            if a["formula_status"] != "not_applicable"
            and abs((D(a["existing_share"]) + D(a["reallocated_share"]) + D(a["new_share"])) - Decimal("1")) > Decimal("0.0001")]
check(not badshare, f"[4c] funding shares sum to 1.0 for all {len(asm) - sum(1 for a in asm.values() if a['formula_status'] == 'not_applicable')} costed programmes",
      f"[4c] FUNDING SHARES DO NOT SUM TO 1.0: {badshare}")

# ---- CHECK 3b: CONFIDENCE DISCIPLINE (independent-critic C-03) -----------
#      'Benchmarked' means external unit-cost evidence exists. A row with no
#      cost_source_id may NOT claim it.
badconf = []
for a in data.get("COSTING_ASSUMPTIONS.csv", []):
    if a["formula_status"] == "not_applicable" and a["cost_category"] in ("derivation", "rate"):
        continue
    if a["confidence"] == "Benchmarked" and not a["cost_source_id"].strip():
        badconf.append(f"{a['assumption_id']}: Benchmarked with no cost_source_id")
    if a["confidence"] == "Confirmed":
        badconf.append(f"{a['assumption_id']}: claims Confirmed - requires authoritative "
                       f"programme/financial/procurement data, which this package does not hold")
    sid = a["cost_source_id"].strip()
    if sid and sid not in src_ids:
        badconf.append(f"{a['assumption_id']}: cost_source_id {sid} not in SOURCE_REGISTER")
check(not badconf,
      f"[3b] confidence discipline: every 'Benchmarked' row carries a resolvable cost_source_id; "
      f"no row claims 'Confirmed'",
      f"[3b] UNSOURCED CONFIDENCE CLAIMS: {badconf[:10]}")

# ---- CHECK 4d: every costed row documents its funding split (critic C-04) -
nobasis = [a["assumption_id"] for a in data.get("COSTING_ASSUMPTIONS.csv", [])
           if a["programme_id"].startswith("PRG-")
           and a["cost_category"] not in ("derivation", "rate")
           and len(a["funding_split_basis"].strip()) < 40]
check(not nobasis,
      f"[4d] all {sum(1 for a in data.get('COSTING_ASSUMPTIONS.csv', []) if a['programme_id'].startswith('PRG-') and a['cost_category'] not in ('derivation', 'rate'))} "
      f"costed programmes document the basis of their existing/reallocated/new split",
      f"[4d] FUNDING SPLIT UNDOCUMENTED: {nobasis}")

# ---- CHECK 8b: reach vs unique beneficiaries actually modelled (C-06) ----
br = data.get("BENEFICIARY_RECONCILIATION.csv", [])
prob = []
for r in br:
    summed, f, uniq = D(r["summed_reach"]), D(r["overlap_factor"]), D(r["unique_estimate"])
    expected = (summed * (Decimal("1") - f)).quantize(Decimal("1"))
    if abs(uniq - expected) > Decimal("1"):
        prob.append(f"{r['overlap_group']}: {uniq} != {expected}")
    if uniq > summed:
        prob.append(f"{r['overlap_group']}: unique exceeds reach")
check(br and not prob,
      f"[8b] reach and unique beneficiaries are modelled separately across "
      f"{len(br)} overlap groups and reconcile against the ASM-030 factor",
      f"[8b] BENEFICIARY RECONCILIATION BROKEN: {prob or 'file absent or empty'}")
units = {r["unit"] for r in br}
check(len(units) == len(br),
      f"[8b] each overlap group uses a distinct unit ({sorted(units)}) - reach is never "
      f"summed across groups",
      f"[8b] overlap groups share a unit, so reach could be wrongly summed: {units}")

# ---- CHECK 2b: ASM-xxx and VAL-xx references resolve (critic M-12) -------
import glob as _glob
asm_defined = set(asm_ids)
val_defined = {r["validation_id"] for r in data.get("VALIDATION_REGISTER.csv", [])}
adpath = os.path.join(HERE, "ASSUMPTIONS_AND_DECISIONS.md")
if os.path.exists(adpath):
    ad = open(adpath, encoding="utf-8").read()
    asm_defined |= set(re.findall(r"\|\s*(ASM-\d{3})\s*\|", ad))
dangling = set()
for f in _glob.glob(os.path.join(HERE, "*.csv")) + _glob.glob(os.path.join(HERE, "*.md")):
    txt = open(f, encoding="utf-8").read()
    for m in re.findall(r"\bASM-[0-9C]\d{2}\b", txt):
        if m not in asm_defined:
            dangling.add(f"{os.path.basename(f)}:{m}")
    for m in re.findall(r"\bVAL-\d{2}\b", txt):
        if m not in val_defined:
            dangling.add(f"{os.path.basename(f)}:{m}")
check(not dangling,
      f"[2b] all ASM-xxx and VAL-xx references across every CSV and Markdown file resolve "
      f"to a definition ({len(asm_defined)} assumptions, {len(val_defined)} validation items)",
      f"[2b] DANGLING REFERENCES: {sorted(dangling)[:12]}")

# ---- CHECK 5 & 6: reconcile totals across every required dimension ------
cm = data.get("COSTING_MODEL.csv", [])
scenarios = sorted({r["scenario"] for r in cm})
grand = {}
for scen in scenarios:
    rows = [r for r in cm if r["scenario"] == scen]
    grand[scen] = sum(D(r["six_year_total"]) for r in rows)
    dims = {"programme": "programme_id", "pillar": "pillar",
            "ministry": "lead_ministry", "cost_category": "cost_category"}
    for label, col in dims.items():
        agg = defaultdict(Decimal)
        for r in rows:
            agg[r[col]] += D(r["six_year_total"])
        check(abs(sum(agg.values()) - grand[scen]) <= TOL,
              f"[5] {scen}: reconciles by {label} ({len(agg)} groups) = RM {grand[scen]:,.3f}m",
              f"[5] {scen}: {label} totals do not reconcile")
    phase_sum = sum(D(r[k]) for r in rows for k in ("years_1_2", "years_3_4", "years_5_6"))
    check(abs(phase_sum - grand[scen]) <= TOL,
          f"[5] {scen}: reconciles by phase = RM {grand[scen]:,.3f}m",
          f"[5] {scen}: phase totals do not reconcile")
    ftype = sum(D(r[k]) for r in rows
                for k in ("existing_funding", "reallocated_funding", "new_funding"))
    check(abs(ftype - grand[scen]) <= TOL,
          f"[5] {scen}: reconciles by funding type = RM {grand[scen]:,.3f}m",
          f"[5] {scen}: funding-type totals do not reconcile")

check(len(scenarios) == 3 and grand.get("conservative", 0) < grand.get("central", 0) < grand.get("expanded", 0),
      f"[6] three scenarios present and strictly ordered: "
      f"conservative RM {grand.get('conservative', 0):,.3f}m < central RM {grand.get('central', 0):,.3f}m "
      f"< expanded RM {grand.get('expanded', 0):,.3f}m",
      f"[6] SCENARIO SET INVALID: {grand}")

# ---- CHECK 7: negative values, malformed numbers, unexplained blanks ----
NUMCOLS = ["years_1_2", "years_3_4", "years_5_6", "six_year_total",
           "existing_funding", "reallocated_funding", "new_funding"]
bad = []
for r in cm:
    for c in NUMCOLS:
        v = D(r[c])
        if v is None:
            bad.append(f"{r['cost_line_id']}.{c} malformed")
        elif v < 0:
            bad.append(f"{r['cost_line_id']}.{c} negative ({v})")
check(not bad, f"[7] no negative or malformed numbers across {len(cm) * len(NUMCOLS)} numeric cells",
      f"[7] BAD NUMBERS: {bad[:10]}")

blanks = []
for fname, cols in REQUIRED.items():
    for r in data.get(fname, []):
        rid = r.get(ID_COL[fname], "?")
        if fname == "PROGRAMME_REGISTER.csv" and not r["retain_decision"].upper().startswith("RETAIN"):
            continue  # rejected programmes legitimately carry '-' placeholders
        for c in cols:
            # cost_source_id is legitimately empty: blank means "no external unit-cost
            # source exists", which check [3b] then forces to confidence=Provisional.
            if c == "cost_source_id":
                continue
            # These two fields are intentionally blank while a legal issue is
            # open/requested. Check [14] requires both once a competent
            # authority records a disposition.
            if fname in {"LEGAL_ISSUES_REGISTER.csv", "FISCAL_VALIDATION_REGISTER.csv", "PROGRAMME_DESIGN_REGISTER.csv", "SERVICE_COMMITMENT_REGISTER.csv", "GOVERNANCE_CONTINUITY_REGISTER.csv", "COST_FORMULA_CONTROL_REGISTER.csv"} and c in {"evidence_reference", "acceptance_date"}:
                continue
            if not str(r.get(c, "")).strip():
                blanks.append(f"{fname}:{rid}.{c}")
check(not blanks, "[7] no unexplained blanks in required fields of any canonical register",
      f"[7] BLANK REQUIRED FIELDS: {blanks[:15]}")

# ---- CHECK 8: duplicate programme-beneficiary combinations --------------
combos = defaultdict(list)
for r in data.get("PROGRAMME_REGISTER.csv", []):
    if r["retain_decision"].upper().startswith("RETAIN"):
        combos[(r["target_group"].strip().lower(), r["delivery_mechanism"].strip().lower()[:60])].append(r["programme_id"])
overlaps = {k: v for k, v in combos.items() if len(v) > 1}
check(not overlaps,
      f"[8] no identical target-group + delivery-mechanism pairs among {len(retained)} retained programmes "
      f"(portfolio overlap treated explicitly at ASM-030)",
      f"[8] DUPLICATE PROGRAMME-BENEFICIARY COMBINATIONS requiring double-count review: {overlaps}")

# ---- CHECK 9: every retained programme has owner, phase, KPI, outcome, cost
missing = []
costed = {r["programme_id"] for r in cm}
kpi_by_prog = {r["programme_id"] for r in data.get("KPI_REGISTER.csv", [])}
resp_by_prog = {r["programme_id"] for r in data.get("RESPONSIBILITY_MATRIX.csv", [])}
for r in data.get("PROGRAMME_REGISTER.csv", []):
    if not r["retain_decision"].upper().startswith("RETAIN"):
        continue
    pid = r["programme_id"]
    if not r["proposed_owner"].strip() or pid not in resp_by_prog:
        missing.append(f"{pid}: owner")
    if not r["phase"].strip():
        missing.append(f"{pid}: phase")
    if pid not in kpi_by_prog:
        missing.append(f"{pid}: KPI")
    if not r["outcome"].strip():
        missing.append(f"{pid}: outcome")
    if pid not in costed:
        missing.append(f"{pid}: cost treatment")
    if r["cost_status"] not in ("Confirmed", "Benchmarked", "Provisional"):
        missing.append(f"{pid}: invalid cost_status '{r['cost_status']}'")
check(not missing,
      f"[9] all {len(retained)} retained programmes have owner, phase, KPI, outcome and a cost treatment",
      f"[9] INCOMPLETE RETAINED PROGRAMMES: {missing}")

# ---- CHECK 10: figures in the proposal map to a claim ID ----------------
prop = os.path.join(HERE, "MIB_2.0_EXECUTIVE_PROPOSAL.md")
if os.path.exists(prop):
    text = open(prop, encoding="utf-8").read()
    cited = set(re.findall(r"\b(CLM-\d{3})\b", text))
    known = {r["claim_id"] for r in data.get("CLAIMS_AND_FIGURES_REGISTER.csv", [])}
    unknown = cited - known
    check(not unknown, f"[10] proposal cites {len(cited)} claim IDs, all resolving to the register",
          f"[10] PROPOSAL CITES UNKNOWN CLAIM IDs: {sorted(unknown)}")
    rejected = {r["claim_id"] for r in data.get("CLAIMS_AND_FIGURES_REGISTER.csv", [])
                if r["verification_status"] in ("rejected", "unsupported")}
    # A rejected claim may be cited only in an explicitly corrective context.
    bad_cites = []
    for cid in sorted(cited & rejected):
        for m in re.finditer(re.escape(cid), text):
            window = text[max(0, m.start() - 400):m.end() + 200].lower()
            if not any(w in window for w in ("reject", "unsupported", "not carried",
                                             "removed", "cannot be", "corrected",
                                             "does not appear", "no basis", "withdraw",
                                             "could not be substantiated", "never existed",
                                             "not adopted", "not supported",
                                             "could not be established", "not established",
                                             "no evidential basis", "did not survive",
                                             "not sustainable", "not proposed")):
                bad_cites.append(cid)
                break
    check(not bad_cites,
          f"[10] {len(cited & rejected)} rejected/unsupported claims appear only in explicitly corrective context",
          f"[10] REJECTED CLAIMS USED AS EVIDENCE: {bad_cites}")
    check(len(cited) >= 25,
          f"[10] proposal traceability density: {len(cited)} distinct claim IDs cited",
          f"[10] proposal cites only {len(cited)} claim IDs - insufficient traceability", hard=False)
else:
    SOFT_WARNINGS.append("[10] proposal not yet written - traceability check deferred")

# ---- CHECK 11: scenario definition consistency --------------------------
by_prog = defaultdict(dict)
for r in cm:
    by_prog[r["programme_id"]][r["scenario"]] = r
inconsistent = []
for pid, d in by_prog.items():
    if set(d) != set(scenarios):
        inconsistent.append(f"{pid}: scenarios {sorted(d)}")
        continue
    base = d["central"]
    for scen in scenarios:
        for col in ("cost_category", "pillar", "lead_ministry", "assumption_ids",
                    "confidence", "price_base_year"):
            if d[scen][col] != base[col]:
                inconsistent.append(f"{pid}/{scen}: {col} differs from central")
check(not inconsistent,
      f"[11] all {len(by_prog)} cost-line groups use identical definitions across all three scenarios "
      f"(scenarios are sensitivity cases, not alternative blueprints)",
      f"[11] SCENARIO DEFINITION DRIFT: {inconsistent[:10]}")

# ---- extra: confidence discipline ---------------------------------------
confidences = Counter(r["confidence"] for r in cm)
check(set(confidences) <= {"Confirmed", "Benchmarked", "Provisional"},
      f"[11] confidence classes valid: {dict(confidences)}",
      f"[11] INVALID CONFIDENCE CLASS: {set(confidences)}")

central_rows = [r for r in cm if r["scenario"] == "central"]
prov = sum(D(r["six_year_total"]) for r in central_rows if r["confidence"] == "Provisional")
conf = sum(D(r["six_year_total"]) for r in central_rows if r["confidence"] == "Confirmed")
tot = sum(D(r["six_year_total"]) for r in central_rows)
PASSED.append(f"[11] central portfolio confidence mix: Confirmed RM {conf:,.3f}m ({conf / tot * 100:.1f}%), "
              f"Provisional RM {prov:,.3f}m ({prov / tot * 100:.1f}%), "
              f"Benchmarked RM {tot - prov - conf:,.3f}m ({(tot - prov - conf) / tot * 100:.1f}%)")

# ---- extra: unresolved conflicts ----------------------------------------
unresolved = [r["conflict_id"] for r in data.get("CONFLICT_AND_DUPLICATION_REGISTER.csv", [])
              if r["status"].strip().lower() != "resolved"]
check(not unresolved, f"[extra] all {len(conf_ids)} registered conflicts marked resolved",
      f"[extra] UNRESOLVED CONFLICTS: {unresolved}", hard=False)

# ---- extra: canonical file presence -------------------------------------
CANON = ["BENEFICIARY_RECONCILIATION.csv", "STATUS.md", "ASSUMPTIONS_AND_DECISIONS.md", "AUDIT_LOG.md", "CRITIC_FINDINGS.md",
         "FINAL_QA_REPORT.md", "SOURCE_REGISTER.csv", "CLAIMS_AND_FIGURES_REGISTER.csv",
         "PROGRAMME_REGISTER.csv", "NARRATIVE_REGISTER.csv",
         "CONFLICT_AND_DUPLICATION_REGISTER.csv", "RESPONSIBILITY_MATRIX.csv",
         "KPI_REGISTER.csv", "RISK_AND_SAFEGUARD_REGISTER.csv", "COSTING_MODEL.csv",
         "COSTING_ASSUMPTIONS.csv", "DECISION_REGISTER.csv", "VALIDATION_REGISTER.csv", "LEGAL_ISSUES_REGISTER.csv", "FISCAL_VALIDATION_REGISTER.csv", "PROGRAMME_DESIGN_REGISTER.csv", "PROGRAMME_DESIGN_SHEETS.md", "SERVICE_COMMITMENT_REGISTER.csv", "SERVICE_COMMITMENTS.md", "GOVERNANCE_CONTINUITY_REGISTER.csv", "GOVERNANCE_CONTINUITY.md", "COST_FORMULA_CONTROL_REGISTER.csv", "STAGE_TRACEABILITY_REGISTER.csv", "STAGE_1_8_REQUIREMENTS.md", "CROSS_STAGE_ASSURANCE_REPORT.md", "verify_outputs.py", "VERIFICATION_RESULTS.md",
         "STAGE_1_DIAGNOSTIC.md", "STAGE_2_RECONCILIATION.md",
         "MIB_2.0_EXECUTIVE_PROPOSAL.md", "TECHNICAL_ANNEXES.md",
         "MIB_2.0_CABINET_SUBMISSION.docx", "MIB_2.0_CABINET_SUBMISSION.pdf",
         "RENDERED_SUBMISSION_MANIFEST.csv", "build_submission_documents.py",
         "build_rendered_manifest.py"]
absent = [f for f in CANON if not os.path.exists(os.path.join(HERE, f))
          or os.path.getsize(os.path.join(HERE, f)) == 0]
check(not absent, f"[extra] all {len(CANON)} canonical files exist and are non-empty",
      f"[extra] MISSING OR EMPTY CANONICAL FILES: {absent}", hard=False)

# ---- CHECK 12: generated document sections match canonical registers -----
# Financial tables in the proposal and annex must never be maintained by
# hand.  Compare the committed text with a fresh render from the CSV model.
from sync_document_integrity import expected_sections, render_programme_design_sheets, render_service_commitments, render_governance_continuity, START, END


def generated_block(document, name):
    start = START.format(name=name)
    end = END.format(name=name)
    if start not in document or end not in document:
        return None
    return start + document.split(start, 1)[1].split(end, 1)[0] + end


proposal_text = open(prop, encoding="utf-8").read() if os.path.exists(prop) else ""
annex_path = os.path.join(HERE, "TECHNICAL_ANNEXES.md")
annex_text = open(annex_path, encoding="utf-8").read() if os.path.exists(annex_path) else ""
assumptions_text = open(adpath, encoding="utf-8").read() if os.path.exists(adpath) else ""
expected = expected_sections()
stale = []
for section_name, rendered in expected.items():
    if section_name in {"TECHNICAL_ANNEX_A", "PHASE_1_FISCAL_SCHEDULE"}:
        document = annex_text
    elif section_name in {"VALIDATION_REGISTER", "LEGAL_ISSUES_REGISTER", "FISCAL_VALIDATION_REGISTER"}:
        document = assumptions_text
    else:
        document = proposal_text
    if generated_block(document, section_name) != rendered:
        stale.append(section_name)
check(not stale,
      f"[12] all {len(expected)} generated proposal/annex sections exactly match the canonical CSV registers",
      f"[12] STALE OR MANUALLY EDITED GENERATED SECTIONS: {stale}; run sync_document_integrity.py")

# ---- CHECK 12a: decision scope is explicit and fiscally non-operative ----
decision_rows = data.get("DECISION_REGISTER.csv", [])
decision_categories = Counter(row["category"] for row in decision_rows)
expected_decision_categories = {
    "approve_now": 5,
    "conditional_endorsement": 4,
    "not_for_approval_now": 7,
}
decision_defects = []
if decision_categories != expected_decision_categories:
    decision_defects.append(
        f"category counts {dict(decision_categories)} != {expected_decision_categories}"
    )
expected_prefix = {
    "approve_now": "AN-",
    "conditional_endorsement": "CE-",
    "not_for_approval_now": "NA-",
}
for row in decision_rows:
    prefix = expected_prefix.get(row["category"])
    if prefix is None or not row["decision_id"].startswith(prefix):
        decision_defects.append(
            f"{row['decision_id']}: ID/category mismatch for {row['category']}"
        )

approve_effect = " ".join(
    row["decision_text"] + " " + row["what_it_authorises"]
    for row in decision_rows if row["category"] == "approve_now"
).lower()
for forbidden in ("approve the final six-year fiscal envelope", "any new design or validation appropriation",
                  "creation of the proposed 35 permanent secretariat posts"):
    if forbidden in approve_effect:
        decision_defects.append(f"approve-now scope contains forbidden operative effect: {forbidden}")

exclusions = " ".join(
    row["decision_text"] + " " + row["what_it_does_not_authorise"]
    for row in decision_rows if row["category"] == "not_for_approval_now"
).lower()
exclusions_normalized = re.sub(r"[^a-z0-9]+", " ", exclusions).strip()
required_exclusions = (
    "final six-year fiscal envelope",
    "ministry reallocations",
    "years 3–6 appropriation",
    "pnb participation",
    "states local authorities trustees or religious authorities",
    "targets whose baselines are not verified",
)
for subject in required_exclusions:
    subject_normalized = re.sub(r"[^a-z0-9]+", " ", subject).strip()
    if subject_normalized not in exclusions_normalized:
        decision_defects.append(f"missing explicit no-approval subject: {subject}")

central_total = grand.get("central", Decimal(0))
central_reallocated = sum(
    D(row["existing_funding"]) + D(row["reallocated_funding"])
    for row in cm if row["scenario"] == "central"
)
phase_1_total = sum(D(row["years_1_2"]) for row in cm if row["scenario"] == "central")
decision_text_all = "\n".join(" | ".join(row.values()) for row in decision_rows)
for amount, label in (
    (central_total, "central total"),
    (central_reallocated, "existing/reallocated total"),
):
    if f"RM{amount:,.3f} million" not in decision_text_all:
        decision_defects.append(f"{label} RM{amount:,.3f}m is not model-derived in decision register")
if f"RM{phase_1_total:,.1f} million" not in decision_text_all:
    decision_defects.append(
        f"Phase 1 amount RM{phase_1_total:,.1f}m is not model-derived in decision register"
    )

obsolete_decision_language = (
    "approve in principle the funding framework",
    "approval in principle of the fiscal framework",
    "d1–d6",
)
for phrase in obsolete_decision_language:
    if phrase in proposal_text.lower():
        decision_defects.append(f"proposal retains obsolete decision language: {phrase}")

check(not decision_defects,
      "[12a] decision register separates 5 operative approvals, 4 conditional endorsements and 7 express deferrals; no fiscal or implementation authority is implied",
      f"[12a] DECISION-SCOPE DEFECTS: {decision_defects[:15]}")

# ---- CHECK 12b: narrative counts match the canonical registers -----------
programme_rows = data.get("PROGRAMME_REGISTER.csv", [])
retained_count = sum(r["retain_decision"].upper().startswith("RETAIN") for r in programme_rows)
non_retained_count = len(programme_rows) - retained_count
risk_rows = data.get("RISK_AND_SAFEGUARD_REGISTER.csv", [])
critical_count = sum(r["inherent_rating"] == "Critical" for r in risk_rows)
high_residual_count = sum(r["residual_rating"] == "High" for r in risk_rows)
kpi_rows = data.get("KPI_REGISTER.csv", [])
baseline_pending_count = sum(r.get("baseline_status") == "to-be-established" for r in kpi_rows)
responsibility_rows = data.get("RESPONSIBILITY_MATRIX.csv", [])
mandate_counts = Counter(r["mandate_verification_status"] for r in responsibility_rows)

count_drift = []
required_proposal_phrases = [
    f"sixteen retained substantive programmes" if retained_count == 16 else f"{retained_count} retained substantive programmes",
    f"Five source proposals were not carried forward" if non_retained_count == 5 else f"{non_retained_count} source proposals were not carried forward",
    f"Twenty-one risks are registered" if len(risk_rows) == 21 else f"{len(risk_rows)} risks are registered",
    f"Fourteen carry a **critical inherent rating**" if critical_count == 14 else f"{critical_count} carry a **critical inherent rating**",
    f"Twelve of the sixteen have a baseline status" if baseline_pending_count == 12 and len(kpi_rows) == 16 else f"{baseline_pending_count} of the {len(kpi_rows)} have a baseline status",
    "The thirty validation items are not one undifferentiated condition",
]
for phrase in required_proposal_phrases:
    if phrase not in proposal_text:
        count_drift.append(f"proposal missing canonical count statement: {phrase}")

required_annex_phrases = [
    f"`RISK_AND_SAFEGUARD_REGISTER.csv` ({len(risk_rows)} rows)",
    f"{critical_count} carry critical inherent ratings",
    f"{high_residual_count} retain a High residual rating",
    f"`SOURCE_REGISTER.csv` ({len(data.get('SOURCE_REGISTER.csv', []))} sources)",
    f"`CLAIMS_AND_FIGURES_REGISTER.csv` ({len(data.get('CLAIMS_AND_FIGURES_REGISTER.csv', []))} claims)",
    f"Mandate verification status: {mandate_counts.get('mandate-consistent-requires-confirmation', 0)} consistent-requires-confirmation, {mandate_counts.get('mandate-requires-establishment', 0)} requires-establishment",
]
for phrase in required_annex_phrases:
    if phrase not in annex_text:
        count_drift.append(f"annex missing canonical count statement: {phrase}")

ad_text = open(adpath, encoding="utf-8").read() if os.path.exists(adpath) else ""
validation_rows = data.get("VALIDATION_REGISTER.csv", [])
validation_ids = [row["validation_id"] for row in validation_rows]
strict_ids = {row["validation_id"] for row in validation_rows if row["criticality"] == "strict_gate"}
expected_strict_ids = {"VAL-01", "VAL-09", "VAL-11", "VAL-19", "VAL-23", "VAL-30"}
if len(validation_ids) != 30 or len(set(validation_ids)) != 30:
    count_drift.append(f"validation register has {len(validation_ids)} rows / {len(set(validation_ids))} unique IDs, expected 30")
if strict_ids != expected_strict_ids:
    count_drift.append(f"strict validation gates are {sorted(strict_ids)}, expected {sorted(expected_strict_ids)}")
check(not count_drift,
      "[12b] programme, KPI, risk, mandate, source, claim and validation counts in narrative match their canonical registers",
      f"[12b] NARRATIVE COUNT DRIFT: {count_drift[:12]}")

# ---- CHECK 13: Stage 3 validation control architecture -------------------
allowed_classes = {
    "pre_submission_gate", "programme_launch_gate", "phase_expansion_gate",
    "operational_baseline", "deferrable_design_matter",
}
allowed_criticality = {"strict_gate", "decision_dependent_critical", "standard"}
allowed_status = {"open", "requested", "received", "accepted", "disputed"}
expected_conditional_ids = {"VAL-03", "VAL-24", "VAL-27", "VAL-28"}
decision_ids = {row["decision_id"] for row in decision_rows}
validation_defects = []
required_detail_fields = (
    "item", "accountable_owner", "supporting_agencies", "required_evidence", "deadline",
    "escalation_route", "financial_consequence", "decision_affected_if_unresolved", "status",
)
for row in validation_rows:
    vid = row["validation_id"]
    if row["classification"] not in allowed_classes:
        validation_defects.append(f"{vid}: invalid classification {row['classification']!r}")
    if row["criticality"] not in allowed_criticality:
        validation_defects.append(f"{vid}: invalid criticality {row['criticality']!r}")
    if row["status"] not in allowed_status:
        validation_defects.append(f"{vid}: invalid status {row['status']!r}")
    for field in required_detail_fields:
        if not row[field].strip():
            validation_defects.append(f"{vid}: blank {field}")
    affected = {item.strip() for item in row["decision_affected_if_unresolved"].split(";") if item.strip()}
    unknown = affected - decision_ids
    if not affected or unknown:
        validation_defects.append(f"{vid}: affected decisions unresolved or unknown {sorted(unknown)}")

conditional_ids = {
    row["validation_id"] for row in validation_rows
    if row["criticality"] == "decision_dependent_critical"
}
if conditional_ids != expected_conditional_ids:
    validation_defects.append(
        f"decision-dependent critical IDs are {sorted(conditional_ids)}, expected {sorted(expected_conditional_ids)}"
    )
class_counts = Counter(row["classification"] for row in validation_rows)
if set(class_counts) != allowed_classes or any(not class_counts[key] for key in allowed_classes):
    validation_defects.append(f"classification coverage incomplete: {dict(class_counts)}")
if "No-cascade rule" not in proposal_text:
    validation_defects.append("proposal lacks the no-cascade rule")
if "Received` does not mean accepted" not in ad_text:
    validation_defects.append("validation register lacks received-versus-accepted status control")

check(not validation_defects,
      "[13] all 30 validation items have one classification, criticality, owner, evidence, deadline, escalation, financial consequence, affected decisions and controlled status",
      f"[13] VALIDATION CONTROL DEFECTS: {validation_defects[:20]}")
check(strict_ids == expected_strict_ids and conditional_ids == expected_conditional_ids,
      "[13a] six strict gates and four decision-dependent critical items match the approved Stage 3 control set",
      f"[13a] VALIDATION CRITICALITY DRIFT: strict={sorted(strict_ids)} conditional={sorted(conditional_ids)}")
check(sum(class_counts.values()) == 30 and len(class_counts) == 5,
      f"[13b] all 30 validation items are distributed across all five gate classifications ({dict(class_counts)})",
      f"[13b] VALIDATION CLASSIFICATION DRIFT: {dict(class_counts)}")

# ---- CHECK 14: Stage 4 legal and jurisdictional clearance matrix --------
legal_rows = data.get("LEGAL_ISSUES_REGISTER.csv", [])
legal_ids = {row["legal_issue_id"] for row in legal_rows}
allowed_legal_stages = {"pre_submission_clearance", "programme_launch_clearance"}
allowed_legal_status = {
    "open", "requested", "received", "cleared", "cleared_with_conditions",
    "not_cleared", "superseded",
}
legal_defects = []
required_legal_fields = (
    "domain", "legal_authority", "authority_source_ids", "legal_question",
    "provisional_design_position", "required_written_clearance", "clearance_owner",
    "consulted_bodies", "affected_programmes", "affected_decisions",
    "related_validation_ids", "consequence_if_unresolved", "clearance_stage", "status",
)
for row in legal_rows:
    lid = row["legal_issue_id"]
    for field in required_legal_fields:
        if not row[field].strip():
            legal_defects.append(f"{lid}: blank {field}")
    if row["clearance_stage"] not in allowed_legal_stages:
        legal_defects.append(f"{lid}: invalid clearance stage {row['clearance_stage']!r}")
    if row["status"] not in allowed_legal_status:
        legal_defects.append(f"{lid}: invalid status {row['status']!r}")
    source_refs = {item.strip() for item in row["authority_source_ids"].split(";") if item.strip()}
    unknown_sources = source_refs - src_ids
    if not source_refs or unknown_sources:
        legal_defects.append(f"{lid}: authority sources missing or unknown {sorted(unknown_sources)}")
    programme_refs = {item.strip() for item in row["affected_programmes"].split(";") if item.strip()}
    unknown_programmes = programme_refs - retained
    if not programme_refs or unknown_programmes:
        legal_defects.append(f"{lid}: affected programmes missing or not retained {sorted(unknown_programmes)}")
    affected_decisions = {item.strip() for item in row["affected_decisions"].split(";") if item.strip()}
    unknown_decisions = affected_decisions - decision_ids
    if not affected_decisions or unknown_decisions:
        legal_defects.append(f"{lid}: affected decisions missing or unknown {sorted(unknown_decisions)}")
    related_validation = {item.strip() for item in row["related_validation_ids"].split(";") if item.strip()}
    unknown_validation = related_validation - set(validation_ids)
    if not related_validation or unknown_validation:
        legal_defects.append(f"{lid}: validation controls missing or unknown {sorted(unknown_validation)}")
    evidence = row["evidence_reference"].strip()
    accepted = row["acceptance_date"].strip()
    disposition_status = {"cleared", "cleared_with_conditions", "not_cleared", "superseded"}
    if row["status"] in disposition_status and (not evidence or not accepted):
        legal_defects.append(f"{lid}: disposition status lacks evidence reference or acceptance date")
    if row["status"] in {"open", "requested"} and (evidence or accepted):
        legal_defects.append(f"{lid}: {row['status']} item improperly carries disposition evidence/date")

expected_legal_ids = {f"LGL-{number:02d}" for number in range(1, 19)}
if legal_ids != expected_legal_ids:
    legal_defects.append(f"legal IDs are {sorted(legal_ids)}, expected LGL-01 to LGL-18")
legal_stage_counts = Counter(row["clearance_stage"] for row in legal_rows)
if legal_stage_counts != Counter({"pre_submission_clearance": 10, "programme_launch_clearance": 8}):
    legal_defects.append(f"clearance-stage distribution drift: {dict(legal_stage_counts)}")
covered_programmes = {
    item.strip()
    for row in legal_rows
    for item in row["affected_programmes"].split(";")
    if item.strip()
}
if covered_programmes != retained:
    legal_defects.append(f"legal coverage does not equal all retained programmes: missing {sorted(retained - covered_programmes)}")

authority_text = " ".join(row["legal_authority"] for row in legal_rows)
for required_authority in (
    "Article 8", "Article 12(1)", "136", "153", "Act 709",
    "Ninth Schedule", "Act 882", "Act 61", "Act 78", "Act 299",
):
    if required_authority not in authority_text:
        legal_defects.append(f"matrix lacks required controlling authority {required_authority}")

prg04_pathway_ids = {"LGL-13", "LGL-14", "LGL-15", "LGL-16", "LGL-17", "LGL-18"}
if not prg04_pathway_ids <= legal_ids:
    legal_defects.append(f"PRG-04 pathway issues missing {sorted(prg04_pathway_ids - legal_ids)}")
for row in legal_rows:
    if row["legal_issue_id"] in prg04_pathway_ids:
        if row["affected_programmes"] != "PRG-04" or "VAL-13" not in row["related_validation_ids"]:
            legal_defects.append(f"{row['legal_issue_id']}: PRG-04 pathway mapping drift")

if "No issue is recorded as cleared" not in proposal_text:
    legal_defects.append("proposal lacks express no-clearance statement")
if "Government Procurement Act 2026" not in proposal_text or "transitional instruments" not in proposal_text:
    legal_defects.append("proposal lacks current Act 882 commencement/transitional control")
if "This drafting exercise has obtained **no legal clearance**" not in annex_text:
    legal_defects.append("technical annex lacks express no-clearance statement")

check(not legal_defects,
      "[14] all 18 legal issues have authorities, questions, provisional boundaries, competent owners, written-clearance requirements, programme/decision/validation mappings and unresolved consequences",
      f"[14] LEGAL ISSUES MATRIX DEFECTS: {legal_defects[:24]}")
check(legal_stage_counts == Counter({"pre_submission_clearance": 10, "programme_launch_clearance": 8}),
      "[14a] legal issues are controlled as 10 pre-submission and 8 programme-launch clearances",
      f"[14a] LEGAL CLEARANCE-STAGE DRIFT: {dict(legal_stage_counts)}")
check(all(
          not (row["status"] in {"cleared", "cleared_with_conditions", "not_cleared", "superseded"}
               and (not row["evidence_reference"].strip() or not row["acceptance_date"].strip()))
          and not (row["status"] in {"open", "requested"}
                   and (row["evidence_reference"].strip() or row["acceptance_date"].strip()))
          for row in legal_rows),
      "[14b] no legal clearance is implied without written evidence and an acceptance date",
      "[14b] ONE OR MORE LEGAL ISSUES IMPROPERLY IMPLY CLEARANCE")
check(prg04_pathway_ids <= legal_ids,
      "[14c] PRG-04 has six separate pathway clearances for public purpose, consent, Islamic administration, legacy referrals, excluded expenditure and religion-data handling",
      f"[14c] PRG-04 LEGAL PATHWAY COVERAGE MISSING: {sorted(prg04_pathway_ids - legal_ids)}")

# ---- CHECK 15: Stage 5 Phase 1 fiscal validation architecture -----------
fiscal_rows = data.get("FISCAL_VALIDATION_REGISTER.csv", [])
fiscal_ids = {row["fiscal_control_id"] for row in fiscal_rows}
expected_fiscal_ids = {f"FIS-{number:02d}" for number in range(1, 11)}
allowed_fiscal_stages = {"phase_1_ceiling_gate", "programme_cost_gate", "later_phase_gate"}
allowed_fiscal_status = {
    "open", "requested", "received", "validated", "validated_with_conditions",
    "rejected", "superseded",
}
fiscal_defects = []
required_fiscal_fields = (
    "domain", "validation_question", "provisional_model_position", "required_evidence",
    "validation_owner", "supporting_bodies", "affected_programmes", "affected_decisions",
    "related_validation_ids", "validation_stage", "consequence_if_unresolved", "status",
)
for row in fiscal_rows:
    fid = row["fiscal_control_id"]
    for field in required_fiscal_fields:
        if not row[field].strip():
            fiscal_defects.append(f"{fid}: blank {field}")
    if row["validation_stage"] not in allowed_fiscal_stages:
        fiscal_defects.append(f"{fid}: invalid validation stage {row['validation_stage']!r}")
    if row["status"] not in allowed_fiscal_status:
        fiscal_defects.append(f"{fid}: invalid status {row['status']!r}")
    programme_refs = {item.strip() for item in row["affected_programmes"].split(";") if item.strip()}
    unknown_programmes = programme_refs - retained
    if not programme_refs or unknown_programmes:
        fiscal_defects.append(f"{fid}: affected programmes missing or not retained {sorted(unknown_programmes)}")
    affected_decisions = {item.strip() for item in row["affected_decisions"].split(";") if item.strip()}
    unknown_decisions = affected_decisions - decision_ids
    if not affected_decisions or unknown_decisions:
        fiscal_defects.append(f"{fid}: affected decisions missing or unknown {sorted(unknown_decisions)}")
    related_validation = {item.strip() for item in row["related_validation_ids"].split(";") if item.strip()}
    unknown_validation = related_validation - set(validation_ids)
    if not related_validation or unknown_validation:
        fiscal_defects.append(f"{fid}: validation controls missing or unknown {sorted(unknown_validation)}")
    evidence = row["evidence_reference"].strip()
    accepted = row["acceptance_date"].strip()
    disposition_status = {"validated", "validated_with_conditions", "rejected", "superseded"}
    if row["status"] in disposition_status and (not evidence or not accepted):
        fiscal_defects.append(f"{fid}: disposition status lacks Treasury evidence or acceptance date")
    if row["status"] in {"open", "requested"} and (evidence or accepted):
        fiscal_defects.append(f"{fid}: {row['status']} item improperly carries disposition evidence/date")

if fiscal_ids != expected_fiscal_ids:
    fiscal_defects.append(f"fiscal IDs are {sorted(fiscal_ids)}, expected FIS-01 to FIS-10")
fiscal_stage_counts = Counter(row["validation_stage"] for row in fiscal_rows)
expected_fiscal_stages = Counter({
    "phase_1_ceiling_gate": 5,
    "programme_cost_gate": 4,
    "later_phase_gate": 1,
})
if fiscal_stage_counts != expected_fiscal_stages:
    fiscal_defects.append(f"fiscal-stage distribution drift: {dict(fiscal_stage_counts)}")
fiscal_covered_programmes = {
    item.strip()
    for row in fiscal_rows
    for item in row["affected_programmes"].split(";")
    if item.strip()
}
if fiscal_covered_programmes != retained:
    fiscal_defects.append(
        f"fiscal coverage does not equal all retained programmes: missing {sorted(retained - fiscal_covered_programmes)}"
    )

required_fiscal_domains = {
    "existing_allocations", "reallocation_authority", "incremental_phase_1_ceiling",
    "staff_establishment_and_emoluments", "unit_cost_validation", "inflation_and_cashflow",
    "economic_and_vote_classification", "procurement_and_disbursement_route",
    "contingent_and_matched_exposure", "scenario_outputs_and_affordability",
}
actual_fiscal_domains = {row["domain"] for row in fiscal_rows}
if actual_fiscal_domains != required_fiscal_domains:
    fiscal_defects.append(
        f"fiscal domains drift: missing {sorted(required_fiscal_domains - actual_fiscal_domains)}"
    )

central_phase_1 = sum(
    D(row["years_1_2"]) for row in cm if row["scenario"] == "central"
)
conservative_phase_1 = sum(
    D(row["years_1_2"]) for row in cm if row["scenario"] == "conservative"
)
expanded_phase_1 = sum(
    D(row["years_1_2"]) for row in cm if row["scenario"] == "expanded"
)
for amount, label in (
    (central_phase_1, "Central"),
    (conservative_phase_1, "Conservative"),
    (expanded_phase_1, "Expanded"),
):
    formatted = f"RM{amount:,.3f}m"
    if formatted not in annex_text:
        fiscal_defects.append(f"Phase 1 schedule lacks model-derived {label} amount {formatted}")

for required_phrase in (
    "gross planning cost, not a requested, net or Treasury-validated ceiling",
    "No modelled existing or reallocated amount is recognised as available funding",
):
    if required_phrase not in proposal_text:
        fiscal_defects.append(f"proposal lacks fiscal boundary: {required_phrase}")
if "no ministry or Treasury has confirmed a Phase 1 funding split" not in annex_text:
    fiscal_defects.append("technical annex improperly implies a Phase 1 funding split")
if "A validated Phase 1 ceiling exists only when FIS-01, FIS-02, FIS-03 and FIS-07 are validated" not in ad_text:
    fiscal_defects.append("fiscal register lacks the composite ceiling rule")

check(not fiscal_defects,
      "[15] all 10 Treasury controls have questions, evidence, owners, programme/decision/validation mappings, unresolved consequences and controlled status",
      f"[15] FISCAL VALIDATION DEFECTS: {fiscal_defects[:24]}")
check(fiscal_stage_counts == expected_fiscal_stages,
      "[15a] fiscal controls are distributed as 5 Phase 1 ceiling, 4 programme-cost and 1 later-phase gate",
      f"[15a] FISCAL VALIDATION-STAGE DRIFT: {dict(fiscal_stage_counts)}")
check(all(
          not (row["status"] in {"validated", "validated_with_conditions", "rejected", "superseded"}
               and (not row["evidence_reference"].strip() or not row["acceptance_date"].strip()))
          and not (row["status"] in {"open", "requested"}
                   and (row["evidence_reference"].strip() or row["acceptance_date"].strip()))
          for row in fiscal_rows),
      "[15b] no Treasury validation is implied without written evidence and an acceptance date",
      "[15b] ONE OR MORE FISCAL CONTROLS IMPROPERLY IMPLY TREASURY VALIDATION")
check(actual_fiscal_domains == required_fiscal_domains and fiscal_covered_programmes == retained,
      "[15c] the ten required fiscal domains cover all 16 retained programmes",
      "[15c] FISCAL DOMAIN OR PROGRAMME COVERAGE IS INCOMPLETE")
check(all(f"RM{value:,.3f}m" in annex_text for value in (
          conservative_phase_1, central_phase_1, expanded_phase_1)),
      "[15d] conservative, central and expanded Phase 1 gross costs are generated directly from the canonical model",
      "[15d] PHASE 1 SCENARIO FIGURES DO NOT MATCH THE CANONICAL MODEL")
check("no ministry or Treasury has confirmed a Phase 1 funding split" in annex_text,
      "[15e] the Phase 1 schedule does not fabricate existing, reallocated or incremental funding splits",
      "[15e] PHASE 1 FUNDING-SPLIT LIMITATION IS MISSING")
check(all(row["status"] == "open" for row in fiscal_rows),
      "[15f] all fiscal controls remain open; no Treasury-reviewed ceiling is represented as complete",
      "[15f] A FISCAL CONTROL HAS CHANGED FROM OPEN WITHOUT EXTERNAL EVIDENCE REVIEW")

# ---- CHECK 16: Stage 6 programme delivery-feasibility sheets ------------
design_rows = data.get("PROGRAMME_DESIGN_REGISTER.csv", [])
design_ids = {row["programme_id"] for row in design_rows}
allowed_design_status = {
    "draft_pending_agency_confirmation", "agency_accepted",
    "agency_accepted_with_conditions", "rejected", "superseded",
}
allowed_signoff_status = {"pending", "accepted", "accepted_with_conditions", "rejected", "superseded"}
design_required_fields = (
    "design_status", "exclusions", "delivery_channel", "geographic_coverage",
    "annual_volume", "volume_status", "complaints_and_appeals", "data_collected",
    "retention_and_access_rule", "key_dependencies", "stop_criteria",
    "redesign_criteria", "expansion_criteria", "signoff_owner", "signoff_status",
)
design_defects = []
for row in design_rows:
    pid = row["programme_id"]
    for field in design_required_fields:
        if not row[field].strip():
            design_defects.append(f"{pid}: blank {field}")
    if row["design_status"] not in allowed_design_status:
        design_defects.append(f"{pid}: invalid design status {row['design_status']!r}")
    if row["signoff_status"] not in allowed_signoff_status:
        design_defects.append(f"{pid}: invalid sign-off status {row['signoff_status']!r}")
    dependency_refs = set(re.findall(r"\b(?:VAL|LGL|FIS)-\d{2}\b", row["key_dependencies"]))
    known_control_refs = set(validation_ids) | legal_ids | fiscal_ids
    unknown_dependencies = dependency_refs - known_control_refs
    if not dependency_refs or unknown_dependencies:
        design_defects.append(f"{pid}: missing or unknown dependency refs {sorted(unknown_dependencies)}")
    evidence = row["evidence_reference"].strip()
    accepted = row["acceptance_date"].strip()
    disposition = {"accepted", "accepted_with_conditions", "rejected", "superseded"}
    if row["signoff_status"] in disposition and (not evidence or not accepted):
        design_defects.append(f"{pid}: disposition lacks written evidence or acceptance date")
    if row["signoff_status"] == "pending" and (evidence or accepted):
        design_defects.append(f"{pid}: pending sheet improperly carries acceptance evidence/date")

check(not design_defects and len(design_rows) == 16,
      "[16] all 16 programme designs contain delivery, coverage, volume, remedy, data, dependency and stop/redesign/expansion controls",
      f"[16] PROGRAMME DESIGN DEFECTS: {design_defects[:24]}; rows={len(design_rows)}")

responsibility_ids = {row["programme_id"] for row in data.get("RESPONSIBILITY_MATRIX.csv", [])}
kpi_programme_ids = {row["programme_id"] for row in data.get("KPI_REGISTER.csv", [])}
central_programme_ids = {
    row["programme_id"] for row in cm
    if row["scenario"] == "central" and not row["programme_id"].startswith("PRG-XX")
}
assumption_programme_ids = {
    row["programme_id"] for row in data.get("COSTING_ASSUMPTIONS.csv", [])
    if row["programme_id"] in retained
}
joined_coverage = (
    design_ids == retained == responsibility_ids == kpi_programme_ids
    == central_programme_ids == assumption_programme_ids
)
check(joined_coverage,
      "[16a] every retained programme resolves one design, responsibility, KPI, central cost and costing-assumption record",
      "[16a] PROGRAMME DESIGN JOIN COVERAGE DOES NOT MATCH THE 16 RETAINED PROGRAMMES")

check(all(
          not (row["signoff_status"] in {"accepted", "accepted_with_conditions", "rejected", "superseded"}
               and (not row["evidence_reference"].strip() or not row["acceptance_date"].strip()))
          and not (row["signoff_status"] == "pending"
                   and (row["evidence_reference"].strip() or row["acceptance_date"].strip()))
          for row in design_rows),
      "[16b] no agency acceptance is implied without written evidence and an acceptance date",
      "[16b] ONE OR MORE PROGRAMME SHEETS IMPROPERLY IMPLY AGENCY ACCEPTANCE")

design_sheets_path = os.path.join(HERE, "PROGRAMME_DESIGN_SHEETS.md")
design_sheets_text = open(design_sheets_path, encoding="utf-8").read() if os.path.exists(design_sheets_path) else ""
check(design_sheets_text == render_programme_design_sheets(),
      "[16c] the complete programme-design-sheet document matches the canonical registers exactly",
      "[16c] PROGRAMME DESIGN SHEETS ARE STALE OR MANUALLY EDITED")

required_sheet_labels = {
    "Problem and baseline", "Target population and eligibility", "Service delivered", "Exclusions",
    "Lead and accounting officer", "Supporting agencies", "Authority route", "Delivery channel and coverage",
    "Volume", "Cost", "KPI and verification", "Complaints and appeals", "Data collected",
    "Retention and access", "Key dependencies", "Stop criteria", "Redesign criteria", "Expansion criteria",
}
sheet_structure_ok = all(
    design_sheets_text.count(f"## {pid} —") == 1 for pid in retained
) and all(f"| {label} |" in design_sheets_text for label in required_sheet_labels)
check(sheet_structure_ok,
      "[16d] each of the 16 sheets contains the complete two-part implementation design structure",
      "[16d] ONE OR MORE PROGRAMME SHEETS OR REQUIRED DESIGN FIELDS ARE MISSING")

asm_by_programme = {
    row["programme_id"]: row for row in data.get("COSTING_ASSUMPTIONS.csv", [])
    if row["programme_id"] in retained
}
programme_by_id = {row["programme_id"]: row for row in programme_rows}
kpi_by_programme = {row["programme_id"]: row for row in kpi_rows}
design_by_id = {row["programme_id"]: row for row in design_rows}
volume_ok = (
    asm_by_programme["PRG-05"]["reach_count"] == "120000"
    and "20,000 students supported per year" in design_by_id["PRG-05"]["annual_volume"]
    and "20,000 applicants per phase" in asm_by_programme["PRG-07"]["frequency_or_duration"]
    and "concurrent capacity for 60,000 households" in programme_by_id["PRG-09"]["output"]
    and "Concurrent capacity for approximately 60,000 households" in kpi_by_programme["PRG-09"]["year_6_target"]
    and "cumulatively" not in programme_by_id["PRG-09"]["output"].lower()
    and asm_by_programme["PRG-10"]["reach_count"] == "5000"
    and "5,000 enterprises" in programme_by_id["PRG-10"]["output"]
    and "5,000 enterprises" in kpi_by_programme["PRG-10"]["year_6_target"]
)
check(volume_ok,
      "[16e] PRG-05, PRG-07, PRG-09 and PRG-10 service volumes reconcile to their formula, reach unit and phase meaning",
      "[16e] PROGRAMME SERVICE VOLUME DRIFTS FROM THE COST OR REACH MODEL")

check(all(row["design_status"] == "draft_pending_agency_confirmation"
          and row["signoff_status"] == "pending" for row in design_rows),
      "[16f] all 16 sheets remain internal drafts pending accounting-officer confirmation",
      "[16f] A PROGRAMME DESIGN HAS CHANGED STATUS WITHOUT EXTERNAL AGENCY REVIEW")

# ---- CHECK 17: Stage 7 household-visible service commitments ------------
service_rows = data.get("SERVICE_COMMITMENT_REGISTER.csv", [])
service_ids = {row["commitment_id"] for row in service_rows}
expected_service_ids = {f"SC-{number:02d}" for number in range(1, 8)}
required_service_names = {
    "Named case ownership", "Acknowledgement and status visibility",
    "Written reasons or referral record", "No-wrong-door referral",
    "Published eligibility and queue rules", "Quarterly service-performance reporting",
    "Defined escalation and complaint route",
}
service_defects = []
service_coverage = set()
for row in service_rows:
    sid = row["commitment_id"]
    affected = {item.strip() for item in row["affected_programmes"].split(";") if item.strip()}
    service_coverage |= affected
    if not affected or not affected <= retained:
        service_defects.append(f"{sid}: missing or unknown affected programmes {sorted(affected - retained)}")
    if row["adoption_status"] != "draft_pending_agency_confirmation":
        service_defects.append(f"{sid}: invalid or unsupported adoption status {row['adoption_status']!r}")
    if row["service_timeline_status"] != "pending_agency_capacity_confirmation":
        service_defects.append(f"{sid}: timeline status does not preserve agency-capacity gate")
    if row["reporting_frequency"] != "quarterly":
        service_defects.append(f"{sid}: reporting frequency is not quarterly")
    if re.search(r"\b\d+\s*(?:business\s+|calendar\s+)?(?:hour|day|week|month)s?\b", row["service_timeline"], re.I):
        service_defects.append(f"{sid}: invented numeric service deadline in timeline")
    if not re.search(r"capacity|workflow|caseload|demand|complaint|reporting", row["capacity_evidence_required"], re.I):
        service_defects.append(f"{sid}: capacity evidence is not operationally specified")
    if row["evidence_reference"].strip() or row["acceptance_date"].strip():
        service_defects.append(f"{sid}: draft commitment improperly carries adoption evidence/date")

check(not service_defects and len(service_rows) == 7 and service_ids == expected_service_ids,
      "[17] seven canonical service commitments have controlled scope, ownership, capacity evidence, reporting and remedy fields",
      f"[17] SERVICE COMMITMENT DEFECTS: {service_defects[:24]}; rows={len(service_rows)}; ids={sorted(service_ids)}")
check({row["commitment_name"] for row in service_rows} == required_service_names,
      "[17a] the seven commitments cover ownership, acknowledgement/status, reasons, no-wrong-door referral, published rules, quarterly reporting and escalation",
      "[17a] REQUIRED SERVICE-COMMITMENT COVERAGE IS INCOMPLETE")
check(service_coverage == retained,
      "[17b] the service standard covers all 16 retained programmes, including portfolio reporting and escalation functions",
      f"[17b] SERVICE-COMMITMENT PROGRAMME COVERAGE DRIFT: missing={sorted(retained - service_coverage)}")
check(all(row["adoption_status"] == "draft_pending_agency_confirmation"
          and not row["evidence_reference"].strip()
          and not row["acceptance_date"].strip() for row in service_rows),
      "[17c] no service commitment is represented as agency-adopted without written evidence and an acceptance date",
      "[17c] A SERVICE COMMITMENT IMPROPERLY IMPLIES AGENCY ADOPTION")
check(all(not re.search(r"\b\d+\s*(?:business\s+|calendar\s+)?(?:hour|day|week|month)s?\b",
                        row["service_timeline"], re.I) for row in service_rows),
      "[17d] no numeric case-processing, referral, queue or complaint deadline is invented before capacity confirmation",
      "[17d] ONE OR MORE SERVICE COMMITMENTS CONTAIN AN UNVALIDATED NUMERIC DEADLINE")
excluded_text = " ".join(row["excluded_outcomes"] for row in service_rows).lower()
required_excluded_outcomes = {
    "citizenship", "admission", "employment", "procurement", "housing",
}
check(all(term in excluded_text for term in required_excluded_outcomes),
      "[17e] the service standard expressly excludes statutory and third-party outcome guarantees",
      "[17e] SERVICE STANDARD DOES NOT EXCLUDE ALL HIGH-RISK OUTCOME GUARANTEES")
service_doc_path = os.path.join(HERE, "SERVICE_COMMITMENTS.md")
service_doc_text = open(service_doc_path, encoding="utf-8").read() if os.path.exists(service_doc_path) else ""
check(service_doc_text == render_service_commitments(),
      "[17f] the detailed service-commitment standard matches the canonical register exactly",
      "[17f] SERVICE COMMITMENT DOCUMENT IS STALE OR MANUALLY EDITED")
sheet_service_mapping_ok = all(
    f"| Minimum service commitments | {'; '.join(sorted(row['commitment_id'] for row in service_rows if pid in {item.strip() for item in row['affected_programmes'].split(';') if item.strip()}))}" in design_sheets_text
    for pid in retained
)
check(sheet_service_mapping_ok,
      "[17g] every programme design sheet contains its exact applicable service-commitment mapping",
      "[17g] ONE OR MORE PROGRAMME SHEETS HAS A STALE SERVICE-COMMITMENT MAPPING")

# ---- CHECK 18: Stage 8 governance continuity below the PM ---------------
continuity_rows = data.get("GOVERNANCE_CONTINUITY_REGISTER.csv", [])
continuity_ids = {row["continuity_id"] for row in continuity_rows}
expected_continuity_ids = {f"GC-{number:02d}" for number in range(1, 9)}
required_components = {
    "Prime Ministerial sponsorship and strategic review",
    "Designated minister between reviews",
    "Senior-officials delivery committee",
    "Ministry delivery officers and planning commitments",
    "Secretariat reporting authority with statutory boundary",
    "Automatic milestone escalation",
    "Meeting-independent public reporting",
    "Political and administrative succession",
}
continuity_defects = []
continuity_coverage = set()
required_boundary_terms = {"statutory", "accounting", "procurement", "vote"}
for row in continuity_rows:
    gid = row["continuity_id"]
    affected = {item.strip() for item in row["affected_programmes"].split(";") if item.strip()}
    continuity_coverage |= affected
    if not affected or not affected <= retained:
        continuity_defects.append(f"{gid}: missing or unknown affected programmes {sorted(affected - retained)}")
    if row["status"] != "draft_pending_cabinet_confirmation":
        continuity_defects.append(f"{gid}: unsupported status {row['status']!r}")
    if row["evidence_reference"].strip() or row["acceptance_date"].strip():
        continuity_defects.append(f"{gid}: draft control improperly carries adoption evidence/date")
    if not row["required_instrument"].strip() or not row["evidence_requirement"].strip():
        continuity_defects.append(f"{gid}: missing instrument or evidence requirement")
    boundary_tokens = set(re.findall(r"[a-z]+", row["authority_boundary"].lower()))
    if gid == "GC-05" and not required_boundary_terms <= boundary_tokens:
        continuity_defects.append("GC-05: secretariat boundary does not expressly preserve statutory, accounting, procurement and vote authority")

check(not continuity_defects and len(continuity_rows) == 8 and continuity_ids == expected_continuity_ids,
      "[18] eight canonical continuity controls contain owners, triggers, cadence, instruments, evidence and authority boundaries",
      f"[18] GOVERNANCE CONTINUITY DEFECTS: {continuity_defects[:24]}; rows={len(continuity_rows)}")
check({row["component"] for row in continuity_rows} == required_components,
      "[18a] continuity design covers sponsorship, minister, officials, delivery officers, secretariat, escalation, reporting and succession",
      "[18a] REQUIRED GOVERNANCE-CONTINUITY COMPONENTS ARE INCOMPLETE")
check(continuity_coverage == retained,
      "[18b] governance continuity covers all 16 retained programmes",
      f"[18b] GOVERNANCE-CONTINUITY COVERAGE DRIFT: missing={sorted(retained - continuity_coverage)}")
check(all(row["status"] == "draft_pending_cabinet_confirmation"
          and not row["evidence_reference"].strip()
          and not row["acceptance_date"].strip() for row in continuity_rows),
      "[18c] no continuity mechanism is represented as adopted without Cabinet evidence and an acceptance date",
      "[18c] A GOVERNANCE-CONTINUITY CONTROL IMPROPERLY IMPLIES ADOPTION")
continuity_doc_path = os.path.join(HERE, "GOVERNANCE_CONTINUITY.md")
continuity_doc_text = open(continuity_doc_path, encoding="utf-8").read() if os.path.exists(continuity_doc_path) else ""
check(continuity_doc_text == render_governance_continuity(),
      "[18d] the detailed governance-continuity standard matches the canonical register exactly",
      "[18d] GOVERNANCE CONTINUITY DOCUMENT IS STALE OR MANUALLY EDITED")
pm_dependency_removed = (
    "daily operating system" in continuity_doc_text
    and "meeting-independent" in " ".join(row["component"].lower() for row in continuity_rows)
    and "Prime Ministerial chairmanship is not sustained" not in next(row["risk_description"] for row in risk_rows if row["risk_id"] == "RSK-01")
    and "meeting held" not in next(row["definition"].lower() for row in kpi_rows if row["kpi_id"] == "KPI-15")
)
check(pm_dependency_removed,
      "[18e] portfolio continuity and KPI-15 no longer depend on a Prime Minister personally convening every quarterly meeting",
      "[18e] PRIME-MINISTER SINGLE-POINT DEPENDENCY REMAINS IN THE CONTROL MODEL")
responsibility_escalation_ok = all(
    "automatic escalation under GC-06" in row["escalation_route"]
    and "Task Force quarterly" not in row["escalation_route"]
    for row in responsibility_rows
)
check(responsibility_escalation_ok,
      "[18f] every programme responsibility row uses the delegated delivery-officer and automatic-escalation chain",
      "[18f] ONE OR MORE PROGRAMMES STILL DEPENDS ON TASK-FORCE-ONLY ESCALATION")

# ---- CHECK 19: Stage 9 cross-stage assurance and traceability ------------
trace_rows = data.get("STAGE_TRACEABILITY_REGISTER.csv", [])
expected_stage_ids = {f"SR-{number:02d}" for number in range(1, 9)}
trace_stage_ids = {row["stage_id"] for row in trace_rows}
requirements_by_stage = Counter(row["stage_id"] for row in trace_rows)
check(len(trace_rows) == 32 and trace_stage_ids == expected_stage_ids
      and all(requirements_by_stage[stage_id] == 4 for stage_id in expected_stage_ids),
      "[19] Stage 1-8 traceability contains four controlled requirements per stage",
      f"[19] TRACEABILITY COVERAGE DEFECT: rows={len(trace_rows)} stages={sorted(trace_stage_ids)} counts={dict(requirements_by_stage)}")

expected_git = {
    "SR-01": ("2", "cf2801d4e22fc8179ed693bb20179b13105e2654", "9a87816ff3eda217d05b9f1cd66eac6e8042ee82"),
    "SR-02": ("3", "30bf112f47f9fe3aaae7421b1160657a1c8db06c", "25e58767f31a9fbfaa8139f3bd372cb2eae07822"),
    "SR-03": ("4", "9e473681c914895bc61e78dd2c7e8676c9108e66", "01947887080c896a91e0d0f0844b94f465e3528c"),
    "SR-04": ("5", "535779802a01e75ef67836a8b0a8630cabb000e0", "bffd003ac63251b3545e3375742343305910a79b"),
    "SR-05": ("6", "fa6e56a09a9e40c9cb8a10a208819183278457c4", "dcf8d75c33b95cb01cf7cf1e08c0da3f1f8429c9"),
    "SR-06": ("7", "74bd4a1f6591834d8aed8eb9c3922ce2c9ff8288", "eccfa9ecb391f0f1d13275ea89adf7194c861d30"),
    "SR-07": ("8", "1eea7d2814a3a6c136bbf4bc658fdd7e58c3a188", "b8179b7cb8597427f4c4b9e4b16851ad29248581"),
    "SR-08": ("9", "df2e7e1378117a2f208288ab2282aa1dcd5fe7b7", "07450be6d38e5364f7dc49eb92af175178378e0b"),
}
git_defects = []
for row in trace_rows:
    expected = expected_git.get(row["stage_id"])
    actual = (row["pr_number"], row["head_commit"], row["merge_commit"])
    if expected != actual:
        git_defects.append(f"{row['requirement_id']}: {actual} != {expected}")
check(not git_defects,
      "[19a] every Stage 1-8 requirement maps to the preserved PR, head commit and merge commit",
      f"[19a] STAGE-TO-GIT PROVENANCE DRIFT: {git_defects[:12]}")

fidelity_defects = [row["requirement_id"] for row in trace_rows
                    if row["prompt_fidelity"] != "reconstructed_from_preserved_evidence_not_verbatim"
                    or "PR #" not in row["prompt_provenance"]]
requirements_doc = open(os.path.join(HERE, "STAGE_1_8_REQUIREMENTS.md"), encoding="utf-8").read()
check(not fidelity_defects and "did not retain the original chat prompts" in requirements_doc
      and "No row may be represented as a verbatim prompt" in requirements_doc,
      "[19b] reconstructed prompt requirements are explicitly non-verbatim and provenance-limited",
      f"[19b] PROMPT-FIDELITY MISREPRESENTATION: {fidelity_defects[:12]}")

evidence_defects = []
for row in trace_rows:
    for filename in [item.strip() for item in row["evidence_files"].split(";") if item.strip()]:
        if not os.path.exists(os.path.join(HERE, filename)):
            evidence_defects.append(f"{row['requirement_id']}:{filename}")
check(not evidence_defects,
      "[19c] every traceability evidence file exists in the controlled package",
      f"[19c] TRACEABILITY REFERENCES MISSING FILES: {evidence_defects[:20]}")

verifier_source = open(__file__, encoding="utf-8").read()
test_ref_defects = []
for row in trace_rows:
    for test_ref in [item.strip() for item in row["verifier_checks"].split(";") if item.strip()]:
        if test_ref not in verifier_source:
            test_ref_defects.append(f"{row['requirement_id']}:{test_ref}")
check(not test_ref_defects,
      "[19d] every traceability test reference resolves to the live verifier",
      f"[19d] TRACEABILITY REFERENCES UNKNOWN TESTS: {test_ref_defects[:20]}")

status_text = open(os.path.join(HERE, "STATUS.md"), encoding="utf-8").read()
status_stage_numbers = re.findall(r"^## Submission-readiness Stage ([1-8])\b", status_text, flags=re.MULTILINE)
check(status_stage_numbers == [str(number) for number in range(1, 9)],
      "[19e] STATUS.md contains each submission-readiness Stage 1-8 exactly once and in order",
      f"[19e] STATUS STAGE TAXONOMY DEFECT: {status_stage_numbers}")

master_text = open(os.path.join(os.path.dirname(HERE), "MASTER_PROMPT.md"), encoding="utf-8").read()
completion = master_text.split("## 17. Final completion condition", 1)[1].split("## 18. Response discipline", 1)[0]
completion_numbers = [int(value) for value in re.findall(r"^(\d+)\.", completion, flags=re.MULTILINE)]
check(completion_numbers == list(range(1, 16))
      and completion.index("All seven service commitments") < completion.index("All eight governance continuity controls"),
      "[19f] master completion criteria are uniquely numbered 1-15 and preserve Stage 7 before Stage 8",
      f"[19f] MASTER COMPLETION STRUCTURE DEFECT: numbers={completion_numbers}")

critic_text = open(os.path.join(HERE, "CRITIC_FINDINGS.md"), encoding="utf-8").read()
qa_text = open(os.path.join(HERE, "FINAL_QA_REPORT.md"), encoding="utf-8").read()
audit_text = open(os.path.join(HERE, "AUDIT_LOG.md"), encoding="utf-8").read()
uninspected_count = sum(row["verification_status"] == "cited-source-not-yet-inspected"
                        for row in data.get("CLAIMS_AND_FIGURES_REGISTER.csv", []))
history_defects = []
if "84-check Stage 2" in audit_text:
    history_defects.append("AUDIT_LOG retains incorrect 84-check Stage 2 reference")
if uninspected_count != 10 or "Ten claims remain `cited-source-not-yet-inspected`" not in critic_text:
    history_defects.append(f"uninspected claim count is not reconciled to 10 (actual {uninspected_count})")
for stale in ("75 resolved, 1 open", "Nine residual limitations", "MOD-04) remains open"):
    if stale in status_text + qa_text + critic_text:
        history_defects.append(f"stale assurance statement: {stale}")
check(not history_defects and "All 76 critic findings are resolved" in critic_text,
      "[19g] stale check counts, claim counts, residual-limit counts and MOD-04 disposition are repaired",
      f"[19g] ASSURANCE-HISTORY DRIFT: {history_defects}")

formula_controls = data.get("COST_FORMULA_CONTROL_REGISTER.csv", [])
formula_control_defects = []
controlled_partial = {row["programme_id"] for row in formula_controls}
if controlled_partial != set(partial) or controlled_partial != {"PRG-01", "PRG-14"}:
    formula_control_defects.append(f"controlled partial set {sorted(controlled_partial)} != live partial set {sorted(partial)}")
for row in formula_controls:
    assumption = asm.get(row["assumption_id"])
    model_row = central.get(row["programme_id"])
    if assumption is None or model_row is None:
        formula_control_defects.append(f"{row['formula_control_id']}: missing assumption or model row")
        continue
    phase_1 = D(assumption["years_1_2_central_rm_m"])
    six_year = phase_1 + D(assumption["years_3_4_central_rm_m"]) + D(assumption["years_5_6_central_rm_m"])
    if D(row["central_phase_1_direct_rm_m"]) != phase_1 or D(row["central_six_year_direct_rm_m"]) != six_year:
        formula_control_defects.append(f"{row['formula_control_id']}: controlled amounts do not match assumptions")
    if abs(D(row["central_six_year_direct_rm_m"]) - D(model_row["six_year_total"])) > TOL:
        formula_control_defects.append(f"{row['formula_control_id']}: controlled total does not match model")
    if row["ceiling_treatment"] != "excluded_from_validated_ceiling_until_formula_complete":
        formula_control_defects.append(f"{row['formula_control_id']}: partial formula is not excluded")
    if row["status"] != "open" or row["evidence_reference"].strip() or row["acceptance_date"].strip():
        formula_control_defects.append(f"{row['formula_control_id']}: unsupported closure or evidence")
check(not formula_control_defects,
      "[19h] every partial formula is amount-reconciled and excluded from a validated ceiling until completion",
      f"[19h] PARTIAL-FORMULA CEILING CONTROL DEFECTS: {formula_control_defects}")

assurance_text = open(os.path.join(HERE, "CROSS_STAGE_ASSURANCE_REPORT.md"), encoding="utf-8").read()
assurance_markers = ["Internally verified", "Externally pending", "Legally pending",
                     "Treasury pending", "Agency pending", "Cabinet pending",
                     "not an external audit opinion", "branch protection must be configured"]
check(all(marker in assurance_text for marker in assurance_markers),
      "[19i] cross-stage report separates internal assurance from every external approval class",
      "[19i] CROSS-STAGE ASSURANCE CLASSIFICATION IS INCOMPLETE")

workflow_path = os.path.join(os.path.dirname(HERE), ".github", "workflows", "assurance.yml")
workflow_text = open(workflow_path, encoding="utf-8").read() if os.path.exists(workflow_path) else ""
workflow_markers = ["pull_request:", "python outputs/verify_outputs.py",
                    "python outputs/build_costing.py", "python outputs/sync_document_integrity.py",
                    "git diff --exit-code -- outputs", "npm run lint", "npm run build"]
check(all(marker in workflow_text for marker in workflow_markers),
      "[19j] GitHub Actions runs policy verification, deterministic regeneration, lint and production build",
      "[19j] GITHUB ACTIONS ASSURANCE WORKFLOW IS MISSING REQUIRED GATES")

render_manifest = data.get("RENDERED_SUBMISSION_MANIFEST.csv", [])
render_defects = []
if len(render_manifest) != 1:
    render_defects.append(f"expected one manifest row, found {len(render_manifest)}")
else:
    row = render_manifest[0]
    source_names = row["canonical_sources"].split(";")
    source_bundle = hashlib.sha256()
    for source_name in source_names:
        source_path = os.path.join(HERE, source_name)
        if not os.path.exists(source_path):
            render_defects.append(f"missing canonical source {source_name}")
            continue
        source_bundle.update(source_name.encode("utf-8"))
        source_bundle.update(b"\0")
        with open(source_path, "rb") as source_stream:
            source_bundle.update(source_stream.read())
        source_bundle.update(b"\0")
    if source_bundle.hexdigest() != row["canonical_source_bundle_sha256"]:
        render_defects.append("canonical source-bundle hash mismatch")
    for label, filename_key, digest_key in (("DOCX", "docx_file", "docx_sha256"),
                                             ("PDF", "pdf_file", "pdf_sha256")):
        artifact_path = os.path.join(HERE, row[filename_key])
        if not os.path.exists(artifact_path):
            render_defects.append(f"missing {label} artifact")
            continue
        digest = hashlib.sha256()
        with open(artifact_path, "rb") as artifact_stream:
            for chunk in iter(lambda: artifact_stream.read(1024 * 1024), b""):
                digest.update(chunk)
        if digest.hexdigest() != row[digest_key]:
            render_defects.append(f"{label} hash mismatch")
    docx_path = os.path.join(HERE, row["docx_file"])
    if os.path.exists(docx_path):
        try:
            with zipfile.ZipFile(docx_path) as package:
                if "word/document.xml" not in package.namelist():
                    render_defects.append("DOCX package lacks word/document.xml")
        except zipfile.BadZipFile:
            render_defects.append("DOCX is not a valid ZIP package")
    pdf_path = os.path.join(HERE, row["pdf_file"])
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as pdf_stream:
            if pdf_stream.read(5) != b"%PDF-":
                render_defects.append("PDF signature is invalid")
    try:
        if int(row["pdf_page_count"]) != 37:
            render_defects.append(f"expected 37 PDF pages, found {row['pdf_page_count']}")
    except ValueError:
        render_defects.append("PDF page count is not numeric")
    if row["render_status"] != "rendered_from_docx":
        render_defects.append("render status is not rendered_from_docx")
    if not row["visual_qa_status"].startswith("passed_"):
        render_defects.append("visual QA is not marked passed")
check(not render_defects,
      "[19k] Cabinet DOCX/PDF signatures, hashes, source bundle, page count and visual QA manifest reconcile",
      f"[19k] RENDERED CABINET PACK CONTROL DEFECTS: {render_defects}")

# ---- CHECK 12c: every typed cross-reference resolves everywhere ----------
known_refs = {
    "CLM": {r["claim_id"] for r in data.get("CLAIMS_AND_FIGURES_REGISTER.csv", [])},
    "KPI": {r["kpi_id"] for r in kpi_rows},
    "PRG": {r["programme_id"] for r in programme_rows},
    "RSK": {r["risk_id"] for r in risk_rows},
    "RSP": {r["responsibility_id"] for r in responsibility_rows},
    "VAL": set(validation_ids),
    "LGL": legal_ids,
    "FIS": fiscal_ids,
    "SC": service_ids,
    "GC": continuity_ids,
    "CFC": {row["formula_control_id"] for row in formula_controls},
}
unresolved_refs = []
for path in _glob.glob(os.path.join(HERE, "*.csv")) + _glob.glob(os.path.join(HERE, "*.md")):
    content = open(path, encoding="utf-8").read()
    for prefix, known_ids in known_refs.items():
        width = 3 if prefix == "CLM" else 2
        for reference in set(re.findall(rf"\b{prefix}-\d{{{width}}}\b", content)):
            if reference not in known_ids:
                unresolved_refs.append(f"{os.path.basename(path)}:{reference}")
check(not unresolved_refs,
      "[12c] every CLM/KPI/PRG/RSK/RSP/VAL reference across canonical CSV and Markdown files resolves",
      f"[12c] UNRESOLVED TYPED REFERENCES: {sorted(unresolved_refs)[:20]}")

# ---- CHECK 12d: manual proposal cost statements match the model ----------
# Tables are generated under [12].  Remaining programme-level prose is
# intentionally authored, so independently compare every stated central cost.
central_costs = {r["programme_id"]: D(r["six_year_total"])
                 for r in cm if r["scenario"] == "central"
                 and not r["programme_id"].startswith("PRG-XX")}
narrative_cost_drift = []
programme_headers = list(re.finditer(r"\*\*(PRG-\d{2})\s+", proposal_text))
checked_programme_costs = 0
for index, match in enumerate(programme_headers):
    end_at = programme_headers[index + 1].start() if index + 1 < len(programme_headers) else len(proposal_text)
    section = proposal_text[match.start():end_at]
    stated = re.search(r"\*\*Six-year central cost:\s*RM([\d,.]+)\s+million", section)
    if not stated:
        continue
    checked_programme_costs += 1
    programme_id = match.group(1)
    amount = D(stated.group(1).replace(",", ""))
    if programme_id not in central_costs or abs(amount - central_costs[programme_id]) > TOL:
        narrative_cost_drift.append(
            f"{programme_id}: proposal RM{amount}m != model RM{central_costs.get(programme_id)}m"
        )

summary_patterns = [
    (r"six-year central (?:cost|planning scenario) of RM([\d,.]+) million", grand.get("central"), "executive central total"),
    (r"(?:incremental new funding requirement is|modelled incremental new funding requirement of) RM([\d,.]+) million", sum(D(r["new_funding"]) for r in central_rows), "incremental new funding"),
    (r"RM([\d,.]+) million (?:being|provisionally classified as) existing allocations (?:and|or) proposed reallocation", sum(D(r["existing_funding"]) + D(r["reallocated_funding"]) for r in central_rows), "non-new funding"),
]
for pattern, expected_amount, label in summary_patterns:
    found = re.search(pattern, proposal_text, flags=re.IGNORECASE)
    if not found:
        narrative_cost_drift.append(f"missing proposal statement: {label}")
        continue
    stated_amount = D(found.group(1).replace(",", ""))
    if abs(stated_amount - expected_amount) > TOL:
        narrative_cost_drift.append(f"{label}: proposal RM{stated_amount}m != model RM{expected_amount}m")
check(not narrative_cost_drift and checked_programme_costs >= 8,
      f"[12d] {checked_programme_costs} authored programme-cost statements and all executive funding headlines match COSTING_MODEL.csv",
      f"[12d] NARRATIVE FINANCIAL DRIFT: {narrative_cost_drift}; only {checked_programme_costs} programme costs inspected")

# ---- CHECK 12e: the canonical headline claim matches the live model ------
claim_054 = next((row for row in data.get("CLAIMS_AND_FIGURES_REGISTER.csv", [])
                  if row["claim_id"] == "CLM-054"), None)
claim_054_defects = []
if claim_054 is None:
    claim_054_defects.append("CLM-054 is missing")
else:
    claim_text = claim_054["verbatim_or_close_claim"]
    expected_claim_amounts = {
        "central": grand.get("central", Decimal(0)),
        "conservative": grand.get("conservative", Decimal(0)),
        "expanded": grand.get("expanded", Decimal(0)),
        "central new funding": sum(D(row["new_funding"]) for row in central_rows),
    }
    for label, amount in expected_claim_amounts.items():
        if f"RM{amount:,.3f} million" not in claim_text:
            claim_054_defects.append(f"{label} RM{amount:,.3f}m missing from CLM-054")
    treatment = claim_054["adopted_treatment"].lower()
    if "indicative" not in treatment or "not" not in treatment or "approved envelope" not in treatment:
        claim_054_defects.append("CLM-054 treatment does not preserve indicative/non-approved status")
check(not claim_054_defects,
      "[12e] CLM-054 matches all three scenario totals and central new funding, and preserves non-approved status",
      f"[12e] CANONICAL FINANCIAL CLAIM DRIFT: {claim_054_defects}")

# ---- CHECK 12f: non-generated headline tables match the live model ------
conservative_new = sum(
    D(row["new_funding"]) for row in cm if row["scenario"] == "conservative"
)
headline_paths = ("STATUS.md", "STAGE_2_RECONCILIATION.md")
headline_drift = []
for filename in headline_paths:
    content = open(os.path.join(HERE, filename), encoding="utf-8").read()
    if f"{conservative_new:,.3f}" not in content:
        headline_drift.append(f"{filename}: missing conservative new funding {conservative_new:,.3f}")
check(not headline_drift,
      "[12f] non-generated status and reconciliation headlines match the canonical conservative new-funding total",
      f"[12f] NARRATIVE CONSERVATIVE-FUNDING DRIFT: {headline_drift}")

# ---- report --------------------------------------------------------------
print(f"\nPASSED ({len(PASSED)}):")
for p in PASSED:
    print("  PASS " + p)
if SOFT_WARNINGS:
    print(f"\nWARNINGS ({len(SOFT_WARNINGS)}):")
    for w in SOFT_WARNINGS:
        print("  WARN " + w)
if HARD_FAILURES:
    print(f"\nHARD FAILURES ({len(HARD_FAILURES)}):")
    for f in HARD_FAILURES:
        print("  FAIL " + f)

print("\n" + "=" * 78)
if HARD_FAILURES:
    print(f"RESULT: FAIL - {len(HARD_FAILURES)} hard failure(s), {len(SOFT_WARNINGS)} warning(s)")
    sys.exit(1)
print(f"RESULT: PASS - {len(PASSED)} checks passed, {len(SOFT_WARNINGS)} warning(s), 0 hard failures")
sys.exit(0)
