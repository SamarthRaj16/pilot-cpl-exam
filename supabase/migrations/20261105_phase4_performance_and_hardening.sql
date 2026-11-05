-- ====================================================================
-- CPL PRACTICE 2.0 — PHASE 4: PERFORMANCE OPTIMISATION, 
-- EXAMINATION RELIABILITY, BACKEND HARDENING & STUDENT MANAGEMENT
-- Migration: 20261105_phase4_performance_and_hardening.sql
-- ====================================================================

-- 1. ADDITIVE COLUMNS ON quiz_attempts FOR RELIABLE TRANSACTIONS & RECOVERY
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'quiz_attempts' AND column_name = 'status'
    ) THEN
        ALTER TABLE public.quiz_attempts ADD COLUMN status VARCHAR(30) NOT NULL DEFAULT 'in_progress';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'quiz_attempts' AND column_name = 'answers_snapshot'
    ) THEN
        ALTER TABLE public.quiz_attempts ADD COLUMN answers_snapshot JSONB DEFAULT '{}'::jsonb;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'quiz_attempts' AND column_name = 'last_saved_at'
    ) THEN
        ALTER TABLE public.quiz_attempts ADD COLUMN last_saved_at TIMESTAMPTZ DEFAULT NOW();
    END IF;
END $$;

-- 2. ADDITIVE COLUMNS ON profiles FOR ADMIN STUDENT MANAGEMENT
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'account_status'
    ) THEN
        ALTER TABLE public.profiles ADD COLUMN account_status VARCHAR(30) NOT NULL DEFAULT 'active';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'suspended_at'
    ) THEN
        ALTER TABLE public.profiles ADD COLUMN suspended_at TIMESTAMPTZ;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'profiles' AND column_name = 'suspended_reason'
    ) THEN
        ALTER TABLE public.profiles ADD COLUMN suspended_reason TEXT;
    END IF;
END $$;

-- 3. HIGH-PERFORMANCE COMPOSITE INDEXES
-- Index for rapid answer retrieval & auto-save deduplication
CREATE INDEX IF NOT EXISTS idx_student_answers_attempt_q 
ON public.student_answers (attempt_id, question_id);

CREATE INDEX IF NOT EXISTS idx_student_answers_attempt_student 
ON public.student_answers (attempt_id, student_id);

-- Index for instant student attempts retrieval and status-filtering
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_student_status 
ON public.quiz_attempts (student_id, status, started_at DESC);

-- Index for smart revision & mistake notebook retrieval
CREATE INDEX IF NOT EXISTS idx_student_mistakes_student_status 
ON public.student_mistakes (student_id, status);

-- Index for Zero-Repeat question exposure lookup
CREATE INDEX IF NOT EXISTS idx_question_exposure_student_subject 
ON public.question_exposure_history (student_id, subject_id);

-- Index for admin student roster searching & filtering
CREATE INDEX IF NOT EXISTS idx_profiles_role_status 
ON public.profiles (role, account_status);

CREATE INDEX IF NOT EXISTS idx_profiles_email_trgm 
ON public.profiles (email);

-- 4. GRANT TABLE PERMISSIONS FOR CLIENT & SERVICE ACCESS
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON ALL ROUTINES IN SCHEMA public TO anon, authenticated, service_role;
