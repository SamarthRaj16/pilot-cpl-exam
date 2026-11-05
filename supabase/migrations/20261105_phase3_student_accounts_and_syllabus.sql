-- ====================================================================
-- CPL PRACTICE — PHASE 3 DATABASE MIGRATION
-- Student Account System & Interactive Syllabus Completion Tracker
-- ====================================================================

-- 1. Create student_syllabus_progress table
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

-- 2. Indexes for fast syllabus queries
CREATE INDEX IF NOT EXISTS idx_syllabus_student_subj 
ON public.student_syllabus_progress (student_id, subject_name);

CREATE INDEX IF NOT EXISTS idx_syllabus_student_topic 
ON public.student_syllabus_progress (student_id, topic_name);

-- 3. Extend profiles table with study preferences if not already present
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'profiles' AND column_name = 'study_preferences'
    ) THEN
        ALTER TABLE public.profiles ADD COLUMN study_preferences JSONB DEFAULT '{"target_exam_date": null, "daily_goal_questions": 30, "preferred_mode": "practice"}'::jsonb;
    END IF;
END $$;

-- 4. Enable Row Level Security (RLS) on student_syllabus_progress
ALTER TABLE public.student_syllabus_progress ENABLE ROW LEVEL SECURITY;

-- 5. Strict RLS Policies for Syllabus Progress
DROP POLICY IF EXISTS "Users can manage own syllabus progress" ON public.student_syllabus_progress;
CREATE POLICY "Users can manage own syllabus progress" 
ON public.student_syllabus_progress 
FOR ALL 
USING (auth.uid() = student_id);

DROP POLICY IF EXISTS "Admins can view all syllabus progress" ON public.student_syllabus_progress;
CREATE POLICY "Admins can view all syllabus progress" 
ON public.student_syllabus_progress 
FOR SELECT 
USING (public.is_admin());

-- 6. Trigger to automatically create profile on Supabase auth.users creation
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

-- 7. Trigger to automatically update updated_at on student_syllabus_progress
CREATE OR REPLACE FUNCTION public.handle_syllabus_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_syllabus_updated_at ON public.student_syllabus_progress;
CREATE TRIGGER trg_syllabus_updated_at
    BEFORE UPDATE ON public.student_syllabus_progress
    FOR EACH ROW EXECUTE FUNCTION public.handle_syllabus_updated_at();

