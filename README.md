# CPL Practice — DGCA Written Examination Platform

A premium, offline-first DGCA Commercial Pilot Licence (CPL, India) written examination preparation platform featuring **839 verified questions**, persistent **Zero-Repeat Question Rotation**, unconditional authoritative answer feedback, and a rich charcoal dashboard inspired by modern aviation LMS interfaces.

> **100% Client-Side & Offline-First** — Operates entirely inside the web browser with zero server requirements, zero dependencies, and zero database setup. Deploys directly to Vercel, GitHub Pages, or runs locally.

---

## 🚀 Key Highlights & Architecture

| Capability | Specification |
|---|---|
| **Question Bank** | **839 authentic questions** across all 6 DGCA CPL subjects and 94 topics |
| **Duplicate Prevention** | Multi-layer normalized & semantic check — **108 duplicate candidates intercepted** (0 duplicates in bank) |
| **Zero-Repeat Rotation** | Previously served questions do NOT repeat on retakes until that chapter/subject pool is exhausted |
| **Authoritative Feedback** | Unconditional display of authoritative correct answer (+1 pt), student choice (0 pts / +1 pt), verified explanations, and source citations |
| **Examination Modes** | **Practice Mode** (instant feedback & educational explanations), **Timed Exam**, and **DGCA Mock Exam** (full CBT simulation) |
| **Scoring Engine** | 70% passing threshold per DGCA paper rules, points tracking, and persistent analytics |
| **CBT Question Navigator** | Interactive grid showing Answered (green), Flagged (orange), Current (purple ring), and Unanswered |
| **Design System** | FLyP Academy-inspired premium dark charcoal aesthetic (`#19191D`, `#202126`, `#292A30`, `#9484F5`, `#719CFF`, `#51C6C1`, `#69CF9B`, `#E5C36C`, `#ED7078`) |

---

## 📚 Question Bank Inventory (839 Total Questions)

| Subject | Questions | Topics | Official Source & Reference |
|---|---|---|---|
| **Air Navigation** | **298 Qs** | 25 Topics (12 Qs/ch) | Oxford ATPL General Navigation / R.K. Bali / CAR Section 7 |
| **Air Regulations** | **300 Qs** | 25 Topics (12 Qs/ch) | DGCA Aircraft Rules 1937, Bharatiya Vayuyan Adhiniyam 2024, CARs |
| **Aviation Meteorology** | **93 Qs** | 18 Topics | I.C. Joshi Aviation Meteorology (Chapters 1–26) |
| **Technical General** | **59 Qs** | 9 Topics | Oxford ATPL Aircraft General Knowledge, Engines, Systems, Principles of Flight |
| **Technical Specific** | **42 Qs** | 7 Topics | Pilot's Operating Handbooks (POH), V-speeds, Limitations, Fuel & Altimetry |
| **RTR (Radio Telephony)** | **47 Qs** | 10 Topics | ICAO Doc 9432, Doc 8400, WPC RTR(A) Syllabus, SSR Transponder Codes |

---

## 🔄 Zero-Repeat Question Rotation Engine

The application includes a persistent question rotation tracking engine (`cpl_served_ids` in `localStorage`):
- When a quiz is initiated, served question IDs are permanently recorded.
- When re-taking a quiz for any chapter or subject, **previously served questions are filtered out**.
- The student experiences fresh, unattempted questions on every retake.
- When an individual topic or subject pool is fully exhausted, the app displays a clear completion banner and enables a one-click **"Reset Question Pool"** option to cycle through the chapter again without clearing long-term performance scores (`cpl_history`).

---

## 📋 Question Bank Audit Modal

Click **"Audit Bank (839 Qs)"** in the top navigation bar to inspect:
- Total active questions and difficulty breakdown (Easy: 125, Medium: 641, Hard: 73).
- Duplicate prevention audit log summary.
- Real-time unserved vs served questions counters across all subjects.
- Quick-action buttons to reset question rotation pools or review coverage.

---

## 📁 Repository Files

- `index.html` — Root entry point for Vercel / GitHub Pages / browser.
- `cpl-exam-direct.html` / `cpl-quiz-standalone.html` — Standalone mirrors for direct offline double-click execution.
- `src/data/questions.json` — The master database containing all 839 validated questions.
- `src/data/examConfig.json` — DGCA CPL examination paper duration and question schemes.
- `scripts/build_direct_html_v2.py` — High-performance compiler script that builds the self-contained app.
- `scripts/rejected_duplicates.json` — Full audit log of 108 duplicate candidates intercepted and rejected.
- `scripts/test_zero_repeat_and_feedback.py` — Automated verification test suite.
- `dgca-cpl-github-upload.zip` — Ready-to-upload zip archive for GitHub web interface.
