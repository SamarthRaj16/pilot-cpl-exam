# -*- coding: utf-8 -*-
"""
Phase 1 Migration Inventory Generator
Analyzes the existing application, question bank, topics, exam config,
and generates the complete database migration inventory.
"""
import json
import os
import sys

BASE = r"c:\VS Code\Codes\dgcacpllearning"
q_path = os.path.join(BASE, "src", "data", "questions.json")
cfg_path = os.path.join(BASE, "src", "data", "examConfig.json")

with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

with open(cfg_path, "r", encoding="utf-8") as f:
    exam_config = json.load(f)

print(f"Loaded {len(questions)} questions.")

# Analyze subjects and topics
subjects_map = {}
for q in questions:
    s = q["subject"]
    t = q.get("topic", "General")
    if s not in subjects_map:
        subjects_map[s] = set()
    subjects_map[s].add(t)

print("\n--- INVENTORY ANALYSIS ---")
print(f"Total Subjects: {len(subjects_map)}")
total_topics = sum(len(topics) for topics in subjects_map.values())
print(f"Total Topics: {total_topics}")

for s, topics in sorted(subjects_map.items()):
    qs = [q for q in questions if q["subject"] == s]
    print(f"  {s}: {len(qs)} questions, {len(topics)} topics")

# Save migration inventory JSON
inv = {
    "total_questions": len(questions),
    "total_subjects": len(subjects_map),
    "total_topics": total_topics,
    "exam_config": exam_config,
    "subjects": {
        s: {
            "question_count": len([q for q in questions if q["subject"] == s]),
            "topic_count": len(topics),
            "topics": sorted(list(topics))
        }
        for s, topics in subjects_map.items()
    }
}

inv_path = os.path.join(BASE, "scripts", "migration_inventory.json")
with open(inv_path, "w", encoding="utf-8") as f:
    json.dump(inv, f, indent=2)

print(f"\nSaved migration inventory to {inv_path}")

