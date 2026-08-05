import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-neutral-50 border-t border-neutral-200 no-print">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          <div>
            <h3 className="text-neutral-900 font-semibold text-sm mb-4">About</h3>
            <ul className="space-y-2.5 text-sm">
              <li><Link href="/why" className="text-neutral-600 hover:text-primary-600 transition-colors">Why MIB 2.0</Link></li>
              <li><Link href="/programmes" className="text-neutral-600 hover:text-primary-600 transition-colors">Four Pillars</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-neutral-900 font-semibold text-sm mb-4">Programmes</h3>
            <ul className="space-y-2.5 text-sm">
              <li><Link href="/programmes" className="text-neutral-600 hover:text-primary-600 transition-colors">Programme Explorer</Link></li>
              <li><Link href="/kpis" className="text-neutral-600 hover:text-primary-600 transition-colors">KPIs</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-neutral-900 font-semibold text-sm mb-4">Evidence</h3>
            <ul className="space-y-2.5 text-sm">
              <li><Link href="/costing" className="text-neutral-600 hover:text-primary-600 transition-colors">Costing</Link></li>
              <li><Link href="/evidence" className="text-neutral-600 hover:text-primary-600 transition-colors">Evidence Room</Link></li>
              <li><Link href="/risks" className="text-neutral-600 hover:text-primary-600 transition-colors">Risks</Link></li>
            </ul>
          </div>

          <div>
            <div className="w-10 h-10 bg-gradient-primary rounded-xl flex items-center justify-center font-bold text-white shadow-glow mb-4">
              MIB
            </div>
            <p className="text-xs text-neutral-600 leading-relaxed">
              Evidence-led policy framework for 2026–2031
            </p>
          </div>
        </div>

        <div className="pt-8 border-t border-neutral-200">
          <div className="text-xs text-neutral-500 space-y-2">
            <p>Malaysian Indian Blueprint 2.0 — Progression Blueprint 2026–2031</p>
            <p>
              All figures derived from authoritative registers at build time. Price basis: 2026 nominal ringgit.
            </p>
            <p className="text-neutral-400">
              Policy proposals for preliminary Cabinet consideration. No figures represent approved funding or guaranteed outcomes.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
