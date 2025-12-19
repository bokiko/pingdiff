-- Add Counter-Strike 2 game and servers
-- Migration: 004_add_counter_strike_2.sql

-- Add Counter-Strike 2 game (update if exists)
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('Counter-Strike 2', 'counter-strike-2', '/icons/cs2.png', true)
ON CONFLICT (slug) DO UPDATE SET is_active = true;

-- Insert Counter-Strike 2 servers (Valve official matchmaking servers)
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
    ('EU', 'Luxembourg', '146.66.152.1', 27015),
    ('EU', 'Stockholm', '146.66.156.1', 27015),
    ('EU', 'Vienna', '146.66.155.1', 27015),
    ('EU', 'Warsaw', '155.133.240.1', 27015),
    ('EU', 'Madrid', '155.133.246.1', 27015),

    -- NA - North America
    ('NA', 'Washington DC', '208.78.164.1', 27015),
    ('NA', 'Atlanta', '162.254.199.1', 27015),
    ('NA', 'Seattle', '192.69.96.1', 27015),
    ('NA', 'Los Angeles', '162.254.194.1', 27015),

    -- ASIA - Asia Pacific
    ('ASIA', 'Singapore', '103.28.54.1', 27015),
    ('ASIA', 'Tokyo', '45.121.186.1', 27015),
    ('ASIA', 'Hong Kong', '155.133.244.1', 27015),
    ('ASIA', 'Mumbai', '180.149.41.1', 27015),
    ('ASIA', 'Sydney', '103.10.125.1', 27015),

    -- SA - South America
    ('SA', 'São Paulo', '209.197.29.1', 27015),
    ('SA', 'Santiago', '155.133.249.1', 27015),
    ('SA', 'Lima', '143.137.146.1', 27015),

    -- ME - Middle East
    ('ME', 'Dubai', '185.25.183.1', 27015)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'counter-strike-2'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs
    WHERE gs.game_id = g.id
    AND gs.location = s.location
);
