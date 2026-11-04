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

    // Build question lookup map from master bank
    const qMap = new Map<string, any>();
    rawQuestions.forEach((q: any) => qMap.set(q.id, q));

    // Also query database questions if connected
    if (process.env.NEXT_PUBLIC_SUPABASE_URL) {
      const qIds = Object.keys(answers);
      if (qIds.length > 0) {
        const { data: dbQs } = await supabase
          .from("questions")
          .select("*")
          .in("id", qIds);

        if (dbQs) {
          dbQs.forEach((q: any) => qMap.set(q.id, q));
        }
      }
    }

    let score = 0;
    const questionIds = Object.keys(answers);
    const totalQuestions = questionIds.length;

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

    // Persist to Supabase if authenticated
    if (user) {
      const adminClient = createAdminClient();

      // Update Attempt
      await adminClient
        .from("quiz_attempts")
        .update({
          score,
          accuracy,
          passed,
          duration_seconds: durationSeconds,
          completed_at: now,
        })
        .eq("id", attemptId);

      // Insert Student Answers
      if (studentAnswerInserts.length > 0) {
        await adminClient.from("student_answers").insert(studentAnswerInserts);
      }

      // Upsert Mistake Notebook
      if (mistakeUpserts.length > 0) {
        await adminClient
          .from("mistake_notebook")
          .upsert(mistakeUpserts, { onConflict: "student_id,question_id" });
      }

      // Upsert Spaced Repetition
      if (spacedRepetitionUpdates.length > 0) {
        await adminClient
          .from("spaced_repetition")
          .upsert(spacedRepetitionUpdates, { onConflict: "student_id,question_id" });
      }

      // Update student points in Profile
      const { data: profile } = await adminClient
        .from("profiles")
        .select("total_points")
        .eq("id", studentId)
        .single();

      const currentPoints = profile?.total_points || 0;
      await adminClient
        .from("profiles")
        .update({
          total_points: currentPoints + score,
          last_active_at: now,
        })
        .eq("id", studentId);
    }

    return NextResponse.json({
      attemptId,
      score,
      totalQuestions,
      accuracy,
      passed,
      durationSeconds,
      passMark: 70,
      reviewItems,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to calculate results" }, { status: 500 });
  }
}
