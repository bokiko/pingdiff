/**
 * Unit tests for src/lib/rate-limit.ts
 *
 * Uses Jest fake timers to control the sliding window without real delays.
 */

// The module uses module-level state (the `stores` Map). We re-import fresh
// each time via jest.isolateModules so state doesn't bleed between tests.
function loadModule() {
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const mod = require('@/lib/rate-limit') as typeof import('@/lib/rate-limit');
  return mod;
}

beforeEach(() => {
  jest.resetModules();
  jest.useFakeTimers();
});

afterEach(() => {
  jest.useRealTimers();
});

// ---------------------------------------------------------------------------
// checkRateLimit
// ---------------------------------------------------------------------------

describe('checkRateLimit', () => {
  it('allows the first request from a new IP', () => {
    const { checkRateLimit } = loadModule();
    expect(checkRateLimit('test', '1.2.3.4')).toBe(true);
  });

  it('allows requests up to the limit', () => {
    const { checkRateLimit } = loadModule();
    const limit = 5;
    for (let i = 0; i < limit; i++) {
      expect(checkRateLimit('bucket', '10.0.0.1', limit)).toBe(true);
    }
  });

  it('blocks the request that exceeds the limit', () => {
    const { checkRateLimit } = loadModule();
    const limit = 3;
    for (let i = 0; i < limit; i++) {
      checkRateLimit('bucket', '10.0.0.2', limit);
    }
    expect(checkRateLimit('bucket', '10.0.0.2', limit)).toBe(false);
  });

  it('continues to block while still within the window', () => {
    const { checkRateLimit } = loadModule();
    const limit = 2;
    const ip = '10.0.0.3';
    checkRateLimit('bucket', ip, limit);
    checkRateLimit('bucket', ip, limit);
    // Both exhausted — these should all be blocked
    expect(checkRateLimit('bucket', ip, limit)).toBe(false);
    expect(checkRateLimit('bucket', ip, limit)).toBe(false);
  });

  it('resets the count after the window expires', () => {
    const { checkRateLimit } = loadModule();
    const limit = 2;
    const windowMs = 60_000;
    const ip = '10.0.0.4';

    checkRateLimit('bucket', ip, limit, windowMs);
    checkRateLimit('bucket', ip, limit, windowMs);
    expect(checkRateLimit('bucket', ip, limit, windowMs)).toBe(false);

    // Advance time past the window
    jest.advanceTimersByTime(windowMs + 1);

    // Should be allowed again
    expect(checkRateLimit('bucket', ip, limit, windowMs)).toBe(true);
  });

  it('treats different IPs as independent', () => {
    const { checkRateLimit } = loadModule();
    const limit = 1;
    checkRateLimit('bucket', 'a.a.a.a', limit); // exhausts a.a.a.a
    expect(checkRateLimit('bucket', 'a.a.a.a', limit)).toBe(false);
    // b.b.b.b should still be allowed
    expect(checkRateLimit('bucket', 'b.b.b.b', limit)).toBe(true);
  });

  it('treats different buckets as independent', () => {
    const { checkRateLimit } = loadModule();
    const limit = 1;
    const ip = '5.5.5.5';
    checkRateLimit('alpha', ip, limit); // exhausts alpha
    expect(checkRateLimit('alpha', ip, limit)).toBe(false);
    // beta bucket is fresh
    expect(checkRateLimit('beta', ip, limit)).toBe(true);
  });

  it('uses default limit of 30 requests per minute', () => {
    const { checkRateLimit } = loadModule();
    const ip = '6.6.6.6';
    for (let i = 0; i < 30; i++) {
      expect(checkRateLimit('default-limit-test', ip)).toBe(true);
    }
    expect(checkRateLimit('default-limit-test', ip)).toBe(false);
  });

  it('returns true after window resets (1ms past boundary)', () => {
    const { checkRateLimit } = loadModule();
    const limit = 1;
    const windowMs = 5_000;
    const ip = '7.7.7.7';
    checkRateLimit('b', ip, limit, windowMs); // uses up the 1 allowed
    // The check is `now > record.resetTime` (strict), so advance 1ms past the window
    jest.advanceTimersByTime(windowMs + 1);
    expect(checkRateLimit('b', ip, limit, windowMs)).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// getClientIP
// ---------------------------------------------------------------------------

function makeRequest(headers: Record<string, string>): Request {
  return {
    headers: {
      get: (name: string) => headers[name] ?? null,
    },
  } as unknown as Request;
}

describe('getClientIP', () => {
  it('returns the first IP from x-forwarded-for', () => {
    const { getClientIP } = loadModule();
    const req = makeRequest({ 'x-forwarded-for': '203.0.113.1, 10.0.0.1' });
    expect(getClientIP(req)).toBe('203.0.113.1');
  });

  it('handles a single IP in x-forwarded-for', () => {
    const { getClientIP } = loadModule();
    const req = makeRequest({ 'x-forwarded-for': '203.0.113.5' });
    expect(getClientIP(req)).toBe('203.0.113.5');
  });

  it('falls back to x-real-ip when x-forwarded-for is absent', () => {
    const { getClientIP } = loadModule();
    const req = makeRequest({ 'x-real-ip': '198.51.100.7' });
    expect(getClientIP(req)).toBe('198.51.100.7');
  });

  it('falls back to 127.0.0.1 when neither header is present', () => {
    const { getClientIP } = loadModule();
    const req = makeRequest({});
    expect(getClientIP(req)).toBe('127.0.0.1');
  });

  it('trims whitespace from x-forwarded-for entries', () => {
    const { getClientIP } = loadModule();
    const req = makeRequest({ 'x-forwarded-for': '  192.0.2.1  , 10.0.0.2' });
    expect(getClientIP(req)).toBe('192.0.2.1');
  });
});
