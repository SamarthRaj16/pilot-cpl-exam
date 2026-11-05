import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      attemptId,
      questionId,
      selectedAnswer,
      timeRemaining,
      mode = "practice",
    } = body;

    if (!attemptId || !questionId) {
      return NextResponse.json({ error: "Missing attemptId or questionId" }, { status: 400 });
    }

    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    // For offline/guest students, acknowledge save
    if (!user) {
      return NextResponse.json({
        success: true,
        savedLocally: true,
        timestamp: new Date().toISOString(),
      });
    }

    const studentId = user.id;
    const adminClient = createAdminClient();
    const now = new Date().toISOString();

    // 1. Upsert into student_answers for real-time recovery
    const answerUpsert = adminClient
      .from("student_answers")
      .upsert(
        {
          attempt_id: attemptId,
          student_id: studentId,
          question_id: questionId,
          selected_answer: selectedAnswer,
          answered_at: now,
        },
        { onConflict: "attempt_id,question_id" }
      );

    // 2. Touch quiz_attempts to update last_saved_at
    const attemptTouch = adminClient
      .from("quiz_attempts")
      .update({
        last_saved_at: now,
      })
      .eq("id", attemptId);

    await Promise.all([answerUpsert, attemptTouch]);

    return NextResponse.json({
      success: true,
      savedAt: now,
      attemptId,
      questionId,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to auto-save answer" },
      { status: 500 }
    );
  }
}

