'use server';

import { revalidatePath } from 'next/cache';
import { createClient } from '@/lib/supabase/server';
import { getUser, toDisplayName } from '@/lib/auth';

export type IdeaSubmitState = { ok: boolean; error?: string };

export async function createIdea(
  _prev: IdeaSubmitState,
  formData: FormData,
): Promise<IdeaSubmitState> {
  const user = await getUser();
  if (!user) return { ok: false, error: 'Please sign in with Google first.' };

  const title = String(formData.get('title') ?? '').trim();
  const description = String(formData.get('description') ?? '').trim();
  if (title.length < 3 || title.length > 140) {
    return { ok: false, error: 'Title must be between 3 and 140 characters.' };
  }
  if (description.length < 3 || description.length > 4000) {
    return { ok: false, error: 'Please describe your idea (3–4000 characters).' };
  }

  const pillar = String(formData.get('pillar') ?? '').trim() || null;
  const fullName =
    (user.user_metadata?.full_name as string | undefined) ??
    (user.user_metadata?.name as string | undefined) ??
    null;

  const supabase = await createClient();
  const { error } = await supabase.from('ideas').insert({
    user_id: user.id,
    author_display_name: toDisplayName(fullName, user.email),
    title,
    description,
    pillar,
    status: 'pending',
  });

  if (error) {
    return { ok: false, error: 'Could not save your idea. Please try again.' };
  }

  revalidatePath('/ideas');
  return { ok: true };
}

export type VoteResult = { ok: boolean; error?: string; voted?: boolean };

/** Toggle the current user's vote on an approved idea. */
export async function toggleVote(ideaId: string): Promise<VoteResult> {
  const user = await getUser();
  if (!user) return { ok: false, error: 'Sign in to vote.' };

  const supabase = await createClient();

  const { data: existing } = await supabase
    .from('idea_votes')
    .select('idea_id')
    .eq('idea_id', ideaId)
    .eq('user_id', user.id)
    .maybeSingle();

  if (existing) {
    const { error } = await supabase
      .from('idea_votes')
      .delete()
      .eq('idea_id', ideaId)
      .eq('user_id', user.id);
    if (error) return { ok: false, error: 'Could not remove your vote.' };
    revalidatePath('/ideas');
    return { ok: true, voted: false };
  }

  const { error } = await supabase
    .from('idea_votes')
    .insert({ idea_id: ideaId, user_id: user.id });
  if (error) return { ok: false, error: 'Could not record your vote.' };
  revalidatePath('/ideas');
  return { ok: true, voted: true };
}
