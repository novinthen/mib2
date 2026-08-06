'use client';

import { useActionState, useState } from 'react';
import { createIdea, type IdeaSubmitState } from '@/app/ideas/actions';
import { PILLAR_OPTIONS } from '@/lib/participation';

const initialState: IdeaSubmitState = { ok: false };

export default function NewIdeaForm() {
  const [open, setOpen] = useState(false);
  const [state, formAction, pending] = useActionState(createIdea, initialState);

  if (state.ok) {
    return (
      <div className="bg-info-50 border border-info-100 text-info-900 rounded-2xl p-5 text-sm">
        ✅ Thanks — your idea was submitted and will appear on the board once it&rsquo;s reviewed.
      </div>
    );
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="px-5 py-3 bg-gradient-primary text-white font-semibold rounded-xl shadow-soft hover:shadow-soft-lg transition-all"
      >
        + Share an idea
      </button>
    );
  }

  return (
    <form action={formAction} className="bg-white rounded-2xl shadow-soft p-6 space-y-4">
      <h2 className="text-lg font-bold text-neutral-900">Share a new idea</h2>

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-neutral-700 mb-2">
          Title
        </label>
        <input
          id="title"
          name="title"
          type="text"
          required
          maxLength={140}
          placeholder="A short, clear headline for your idea"
          className="w-full px-4 py-2.5 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
      </div>

      <div>
        <label htmlFor="pillar" className="block text-sm font-medium text-neutral-700 mb-2">
          Pillar (optional)
        </label>
        <select
          id="pillar"
          name="pillar"
          defaultValue=""
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
        <label htmlFor="description" className="block text-sm font-medium text-neutral-700 mb-2">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          rows={4}
          required
          maxLength={4000}
          placeholder="Explain your idea and why it matters…"
          className="w-full px-4 py-3 bg-neutral-50 border border-neutral-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-y"
        />
      </div>

      {state.error && (
        <p className="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-4 py-3">
          {state.error}
        </p>
      )}

      <div className="flex items-center gap-3">
        <button
          type="submit"
          disabled={pending}
          className="px-6 py-3 bg-gradient-primary text-white font-semibold rounded-xl shadow-soft hover:shadow-soft-lg transition-all disabled:opacity-60"
        >
          {pending ? 'Submitting…' : 'Submit idea'}
        </button>
        <button
          type="button"
          onClick={() => setOpen(false)}
          className="px-4 py-3 text-sm font-medium text-neutral-600 hover:text-neutral-900"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}
