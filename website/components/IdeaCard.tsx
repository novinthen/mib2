'use client';

import { useState, useTransition } from 'react';
import { toggleVote } from '@/app/ideas/actions';
import type { Idea } from '@/lib/participation';

const PILLAR_CHIP: Record<string, string> = {
  'P1 Foundations': 'bg-primary-50 text-primary-700 border-primary-200',
  'P2 Progression': 'bg-info-50 text-info-700 border-info-200',
  'P3 Livelihoods': 'bg-accent-50 text-accent-700 border-accent-200',
  'P4 Institutional Participation': 'bg-purple-50 text-purple-700 border-purple-200',
};

export default function IdeaCard({
  idea,
  initialVoted,
  canVote,
}: {
  idea: Idea;
  initialVoted: boolean;
  canVote: boolean;
}) {
  const [voted, setVoted] = useState(initialVoted);
  const [count, setCount] = useState(idea.vote_count);
  const [pending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  const onVote = () => {
    if (!canVote) {
      setError('Sign in to vote.');
      return;
    }
    // Optimistic update.
    const nextVoted = !voted;
    setVoted(nextVoted);
    setCount((c) => c + (nextVoted ? 1 : -1));
    setError(null);

    startTransition(async () => {
      const res = await toggleVote(idea.id);
      if (!res.ok) {
        // Roll back.
        setVoted(!nextVoted);
        setCount((c) => c + (nextVoted ? -1 : 1));
        setError(res.error ?? 'Something went wrong.');
      } else if (typeof res.voted === 'boolean') {
        setVoted(res.voted);
      }
    });
  };

  const chip = idea.pillar ? PILLAR_CHIP[idea.pillar] : null;

  return (
    <div className="bg-white rounded-2xl shadow-soft hover:shadow-soft-lg transition-all p-6 flex gap-4">
      <div className="shrink-0">
        <button
          onClick={onVote}
          disabled={pending}
          aria-pressed={voted}
          aria-label={voted ? 'Remove your vote' : 'Upvote this idea'}
          className={`w-14 flex flex-col items-center justify-center py-2 rounded-xl border transition-colors disabled:opacity-60 ${
            voted
              ? 'bg-primary-600 border-primary-600 text-white'
              : 'bg-neutral-50 border-neutral-200 text-neutral-700 hover:border-primary-300 hover:text-primary-600'
          }`}
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
          </svg>
          <span className="text-sm font-bold tabular-nums mt-0.5">{count}</span>
        </button>
      </div>

      <div className="min-w-0 flex-grow">
        <div className="flex flex-wrap items-center gap-2 mb-2">
          {chip && (
            <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-lg border ${chip}`}>
              {idea.pillar}
            </span>
          )}
          <span className="text-xs text-neutral-400">by {idea.author_display_name}</span>
        </div>
        <h3 className="text-lg font-bold text-neutral-900 mb-1">{idea.title}</h3>
        <p className="text-sm text-neutral-600 whitespace-pre-wrap">{idea.description}</p>
        {error && <p className="mt-2 text-xs text-red-600">{error}</p>}
      </div>
    </div>
  );
}
