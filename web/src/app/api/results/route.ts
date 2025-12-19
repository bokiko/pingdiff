import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

interface PingResultData {
  server_id: string;
  server_location: string;
  ping_avg: number;
  ping_min: number;
  ping_max: number;
  jitter: number;
  packet_loss: number;
  raw_times: number[];
}

interface SubmitRequest {
  game: string;
  results: PingResultData[];
  isp: string;
  country: string;
  city: string;
  ip_hash: string;
  client_version: string;
  anonymous_id: string;
}

export async function POST(request: NextRequest) {
  try {
    const body: SubmitRequest = await request.json();

    // Get game by slug
    const { data: game, error: gameError } = await supabase
      .from('games')
      .select('id')
      .eq('slug', body.game || 'overwatch-2')
      .single();

    if (gameError || !game) {
      return NextResponse.json(
        { error: 'Game not found' },
        { status: 404 }
      );
    }

    // Insert all test results
    const resultsToInsert = body.results.map(result => ({
      game_id: game.id,
      server_id: result.server_id,
      ping_avg: result.ping_avg,
      ping_min: result.ping_min,
      ping_max: result.ping_max,
      jitter: result.jitter,
      packet_loss: result.packet_loss,
      isp: body.isp,
      country: body.country,
      city: body.city,
      ip_hash: body.ip_hash,
      client_version: body.client_version,
      raw_data: {
        raw_times: result.raw_times,
        anonymous_id: body.anonymous_id,
      },
    }));

    const { data: insertedResults, error: insertError } = await supabase
      .from('test_results')
      .insert(resultsToInsert)
      .select('id');

    if (insertError) {
      console.error('Error inserting results:', insertError);
      return NextResponse.json(
        { error: 'Failed to save results' },
        { status: 500 }
      );
    }

    // Return the first result ID for dashboard link
    const resultId = insertedResults?.[0]?.id;

    return NextResponse.json({
      success: true,
      id: resultId,
      url: `/dashboard?result=${resultId}`,
      count: insertedResults?.length || 0,
    });
  } catch (error) {
    console.error('Error processing results:', error);
    return NextResponse.json(
      { error: 'Invalid request' },
      { status: 400 }
    );
  }
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const resultId = searchParams.get('id');
  const anonymousId = searchParams.get('anonymous_id');
  const limit = parseInt(searchParams.get('limit') || '50');

  try {
    let query = supabase
      .from('test_results')
      .select(`
        *,
        game_servers (
          location,
          region
        )
      `)
      .order('created_at', { ascending: false })
      .limit(limit);

    if (resultId) {
      query = query.eq('id', resultId);
    } else if (anonymousId) {
      query = query.contains('raw_data', { anonymous_id: anonymousId });
    }

    const { data: results, error } = await query;

    if (error) {
      throw error;
    }

    return NextResponse.json(results);
  } catch (error) {
    console.error('Error fetching results:', error);
    return NextResponse.json(
      { error: 'Failed to fetch results' },
      { status: 500 }
    );
  }
}
