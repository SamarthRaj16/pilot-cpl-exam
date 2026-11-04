"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";

export default function ReadinessPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadReadiness() {
      try {
        const res = await fetch("/api/student/readiness");
        const json = await res.json();
        setData(json);
      } catch {
        // Fallback demo data
        setData({
          overallScore: 68,
          status: "Developing",
          weakestSubject: "Technical General",
          strongestSubject: "Air Regulations",
          recommendedActions: [
            "Focus intensive practice on Technical General (currently 54%, below the 70% DGCA passing threshold).",
            "Complete at least 2 full-length Timed Mock Examinations per week to build speed and accuracy.",
            "Review mistakes in your Mistake Notebook daily before beginning new question sets.",
          ],
          subjectScores: {
            "Air Navigation": { accuracy: 74, coverage: 45, attempted: 135, status: "PASS READY" },
            "Air Regulations": { accuracy: 82, coverage: 50, attempted: 150, status: "PASS READY" },
            "Aviation Meteorology": { accuracy: 71, coverage: 60, attempted: 55, status: "PASS READY" },
            "Technical General": { accuracy: 54, coverage: 40, attempted: 24, status: "NEEDS FOCUS" },
            "Technical Specific": { accuracy: 65, coverage: 35, attempted: 15, status: "NEEDS FOCUS" },
            RTR: { accuracy: 78, coverage: 30, attempted: 14, status: "INSUFFICIENT DATA" },
          },
        });
      } finally {
        setLoading(false);
      }
    }
    loadReadiness();
  }, []);

  if (loading || !data) {
    return (
      <div className="min-h-[400px] flex items-center justify-center text-xs font-bold text-text-muted">
        Calculating DGCA examination readiness metrics...
      </div>
    );
  }

  const { overallScore, status, subjectScores = {}, recommendedActions = [] } = data;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
          <span>📈</span> DGCA Exam Readiness Analytics
        </h2>
        <p className="text-xs text-text-muted mt-0.5">
          Comprehensive readiness index benchmarked against the official DGCA 70% pass requirement
        </p>
      </div>

      {/* Main Readiness Score Card */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 sm:p-8 shadow-card flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="space-y-2 text-center sm:text-left">
          <span className="text-xs font-bold uppercase tracking-wider text-text-muted">
            Estimated Examination Readiness
          </span>
          <div className="text-4xl sm:text-5xl font-black text-white tracking-tight">
            {overallScore}%{" "}
            <span
              className={`text-lg sm:text-xl font-bold ml-2 ${
                status === "Exam Ready"
                  ? "text-brand-green"
                  : status === "Developing"
                  ? "text-brand-gold"
                  : "text-brand-orange"
              }`}
            >
              {status}
            </span>
          </div>
          <p className="text-xs text-text-secondary max-w-md">
            Educational estimate based on syllabus coverage, mock paper scores, and chapter accuracy. (Requires ≥ 70% in each individual paper).
          </p>
        </div>

        <div className="flex-shrink-0 text-center">
          <div className="w-28 h-28 rounded-full border-4 border-brand-purple/40 border-t-brand-purple flex items-center justify-center text-2xl font-black text-white shadow-glow">
            {overallScore}%
          </div>
        </div>
      </div>

      {/* Subject Readiness Grid */}
      <div className="space-y-4">
        <h3 className="text-sm font-extrabold text-white uppercase tracking-wider">
          Subject-by-Subject Paper Readiness
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(subjectScores).map(([subj, stats]: [string, any]) => {
            const isPass = stats.status === "PASS READY";
            const isInsufficient = stats.status === "INSUFFICIENT DATA";

            return (
              <div
                key={subj}
                className="bg-card-primary border border-border-charcoal rounded-2xl p-5 shadow-card space-y-3"
              >
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-extrabold text-white">{subj}</h4>
                  <span
                    className={`text-[10px] uppercase font-black px-2 py-0.5 rounded ${
                      isPass
                        ? "bg-brand-green/20 text-brand-green border border-brand-green/30"
                        : isInsufficient
                        ? "bg-surface-interactive text-text-muted"
                        : "bg-brand-orange/20 text-brand-orange border border-brand-orange/30"
                    }`}
                  >
                    {stats.status}
                  </span>
                </div>

                <div>
                  <div className="flex justify-between text-xs font-bold mb-1">
                    <span className="text-text-muted">Accuracy:</span>
                    <span className={isPass ? "text-brand-green" : "text-brand-orange"}>
                      {stats.accuracy}%
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-surface-interactive rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${
                        isPass ? "bg-brand-green" : "bg-brand-orange"
                      }`}
                      style={{ width: `${stats.accuracy}%` }}
                    ></div>
                  </div>
                </div>

                <div className="flex justify-between text-xs text-text-muted font-medium pt-1">
                  <span>Attempted: {stats.attempted} Qs</span>
                  <span>Coverage: {stats.coverage}%</span>
                </div>

                {isInsufficient && (
                  <div className="text-[10px] text-brand-orange font-bold pt-1">
                    ⚠️ Minimum 15 questions needed for reliable mastery rating
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Recommended Action Priorities */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-3">
        <h3 className="text-sm font-extrabold text-white uppercase tracking-wider">
          Recommended Study Priorities
        </h3>
        <ul className="space-y-2 text-xs text-text-secondary">
          {recommendedActions.map((rec: string, i: number) => (
            <li key={i} className="flex items-start gap-2">
              <span className="text-brand-purple font-bold">&bull;</span>
              <span>{rec}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
