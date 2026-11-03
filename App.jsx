import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HomeScreen from './components/HomeScreen';
import QuizScreen from './components/QuizScreen';
import ResultsScreen from './components/ResultsScreen';
import ReviewScreen from './components/ReviewScreen';
import ConfirmModal from './components/ConfirmModal';
import { useLocalStorage } from './hooks/useLocalStorage';

import questionsData from './data/questions.json';
import examConfigData from './data/examConfig.json';

// Helper: Fisher-Yates array shuffle
function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Helper: Prepare question with shuffled options and remapped answerIndex
function prepareQuestion(q) {
  const indices = [0, 1, 2, 3];
  const shuffledIndices = shuffleArray(indices);
  const newOptions = shuffledIndices.map(i => q.options[i]);
  const newAnswerIndex = shuffledIndices.indexOf(q.answerIndex);

  return {
    ...q,
    originalOptions: q.options,
    originalAnswerIndex: q.answerIndex,
    options: newOptions,
    answerIndex: newAnswerIndex
  };
}

export default function App() {
  const [darkMode, setDarkMode] = useLocalStorage('dgca_cpl_dark_mode', false);
  const [history, setHistory] = useLocalStorage('dgca_cpl_history', []);
  const [activeSession, setActiveSession] = useLocalStorage('dgca_cpl_active_session', null);

  const [currentScreen, setCurrentScreen] = useState('home'); // 'home' | 'quiz' | 'results' | 'review'
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [quizConfig, setQuizConfig] = useState({ mode: 'practice', timeLimitMinutes: 0 });
  const [sessionResult, setSessionResult] = useState(null);

  const [showExitConfirm, setShowExitConfirm] = useState(false);
  const [showResetConfirm, setShowResetConfirm] = useState(false);

  // Apply dark theme attribute to HTML root
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  // Restore active session on load if user refreshed
  useEffect(() => {
    if (activeSession && activeSession.questions && activeSession.questions.length > 0 && currentScreen === 'home') {
      setQuizQuestions(activeSession.questions);
      setQuizConfig(activeSession.config);
      setCurrentScreen('quiz');
    }
  }, []);

  // Start Quiz handler
  const handleStartQuiz = ({ pool, questionLimit, mode, timeLimitMinutes }) => {
    if (!pool || pool.length === 0) return;

    // 1. Randomise question order
    const shuffledPool = shuffleArray(pool).slice(0, questionLimit);

    // 2. Randomise option order for every question
    const preparedQuestions = shuffledPool.map(prepareQuestion);

    const config = { mode, timeLimitMinutes };
    setQuizQuestions(preparedQuestions);
    setQuizConfig(config);
    setActiveSession({ questions: preparedQuestions, config });
    setCurrentScreen('quiz');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Finish Quiz / Submit handler
  const handleFinishQuiz = ({ userAnswers, flags, timeTakenSeconds, timedOut }) => {
    setActiveSession(null);

    let correctCount = 0;
    const subjBreakdownMap = {};
    const topicBreakdownMap = {};
    const wrongQuestions = [];

    quizQuestions.forEach((q, i) => {
      const selected = userAnswers[i];
      const isCorrect = selected === q.answerIndex;

      if (isCorrect) correctCount++;
      else {
        wrongQuestions.push({
          question: q,
          userSelected: selected,
          correctIndex: q.answerIndex
        });
      }

      // Subject breakdown
      if (!subjBreakdownMap[q.subject]) {
        subjBreakdownMap[q.subject] = { total: 0, correct: 0 };
      }
      subjBreakdownMap[q.subject].total++;
      if (isCorrect) subjBreakdownMap[q.subject].correct++;

      // Topic breakdown
      const topic = q.topic || 'General';
      if (!topicBreakdownMap[topic]) {
        topicBreakdownMap[topic] = { total: 0, correct: 0, subject: q.subject };
      }
      topicBreakdownMap[topic].total++;
      if (isCorrect) topicBreakdownMap[topic].correct++;
    });

    const total = quizQuestions.length;
    const percentage = total > 0 ? Math.round((correctCount / total) * 100) : 0;
    const isPass = percentage >= examConfigData.generalRules.passPercentage;

    const breakdown = Object.entries(subjBreakdownMap).map(([subject, data]) => ({
      subject,
      total: data.total,
      correct: data.correct,
      percentage: Math.round((data.correct / data.total) * 100)
    }));

    const topicBreakdown = Object.entries(topicBreakdownMap).map(([topic, data]) => ({
      topic,
      subject: data.subject,
      total: data.total,
      correct: data.correct,
      percentage: Math.round((data.correct / data.total) * 100)
    }));

    const result = {
      id: Date.now(),
      date: new Date().toISOString(),
      mode: quizConfig.mode,
      total,
      score: correctCount,
      percentage,
      isPass,
      timeTakenSeconds,
      timedOut,
      breakdown,
      topicBreakdown,
      wrongQuestions,
      allQuestions: quizQuestions
    };

    setSessionResult(result);
    setHistory(prev => [result, ...prev]);
    setCurrentScreen('results');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Quit active quiz
  const handleQuitQuiz = () => {
    setActiveSession(null);
    setCurrentScreen('home');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Retake all questions from this session
  const handleRetakeFull = () => {
    const freshPrepared = sessionResult.allQuestions.map(q => {
      // Re-shuffle from original options
      const unrolled = {
        ...q,
        options: q.originalOptions || q.options,
        answerIndex: q.originalAnswerIndex !== undefined ? q.originalAnswerIndex : q.answerIndex
      };
      return prepareQuestion(unrolled);
    });

    setQuizQuestions(freshPrepared);
    setActiveSession({ questions: freshPrepared, config: quizConfig });
    setCurrentScreen('quiz');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Retry only incorrectly answered questions
  const handleRetryWrongOnly = () => {
    if (!sessionResult || !sessionResult.wrongQuestions || sessionResult.wrongQuestions.length === 0) return;

    const wrongList = sessionResult.wrongQuestions.map(item => {
      const q = item.question;
      const unrolled = {
        ...q,
        options: q.originalOptions || q.options,
        answerIndex: q.originalAnswerIndex !== undefined ? q.originalAnswerIndex : q.answerIndex
      };
      return prepareQuestion(unrolled);
    });

    const freshQuestions = shuffleArray(wrongList);
    const newConfig = { mode: 'practice', timeLimitMinutes: 0 };
    setQuizQuestions(freshQuestions);
    setQuizConfig(newConfig);
    setActiveSession({ questions: freshQuestions, config: newConfig });
    setCurrentScreen('quiz');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Reset all history progress
  const handleConfirmReset = () => {
    setHistory([]);
    setActiveSession(null);
    setShowResetConfirm(false);
  };

  return (
    <div className="app-container">
      <Header
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        isQuizActive={currentScreen === 'quiz'}
        onGoHome={() => {
          if (currentScreen === 'quiz') {
            setShowExitConfirm(true);
          } else {
            setCurrentScreen('home');
          }
        }}
      />

      <main>
        {currentScreen === 'home' && (
          <HomeScreen
            examConfig={examConfigData}
            allQuestions={questionsData}
            history={history}
            onStartQuiz={handleStartQuiz}
            onResetProgress={() => setShowResetConfirm(true)}
          />
        )}

        {currentScreen === 'quiz' && (
          <QuizScreen
            questions={quizQuestions}
            mode={quizConfig.mode}
            timeLimitMinutes={quizConfig.timeLimitMinutes}
            onFinishQuiz={handleFinishQuiz}
            onQuitQuiz={handleQuitQuiz}
          />
        )}

        {currentScreen === 'results' && sessionResult && (
          <ResultsScreen
            sessionResult={sessionResult}
            onReviewMistakes={() => setCurrentScreen('review')}
            onRetryWrongOnly={handleRetryWrongOnly}
            onRetakeFull={handleRetakeFull}
            onReturnHome={() => setCurrentScreen('home')}
          />
        )}

        {currentScreen === 'review' && sessionResult && (
          <ReviewScreen
            wrongQuestions={sessionResult.wrongQuestions}
            onBackToResults={() => setCurrentScreen('results')}
            onRetryWrongOnly={handleRetryWrongOnly}
          />
        )}
      </main>

      {/* Confirmation Modals */}
      <ConfirmModal
        isOpen={showExitConfirm}
        title="Leave Active Exam Session?"
        message="An examination session is currently underway. Leaving will discard your current progress."
        confirmText="Yes, Return to Home"
        cancelText="Stay on Exam"
        isDanger={true}
        onConfirm={() => {
          setShowExitConfirm(false);
          handleQuitQuiz();
        }}
        onCancel={() => setShowExitConfirm(false)}
      />

      <ConfirmModal
        isOpen={showResetConfirm}
        title="Reset All Progress and History?"
        message="This action will permanently delete your test history, accuracy metrics, and weak topic analytics from localStorage. This cannot be undone."
        confirmText="Yes, Reset Everything"
        cancelText="Cancel"
        isDanger={true}
        onConfirm={handleConfirmReset}
        onCancel={() => setShowResetConfirm(false)}
      />
    </div>
  );
}

