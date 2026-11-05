"use client";

export const dynamic = "force-dynamic";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
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

export default function SubjectSyllabusPage() {
  const params = useParams();
  const router = useRouter();
  const subjectSlug = params?.subjectId as string;

  const currentSubject = useMemo(() => {
    return syllabusData.find(
      (s) => s.slug === subjectSlug || s.name.toLowerCase().replace(/\s+/g, "-") === subjectSlug
    );
  }, [subjectSlug]);

  const [progressMap, setProgressMap] = useState<Record<string, TopicProgress>>({});
  const [activeNoteTopic, setActiveNoteTopic] = useState<{
    subject: string;
    topic: string;
    notes: string;
  } | null>(null);
  const [isSavingNote, setIsSavingNote] = useState(false);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("cpl_syllabus_progress");
      if (stored) {
        setProgressMap(JSON.parse(stored));
      }
    } catch {}

    async function loadRemote() {
      try {
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
              };
            });
            setProgressMap((prev) => ({ ...prev, ...remoteMap }));
          }
        }
      } catch {}
    }
    loadRemote();
  }, []);

  if (!currentSubject) {
    return (
      <div className="max-w-4xl mx-auto p-12 text-center space-y-4">
        <h2 className="text-xl font-bold text-text-primary">Subject Not Found</h2>
        <p className="text-xs text-text-secondary">
          The requested subject does not match any DGCA CPL category.
        </p>
        <Link
          href="/dashboard/syllabus"
          className="inline-block px-4 py-2 rounded-xl bg-brand-blue text-bg-main text-xs font-bold"
        >
          Return to Syllabus Tracker
        </Link>
      </div>
    );
  }

  const totalTopics = currentSubject.topics.length;
  const totalItems = totalTopics * 3;

  const subMetrics = useMemo(() => {
    let theory = 0;
    let practice = 0;
    let mock = 0;
    let complete = 0;

    currentSubject.topics.forEach((t) => {
      const key = `${currentSubject.name}:::${t.name}`;
      const p = progressMap[key];
      if (p?.theory_completed) theory += 1;
      if (p?.practice_completed) practice += 1;
      if (p?.mock_completed) mock += 1;
      if (p?.theory_completed && p?.practice_completed && p?.mock_completed) complete += 1;
    });

    const totalDone = theory + practice + mock;
    const overallPct = totalItems > 0 ? Math.round((totalDone / totalItems) * 100) : 0;

    return {
      theory,
      practice,
      mock,
      totalDone,
      overallPct,
      complete,
    };
  }, [currentSubject, progressMap, totalItems]);

  const handleToggle = async (
    topicName: string,
    type: "theory_completed" | "practice_completed" | "mock_completed"
  ) => {
    const key = `${currentSubject.name}:::${topicName}`;
    const current = progressMap[key] || {
      subject_name: currentSubject.name,
      topic_name: topicName,
      theory_completed: false,
      practice_completed: false,
      mock_completed: false,
    };

    const updated: TopicProgress = {
      ...current,
      [type]: !current[type],
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
  };

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

    const updated = {
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

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-xs font-bold text-text-muted uppercase tracking-widest">
        <Link href="/dashboard" className="hover:text-brand-blue">
          Dashboard
        </Link>
        <span>/</span>
        <Link href="/dashboard/syllabus" className="hover:text-brand-blue">
          Syllabus Tracker
        </Link>
        <span>/</span>
        <span className="text-brand-blue">{currentSubject.name}</span>
      </div>

      {/* Header Banner */}
      <div className="bg-card-primary p-6 md:p-8 rounded-2xl border border-border-charcoal flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <span className="text-4xl">{currentSubject.meta.icon}</span>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-black text-text-primary">{currentSubject.name}</h1>
              <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-surface-interactive text-text-muted border border-border-charcoal">
                {currentSubject.meta.code}
              </span>
            </div>
            <p className="text-xs text-text-secondary mt-1">
              {currentSubject.topics.length} topics • {currentSubject.question_count} authoritative questions
            </p>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="text-right">
            <div className="text-2xl font-black text-text-primary">{subMetrics.overallPct}%</div>
            <div className="text-[10px] uppercase font-bold text-text-muted">Subject Coverage</div>
          </div>
          <Link
            href={`/dashboard/exam?subjects=${encodeURIComponent(currentSubject.name)}&mode=practice`}
            className="px-5 py-2.5 rounded-xl bg-brand-blue text-bg-main text-xs font-black shadow-card hover:bg-opacity-90 transition-all"
          >
            Practice Full Subject ➔
          </Link>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-card-primary p-4 rounded-xl border border-border-charcoal">
          <div className="text-xs text-text-muted font-bold">📚 Theory Studied</div>
          <div className="text-xl font-bold text-text-primary mt-1">
            {subMetrics.theory} / {totalTopics}
          </div>
        </div>
        <div className="bg-card-primary p-4 rounded-xl border border-border-charcoal">
          <div className="text-xs text-text-muted font-bold">✍️ Practice Mastered</div>
          <div className="text-xl font-bold text-semantic-teal mt-1">
            {subMetrics.practice} / {totalTopics}
          </div>
        </div>
        <div className="bg-card-primary p-4 rounded-xl border border-border-charcoal">
          <div className="text-xs text-text-muted font-bold">🎯 Mock Exam Completed</div>
          <div className="text-xl font-bold text-brand-gold mt-1">
            {subMetrics.mock} / {totalTopics}
          </div>
        </div>
      </div>

      {/* Checklist Table */}
      <div className="bg-card-primary rounded-2xl border border-border-charcoal overflow-hidden shadow-card">
        <div className="p-4 border-b border-border-charcoal bg-surface-secondary flex items-center justify-between">
          <h2 className="text-sm font-bold text-text-primary">Chapter & Topic Checklists</h2>
          <span className="text-xs text-text-muted">
            {subMetrics.complete} of {totalTopics} topics fully mastered
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-surface-secondary text-text-muted text-[10px] uppercase tracking-wider border-b border-border-charcoal">
                <th className="py-3 px-4 font-bold w-1/3">Topic</th>
                <th className="py-3 px-3 font-bold text-center w-28">📚 Theory</th>
                <th className="py-3 px-3 font-bold text-center w-28">✍️ Practice</th>
                <th className="py-3 px-3 font-bold text-center w-28">🎯 Mock Exam</th>
                <th className="py-3 px-4 font-bold text-center w-28">Notes</th>
                <th className="py-3 px-4 font-bold text-right w-28">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-charcoal/40">
              {currentSubject.topics.map((t) => {
                const key = `${currentSubject.name}:::${t.name}`;
                const p = progressMap[key];
                const theoryDone = !!p?.theory_completed;
                const practiceDone = !!p?.practice_completed;
                const mockDone = !!p?.mock_completed;
                const hasNote = !!p?.notes && p.notes.trim().length > 0;
                const isAllDone = theoryDone && practiceDone && mockDone;

                return (
                  <tr
                    key={t.name}
                    className={`hover:bg-card-elevated/60 transition-colors ${
                      isAllDone ? "bg-semantic-teal/5" : ""
                    }`}
                  >
                    <td className="py-3.5 px-4 font-medium text-text-primary">
                      <div className="flex items-center gap-2">
                        {isAllDone && <span className="text-semantic-teal font-bold">✓</span>}
                        <span>{t.name}</span>
                      </div>
                      <span className="text-[10px] text-text-muted">{t.question_count} questions</span>
                    </td>

                    <td className="py-3.5 px-3 text-center">
                      <label className="inline-flex items-center justify-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={theoryDone}
                          onChange={() => handleToggle(t.name, "theory_completed")}
                          className="w-4 h-4 rounded border-border-charcoal text-brand-blue focus:ring-brand-blue bg-surface-interactive cursor-pointer"
                        />
                      </label>
                    </td>

                    <td className="py-3.5 px-3 text-center">
                      <label className="inline-flex items-center justify-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={practiceDone}
                          onChange={() => handleToggle(t.name, "practice_completed")}
                          className="w-4 h-4 rounded border-border-charcoal text-semantic-teal focus:ring-semantic-teal bg-surface-interactive cursor-pointer"
                        />
                      </label>
                    </td>

                    <td className="py-3.5 px-3 text-center">
                      <label className="inline-flex items-center justify-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={mockDone}
                          onChange={() => handleToggle(t.name, "mock_completed")}
                          className="w-4 h-4 rounded border-border-charcoal text-brand-gold focus:ring-brand-gold bg-surface-interactive cursor-pointer"
                        />
                      </label>
                    </td>

                    <td className="py-3.5 px-4 text-center">
                      <button
                        onClick={() =>
                          setActiveNoteTopic({
                            subject: currentSubject.name,
                            topic: t.name,
                            notes: p?.notes || "",
                          })
                        }
                        className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-all ${
                          hasNote
                            ? "bg-brand-blue/20 text-brand-blue border border-brand-blue/40"
                            : "bg-surface-interactive text-text-muted hover:text-text-primary"
                        }`}
                      >
                        {hasNote ? "📝 Note" : "+ Note"}
                      </button>
                    </td>

                    <td className="py-3.5 px-4 text-right">
                      <Link
                        href={`/dashboard/exam?subjects=${encodeURIComponent(
                          currentSubject.name
                        )}&topic=${encodeURIComponent(t.name)}&mode=practice`}
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
      </div>

      {/* Note Modal */}
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

            <textarea
              rows={6}
              value={activeNoteTopic.notes}
              onChange={(e) =>
                setActiveNoteTopic({ ...activeNoteTopic, notes: e.target.value })
              }
              placeholder="Record your personal notes, memory aids, and key formulas..."
              className="w-full p-3 rounded-xl bg-surface-interactive border border-border-charcoal text-text-primary text-xs focus:outline-none focus:border-brand-blue resize-none"
            />

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

