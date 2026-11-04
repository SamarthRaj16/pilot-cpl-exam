import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { subjectId, topicId } = body;

    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      return NextResponse.json({ message: "Guest rotation reset" }, { status: 200 });
    }

    let query = supabase
      .from("question_exposure_history")
      .delete()
      .eq("student_id", user.id);

    if (subjectId) query = query.eq("subject_id", subjectId);
    if (topicId) query = query.eq("topic_id", topicId);

    const { error } = await query;
    if (error) {
      return NextResponse.json({ error: error.message }, { status: 400 });
    }

    return NextResponse.json({
      success: true,
      message: `Zero-repeat question exposure history reset for ${
        topicId ? `topic ${topicId}` : subjectId ? `subject ${subjectId}` : "all subjects"
      }. Score history preserved.`,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to reset rotation pool" }, { status: 500 });
  }
}

