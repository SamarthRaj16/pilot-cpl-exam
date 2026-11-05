-- ====================================================================
-- CPL PRACTICE — PHASE 1.5 DATABASE MIGRATION
-- Smart Question Revision Queue & Multi-Topic Practice Support
-- ====================================================================

-- 0. Ensure student_mistakes table exists
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

ALTER TABLE public.student_mistakes ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE tablename = 'student_mistakes' AND policyname = 'Users can manage own student mistakes'
    ) THEN
        CREATE POLICY "Users can manage own student mistakes" ON public.student_mistakes FOR ALL USING (auth.uid() = student_id);
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies WHERE tablename = 'student_mistakes' AND policyname = 'Admins can view all student mistakes'
    ) THEN
        CREATE POLICY "Admins can view all student mistakes" ON public.student_mistakes FOR SELECT USING (public.is_admin());
    END IF;
END $$;

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

