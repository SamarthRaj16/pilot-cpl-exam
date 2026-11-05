import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(request: NextRequest) {
  try {
    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      return NextResponse.json({ progress: [], isGuest: true });
    }

    const adminClient = createAdminClient();
    const { data, error } = await adminClient
      .from("student_syllabus_progress")
      .select("*")
      .eq("student_id", user.id);

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ progress: data || [], isGuest: false });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to load syllabus" }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      subject_name,
      topic_name,
      theory_completed,
      practice_completed,
      mock_completed,
      notes,
    } = body;

    if (!subject_name || !topic_name) {
      return NextResponse.json(
        { error: "subject_name and topic_name are required" },
        { status: 400 }
      );
    }

    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    const now = new Date().toISOString();

    if (!user) {
      // Guest response: client persists locally
      return NextResponse.json({
        success: true,
        isGuest: true,
        item: {
          subject_name,
          topic_name,
          theory_completed: !!theory_completed,
          practice_completed: !!practice_completed,
          mock_completed: !!mock_completed,
          notes: notes || null,
          updated_at: now,
        },
      });
    }

    const adminClient = createAdminClient();
    const { data, error } = await adminClient
      .from("student_syllabus_progress")
      .upsert(
        {
          student_id: user.id,
          subject_name,
          topic_name,
          theory_completed: !!theory_completed,
          practice_completed: !!practice_completed,
          mock_completed: !!mock_completed,
          notes: notes !== undefined ? notes : null,
          updated_at: now,
        },
        { onConflict: "student_id,subject_name,topic_name" }
      )
      .select()
      .single();

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ success: true, isGuest: false, item: data });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to update syllabus" }, { status: 500 });
  }
}

// Bulk sync endpoint for student login / migration
export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const { items } = body;

    if (!Array.isArray(items) || items.length === 0) {
      return NextResponse.json({ success: true, count: 0 });
    }

    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      return NextResponse.json({ success: true, isGuest: true, count: items.length });
    }

    const now = new Date().toISOString();
    const rows = items.map((it: any) => ({
      student_id: user.id,
      subject_name: it.subject_name,
      topic_name: it.topic_name,
      theory_completed: !!it.theory_completed,
      practice_completed: !!it.practice_completed,
      mock_completed: !!it.mock_completed,
      notes: it.notes || null,
      updated_at: now,
    }));

    const adminClient = createAdminClient();
    const { error } = await adminClient
      .from("student_syllabus_progress")
      .upsert(rows, { onConflict: "student_id,subject_name,topic_name" });

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({ success: true, isGuest: false, count: rows.length });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to bulk sync syllabus" }, { status: 500 });
  }
}

