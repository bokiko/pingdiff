import { createClient, SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

// Create client only if credentials are available
export const supabase: SupabaseClient = supabaseUrl && supabaseAnonKey
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null as unknown as SupabaseClient;

// Types for our database
export interface Game {
  id: string;
  name: string;
  slug: string;
  icon_url: string | null;
  is_active: boolean;
  created_at: string;
}

export interface GameServer {
  id: string;
  game_id: string;
  region: string;
  location: string;
  ip_address: string;
  port: number | null;
  is_active: boolean;
  created_at: string;
}

export interface TestResult {
  id: string;
  user_id: string | null;
  game_id: string;
  server_id: string;
  ping_avg: number;
  ping_min: number | null;
  ping_max: number | null;
  jitter: number | null;
  packet_loss: number;
  isp: string | null;
  country: string | null;
  city: string | null;
  ip_hash: string | null;
  client_version: string | null;
  created_at: string;
  raw_data: Record<string, unknown> | null;
}

export interface Profile {
  id: string;
  username: string | null;
  display_name: string | null;
  avatar_url: string | null;
  country: string | null;
  isp: string | null;
  favorite_game_id: string | null;
  is_public: boolean;
  created_at: string;
  updated_at: string;
}

export interface Tip {
  id: string;
  user_id: string;
  game_id: string;
  server_id: string | null;
  isp: string | null;
  region: string | null;
  title: string;
  content: string;
  upvotes: number;
  created_at: string;
  updated_at: string;
}
