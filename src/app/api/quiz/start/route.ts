import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";
import { createAdminClient } from "@/lib/supabase/admin";
import rawQuestions from "@/data/questions.json";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const {
      subjectId,
      subjectIds,
      topicId,
      topicIds,
      topics,
      mode = "practice",
      practiceMode = "smart", // 'smart' | 'fresh_only' | 'revision_only' | 'all_incorrect'
      questionCount = 50,
      clientMistakeIds = [], // Fallback/offline pending mistake IDs
      clientServedIds = [],  // Fallback/offline served IDs
    } = body;

    // Normalize set size: strictly enforce max 50 questions
    const requestedCount = Math.min(50, Math.max(10, Number(questionCount) || 50));

    // Normalize subjects and topics into arrays
    let targetSubjects: string[] = [];
    if (Array.isArray(subjectIds) && subjectIds.length > 0) {
      targetSubjects = subjectIds;
    } else if (typeof subjectIds === "string" && subjectIds.trim()) {
      targetSubjects = subjectIds.split(",").map((s) => s.trim());
    } else if (subjectId) {
      targetSubjects = [subjectId];
    }

    let targetTopics: string[] = [];
    if (Array.isArray(topicIds) && topicIds.length > 0) {
      targetTopics = topicIds;
    } else if (Array.isArray(topics) && topics.length > 0) {
      targetTopics = topics;
    } else if (typeof topicIds === "string" && topicIds.trim()) {
      targetTopics = topicIds.split(",").map((t) => t.trim());
    } else if (typeof topics === "string" && topics.trim()) {
      targetTopics = topics.split(",").map((t) => t.trim());
    } else if (topicId) {
      targetTopics = [topicId];
    }

    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    const studentId = user?.id || "demo-student-id";

    // 1 & 2. Concurrently Fetch Exposed Questions & Pending Revision Mistakes (Parallel DB IO)
    const exposedIds = new Set<string>(clientServedIds);
    const pendingRevisionMap = new Map<string, any>();
    if (Array.isArray(clientMistakeIds)) {
      clientMistakeIds.forEach((id: string) => {
        pendingRevisionMap.set(id, { question_id: id, incorrect_count: 1 });
      });
    }

    if (user) {
      const [exposureRes, mistakeRes] = await Promise.all([
        supabase
          .from("question_exposure_history")
          .select("question_id")
          .eq("student_id", studentId),
        supabase
          .from("student_mistakes")
          .select("question_id, incorrect_count, last_attempted_at, status")
          .eq("student_id", studentId)
          .in("status", ["unresolved", "pending_revision"]),
      ]);

      if (exposureRes.data) {
        exposureRes.data.forEach((e: any) => exposedIds.add(e.question_id));
      }

      if (mistakeRes.data) {
        mistakeRes.data.forEach((m: any) => {
          pendingRevisionMap.set(m.question_id, m);
        });
      }
    }

    // 3. Filter Master Question Pool by Selected Subjects & Topics
    const candidatePool = (rawQuestions as any[]).filter((q) => {
      if (practiceMode === "all_incorrect") return true;
      if (targetSubjects.length > 0 && !targetSubjects.includes(q.subject)) return false;
      if (targetTopics.length > 0 && !targetTopics.includes(q.topic)) return false;
      return true;
    });

    // Partition candidate questions into Pool A (Fresh) and Pool B (Revision)
    const poolBFreshPending: any[] = [];
    const poolAFreshUnserved: any[] = [];

    candidatePool.forEach((q) => {
      if (pendingRevisionMap.has(q.id)) {
        poolBFreshPending.push({
          ...q,
          isRevision: true,
          mistakeMeta: pendingRevisionMap.get(q.id),
        });
      } else if (!exposedIds.has(q.id)) {
        poolAFreshUnserved.push({
          ...q,
          isRevision: false,
        });
      }
    });

    // 4. Assemble Session Questions based on Practice Mode
    let finalSelectedQuestions: any[] = [];

    if (practiceMode === "revision_only" || practiceMode === "all_incorrect") {
      // Prioritize by incorrect count and oldest attempt
      poolBFreshPending.sort((a, b) => {
        const countA = a.mistakeMeta?.incorrect_count || 1;
        const countB = b.mistakeMeta?.incorrect_count || 1;
        return countB - countA;
      });
      finalSelectedQuestions = poolBFreshPending.slice(0, requestedCount);
    } else if (practiceMode === "fresh_only") {
      // Fresh unserved questions only
      const shuffledFresh = [...poolAFreshUnserved].sort(() => Math.random() - 0.5);
      finalSelectedQuestions = shuffledFresh.slice(0, requestedCount);
    } else {
      // "smart" mode (Default): combines revision questions + fresh questions
      // Limit revision questions to max 20 (or half of requested count)
      const maxRevisionSlots = Math.min(20, Math.floor(requestedCount * 0.4) || 5);
      
      poolBFreshPending.sort((a, b) => {
        const countA = a.mistakeMeta?.incorrect_count || 1;
        const countB = b.mistakeMeta?.incorrect_count || 1;
        return countB - countA;
      });

      const selectedRevision = poolBFreshPending.slice(0, maxRevisionSlots);
      const remainingSlots = requestedCount - selectedRevision.length;

      // Select fresh questions with balanced difficulty (~30% easy, ~50% med, ~20% hard)
      const easyFresh = poolAFreshUnserved.filter((q) => q.difficulty === "easy").sort(() => Math.random() - 0.5);
      const medFresh = poolAFreshUnserved.filter((q) => q.difficulty === "medium").sort(() => Math.random() - 0.5);
      const hardFresh = poolAFreshUnserved.filter((q) => q.difficulty === "hard").sort(() => Math.random() - 0.5);

      const targetEasy = Math.round(remainingSlots * 0.3);
      const targetMed = Math.round(remainingSlots * 0.5);
      const targetHard = remainingSlots - targetEasy - targetMed;

      const pickedFresh: any[] = [];
      pickedFresh.push(...easyFresh.slice(0, targetEasy));
      pickedFresh.push(...medFresh.slice(0, targetMed));
      pickedFresh.push(...hardFresh.slice(0, targetHard));

      // If not filled to remainingSlots, backfill from whatever fresh remains
      if (pickedFresh.length < remainingSlots) {
        const pickedSet = new Set(pickedFresh.map((q) => q.id));
        for (const q of poolAFreshUnserved) {
          if (!pickedSet.has(q.id)) {
            pickedFresh.push(q);
            if (pickedFresh.length >= remainingSlots) break;
          }
        }
      }

      finalSelectedQuestions = [...selectedRevision, ...pickedFresh];

      // If still under requestedCount and fresh pool was exhausted, can include more pending mistakes
      if (finalSelectedQuestions.length < requestedCount && poolBFreshPending.length > selectedRevision.length) {
        const additionalRevision = poolBFreshPending.slice(
          selectedRevision.length,
          selectedRevision.length + (requestedCount - finalSelectedQuestions.length)
        );
        finalSelectedQuestions.push(...additionalRevision);
      }
    }

    // 5. Check Availability / Pool Exhaustion
    let availabilityNotice = null;

    if (finalSelectedQuestions.length === 0) {
      return NextResponse.json(
        {
          status: "exhausted",
          message:
            "All fresh questions in the selected topic(s) have been completed and no pending revision questions remain.",
          totalCandidatePool: candidatePool.length,
          totalEligible: 0,
        },
        { status: 200 }
      );
    }

    if (finalSelectedQuestions.length < requestedCount) {
      availabilityNotice = `${finalSelectedQuestions.length} unique questions are currently available for your selected topics.`;
    }

    // Shuffle questions so revision questions are smoothly interleaved
    finalSelectedQuestions.sort(() => Math.random() - 0.5);

    // 6 & 7. Concurrently Record Question Exposure & Create Quiz Attempt (Parallel DB writes)
    let attemptId = `att-${Date.now()}`;
    if (user) {
      const adminClient = createAdminClient();
      const freshOnly = finalSelectedQuestions.filter((q) => !q.isRevision);
      const writeTasks: any[] = [];

      if (freshOnly.length > 0) {
        const exposureInserts = freshOnly.map((q: any) => ({
          student_id: studentId,
          question_id: q.id,
          subject_id: q.subject_id || q.subject,
          topic_id: q.topic_id || q.topic,
        }));

        writeTasks.push(
          adminClient
            .from("question_exposure_history")
            .upsert(exposureInserts, { onConflict: "student_id,question_id" })
        );
      }

      const primarySubject = targetSubjects.length > 0 ? targetSubjects.join(", ") : "Multi-Subject";
      const primaryTopic = targetTopics.length > 0 ? targetTopics.join(", ") : "Combined Practice";

      const attemptPromise = supabase
        .from("quiz_attempts")
        .insert({
          student_id: studentId,
          subject_id: primarySubject,
          topic_id: primaryTopic,
          mode,
          status: "in_progress",
          total_questions: finalSelectedQuestions.length,
          started_at: new Date().toISOString(),
        })
        .select("id")
        .single();

      writeTasks.push(attemptPromise);

      const results = await Promise.all(writeTasks);
      const attemptRes = results[results.length - 1];
      if (attemptRes && attemptRes.data?.id) {
        attemptId = attemptRes.data.id;
      }
    }

    // 8. Client Payload Sanitization
    const clientQuestions = finalSelectedQuestions.map((q: any) => {
      const base = {
        id: q.id,
        subject: q.subject || q.subject_id,
        topic: q.topic || q.topic_name,
        difficulty: q.difficulty,
        question: q.question,
        options: q.options,
        isRevision: Boolean(q.isRevision),
      };

      if (mode === "practice") {
        return {
          ...base,
          answerIndex: q.answer_index !== undefined ? q.answer_index : q.answerIndex,
          explanation: q.explanation,
          source: q.source,
        };
      } else {
        // Securely strip correct answer and explanation for Timed & Mock Exams
        return base;
      }
    });

    return NextResponse.json({
      attemptId,
      mode,
      practiceMode,
      totalQuestions: clientQuestions.length,
      requestedCount,
      availabilityNotice,
      poolA_freshAvailable: poolAFreshUnserved.length,
      poolB_revisionAvailable: poolBFreshPending.length,
      questions: clientQuestions,
      startedAt: Date.now(),
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to start quiz" }, { status: 500 });
  }
}
