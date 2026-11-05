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
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const calculatePasswordStrength = (pass: string) => {
    let score = 0;
    if (pass.length >= 8) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/[0-9]/.test(pass)) score++;
    if (/[^A-Za-z0-9]/.test(pass)) score++;
    return score;
  };

  const passwordStrength = calculatePasswordStrength(password);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (!agreeTerms) {
      setError("Please accept the Terms of Examination and Privacy Policy.");
      setLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters long.");
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

      // Ensure profile record is inserted
      if (data.user) {
        const studentUserId = data.user.id;
        await supabase.from("profiles").upsert({
          id: studentUserId,
          email,
          full_name: fullName,
          role: "student",
        });

        // Safe guest migration: if guest had served questions or mistakes, migrate them now
        try {
          const guestServed = localStorage.getItem("cpl_served_ids");
          if (guestServed) {
            const ids: string[] = JSON.parse(guestServed);
            if (ids.length > 0) {
              const rows = ids.map((qid) => ({
                student_id: studentUserId,
                question_id: qid,
                subject_id: "Air Navigation",
                topic_id: "General",
              }));
              await supabase.from("question_exposure_history").upsert(rows, { onConflict: "student_id,question_id" });
            }
          }
        } catch {}
      }

      router.push("/dashboard");
      router.refresh();
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred during registration.");
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setGoogleLoading(true);
    setError(null);
    try {
      const supabase = createClient();
      const origin = window.location.origin;
      const { error: oauthError } = await supabase.auth.signInWithOAuth({
        provider: "google",
        options: {
          redirectTo: `${origin}/auth/callback?redirect=/dashboard`,
        },
      });

      if (oauthError) {
        setError(oauthError.message);
        setGoogleLoading(false);
      }
    } catch (err: any) {
      setError(err.message || "Failed to initialize Google Sign In.");
      setGoogleLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-bg-main py-10">
      <div className="w-full max-w-md bg-card-primary border border-border-charcoal rounded-2xl p-6 sm:p-8 shadow-elevated">
        <div className="text-center mb-6">
          <div className="w-14 h-14 mx-auto rounded-xl bg-card-elevated border border-border-charcoal flex items-center justify-center text-3xl mb-3 shadow-card">
            ✈️
          </div>
          <h1 className="text-2xl font-black tracking-tight text-text-primary">
            Student Registration
          </h1>
          <p className="text-xs uppercase tracking-wider text-text-muted font-bold mt-1">
            DGCA CPL Written Examination Portal
          </p>
        </div>

        {error && (
          <div className="mb-5 p-3.5 rounded-xl bg-brand-red/10 border border-brand-red/30 text-brand-red text-xs font-semibold">
            {error}
          </div>
        )}

        {/* Optional Google Sign In */}
        <button
          type="button"
          onClick={handleGoogleSignIn}
          disabled={googleLoading || loading}
          className="w-full py-3 px-4 rounded-xl bg-card-elevated hover:bg-surface-interactive text-text-primary font-bold text-xs border border-border-charcoal transition-all flex items-center justify-center gap-2 mb-4"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
            />
          </svg>
          <span>{googleLoading ? "Connecting..." : "Register with Google"}</span>
        </button>

        <div className="relative my-4 text-center">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-border-charcoal"></div>
          </div>
          <span className="relative px-3 bg-card-primary text-[10px] uppercase text-text-muted font-extrabold tracking-wider">
            Or Register with Email
          </span>
        </div>

        <form onSubmit={handleRegister} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              Full Legal Name (as per DGCA Pariksha)
            </label>
            <input
              type="text"
              required
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Capt. Aditya Sharma"
              className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-blue transition-all text-xs"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              Email Address
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

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              Password (min 8 characters)
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-3 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary placeholder:text-text-muted focus:outline-none focus:border-brand-blue transition-all text-xs"
            />
            {password.length > 0 && (
              <div className="mt-1.5 flex items-center gap-1.5">
                <div className="flex-1 h-1 rounded-full bg-surface-interactive overflow-hidden">
                  <div
                    className={`h-full transition-all ${
                      passwordStrength <= 1
                        ? "w-1/4 bg-brand-red"
                        : passwordStrength === 2
                        ? "w-2/4 bg-brand-gold"
                        : passwordStrength === 3
                        ? "w-3/4 bg-brand-blue"
                        : "w-full bg-brand-teal"
                    }`}
                  ></div>
                </div>
                <span className="text-[10px] text-text-muted font-bold">
                  {passwordStrength <= 1
                    ? "Weak"
                    : passwordStrength === 2
                    ? "Fair"
                    : passwordStrength === 3
                    ? "Good"
                    : "Strong"}
                </span>
              </div>
            )}
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
              Confirm Password
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

          <div className="pt-1">
            <label className="flex items-start gap-2.5 cursor-pointer text-xs text-text-secondary leading-relaxed">
              <input
                type="checkbox"
                required
                checked={agreeTerms}
                onChange={(e) => setAgreeTerms(e.target.checked)}
                className="mt-0.5 w-4 h-4 rounded border-border-charcoal bg-card-elevated text-brand-blue focus:ring-0"
              />
              <span>
                I agree to the <span className="text-brand-blue underline">Terms of Examination</span> and <span className="text-brand-blue underline">Privacy Policy</span>. My learning data will be securely synchronized to my personal profile.
              </span>
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-4 rounded-xl bg-brand-blue hover:bg-brand-skyDark text-bg-main font-black text-xs shadow-glow transition-all flex items-center justify-center gap-2 mt-2 disabled:opacity-50"
          >
            {loading ? "Registering Cadet..." : "Create Pilot Account →"}
          </button>
        </form>

        <p className="text-center text-xs text-text-muted mt-5">
          Already have an account?{" "}
          <Link href="/auth/login" className="text-brand-blue hover:underline font-bold">
            Sign In here
          </Link>
        </p>
      </div>
    </div>
  );
}
