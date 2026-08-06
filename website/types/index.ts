// Core data types for MIB 2.0 website
// Generated from authoritative CSV registers

export type Scenario = 'conservative' | 'central' | 'expanded';

export type ConfidenceClass = 'Confirmed' | 'Benchmarked' | 'Provisional';

export type Phase = '1' | '2' | '3' | '1-2' | '1-3' | '2-3' | '1-2-3';

export type CostCategory =
  | 'operating_expenditure'
  | 'development_expenditure'
  | 'transfer_grant'
  | 'administration'
  | 'monitoring_evaluation';

export type BaselineStatus =
  | 'source-verified'
  | 'to-be-established'
  | 'disputed'
  | 'unmeasured historic target';

export type Pillar =
  | 'P1 Foundations'
  | 'P2 Progression'
  | 'P3 Livelihoods'
  | 'P4 Institutional Participation'
  | 'X Delivery';

export interface Programme {
  programme_id: string;
  source_document: string;
  programme_name: string;
  pillar: Pillar;
  problem_addressed: string;
  structural_cause: string;
  target_group: string;
  eligibility: string;
  delivery_mechanism: string;
  proposed_owner: string;
  supporting_agencies: string;
  phase: string;
  output: string;
  outcome: string;
  kpi_id: string;
  stated_cost_in_source: string;
  cost_status: string;
  duplication_assessment: string;
  missing_design_information: string;
  preliminary_feasibility: string;
  retain_decision: string;
}

export interface KPI {
  kpi_id: string;
  programme_id: string;
  kpi_name: string;
  indicator_type: string;
  definition: string;
  baseline_value: string;
  baseline_year: string;
  baseline_status: BaselineStatus;
  year_2_target: string;
  year_4_target: string;
  year_6_target: string;
  measurement_frequency: string;
  data_owner: string;
  verification_source: string;
  disaggregation: string;
  notes: string;
}

export interface CostLine {
  cost_line_id: string;
  programme_id: string;
  programme_name: string;
  pillar: Pillar;
  lead_ministry: string;
  cost_category: CostCategory;
  price_base_year: string;
  scenario: Scenario;
  years_1_2: number;
  years_3_4: number;
  years_5_6: number;
  six_year_total: number;
  existing_funding: number;
  reallocated_funding: number;
  new_funding: number;
  cost_method: string;
  assumption_ids: string;
  confidence: ConfidenceClass;
  cost_source_id: string;
  funding_split_basis: string;
  reach_count: number | null;
  reach_unit: string;
  overlap_group: string;
  phases_active: string;
  notes: string;
}

export interface Risk {
  risk_id: string;
  risk_category: string;
  risk_description: string;
  affected_programmes: string;
  likelihood: string;
  impact: string;
  inherent_rating: string;
  safeguard: string;
  residual_rating: string;
  owner: string;
  monitoring_trigger: string;
}

export interface ClaimFigure {
  claim_id: string;
  source_document: string;
  source_location: string;
  verbatim_or_close_claim: string;
  claim_type: string;
  population_scope: string;
  geography: string;
  reference_period: string;
  cited_source: string;
  verification_status: string;
  source_id: string;
  conflict_id: string;
  adopted_treatment: string;
  notes: string;
}

export interface Source {
  source_id: string;
  title: string;
  issuing_institution: string;
  publication_date: string;
  location_in_source: string;
  url: string;
  access_date: string;
  geographic_scope: string;
  population_scope: string;
  definition_used: string;
  tier: string;
  limitations: string;
  supports_directly_or_inference: string;
}

// A single authored costing assumption (from COSTING_ASSUMPTIONS.csv) — the
// origin of every figure in the costing model. Referenced by CostLine.assumption_ids.
export interface CostingAssumption {
  assumption_id: string;
  programme_id: string;
  cost_method: string;
  eligible_population: string;
  participation_basis: string;
  unit_cost_rm: string;
  frequency_or_duration: string;
  basis_and_benchmark: string;
  validation_item: string;
  recurring_or_one_off: string;
  confidence: ConfidenceClass;
  cost_source_id: string;
}

export interface Responsibility {
  responsibility_id: string;
  programme_id: string;
  programme_name: string;
  lead_ministry_or_agency: string;
  mandate_basis: string;
  supporting_agencies: string;
  accounting_officer: string;
  phase: string;
  escalation_route: string;
  mandate_verification_status: string;
  notes: string;
}

export interface CostingSummary {
  scenario: Scenario;
  six_year_gross: number;
  existing_funding: number;
  reallocated_funding: number;
  new_funding: number;
  by_pillar: Record<Pillar, number>;
  by_phase: {
    years_1_2: number;
    years_3_4: number;
    years_5_6: number;
  };
  confidence_mix: Record<ConfidenceClass, { amount: number; percentage: number }>;
}

export interface FilterState {
  pillar?: Pillar[];
  phase?: string[];
  ministry?: string[];
  search?: string;
}
