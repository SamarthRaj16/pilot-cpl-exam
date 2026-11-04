"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import rawQuestions from "@/data/questions.json";

const SUBJECTS_INFO = [
  {
    name: "Air Navigation",
    code: "CAR SEC 7",
    color: "#719CFF",
    icon: "🧭",
    topics: 25,
    qCount: 298,
    desc: "General Navigation, Chart Projections, Instrumentation, Dead Reckoning & PNR/CP.",
  },
  {
    name: "Air Regulations",
    code: "ICAO / CAR",
    color: "#9484F5",
    icon: "📜",
    topics: 25,
    qCount: 300,
    desc: "Aircraft Rules 1937, Bharatiya Vayuyan Adhiniyam 2024, Airspace & Aerodromes.",
  },
  {
    name: "Aviation Meteorology",
    code: "I.C. JOSHI",
    color: "#51C6C1",
    icon: "⛅",
    topics: 18,
    qCount: 93,
    desc: "Atmospheric Pressure, Wind Systems, Monsoon Dynamics, Icing, METAR & TAF.",
  },
  {
    name: "Technical General",
    code: "AGK / ENGINES",
    color: "#69CF9B",
    icon: "⚙️",
    topics: 9,
    qCount: 59,
    desc: "Principles of Flight, Piston Engines, Hydraulics, Propellers & Flight Instruments.",
  },
  {
    name: "Technical Specific",
    code: "POH / PERF",
    color: "#ECA85B",
    icon: "🛩️",
    topics: 7,
    qCount: 42,
    desc: "Light Aircraft POH, V-speeds, Limitations, Fuel & Altimetry Procedures.",
  },
  {
    name: "RTR",
    code: "ICAO DOC 9432",
    color: "#51C6C1",
    icon: "🎙️",
    topics: 10,
    qCount: 47,
    desc: "Radio Telephony Restricted, Phraseology, Distress/Urgency, & VHF Propagation.",
  },
];

export default function DashboardPage() {
  const router = useRouter();

  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string>("");
  const [mode, setMode] = useState<"practice" | "timed" | "mock">("practice");
  const [servedIds, setServedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);

  // Load served IDs from localStorage for client Zero-Repeat tracking
  useEffect(() => {
    try {
      const stored = localStorage.getItem("cpl_served_ids");
      if (stored) {
        setServedIds(new Set(JSON.parse(stored)));
      }
    } catch {
      // Ignored
    }
  }, []);

  const totalBankCount = rawQuestions.length; // 839

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
    } catch {
      // Ignored
    }
  };

  const handleStartExam = () => {
    setLoading(true);
    // If exhausted, auto reset first
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
      {/* Hero Banners */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-6 rounded-2xl bg-gradient-to-br from-[#182824] to-card-primary border border-brand-teal/30 flex flex-col justify-between min-h-[140px] shadow-card">
          <div>
            <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              <span className="text-brand-teal flex items-center gap-1.5">
                ✨ Continue where you left off
              </span>
              <span>Daily Practice</span>
            </div>
            <h2 className="text-2xl font-extrabold text-white">Air Navigation</h2>
            <p className="text-sm text-text-secondary mt-1">General Navigation &bull; 298 Verified Questions</p>
          </div>
          <div className="flex items-center justify-between mt-4">
            <button
              onClick={() => {
                setSelectedSubjects(["Air Navigation"]);
                setMode("practice");
                handleStartExam();
              }}
              className="text-xs font-bold text-brand-teal hover:underline flex items-center gap-1"
            >
              Start Practice Session &rarr;
            </button>
            <span className="text-xs text-text-muted">CAR SEC 7 Standard</span>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-gradient-to-br from-[#261e38] to-card-primary border border-brand-purple/30 flex flex-col justify-between min-h-[140px] shadow-card">
          <div>
            <div className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-text-muted mb-2">
              <span className="text-brand-purple flex items-center gap-1.5">
                📊 Complete CBT Simulation
              </span>
              <span>Full Paper</span>
            </div>
            <h2 className="text-2xl font-extrabold text-white">DGCA Mock Exam Hub</h2>
            <p className="text-sm text-text-secondary mt-1">
              70% Passing Threshold &bull; Authentic Timers &bull; 0 Negative Marking
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
            <span className="text-xs text-text-muted">Valid for 5 Years</span>
          </div>
        </div>
      </div>

      {/* Examination Setup & Zero-Repeat Controls */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-6">
        <div>
          <h3 className="text-lg font-extrabold text-white">Examination & Practice Setup</h3>
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
          {SUBJECTS_INFO.map((subj) => {
            const isSelected = selectedSubjects.includes(subj.name);
            const subjQuestions = rawQuestions.filter((q: any) => q.subject === subj.name);
            const unservedInSubj = subjQuestions.filter((q: any) => !servedIds.has(q.id)).length;
            const completionPct = Math.round(
              ((subj.qCount - unservedInSubj) / subj.qCount) * 100
            );

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
                      {unservedInSubj} unserved / {subj.qCount} Qs
                    </span>
                    <span className="text-brand-purple">{completionPct}% Completed</span>
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

