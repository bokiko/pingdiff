-- PingDiff Database Schema
-- Multi-game ready architecture

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Games table (expandable for multiple games)
CREATE TABLE games (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    icon_url TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Game servers table
CREATE TABLE game_servers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
    region TEXT NOT NULL, -- 'EU', 'NA', 'ASIA'
    location TEXT NOT NULL, -- 'Amsterdam', 'Chicago', etc.
    ip_address TEXT NOT NULL,
    port INTEGER,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User profiles (extends Supabase auth.users)
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    display_name TEXT,
    avatar_url TEXT,
    country TEXT,
    isp TEXT,
    favorite_game_id UUID REFERENCES games(id),
    is_public BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Test results
CREATE TABLE test_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    game_id UUID NOT NULL REFERENCES games(id),
    server_id UUID NOT NULL REFERENCES game_servers(id),
    ping_avg FLOAT NOT NULL,
    ping_min FLOAT,
    ping_max FLOAT,
    jitter FLOAT,
    packet_loss FLOAT DEFAULT 0, -- percentage
    isp TEXT,
    country TEXT,
    city TEXT,
    ip_hash TEXT, -- hashed for privacy
    client_version TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    raw_data JSONB -- full ping results for detailed analysis
);

-- Community tips
CREATE TABLE tips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    game_id UUID NOT NULL REFERENCES games(id),
    server_id UUID REFERENCES game_servers(id),
    isp TEXT,
    region TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    upvotes INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Comments on tips
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tip_id UUID NOT NULL REFERENCES tips(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tip votes (prevent double voting)
CREATE TABLE tip_votes (
    tip_id UUID NOT NULL REFERENCES tips(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    vote INTEGER NOT NULL CHECK (vote IN (-1, 1)),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (tip_id, user_id)
);

-- Indexes for performance
CREATE INDEX idx_test_results_user ON test_results(user_id);
CREATE INDEX idx_test_results_game ON test_results(game_id);
CREATE INDEX idx_test_results_server ON test_results(server_id);
CREATE INDEX idx_test_results_created ON test_results(created_at DESC);
CREATE INDEX idx_test_results_isp ON test_results(isp);
CREATE INDEX idx_tips_game ON tips(game_id);
CREATE INDEX idx_tips_isp ON tips(isp);
CREATE INDEX idx_game_servers_game ON game_servers(game_id);

-- Insert initial games
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('Overwatch 2', 'overwatch-2', '/icons/overwatch2.png', true),
    ('Valorant', 'valorant', '/icons/valorant.png', false),
    ('Counter-Strike 2', 'cs2', '/icons/cs2.png', false),
    ('Apex Legends', 'apex-legends', '/icons/apex.png', false);

-- Insert Overwatch 2 servers (these are approximate/known ranges)
INSERT INTO game_servers (game_id, region, location, ip_address, port, is_active)
SELECT
    g.id,
    s.region,
    s.location,
    s.ip_address,
    s.port,
    true
FROM games g
CROSS JOIN (VALUES
    ('NA', 'Los Angeles (US West)', '24.105.30.129', 26503),
    ('NA', 'Chicago (US Central)', '24.105.62.129', 26503),
    ('NA', 'New York (US East)', '24.105.94.129', 26503),
    ('EU', 'Amsterdam', '185.60.112.157', 26503),
    ('EU', 'Paris', '185.60.114.159', 26503),
    ('ASIA', 'Singapore', '137.221.106.104', 26503),
    ('ASIA', 'Seoul', '117.52.35.100', 26503),
    ('ASIA', 'Sydney', '103.4.115.100', 26503)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'overwatch-2';

-- Row Level Security (RLS) Policies

-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE tips ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE tip_votes ENABLE ROW LEVEL SECURITY;

-- Profiles: users can read public profiles, edit their own
CREATE POLICY "Public profiles are viewable by everyone"
    ON profiles FOR SELECT
    USING (is_public = true OR auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON profiles FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
    ON profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Test results: users can read all, insert their own
CREATE POLICY "Test results are viewable by everyone"
    ON test_results FOR SELECT
    USING (true);

CREATE POLICY "Users can insert own test results"
    ON test_results FOR INSERT
    WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

-- Anonymous test results allowed
CREATE POLICY "Anonymous test results allowed"
    ON test_results FOR INSERT
    WITH CHECK (user_id IS NULL);

-- Tips: public read, authenticated write
CREATE POLICY "Tips are viewable by everyone"
    ON tips FOR SELECT
    USING (true);

CREATE POLICY "Authenticated users can create tips"
    ON tips FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own tips"
    ON tips FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own tips"
    ON tips FOR DELETE
    USING (auth.uid() = user_id);

-- Comments: public read, authenticated write
CREATE POLICY "Comments are viewable by everyone"
    ON comments FOR SELECT
    USING (true);

CREATE POLICY "Authenticated users can create comments"
    ON comments FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own comments"
    ON comments FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own comments"
    ON comments FOR DELETE
    USING (auth.uid() = user_id);

-- Tip votes: authenticated users only
CREATE POLICY "Votes are viewable by everyone"
    ON tip_votes FOR SELECT
    USING (true);

CREATE POLICY "Authenticated users can vote"
    ON tip_votes FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can change own vote"
    ON tip_votes FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can remove own vote"
    ON tip_votes FOR DELETE
    USING (auth.uid() = user_id);

-- Games and servers are public read-only (admin managed)
-- No RLS needed, just public access

-- Function to auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, username, display_name, avatar_url)
    VALUES (
        NEW.id,
        NEW.raw_user_meta_data->>'username',
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'name'),
        NEW.raw_user_meta_data->>'avatar_url'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for auto profile creation
CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Function to update tip upvotes count
CREATE OR REPLACE FUNCTION public.update_tip_upvotes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE tips SET upvotes = upvotes + NEW.vote WHERE id = NEW.tip_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE tips SET upvotes = upvotes - OLD.vote WHERE id = OLD.tip_id;
    ELSIF TG_OP = 'UPDATE' THEN
        UPDATE tips SET upvotes = upvotes - OLD.vote + NEW.vote WHERE id = NEW.tip_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for upvotes
CREATE TRIGGER on_tip_vote_change
    AFTER INSERT OR UPDATE OR DELETE ON tip_votes
    FOR EACH ROW EXECUTE FUNCTION public.update_tip_upvotes();
