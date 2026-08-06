import Link from 'next/link';
import IdeaCard from '@/components/IdeaCard';
import NewIdeaForm from '@/components/NewIdeaForm';
import AuthButton from '@/components/AuthButton';
import { getUser } from '@/lib/auth';
import { createClient } from '@/lib/supabase/server';
import { isSupabaseConfigured } from '@/lib/supabase/env';
import { PILLAR_OPTIONS, type Idea } from '@/lib/participation';

export const dynamic = 'force-dynamic';

export const metadata = {
  title: 'Idea Board',
  description: 'Public ideas for the Malaysian Indian Blueprint 2.0 — vote for what matters.',
};

export default async function IdeasPage({
  searchParams,
}: {
  searchParams: Promise<{ pillar?: string }>;
}) {
  const { pillar } = await searchParams;

  return (
    <div className="bg-neutral-50 min-h-screen">
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-700 via-primary-600 to-primary-800 text-white py-14 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white/5 to-white/10" />
        <div className="relative max-w-4xl mx-auto">
          <h1 className="text-3xl sm:text-4xl font-bold mb-3">Idea Board</h1>
          <p className="text-lg text-white/80">
            Ideas from the public for the Malaysian Indian Blueprint 2.0. Vote for the ones that
            matter to you — the most-supported ideas rise to the top.
          </p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {!isSupabaseConfigured ? <NotConfigured /> : <IdeasContent pillar={pillar} />}
      </div>
    </div>
  );
}

async function IdeasContent({ pillar }: { pillar?: string }) {
  const user = await getUser();
  const supabase = await createClient();

  let query = supabase
    .from('ideas')
    .select('*')
    .eq('status', 'approved')
    .order('vote_count', { ascending: false })
    .order('created_at', { ascending: false });

  if (pillar && (PILLAR_OPTIONS as readonly string[]).includes(pillar)) {
    query = query.eq('pillar', pillar);
  }

  const { data: ideas } = await query;
  const list = (ideas ?? []) as Idea[];

  // Which of these has the current user already voted for?
  let votedIds = new Set<string>();
  if (user && list.length > 0) {
    const { data: votes } = await supabase
      .from('idea_votes')
      .select('idea_id')
      .eq('user_id', user.id)
      .in(
        'idea_id',
        list.map((i) => i.id),
      );
    votedIds = new Set((votes ?? []).map((v) => v.idea_id as string));
  }

  return (
    <div className="space-y-6">
      {/* Actions row */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <PillarFilter active={pillar} />
        {user ? (
          <NewIdeaForm />
        ) : (
          <div className="flex items-center gap-3 text-sm text-neutral-600">
            <span className="hidden sm:inline">Sign in to add or vote:</span>
            <AuthButton />
          </div>
        )}
      </div>

      {list.length === 0 ? (
        <div className="bg-white rounded-2xl shadow-soft p-12 text-center">
          <div className="text-4xl mb-3">💡</div>
          <h3 className="text-lg font-semibold text-neutral-900 mb-1">No ideas yet</h3>
          <p className="text-neutral-600">Be the first to share one.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {list.map((idea) => (
            <IdeaCard
              key={idea.id}
              idea={idea}
              initialVoted={votedIds.has(idea.id)}
              canVote={Boolean(user)}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function PillarFilter({ active }: { active?: string }) {
  const base =
    'px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors';
  const on = 'bg-primary-600 border-primary-600 text-white';
  const off = 'bg-white border-neutral-200 text-neutral-600 hover:border-primary-300';
  return (
    <div className="flex flex-wrap gap-2">
      <Link href="/ideas" className={`${base} ${!active ? on : off}`}>
        All
      </Link>
      {PILLAR_OPTIONS.map((p) => (
        <Link
          key={p}
          href={`/ideas?pillar=${encodeURIComponent(p)}`}
          className={`${base} ${active === p ? on : off}`}
        >
          {p.replace(/^P\d\s/, '')}
        </Link>
      ))}
    </div>
  );
}

function NotConfigured() {
  return (
    <div className="bg-white rounded-2xl shadow-soft p-8 text-center space-y-3">
      <div className="text-4xl">🛠️</div>
      <h2 className="text-xl font-bold text-neutral-900">Coming soon</h2>
      <p className="text-neutral-600 max-w-md mx-auto">
        The public idea board is being set up and will open shortly.
      </p>
    </div>
  );
}
