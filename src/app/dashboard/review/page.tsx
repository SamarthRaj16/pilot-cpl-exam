"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function ReviewPage() {
  const router = useRouter();
  const [reviewItems, setReviewItems] = useState<any[]>([]);
  const [filterMistakesOnly, setFilterMistakesOnly] = useState(false);

  const LETTERS = ["A", "B", "C", "D"];

  useEffect(() => {
    try {
      const stored = sessionStorage.getItem("last_exam_result");
      if (stored) {
        const parsed = JSON.parse(stored);
        setReviewItems(parsed.reviewItems || []);
      } else {
        router.push("/dashboard");
      }
    } catch {
      router.push("/dashboard");
    }
  }, [router]);

  const filtered = filterMistakesOnly
    ? reviewItems.filter((item) => !item.isCorrect)
    : reviewItems;

  const totalMistakes = reviewItems.filter((i) => !i.isCorrect).length;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header and Filter */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-border-charcoal">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <span>🔍</span> Authoritative Answer Key & Explanations
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Verified step-by-step reasoning and official aviation regulatory references
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setFilterMistakesOnly(false)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              !filterMistakesOnly
                ? "bg-brand-purple text-white shadow-glow"
                : "bg-card-elevated border border-border-charcoal text-text-secondary"
            }`}
          >
            All Questions ({reviewItems.length})
          </button>
          <button
            onClick={() => setFilterMistakesOnly(true)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              filterMistakesOnly
                ? "bg-brand-orange text-black shadow-glow"
                : "bg-card-elevated border border-border-charcoal text-text-secondary"
            }`}
          >
            Mistakes Only ({totalMistakes})
          </button>
          <Link
            href="/dashboard/results"
            className="px-3 py-1.5 rounded-lg bg-surface-interactive text-text-secondary hover:text-white text-xs font-bold ml-2"
          >
            &larr; Results
          </Link>
        </div>
      </div>

      {/* Review Questions List */}
      <div className="space-y-4">
        {filtered.map((item, idx) => {
          const {
            questionId,
            subject,
            topic,
            question,
            options,
            studentChoice,
            correctChoice,
            isCorrect,
            pointsAwarded,
            explanation,
            source,
          } = item;

          return (
            <div
              key={questionId || idx}
              className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-4"
            >
              {/* Card Meta Header */}
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="text-text-muted uppercase tracking-wider">
                  Question {idx + 1} &bull; {subject} &bull; {topic}
                </span>
                <span
                  className={`px-2.5 py-0.5 rounded-full text-[10px] uppercase font-black tracking-wider ${
                    isCorrect
                      ? "bg-brand-green/20 text-brand-green border border-brand-green/30"
                      : "bg-brand-red/20 text-brand-red border border-brand-red/30"
                  }`}
                >
                  {isCorrect ? "+1 Point Awarded" : "0 Points (Incorrect)"}
                </span>
              </div>

              {/* Question Text */}
              <h4 className="text-base font-bold text-white leading-relaxed">{question}</h4>

              {/* Student's Choice */}
              <div>
                {studentChoice < 0 ? (
                  <div className="p-3 rounded-xl bg-brand-orange/10 border border-brand-orange/30 text-xs font-bold text-brand-orange">
                    ⚠️ Your Choice: Skipped / Unanswered (0 pts)
                  </div>
                ) : isCorrect ? (
                  <div className="p-3 rounded-xl bg-brand-green/10 border border-brand-green/30 text-xs font-bold text-brand-green">
                    ✓ Your Choice: {LETTERS[studentChoice]}. {options[studentChoice]} (+1 pt)
                  </div>
                ) : (
                  <div className="p-3 rounded-xl bg-brand-red/10 border border-brand-red/30 text-xs font-bold text-brand-red">
                    ✗ Your Choice: {LETTERS[studentChoice]}. {options[studentChoice]} (0 pts)
                  </div>
                )}
              </div>

              {/* Authoritative Correct Answer */}
              <div className="p-3 rounded-xl bg-brand-green/10 border border-brand-green/30 text-xs font-bold text-brand-green">
                ✓ Authoritative Correct Answer: {LETTERS[correctChoice]}. {options[correctChoice]}
              </div>

              {/* Educational Explanation */}
              <div className="p-4 rounded-xl bg-card-elevated border border-border-charcoal text-xs text-text-secondary leading-relaxed">
                <strong className="text-white block mb-1">Authoritative Explanation:</strong>
                {explanation}
              </div>

              {/* Official Source Reference Citation */}
              <div className="text-[11px] font-bold text-text-muted pt-1">
                📚 Official Reference: {source}
              </div>
            </div>
          );
        })}
      </div>

      <div className="text-center pt-4">
        <Link
          href="/dashboard"
          className="inline-block px-6 py-3 rounded-xl bg-surface-interactive hover:bg-surface-hover text-white text-xs font-bold border border-border-charcoal transition-all"
        >
          Return to Dashboard
        </Link>
      </div>
    </div>
  );
}
