# Data Quality Methodology

This document describes how data quality is maintained across the MIB 2.0 website.

## Authoritative Sources

All data derives from CSV registers in `../outputs/`:

- `PROGRAMME_REGISTER.csv`
- `KPI_REGISTER.csv`
- `COSTING_MODEL.csv`
- `RISK_AND_SAFEGUARD_REGISTER.csv`
- `CLAIMS_AND_FIGURES_REGISTER.csv`
- `SOURCE_REGISTER.csv`
- `RESPONSIBILITY_MATRIX.csv`
- `COSTING_ASSUMPTIONS.csv`
- `BENEFICIARY_RECONCILIATION.csv`
- `CONFLICT_AND_DUPLICATION_REGISTER.csv`
- `NARRATIVE_REGISTER.csv`
- `DECISION_REGISTER.csv`
- `VALIDATION_REGISTER.csv`
- `LEGAL_ISSUES_REGISTER.csv`
- `FISCAL_VALIDATION_REGISTER.csv`

These files are the **single source of truth**. The website displays them; it does not store data separately.

## Validation at Build Time

The `lib/data-loader.ts` module performs strict validation:

### 1. Duplicate ID Check

Every register with an ID column must have unique IDs. Duplicates fail the build.

```typescript
const seenIds = new Set<string>();
if (seenIds.has(id)) {
  throw new ValidationError(`Duplicate ID ${id}`);
}
```

### 2. Foreign Key Validation

References between registers must resolve:

- `KPI_REGISTER.programme_id` → `PROGRAMME_REGISTER.programme_id`
- `COSTING_MODEL.programme_id` → `PROGRAMME_REGISTER.programme_id`
- `RESPONSIBILITY_MATRIX.programme_id` → `PROGRAMME_REGISTER.programme_id`

Exception: `PRG-XX-ADMIN` and `PRG-XX-CONT` are portfolio-level lines exempt from programme validation.

### 3. Numeric Integrity

For every cost line:

```
years_1_2 + years_3_4 + years_5_6 = six_year_total (±0.01 tolerance)
existing_funding + reallocated_funding + new_funding = six_year_total (±0.01 tolerance)
```

Negative numbers are rejected. Malformed numbers (text, empty cells where numbers expected) fail the build.

### 4. Required Fields

Critical fields cannot be empty:

- Programme: `programme_id`, `programme_name`, `pillar`
- KPI: `kpi_id`, `programme_id`, `kpi_name`
- Cost Line: `cost_line_id`, `programme_id`, `scenario`, all numeric columns

## Conflicts & Inconsistencies

### Disclosed, Not Hidden

When sources conflict (example: 527 vs 528 SJKT), both figures appear in the evidence room with:

- The conflict ID
- The conflicting values
- The adopted treatment
- Notes explaining the discrepancy

Silent reconciliation is **prohibited**. If a number is disputed, it's flagged as such.

### Baseline Status

KPIs carry a `baseline_status` field:

- `source-verified`: Baseline exists and is traceable
- `to-be-established`: No baseline exists; Year 1 deliverable
- `disputed`: Conflicting sources
- `unmeasured historic target`: MIB 2017 target with no published outturn

Missing baselines are **never** shown as zero. They appear as "Not established" or "Pending".

## Confidence Classes

Every cost line has a confidence class:

- **Confirmed** (0.0% of portfolio): Published outturn or gazetted instrument
- **Benchmarked** (31.9%): Comparable programme or market benchmark with source
- **Provisional** (68.1%): Planning assumption pending MOF/ministry confirmation

The confidence mix is computed from cost lines, not asserted separately.

## Totals Reconciliation

All totals are **computed**, not stored:

```typescript
const six_year_gross = costLines.reduce((sum, c) => sum + c.six_year_total, 0);
const by_pillar = costLines.reduce((acc, c) => {
  acc[c.pillar] += c.six_year_total;
  return acc;
}, {});
```

If a cost line changes, all totals update automatically. There is no risk of stale aggregates.

## Material Inconsistencies

Material inconsistencies are recorded in `CONFLICT_AND_DUPLICATION_REGISTER.csv` and disclosed in:

- Programme notes
- KPI notes
- Evidence room conflict entries

Example treatments:

- **CNF-006**: 527 vs 528 SJKT — adopt 528 from the May 2026 source; disclose the 527 variant
- **CNF-017**: SJKT existing-funding share reduced from 0.55 to 0.20 to avoid double-counting the national dilapidated-schools programme

## Missing Data

Missing values are **explicitly indicated**:

- KPI baseline: "Not established" (not zero)
- Optional fields: Empty or "n/a"
- Pending validation: "Pending MOF confirmation" (in notes)

Invented figures are **prohibited**. If a baseline doesn't exist, the KPI states that openly.

## Data Refresh Process

1. Update the source CSV in `../outputs/`
2. Run `npm run build`
3. If validation fails, the build stops with a specific error:
   - Line number
   - Field name
   - What was expected vs what was found
4. Fix the CSV (not the code)
5. Rebuild

## Machine Verification

The Python script `verify_outputs.py` runs 76 checks before the proposal is released. The website enforces the same validation logic at build time, so any CSV that passes `verify_outputs.py` will build successfully.

Checks include:

- Field completeness (no required fields empty)
- Numeric reconciliation (phases sum to totals, funding types sum to totals)
- Foreign-key resolution
- Confidence-class discipline (no "Confirmed" without a source)
- Reach/beneficiary reconciliation

## Traceability

Every claim on the website can be traced:

1. **Claim** → `CLAIMS_AND_FIGURES_REGISTER.csv` (claim_id)
2. **Claim** → `SOURCE_REGISTER.csv` (source_id)
3. **Figure** → Cost line or KPI entry with stable ID
4. **Programme** → Stable programme_id (PRG-01 through PRG-16)

Links are preserved in URLs (`/programmes/PRG-01`) so external references remain stable.

## What This Ensures

- **No duplicate data**: Figures exist in one place (the CSV), displayed everywhere
- **Automatic updates**: Change a CSV, rebuild, and all pages update
- **Error detection**: Validation catches inconsistencies before they reach production
- **Audit trail**: Every number traces to a register row with a stable ID

## What This Does Not Guarantee

- **External source verification**: The website validates CSV structure, not the truth of the underlying sources
- **Real-time updates**: Data is fixed at build time; live dashboards require a different architecture
- **Completeness**: If a programme is missing from the CSV, it won't appear on the site — by design

## Limitations Disclosed

Material limitations are recorded in:

- `SOURCE_REGISTER.csv` (limitations column)
- Programme notes
- KPI notes
- `DATA_QUALITY.md` (this document)

Examples:

- "Indian MEDIAN household income for 2022 not obtained at source" (SRC-002)
- "MIB 2017 targets have no published progress reporting" (SRC-001)
- "State-by-state consent required; Federal delivery depends on state cooperation" (PRG-04)

## Quality Gates

Before the site can be deployed:

1. `npm run build` must succeed (exit code 0)
2. All 76 validation checks must pass
3. TypeScript must compile without errors
4. No console errors in browser
5. Accessibility audit (manual)
6. Print layout review (manual)

## Responsibility

Data quality is maintained in the **source CSVs**, not in the website code. The website is a read-only renderer. If a figure is wrong, the fix goes into the CSV, and the site is rebuilt.

The authoritative registers are version-controlled and validated by `verify_outputs.py` before being committed.
