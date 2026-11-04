# -*- coding: utf-8 -*-
"""
Verification Test Suite for CPL Practice Phase 1.5
Validates all features and requirements requested.
"""
import json
import os
import re
import sys

BASE_DIR = r"c:\VS Code\Codes\dgcacpllearning"
passed_tests = 0
failed_tests = 0

def test(description):
    def decorator(fn):
        global passed_tests, failed_tests
        try:
            fn()
            print(f"  [PASS] {description}")
            passed_tests += 1
        except AssertionError as e:
            print(f"  [FAIL] {description}: {e}")
            failed_tests += 1
        except Exception as e:
            print(f"  [ERROR] {description}: {type(e).__name__}: {e}")
            failed_tests += 1
        return fn
    return decorator

print("=" * 70)
print("RUNNING CPL PRACTICE PHASE 1.5 VERIFICATION TEST SUITE")
print("=" * 70)

# Test 1: Question Bank Audit & Meteorology Expansion
@test("1. Question Bank Totals & Aviation Meteorology Expansion (>= 200 Qs)")
def test_met_expansion():
    q_path = os.path.join(BASE_DIR, "src", "data", "questions.json")
    with open(q_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    
    assert len(questions) >= 950, f"Expected >= 950 questions, found {len(questions)}"
    
    met_qs = [q for q in questions if q["subject"] == "Aviation Meteorology"]
    assert len(met_qs) >= 200, f"Expected >= 200 Aviation Meteorology questions, found {len(met_qs)}"
    
    # Check topic count for Met
    met_topics = set(q["topic"] for q in met_qs)
    assert len(met_topics) >= 18, f"Expected >= 18 Meteorology topics, found {len(met_topics)}"

# Test 2: Schema Integrity & Uniqueness
@test("2. Question Schema Integrity & Unique ID Enforcement")
def test_schema_integrity():
    q_path = os.path.join(BASE_DIR, "src", "data", "questions.json")
    with open(q_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    seen_ids = set()
    seen_texts = set()
    
    for i, q in enumerate(questions):
        assert "id" in q and q["id"], f"Missing id at index {i}"
        assert q["id"] not in seen_ids, f"Duplicate ID: {q['id']}"
        seen_ids.add(q["id"])
        
        assert q["subject"] in [
            "Air Navigation", "Air Regulations", "Aviation Meteorology",
            "Technical General", "Technical Specific", "RTR"
        ], f"Invalid subject: {q['subject']}"
        
        assert "topic" in q and len(q["topic"]) > 0, f"Empty topic at {q['id']}"
        assert "question" in q and len(q["question"]) > 5, f"Short question at {q['id']}"
        assert "options" in q and len(q["options"]) == 4, f"Options must be 4 items at {q['id']}"
        assert ("answerIndex" in q and q["answerIndex"] in [0, 1, 2, 3]) or ("answer" in q and q["answer"] in [0, 1, 2, 3]), f"Invalid answer index at {q['id']}"
        assert "explanation" in q and len(q["explanation"]) > 10, f"Short explanation at {q['id']}"
        assert "source" in q and len(q["source"]) > 3, f"Missing source citation at {q['id']}"
        
        # Check text uniqueness
        norm_text = re.sub(r"\s+", " ", q["question"].strip().lower())
        assert norm_text not in seen_texts, f"Duplicate question text: {q['question'][:50]}"
        seen_texts.add(norm_text)

# Test 3: Backend API Zero-Repeat & Multi-Topic Logic
@test("3. Backend API Route Implementation (/api/quiz/start)")
def test_api_start_logic():
    api_path = os.path.join(BASE_DIR, "src", "app", "api", "quiz", "start", "route.ts")
    assert os.path.exists(api_path), "Missing /api/quiz/start/route.ts"
    with open(api_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Check multi-subject and multi-topic support
    assert "topics" in code, "API start must handle topics array"
    assert "subjects" in code, "API start must handle subjects array"
    # Check max limit 50 enforcement
    assert "Math.min(50" in code, "API start must enforce maximum 50 questions"
    # Check revision queue mixing
    assert "revision_only" in code or "smart" in code, "API start must handle smart revision"
    assert "poolB_revision" in code or "revisionPool" in code, "API start must partition revision pool"

# Test 4: Backend API Finish Route & Recovery Logic
@test("4. Backend API Route Implementation (/api/quiz/finish)")
def test_api_finish_logic():
    api_path = os.path.join(BASE_DIR, "src", "app", "api", "quiz", "finish", "route.ts")
    assert os.path.exists(api_path), "Missing /api/quiz/finish/route.ts"
    with open(api_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Check status updates for student_mistakes
    assert "resolved" in code, "API finish must resolve recovered mistakes"
    assert "recovered_questions" in code or "recovered_at" in code, "API finish must track recovered questions"

# Test 5: Next.js Suspense & Prerendering Safety
@test("5. Next.js Suspense & Dynamic Force Prerendering Guard")
def test_prerender_safety():
    login_path = os.path.join(BASE_DIR, "src", "app", "auth", "login", "page.tsx")
    exam_path = os.path.join(BASE_DIR, "src", "app", "dashboard", "exam", "page.tsx")
    
    with open(login_path, "r", encoding="utf-8") as f:
        login_code = f.read()
    with open(exam_path, "r", encoding="utf-8") as f:
        exam_code = f.read()
        
    assert "<Suspense" in login_code, "Login page must wrap useSearchParams in Suspense"
    assert 'dynamic = "force-dynamic"' in login_code or "force-dynamic" in login_code, "Login page must export force-dynamic"
    
    assert "<Suspense" in exam_code, "Exam page must wrap useSearchParams in Suspense"
    assert 'dynamic = "force-dynamic"' in exam_code or "force-dynamic" in exam_code, "Exam page must export force-dynamic"

# Test 6: Custom Practice Page Implementation
@test("6. Custom Practice Page & Multi-Topic UI")
def test_custom_practice_page():
    cp_path = os.path.join(BASE_DIR, "src", "app", "dashboard", "custom-practice", "page.tsx")
    assert os.path.exists(cp_path), "Custom practice page must exist"
    with open(cp_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    assert "Custom Practice" in code, "Must include Custom Practice title"
    assert "Build your own quiz by selecting multiple subjects and topics" in code, "Must include requested subtitle"
    assert "questionLimit" in code, "Must have question limit selector"
    assert "smart" in code and "fresh_only" in code, "Must support practice modes"

# Test 7: Question Navigator Colour Logic in Exam Engine
@test("7. Question Navigator Colour Logic in Exam Page")
def test_navigator_colour_logic():
    exam_path = os.path.join(BASE_DIR, "src", "app", "dashboard", "exam", "page.tsx")
    with open(exam_path, "r", encoding="utf-8") as f:
        code = f.read()
        
    # Practice mode must color green for correct, red for incorrect
    assert "mode === \"practice\"" in code, "Must check for practice mode"
    assert "bg-brand-green" in code, "Must use brand-green for correct answers"
    assert "bg-brand-red" in code, "Must use brand-red for incorrect answers"
    # Current question purple ring
    assert "ring-brand-purple" in code, "Must have purple ring for current question"
    # Flagged overlay badge
    assert "bg-brand-orange" in code, "Must have orange flag indicator"

# Test 8: Supabase Migration & Seed SQL
@test("8. Supabase Schema Migration & Full Seed Sync")
def test_db_artifacts():
    mig_path = os.path.join(BASE_DIR, "supabase", "migrations", "20261104_phase1_5_smart_revision.sql")
    seed_path = os.path.join(BASE_DIR, "supabase", "seed.sql")
    
    assert os.path.exists(mig_path), "Migration SQL must exist"
    assert os.path.exists(seed_path), "Seed SQL must exist"
    
    with open(seed_path, "r", encoding="utf-8") as f:
        seed_sql = f.read()
        
    assert "INSERT INTO public.questions" in seed_sql, "Seed must populate questions"
    assert "MET-213" in seed_sql, "Seed must include expanded meteorology questions"

# Test 9: Standalone Single-File HTML Bundles Sync
@test("9. Standalone HTML Bundles (cpl-exam-direct.html, cpl-quiz-standalone.html, index.html)")
def test_standalone_bundles():
    direct_path = os.path.join(BASE_DIR, "cpl-exam-direct.html")
    index_path = os.path.join(BASE_DIR, "index.html")
    
    assert os.path.exists(direct_path), "cpl-exam-direct.html must exist"
    assert os.path.exists(index_path), "index.html must exist"
    
    with open(direct_path, "r", encoding="utf-8") as f:
        direct_html = f.read()
        
    assert "answered-correct" in direct_html, "Standalone must implement answered-correct style"
    assert "answered-incorrect" in direct_html, "Standalone must implement answered-incorrect style"
    assert "MET-213" in direct_html, "Standalone must contain expanded meteorology questions"

# Test 10: Graceful Fallback without Supabase Keys
@test("10. Environment Variable Resilience (Guest/Offline fallback)")
def test_env_resilience():
    middleware_path = os.path.join(BASE_DIR, "src", "middleware.ts")
    client_path = os.path.join(BASE_DIR, "src", "lib", "supabase", "client.ts")
    
    with open(middleware_path, "r", encoding="utf-8") as f:
        mid_code = f.read()
    with open(client_path, "r", encoding="utf-8") as f:
        cli_code = f.read()
        
    assert "placeholder-url" in cli_code or "placeholder" in cli_code, "Client must provide placeholder fallback"
    assert "!supabaseUrl || !supabaseAnonKey" in mid_code, "Middleware must allow bypass when env vars not configured"

print("\nExecuting tests...")
test_met_expansion()
test_schema_integrity()
test_api_start_logic()
test_api_finish_logic()
test_prerender_safety()
test_custom_practice_page()
test_navigator_colour_logic()
test_db_artifacts()
test_standalone_bundles()
test_env_resilience()

print("=" * 70)
print(f"TEST RESULTS: {passed_tests} PASSED, {failed_tests} FAILED")
print("=" * 70)

if failed_tests > 0:
    sys.exit(1)
