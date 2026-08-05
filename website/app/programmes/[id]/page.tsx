import { loadProgrammes, loadKPIs, loadCostLines, loadRisks, loadResponsibilities } from '@/lib/data-loader';
import { notFound } from 'next/navigation';
import Link from 'next/link';

export async function generateStaticParams() {
  const programmes = loadProgrammes();
  return programmes.map((p) => ({
    id: p.programme_id,
  }));
}

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const programmes = loadProgrammes();
  const programme = programmes.find((p) => p.programme_id === id);

  if (!programme) {
    return { title: 'Programme Not Found' };
  }

  return {
    title: `${programme.programme_name} — MIB 2.0`,
    description: programme.problem_addressed,
  };
}

export default async function ProgrammePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const programmes = loadProgrammes();
  const programme = programmes.find((p) => p.programme_id === id);

  if (!programme) {
    notFound();
  }

  const kpis = loadKPIs().filter((k) => k.programme_id === id);
  const costLines = loadCostLines().filter((c) => c.programme_id === id && c.scenario === 'central');
  const risks = loadRisks().filter((r) => r.affected_programmes.includes(id));
  const responsibility = loadResponsibilities().find((r) => r.programme_id === id);

  const totalCost = costLines.reduce((sum, c) => sum + c.six_year_total, 0);
  const newFunding = costLines.reduce((sum, c) => sum + c.new_funding, 0);

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="bg-navy-950 text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <div className="mb-4">
            <Link href="/programmes" className="text-sm text-gray-400 hover:text-white">
              ← Back to programmes
            </Link>
          </div>
          <div className="flex items-center gap-3 mb-4">
            <span className="text-sm font-mono text-gray-400">{programme.programme_id}</span>
            <span className="text-sm font-semibold px-3 py-1 rounded-full bg-gold-600 text-navy-950">
              {programme.pillar}
            </span>
            <span className="text-sm font-semibold px-3 py-1 rounded-full bg-navy-800 border border-navy-700">
              Phase {programme.phase}
            </span>
          </div>
          <h1 className="text-4xl font-bold mb-4">{programme.programme_name}</h1>
          <p className="text-xl text-gray-300">{programme.problem_addressed}</p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Problem → Cause → Intervention */}
        <section className="bg-white rounded-lg border border-gray-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-navy-950 mb-6">Programme Logic</h2>

          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Problem</h3>
              <p className="text-gray-900">{programme.problem_addressed}</p>
            </div>

            <div className="pl-8 border-l-4 border-teal-500">
              <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Structural Cause</h3>
              <p className="text-gray-900">{programme.structural_cause}</p>
            </div>

            <div className="pl-16 border-l-4 border-gold-500">
              <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Intervention</h3>
              <p className="text-gray-900">{programme.delivery_mechanism}</p>
            </div>
          </div>
        </section>

        {/* Target Group & Eligibility */}
        <section className="bg-white rounded-lg border border-gray-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-navy-950 mb-6">Who & How</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Target Group</h3>
              <p className="text-gray-900">{programme.target_group}</p>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Eligibility</h3>
              <p className="text-gray-900">{programme.eligibility}</p>
            </div>
          </div>
        </section>

        {/* Outputs & Outcomes */}
        <section className="bg-white rounded-lg border border-gray-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-navy-950 mb-6">Deliverables</h2>

          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Outputs</h3>
              <p className="text-gray-900">{programme.output}</p>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Outcomes</h3>
              <p className="text-gray-900">{programme.outcome}</p>
            </div>
          </div>
        </section>

        {/* KPIs */}
        {kpis.length > 0 && (
          <section className="bg-white rounded-lg border border-gray-200 p-8 mb-8">
            <h2 className="text-2xl font-bold text-navy-950 mb-6">Key Performance Indicators</h2>

            {kpis.map((kpi) => (
              <div key={kpi.kpi_id} className="mb-6 last:mb-0">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <span className="text-sm font-mono text-gray-500">{kpi.kpi_id}</span>
                    <h3 className="text-lg font-semibold text-navy-950">{kpi.kpi_name}</h3>
                  </div>
                  <span className={`text-xs font-semibold px-3 py-1 rounded-full ${
                    kpi.baseline_status === 'source-verified'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {kpi.baseline_status}
                  </span>
                </div>

                <p className="text-sm text-gray-600 mb-4">{kpi.definition}</p>

                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <div className="text-gray-500 font-medium">Baseline</div>
                    <div className="text-gray-900">{kpi.baseline_value || 'Not established'}</div>
                  </div>
                  <div>
                    <div className="text-gray-500 font-medium">Year 2</div>
                    <div className="text-gray-900">{kpi.year_2_target || '—'}</div>
                  </div>
                  <div>
                    <div className="text-gray-500 font-medium">Year 4</div>
                    <div className="text-gray-900">{kpi.year_4_target || '—'}</div>
                  </div>
                  <div>
                    <div className="text-gray-500 font-medium">Year 6</div>
                    <div className="text-gray-900">{kpi.year_6_target || '—'}</div>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500 font-medium">Owner: </span>
                      <span className="text-gray-900">{kpi.data_owner}</span>
                    </div>
                    <div>
                      <span className="text-gray-500 font-medium">Verification: </span>
                      <span className="text-gray-900">{kpi.verification_source}</span>
                    </div>
                  </div>
                </div>

                {kpi.notes && (
                  <div className="mt-3 p-3 bg-gray-50 rounded text-sm text-gray-600">
                    <strong>Note:</strong> {kpi.notes}
                  </div>
                )}
              </div>
            ))}
          </section>
        )}

        {/* Costing */}
        <section className="bg-white rounded-lg border border-gray-200 p-8 mb-8">
          <h2 className="text-2xl font-bold text-navy-950 mb-6">Costing (Central Scenario)</h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm text-gray-500 mb-1">Six-Year Total</div>
              <div className="text-2xl font-bold text-navy-950">
                RM {totalCost.toFixed(1)}m
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm text-gray-500 mb-1">New Funding</div>
              <div className="text-2xl font-bold text-teal-600">
                RM {newFunding.toFixed(1)}m
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm text-gray-500 mb-1">Existing</div>
              <div className="text-2xl font-bold text-gray-700">
                RM {(totalCost - newFunding - costLines.reduce((sum, c) => sum + c.reallocated_funding, 0)).toFixed(1)}m
              </div>
            </div>
            <div className="bg-gray-50 p-4 rounded">
              <div className="text-sm text-gray-500 mb-1">Reallocated</div>
              <div className="text-2xl font-bold text-gray-700">
                RM {costLines.reduce((sum, c) => sum + c.reallocated_funding, 0).toFixed(1)}m
              </div>
            </div>
          </div>

          <Link href="/costing" className="text-sm font-semibold text-teal-600 hover:text-teal-700">
            View full costing scenarios →
          </Link>
        </section>

        {/* Delivery */}
        {responsibility && (
          <section className="bg-white rounded-lg border border-gray-200 p-8 mb-8">
            <h2 className="text-2xl font-bold text-navy-950 mb-6">Delivery & Accountability</h2>

            <div className="space-y-4">
              <div>
                <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Lead Ministry</h3>
                <p className="text-gray-900">{responsibility.lead_ministry_or_agency}</p>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Accounting Officer</h3>
                <p className="text-gray-900">{responsibility.accounting_officer}</p>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Supporting Agencies</h3>
                <p className="text-gray-900">{programme.supporting_agencies}</p>
              </div>

              {responsibility.mandate_basis && (
                <div>
                  <h3 className="text-sm font-semibold text-gray-700 uppercase mb-2">Mandate Basis</h3>
                  <p className="text-gray-900">{responsibility.mandate_basis}</p>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Risks */}
        {risks.length > 0 && (
          <section className="bg-white rounded-lg border border-gray-200 p-8">
            <h2 className="text-2xl font-bold text-navy-950 mb-6">Risks & Safeguards</h2>

            <div className="space-y-6">
              {risks.map((risk) => (
                <div key={risk.risk_id} className="pb-6 last:pb-0 border-b last:border-b-0 border-gray-200">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <span className="text-sm font-mono text-gray-500">{risk.risk_id}</span>
                      <h3 className="text-lg font-semibold text-navy-950">{risk.risk_category}</h3>
                    </div>
                    <div className="flex gap-2">
                      <span className={`text-xs font-semibold px-3 py-1 rounded-full ${
                        risk.inherent_rating === 'Critical'
                          ? 'bg-red-100 text-red-800'
                          : risk.inherent_rating === 'Major'
                          ? 'bg-orange-100 text-orange-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {risk.inherent_rating}
                      </span>
                      <span className="text-xs font-semibold px-3 py-1 rounded-full bg-gray-100 text-gray-700">
                        → {risk.residual_rating}
                      </span>
                    </div>
                  </div>

                  <p className="text-gray-900 mb-3">{risk.risk_description}</p>

                  <div className="p-3 bg-teal-50 rounded">
                    <h4 className="text-sm font-semibold text-teal-900 mb-1">Safeguard</h4>
                    <p className="text-sm text-teal-800">{risk.safeguard}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
