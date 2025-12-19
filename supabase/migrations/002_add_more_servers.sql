-- Add more Overwatch 2 servers
-- Migration: 002_add_more_servers.sql

-- Add new servers for existing regions and new regions (SA, ME)
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
    -- EU - Add Frankfurt
    ('EU', 'Frankfurt', '185.60.112.158', 26503),
    
    -- ASIA - Add Japan and Taiwan
    ('ASIA', 'Tokyo', '34.84.155.100', 26503),
    ('ASIA', 'Taiwan', '203.66.81.98', 26503),
    
    -- SA - South America (new region)
    ('SA', 'São Paulo', '54.207.107.12', 26503),
    
    -- ME - Middle East (new region)
    ('ME', 'Bahrain', '157.175.45.1', 26503),
    ('ME', 'Dubai', '34.18.61.77', 26503)
) AS s(region, location, ip_address, port)
WHERE g.slug = 'overwatch-2'
AND NOT EXISTS (
    SELECT 1 FROM game_servers gs 
    WHERE gs.game_id = g.id 
    AND gs.location = s.location
);

-- Update location names to be cleaner (remove US West/Central/East from names)
UPDATE game_servers 
SET location = 'Los Angeles' 
WHERE location = 'Los Angeles (US West)';

UPDATE game_servers 
SET location = 'Chicago' 
WHERE location = 'Chicago (US Central)';

UPDATE game_servers 
SET location = 'New York' 
WHERE location = 'New York (US East)';
