import { loadKPIs, loadProgrammes } from '@/lib/data-loader';
import Link from 'next/link';

export const metadata = {
  title: 'KPIs — MIB 2.0',
  description: 'Key Performance Indicators with Year 2/4/6 targets, baseline status, and verification sources',
};

export default function KPIsPage() {
  const kpis = loadKPIs();
  const programmes = loadProgrammes();

  const baselineStats = {
    verified: kpis.filter(k => k.baseline_status === 'source-verified').length,
    toEstablish: kpis.filter(k => k.baseline_status === 'to-be-established').length,
    disputed: kpis.filter(k => k.baseline_status === 'disputed').length,
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
              Key Performance Indicators
            </h1>
            <p className="text-lg text-white/80">
              {kpis.length} KPIs measuring outputs and outcomes. {baselineStats.verified} have
              verified baselines; {baselineStats.toEstablish} require establishment in Year 1.
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Baseline Status Summary */}
        <div className="bg-white rounded-2xl shadow-soft p-8 mb-8">
          <h2 className="text-2xl font-bold text-neutral-900 mb-6">Baseline Status</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatusCard
              count={baselineStats.verified}
              label="Source-Verified"
              description="Baseline exists and is traceable"
              gradient="from-green-500 to-green-600"
            />
            <StatusCard
              count={baselineStats.toEstablish}
              label="To Be Established"
              description="Year 1 deliverable"
              gradient="from-amber-500 to-amber-600"
            />
            <StatusCard
              count={baselineStats.disputed}
              label="Disputed"
              description="Conflicting sources"
              gradient="from-orange-500 to-orange-600"
            />
          </div>

          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-xl">
            <p className="text-sm text-blue-900">
              <strong>Baseline integrity:</strong> Establishing baselines is the principal Phase 1 deliverable.
              No numeric outcome target is set where no baseline exists.
            </p>
          </div>
        </div>

        {/* KPI List */}
        <div className="space-y-6">
          {kpis.map((kpi) => {
            const programme = programmes.find(p => p.programme_id === kpi.programme_id);
            
            const statusColors: Record<string, string> = {
              'source-verified': 'bg-green-100 text-green-800 border-green-200',
              'disputed': 'bg-orange-100 text-orange-800 border-orange-200',
              'to-be-established': 'bg-amber-100 text-amber-800 border-amber-200',
            };

            const typeColors: Record<string, string> = {
              'output': 'bg-blue-100 text-blue-800 border-blue-200',
              'outcome': 'bg-purple-100 text-purple-800 border-purple-200',
            };

            return (
              <div key={kpi.kpi_id} className="bg-white rounded-2xl shadow-soft hover:shadow-soft-lg transition-all p-8">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-sm font-mono text-neutral-500 bg-neutral-50 px-3 py-1.5 rounded-lg">
                        {kpi.kpi_id}
                      </span>
                      <span className={`text-xs font-semibold px-3 py-1.5 rounded-lg border ${statusColors[kpi.baseline_status] || statusColors['to-be-established']}`}>
                        {kpi.baseline_status}
                      </span>
                      <span className={`text-xs font-semibold px-3 py-1.5 rounded-lg border ${typeColors[kpi.indicator_type]}`}>
                        {kpi.indicator_type}
                      </span>
                    </div>
                    <h3 className="text-2xl font-bold text-neutral-900 mb-2">{kpi.kpi_name}</h3>
                    {programme && (
                      <Link
                        href={`/programmes/${programme.programme_id}`}
                        className="text-sm text-primary-600 hover:text-primary-700 font-medium inline-flex items-center gap-1"
                      >
                        {programme.programme_name}
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </Link>
                    )}
                  </div>
                </div>

                <div className="mb-6 p-4 bg-neutral-50 rounded-xl">
                  <h4 className="text-sm font-semibold text-neutral-700 mb-2">Definition</h4>
                  <p className="text-neutral-900 leading-relaxed">{kpi.definition}</p>
                </div>

                {/* Baseline & Targets */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-neutral-50 rounded-xl p-4">
                    <div className="text-xs font-semibold text-neutral-600 uppercase mb-1">
                      Baseline ({kpi.baseline_year || 'TBE'})
                    </div>
                    <div className="text-base font-semibold text-neutral-900">
                      {kpi.baseline_value || 'Not established'}
                    </div>
                  </div>
                  <div className="bg-blue-50 rounded-xl p-4">
                    <div className="text-xs font-semibold text-blue-700 uppercase mb-1">Year 2</div>
                    <div className="text-base font-semibold text-blue-900">
                      {kpi.year_2_target || 'n/a'}
                    </div>
                  </div>
                  <div className="bg-blue-50 rounded-xl p-4">
                    <div className="text-xs font-semibold text-blue-700 uppercase mb-1">Year 4</div>
                    <div className="text-base font-semibold text-blue-900">
                      {kpi.year_4_target || 'n/a'}
                    </div>
                  </div>
                  <div className="bg-blue-50 rounded-xl p-4">
                    <div className="text-xs font-semibold text-blue-700 uppercase mb-1">Year 6</div>
                    <div className="text-base font-semibold text-blue-900">
                      {kpi.year_6_target || 'n/a'}
                    </div>
                  </div>
                </div>

                {/* Measurement Details */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pb-6 border-b border-neutral-200">
                  <div>
                    <div className="text-sm font-semibold text-neutral-700 mb-1">Data Owner</div>
                    <div className="text-sm text-neutral-900">{kpi.data_owner}</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-neutral-700 mb-1">Verification</div>
                    <div className="text-sm text-neutral-900">{kpi.verification_source}</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-neutral-700 mb-1">Frequency</div>
                    <div className="text-sm text-neutral-900">{kpi.measurement_frequency}</div>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-neutral-700 mb-1">Disaggregation</div>
                    <div className="text-sm text-neutral-900">{kpi.disaggregation || 'n/a'}</div>
                  </div>
                </div>

                {/* Notes */}
                {kpi.notes && (
                  <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-xl">
                    <h4 className="text-sm font-semibold text-amber-900 mb-2">Note</h4>
                    <p className="text-sm text-amber-900">{kpi.notes}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function StatusCard({ 
  count, 
  label, 
  description, 
  gradient 
}: { 
  count: number; 
  label: string; 
  description: string; 
  gradient: string;
}) {
  return (
    <div className="relative bg-white rounded-xl p-6 border border-neutral-200">
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-5 rounded-xl`} />
      <div className="relative">
        <div className={`text-4xl font-bold bg-gradient-to-br ${gradient} bg-clip-text text-transparent mb-2`}>
          {count}
        </div>
        <div className="text-sm font-semibold text-neutral-900 mb-1">{label}</div>
        <div className="text-xs text-neutral-600">{description}</div>
      </div>
    </div>
  );
}
