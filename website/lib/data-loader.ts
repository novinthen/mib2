// Data loader with strict validation
// Derives figures from canonical registers at build time
// Never duplicates or hard-codes them in UI components

import path from 'path';
import {
  Programme,
  KPI,
  CostLine,
  Risk,
  ClaimFigure,
  Source,
  Responsibility,
  CostingSummary,
  CostingAssumption,
  Scenario,
  Pillar,
  ConfidenceClass,
  BaselineStatus,
  CostCategory,
} from '@/types';
import { parseCSV, parseNumber, validateRequired, validateForeignKey, ValidationError } from './csv-parser';

const DATA_DIR = path.join(process.cwd(), '..', 'outputs');
type CSVRow = Record<string, string>;

export function loadProgrammes(): Programme[] {
  const filePath = path.join(DATA_DIR, 'PROGRAMME_REGISTER.csv');
  const raw = parseCSV<CSVRow>(filePath);

  return raw
    .filter((r) => r.retain_decision?.includes('RETAIN'))
    .map((r, idx) => {
      validateRequired(r.programme_id, 'programme_id', `PROGRAMME_REGISTER:${idx + 2}`);
      validateRequired(r.programme_name, 'programme_name', `PROGRAMME_REGISTER:${idx + 2}`);
      validateRequired(r.pillar, 'pillar', `PROGRAMME_REGISTER:${idx + 2}`);

      return {
        programme_id: r.programme_id,
        source_document: r.source_document || '',
        programme_name: r.programme_name,
        pillar: r.pillar as Pillar,
        problem_addressed: r.problem_addressed || '',
        structural_cause: r.structural_cause || '',
        target_group: r.target_group || '',
        eligibility: r.eligibility || '',
        delivery_mechanism: r.delivery_mechanism || '',
        proposed_owner: r.proposed_owner || '',
        supporting_agencies: r.supporting_agencies || '',
        phase: r.phase || '',
        output: r.output || '',
        outcome: r.outcome || '',
        kpi_id: r.kpi_id || '',
        stated_cost_in_source: r.stated_cost_in_source || '',
        cost_status: r.cost_status || '',
        duplication_assessment: r.duplication_assessment || '',
        missing_design_information: r.missing_design_information || '',
        preliminary_feasibility: r.preliminary_feasibility || '',
        retain_decision: r.retain_decision || '',
      };
    });
}

export function loadKPIs(): KPI[] {
  const filePath = path.join(DATA_DIR, 'KPI_REGISTER.csv');
  const raw = parseCSV<CSVRow>(filePath);
  const programmes = loadProgrammes();

  return raw.map((r, idx) => {
    const context = `KPI_REGISTER:${idx + 2}`;
    validateRequired(r.kpi_id, 'kpi_id', context);
    validateRequired(r.programme_id, 'programme_id', context);
    validateForeignKey(r.programme_id, programmes, 'programme_id', context);

    return {
      kpi_id: r.kpi_id,
      programme_id: r.programme_id,
      kpi_name: r.kpi_name || '',
      indicator_type: r.indicator_type || '',
      definition: r.definition || '',
      baseline_value: r.baseline_value || '',
      baseline_year: r.baseline_year || '',
      baseline_status: (r.baseline_status || 'to-be-established') as BaselineStatus,
      year_2_target: r.year_2_target || '',
      year_4_target: r.year_4_target || '',
      year_6_target: r.year_6_target || '',
      measurement_frequency: r.measurement_frequency || '',
      data_owner: r.data_owner || '',
      verification_source: r.verification_source || '',
      disaggregation: r.disaggregation || '',
      notes: r.notes || '',
    };
  });
}

export function loadCostLines(): CostLine[] {
  const filePath = path.join(DATA_DIR, 'COSTING_MODEL.csv');
  const raw = parseCSV<CSVRow>(filePath);
  const programmes = loadProgrammes();

  return raw.map((r, idx) => {
    const context = `COSTING_MODEL:${idx + 2}`;
    validateRequired(r.cost_line_id, 'cost_line_id', context);
    validateRequired(r.programme_id, 'programme_id', context);

    // Special programme IDs that don't map to specific programmes:
    // PRG-XX-ADMIN: portfolio administration overhead
    // PRG-XX-CONT: contingency or other cross-cutting lines
    const specialProgrammeIds = ['PRG-XX-ADMIN', 'PRG-XX-CONT'];
    if (!specialProgrammeIds.includes(r.programme_id)) {
      validateForeignKey(r.programme_id, programmes, 'programme_id', context);
    }

    const years_1_2 = parseNumber(r.years_1_2, `${context}.years_1_2`);
    const years_3_4 = parseNumber(r.years_3_4, `${context}.years_3_4`);
    const years_5_6 = parseNumber(r.years_5_6, `${context}.years_5_6`);
    const six_year_total = parseNumber(r.six_year_total, `${context}.six_year_total`);

    // Validate that phases sum to total (with 0.01 tolerance for rounding)
    const computed_total = years_1_2 + years_3_4 + years_5_6;
    if (Math.abs(computed_total - six_year_total) > 0.01) {
      throw new ValidationError(
        `${context}: Phases sum to ${computed_total.toFixed(3)} but six_year_total is ${six_year_total}`
      );
    }

    const existing = parseNumber(r.existing_funding, `${context}.existing_funding`);
    const reallocated = parseNumber(r.reallocated_funding, `${context}.reallocated_funding`);
    const new_funding = parseNumber(r.new_funding, `${context}.new_funding`);

    // Validate that funding types sum to total
    const funding_sum = existing + reallocated + new_funding;
    if (Math.abs(funding_sum - six_year_total) > 0.01) {
      throw new ValidationError(
        `${context}: Funding types sum to ${funding_sum.toFixed(3)} but six_year_total is ${six_year_total}`
      );
    }

    return {
      cost_line_id: r.cost_line_id,
      programme_id: r.programme_id,
      programme_name: r.programme_name || '',
      pillar: r.pillar as Pillar,
      lead_ministry: r.lead_ministry || '',
      cost_category: (r.cost_category || 'operating_expenditure') as CostCategory,
      price_base_year: r.price_base_year || '2026',
      scenario: r.scenario as Scenario,
      years_1_2,
      years_3_4,
      years_5_6,
      six_year_total,
      existing_funding: existing,
      reallocated_funding: reallocated,
      new_funding,
      cost_method: r.cost_method || '',
      assumption_ids: r.assumption_ids || '',
      confidence: r.confidence as ConfidenceClass,
      cost_source_id: r.cost_source_id || '',
      funding_split_basis: r.funding_split_basis || '',
      reach_count: r.reach_count ? parseNumber(r.reach_count, `${context}.reach_count`) : null,
      reach_unit: r.reach_unit || '',
      overlap_group: r.overlap_group || '',
      phases_active: r.phases_active || '',
      notes: r.notes || '',
    };
  });
}

export function loadRisks(): Risk[] {
  const filePath = path.join(DATA_DIR, 'RISK_AND_SAFEGUARD_REGISTER.csv');
  const raw = parseCSV<CSVRow>(filePath);

  return raw.map((r) => ({
    risk_id: r.risk_id,
    risk_category: r.risk_category || '',
    risk_description: r.risk_description || '',
    affected_programmes: r.affected_programmes || '',
    likelihood: r.likelihood || '',
    impact: r.impact || '',
    inherent_rating: r.inherent_rating || '',
    safeguard: r.safeguard || '',
    residual_rating: r.residual_rating || '',
    owner: r.owner || '',
    monitoring_trigger: r.monitoring_trigger || '',
  }));
}

export function loadClaims(): ClaimFigure[] {
  const filePath = path.join(DATA_DIR, 'CLAIMS_AND_FIGURES_REGISTER.csv');
  const raw = parseCSV<CSVRow>(filePath);

  return raw.map((r) => ({
    claim_id: r.claim_id,
    source_document: r.source_document || '',
    source_location: r.source_location || '',
    verbatim_or_close_claim: r.verbatim_or_close_claim || '',
    claim_type: r.claim_type || '',
    population_scope: r.population_scope || '',
    geography: r.geography || '',
    reference_period: r.reference_period || '',
    cited_source: r.cited_source || '',
    verification_status: r.verification_status || '',
    source_id: r.source_id || '',
    conflict_id: r.conflict_id || '',
    adopted_treatment: r.adopted_treatment || '',
    notes: r.notes || '',
  }));
}

export function loadSources(): Source[] {
  const filePath = path.join(DATA_DIR, 'SOURCE_REGISTER.csv');
  const raw = parseCSV<CSVRow>(filePath);

  return raw.map((r) => ({
    source_id: r.source_id,
    title: r.title || '',
    issuing_institution: r.issuing_institution || '',
    publication_date: r.publication_date || '',
    location_in_source: r.location_in_source || '',
    url: r.url || '',
    access_date: r.access_date || '',
    geographic_scope: r.geographic_scope || '',
    population_scope: r.population_scope || '',
    definition_used: r.definition_used || '',
    tier: r.tier || '',
    limitations: r.limitations || '',
    supports_directly_or_inference: r.supports_directly_or_inference || '',
  }));
}

export function loadCostingAssumptions(): CostingAssumption[] {
  const filePath = path.join(DATA_DIR, 'COSTING_ASSUMPTIONS.csv');
  const raw = parseCSV<CSVRow>(filePath);

  return raw
    .filter((r) => r.assumption_id)
    .map((r) => ({
      assumption_id: r.assumption_id,
      programme_id: r.programme_id || '',
      cost_method: r.cost_method || '',
      eligible_population: r.eligible_population || '',
      participation_basis: r.participation_basis || '',
      unit_cost_rm: r.unit_cost_rm || '',
      frequency_or_duration: r.frequency_or_duration || '',
      basis_and_benchmark: r.basis_and_benchmark || '',
      validation_item: r.validation_item || '',
      recurring_or_one_off: r.recurring_or_one_off || '',
      confidence: r.confidence as ConfidenceClass,
      cost_source_id: r.cost_source_id || '',
    }));
}

export function loadResponsibilities(): Responsibility[] {
  const filePath = path.join(DATA_DIR, 'RESPONSIBILITY_MATRIX.csv');
  const raw = parseCSV<CSVRow>(filePath);

  return raw.map((r) => ({
    responsibility_id: r.responsibility_id,
    programme_id: r.programme_id,
    programme_name: r.programme_name || '',
    lead_ministry_or_agency: r.lead_ministry_or_agency || '',
    mandate_basis: r.mandate_basis || '',
    supporting_agencies: r.supporting_agencies || '',
    accounting_officer: r.accounting_officer || '',
    phase: r.phase || '',
    escalation_route: r.escalation_route || '',
    mandate_verification_status: r.mandate_verification_status || '',
    notes: r.notes || '',
  }));
}

export function calculateCostingSummary(scenario: Scenario): CostingSummary {
  const costLines = loadCostLines().filter((c) => c.scenario === scenario);

  const six_year_gross = costLines.reduce((sum, c) => sum + c.six_year_total, 0);
  const existing_funding = costLines.reduce((sum, c) => sum + c.existing_funding, 0);
  const reallocated_funding = costLines.reduce((sum, c) => sum + c.reallocated_funding, 0);
  const new_funding = costLines.reduce((sum, c) => sum + c.new_funding, 0);

  const by_pillar: Record<Pillar, number> = {
    'P1 Foundations': 0,
    'P2 Progression': 0,
    'P3 Livelihoods': 0,
    'P4 Institutional Participation': 0,
    'X Delivery': 0,
  };

  costLines.forEach((c) => {
    by_pillar[c.pillar] += c.six_year_total;
  });

  const by_phase = {
    years_1_2: costLines.reduce((sum, c) => sum + c.years_1_2, 0),
    years_3_4: costLines.reduce((sum, c) => sum + c.years_3_4, 0),
    years_5_6: costLines.reduce((sum, c) => sum + c.years_5_6, 0),
  };

  const confidence_amounts: Record<ConfidenceClass, number> = {
    Confirmed: 0,
    Benchmarked: 0,
    Provisional: 0,
  };

  costLines.forEach((c) => {
    confidence_amounts[c.confidence] += c.six_year_total;
  });

  const confidence_mix: Record<ConfidenceClass, { amount: number; percentage: number }> = {
    Confirmed: {
      amount: confidence_amounts.Confirmed,
      percentage: (confidence_amounts.Confirmed / six_year_gross) * 100,
    },
    Benchmarked: {
      amount: confidence_amounts.Benchmarked,
      percentage: (confidence_amounts.Benchmarked / six_year_gross) * 100,
    },
    Provisional: {
      amount: confidence_amounts.Provisional,
      percentage: (confidence_amounts.Provisional / six_year_gross) * 100,
    },
  };

  return {
    scenario,
    six_year_gross,
    existing_funding,
    reallocated_funding,
    new_funding,
    by_pillar,
    by_phase,
    confidence_mix,
  };
}
