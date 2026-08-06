-- ============================================================================
-- MIB 2.0 — Public participation schema
-- Feedback form (Option 1) + Idea board with voting (Option 2)
-- Run this in the Supabase SQL editor (or via the Supabase CLI).
-- ============================================================================

-- ----------------------------------------------------------------------------
-- profiles: private PII for each signed-in user. Public reads never touch this;
-- ideas/feedback carry a denormalised `author_display_name` instead.
-- ----------------------------------------------------------------------------
create table if not exists public.profiles (
  id           uuid primary key references auth.users (id) on delete cascade,
  email        text,
  full_name    text,
  avatar_url   text,
  display_name text,
  created_at   timestamptz not null default now()
);

alter table public.profiles enable row level security;

drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own" on public.profiles
  for select using (auth.uid() = id);

drop policy if exists "profiles_upsert_own" on public.profiles;
create policy "profiles_upsert_own" on public.profiles
  for insert with check (auth.uid() = id);

drop policy if exists "profiles_update_own" on public.profiles;
create policy "profiles_update_own" on public.profiles
  for update using (auth.uid() = id) with check (auth.uid() = id);

-- ----------------------------------------------------------------------------
-- feedback (Option 1): private input. Only the author can read their own rows;
-- moderation happens via the service role (admin page).
-- ----------------------------------------------------------------------------
create table if not exists public.feedback (
  id                   uuid primary key default gen_random_uuid(),
  user_id              uuid not null references auth.users (id) on delete cascade,
  author_display_name  text not null,
  programme_id         text,
  pillar               text,
  contributor_role     text,
  message              text not null check (char_length(message) between 3 and 4000),
  status               text not null default 'new' check (status in ('new', 'reviewed')),
  created_at           timestamptz not null default now()
);

alter table public.feedback enable row level security;

drop policy if exists "feedback_insert_own" on public.feedback;
create policy "feedback_insert_own" on public.feedback
  for insert with check (auth.uid() = user_id);

drop policy if exists "feedback_select_own" on public.feedback;
create policy "feedback_select_own" on public.feedback
  for select using (auth.uid() = user_id);

-- ----------------------------------------------------------------------------
-- ideas (Option 2): pre-moderated. Public sees only 'approved'; authors also
-- see their own pending rows. vote_count is kept in sync by a trigger.
-- ----------------------------------------------------------------------------
create table if not exists public.ideas (
  id                   uuid primary key default gen_random_uuid(),
  user_id              uuid not null references auth.users (id) on delete cascade,
  author_display_name  text not null,
  title                text not null check (char_length(title) between 3 and 140),
  description          text not null check (char_length(description) between 3 and 4000),
  programme_id         text,
  pillar               text,
  status               text not null default 'pending'
                         check (status in ('pending', 'approved', 'rejected')),
  vote_count           integer not null default 0,
  created_at           timestamptz not null default now()
);

create index if not exists ideas_status_votes_idx
  on public.ideas (status, vote_count desc, created_at desc);

alter table public.ideas enable row level security;

-- Public + authors: read approved, or your own (any status).
drop policy if exists "ideas_select_approved_or_own" on public.ideas;
create policy "ideas_select_approved_or_own" on public.ideas
  for select using (status = 'approved' or auth.uid() = user_id);

-- Insert only your own rows, and only as 'pending' (moderation gate).
drop policy if exists "ideas_insert_own_pending" on public.ideas;
create policy "ideas_insert_own_pending" on public.ideas
  for insert with check (auth.uid() = user_id and status = 'pending');

-- ----------------------------------------------------------------------------
-- idea_votes: one row per (idea, user) => one vote per person per idea.
-- ----------------------------------------------------------------------------
create table if not exists public.idea_votes (
  idea_id    uuid not null references public.ideas (id) on delete cascade,
  user_id    uuid not null references auth.users (id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (idea_id, user_id)
);

alter table public.idea_votes enable row level security;

-- Only allow voting on approved ideas.
drop policy if exists "idea_votes_insert_own_approved" on public.idea_votes;
create policy "idea_votes_insert_own_approved" on public.idea_votes
  for insert with check (
    auth.uid() = user_id
    and exists (
      select 1 from public.ideas i
      where i.id = idea_id and i.status = 'approved'
    )
  );

drop policy if exists "idea_votes_delete_own" on public.idea_votes;
create policy "idea_votes_delete_own" on public.idea_votes
  for delete using (auth.uid() = user_id);

drop policy if exists "idea_votes_select_own" on public.idea_votes;
create policy "idea_votes_select_own" on public.idea_votes
  for select using (auth.uid() = user_id);

-- ----------------------------------------------------------------------------
-- Trigger: keep ideas.vote_count in sync with idea_votes.
-- ----------------------------------------------------------------------------
create or replace function public.sync_idea_vote_count()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if (tg_op = 'INSERT') then
    update public.ideas set vote_count = vote_count + 1 where id = new.idea_id;
    return new;
  elsif (tg_op = 'DELETE') then
    update public.ideas set vote_count = greatest(vote_count - 1, 0) where id = old.idea_id;
    return old;
  end if;
  return null;
end;
$$;

drop trigger if exists trg_sync_idea_vote_count on public.idea_votes;
create trigger trg_sync_idea_vote_count
  after insert or delete on public.idea_votes
  for each row execute function public.sync_idea_vote_count();
