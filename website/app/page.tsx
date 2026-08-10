import Link from 'next/link';
import { loadProgrammes, calculateCostingSummary } from '@/lib/data-loader';

export default function HomePage() {
  const programmes = loadProgrammes();
  const costingSummary = calculateCostingSummary('central');

  const pillarCounts = {
    'P1 Foundations': programmes.filter(p => p.pillar === 'P1 Foundations').length,
    'P2 Progression': programmes.filter(p => p.pillar === 'P2 Progression').length,
    'P3 Livelihoods': programmes.filter(p => p.pillar === 'P3 Livelihoods').length,
    'P4 Institutional Participation': programmes.filter(p => p.pillar === 'P4 Institutional Participation').length,
  };

  return (
    <div className="bg-white">
      {/* Hero Section with Modern Gradient */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-500 to-primary-700">
        <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white/5 to-white/10" />
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
          <div className="text-center space-y-8 animate-fade-in">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full border border-white/20">
              <span className="w-2 h-2 bg-accent-400 rounded-full animate-pulse" />
              <span className="text-white/90 text-sm font-medium">Policy Framework 2026–2031</span>
            </div>
            
            <h1 className="text-display-md sm:text-display-lg text-white max-w-4xl mx-auto">
              Malaysian Indian Blueprint 2.0
            </h1>
            
            <p className="text-xl sm:text-2xl text-white/80 max-w-2xl mx-auto font-light">
              Evidence-led progression framework addressing structural barriers across {programmes.length} targeted programmes
            </p>
            
            <div className="flex flex-wrap justify-center gap-4 pt-4">
              <Link
                href="/programmes"
                className="group px-8 py-4 bg-white text-primary-600 font-semibold rounded-xl hover:bg-white/95 transition-all shadow-soft-lg hover:shadow-soft-xl hover:-translate-y-0.5"
              >
                <span className="flex items-center gap-2">
                  Explore Programmes
                  <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </span>
              </Link>
              <Link
                href="/why"
                className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl hover:bg-white/20 transition-all border border-white/20"
              >
                Why MIB 2.0
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Key Figures with Modern Cards */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-neutral-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-neutral-900 mb-4">Portfolio Overview</h2>
            <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
              Comprehensive framework with verified baselines and transparent costing
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard
              label="Programmes"
              value={programmes.length.toString()}
              description="Across four pillars"
              gradient="from-primary-500 to-primary-600"
            />
            <StatCard
              label="Investment"
              value={`RM ${(costingSummary.six_year_gross / 1000).toFixed(2)}bn`}
              description="Six-year total (2026 prices)"
              gradient="from-accent-500 to-accent-600"
            />
            <StatCard
              label="New Funding"
              value={`RM ${(costingSummary.new_funding / 1000).toFixed(2)}bn`}
              description="Incremental requirement"
              gradient="from-info-500 to-info-600"
            />
            <StatCard
              label="KPIs"
              value="16"
              description="Measurable outcomes"
              gradient="from-purple-500 to-purple-600"
            />
          </div>
        </div>
      </section>

      {/* Four Pillars */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-neutral-900 mb-4">Four Pillars</h2>
            <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
              Targeted interventions addressing specific structural barriers with clear outcomes
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <PillarCard
              number="1"
              title="Foundations"
              description="Documentation, early childhood, schools, and community facilities"
              programmeCount={pillarCounts['P1 Foundations']}
              href="/programmes"
              color="primary"
            />
            <PillarCard
              number="2"
              title="Progression"
              description="School-to-pathway guidance, TVET, tertiary access, and professional entry"
              programmeCount={pillarCounts['P2 Progression']}
              href="/programmes"
              color="info"
            />
            <PillarCard
              number="3"
              title="Livelihoods"
              description="Household progression, enterprise growth, savings, and housing security"
              programmeCount={pillarCounts['P3 Livelihoods']}
              href="/programmes"
              color="accent"
            />
            <PillarCard
              number="4"
              title="Participation"
              description="Public service pipeline and professional advancement"
              programmeCount={pillarCounts['P4 Institutional Participation']}
              href="/programmes"
              color="purple"
            />
          </div>
        </div>
      </section>

      {/* Key Principles */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-neutral-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-neutral-900 mb-4">Key Principles</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <PrincipleCard
              title="Evidence-Led"
              description="Every claim traceable to verified sources. Missing baselines acknowledged, not invented."
              icon="📊"
            />
            <PrincipleCard
              title="Needs-Based"
              description="Targeting household income, documentation status, and structural barriers—not ethnicity alone."
              icon="⚖️"
            />
            <PrincipleCard
              title="Transparent"
              description="Delegated delivery ownership, meeting-independent dashboards, and independent evaluation."
              icon="🔍"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">
          <div className="relative overflow-hidden bg-gradient-to-br from-primary-600 to-primary-700 rounded-3xl p-12 text-center shadow-soft-xl">
            <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white/5 to-white/10" />
            <div className="relative space-y-6">
              <h2 className="text-3xl sm:text-4xl font-bold text-white">
                Explore the Blueprint
              </h2>
              <p className="text-lg text-white/80 max-w-2xl mx-auto">
                Navigate through programmes, costing scenarios, KPIs, and evidence sources
              </p>
              <div className="flex flex-wrap justify-center gap-4 pt-4">
                <Link href="/programmes" className="px-8 py-4 bg-white text-primary-600 font-semibold rounded-xl hover:bg-white/95 transition-all shadow-soft">
                  Programme Explorer
                </Link>
                <Link href="/costing" className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl hover:bg-white/20 transition-all border border-white/20">
                  Costing Scenarios
                </Link>
                <Link href="/evidence" className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-xl hover:bg-white/20 transition-all border border-white/20">
                  Evidence Room
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function StatCard({ label, value, description, gradient }: { 
  label: string; 
  value: string; 
  description: string;
  gradient: string;
}) {
  return (
    <div className="group relative bg-white rounded-2xl p-8 shadow-soft hover:shadow-soft-lg transition-all hover:-translate-y-1">
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-5 rounded-2xl transition-opacity`} />
      <div className="relative">
        <div className="text-sm font-medium text-neutral-500 mb-2">{label}</div>
        <div className={`text-4xl font-bold bg-gradient-to-br ${gradient} bg-clip-text text-transparent mb-2`}>
          {value}
        </div>
        <div className="text-sm text-neutral-600">{description}</div>
      </div>
    </div>
  );
}

function PillarCard({
  number,
  title,
  description,
  programmeCount,
  href,
  color
}: {
  number: string;
  title: string;
  description: string;
  programmeCount: number;
  href: string;
  color: 'primary' | 'info' | 'accent' | 'purple';
}) {
  const colorClasses = {
    primary: 'from-primary-500 to-primary-600',
    info: 'from-info-500 to-info-600',
    accent: 'from-accent-500 to-accent-600',
    purple: 'from-purple-500 to-purple-600',
  };

  return (
    <Link href={href} className="group">
      <div className="relative bg-white rounded-2xl p-8 shadow-soft hover:shadow-soft-lg transition-all hover:-translate-y-1 h-full">
        <div className={`absolute inset-0 bg-gradient-to-br ${colorClasses[color]} opacity-0 group-hover:opacity-5 rounded-2xl transition-opacity`} />
        <div className="relative space-y-4">
          <div className="flex items-center justify-between">
            <div className={`w-14 h-14 bg-gradient-to-br ${colorClasses[color]} rounded-2xl flex items-center justify-center text-2xl font-bold text-white shadow-glow`}>
              {number}
            </div>
            <div className="text-sm font-semibold text-neutral-500">{programmeCount} programmes</div>
          </div>
          <h3 className="text-xl font-bold text-neutral-900 group-hover:text-primary-600 transition-colors">
            {title}
          </h3>
          <p className="text-sm text-neutral-600 leading-relaxed">{description}</p>
        </div>
      </div>
    </Link>
  );
}

function PrincipleCard({ title, description, icon }: { title: string; description: string; icon: string }) {
  return (
    <div className="bg-white rounded-2xl p-8 shadow-soft hover:shadow-soft-lg transition-all">
      <div className="text-5xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold text-neutral-900 mb-3">{title}</h3>
      <p className="text-neutral-600 leading-relaxed">{description}</p>
    </div>
  );
}
