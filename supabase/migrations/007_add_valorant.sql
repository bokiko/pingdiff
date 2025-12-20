-- Add Valorant game and servers
-- Migration: 007_add_valorant.sql

-- Add Valorant game (update if exists)
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('Valorant', 'valorant', '/icons/valorant.png', true)
ON CONFLICT (slug) DO UPDATE SET is_active = true;

-- Insert Valorant servers (Riot Direct infrastructure)
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
    ('EU', 'London', '104.160.141.3', 443),
    ('EU', 'Paris', '162.249.72.1', 443),
    ('EU', 'Frankfurt', '162.249.73.1', 443),
    ('EU', 'Stockholm', '162.249.74.1', 443),
    ('EU', 'Warsaw', '162.249.75.1', 443),

    -- NA - North America
    ('NA', 'Ashburn', '104.160.131.3', 443),
    ('NA', 'Chicago', '104.160.136.3', 443),
    ('NA', 'Dallas', '104.160.151.182', 443),
    ('NA', 'Los Angeles', '104.160.159.1', 443),
    ('NA', 'Atlanta', '104.160.156.1', 443),
    ('NA', 'Seattle', '104.160.158.1', 443),

    -- ASIA - Asia Pacific
    ('ASIA', 'Tokyo', '104.160.129.1', 443),
    ('ASIA', 'Seoul', '104.160.142.1', 443),
    ('ASIA', 'Singapore', '151.106.248.1', 443),
    ('ASIA', 'Hong Kong', '104.160.144.1', 443),
    ('ASIA', 'Mumbai', '151.106.246.1', 443),
    ('ASIA', 'Sydney', '43.229.64.1', 443),

    -- SA - South America
    ('SA', 'São Paulo', '104.160.152.1', 443),
    ('SA', 'Santiago', '104.160.154.1', 443),

    -- ME - Middle East
    ('ME', 'Bahrain', '104.160.146.1', 443)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'valorant'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs
    WHERE gs.game_id = g.id
    AND gs.location = s.location
);
