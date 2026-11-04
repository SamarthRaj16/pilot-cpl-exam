# -*- coding: utf-8 -*-
"""
PostgreSQL / Supabase Schema & Seed Generator
Generates:
1. supabase/migrations/20261104000000_cpl_core_schema.sql (DDL + RLS Policies)
2. supabase/seed.sql (Full relational seed for 6 subjects, 94 topics, 839 questions)
"""
import json
import os
import re

BASE = r"c:\VS Code\Codes\dgcacpllearning"
q_path = os.path.join(BASE, "src", "data", "questions.json")
cfg_path = os.path.join(BASE, "src", "data", "examConfig.json")

with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

with open(cfg_path, "r", encoding="utf-8") as f:
    exam_config = json.load(f)

print(f"Loaded {len(questions)} validated questions.")

# Helper to slugify
def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# Helper to escape SQL single quotes
def sql_str(s):
    if s is None:
        return "NULL"
    s = str(s).replace("'", "''")
    return f"'{s}'"

SUBJECT_CONFIG = {
    "Air Navigation": {
        "id": "air-navigation",
        "code": "CAR SEC 7",
        "icon": "🧭",
        "color": "#719CFF",
        "desc": "General Navigation, Chart Projections, Instrumentation, Dead Reckoning and Point of No Return / Critical Point calculations.",
        "order": 1,
        "questions": 100,
        "duration": 180
    },
    "Air Regulations": {
        "id": "air-regulations",
        "code": "ICAO / CAR",
        "icon": "📜",
        "color": "#9484F5",
        "desc": "Aircraft Rules 1937, Bharatiya Vayuyan Adhiniyam 2024, Airspace Classification, Rules of the Air, and Aerodrome Standards.",
        "order": 2,
        "questions": 50,
        "duration": 90
    },
    "Aviation Meteorology": {
        "id": "aviation-meteorology",
        "code": "I.C. JOSHI",
        "icon": "⛅",
        "color": "#51C6C1",
        "desc": "The Atmosphere, Atmospheric Pressure, Wind Systems, Climatology of India, Monsoon Dynamics, Icing, and METAR/TAF Decoding.",
        "order": 3,
        "questions": 50,
        "duration": 120
    },
    "Technical General": {
        "id": "technical-general",
        "code": "AGK / ENGINES",
        "icon": "⚙️",
        "color": "#69CF9B",
        "desc": "Principles of Flight, Piston Engines, Aircraft Systems, Electrical, Hydraulics, Propellers, and Gyroscopic Flight Instruments.",
        "order": 4,
        "questions": 100,
        "duration": 150
    },
    "Technical Specific": {
        "id": "technical-specific",
        "code": "POH / PERF",
        "icon": "🛩️",
        "color": "#ECA85B",
        "desc": "Light Aircraft Pilot Operating Handbooks (POH), V-speeds, Limitations, Fuel Systems, Weight & Balance, and Performance Charts.",
        "order": 5,
        "questions": 50,
        "duration": 90
    },
    "RTR": {
        "id": "rtr",
        "code": "ICAO DOC 9432",
        "icon": "🎙️",
        "color": "#51C6C1",
        "desc": "Radio Telephony Restricted (Aeronautical), Standard ICAO Phraseology, Readability Scale, Distress/Urgency, and VHF Propagation.",
        "order": 6,
        "questions": 50,
        "duration": 60
    }
}

# 1. DDL SCHEMA
ddl_sql = """-- ====================================================================
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
"""

# Write DDL migration file
migration_path = os.path.join(BASE, "supabase", "migrations", "20261104000000_cpl_core_schema.sql")
with open(migration_path, "w", encoding="utf-8") as f:
    f.write(ddl_sql)

print(f"Generated DDL Schema migration: {migration_path}")

# 2. GENERATE SEED DATA (Subjects, Topics, Questions)
seed_lines = [
    "-- ====================================================================",
    "-- CPL PRACTICE 2.0 — COMPLETE DATABASE SEED",
    "-- Contains all 6 Subjects, 94 Topics, and 839 Verified Questions",
    "-- ====================================================================",
    "",
    "-- 1. INSERT SUBJECTS",
]

for s_name, s_cfg in SUBJECT_CONFIG.items():
    seed_lines.append(
        f"INSERT INTO public.subjects (id, name, code, icon, color, description, default_question_count, default_duration_minutes, display_order) "
        f"VALUES ({sql_str(s_cfg['id'])}, {sql_str(s_name)}, {sql_str(s_cfg['code'])}, {sql_str(s_cfg['icon'])}, {sql_str(s_cfg['color'])}, {sql_str(s_cfg['desc'])}, {s_cfg['questions']}, {s_cfg['duration']}, {s_cfg['order']}) "
        f"ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, code = EXCLUDED.code, icon = EXCLUDED.icon, color = EXCLUDED.color, description = EXCLUDED.description;"
    )

seed_lines.append("\n-- 2. INSERT TOPICS")

# Gather topics
topics_map = {}
for q in questions:
    subj_name = q["subject"]
    s_cfg = SUBJECT_CONFIG[subj_name]
    subj_id = s_cfg["id"]
    t_name = q.get("topic", "General")
    t_id = f"{subj_id}-{slugify(t_name)}"
    if t_id not in topics_map:
        topics_map[t_id] = {
            "id": t_id,
            "subject_id": subj_id,
            "name": t_name,
            "order": len(topics_map) + 1
        }

for t_id, t_data in sorted(topics_map.items()):
    seed_lines.append(
        f"INSERT INTO public.topics (id, subject_id, name, display_order) "
        f"VALUES ({sql_str(t_data['id'])}, {sql_str(t_data['subject_id'])}, {sql_str(t_data['name'])}, {t_data['order']}) "
        f"ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, subject_id = EXCLUDED.subject_id;"
    )

seed_lines.append("\n-- 3. INSERT QUESTIONS (839 VALIDATED QUESTIONS)")

for q in questions:
    subj_name = q["subject"]
    s_cfg = SUBJECT_CONFIG[subj_name]
    subj_id = s_cfg["id"]
    t_name = q.get("topic", "General")
    t_id = f"{subj_id}-{slugify(t_name)}"
    
    q_id = q["id"]
    diff = q.get("difficulty", "medium")
    q_text = q["question"]
    opts_json = json.dumps(q["options"], ensure_ascii=False)
    ans_idx = q.get("answerIndex", 0)
    expl = q["explanation"]
    source = q["source"]

    seed_lines.append(
        f"INSERT INTO public.questions (id, subject_id, topic_id, topic_name, difficulty, question, options, answer_index, explanation, source, validation_status) "
        f"VALUES ({sql_str(q_id)}, {sql_str(subj_id)}, {sql_str(t_id)}, {sql_str(t_name)}, {sql_str(diff)}, {sql_str(q_text)}, {sql_str(opts_json)}::jsonb, {ans_idx}, {sql_str(expl)}, {sql_str(source)}, 'approved') "
        f"ON CONFLICT (id) DO UPDATE SET question = EXCLUDED.question, options = EXCLUDED.options, answer_index = EXCLUDED.answer_index, explanation = EXCLUDED.explanation, source = EXCLUDED.source, validation_status = EXCLUDED.validation_status;"
    )

seed_path = os.path.join(BASE, "supabase", "seed.sql")
with open(seed_path, "w", encoding="utf-8") as f:
    f.write("\n".join(seed_lines))

print(f"Generated complete Seed SQL: {seed_path} ({len(seed_lines)} SQL statements)")
print("MIGRATION SCRIPTS COMPLETE!")
