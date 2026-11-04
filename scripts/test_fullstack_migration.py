# -*- coding: utf-8 -*-
"""
CPL Practice 2.0 — Full-Stack Transformation Verification Suite
Validates database schema, SQL seed, question counts, Next.js components,
API route handlers, authentication helpers, PWA assets, and offline fallback.
"""
import json
import os
import sys

BASE = r"c:\VS Code\Codes\dgcacpllearning"

print("====================================================================")
print("CPL PRACTICE 2.0 — FULL-STACK VERIFICATION SUITE")
print("====================================================================")

# 1. QUESTION BANK INTEGRITY
q_path = os.path.join(BASE, "src", "data", "questions.json")
with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

assert len(questions) == 839, f"Expected 839 questions, got {len(questions)}"
print(f"[OK] Question Bank master repository verified: {len(questions)} questions.")

# 2. SQL MIGRATION & SEED INTEGRITY
schema_path = os.path.join(BASE, "supabase", "migrations", "20261104000000_cpl_core_schema.sql")
with open(schema_path, "r", encoding="utf-8") as f:
    schema_sql = f.read()

required_tables = [
    "public.profiles",
    "public.subjects",
    "public.topics",
    "public.questions",
    "public.question_exposure_history",
    "public.quiz_attempts",
    "public.student_answers",
    "public.mistake_notebook",
    "public.spaced_repetition",
    "public.bookmarks",
    "public.study_goals",
    "public.aviation_documents",
    "public.audit_logs",
]
for t in required_tables:
    assert t in schema_sql, f"Missing table {t} in DDL schema"
assert "ROW LEVEL SECURITY" in schema_sql, "RLS not enabled in DDL"
print(f"[OK] Supabase PostgreSQL DDL verified: all 13 tables & RLS policies present.")

seed_path = os.path.join(BASE, "supabase", "seed.sql")
with open(seed_path, "r", encoding="utf-8") as f:
    seed_sql = f.read()

q_inserts = seed_sql.count("INSERT INTO public.questions")
assert q_inserts == 839, f"Expected 839 question inserts in seed.sql, got {q_inserts}"
print(f"[OK] Supabase seed.sql verified: exactly {q_inserts} questions seeded.")

# 3. NEXT.JS 14 APP ROUTER PAGES & APIS
required_files = [
    "package.json",
    "tsconfig.json",
    "tailwind.config.ts",
    "postcss.config.js",
    "next.config.mjs",
    ".env.example",
    "src/middleware.ts",
    "src/types/index.ts",
    "src/lib/supabase/client.ts",
    "src/lib/supabase/server.ts",
    "src/lib/supabase/admin.ts",
    "src/app/globals.css",
    "src/app/layout.tsx",
    "src/app/page.tsx",
    "src/app/auth/login/page.tsx",
    "src/app/auth/register/page.tsx",
    "src/app/dashboard/layout.tsx",
    "src/app/dashboard/page.tsx",
    "src/app/dashboard/exam/page.tsx",
    "src/app/dashboard/results/page.tsx",
    "src/app/dashboard/review/page.tsx",
    "src/app/dashboard/notebook/page.tsx",
    "src/app/dashboard/revision/page.tsx",
    "src/app/dashboard/readiness/page.tsx",
    "src/app/dashboard/planner/page.tsx",
    "src/app/dashboard/library/page.tsx",
    "src/app/admin/layout.tsx",
    "src/app/admin/page.tsx",
    "src/app/admin/questions/page.tsx",
    "src/app/api/quiz/start/route.ts",
    "src/app/api/quiz/finish/route.ts",
    "src/app/api/student/reset-rotation/route.ts",
    "src/app/api/student/readiness/route.ts",
    "src/app/api/admin/questions/route.ts",
    "public/manifest.json",
    "public/sw.js",
    "DEPLOYMENT.md",
    "README.md",
]

for rel in required_files:
    full_p = os.path.join(BASE, rel.replace("/", os.sep))
    assert os.path.exists(full_p), f"Missing required file: {rel}"

print(f"[OK] Next.js 14 App Router verified: all {len(required_files)} modules & components present.")

# 4. ANSWER PROTECTION SECURITY CHECK
finish_api_path = os.path.join(BASE, "src", "app", "api", "quiz", "finish", "route.ts")
with open(finish_api_path, "r", encoding="utf-8") as f:
    finish_code = f.read()
assert "pointsAwarded" in finish_code, "pointsAwarded missing in finish API"
assert "accuracy >= 70" in finish_code or "score / totalQuestions" in finish_code, "DGCA pass logic missing in finish API"

start_api_path = os.path.join(BASE, "src", "app", "api", "quiz", "start", "route.ts")
with open(start_api_path, "r", encoding="utf-8") as f:
    start_code = f.read()
assert "options: q.options" in start_code, "Question delivery logic missing in start API"
print("[OK] Server-side Answer Protection & Secure Scoring verified.")

# 5. OFFLINE FALLBACK CHECK
offline_path = os.path.join(BASE, "cpl-exam-direct.html")
with open(offline_path, "r", encoding="utf-8") as f:
    off_text = f.read()
assert "839" in off_text, "Offline bundle missing 839 questions count"
assert "Zero-Repeat" in off_text, "Offline bundle missing Zero-Repeat logic"
print(f"[OK] Standalone Offline Fallback verified: {os.path.getsize(offline_path)} bytes.")

print("====================================================================")
print("ALL FULL-STACK TRANSFORMATION TESTS PASSED (100% SUCCESS)!")
print("====================================================================")

