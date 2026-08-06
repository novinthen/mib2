'use client';

import { useTransition } from 'react';
import { deleteIdea, markFeedbackReviewed, setIdeaStatus } from '@/app/admin/actions';

function btn(kind: 'approve' | 'reject' | 'delete' | 'neutral') {
  const base = 'px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors disabled:opacity-50';
  const map = {
    approve: 'bg-green-600 text-white hover:bg-green-700',
    reject: 'bg-neutral-200 text-neutral-800 hover:bg-neutral-300',
    delete: 'bg-red-600 text-white hover:bg-red-700',
    neutral: 'bg-primary-600 text-white hover:bg-primary-700',
  };
  return `${base} ${map[kind]}`;
}

export function IdeaModerationButtons({
  ideaId,
  status,
}: {
  ideaId: string;
  status: 'pending' | 'approved' | 'rejected';
}) {
  const [pending, start] = useTransition();
  return (
    <div className="flex flex-wrap gap-2">
      {status !== 'approved' && (
        <button
          disabled={pending}
          onClick={() => start(() => setIdeaStatus(ideaId, 'approved'))}
          className={btn('approve')}
        >
          Approve
        </button>
      )}
      {status !== 'rejected' && (
        <button
          disabled={pending}
          onClick={() => start(() => setIdeaStatus(ideaId, 'rejected'))}
          className={btn('reject')}
        >
          Reject
        </button>
      )}
      {status === 'rejected' && (
        <button
          disabled={pending}
          onClick={() => start(() => setIdeaStatus(ideaId, 'pending'))}
          className={btn('neutral')}
        >
          Restore to pending
        </button>
      )}
      <button
        disabled={pending}
        onClick={() => {
          if (confirm('Permanently delete this idea?')) start(() => deleteIdea(ideaId));
        }}
        className={btn('delete')}
      >
        Delete
      </button>
    </div>
  );
}

export function FeedbackReviewButton({
  feedbackId,
  reviewed,
}: {
  feedbackId: string;
  reviewed: boolean;
}) {
  const [pending, start] = useTransition();
  return (
    <button
      disabled={pending}
      onClick={() => start(() => markFeedbackReviewed(feedbackId, !reviewed))}
      className={btn(reviewed ? 'reject' : 'neutral')}
    >
      {reviewed ? 'Mark as new' : 'Mark reviewed'}
    </button>
  );
}
