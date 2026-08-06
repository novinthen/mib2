import {
  calculateCostingSummary,
  loadCostLines,
  loadProgrammes,
  loadSources,
  loadCostingAssumptions,
} from '@/lib/data-loader';
import CostingClient from '@/components/CostingClient';
import ConfidenceBadge from '@/components/ConfidenceBadge';

export const metadata = {
  title: 'Costing — MIB 2.0',
  description: 'Three costing scenarios with transparent assumptions for the Malaysian Indian Blueprint 2.0',
};

export default function CostingPage() {
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
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-6">
        {/* How to read this */}
        <div className="bg-white rounded-2xl shadow-soft p-6 sm:p-8">
          <h2 className="text-lg font-bold text-neutral-900 mb-4">How to read costing</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-xs font-semibold tracking-wide text-neutral-500 uppercase mb-3">
                Confidence of each figure
              </h3>
              <ul className="space-y-2.5">
                <li className="flex items-start gap-3">
                  <ConfidenceBadge confidence="Confirmed" />
                  <span className="text-sm text-neutral-600">Published outturn or gazetted figure.</span>
                </li>
                <li className="flex items-start gap-3">
                  <ConfidenceBadge confidence="Benchmarked" />
                  <span className="text-sm text-neutral-600">Benchmarked to a comparable programme or source.</span>
                </li>
                <li className="flex items-start gap-3">
                  <ConfidenceBadge confidence="Provisional" />
                  <span className="text-sm text-neutral-600">Planning assumption pending validation.</span>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-xs font-semibold tracking-wide text-neutral-500 uppercase mb-3">
                What the funding split means
              </h3>
              <ul className="space-y-2.5 text-sm text-neutral-600">
                <li>
                  <span className="font-semibold text-neutral-800">Existing</span> — already funded within a
                  ministry&rsquo;s current budget.
                </li>
                <li>
                  <span className="font-semibold text-neutral-800">Reallocated</span> — redirected from other
                  existing budget lines.
                </li>
                <li>
                  <span className="font-semibold text-info-700">New</span> — the incremental funding this plan
                  asks for.
                </li>
              </ul>
            </div>
          </div>
          <p className="mt-5 pt-4 border-t border-neutral-100 text-sm text-neutral-500">
            All figures are in 2026 nominal ringgit. Select a programme in the table below to expand its{' '}
            <span className="font-medium text-neutral-700">method, assumptions and sources</span>.
          </p>
        </div>

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
