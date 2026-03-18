/**
 * Simple in-memory sliding-window rate limiter.
 *
 * Shared across all API routes so limits are enforced consistently.
 * Note: resets on server restart; for production use a Redis-backed solution.
 */

interface RateLimitRecord {
  count: number;
  resetTime: number;
}

const stores = new Map<string, Map<string, RateLimitRecord>>();

/**
 * Check whether a client IP has exceeded its rate limit for a named bucket.
 *
 * @param bucket  - A name identifying the limit pool (e.g. "results", "servers")
 * @param ip      - Client IP address
 * @param limit   - Max requests allowed per window (default 30)
 * @param windowMs - Window duration in milliseconds (default 60 000)
 * @returns true if the request is allowed, false if rate-limited
 */
export function checkRateLimit(
  bucket: string,
  ip: string,
  limit = 30,
  windowMs = 60_000
): boolean {
  if (!stores.has(bucket)) {
    stores.set(bucket, new Map());
  }
  const store = stores.get(bucket)!;

  const now = Date.now();
  const record = store.get(ip);

  if (!record || now > record.resetTime) {
    store.set(ip, { count: 1, resetTime: now + windowMs });
    return true;
  }

  if (record.count >= limit) {
    return false;
  }

  record.count++;
  return true;
}

/**
 * Extract the real client IP from a Next.js request, handling proxies.
 */
export function getClientIP(request: Request): string {
  // NextRequest extends Request and exposes headers
  const forwarded = (request as { headers: Headers }).headers.get("x-forwarded-for");
  const realIP = (request as { headers: Headers }).headers.get("x-real-ip");
  return forwarded?.split(",")[0]?.trim() ?? realIP ?? "127.0.0.1";
}
