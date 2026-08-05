import { loadProgrammes } from '@/lib/data-loader';
import ProgrammeFilter from '@/components/ProgrammeFilter';

export const metadata = {
  title: 'Programme Explorer — MIB 2.0',
  description: 'Explore all 16 programmes across the four pillars of the Malaysian Indian Blueprint 2.0',
};

export default function ProgrammesPage() {
  const programmes = loadProgrammes();

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <div className="bg-gradient-to-br from-primary-600 to-primary-700 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl">
            <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
              Programme Explorer
            </h1>
            <p className="text-lg text-white/80">
              Browse all {programmes.length} programmes across four pillars. Each programme connects
              structural problems to targeted interventions with clear outputs and evidence-linked KPIs.
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <ProgrammeFilter programmes={programmes} />
      </div>
    </div>
  );
}
