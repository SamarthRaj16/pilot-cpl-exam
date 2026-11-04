import json
import os

BASE = r"c:\VS Code\Codes\dgcacpllearning"
for fname in ["nav_raw.json", "reg_raw.json"]:
    fpath = os.path.join(BASE, "scripts", fname)
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"\n=== {fname} ({len(data)} items) ===")
    sample = data[0]
    print("Sample item keys:", sample.keys())
    print("Chapter:", sample.get("chapter"))
    inner_data = sample.get("data", {})
    if isinstance(inner_data, dict):
        print("Inner data keys:", inner_data.keys())
        questions = inner_data.get("questions", [])
        print(f"Number of inner questions in this chapter item: {len(questions)}")
        if questions:
            print("First question sample:", json.dumps(questions[0], indent=2)[:400])
    elif isinstance(inner_data, list):
        print("Inner data is a list of len:", len(inner_data))
        if inner_data:
            print("First item sample:", json.dumps(inner_data[0], indent=2)[:400])

