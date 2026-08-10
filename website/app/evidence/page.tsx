import { loadClaims, loadSources } from '@/lib/data-loader';

export const metadata = {
  title: 'Evidence Room — MIB 2.0',
  description: 'Claims, figures, sources, conflicts, assumptions, and quality assessments with stable IDs',
};

export default function EvidencePage() {
  const claims = loadClaims();
  const sources = loadSources();

  const byStatus = {
    verified: claims.filter(c => c.verification_status === 'source-verified'),
    unsupported: claims.filter(c => c.verification_status === 'unsupported'),
    disputed: claims.filter(c => c.verification_status === 'inconsistent' || c.verification_status === 'disputed'),
    pending: claims.filter(c => c.verification_status === 'cited-source-not-yet-inspected'),
  };

  const tierCounts = sources.reduce((acc, s) => {
    const tier = parseInt(s.tier) || 0;
    acc[tier] = (acc[tier] || 0) + 1;
    return acc;
  }, {} as Record<number, number>);

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
              Evidence Room
            </h1>
            <p className="text-lg text-white/80">
              Every claim traceable to a source with stable IDs. {byStatus.verified.length} claims verified,
              {byStatus.unsupported.length} unsupported. Conflicts disclosed, never silently reconciled.
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Summary */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-2xl shadow-soft p-8">
            <h2 className="text-2xl font-bold text-neutral-900 mb-6">Claims & Figures</h2>
            <div className="space-y-4">
              <StatRow label="Source-Verified" value={byStatus.verified.length} gradient="from-green-500 to-green-600" />
              <StatRow label="Unsupported" value={byStatus.unsupported.length} gradient="from-red-500 to-red-600" />
              <StatRow label="Disputed" value={byStatus.disputed.length} gradient="from-orange-500 to-orange-600" />
              <StatRow label="Pending" value={byStatus.pending.length} gradient="from-amber-500 to-amber-600" />
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-soft p-8">
            <h2 className="text-2xl font-bold text-neutral-900 mb-6">Sources</h2>
            <div className="text-5xl font-bold bg-gradient-to-br from-primary-500 to-primary-600 bg-clip-text text-transparent mb-2">
              {sources.length}
            </div>
            <div className="text-sm text-neutral-600 mb-6">Total sources in register</div>
            <div className="pt-4 border-t border-neutral-200">
              <div className="text-sm font-semibold text-neutral-700 mb-3">By Tier</div>
              <div className="space-y-2">
                {Object.entries(tierCounts)
                  .sort(([a], [b]) => parseInt(a) - parseInt(b))
                  .map(([tier, count]) => (
                    <div key={tier} className="flex justify-between items-center text-sm">
                      <span className="text-neutral-600">Tier {tier}</span>
                      <span className="font-semibold text-neutral-900 bg-neutral-100 px-3 py-1 rounded-lg">{count}</span>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        </div>

        {/* Sources */}
        <div className="bg-white rounded-2xl shadow-soft p-8 mb-8">
          <h2 className="text-2xl font-bold text-neutral-900 mb-6">Source Register</h2>
          <div className="space-y-6">
            {sources.map((source) => (
              <div key={source.source_id} className="pb-6 last:pb-0 border-b last:border-b-0 border-neutral-100">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-grow">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-sm font-mono text-neutral-500 bg-neutral-50 px-3 py-1.5 rounded-lg">
                        {source.source_id}
                      </span>
                      <span className="text-xs font-semibold px-3 py-1.5 rounded-lg bg-blue-100 text-blue-800 border border-blue-200">
                        Tier {source.tier}
                      </span>
                    </div>
                    <h3 className="text-lg font-semibold text-neutral-900">{source.title}</h3>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3 text-sm">
                  <div>
                    <span className="text-neutral-600">Institution: </span>
                    <span className="text-neutral-900 font-medium">{source.issuing_institution}</span>
                  </div>
                  <div>
                    <span className="text-neutral-600">Date: </span>
                    <span className="text-neutral-900 font-medium">{source.publication_date}</span>
                  </div>
                  <div>
                    <span className="text-neutral-600">Scope: </span>
                    <span className="text-neutral-900 font-medium">{source.geographic_scope}</span>
                  </div>
                  <div>
                    <span className="text-neutral-600">Support: </span>
                    <span className="text-neutral-900 font-medium">{source.supports_directly_or_inference}</span>
                  </div>
                </div>

                {source.limitations && (
                  <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-sm mb-3">
                    <strong className="text-amber-900">Limitations:</strong>{' '}
                    <span className="text-amber-900">{source.limitations}</span>
                  </div>
                )}

                {source.url && source.url.startsWith('http') && (
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 font-medium"
                  >
                    View source
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Claims by Status */}
        {Object.entries(byStatus).map(([status, statusClaims]) => {
          if (statusClaims.length === 0) return null;

          const statusConfig: Record<string, { bg: string; border: string; text: string }> = {
            verified: { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-900' },
            unsupported: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-900' },
            disputed: { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-900' },
            pending: { bg: 'bg-amber-50', border: 'border-amber-200', text: 'text-amber-900' },
          };

          const config = statusConfig[status];

          return (
            <div key={status} className={`${config.bg} border ${config.border} rounded-2xl p-8 mb-8`}>
              <h2 className={`text-2xl font-bold ${config.text} mb-6 capitalize`}>
                {status} Claims ({statusClaims.length})
              </h2>
              <div className="space-y-4">
                {statusClaims.slice(0, 10).map((claim) => (
                  <div key={claim.claim_id} className="bg-white rounded-xl p-4 shadow-soft">
                    <div className="flex items-start justify-between mb-2">
                      <span className="text-sm font-mono text-neutral-500 bg-neutral-50 px-3 py-1 rounded-lg">
                        {claim.claim_id}
                      </span>
                      <span className="text-xs font-semibold px-2 py-1 rounded-lg bg-neutral-100 text-neutral-700">
                        {claim.claim_type}
                      </span>
                    </div>
                    <p className="text-sm text-neutral-900 mb-2 leading-relaxed">{claim.verbatim_or_close_claim}</p>
                    {claim.adopted_treatment && (
                      <p className="text-xs text-neutral-600">
                        <strong>Treatment:</strong> {claim.adopted_treatment}
                      </p>
                    )}
                  </div>
                ))}
                {statusClaims.length > 10 && (
                  <p className="text-sm text-neutral-600 text-center pt-2">
                    ... and {statusClaims.length - 10} more
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function StatRow({ label, value, gradient }: { label: string; value: number; gradient: string }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-neutral-100 last:border-b-0">
      <span className="text-sm text-neutral-700 font-medium">{label}</span>
      <span className={`text-2xl font-bold bg-gradient-to-br ${gradient} bg-clip-text text-transparent`}>
        {value}
      </span>
    </div>
  );
}
