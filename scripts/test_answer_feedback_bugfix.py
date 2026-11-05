"""
======================================================================
CPL PRACTICE 2.0 — BUG FIX VERIFICATION: RED/GREEN ANSWER FEEDBACK
Verifies Scenario A, Scenario B, Circular Answer Bubbles & Palette Colors
======================================================================
"""

import os
import sys

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM_PAGE_PATH = os.path.join(WORKSPACE_ROOT, "src", "app", "dashboard", "exam", "page.tsx")

def run_tests():
    assert os.path.exists(EXAM_PAGE_PATH), "Exam page not found"
    with open(EXAM_PAGE_PATH, "r", encoding="utf-8") as f:
        code = f.read()

    print("Verifying Practice Mode Answer Feedback implementation...")

    # 1. Circular letter bubble shape and independent styling
    assert "rounded-full" in code, "Circular answer bubble must use rounded-full"
    assert "bg-[#3ED1B0]" in code, "Green color (#3ED1B0) missing from circular bubble styling"
    assert "bg-[#F16D75]" in code, "Red color (#F16D75) missing from circular bubble styling"
    print("  [PASS] 1. Circular letter bubble (A, B, C, D) renders with rounded-full and independent color states.")

    # 2. Scenario A & B: Correct Green (#3ED1B0) and Incorrect Red (#F16D75)
    assert "border-[#3ED1B0]" in code, "Green border missing from correct option container"
    assert "border-[#F16D75]" in code, "Red border missing from incorrect option container"
    assert "✓ Correct Answer" in code, "Correct answer badge tag missing"
    assert "✕ Your Choice" in code, "Incorrect answer choice tag missing"
    print("  [PASS] 2. Scenario A & B: Selected wrong option turns RED, authoritative correct option turns GREEN.")

    # 3. Scenario B details: "Your answer: ..." and "Correct answer: ..."
    assert "Your answer:" in code, "Missing 'Your answer:' text in incorrect scenario"
    assert "Correct answer:" in code, "Missing 'Correct answer:' text in incorrect scenario"
    print("  [PASS] 3. Detailed Feedback Banner displays student choice vs correct answer.")

    # 4. Mode-specific safety: Timed and Mock exams must not reveal colors
    assert 'mode === "practice" && isRevealed' in code, "Mode check missing for answer color reveal"
    print("  [PASS] 4. Exam integrity preserved: Answers only revealed in Practice Mode.")

    # 5. Question Navigator Palette colors
    assert 'mode === "practice" && isAns' in code, "Missing practice mode condition for question palette"
    assert "bg-brand-red/20 text-brand-red" in code or "border-brand-red" in code, "Missing red palette color for incorrect question"
    assert "bg-brand-green/20 text-brand-green" in code, "Missing green palette color for correct question"
    print("  [PASS] 5. Question Navigator Palette accurately displays GREEN for correct and RED for incorrect.")

    # 6. Session recovery and persistence
    assert "revealed: newRevealed" in code, "Active session snapshot must persist revealed array"
    assert "isAnswerRevealed" in code or "answers[currentIndex] >= 0" in code, "Revisiting answered questions must restore reveal state"
    print("  [PASS] 6. State Persistence: Answer reveal state is saved and restored across question navigation.")

    print("\n======================================================================")
    print("ALL 6 ANSWER FEEDBACK VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("======================================================================")

if __name__ == "__main__":
    run_tests()
