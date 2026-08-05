'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Programme, Pillar } from '@/types';

interface ProgrammeFilterProps {
  programmes: Programme[];
}

export default function ProgrammeFilter({ programmes }: ProgrammeFilterProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPillar, setSelectedPillar] = useState<Pillar | 'all'>('all');
  const [selectedPhase, setSelectedPhase] = useState<string>('all');

  const pillars: (Pillar | 'all')[] = [
    'all',
    'P1 Foundations',
    'P2 Progression',
    'P3 Livelihoods',
    'P4 Institutional Participation',
  ];

  const phases = ['all', '1', '2', '3', '1-2', '1-3', '2-3', '1-2-3'];

  const filtered = programmes.filter((p) => {
    const matchesSearch =
      searchTerm === '' ||
      p.programme_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.problem_addressed.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.target_group.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesPillar = selectedPillar === 'all' || p.pillar === selectedPillar;
    const matchesPhase = selectedPhase === 'all' || p.phase.includes(selectedPhase);

    return matchesSearch && matchesPillar && matchesPhase;
  });

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="bg-white rounded-2xl shadow-soft p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-neutral-700 mb-2">
              Search
            </label>
            <div className="relative">
              <input
                id="search"
                type="text"
                placeholder="Search programmes..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2.5 pl-10 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              />
              <svg className="w-5 h-5 text-neutral-400 absolute left-3 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          <div>
            <label htmlFor="pillar" className="block text-sm font-medium text-neutral-700 mb-2">
              Pillar
            </label>
            <select
              id="pillar"
              value={selectedPillar}
              onChange={(e) => setSelectedPillar(e.target.value as Pillar | 'all')}
              className="w-full px-4 py-2.5 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            >
              {pillars.map((p) => (
                <option key={p} value={p}>
                  {p === 'all' ? 'All Pillars' : p}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="phase" className="block text-sm font-medium text-neutral-700 mb-2">
              Phase
            </label>
            <select
              id="phase"
              value={selectedPhase}
              onChange={(e) => setSelectedPhase(e.target.value)}
              className="w-full px-4 py-2.5 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            >
              {phases.map((phase) => (
                <option key={phase} value={phase}>
                  {phase === 'all' ? 'All Phases' : `Phase ${phase}`}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="mt-4 flex items-center justify-between">
          <span className="text-sm text-neutral-600">
            Showing <span className="font-semibold text-neutral-900">{filtered.length}</span> of {programmes.length} programmes
          </span>
          {(searchTerm || selectedPillar !== 'all' || selectedPhase !== 'all') && (
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedPillar('all');
                setSelectedPhase('all');
              }}
              className="text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              Clear filters
            </button>
          )}
        </div>
      </div>

      {/* Results */}
      <div className="grid grid-cols-1 gap-6">
        {filtered.map((programme) => (
          <ProgrammeCard key={programme.programme_id} programme={programme} />
        ))}

        {filtered.length === 0 && (
          <div className="text-center py-16 bg-white rounded-2xl shadow-soft">
            <svg className="w-16 h-16 text-neutral-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-lg font-semibold text-neutral-900 mb-2">No programmes found</h3>
            <p className="text-neutral-600">Try adjusting your search criteria</p>
          </div>
        )}
      </div>
    </div>
  );
}

function ProgrammeCard({ programme }: { programme: Programme }) {
  const pillarColors: Record<string, { bg: string; text: string; border: string }> = {
    'P1 Foundations': { bg: 'bg-primary-50', text: 'text-primary-700', border: 'border-primary-200' },
    'P2 Progression': { bg: 'bg-info-50', text: 'text-info-700', border: 'border-info-200' },
    'P3 Livelihoods': { bg: 'bg-accent-50', text: 'text-accent-700', border: 'border-accent-200' },
    'P4 Institutional Participation': { bg: 'bg-purple-50', text: 'text-purple-700', border: 'border-purple-200' },
  };

  const colors = pillarColors[programme.pillar] || pillarColors['P1 Foundations'];

  return (
    <Link href={`/programmes/${programme.programme_id}`}>
      <div className="group bg-white rounded-2xl shadow-soft hover:shadow-soft-lg transition-all hover:-translate-y-1 p-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-grow">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-xs font-mono text-neutral-500 bg-neutral-50 px-3 py-1 rounded-lg">
                {programme.programme_id}
              </span>
              <span className={`text-xs font-semibold px-3 py-1 rounded-lg ${colors.bg} ${colors.text} border ${colors.border}`}>
                {programme.pillar}
              </span>
              <span className="text-xs font-semibold px-3 py-1 rounded-lg bg-neutral-100 text-neutral-700">
                Phase {programme.phase}
              </span>
            </div>
            <h3 className="text-xl font-bold text-neutral-900 group-hover:text-primary-600 transition-colors mb-2">
              {programme.programme_name}
            </h3>
          </div>
        </div>

        <div className="space-y-3 text-sm">
          <div>
            <span className="font-semibold text-neutral-700">Problem: </span>
            <span className="text-neutral-600">{programme.problem_addressed}</span>
          </div>

          <div>
            <span className="font-semibold text-neutral-700">Target: </span>
            <span className="text-neutral-600">{programme.target_group}</span>
          </div>

          <div>
            <span className="font-semibold text-neutral-700">Lead: </span>
            <span className="text-neutral-600">{programme.proposed_owner}</span>
          </div>
        </div>

        <div className="mt-5 pt-5 border-t border-neutral-100">
          <div className="flex items-center text-sm font-medium text-primary-600 group-hover:text-primary-700">
            View details
            <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </div>
    </Link>
  );
}
