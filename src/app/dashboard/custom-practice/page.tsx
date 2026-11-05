"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import rawQuestions from "@/data/questions.json";

interface SubjectData {
  name: string;
  code: string;
  icon: string;
  color: string;
  topics: {
    name: string;
    total: number;
    fresh: number;
    pendingMistakes: number;
  }[];
}

export default function CustomPracticePage() {
  const router = useRouter();

  const [servedIds, setServedIds] = useState<Set<string>>(new Set());
  const [mistakeIds, setMistakeIds] = useState<Set<string>>(new Set());
  const [selectedTopics, setSelectedTopics] = useState<Set<string>>(new Set());
  const [expandedSubjects, setExpandedSubjects] = useState<Set<string>>(new Set());
  const [questionLimit, setQuestionLimit] = useState<number>(50);
  const [practiceMode, setPracticeMode] = useState<"smart" | "fresh_only" | "revision_only" | "all_incorrect">("smart");
  const [loading, setLoading] = useState(false);

  // Load local served IDs and mistakes
  useEffect(() => {
    try {
      const storedServed = localStorage.getItem("cpl_served_ids");
      if (storedServed) {
        setServedIds(new Set(JSON.parse(storedServed)));
      }
      const storedMistakes = localStorage.getItem("cpl_mistakes");
      if (storedMistakes) {
        const mObj = JSON.parse(storedMistakes);
        const pSet = new Set<string>();
        Object.keys(mObj).forEach((qId) => {
          if (mObj[qId].status === "pending_revision" || mObj[qId].status === "unresolved") {
            pSet.add(qId);
          }
        });
        setMistakeIds(pSet);
      }
    } catch {
      // Ignored
    }
  }, []);

  // Group questions by subject and topic
  const subjectsMap: Record<string, SubjectData> = {};

  const SUBJECT_METADATA: Record<string, { code: string; icon: string; color: string }> = {
    "Air Navigation": { code: "CAR SEC 7", icon: "🧭", color: "#719CFF" },
    "Air Regulations": { code: "ICAO / CAR", icon: "📜", color: "#9484F5" },
    "Aviation Meteorology": { code: "I.C. JOSHI", icon: "⛅", color: "#51C6C1" },
    "Technical General": { code: "AGK / ENGINES", icon: "⚙️", color: "#69CF9B" },
    "Technical Specific": { code: "POH / PERF", icon: "🛩️", color: "#ECA85B" },
    "RTR": { code: "ICAO DOC 9432", icon: "🎙️", color: "#51C6C1" },
  };

  (rawQuestions as any[]).forEach((q) => {
    const sName = q.subject || "Other";
    const tName = q.topic || "General";

    if (!subjectsMap[sName]) {
      const meta = SUBJECT_METADATA[sName] || { code: "DGCA", icon: "📖", color: "#9484F5" };
      subjectsMap[sName] = {
        name: sName,
        code: meta.code,
        icon: meta.icon,
        color: meta.color,
        topics: [],
      };
    }

    let tObj = subjectsMap[sName].topics.find((t) => t.name === tName);
    if (!tObj) {
      tObj = { name: tName, total: 0, fresh: 0, pendingMistakes: 0 };
      subjectsMap[sName].topics.push(tObj);
    }

    tObj.total += 1;
    if (!servedIds.has(q.id)) {
      tObj.fresh += 1;
    }
    if (mistakeIds.has(q.id)) {
      tObj.pendingMistakes += 1;
    }
  });

  const subjectsList = Object.values(subjectsMap);

  // Expand all subjects by default on first load
  useEffect(() => {
    if (subjectsList.length > 0 && expandedSubjects.size === 0) {
      setExpandedSubjects(new Set(subjectsList.map((s) => s.name)));
    }
  }, [subjectsList.length]);

  // Topic selection helpers
  const toggleTopic = (topicName: string) => {
    const next = new Set(selectedTopics);
    if (next.has(topicName)) {
      next.delete(topicName);
    } else {
      next.add(topicName);
    }
    setSelectedTopics(next);
  };

  const toggleSubjectAllTopics = (subj: SubjectData) => {
    const next = new Set(selectedTopics);
    const allTopicNames = subj.topics.map((t) => t.name);
    const areAllSelected = allTopicNames.every((t) => next.has(t));

    if (areAllSelected) {
      allTopicNames.forEach((t) => next.delete(t));
    } else {
      allTopicNames.forEach((t) => next.add(t));
    }
    setSelectedTopics(next);
  };

  const handleSelectAll = () => {
    const all = new Set<string>();
    subjectsList.forEach((s) => s.topics.forEach((t) => all.add(t.name)));
    setSelectedTopics(all);
  };

  const handleClearAll = () => {
    setSelectedTopics(new Set());
  };

  const toggleExpand = (subjName: string) => {
    const next = new Set(expandedSubjects);
    if (next.has(subjName)) {
      next.delete(subjName);
    } else {
      next.add(subjName);
    }
    setExpandedSubjects(next);
  };

  const handleExpandAll = () => {
    setExpandedSubjects(new Set(subjectsList.map((s) => s.name)));
  };

  const handleCollapseAll = () => {
    setExpandedSubjects(new Set());
  };

  // Calculate Selection Summary Metrics
  let selectedSubjectsCount = 0;
  let totalSelectedQuestions = 0;
  let freshSelectedQuestions = 0;
  let pendingRevisionCount = 0;

  subjectsList.forEach((s) => {
    const hasSelectedTopic = s.topics.some((t) => selectedTopics.has(t.name));
    if (hasSelectedTopic) selectedSubjectsCount += 1;

    s.topics.forEach((t) => {
      if (selectedTopics.has(t.name)) {
        totalSelectedQuestions += t.total;
        freshSelectedQuestions += t.fresh;
        pendingRevisionCount += t.pendingMistakes;
      }
    });
  });

  // Effective questions to be served
  let effectivePool = freshSelectedQuestions;
  if (practiceMode === "smart") {
    effectivePool = freshSelectedQuestions + pendingRevisionCount;
  } else if (practiceMode === "revision_only") {
    effectivePool = pendingRevisionCount;
  } else if (practiceMode === "all_incorrect") {
    effectivePool = mistakeIds.size;
  }

  const sessionQuestionCount = Math.min(questionLimit, effectivePool || totalSelectedQuestions);

  const handleLaunchPractice = () => {
    if (selectedTopics.size === 0 && practiceMode !== "all_incorrect") {
      alert("Please select at least one topic to start practice.");
      return;
    }

    setLoading(true);

    // Identify selected subjects
    const chosenSubjects = subjectsList
      .filter((s) => s.topics.some((t) => selectedTopics.has(t.name)))
      .map((s) => s.name);

    const queryParams = new URLSearchParams();
    if (chosenSubjects.length > 0) {
      queryParams.set("subjects", chosenSubjects.join(","));
    }
    if (selectedTopics.size > 0) {
      queryParams.set("topics", Array.from(selectedTopics).join(","));
    }
    queryParams.set("mode", "practice");
    queryParams.set("practiceMode", practiceMode);
    queryParams.set("limit", String(questionLimit));

    router.push(`/dashboard/exam?${queryParams.toString()}`);
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Title & Introduction */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border-charcoal pb-6">
        <div>
          <div className="flex items-center gap-2.5">
            <span className="text-2xl">🎯</span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Custom Practice
            </h1>
          </div>
          <p className="text-xs sm:text-sm text-text-secondary mt-1 font-medium">
            Build your own quiz by selecting multiple subjects and topics.
          </p>
        </div>

        {/* Global Toolbar Controls */}
        <div className="flex flex-wrap items-center gap-2 text-xs font-bold">
          <button
            onClick={handleSelectAll}
            className="px-3 py-1.5 rounded-lg bg-surface-interactive hover:bg-surface-hover text-text-primary border border-border-charcoal transition-all"
          >
            Select All
          </button>
          <button
            onClick={handleClearAll}
            className="px-3 py-1.5 rounded-lg bg-surface-interactive hover:bg-surface-hover text-text-muted hover:text-white border border-border-charcoal transition-all"
          >
            Clear All
          </button>
          <span className="text-border-charcoal">|</span>
          <button
            onClick={handleExpandAll}
            className="px-3 py-1.5 rounded-lg bg-card-elevated hover:bg-surface-interactive text-text-secondary border border-border-charcoal transition-all"
          >
            Expand All
          </button>
          <button
            onClick={handleCollapseAll}
            className="px-3 py-1.5 rounded-lg bg-card-elevated hover:bg-surface-interactive text-text-secondary border border-border-charcoal transition-all"
          >
            Collapse All
          </button>
        </div>
      </div>

      {/* Configuration Grid: Set Size & Practice Mode */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Question Set Size Selection */}
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-4">
          <div className="flex items-center justify-between">
            <label className="text-xs font-extrabold uppercase tracking-wider text-text-muted">
              Question Set Size (Max 50 Questions)
            </label>
            <span className="text-xs font-bold text-brand-purple">
              {questionLimit} Questions Selected
            </span>
          </div>

          <div className="grid grid-cols-5 gap-2">
            {[10, 20, 30, 40, 50].map((size) => (
              <button
                key={size}
                type="button"
                onClick={() => setQuestionLimit(size)}
                className={`py-3 rounded-xl border text-xs font-extrabold transition-all flex flex-col items-center justify-center gap-1 ${
                  questionLimit === size
                    ? "bg-brand-purple text-white border-brand-purple shadow-glow"
                    : "bg-card-elevated hover:bg-surface-interactive border-border-charcoal text-text-secondary hover:text-white"
                }`}
              >
                <span>{size}</span>
                <span className="text-[9px] font-normal opacity-70">MCQs</span>
              </button>
            ))}
          </div>
          <p className="text-[11px] text-text-muted">
            Sets are capped at 50 questions to maintain focus and test endurance according to DGCA CBT standards.
          </p>
        </div>

        {/* Practice Mode Selector */}
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-4">
          <label className="text-xs font-extrabold uppercase tracking-wider text-text-muted block">
            Practice Engine Strategy
          </label>

          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => setPracticeMode("smart")}
              className={`p-3 rounded-xl border text-left transition-all ${
                practiceMode === "smart"
                  ? "bg-brand-purple/20 border-brand-purple text-white"
                  : "bg-card-elevated hover:bg-surface-interactive border-border-charcoal text-text-secondary"
              }`}
            >
              <div className="text-xs font-extrabold flex items-center justify-between">
                <span>⚡ Smart Practice</span>
                <span className="text-[9px] px-1.5 py-0.5 rounded bg-brand-purple/30 text-brand-purple uppercase">
                  Recommended
                </span>
              </div>
              <div className="text-[10px] text-text-muted mt-1 leading-tight">
                Interleaves pending mistakes with fresh unseen questions.
              </div>
            </button>

            <button
              type="button"
              onClick={() => setPracticeMode("fresh_only")}
              className={`p-3 rounded-xl border text-left transition-all ${
                practiceMode === "fresh_only"
                  ? "bg-brand-teal/20 border-brand-teal text-white"
                  : "bg-card-elevated hover:bg-surface-interactive border-border-charcoal text-text-secondary"
              }`}
            >
              <div className="text-xs font-extrabold">🌱 Fresh Only</div>
              <div className="text-[10px] text-text-muted mt-1 leading-tight">
                Zero-repeat mode: strictly unattempted questions only.
              </div>
            </button>

            <button
              type="button"
              onClick={() => setPracticeMode("revision_only")}
              className={`p-3 rounded-xl border text-left transition-all ${
                practiceMode === "revision_only"
                  ? "bg-brand-orange/20 border-brand-orange text-white"
                  : "bg-card-elevated hover:bg-surface-interactive border-border-charcoal text-text-secondary"
              }`}
            >
              <div className="text-xs font-extrabold">↺ Revision Queue</div>
              <div className="text-[10px] text-text-muted mt-1 leading-tight">
                Target only questions answered incorrectly in chosen topics.
              </div>
            </button>

            <button
              type="button"
              onClick={() => setPracticeMode("all_incorrect")}
              className={`p-3 rounded-xl border text-left transition-all ${
                practiceMode === "all_incorrect"
                  ? "bg-brand-red/20 border-brand-red text-white"
                  : "bg-card-elevated hover:bg-surface-interactive border-border-charcoal text-text-secondary"
              }`}
            >
              <div className="text-xs font-extrabold">⚠️ All Mistakes</div>
              <div className="text-[10px] text-text-muted mt-1 leading-tight">
                Review mistakes across all subjects regardless of topic filter.
              </div>
            </button>
          </div>
        </div>
      </div>

      {/* Dynamic Selection Summary Box */}
      <div className="bg-gradient-to-r from-card-primary to-card-elevated border border-border-charcoal rounded-2xl p-6 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-4">
          <div>
            <div className="text-xs text-text-muted font-bold uppercase tracking-wider">Subjects</div>
            <div className="text-xl font-extrabold text-white mt-1">
              {selectedSubjectsCount} / {subjectsList.length}
            </div>
          </div>
          <div>
            <div className="text-xs text-text-muted font-bold uppercase tracking-wider">Topics</div>
            <div className="text-xl font-extrabold text-brand-purple mt-1">
              {selectedTopics.size}
            </div>
          </div>
          <div>
            <div className="text-xs text-text-muted font-bold uppercase tracking-wider">Total Pool</div>
            <div className="text-xl font-extrabold text-text-secondary mt-1">
              {totalSelectedQuestions}
            </div>
          </div>
          <div>
            <div className="text-xs text-text-muted font-bold uppercase tracking-wider">Fresh Unseen</div>
            <div className="text-xl font-extrabold text-brand-teal mt-1">
              {freshSelectedQuestions}
            </div>
          </div>
          <div>
            <div className="text-xs text-text-muted font-bold uppercase tracking-wider">Pending Revision</div>
            <div className="text-xl font-extrabold text-brand-orange mt-1">
              {pendingRevisionCount}
            </div>
          </div>
        </div>

        {/* Start Button */}
        <div className="shrink-0 flex flex-col items-end gap-2">
          {effectivePool < questionLimit && effectivePool > 0 && (
            <span className="text-[11px] text-brand-gold font-bold">
              ℹ️ {effectivePool} unique questions available for your scope.
            </span>
          )}
          <button
            onClick={handleLaunchPractice}
            disabled={loading || (selectedTopics.size === 0 && practiceMode !== "all_incorrect")}
            className="w-full sm:w-auto px-8 py-4 rounded-xl bg-brand-purple hover:bg-brand-purpleDark disabled:opacity-40 disabled:cursor-not-allowed text-white font-extrabold text-sm shadow-card hover:shadow-glow transition-all flex items-center justify-center gap-2"
          >
            {loading ? "Preparing Session..." : `Launch Practice Session (${sessionQuestionCount} Questions) →`}
          </button>
        </div>
      </div>

      {/* Expandable Subject Accordions with Topic Checkboxes */}
      <div className="space-y-4">
        <h2 className="text-base font-extrabold text-white tracking-tight flex items-center gap-2">
          <span>📚</span>
          Select Subjects & Chapters
        </h2>

        <div className="space-y-4">
          {subjectsList.map((subj) => {
            const isExpanded = expandedSubjects.has(subj.name);
            const allTopicNames = subj.topics.map((t) => t.name);
            const selectedInSubj = allTopicNames.filter((t) => selectedTopics.has(t)).length;
            const isAllSubjSelected = selectedInSubj === allTopicNames.length && allTopicNames.length > 0;
            const isPartialSubjSelected = selectedInSubj > 0 && selectedInSubj < allTopicNames.length;

            const subjTotal = subj.topics.reduce((acc, t) => acc + t.total, 0);
            const subjFresh = subj.topics.reduce((acc, t) => acc + t.fresh, 0);
            const subjMistakes = subj.topics.reduce((acc, t) => acc + t.pendingMistakes, 0);

            return (
              <div
                key={subj.name}
                className="bg-card-primary border border-border-charcoal rounded-2xl overflow-hidden shadow-card transition-all"
              >
                {/* Subject Header */}
                <div className="p-5 flex flex-wrap items-center justify-between gap-4 bg-card-primary hover:bg-card-elevated/40 transition-colors">
                  <div className="flex items-center gap-3">
                    <button
                      type="button"
                      onClick={() => toggleSubjectAllTopics(subj)}
                      className={`w-5 h-5 rounded border flex items-center justify-center transition-all ${
                        isAllSubjSelected
                          ? "bg-brand-purple border-brand-purple text-white"
                          : isPartialSubjSelected
                          ? "bg-brand-purple/40 border-brand-purple text-white"
                          : "border-border-charcoal bg-card-elevated"
                      }`}
                    >
                      {isAllSubjSelected && "✓"}
                      {isPartialSubjSelected && "–"}
                    </button>

                    <div
                      onClick={() => toggleExpand(subj.name)}
                      className="cursor-pointer flex items-center gap-3"
                    >
                      <div className="w-9 h-9 rounded-xl bg-card-elevated border border-border-charcoal flex items-center justify-center text-lg shadow-card">
                        {subj.icon}
                      </div>
                      <div>
                        <div className="text-sm font-extrabold text-white flex items-center gap-2">
                          {subj.name}
                          <span
                            className="text-[9px] font-bold px-2 py-0.5 rounded-full border"
                            style={{ borderColor: subj.color, color: subj.color }}
                          >
                            {subj.code}
                          </span>
                        </div>
                        <div className="text-[11px] text-text-muted mt-0.5">
                          {selectedInSubj} of {subj.topics.length} topics selected &bull; {subjTotal} validated questions
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Subject Badges & Expand Toggle */}
                  <div className="flex items-center gap-3">
                    <div className="hidden sm:flex items-center gap-2 text-[10px] font-bold">
                      <span className="px-2 py-1 rounded-md bg-brand-teal/10 text-brand-teal border border-brand-teal/20">
                        {subjFresh} Fresh
                      </span>
                      {subjMistakes > 0 && (
                        <span className="px-2 py-1 rounded-md bg-brand-orange/10 text-brand-orange border border-brand-orange/20">
                          {subjMistakes} Revision
                        </span>
                      )}
                    </div>

                    <button
                      type="button"
                      onClick={() => toggleExpand(subj.name)}
                      className="w-8 h-8 rounded-lg bg-surface-interactive hover:bg-surface-hover text-text-secondary hover:text-white flex items-center justify-center font-bold text-sm transition-all"
                    >
                      {isExpanded ? "▲" : "▼"}
                    </button>
                  </div>
                </div>

                {/* Topics Grid (Accordion Body) */}
                {isExpanded && (
                  <div className="p-5 pt-2 border-t border-border-charcoal/60 bg-bg-secondary/40">
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                      {subj.topics.map((top) => {
                        const isTopicSelected = selectedTopics.has(top.name);

                        return (
                          <div
                            key={top.name}
                            onClick={() => toggleTopic(top.name)}
                            className={`p-3.5 rounded-xl border cursor-pointer transition-all flex items-start gap-3 ${
                              isTopicSelected
                                ? "bg-card-elevated border-brand-purple shadow-sm"
                                : "bg-card-primary/80 hover:bg-card-elevated border-border-charcoal text-text-secondary"
                            }`}
                          >
                            <input
                              type="checkbox"
                              checked={isTopicSelected}
                              onChange={() => {}}
                              className="mt-1 accent-brand-purple w-4 h-4 cursor-pointer"
                            />

                            <div className="flex-1 min-w-0">
                              <div
                                className={`text-xs font-bold truncate ${
                                  isTopicSelected ? "text-white" : "text-text-primary"
                                }`}
                              >
                                {top.name}
                              </div>

                              <div className="flex items-center gap-2 text-[10px] font-bold text-text-muted mt-1.5">
                                <span>{top.total} Qs</span>
                                <span>&bull;</span>
                                <span className="text-brand-teal">{top.fresh} Fresh</span>
                                {top.pendingMistakes > 0 && (
                                  <>
                                    <span>&bull;</span>
                                    <span className="text-brand-orange">
                                      {top.pendingMistakes} Revision
                                    </span>
                                  </>
                                )}
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
