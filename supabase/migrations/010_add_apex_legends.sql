-- Add Apex Legends game and servers
-- Migration: 010_add_apex_legends.sql

-- Add Apex Legends game (update if exists)
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('Apex Legends', 'apex-legends', '/icons/apex-legends.png', true)
ON CONFLICT (slug) DO UPDATE SET is_active = true;

-- Insert Apex Legends servers (AWS infrastructure - migrated April 2025)
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
    ('EU', 'London', '13.43.48.202', 443),
    ('EU', 'Frankfurt', '52.94.141.14', 443),
    ('EU', 'Amsterdam', '3.66.90.156', 443),
    ('EU', 'Belgium', '13.37.152.32', 443),

    -- NA - North America
    ('NA', 'Virginia', '209.54.182.34', 443),
    ('NA', 'Oregon', '52.119.174.12', 443),
    ('NA', 'Ohio', '3.129.132.172', 443),
    ('NA', 'Dallas', '44.198.247.11', 443),

    -- ASIA - Asia Pacific
    ('ASIA', 'Tokyo', '99.77.58.84', 443),
    ('ASIA', 'Singapore', '15.221.8.220', 443),
    ('ASIA', 'Hong Kong', '99.83.81.12', 443),
    ('ASIA', 'Sydney', '99.83.81.12', 443),

    -- SA - South America
    ('SA', 'São Paulo', '177.72.245.178', 443),

    -- ME - Middle East
    ('ME', 'Bahrain', '99.82.132.91', 443)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'apex-legends'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs
    WHERE gs.game_id = g.id
    AND gs.location = s.location
);
