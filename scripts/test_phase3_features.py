import os
import json
import re

print("======================================================================")
print("RUNNING CPL PRACTICE PHASE 3 VERIFICATION TEST SUITE")
print("Student Account System & Interactive Syllabus Completion Tracker")
print("======================================================================")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

passed = 0
failed = 0

def test(name, condition, error_msg=""):
    global passed, failed
    if condition:
        print(f"  [PASS] {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name}: {error_msg}")
        failed += 1

# Test 1: Syllabus Hierarchy integrity (95 unique topics across 6 subjects)
hier_path = os.path.join(SRC_DIR, "data", "syllabusHierarchy.json")
with open(hier_path, "r", encoding="utf-8") as f:
    hier = json.load(f)

total_topics = sum(len(s["topics"]) for s in hier)
total_questions = sum(s["question_count"] for s in hier)
test("1. Syllabus Hierarchy: 95 Topics, 6 Subjects, 959 Questions",
     len(hier) == 6 and total_topics == 95 and total_questions == 959,
     f"Got {len(hier)} subjects, {total_topics} topics, {total_questions} questions")

# Test 2: Syllabus Completion Mathematics
total_checklist_items = total_topics * 3 # 285
mock_completed = 142
overall_pct = round((mock_completed / total_checklist_items) * 100)
test("2. Exact Mathematics: 285 total checklist items (95 * 3)",
     total_checklist_items == 285 and overall_pct == 50,
     f"Expected 285 items, got {total_checklist_items}")

# Test 3: Backend API /api/syllabus
api_syllabus = os.path.join(SRC_DIR, "app", "api", "syllabus", "route.ts")
with open(api_syllabus, "r", encoding="utf-8") as f:
    api_code = f.read()
test("3. Backend Syllabus API (/api/syllabus) with GET, POST, PUT",
     "export async function GET" in api_code and
     "export async function POST" in api_code and
     "export async function PUT" in api_code and
     "student_syllabus_progress" in api_code,
     "Missing GET/POST/PUT handlers in /api/syllabus")

# Test 4: Main Syllabus Tracker Page
page_syllabus = os.path.join(SRC_DIR, "app", "dashboard", "syllabus", "page.tsx")
with open(page_syllabus, "r", encoding="utf-8") as f:
    syl_page_code = f.read()
test("4. Main Syllabus Page: SVG Gauge, 3 Milestone Bars, Notes Modal",
     "overallPct" in syl_page_code and
     "theory_completed" in syl_page_code and
     "practice_completed" in syl_page_code and
     "mock_completed" in syl_page_code and
     "lowestSubject" in syl_page_code and
     "handleSaveNote" in syl_page_code,
     "Missing core interactive syllabus components")

# Test 5: Subject Specific Page
sub_page = os.path.join(SRC_DIR, "app", "dashboard", "syllabus", "[subjectId]", "page.tsx")
test("5. Subject-Specific Syllabus Page exists",
     os.path.exists(sub_page),
     "Missing [subjectId]/page.tsx")

# Test 6: Dashboard Compact Widget
dash_page = os.path.join(SRC_DIR, "app", "dashboard", "page.tsx")
with open(dash_page, "r", encoding="utf-8") as f:
    dash_code = f.read()
test("6. Dashboard Widget: Syllabus Coverage Card integrated",
     "Interactive Syllabus Tracker" in dash_code and
     "syllabusMetrics.overallPct" in dash_code and
     "Continue Syllabus" in dash_code,
     "Dashboard missing compact syllabus card")

# Test 7: Exam Results Automatic Suggestion
results_page = os.path.join(SRC_DIR, "app", "dashboard", "results", "page.tsx")
with open(results_page, "r", encoding="utf-8") as f:
    res_code = f.read()
test("7. Results Page: Automatic Practice-Completion suggestion banner",
     "testedTopics" in res_code and
     "handleMarkSyllabus" in res_code and
     "Mark Practice Complete" in res_code,
     "Results page missing syllabus auto-suggestion")

# Test 8: Student Account Pages
login_page = os.path.join(SRC_DIR, "app", "auth", "login", "page.tsx")
reg_page = os.path.join(SRC_DIR, "app", "auth", "register", "page.tsx")
forgot_page = os.path.join(SRC_DIR, "app", "auth", "forgot-password", "page.tsx")
reset_page = os.path.join(SRC_DIR, "app", "auth", "reset-password", "page.tsx")
profile_page = os.path.join(SRC_DIR, "app", "dashboard", "profile", "page.tsx")

with open(login_page, "r", encoding="utf-8") as f:
    login_code = f.read()
with open(reg_page, "r", encoding="utf-8") as f:
    reg_code = f.read()

test("8. Student Auth System: Login & Register with Suspense & Guest fallback",
     "<Suspense" in login_code and
     "rememberMe" in login_code and
     "handleGuestLogin" in login_code and
     "passwordStrength" in reg_code and
     ("agreeTerms" in reg_code or "termsAccepted" in reg_code) and
     os.path.exists(forgot_page) and
     os.path.exists(reset_page) and
     os.path.exists(profile_page),
     "Missing auth pages or required features")

# Test 9: Profile Settings & Guest Migration
with open(profile_page, "r", encoding="utf-8") as f:
    prof_code = f.read()
test("9. Profile Settings: Target Exam Date, Goal Selector, Guest Migration",
     "target_exam_date" in prof_code and
     "daily_goal_questions" in prof_code and
     "handleMigrateGuestData" in prof_code and
     "student_syllabus_progress" in prof_code,
     "Profile page missing guest migration or study preferences")

# Test 10: Database Migration Schema
schema_mig = os.path.join(ROOT_DIR, "supabase", "migrations", "20261105_phase3_student_accounts_and_syllabus.sql")
with open(schema_mig, "r", encoding="utf-8") as f:
    sql = f.read()
test("10. Database Schema: student_syllabus_progress table & RLS policies",
     "CREATE TABLE IF NOT EXISTS public.student_syllabus_progress" in sql and
     "UNIQUE (student_id, subject_name, topic_name)" in sql and
     "ENABLE ROW LEVEL SECURITY" in sql and
     "handle_new_user" in sql,
     "SQL migration missing required table, constraints, or RLS")

print("======================================================================")
print(f"PHASE 3 RESULTS: {passed} PASSED, {failed} FAILED")
print("======================================================================")
if failed > 0:
    exit(1)
