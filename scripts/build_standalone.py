#!/usr/bin/env python3
"""
Build standalone HTML — inlines questions.json into index.html, cpl-exam-direct.html, and cpl-quiz-standalone.html.
Standard library only.
"""

import os
import sys
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIRECT = os.path.join(BASE, "scripts", "build_direct_html.py")

def build():
    print("DGCA CPL Quiz — Standalone HTML Builder")
    result = subprocess.run([sys.executable, BUILD_DIRECT], cwd=BASE)
    if result.returncode != 0:
        sys.exit(result.returncode)

if __name__ == "__main__":
    build()

