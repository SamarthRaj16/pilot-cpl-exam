import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { full_name, study_preferences } = body;

    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      return NextResponse.json({ error: "Unauthorized. Please sign in." }, { status: 401 });
    }

    const adminClient = createAdminClient();
    const now = new Date().toISOString();

    // 1. Update profiles table using admin privileges (immune to grant/RLS permission issues)
    const { data: updatedProfile, error: profileError } = await adminClient
      .from("profiles")
      .update({
        full_name: full_name?.trim() || "Cadet Pilot",
        study_preferences: study_preferences || {},
        updated_at: now,
      })
      .eq("id", user.id)
      .select()
      .single();

    if (profileError) {
      return NextResponse.json({ error: profileError.message }, { status: 500 });
    }

    // 2. Also sync name with Supabase Auth metadata
    try {
      await adminClient.auth.admin.updateUserById(user.id, {
        user_metadata: { full_name: full_name?.trim() || "Cadet Pilot" },
      });
    } catch {}

    return NextResponse.json({
      success: true,
      profile: updatedProfile,
    });
  } catch (err: any) {
    return NextResponse.json(
      { error: err.message || "Failed to update profile." },
      { status: 500 }
    );
  }
}
