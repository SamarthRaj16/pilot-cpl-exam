import { NextRequest, NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";
import rawQuestions from "@/data/questions.json";

export async function GET(request: NextRequest) {
  try {
    const supabase = createServerSupabaseClient();
    const {
      data: { user },
    } = await supabase.auth.getUser();

    const studentId = user?.id;

    // Subjects in DGCA CPL
    const SUBJECTS = [
      "Air Navigation",
      "Air Regulations",
      "Aviation Meteorology",
      "Technical General",
      "Technical Specific",
      "RTR",
    ];

    let attempts: any[] = [];
    let answers: any[] = [];

    if (user && process.env.NEXT_PUBLIC_SUPABASE_URL) {
      const { data: attData } = await supabase
        .from("quiz_attempts")
        .select("*")
        .eq("student_id", studentId);
      if (attData) attempts = attData;

      const { data: ansData } = await supabase
        .from("student_answers")
        .select("*")
        .eq("student_id", studentId);
      if (ansData) answers = ansData;
    }

    const subjectStats: Record<string, any> = {};

    let totalScoreSum = 0;
    let validSubjectCount = 0;
    let weakestSubj = "";
    let minPct = 101;
    let strongestSubj = "";
    let maxPct = -1;

    for (const subj of SUBJECTS) {
      const subjQuestions = rawQuestions.filter((q: any) => q.subject === subj);
      const totalInBank = subjQuestions.length;

      // Filter answers for this subject
      const qIds = new Set(subjQuestions.map((q: any) => q.id));
      const subjAnswers = answers.filter((a: any) => qIds.has(a.question_id));
      const attempted = subjAnswers.length;
      const correct = subjAnswers.filter((a: any) => a.is_correct).length;

      const accuracy = attempted > 0 ? Math.round((correct / attempted) * 100) : 0;
      const coverage = totalInBank > 0 ? Math.round((attempted / totalInBank) * 100) : 0;

      let status = "INSUFFICIENT DATA";
      if (attempted >= 15) {
        if (accuracy >= 70) {
          status = "PASS READY";
        } else if (accuracy >= 50) {
          status = "NEEDS FOCUS";
        } else {
          status = "CRITICAL";
        }

        totalScoreSum += accuracy;
        validSubjectCount += 1;

        if (accuracy < minPct) {
          minPct = accuracy;
          weakestSubj = subj;
        }
        if (accuracy > maxPct) {
          maxPct = accuracy;
          strongestSubj = subj;
        }
      }

      subjectStats[subj] = {
        score: accuracy,
        attempted,
        correct,
        totalInBank,
        accuracy,
        coverage,
        status,
      };
    }

    const overallScore =
      validSubjectCount > 0 ? Math.round(totalScoreSum / validSubjectCount) : 0;

    let overallStatus: "Exam Ready" | "Developing" | "Action Needed" | "Insufficient Data" =
      "Insufficient Data";

    if (validSubjectCount >= 4) {
      if (overallScore >= 70) overallStatus = "Exam Ready";
      else if (overallScore >= 50) overallStatus = "Developing";
      else overallStatus = "Action Needed";
    }

    const recommendedActions: string[] = [];
    if (weakestSubj) {
      recommendedActions.push(
        `Focus intensive practice on ${weakestSubj} (currently ${minPct}%, below the 70% DGCA passing threshold).`
      );
    }
    recommendedActions.push(
      "Complete at least 2 full-length Timed Mock Examinations per week to build speed and accuracy."
    );
    recommendedActions.push(
      "Review mistakes in your Mistake Notebook daily before beginning new question sets."
    );

    return NextResponse.json({
      overallScore,
      status: overallStatus,
      subjectScores: subjectStats,
      weakestSubject: weakestSubj || "None identified yet",
      strongestSubject: strongestSubj || "None identified yet",
      recommendedActions,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Failed to calculate readiness" }, { status: 500 });
  }
}
