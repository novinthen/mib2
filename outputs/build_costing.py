"""
Deterministic costing-model builder for MIB 2.0.

Reads  : outputs/COSTING_ASSUMPTIONS.csv   (the only place numbers are authored)
Writes : outputs/COSTING_MODEL.csv         (fully derived; never hand-edited)

Every figure in COSTING_MODEL.csv is computed here from a documented assumption
row, so the model can be rebuilt and re-checked at any time.

Method
------
1. Delivery lines: one row per (programme, scenario). Scenario scaling is applied
   only to the VARIABLE component of each programme's phase cost:
       amount(scenario) = fixed + multiplier * variable
   where fixed = (1 - variable_share) * central_amount.
2. Administration: ASM-040 rate applied to total delivery, per phase and scenario.
3. Contingency: ASM-041 rate applied to (delivery + administration).
4. Funding split (existing / reallocated / new) is applied per row and the three
   components are forced to sum exactly to the row total using largest-remainder
   allocation on cents, so no rounding residue can appear.

Usage: python outputs/build_costing.py
"""

import csv
import os
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN

HERE = os.path.dirname(os.path.abspath(__file__))
ASSUMPTIONS = os.path.join(HERE, "COSTING_ASSUMPTIONS.csv")
MODEL = os.path.join(HERE, "COSTING_MODEL.csv")

SCENARIOS = {"conservative": Decimal("0.75"),
             "central": Decimal("1.00"),
             "expanded": Decimal("1.30")}

ADMIN_RATE = Decimal("0.040")        # ASM-040
CONTINGENCY_RATE = Decimal("0.075")  # ASM-041
PRICE_BASE_YEAR = "2026"

# Programme metadata not carried in the assumptions file
PROGRAMME_META = {
    "PRG-01": ("P1 Foundations", "Ministry of Home Affairs (JPN)", "National Documentation Resolution Programme", "1-2-3"),
    "PRG-02": ("P1 Foundations", "Ministry of Education", "Early Childhood Access Programme", "1-2-3"),
    "PRG-03": ("P1 Foundations", "Ministry of Education", "SJKT Safety and Learning Environment Programme", "1-2-3"),
    "PRG-04": ("P1 Foundations", "Ministry of National Unity", "Multi-Faith Community Institution Safety and Compliance Programme", "1-2-3"),
    "PRG-05": ("P2 Progression", "Ministry of Education", "School-to-Pathway Guidance and Placement Support", "1-2-3"),
    "PRG-06": ("P2 Progression", "Ministry of Human Resources", "TVET and STEM Progression Pipeline", "1-2-3"),
    "PRG-07": ("P2 Progression", "Ministry of Education", "Tertiary Access Navigation and Transparency", "1-2-3"),
    "PRG-08": ("P2 Progression", "Ministry of Higher Education", "Professional Entry and Mentoring", "2-3"),
    "PRG-09": ("P3 Livelihoods", "Prime Minister's Department", "Household Progression Programme", "1-2-3"),
    "PRG-10": ("P3 Livelihoods", "Ministry of Entrepreneur and Cooperatives Development", "Microenterprise Growth and Vendor Capability Programme", "2-3"),
    "PRG-11": ("P3 Livelihoods", "Ministry of Finance", "Household Savings and Asset Accumulation Scheme", "1-2-3"),
    "PRG-12": ("P3 Livelihoods", "Ministry of Housing and Local Government", "Housing Access and Estate Legacy Resolution", "1-2-3"),
    "PRG-13": ("P4 Institutional Participation", "Public Service Department (JPA)", "Public Service Application Pipeline Programme", "1-2-3"),
    "PRG-14": ("P4 Institutional Participation", "Public Service Department (JPA)", "Public Service Professional Advancement", "2-3"),
    "PRG-15": ("X Delivery", "Prime Minister's Department", "Task Force and Delivery Secretariat", "1-2-3"),
    "PRG-16": ("X Delivery", "Prime Minister's Department", "Data, Evaluation and Public Reporting", "1-2-3"),
}

CENTS = Decimal("0.001")  # model is in RM million to 3 dp


def q(x):
    return Decimal(x).quantize(CENTS, rounding=ROUND_HALF_UP)


def split_funding(total, shares):
    """Split `total` into len(shares) parts that sum EXACTLY to total."""
    raw = [total * Decimal(str(s)) for s in shares]
    floors = [r.quantize(CENTS, rounding=ROUND_DOWN) for r in raw]
    residue = total - sum(floors)
    # true largest-remainder: distribute the residue one unit at a time to the
    # components with the largest fractional remainders (MIN-02 correction).
    order = sorted(range(len(raw)), key=lambda i: raw[i] - floors[i], reverse=True)
    i = 0
    while residue > 0 and order:
        floors[order[i % len(order)]] += CENTS
        residue -= CENTS
        i += 1
    return floors


def main():
    with open(ASSUMPTIONS, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh)]

    delivery_rows = [r for r in rows
                     if r["programme_id"].startswith("PRG-")
                     and r["cost_category"] not in ("derivation", "rate")]

    out = []
    line_no = 0

    # ---- 1. Delivery lines -------------------------------------------------
    scenario_phase_delivery = {s: [Decimal(0), Decimal(0), Decimal(0)] for s in SCENARIOS}

    for r in delivery_rows:
        pid = r["programme_id"]
        pillar, ministry, name, phases = PROGRAMME_META[pid]
        vs = Decimal(r["variable_share"])
        centrals = [Decimal(r["years_1_2_central_rm_m"]),
                    Decimal(r["years_3_4_central_rm_m"]),
                    Decimal(r["years_5_6_central_rm_m"])]
        shares = (Decimal(r["existing_share"]),
                  Decimal(r["reallocated_share"]),
                  Decimal(r["new_share"]))
        if q(sum(shares)) != Decimal("1.000"):
            raise SystemExit(f"FATAL: funding shares for {pid} sum to {sum(shares)}, not 1.0")

        for scen, mult in SCENARIOS.items():
            amts = []
            for c in centrals:
                fixed = c * (Decimal("1") - vs)
                variable = c * vs
                amts.append(q(fixed + mult * variable))
            total = q(sum(amts))
            for i in range(3):
                scenario_phase_delivery[scen][i] += amts[i]
            ex, re_, nw = split_funding(total, shares)
            line_no += 1
            out.append(dict(
                cost_line_id=f"CL-{line_no:03d}",
                programme_id=pid,
                programme_name=name,
                pillar=pillar,
                lead_ministry=ministry,
                cost_category=r["cost_category"],
                price_base_year=PRICE_BASE_YEAR,
                scenario=scen,
                years_1_2=str(amts[0]),
                years_3_4=str(amts[1]),
                years_5_6=str(amts[2]),
                six_year_total=str(total),
                existing_funding=str(ex),
                reallocated_funding=str(re_),
                new_funding=str(nw),
                cost_method=r["cost_method"],
                assumption_ids=r["assumption_id"],
                confidence=r["confidence"],
                cost_source_id=r.get("cost_source_id", ""),
                funding_split_basis=r.get("funding_split_basis", ""),
                reach_count=r.get("reach_count", ""),
                reach_unit=r.get("reach_unit", "n/a"),
                overlap_group=r.get("overlap_group", "none"),
                phases_active=phases,
                notes=r["basis_and_benchmark"][:300],
            ))

    # ---- 2. Administration -------------------------------------------------
    admin_row = next(r for r in rows if r["assumption_id"] == "ASM-040")
    admin_shares = (Decimal(admin_row["existing_share"]),
                    Decimal(admin_row["reallocated_share"]),
                    Decimal(admin_row["new_share"]))
    scenario_phase_admin = {}
    for scen in SCENARIOS:
        amts = [q(d * ADMIN_RATE) for d in scenario_phase_delivery[scen]]
        scenario_phase_admin[scen] = amts
        total = q(sum(amts))
        ex, re_, nw = split_funding(total, admin_shares)
        line_no += 1
        out.append(dict(
            cost_line_id=f"CL-{line_no:03d}", programme_id="PRG-XX-ADMIN",
            programme_name="Portfolio administration overhead", pillar="X Delivery",
            lead_ministry="All lead ministries", cost_category="administration",
            price_base_year=PRICE_BASE_YEAR, scenario=scen,
            years_1_2=str(amts[0]), years_3_4=str(amts[1]), years_5_6=str(amts[2]),
            six_year_total=str(total), existing_funding=str(ex),
            reallocated_funding=str(re_), new_funding=str(nw),
            cost_method="4.0% of programme delivery cost (ASM-040)",
            assumption_ids="ASM-040", confidence="Provisional",
            cost_source_id="", funding_split_basis=admin_row.get("funding_split_basis", ""),
            reach_count="", reach_unit="n/a", overlap_group="none", phases_active="1-2-3",
            notes="Financial administration, procurement and compliance at delivering agencies. Excludes the delivery secretariat, costed at PRG-15.",
        ))

    # ---- 3. Contingency ----------------------------------------------------
    cont_row = next(r for r in rows if r["assumption_id"] == "ASM-041")
    cont_shares = (Decimal(cont_row["existing_share"]),
                   Decimal(cont_row["reallocated_share"]),
                   Decimal(cont_row["new_share"]))
    for scen in SCENARIOS:
        base = [scenario_phase_delivery[scen][i] + scenario_phase_admin[scen][i] for i in range(3)]
        amts = [q(b * CONTINGENCY_RATE) for b in base]
        total = q(sum(amts))
        ex, re_, nw = split_funding(total, cont_shares)
        line_no += 1
        out.append(dict(
            cost_line_id=f"CL-{line_no:03d}", programme_id="PRG-XX-CONT",
            programme_name="Portfolio contingency", pillar="X Delivery",
            lead_ministry="Ministry of Finance", cost_category="contingency",
            price_base_year=PRICE_BASE_YEAR, scenario=scen,
            years_1_2=str(amts[0]), years_3_4=str(amts[1]), years_5_6=str(amts[2]),
            six_year_total=str(total), existing_funding=str(ex),
            reallocated_funding=str(re_), new_funding=str(nw),
            cost_method="7.5% of delivery plus administration (ASM-041)",
            assumption_ids="ASM-041", confidence="Provisional",
            cost_source_id="", funding_split_basis=cont_row.get("funding_split_basis", ""),
            reach_count="", reach_unit="n/a", overlap_group="none", phases_active="1-2-3",
            notes="Set at the lower end of the 5-15% range because the portfolio is weighted towards recurrent service delivery rather than construction.",
        ))

    cols = ["cost_line_id", "programme_id", "programme_name", "pillar", "lead_ministry",
            "cost_category", "price_base_year", "scenario", "years_1_2", "years_3_4",
            "years_5_6", "six_year_total", "existing_funding", "reallocated_funding",
            "new_funding", "cost_method", "assumption_ids", "confidence",
            "cost_source_id", "funding_split_basis", "reach_count", "reach_unit",
            "overlap_group", "phases_active", "notes"]
    with open(MODEL, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    # ---- 4. Reach vs unique beneficiaries (C-06) --------------------------
    OVERLAP = {"household": Decimal("0.45")}   # ASM-030
    groups = {}
    for r in out:
        if r["scenario"] != "central" or not r["reach_count"]:
            continue
        groups.setdefault(r["overlap_group"], []).append(
            (r["programme_id"], Decimal(r["reach_count"]), r["reach_unit"]))
    bpath = os.path.join(HERE, "BENEFICIARY_RECONCILIATION.csv")
    with open(bpath, "w", newline="", encoding="utf-8") as fh:
        bw = csv.writer(fh)
        bw.writerow(["overlap_group", "unit", "programmes", "summed_reach",
                     "overlap_factor", "unique_estimate", "note"])
        for g, items in sorted(groups.items()):
            summed = sum(c for _, c, _ in items)
            f = OVERLAP.get(g, Decimal("0"))
            uniq = (summed * (Decimal("1") - f)).quantize(Decimal("1"))
            bw.writerow([g, items[0][2], ";".join(p for p, _, _ in items), str(summed),
                         str(f), str(uniq) if f else str(summed),
                         "Overlap factor from ASM-030 (provisional, VAL-25). Reach is NEVER summed "
                         "across overlap groups because the units differ." if f else
                         "No overlap factor applied: units are not interchangeable with other groups."])
    print(f"Wrote BENEFICIARY_RECONCILIATION.csv ({len(groups)} overlap groups)")
    print(f"Wrote {len(out)} cost lines to COSTING_MODEL.csv")
    for scen in ("conservative", "central", "expanded"):
        tot = sum(Decimal(r["six_year_total"]) for r in out if r["scenario"] == scen)
        new = sum(Decimal(r["new_funding"]) for r in out if r["scenario"] == scen)
        p = [sum(Decimal(r[k]) for r in out if r["scenario"] == scen)
             for k in ("years_1_2", "years_3_4", "years_5_6")]
        print(f"  {scen:>12}: total RM {tot:>10,.3f}m | new funding RM {new:>10,.3f}m | "
              f"phases {p[0]:,.1f} / {p[1]:,.1f} / {p[2]:,.1f}")


if __name__ == "__main__":
    main()
