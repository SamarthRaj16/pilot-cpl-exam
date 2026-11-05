"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import rawQuestions from "@/data/questions.json";

interface MistakeItem {
  id: string;
  question: string;
  options: string[];
  correctChoice: number;
  userChoice: number;
  subject: string;
  topic: string;
  explanation: string;
  source: string;
  status: "unresolved" | "resolved";
  incorrectCount: number;
  correctedCount: number;
  date: string;
}

export default function MistakeNotebookPage() {
  const router = useRouter();
  const [filterStatus, setFilterStatus] = useState<"all" | "unresolved" | "resolved">("unresolved");
  const [selectedSubject, setSelectedSubject] = useState<string>("");
  const [mistakes, setMistakes] = useState<MistakeItem[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  const LETTERS = ["A", "B", "C", "D"];

  // Fast lookup map for all 959 authoritative questions
  const questionsMap = useMemo(() => {
    const map = new Map<string, any>();
    (rawQuestions as any[]).forEach((q) => map.set(q.id, q));
    return map;
  }, []);

  // Subjects in DGCA CPL
  const ALL_SUBJECTS = [
    "Air Navigation",
    "Air Regulations",
    "Aviation Meteorology",
    "Technical General",
    "Technical Specific",
    "RTR",
  ];

  useEffect(() => {
    try {
      const stored = localStorage.getItem("cpl_mistakes");
      if (stored) {
        const parsed = JSON.parse(stored);
        // Normalize whether stored as Dictionary Object { [id]: data } or Array [ data, ... ]
        const rawEntries: any[] = Array.isArray(parsed)
          ? parsed
          : Object.values(parsed || {});

        const normalizedList: MistakeItem[] = rawEntries
          .map((raw: any) => {
            const qId = raw.id || raw.questionId;
            if (!qId) return null;

            const qData = questionsMap.get(qId);

            const questionText =
              qData?.question || raw.question || `Question ${qId}`;
            const options =
              qData?.options || raw.options || [
                "Option A",
                "Option B",
                "Option C",
                "Option D",
              ];
            const correctChoice =
              qData?.answerIndex !== undefined
                ? qData.answerIndex
                : qData?.answer_index !== undefined
                ? qData.answer_index
                : raw.correctChoice !== undefined
                ? raw.correctChoice
                : 0;

            const studentChoice =
              raw.studentChoice !== undefined
                ? raw.studentChoice
                : raw.userChoice !== undefined
                ? raw.userChoice
                : -1;

            const explanation =
              qData?.explanation ||
              raw.explanation ||
              "Authoritative explanation available in official DGCA study references.";

            const source =
              qData?.source ||
              raw.source ||
              "DGCA CPL Reference Material";

            const subject =
              qData?.subject || raw.subject || "Air Navigation";
            const topic =
              qData?.topic || raw.topic || "General Syllabus";

            // Map statuses: "pending_revision" / "unresolved" -> "unresolved"; "recovered" / "resolved" -> "resolved"
            const isResolved =
              raw.status === "resolved" || raw.status === "recovered";

            return {
              id: qId,
              question: questionText,
              options,
              correctChoice,
              userChoice: studentChoice,
              subject,
              topic,
              explanation,
              source,
              status: isResolved ? "resolved" : "unresolved",
              incorrectCount: raw.incorrectCount || raw.incorrect_count || 1,
              correctedCount: isResolved ? 1 : raw.correctedCount || 0,
              date: raw.lastIncorrectAt
                ? new Date(raw.lastIncorrectAt).toLocaleDateString("en-IN", {
                    month: "short",
                    day: "numeric",
                  })
                : "Recent session",
            };
          })
          .filter((item): item is MistakeItem => item !== null);

        setMistakes(normalizedList);
      } else {
        // Sample seed if notebook is fresh and empty
        const sampleSeed: MistakeItem[] = [
          {
            id: "NAV-001",
            question: "Compass deviation is the angle between",
            options: [
              "true north and magnetic north",
              "grid north and true north",
              "aircraft heading and track",
              "magnetic north and compass north",
            ],
            correctChoice: 3,
            userChoice: 0,
            subject: "Air Navigation",
            topic: "Aircraft Magnetism and the Compasses",
            explanation:
              "Deviation is the angle between magnetic north and compass north, produced by magnetic influences within the aircraft.",
            source: "R.K. Bali Air Navigation / Oxford ATPL Gen Nav",
            status: "unresolved",
            incorrectCount: 2,
            correctedCount: 0,
            date: "Today",
          },
          {
            id: "MET-004",
            question: "When an aircraft altimeter subscale is set to QNH, the altimeter indicates:",
            options: [
              "Height above the aerodrome elevation",
              "Altitude above Mean Sea Level (MSL)",
              "Pressure altitude relative to the 1013.25 hPa datum",
              "True height above the instantaneous ground level (AGL)",
            ],
            correctChoice: 1,
            userChoice: 2,
            subject: "Aviation Meteorology",
            topic: "Atmospheric Pressure",
            explanation:
              "QNH is station pressure reduced to MSL using standard ISA temperature lapse rates. Setting QNH indicates altitude above Mean Sea Level (MSL).",
            source: "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure'",
            status: "unresolved",
            incorrectCount: 1,
            correctedCount: 0,
            date: "Recent session",
          },
        ];
        setMistakes(sampleSeed);
      }
    } catch (err) {
      console.error("Error loading mistake notebook:", err);
      setMistakes([]);
    } finally {
      setIsLoaded(true);
    }
  }, [questionsMap]);

  const handleToggleResolved = (id: string) => {
    const updated = mistakes.map((m) => {
      if (m.id === id) {
        const nextStatus: "unresolved" | "resolved" =
          m.status === "unresolved" ? "resolved" : "unresolved";
        return {
          ...m,
          status: nextStatus,
          correctedCount: nextStatus === "resolved" ? m.correctedCount + 1 : m.correctedCount,
        };
      }
      return m;
    });

    setMistakes(updated);

    // Sync back to localStorage in standard dictionary format
    try {
      const stored = localStorage.getItem("cpl_mistakes");
      const currentDict = stored ? JSON.parse(stored) : {};

      const target = updated.find((m) => m.id === id);
      if (target) {
        currentDict[id] = {
          questionId: target.id,
          subject: target.subject,
          topic: target.topic,
          studentChoice: target.userChoice,
          correctChoice: target.correctChoice,
          incorrectCount: target.incorrectCount,
          status: target.status === "resolved" ? "recovered" : "pending_revision",
          lastIncorrectAt: new Date().toISOString(),
        };
        localStorage.setItem("cpl_mistakes", JSON.stringify(currentDict));
      }
    } catch {}
  };

  const handleStartPracticeMistakes = () => {
    const query = new URLSearchParams();
    query.set("mode", "practice");
    query.set("practiceMode", "all_incorrect");
    query.set("limit", "30");
    if (selectedSubject) {
      query.set("subjects", selectedSubject);
    }
    router.push(`/dashboard/exam?${query.toString()}`);
  };

  const filtered = useMemo(() => {
    return mistakes.filter((m) => {
      if (filterStatus !== "all" && m.status !== filterStatus) return false;
      if (selectedSubject && m.subject !== selectedSubject) return false;
      return true;
    });
  }, [mistakes, filterStatus, selectedSubject]);

  const unresolvedCount = mistakes.filter((m) => m.status === "unresolved").length;
  const resolvedCount = mistakes.filter((m) => m.status === "resolved").length;

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-border-charcoal">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xl">📓</span>
            <h1 className="text-xl sm:text-2xl font-black text-text-primary tracking-tight">
              Personal Mistake Notebook
            </h1>
          </div>
          <p className="text-xs sm:text-sm text-text-secondary mt-1">
            Auto-catalog of previously missed questions with attempt tracking, step-by-step reasoning &amp; regulatory references
          </p>
        </div>

        {unresolvedCount > 0 && (
          <button
            onClick={handleStartPracticeMistakes}
            className="self-start sm:self-auto px-4 py-2.5 rounded-xl bg-brand-blue hover:bg-brand-skyDark text-bg-main font-bold text-xs shadow-glow transition-all flex items-center gap-2"
          >
            <span>🎯 Practice Mistakes ({unresolvedCount} Due)</span>
            <span>&rarr;</span>
          </button>
        )}
      </div>

      {/* Filter and Control Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 rounded-xl bg-card-primary border border-border-charcoal">
        {/* Status Filter Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setFilterStatus("unresolved")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              filterStatus === "unresolved"
                ? "bg-brand-red text-white shadow-sm"
                : "bg-card-elevated border border-border-charcoal text-text-secondary hover:text-white"
            }`}
          >
            Active Mistakes ({unresolvedCount})
          </button>

          <button
            onClick={() => setFilterStatus("resolved")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              filterStatus === "resolved"
                ? "bg-brand-teal text-bg-main font-black shadow-sm"
                : "bg-card-elevated border border-border-charcoal text-text-secondary hover:text-white"
            }`}
          >
            Resolved ({resolvedCount})
          </button>

          <button
            onClick={() => setFilterStatus("all")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              filterStatus === "all"
                ? "bg-brand-blue text-bg-main font-black shadow-sm"
                : "bg-card-elevated border border-border-charcoal text-text-secondary hover:text-white"
            }`}
          >
            All Entries ({mistakes.length})
          </button>
        </div>

        {/* Subject Filter Dropdown */}
        <div className="flex items-center gap-2">
          <label className="text-xs text-text-muted font-bold">Subject:</label>
          <select
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-card-elevated border border-border-charcoal text-text-primary text-xs font-semibold focus:outline-none focus:border-brand-blue"
          >
            <option value="">All Subjects</option>
            {ALL_SUBJECTS.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Mistake Items List */}
      {!isLoaded ? (
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-12 text-center text-text-muted text-xs font-bold">
          Loading mistake catalog...
        </div>
      ) : filtered.length === 0 ? (
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-12 text-center text-text-muted space-y-3">
          <div className="text-4xl mb-1">🎉</div>
          <h3 className="text-base font-bold text-text-primary">
            No mistakes found in this view!
          </h3>
          <p className="text-xs text-text-secondary max-w-md mx-auto leading-relaxed">
            {filterStatus === "unresolved"
              ? "All recorded mistakes have been resolved and mastered. Keep up the high accuracy in your practice sessions!"
              : "No questions match your current filter parameters."}
          </p>
          <div className="pt-2">
            <Link
              href="/dashboard/custom-practice"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-card-elevated hover:bg-surface-interactive text-brand-blue text-xs font-bold border border-border-charcoal transition-colors"
            >
              <span>Build Practice Quiz &rarr;</span>
            </Link>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {filtered.map((item) => {
            const hasUserChoice =
              item.userChoice !== undefined &&
              item.userChoice >= 0 &&
              item.options &&
              item.userChoice < item.options.length;

            const hasCorrectChoice =
              item.correctChoice !== undefined &&
              item.correctChoice >= 0 &&
              item.options &&
              item.correctChoice < item.options.length;

            return (
              <div
                key={item.id}
                className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-4 transition-all hover:border-border-charcoal/80"
              >
                {/* Meta Bar */}
                <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-bold">
                  <div className="flex items-center gap-2">
                    <span className="text-brand-blue font-extrabold">{item.id}</span>
                    <span className="text-text-muted">&bull;</span>
                    <span className="text-text-primary">{item.subject}</span>
                    <span className="text-text-muted">&bull;</span>
                    <span className="text-text-secondary">{item.topic}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="text-[10px] uppercase font-black px-2 py-0.5 rounded bg-brand-red/15 text-brand-red border border-brand-red/30">
                      {item.incorrectCount} Missed {item.incorrectCount === 1 ? "Attempt" : "Attempts"}
                    </span>
                    {item.status === "resolved" ? (
                      <span className="text-[10px] uppercase font-black px-2 py-0.5 rounded bg-brand-teal/15 text-brand-teal border border-brand-teal/30">
                        ✓ Mastered
                      </span>
                    ) : (
                      <span className="text-[10px] uppercase font-black px-2 py-0.5 rounded bg-brand-gold/15 text-brand-gold border border-brand-gold/30">
                        Pending Revision
                      </span>
                    )}
                  </div>
                </div>

                {/* Question Text */}
                <h3 className="text-sm sm:text-base font-bold text-text-primary leading-relaxed">
                  {item.question}
                </h3>

                {/* Comparison Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-medium">
                  {/* Previous Student Choice */}
                  <div className="p-3.5 rounded-xl bg-brand-red/10 border border-brand-red/30 text-brand-red space-y-1">
                    <span className="font-extrabold block text-[10px] uppercase tracking-wider text-brand-red/90">
                      ✗ Your Previous Choice:
                    </span>
                    <div className="font-bold">
                      {hasUserChoice
                        ? `${LETTERS[item.userChoice]}. ${item.options[item.userChoice]}`
                        : "Skipped / Unanswered"}
                    </div>
                  </div>

                  {/* Authoritative Correct Answer */}
                  <div className="p-3.5 rounded-xl bg-brand-teal/10 border border-brand-teal/30 text-brand-teal space-y-1">
                    <span className="font-extrabold block text-[10px] uppercase tracking-wider text-brand-teal/90">
                      ✓ Authoritative Correct Answer:
                    </span>
                    <div className="font-bold">
                      {hasCorrectChoice
                        ? `${LETTERS[item.correctChoice]}. ${item.options[item.correctChoice]}`
                        : "Authoritative choice"}
                    </div>
                  </div>
                </div>

                {/* Authoritative Explanation */}
                <div className="p-4 rounded-xl bg-card-elevated border border-border-charcoal text-xs text-text-secondary leading-relaxed space-y-1">
                  <div className="text-text-primary font-bold text-[11px] uppercase tracking-wider">
                    Authoritative Reasoning &amp; DGCA Concept:
                  </div>
                  <div>{item.explanation}</div>
                </div>

                {/* Footer Reference & Toggle Action */}
                <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-border-charcoal/60 text-xs">
                  <span className="text-[11px] text-text-muted font-medium">
                    📚 Source: <span className="text-text-secondary">{item.source}</span>
                  </span>

                  <button
                    onClick={() => handleToggleResolved(item.id)}
                    className={`px-3 py-1.5 rounded-lg font-bold text-xs border transition-all ${
                      item.status === "resolved"
                        ? "bg-brand-teal text-bg-main border-brand-teal"
                        : "border-border-charcoal bg-card-elevated text-text-secondary hover:text-text-primary hover:border-brand-blue"
                    }`}
                  >
                    {item.status === "resolved"
                      ? "✓ Mastered (Click to Re-open)"
                      : "Mark as Understood"}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
