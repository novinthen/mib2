'use client';

import { useState } from 'react';
import { Programme, CostingSummary, CostLine, Scenario } from '@/types';

interface CostingClientProps {
  allData: {
    conservative: { summary: CostingSummary; costLines: CostLine[] };
    central: { summary: CostingSummary; costLines: CostLine[] };
    expanded: { summary: CostingSummary; costLines: CostLine[] };
  };
  programmes: Programme[];
}

export default function CostingClient({ allData, programmes }: CostingClientProps) {
  const [selectedScenario, setSelectedScenario] = useState<Scenario>('central');

  const summary = allData[selectedScenario].summary;
  const costLines = allData[selectedScenario].costLines;

  const scenarioDescriptions = {
    conservative: 'Lower reach, longer timelines, higher existing-funding assumptions',
    central: 'Planning baseline with verified costing assumptions',
    expanded: 'Higher reach, accelerated timelines, more intensive delivery'
  };

  return (
    <div className="space-y-6">
      {/* Scenario Selector */}
      <div className="bg-white rounded-2xl shadow-soft p-6">
        <h2 className="text-xl font-bold text-neutral-900 mb-4">Select Scenario</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(['conservative', 'central', 'expanded'] as Scenario[]).map((scenario) => (
            <button
              key={scenario}
              onClick={() => setSelectedScenario(scenario)}
              className={`p-5 rounded-xl text-left transition-all ${
                selectedScenario === scenario
                  ? 'bg-primary-50 border-2 border-primary-500 shadow-glow'
                  : 'bg-neutral-50 border-2 border-neutral-200 hover:border-neutral-300'
              }`}
            >
              <div className="font-semibold text-neutral-900 mb-1 capitalize">{scenario}</div>
              <div className="text-sm text-neutral-600">{scenarioDescriptions[scenario]}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <SummaryCard
          label="Six-Year Total"
          value={`RM ${(summary.six_year_gross / 1000).toFixed(2)}bn`}
          subValue={`RM ${summary.six_year_gross.toFixed(1)}m`}
          gradient="from-primary-500 to-primary-600"
        />
        <SummaryCard
          label="New Funding"
          value={`RM ${(summary.new_funding / 1000).toFixed(2)}bn`}
          subValue={`${((summary.new_funding / summary.six_year_gross) * 100).toFixed(1)}% of total`}
          gradient="from-info-500 to-info-600"
        />
        <SummaryCard
          label="Existing"
          value={`RM ${(summary.existing_funding / 1000).toFixed(2)}bn`}
          subValue={`${((summary.existing_funding / summary.six_year_gross) * 100).toFixed(1)}% of total`}
          gradient="from-neutral-500 to-neutral-600"
        />
        <SummaryCard
          label="Reallocated"
          value={`RM ${(summary.reallocated_funding / 1000).toFixed(2)}bn`}
          subValue={`${((summary.reallocated_funding / summary.six_year_gross) * 100).toFixed(1)}% of total`}
          gradient="from-accent-500 to-accent-600"
        />
      </div>

      {/* By Phase */}
      <div className="bg-white rounded-2xl shadow-soft p-8">
        <h2 className="text-2xl font-bold text-neutral-900 mb-6">By Phase</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { label: 'Years 1–2', value: summary.by_phase.years_1_2 },
            { label: 'Years 3–4', value: summary.by_phase.years_3_4 },
            { label: 'Years 5–6', value: summary.by_phase.years_5_6 },
          ].map((phase, idx) => (
            <div key={idx} className="bg-neutral-50 rounded-xl p-6">
              <div className="text-sm font-medium text-neutral-600 mb-2">{phase.label}</div>
              <div className="text-3xl font-bold text-neutral-900 mb-1">
                RM {phase.value.toFixed(1)}m
              </div>
              <div className="text-sm text-neutral-500">
                {((phase.value / summary.six_year_gross) * 100).toFixed(1)}% of total
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* By Pillar */}
      <div className="bg-white rounded-2xl shadow-soft p-8">
        <h2 className="text-2xl font-bold text-neutral-900 mb-6">By Pillar</h2>
        <div className="space-y-6">
          {Object.entries(summary.by_pillar).map(([pillar, amount]) => (
            <div key={pillar}>
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-neutral-900">{pillar}</span>
                <div className="text-right">
                  <div className="text-xl font-bold text-neutral-900">RM {amount.toFixed(1)}m</div>
                  <div className="text-sm text-neutral-500">
                    {((amount / summary.six_year_gross) * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
              <div className="w-full bg-neutral-100 rounded-full h-3 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${(amount / summary.six_year_gross) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Confidence Mix */}
      <div className="bg-white rounded-2xl shadow-soft p-8">
        <h2 className="text-2xl font-bold text-neutral-900 mb-6">Confidence Mix</h2>
        <div className="space-y-6">
          {Object.entries(summary.confidence_mix).map(([confidence, data]) => {
            const gradients: Record<string, string> = {
              Confirmed: 'from-green-500 to-green-600',
              Benchmarked: 'from-blue-500 to-blue-600',
              Provisional: 'from-amber-500 to-amber-600',
            };

            return (
              <div key={confidence}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <span className={`text-xs font-semibold px-3 py-1.5 rounded-lg bg-gradient-to-r ${gradients[confidence]} text-white`}>
                      {confidence}
                    </span>
                    <span className="text-sm text-neutral-600">
                      {confidence === 'Confirmed' && 'Published outturn or gazetted'}
                      {confidence === 'Benchmarked' && 'Comparable programme benchmark'}
                      {confidence === 'Provisional' && 'Planning assumption pending validation'}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-neutral-900">RM {data.amount.toFixed(1)}m</div>
                    <div className="text-sm text-neutral-500">{data.percentage.toFixed(1)}%</div>
                  </div>
                </div>
                <div className="w-full bg-neutral-100 rounded-full h-3 overflow-hidden">
                  <div
                    className={`bg-gradient-to-r ${gradients[confidence]} h-3 rounded-full transition-all duration-500`}
                    style={{ width: `${data.percentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-xl">
          <p className="text-sm text-amber-900">
            <strong>Note:</strong> {summary.confidence_mix.Provisional.percentage.toFixed(1)}% of this
            scenario is Provisional, pending MOF/ministry confirmation.
          </p>
        </div>
      </div>

      {/* Programme Table */}
      <div className="bg-white rounded-2xl shadow-soft p-8 overflow-hidden">
        <h2 className="text-2xl font-bold text-neutral-900 mb-6">Programme Details</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b-2 border-neutral-200">
                <th className="text-left py-4 px-3 font-semibold text-neutral-700">Programme</th>
                <th className="text-right py-4 px-3 font-semibold text-neutral-700">Total</th>
                <th className="text-right py-4 px-3 font-semibold text-neutral-700">Existing</th>
                <th className="text-right py-4 px-3 font-semibold text-neutral-700">Reallocated</th>
                <th className="text-right py-4 px-3 font-semibold text-neutral-700">New</th>
                <th className="text-center py-4 px-3 font-semibold text-neutral-700">Confidence</th>
              </tr>
            </thead>
            <tbody>
              {programmes.map((programme) => {
                const progCosts = costLines.filter(c => c.programme_id === programme.programme_id);
                const total = progCosts.reduce((sum, c) => sum + c.six_year_total, 0);
                const existing = progCosts.reduce((sum, c) => sum + c.existing_funding, 0);
                const reallocated = progCosts.reduce((sum, c) => sum + c.reallocated_funding, 0);
                const newFund = progCosts.reduce((sum, c) => sum + c.new_funding, 0);
                const confidence = progCosts[0]?.confidence || 'Provisional';

                const confidenceColors: Record<string, string> = {
                  Confirmed: 'bg-green-100 text-green-800 border-green-200',
                  Benchmarked: 'bg-blue-100 text-blue-800 border-blue-200',
                  Provisional: 'bg-amber-100 text-amber-800 border-amber-200',
                };

                return (
                  <tr key={programme.programme_id} className="border-b border-neutral-100 hover:bg-neutral-50 transition-colors">
                    <td className="py-4 px-3">
                      <div className="font-medium text-neutral-900">{programme.programme_name}</div>
                      <div className="text-xs text-neutral-500 font-mono mt-0.5">{programme.programme_id}</div>
                    </td>
                    <td className="text-right py-4 px-3 font-semibold text-neutral-900">RM {total.toFixed(1)}m</td>
                    <td className="text-right py-4 px-3 text-neutral-600">RM {existing.toFixed(1)}m</td>
                    <td className="text-right py-4 px-3 text-neutral-600">RM {reallocated.toFixed(1)}m</td>
                    <td className="text-right py-4 px-3 font-semibold text-info-600">RM {newFund.toFixed(1)}m</td>
                    <td className="text-center py-4 px-3">
                      <span className={`text-xs font-semibold px-3 py-1 rounded-lg border ${confidenceColors[confidence]}`}>
                        {confidence}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
            <tfoot>
              <tr className="border-t-2 border-neutral-300 font-bold bg-neutral-50">
                <td className="py-4 px-3 text-neutral-900">Total</td>
                <td className="text-right py-4 px-3 text-neutral-900">RM {summary.six_year_gross.toFixed(1)}m</td>
                <td className="text-right py-4 px-3 text-neutral-900">RM {summary.existing_funding.toFixed(1)}m</td>
                <td className="text-right py-4 px-3 text-neutral-900">RM {summary.reallocated_funding.toFixed(1)}m</td>
                <td className="text-right py-4 px-3 text-info-600">RM {summary.new_funding.toFixed(1)}m</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </div>
  );
}

function SummaryCard({
  label,
  value,
  subValue,
  gradient
}: {
  label: string;
  value: string;
  subValue: string;
  gradient: string;
}) {
  return (
    <div className="relative bg-white rounded-2xl p-6 shadow-soft hover:shadow-soft-lg transition-all">
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-5 rounded-2xl`} />
      <div className="relative">
        <div className="text-sm font-medium text-neutral-500 mb-2">{label}</div>
        <div className={`text-3xl font-bold bg-gradient-to-br ${gradient} bg-clip-text text-transparent mb-1`}>
          {value}
        </div>
        <div className="text-xs text-neutral-500">{subValue}</div>
      </div>
    </div>
  );
}
