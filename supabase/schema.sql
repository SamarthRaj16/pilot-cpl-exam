-- ====================================================================
-- CPL PRACTICE 2.0 — FULL-STACK SUPABASE POSTGRESQL SCHEMA
-- Schema Migration: 20261104000000_cpl_core_schema.sql
-- ====================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. PROFILES (Students and Administrators)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'student' CHECK (role IN ('student', 'admin')),
    avatar_url TEXT,
    study_streak INTEGER NOT NULL DEFAULT 0,
    total_points INTEGER NOT NULL DEFAULT 0,
    recovered_questions INTEGER NOT NULL DEFAULT 0,
    revision_limit INTEGER NOT NULL DEFAULT 20,
    study_preferences JSONB DEFAULT '{"target_exam_date": null, "daily_goal_questions": 30, "preferred_mode": "practice"}'::jsonb,
    last_active_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. SUBJECTS
CREATE TABLE IF NOT EXISTS public.subjects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL,
    icon TEXT NOT NULL,
    color TEXT NOT NULL,
    description TEXT,
    default_question_count INTEGER NOT NULL DEFAULT 50,
    default_duration_minutes INTEGER NOT NULL DEFAULT 90,
    pass_percentage INTEGER NOT NULL DEFAULT 70,
    display_order INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. TOPICS / CHAPTERS
CREATE TABLE IF NOT EXISTS public.topics (
    id TEXT PRIMARY KEY,
    subject_id TEXT NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    chapter_info TEXT,
    display_order INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (subject_id, name)
);

-- 4. QUESTIONS (MASTER REPOSITORY)
CREATE TABLE IF NOT EXISTS public.questions (
    id TEXT PRIMARY KEY, -- Permanent ID (e.g. NAV-001, REG-045)
    subject_id TEXT NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    topic_id TEXT NOT NULL REFERENCES public.topics(id) ON DELETE CASCADE,
    topic_name TEXT NOT NULL,
    difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    question TEXT NOT NULL,
    options JSONB NOT NULL, -- Array of 4 strings
    answer_index INTEGER NOT NULL CHECK (answer_index >= 0 AND answer_index <= 3),
    explanation TEXT NOT NULL,
    source TEXT NOT NULL,
    validation_status TEXT NOT NULL DEFAULT 'approved' CHECK (validation_status IN ('approved', 'pending', 'rejected', 'archived')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. QUESTION EXPOSURE HISTORY (ZERO-REPEAT ROTATION ENGINE)
CREATE TABLE IF NOT EXISTS public.question_exposure_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    question_id TEXT NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    subject_id TEXT NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    topic_id TEXT NOT NULL REFERENCES public.topics(id) ON DELETE CASCADE,
    first_served_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    exposure_count INTEGER NOT NULL DEFAULT 1,
    UNIQUE (student_id, question_id)
);

-- 6. QUIZ ATTEMPTS (EXAMINATION SESSIONS)
CREATE TABLE IF NOT EXISTS public.quiz_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    subject_id TEXT REFERENCES public.subjects(id) ON DELETE SET NULL,
    topic_id TEXT REFERENCES public.topics(id) ON DELETE SET NULL,
    mode TEXT NOT NULL CHECK (mode IN ('practice', 'timed', 'mock')),
    total_questions INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    accuracy NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    duration_seconds INTEGER NOT NULL DEFAULT 0,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- 7. STUDENT ANSWERS (QUESTION-BY-QUESTION LOG)
CREATE TABLE IF NOT EXISTS public.student_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    attempt_id UUID NOT NULL REFERENCES public.quiz_attempts(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    question_id TEXT NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    selected_answer INTEGER NOT NULL, -- 0, 1, 2, 3, or -1 (skipped)
    is_correct BOOLEAN NOT NULL,
    points_awarded INTEGER NOT NULL DEFAULT 0,
    answered_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. MISTAKE NOTEBOOK
CREATE TABLE IF NOT EXISTS public.mistake_notebook (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    question_id TEXT NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    subject_id TEXT NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    topic_id TEXT NOT NULL REFERENCES public.topics(id) ON DELETE CASCADE,
    incorrect_count INTEGER NOT NULL DEFAULT 1,
    corrected_count INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'unresolved' CHECK (status IN ('unresolved', 'resolved')),
    last_incorrect_choice INTEGER,
    last_attempted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    UNIQUE (student_id, question_id)
);

-- 8b. STUDENT MISTAKES (REVISION QUEUE & PERSISTENCE)
CREATE TABLE IF NOT EXISTS public.student_mistakes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    question_id TEXT NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    subject_id TEXT,
    topic_id TEXT,
    status TEXT NOT NULL DEFAULT 'unresolved' CHECK (status IN ('unresolved', 'pending_revision', 'resolved', 'ignored')),
    incorrect_count INTEGER NOT NULL DEFAULT 1,
    last_incorrect_choice INTEGER,
    authoritative_answer INTEGER,
    notes TEXT,
    recovered_at TIMESTAMPTZ,
    last_attempted_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (student_id, question_id)
);

-- 9. SPACED REPETITION (SM-2 ADAPTIVE REVISION)
CREATE TABLE IF NOT EXISTS public.spaced_repetition (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    question_id TEXT NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    subject_id TEXT NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    ease_factor NUMERIC(4,2) NOT NULL DEFAULT 2.50,
    interval_days INTEGER NOT NULL DEFAULT 1,
    repetitions INTEGER NOT NULL DEFAULT 0,
    next_review_date DATE NOT NULL DEFAULT CURRENT_DATE + INTERVAL '1 day',
    last_reviewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (student_id, question_id)
);

-- 10. BOOKMARKS
CREATE TABLE IF NOT EXISTS public.bookmarks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    question_id TEXT NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (student_id, question_id)
);

-- 11. STUDY GOALS
CREATE TABLE IF NOT EXISTS public.study_goals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    goal_type TEXT NOT NULL CHECK (goal_type IN ('daily_questions', 'weekly_mock', 'study_time', 'subject_mastery')),
    target_value INTEGER NOT NULL,
    current_value INTEGER NOT NULL DEFAULT 0,
    period TEXT NOT NULL CHECK (period IN ('daily', 'weekly', 'monthly')),
    target_date DATE,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 12. AVIATION REFERENCE LIBRARY
CREATE TABLE IF NOT EXISTS public.aviation_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id TEXT NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    topic_id TEXT REFERENCES public.topics(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    description TEXT,
    file_url TEXT NOT NULL,
    file_type TEXT NOT NULL DEFAULT 'pdf',
    source TEXT,
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 13. AUDIT LOGS
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    action TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    entity_id TEXT,
    details JSONB,
    ip_address TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ====================================================================
-- PERFORMANCE INDEXES
-- ====================================================================
CREATE INDEX IF NOT EXISTS idx_questions_subject_topic ON public.questions (subject_id, topic_id);
CREATE INDEX IF NOT EXISTS idx_questions_status ON public.questions (validation_status);
CREATE INDEX IF NOT EXISTS idx_exposure_student_subject ON public.question_exposure_history (student_id, subject_id);
CREATE INDEX IF NOT EXISTS idx_exposure_student_topic ON public.question_exposure_history (student_id, topic_id);
CREATE INDEX IF NOT EXISTS idx_attempts_student ON public.quiz_attempts (student_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_answers_attempt ON public.student_answers (attempt_id);
CREATE INDEX IF NOT EXISTS idx_notebook_student ON public.mistake_notebook (student_id, status);
CREATE INDEX IF NOT EXISTS idx_repetition_due ON public.spaced_repetition (student_id, next_review_date);

-- ====================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ====================================================================
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.question_exposure_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quiz_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mistake_notebook ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_mistakes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.spaced_repetition ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bookmarks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.study_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.aviation_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- Helper function: Is Current User Admin?
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = auth.uid() AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Subjects & Topics: Publicly readable by authenticated students, manageable by admins
CREATE POLICY "Subjects are viewable by authenticated users" ON public.subjects FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Subjects are manageable by admins" ON public.subjects FOR ALL USING (public.is_admin());

CREATE POLICY "Topics are viewable by authenticated users" ON public.topics FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "Topics are manageable by admins" ON public.topics FOR ALL USING (public.is_admin());

-- Questions: Approved questions viewable by authenticated users, all manageable by admins
CREATE POLICY "Approved questions viewable by authenticated users" ON public.questions FOR SELECT USING (auth.role() = 'authenticated' AND (validation_status = 'approved' OR public.is_admin()));
CREATE POLICY "Questions are manageable by admins" ON public.questions FOR ALL USING (public.is_admin());

-- Profiles: Users can view and update their own profile; admins can view all
CREATE POLICY "Users can view own profile" ON public.profiles FOR SELECT USING (auth.uid() = id OR public.is_admin());
CREATE POLICY "Users can update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);

-- Exposure History: Strict student isolation
CREATE POLICY "Users can manage own exposure history" ON public.question_exposure_history FOR ALL USING (auth.uid() = student_id);

-- Quiz Attempts: Strict student isolation
CREATE POLICY "Users can manage own attempts" ON public.quiz_attempts FOR ALL USING (auth.uid() = student_id);

-- Student Answers: Strict student isolation
CREATE POLICY "Users can manage own answers" ON public.student_answers FOR ALL USING (auth.uid() = student_id);

-- Mistake Notebook: Strict student isolation
CREATE POLICY "Users can manage own mistake notebook" ON public.mistake_notebook FOR ALL USING (auth.uid() = student_id);

-- Student Mistakes (Revision Queue): Strict student isolation & Admin monitoring
CREATE POLICY "Users can manage own student mistakes" ON public.student_mistakes FOR ALL USING (auth.uid() = student_id);
CREATE POLICY "Admins can view all student mistakes" ON public.student_mistakes FOR SELECT USING (public.is_admin());

-- Spaced Repetition: Strict student isolation
CREATE POLICY "Users can manage own spaced repetition" ON public.spaced_repetition FOR ALL USING (auth.uid() = student_id);

-- Bookmarks: Strict student isolation
CREATE POLICY "Users can manage own bookmarks" ON public.bookmarks FOR ALL USING (auth.uid() = student_id);

-- Study Goals: Strict student isolation
CREATE POLICY "Users can manage own study goals" ON public.study_goals FOR ALL USING (auth.uid() = student_id);

-- Aviation Documents: Publicly viewable, manageable by admins
CREATE POLICY "Documents viewable by authenticated users" ON public.aviation_documents FOR SELECT USING (auth.role() = 'authenticated' AND (is_public = TRUE OR public.is_admin()));
CREATE POLICY "Documents manageable by admins" ON public.aviation_documents FOR ALL USING (public.is_admin());

-- Audit Logs: Viewable and insertable only by admins or system triggers
CREATE POLICY "Audit logs manageable by admins" ON public.audit_logs FOR ALL USING (public.is_admin());
-- ====================================================================
-- CPL PRACTICE — PHASE 1.5 DATABASE MIGRATION
-- Smart Question Revision Queue & Multi-Topic Practice Support
-- ====================================================================

-- 1. Extend student_mistakes with revision tracking columns
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'student_mistakes' AND column_name = 'incorrect_count'
    ) THEN
        ALTER TABLE public.student_mistakes ADD COLUMN incorrect_count INTEGER NOT NULL DEFAULT 1;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'student_mistakes' AND column_name = 'recovered_at'
    ) THEN
        ALTER TABLE public.student_mistakes ADD COLUMN recovered_at TIMESTAMPTZ;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'student_mistakes' AND column_name = 'authoritative_answer'
    ) THEN
        ALTER TABLE public.student_mistakes ADD COLUMN authoritative_answer INTEGER;
    END IF;
END $$;

-- 2. Extend profiles with recovered_questions metric
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'profiles' AND column_name = 'recovered_questions'
    ) THEN
        ALTER TABLE public.profiles ADD COLUMN recovered_questions INTEGER NOT NULL DEFAULT 0;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'profiles' AND column_name = 'revision_limit'
    ) THEN
        ALTER TABLE public.profiles ADD COLUMN revision_limit INTEGER NOT NULL DEFAULT 20;
    END IF;
END $$;

-- 3. Create index for fast revision queue queries
CREATE INDEX IF NOT EXISTS idx_student_mistakes_revision 
ON public.student_mistakes (student_id, status, subject_id, topic_id);

-- 4. Function to atomically mark mistake resolved and increment recovered_questions
CREATE OR REPLACE FUNCTION public.resolve_student_mistake(
    p_student_id UUID,
    p_question_id TEXT
) RETURNS VOID AS $$
BEGIN
    UPDATE public.student_mistakes
    SET 
        status = 'resolved',
        recovered_at = NOW()
    WHERE student_id = p_student_id 
      AND question_id = p_question_id 
      AND status != 'resolved';

    IF FOUND THEN
        UPDATE public.profiles
        SET recovered_questions = recovered_questions + 1
        WHERE id = p_student_id;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ====================================================================
-- CPL PRACTICE — PHASE 3: STUDENT ACCOUNTS & SYLLABUS PROGRESS TRACKER
-- ====================================================================

CREATE TABLE IF NOT EXISTS public.student_syllabus_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    subject_name TEXT NOT NULL,
    topic_name TEXT NOT NULL,
    theory_completed BOOLEAN NOT NULL DEFAULT FALSE,
    practice_completed BOOLEAN NOT NULL DEFAULT FALSE,
    mock_completed BOOLEAN NOT NULL DEFAULT FALSE,
    theory_completed_at TIMESTAMPTZ,
    practice_completed_at TIMESTAMPTZ,
    mock_completed_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (student_id, subject_name, topic_name)
);

CREATE INDEX IF NOT EXISTS idx_syllabus_student_subj 
ON public.student_syllabus_progress (student_id, subject_name);

CREATE INDEX IF NOT EXISTS idx_syllabus_student_topic 
ON public.student_syllabus_progress (student_id, topic_name);

ALTER TABLE public.student_syllabus_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own syllabus progress" 
ON public.student_syllabus_progress 
FOR ALL 
USING (auth.uid() = student_id);

CREATE POLICY "Admins can view all syllabus progress" 
ON public.student_syllabus_progress 
FOR SELECT 
USING (public.is_admin());

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, role)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
        COALESCE(NEW.raw_user_meta_data->>'role', 'student')
    )
    ON CONFLICT (id) DO UPDATE SET
        email = EXCLUDED.email,
        full_name = COALESCE(EXCLUDED.full_name, public.profiles.full_name),
        updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

