import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { supabase } from '@/lib/supabase';

// Input validation schemas
const PingResultSchema = z.object({
  server_id: z.string().min(1).max(100),
  server_location: z.string().min(1).max(100),
  ping_avg: z.number().min(0).max(10000),
  ping_min: z.number().min(0).max(10000),
  ping_max: z.number().min(0).max(10000),
  jitter: z.number().min(0).max(1000),
  packet_loss: z.number().min(0).max(100),
  raw_times: z.array(z.number().min(0).max(10000)).max(100),
});

const SubmitRequestSchema = z.object({
  game: z.string().min(1).max(50).default('overwatch-2'),
  results: z.array(PingResultSchema).min(1).max(50),
  isp: z.string().max(200).default('Unknown'),
  country: z.string().max(100).default('Unknown'),
  city: z.string().max(100).default('Unknown'),
  ip_hash: z.string().max(64).default(''),
  client_version: z.string().max(20).default('unknown'),
  anonymous_id: z.string().max(100).default('anonymous'),
});

// Simple in-memory rate limiting
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();
const RATE_LIMIT = 30; // requests per window
const RATE_WINDOW = 60 * 1000; // 1 minute

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const record = rateLimitMap.get(ip);

  if (!record || now > record.resetTime) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + RATE_WINDOW });
    return true;
  }

  if (record.count >= RATE_LIMIT) {
    return false;
  }

  record.count++;
  return true;
}

function getClientIP(request: NextRequest): string {
  const forwarded = request.headers.get('x-forwarded-for');
  const realIP = request.headers.get('x-real-ip');
  return forwarded?.split(',')[0]?.trim() || realIP || '127.0.0.1';
}

export async function POST(request: NextRequest) {
  const clientIP = getClientIP(request);

  // Rate limiting
  if (!checkRateLimit(clientIP)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded. Please try again later.' },
      { status: 429 }
    );
  }

  try {
    const rawBody = await request.json();

    // Validate input
    const parseResult = SubmitRequestSchema.safeParse(rawBody);
    if (!parseResult.success) {
      return NextResponse.json(
        { error: 'Invalid request data', details: parseResult.error.issues },
        { status: 400 }
      );
    }

    const body = parseResult.data;

    // Get game by slug
    const { data: game, error: gameError } = await supabase
      .from('games')
      .select('id')
      .eq('slug', body.game)
      .single();

    if (gameError || !game) {
      console.error('Game not found:', body.game);
      return NextResponse.json(
        { error: 'Game not found' },
        { status: 404 }
      );
    }

    // Get all servers for this game to map string IDs to UUIDs
    const { data: servers } = await supabase
      .from('game_servers')
      .select('id, location')
      .eq('game_id', game.id);

    // Create a map of location to server UUID
    const serverMap = new Map<string, string>();
    servers?.forEach(server => {
      serverMap.set(server.location.toLowerCase(), server.id);
    });

    // Insert all test results
    const resultsToInsert = body.results.map(result => {
      const serverUuid = serverMap.get(result.server_location.toLowerCase());

      return {
        game_id: game.id,
        server_id: serverUuid || null,
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
          server_string_id: result.server_id,
          server_location: result.server_location,
        },
      };
    });

    const { data: insertedResults, error: insertError } = await supabase
      .from('test_results')
      .insert(resultsToInsert)
      .select('id');

    if (insertError) {
      console.error('Database error:', insertError.message);
      return NextResponse.json(
        { error: 'Failed to save results' },
        { status: 500 }
      );
    }

    const resultId = insertedResults?.[0]?.id;

    return NextResponse.json({
      success: true,
      id: resultId,
      url: `/dashboard?result=${resultId}`,
      count: insertedResults?.length || 0,
    });
  } catch (error) {
    console.error('Request error:', error);
    return NextResponse.json(
      { error: 'Invalid request' },
      { status: 400 }
    );
  }
}

// UUID validation regex
const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function GET(request: NextRequest) {
  const clientIP = getClientIP(request);

  // Rate limiting
  if (!checkRateLimit(clientIP)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    );
  }

  const searchParams = request.nextUrl.searchParams;
  const resultId = searchParams.get('id');
  const anonymousId = searchParams.get('anonymous_id');
  const limitParam = searchParams.get('limit');
  const limit = Math.min(Math.max(parseInt(limitParam || '50'), 1), 100);

  // Validate UUID format if provided
  if (resultId && !uuidRegex.test(resultId)) {
    return NextResponse.json(
      { error: 'Invalid result ID format' },
      { status: 400 }
    );
  }

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
      // Sanitize anonymous_id
      const sanitizedId = anonymousId.slice(0, 100);
      query = query.contains('raw_data', { anonymous_id: sanitizedId });
    }

    const { data: results, error } = await query;

    if (error) {
      console.error('Database error:', error.message);
      throw error;
    }

    return NextResponse.json(results, {
      headers: {
        'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=300'
      }
    });
  } catch (error) {
    console.error('Fetch error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch results' },
      { status: 500 }
    );
  }
}
