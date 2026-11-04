"use client";

import React, { Suspense, useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import rawQuestions from "@/data/questions.json";

function ExamSessionContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const subjectsParam = searchParams.get("subjects");
  const topicParam = searchParams.get("topic");
  const mode = (searchParams.get("mode") || "practice") as "practice" | "timed" | "mock";

  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [flags, setFlags] = useState<boolean[]>([]);
  const [revealed, setRevealed] = useState<boolean[]>([]);
  const [timeRemaining, setTimeRemaining] = useState(mode === "mock" ? 90 * 60 : 30 * 60);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [attemptId, setAttemptId] = useState("");

  const LETTERS = ["A", "B", "C", "D"];

  // Initialize Quiz Session via API
  useEffect(() => {
    async function initSession() {
      try {
        const res = await fetch("/api/quiz/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            subjectId: subjectsParam ? subjectsParam.split(",")[0] : undefined,
            topicId: topicParam || undefined,
            mode,
            questionCount: mode === "mock" ? 50 : 30,
          }),
        });

        const data = await res.json();
        if (data.questions && data.questions.length > 0) {
          setQuestions(data.questions);
          setAnswers(new Array(data.questions.length).fill(-1));
          setFlags(new Array(data.questions.length).fill(false));
          setRevealed(new Array(data.questions.length).fill(false));
          setAttemptId(data.attemptId || `att-${Date.now()}`);

          // Track served IDs locally for Zero-Repeat
          try {
            const stored = localStorage.getItem("cpl_served_ids");
            const set = new Set(stored ? JSON.parse(stored) : []);
            data.questions.forEach((q: any) => set.add(q.id));
            localStorage.setItem("cpl_served_ids", JSON.stringify(Array.from(set)));
          } catch {
            // Ignored
          }
        } else {
          // Fallback from rawQuestions
          const filtered = rawQuestions.slice(0, 30);
          setQuestions(filtered);
          setAnswers(new Array(filtered.length).fill(-1));
          setFlags(new Array(filtered.length).fill(false));
          setRevealed(new Array(filtered.length).fill(false));
        }
      } catch {
        const filtered = rawQuestions.slice(0, 30);
        setQuestions(filtered);
        setAnswers(new Array(filtered.length).fill(-1));
        setFlags(new Array(filtered.length).fill(false));
        setRevealed(new Array(filtered.length).fill(false));
      }
    }
    initSession();
  }, [subjectsParam, topicParam, mode]);

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
  const isAnswered = answers[currentIndex] >= 0;
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
      router.push("/dashboard");
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
        {/* Header */}
        <div className="flex flex-wrap items-center justify-between gap-3 pb-5 border-b border-border-charcoal">
          <div>
            <span className="text-xs font-bold text-brand-purple uppercase tracking-wider">
              {currentQ.subject}
            </span>
            <div className="text-sm font-extrabold text-white mt-0.5">
              {currentQ.topic || "General"}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs uppercase font-bold px-2.5 py-1 rounded-md bg-card-elevated border border-border-charcoal text-brand-gold">
              {currentQ.difficulty || "Medium"}
            </span>
            <span className="text-xs uppercase font-bold px-2.5 py-1 rounded-md bg-surface-interactive text-text-muted">
              {mode.toUpperCase()}
            </span>
          </div>
        </div>

        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-xs text-text-muted font-bold mb-2">
            <span>
              Question {currentIndex + 1} of {totalQuestions}
            </span>
            <span>{Math.round(((currentIndex + 1) / totalQuestions) * 100)}% Complete</span>
          </div>
          <div className="w-full h-1.5 bg-surface-interactive rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-brand-blue to-brand-purple transition-all duration-300 rounded-full"
              style={{ width: `${((currentIndex + 1) / totalQuestions) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Question Prompt */}
        <div className="py-2">
          <h3 className="text-base sm:text-lg font-bold text-white leading-relaxed">
            {currentQ.question}
          </h3>
        </div>

        {/* Options */}
        <div className="space-y-3">
          {currentQ.options.map((opt: string, oi: number) => {
            const isSelected = answers[currentIndex] === oi;
            const isCorrect = mode === "practice" && isRevealed && oi === currentQ.answerIndex;
            const isWrong =
              mode === "practice" && isRevealed && isSelected && oi !== currentQ.answerIndex;

            let btnStyle =
              "bg-card-elevated border-border-charcoal text-text-primary hover:border-brand-purple hover:bg-surface-interactive";
            if (isCorrect) {
              btnStyle = "bg-brand-green/20 border-brand-green text-white";
            } else if (isWrong) {
              btnStyle = "bg-brand-red/20 border-brand-red text-white";
            } else if (isSelected) {
              btnStyle = "bg-surface-interactive border-brand-purple text-white shadow-glow";
            }

            return (
              <button
                key={oi}
                onClick={() => handleSelectOption(oi)}
                className={`w-full p-4 rounded-xl border text-left text-sm font-medium transition-all flex items-center justify-between gap-4 ${btnStyle}`}
              >
                <div className="flex items-center gap-3">
                  <span
                    className={`w-7 h-7 rounded-lg flex items-center justify-center font-extrabold text-xs flex-shrink-0 ${
                      isCorrect
                        ? "bg-brand-green text-black"
                        : isWrong
                        ? "bg-brand-red text-white"
                        : isSelected
                        ? "bg-brand-purple text-white"
                        : "bg-surface-interactive text-text-secondary"
                    }`}
                  >
                    {LETTERS[oi]}
                  </span>
                  <span>{opt}</span>
                </div>
                {isCorrect && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-brand-green text-black">
                    ✓ Correct (+1 pt)
                  </span>
                )}
                {isWrong && (
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-brand-red text-white">
                    ✗ Your Choice (0 pts)
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Instant Authoritative Feedback (Practice Mode) */}
        {mode === "practice" && isRevealed && (
          <div
            className={`p-5 rounded-xl border text-sm space-y-2 animate-fadeIn ${
              answers[currentIndex] === currentQ.answerIndex
                ? "bg-brand-green/10 border-brand-green/30 text-text-primary"
                : "bg-brand-red/10 border-brand-red/30 text-text-primary"
            }`}
          >
            <div className="font-extrabold flex items-center gap-2">
              {answers[currentIndex] === currentQ.answerIndex ? (
                <span className="text-brand-green">✓ Correct! (+1 Point Received)</span>
              ) : (
                <span className="text-brand-red">
                  ✗ Incorrect (0 Points) &bull; Authoritative Answer:{" "}
                  {LETTERS[currentQ.answerIndex]}. {currentQ.options[currentQ.answerIndex]}
                </span>
              )}
            </div>
            <p className="text-text-secondary leading-relaxed pt-1">
              <strong>Explanation:</strong> {currentQ.explanation}
            </p>
            <div className="text-xs font-bold text-text-muted pt-2 border-t border-border-charcoal/40">
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

          <div className="grid grid-cols-5 gap-2 max-h-60 overflow-y-auto pr-1">
            {questions.map((_, idx) => {
              const isCurrent = idx === currentIndex;
              const ans = answers[idx] >= 0;
              const flag = flags[idx];

              let cellStyle = "bg-card-elevated border-border-charcoal text-text-secondary";
              if (isCurrent) {
                cellStyle = "border-brand-purple ring-2 ring-brand-purple text-white";
              } else if (ans) {
                cellStyle = "bg-brand-green/20 border-brand-green text-brand-green";
              } else if (flag) {
                cellStyle = "bg-brand-orange/20 border-brand-orange text-brand-orange";
              }

              return (
                <button
                  key={idx}
                  onClick={() => setCurrentIndex(idx)}
                  className={`aspect-square rounded-lg border text-xs font-extrabold flex items-center justify-center transition-all ${cellStyle}`}
                >
                  {idx + 1}
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

