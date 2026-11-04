"use client";

import React, { useState } from "react";

export default function StudyPlannerPage() {
  const [dailyTarget, setDailyTarget] = useState(40);
  const [dailyCompleted] = useState(28);
  const [examDate, setExamDate] = useState("2026-12-15");

  const pct = Math.min(100, Math.round((dailyCompleted / dailyTarget) * 100));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
          <span>📅</span> Personal Study Planner
        </h2>
        <p className="text-xs text-text-muted mt-0.5">
          Set study velocity goals and maintain consistent preparation for upcoming DGCA sessions
        </p>
      </div>

      {/* Target Tracker Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-text-muted">
            Daily Question Target
          </span>
          <div className="text-3xl font-black text-white">
            {dailyCompleted} / {dailyTarget} Qs
          </div>
          <div className="w-full h-2 bg-surface-interactive rounded-full overflow-hidden">
            <div
              className="h-full bg-brand-purple rounded-full transition-all duration-500"
              style={{ width: `${pct}%` }}
            ></div>
          </div>
          <p className="text-xs text-brand-teal font-bold">{pct}% of daily target reached</p>
        </div>

        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-text-muted">
            Weekly Mock Exam Goal
          </span>
          <div className="text-3xl font-black text-white">2 / 3 Exams</div>
          <div className="w-full h-2 bg-surface-interactive rounded-full overflow-hidden">
            <div
              className="h-full bg-brand-green rounded-full transition-all duration-500"
              style={{ width: "66%" }}
            ></div>
          </div>
          <p className="text-xs text-brand-green font-bold">1 full-length mock paper left this week</p>
        </div>

        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-text-muted">
            Next DGCA Exam Session
          </span>
          <div className="text-2xl font-black text-white">{examDate}</div>
          <p className="text-xs text-text-secondary">
            Estimated 41 days remaining for complete syllabus revision.
          </p>
          <input
            type="date"
            value={examDate}
            onChange={(e) => setExamDate(e.target.value)}
            className="w-full px-3 py-1.5 rounded-lg bg-card-elevated border border-border-charcoal text-xs text-text-primary focus:outline-none"
          />
        </div>
      </div>

      {/* Weekly Schedule */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-4">
        <h3 className="text-sm font-extrabold text-white uppercase tracking-wider">
          Weekly Study Schedule & Focus Topics
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          <div className="p-4 rounded-xl bg-card-elevated border border-border-charcoal space-y-1">
            <div className="font-extrabold text-brand-purple">Monday &bull; Air Navigation</div>
            <div className="text-text-secondary">Lambert Conformal Charts & PNR Calculations</div>
          </div>
          <div className="p-4 rounded-xl bg-card-elevated border border-border-charcoal space-y-1">
            <div className="font-extrabold text-brand-blue">Wednesday &bull; Meteorology</div>
            <div className="text-text-secondary">Monsoon Systems & Tropical Depressions</div>
          </div>
          <div className="p-4 rounded-xl bg-card-elevated border border-border-charcoal space-y-1">
            <div className="font-extrabold text-brand-green">Friday &bull; Tech General</div>
            <div className="text-text-secondary">Piston Engine Magnetos & Gyro Precession</div>
          </div>
          <div className="p-4 rounded-xl bg-card-elevated border border-brand-gold/30 bg-brand-gold/5 space-y-1">
            <div className="font-extrabold text-brand-gold">Sunday &bull; DGCA Mock</div>
            <div className="text-text-secondary">Full 100-Question Timed Paper (70% Pass Mark)</div>
          </div>
        </div>
      </div>
    </div>
  );
}

