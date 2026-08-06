import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { toDisplayName } from '@/lib/auth';

/**
 * OAuth (PKCE) callback: exchanges the code for a session, upserts the user's
 * profile, then redirects back to where they started.
 */
export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get('code');
  const next = searchParams.get('next') ?? '/';

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);

    if (!error) {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (user) {
        const fullName =
          (user.user_metadata?.full_name as string | undefined) ??
          (user.user_metadata?.name as string | undefined) ??
          null;
        const avatarUrl = (user.user_metadata?.avatar_url as string | undefined) ?? null;

        await supabase.from('profiles').upsert(
          {
            id: user.id,
            email: user.email,
            full_name: fullName,
            avatar_url: avatarUrl,
            display_name: toDisplayName(fullName, user.email),
          },
          { onConflict: 'id' },
        );
      }

      return NextResponse.redirect(`${origin}${next}`);
    }
  }

  return NextResponse.redirect(`${origin}/?auth_error=1`);
}
