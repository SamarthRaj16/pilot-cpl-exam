"use client";

export const dynamic = "force-dynamic";

import React, { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import rawQuestions from "@/data/questions.json";

interface SubjectMeta {
  name: string;
  code: string;
  icon: string;
  desc: string;
}

const BASE_SUBJECTS_METADATA: SubjectMeta[] = [
  {
    name: "Air Navigation",
    code: "CAR SEC 7",
    icon: "🧭",
    desc: "General Navigation, Chart Projections, Instrumentation, Dead Reckoning & PNR/CP.",
  },
  {
    name: "Air Regulations",
    code: "ICAO / CAR",
    icon: "📜",
    desc: "Aircraft Rules 1937, Bharatiya Vayuyan Adhiniyam 2024, Airspace & Aerodromes.",
  },
  {
    name: "Aviation Meteorology",
    code: "I.C. JOSHI 3RD ED",
    icon: "⛅",
    desc: "Atmospheric Pressure, Wind Systems, Monsoon Dynamics, Icing, METAR & TAF.",
  },
  {
    name: "Technical General",
    code: "AGK / ENGINES",
    icon: "⚙️",
    desc: "Principles of Flight, Piston Engines, Hydraulics, Propellers & Flight Instruments.",
  },
  {
    name: "Technical Specific",
    code: "POH / PERF",
    icon: "🛩️",
    desc: "Light Aircraft POH, V-speeds, Limitations, Fuel & Altimetry Procedures.",
  },
  {
    name: "RTR",
    code: "ICAO DOC 9432",
    icon: "🎙️",
    desc: "Radio Telephony Restricted, Phraseology, Distress/Urgency, & VHF Propagation.",
  },
];

export default function DashboardPage() {
  const router = useRouter();

  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string>("");
  const [mode, setMode] = useState<"practice" | "timed" | "mock">("practice");
  const [questionCount, setQuestionCount] = useState<number>(30);
  const [servedIds, setServedIds] = useState<Set<string>>(new Set());
  const [activeMistakes, setActiveMistakes] = useState<number>(0);
  const [recoveredCount, setRecoveredCount] = useState<number>(0);
  const [lastSession, setLastSession] = useState<{ subject: string; topic?: string; date?: string } | null>(null);
  const [loading, setLoading] = useState(false);

  // Compute live question & topic counts directly from authoritative question bank
  const subjectStats = useMemo(() => {
    const stats: Record<string, { total: number; topics: Set<string> }> = {};
    rawQuestions.forEach((q: any) => {
      if (!stats[q.subject]) {
        stats[q.subject] = { total: 0, topics: new Set() };
      }
      stats[q.subject].total += 1;
      stats[q.subject].topics.add(q.topic);
    });
    return stats;
  }, []);

  // Load served IDs, mistakes, and last session from localStorage
  useEffect(() => {
    try {
      const storedServed = localStorage.getItem("cpl_served_ids");
      if (storedServed) {
        setServedIds(new Set(JSON.parse(storedServed)));
      }
    } catch {}

    try {
      const storedMistakes = localStorage.getItem("cpl_mistakes");
      if (storedMistakes) {
        const parsed = JSON.parse(storedMistakes);
        const entries = Object.values(parsed) as any[];
        setActiveMistakes(entries.filter((e) => e.status === "active").length);
        setRecoveredCount(entries.filter((e) => e.status === "resolved").length);
      }
    } catch {}

    try {
      const storedSession = localStorage.getItem("cpl_last_session");
      if (storedSession) {
        setLastSession(JSON.parse(storedSession));
      }
    } catch {}
  }, []);

  const totalBankCount = rawQuestions.length; // 959

  // Filter pool for Quick Launcher
  const candidatePool = useMemo(() => {
    return rawQuestions.filter((q: any) => {
      if (selectedSubjects.length > 0 && !selectedSubjects.includes(q.subject)) return false;
      if (selectedTopic && q.topic !== selectedTopic) return false;
      return true;
    });
  }, [selectedSubjects, selectedTopic]);

  const unservedPool = useMemo(() => {
    return candidatePool.filter((q: any) => !servedIds.has(q.id));
  }, [candidatePool, servedIds]);

  const isExhausted = unservedPool.length === 0 && candidatePool.length > 0;

  // Available topics for selected subjects
  const availableTopics = useMemo(() => {
    return Array.from(
      new Set(
        rawQuestions
          .filter((q: any) => selectedSubjects.length === 0 || selectedSubjects.includes(q.subject))
          .map((q: any) => q.topic)
      )
    ).sort();
  }, [selectedSubjects]);

  const handleToggleSubject = (subjName: string) => {
    if (selectedSubjects.includes(subjName)) {
      setSelectedSubjects(selectedSubjects.filter((s) => s !== subjName));
    } else {
      setSelectedSubjects([...selectedSubjects, subjName]);
    }
  };

  const handleResetRotation = () => {
    const newSet = new Set(servedIds);
    candidatePool.forEach((q: any) => newSet.delete(q.id));
    setServedIds(newSet);
    try {
      localStorage.setItem("cpl_served_ids", JSON.stringify(Array.from(newSet)));
    } catch {}
  };

  const handleStartExam = (overrideSubj?: string, overrideTopic?: string) => {
    setLoading(true);
    const subjs = overrideSubj ? [overrideSubj] : selectedSubjects;
    const top = overrideTopic !== undefined ? overrideTopic : selectedTopic;

    // Track last session for Continue Learning
    try {
      localStorage.setItem(
        "cpl_last_session",
        JSON.stringify({
          subject: subjs[0] || "Air Navigation",
          topic: top || "General Syllabus",
          date: new Date().toLocaleDateString("en-IN", { month: "short", day: "numeric" }),
        })
      );
    } catch {}

    const queryParams = new URLSearchParams();
    if (subjs.length > 0) {
      queryParams.set("subjects", subjs.join(","));
    }
    if (top) {
      queryParams.set("topic", top);
    }
    queryParams.set("mode", mode);
    queryParams.set("limit", questionCount.toString());

    router.push(`/dashboard/exam?${queryParams.toString()}`);
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* A. Welcome Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-border-charcoal pb-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-text-primary">
            Welcome back, Pilot.
          </h1>
          <p className="text-xs sm:text-sm text-text-secondary mt-0.5">
            Continue your journey towards your Commercial Pilot Licence.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/dashboard/custom-practice"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface-interactive hover:bg-surface-hover text-brand-sky text-xs font-semibold border border-border-charcoal transition-colors"
          >
            <span>⚡ Custom Quiz Builder</span>
          </Link>
        </div>
      </div>

      {/* B. Continue Learning (Compact) */}
      <div className="p-4 sm:p-5 rounded-xl bg-card-primary border border-border-charcoal flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-brand-teal"></span>
            <span className="text-[11px] font-semibold uppercase tracking-wider text-text-muted">
              Continue Learning
            </span>
            {lastSession?.date && (
              <span className="text-[11px] text-text-muted">&bull; Last practiced {lastSession.date}</span>
            )}
          </div>
          <div className="text-base font-bold text-text-primary">
            {lastSession?.subject || "Air Navigation"}
          </div>
          <div className="text-xs text-text-secondary">
            {lastSession?.topic && lastSession.topic !== "General Syllabus"
              ? `Chapter: ${lastSession.topic}`
              : "General Navigation, Chart Projections & Instrumentation"}
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <button
            onClick={() => handleStartExam(lastSession?.subject || "Air Navigation", lastSession?.topic || "")}
            className="w-full sm:w-auto px-4 py-2 rounded-lg bg-brand-sky hover:bg-brand-skyDark text-bg-main font-bold text-xs shadow-sm transition-colors flex items-center justify-center gap-1.5"
          >
            <span>Continue Practice</span>
            <span>&rarr;</span>
          </button>
        </div>
      </div>

      {/* C. Performance Overview (Compact 4-Metric Grid) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-bold uppercase tracking-wider text-text-muted">
            Performance Overview
          </h2>
          {isExhausted && (
            <span className="text-xs text-brand-gold font-medium">
              Selected pool completed &bull; Click reset in launcher to retake
            </span>
          )}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal">
            <div className="text-[11px] text-text-muted">Total Bank</div>
            <div className="text-xl font-bold text-text-primary mt-1">{totalBankCount}</div>
            <div className="text-[10px] text-text-secondary mt-0.5">Across 6 DGCA subjects</div>
          </div>

          <div className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal">
            <div className="text-[11px] text-text-muted">Questions Seen</div>
            <div className="text-xl font-bold text-brand-sky mt-1">{servedIds.size}</div>
            <div className="text-[10px] text-text-secondary mt-0.5">
              {Math.round((servedIds.size / totalBankCount) * 100)}% question bank coverage
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal">
            <div className="text-[11px] text-text-muted">Pending Mistakes</div>
            <div className="text-xl font-bold text-brand-red mt-1">{activeMistakes}</div>
            <div className="text-[10px] text-text-secondary mt-0.5">In mistake notebook queue</div>
          </div>

          <div className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal">
            <div className="text-[11px] text-text-muted">Recovered Questions</div>
            <div className="text-xl font-bold text-brand-green mt-1">{recoveredCount}</div>
            <div className="text-[10px] text-text-secondary mt-0.5">Mastered after revision</div>
          </div>
        </div>
      </div>

      {/* D. Subject Selection Grid */}
      <div id="subjects" className="space-y-3 scroll-mt-20">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-text-primary">DGCA Written Subjects</h2>
            <p className="text-xs text-text-secondary">
              Select a subject to practice or launch a targeted quiz
            </p>
          </div>
          <button
            onClick={() => {
              setSelectedSubjects([]);
              setSelectedTopic("");
            }}
            className={`text-xs font-semibold px-2.5 py-1 rounded-lg border transition-colors ${
              selectedSubjects.length === 0
                ? "bg-brand-sky/10 text-brand-sky border-brand-sky/30"
                : "border-border-charcoal text-text-secondary hover:text-text-primary"
            }`}
          >
            All Subjects
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {BASE_SUBJECTS_METADATA.map((subj) => {
            const isSelected = selectedSubjects.includes(subj.name);
            const totalInSubj = subjectStats[subj.name]?.total || 0;
            const topicCount = subjectStats[subj.name]?.topics.size || 0;
            const subjQuestions = rawQuestions.filter((q: any) => q.subject === subj.name);
            const unservedInSubj = subjQuestions.filter((q: any) => !servedIds.has(q.id)).length;
            const completionPct = totalInSubj > 0
              ? Math.round(((totalInSubj - unservedInSubj) / totalInSubj) * 100)
              : 0;

            return (
              <div
                key={subj.name}
                onClick={() => handleToggleSubject(subj.name)}
                className={`p-4 rounded-xl bg-card-primary border cursor-pointer transition-all flex flex-col justify-between min-h-[145px] hover:-translate-y-0.5 ${
                  isSelected
                    ? "border-brand-sky ring-1 ring-brand-sky/50 bg-card-elevated"
                    : "border-border-charcoal hover:border-brand-sky/50"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xl">{subj.icon}</span>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-surface-interactive text-text-secondary border border-border-charcoal">
                      {subj.code}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-text-primary">{subj.name}</h3>
                  <p className="text-xs text-text-secondary mt-1 line-clamp-2 leading-relaxed">
                    {subj.desc}
                  </p>
                </div>

                <div className="mt-3 pt-2.5 border-t border-border-charcoal/60">
                  <div className="flex items-center justify-between text-[11px] text-text-muted mb-1">
                    <span>
                      {unservedInSubj} unserved / {totalInSubj} Qs
                    </span>
                    <span className="font-semibold text-brand-sky">{completionPct}%</span>
                  </div>
                  <div className="w-full h-1 bg-surface-interactive rounded-full overflow-hidden">
                    <div
                      className="h-full bg-brand-sky transition-all duration-300 rounded-full"
                      style={{ width: `${completionPct}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* E. Quick Exam Launcher (Clean & Compact) */}
      <div className="p-5 rounded-xl bg-card-primary border border-border-charcoal space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold text-text-primary">Quick Exam Launcher</h2>
            <p className="text-xs text-text-muted">
              Configure your test parameters and start immediately
            </p>
          </div>
          {servedIds.size > 0 && (
            <button
              onClick={handleResetRotation}
              type="button"
              className="text-xs text-brand-gold hover:underline font-medium"
            >
              Reset Exposure
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {/* Mode Selector */}
          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider text-text-muted mb-1.5">
              Mode
            </label>
            <div className="grid grid-cols-3 gap-1 p-1 bg-bg-secondary rounded-lg border border-border-charcoal text-xs">
              {(["practice", "timed", "mock"] as const).map((m) => (
                <button
                  key={m}
                  type="button"
                  onClick={() => setMode(m)}
                  className={`py-1.5 rounded-md font-semibold capitalize transition-colors ${
                    mode === m
                      ? "bg-card-elevated text-brand-sky font-bold shadow-sm"
                      : "text-text-secondary hover:text-text-primary"
                  }`}
                >
                  {m === "mock" ? "Mock" : m}
                </button>
              ))}
            </div>
          </div>

          {/* Chapter Filter */}
          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider text-text-muted mb-1.5">
              Chapter Filter ({availableTopics.length} available)
            </label>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="w-full px-3 py-1.5 rounded-lg bg-bg-secondary border border-border-charcoal text-text-primary text-xs focus:outline-none focus:border-brand-sky"
            >
              <option value="">All Chapters</option>
              {availableTopics.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>

          {/* Question Count Selector */}
          <div>
            <label className="block text-[11px] font-semibold uppercase tracking-wider text-text-muted mb-1.5">
              Question Count
            </label>
            <div className="grid grid-cols-5 gap-1 p-1 bg-bg-secondary rounded-lg border border-border-charcoal text-xs">
              {[10, 20, 30, 40, 50].map((count) => (
                <button
                  key={count}
                  type="button"
                  onClick={() => setQuestionCount(count)}
                  className={`py-1.5 rounded-md font-semibold transition-colors ${
                    questionCount === count
                      ? "bg-card-elevated text-brand-sky font-bold shadow-sm"
                      : "text-text-secondary hover:text-text-primary"
                  }`}
                >
                  {count}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Launch Button */}
        <button
          onClick={() => handleStartExam()}
          disabled={loading || candidatePool.length === 0}
          className="w-full py-2.5 rounded-lg bg-brand-sky hover:bg-brand-skyDark text-bg-main font-bold text-xs sm:text-sm shadow-sm transition-colors flex items-center justify-center gap-1.5 disabled:opacity-40"
        >
          {isExhausted
            ? `Pool Completed — Click to Reset & Retake (${candidatePool.length} Qs)`
            : `Start ${mode === "mock" ? "Mock Exam" : mode === "timed" ? "Timed Exam" : "Practice"} (${unservedPool.length} unserved Qs) →`}
        </button>
      </div>

      {/* F. Specialized Learning Tools (Clean Icon Grid) */}
      <div className="space-y-3 pt-2">
        <h2 className="text-xs font-bold uppercase tracking-wider text-text-muted">
          Specialised Learning Tools
        </h2>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          <Link
            href="/dashboard/notebook"
            className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal hover:border-brand-sky/40 transition-colors group flex flex-col justify-between"
          >
            <div>
              <div className="text-xl mb-1.5">📓</div>
              <div className="text-xs font-bold text-text-primary group-hover:text-brand-sky">Mistake Notebook</div>
              <p className="text-[10px] text-text-muted mt-0.5 line-clamp-2">Target &amp; revise previous mistakes</p>
            </div>
            <span className="text-[10px] text-brand-sky mt-2 font-medium">Open &rarr;</span>
          </Link>

          <Link
            href="/dashboard/revision"
            className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal hover:border-brand-sky/40 transition-colors group flex flex-col justify-between"
          >
            <div>
              <div className="text-xl mb-1.5">🔄</div>
              <div className="text-xs font-bold text-text-primary group-hover:text-brand-sky">Spaced Revision</div>
              <p className="text-[10px] text-text-muted mt-0.5 line-clamp-2">Interval retention algorithm</p>
            </div>
            <span className="text-[10px] text-brand-sky mt-2 font-medium">Open &rarr;</span>
          </Link>

          <Link
            href="/dashboard/readiness"
            className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal hover:border-brand-sky/40 transition-colors group flex flex-col justify-between"
          >
            <div>
              <div className="text-xl mb-1.5">📊</div>
              <div className="text-xs font-bold text-text-primary group-hover:text-brand-sky">Exam Readiness</div>
              <p className="text-[10px] text-text-muted mt-0.5 line-clamp-2">Predicted pass probability</p>
            </div>
            <span className="text-[10px] text-brand-sky mt-2 font-medium">Open &rarr;</span>
          </Link>

          <Link
            href="/dashboard/planner"
            className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal hover:border-brand-sky/40 transition-colors group flex flex-col justify-between"
          >
            <div>
              <div className="text-xl mb-1.5">📅</div>
              <div className="text-xs font-bold text-text-primary group-hover:text-brand-sky">Study Planner</div>
              <p className="text-[10px] text-text-muted mt-0.5 line-clamp-2">Topic schedule &amp; timeline</p>
            </div>
            <span className="text-[10px] text-brand-sky mt-2 font-medium">Open &rarr;</span>
          </Link>

          <Link
            href="/dashboard/library"
            className="p-3.5 rounded-xl bg-card-primary border border-border-charcoal hover:border-brand-sky/40 transition-colors group flex flex-col justify-between"
          >
            <div>
              <div className="text-xl mb-1.5">📚</div>
              <div className="text-xs font-bold text-text-primary group-hover:text-brand-sky">Reference Library</div>
              <p className="text-[10px] text-text-muted mt-0.5 line-clamp-2">CARs, syllabi &amp; I.C. Joshi</p>
            </div>
            <span className="text-[10px] text-brand-sky mt-2 font-medium">Open &rarr;</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
