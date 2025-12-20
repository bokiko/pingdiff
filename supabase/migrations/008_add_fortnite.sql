-- Add Fortnite game and servers
-- Migration: 008_add_fortnite.sql

-- Add Fortnite game (update if exists)
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('Fortnite', 'fortnite', '/icons/fortnite.png', true)
ON CONFLICT (slug) DO UPDATE SET is_active = true;

-- Insert Fortnite servers (AWS infrastructure)
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
    ('EU', 'London', '18.133.162.190', 443),
    ('EU', 'Frankfurt', '3.66.90.29', 443),
    ('EU', 'Paris', '13.37.148.3', 443),
    ('EU', 'Stockholm', '15.237.20.100', 443),

    -- NA - North America
    ('NA', 'Virginia', '3.129.132.114', 443),
    ('NA', 'Ohio', '44.192.143.240', 443),
    ('NA', 'Oregon', '44.237.247.68', 443),
    ('NA', 'California', '3.101.95.110', 443),

    -- ASIA - Asia Pacific
    ('ASIA', 'Tokyo', '35.72.18.106', 443),
    ('ASIA', 'Sydney', '3.25.159.13', 443),

    -- SA - South America
    ('SA', 'São Paulo', '15.228.25.140', 443),

    -- ME - Middle East
    ('ME', 'Bahrain', '15.184.13.113', 443)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'fortnite'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs
    WHERE gs.game_id = g.id
    AND gs.location = s.location
);
