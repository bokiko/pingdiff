import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const gameSlug = searchParams.get('game') || 'overwatch-2';

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
      .select('*')
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

    for (const server of servers || []) {
      if (!serversByRegion[server.region]) {
        serversByRegion[server.region] = [];
      }
      serversByRegion[server.region].push({
        id: server.id,
        location: server.location,
        ip: server.ip_address,
        port: server.port || 26503,
      });
    }

    return NextResponse.json(serversByRegion);
  } catch (error) {
    console.error('Error fetching servers:', error);
    return NextResponse.json(
      { error: 'Failed to fetch servers' },
      { status: 500 }
    );
  }
}
