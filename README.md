# DGCA CPL Exam Practice Quiz

A personalised, offline-capable Multiple Choice Question practice app for the **DGCA Commercial Pilot Licence (CPL) written exams** in India.

> **Offline first** — works entirely in the browser with no server, no backend, and no internet required after the first load.

---

## Screenshots

_(Add screenshots here after running the app)_

---

## Features

| Feature | Details |
|---------|---------|
| **6 Subjects** | Air Navigation, Air Regulations, Aviation Meteorology, Technical General, Technical Specific, RTR |
| **Practice Mode** | Instant right/wrong feedback with full explanation and source reference |
| **Timed Mode** | User-configurable countdown timer; results shown at the end |
| **Mock Exam Mode** | Follows DGCA exam paper counts and durations from `examConfig.json` |
| **Topic Filter** | Filter questions by specific chapter/topic within a subject |
| **Question Navigator** | Visual grid showing answered ✅, flagged 🚩, current 🔵, unanswered ⬜ |
| **Flag for Review** | Mark any question; see count on finish prompt |
| **Results Screen** | Score, %, pass/fail, time taken, subject breakdown with bar charts, topic breakdown |
| **Review Mistakes** | Every wrong answer shown with your choice, correct answer, explanation, and source |
| **Retry Wrong Only** | One-click to retry only the questions you got wrong |
| **Progress Saved** | `localStorage` (try/catch guarded) — survives refresh; per-subject accuracy history |
| **Weak Areas Panel** | Home screen shows your weakest subjects sorted by accuracy |
| **Dark Mode** | Toggle (persisted across sessions) |
| **Randomised** | Question order and option order shuffled on every attempt |
| **Keyboard shortcuts** | `←/p` prev · `→/n/Space` next · `1–4` select option · `f` flag |
| **Responsive** | Mobile-first, large tap targets, works on phone and laptop |
| **Accessible** | Keyboard-navigable, good colour contrast, focus indicators |

---

## DGCA CPL Exam Scheme (from `examConfig.json`)

| Subject | Questions | Duration | Pass Mark |
|---------|-----------|----------|-----------|
| Air Navigation | 100 MCQs | 3 h | 70% |
| Aviation Meteorology | 50 MCQs | 2 h | 70% |
| Air Regulations | 50 MCQs | 1.5 h | 70% |
| Technical General | 100 MCQs | 2.5 h | 70% |
| Technical Specific | 50 MCQs | 1.5 h | 70% |
| RTR(A) | Separate exam | — | — |

**No negative marking.** Each paper must be passed independently at ≥ 70%.

---

## How to Run Locally

### Option A — Just open the standalone HTML (no install needed)

```bash
# Open directly in any browser:
open cpl-quiz-standalone.html
```

### Option B — Run from source (Vite dev server)

```bash
npm install
npm run dev
# Open http://localhost:5173
```

### Build production bundle

```bash
npm run build
# Output goes to dist/
```

---

## How to Add or Replace Questions

1. Open `src/data/questions.json`
2. Each question follows this schema:

```json
{
  "id": "NAV-001",
  "subject": "Air Navigation",
  "topic": "The Earth, Direction and Position",
  "difficulty": "easy",
  "question": "What does the term 'graticule' describe?",
  "options": [
    "Every line printed on a chart",
    "The network of meridians and parallels on a globe, map or chart",
    "Only the small circles near a pole",
    "A magnetic compass correction card"
  ],
  "answerIndex": 1,
  "explanation": "The graticule is the network formed by meridians and parallels, with the prime meridian and equator as its reference lines.",
  "source": "R.K. Bali Air Navigation / Oxford ATPL Gen Nav, Chapter 'The Earth, Direction and Position', Sec 4"
}
```

3. Run the validator to check for errors:

```bash
python scripts/validate_questions.py
```

4. Rebuild the standalone HTML:

```bash
python scripts/build_standalone.py
```

---

## Project Structure

```
dgcacpllearning/
├── src/
│   └── data/
│       ├── questions.json        ← Question bank (edit here)
│       └── examConfig.json       ← DGCA exam scheme
├── scripts/
│   ├── validate_questions.py     ← Validation tool (run before pushing)
│   └── build_standalone.py       ← Builds the single-file HTML
├── cpl-exam-direct.html          ← App template (with placeholder)
├── cpl-quiz-standalone.html      ← Built output — open this!
├── public/
├── index.html
├── package.json
└── README.md
```

---

## How to Deploy on Vercel

1. Push to GitHub:

```bash
git init
git add .
git commit -m "Initial commit — DGCA CPL quiz app"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. Go to [vercel.com](https://vercel.com), click **Add New Project**, import your GitHub repo.
3. Vercel auto-detects Vite; set:
   - **Framework preset**: Vite
   - **Output directory**: `dist`
   - **Build command**: `npm run build`
4. Click **Deploy**. Done! 🚀

> **Alternative**: For the standalone HTML, just drag `cpl-quiz-standalone.html` to [tiiny.host](https://tiiny.host) or any static host — no config needed.

---

## Source Books Referenced

The question bank is based on these standard textbooks (not included in this repo):

- **R.K. Bali** — Air Navigation, Air Regulations (India DGCA syllabus)
- **I.C. Joshi** — Aviation Meteorology
- **CAE Oxford ATPL** manuals (Gen Nav, Meteorology, AGK, Air Law)
- **aviationgrade.in** — Chapter-wise study notes and question breakdowns

> ⚠️ Source books are **not** included in this repository (copyrighted material).

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `←` or `p` | Previous question |
| `→`, `n`, or `Space` | Next question |
| `1` – `4` | Select option A–D |
| `f` | Flag / unflag current question |

---

## License

MIT — free for personal use. Source book content belongs to respective publishers.

