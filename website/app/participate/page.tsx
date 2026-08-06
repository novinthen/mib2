import Link from 'next/link';
import FeedbackForm from '@/components/FeedbackForm';
import AuthButton from '@/components/AuthButton';
import { getUser } from '@/lib/auth';
import { isSupabaseConfigured } from '@/lib/supabase/env';
import { loadProgrammes } from '@/lib/data-loader';

export const metadata = {
  title: 'Share your view',
  description: 'Send your suggestions and ideas on the Malaysian Indian Blueprint 2.0.',
};

export default async function ParticipatePage({
  searchParams,
}: {
  searchParams: Promise<{ programme?: string; pillar?: string }>;
}) {
  const { programme, pillar } = await searchParams;

  let programmeName: string | undefined;
  let programmePillar: string | undefined;
  if (programme) {
    const match = loadProgrammes().find((p) => p.programme_id === programme);
    programmeName = match?.programme_name;
    programmePillar = match?.pillar;
  }

  const user = isSupabaseConfigured ? await getUser() : null;

  return (
    <div className="bg-neutral-50 min-h-screen">
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-700 via-primary-600 to-primary-800 text-white py-14 px-4 sm:px-6 lg:px-8">
        <div className="absolute inset-0 bg-gradient-to-br from-transparent via-white/5 to-white/10" />
        <div className="relative max-w-3xl mx-auto">
          <h1 className="text-3xl sm:text-4xl font-bold mb-3">Share your view</h1>
          <p className="text-lg text-white/80">
            Your suggestions help shape the Malaysian Indian Blueprint 2.0. Tell us what to
            improve — for the whole plan or a specific programme.
          </p>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {programmeName && (
          <div className="mb-6 text-sm bg-primary-50 text-primary-800 border border-primary-100 rounded-xl px-4 py-3">
            You&rsquo;re commenting on{' '}
            <Link href={`/programmes/${programme}`} className="font-semibold underline">
              {programmeName}
            </Link>
            .
          </div>
        )}

        {!isSupabaseConfigured ? (
          <NotConfigured />
        ) : !user ? (
          <SignInCard />
        ) : (
          <FeedbackForm
            initialProgramme={programme}
            initialPillar={pillar ?? programmePillar}
          />
        )}
      </div>
    </div>
  );
}

function SignInCard() {
  return (
    <div className="bg-white rounded-2xl shadow-soft p-8 text-center space-y-4">
      <div className="text-4xl">🔐</div>
      <h2 className="text-xl font-bold text-neutral-900">Sign in to contribute</h2>
      <p className="text-neutral-600 max-w-md mx-auto">
        We ask everyone to sign in with Google before submitting. This keeps contributions
        genuine and spam-free. Your name and email stay private.
      </p>
      <div className="flex justify-center pt-2">
        <AuthButton />
      </div>
    </div>
  );
}

function NotConfigured() {
  return (
    <div className="bg-white rounded-2xl shadow-soft p-8 text-center space-y-3">
      <div className="text-4xl">🛠️</div>
      <h2 className="text-xl font-bold text-neutral-900">Coming soon</h2>
      <p className="text-neutral-600 max-w-md mx-auto">
        Public contributions are being set up and will open shortly.
      </p>
    </div>
  );
}
