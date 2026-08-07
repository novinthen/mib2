# MIB 2.0 — Security Review Report

**Scope:** Full security review of the `website/` Next.js 16 app (auth, RLS, server
actions, admin, secret handling, headers, dependencies). **Read-only — no application code changed.**
**Branch:** `claude/site-needs-assessment-630qy9`. **Date:** 2026-08-07.
**Reviewer method:** manual expert read of all security-relevant files + `npm audit` +
static scans for dangerous sinks, secret leakage, and client/server boundary violations.

## Summary

The app has a **genuinely solid security foundation**: Postgres Row-Level Security is
enabled on every table with least-privilege policies, the service-role key is correctly
isolated to server-only modules, auth uses `getUser()` (server-side JWT validation) rather
than trusting `getSession()`, admin actions re-check authorization on every call, and no
secrets are committed. `npm audit` reports **0 vulnerabilities**.

No Critical or High issues were found. The findings below are hardening items:
**2 Medium** (abuse/DoS surface, missing HTTP security headers) and **4 Low/Informational**.

| # | Severity | Finding | Location |
|---|----------|---------|----------|
| 1 | Medium | No rate-limiting / anti-automation on public write paths | `app/participate/actions.ts`, `app/ideas/actions.ts` |
| 2 | Medium | Missing HTTP security headers (CSP, frame-ancestors, HSTS, etc.) | `next.config.ts` / `vercel.json` |
| 3 | Low | Unvalidated `next` redirect param in OAuth callback | `app/auth/callback/route.ts:11,36` |
| 4 | Low | CSRF sign-out via unauthenticated cross-site POST | `app/auth/signout/route.ts` |
| 5 | Low | `programme_id` / `pillar` accepted as unvalidated free text | `app/participate/actions.ts`, `app/ideas/actions.ts` |
| 6 | Info | Optimistic-vote race (integrity protected by PK) | `app/ideas/actions.ts:toggleVote` |

---

## Findings

### 1. (Medium) No rate-limiting or anti-automation on public write paths
`submitFeedback`, `createIdea`, and `toggleVote` gate on a signed-in Google user but
impose no per-user or per-IP throttle, and there is no CAPTCHA. A single authenticated
user — or a pool of free Google accounts — can flood the `feedback` and `ideas` tables and
the moderation queue, and drive unbounded database growth. The sign-in wall the UI advertises
as keeping things "spam-free" is weak on its own. Ideas are pre-moderated so **the public
board is protected from spam display**, which contains the blast radius, but the admin inbox
and storage are not.
*Recommendation:* add a lightweight per-user rate limit (e.g. N submissions / hour) in the
server actions, or Supabase-side (a `created_at` count check / policy), and consider
Turnstile/hCaptcha on the forms.

### 2. (Medium) Missing HTTP security headers
No `Content-Security-Policy`, `X-Frame-Options` / `frame-ancestors`, `Strict-Transport-Security`,
`X-Content-Type-Options`, or `Referrer-Policy` is set (`next.config.ts` defines only image
`remotePatterns`; `vercel.json` sets none). Consequences: the sensitive `/admin` and
`/participate` pages are framable (clickjacking), and there is no CSP to contain any future
XSS. React's auto-escaping and the absence of `dangerouslySetInnerHTML`/`innerHTML` keep
current XSS risk low, so this is defense-in-depth.
*Recommendation:* add a `headers()` block in `next.config.ts` — at minimum
`X-Frame-Options: DENY` (or CSP `frame-ancestors 'none'`), `X-Content-Type-Options: nosniff`,
`Referrer-Policy: strict-origin-when-cross-origin`, HSTS, and a starter CSP.

### 3. (Low) Unvalidated `next` redirect parameter in OAuth callback
`app/auth/callback/route.ts` reads `next` from the query string and redirects to
`` `${origin}${next}` `` without validating it. In practice the leading-`origin`
concatenation neutralizes the usual open-redirect vectors (protocol-relative `//evil.com`
resolves to a *path* on the origin; scheme injection produces an invalid URL), and the
redirect only fires after a valid PKCE code exchange — so this is **latent, not clearly
exploitable**. Still worth fixing.
*Recommendation:* accept `next` only when it matches `^/(?!/)` (a single-slash-relative path);
otherwise fall back to `/`.

### 4. (Low) CSRF sign-out
`POST /auth/signout` is a plain route handler with no CSRF token or Origin check, so a
cross-site auto-submitting form can force-sign-out a logged-in user. Impact is limited to
nuisance (no data disclosure or state corruption).
*Recommendation:* verify the request `Origin`/`Sec-Fetch-Site`, or route sign-out through a
server action (which carries Next.js's built-in CSRF protection).

### 5. (Low) Unvalidated `programme_id` / `pillar` free text
Both write actions store `programme_id` and `pillar` as arbitrary trimmed strings without
checking them against the known `PILLAR_OPTIONS` / real programme IDs. RLS scopes the rows and
React escapes them on render, so security impact is minimal — this is mainly data-integrity
hygiene.
*Recommendation:* validate `pillar` against `PILLAR_OPTIONS` and `programme_id` against loaded
programmes; reject or null out unknown values.

### 6. (Info) Optimistic-vote race
`toggleVote` does a check-then-insert that can race under concurrent clicks, but the
`idea_votes` composite primary key `(idea_id, user_id)` guarantees one vote per user; a lost
race simply surfaces "Could not record your vote." No integrity issue.

---

## Verified strengths (no action needed)

- **RLS on every table** (`supabase/migrations/0001_participation.sql`) with least privilege:
  feedback/profiles readable only by their owner; ideas readable only when `approved` or own;
  inserts forced to `auth.uid()` and (ideas) `status='pending'`; votes allowed only on
  `approved` ideas; no user-facing UPDATE/DELETE on ideas (moderation is service-role only).
- **Service-role key isolation:** `lib/supabase/admin.ts` is `import 'server-only'`, keyed off
  a non-`NEXT_PUBLIC` env var, and imported *only* by `app/admin/page.tsx` and
  `app/admin/actions.ts`. Scan confirmed **no client component imports** it.
- **Admin authorization** is enforced server-side on the page (`notFound()` for non-admins)
  **and** re-checked in every admin action via `assertAdmin()` — not just hidden in the UI.
- **Auth correctness:** `getUser()` calls `supabase.auth.getUser()` (validates the JWT with
  Supabase) rather than trusting an unverified session.
- **Secret hygiene:** `.env*` is gitignored; no service-role key or JWT is committed
  (`.env.example` holds only placeholders); the anon key is public by design.
- **`security definer` trigger** `sync_idea_vote_count` pins `search_path = public`.
- **Input length caps** enforced in both the DB (`char_length` checks) and the server actions;
  React auto-escaping throughout; no `dangerouslySetInnerHTML`, `eval`, `innerHTML`, or
  `child_process` anywhere in the app.
- **`npm audit`: 0 vulnerabilities.**

## How this review was validated
Every finding was traced to specific file:line evidence and a concrete failure scenario;
boundary claims (service-role isolation, client/server leaks) were confirmed by repo-wide
ripgrep scans; dependency risk via `npm audit`. No runtime exploitation was performed
(read-only engagement).
