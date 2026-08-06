'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import type { User } from '@supabase/supabase-js';
import { createClient } from '@/lib/supabase/client';
import { isSupabaseConfigured } from '@/lib/supabase/env';

function GoogleMark() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 24 24" aria-hidden>
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.1a6.6 6.6 0 0 1 0-4.2V7.06H2.18a11 11 0 0 0 0 9.88l3.66-2.84z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1A11 11 0 0 0 2.18 7.06l3.66 2.84C6.71 7.3 9.14 5.38 12 5.38z"
      />
    </svg>
  );
}

export default function AuthButton() {
  const [user, setUser] = useState<User | null>(null);
  // When Supabase isn't configured we're immediately "ready" (nothing to load).
  const [ready, setReady] = useState(!isSupabaseConfigured);

  useEffect(() => {
    if (!isSupabaseConfigured) return;
    const supabase = createClient();
    supabase.auth.getUser().then(({ data }) => {
      setUser(data.user);
      setReady(true);
    });
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });
    return () => subscription.unsubscribe();
  }, []);

  const signIn = async () => {
    const supabase = createClient();
    const next = typeof window !== 'undefined' ? window.location.pathname : '/';
    await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}`,
      },
    });
  };

  // Hide entirely if the backend isn't configured yet.
  if (!isSupabaseConfigured || !ready) return null;

  if (!user) {
    return (
      <button
        onClick={signIn}
        className="inline-flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium bg-white border border-neutral-200 text-neutral-800 hover:bg-neutral-50 shadow-soft transition-colors"
      >
        <GoogleMark />
        <span className="hidden sm:inline">Sign in</span>
      </button>
    );
  }

  const avatar = (user.user_metadata?.avatar_url as string | undefined) ?? null;
  const name =
    (user.user_metadata?.full_name as string | undefined) ??
    (user.user_metadata?.name as string | undefined) ??
    user.email ??
    'Account';

  return (
    <div className="flex items-center gap-2">
      {avatar ? (
        <Image
          src={avatar}
          alt=""
          width={28}
          height={28}
          className="w-7 h-7 rounded-full border border-neutral-200"
          unoptimized
        />
      ) : (
        <span className="w-7 h-7 rounded-full bg-primary-100 text-primary-700 text-xs font-semibold flex items-center justify-center">
          {name.charAt(0).toUpperCase()}
        </span>
      )}
      <form action="/auth/signout" method="post">
        <button
          type="submit"
          className="px-3 py-1.5 rounded-lg text-sm font-medium text-neutral-600 hover:text-neutral-900 hover:bg-neutral-100 transition-colors"
        >
          Sign out
        </button>
      </form>
    </div>
  );
}
