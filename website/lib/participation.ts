// Shared types + constants for the public participation features
// (feedback form + idea board).

export const PILLAR_OPTIONS = [
  'P1 Foundations',
  'P2 Progression',
  'P3 Livelihoods',
  'P4 Institutional Participation',
] as const;

export const CONTRIBUTOR_ROLES = [
  'Parent / guardian',
  'Student',
  'Educator',
  'Community / NGO',
  'Public servant',
  'Researcher',
  'Business owner',
  'Other',
] as const;

export interface Idea {
  id: string;
  author_display_name: string;
  title: string;
  description: string;
  programme_id: string | null;
  pillar: string | null;
  status: 'pending' | 'approved' | 'rejected';
  vote_count: number;
  created_at: string;
  user_id: string;
}

export interface FeedbackItem {
  id: string;
  author_display_name: string;
  programme_id: string | null;
  pillar: string | null;
  contributor_role: string | null;
  message: string;
  status: 'new' | 'reviewed';
  created_at: string;
}
