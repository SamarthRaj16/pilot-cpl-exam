import re
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

file_path = r"c:\VS Code\Codes\dgcacpllearning\cpl-exam-direct.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

parts = html.split("<script>")
if len(parts) < 2:
    print("ERROR: No <script> found in html file!")
    sys.exit(1)

html_part = parts[0]
script_part = parts[1].split("</script>")[0]

ids_in_script = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', script_part))
ids_in_html = set(re.findall(r'id=["\']([^"\']+)["\']', html_part))

missing = ids_in_script - ids_in_html
print(f"Total IDs in script: {len(ids_in_script)}")
print(f"Total IDs in HTML: {len(ids_in_html)}")
for item in sorted(ids_in_script):
    print(f"  ID: {item}")
if missing:
    print(f"❌ Missing IDs in HTML: {missing}")
else:
    print("✅ All getElementById references match IDs in HTML!")

# Check screens
screens = ["homeScreen", "quizScreen", "resultScreen", "reviewScreen"]
for s in screens:
    if s not in ids_in_html:
        print(f"❌ Missing screen: {s}")
    else:
        print(f"  Screen found: {s}")

