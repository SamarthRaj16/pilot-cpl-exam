"use client";

export const dynamic = "force-dynamic";

import React, { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import rawQuestions from "@/data/questions.json";

const BASE_SUBJECTS_METADATA = [
  {
    name: "Air Navigation",
    code: "CAR SEC 7",
    color: "#719CFF",
    icon: "🧭",
    desc: "General Navigation, Chart Projections, Instrumentation, Dead Reckoning & PNR/CP.",
  },
  {
    name: "Air Regulations",
    code: "ICAO / CAR",
    color: "#9484F5",
    icon: "📜",
    desc: "Aircraft Rules 1937, Bharatiya Vayuyan Adhiniyam 2024, Airspace & Aerodromes.",
  },
  {
    name: "Aviation Meteorology",
    code: "I.C. JOSHI 3RD ED",
    color: "#51C6C1",
    icon: "⛅",
    desc: "Atmospheric Pressure, Wind Systems, Monsoon Dynamics, Icing, METAR & TAF.",
  },
  {
    name: "Technical General",
    code: "AGK / ENGINES",
    color: "#69CF9B",
    icon: "⚙️",
    desc: "Principles of Flight, Piston Engines, Hydraulics, Propellers & Flight Instruments.",
  },
  {
    name: "Technical Specific",
    code: "POH / PERF",
    color: "#ECA85B",
    icon: "🛩️",
    desc: "Light Aircraft POH, V-speeds, Limitations, Fuel & Altimetry Procedures.",
  },
  {
    name: "RTR",
    code: "ICAO DOC 9432",
    color: "#51C6C1",
    icon: "🎙️",
    desc: "Radio Telephony Restricted, Phraseology, Distress/Urgency, & VHF Propagation.",
  },
];

export default function DashboardPage() {
  const router = useRouter();

  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string>("");
  const [mode, setMode] = useState<"practice" | "timed" | "mock">("practice");
  const [servedIds, setServedIds] = useState<Set<string>>(new Set());
  const [activeMistakes, setActiveMistakes] = useState<number>(0);
  const [recoveredCount, setRecoveredCount] = useState<number>(0);
  const [loading, setLoading] = useState(false);

  // Compute live counts per subject directly from the authoritative question bank
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

  // Load served IDs and mistakes from localStorage for client Zero-Repeat & Revision tracking
  useEffect(() => {
    try {
      const stored = localStorage.getItem("cpl_served_ids");
      if (stored) {
        setServedIds(new Set(JSON.parse(stored)));
      }
    } catch {}

    try {
      const storedMistakes = localStorage.getItem("cpl_mistakes");
      if (storedMistakes) {
        const parsed = JSON.parse(storedMistakes);
        const entries = Object.values(parsed) as any[];
        const active = entries.filter((e) => e.status === "active").length;
        const recovered = entries.filter((e) => e.status === "resolved").length;
        setActiveMistakes(active);
        setRecoveredCount(recovered);
      }
    } catch {}
  }, []);

  const totalBankCount = rawQuestions.length; // 959

  // Filter pool
  const candidatePool = rawQuestions.filter((q: any) => {
    if (selectedSubjects.length > 0 && !selectedSubjects.includes(q.subject)) return false;
    if (selectedTopic && q.topic !== selectedTopic) return false;
    return true;
  });

  const unservedPool = candidatePool.filter((q: any) => !servedIds.has(q.id));
  const isExhausted = unservedPool.length === 0 && candidatePool.length > 0;

  // Available topics for selected subjects
  const availableTopics = Array.from(
    new Set(
      rawQuestions
        .filter((q: any) => selectedSubjects.length === 0 || selectedSubjects.includes(q.subject))
        .map((q: any) => q.topic)
    )
  ).sort();

  const handleToggleSubject = (subjName: string) => {
    if (selectedSubjects.includes(subjName)) {
      setSelectedSubjects(selectedSubjects.filter((s) => s !== subjName));
    } else {
      setSelectedSubjects([...selectedSubjects, subjName]);
    }
  };

  const handleSelectAllSubjects = () => {
    setSelectedSubjects([]);
    setSelectedTopic("");
  };

  const handleResetRotation = () => {
    const newSet = new Set(servedIds);
    candidatePool.forEach((q: any) => newSet.delete(q.id));
    setServedIds(newSet);
    try {
      localStorage.setItem("cpl_served_ids", JSON.stringify(Array.from(newSet)));
    } catch {}
  };

  const handleStartExam = () => {
    setLoading(true);
    if (isExhausted) {
      handleResetRotation();
    }

    const queryParams = new URLSearchParams();
    if (selectedSubjects.length > 0) {
      queryParams.set("subjects", selectedSubjects.join(","));
    }
    if (selectedTopic) {
      queryParams.set("topic", selectedTopic);
    }
    queryParams.set("mode", mode);

    router.push(`/dashboard/exam?${queryParams.toString()}`);
  };

  return (
    <div className="space-y-8">
      {/* Phase 1.5 Feature Highlight: Custom Practice Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-[#201d3a] via-[#1a2336] to-[#162725] border border-brand-purple/40 shadow-glow flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-extrabold uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-brand-purple/20 text-brand-purple border border-brand-purple/40">
              ⚡ Multi-Topic Quiz Builder
            </span>
            <span className="text-xs text-text-muted">&bull; Up to 50 Qs</span>
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">
            Custom Practice &amp; Smart Revision Engine
          </h2>
          <p className="text-sm text-text-secondary max-w-2xl">
            Select multiple subjects and specific chapters simultaneously. Automatically mixes unserved questions with your active mistake revision queue (up to 20 revision slots) for maximum retention.
          </p>
        </div>
        <div className="flex items-center gap-3 w-full md:w-auto">
          <button
            onClick={() => router.push("/dashboard/custom-practice")}
            className="w-full md:w-auto px-6 py-3.5 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white font-black text-sm shadow-glow transition-all flex items-center justify-center gap-2 whitespace-nowrap"
          >
            <span>🎯 Open Custom Practice</span>
            <span>&rarr;</span>
          </button>
        </div>
      </div>

      {/* Revision & Mistake Recovery Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-card-primary border border-border-charcoal">
          <div className="text-[10px] uppercase font-bold tracking-wider text-text-muted mb-1">
            Question Bank
          </div>
          <div className="text-2xl font-black text-white">{totalBankCount}</div>
          <div className="text-xs text-text-secondary mt-1">Across 6 DGCA Subjects</div>
        </div>

        <div className="p-4 rounded-xl bg-card-primary border border-border-charcoal">
          <div className="text-[10px] uppercase font-bold tracking-wider text-text-muted mb-1">
            Zero-Repeat Seen
          </div>
          <div className="text-2xl font-black text-brand-blue">{servedIds.size}</div>
          <div className="text-xs text-text-secondary mt-1">
            {Math.round((servedIds.size / totalBankCount) * 100)}% bank exposure
          </div>
        </div>

        <div className="p-4 rounded-xl bg-card-primary border border-border-charcoal">
          <div className="text-[10px] uppercase font-bold tracking-wider text-text-muted mb-1">
            Pending Mistakes
          </div>
          <div className="text-2xl font-black text-brand-red">{activeMistakes}</div>
          <div className="text-xs text-text-secondary mt-1">Awaiting Smart Revision</div>
        </div>

        <div className="p-4 rounded-xl bg-card-primary border border-border-charcoal">
          <div className="text-[10px] uppercase font-bold tracking-wider text-text-muted mb-1">
            Recovered Questions
          </div>
          <div className="text-2xl font-black text-brand-green">{recoveredCount}</div>
          <div className="text-xs text-text-secondary mt-1">Mastered after mistake</div>
        </div>
      </div>

      {/* Quick Launch Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-6 rounded-2xl bg-gradient-to-br from-[#182824] to-card-primary border border-brand-teal/30 flex flex-col justify-between min-h-[140px] shadow-card">
          <div>
            <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              <span className="text-brand-teal flex items-center gap-1.5">
                ⛅ Expanded Question Bank
              </span>
              <span>I.C. Joshi 3rd Ed</span>
            </div>
            <h3 className="text-xl font-extrabold text-white">Aviation Meteorology</h3>
            <p className="text-xs text-text-secondary mt-1">
              Expanded to 213 verified questions &bull; 20 syllabus topics &bull; Monsoons, Altimetry, Radar
            </p>
          </div>
          <div className="flex items-center justify-between mt-4">
            <button
              onClick={() => {
                setSelectedSubjects(["Aviation Meteorology"]);
                setMode("practice");
                handleStartExam();
              }}
              className="text-xs font-bold text-brand-teal hover:underline flex items-center gap-1"
            >
              Start Meteorology Practice &rarr;
            </button>
            <span className="text-xs text-text-muted">213 Verified Qs</span>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-gradient-to-br from-[#261e38] to-card-primary border border-brand-purple/30 flex flex-col justify-between min-h-[140px] shadow-card">
          <div>
            <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              <span className="text-brand-purple flex items-center gap-1.5">
                📊 DGCA CBT Simulation
              </span>
              <span>Official Format</span>
            </div>
            <h3 className="text-xl font-extrabold text-white">Full Mock Examination</h3>
            <p className="text-xs text-text-secondary mt-1">
              50 Questions &bull; 70% Passing Threshold &bull; Authentic Timers &bull; Zero Negative Marking
            </p>
          </div>
          <div className="flex items-center justify-between mt-4">
            <button
              onClick={() => {
                setMode("mock");
                handleStartExam();
              }}
              className="text-xs font-bold text-brand-purple hover:underline flex items-center gap-1"
            >
              Launch DGCA Mock Exam &rarr;
            </button>
            <span className="text-xs text-text-muted">Timed CBT Interface</span>
          </div>
        </div>
      </div>

      {/* Examination Setup & Zero-Repeat Controls */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-6">
        <div>
          <h3 className="text-lg font-extrabold text-white">Quick Exam Launcher</h3>
          <p className="text-xs text-text-muted">
            Configure examination mode, target subjects, and chapter filters
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Examination Mode
            </label>
            <div className="flex gap-2 p-1 bg-card-elevated border border-border-charcoal rounded-xl">
              <button
                type="button"
                onClick={() => setMode("practice")}
                className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
                  mode === "practice"
                    ? "bg-brand-purple text-white shadow-glow"
                    : "text-text-secondary hover:text-white"
                }`}
              >
                Practice Mode
              </button>
              <button
                type="button"
                onClick={() => setMode("timed")}
                className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
                  mode === "timed"
                    ? "bg-brand-purple text-white shadow-glow"
                    : "text-text-secondary hover:text-white"
                }`}
              >
                Timed Exam
              </button>
              <button
                type="button"
                onClick={() => setMode("mock")}
                className={`flex-1 py-2.5 rounded-lg text-xs font-bold transition-all ${
                  mode === "mock"
                    ? "bg-brand-purple text-white shadow-glow"
                    : "text-text-secondary hover:text-white"
                }`}
              >
                DGCA Mock
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              Topic / Chapter Filter ({availableTopics.length} available)
            </label>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="w-full px-4 py-2.5 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary text-xs font-semibold focus:outline-none focus:border-brand-purple"
            >
              <option value="">All Topics in selected subjects</option>
              {availableTopics.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Zero-Repeat Status Banner */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 rounded-xl bg-surface-interactive border border-border-charcoal text-xs">
          <div className="flex items-center gap-2 text-brand-teal font-bold">
            <span>🔄 Zero-Repeat Rotation Engine:</span>
            <span className="text-text-primary">
              {unservedPool.length} unserved of {candidatePool.length} available questions
            </span>
          </div>
          <button
            onClick={handleResetRotation}
            type="button"
            className="text-brand-orange hover:bg-brand-orange/10 px-3 py-1.5 rounded-lg border border-brand-orange/30 font-bold transition-all"
          >
            Reset Exposure for Selection
          </button>
        </div>

        <button
          onClick={handleStartExam}
          disabled={loading || candidatePool.length === 0}
          className="w-full py-4 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white font-extrabold text-base shadow-card hover:shadow-glow transition-all flex items-center justify-center gap-2"
        >
          {isExhausted
            ? `Pool Completed! Click to Reset & Retake (${candidatePool.length} Qs)`
            : `Start ${mode === "mock" ? "Mock Exam" : mode === "timed" ? "Timed Exam" : "Practice"} (${unservedPool.length} unserved Qs)`}
        </button>
      </div>

      {/* DGCA CPL Subject Selection Cards */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-extrabold text-white">DGCA CPL Subjects</h3>
            <p className="text-xs text-text-muted">
              Select one or more subjects to focus your question bank
            </p>
          </div>
          <button
            onClick={handleSelectAllSubjects}
            className={`text-xs font-bold px-3 py-1.5 rounded-lg border transition-all ${
              selectedSubjects.length === 0
                ? "bg-brand-purple/20 text-brand-purple border-brand-purple/40"
                : "border-border-charcoal text-text-secondary hover:text-white"
            }`}
          >
            Select All Subjects
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
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
                className={`p-5 rounded-2xl bg-card-primary border cursor-pointer transition-all flex flex-col justify-between min-h-[170px] shadow-card hover:-translate-y-1 ${
                  isSelected
                    ? "border-brand-purple ring-2 ring-brand-purple/40 shadow-glow"
                    : "border-border-charcoal hover:border-brand-purple/50"
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-2xl">{subj.icon}</span>
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-card-elevated border border-border-charcoal text-text-muted">
                      {subj.code}
                    </span>
                  </div>
                  <h4 className="text-base font-extrabold text-white mb-1">{subj.name}</h4>
                  <p className="text-xs text-text-secondary line-clamp-2">{subj.desc}</p>
                </div>

                <div className="mt-4 pt-3 border-t border-border-charcoal/50">
                  <div className="flex items-center justify-between text-xs text-text-muted font-bold mb-1.5">
                    <span>
                      {unservedInSubj} unserved / {totalInSubj} Qs &bull; {topicCount} Topics
                    </span>
                    <span className="text-brand-purple">{completionPct}%</span>
                  </div>
                  <div className="w-full h-1.5 bg-surface-interactive rounded-full overflow-hidden">
                    <div
                      className="h-full bg-brand-purple transition-all duration-500 rounded-full"
                      style={{ width: `${completionPct}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
