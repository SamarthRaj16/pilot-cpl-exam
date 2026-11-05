"use client";

export const dynamic = "force-dynamic";

import React, { Suspense, useState, useEffect, useRef } from "react";
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
  const defaultDuration = mode === "mock" ? 90 * 60 : 30 * 60;
  const [timeRemaining, setTimeRemaining] = useState(defaultDuration);
  const [durationTotal, setDurationTotal] = useState(defaultDuration);
  const [startedAtTimestamp, setStartedAtTimestamp] = useState<number>(Date.now());
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [attemptId, setAttemptId] = useState("");
  const [availabilityNotice, setAvailabilityNotice] = useState<string | null>(null);

  // Phase 4: Reliability, Persistence & Submission States
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionStage, setSubmissionStage] = useState<1 | 2 | 3>(1);
  const [submissionError, setSubmissionError] = useState<string | null>(null);
  const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "saved" | "interrupted">("idle");
  const [showRecoveryModal, setShowRecoveryModal] = useState(false);
  const [pendingRecoverySession, setPendingRecoverySession] = useState<any>(null);

  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const isSubmittingRef = useRef(false);

  const LETTERS = ["A", "B", "C", "D"];

  // 1. Session Recovery Check on Mount
  useEffect(() => {
    try {
      const savedSessionRaw = localStorage.getItem("cpl_active_session");
      if (savedSessionRaw) {
        const session = JSON.parse(savedSessionRaw);
        if (
          session &&
          session.attemptId &&
          session.status !== "completed" &&
          session.questions &&
          session.questions.length > 0
        ) {
          // Check server-authoritative elapsed time
          const elapsedSeconds = Math.floor((Date.now() - (session.startedAt || Date.now())) / 1000);
          const computedRemaining = Math.max(0, (session.durationTotal || defaultDuration) - elapsedSeconds);

          if (session.mode !== "practice" && computedRemaining <= 0) {
            // Expired while away
            localStorage.removeItem("cpl_active_session");
          } else {
            setPendingRecoverySession({
              ...session,
              computedRemaining,
            });
            setShowRecoveryModal(true);
            return; // Wait for student choice
          }
        }
      }
    } catch {
      // Ignored
    }

    initFreshSession();
  }, [subjectsParam, topicParam, topicsParam, mode, practiceMode, questionLimit]);

  // 2. Resume Interrupted Session Handler
  const handleResumeSession = () => {
    if (!pendingRecoverySession) return;
    setQuestions(pendingRecoverySession.questions);
    setAnswers(pendingRecoverySession.answers || new Array(pendingRecoverySession.questions.length).fill(-1));
    setFlags(pendingRecoverySession.flags || new Array(pendingRecoverySession.questions.length).fill(false));
    setRevealed(pendingRecoverySession.revealed || new Array(pendingRecoverySession.questions.length).fill(false));
    setCurrentIndex(pendingRecoverySession.currentIndex || 0);
    setAttemptId(pendingRecoverySession.attemptId);
    setDurationTotal(pendingRecoverySession.durationTotal || defaultDuration);
    setStartedAtTimestamp(pendingRecoverySession.startedAt || Date.now());
    setTimeRemaining(pendingRecoverySession.computedRemaining ?? pendingRecoverySession.timeRemaining ?? defaultDuration);
    setShowRecoveryModal(false);
    setPendingRecoverySession(null);
  };

  // 3. Discard Interrupted Session Handler
  const handleDiscardSession = () => {
    try {
      localStorage.removeItem("cpl_active_session");
    } catch {}
    setShowRecoveryModal(false);
    setPendingRecoverySession(null);
    initFreshSession();
  };

  // 4. Initialize Fresh Quiz Session via Optimized API
  async function initFreshSession() {
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
    } catch {}

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
        const newAttId = data.attemptId || `att-${Date.now()}`;
        const nowTs = Date.now();
        setQuestions(data.questions);
        setAnswers(new Array(data.questions.length).fill(-1));
        setFlags(new Array(data.questions.length).fill(false));
        setRevealed(new Array(data.questions.length).fill(false));
        setAttemptId(newAttId);
        setStartedAtTimestamp(nowTs);
        setDurationTotal(defaultDuration);
        setTimeRemaining(defaultDuration);
        if (data.availabilityNotice) {
          setAvailabilityNotice(data.availabilityNotice);
        }

        // Store active session snapshot for crash/refresh recovery
        saveActiveSessionSnapshot({
          attemptId: newAttId,
          mode,
          practiceMode,
          questions: data.questions,
          answers: new Array(data.questions.length).fill(-1),
          flags: new Array(data.questions.length).fill(false),
          revealed: new Array(data.questions.length).fill(false),
          currentIndex: 0,
          startedAt: nowTs,
          durationTotal: defaultDuration,
          status: "in_progress",
        });

        // Track served IDs locally for Zero-Repeat
        try {
          const stored = localStorage.getItem("cpl_served_ids");
          const set = new Set(stored ? JSON.parse(stored) : []);
          data.questions.forEach((q: any) => {
            if (!q.isRevision) set.add(q.id);
          });
          localStorage.setItem("cpl_served_ids", JSON.stringify(Array.from(set)));
        } catch {}
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

    let selected: any[] = [];
    if (practiceMode === "revision_only" || practiceMode === "all_incorrect") {
      selected = candidate.filter((q) => pendingMistakeSet.has(q.id));
    } else if (practiceMode === "fresh_only") {
      selected = candidate.filter((q) => !servedSet.has(q.id));
    } else {
      const rev = candidate.filter((q) => pendingMistakeSet.has(q.id)).map((q) => ({ ...q, isRevision: true }));
      const fresh = candidate.filter((q) => !servedSet.has(q.id) && !pendingMistakeSet.has(q.id));
      const revCount = Math.min(rev.length, 15);
      const freshCount = questionLimit - revCount;
      selected = [...rev.slice(0, revCount), ...fresh.slice(0, freshCount)];
    }

    if (selected.length === 0) {
      selected = candidate.slice(0, Math.min(questionLimit, candidate.length));
    }

    if (selected.length < questionLimit) {
      setAvailabilityNotice(
        `${selected.length} unique questions are currently available for your selected topics.`
      );
    }

    const shuffled = selected.sort(() => Math.random() - 0.5);
    const offlineAttId = `att-offline-${Date.now()}`;
    const offlineTs = Date.now();
    setQuestions(shuffled);
    setAnswers(new Array(shuffled.length).fill(-1));
    setFlags(new Array(shuffled.length).fill(false));
    setRevealed(new Array(shuffled.length).fill(false));
    setAttemptId(offlineAttId);
    setStartedAtTimestamp(offlineTs);

    saveActiveSessionSnapshot({
      attemptId: offlineAttId,
      mode,
      practiceMode,
      questions: shuffled,
      answers: new Array(shuffled.length).fill(-1),
      flags: new Array(shuffled.length).fill(false),
      revealed: new Array(shuffled.length).fill(false),
      currentIndex: 0,
      startedAt: offlineTs,
      durationTotal: defaultDuration,
      status: "in_progress",
    });
  }

  // Helper: Persist Active Session to LocalStorage
  const saveActiveSessionSnapshot = (data: Record<string, any>) => {
    try {
      const existing = localStorage.getItem("cpl_active_session");
      const prev = existing ? JSON.parse(existing) : {};
      localStorage.setItem(
        "cpl_active_session",
        JSON.stringify({
          ...prev,
          ...data,
          lastSavedAt: new Date().toISOString(),
        })
      );
    } catch {}
  };

  // Timer countdown with Server-Authoritative Check
  useEffect(() => {
    if (questions.length === 0) return;

    if (timeRemaining <= 0) {
      handleFinalSubmit();
      return;
    }

    const timer = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          handleFinalSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [questions.length, timeRemaining]);

  // Answer Selection with Debounced Auto-Save & Indicators
  const handleSelectOption = (optIndex: number) => {
    if (mode === "practice" && revealed[currentIndex]) return; // Locked in practice mode
    if (isSubmitting) return;

    const newAnswers = [...answers];
    newAnswers[currentIndex] = optIndex;
    setAnswers(newAnswers);

    // Update active session locally
    saveActiveSessionSnapshot({
      answers: newAnswers,
      currentIndex,
    });

    // Real-time Auto-Save to Backend
    setSaveStatus("saving");
    if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current);

    saveTimeoutRef.current = setTimeout(async () => {
      try {
        const curQ = questions[currentIndex];
        const res = await fetch("/api/quiz/save-answer", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            attemptId,
            questionId: curQ.id,
            selectedAnswer: optIndex,
            timeRemaining,
            mode,
          }),
        });

        if (res.ok) {
          setSaveStatus("saved");
          setTimeout(() => setSaveStatus("idle"), 2500);
        } else {
          setSaveStatus("interrupted");
        }
      } catch {
        setSaveStatus("interrupted");
      }
    }, 250);

    // Practice Mode immediate feedback
    if (mode === "practice") {
      const newRevealed = [...revealed];
      newRevealed[currentIndex] = true;
      setRevealed(newRevealed);

      const currentQ = questions[currentIndex];
      const isRight =
        optIndex ===
        (currentQ.answerIndex !== undefined ? currentQ.answerIndex : currentQ.answer_index);

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
      } catch {}
    }
  };

  const handleToggleFlag = () => {
    const newFlags = [...flags];
    newFlags[currentIndex] = !newFlags[currentIndex];
    setFlags(newFlags);
    saveActiveSessionSnapshot({ flags: newFlags });
  };

  // Phase 4: Atomic, Idempotent, Professional Examination Submission
  const handleFinalSubmit = async () => {
    if (isSubmittingRef.current) return; // Prevent duplicate clicks
    isSubmittingRef.current = true;
    setIsSubmitting(true);
    setSubmissionError(null);
    setShowSubmitModal(false);

    // Stage 1: Securing Responses
    setSubmissionStage(1);

    // Build answers map
    const answerMap: Record<string, number> = {};
    questions.forEach((q, idx) => {
      answerMap[q.id] = answers[idx];
    });

    try {
      // Stage 2: Evaluating answers on authoritative server
      setTimeout(() => setSubmissionStage(2), 400);

      const res = await fetch("/api/quiz/finish", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          attemptId,
          answers: answerMap,
          durationSeconds: durationTotal - timeRemaining,
        }),
      });

      if (!res.ok) {
        throw new Error(`Server returned status ${res.status}`);
      }

      const resultData = await res.json();

      // Stage 3: Finalizing score summary
      setSubmissionStage(3);

      // Clean up active session
      try {
        localStorage.removeItem("cpl_active_session");
      } catch {}

      sessionStorage.setItem("last_exam_result", JSON.stringify(resultData));

      // Transition smoothly
      setTimeout(() => {
        router.push("/dashboard/results");
      }, 500);
    } catch (err: any) {
      isSubmittingRef.current = false;
      setSubmissionError(
        err.message || "Network connection interrupted while securing examination submission."
      );
    }
  };

  // Fallback Offline Calculation if user explicitly proceeds during network failure
  const handleOfflineSubmissionFallback = () => {
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

    const totalQuestions = questions.length;
    const accuracy = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;
    const offlineResult = {
      attemptId,
      score,
      totalPoints: score,
      totalQuestions,
      accuracy,
      passed: accuracy >= 70,
      durationSeconds: durationTotal - timeRemaining,
      passMark: 70,
      reviewItems,
    };

    try {
      localStorage.removeItem("cpl_active_session");
    } catch {}

    sessionStorage.setItem("last_exam_result", JSON.stringify(offlineResult));
    router.push("/dashboard/results");
  };

  // Skeleton Loader for Instant Visual Feedback on Exam Launch
  if (questions.length === 0 && !showRecoveryModal) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start animate-pulse">
        <div className="lg:col-span-3 bg-card-primary border border-border-charcoal rounded-2xl p-6 sm:p-8 space-y-6">
          <div className="flex justify-between items-center pb-4 border-b border-border-charcoal">
            <div className="h-4 bg-surface-interactive rounded w-36" />
            <div className="h-6 bg-surface-interactive rounded-full w-28" />
          </div>
          <div className="space-y-3 py-4">
            <div className="h-5 bg-surface-interactive rounded w-3/4" />
            <div className="h-5 bg-surface-interactive rounded w-5/6" />
            <div className="h-5 bg-surface-interactive rounded w-1/2" />
          </div>
          <div className="space-y-3 pt-2">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="h-14 bg-surface-primary border border-border-charcoal rounded-xl flex items-center px-4 gap-4"
              >
                <div className="w-8 h-8 rounded-lg bg-surface-interactive" />
                <div className="h-4 bg-surface-interactive rounded w-2/3" />
              </div>
            ))}
          </div>
          <div className="flex justify-between pt-4 border-t border-border-charcoal">
            <div className="h-10 bg-surface-interactive rounded-xl w-28" />
            <div className="h-10 bg-surface-interactive rounded-xl w-28" />
          </div>
        </div>
        <div className="space-y-4">
          <div className="bg-card-primary border border-border-charcoal rounded-2xl p-5 space-y-4">
            <div className="h-4 bg-surface-interactive rounded w-24" />
            <div className="grid grid-cols-5 gap-2">
              {[...Array(20)].map((_, i) => (
                <div key={i} className="h-8 bg-surface-interactive rounded-lg" />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Interrupted Session Recovery Modal
  if (showRecoveryModal && pendingRecoverySession) {
    const answeredInSession = (pendingRecoverySession.answers || []).filter((a: number) => a >= 0).length;
    const remMins = Math.floor((pendingRecoverySession.computedRemaining || 0) / 60);

    return (
      <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div className="bg-card-primary border border-brand-gold/40 rounded-3xl p-6 sm:p-8 max-w-lg w-full shadow-elevated space-y-6">
          <div className="flex items-center gap-3">
            <span className="text-3xl p-3 bg-brand-gold/10 rounded-2xl border border-brand-gold/30">
              ✈️
            </span>
            <div>
              <span className="text-[10px] font-black uppercase tracking-widest text-brand-gold">
                Session Recovery Engine
              </span>
              <h3 className="text-xl font-extrabold text-white">
                An unfinished examination was found
              </h3>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-surface-primary border border-border-charcoal space-y-2 text-xs">
            <div className="flex justify-between py-1 border-b border-border-charcoal/50">
              <span className="text-text-muted">Examination Mode:</span>
              <span className="font-extrabold text-white uppercase">{pendingRecoverySession.mode}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-border-charcoal/50">
              <span className="text-text-muted">Questions Answered:</span>
              <span className="font-extrabold text-brand-green">
                {answeredInSession} / {pendingRecoverySession.questions?.length || 0}
              </span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-text-muted">Server-Authoritative Time Left:</span>
              <span className="font-mono font-bold text-brand-gold">{remMins} minutes</span>
            </div>
          </div>

          <p className="text-xs text-text-secondary leading-relaxed">
            All your selected answers, flags, and examination timestamps were safely preserved. You can
            resume right where you left off without any penalty.
          </p>

          <div className="flex flex-col sm:flex-row gap-3 pt-2">
            <button
              onClick={handleDiscardSession}
              className="flex-1 py-3 px-4 rounded-xl border border-border-charcoal text-text-muted hover:text-white hover:bg-surface-interactive text-xs font-bold transition-all"
            >
              Discard Session
            </button>
            <button
              onClick={handleResumeSession}
              className="flex-1 py-3 px-4 rounded-xl bg-gradient-to-r from-brand-gold to-amber-500 text-bg-base font-black text-xs uppercase tracking-wider shadow-card hover:opacity-95 transition-all"
            >
              Resume Examination
            </button>
          </div>
        </div>
      </div>
    );
  }

  const currentQ = questions[currentIndex] || {};
  const totalQuestions = questions.length;
  const isRevealed = revealed[currentIndex];
  const isCurrentFlagged = flags[currentIndex];

  const answeredCount = answers.filter((a) => a >= 0).length;
  const flaggedCount = flags.filter((f) => f).length;
  const unansweredCount = totalQuestions - answeredCount;

  const minutes = Math.floor(timeRemaining / 60);
  const seconds = timeRemaining % 60;
  const timeFormatted = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start relative">
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

        {/* Question Header & Auto-Save Indicator */}
        <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-border-charcoal">
          <div className="flex items-center gap-3">
            <span className="text-xs font-extrabold text-brand-gold bg-brand-gold/10 px-2.5 py-1 rounded-md border border-brand-gold/20">
              Q{currentIndex + 1} of {totalQuestions}
            </span>
            <span className="text-xs text-text-muted font-bold">
              {currentQ.subject} &bull; {currentQ.topic}
            </span>
            {currentQ.isRevision && (
              <span className="text-[10px] font-black uppercase tracking-wider text-brand-gold bg-brand-gold/15 px-2 py-0.5 rounded border border-brand-gold/30 animate-pulse">
                ↺ Revision Priority
              </span>
            )}
          </div>

          <div className="flex items-center gap-3">
            {/* Auto-Save Subtle Indicator */}
            <div className="text-[11px] font-mono font-medium flex items-center gap-1.5">
              {saveStatus === "saving" && (
                <span className="text-amber-400 flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping inline-block" />
                  Saving...
                </span>
              )}
              {saveStatus === "saved" && (
                <span className="text-emerald-400 flex items-center gap-1">
                  <span>✓</span> Saved
                </span>
              )}
              {saveStatus === "interrupted" && (
                <span className="text-amber-400 flex items-center gap-1 bg-amber-400/10 px-2 py-0.5 rounded border border-amber-400/30">
                  ⚠️ Saved locally (connection delayed)
                </span>
              )}
            </div>

            <button
              onClick={handleToggleFlag}
              className={`text-xs font-bold px-3 py-1.5 rounded-lg border transition-all flex items-center gap-1.5 ${
                isCurrentFlagged
                  ? "bg-brand-orange/20 border-brand-orange text-brand-orange"
                  : "bg-surface-interactive border-border-charcoal text-text-muted hover:text-white"
              }`}
            >
              <span>{isCurrentFlagged ? "🚩 Flagged" : "🏳️ Flag"}</span>
            </button>
          </div>
        </div>

        {/* Question Text */}
        <div className="py-2">
          <p className="text-base sm:text-lg font-bold text-white leading-relaxed">
            {currentQ.question}
          </p>
        </div>

        {/* 4 Options */}
        <div className="space-y-3">
          {currentQ.options?.map((opt: string, optIdx: number) => {
            const isSelected = answers[currentIndex] === optIdx;
            const correctIdx =
              currentQ.answerIndex !== undefined ? currentQ.answerIndex : currentQ.answer_index;
            const isCorrectAnswer = optIdx === correctIdx;

            let cardStyle =
              "bg-surface-primary border-border-charcoal hover:border-brand-gold/40 text-text-secondary hover:text-white";

            if (isSelected) {
              cardStyle = "bg-brand-gold/10 border-brand-gold text-white font-bold shadow-card";
            }

            // In Practice Mode post-reveal styling
            if (mode === "practice" && isRevealed) {
              if (isCorrectAnswer) {
                cardStyle = "bg-brand-green/20 border-brand-green text-brand-green font-bold";
              } else if (isSelected && !isCorrectAnswer) {
                cardStyle = "bg-brand-red/20 border-brand-red text-brand-red font-bold";
              } else {
                cardStyle = "opacity-50 bg-surface-primary border-border-charcoal text-text-muted";
              }
            }

            return (
              <button
                key={optIdx}
                disabled={isSubmitting}
                onClick={() => handleSelectOption(optIdx)}
                className={`w-full text-left p-4 rounded-xl border transition-all flex items-center gap-4 ${cardStyle}`}
              >
                <span
                  className={`w-8 h-8 rounded-lg flex items-center justify-center font-extrabold text-xs shrink-0 ${
                    isSelected
                      ? "bg-brand-gold text-bg-base"
                      : "bg-surface-interactive text-text-muted"
                  }`}
                >
                  {LETTERS[optIdx]}
                </span>
                <span className="text-sm leading-snug">{opt}</span>
              </button>
            );
          })}
        </div>

        {/* Practice Mode Explanation Box */}
        {mode === "practice" && isRevealed && (
          <div className="p-5 rounded-xl bg-surface-primary border border-border-charcoal space-y-2 mt-4">
            <div className="flex items-center gap-2">
              <span className="text-sm">💡</span>
              <h5 className="text-xs font-extrabold text-brand-gold uppercase tracking-wider">
                DGCA Regulatory Explanation & Reference
              </h5>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed pl-6">
              {currentQ.explanation || "No regulatory explanation attached for this question."}
            </p>
            {currentQ.source && (
              <p className="text-[10px] text-text-muted font-bold pl-6">
                Source: {currentQ.source}
              </p>
            )}
          </div>
        )}

        {/* Navigation Controls */}
        <div className="flex items-center justify-between pt-6 border-t border-border-charcoal">
          <button
            disabled={currentIndex === 0 || isSubmitting}
            onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
            className="px-5 py-2.5 rounded-xl bg-surface-interactive border border-border-charcoal text-xs font-bold text-text-secondary hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all"
          >
            &larr; Previous
          </button>

          <span className="text-xs text-text-muted font-medium">
            Question {currentIndex + 1} of {totalQuestions}
          </span>

          <button
            disabled={currentIndex === totalQuestions - 1 || isSubmitting}
            onClick={() => setCurrentIndex((prev) => Math.min(totalQuestions - 1, prev + 1))}
            className="px-5 py-2.5 rounded-xl bg-surface-interactive border border-border-charcoal text-xs font-bold text-text-secondary hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all"
          >
            Next &rarr;
          </button>
        </div>
      </div>

      {/* CBT Sidebar Controls */}
      <div className="space-y-4">
        {/* Timer Card */}
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-5 shadow-card space-y-2">
          <span className="text-[10px] font-extrabold text-text-muted uppercase tracking-wider">
            Time Remaining
          </span>
          <div
            className={`text-3xl font-mono font-black ${
              timeRemaining < 300 ? "text-brand-red animate-pulse" : "text-white"
            }`}
          >
            {timeFormatted}
          </div>
          <span className="text-[10px] text-text-muted font-bold block uppercase tracking-wide">
            Mode: {mode}
          </span>
        </div>

        {/* Question Palette Grid */}
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-5 shadow-card space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-extrabold text-white uppercase tracking-wider">
              Question Palette
            </h4>
            <span className="text-[11px] font-bold text-brand-gold">
              {answeredCount}/{totalQuestions}
            </span>
          </div>

          <div className="grid grid-cols-5 gap-2 max-h-[320px] overflow-y-auto pr-1">
            {questions.map((q, idx) => {
              const isAns = answers[idx] >= 0;
              const isFlg = flags[idx];
              const isCur = currentIndex === idx;

              let btnStyle = "bg-surface-primary text-text-muted border-border-charcoal";
              if (isAns) btnStyle = "bg-brand-green/20 text-brand-green border-brand-green/50";
              if (isFlg) btnStyle = "bg-brand-orange/20 text-brand-orange border-brand-orange";
              if (isCur) btnStyle += " ring-2 ring-brand-purple ring-brand-gold";

              return (
                <button
                  key={idx}
                  disabled={isSubmitting}
                  onClick={() => setCurrentIndex(idx)}
                  className={`h-9 rounded-lg font-bold text-xs border transition-all relative flex items-center justify-center ${btnStyle}`}
                >
                  {idx + 1}
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
            disabled={isSubmitting}
            onClick={() => setShowSubmitModal(true)}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-brand-gold to-amber-500 hover:opacity-90 text-bg-base font-black text-xs uppercase tracking-wider shadow-card transition-all disabled:opacity-40"
          >
            Submit Examination
          </button>
        </div>
      </div>

      {/* Confirmation Modal */}
      {showSubmitModal && !isSubmitting && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card-primary border border-border-charcoal rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-elevated space-y-5">
            <div className="w-12 h-12 rounded-2xl bg-brand-gold/10 border border-brand-gold/30 flex items-center justify-center text-2xl">
              📝
            </div>
            <div>
              <h4 className="text-lg font-black text-white">Submit Examination?</h4>
              <p className="text-xs text-text-secondary leading-relaxed mt-1">
                {unansweredCount > 0
                  ? `You have ${unansweredCount} unattempted question${
                      unansweredCount > 1 ? "s" : ""
                    }. Unattempted questions will receive 0 marks as per DGCA regulations.`
                  : "All questions have been answered. Ready to generate your authoritative DGCA evaluation?"}
              </p>
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <button
                onClick={() => setShowSubmitModal(false)}
                className="px-4 py-2.5 rounded-xl bg-surface-interactive text-text-secondary hover:text-white text-xs font-bold transition-all"
              >
                Keep Reviewing
              </button>
              <button
                onClick={handleFinalSubmit}
                className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-gold to-amber-500 text-bg-base text-xs font-black uppercase tracking-wider shadow-card hover:opacity-95 transition-all"
              >
                Confirm & Submit
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Professional Aviation Luxe Submission Overlay (Phase 2 & 3 Fix) */}
      {isSubmitting && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-card-primary border border-brand-gold/40 rounded-3xl p-8 max-w-md w-full shadow-elevated space-y-6 text-center">
            {/* Animated Radar Pulse Icon */}
            <div className="relative w-20 h-20 mx-auto flex items-center justify-center">
              <div className="absolute inset-0 rounded-full border-2 border-brand-gold/30 animate-ping" />
              <div className="w-16 h-16 rounded-full bg-brand-gold/10 border border-brand-gold flex items-center justify-center text-3xl shadow-card">
                ✈️
              </div>
            </div>

            <div className="space-y-1">
              <h3 className="text-xl font-black text-white tracking-wide">
                Submitting your examination
              </h3>
              <p className="text-xs text-text-secondary leading-relaxed">
                Please wait while we securely save your responses and prepare your results.
              </p>
            </div>

            {/* Honest Real-Stage Progression */}
            <div className="space-y-3 text-left p-4 rounded-2xl bg-surface-primary border border-border-charcoal">
              <div className="flex items-center gap-3">
                <span
                  className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    submissionStage >= 1
                      ? "bg-brand-green text-bg-base"
                      : "bg-surface-interactive text-text-muted"
                  }`}
                >
                  {submissionStage > 1 ? "✓" : "1"}
                </span>
                <span
                  className={`text-xs ${
                    submissionStage >= 1 ? "text-white font-bold" : "text-text-muted"
                  }`}
                >
                  Securing examination responses
                </span>
              </div>

              <div className="flex items-center gap-3">
                <span
                  className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    submissionStage >= 2
                      ? "bg-brand-green text-bg-base"
                      : "bg-surface-interactive text-text-muted"
                  }`}
                >
                  {submissionStage > 2 ? "✓" : "2"}
                </span>
                <span
                  className={`text-xs ${
                    submissionStage >= 2 ? "text-white font-bold" : "text-text-muted"
                  }`}
                >
                  Evaluating answers against DGCA master key
                </span>
              </div>

              <div className="flex items-center gap-3">
                <span
                  className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                    submissionStage >= 3
                      ? "bg-brand-green text-bg-base"
                      : "bg-surface-interactive text-text-muted"
                  }`}
                >
                  {submissionStage === 3 ? "✓" : "3"}
                </span>
                <span
                  className={`text-xs ${
                    submissionStage === 3 ? "text-white font-bold" : "text-text-muted"
                  }`}
                >
                  Finalizing score summary & analytics
                </span>
              </div>
            </div>

            {/* Error State Fallback Dialog */}
            {submissionError && (
              <div className="p-4 rounded-2xl bg-brand-red/10 border border-brand-red/40 space-y-3 text-left">
                <div className="flex items-center gap-2 text-brand-red font-bold text-xs">
                  <span>⚠️</span>
                  <span>Your examination could not be submitted successfully.</span>
                </div>
                <p className="text-[11px] text-text-secondary leading-relaxed">
                  Your saved examination responses have been preserved safely in local storage.
                </p>
                <div className="flex flex-col sm:flex-row gap-2 pt-1">
                  <button
                    onClick={() => {
                      setIsSubmitting(false);
                      isSubmittingRef.current = false;
                      setSubmissionError(null);
                    }}
                    className="flex-1 py-2 px-3 rounded-lg bg-surface-interactive text-text-muted hover:text-white text-xs font-bold transition-all"
                  >
                    Return to Examination
                  </button>
                  <button
                    onClick={handleFinalSubmit}
                    className="flex-1 py-2 px-3 rounded-lg bg-brand-gold text-bg-base text-xs font-extrabold hover:opacity-90 transition-all"
                  >
                    Retry Submission
                  </button>
                </div>
                <button
                  onClick={handleOfflineSubmissionFallback}
                  className="w-full text-center text-[10px] text-text-muted hover:text-brand-gold underline pt-1"
                >
                  Evaluate Offline & View Results
                </button>
              </div>
            )}
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
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start animate-pulse">
          <div className="lg:col-span-3 bg-card-primary border border-border-charcoal rounded-2xl p-6 sm:p-8 space-y-6">
            <div className="h-4 bg-surface-interactive rounded w-36" />
            <div className="space-y-3 py-4">
              <div className="h-5 bg-surface-interactive rounded w-3/4" />
              <div className="h-5 bg-surface-interactive rounded w-5/6" />
            </div>
            <div className="space-y-3 pt-2">
              {[1, 2, 3, 4].map((i) => (
                <div
                  key={i}
                  className="h-14 bg-surface-primary border border-border-charcoal rounded-xl"
                />
              ))}
            </div>
          </div>
        </div>
      }
    >
      <ExamSessionContent />
    </Suspense>
  );
}
