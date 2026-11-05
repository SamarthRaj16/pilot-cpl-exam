"use client";

export const dynamic = "force-dynamic";

import React, { useState, useEffect, useMemo, Suspense } from "react";
import Link from "next/link";
import syllabusData from "@/data/syllabusHierarchy.json";
import { createClient } from "@/lib/supabase/client";

interface TopicProgress {
  subject_name: string;
  topic_name: string;
  theory_completed: boolean;
  practice_completed: boolean;
  mock_completed: boolean;
  notes?: string | null;
  updated_at?: string;
}

export default function SyllabusTrackerPage() {
  const [progressMap, setProgressMap] = useState<Record<string, TopicProgress>>({});
  const [activeSubject, setActiveSubject] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [filterMode, setFilterMode] = useState<"all" | "incomplete" | "completed">("all");
  const [expandedSubjects, setExpandedSubjects] = useState<Record<string, boolean>>({
    "Air Navigation": true,
    "Air Regulations": true,
    "Aviation Meteorology": true,
    "Technical General": true,
    "Technical Specific": true,
    "RTR": true,
  });

  // Notes Modal state
  const [activeNoteTopic, setActiveNoteTopic] = useState<{
    subject: string;
    topic: string;
    notes: string;
  } | null>(null);
  const [isSavingNote, setIsSavingNote] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [user, setUser] = useState<any>(null);

  // Load progress from localStorage and Supabase on mount
  useEffect(() => {
    // 1. Initial local load
    try {
      const stored = localStorage.getItem("cpl_syllabus_progress");
      if (stored) {
        setProgressMap(JSON.parse(stored));
      }
    } catch (e) {
      console.warn("Failed to read local syllabus cache", e);
    }

    // 2. Fetch from Supabase API
    async function loadRemoteProgress() {
      try {
        const supabase = createClient();
        const {
          data: { user: authUser },
        } = await supabase.auth.getUser();

        if (authUser) {
          setUser(authUser);
          const res = await fetch("/api/syllabus");
          if (res.ok) {
            const data = await res.json();
            if (Array.isArray(data.progress)) {
              const remoteMap: Record<string, TopicProgress> = {};
              data.progress.forEach((item: any) => {
                const key = `${item.subject_name}:::${item.topic_name}`;
                remoteMap[key] = {
                  subject_name: item.subject_name,
                  topic_name: item.topic_name,
                  theory_completed: !!item.theory_completed,
                  practice_completed: !!item.practice_completed,
                  mock_completed: !!item.mock_completed,
                  notes: item.notes || null,
                  updated_at: item.updated_at,
                };
              });

              // Merge local + remote
              setProgressMap((prev) => {
                const merged = { ...prev, ...remoteMap };
                try {
                  localStorage.setItem("cpl_syllabus_progress", JSON.stringify(merged));
                } catch {}
                return merged;
              });
            }
          }
        }
      } catch (err) {
        console.warn("Offline or unauthenticated syllabus mode", err);
      }
    }
    loadRemoteProgress();
  }, []);

  const totalTopics = 95;
  const totalChecklistItems = totalTopics * 3; // 285

  // Calculate Metrics
  const metrics = useMemo(() => {
    let completedTheory = 0;
    let completedPractice = 0;
    let completedMock = 0;
    let fullyCompletedTopics = 0;

    syllabusData.forEach((s) => {
      s.topics.forEach((t) => {
        const key = `${s.name}:::${t.name}`;
        const p = progressMap[key];
        const tDone = p?.theory_completed || false;
        const pDone = p?.practice_completed || false;
        const mDone = p?.mock_completed || false;

        if (tDone) completedTheory += 1;
        if (pDone) completedPractice += 1;
        if (mDone) completedMock += 1;
        if (tDone && pDone && mDone) fullyCompletedTopics += 1;
      });
    });

    const totalCompleted = completedTheory + completedPractice + completedMock;
    const overallPct = Math.round((totalCompleted / totalChecklistItems) * 100);
    const theoryPct = Math.round((completedTheory / totalTopics) * 100);
    const practicePct = Math.round((completedPractice / totalTopics) * 100);
    const mockPct = Math.round((completedMock / totalTopics) * 100);

    return {
      totalCompleted,
      overallPct,
      completedTheory,
      theoryPct,
      completedPractice,
      practicePct,
      completedMock,
      mockPct,
      fullyCompletedTopics,
    };
  }, [progressMap, totalChecklistItems, totalTopics]);

  // Subject Stats & Lowest Completion Subject Finder
  const subjectStats = useMemo(() => {
    return syllabusData.map((s) => {
      let subjectCompleted = 0;
      const subTotal = s.topics.length * 3;

      s.topics.forEach((t) => {
        const key = `${s.name}:::${t.name}`;
        const p = progressMap[key];
        if (p?.theory_completed) subjectCompleted += 1;
        if (p?.practice_completed) subjectCompleted += 1;
        if (p?.mock_completed) subjectCompleted += 1;
      });

      const pct = subTotal > 0 ? Math.round((subjectCompleted / subTotal) * 100) : 0;
      return {
        ...s,
        completedItems: subjectCompleted,
        totalItems: subTotal,
        percentage: pct,
      };
    });
  }, [progressMap]);

  const lowestSubject = useMemo(() => {
    if (subjectStats.length === 0) return null;
    return [...subjectStats].sort((a, b) => a.percentage - b.percentage)[0];
  }, [subjectStats]);

  // Toggle Checklist Checkbox
  const handleToggle = async (
    subject: string,
    topic: string,
    type: "theory_completed" | "practice_completed" | "mock_completed"
  ) => {
    const key = `${subject}:::${topic}`;
    const current = progressMap[key] || {
      subject_name: subject,
      topic_name: topic,
      theory_completed: false,
      practice_completed: false,
      mock_completed: false,
      notes: null,
    };

    const updated: TopicProgress = {
      ...current,
      [type]: !current[type],
      updated_at: new Date().toISOString(),
    };

    const nextMap = { ...progressMap, [key]: updated };
    setProgressMap(nextMap);

    // Persist locally
    try {
      localStorage.setItem("cpl_syllabus_progress", JSON.stringify(nextMap));
    } catch {}

    // Async sync to API
    try {
      setIsSyncing(true);
      await fetch("/api/syllabus", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });
    } catch (err) {
      console.warn("Background syllabus sync failed", err);
    } finally {
      setIsSyncing(false);
    }
  };

  // Save Note
  const handleSaveNote = async () => {
    if (!activeNoteTopic) return;
    setIsSavingNote(true);
    const { subject, topic, notes } = activeNoteTopic;
    const key = `${subject}:::${topic}`;
    const current = progressMap[key] || {
      subject_name: subject,
      topic_name: topic,
      theory_completed: false,
      practice_completed: false,
      mock_completed: false,
    };

    const updated: TopicProgress = {
      ...current,
      notes,
      updated_at: new Date().toISOString(),
    };

    const nextMap = { ...progressMap, [key]: updated };
    setProgressMap(nextMap);

    try {
      localStorage.setItem("cpl_syllabus_progress", JSON.stringify(nextMap));
      await fetch("/api/syllabus", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updated),
      });
    } catch {}
    setIsSavingNote(false);
    setActiveNoteTopic(null);
  };

  const toggleSubjectExpand = (sName: string) => {
    setExpandedSubjects((prev) => ({ ...prev, [sName]: !prev[sName] }));
  };

  // Filtered Subject List
  const filteredSubjects = useMemo(() => {
    return subjectStats
      .filter((s) => activeSubject === "all" || s.name === activeSubject)
      .map((s) => {
        const filteredTopics = s.topics.filter((t) => {
          if (searchQuery.trim() && !t.name.toLowerCase().includes(searchQuery.toLowerCase())) {
            return false;
          }
          const key = `${s.name}:::${t.name}`;
          const p = progressMap[key];
          const isComplete = p?.theory_completed && p?.practice_completed && p?.mock_completed;
          if (filterMode === "completed" && !isComplete) return false;
          if (filterMode === "incomplete" && isComplete) return false;
          return true;
        });
        return {
          ...s,
          filteredTopics,
        };
      })
      .filter((s) => s.filteredTopics.length > 0 || !searchQuery.trim());
  }, [subjectStats, activeSubject, searchQuery, filterMode, progressMap]);

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Top Header & Breadcrumbs */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border-charcoal pb-6">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-text-muted mb-1 uppercase tracking-widest">
            <Link href="/dashboard" className="hover:text-brand-blue">
              Dashboard
            </Link>
            <span>/</span>
            <span className="text-brand-blue">Interactive Syllabus Tracker</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-black text-text-primary tracking-tight">
            DGCA CPL Syllabus Completion Tracker
          </h1>
          <p className="text-xs md:text-sm text-text-secondary mt-1 max-w-2xl">
            Track Theory review, Practice Question mastery, and Mock Examinations for every topic
            across all 6 DGCA Commercial Pilot Licence subjects.
          </p>
        </div>

        {/* Sync Status Badge */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-[10px] uppercase font-bold text-text-muted tracking-wider">
              Sync Mode
            </div>
            <div className="text-xs font-bold text-text-primary flex items-center justify-end gap-1.5">
              <span className={`w-2 h-2 rounded-full ${user ? "bg-semantic-success" : "bg-semantic-warning animate-pulse"}`}></span>
              {user ? "Cloud Sync (Supabase)" : "Local Storage (Guest)"}
            </div>
          </div>
          {lowestSubject && (
            <Link
              href={`#subject-${lowestSubject.slug}`}
              className="px-4 py-2 rounded-xl bg-brand-blue text-bg-main text-xs font-black shadow-card hover:bg-opacity-90 transition-all flex items-center gap-1.5"
            >
              Continue Syllabus →
            </Link>
          )}
        </div>
      </div>

      {/* Hero Overview: Mathematics Card */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 bg-card-primary p-6 md:p-8 rounded-2xl border border-border-charcoal relative overflow-hidden">
        {/* Overall Completion Ring & Main Stats */}
        <div className="lg:col-span-5 flex flex-col sm:flex-row items-center gap-6 border-b lg:border-b-0 lg:border-r border-border-charcoal pb-6 lg:pb-0 lg:pr-6">
          {/* Circular SVG Progress */}
          <div className="relative w-36 h-36 flex-shrink-0 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
              <circle
                cx="60"
                cy="60"
                r="50"
                className="stroke-surface-interactive"
                strokeWidth="10"
                fill="transparent"
              />
              <circle
                cx="60"
                cy="60"
                r="50"
                className="stroke-brand-blue transition-all duration-700 ease-out"
                strokeWidth="10"
                strokeDasharray={314.159}
                strokeDashoffset={314.159 - (314.159 * metrics.overallPct) / 100}
                strokeLinecap="round"
                fill="transparent"
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
              <span className="text-3xl font-black text-text-primary">{metrics.overallPct}%</span>
              <span className="text-[10px] font-bold text-text-muted uppercase tracking-wider">
                Overall
              </span>
            </div>
          </div>

          <div className="space-y-2 text-center sm:text-left">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-brand-blue/10 border border-brand-blue/20 text-brand-blue text-[11px] font-bold">
              <span>✈️</span> DGCA Coverage Math
            </div>
            <div className="text-xl font-bold text-text-primary">
              {metrics.totalCompleted}{" "}
              <span className="text-xs font-normal text-text-muted">
                / {totalChecklistItems} checklist items completed
              </span>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              Calculated across <strong>95 DGCA topics</strong> with 3 checklist milestones per topic (Theory, Practice, Mock).
            </p>
            <div className="text-xs text-semantic-teal font-semibold">
              ✓ {metrics.fullyCompletedTopics} of 95 topics fully mastered (all 3 complete)
            </div>
          </div>
        </div>

        {/* Category Progress Breakdown Bars */}
        <div className="lg:col-span-7 flex flex-col justify-center space-y-4">
          <div className="text-xs font-bold text-text-muted uppercase tracking-wider">
            Three Milestone Pillars
          </div>

          {/* Theory Bar */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <span className="font-bold text-text-primary flex items-center gap-1.5">
                <span>📚</span> Theory Study Checklist
              </span>
              <span className="font-mono text-text-secondary">
                {metrics.completedTheory} / {totalTopics} ({metrics.theoryPct}%)
              </span>
            </div>
            <div className="w-full bg-surface-interactive h-2.5 rounded-full overflow-hidden">
              <div
                className="bg-brand-blue h-full rounded-full transition-all duration-500"
                style={{ width: `${metrics.theoryPct}%` }}
              ></div>
            </div>
          </div>

          {/* Practice Bar */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <span className="font-bold text-text-primary flex items-center gap-1.5">
                <span>✍️</span> Practice Question Bank Mastery
              </span>
              <span className="font-mono text-text-secondary">
                {metrics.completedPractice} / {totalTopics} ({metrics.practicePct}%)
              </span>
            </div>
            <div className="w-full bg-surface-interactive h-2.5 rounded-full overflow-hidden">
              <div
                className="bg-semantic-teal h-full rounded-full transition-all duration-500"
                style={{ width: `${metrics.practicePct}%` }}
              ></div>
            </div>
          </div>

          {/* Mock Bar */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <span className="font-bold text-text-primary flex items-center gap-1.5">
                <span>🎯</span> Mock Examination Checklist
              </span>
              <span className="font-mono text-text-secondary">
                {metrics.completedMock} / {totalTopics} ({metrics.mockPct}%)
              </span>
            </div>
            <div className="w-full bg-surface-interactive h-2.5 rounded-full overflow-hidden">
              <div
                className="bg-brand-gold h-full rounded-full transition-all duration-500"
                style={{ width: `${metrics.mockPct}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* 6 Subject Summary Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {subjectStats.map((sub) => {
          const isLowest = lowestSubject && lowestSubject.name === sub.name;
          return (
            <div
              key={sub.name}
              id={`subject-${sub.slug}`}
              className={`p-5 rounded-2xl bg-card-primary border transition-all ${
                isLowest
                  ? "border-brand-gold/60 ring-1 ring-brand-gold/40 shadow-glow"
                  : "border-border-charcoal hover:border-brand-blue/50"
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <span className="text-2xl">{sub.meta.icon}</span>
                  <div>
                    <h3 className="font-bold text-sm text-text-primary">{sub.name}</h3>
                    <span className="text-[10px] font-mono text-text-muted">{sub.meta.code}</span>
                  </div>
                </div>
                {isLowest && (
                  <span className="px-2 py-0.5 rounded-full bg-brand-gold/20 text-brand-gold text-[10px] font-extrabold uppercase tracking-wider">
                    Lowest Completion
                  </span>
                )}
              </div>

              <div className="mt-4 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-text-secondary">{sub.completedItems} / {sub.totalItems} done</span>
                  <span className="font-bold text-text-primary">{sub.percentage}%</span>
                </div>
                <div className="w-full bg-surface-interactive h-2 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${sub.percentage}%`,
                      backgroundColor: sub.meta.color || "#48A9FF",
                    }}
                  ></div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-border-charcoal/60 flex items-center justify-between text-xs">
                <span className="text-text-muted text-[11px]">
                  {sub.topics.length} topics • {sub.question_count} questions
                </span>
                <Link
                  href={`/dashboard/syllabus/${sub.slug}`}
                  className="text-brand-blue hover:underline font-bold text-xs"
                >
                  View Subject →
                </Link>
              </div>
            </div>
          );
        })}
      </div>

      {/* Filter & Search Bar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 bg-card-primary p-4 rounded-xl border border-border-charcoal">
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setActiveSubject("all")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeSubject === "all"
                ? "bg-brand-blue text-bg-main shadow-card"
                : "bg-surface-interactive text-text-secondary hover:text-white"
            }`}
          >
            All Subjects (95 Topics)
          </button>
          {syllabusData.map((s) => (
            <button
              key={s.name}
              onClick={() => setActiveSubject(s.name)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                activeSubject === s.name
                  ? "bg-brand-blue text-bg-main shadow-card"
                  : "bg-surface-interactive text-text-secondary hover:text-white"
              }`}
            >
              {s.name}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <input
            type="text"
            placeholder="Search topic name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-surface-interactive border border-border-charcoal text-text-primary placeholder-text-muted text-xs focus:outline-none focus:border-brand-blue w-full md:w-56"
          />
          <select
            value={filterMode}
            onChange={(e: any) => setFilterMode(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-surface-interactive border border-border-charcoal text-text-secondary text-xs focus:outline-none focus:border-brand-blue"
          >
            <option value="all">All Topics</option>
            <option value="incomplete">Incomplete Only</option>
            <option value="completed">Fully Completed Only</option>
          </select>
        </div>
      </div>

      {/* Accordion List by Subject */}
      <div className="space-y-6">
        {filteredSubjects.map((sub) => {
          const isExpanded = expandedSubjects[sub.name] !== false;
          return (
            <div
              key={sub.name}
              className="bg-card-primary rounded-2xl border border-border-charcoal overflow-hidden shadow-card"
            >
              {/* Subject Accordion Header */}
              <div
                onClick={() => toggleSubjectExpand(sub.name)}
                className="p-5 flex items-center justify-between cursor-pointer hover:bg-card-elevated transition-all border-b border-border-charcoal"
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{sub.meta.icon}</span>
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="text-base font-bold text-text-primary">{sub.name}</h2>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-surface-interactive text-text-muted">
                        {sub.meta.code}
                      </span>
                    </div>
                    <p className="text-xs text-text-secondary mt-0.5">
                      {sub.filteredTopics.length} topics shown • {sub.completedItems} / {sub.totalItems} checklist items done ({sub.percentage}%)
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="hidden sm:block w-32 bg-surface-interactive h-2 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{
                        width: `${sub.percentage}%`,
                        backgroundColor: sub.meta.color || "#48A9FF",
                      }}
                    ></div>
                  </div>
                  <span className="text-text-muted text-sm font-bold">
                    {isExpanded ? "▲" : "▼"}
                  </span>
                </div>
              </div>

              {/* Topics Table */}
              {isExpanded && (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="bg-surface-secondary text-text-muted text-[10px] uppercase tracking-wider border-b border-border-charcoal">
                        <th className="py-3 px-4 font-bold w-1/3">Topic Title & Bank Count</th>
                        <th className="py-3 px-3 font-bold text-center w-28">📚 Theory</th>
                        <th className="py-3 px-3 font-bold text-center w-28">✍️ Practice</th>
                        <th className="py-3 px-3 font-bold text-center w-28">🎯 Mock Exam</th>
                        <th className="py-3 px-4 font-bold text-center w-28">Notes</th>
                        <th className="py-3 px-4 font-bold text-right w-28">Quick Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border-charcoal/40">
                      {sub.filteredTopics.map((topic) => {
                        const key = `${sub.name}:::${topic.name}`;
                        const p = progressMap[key];
                        const theoryDone = !!p?.theory_completed;
                        const practiceDone = !!p?.practice_completed;
                        const mockDone = !!p?.mock_completed;
                        const hasNote = !!p?.notes && p.notes.trim().length > 0;
                        const isAllDone = theoryDone && practiceDone && mockDone;

                        return (
                          <tr
                            key={topic.name}
                            className={`hover:bg-card-elevated/60 transition-colors ${
                              isAllDone ? "bg-semantic-teal/5" : ""
                            }`}
                          >
                            {/* Topic Title */}
                            <td className="py-3.5 px-4 font-medium text-text-primary">
                              <div className="flex items-center gap-2">
                                {isAllDone && (
                                  <span className="text-semantic-teal font-bold" title="Topic Mastered">
                                    ✓
                                  </span>
                                )}
                                <span>{topic.name}</span>
                              </div>
                              <div className="text-[10px] text-text-muted mt-0.5">
                                {topic.question_count} authoritative questions
                              </div>
                            </td>

                            {/* Theory Checkbox */}
                            <td className="py-3.5 px-3 text-center">
                              <label className="inline-flex items-center justify-center cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={theoryDone}
                                  onChange={() => handleToggle(sub.name, topic.name, "theory_completed")}
                                  className="w-4 h-4 rounded border-border-charcoal text-brand-blue focus:ring-brand-blue bg-surface-interactive cursor-pointer"
                                />
                              </label>
                            </td>

                            {/* Practice Checkbox */}
                            <td className="py-3.5 px-3 text-center">
                              <label className="inline-flex items-center justify-center cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={practiceDone}
                                  onChange={() => handleToggle(sub.name, topic.name, "practice_completed")}
                                  className="w-4 h-4 rounded border-border-charcoal text-semantic-teal focus:ring-semantic-teal bg-surface-interactive cursor-pointer"
                                />
                              </label>
                            </td>

                            {/* Mock Checkbox */}
                            <td className="py-3.5 px-3 text-center">
                              <label className="inline-flex items-center justify-center cursor-pointer">
                                <input
                                  type="checkbox"
                                  checked={mockDone}
                                  onChange={() => handleToggle(sub.name, topic.name, "mock_completed")}
                                  className="w-4 h-4 rounded border-border-charcoal text-brand-gold focus:ring-brand-gold bg-surface-interactive cursor-pointer"
                                />
                              </label>
                            </td>

                            {/* Study Notes Button */}
                            <td className="py-3.5 px-4 text-center">
                              <button
                                onClick={() =>
                                  setActiveNoteTopic({
                                    subject: sub.name,
                                    topic: topic.name,
                                    notes: p?.notes || "",
                                  })
                                }
                                className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-all ${
                                  hasNote
                                    ? "bg-brand-blue/20 text-brand-blue border border-brand-blue/40"
                                    : "bg-surface-interactive text-text-muted hover:text-text-primary"
                                }`}
                              >
                                {hasNote ? "📝 View Note" : "+ Note"}
                              </button>
                            </td>

                            {/* Practice Quick Launch */}
                            <td className="py-3.5 px-4 text-right">
                              <Link
                                href={`/dashboard/exam?subjects=${encodeURIComponent(
                                  sub.name
                                )}&topic=${encodeURIComponent(topic.name)}&mode=practice`}
                                className="inline-block px-3 py-1 rounded-lg bg-surface-interactive hover:bg-brand-blue hover:text-bg-main text-text-secondary text-[11px] font-bold transition-all"
                              >
                                Practice ➔
                              </Link>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Study Notes Modal */}
      {activeNoteTopic && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="bg-card-primary border border-border-charcoal w-full max-w-lg rounded-2xl p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-border-charcoal pb-3">
              <div>
                <span className="text-[10px] uppercase font-bold text-brand-blue tracking-wider">
                  {activeNoteTopic.subject}
                </span>
                <h3 className="text-base font-bold text-text-primary">
                  Study Notes: {activeNoteTopic.topic}
                </h3>
              </div>
              <button
                onClick={() => setActiveNoteTopic(null)}
                className="text-text-muted hover:text-white font-bold text-sm"
              >
                ✕
              </button>
            </div>

            <div>
              <label className="block text-xs font-bold text-text-secondary mb-2">
                Personal Pilot Notes & Formulas:
              </label>
              <textarea
                rows={6}
                value={activeNoteTopic.notes}
                onChange={(e) =>
                  setActiveNoteTopic({ ...activeNoteTopic, notes: e.target.value })
                }
                placeholder="Write memory formulas, key limitations, ICAO rules, or specific points to remember..."
                className="w-full p-3 rounded-xl bg-surface-interactive border border-border-charcoal text-text-primary text-xs focus:outline-none focus:border-brand-blue resize-none"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setActiveNoteTopic(null)}
                className="px-4 py-2 rounded-xl bg-surface-interactive text-text-secondary hover:text-white text-xs font-bold"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveNote}
                disabled={isSavingNote}
                className="px-5 py-2 rounded-xl bg-brand-blue text-bg-main text-xs font-black shadow-card hover:bg-opacity-90 disabled:opacity-50"
              >
                {isSavingNote ? "Saving..." : "Save Note"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
