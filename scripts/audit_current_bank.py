import json
import os
import sys

BASE = r"c:\VS Code\Codes\dgcacpllearning"
q_file = os.path.join(BASE, "src", "data", "questions.json")

with open(q_file, "r", encoding="utf-8") as f:
    qs = json.load(f)

print(f"Total existing questions: {len(qs)}")

subj_counts = {}
topic_counts = {}
difficulties = {}
id_prefixes = set()

for q in qs:
    s = q.get("subject", "Unknown")
    t = q.get("topic", "Unknown")
    key = f"{s} || {t}"
    d = q.get("difficulty", "Unknown")
    qid = q.get("id", "")
    prefix = qid.split("-")[0] if "-" in qid else "OTHER"
    id_prefixes.add(prefix)
    
    subj_counts[s] = subj_counts.get(s, 0) + 1
    topic_counts[key] = topic_counts.get(key, 0) + 1
    difficulties[d] = difficulties.get(d, 0) + 1

print("\n--- SUBJECT BREAKDOWN ---")
for s, c in sorted(subj_counts.items()):
    print(f"  {s}: {c} questions")

print("\n--- DIFFICULTY BREAKDOWN ---")
for d, c in sorted(difficulties.items()):
    print(f"  {d}: {c} questions")

print(f"\nTotal unique topics: {len(topic_counts)}")
print("\n--- TOPICS WITH QUESTION COUNTS ---")
for k, c in sorted(topic_counts.items()):
    print(f"  {k}: {c} Qs")

print(f"\nID Prefixes in use: {id_prefixes}")

# Inspect raw sources in scripts directory
print("\n--- CHECKING RAW SOURCE FILES ---")
for fname in ["nav_raw.json", "reg_raw.json"]:
    fpath = os.path.join(BASE, "scripts", fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as rf:
            raw_data = json.load(rf)
            print(f"  Found {fname}: {len(raw_data)} items")
            if raw_data:
                first = raw_data[0]
                print(f"    Sample keys: {list(first.keys())}")
    else:
        print(f"  {fname} not found!")

# Check other files or source materials in the repo or parent
print("\n--- CHECKING SOURCE DIRECTORY / WORKSPACE ---")
for item in os.listdir(BASE):
    item_path = os.path.join(BASE, item)
    if os.path.isfile(item_path):
        size = os.path.getsize(item_path)
        print(f"  File: {item} ({size} bytes)")
    else:
        print(f"  Dir:  {item}/")

