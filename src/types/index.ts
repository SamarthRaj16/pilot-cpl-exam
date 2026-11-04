export type Role = "student" | "admin";

export interface Profile {
  id: string;
  email: string;
  full_name: string;
  role: Role;
  avatar_url?: string;
  study_streak: number;
  total_points: number;
  last_active_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Subject {
  id: string;
  name: string;
  code: string;
  icon: string;
  color: string;
  description?: string;
  default_question_count: number;
  default_duration_minutes: number;
  pass_percentage: number;
  display_order: number;
}

export interface Topic {
  id: string;
  subject_id: string;
  name: string;
  chapter_info?: string;
  display_order: number;
}

export type Difficulty = "easy" | "medium" | "hard";
export type ValidationStatus = "approved" | "pending" | "rejected" | "archived";

export interface Question {
  id: string; // Permanent ID e.g. NAV-001
  subject_id: string;
  topic_id: string;
  topic_name: string;
  difficulty: Difficulty;
  question: string;
  options: string[]; // exactly 4 options
  answer_index: number; // 0..3 (hidden in Mock Exam mode before submission!)
  explanation: string;
  source: string;
  validation_status: ValidationStatus;
  created_at?: string;
  updated_at?: string;
}

// Client-sanitized question for secure exam delivery (without answer key)
export interface SecureExamQuestion {
  id: string;
  subject_id: string;
  topic_id: string;
  topic_name: string;
  difficulty: Difficulty;
  question: string;
  options: string[];
}

export type QuizMode = "practice" | "timed" | "mock";

export interface QuizAttempt {
  id: string;
  student_id: string;
  subject_id?: string;
  topic_id?: string;
  mode: QuizMode;
  total_questions: number;
  score: number;
  accuracy: number;
  passed: boolean;
  duration_seconds: number;
  started_at: string;
  completed_at?: string;
}

export interface StudentAnswer {
  id: string;
  attempt_id: string;
  student_id: string;
  question_id: string;
  selected_answer: number;
  is_correct: boolean;
  points_awarded: number;
  answered_at: string;
}

export interface MistakeNotebookItem {
  id: string;
  student_id: string;
  question_id: string;
  subject_id: string;
  topic_id: string;
  incorrect_count: number;
  corrected_count: number;
  status: "unresolved" | "resolved";
  last_incorrect_choice?: number;
  last_attempted_at: string;
  resolved_at?: string;
  question?: Question;
}

export interface SpacedRepetitionItem {
  id: string;
  student_id: string;
  question_id: string;
  subject_id: string;
  ease_factor: number;
  interval_days: number;
  repetitions: number;
  next_review_date: string;
  last_reviewed_at: string;
  question?: Question;
}

export interface BookmarkItem {
  id: string;
  student_id: string;
  question_id: string;
  created_at: string;
  question?: Question;
}

export interface StudyGoal {
  id: string;
  student_id: string;
  goal_type: "daily_questions" | "weekly_mock" | "study_time" | "subject_mastery";
  target_value: number;
  current_value: number;
  period: "daily" | "weekly" | "monthly";
  target_date?: string;
  completed: boolean;
  created_at: string;
}

export interface AviationDocument {
  id: string;
  subject_id: string;
  topic_id?: string;
  title: string;
  description?: string;
  file_url: string;
  file_type: string;
  source?: string;
  is_public: boolean;
  created_at: string;
}

export interface AuditLog {
  id: string;
  user_id?: string;
  action: string;
  entity_type: string;
  entity_id?: string;
  details?: Record<string, any>;
  ip_address?: string;
  created_at: string;
}

export interface ExamConfigSubject {
  questions: number;
  duration: number;
}

export interface ExamConfig {
  passMark: number;
  negativeMarking: boolean;
  subjects: Record<string, ExamConfigSubject>;
}

export interface ReadinessScore {
  overallScore: number; // 0 to 100
  status: "Exam Ready" | "Developing" | "Action Needed" | "Insufficient Data";
  subjectScores: Record<
    string,
    {
      score: number;
      attempted: number;
      accuracy: number;
      coverage: number;
      status: "PASS READY" | "NEEDS FOCUS" | "CRITICAL" | "INSUFFICIENT DATA";
    }
  >;
  weakestSubject?: string;
  strongestSubject?: string;
  recommendedActions: string[];
}

