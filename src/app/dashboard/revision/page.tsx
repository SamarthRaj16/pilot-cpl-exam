"use client";

import React, { useState } from "react";
import Link from "next/link";

export default function RevisionQueuePage() {
  const [revisionItems] = useState([
    {
      id: "NAV-012",
      subject: "Air Navigation",
      topic: "Great Circles and Rhumb Lines",
      question: "On a Lambert conformal conic chart, a great circle is represented as:",
      interval: 3,
      dueStatus: "due_today",
      nextDate: "Today",
      repetitions: 2,
    },
    {
      id: "MET-007",
      subject: "Aviation Meteorology",
      topic: "Thunderstorms",
      question: "The mature stage of a thunderstorm is definitively marked by:",
      interval: 7,
      dueStatus: "due_today",
      nextDate: "Today",
      repetitions: 3,
    },
    {
      id: "TG-003",
      subject: "Technical General",
      topic: "Piston Engines",
      question: "Engine detonation is typically caused by:",
      interval: 1,
      dueStatus: "overdue",
      nextDate: "Yesterday",
      repetitions: 1,
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-border-charcoal">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <span>🧠</span> Adaptive Spaced Repetition
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Scientifically scheduled revision intervals (1d &bull; 3d &bull; 7d &bull; 14d &bull; 30d) for long-term memory retention
          </p>
        </div>

        <Link
          href="/dashboard/exam?mode=practice"
          className="px-4 py-2 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white text-xs font-bold shadow-card transition-all"
        >
          Start Revision Session (3 Due) &rarr;
        </Link>
      </div>

      {/* Interval Status Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-card-primary border border-border-charcoal text-center shadow-card">
          <div className="text-2xl font-black text-brand-red">1</div>
          <div className="text-[10px] uppercase font-bold text-text-muted mt-1">Overdue Revisions</div>
        </div>
        <div className="p-4 rounded-xl bg-card-primary border border-border-charcoal text-center shadow-card">
          <div className="text-2xl font-black text-brand-orange">2</div>
          <div className="text-[10px] uppercase font-bold text-text-muted mt-1">Due Today</div>
        </div>
        <div className="p-4 rounded-xl bg-card-primary border border-border-charcoal text-center shadow-card">
          <div className="text-2xl font-black text-brand-teal">18</div>
          <div className="text-[10px] uppercase font-bold text-text-muted mt-1">Learning (1-7 Days)</div>
        </div>
        <div className="p-4 rounded-xl bg-card-primary border border-border-charcoal text-center shadow-card">
          <div className="text-2xl font-black text-brand-green">42</div>
          <div className="text-[10px] uppercase font-bold text-text-muted mt-1">Mastered (30+ Days)</div>
        </div>
      </div>

      {/* Revision Queue List */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider">
          Active Queue for Today
        </h3>

        {revisionItems.map((item) => (
          <div
            key={item.id}
            className="p-5 rounded-xl bg-card-primary border border-border-charcoal flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-card"
          >
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-bold text-brand-purple">{item.id}</span>
                <span className="text-text-muted text-xs">&bull;</span>
                <span className="text-xs text-text-secondary font-semibold">
                  {item.subject} &bull; {item.topic}
                </span>
                <span
                  className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                    item.dueStatus === "overdue"
                      ? "bg-brand-red/20 text-brand-red border border-brand-red/30"
                      : "bg-brand-orange/20 text-brand-orange border border-brand-orange/30"
                  }`}
                >
                  {item.dueStatus === "overdue" ? "Overdue" : "Due Today"}
                </span>
              </div>
              <h4 className="text-sm font-bold text-white">{item.question}</h4>
            </div>

            <div className="flex items-center gap-3 self-end sm:self-center">
              <span className="text-xs text-text-muted">Interval: {item.interval} days</span>
              <Link
                href="/dashboard/exam?mode=practice"
                className="px-3 py-1.5 rounded-lg bg-surface-interactive hover:bg-surface-hover text-white text-xs font-bold border border-border-charcoal"
              >
                Review Now
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

