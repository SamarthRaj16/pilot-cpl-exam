"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleReset = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const supabase = createClient();
      const redirectUrl = `${window.location.origin}/auth/reset-password`;
      const { error: resetError } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: redirectUrl,
      });

      if (resetError) {
        setError(resetError.message);
        setLoading(false);
        return;
      }

      setSubmitted(true);
      setLoading(false);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred while requesting reset.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-bg-main">
      <div className="w-full max-w-md bg-card-primary border border-border-charcoal rounded-2xl p-8 shadow-elevated">
        <div className="text-center mb-8">
          <div className="w-14 h-14 mx-auto rounded-xl bg-card-elevated border border-border-charcoal flex items-center justify-center text-3xl mb-3 shadow-card">
            🔑
          </div>
          <h1 className="text-2xl font-black tracking-tight text-text-primary">
            Account Recovery
          </h1>
          <p className="text-xs uppercase tracking-wider text-text-muted font-bold mt-1">
            Reset Your Pilot Access Credentials
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-brand-red/10 border border-brand-red/30 text-brand-red text-xs font-semibold">
            {error}
          </div>
        )}

        {submitted ? (
          <div className="space-y-5 text-center">
            <div className="p-4 rounded-xl bg-brand-teal/10 border border-brand-teal/30 text-brand-teal text-xs font-semibold leading-relaxed">
              ✓ Password reset link has been dispatched to <strong>{email}</strong>. Please check your inbox and click the recovery link.
            </div>

            <p className="text-xs text-text-muted">
              Didn&apos;t receive the email? Check your spam folder or try again in a few minutes.
            </p>

            <Link
              href="/auth/login"
              className="inline-block w-full py-3 px-4 rounded-xl bg-card-elevated hover:bg-surface-interactive text-brand-blue font-bold text-xs border border-border-charcoal transition-all"
            >
              Return to Sign In &rarr;
            </Link>
          </div>
        ) : (
          <form onSubmit={handleReset} className="space-y-4">
            <p className="text-xs text-text-secondary leading-relaxed">
              Enter your registered pilot email address below. We will send you an official link to securely reset your password.
            </p>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
                Registered Email
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="pilot@aviation.in"
                className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-blue transition-all text-xs"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 px-4 rounded-xl bg-brand-blue hover:bg-brand-skyDark text-bg-main font-black text-xs shadow-glow transition-all flex items-center justify-center gap-2 mt-2 disabled:opacity-50"
            >
              {loading ? "Transmitting..." : "Send Reset Link →"}
            </button>

            <div className="pt-4 text-center">
              <Link
                href="/auth/login"
                className="text-xs text-text-muted hover:text-brand-blue font-semibold transition-colors"
              >
                ← Remember your password? Sign In
              </Link>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

