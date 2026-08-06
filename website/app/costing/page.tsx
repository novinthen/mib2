import {
  calculateCostingSummary,
  loadCostLines,
  loadProgrammes,
  loadSources,
  loadCostingAssumptions,
} from '@/lib/data-loader';
import { Scenario } from '@/types';
import CostingClient from '@/components/CostingClient';

export const metadata = {
  title: 'Costing — MIB 2.0',
  description: 'Three costing scenarios with transparent assumptions for the Malaysian Indian Blueprint 2.0',
};

export default function CostingPage() {
  const scenarios: Scenario[] = ['conservative', 'central', 'expanded'];

  const allData = {
    conservative: {
      summary: calculateCostingSummary('conservative'),
      costLines: loadCostLines().filter(c => c.scenario === 'conservative'),
    },
    central: {
      summary: calculateCostingSummary('central'),
      costLines: loadCostLines().filter(c => c.scenario === 'central'),
    },
    expanded: {
      summary: calculateCostingSummary('expanded'),
      costLines: loadCostLines().filter(c => c.scenario === 'expanded'),
    },
  };

  const programmes = loadProgrammes();
  const sources = Object.fromEntries(loadSources().map((s) => [s.source_id, s]));
  const assumptions = Object.fromEntries(loadCostingAssumptions().map((a) => [a.assumption_id, a]));

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
              Costing Model
            </h1>
            <p className="text-lg text-white/80">
              Three scenarios with transparent assumptions. All figures in 2026 nominal ringgit.
              Conservative/central/expanded scenarios distinguish gross, existing, reallocated, and
              incremental funding.
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <CostingClient
          allData={allData}
          programmes={programmes}
          sources={sources}
          assumptions={assumptions}
        />
      </div>
    </div>
  );
}
