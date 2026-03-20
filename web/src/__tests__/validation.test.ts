/**
 * Unit tests for src/lib/validation.ts
 *
 * Tests the Zod schemas used to validate API requests before they hit the DB.
 */

import { PingResultSchema, SubmitRequestSchema } from '@/lib/validation';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function validPingResult() {
  return {
    server_id: 'us-west-1',
    server_location: 'Los Angeles, US',
    ping_avg: 42,
    ping_min: 35,
    ping_max: 55,
    jitter: 4.5,
    packet_loss: 0,
    raw_times: [35, 40, 42, 50, 55],
  };
}

function validSubmitRequest() {
  return {
    game: 'overwatch-2',
    results: [validPingResult()],
    isp: 'Comcast',
    country: 'US',
    city: 'Los Angeles',
    ip_hash: 'abc123',
    client_version: '2.1.0',
    anonymous_id: 'user-xyz-789',
  };
}

// ---------------------------------------------------------------------------
// PingResultSchema
// ---------------------------------------------------------------------------

describe('PingResultSchema', () => {
  it('accepts a fully valid ping result', () => {
    const result = PingResultSchema.safeParse(validPingResult());
    expect(result.success).toBe(true);
  });

  it('rejects missing server_id', () => {
    const data = { ...validPingResult(), server_id: undefined };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });

  it('rejects empty server_id string', () => {
    const data = { ...validPingResult(), server_id: '' };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });

  it('rejects server_id longer than 100 characters', () => {
    const data = { ...validPingResult(), server_id: 'x'.repeat(101) };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });

  it('rejects negative ping_avg', () => {
    const data = { ...validPingResult(), ping_avg: -1 };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });

  it('rejects ping_avg above 10000', () => {
    const data = { ...validPingResult(), ping_avg: 10001 };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });

  it('accepts ping_avg at the boundary (0 and 10000)', () => {
    expect(PingResultSchema.safeParse({ ...validPingResult(), ping_avg: 0 }).success).toBe(true);
    expect(PingResultSchema.safeParse({ ...validPingResult(), ping_avg: 10000 }).success).toBe(true);
  });

  it('rejects jitter above 1000', () => {
    const data = { ...validPingResult(), jitter: 1001 };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });

  it('rejects packet_loss above 100', () => {
    const data = { ...validPingResult(), packet_loss: 100.1 };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });

  it('accepts 100% packet loss', () => {
    const data = { ...validPingResult(), packet_loss: 100 };
    expect(PingResultSchema.safeParse(data).success).toBe(true);
  });

  it('rejects raw_times with more than 100 entries', () => {
    const data = { ...validPingResult(), raw_times: Array(101).fill(10) };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });

  it('accepts raw_times with exactly 100 entries', () => {
    const data = { ...validPingResult(), raw_times: Array(100).fill(10) };
    expect(PingResultSchema.safeParse(data).success).toBe(true);
  });

  it('accepts empty raw_times array', () => {
    const data = { ...validPingResult(), raw_times: [] };
    expect(PingResultSchema.safeParse(data).success).toBe(true);
  });

  it('rejects a raw_time value above 10000', () => {
    const data = { ...validPingResult(), raw_times: [10001] };
    expect(PingResultSchema.safeParse(data).success).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// SubmitRequestSchema
// ---------------------------------------------------------------------------

describe('SubmitRequestSchema', () => {
  it('accepts a fully valid submit request', () => {
    const result = SubmitRequestSchema.safeParse(validSubmitRequest());
    expect(result.success).toBe(true);
  });

  it('applies defaults for omitted optional fields', () => {
    const minimal = { results: [validPingResult()] };
    const result = SubmitRequestSchema.safeParse(minimal);
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.game).toBe('overwatch-2');
      expect(result.data.isp).toBe('Unknown');
      expect(result.data.country).toBe('Unknown');
      expect(result.data.city).toBe('Unknown');
      expect(result.data.ip_hash).toBe('');
      expect(result.data.client_version).toBe('unknown');
      expect(result.data.anonymous_id).toBe('anonymous');
    }
  });

  it('rejects empty results array', () => {
    const data = { ...validSubmitRequest(), results: [] };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('rejects results with more than 50 entries', () => {
    const data = { ...validSubmitRequest(), results: Array(51).fill(validPingResult()) };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('accepts results with exactly 50 entries', () => {
    const data = { ...validSubmitRequest(), results: Array(50).fill(validPingResult()) };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(true);
  });

  it('rejects game slug longer than 50 characters', () => {
    const data = { ...validSubmitRequest(), game: 'g'.repeat(51) };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('rejects empty game slug', () => {
    const data = { ...validSubmitRequest(), game: '' };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('rejects ISP longer than 200 characters', () => {
    const data = { ...validSubmitRequest(), isp: 'x'.repeat(201) };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('rejects ip_hash longer than 64 characters', () => {
    const data = { ...validSubmitRequest(), ip_hash: 'a'.repeat(65) };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('rejects client_version longer than 20 characters', () => {
    const data = { ...validSubmitRequest(), client_version: '1'.repeat(21) };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('rejects anonymous_id longer than 100 characters', () => {
    const data = { ...validSubmitRequest(), anonymous_id: 'u'.repeat(101) };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('rejects a request containing an invalid nested ping result', () => {
    const badResult = { ...validPingResult(), ping_avg: -5 };
    const data = { ...validSubmitRequest(), results: [badResult] };
    expect(SubmitRequestSchema.safeParse(data).success).toBe(false);
  });

  it('passes through valid data unchanged (no coercion side effects)', () => {
    const input = validSubmitRequest();
    const result = SubmitRequestSchema.safeParse(input);
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.game).toBe(input.game);
      expect(result.data.results[0].ping_avg).toBe(input.results[0].ping_avg);
    }
  });
});
