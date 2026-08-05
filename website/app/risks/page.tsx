import { loadRisks } from '@/lib/data-loader';

export const metadata = {
  title: 'Risks & Safeguards — MIB 2.0',
  description: 'Risk register with safeguards, residual ratings, and monitoring triggers',
};

export default function RisksPage() {
  const risks = loadRisks();

  const byCategory = risks.reduce((acc, risk) => {
    if (!acc[risk.risk_category]) {
      acc[risk.risk_category] = [];
    }
    acc[risk.risk_category].push(risk);
    return acc;
  }, {} as Record<string, typeof risks>);

  const criticalCount = risks.filter(r => r.residual_rating === 'Critical').length;
  const highCount = risks.filter(r => r.residual_rating === 'High').length;
  const mediumCount = risks.filter(r => r.residual_rating === 'Medium').length;
  const lowCount = risks.filter(r => r.residual_rating === 'Low').length;

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
              Risks & Safeguards
            </h1>
            <p className="text-lg text-white/80">
              {risks.length} identified risks with safeguards, residual ratings, and monitoring triggers.
              Every risk has an accountable owner and defined escalation path.
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Risk Summary */}
        <div className="bg-white rounded-2xl shadow-soft p-8 mb-8">
          <h2 className="text-2xl font-bold text-neutral-900 mb-6">Residual Risk Profile</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <RiskCard label="Critical" count={criticalCount} gradient="from-red-500 to-red-600" />
            <RiskCard label="High" count={highCount} gradient="from-orange-500 to-orange-600" />
            <RiskCard label="Medium" count={mediumCount} gradient="from-amber-500 to-amber-600" />
            <RiskCard label="Low" count={lowCount} gradient="from-green-500 to-green-600" />
          </div>
        </div>

        {/* Risks by Category */}
        {Object.entries(byCategory).map(([category, categoryRisks]) => (
          <div key={category} className="bg-white rounded-2xl shadow-soft p-8 mb-8">
            <h2 className="text-2xl font-bold text-neutral-900 mb-6 capitalize">
              {category.replace(/_/g, ' ')} Risks
            </h2>

            <div className="space-y-8">
              {categoryRisks.map((risk) => {
                const inherentColors: Record<string, string> = {
                  Critical: 'bg-red-100 text-red-800 border-red-200',
                  Major: 'bg-orange-100 text-orange-800 border-orange-200',
                  High: 'bg-amber-100 text-amber-800 border-amber-200',
                };

                const residualColors: Record<string, string> = {
                  Critical: 'bg-red-100 text-red-800 border-red-200',
                  High: 'bg-orange-100 text-orange-800 border-orange-200',
                  Medium: 'bg-amber-100 text-amber-800 border-amber-200',
                  Low: 'bg-green-100 text-green-800 border-green-200',
                };

                return (
                  <div key={risk.risk_id} className="pb-8 last:pb-0 border-b last:border-b-0 border-neutral-100">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-grow">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-sm font-mono text-neutral-500 bg-neutral-50 px-3 py-1.5 rounded-lg">
                            {risk.risk_id}
                          </span>
                        </div>
                        <h3 className="text-xl font-bold text-neutral-900">{risk.risk_category}</h3>
                      </div>
                      <div className="flex gap-2">
                        <span className={`text-xs font-semibold px-3 py-1.5 rounded-lg border whitespace-nowrap ${inherentColors[risk.inherent_rating]}`}>
                          Inherent: {risk.inherent_rating}
                        </span>
                        <span className={`text-xs font-semibold px-3 py-1.5 rounded-lg border whitespace-nowrap ${residualColors[risk.residual_rating]}`}>
                          Residual: {risk.residual_rating}
                        </span>
                      </div>
                    </div>

                    <p className="text-neutral-900 mb-4 leading-relaxed">{risk.risk_description}</p>

                    {/* Safeguard */}
                    <div className="p-4 bg-info-50 border border-info-200 rounded-xl mb-4">
                      <h4 className="text-sm font-semibold text-info-900 mb-2">Safeguard</h4>
                      <p className="text-sm text-info-900 leading-relaxed">{risk.safeguard}</p>
                    </div>

                    {/* Metadata */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <div className="text-neutral-600 font-medium mb-1">Owner</div>
                        <div className="text-neutral-900">{risk.owner}</div>
                      </div>
                      <div>
                        <div className="text-neutral-600 font-medium mb-1">Likelihood × Impact</div>
                        <div className="text-neutral-900">{risk.likelihood} × {risk.impact}</div>
                      </div>
                      <div>
                        <div className="text-neutral-600 font-medium mb-1">Affected Programmes</div>
                        <div className="text-neutral-900">
                          {risk.affected_programmes === 'All' ? (
                            'All programmes'
                          ) : (
                            <span className="font-mono text-xs">{risk.affected_programmes}</span>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Monitoring Trigger */}
                    {risk.monitoring_trigger && (
                      <div className="mt-4 p-3 bg-neutral-50 rounded-xl border border-neutral-200">
                        <h4 className="text-xs font-semibold text-neutral-700 uppercase mb-1">Monitoring Trigger</h4>
                        <p className="text-sm text-neutral-900">{risk.monitoring_trigger}</p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function RiskCard({ label, count, gradient }: { label: string; count: number; gradient: string }) {
  return (
    <div className="relative bg-white rounded-xl p-6 text-center border border-neutral-200">
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-5 rounded-xl`} />
      <div className="relative">
        <div className={`text-4xl font-bold bg-gradient-to-br ${gradient} bg-clip-text text-transparent mb-2`}>
          {count}
        </div>
        <div className="text-sm font-semibold text-neutral-900">{label}</div>
      </div>
    </div>
  );
}
