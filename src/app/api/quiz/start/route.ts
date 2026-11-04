import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";
import { createAdminClient } from "@/lib/supabase/admin";
import rawQuestions from "@/data/questions.json";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { subjectId, topicId, mode = "practice", questionCount = 50 } = body;

    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    const studentId = user?.id || "demo-student-id";

    // 1. Fetch student's question exposure history (Zero-Repeat Engine)
    let exposedIds = new Set<string>();
    if (user) {
      const { data: exposures } = await supabase
        .from("question_exposure_history")
        .select("question_id")
        .eq("student_id", studentId);

      if (exposures) {
        exposures.forEach((e) => exposedIds.add(e.question_id));
      }
    }

    // 2. Fetch candidate questions from Supabase (or fallback to master JSON in preview mode)
    let candidatePool = [];
    if (process.env.NEXT_PUBLIC_SUPABASE_URL) {
      let query = supabase
        .from("questions")
        .select("*")
        .eq("validation_status", "approved");

      if (subjectId) query = query.eq("subject_id", subjectId);
      if (topicId) query = query.eq("topic_id", topicId);

      const { data, error } = await query;
      if (!error && data && data.length > 0) {
        candidatePool = data;
      }
    }

    // Fallback if DB not seeded yet
    if (candidatePool.length === 0) {
      candidatePool = rawQuestions.filter((q: any) => {
        if (subjectId && q.subject !== subjectId) return false;
        if (topicId && q.topic !== topicId) return false;
        return true;
      });
    }

    // 3. Filter out previously served questions (ZERO-REPEAT ROTATION)
    const unservedPool = candidatePool.filter((q: any) => !exposedIds.has(q.id));

    // Handle pool exhaustion
    if (unservedPool.length === 0 && candidatePool.length > 0) {
      return NextResponse.json(
        {
          status: "exhausted",
          message:
            "All questions in this selection have been completed. Reset question exposure pool to cycle again.",
          totalQuestions: candidatePool.length,
        },
        { status: 200 }
      );
    }

    // 4. Shuffle unserved pool and pick batch
    const poolToUse = unservedPool.length > 0 ? unservedPool : candidatePool;
    const shuffled = [...poolToUse].sort(() => Math.random() - 0.5);
    const selectedQuestions = shuffled.slice(0, Math.min(questionCount, shuffled.length));

    // 5. Record question exposure
    if (user) {
      const adminClient = createAdminClient();
      const exposureInserts = selectedQuestions.map((q: any) => ({
        student_id: studentId,
        question_id: q.id,
        subject_id: q.subject_id || q.subject,
        topic_id: q.topic_id || q.topic,
      }));

      await adminClient
        .from("question_exposure_history")
        .upsert(exposureInserts, { onConflict: "student_id,question_id" });
    }

    // 6. Create Quiz Attempt record
    let attemptId = `att-${Date.now()}`;
    if (user) {
      const { data: attempt, error: attemptErr } = await supabase
        .from("quiz_attempts")
        .insert({
          student_id: studentId,
          subject_id: subjectId,
          topic_id: topicId,
          mode,
          total_questions: selectedQuestions.length,
          started_at: new Date().toISOString(),
        })
        .select("id")
        .single();

      if (!attemptErr && attempt) {
        attemptId = attempt.id;
      }
    }

    // 7. Security: Strip answer_index and explanation for Timed & Mock modes!
    const clientQuestions = selectedQuestions.map((q: any) => {
      // In practice mode, we can include explanation or allow immediate validation
      if (mode === "practice") {
        return {
          id: q.id,
          subject: q.subject || q.subject_id,
          topic: q.topic || q.topic_name,
          difficulty: q.difficulty,
          question: q.question,
          options: q.options,
          answerIndex: q.answer_index !== undefined ? q.answer_index : q.answerIndex,
          explanation: q.explanation,
          source: q.source,
        };
      } else {
        // SECURE STRIPPED QUESTION FOR TIMED/MOCK EXAMS
        return {
          id: q.id,
          subject: q.subject || q.subject_id,
          topic: q.topic || q.topic_name,
          difficulty: q.difficulty,
          question: q.question,
          options: q.options,
        };
      }
    });

    return NextResponse.json({
      attemptId,
      mode,
      totalQuestions: clientQuestions.length,
      questions: clientQuestions,
      startedAt: Date.now(),
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to start quiz" }, { status: 500 });
  }
}
