"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function ResultsPage() {
  const router = useRouter();
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    try {
      const stored = sessionStorage.getItem("last_exam_result");
      if (stored) {
        setResult(JSON.parse(stored));
      } else {
        router.push("/dashboard");
      }
    } catch {
      router.push("/dashboard");
    }
  }, [router]);

  if (!result) return null;

  const { score, totalQuestions, accuracy, passed, durationSeconds = 0, reviewItems = [] } = result;
  const missedCount = totalQuestions - score;
  const minutes = Math.floor(durationSeconds / 60);
  const seconds = durationSeconds % 60;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Result Hero Card */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl p-8 text-center shadow-card space-y-4">
        <div className="text-5xl mb-2">{passed ? "🏆" : "⚠️"}</div>
        <div className="text-xs uppercase font-extrabold tracking-wider text-text-muted">
          Total Points Received
        </div>
        <div className="text-5xl font-black text-white tracking-tight">
          {score} / {totalQuestions}
        </div>
        <div className="text-lg font-bold text-brand-gold">{accuracy}% Accuracy</div>

        <div className="pt-2">
          <span
            className={`inline-block px-5 py-2 rounded-full text-xs font-black uppercase tracking-wider ${
              passed
                ? "bg-brand-green/20 text-brand-green border border-brand-green/30"
                : "bg-brand-red/20 text-brand-red border border-brand-red/30"
            }`}
          >
            {passed
              ? "✓ PASS • Met DGCA 70% Written Requirement"
              : `✗ FAIL • Minimum 70% (${Math.ceil(totalQuestions * 0.7)} pts) required to pass`}
          </span>
        </div>

        <p className="text-xs text-text-muted pt-2">
          ⏱️ Time Taken: {minutes}m {seconds}s &bull; DGCA Pass Mark: 70% &bull; No Negative Marking
        </p>
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Link
          href="/dashboard/review"
          className="p-3.5 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white font-extrabold text-xs text-center shadow-card transition-all flex items-center justify-center gap-1.5"
        >
          🔍 Review All {totalQuestions} Questions
        </Link>

        {missedCount > 0 && (
          <Link
            href="/dashboard/notebook"
            className="p-3.5 rounded-xl bg-surface-interactive hover:bg-surface-hover text-brand-orange border border-brand-orange/30 font-bold text-xs text-center transition-all flex items-center justify-center gap-1.5"
          >
            📓 View {missedCount} in Mistake Notebook
          </Link>
        )}

        <Link
          href="/dashboard"
          className="p-3.5 rounded-xl bg-card-elevated hover:bg-surface-interactive text-text-secondary hover:text-white font-bold text-xs text-center border border-border-charcoal transition-all flex items-center justify-center gap-1.5"
        >
          🏠 Return to Dashboard
        </Link>
      </div>
    </div>
  );
}
