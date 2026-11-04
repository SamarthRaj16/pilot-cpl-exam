"use client";

import React, { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectPath = searchParams.get("redirect") || "/dashboard";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const supabase = createClient();
      const { data, error: authError } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (authError) {
        setError(authError.message);
        setLoading(false);
        return;
      }

      router.push(redirectPath);
      router.refresh();
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred during sign in.");
      setLoading(false);
    }
  };

  const handleGuestLogin = () => {
    router.push("/dashboard");
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-bg-main">
      <div className="w-full max-w-md bg-card-primary border border-border-charcoal rounded-2xl p-8 shadow-elevated">
        <div className="text-center mb-8">
          <div className="w-14 h-14 mx-auto rounded-xl bg-card-elevated border border-border-charcoal flex items-center justify-center text-3xl mb-3 shadow-card">
            ✈️
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-text-primary">
            CPL Practice
          </h1>
          <p className="text-xs uppercase tracking-wider text-text-muted font-bold mt-1">
            DGCA Written Examination Platform
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-brand-red/10 border border-brand-red/30 text-brand-red text-sm font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Email Address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="pilot@aviation.in"
              className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-purple transition-all text-sm"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-purple transition-all text-sm"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-4 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white font-bold text-sm shadow-card hover:shadow-glow transition-all flex items-center justify-center gap-2 mt-2"
          >
            {loading ? "Authenticating..." : "Sign In to Pilot Portal"}
          </button>
        </form>

        <div className="relative my-6 text-center">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-border-charcoal"></div>
          </div>
          <span className="relative px-3 bg-card-primary text-xs uppercase text-text-muted font-bold">
            Or
          </span>
        </div>

        <button
          onClick={handleGuestLogin}
          type="button"
          className="w-full py-3 px-4 rounded-xl bg-surface-interactive hover:bg-surface-hover text-text-secondary hover:text-white font-bold text-sm border border-border-charcoal transition-all"
        >
          Continue as Offline Guest Pilot
        </button>

        <p className="text-center text-xs text-text-muted mt-6">
          Don&apos;t have a pilot account?{" "}
          <Link href="/auth/register" className="text-brand-purple hover:underline font-bold">
            Create an Account
          </Link>
        </p>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center p-4 bg-bg-main text-text-muted text-sm">
          Loading authentication portal...
        </div>
      }
    >
      <LoginForm />
    </Suspense>
  );
}

