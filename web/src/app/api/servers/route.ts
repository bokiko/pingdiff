import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { checkRateLimit, getClientIP } from '@/lib/rate-limit';

// Allowlist of known game slugs to prevent arbitrary DB probing.
// Keep in sync with the `games` table.
const ALLOWED_GAME_SLUGS = /^[a-z0-9-]{1,50}$/;

export async function GET(request: NextRequest) {
  // Rate-limit this endpoint independently (higher limit; read-only, cacheable)
  const clientIP = getClientIP(request);
  if (!checkRateLimit('servers', clientIP, 60, 60_000)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded. Please try again later.' },
      { status: 429 }
    );
  }

  const searchParams = request.nextUrl.searchParams;
  const rawSlug = searchParams.get('game') ?? 'overwatch-2';

  // Validate slug format to prevent injection / unexpected DB queries
  if (!ALLOWED_GAME_SLUGS.test(rawSlug)) {
    return NextResponse.json(
      { error: 'Invalid game slug.' },
      { status: 400 }
    );
  }

  const gameSlug = rawSlug;

  try {
    // Get game by slug
    const { data: game, error: gameError } = await supabase
      .from('games')
      .select('id')
      .eq('slug', gameSlug)
      .eq('is_active', true)
      .single();

    if (gameError || !game) {
      return NextResponse.json(
        { error: 'Game not found' },
        { status: 404 }
      );
    }

    // Get servers for the game
    const { data: servers, error: serversError } = await supabase
      .from('game_servers')
      .select('id, location, region, ip_address, port')
      .eq('game_id', game.id)
      .eq('is_active', true)
      .order('region')
      .order('location');

    if (serversError) {
      throw serversError;
    }

    // Group servers by region
    const serversByRegion: Record<string, Array<{
      id: string;
      location: string;
      ip: string;
      port: number;
    }>> = {};

    for (const server of servers ?? []) {
      if (!serversByRegion[server.region]) {
        serversByRegion[server.region] = [];
      }
      serversByRegion[server.region].push({
        id: server.id,
        location: server.location,
        ip: server.ip_address,
        port: server.port ?? 26503,
      });
    }

    return NextResponse.json(serversByRegion, {
      headers: {
        // Servers list changes rarely — cache aggressively at the CDN layer
        'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
      },
    });
  } catch (error) {
    console.error('Error fetching servers:', error);
    return NextResponse.json(
      { error: 'Failed to fetch servers' },
      { status: 500 }
    );
  }
}
