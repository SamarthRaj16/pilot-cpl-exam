"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { createClient } from "@/lib/supabase/client";

export default function RegisterPage() {
  const router = useRouter();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      setLoading(false);
      return;
    }

    try {
      const supabase = createClient();
      const { data, error: authError } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
            role: "student",
          },
        },
      });

      if (authError) {
        setError(authError.message);
        setLoading(false);
        return;
      }

      // Automatically create Profile record
      if (data.user) {
        await supabase.from("profiles").upsert({
          id: data.user.id,
          email,
          full_name: fullName,
          role: "student",
        });
      }

      router.push("/dashboard");
      router.refresh();
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred during registration.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-bg-main">
      <div className="w-full max-w-md bg-card-primary border border-border-charcoal rounded-2xl p-8 shadow-elevated">
        <div className="text-center mb-8">
          <div className="w-14 h-14 mx-auto rounded-xl bg-card-elevated border border-border-charcoal flex items-center justify-center text-3xl mb-3 shadow-card">
            ✈️
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight text-text-primary">
            Student Registration
          </h1>
          <p className="text-xs uppercase tracking-wider text-text-muted font-bold mt-1">
            DGCA CPL Written Examination Portal
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-xl bg-brand-red/10 border border-brand-red/30 text-brand-red text-sm font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Full Legal Name (as per DGCA Pariksha)
            </label>
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Capt. Rahul Sharma"
              className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-purple transition-all text-sm"
            />
          </div>

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

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Confirm Password
            </label>
            <input
              type="password"
              required
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-purple transition-all text-sm"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-4 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white font-bold text-sm shadow-card hover:shadow-glow transition-all flex items-center justify-center gap-2 mt-2"
          >
            {loading ? "Creating Account..." : "Register Pilot Account"}
          </button>
        </form>

        <p className="text-center text-xs text-text-muted mt-6">
          Already registered?{" "}
          <Link href="/auth/login" className="text-brand-purple hover:underline font-bold">
            Sign In here
          </Link>
        </p>
      </div>
    </div>
  );
}

