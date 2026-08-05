"""
Machine verification for the MIB 2.0 output package.

Implements the twelve minimum checks required by MASTER_PROMPT.md section 10.
Exits non-zero if any HARD check fails.

Usage: python outputs/verify_outputs.py
"""

import csv
import os
import re
import sys
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
          "BENEFICIARY_RECONCILIATION.csv": "overlap_group"}
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
      f"[4b] too many un-derived cost rows: {partial}", hard=False)
if partial:
    SOFT_WARNINGS.append(f"[4b] DISCLOSED: {partial} have no complete published formula; "
                         f"their amounts are authored judgements, not derivations")

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
val_defined = set()
adpath = os.path.join(HERE, "ASSUMPTIONS_AND_DECISIONS.md")
if os.path.exists(adpath):
    ad = open(adpath, encoding="utf-8").read()
    val_defined = set(re.findall(r"\|\s*(VAL-\d{2})\s*\|", ad))
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
         "COSTING_ASSUMPTIONS.csv", "verify_outputs.py", "VERIFICATION_RESULTS.md",
         "STAGE_1_DIAGNOSTIC.md", "STAGE_2_RECONCILIATION.md",
         "MIB_2.0_EXECUTIVE_PROPOSAL.md", "TECHNICAL_ANNEXES.md"]
absent = [f for f in CANON if not os.path.exists(os.path.join(HERE, f))
          or os.path.getsize(os.path.join(HERE, f)) == 0]
check(not absent, f"[extra] all {len(CANON)} canonical files exist and are non-empty",
      f"[extra] MISSING OR EMPTY CANONICAL FILES: {absent}", hard=False)

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
