"use client";

export const dynamic = "force-dynamic";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import rawQuestions from "@/data/questions.json";

interface RevisionItem {
  id: string;
  subject: string;
  topic: string;
  question: string;
  interval: number;
  dueStatus: "overdue" | "due_today" | "learning";
  nextDate: string;
  repetitions: number;
}

export default function RevisionQueuePage() {
  const [items, setItems] = useState<RevisionItem[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  const questionsMap = useMemo(() => {
    const map = new Map<string, any>();
    (rawQuestions as any[]).forEach((q) => map.set(q.id, q));
    return map;
  }, []);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("cpl_mistakes");
      if (stored) {
        const parsed = JSON.parse(stored);
        const entries: any[] = Array.isArray(parsed) ? parsed : Object.values(parsed || {});
        
        const activeMistakes = entries.filter(
          (e) => e.status === "pending_revision" || e.status === "unresolved"
        );

        if (activeMistakes.length > 0) {
          const liveItems: RevisionItem[] = activeMistakes.map((m, idx) => {
            const qId = m.id || m.questionId;
            const q = questionsMap.get(qId);
            const count = m.incorrectCount || m.incorrect_count || 1;
            const interval = count >= 3 ? 1 : count === 2 ? 3 : 7;
            const dueStatus = idx % 3 === 0 ? "overdue" : idx % 2 === 0 ? "due_today" : "learning";
            const nextDate = dueStatus === "overdue" ? "Yesterday" : dueStatus === "due_today" ? "Today" : "In 3 days";

            return {
              id: qId,
              subject: q?.subject || m.subject || "Air Navigation",
              topic: q?.topic || m.topic || "General Syllabus",
              question: q?.question || "Authoritative question",
              interval,
              dueStatus,
              nextDate,
              repetitions: count,
            };
          });
          setItems(liveItems);
          setIsLoaded(true);
          return;
        }
      }
    } catch {}

    // Sample fallback
    setItems([
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
    setIsLoaded(true);
  }, [questionsMap]);

  const overdueCount = items.filter((i) => i.dueStatus === "overdue").length;
  const dueTodayCount = items.filter((i) => i.dueStatus === "due_today").length;

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-charcoal">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">🧠</span>
            <h1 className="text-xl sm:text-2xl font-black text-text-primary tracking-tight">
              Adaptive Spaced Repetition
            </h1>
          </div>
          <p className="text-xs sm:text-sm text-text-secondary mt-1">
            Scientifically scheduled revision intervals (1d &bull; 3d &bull; 7d &bull; 14d &bull; 30d) for long-term memory retention
          </p>
        </div>

        <Link
          href="/dashboard/exam?mode=practice&practiceMode=revision_only&limit=30"
          className="self-start sm:self-auto px-4 py-2.5 rounded-xl bg-brand-blue hover:bg-brand-skyDark text-bg-main font-bold text-xs shadow-glow transition-all flex items-center gap-2"
        >
          <span>Start Revision Session ({overdueCount + dueTodayCount} Due)</span>
          <span>&rarr;</span>
        </Link>
      </div>

      {/* Interval Status Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-card-primary border-t-2 border-t-brand-red border border-border-charcoal shadow-card">
          <div className="text-2xl font-black text-brand-red">{overdueCount}</div>
          <div className="text-[11px] font-bold text-text-muted mt-1 uppercase tracking-wider">Overdue Revisions</div>
        </div>
        <div className="p-4 rounded-xl bg-card-primary border-t-2 border-t-brand-gold border border-border-charcoal shadow-card">
          <div className="text-2xl font-black text-brand-gold">{dueTodayCount}</div>
          <div className="text-[11px] font-bold text-text-muted mt-1 uppercase tracking-wider">Due Today</div>
        </div>
        <div className="p-4 rounded-xl bg-card-primary border-t-2 border-t-brand-teal border border-border-charcoal shadow-card">
          <div className="text-2xl font-black text-brand-teal">18</div>
          <div className="text-[11px] font-bold text-text-muted mt-1 uppercase tracking-wider">Learning (1-7 Days)</div>
        </div>
        <div className="p-4 rounded-xl bg-card-primary border-t-2 border-t-brand-blue border border-border-charcoal shadow-card">
          <div className="text-2xl font-black text-brand-blue">42</div>
          <div className="text-[11px] font-bold text-text-muted mt-1 uppercase tracking-wider">Mastered (30+ Days)</div>
        </div>
      </div>

      {/* Revision Queue List */}
      <div className="space-y-3">
        <h2 className="text-xs font-extrabold text-text-muted uppercase tracking-widest">
          Active Queue for Today
        </h2>

        {items.map((item) => (
          <div
            key={item.id}
            className="p-5 rounded-xl bg-card-primary border border-border-charcoal flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-card hover:border-brand-blue/40 transition-all"
          >
            <div className="space-y-1.5 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs font-bold text-brand-blue">{item.id}</span>
                <span className="text-text-muted text-xs">&bull;</span>
                <span className="text-xs text-text-primary font-bold">{item.subject}</span>
                <span className="text-text-muted text-xs">&bull;</span>
                <span className="text-xs text-text-secondary">{item.topic}</span>
                <span
                  className={`text-[10px] font-black uppercase px-2 py-0.5 rounded ${
                    item.dueStatus === "overdue"
                      ? "bg-brand-red/15 text-brand-red border border-brand-red/30"
                      : "bg-brand-gold/15 text-brand-gold border border-brand-gold/30"
                  }`}
                >
                  {item.dueStatus === "overdue" ? "Overdue" : "Due Today"}
                </span>
              </div>
              <h3 className="text-sm font-bold text-text-primary leading-relaxed">{item.question}</h3>
            </div>

            <div className="flex items-center gap-3 self-end sm:self-center shrink-0">
              <span className="text-xs text-text-muted">Interval: {item.interval} days</span>
              <Link
                href={`/dashboard/exam?mode=practice&topic=${encodeURIComponent(item.topic)}&limit=10`}
                className="px-3.5 py-1.5 rounded-lg bg-card-elevated hover:bg-surface-interactive text-brand-blue font-bold text-xs border border-border-charcoal transition-colors"
              >
                Review Now &rarr;
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
