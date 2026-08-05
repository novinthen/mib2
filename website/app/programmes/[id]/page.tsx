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
    title: programme.programme_name,
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
  const reallocated = costLines.reduce((sum, c) => sum + c.reallocated_funding, 0);
  const existing = totalCost - newFunding - reallocated;

  return (
    <div className="bg-neutral-50 min-h-screen">
      {/* Header */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-700 via-primary-600 to-primary-800 text-white py-14 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white/5 to-white/10" />
        <div className="relative max-w-5xl mx-auto">
          <div className="mb-6">
            <Link href="/programmes" className="inline-flex items-center gap-1.5 text-sm text-white/70 hover:text-white transition-colors">
              <span aria-hidden>←</span> Back to programmes
            </Link>
          </div>
          <div className="flex flex-wrap items-center gap-2 mb-4">
            <span className="text-xs font-mono text-white/70 bg-white/10 px-3 py-1 rounded-full border border-white/15">
              {programme.programme_id}
            </span>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-accent-400 text-neutral-900">
              {programme.pillar}
            </span>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-white/10 border border-white/20 text-white">
              Phase {programme.phase}
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold mb-4">{programme.programme_name}</h1>
          <p className="text-lg text-white/80 max-w-3xl">{programme.problem_addressed}</p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
        {/* Problem → Cause → Intervention */}
        <Section title="Programme Logic">
          <div className="space-y-6">
            <div>
              <FieldLabel>Problem</FieldLabel>
              <p className="text-neutral-800">{programme.problem_addressed}</p>
            </div>

            <div className="pl-6 border-l-4 border-info-500">
              <FieldLabel>Structural Cause</FieldLabel>
              <p className="text-neutral-800">{programme.structural_cause}</p>
            </div>

            <div className="pl-12 border-l-4 border-accent-500">
              <FieldLabel>Intervention</FieldLabel>
              <p className="text-neutral-800">{programme.delivery_mechanism}</p>
            </div>
          </div>
        </Section>

        {/* Target Group & Eligibility */}
        <Section title="Who & How">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <FieldLabel>Target Group</FieldLabel>
              <p className="text-neutral-800">{programme.target_group}</p>
            </div>
            <div>
              <FieldLabel>Eligibility</FieldLabel>
              <p className="text-neutral-800">{programme.eligibility}</p>
            </div>
          </div>
        </Section>

        {/* Outputs & Outcomes */}
        <Section title="Deliverables">
          <div className="space-y-6">
            <div>
              <FieldLabel>Outputs</FieldLabel>
              <p className="text-neutral-800">{programme.output}</p>
            </div>
            <div>
              <FieldLabel>Outcomes</FieldLabel>
              <p className="text-neutral-800">{programme.outcome}</p>
            </div>
          </div>
        </Section>

        {/* KPIs */}
        {kpis.length > 0 && (
          <Section title="Key Performance Indicators">
            <div className="divide-y divide-neutral-100">
              {kpis.map((kpi) => (
                <div key={kpi.kpi_id} className="py-6 first:pt-0 last:pb-0">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div>
                      <span className="text-xs font-mono text-neutral-500">{kpi.kpi_id}</span>
                      <h3 className="text-lg font-semibold text-neutral-900">{kpi.kpi_name}</h3>
                    </div>
                    <span className={`shrink-0 text-xs font-semibold px-3 py-1 rounded-full ${
                      kpi.baseline_status === 'source-verified'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {kpi.baseline_status}
                    </span>
                  </div>

                  <p className="text-sm text-neutral-600 mb-4">{kpi.definition}</p>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <TargetCell label="Baseline" value={kpi.baseline_value || 'Not established'} />
                    <TargetCell label="Year 2" value={kpi.year_2_target || '—'} />
                    <TargetCell label="Year 4" value={kpi.year_4_target || '—'} />
                    <TargetCell label="Year 6" value={kpi.year_6_target || '—'} />
                  </div>

                  <div className="mt-4 pt-4 border-t border-neutral-100 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-neutral-500 font-medium">Owner: </span>
                      <span className="text-neutral-900">{kpi.data_owner}</span>
                    </div>
                    <div>
                      <span className="text-neutral-500 font-medium">Verification: </span>
                      <span className="text-neutral-900">{kpi.verification_source}</span>
                    </div>
                  </div>

                  {kpi.notes && (
                    <div className="mt-3 p-3 bg-neutral-50 rounded-lg text-sm text-neutral-600">
                      <strong className="font-semibold text-neutral-700">Note:</strong> {kpi.notes}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </Section>
        )}

        {/* Costing */}
        <Section title="Costing (Central Scenario)">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <CostCell label="Six-Year Total" value={`RM ${totalCost.toFixed(1)}m`} tone="neutral" />
            <CostCell label="New Funding" value={`RM ${newFunding.toFixed(1)}m`} tone="info" />
            <CostCell label="Existing" value={`RM ${existing.toFixed(1)}m`} tone="muted" />
            <CostCell label="Reallocated" value={`RM ${reallocated.toFixed(1)}m`} tone="muted" />
          </div>

          <Link href="/costing" className="text-sm font-semibold text-primary-600 hover:text-primary-700">
            View full costing scenarios →
          </Link>
        </Section>

        {/* Delivery */}
        {responsibility && (
          <Section title="Delivery & Accountability">
            <div className="space-y-4">
              <div>
                <FieldLabel>Lead Ministry</FieldLabel>
                <p className="text-neutral-800">{responsibility.lead_ministry_or_agency}</p>
              </div>
              <div>
                <FieldLabel>Accounting Officer</FieldLabel>
                <p className="text-neutral-800">{responsibility.accounting_officer}</p>
              </div>
              <div>
                <FieldLabel>Supporting Agencies</FieldLabel>
                <p className="text-neutral-800">{programme.supporting_agencies}</p>
              </div>
              {responsibility.mandate_basis && (
                <div>
                  <FieldLabel>Mandate Basis</FieldLabel>
                  <p className="text-neutral-800">{responsibility.mandate_basis}</p>
                </div>
              )}
            </div>
          </Section>
        )}

        {/* Risks */}
        {risks.length > 0 && (
          <Section title="Risks & Safeguards">
            <div className="divide-y divide-neutral-100">
              {risks.map((risk) => (
                <div key={risk.risk_id} className="py-6 first:pt-0 last:pb-0">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <div>
                      <span className="text-xs font-mono text-neutral-500">{risk.risk_id}</span>
                      <h3 className="text-lg font-semibold text-neutral-900">{risk.risk_category}</h3>
                    </div>
                    <div className="flex flex-wrap gap-2 justify-end">
                      <span className={`text-xs font-semibold px-3 py-1 rounded-full ${
                        risk.inherent_rating === 'Critical'
                          ? 'bg-red-100 text-red-800'
                          : risk.inherent_rating === 'Major'
                          ? 'bg-orange-100 text-orange-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {risk.inherent_rating}
                      </span>
                      <span className="text-xs font-semibold px-3 py-1 rounded-full bg-neutral-100 text-neutral-700">
                        → {risk.residual_rating}
                      </span>
                    </div>
                  </div>

                  <p className="text-neutral-800 mb-3">{risk.risk_description}</p>

                  <div className="p-3 bg-info-50 rounded-lg">
                    <h4 className="text-sm font-semibold text-info-900 mb-1">Safeguard</h4>
                    <p className="text-sm text-info-800">{risk.safeguard}</p>
                  </div>
                </div>
              ))}
            </div>
          </Section>
        )}
      </div>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="bg-white rounded-2xl shadow-soft p-6 sm:p-8">
      <h2 className="text-2xl font-bold text-neutral-900 mb-6">{title}</h2>
      {children}
    </section>
  );
}

function FieldLabel({ children }: { children: React.ReactNode }) {
  return (
    <h3 className="text-xs font-semibold tracking-wide text-neutral-500 uppercase mb-2">{children}</h3>
  );
}

function TargetCell({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-neutral-500 font-medium">{label}</div>
      <div className="text-neutral-900">{value}</div>
    </div>
  );
}

function CostCell({ label, value, tone }: { label: string; value: string; tone: 'neutral' | 'info' | 'muted' }) {
  const toneClass =
    tone === 'info' ? 'text-info-600' : tone === 'muted' ? 'text-neutral-700' : 'text-neutral-900';
  return (
    <div className="bg-neutral-50 p-4 rounded-xl">
      <div className="text-sm text-neutral-500 mb-1">{label}</div>
      <div className={`text-2xl font-bold ${toneClass}`}>{value}</div>
    </div>
  );
}
