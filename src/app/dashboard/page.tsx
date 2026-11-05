"use client";

import React, { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import rawQuestions from "@/data/questions.json";
import syllabusHierarchy from "@/data/syllabusHierarchy.json";
import SubjectArtwork from "@/components/SubjectArtwork";
import PerformanceTrendCharts from "@/components/PerformanceTrendCharts";

interface SubjectMeta {
  name: string;
  code: string;
  icon: string;
  accent: string;
  desc: string;
}

const BASE_SUBJECTS_METADATA: SubjectMeta[] = [
  {
    name: "Air Navigation",
    code: "CAR SEC 7",
    icon: "🧭",
    accent: "#48A9FF",
    desc: "General Navigation, Chart Projections, Instrumentation, Dead Reckoning & PNR/CP.",
  },
  {
    name: "Air Regulations",
    code: "ICAO / CAR",
    icon: "📜",
    accent: "#A58BFA",
    desc: "Aircraft Rules 1937, Bharatiya Vayuyan Adhiniyam 2024, Airspace & Aerodromes.",
  },
  {
    name: "Aviation Meteorology",
    code: "I.C. JOSHI 3RD ED",
    icon: "⛅",
    accent: "#3ED1B0",
    desc: "Atmospheric Pressure, Wind Systems, Monsoon Dynamics, Icing, METAR & TAF.",
  },
  {
    name: "Technical General",
    code: "AGK / ENGINES",
    icon: "⚙️",
    accent: "#3ED1B0",
    desc: "Principles of Flight, Piston Engines, Hydraulics, Propellers & Flight Instruments.",
  },
  {
    name: "Technical Specific",
    code: "POH / PERF",
    icon: "🛩️",
    accent: "#F2B94B",
    desc: "Light Aircraft POH, V-speeds, Limitations, Fuel & Altimetry Procedures.",
  },
  {
    name: "RTR",
    code: "ICAO DOC 9432",
    icon: "🎙️",
    accent: "#48A9FF",
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
  const [syllabusProgress, setSyllabusProgress] = useState<Record<string, any>>({});
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

    try {
      const storedSyllabus = localStorage.getItem("cpl_syllabus_progress");
      if (storedSyllabus) {
        setSyllabusProgress(JSON.parse(storedSyllabus));
      }
    } catch {}
  }, []);

  // Compute Syllabus Tracker Metrics (95 Topics * 3 Milestones = 285 Items)
  const syllabusMetrics = useMemo(() => {
    const totalTopics = 95;
    const totalItems = totalTopics * 3;
    let theoryDone = 0;
    let practiceDone = 0;
    let mockDone = 0;

    const subList = syllabusHierarchy.map((sub: any) => {
      let subDone = 0;
      sub.topics.forEach((t: any) => {
        const key = `${sub.name}:::${t.name}`;
        const p = syllabusProgress[key];
        if (p?.theory_completed) { theoryDone++; subDone++; }
        if (p?.practice_completed) { practiceDone++; subDone++; }
        if (p?.mock_completed) { mockDone++; subDone++; }
      });
      const subPct = sub.topics.length > 0 ? Math.round((subDone / (sub.topics.length * 3)) * 100) : 0;
      return { name: sub.name, pct: subPct, icon: sub.meta.icon, slug: sub.slug };
    });

    const totalDone = theoryDone + practiceDone + mockDone;
    const overallPct = Math.round((totalDone / totalItems) * 100);
    const theoryPct = Math.round((theoryDone / totalTopics) * 100);
    const practicePct = Math.round((practiceDone / totalTopics) * 100);
    const mockPct = Math.round((mockDone / totalTopics) * 100);

    const sortedSubs = [...subList].sort((a, b) => a.pct - b.pct);
    const lowestSub = sortedSubs.length > 0 ? sortedSubs[0] : null;

    return {
      totalDone,
      totalItems,
      overallPct,
      theoryDone,
      theoryPct,
      practiceDone,
      practicePct,
      mockDone,
      mockPct,
      lowestSub,
    };
  }, [syllabusProgress]);

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
    <div className="space-y-9 max-w-7xl mx-auto">
      {/* 1. Aviation Luxe Hero Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#171D28] via-[#1B2332] to-[#141B26] border border-border-charcoal p-6 sm:p-8 shadow-elevated">
        {/* Subtle decorative background vector */}
        <div className="absolute right-0 top-0 bottom-0 w-1/2 opacity-15 pointer-events-none hidden md:block">
          <svg viewBox="0 0 400 200" className="w-full h-full" fill="none">
            <circle cx="300" cy="100" r="120" stroke="#48A9FF" strokeWidth="1" strokeDasharray="4 4" />
            <circle cx="300" cy="100" r="80" stroke="#3ED1B0" strokeWidth="1.2" />
            <line x1="180" y1="100" x2="420" y2="100" stroke="#48A9FF" strokeWidth="0.8" />
            <line x1="300" y1="-20" x2="300" y2="220" stroke="#48A9FF" strokeWidth="0.8" />
            <path d="M120 180 Q220 80 340 30" stroke="#F2B94B" strokeWidth="2" strokeDasharray="6 4" />
          </svg>
        </div>

        <div className="relative z-10 max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-blue/15 border border-brand-blue/30 text-xs font-bold text-brand-blue">
            <span>✈️</span>
            <span>DGCA CBT Written Examination Platform</span>
          </div>

          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-black text-text-primary tracking-tight">
            Welcome back, Pilot.
          </h1>

          <p className="text-sm sm:text-base text-text-secondary leading-relaxed">
            Your next step towards becoming a Commercial Pilot. 959 verified questions, authentic DGCA Computer-Based Testing, and zero-repeat question rotation.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            <button
              onClick={() => handleStartExam(lastSession?.subject || "Air Navigation", lastSession?.topic || "")}
              className="px-6 py-3 rounded-xl bg-brand-blue hover:bg-brand-skyDark text-bg-main font-black text-sm shadow-glow transition-all flex items-center gap-2 hover:scale-[1.02]"
            >
              <span>Continue Practice</span>
              <span>&rarr;</span>
            </button>

            <Link
              href="/dashboard/custom-practice"
              className="px-5 py-3 rounded-xl bg-card-elevated hover:bg-surface-interactive text-text-primary font-bold text-xs sm:text-sm border border-border-charcoal transition-all flex items-center gap-2"
            >
              <span>⚡ Custom Quiz Builder</span>
            </Link>
          </div>
        </div>
      </div>

      {/* 2. Continue Learning Section (The Focal Point) */}
      <div className="p-5 sm:p-6 rounded-2xl bg-card-primary border-l-4 border-l-brand-teal border border-border-charcoal shadow-card flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-brand-teal animate-pulse"></span>
            <span className="text-xs font-bold uppercase tracking-wider text-brand-teal">
              Active Study Plan
            </span>
            {lastSession?.date && (
              <span className="text-xs text-text-muted">&bull; Last session {lastSession.date}</span>
            )}
          </div>
          <h2 className="text-lg sm:text-xl font-bold text-text-primary">
            {lastSession?.subject || "Air Navigation"}
          </h2>
          <p className="text-xs sm:text-sm text-text-secondary">
            {lastSession?.topic && lastSession.topic !== "General Syllabus"
              ? `Chapter focus: ${lastSession.topic}`
              : "General Navigation, Chart Projections, Instrumentation & Dead Reckoning"}
          </p>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <button
            onClick={() => handleStartExam(lastSession?.subject || "Air Navigation", lastSession?.topic || "")}
            className="w-full md:w-auto px-5 py-2.5 rounded-xl bg-brand-teal hover:bg-brand-teal/90 text-bg-main font-extrabold text-xs sm:text-sm shadow-sm transition-all flex items-center justify-center gap-2"
          >
            <span>Resume Chapter Quiz</span>
            <span>&rarr;</span>
          </button>
        </div>
      </div>

      {/* 3. Performance Indicators (High Contrast, Distinctive Accents) */}
      <div className="space-y-3.5">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-extrabold uppercase tracking-widest text-text-muted">
            Performance Overview
          </h2>
          {isExhausted && (
            <span className="text-xs text-brand-gold font-bold">
              Selected pool completed &bull; Click reset in launcher to retake
            </span>
          )}
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Total Bank */}
          <div className="p-4 sm:p-5 rounded-2xl bg-card-primary border-t-2 border-t-brand-blue border border-border-charcoal shadow-card">
            <div className="flex items-center justify-between text-xs text-text-muted font-bold">
              <span>Question Bank</span>
              <span className="text-lg">📚</span>
            </div>
            <div className="text-2xl sm:text-3xl font-black text-text-primary mt-2">
              {totalBankCount}
            </div>
            <div className="text-xs text-text-secondary mt-1">Across 6 DGCA subjects</div>
          </div>

          {/* Questions Seen */}
          <div className="p-4 sm:p-5 rounded-2xl bg-card-primary border-t-2 border-t-brand-teal border border-border-charcoal shadow-card">
            <div className="flex items-center justify-between text-xs text-text-muted font-bold">
              <span>Zero-Repeat Seen</span>
              <span className="text-lg">🔄</span>
            </div>
            <div className="text-2xl sm:text-3xl font-black text-brand-teal mt-2">
              {servedIds.size}
            </div>
            <div className="text-xs text-text-secondary mt-1">
              {Math.round((servedIds.size / totalBankCount) * 100)}% bank exposure
            </div>
          </div>

          {/* Pending Mistakes */}
          <div className="p-4 sm:p-5 rounded-2xl bg-card-primary border-t-2 border-t-brand-red border border-border-charcoal shadow-card">
            <div className="flex items-center justify-between text-xs text-text-muted font-bold">
              <span>Pending Mistakes</span>
              <span className="text-lg">⚠️</span>
            </div>
            <div className="text-2xl sm:text-3xl font-black text-brand-red mt-2">
              {activeMistakes}
            </div>
            <div className="text-xs text-text-secondary mt-1">In revision queue</div>
          </div>

          {/* Recovered Questions */}
          <div className="p-4 sm:p-5 rounded-2xl bg-card-primary border-t-2 border-t-brand-gold border border-border-charcoal shadow-card">
            <div className="flex items-center justify-between text-xs text-text-muted font-bold">
              <span>Recovered Questions</span>
              <span className="text-lg">⭐</span>
            </div>
            <div className="text-2xl sm:text-3xl font-black text-brand-gold mt-2">
              {recoveredCount}
            </div>
            <div className="text-xs text-text-secondary mt-1">Mastered after mistake</div>
          </div>
        </div>
      </div>

      {/* 3.5. Interactive Syllabus Coverage Widget */}
      <div className="p-5 sm:p-6 rounded-2xl bg-card-primary border border-border-charcoal shadow-card relative overflow-hidden">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          {/* Left: Overall Ring & Title */}
          <div className="flex items-center gap-4 sm:gap-6">
            <div className="relative w-20 h-20 flex-shrink-0 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="42" className="stroke-surface-interactive" strokeWidth="8" fill="transparent" />
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  className="stroke-brand-blue transition-all duration-700 ease-out"
                  strokeWidth="8"
                  strokeDasharray={263.89}
                  strokeDashoffset={263.89 - (263.89 * syllabusMetrics.overallPct) / 100}
                  strokeLinecap="round"
                  fill="transparent"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
                <span className="text-base font-black text-text-primary">{syllabusMetrics.overallPct}%</span>
              </div>
            </div>

            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider text-brand-blue">
                  Interactive Syllabus Tracker
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 bg-surface-interactive rounded text-text-muted">
                  95 Topics • 285 Milestones
                </span>
              </div>
              <h2 className="text-base sm:text-lg font-bold text-text-primary mt-0.5">
                {syllabusMetrics.totalDone} of {syllabusMetrics.totalItems} Checklist Milestones Completed
              </h2>
              {syllabusMetrics.lowestSub && (
                <p className="text-xs text-text-secondary mt-1">
                  Recommended Focus: <strong className="text-brand-gold">{syllabusMetrics.lowestSub.name}</strong> ({syllabusMetrics.lowestSub.pct}% completed)
                </p>
              )}
            </div>
          </div>

          {/* Middle: 3 Milestone Bars */}
          <div className="w-full lg:w-72 space-y-2 border-t lg:border-t-0 lg:border-l border-border-charcoal pt-4 lg:pt-0 lg:pl-6">
            <div className="space-y-1">
              <div className="flex justify-between text-[11px]">
                <span className="text-text-secondary font-medium">📚 Theory</span>
                <span className="font-mono text-text-primary font-bold">{syllabusMetrics.theoryPct}%</span>
              </div>
              <div className="w-full bg-surface-interactive h-1.5 rounded-full overflow-hidden">
                <div className="bg-brand-blue h-full rounded-full transition-all" style={{ width: `${syllabusMetrics.theoryPct}%` }}></div>
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-[11px]">
                <span className="text-text-secondary font-medium">✍️ Practice</span>
                <span className="font-mono text-semantic-teal font-bold">{syllabusMetrics.practicePct}%</span>
              </div>
              <div className="w-full bg-surface-interactive h-1.5 rounded-full overflow-hidden">
                <div className="bg-semantic-teal h-full rounded-full transition-all" style={{ width: `${syllabusMetrics.practicePct}%` }}></div>
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-[11px]">
                <span className="text-text-secondary font-medium">🎯 Mock Exam</span>
                <span className="font-mono text-brand-gold font-bold">{syllabusMetrics.mockPct}%</span>
              </div>
              <div className="w-full bg-surface-interactive h-1.5 rounded-full overflow-hidden">
                <div className="bg-brand-gold h-full rounded-full transition-all" style={{ width: `${syllabusMetrics.mockPct}%` }}></div>
              </div>
            </div>
          </div>

          {/* Right: CTA Button */}
          <div className="flex-shrink-0 w-full lg:w-auto">
            <Link
              href="/dashboard/syllabus"
              className="w-full lg:w-auto px-5 py-2.5 rounded-xl bg-brand-blue text-bg-main text-xs font-black shadow-card hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
            >
              <span>Continue Syllabus</span>
              <span>&rarr;</span>
            </Link>
          </div>
        </div>
      </div>

      {/* 4. Image-Led Subject Cards (Main Visual Interest) */}
      <div id="subjects" className="space-y-4 scroll-mt-24">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-lg sm:text-xl font-black text-text-primary tracking-tight">
              DGCA CPL Written Subjects
            </h2>
            <p className="text-xs sm:text-sm text-text-secondary mt-0.5">
              Comprehensive syllabus coverage with verified questions &amp; explanations
            </p>
          </div>
          <button
            onClick={() => {
              setSelectedSubjects([]);
              setSelectedTopic("");
            }}
            className={`text-xs font-bold px-3 py-1.5 rounded-lg border transition-all ${
              selectedSubjects.length === 0
                ? "bg-brand-blue/20 text-brand-blue border-brand-blue/40"
                : "border-border-charcoal text-text-secondary hover:text-text-primary"
            }`}
          >
            Select All Subjects
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
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
                className={`group rounded-2xl bg-card-primary border overflow-hidden cursor-pointer transition-all duration-200 flex flex-col justify-between shadow-card hover:-translate-y-1 ${
                  isSelected
                    ? "border-brand-blue ring-2 ring-brand-blue/50 shadow-glow"
                    : "border-border-charcoal hover:border-brand-blue/60"
                }`}
              >
                {/* Visual Image Header */}
                <div className="relative w-full h-36 bg-card-elevated overflow-hidden border-b border-border-charcoal/60">
                  <SubjectArtwork subject={subj.name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                  
                  {/* Dark gradient overlay for text readability */}
                  <div className="absolute inset-0 bg-gradient-to-t from-card-primary via-card-primary/40 to-transparent"></div>

                  {/* Syllabus Badge */}
                  <div className="absolute top-3 right-3">
                    <span className="text-[10px] font-extrabold uppercase px-2.5 py-1 rounded-md bg-bg-main/80 backdrop-blur-md border border-border-charcoal text-text-secondary">
                      {subj.code}
                    </span>
                  </div>

                  {/* Icon & Subject Title overlay */}
                  <div className="absolute bottom-2.5 left-4 right-4 flex items-center gap-2.5">
                    <span className="text-2xl drop-shadow-md">{subj.icon}</span>
                    <h3 className="text-base sm:text-lg font-black text-white drop-shadow-md leading-tight">
                      {subj.name}
                    </h3>
                  </div>
                </div>

                {/* Card Content */}
                <div className="p-4 pt-3 flex-1 flex flex-col justify-between space-y-3">
                  <p className="text-xs sm:text-sm text-text-secondary leading-relaxed line-clamp-2">
                    {subj.desc}
                  </p>

                  <div className="pt-2 border-t border-border-charcoal/50 space-y-2">
                    <div className="flex items-center justify-between text-xs text-text-muted font-bold">
                      <span>
                        {unservedInSubj} unserved of {totalInSubj} Qs &bull; {topicCount} Topics
                      </span>
                      <span className="text-brand-blue">{completionPct}%</span>
                    </div>

                    <div className="w-full h-1.5 bg-surface-interactive rounded-full overflow-hidden">
                      <div
                        className="h-full bg-brand-blue transition-all duration-500 rounded-full"
                        style={{ width: `${completionPct}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 5. Quick Exam Launcher (Flight Operations Console) */}
      <div className="p-6 rounded-2xl bg-card-primary border border-border-charcoal shadow-card space-y-5">
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border-charcoal pb-4">
          <div>
            <h2 className="text-base sm:text-lg font-bold text-text-primary flex items-center gap-2">
              <span>🎯</span>
              <span>Quick Exam Launcher</span>
            </h2>
            <p className="text-xs text-text-secondary mt-0.5">
              Launch an immediate exam session with custom parameters
            </p>
          </div>
          {servedIds.size > 0 && (
            <button
              onClick={handleResetRotation}
              type="button"
              className="text-xs text-brand-gold hover:underline font-bold"
            >
              Reset Exposure for Selection
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Mode Selector */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Examination Mode
            </label>
            <div className="grid grid-cols-3 gap-1 p-1 bg-card-elevated rounded-xl border border-border-charcoal text-xs">
              {(["practice", "timed", "mock"] as const).map((m) => (
                <button
                  key={m}
                  type="button"
                  onClick={() => setMode(m)}
                  className={`py-2 rounded-lg font-bold capitalize transition-all ${
                    mode === m
                      ? "bg-brand-blue text-bg-main shadow-sm"
                      : "text-text-secondary hover:text-text-primary"
                  }`}
                >
                  {m === "mock" ? "Mock Exam" : m}
                </button>
              ))}
            </div>
          </div>

          {/* Chapter Filter */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Chapter Filter ({availableTopics.length} available)
            </label>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary text-xs font-semibold focus:outline-none focus:border-brand-blue"
            >
              <option value="">All Topics in selected subjects</option>
              {availableTopics.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>

          {/* Question Count Selector */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Question Count
            </label>
            <div className="grid grid-cols-5 gap-1 p-1 bg-card-elevated rounded-xl border border-border-charcoal text-xs">
              {[10, 20, 30, 40, 50].map((count) => (
                <button
                  key={count}
                  type="button"
                  onClick={() => setQuestionCount(count)}
                  className={`py-2 rounded-lg font-bold transition-all ${
                    questionCount === count
                      ? "bg-brand-blue text-bg-main shadow-sm"
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
          className="w-full py-3.5 rounded-xl bg-brand-blue hover:bg-brand-skyDark text-bg-main font-black text-sm shadow-glow transition-all flex items-center justify-center gap-2 disabled:opacity-40"
        >
          {isExhausted
            ? `Pool Completed — Click to Reset & Retake (${candidatePool.length} Qs)`
            : `Start ${mode === "mock" ? "Mock Exam" : mode === "timed" ? "Timed Exam" : "Practice"} (${unservedPool.length} unserved Qs) →`}
        </button>
      </div>

      {/* 5.5 Feature C2: Continuous Performance Trend Charts */}
      <PerformanceTrendCharts />

      {/* 6. Specialised Learning Tools */}
      <div className="space-y-4 pt-2">
        <h2 className="text-xs font-extrabold uppercase tracking-widest text-text-muted">
          Specialised Learning Tools
        </h2>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          <Link
            href="/dashboard/notebook"
            className="p-4 rounded-2xl bg-card-primary border border-border-charcoal hover:border-brand-red/50 transition-all group flex flex-col justify-between shadow-card hover:-translate-y-0.5"
          >
            <div>
              <div className="text-2xl mb-2">📓</div>
              <div className="text-sm font-bold text-text-primary group-hover:text-brand-red">Mistake Notebook</div>
              <p className="text-xs text-text-muted mt-1 leading-relaxed">Target &amp; revise previous mistakes</p>
            </div>
            <span className="text-xs text-brand-red mt-3 font-bold">Open &rarr;</span>
          </Link>

          <Link
            href="/dashboard/revision"
            className="p-4 rounded-2xl bg-card-primary border border-border-charcoal hover:border-brand-teal/50 transition-all group flex flex-col justify-between shadow-card hover:-translate-y-0.5"
          >
            <div>
              <div className="text-2xl mb-2">🔄</div>
              <div className="text-sm font-bold text-text-primary group-hover:text-brand-teal">Spaced Revision</div>
              <p className="text-xs text-text-muted mt-1 leading-relaxed">Interval retention algorithm</p>
            </div>
            <span className="text-xs text-brand-teal mt-3 font-bold">Open &rarr;</span>
          </Link>

          <Link
            href="/dashboard/readiness"
            className="p-4 rounded-2xl bg-card-primary border border-border-charcoal hover:border-brand-gold/50 transition-all group flex flex-col justify-between shadow-card hover:-translate-y-0.5"
          >
            <div>
              <div className="text-2xl mb-2">📊</div>
              <div className="text-sm font-bold text-text-primary group-hover:text-brand-gold">Exam Readiness</div>
              <p className="text-xs text-text-muted mt-1 leading-relaxed">Predicted pass probability</p>
            </div>
            <span className="text-xs text-brand-gold mt-3 font-bold">Open &rarr;</span>
          </Link>

          <Link
            href="/dashboard/planner"
            className="p-4 rounded-2xl bg-card-primary border border-border-charcoal hover:border-brand-blue/50 transition-all group flex flex-col justify-between shadow-card hover:-translate-y-0.5"
          >
            <div>
              <div className="text-2xl mb-2">📅</div>
              <div className="text-sm font-bold text-text-primary group-hover:text-brand-blue">Study Planner</div>
              <p className="text-xs text-text-muted mt-1 leading-relaxed">Topic schedule &amp; timeline</p>
            </div>
            <span className="text-xs text-brand-blue mt-3 font-bold">Open &rarr;</span>
          </Link>

          <Link
            href="/dashboard/library"
            className="p-4 rounded-2xl bg-card-primary border border-border-charcoal hover:border-brand-blue/50 transition-all group flex flex-col justify-between shadow-card hover:-translate-y-0.5"
          >
            <div>
              <div className="text-2xl mb-2">📚</div>
              <div className="text-sm font-bold text-text-primary group-hover:text-brand-blue">Reference Library</div>
              <p className="text-xs text-text-muted mt-1 leading-relaxed">CARs, syllabi &amp; I.C. Joshi</p>
            </div>
            <span className="text-xs text-brand-blue mt-3 font-bold">Open &rarr;</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
