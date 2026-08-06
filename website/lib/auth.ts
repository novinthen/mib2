import 'server-only';

import type { User } from '@supabase/supabase-js';
import { createClient } from './supabase/server';
import { isSupabaseConfigured } from './supabase/env';

/** The signed-in Supabase user, or null. */
export async function getUser(): Promise<User | null> {
  if (!isSupabaseConfigured) return null;
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  return user;
}

/** Comma-separated allowlist of admin emails (server env). */
function adminEmails(): string[] {
  return (process.env.ADMIN_EMAILS ?? '')
    .split(',')
    .map((e) => e.trim().toLowerCase())
    .filter(Boolean);
}

export function isAdminEmail(email: string | null | undefined): boolean {
  if (!email) return false;
  return adminEmails().includes(email.toLowerCase());
}

/**
 * Build a public-safe display name: "First L." from a full name, falling back
 * to the email local-part. Keeps full name / email private.
 */
export function toDisplayName(fullName?: string | null, email?: string | null): string {
  const name = (fullName ?? '').trim();
  if (name) {
    const parts = name.split(/\s+/);
    const first = parts[0];
    const lastInitial = parts.length > 1 ? ` ${parts[parts.length - 1][0].toUpperCase()}.` : '';
    return `${first}${lastInitial}`;
  }
  const local = (email ?? '').split('@')[0];
  return local || 'Contributor';
}
