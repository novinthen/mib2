'use client';

import { useActionState } from 'react';
import { submitFeedback, type SubmitState } from '@/app/participate/actions';
import { CONTRIBUTOR_ROLES, PILLAR_OPTIONS } from '@/lib/participation';

const initialState: SubmitState = { ok: false };

export default function FeedbackForm({
  initialProgramme,
  initialPillar,
}: {
  initialProgramme?: string;
  initialPillar?: string;
}) {
  const [state, formAction, pending] = useActionState(submitFeedback, initialState);

  if (state.ok) {
    return (
      <div className="bg-white rounded-2xl shadow-soft p-8 text-center">
        <div className="text-4xl mb-3">🙏</div>
        <h2 className="text-xl font-bold text-neutral-900 mb-2">Thank you</h2>
        <p className="text-neutral-600">
          Your suggestion has been received. The team reviews every submission.
        </p>
      </div>
    );
  }

  return (
    <form action={formAction} className="bg-white rounded-2xl shadow-soft p-6 sm:p-8 space-y-5">
      {initialProgramme && <input type="hidden" name="programme_id" value={initialProgramme} />}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label htmlFor="pillar" className="block text-sm font-medium text-neutral-700 mb-2">
            Pillar (optional)
          </label>
          <select
            id="pillar"
            name="pillar"
            defaultValue={initialPillar ?? ''}
            className="w-full px-4 py-2.5 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">— Select a pillar —</option>
            {PILLAR_OPTIONS.map((p) => (
              <option key={p} value={p}>
                {p}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="contributor_role" className="block text-sm font-medium text-neutral-700 mb-2">
            You are a… (optional)
          </label>
          <select
            id="contributor_role"
            name="contributor_role"
            defaultValue=""
            className="w-full px-4 py-2.5 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">— Select —</option>
            {CONTRIBUTOR_ROLES.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium text-neutral-700 mb-2">
          Your suggestion
        </label>
        <textarea
          id="message"
          name="message"
          rows={6}
          required
          maxLength={4000}
          placeholder="Share your idea, concern, or improvement for this plan…"
          className="w-full px-4 py-3 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-y"
        />
      </div>

      {state.error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-4 py-3">
          {state.error}
        </p>
      )}

      <div className="flex items-center justify-between gap-4">
        <p className="text-xs text-neutral-500">
          Your name and email are kept private. Only a short display name (e.g. “Novin T.”)
          is visible to the review team.
        </p>
        <button
          type="submit"
          disabled={pending}
          className="shrink-0 px-6 py-3 bg-gradient-primary text-white font-semibold rounded-xl shadow-soft hover:shadow-soft-lg transition-all disabled:opacity-60"
        >
          {pending ? 'Sending…' : 'Submit'}
        </button>
      </div>
    </form>
  );
}
