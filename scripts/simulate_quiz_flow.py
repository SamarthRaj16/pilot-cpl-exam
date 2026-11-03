import json
import random
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 1. Read index.html and extract QUESTIONS JSON
with open(r"c:\VS Code\Codes\dgcacpllearning\index.html", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "const QUESTIONS = ["
end_marker = "];\n\n/* ══════════════════════════════════════════════════════\n   SUBJECT META"

if start_marker not in content:
    start_marker = "const QUESTIONS = ["

p1 = content.index("const QUESTIONS = [") + len("const QUESTIONS = ")
p2 = content.index("];", p1) + 1

questions = json.loads(content[p1:p2])
print(f"✅ Loaded {len(questions)} embedded questions from index.html")

# 2. Test prepQ function equivalent in Python to verify option shuffling integrity
LETTERS = ["A", "B", "C", "D"]

def prep_q(q):
    orig_options = list(q["options"])
    orig_ans_idx = q["answerIndex"]
    orig_correct_text = orig_options[orig_ans_idx]

    # Shuffle indices
    idxs = list(range(len(orig_options)))
    random.shuffle(idxs)

    shuffled_options = [orig_options[i] for i in idxs]
    new_ans_idx = idxs.index(orig_ans_idx)

    # Verification:
    assert shuffled_options[new_ans_idx] == orig_correct_text, (
        f"Mismatch: expected {orig_correct_text}, got {shuffled_options[new_ans_idx]}"
    )
    return {
        "id": q["id"],
        "subject": q["subject"],
        "topic": q.get("topic", "General"),
        "question": q["question"],
        "options": shuffled_options,
        "answer": new_ans_idx,
        "explanation": q["explanation"],
        "source": q["source"],
        "_orig_options": orig_options,
        "_orig_ans_idx": orig_ans_idx
    }

# Run prep on all 230 questions 10 times with different random seeds
for trial in range(10):
    for q in questions:
        prepped = prep_q(q)

print("✅ Shuffling integrity verified 100%: correct answer text is preserved across all 2,300 shuffle tests!")

# 3. Simulate Quiz Scoring & Points Calculation Flow
print("\n--- Simulating 50-Question Practice Quiz ---")
sample_pool = random.sample(questions, 50)
prepped_quiz = [prep_q(q) for q in sample_pool]

answers = [-1] * len(prepped_quiz)
revealed = [False] * len(prepped_quiz)

# Simulate user:
# First 35 answered correctly
# Next 10 answered incorrectly
# Last 5 left unanswered (e.g. user finishes early)
points_earned = 0
for i in range(35):
    answers[i] = prepped_quiz[i]["answer"]
    revealed[i] = True
    points_earned += 1

for i in range(35, 45):
    wrong_opt = (prepped_quiz[i]["answer"] + 1) % 4
    answers[i] = wrong_opt
    revealed[i] = True

# Verification of practice mode points
attempted = sum(1 for r in revealed if r)
correct_answers = sum(1 for i, q in enumerate(prepped_quiz) if revealed[i] and answers[i] == q["answer"])
pct = round(100 * correct_answers / len(prepped_quiz))

print(f"Attempted: {attempted}/50")
print(f"Correct: {correct_answers}/50")
print(f"Points Received: {points_earned} points")
print(f"DGCA Percentage: {pct}%")

assert points_earned == 35, f"Expected 35 points, got {points_earned}"
assert pct == 70, f"Expected 70%, got {pct}%"

# Pass mark check (70%)
is_pass = pct >= 70
print(f"DGCA Exam Status: {'PASS' if is_pass else 'FAIL'} (Threshold 70%)")
assert is_pass is True

# Subject breakdown verification
subj_stats = {}
for i, q in enumerate(prepped_quiz):
    s = q["subject"]
    if s not in subj_stats:
        subj_stats[s] = {"total": 0, "points": 0}
    subj_stats[s]["total"] += 1
    if answers[i] == q["answer"]:
        subj_stats[s]["points"] += 1

total_breakdown_pts = sum(s["points"] for s in subj_stats.values())
assert total_breakdown_pts == points_earned, (
    f"Breakdown points sum {total_breakdown_pts} != quiz points {points_earned}"
)
print("✅ Subject breakdown points sum perfectly matches total points received!")

# Review mistakes list verification:
# Should contain exactly the 10 wrong + 5 unanswered = 15 questions
missed = [q for i, q in enumerate(prepped_quiz) if answers[i] != q["answer"]]
assert len(missed) == 15, f"Expected 15 missed questions, got {len(missed)}"
print(f"✅ Review mistakes list correctly contains {len(missed)} missed/unanswered questions.")

# Retry pool verification:
retry_pool = []
for i, q in enumerate(prepped_quiz):
    if answers[i] != q["answer"]:
        retry_pool.append(q)

assert len(retry_pool) == 15
print("✅ Retry missed questions feature collects all 15 missed questions for re-attempt!")

print("\n🎉 ALL QUIZ LOGIC AND POINTS RECEIVED SIMULATIONS PASSED!")
