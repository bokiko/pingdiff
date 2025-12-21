-- Add League of Legends game and servers
-- Migration: 009_add_league_of_legends.sql

-- Add League of Legends game (update if exists)
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('League of Legends', 'league-of-legends', '/icons/league-of-legends.png', true)
ON CONFLICT (slug) DO UPDATE SET is_active = true;

-- Insert League of Legends servers (Riot Direct infrastructure)
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
    -- EU - Europe
    ('EU', 'Amsterdam', '104.160.141.3', 443),
    ('EU', 'Frankfurt', '104.160.142.3', 443),
    ('EU', 'Istanbul', '104.160.143.3', 443),

    -- NA - North America
    ('NA', 'Chicago', '104.160.131.3', 443),
    ('NA', 'Miami', '104.160.136.3', 443),

    -- ASIA - Asia Pacific
    ('ASIA', 'Tokyo', '104.160.129.3', 443),
    ('ASIA', 'Seoul', '104.160.142.1', 443),
    ('ASIA', 'Singapore', '151.106.248.3', 443),
    ('ASIA', 'Sydney', '104.160.156.1', 443),

    -- SA - South America
    ('SA', 'São Paulo', '104.160.152.3', 443),

    -- ME - Middle East (uses Turkey server)
    ('ME', 'Istanbul', '104.160.143.3', 443)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'league-of-legends'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs
    WHERE gs.game_id = g.id
    AND gs.location = s.location
);
