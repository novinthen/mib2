"""Synchronise generated proposal/annex sections with canonical registers.

The CSV registers are the only authored source for portfolio financial figures.
This script renders every duplicated financial table and decision section in
the executive proposal and technical annexes. It also exposes the renderers to
verify_outputs.py so CI can fail if a document is stale.

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
ASSUMPTIONS = os.path.join(HERE, "ASSUMPTIONS_AND_DECISIONS.md")
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


def decision_data() -> list[dict[str, str]]:
    return load_csv("DECISION_REGISTER.csv")


def validation_data() -> list[dict[str, str]]:
    return load_csv("VALIDATION_REGISTER.csv")


def legal_data() -> list[dict[str, str]]:
    return load_csv("LEGAL_ISSUES_REGISTER.csv")


def fiscal_data() -> list[dict[str, str]]:
    return load_csv("FISCAL_VALIDATION_REGISTER.csv")


def render_fiscal_summary() -> str:
    rows = fiscal_data()
    scenarios = scenario_summary(cost_data()[0])
    central_phase_1 = scenarios["central"]["phase_1"]
    stage_counts = {
        stage: sum(row["validation_stage"] == stage for row in rows)
        for stage in ("phase_1_ceiling_gate", "programme_cost_gate", "later_phase_gate")
    }
    status_counts = {
        status: sum(row["status"] == status for row in rows)
        for status in sorted({row["status"] for row in rows})
    }
    return "\n".join([
        START.format(name="FISCAL_VALIDATION_SUMMARY"),
        "## 2.6 Phase 1 fiscal validation architecture",
        "",
        f"`FISCAL_VALIDATION_REGISTER.csv` controls **{len(rows)} Treasury questions**: "
        f"**{stage_counts['phase_1_ceiling_gate']} Phase 1 ceiling gates**, "
        f"**{stage_counts['programme_cost_gate']} programme-cost gates** and "
        f"**{stage_counts['later_phase_gate']} later-phase gate**. The current central Phase 1 figure of "
        f"**RM{money(central_phase_1, 1)} million is a gross planning cost, not a requested, net or "
        "Treasury-validated ceiling.**",
        "",
        "| Treasury block | Required result before a later implementation request |",
        "|---|---|",
        "| Existing allocations and reallocations | Vote-level confirmation of available, lawful and uncommitted funding; no displacement hidden as an existing contribution |",
        "| Incremental ceiling and staffing | Exact Phase 1 components, annual cash flow, net new requirement, accounting officer, establishment authority and fully loaded employment cost |",
        "| Unit costs and classifications | Evidence-backed quantities and rates, operating/development/object classification, chargeable vote and recurrent consequence |",
        "| Procurement, grants and exposure | Authorised transaction route, payment and recovery controls, capped federal exposure and treatment of matched or contingent obligations |",
        "| Scenarios and later years | Output-defined conservative/central/expanded options; Treasury price basis; Years 3–6 remain indicative and return through later appropriations |",
        "",
        "Current status: " + ", ".join(
            f"**{count} {status.replace('_', ' ')}**" for status, count in status_counts.items()
        ) + ". No modelled existing or reallocated amount is recognised as available funding, and no "
        "fiscal control may be marked `validated` without a Treasury evidence reference and acceptance date.",
        "",
        "**Submission boundary.** The later Cabinet paper must seek one Treasury-reviewed Phase 1 ceiling "
        "for an identified component package. It must show gross cost, confirmed existing allocations, "
        "approved reallocations and true incremental funding separately. Years 3–6 remain non-binding "
        "planning scenarios subject to evaluation, refreshed costing and separate appropriations.",
        END.format(name="FISCAL_VALIDATION_SUMMARY"),
    ])


def render_fiscal_register() -> str:
    rows = fiscal_data()
    labels = {
        "phase_1_ceiling_gate": "Phase 1 ceiling gates",
        "programme_cost_gate": "Programme-cost gates",
        "later_phase_gate": "Later-phase gate",
    }
    lines = [
        START.format(name="FISCAL_VALIDATION_REGISTER"),
        "**Fiscal status rule.** This register instructs Treasury and lead-ministry validation; it is not "
        "a Treasury memorandum and records no appropriation. `Requested` and `received` are workflow "
        "states only. `Validated`, `validated_with_conditions` or `rejected` requires a Ministry of "
        "Finance evidence reference and acceptance date.",
        "",
    ]
    for stage, label in labels.items():
        selected = [row for row in rows if row["validation_stage"] == stage]
        lines += [f"### {label} ({len(selected)})", ""]
        for row in selected:
            lines += [
                f"#### {row['fiscal_control_id']} — {row['domain'].replace('_', ' ').title()}",
                "",
                f"- **Validation question:** {row['validation_question']}",
                f"- **Current model position:** {row['provisional_model_position']}",
                f"- **Required evidence:** {row['required_evidence']}",
                f"- **Validation owner:** {row['validation_owner']}",
                f"- **Supporting bodies:** {row['supporting_bodies']}",
                f"- **Affected programmes / decisions:** {row['affected_programmes']} / {row['affected_decisions']}",
                f"- **Related validation controls:** {row['related_validation_ids']}",
                f"- **Consequence if unresolved:** {row['consequence_if_unresolved']}",
                f"- **Status:** `{row['status']}`",
                "",
            ]
    lines += [
        "**Ceiling rule.** A validated Phase 1 ceiling exists only when FIS-01, FIS-02, FIS-03 and "
        "FIS-07 are validated and every included component has cleared its applicable programme-cost "
        "gates. A component that remains open is excluded or shown separately as a non-approved sensitivity; "
        "it cannot be absorbed into contingency.",
        END.format(name="FISCAL_VALIDATION_REGISTER"),
    ]
    return "\n".join(lines)


def render_phase_1_fiscal_schedule() -> str:
    rows, central_rows = cost_data()
    scenarios = scenario_summary(rows)
    selected = sorted(central_rows, key=lambda row: row["cost_line_id"])
    lines = [
        START.format(name="PHASE_1_FISCAL_SCHEDULE"),
        "## Annex L — Phase 1 fiscal validation schedule",
        "",
        "The schedule below is generated from the central rows of `COSTING_MODEL.csv`. It states gross "
        "Years 1–2 cost only. The model's existing/reallocated/new columns cover six years and are not "
        "apportioned here because no ministry or Treasury has confirmed a Phase 1 funding split.",
        "",
        "| Cost line | Programme / portfolio line | Lead ministry | Planning category | Phase 1 gross cost | Confidence |",
        "|---|---|---|---|---:|---|",
    ]
    for row in selected:
        lines.append(
            f"| {row['cost_line_id']} | {row['programme_id']} — {row['programme_name']} | "
            f"{row['lead_ministry']} | {row['cost_category'].replace('_', ' ')} | "
            f"RM{money(d(row['years_1_2']))}m | {row['confidence']} |"
        )
    lines += [
        f"| **Total** | **Central planning case** |  |  | **RM{money(scenarios['central']['phase_1'])}m** | **Unvalidated** |",
        "",
        "### L.1 Scenario boundary",
        "",
        "| Scenario | Phase 1 gross planning cost | Status |",
        "|---|---:|---|",
        f"| Conservative | RM{money(scenarios['conservative']['phase_1'])}m | Cost sensitivity only; output package not yet specified |",
        f"| Central | RM{money(scenarios['central']['phase_1'])}m | Gross design case; not a ceiling or request |",
        f"| Expanded | RM{money(scenarios['expanded']['phase_1'])}m | Cost sensitivity only; output package not yet specified |",
        "",
        "Before submission for implementation, MOF must replace this gross schedule with an accepted "
        "annual schedule of components and outputs showing confirmed existing funding, approved reallocation "
        "and incremental funding by vote, programme/activity, object, accounting officer and transaction route. "
        "The validated total may be lower or higher than the current central case; it is not mechanically "
        "selected from these three sensitivities.",
        END.format(name="PHASE_1_FISCAL_SCHEDULE"),
    ]
    return "\n".join(lines)


def render_legal_summary() -> str:
    rows = legal_data()
    status_counts = {
        status: sum(row["status"] == status for row in rows)
        for status in sorted({row["status"] for row in rows})
    }
    pre_submission = sum(row["clearance_stage"] == "pre_submission_clearance" for row in rows)
    programme_launch = sum(row["clearance_stage"] == "programme_launch_clearance" for row in rows)
    prg04 = [row["legal_issue_id"] for row in rows if row["legal_issue_id"].startswith("LGL-1") and row["legal_issue_id"] >= "LGL-13"]
    lines = [
        START.format(name="LEGAL_CLEARANCE_SUMMARY"),
        "## 2.5 Legal and jurisdictional clearance architecture",
        "",
        f"`LEGAL_ISSUES_REGISTER.csv` controls **{len(rows)} legal issues**: "
        f"**{pre_submission} pre-submission clearances** and **{programme_launch} programme-launch clearances**. "
        "This is an issues and instructions matrix, not legal advice. **No issue is recorded as cleared, "
        "and no written AGC or other competent-authority clearance has been obtained by this drafting exercise.**",
        "",
        "| Clearance block | Issues | Required result |",
        "|---|---|---|",
        "| Constitutional targeting and discretion | LGL-01 to LGL-04 | AGC defines the lawful boundary for equality, education aid, public-service impartiality and citizenship/documentation administration |",
        "| Institutional, financial and procurement authority | LGL-05 to LGL-08 | Every function, payment and procurement has a competent body, lawful instrument, accounting officer and operative approval route |",
        "| Data governance and sharing | LGL-09 to LGL-11 | Government and private-party processing, linkage, disclosure, retention, correction and breach controls are identified dataset by dataset |",
        "| Federal-state jurisdiction | LGL-12 | Each participating state confirms the applicable land, local-government, housing and approval route, including Sabah and Sarawak differences |",
        f"| PRG-04 pathway-specific clearance | {prg04[0]} to {prg04[-1]} | Public purpose, consent, Islamic-administration, temple/estate referral, excluded expenditure and religion-data rules are separately cleared |",
        "",
        "Current status: " + ", ".join(
            f"**{count} {status.replace('_', ' ')}**" for status, count in status_counts.items()
        ) + ". `Received` evidence does not equal clearance. A status may change to `cleared` or "
        "`cleared_with_conditions` only when the register contains "
        "the competent authority's written evidence reference and acceptance date. A conditional clearance must "
        "state every condition in the evidence itself; the drafting secretariat cannot infer or waive it.",
        "",
        "**Current-law control.** AGC's legislation portal now lists the Government Procurement Act 2026 "
        "[Act 882]. LGL-08 therefore requires MOF and AGC to identify its commencement, subsidiary and "
        "transitional instruments and the regime applicable to each transaction. The proposal does not assume "
        "that either the new Act or the prior administrative framework applies without that confirmation.",
        "",
        "**Legal no-cascade rule.** An unresolved issue blocks only the programmes and decisions identified "
        "against it. PRG-04 state or religious-authority clearance is facility- and jurisdiction-specific unless "
        "the competent authority concludes that the defect affects the national instrument itself.",
        END.format(name="LEGAL_CLEARANCE_SUMMARY"),
    ]
    return "\n".join(lines)


def render_legal_register() -> str:
    rows = legal_data()
    labels = {
        "pre_submission_clearance": "Pre-submission legal clearances",
        "programme_launch_clearance": "Programme-launch legal clearances",
    }
    lines = [
        START.format(name="LEGAL_ISSUES_REGISTER"),
        "**Legal status rule.** This matrix identifies questions for competent authorities. It does not "
        "express a legal opinion or certify compliance. Every issue starts as `open`. "
        "`Requested` and `received` record workflow, not legal sufficiency. `Cleared`, "
        "`cleared_with_conditions` or `not_cleared` requires a written evidence reference and acceptance date.",
        "",
    ]
    for stage, label in labels.items():
        selected = [row for row in rows if row["clearance_stage"] == stage]
        lines += [f"### {label} ({len(selected)})", ""]
        for row in selected:
            lines += [
                f"#### {row['legal_issue_id']} — {row['domain'].replace('_', ' ').title()}",
                "",
                f"- **Authority:** {row['legal_authority']} ({row['authority_source_ids']})",
                f"- **Question for clearance:** {row['legal_question']}",
                f"- **Provisional design position:** {row['provisional_design_position']}",
                f"- **Required written clearance:** {row['required_written_clearance']}",
                f"- **Clearance owner:** {row['clearance_owner']}",
                f"- **Bodies to consult:** {row['consulted_bodies']}",
                f"- **Affected programmes / decisions:** {row['affected_programmes']} / {row['affected_decisions']}",
                f"- **Related validation controls:** {row['related_validation_ids']}",
                f"- **Consequence if unresolved:** {row['consequence_if_unresolved']}",
                f"- **Status:** `{row['status']}`",
                "",
            ]
    lines += [
        "**Recording rule.** The secretariat may record and index advice but may not mark its own legal "
        "position as cleared. Conflicting advice is escalated to the named clearance owner and remains "
        "`received` or `not_cleared` until the competent authority resolves it in writing.",
        END.format(name="LEGAL_ISSUES_REGISTER"),
    ]
    return "\n".join(lines)


def render_validation_summary() -> str:
    rows = validation_data()
    labels = {
        "pre_submission_gate": "Pre-submission gate",
        "programme_launch_gate": "Programme-launch gate",
        "phase_expansion_gate": "Phase-expansion gate",
        "operational_baseline": "Operational baseline",
        "deferrable_design_matter": "Deferrable design matter",
    }
    counts = {key: sum(row["classification"] == key for row in rows) for key in labels}
    strict = [row["validation_id"] for row in rows if row["criticality"] == "strict_gate"]
    conditional = [
        row["validation_id"] for row in rows
        if row["criticality"] == "decision_dependent_critical"
    ]
    lines = [
        START.format(name="VALIDATION_SUMMARY"),
        "## 2.4 Validation control architecture",
        "",
        "The thirty validation items are not one undifferentiated condition. Each is assigned to "
        "the earliest decision it can legitimately block:",
        "",
        "| Classification | Items | Control effect |",
        "|---|---:|---|",
        f"| **{labels['pre_submission_gate']}** | {counts['pre_submission_gate']} | Must resolve before the affected implementation or funding decision is submitted |",
        f"| **{labels['programme_launch_gate']}** | {counts['programme_launch_gate']} | Blocks only the named programme or jurisdiction |",
        f"| **{labels['phase_expansion_gate']}** | {counts['phase_expansion_gate']} | Blocks scale-up or later-phase appropriation, not controlled Phase 1 work |",
        f"| **{labels['operational_baseline']}** | {counts['operational_baseline']} | May be established during operations but must precede target calibration |",
        f"| **{labels['deferrable_design_matter']}** | {counts['deferrable_design_matter']} | Does not block submission or launch unless the disputed material is used |",
        "",
        f"The six strict gates remain **{', '.join(strict)}**. Four further items — "
        f"**{', '.join(conditional)}** — are decision-dependent critical: they become "
        "submission blockers only if the later request relies on the affected funding, measurement, "
        "governance or reallocation proposition.",
        "",
        "Every item has one accountable owner, supporting agencies, required evidence, a control "
        "deadline, escalation route, financial consequence, affected decision and controlled status. "
        "The deadlines run from Cabinet notification or the stated programme/phase event; they are "
        "management controls, not statutory time limits. Status is restricted to `open`, `requested`, "
        "`received`, `accepted` or `disputed`.",
        "",
        "**No-cascade rule.** An unresolved item blocks only the decision IDs listed against it in "
        "`VALIDATION_REGISTER.csv`. It does not suspend unrelated validation work or programmes.",
        END.format(name="VALIDATION_SUMMARY"),
    ]
    return "\n".join(lines)


def render_validation_register() -> str:
    rows = validation_data()
    labels = {
        "pre_submission_gate": "Pre-submission gates",
        "programme_launch_gate": "Programme-launch gates",
        "phase_expansion_gate": "Phase-expansion gates",
        "operational_baseline": "Operational baselines",
        "deferrable_design_matter": "Deferrable design matters",
    }
    lines = [
        START.format(name="VALIDATION_REGISTER"),
        "**Control rule.** Classification determines when an unresolved item can block action. "
        "Criticality is separate: `strict_gate` preserves the six existing hard gates, while "
        "`decision_dependent_critical` identifies VAL-03, VAL-24, VAL-27 and VAL-28 as blockers "
        "only when the proposed decision relies on them.",
        "",
    ]
    for category in labels:
        selected = [row for row in rows if row["classification"] == category]
        lines += [f"### {labels[category]} ({len(selected)})", ""]
        for row in selected:
            criticality = row["criticality"].replace("_", " ")
            lines += [
                f"#### {row['validation_id']} — {row['item']}",
                "",
                f"- **Criticality / status:** {criticality}; `{row['status']}`",
                f"- **Accountable owner:** {row['accountable_owner']}",
                f"- **Supporting agencies:** {row['supporting_agencies']}",
                f"- **Required evidence:** {row['required_evidence']}",
                f"- **Control deadline:** {row['deadline']}",
                f"- **Escalation:** {row['escalation_route']}",
                f"- **Financial consequence if unresolved:** {row['financial_consequence']}",
                f"- **Decision affected:** {row['decision_affected_if_unresolved']}",
                "",
            ]
    lines += [
        "**Status control.** Only the accountable owner may propose `accepted`; the interim "
        "secretariat records the evidence reference and acceptance date. `Received` does not mean "
        "accepted. Conflicting or incomplete evidence is `disputed` and follows the stated escalation route.",
        END.format(name="VALIDATION_REGISTER"),
    ]
    return "\n".join(lines)


def render_decision_architecture() -> str:
    rows = decision_data()
    labels = {
        "approve_now": "Approve now",
        "conditional_endorsement": "Endorse conditionally",
        "not_for_approval_now": "Do not approve now",
    }
    introductions = {
        "approve_now": (
            "These decisions create authority to validate and prepare. They do not launch the "
            "six-year programme or approve new expenditure."
        ),
        "conditional_endorsement": (
            "These propositions may guide detailed design, but have no operative effect unless "
            "their stated dependencies are cleared and a later decision expressly activates them."
        ),
        "not_for_approval_now": (
            "These exclusions are part of the decision itself. Silence or general endorsement must "
            "not be interpreted as approval of any item below."
        ),
    }
    lines = [START.format(name="DECISION_ARCHITECTURE")]
    for category in ("approve_now", "conditional_endorsement", "not_for_approval_now"):
        selected = [row for row in rows if row["category"] == category]
        lines += [f"## 2.{1 + list(labels).index(category)} {labels[category]}", "", introductions[category], ""]
        if category == "not_for_approval_now":
            lines += ["| # | Excluded decision | Required before reconsideration |", "|---|---|---|"]
            for row in selected:
                lines.append(f"| **{row['decision_id']}** | {row['decision_text']} | {row['dependency']} |")
        else:
            lines += ["| # | Decision | What it authorises | What it does **not** authorise |", "|---|---|---|---|"]
            for row in selected:
                lines.append(
                    f"| **{row['decision_id']}** | {row['decision_text']} | "
                    f"{row['what_it_authorises']} | {row['what_it_does_not_authorise']} |"
                )
        lines.append("")
    lines += [
        "**Decision rule.** Only AN-01 to AN-05 would take effect on this preliminary decision. "
        "CE-01 to CE-04 are design parameters, not operative approvals. NA-01 to NA-07 are "
        "express exclusions. If the recorded Cabinet decision does not preserve that distinction, "
        "the sponsoring ministry must correct the record before undertaking any action.",
        END.format(name="DECISION_ARCHITECTURE"),
    ]
    return "\n".join(lines)


def render_final_decision_resolution() -> str:
    rows = decision_data()
    approve = [row for row in rows if row["category"] == "approve_now"]
    conditional = [row for row in rows if row["category"] == "conditional_endorsement"]
    excluded = [row for row in rows if row["category"] == "not_for_approval_now"]
    lines = [
        START.format(name="FINAL_DECISION_RESOLUTION"),
        "Cabinet is respectfully invited to:",
        "",
        "### Approve now",
        "",
    ]
    lines += [f"{i}. **{row['decision_id']}:** {row['decision_text']}" for i, row in enumerate(approve, 1)]
    lines += ["", "### Endorse conditionally", ""]
    lines += [f"{i}. **{row['decision_id']}:** {row['decision_text']}" for i, row in enumerate(conditional, 1)]
    lines += ["", "### Record as not approved at this stage", ""]
    lines += [f"{i}. **{row['decision_id']}:** {row['decision_text']}" for i, row in enumerate(excluded, 1)]
    lines += [
        "",
        "For avoidance of doubt, this resolution creates no appropriation, procurement authority, "
        "statutory power, permanent establishment, programme launch, third-party commitment or "
        "beneficiary entitlement. Any later implementation authority must identify the approved "
        "programme components, ceiling, funding source, accounting officer, legal basis, launch "
        "conditions and review gate.",
        END.format(name="FINAL_DECISION_RESOLUTION"),
    ]
    return "\n".join(lines)


def render_phase_table() -> str:
    rows, _ = cost_data()
    central = scenario_summary(rows)["central"]
    return "\n".join([
        START.format(name="PHASE_TABLE"),
        "| | **Phase 1 (Years 1–2)** | **Phase 2 (Years 3–4)** | **Phase 3 (Years 5–6)** |",
        "|---|---|---|---|",
        "| **Purpose** | Establish what does not exist | Build the pathways | Consolidate and graduate |",
        f"| **Indicative central planning cost** | RM{money(central['phase_1'], 1)}m | RM{money(central['phase_2'], 1)}m | RM{money(central['phase_3'], 1)}m |",
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

    lines = [START.format(name="PROPOSAL_FINANCE"), "## 7.1 Indicative planning scenarios — not approval envelopes", "",
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
        f"**The indicative central scenario has a gross portfolio cost of RM{money(total)} million and a modelled incremental new fiscal requirement of RM{money(scenarios['central']['new'])} million** — approximately RM{scenarios['central']['new'] / Decimal(6):.0f} million per year averaged over six years, against MITRA's verified 2026 allocation of RM150 million (CLM-019). The remaining RM{money(non_new)} million is modelled as RM{money(scenarios['central']['existing'])} million of existing allocations and RM{money(scenarios['central']['reallocated'])} million of proposed reallocations. These are unverified planning classifications, not recognised funding sources, and remain subject to Treasury and ministry validation.",
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
        "**No cost line in this portfolio is Confirmed.** The central scenario is therefore presented for conditional endorsement as a planning case only, not as a fiscal framework or envelope for approval. No programme in this proposal is described as fully costed while material assumptions remain provisional.",
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
        "DECISION_ARCHITECTURE": render_decision_architecture(),
        "VALIDATION_SUMMARY": render_validation_summary(),
        "VALIDATION_REGISTER": render_validation_register(),
        "LEGAL_CLEARANCE_SUMMARY": render_legal_summary(),
        "LEGAL_ISSUES_REGISTER": render_legal_register(),
        "FISCAL_VALIDATION_SUMMARY": render_fiscal_summary(),
        "FISCAL_VALIDATION_REGISTER": render_fiscal_register(),
        "PHASE_TABLE": render_phase_table(),
        "PROPOSAL_FINANCE": render_proposal_finance(),
        "FINAL_DECISION_RESOLUTION": render_final_decision_resolution(),
        "TECHNICAL_ANNEX_A": render_technical_annex_a(),
        "PHASE_1_FISCAL_SCHEDULE": render_phase_1_fiscal_schedule(),
    }


def main() -> None:
    with open(PROPOSAL, encoding="utf-8", newline="") as fh:
        proposal = fh.read()
    proposal_eol = "\r\n" if "\r\n" in proposal else "\n"
    proposal = replace_generated(proposal, "DECISION_ARCHITECTURE", render_decision_architecture().replace("\n", proposal_eol))
    proposal = replace_generated(proposal, "VALIDATION_SUMMARY", render_validation_summary().replace("\n", proposal_eol))
    proposal = replace_generated(proposal, "LEGAL_CLEARANCE_SUMMARY", render_legal_summary().replace("\n", proposal_eol))
    proposal = replace_generated(proposal, "FISCAL_VALIDATION_SUMMARY", render_fiscal_summary().replace("\n", proposal_eol))
    proposal = replace_generated(proposal, "PHASE_TABLE", render_phase_table().replace("\n", proposal_eol))
    proposal = replace_generated(proposal, "PROPOSAL_FINANCE", render_proposal_finance().replace("\n", proposal_eol))
    proposal = replace_generated(proposal, "FINAL_DECISION_RESOLUTION", render_final_decision_resolution().replace("\n", proposal_eol))
    with open(PROPOSAL, "w", encoding="utf-8", newline="") as fh:
        fh.write(proposal)

    with open(ANNEXES, encoding="utf-8", newline="") as fh:
        annexes = fh.read()
    annex_eol = "\r\n" if "\r\n" in annexes else "\n"
    annexes = replace_generated(
        annexes, "TECHNICAL_ANNEX_A", render_technical_annex_a().replace("\n", annex_eol)
    )
    annexes = replace_generated(
        annexes, "PHASE_1_FISCAL_SCHEDULE", render_phase_1_fiscal_schedule().replace("\n", annex_eol)
    )
    with open(ANNEXES, "w", encoding="utf-8", newline="") as fh:
        fh.write(annexes)

    with open(ASSUMPTIONS, encoding="utf-8", newline="") as fh:
        assumptions = fh.read()
    assumptions_eol = "\r\n" if "\r\n" in assumptions else "\n"
    assumptions = replace_generated(
        assumptions, "VALIDATION_REGISTER", render_validation_register().replace("\n", assumptions_eol)
    )
    assumptions = replace_generated(
        assumptions, "LEGAL_ISSUES_REGISTER", render_legal_register().replace("\n", assumptions_eol)
    )
    assumptions = replace_generated(
        assumptions, "FISCAL_VALIDATION_REGISTER", render_fiscal_register().replace("\n", assumptions_eol)
    )
    with open(ASSUMPTIONS, "w", encoding="utf-8", newline="") as fh:
        fh.write(assumptions)
    print("Synchronised generated integrity sections in proposal, assumptions and technical annexes")


if __name__ == "__main__":
    main()
