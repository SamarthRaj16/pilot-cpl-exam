#!/usr/bin/env python3
"""
DGCA CPL Quiz — Question Bank Validator
Checks questions.json for completeness, correctness, and duplicates.
Standard library only — no external dependencies.
"""

import json
import sys
import os
import re
from collections import Counter

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

REQUIRED_FIELDS = ["id", "subject", "topic", "difficulty", "question", "options", "answerIndex", "explanation", "source"]

VALID_SUBJECTS = {"Air Navigation", "Air Regulations", "Aviation Meteorology", "Technical General", "Technical Specific", "RTR"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}

def validate(path):
    print(f"\n{'='*60}")
    print(f"DGCA CPL Quiz — Question Bank Validator")
    print(f"File: {path}")
    print(f"{'='*60}\n")

    if not os.path.exists(path):
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        try:
            questions = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON: {e}")
            sys.exit(1)

    if not isinstance(questions, list):
        print("ERROR: questions.json must be a JSON array.")
        sys.exit(1)

    errors = []
    warnings = []

    ids_seen = set()
    questions_seen = set()
    subject_counts = Counter()
    topic_counts = Counter()

    for idx, q in enumerate(questions):
        qid = q.get("id", f"[index {idx}]")
        prefix = f"  Q #{idx+1} ({qid})"

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in q:
                errors.append(f"{prefix}: Missing required field '{field}'")
            elif not q[field] and q[field] != 0:
                errors.append(f"{prefix}: Field '{field}' is empty")

        if "id" not in q:
            continue

        # Check for garbled text (character-by-character quoting pattern)
        if "question" in q and re.search(r"'[a-z]''[a-z]'", q.get("question", "")):
            errors.append(f"{prefix}: question text appears to be garbled (character-quoted)")

        # Duplicate IDs
        if qid in ids_seen:
            errors.append(f"{prefix}: Duplicate ID '{qid}'")
        ids_seen.add(qid)

        # Duplicate question text
        qtext = q.get("question", "").strip().lower()
        if qtext in questions_seen and qtext:
            errors.append(f"{prefix}: Duplicate question text")
        questions_seen.add(qtext)

        # Subject check
        subj = q.get("subject", "")
        if subj not in VALID_SUBJECTS:
            errors.append(f"{prefix}: Unknown subject '{subj}'. Must be one of: {sorted(VALID_SUBJECTS)}")
        else:
            subject_counts[subj] += 1

        # Difficulty check
        diff = q.get("difficulty", "")
        if diff not in VALID_DIFFICULTIES:
            errors.append(f"{prefix}: Invalid difficulty '{diff}'. Must be: easy, medium, or hard")

        # Options check
        opts = q.get("options", [])
        if not isinstance(opts, list):
            errors.append(f"{prefix}: 'options' must be a list")
        elif len(opts) != 4:
            errors.append(f"{prefix}: Must have exactly 4 options, found {len(opts)}")
        else:
            for i, opt in enumerate(opts):
                if not isinstance(opt, str) or not opt.strip():
                    errors.append(f"{prefix}: Option {i} is empty or not a string")

        # answerIndex check
        ans = q.get("answerIndex")
        if not isinstance(ans, int):
            errors.append(f"{prefix}: 'answerIndex' must be an integer")
        elif not isinstance(opts, list):
            pass  # already reported
        elif ans < 0 or ans >= len(opts):
            errors.append(f"{prefix}: 'answerIndex' {ans} is out of range (0-{len(opts)-1})")

        # Source check
        src = q.get("source", "")
        if not src or len(src.strip()) < 5:
            errors.append(f"{prefix}: 'source' is missing or too short")

        # Explanation check
        expl = q.get("explanation", "")
        if len(expl.strip()) < 10:
            warnings.append(f"{prefix}: explanation is very short ({len(expl)} chars)")

        # Topic check
        topic = q.get("topic", "")
        if topic:
            topic_counts[(subj, topic)] += 1

    # Summary
    print(f"Total questions: {len(questions)}\n")

    print("Subject breakdown:")
    for subj in sorted(VALID_SUBJECTS):
        count = subject_counts.get(subj, 0)
        note = " ⚠️  (< 25)" if count < 25 else ""
        print(f"  {subj}: {count} questions{note}")

    print()
    if errors:
        print(f"ERRORS ({len(errors)} found):")
        for e in errors:
            print(f"  ❌ {e}")
    else:
        print("✅ No errors found!")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)} found):")
        for w in warnings:
            print(f"  ⚠️  {w}")

    print(f"\n{'='*60}")
    if errors:
        print(f"RESULT: FAILED — {len(errors)} error(s) must be fixed.")
        return False
    else:
        print(f"RESULT: PASSED — question bank is valid.")
        return True

if __name__ == "__main__":
    qpath = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), "..", "src", "data", "questions.json"
    )
    ok = validate(qpath)
    sys.exit(0 if ok else 1)

