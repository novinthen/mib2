# Participation setup — Google login, feedback form & idea board

This guide turns on the two public-participation features:

- **Share your view** (`/participate`) — a structured feedback form.
- **Idea Board** (`/ideas`) — public ideas with one-vote-per-person, shown after moderation.
- **Moderation** (`/admin`) — approve/reject ideas and read feedback.

Everything runs on **Supabase** (Postgres + Auth + Row-Level Security). Login is **Google only**. Until the environment variables below are set, these pages politely show "Coming soon" and the rest of the site works normally.

You do these steps in your own dashboards — they need your logins.

---

## 1. Create a Supabase project

1. Go to <https://supabase.com> → **New project**. Pick a name and a strong database password.
2. When it's ready, open **Project Settings → API** and copy:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **anon public** key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **service_role** key → `SUPABASE_SERVICE_ROLE_KEY` (secret — server only)

## 2. Create the database tables

1. In Supabase → **SQL Editor → New query**.
2. Paste the entire contents of [`supabase/migrations/0001_participation.sql`](supabase/migrations/0001_participation.sql) and **Run**.
3. This creates `profiles`, `feedback`, `ideas`, `idea_votes`, all Row-Level-Security policies, and the vote-count trigger.

## 3. Set up Google as the (only) login provider

**a. Google Cloud — create OAuth credentials**
1. <https://console.cloud.google.com> → create/select a project.
2. **APIs & Services → OAuth consent screen** → External → fill app name, support email, developer email. Add your domain later under *Authorized domains*.
3. **APIs & Services → Credentials → Create credentials → OAuth client ID → Web application**.
4. Under **Authorized redirect URIs** add your Supabase callback:
   `https://YOUR-PROJECT-ref.supabase.co/auth/v1/callback`
5. Copy the **Client ID** and **Client secret**.

**b. Supabase — enable Google, disable the rest**
1. Supabase → **Authentication → Providers → Google** → enable, paste Client ID + secret, **Save**.
2. Leave **Email** and every other provider **disabled** so login is Google-only.
3. **Authentication → URL Configuration**:
   - **Site URL**: your production URL (e.g. `https://novinthen.com`, or the Vercel URL for now).
   - **Redirect URLs** (add each): `http://localhost:3000/**`, your Vercel preview URL `…/**`, and your production URL `…/**`.

## 4. Add environment variables

**Local:** copy `.env.example` to `.env.local` and fill in the four values.

**Vercel:** Project → **Settings → Environment Variables** → add all four for Production (and Preview if you want it live there):

| Variable | Value | Exposed to browser? |
|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Project URL | Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | anon public key | Yes |
| `SUPABASE_SERVICE_ROLE_KEY` | service_role key | **No — secret** |
| `ADMIN_EMAILS` | your admin emails, comma-separated | No |

Redeploy after adding them.

## 5. Verify

1. Visit `/participate` and `/ideas` → click **Sign in** → Google flow → you're returned signed in (avatar in the header).
2. Submit feedback → appears in `/admin` → **Feedback inbox**.
3. Post an idea → it's **not** on `/ideas` yet (pending) → open `/admin` → **Approve** → refresh `/ideas` → it appears.
4. Upvote it → count changes; try to vote twice → the second is blocked (one vote per person).
5. Open `/admin` from a non-admin Google account → you get a 404 (correct — it's gated to `ADMIN_EMAILS`).

## How privacy works

- A contributor's **full name and email are stored only in `profiles`**, locked down by Row-Level Security.
- Public ideas show only a **display name** like "Novin T." (first name + last initial), written onto the idea at submit time.
- Feedback is **never public** — only the author and admins (service role) can read it.

## Notes

- **Pre-moderation**: new ideas are `pending` and invisible until an admin approves them.
- **Admin access** is controlled purely by `ADMIN_EMAILS`; add/remove emails and redeploy.
- The service-role key bypasses RLS — keep it only in server env vars, never `NEXT_PUBLIC_*`.
