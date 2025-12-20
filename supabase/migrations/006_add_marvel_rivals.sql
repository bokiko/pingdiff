-- Add Marvel Rivals game and servers
-- Migration: 006_add_marvel_rivals.sql

-- Add Marvel Rivals game (update if exists)
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('Marvel Rivals', 'marvel-rivals', '/icons/marvel-rivals.png', true)
ON CONFLICT (slug) DO UPDATE SET is_active = true;

-- Insert Marvel Rivals servers (AWS cloud infrastructure)
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
    ('EU', 'Dublin', '52.94.76.1', 443),
    ('EU', 'London', '52.94.77.1', 443),
    ('EU', 'Paris', '52.94.78.1', 443),
    ('EU', 'Frankfurt', '52.94.79.1', 443),
    ('EU', 'Stockholm', '52.94.80.1', 443),

    -- NA - North America
    ('NA', 'Virginia', '52.94.81.1', 443),
    ('NA', 'Ohio', '52.94.82.1', 443),
    ('NA', 'California', '52.94.83.1', 443),
    ('NA', 'Oregon', '52.94.84.1', 443),

    -- ASIA - Asia Pacific
    ('ASIA', 'Tokyo', '52.94.85.1', 443),
    ('ASIA', 'Seoul', '52.94.86.1', 443),
    ('ASIA', 'Singapore', '52.94.87.1', 443),
    ('ASIA', 'Sydney', '52.94.88.1', 443),
    ('ASIA', 'Mumbai', '52.94.89.1', 443),

    -- SA - South America
    ('SA', 'São Paulo', '52.94.90.1', 443),

    -- ME - Middle East
    ('ME', 'Bahrain', '52.94.91.1', 443)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'marvel-rivals'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs
    WHERE gs.game_id = g.id
    AND gs.location = s.location
);
