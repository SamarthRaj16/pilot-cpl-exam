"use client";

export const dynamic = "force-dynamic";

import React, { Suspense, useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import rawQuestions from "@/data/questions.json";

function ExamSessionContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const subjectsParam = searchParams.get("subjects");
  const topicParam = searchParams.get("topic");
  const topicsParam = searchParams.get("topics");
  const mode = (searchParams.get("mode") || "practice") as "practice" | "timed" | "mock";
  const practiceMode = searchParams.get("practiceMode") || "smart";
  const limitParam = Number(searchParams.get("limit") || searchParams.get("questionCount") || (mode === "mock" ? 50 : 30));
  const questionLimit = Math.min(50, Math.max(10, limitParam || 50));

  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [flags, setFlags] = useState<boolean[]>([]);
  const [revealed, setRevealed] = useState<boolean[]>([]);
  const [timeRemaining, setTimeRemaining] = useState(mode === "mock" ? 90 * 60 : 30 * 60);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [attemptId, setAttemptId] = useState("");
  const [availabilityNotice, setAvailabilityNotice] = useState<string | null>(null);

  const LETTERS = ["A", "B", "C", "D"];

  // Initialize Quiz Session via API with Client-Side Fallback
  useEffect(() => {
    async function initSession() {
      // Gather local mistake and served IDs
      let clientMistakeIds: string[] = [];
      let clientServedIds: string[] = [];
      try {
        const storedMistakes = localStorage.getItem("cpl_mistakes");
        if (storedMistakes) {
          const mObj = JSON.parse(storedMistakes);
          clientMistakeIds = Object.keys(mObj).filter(
            (id) => mObj[id].status === "pending_revision" || mObj[id].status === "unresolved"
          );
        }
        const storedServed = localStorage.getItem("cpl_served_ids");
        if (storedServed) {
          clientServedIds = JSON.parse(storedServed);
        }
      } catch {
        // Ignored
      }

      // Parse subjects and topics arrays
      let subjectsList: string[] = [];
      if (subjectsParam) {
        subjectsList = subjectsParam.split(",").map((s) => s.trim()).filter(Boolean);
      }

      let topicsList: string[] = [];
      if (topicsParam) {
        topicsList = topicsParam.split(",").map((t) => t.trim()).filter(Boolean);
      } else if (topicParam) {
        topicsList = [topicParam.trim()];
      }

      try {
        const res = await fetch("/api/quiz/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            subjectIds: subjectsList,
            topicIds: topicsList,
            mode,
            practiceMode,
            questionCount: questionLimit,
            clientMistakeIds,
            clientServedIds,
          }),
        });

        const data = await res.json();
        if (data.questions && data.questions.length > 0) {
          setQuestions(data.questions);
          setAnswers(new Array(data.questions.length).fill(-1));
          setFlags(new Array(data.questions.length).fill(false));
          setRevealed(new Array(data.questions.length).fill(false));
          setAttemptId(data.attemptId || `att-${Date.now()}`);
          if (data.availabilityNotice) {
            setAvailabilityNotice(data.availabilityNotice);
          }

          // Track served IDs locally for Zero-Repeat
          try {
            const stored = localStorage.getItem("cpl_served_ids");
            const set = new Set(stored ? JSON.parse(stored) : []);
            data.questions.forEach((q: any) => {
              if (!q.isRevision) set.add(q.id);
            });
            localStorage.setItem("cpl_served_ids", JSON.stringify(Array.from(set)));
          } catch {
            // Ignored
          }
          return;
        }
      } catch {
        // Network or offline fallback
      }

      // Offline Standalone Selection Logic
      const servedSet = new Set(clientServedIds);
      const pendingMistakeSet = new Set(clientMistakeIds);

      const candidate = (rawQuestions as any[]).filter((q) => {
        if (practiceMode === "all_incorrect") return pendingMistakeSet.has(q.id);
        if (subjectsList.length > 0 && !subjectsList.includes(q.subject)) return false;
        if (topicsList.length > 0 && !topicsList.includes(q.topic)) return false;
        return true;
      });

      const poolRevision: any[] = [];
      const poolFresh: any[] = [];

      candidate.forEach((q) => {
        if (pendingMistakeSet.has(q.id)) {
          poolRevision.push({ ...q, isRevision: true });
        } else if (!servedSet.has(q.id)) {
          poolFresh.push({ ...q, isRevision: false });
        }
      });

      let selected: any[] = [];
      if (practiceMode === "revision_only" || practiceMode === "all_incorrect") {
        selected = poolRevision.slice(0, questionLimit);
      } else if (practiceMode === "fresh_only") {
        selected = poolFresh.sort(() => Math.random() - 0.5).slice(0, questionLimit);
      } else {
        // Smart mode: combine up to 20 revision + fresh questions
        const maxRev = Math.min(20, Math.floor(questionLimit * 0.4) || 5);
        const revPicked = poolRevision.slice(0, maxRev);
        const freshPicked = poolFresh
          .sort(() => Math.random() - 0.5)
          .slice(0, questionLimit - revPicked.length);
        selected = [...revPicked, ...freshPicked];

        if (selected.length < questionLimit && poolRevision.length > maxRev) {
          selected.push(...poolRevision.slice(maxRev, maxRev + (questionLimit - selected.length)));
        }
      }

      if (selected.length === 0) {
        selected = candidate.slice(0, Math.min(questionLimit, candidate.length));
      }

      if (selected.length < questionLimit) {
        setAvailabilityNotice(
          `${selected.length} unique questions are currently available for your selected topics.`
        );
      }

      setQuestions(selected.sort(() => Math.random() - 0.5));
      setAnswers(new Array(selected.length).fill(-1));
      setFlags(new Array(selected.length).fill(false));
      setRevealed(new Array(selected.length).fill(false));
      setAttemptId(`att-offline-${Date.now()}`);

      // Record offline exposures
      try {
        const stored = localStorage.getItem("cpl_served_ids");
        const set = new Set(stored ? JSON.parse(stored) : []);
        selected.forEach((q) => {
          if (!q.isRevision) set.add(q.id);
        });
        localStorage.setItem("cpl_served_ids", JSON.stringify(Array.from(set)));
      } catch {
        // Ignored
      }
    }
    initSession();
  }, [subjectsParam, topicParam, topicsParam, mode, practiceMode, questionLimit]);

  // Timer countdown
  useEffect(() => {
    if (timeRemaining <= 0) {
      handleFinalSubmit();
      return;
    }
    const timer = setInterval(() => {
      setTimeRemaining((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [timeRemaining]);

  if (questions.length === 0) {
    return (
      <div className="min-h-[500px] flex items-center justify-center">
        <div className="text-center space-y-3">
          <div className="text-3xl animate-bounce">✈️</div>
          <p className="text-sm font-bold text-text-secondary">
            Loading secure examination session...
          </p>
        </div>
      </div>
    );
  }

  const currentQ = questions[currentIndex];
  const totalQuestions = questions.length;
  const isRevealed = revealed[currentIndex];
  const isCurrentFlagged = flags[currentIndex];

  const handleSelectOption = (optIndex: number) => {
    if (mode === "practice" && isRevealed) return; // Locked in practice mode

    const newAnswers = [...answers];
    newAnswers[currentIndex] = optIndex;
    setAnswers(newAnswers);

    if (mode === "practice") {
      const newRevealed = [...revealed];
      newRevealed[currentIndex] = true;
      setRevealed(newRevealed);

      // Real-time persistent mistake and recovery tracking
      const isRight = optIndex === (currentQ.answerIndex !== undefined ? currentQ.answerIndex : currentQ.answer_index);
      try {
        const stored = localStorage.getItem("cpl_mistakes");
        const mistakes = stored ? JSON.parse(stored) : {};

        if (!isRight) {
          const existing = mistakes[currentQ.id];
          mistakes[currentQ.id] = {
            questionId: currentQ.id,
            subject: currentQ.subject,
            topic: currentQ.topic,
            studentChoice: optIndex,
            correctChoice: currentQ.answerIndex,
            incorrectCount: (existing?.incorrectCount || 0) + 1,
            lastIncorrectAt: new Date().toISOString(),
            status: "pending_revision",
          };
        } else {
          if (mistakes[currentQ.id] && mistakes[currentQ.id].status === "pending_revision") {
            mistakes[currentQ.id].status = "recovered";
            mistakes[currentQ.id].recoveredAt = new Date().toISOString();
            const prevRecovered = Number(localStorage.getItem("cpl_recovered_count") || "0");
            localStorage.setItem("cpl_recovered_count", String(prevRecovered + 1));
          }
        }
        localStorage.setItem("cpl_mistakes", JSON.stringify(mistakes));
      } catch {
        // Storage fail
      }
    }
  };

  const handleToggleFlag = () => {
    const newFlags = [...flags];
    newFlags[currentIndex] = !newFlags[currentIndex];
    setFlags(newFlags);
  };

  const handleFinalSubmit = async () => {
    setShowSubmitModal(false);

    // Build answers map
    const answerMap: Record<string, number> = {};
    questions.forEach((q, idx) => {
      answerMap[q.id] = answers[idx];
    });

    try {
      const res = await fetch("/api/quiz/finish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          attemptId,
          answers: answerMap,
          durationSeconds: (mode === "mock" ? 90 * 60 : 30 * 60) - timeRemaining,
        }),
      });

      const resultData = await res.json();
      sessionStorage.setItem("last_exam_result", JSON.stringify(resultData));
      router.push("/dashboard/results");
    } catch {
      // Offline result calculation fallback
      let score = 0;
      const reviewItems = questions.map((q, idx) => {
        const studentChoice = answers[idx];
        const correctChoice = q.answerIndex !== undefined ? q.answerIndex : q.answer_index;
        const isCorrect = studentChoice === correctChoice && studentChoice >= 0;
        if (isCorrect) score += 1;
        return {
          questionId: q.id,
          subject: q.subject,
          topic: q.topic,
          difficulty: q.difficulty,
          question: q.question,
          options: q.options,
          studentChoice,
          correctChoice,
          isCorrect,
          pointsAwarded: isCorrect ? 1 : 0,
          explanation: q.explanation,
          source: q.source,
        };
      });

      const accuracy = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;
      const offlineResult = {
        attemptId,
        score,
        totalQuestions,
        accuracy,
        passed: accuracy >= 70,
        durationSeconds: (mode === "mock" ? 90 * 60 : 30 * 60) - timeRemaining,
        passMark: 70,
        reviewItems,
      };
      sessionStorage.setItem("last_exam_result", JSON.stringify(offlineResult));
      router.push("/dashboard/results");
    }
  };

  const answeredCount = answers.filter((a) => a >= 0).length;
  const flaggedCount = flags.filter((f) => f).length;
  const unansweredCount = totalQuestions - answeredCount;

  const minutes = Math.floor(timeRemaining / 60);
  const seconds = timeRemaining % 60;
  const timeFormatted = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
      {/* Main CBT Question Area */}
      <div className="lg:col-span-3 bg-card-primary border border-border-charcoal rounded-2xl p-6 sm:p-8 shadow-card space-y-6">
        {/* Availability Notification Banner */}
        {availabilityNotice && (
          <div className="p-3.5 rounded-xl bg-brand-gold/10 border border-brand-gold/30 text-brand-gold text-xs font-bold flex items-center justify-between">
            <span>ℹ️ {availabilityNotice}</span>
            <button
              onClick={() => setAvailabilityNotice(null)}
              className="text-text-muted hover:text-white px-2 py-0.5 rounded"
            >
              ✕
            </button>
          </div>
        )}

        {/* Header */}
        <div className="flex flex-wrap items-center justify-between gap-3 pb-5 border-b border-border-charcoal">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-brand-purple uppercase tracking-wider">
                {currentQ.subject}
              </span>
              {currentQ.isRevision && (
                <span className="text-[10px] uppercase font-extrabold px-2 py-0.5 rounded-full bg-brand-orange/20 text-brand-orange border border-brand-orange/40">
                  ↺ Revision Question
                </span>
              )}
            </div>
            <div className="text-sm font-extrabold text-white mt-0.5">
              {currentQ.topic || "General"}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs uppercase font-bold px-2.5 py-1 rounded-md bg-card-elevated border border-border-charcoal text-brand-gold">
              {currentQ.difficulty || "Medium"}
            </span>
            <span className="text-xs font-bold text-text-muted">
              Question {currentIndex + 1} of {totalQuestions}
            </span>
          </div>
        </div>

        {/* Question Text */}
        <div className="space-y-4">
          <p className="text-base sm:text-lg font-medium text-text-primary leading-relaxed">
            {currentQ.question}
          </p>
        </div>

        {/* Answer Options */}
        <div className="space-y-3 pt-2">
          {currentQ.options.map((opt: string, optIndex: number) => {
            const isSelected = answers[currentIndex] === optIndex;
            const isCorrect = currentQ.answerIndex === optIndex;
            const isStudentWrong = isSelected && !isCorrect;

            let optStyle =
              "bg-card-elevated hover:bg-surface-interactive border-border-charcoal text-text-primary";

            if (mode === "practice" && isRevealed) {
              if (isCorrect) {
                optStyle = "bg-brand-green/20 border-brand-green text-brand-green font-bold";
              } else if (isStudentWrong) {
                optStyle = "bg-brand-red/20 border-brand-red text-brand-red font-bold";
              } else {
                optStyle = "bg-card-elevated/40 border-border-charcoal/40 text-text-muted opacity-60";
              }
            } else if (isSelected) {
              optStyle = "bg-brand-purple/20 border-brand-purple text-white font-bold";
            }

            return (
              <button
                key={optIndex}
                onClick={() => handleSelectOption(optIndex)}
                className={`w-full p-4 rounded-xl border text-left flex items-start gap-3.5 transition-all ${optStyle}`}
              >
                <div className="w-7 h-7 rounded-lg border border-border-charcoal bg-card-primary flex items-center justify-center font-bold text-xs shrink-0">
                  {LETTERS[optIndex]}
                </div>
                <div className="text-sm pt-0.5 leading-relaxed">{opt}</div>
              </button>
            );
          })}
        </div>

        {/* Instant Authoritative Feedback (Practice Mode strictly) */}
        {mode === "practice" && isRevealed && (
          <div
            className={`p-5 rounded-xl border text-sm space-y-3 animate-fadeIn ${
              answers[currentIndex] === currentQ.answerIndex
                ? "bg-brand-green/10 border-brand-green/30 text-text-primary"
                : "bg-brand-red/10 border-brand-red/30 text-text-primary"
            }`}
          >
            <div className="font-extrabold flex items-center gap-2">
              {answers[currentIndex] === currentQ.answerIndex ? (
                <span className="text-brand-green text-base font-extrabold flex items-center gap-1.5">
                  ✓ Correct Answer! (+1 Mark Awarded)
                </span>
              ) : (
                <span className="text-brand-red text-base font-extrabold flex items-center gap-1.5">
                  ✗ Incorrect (0 Marks Awarded)
                </span>
              )}
            </div>

            {/* Exact Authoritative Answer Display when incorrect */}
            {answers[currentIndex] !== currentQ.answerIndex && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs py-2.5 px-3 rounded-lg bg-card-primary/80 border border-border-charcoal">
                <div>
                  <span className="text-text-muted font-bold block mb-0.5">Your answer:</span>
                  <span className="text-brand-red font-bold">
                    {LETTERS[answers[currentIndex]]}. {currentQ.options[answers[currentIndex]]}
                  </span>
                </div>
                <div>
                  <span className="text-text-muted font-bold block mb-0.5">Authoritative Correct Answer:</span>
                  <span className="text-brand-green font-bold">
                    {LETTERS[currentQ.answerIndex]}. {currentQ.options[currentQ.answerIndex]}
                  </span>
                </div>
              </div>
            )}

            <p className="text-text-secondary leading-relaxed pt-1 text-xs sm:text-sm">
              <strong className="text-white">Explanation:</strong> {currentQ.explanation}
            </p>
            <div className="text-[11px] font-bold text-text-muted pt-2 border-t border-border-charcoal/40">
              📚 Source Reference: {currentQ.source}
            </div>
          </div>
        )}

        {/* Navigation Footer */}
        <div className="flex items-center justify-between gap-3 pt-6 border-t border-border-charcoal">
          <button
            onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
            disabled={currentIndex === 0}
            className="px-4 py-2.5 rounded-xl bg-surface-interactive hover:bg-surface-hover text-text-secondary hover:text-white font-bold text-xs disabled:opacity-40 transition-all"
          >
            &larr; Previous
          </button>

          <button
            onClick={handleToggleFlag}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold border transition-all ${
              isCurrentFlagged
                ? "bg-brand-orange text-black border-brand-orange"
                : "border-brand-orange/30 text-brand-orange hover:bg-brand-orange/10"
            }`}
          >
            {isCurrentFlagged ? "🚩 Flagged for Review" : "🚩 Flag Question"}
          </button>

          {currentIndex < totalQuestions - 1 ? (
            <button
              onClick={() => setCurrentIndex((prev) => prev + 1)}
              className="px-5 py-2.5 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white font-bold text-xs shadow-card transition-all"
            >
              Next &rarr;
            </button>
          ) : (
            <button
              onClick={() => setShowSubmitModal(true)}
              className="px-5 py-2.5 rounded-xl bg-brand-green hover:bg-brand-green/80 text-black font-extrabold text-xs shadow-card transition-all"
            >
              Review & Submit Exam
            </button>
          )}
        </div>
      </div>

      {/* CBT Sidebar (Timer & Question Grid) */}
      <div className="space-y-6">
        {/* Circular Countdown Timer */}
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-5 text-center shadow-card">
          <div className="text-3xl font-extrabold font-mono tracking-tight text-white mb-1">
            {timeFormatted}
          </div>
          <div className="text-[10px] uppercase font-bold tracking-wider text-text-muted">
            Time Remaining
          </div>
        </div>

        {/* Question Navigator */}
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-5 shadow-card space-y-4">
          <div className="flex items-center justify-between text-xs font-bold">
            <span className="text-white">Question Navigator</span>
            <span className="text-text-muted">
              {answeredCount} / {totalQuestions}
            </span>
          </div>

          {/* CRITICAL FIX: Question Navigator Colours */}
          <div className="grid grid-cols-5 gap-2 max-h-60 overflow-y-auto pr-1">
            {questions.map((q, idx) => {
              const isCurrent = idx === currentIndex;
              const studentAns = answers[idx];
              const isAttempted = studentAns >= 0;
              const correctAns = q.answerIndex !== undefined ? q.answerIndex : q.answer_index;
              const isCorrect = isAttempted && studentAns === correctAns;
              const isRev = revealed[idx];
              const isFlag = flags[idx];

              // Base state: Unanswered is Grey (#373942)
              let cellBg = "bg-card-elevated border-border-charcoal text-text-secondary";

              if (mode === "practice") {
                // In Practice Mode: Green if correct, Red if incorrect!
                if (isRev && isAttempted) {
                  if (isCorrect) {
                    cellBg = "bg-brand-green/20 border-brand-green text-brand-green";
                  } else {
                    cellBg = "bg-brand-red/20 border-brand-red text-brand-red";
                  }
                }
              } else {
                // In Timed / Mock Mode: Neutral answered state (NO PREMATURE GREEN/RED)
                if (isAttempted) {
                  cellBg = "bg-brand-blue/20 border-brand-blue text-brand-blue";
                }
              }

              // Selected state: Purple ring that DOES NOT overwrite green/red/grey
              const currentRing = isCurrent
                ? "ring-2 ring-brand-purple border-brand-purple shadow-glow"
                : "";

              return (
                <button
                  key={idx}
                  onClick={() => setCurrentIndex(idx)}
                  className={`relative aspect-square rounded-lg border text-xs font-extrabold flex items-center justify-center transition-all ${cellBg} ${currentRing}`}
                >
                  <span>{idx + 1}</span>

                  {/* Flag indicator: Orange badge that overlays without replacing tile color */}
                  {isFlag && (
                    <span className="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-brand-orange text-black text-[9px] font-extrabold flex items-center justify-center shadow-sm">
                      ⚑
                    </span>
                  )}

                  {/* Subtle Revision indicator */}
                  {q.isRevision && (
                    <span className="absolute bottom-0.5 right-1 text-[8px] text-brand-gold opacity-90 font-bold">
                      ↺
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          <div className="flex justify-between text-[10px] font-bold text-text-muted pt-2 border-t border-border-charcoal">
            <span className="text-brand-green">{answeredCount} Answered</span>
            <span className="text-brand-orange">{flaggedCount} Flagged</span>
            <span>{unansweredCount} Left</span>
          </div>

          <button
            onClick={() => setShowSubmitModal(true)}
            className="w-full py-3 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white font-extrabold text-xs shadow-card transition-all"
          >
            Submit Examination
          </button>
        </div>
      </div>

      {/* Confirmation Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 max-w-md w-full shadow-elevated space-y-4">
            <div className="text-3xl">📝</div>
            <h4 className="text-lg font-extrabold text-white">Submit Examination?</h4>
            <p className="text-xs text-text-secondary leading-relaxed">
              {unansweredCount > 0
                ? `You have ${unansweredCount} unanswered question${
                    unansweredCount > 1 ? "s" : ""
                  }. Unattempted questions will receive 0 marks.`
                : "You have answered all questions. Ready to calculate official DGCA score?"}
            </p>
            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setShowSubmitModal(false)}
                className="px-4 py-2 rounded-xl bg-surface-interactive text-text-secondary hover:text-white text-xs font-bold"
              >
                Keep Reviewing
              </button>
              <button
                onClick={handleFinalSubmit}
                className="px-5 py-2 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white text-xs font-extrabold shadow-card"
              >
                Confirm & Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function ExamPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-[500px] flex items-center justify-center">
          <div className="text-center space-y-3">
            <div className="text-3xl animate-bounce">✈️</div>
            <p className="text-sm font-bold text-text-secondary">
              Preparing examination environment...
            </p>
          </div>
        </div>
      }
    >
      <ExamSessionContent />
    </Suspense>
  );
}
