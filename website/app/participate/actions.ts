'use server';

import { createClient } from '@/lib/supabase/server';
import { getUser, toDisplayName } from '@/lib/auth';

export type SubmitState = { ok: boolean; error?: string };

export async function submitFeedback(
  _prev: SubmitState,
  formData: FormData,
): Promise<SubmitState> {
  const user = await getUser();
  if (!user) {
    return { ok: false, error: 'Please sign in with Google before submitting.' };
  }

  const message = String(formData.get('message') ?? '').trim();
  if (message.length < 3) {
    return { ok: false, error: 'Please enter your suggestion (at least a few words).' };
  }
  if (message.length > 4000) {
    return { ok: false, error: 'Please keep your message under 4000 characters.' };
  }

  const programmeId = String(formData.get('programme_id') ?? '').trim() || null;
  const pillar = String(formData.get('pillar') ?? '').trim() || null;
  const role = String(formData.get('contributor_role') ?? '').trim() || null;

  const fullName =
    (user.user_metadata?.full_name as string | undefined) ??
    (user.user_metadata?.name as string | undefined) ??
    null;

  const supabase = await createClient();
  const { error } = await supabase.from('feedback').insert({
    user_id: user.id,
    author_display_name: toDisplayName(fullName, user.email),
    programme_id: programmeId,
    pillar,
    contributor_role: role,
    message,
  });

  if (error) {
    return { ok: false, error: 'Something went wrong saving your feedback. Please try again.' };
  }

  return { ok: true };
}
