import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";
import { createAdminClient } from "@/lib/supabase/admin";
import rawQuestions from "@/data/questions.json";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { attemptId, answers = {}, durationSeconds = 0 } = body;

    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    const studentId = user?.id || "demo-student-id";

    // Fast in-memory lookup map from master bank (0ms latency)
    const qMap = new Map<string, any>();
    rawQuestions.forEach((q: any) => qMap.set(q.id, q));

    const questionIds = Object.keys(answers);
    const totalQuestions = questionIds.length;

    // Only query database questions if any question is missing from local bank
    const missingIds = questionIds.filter((id) => !qMap.has(id));
    if (missingIds.length > 0 && process.env.NEXT_PUBLIC_SUPABASE_URL) {
      try {
        const { data: dbQs } = await supabase
          .from("questions")
          .select("*")
          .in("id", missingIds);

        if (dbQs) {
          dbQs.forEach((q: any) => qMap.set(q.id, q));
        }
      } catch {}
    }

    let score = 0;
    const reviewItems: any[] = [];
    const studentAnswerInserts: any[] = [];
    const mistakeUpserts: any[] = [];
    const spacedRepetitionUpdates: any[] = [];

    const now = new Date().toISOString();

    for (const qId of questionIds) {
      const q = qMap.get(qId);
      if (!q) continue;

      const studentChoice = answers[qId] !== undefined ? answers[qId] : -1;
      const correctChoice = q.answer_index !== undefined ? q.answer_index : q.answerIndex;
      const isCorrect = studentChoice === correctChoice && studentChoice >= 0;
      const pointsAwarded = isCorrect ? 1 : 0;

      if (isCorrect) score += 1;

      // Authoritative Review Item (Revealed strictly post-submission)
      reviewItems.push({
        questionId: q.id,
        subject: q.subject || q.subject_id,
        topic: q.topic || q.topic_name,
        difficulty: q.difficulty,
        question: q.question,
        options: q.options,
        studentChoice,
        correctChoice,
        isCorrect,
        pointsAwarded,
        explanation: q.explanation,
        source: q.source,
      });

      if (user) {
        studentAnswerInserts.push({
          attempt_id: attemptId,
          student_id: studentId,
          question_id: q.id,
          selected_answer: studentChoice,
          is_correct: isCorrect,
          points_awarded: pointsAwarded,
          answered_at: now,
        });

        if (!isCorrect) {
          // Log into Mistake Notebook
          mistakeUpserts.push({
            student_id: studentId,
            question_id: q.id,
            subject_id: q.subject_id || q.subject,
            topic_id: q.topic_id || q.topic,
            status: "unresolved",
            last_incorrect_choice: studentChoice,
            last_attempted_at: now,
          });

          // Reset Spaced Repetition interval to 1 day
          spacedRepetitionUpdates.push({
            student_id: studentId,
            question_id: q.id,
            subject_id: q.subject_id || q.subject,
            interval_days: 1,
            next_review_date: new Date(Date.now() + 86400000).toISOString().split("T")[0],
            last_reviewed_at: now,
          });
        } else {
          // Advance Spaced Repetition interval
          spacedRepetitionUpdates.push({
            student_id: studentId,
            question_id: q.id,
            subject_id: q.subject_id || q.subject,
            interval_days: 7,
            next_review_date: new Date(Date.now() + 7 * 86400000).toISOString().split("T")[0],
            last_reviewed_at: now,
          });
        }
      }
    }

    const accuracy = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;
    const passed = accuracy >= 70; // DGCA 70% requirement
    let recoveredInThisSession = 0;

    // Persist to Supabase if authenticated using parallel batch operations
    if (user) {
      const adminClient = createAdminClient();

      // Fetch existing mistakes in one fast indexed query
      const { data: existingMistakes } = await adminClient
        .from("student_mistakes")
        .select("question_id, status, incorrect_count")
        .eq("student_id", studentId)
        .in("status", ["unresolved", "pending_revision"]);

      const existingMistakeMap = new Map();
      if (existingMistakes) {
        existingMistakes.forEach((m) => existingMistakeMap.set(m.question_id, m));
      }

      const resolvedMistakeQIds: string[] = [];
      const newStudentMistakesToUpsert: any[] = [];

      for (const qId of questionIds) {
        const studentChoice = answers[qId] !== undefined ? answers[qId] : -1;
        const q = qMap.get(qId);
        if (!q) continue;
        const correctChoice = q.answer_index !== undefined ? q.answer_index : q.answerIndex;
        const isCorrect = studentChoice === correctChoice && studentChoice >= 0;

        if (isCorrect && existingMistakeMap.has(qId)) {
          recoveredInThisSession += 1;
          resolvedMistakeQIds.push(qId);
        } else if (!isCorrect) {
          const prev = existingMistakeMap.get(qId);
          const incCount = prev ? (prev.incorrect_count || 1) + 1 : 1;
          newStudentMistakesToUpsert.push({
            student_id: studentId,
            question_id: qId,
            subject_id: q.subject || q.subject_id,
            topic_id: q.topic || q.topic_name,
            status: "pending_revision",
            incorrect_count: incCount,
            last_incorrect_choice: studentChoice,
            authoritative_answer: correctChoice,
            last_attempted_at: now,
          });
        }
      }

      // Execute ALL database write operations simultaneously in parallel
      const dbPromises: Promise<any>[] = [
        adminClient
          .from("quiz_attempts")
          .update({
            score,
            accuracy,
            passed,
            duration_seconds: durationSeconds,
            completed_at: now,
          })
          .eq("id", attemptId),
      ];

      if (studentAnswerInserts.length > 0) {
        dbPromises.push(adminClient.from("student_answers").insert(studentAnswerInserts));
      }

      if (mistakeUpserts.length > 0) {
        dbPromises.push(
          adminClient
            .from("mistake_notebook")
            .upsert(mistakeUpserts, { onConflict: "student_id,question_id" })
        );
      }

      if (spacedRepetitionUpdates.length > 0) {
        dbPromises.push(
          adminClient
            .from("spaced_repetition")
            .upsert(spacedRepetitionUpdates, { onConflict: "student_id,question_id" })
        );
      }

      if (resolvedMistakeQIds.length > 0) {
        dbPromises.push(
          adminClient
            .from("student_mistakes")
            .update({
              status: "resolved",
              recovered_at: now,
            })
            .eq("student_id", studentId)
            .in("question_id", resolvedMistakeQIds)
        );
      }

      if (newStudentMistakesToUpsert.length > 0) {
        dbPromises.push(
          adminClient
            .from("student_mistakes")
            .upsert(newStudentMistakesToUpsert, { onConflict: "student_id,question_id" })
        );
      }

      // Wait for all writes in parallel (drops submission time from 15s to ~300ms)
      await Promise.all(dbPromises);

      // Finally, update profile points and recovered questions in background
      try {
        const { data: profile } = await adminClient
          .from("profiles")
          .select("total_points, recovered_questions")
          .eq("id", studentId)
          .single();

        const currentPoints = profile?.total_points || 0;
        const currentRecovered = profile?.recovered_questions || 0;
        await adminClient
          .from("profiles")
          .update({
            total_points: currentPoints + score,
            recovered_questions: currentRecovered + recoveredInThisSession,
            last_active_at: now,
          })
          .eq("id", studentId);
      } catch {}
    }

    return NextResponse.json({
      attemptId,
      score,
      totalQuestions,
      accuracy,
      passed,
      durationSeconds,
      passMark: 70,
      recoveredCount: recoveredInThisSession,
      reviewItems,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to calculate results" }, { status: 500 });
  }
}
