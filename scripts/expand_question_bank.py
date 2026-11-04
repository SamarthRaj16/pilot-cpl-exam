# -*- coding: utf-8 -*-
import json
import os
import re
import difflib
import sys

BASE = r"c:\VS Code\Codes\dgcacpllearning"
sys.path.append(os.path.join(BASE, "scripts"))
import build_met_tg_ts_rtr_bank as extra_bank

# Helper to normalize text for duplicate detection
def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    # Remove all non-alphanumeric characters
    return re.sub(r'[^a-z0-9]', '', text)

def get_word_set(text):
    if not text:
        return set()
    return set(re.findall(r'\b[a-z]{3,}\b', text.lower()))

def jaccard_similarity(set1, set2):
    if not set1 or not set2:
        return 0.0
    return len(set1 & set2) / len(set1 | set2)

def clean_str(s):
    if not isinstance(s, str):
        return str(s) if s is not None else ""
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("?T", "'").replace("?", "'") if "?T" in s else s
    return s.strip()

# 1. Load existing questions
existing_path = os.path.join(BASE, "src", "data", "questions.json")
with open(existing_path, "r", encoding="utf-8") as f:
    existing_questions = json.load(f)

print(f"Loaded {len(existing_questions)} existing questions.")

# Set up tracking structures
final_bank = []
norm_to_q = {}
rejected_duplicates = []

# Index existing questions
for q in existing_questions:
    clean_q = {
        "id": q["id"],
        "subject": clean_str(q["subject"]),
        "topic": clean_str(q["topic"]),
        "difficulty": q.get("difficulty", "medium"),
        "question": clean_str(q["question"]),
        "options": [clean_str(opt) for opt in q["options"]],
        "answerIndex": q.get("answerIndex", q.get("answer", 0)),
        "explanation": clean_str(q["explanation"]),
        "source": clean_str(q["source"])
    }
    final_bank.append(clean_q)
    norm = normalize_text(clean_q["question"])
    norm_to_q[norm] = clean_q

def is_duplicate(candidate_q_text):
    cand_norm = normalize_text(candidate_q_text)
    if not cand_norm:
        return True, None, 1.0, "Empty question"

    # 1. Exact normalized match
    if cand_norm in norm_to_q:
        matched = norm_to_q[cand_norm]
        return True, matched, 1.0, "Exact normalized text match"

    # 2. Token overlap and sequence similarity check
    cand_words = get_word_set(candidate_q_text)
    for exist_norm, exist_q in norm_to_q.items():
        exist_words = get_word_set(exist_q["question"])
        j_sim = jaccard_similarity(cand_words, exist_words)
        if j_sim > 0.70:
            seq_sim = difflib.SequenceMatcher(None, cand_norm, exist_norm).ratio()
            if seq_sim > 0.75:
                return True, exist_q, max(j_sim, seq_sim), f"Semantic token/sequence overlap ({seq_sim:.2f})"

    return False, None, 0.0, ""

# 2. Extract remaining questions from nav_raw.json (300 items)
with open(os.path.join(BASE, "scripts", "nav_raw.json"), "r", encoding="utf-8") as f:
    nav_raw = json.load(f)

nav_admitted = 0
current_nav_id_num = max([int(q["id"].split("-")[1]) for q in existing_questions if q["id"].startswith("NAV-")] or [0])

for item in nav_raw:
    chap = clean_str(item.get("chapter", "Air Navigation"))
    d = item["data"]
    q_text = clean_str(d["q"])
    
    dup, matched, score, reason = is_duplicate(q_text)
    if dup:
        rejected_duplicates.append({
            "candidate_subject": "Air Navigation",
            "candidate_topic": chap,
            "candidate_question": q_text,
            "matched_id": matched["id"] if matched else "N/A",
            "matched_question": matched["question"] if matched else "",
            "similarity_score": round(score, 3),
            "rejection_reason": reason
        })
        continue

    current_nav_id_num += 1
    new_id = f"NAV-{current_nav_id_num:03d}"
    new_q = {
        "id": new_id,
        "subject": "Air Navigation",
        "topic": chap,
        "difficulty": "medium",
        "question": q_text,
        "options": [clean_str(opt) for opt in d["o"]],
        "answerIndex": d["a"],
        "explanation": clean_str(d["e"]),
        "source": f"Oxford ATPL General Navigation / R.K. Bali, Chapter '{chap}'"
    }
    final_bank.append(new_q)
    norm_to_q[normalize_text(q_text)] = new_q
    nav_admitted += 1

print(f"Air Navigation: admitted {nav_admitted} new questions from raw pool.")

# 3. Extract remaining questions from reg_raw.json (300 items)
with open(os.path.join(BASE, "scripts", "reg_raw.json"), "r", encoding="utf-8") as f:
    reg_raw = json.load(f)

reg_admitted = 0
current_reg_id_num = max([int(q["id"].split("-")[1]) for q in existing_questions if q["id"].startswith("REG-")] or [0])

for item in reg_raw:
    chap = clean_str(item.get("chapter", "Definitions and Framework"))
    d = item["data"]
    q_text = clean_str(d["q"])
    
    dup, matched, score, reason = is_duplicate(q_text)
    if dup:
        rejected_duplicates.append({
            "candidate_subject": "Air Regulations",
            "candidate_topic": chap,
            "candidate_question": q_text,
            "matched_id": matched["id"] if matched else "N/A",
            "matched_question": matched["question"] if matched else "",
            "similarity_score": round(score, 3),
            "rejection_reason": reason
        })
        continue

    current_reg_id_num += 1
    new_id = f"REG-{current_reg_id_num:03d}"
    new_q = {
        "id": new_id,
        "subject": "Air Regulations",
        "topic": chap,
        "difficulty": "medium",
        "question": q_text,
        "options": [clean_str(opt) for opt in d["o"]],
        "answerIndex": d["a"],
        "explanation": clean_str(d["e"]),
        "source": f"R.K. Bali Air Regulations / DGCA CAR, Chapter '{chap}'"
    }
    final_bank.append(new_q)
    norm_to_q[normalize_text(q_text)] = new_q
    reg_admitted += 1

print(f"Air Regulations: admitted {reg_admitted} new questions from raw pool.")

# 4. Add Extra Met, TG, TS, RTR questions
extra_specs = [
    ("Aviation Meteorology", "MET", extra_bank.MET_NEW_QUESTIONS),
    ("Technical General", "TG", extra_bank.TG_NEW_QUESTIONS),
    ("Technical Specific", "TS", extra_bank.TS_NEW_QUESTIONS),
    ("RTR", "RTR", extra_bank.RTR_NEW_QUESTIONS),
]

for subj_name, prefix, q_list in extra_specs:
    admitted = 0
    curr_id = max([int(q["id"].split("-")[1]) for q in existing_questions if q["id"].startswith(f"{prefix}-")] or [0])
    for cand in q_list:
        q_text = clean_str(cand["question"])
        dup, matched, score, reason = is_duplicate(q_text)
        if dup:
            rejected_duplicates.append({
                "candidate_subject": subj_name,
                "candidate_topic": cand.get("topic", "General"),
                "candidate_question": q_text,
                "matched_id": matched["id"] if matched else "N/A",
                "matched_question": matched["question"] if matched else "",
                "similarity_score": round(score, 3),
                "rejection_reason": reason
            })
            continue

        curr_id += 1
        new_id = f"{prefix}-{curr_id:03d}"
        new_q = {
            "id": new_id,
            "subject": subj_name,
            "topic": clean_str(cand["topic"]),
            "difficulty": cand.get("difficulty", "medium"),
            "question": q_text,
            "options": [clean_str(opt) for opt in cand["options"]],
            "answerIndex": cand["answerIndex"],
            "explanation": clean_str(cand["explanation"]),
            "source": clean_str(cand["source"])
        }
        final_bank.append(new_q)
        norm_to_q[normalize_text(q_text)] = new_q
        admitted += 1
    print(f"{subj_name}: admitted {admitted} new verified questions.")

# 5. Strict Validation Pass on ALL questions
print("\n--- RUNNING STRICT VALIDATION ON ALL QUESTIONS ---")
seen_ids = set()
for idx, q in enumerate(final_bank):
    assert q["id"] not in seen_ids, f"Duplicate ID detected: {q['id']}"
    seen_ids.add(q["id"])
    assert len(q["subject"]) > 2, f"Invalid subject at index {idx}"
    assert len(q["topic"]) > 1, f"Invalid topic in {q['id']}"
    assert q["difficulty"] in ["easy", "medium", "hard"], f"Invalid difficulty in {q['id']}"
    assert len(q["question"]) > 10, f"Question text too short in {q['id']}"
    assert len(q["options"]) == 4, f"Options count is not 4 in {q['id']}"
    for opt_idx, opt in enumerate(q["options"]):
        assert len(opt) > 0, f"Empty option {opt_idx} in {q['id']}"
    assert isinstance(q["answerIndex"], int) and 0 <= q["answerIndex"] <= 3, f"Invalid answerIndex in {q['id']}"
    assert len(q["explanation"]) > 10, f"Explanation too short in {q['id']}"
    assert len(q["source"]) > 5, f"Source citation too short in {q['id']}"

print("All validation assertions PASSED successfully!")

# 6. Save expanded question bank
out_path = os.path.join(BASE, "src", "data", "questions.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(final_bank, f, ensure_ascii=False, indent=2)

print(f"\nSUCCESS: Saved expanded question bank to {out_path} ({len(final_bank)} total questions).")

# 7. Save rejected duplicates audit
rej_path = os.path.join(BASE, "scripts", "rejected_duplicates.json")
with open(rej_path, "w", encoding="utf-8") as f:
    json.dump(rejected_duplicates, f, ensure_ascii=False, indent=2)

print(f"Saved duplicate audit to {rej_path} ({len(rejected_duplicates)} rejected candidates).")

# 8. Print Subject breakdown
from collections import Counter
subj_counts = Counter(q["subject"] for q in final_bank)
diff_counts = Counter(q["difficulty"] for q in final_bank)
topic_counts = len(set(q["topic"] for q in final_bank))

print("\n--- FINAL QUESTION BANK INVENTORY ---")
print(f"Total Questions: {len(final_bank)}")
print(f"Total Topics: {topic_counts}")
print("\nBy Subject:")
for s, c in sorted(subj_counts.items()):
    print(f"  {s}: {c} questions")

print("\nBy Difficulty:")
for d, c in sorted(diff_counts.items()):
    print(f"  {d}: {c} questions")

