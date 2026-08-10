"""Synchronise generated proposal/annex sections with canonical registers.

The CSV registers are the only authored source for portfolio financial figures.
This script renders every duplicated financial table in the executive proposal
and technical annexes.  It also exposes the renderers to verify_outputs.py so
CI can fail if a document is stale.

Usage: python outputs/sync_document_integrity.py
"""

from __future__ import annotations

import csv
import os
from collections import defaultdict
from decimal import Decimal


HERE = os.path.dirname(os.path.abspath(__file__))
PROPOSAL = os.path.join(HERE, "MIB_2.0_EXECUTIVE_PROPOSAL.md")
ANNEXES = os.path.join(HERE, "TECHNICAL_ANNEXES.md")
START = "<!-- GENERATED:{name}:START -->"
END = "<!-- GENERATED:{name}:END -->"


def load_csv(name: str) -> list[dict[str, str]]:
    with open(os.path.join(HERE, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def d(value: str) -> Decimal:
    return Decimal(value)


def money(value: Decimal, decimals: int = 3) -> str:
    return f"{value:,.{decimals}f}"


def percent(value: Decimal, total: Decimal) -> str:
    return f"{value / total * 100:.1f}%"


def aggregate(rows: list[dict[str, str]], column: str) -> dict[str, Decimal]:
    out: dict[str, Decimal] = defaultdict(Decimal)
    for row in rows:
        out[row[column]] += d(row["six_year_total"])
    return dict(out)


def cost_data() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows = load_csv("COSTING_MODEL.csv")
    central = [row for row in rows if row["scenario"] == "central"]
    return rows, central


def scenario_summary(rows: list[dict[str, str]]) -> dict[str, dict[str, Decimal]]:
    result = {}
    for scenario in ("conservative", "central", "expanded"):
        selected = [row for row in rows if row["scenario"] == scenario]
        result[scenario] = {
            "total": sum(d(row["six_year_total"]) for row in selected),
            "phase_1": sum(d(row["years_1_2"]) for row in selected),
            "phase_2": sum(d(row["years_3_4"]) for row in selected),
            "phase_3": sum(d(row["years_5_6"]) for row in selected),
            "existing": sum(d(row["existing_funding"]) for row in selected),
            "reallocated": sum(d(row["reallocated_funding"]) for row in selected),
            "new": sum(d(row["new_funding"]) for row in selected),
        }
    return result


def render_phase_table() -> str:
    rows, _ = cost_data()
    central = scenario_summary(rows)["central"]
    return "\n".join([
        START.format(name="PHASE_TABLE"),
        "| | **Phase 1 (Years 1–2)** | **Phase 2 (Years 3–4)** | **Phase 3 (Years 5–6)** |",
        "|---|---|---|---|",
        "| **Purpose** | Establish what does not exist | Build the pathways | Consolidate and graduate |",
        f"| **Central cost** | RM{money(central['phase_1'], 1)}m | RM{money(central['phase_2'], 1)}m | RM{money(central['phase_3'], 1)}m |",
        "| **Defining deliverables** | Verified caseload baseline; 528 SJKT audits; baseline survey; DPIA; dashboard live; secretariat operational; 12 of 16 KPIs baselined | TVET pipeline at scale; enterprise advisory; housing legacy review tabled; first disaggregated intake series published for three consecutive years | Savings scheme at scale; graduation measurement; final independent evaluation |",
        "| **Gate** | **End-Year 2 administrative readiness review:** Cabinet or its authorised committee decides whether Phase 2 may proceed, be corrected or be re-scoped | **End-Year 3 independent mid-term evaluation:** determines whether Phase 3 may proceed and whether ongoing Phase 2 delivery must be corrected or re-scoped | **Year 6 final evaluation:** informs successor arrangements; creates no automatic continuation |",
        END.format(name="PHASE_TABLE"),
    ])


def render_proposal_finance() -> str:
    rows, central_rows = cost_data()
    scenarios = scenario_summary(rows)
    confidence = aggregate(central_rows, "confidence")
    total = scenarios["central"]["total"]
    non_new = scenarios["central"]["existing"] + scenarios["central"]["reallocated"]

    lines = [START.format(name="PROPOSAL_FINANCE"), "## 7.1 The envelope", "",
             "| Scenario | Six-year total | Phase 1 | Phase 2 | Phase 3 | New funding |",
             "|---|---:|---:|---:|---:|---:|"]
    for scenario, label in (("conservative", "Conservative"),
                            ("central", "Central"), ("expanded", "Expanded")):
        values = scenarios[scenario]
        bold = "**" if scenario == "central" else ""
        lines.append(
            f"| {bold}{label}{bold} | {bold}RM{money(values['total'])}m{bold} | "
            f"{bold}RM{money(values['phase_1'], 1)}m{bold} | {bold}RM{money(values['phase_2'], 1)}m{bold} | "
            f"{bold}RM{money(values['phase_3'], 1)}m{bold} | {bold}RM{money(values['new'])}m{bold} |"
        )
    lines += [
        "",
        "Scenarios are **sensitivity cases on identical programme definitions**, not alternative blueprints. Conservative applies 0.75× and expanded 1.30× to the variable component of each programme; fixed components (systems, audits, secretariat, evaluations) do not scale. The conservative case approximates the position if participation across the portfolio runs 25% below plan.",
        "",
        f"**Gross portfolio cost is RM{money(total)} million. The incremental new fiscal requirement is RM{money(scenarios['central']['new'])} million** — approximately RM{scenarios['central']['new'] / Decimal(6):.0f} million per year averaged over six years, against MITRA's verified 2026 allocation of RM150 million (CLM-019). The remaining RM{money(non_new)} million comprises RM{money(scenarios['central']['existing'])} million of existing allocations and RM{money(scenarios['central']['reallocated'])} million of proposed reallocations. Both classifications remain subject to Treasury and ministry validation.",
        "",
        "## 7.2 Confidence",
        "",
        "| Class | Central amount | Share |",
        "|---|---:|---:|",
    ]
    descriptions = {
        "Confirmed": "supported by authoritative programme, financial or procurement data",
        "Benchmarked": "based on comparable official programmes or credible unit-cost evidence",
        "Provisional": "transparent but unverified assumptions",
    }
    for classification in ("Confirmed", "Benchmarked", "Provisional"):
        amount = confidence.get(classification, Decimal(0))
        lines.append(f"| **{classification}** — {descriptions[classification]} | RM{money(amount)}m | **{percent(amount, total)}** |")
    lines += [
        "",
        "**No cost line in this portfolio is Confirmed.** That is stated plainly because it determines what Cabinet is being asked to approve: a framework in principle, not a fully costed implementation programme. No programme in this proposal is described as fully costed while material assumptions remain provisional.",
        END.format(name="PROPOSAL_FINANCE"),
    ]
    return "\n".join(lines)


def render_technical_annex_a() -> str:
    rows, central_rows = cost_data()
    programmes = load_csv("PROGRAMME_REGISTER.csv")
    non_retained = sum(1 for row in programmes
                       if not row["retain_decision"].upper().startswith("RETAIN"))
    scenarios = scenario_summary(rows)
    total = scenarios["central"]["total"]
    lines = [START.format(name="TECHNICAL_ANNEX_A"),
             "## Annex A — Six-year costing model, central scenario", "",
             "Generated by `build_costing.py` from `COSTING_ASSUMPTIONS.csv`; this entire annex section is generated by `sync_document_integrity.py` and verified by `verify_outputs.py`.", "",
             "| ID | Programme | Pillar | Lead ministry | Yrs 1–2 | Yrs 3–4 | Yrs 5–6 | **Total** | Existing | Realloc. | **New** | Confidence |",
             "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for row in central_rows:
        pid = row["programme_id"] if not row["programme_id"].startswith("PRG-XX") else "—"
        lines.append(
            f"| {pid} | {row['programme_name']} | {row['pillar']} | {row['lead_ministry']} | "
            f"{money(d(row['years_1_2']))} | {money(d(row['years_3_4']))} | {money(d(row['years_5_6']))} | "
            f"**{money(d(row['six_year_total']))}** | {money(d(row['existing_funding']))} | "
            f"{money(d(row['reallocated_funding']))} | {money(d(row['new_funding']))} | {row['confidence']} |"
        )
    c = scenarios["central"]
    lines += [
        f"| | **TOTAL** | | | **{money(c['phase_1'])}** | **{money(c['phase_2'])}** | **{money(c['phase_3'])}** | **{money(c['total'])}** | **{money(c['existing'])}** | **{money(c['reallocated'])}** | **{money(c['new'])}** | |",
        "",
        f"*Portfolio-count convention: {sum(1 for row in central_rows if row['programme_id'].startswith('PRG-') and not row['programme_id'].startswith('PRG-XX'))} retained substantive programme rows plus {sum(1 for row in central_rows if row['programme_id'].startswith('PRG-XX'))} portfolio-level financial rows (administration and contingency) = {len(central_rows)} central-scenario cost lines. The programme register separately preserves {non_retained} non-retained source proposals for auditability.*",
        "",
        f"*Column check: {money(c['phase_1'])} + {money(c['phase_2'])} + {money(c['phase_3'])} = {money(c['total'])}. Funding check: {money(c['existing'])} + {money(c['reallocated'])} + {money(c['new'])} = {money(c['total'])}. Both are machine-verified.*",
    ]

    dimensions = [
        ("A.1 Reconciliation by pillar", "pillar", "Pillar"),
        ("A.2 Reconciliation by cost category", "cost_category", "Category"),
        ("A.3 Reconciliation by lead ministry", "lead_ministry", "Ministry / agency"),
    ]
    labels = {
        "operating_expenditure": "Operating expenditure",
        "transfer_grant": "Transfers and grants",
        "development_expenditure": "Development expenditure",
        "monitoring_evaluation": "Monitoring and evaluation",
        "administration": "Administration",
        "contingency": "Contingency",
    }
    for heading, column, label in dimensions:
        values = aggregate(central_rows, column)
        lines += ["", f"### {heading}", "", f"| {label} | Central total | Share |", "|---|---:|---:|"]
        for key, value in sorted(values.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {labels.get(key, key)} | {money(value)} | {percent(value, total)} |")
        lines.append(f"| **Total** | **{money(total)}** | **100.0%** |")

    lines += ["", "### A.4 Scenario comparison", "",
              "| | Conservative | Central | Expanded |", "|---|---:|---:|---:|"]
    for key, label, decimals in (("phase_1", "Phase 1", 1), ("phase_2", "Phase 2", 1),
                                 ("phase_3", "Phase 3", 1), ("total", "**Six-year total**", 3),
                                 ("new", "**New funding**", 3)):
        vals = [money(scenarios[s][key], decimals) for s in ("conservative", "central", "expanded")]
        lines.append(f"| {label} | {vals[0]} | {vals[1]} | {vals[2]} |")
    variance_con = (scenarios["conservative"]["total"] / total - 1) * 100
    variance_exp = (scenarios["expanded"]["total"] / total - 1) * 100
    lines += [
        f"| Variance vs central | {variance_con:.1f}% | — | +{variance_exp:.1f}% |",
        "",
        "Scenarios apply 0.75× / 1.00× / 1.30× to the **variable component only**. Fixed components — systems, audits, secretariat and evaluations — do not scale. Programme definitions, owners, categories, confidence classes and price base are identical across all three scenarios: these are sensitivity cases, not alternative blueprints.",
        END.format(name="TECHNICAL_ANNEX_A"),
    ]
    return "\n".join(lines)


def replace_generated(text: str, name: str, rendered: str) -> str:
    start = START.format(name=name)
    end = END.format(name=name)
    if start not in text or end not in text:
        raise ValueError(f"missing generated markers for {name}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + rendered + after


def expected_sections() -> dict[str, str]:
    return {
        "PHASE_TABLE": render_phase_table(),
        "PROPOSAL_FINANCE": render_proposal_finance(),
        "TECHNICAL_ANNEX_A": render_technical_annex_a(),
    }


def main() -> None:
    with open(PROPOSAL, encoding="utf-8", newline="") as fh:
        proposal = fh.read()
    proposal_eol = "\r\n" if "\r\n" in proposal else "\n"
    proposal = replace_generated(proposal, "PHASE_TABLE", render_phase_table().replace("\n", proposal_eol))
    proposal = replace_generated(proposal, "PROPOSAL_FINANCE", render_proposal_finance().replace("\n", proposal_eol))
    with open(PROPOSAL, "w", encoding="utf-8", newline="") as fh:
        fh.write(proposal)

    with open(ANNEXES, encoding="utf-8", newline="") as fh:
        annexes = fh.read()
    annex_eol = "\r\n" if "\r\n" in annexes else "\n"
    annexes = replace_generated(
        annexes, "TECHNICAL_ANNEX_A", render_technical_annex_a().replace("\n", annex_eol)
    )
    with open(ANNEXES, "w", encoding="utf-8", newline="") as fh:
        fh.write(annexes)
    print("Synchronised generated integrity sections in proposal and technical annexes")


if __name__ == "__main__":
    main()
