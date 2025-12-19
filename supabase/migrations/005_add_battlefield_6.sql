-- Add Battlefield 6 game and servers
-- Migration: 005_add_battlefield_6.sql

-- Add Battlefield 6 game (update if exists)
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('Battlefield 6', 'battlefield-6', '/icons/bf6.png', true)
ON CONFLICT (slug) DO UPDATE SET is_active = true;

-- Insert Battlefield 6 servers (AWS regional infrastructure)
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
    ('EU', 'London', '35.71.111.102', 25200),
    ('EU', 'Dublin', '35.71.75.100', 25200),
    ('EU', 'Frankfurt', '35.71.105.10', 25200),
    ('EU', 'Paris', '35.71.101.129', 25200),
    ('EU', 'Stockholm', '35.71.98.128', 25200),

    -- NA - North America
    ('NA', 'Virginia', '3.218.182.208', 25200),
    ('NA', 'Ohio', '35.71.102.135', 25200),
    ('NA', 'California', '35.71.117.132', 25200),
    ('NA', 'Oregon', '35.71.66.124', 25200),

    -- ASIA - Asia Pacific
    ('ASIA', 'Tokyo', '52.94.8.118', 25200),
    ('ASIA', 'Seoul', '35.71.109.128', 25200),
    ('ASIA', 'Singapore', '35.71.118.128', 25200),
    ('ASIA', 'Sydney', '35.71.97.129', 25200),
    ('ASIA', 'Mumbai', '35.71.100.130', 25200),

    -- SA - South America
    ('SA', 'São Paulo', '35.71.106.104', 25200),

    -- ME - Middle East
    ('ME', 'Bahrain', '35.71.99.128', 25200)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'battlefield-6'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs
    WHERE gs.game_id = g.id
    AND gs.location = s.location
);
