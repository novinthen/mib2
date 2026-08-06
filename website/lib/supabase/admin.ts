import 'server-only';

import { createClient as createSupabaseClient } from '@supabase/supabase-js';
import { SUPABASE_URL } from './env';

const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY ?? '';

/** True when the server-only service role key is available. */
export const isAdminConfigured = Boolean(SUPABASE_URL && SERVICE_ROLE_KEY);

/**
 * Service-role Supabase client that BYPASSES Row-Level Security.
 * Server-only — never import this into a client component. Use exclusively for
 * moderation (reading feedback, approving/removing ideas) after an admin check.
 */
export function createAdminClient() {
  return createSupabaseClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
    auth: { autoRefreshToken: false, persistSession: false },
  });
}
