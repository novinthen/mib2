export const metadata = {
  title: 'Why MIB 2.0 — Malaysian Indian Blueprint',
  description: 'The case for a coordinated policy framework addressing structural barriers',
};

export default function WhyPage() {
  return (
    <div className="bg-white">
      {/* Hero */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-700 py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">Why MIB 2.0</h1>
          <p className="text-xl text-white/80">
            The case for a coordinated, evidence-led framework addressing structural barriers
            across documentation, education, livelihoods, and institutional participation
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
        {/* The Problem */}
        <section>
          <h2 className="text-3xl font-bold text-neutral-900 mb-6">The Structural Challenge</h2>
          <div className="space-y-4 text-lg text-neutral-700 leading-relaxed">
            <p>
              A child without documentation struggles to enter school. A student without guidance misses opportunities.
              A graduate without networks struggles to find quality work. A family with unstable income postpones
              ownership. The barriers compound.
            </p>
            <p>
              Indian absolute poverty incidence rose from 4.8% (2019) to 5.4% (2022) — below the Bumiputera rate of
              7.9%, but on an adverse trend. The justification rests not on aggregate poverty superiority but on
              specific structural exclusions.
            </p>
            <p>
              Documentation sits with one authority, education with another, training and housing elsewhere. For a
              low-income household, an elderly applicant, a single mother, or a displaced estate family, the system
              itself becomes the obstacle.
            </p>
          </div>
        </section>

        {/* What's Different */}
        <section className="bg-gradient-to-br from-primary-50 to-info-50 rounded-3xl p-8 md:p-12">
          <h2 className="text-3xl font-bold text-neutral-900 mb-8">What&apos;s Different This Time</h2>
          <div className="space-y-6">
            <DifferenceCard
              title="Evidence-Led, Not Assertion-Based"
              description="Every claim is traceable to verified sources. Eleven of sixteen KPIs have no baseline — establishing
              baselines is the principal Phase 1 deliverable. Missing baselines are acknowledged, not invented."
            />
            <DifferenceCard
              title="Needs-Based Eligibility"
              description="Support targets household income, documentation status, and structural barriers — not ethnicity alone.
              Designed to be extensible to any community facing similar barriers."
            />
            <DifferenceCard
              title="Quarterly Prime Ministerial Oversight"
              description="A PM-chaired Task Force meeting quarterly with published dashboards within 14 days. Sustained
              chairmanship is the single largest delivery risk and is named openly (RSK-01)."
            />
            <DifferenceCard
              title="Transparent Costing"
              description="Three scenarios (conservative/central/expanded) with confidence classes. 68.1% of the central scenario
              is Provisional — assumptions are flagged, not hidden. The RM355.3 million central Phase 1 figure is a gross
              planning cost, not a Treasury-validated ceiling; ten fiscal controls define the evidence required before funding."
            />
          </div>
        </section>

        {/* The Coordination Argument */}
        <section>
          <h2 className="text-3xl font-bold text-neutral-900 mb-6">Why Coordination Matters</h2>
          <div className="space-y-4 text-lg text-neutral-700 leading-relaxed">
            <p>
              The citizenship backlog sits in the Home Ministry, civil service intake in JPA, matriculation and SJKT
              in Education, equity and micro-credit across finance agencies. No ministerial-level unit can coordinate
              across these silos.
            </p>
            <p>
              Money is disbursed. Training is completed. An application is approved. A beneficiary is counted. But the
              system does not answer whether the family moved forward.
            </p>
            <p>
              One family should experience one Government. The delivery model structures household-centered case
              management, not programme-centered activity reporting.
            </p>
          </div>
        </section>

        {/* The Implementation Gap */}
        <section className="bg-blue-50 rounded-3xl p-8 md:p-12 border border-blue-200">
          <h2 className="text-3xl font-bold text-neutral-900 mb-6">The Implementation Gap</h2>
          <div className="space-y-4 text-lg text-neutral-700 leading-relaxed">
            <p>
              The community has never lacked plans, only execution. MIB 2017 set a 7% civil service target by 2026 —
              the actual share rose from 3.6% (2017) to 3.7% (2024). A resolution target for 25,000 documentation
              cases — no published outturn exists.
            </p>
            <p>
              Coordination units placed in line ministries lose convening power over other ministries. MITRA holds
              programme funds but no authority over ministries that control the levers.
            </p>
            <p>
              The Task Force design addresses this: PM chairmanship, quarterly cadence, published dashboards,
              independent evaluation, and phase gating so that failure does not strand investment.
            </p>
          </div>
        </section>

        {/* What This Is Not */}
        <section>
          <h2 className="text-3xl font-bold text-neutral-900 mb-6">What This Is Not</h2>
          <div className="space-y-4">
            <NotCard
              title="Not a quota or set-aside"
              description="The 2% procurement quota was rejected on Article 8 grounds. Eligibility is needs-based with outreach targeted to the community."
            />
            <NotCard
              title="Not universal coverage"
              description="Household progression has a proposed Phase 3 concurrent service capacity of approximately 10% of the estimated low-income population. Cumulative reach is not claimed. Enrolment is voluntary and consent-based."
            />
            <NotCard
              title="Not guaranteed outcomes"
              description="Citizenship decisions rest with the Minister under Article 15A. Public service appointments rest with SPA. Outcomes are measured and published, not mandated."
            />
          </div>
        </section>

        {/* Next Steps */}
        <section className="bg-gradient-to-br from-info-600 to-info-700 rounded-3xl p-8 md:p-12 text-white">
          <h2 className="text-3xl font-bold mb-6">Next Steps</h2>
          <div className="space-y-4 text-lg leading-relaxed text-white/90">
            <p>
              This proposal asks Cabinet to approve policy direction and a 90-day validation exercise. The programme
              architecture is conditionally endorsed only as a design basis; no implementation or fiscal envelope is approved.
            </p>
            <p>
              Phase 1 requires a later express decision identifying its approved components, ceiling, owners and launch
              conditions. The 30 open validation items are now separated into 12 pre-submission gates, 8
              programme-launch gates, 2 phase-expansion gates, 5 operational baselines, and 3 deferrable matters.
            </p>
            <p>
              Six strict gates remain. Four further items are decision-dependent critical. Each item has one owner,
              required evidence, a deadline, escalation route, financial consequence, and mapped decision. An unresolved
              item blocks only the affected decision or programme—not unrelated work.
            </p>
            <p>
              Legal clearance is not claimed. Eighteen legal issues remain open: 10 must be resolved before the affected
              implementation submission and 8 before the affected programme launches. Each issue identifies the competent
              authority, written evidence required, affected decision, and consequence if unresolved. PRG-04 has six
              separate state, religious-administration, public-purpose, referral, expenditure, and data clearances.
            </p>
            <p>
              Sixteen programme design sheets now specify the service, exclusions, accountable owner, authority route,
              delivery channel, geography, provisional volume and cost, KPI, complaint route, data controls, dependencies,
              and stop, redesign, and expansion tests. All 16 remain internal drafts; none is represented as accepted by
              its accounting officer or ready to launch.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}

function DifferenceCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-soft">
      <h3 className="text-xl font-bold text-neutral-900 mb-3">{title}</h3>
      <p className="text-neutral-700 leading-relaxed">{description}</p>
    </div>
  );
}

function NotCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="flex items-start gap-4 p-6 bg-neutral-50 rounded-2xl border border-neutral-200">
      <div className="text-3xl flex-shrink-0">❌</div>
      <div>
        <h3 className="font-bold text-neutral-900 mb-2">{title}</h3>
        <p className="text-neutral-700 leading-relaxed">{description}</p>
      </div>
    </div>
  );
}
