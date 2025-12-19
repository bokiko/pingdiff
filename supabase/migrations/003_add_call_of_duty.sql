-- Add Call of Duty game and servers
-- Migration: 003_add_call_of_duty.sql

-- Add Call of Duty game
INSERT INTO games (name, slug, icon_url, is_active) VALUES
    ('Call of Duty', 'call-of-duty', '/icons/call-of-duty.png', true)
ON CONFLICT (slug) DO UPDATE SET is_active = true;

-- Insert Call of Duty servers (using Vultr/Choopa data center IPs)
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
    ('EU', 'Amsterdam', '108.61.198.102', 3074),
    ('EU', 'London', '108.61.196.101', 3074),
    ('EU', 'Frankfurt', '108.61.210.117', 3074),
    ('EU', 'Paris', '108.61.209.127', 3074),
    ('EU', 'Madrid', '208.76.222.30', 3074),

    -- NA - North America
    ('NA', 'Atlanta', '108.61.193.166', 3074),
    ('NA', 'Chicago', '107.191.51.12', 3074),
    ('NA', 'Dallas', '108.61.224.175', 3074),
    ('NA', 'Los Angeles', '108.61.219.200', 3074),
    ('NA', 'Miami', '104.156.244.232', 3074),
    ('NA', 'New York', '108.61.149.182', 3074),
    ('NA', 'San Francisco', '104.156.230.107', 3074),
    ('NA', 'Seattle', '108.61.194.105', 3074),

    -- ASIA - Asia Pacific
    ('ASIA', 'Tokyo', '108.61.201.151', 3074),
    ('ASIA', 'Seoul', '141.164.34.61', 3074),
    ('ASIA', 'Singapore', '45.32.100.168', 3074),
    ('ASIA', 'Sydney', '108.61.212.117', 3074),

    -- SA - South America
    ('SA', 'São Paulo', '216.238.98.118', 3074),
    ('SA', 'Santiago', '64.176.2.7', 3074),

    -- ME - Middle East
    ('ME', 'Tel Aviv', '64.176.162.16', 3074)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'call-of-duty'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs
    WHERE gs.game_id = g.id
    AND gs.location = s.location
);
