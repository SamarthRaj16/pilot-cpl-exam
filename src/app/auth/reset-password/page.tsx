"use client";

import React, { useState, Suspense } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";

function ResetPasswordForm() {
  const router = useRouter();
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpdatePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (password.length < 8) {
      setError("Password must be at least 8 characters long.");
      setLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }

    try {
      const supabase = createClient();
      const { error: updateError } = await supabase.auth.updateUser({
        password: password,
      });

      if (updateError) {
        setError(updateError.message);
        setLoading(false);
        return;
      }

      setSuccess(true);
      setLoading(false);
      setTimeout(() => {
        router.push("/dashboard");
      }, 2000);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred during password update.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-bg-main">
      <div className="w-full max-w-md bg-card-primary border border-border-charcoal rounded-2xl p-8 shadow-elevated">
        <div className="text-center mb-8">
          <div className="w-14 h-14 mx-auto rounded-xl bg-card-elevated border border-border-charcoal flex items-center justify-center text-3xl mb-3 shadow-card">
            🛡️
          </div>
          <h1 className="text-2xl font-black tracking-tight text-text-primary">
            Set New Password
          </h1>
          <p className="text-xs uppercase tracking-wider text-text-muted font-bold mt-1">
            Choose a Strong Password for Your Pilot Account
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-brand-red/10 border border-brand-red/30 text-brand-red text-xs font-semibold">
            {error}
          </div>
        )}

        {success ? (
          <div className="space-y-4 text-center">
            <div className="p-4 rounded-xl bg-brand-teal/10 border border-brand-teal/30 text-brand-teal text-xs font-semibold">
              ✓ Password successfully updated! Redirecting to your dashboard...
            </div>
            <Link
              href="/dashboard"
              className="inline-block w-full py-3 px-4 rounded-xl bg-brand-blue text-bg-main font-bold text-xs"
            >
              Open Dashboard Now →
            </Link>
          </div>
        ) : (
          <form onSubmit={handleUpdatePassword} className="space-y-4">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
                New Password (min 8 characters)
              </label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-blue transition-all text-xs"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
                Confirm New Password
              </label>
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-blue transition-all text-xs"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 px-4 rounded-xl bg-brand-blue hover:bg-brand-skyDark text-bg-main font-black text-xs shadow-glow transition-all flex items-center justify-center gap-2 mt-2 disabled:opacity-50"
            >
              {loading ? "Updating..." : "Update Password & Continue →"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center p-4 bg-bg-main text-text-muted text-xs">
          Loading recovery portal...
        </div>
      }
    >
      <ResetPasswordForm />
    </Suspense>
  );
}

