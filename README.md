# ✈️ DGCA CPL Exam Practice — Commercial Pilot Ground School

An authentic, exam-focused web application built for pilots preparing for the **DGCA CPL (Commercial Pilot Licence)** written examinations administered by the Directorate General of Civil Aviation, Government of India.

Designed for fast revision, topic-wise practice, and full CBT mock exams on phones, tablets, and laptops.

---

## 🎯 Target Examination Subjects

1. **Air Navigation** (General Navigation, Earth Magnetism, Chart Projections, Dead Reckoning, 1-in-60 Rule, Critical Point & PNR)
2. **Air Regulations & Human Factors** (The Aircraft Act 1934, Aircraft Rules 1937, DGCA Civil Aviation Requirements, ICAO Annexes 1/2/14, Rules of the Air, Separation Minima, and Aviation Physiology)
3. **Aviation Meteorology** (Atmosphere, Pressure, Altimetry, Density, Stability, Winds, Hazards, Thunderstorms, Climatology of India, METAR, SPECI, and TAF Codes)

---

## 🚀 Key Features

- **Two Training Modes**:
  - **📝 Practice Mode**: Untimed training with immediate feedback, detailed explanations, and exact textbook citations on every question.
  - **⏱️ Mock Exam Mode**: Follows official DGCA Pariksha CBT rules (full countdown timer, 70% passing threshold, score revealed only upon final submission).
- **Navigation & Palette Grid**:
  - Live color-coded question palette indicating *Answered*, *Unanswered*, *Flagged 🚩*, and *Current* questions.
  - One-click jump to any question in the exam.
- **Mistake Review & Smart Retry**:
  - Detailed review screen highlighting your selection vs. the correct answer side-by-side with official explanations.
  - **"Retry Wrong Questions Only"** button to instantly launch a targeted remediation drill with only the questions missed.
- **Performance Analytics & Weak Area Tracking**:
  - Automatically tracks attempts and accuracy in browser `localStorage` (wrapped in fail-safe try/catch blocks).
  - Displays subject accuracy bars (identifying whether you are above or below the DGCA 70% pass threshold).
  - Highlights top weak topics requiring study priority.
- **Dynamic Randomisation**:
  - Question sequence and option orders (A, B, C, D) are randomised on every single attempt to eliminate positional memory.
- **Cockpit Night Mode**:
  - High-contrast day/night toggle designed for low-light cockpit/study environments with persisted preference.
- **Keyboard Shortcuts (Laptop / Desktop)**:
  - `1`, `2`, `3`, `4`: Select option A, B, C, or D
  - `ArrowLeft` / `P`: Previous question
  - `ArrowRight` / `N`: Next question
  - `F`: Toggle flag for review
  - `Escape`: Close modals

---

## 📚 Ground School Source Materials

All 140 multiple-choice questions in the question bank are sourced from standard DGCA ground school literature and syllabi:

- **Air Navigation**: *R.K. Bali — Air Navigation* and *CAE Oxford Aviation ATPL Book 10 (General Navigation)* via AviationGrade curriculum.
- **Air Regulations & Human Factors**: *Air Regulation and Human Factors Book (17th Edition)*, *The Aircraft Act 1934*, *Aircraft Rules 1937*, and *DGCA Civil Aviation Requirements (CARs)*.
- **Aviation Meteorology**: *I.C. Joshi — Aviation Meteorology (3rd Edition, Himalayan Books)*, *ICAO Annex 3*, and *WMO Manual on Codes*.

*(Note: In compliance with copyright requirements, source books and PDF files are NOT distributed in this repository. Questions reference specific chapters, sections, and pages).*

---

## 🛠️ Project Structure

```text
dgcacpllearning/
├── public/                 # Static assets
├── scripts/
│   ├── validate_questions.py  # Zero-dependency Python question validator
│   ├── build_question_bank.py # Question bank assembly script
│   ├── fetch_nav.mjs          # Navigation curriculum fetcher
│   └── fetch_reg.mjs          # Regulation curriculum fetcher
├── src/
│   ├── components/
│   │   ├── Header.jsx         # App header with branding and night mode toggle
│   │   ├── HomeScreen.jsx     # Subject & mode selection, weak area analytics
│   │   ├── QuizScreen.jsx     # Exam screen with questions, timer, action bar
│   │   ├── QuestionGrid.jsx   # Collapsible question palette
│   │   ├── ResultsScreen.jsx  # Pass/Fail evaluation, subject/topic breakdown
│   │   ├── ReviewScreen.jsx   # Step-by-step mistake review with citations
│   │   └── ConfirmModal.jsx   # Dialog for early submission, exit, and reset
│   ├── data/
│   │   ├── examConfig.json    # DGCA CPL exam pattern, timing, pass marks
│   │   └── questions.json     # 140 verified questions with source citations
│   ├── hooks/
│   │   └── useLocalStorage.js # Fail-safe storage hook
│   ├── App.jsx                # Application state machine and randomisation
│   ├── index.css              # Aviation-themed CSS stylesheet
│   └── main.jsx               # React DOM entry point
├── index.html                 # Single page application HTML
├── package.json               # Vite & React dependencies
├── vite.config.js             # Vite configuration
└── README.md                  # Documentation
```

---

## 💻 Local Setup & Development

### Prerequisites
- **Node.js** (v18.0.0 or higher recommended)
- **Python 3** (for running the validation script)

### 1. Clone & Install Dependencies
```bash
git clone <your-repository-url>
cd dgcacpllearning
npm install
```

### 2. Run the Development Server
```bash
npm run dev
```
Open your browser at `http://localhost:3000` to start practicing.

### 3. Build for Production
```bash
npm run build
```
The optimized static build will be placed in the `dist/` directory.

### 4. Preview Production Build
```bash
npm run preview
```

---

## 🧪 Validating Question Content

To ensure question integrity, run the Python validator (uses Python standard library only, no pip dependencies required):

```bash
python scripts/validate_questions.py
```

The validator checks:
- ✅ Required fields: `id`, `subject`, `topic`, `difficulty`, `question`, `options`, `answerIndex`, `explanation`, `source`
- ✅ Exactly 4 options per question
- ✅ `answerIndex` is an integer within `0..3`
- ✅ No duplicate question texts or IDs
- ✅ Valid difficulty (`easy`, `medium`, `hard`)
- ✅ Presence of an official textbook source citation

---

## ✍️ How to Add Questions

Questions are stored in `src/data/questions.json`. To add a new question, append an object following this schema:

```json
{
  "id": "NAV-051",
  "subject": "Air Navigation",
  "topic": "Great Circles and Rhumb Lines",
  "difficulty": "medium",
  "question": "What is the primary defining property of a Great Circle on the Earth's surface?",
  "options": [
    "It cuts all meridians at the same constant angle",
    "It is a circle on the surface of a sphere whose plane passes through the centre of the sphere",
    "It is any circle parallel to the equator",
    "It represents a line of constant compass heading"
  ],
  "answerIndex": 1,
  "explanation": "A great circle is a circle on the surface of a sphere whose center and radius are those of the sphere itself, dividing the sphere into two equal hemispheres. It marks the shortest distance between two points.",
  "source": "R.K. Bali Air Navigation / Oxford ATPL Gen Nav, Chapter 'Great Circles and Rhumb Lines', Sec 2"
}
```

After adding questions, run:
```bash
python scripts/validate_questions.py
npm run build
```

---

## ☁️ Deploying to Vercel

This application is built with standard Vite and React. It deploys to Vercel as a 100% static site with zero backend or database required.

### Method A: Deploy via GitHub (Recommended)
1. Push this repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: DGCA CPL Exam Practice App"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```
2. Log in to [Vercel](https://vercel.com).
3. Click **"Add New Project"** and select your GitHub repository.
4. Keep the default settings:
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Click **"Deploy"**. Your application will be live in seconds with an SSL-enabled `.vercel.app` URL.

### Method B: Deploy via Vercel CLI
```bash
npm install -g vercel
vercel
```
Follow the interactive prompt, accept the default Vite presets, and your app will be live immediately.

---

## ⚖️ License & Disclaimer

This project is created strictly for educational practice and exam preparation for DGCA pilot licence applicants. It is not affiliated with the Directorate General of Civil Aviation (DGCA) or the Ministry of Civil Aviation, Government of India.

