import { notFound } from 'next/navigation';
import { getUser, isAdminEmail } from '@/lib/auth';
import { createAdminClient, isAdminConfigured } from '@/lib/supabase/admin';
import { isSupabaseConfigured } from '@/lib/supabase/env';
import { IdeaModerationButtons, FeedbackReviewButton } from '@/components/AdminControls';
import type { FeedbackItem, Idea } from '@/lib/participation';

export const dynamic = 'force-dynamic';

export const metadata = {
  title: 'Moderation',
  robots: { index: false, follow: false },
};

export default async function AdminPage() {
  const user = isSupabaseConfigured ? await getUser() : null;

  // Gate: only allowlisted admins may even see this page exists.
  if (!user || !isAdminEmail(user.email)) {
    notFound();
  }

  if (!isAdminConfigured) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16">
        <div className="bg-white rounded-2xl shadow-soft p-8 text-center">
          <h1 className="text-xl font-bold text-neutral-900 mb-2">Admin not configured</h1>
          <p className="text-neutral-600">
            Set <code>SUPABASE_SERVICE_ROLE_KEY</code> to enable moderation.
          </p>
        </div>
      </div>
    );
  }

  const admin = createAdminClient();

  const [{ data: pendingRaw }, { data: allRaw }, { data: feedbackRaw }] = await Promise.all([
    admin.from('ideas').select('*').eq('status', 'pending').order('created_at', { ascending: false }),
    admin.from('ideas').select('*').order('created_at', { ascending: false }),
    admin.from('feedback').select('*').order('created_at', { ascending: false }),
  ]);

  const pending = (pendingRaw ?? []) as Idea[];
  const all = (allRaw ?? []) as Idea[];
  const feedback = (feedbackRaw ?? []) as FeedbackItem[];

  return (
    <div className="bg-neutral-50 min-h-screen">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
        <header>
          <h1 className="text-3xl font-bold text-neutral-900">Moderation</h1>
          <p className="text-neutral-600 mt-1">
            Signed in as {user.email}. Approve ideas to publish them to the public board.
          </p>
        </header>

        {/* Pending ideas */}
        <Section title={`Pending ideas (${pending.length})`}>
          {pending.length === 0 ? (
            <Empty>No ideas awaiting review.</Empty>
          ) : (
            pending.map((idea) => (
              <IdeaRow key={idea.id} idea={idea} />
            ))
          )}
        </Section>

        {/* All ideas */}
        <Section title={`All ideas (${all.length})`}>
          {all.length === 0 ? (
            <Empty>No ideas yet.</Empty>
          ) : (
            all.map((idea) => <IdeaRow key={idea.id} idea={idea} showStatus />)
          )}
        </Section>

        {/* Feedback inbox */}
        <Section title={`Feedback inbox (${feedback.length})`}>
          {feedback.length === 0 ? (
            <Empty>No feedback yet.</Empty>
          ) : (
            feedback.map((f) => (
              <div key={f.id} className="bg-white rounded-xl shadow-soft p-5">
                <div className="flex items-start justify-between gap-4 mb-2">
                  <div className="text-xs text-neutral-500">
                    <span className="font-semibold text-neutral-700">{f.author_display_name}</span>
                    {f.contributor_role ? ` · ${f.contributor_role}` : ''}
                    {f.pillar ? ` · ${f.pillar}` : ''}
                    {f.programme_id ? ` · ${f.programme_id}` : ''}
                    {' · '}
                    {new Date(f.created_at).toLocaleDateString()}
                  </div>
                  <div className="flex items-center gap-2">
                    <StatusPill status={f.status} />
                    <FeedbackReviewButton feedbackId={f.id} reviewed={f.status === 'reviewed'} />
                  </div>
                </div>
                <p className="text-sm text-neutral-800 whitespace-pre-wrap">{f.message}</p>
              </div>
            ))
          )}
        </Section>
      </div>
    </div>
  );
}

function IdeaRow({ idea, showStatus }: { idea: Idea; showStatus?: boolean }) {
  return (
    <div className="bg-white rounded-xl shadow-soft p-5">
      <div className="flex items-start justify-between gap-4 mb-2">
        <div>
          <h3 className="font-bold text-neutral-900">{idea.title}</h3>
          <div className="text-xs text-neutral-500 mt-0.5">
            by {idea.author_display_name}
            {idea.pillar ? ` · ${idea.pillar}` : ''} · {idea.vote_count} votes ·{' '}
            {new Date(idea.created_at).toLocaleDateString()}
          </div>
        </div>
        {showStatus && <StatusPill status={idea.status} />}
      </div>
      <p className="text-sm text-neutral-700 whitespace-pre-wrap mb-3">{idea.description}</p>
      <IdeaModerationButtons ideaId={idea.id} status={idea.status} />
    </div>
  );
}

function StatusPill({ status }: { status: string }) {
  const map: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-neutral-200 text-neutral-700',
    new: 'bg-yellow-100 text-yellow-800',
    reviewed: 'bg-green-100 text-green-800',
  };
  return (
    <span className={`shrink-0 text-xs font-semibold px-2.5 py-1 rounded-full ${map[status] ?? 'bg-neutral-100 text-neutral-700'}`}>
      {status}
    </span>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="text-lg font-bold text-neutral-900 mb-4">{title}</h2>
      <div className="space-y-3">{children}</div>
    </section>
  );
}

function Empty({ children }: { children: React.ReactNode }) {
  return <p className="text-sm text-neutral-500 bg-white rounded-xl p-5 shadow-soft">{children}</p>;
}
