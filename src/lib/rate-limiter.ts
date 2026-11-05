/**
 * Sliding Window In-Memory Rate Limiter (Feature D7 & Phase 7.D)
 * Protects auth endpoints, examination submission, and admin APIs against abuse
 */

interface RateLimitRecord {
  timestamps: number[];
}

const rateLimitMap = new Map<string, RateLimitRecord>();

// Clean up stale entries every 5 minutes
if (typeof setInterval !== "undefined") {
  setInterval(() => {
    const now = Date.now();
    for (const [key, record] of rateLimitMap.entries()) {
      record.timestamps = record.timestamps.filter((ts) => now - ts < 300000);
      if (record.timestamps.length === 0) {
        rateLimitMap.delete(key);
      }
    }
  }, 300000);
}

export interface RateLimitOptions {
  windowMs: number; // e.g. 60000 for 1 minute
  maxRequests: number; // e.g. 20 requests per minute
}

export function checkRateLimit(
  identifier: string,
  options: RateLimitOptions = { windowMs: 60000, maxRequests: 30 }
): { allowed: boolean; remaining: number; retryAfterSeconds: number } {
  const now = Date.now();
  let record = rateLimitMap.get(identifier);

  if (!record) {
    record = { timestamps: [] };
    rateLimitMap.set(identifier, record);
  }

  // Remove timestamps outside the sliding window
  record.timestamps = record.timestamps.filter((ts) => now - ts < options.windowMs);

  if (record.timestamps.length >= options.maxRequests) {
    const oldest = record.timestamps[0];
    const retryAfterSeconds = Math.ceil((oldest + options.windowMs - now) / 1000);
    return {
      allowed: false,
      remaining: 0,
      retryAfterSeconds: Math.max(1, retryAfterSeconds),
    };
  }

  record.timestamps.push(now);
  return {
    allowed: true,
    remaining: options.maxRequests - record.timestamps.length,
    retryAfterSeconds: 0,
  };
}
