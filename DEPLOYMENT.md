# CPL Practice 2.0 — Full-Stack Deployment & Operation Manual

## 1. System Architecture Overview

CPL Practice 2.0 is built as a production-grade, full-stack aviation examination platform designed for the DGCA Commercial Pilot Licence (India) syllabus:

```
┌─────────────────────────────────────────────────────────────┐
│                 PRESENTATION & CLIENT LAYER                 │
│      Next.js 14 (App Router) + React 18 + Tailwind CSS      │
│      Dark Charcoal Aviation Design (#19191D / #202126)      │
│      Responsive CBT Interface & PWA Service Worker (sw.js)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 APPLICATION & SECURITY LAYER                │
│       Next.js Route Handlers & Edge-Compatible APIs         │
│  • /api/quiz/start          • /api/quiz/finish              │
│  • /api/student/readiness   • /api/student/reset-rotation   │
│  • /api/admin/questions     • Auth Middleware & Role Checks │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 DATABASE & PERSISTENCE LAYER                │
│                     Supabase PostgreSQL 15+                 │
│  • public.profiles          • public.questions (839 Qs)     │
│  • public.subjects (6)      • public.topics (94)            │
│  • public.quiz_attempts     • public.student_answers        │
│  • public.mistake_notebook  • public.spaced_repetition      │
│  • public.exposure_history  • public.aviation_documents     │
│  • Row Level Security (RLS) • Complete Seed (seed.sql)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Environment Configuration

1. Copy `.env.example` to `.env.local`:
```bash
cp .env.example .env.local
```

2. Fill in your Supabase credentials:
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-public-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-secret-service-role-key
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_PASS_MARK_PERCENT=70
```

---

## 3. Database Migration & Seeding

### Applying Migrations via Supabase CLI or SQL Editor:
1. Open your **Supabase Project Dashboard -> SQL Editor**.
2. Run `supabase/migrations/20261104000000_cpl_core_schema.sql` to create all 13 tables, performance indexes, and RLS security policies.
3. Run `supabase/seed.sql` to populate all **6 Subjects, 94 Topics, and 839 Verified Questions**.

### Question Bank Relational Verification:
- **Air Navigation**: 298 questions across 25 topics
- **Air Regulations**: 300 questions across 25 topics
- **Aviation Meteorology**: 93 questions across 18 topics
- **Technical General**: 59 questions across 9 topics
- **Technical Specific**: 42 questions across 7 topics
- **RTR**: 47 questions across 10 topics
- **Total**: Exactly **839 verified questions** with 0 loss and 0 duplicates.

---

## 4. Key Security & Functional Protections

1. **Answer Protection**:
   - In **Timed** and **Mock Exam** modes, `/api/quiz/start` strips `answer_index` and `explanation` from the JSON payload.
   - The authoritative answer key is stored exclusively on the server and is revealed only after the exam is submitted to `/api/quiz/finish`.
2. **Server-Side Scoring**:
   - Official scores, accuracy percentages, and pass/fail statuses are computed on the server.
3. **Zero-Repeat Rotation**:
   - `question_exposure_history` tracks every served question per student. Retaking a chapter filters out served questions until the chapter pool is exhausted.
4. **Role-Based Access Control**:
   - Middleware blocks non-admin students from accessing `/admin` routes.
5. **Offline Fallback**:
   - Standalone offline mirrors (`cpl-exam-direct.html`, `index.html`) continue to run without requiring a server or database.

---

## 5. Local Development & Production Build

```bash
# Install dependencies
npm install

# Run local development server
npm run dev

# Run production build
npm run build

# Start production server
npm start
```

---

## 6. Vercel Production Deployment

1. Push your repository to **GitHub**.
2. Go to [Vercel Dashboard](https://vercel.com) -> **Add New Project** -> Import your repository.
3. In **Environment Variables**, add:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
4. Click **Deploy**. Vercel will build and deploy the Next.js application automatically.
