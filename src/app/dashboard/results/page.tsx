"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function ResultsPage() {
  const router = useRouter();
  const [result, setResult] = useState<any>(null);
  const [syllabusMarked, setSyllabusMarked] = useState<Record<string, boolean>>({});
  const [markingSyllabus, setMarkingSyllabus] = useState(false);

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

  // Extract unique subject/topic pairs tested in this session
  const testedTopics: { subject: string; topic: string }[] = [];
  const seenKeys = new Set<string>();

  reviewItems.forEach((item: any) => {
    if (item.subject && item.topic) {
      const key = `${item.subject}:::${item.topic}`;
      if (!seenKeys.has(key)) {
        seenKeys.add(key);
        testedTopics.push({ subject: item.subject, topic: item.topic });
      }
    }
  });

  const handleMarkSyllabus = async (subject: string, topic: string) => {
    const key = `${subject}:::${topic}`;
    setMarkingSyllabus(true);
    try {
      // 1. Read existing local progress
      let currentMap: Record<string, any> = {};
      try {
        const stored = localStorage.getItem("cpl_syllabus_progress");
        if (stored) currentMap = JSON.parse(stored);
      } catch {}

      const existing = currentMap[key] || {
        subject_name: subject,
        topic_name: topic,
        theory_completed: false,
        practice_completed: false,
        mock_completed: false,
      };

      const updated = {
        ...existing,
        practice_completed: true,
        updated_at: new Date().toISOString(),
      };

      currentMap[key] = updated;
      localStorage.setItem("cpl_syllabus_progress", JSON.stringify(currentMap));

      // 2. Sync to API
      await fetch("/api/syllabus", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });

      setSyllabusMarked((prev) => ({ ...prev, [key]: true }));
    } catch (e) {
      console.warn("Failed to update syllabus from results", e);
    } finally {
      setMarkingSyllabus(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 pb-12">
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
                ? "bg-semantic-teal/20 text-semantic-teal border border-semantic-teal/30"
                : "bg-semantic-error/20 text-semantic-error border border-semantic-error/30"
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

      {/* Syllabus Completion Suggestion Banner (Phase 3 Integration) */}
      {testedTopics.length > 0 && (
        <div className="bg-card-primary border border-brand-blue/30 rounded-2xl p-6 shadow-card space-y-3">
          <div className="flex items-center gap-2">
            <span className="text-xl">📋</span>
            <div>
              <h3 className="text-sm font-bold text-text-primary">
                Update Syllabus Progress Tracker
              </h3>
              <p className="text-xs text-text-secondary">
                You just practiced questions covering the following DGCA topic(s). Would you like to mark &ldquo;Practice&rdquo; as completed in your Syllabus Tracker?
              </p>
            </div>
          </div>

          <div className="space-y-2 pt-2">
            {testedTopics.map(({ subject, topic }) => {
              const key = `${subject}:::${topic}`;
              const isMarked = syllabusMarked[key];
              return (
                <div
                  key={key}
                  className="flex items-center justify-between p-3 rounded-xl bg-surface-interactive border border-border-charcoal text-xs"
                >
                  <div>
                    <span className="font-bold text-text-primary">{topic}</span>
                    <span className="text-[10px] text-text-muted ml-2">({subject})</span>
                  </div>
                  {isMarked ? (
                    <span className="text-xs font-bold text-semantic-teal flex items-center gap-1">
                      ✓ Practice Marked Complete
                    </span>
                  ) : (
                    <button
                      onClick={() => handleMarkSyllabus(subject, topic)}
                      disabled={markingSyllabus}
                      className="px-3 py-1.5 rounded-lg bg-brand-blue text-bg-main text-xs font-bold hover:bg-opacity-90 transition-all disabled:opacity-50"
                    >
                      ✓ Mark Practice Complete
                    </button>
                  )}
                </div>
              );
            })}
          </div>

          <div className="pt-2 flex justify-end">
            <Link
              href="/dashboard/syllabus"
              className="text-xs font-bold text-brand-blue hover:underline"
            >
              View Full Syllabus Tracker →
            </Link>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Link
          href="/dashboard/review"
          className="p-3.5 rounded-xl bg-brand-blue text-bg-main font-extrabold text-xs text-center shadow-card hover:bg-opacity-90 transition-all flex items-center justify-center gap-1.5"
        >
          🔍 Review All {totalQuestions} Questions
        </Link>

        {missedCount > 0 && (
          <Link
            href="/dashboard/notebook"
            className="p-3.5 rounded-xl bg-surface-interactive hover:bg-surface-hover text-semantic-warning border border-semantic-warning/30 font-bold text-xs text-center transition-all flex items-center justify-center gap-1.5"
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
