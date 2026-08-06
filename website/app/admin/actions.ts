'use server';

import { revalidatePath } from 'next/cache';
import { getUser, isAdminEmail } from '@/lib/auth';
import { createAdminClient, isAdminConfigured } from '@/lib/supabase/admin';

async function assertAdmin() {
  const user = await getUser();
  if (!user || !isAdminEmail(user.email)) {
    throw new Error('Not authorised');
  }
  if (!isAdminConfigured) {
    throw new Error('Service role key not configured');
  }
}

export async function setIdeaStatus(ideaId: string, status: 'approved' | 'rejected' | 'pending') {
  await assertAdmin();
  const admin = createAdminClient();
  await admin.from('ideas').update({ status }).eq('id', ideaId);
  revalidatePath('/admin');
  revalidatePath('/ideas');
}

export async function deleteIdea(ideaId: string) {
  await assertAdmin();
  const admin = createAdminClient();
  await admin.from('ideas').delete().eq('id', ideaId);
  revalidatePath('/admin');
  revalidatePath('/ideas');
}

export async function markFeedbackReviewed(feedbackId: string, reviewed: boolean) {
  await assertAdmin();
  const admin = createAdminClient();
  await admin
    .from('feedback')
    .update({ status: reviewed ? 'reviewed' : 'new' })
    .eq('id', feedbackId);
  revalidatePath('/admin');
}
