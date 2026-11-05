/**
 * CPL Practice 2.0 — Structured Backend Logger & Error Monitor (Feature D5)
 * 
 * Provides:
 * - Correlation IDs for request tracing
 * - High-resolution performance timers (latency tracking)
 * - Strict Privacy Engine: redacts passwords, tokens, API keys, answer keys & PII
 * - In-memory diagnostic ring buffer for administrative health inspection
 */

export type LogLevel = "info" | "warn" | "error" | "perf";

export interface LogEntry {
  id: string;
  timestamp: string;
  level: LogLevel;
  correlationId?: string;
  event: string;
  durationMs?: number;
  metadata?: Record<string, any>;
  error?: {
    name?: string;
    message: string;
    stack?: string;
  };
}

// In-memory circular buffer for recent application events (last 100 entries)
const LOG_BUFFER_SIZE = 100;
const memoryLogRingBuffer: LogEntry[] = [];

// Sensitive field masks
const SENSITIVE_KEY_PATTERNS = [
  /passw(or)?d/i,
  /token/i,
  /secret/i,
  /key/i,
  /auth(orization)?/i,
  /cookie/i,
  /credential/i,
  /answer_?key/i,
  /correct_?choice/i,
  /authoritative_?answer/i,
];

/**
 * Privacy Redaction: Scrubs passwords, keys, tokens, and PII from log payloads
 */
export function sanitizeLogData(input: any): any {
  if (input === null || input === undefined) return input;
  if (typeof input !== "object") return input;

  if (Array.isArray(input)) {
    return input.map((item) => sanitizeLogData(item));
  }

  const sanitized: Record<string, any> = {};
  for (const [k, v] of Object.entries(input)) {
    const isSensitive = SENSITIVE_KEY_PATTERNS.some((pat) => pat.test(k));
    if (isSensitive) {
      sanitized[k] = "[REDACTED_CONFIDENTIAL]";
    } else if (k === "email" && typeof v === "string") {
      const parts = v.split("@");
      sanitized[k] = parts.length === 2 ? `${parts[0].slice(0, 2)}***@${parts[1]}` : "[REDACTED_EMAIL]";
    } else if (typeof v === "object") {
      sanitized[k] = sanitizeLogData(v);
    } else {
      sanitized[k] = v;
    }
  }
  return sanitized;
}

export function generateCorrelationId(): string {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return `corr-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

class Logger {
  private log(
    level: LogLevel,
    event: string,
    metadata?: Record<string, any>,
    err?: Error | unknown,
    durationMs?: number,
    correlationId?: string
  ): LogEntry {
    const entry: LogEntry = {
      id: `log-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
      timestamp: new Date().toISOString(),
      level,
      correlationId: correlationId || generateCorrelationId(),
      event,
      durationMs,
      metadata: metadata ? sanitizeLogData(metadata) : undefined,
      error:
        err instanceof Error
          ? {
              name: err.name,
              message: err.message,
              stack: process.env.NODE_ENV !== "production" ? err.stack : undefined,
            }
          : err
          ? { message: String(err) }
          : undefined,
    };

    // Push into ring buffer
    memoryLogRingBuffer.unshift(entry);
    if (memoryLogRingBuffer.length > LOG_BUFFER_SIZE) {
      memoryLogRingBuffer.pop();
    }

    // Output formatted structured log to console
    const jsonStr = JSON.stringify(entry);
    if (level === "error") {
      console.error(jsonStr);
    } else if (level === "warn") {
      console.warn(jsonStr);
    } else {
      console.log(jsonStr);
    }

    return entry;
  }

  info(event: string, metadata?: Record<string, any>, correlationId?: string) {
    return this.log("info", event, metadata, undefined, undefined, correlationId);
  }

  warn(event: string, metadata?: Record<string, any>, correlationId?: string) {
    return this.log("warn", event, metadata, undefined, undefined, correlationId);
  }

  error(event: string, err?: Error | unknown, metadata?: Record<string, any>, correlationId?: string) {
    return this.log("error", event, metadata, err, undefined, correlationId);
  }

  perf(event: string, durationMs: number, metadata?: Record<string, any>, correlationId?: string) {
    return this.log("perf", event, metadata, undefined, durationMs, correlationId);
  }

  startTimer(event: string, correlationId?: string) {
    const start = performance.now();
    const corrId = correlationId || generateCorrelationId();
    return {
      correlationId: corrId,
      end: (metadata?: Record<string, any>) => {
        const duration = Math.round((performance.now() - start) * 10) / 10;
        this.perf(event, duration, metadata, corrId);
        return duration;
      },
    };
  }

  getRecentLogs(): LogEntry[] {
    return [...memoryLogRingBuffer];
  }
}

export const logger = new Logger();

