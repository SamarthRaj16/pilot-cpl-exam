import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";
import { createAdminClient } from "@/lib/supabase/admin";
import rawQuestions from "@/data/questions.json";

// Helper to normalize text for duplicate detection
function normalizeText(text: string) {
  return (text || "").toLowerCase().replace(/[^a-z0-9]/g, "");
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const subject = searchParams.get("subject");
    const difficulty = searchParams.get("difficulty");
    const status = searchParams.get("status") || "approved";
    const search = searchParams.get("search")?.toLowerCase();
    const page = parseInt(searchParams.get("page") || "1");
    const limit = parseInt(searchParams.get("limit") || "20");

    let pool = rawQuestions;

    if (process.env.NEXT_PUBLIC_SUPABASE_URL) {
      const supabase = createAdminClient();
      let query = supabase.from("questions").select("*");
      if (subject) query = query.eq("subject_id", subject);
      if (difficulty) query = query.eq("difficulty", difficulty);
      if (status) query = query.eq("validation_status", status);

      const { data, error } = await query;
      if (!error && data && data.length > 0) {
        pool = data;
      }
    }

    let filtered = pool.filter((q: any) => {
      if (subject && q.subject !== subject && q.subject_id !== subject) return false;
      if (difficulty && q.difficulty !== difficulty) return false;
      if (search) {
        const textMatch = q.question.toLowerCase().includes(search);
        const idMatch = q.id.toLowerCase().includes(search);
        const topicMatch = (q.topic || q.topic_name || "").toLowerCase().includes(search);
        if (!textMatch && !idMatch && !topicMatch) return false;
      }
      return true;
    });

    const total = filtered.length;
    const startIndex = (page - 1) * limit;
    const paginated = filtered.slice(startIndex, startIndex + limit);

    return NextResponse.json({
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
      questions: paginated,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to fetch questions" }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    // Check admin permissions
    if (user) {
      const { data: profile } = await supabase
        .from("profiles")
        .select("role")
        .eq("id", user.id)
        .single();

      if (profile?.role !== "admin") {
        return NextResponse.json({ error: "Unauthorized. Admin role required." }, { status: 403 });
      }
    }

    const body = await request.json();
    const {
      subject,
      topic,
      difficulty = "medium",
      question,
      options,
      answerIndex,
      explanation,
      source,
    } = body;

    // Strict validation
    if (!subject || !topic || !question || !explanation || !source) {
      return NextResponse.json({ error: "Missing required question fields." }, { status: 400 });
    }
    if (!Array.isArray(options) || options.length !== 4) {
      return NextResponse.json({ error: "Options must be an array of exactly 4 strings." }, { status: 400 });
    }
    if (typeof answerIndex !== "number" || answerIndex < 0 || answerIndex > 3) {
      return NextResponse.json({ error: "answerIndex must be an integer between 0 and 3." }, { status: 400 });
    }

    // Duplicate Check against active database
    const norm = normalizeText(question);
    const isDup = rawQuestions.some((q: any) => normalizeText(q.question) === norm);
    if (isDup) {
      return NextResponse.json(
        { error: "Duplicate question detected. This question already exists in the question bank." },
        { status: 409 }
      );
    }

    // Generate permanent ID
    const prefixMap: Record<string, string> = {
      "Air Navigation": "NAV",
      "Air Regulations": "REG",
      "Aviation Meteorology": "MET",
      "Technical General": "TG",
      "Technical Specific": "TS",
      RTR: "RTR",
    };
    const prefix = prefixMap[subject] || "CPL";
    const newId = `${prefix}-${Date.now().toString().slice(-4)}`;

    const newQuestion = {
      id: newId,
      subject_id: subject.toLowerCase().replace(/[^a-z0-9]/g, "-"),
      topic_id: topic.toLowerCase().replace(/[^a-z0-9]/g, "-"),
      topic_name: topic,
      difficulty,
      question,
      options,
      answer_index: answerIndex,
      explanation,
      source,
      validation_status: "approved",
    };

    if (process.env.NEXT_PUBLIC_SUPABASE_URL) {
      const adminClient = createAdminClient();
      await adminClient.from("questions").insert(newQuestion);
    }

    return NextResponse.json({
      success: true,
      message: `Question ${newId} created and approved successfully.`,
      question: newQuestion,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to create question" }, { status: 500 });
  }
}
