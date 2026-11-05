"use client";

export const dynamic = "force-dynamic";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";

export default function ProfilePage() {
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [profile, setProfile] = useState<any>({
    full_name: "Cadet Pilot",
    email: "",
    role: "student",
    total_points: 0,
    recovered_questions: 0,
    study_streak: 1,
    created_at: "",
  });

  const [preferences, setPreferences] = useState({
    target_exam_date: "",
    daily_goal_questions: 30,
    preferred_mode: "practice",
  });

  // Password change state
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passLoading, setPassLoading] = useState(false);
  const [passMsg, setPassMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // Status feedback
  const [statusMsg, setStatusMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);

  // Guest data migration check
  const [hasGuestData, setHasGuestData] = useState(false);
  const [migrating, setMigrating] = useState(false);
  const [guestCounts, setGuestCounts] = useState({ served: 0, mistakes: 0, syllabus: 0 });

  useEffect(() => {
    async function loadProfile() {
      try {
        const supabase = createClient();
        const {
          data: { user: authUser },
        } = await supabase.auth.getUser();

        if (authUser) {
          setUser(authUser);
          const { data: dbProfile } = await supabase
            .from("profiles")
            .select("*")
            .eq("id", authUser.id)
            .single();

          if (dbProfile) {
            setProfile(dbProfile);
            if (dbProfile.study_preferences) {
              setPreferences({
                target_exam_date: dbProfile.study_preferences.target_exam_date || "",
                daily_goal_questions: dbProfile.study_preferences.daily_goal_questions || 30,
                preferred_mode: dbProfile.study_preferences.preferred_mode || "practice",
              });
            }
          }
        }
      } catch (err) {
        console.error("Error loading user profile:", err);
      } finally {
        setLoading(false);
      }
    }
    loadProfile();

    // Check for local guest data
    try {
      const served = localStorage.getItem("cpl_served_ids");
      const mistakes = localStorage.getItem("cpl_mistakes");
      const syllabus = localStorage.getItem("cpl_syllabus_progress");
      const servedCount = served ? JSON.parse(served).length : 0;
      const mistakesCount = mistakes ? Object.keys(JSON.parse(mistakes)).length : 0;
      const syllabusCount = syllabus ? Object.keys(JSON.parse(syllabus)).length : 0;

      if (servedCount > 0 || mistakesCount > 0 || syllabusCount > 0) {
        setHasGuestData(true);
        setGuestCounts({ served: servedCount, mistakes: mistakesCount, syllabus: syllabusCount });
      }
    } catch {}
  }, []);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;
    setSaving(true);
    setStatusMsg(null);

    try {
      const supabase = createClient();
      const { error } = await supabase
        .from("profiles")
        .update({
          full_name: profile.full_name,
          study_preferences: preferences,
          updated_at: new Date().toISOString(),
        })
        .eq("id", user.id);

      if (error) throw error;
      setStatusMsg({ type: "success", text: "Profile & study preferences updated successfully!" });
    } catch (err: any) {
      setStatusMsg({ type: "error", text: err.message || "Failed to update profile." });
    } finally {
      setSaving(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPassLoading(true);
    setPassMsg(null);

    if (newPassword.length < 8) {
      setPassMsg({ type: "error", text: "Password must be at least 8 characters long." });
      setPassLoading(false);
      return;
    }

    if (newPassword !== confirmPassword) {
      setPassMsg({ type: "error", text: "Passwords do not match." });
      setPassLoading(false);
      return;
    }

    try {
      const supabase = createClient();
      const { error } = await supabase.auth.updateUser({ password: newPassword });
      if (error) throw error;
      setPassMsg({ type: "success", text: "Password changed successfully!" });
      setNewPassword("");
      setConfirmPassword("");
    } catch (err: any) {
      setPassMsg({ type: "error", text: err.message || "Failed to change password." });
    } finally {
      setPassLoading(false);
    }
  };

  const handleMigrateGuestData = async () => {
    if (!user || !user.id) return;
    const studentId = user.id;
    setMigrating(true);
    try {
      const supabase = createClient();

      // 1. Sync Exposure
      const served = localStorage.getItem("cpl_served_ids");
      if (served) {
        const ids: string[] = JSON.parse(served);
        if (ids.length > 0) {
          const rows = ids.map((qid) => ({
            student_id: studentId,
            question_id: qid,
            subject_id: "Air Navigation",
            topic_id: "General",
          }));
          await supabase.from("question_exposure_history").upsert(rows, { onConflict: "student_id,question_id" });
        }
      }

      // 2. Sync Syllabus
      const syllabus = localStorage.getItem("cpl_syllabus_progress");
      if (syllabus) {
        const dict = JSON.parse(syllabus);
        const rows = Object.values(dict).map((item: any) => ({
          student_id: studentId,
          subject_name: item.subject_name,
          topic_name: item.topic_name,
          theory_completed: item.theory_completed || false,
          practice_completed: item.practice_completed || false,
          mock_completed: item.mock_completed || false,
          notes: item.notes || null,
        }));
        if (rows.length > 0) {
          await supabase.from("student_syllabus_progress").upsert(rows, { onConflict: "student_id,subject_name,topic_name" });
        }
      }

      setHasGuestData(false);
      setStatusMsg({ type: "success", text: "Guest learning progress safely synchronized to your account!" });
    } catch (err: any) {
      setStatusMsg({ type: "error", text: err.message || "Failed to migrate guest data." });
    } finally {
      setMigrating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[400px] flex items-center justify-center text-xs font-bold text-text-muted">
        Loading pilot credentials...
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="pb-4 border-b border-border-charcoal flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-black text-text-primary tracking-tight flex items-center gap-2">
            <span>🛡️</span>
            <span>Pilot Profile &amp; Flight Records</span>
          </h1>
          <p className="text-xs sm:text-sm text-text-secondary mt-0.5">
            Manage your student credentials, study preferences, and cross-device synchronization
          </p>
        </div>
      </div>

      {statusMsg && (
        <div
          className={`p-4 rounded-xl text-xs font-bold ${
            statusMsg.type === "success"
              ? "bg-brand-teal/15 text-brand-teal border border-brand-teal/30"
              : "bg-brand-red/15 text-brand-red border border-brand-red/30"
          }`}
        >
          {statusMsg.text}
        </div>
      )}

      {/* Guest Data Migration Card */}
      {hasGuestData && (
        <div className="p-5 rounded-2xl bg-card-primary border-l-4 border-l-brand-gold border border-border-charcoal shadow-card flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="text-xs font-extrabold uppercase tracking-wider text-brand-gold">
              Guest Progress Detected on this Device
            </div>
            <div className="text-sm font-bold text-text-primary">
              Link Your Local Flight Logs to this Account
            </div>
            <div className="text-xs text-text-secondary">
              Found {guestCounts.served} seen questions and {guestCounts.syllabus} syllabus checklist items. Synchronize them permanently to your account cloud profile.
            </div>
          </div>

          <button
            onClick={handleMigrateGuestData}
            disabled={migrating}
            className="shrink-0 px-4 py-2.5 rounded-xl bg-brand-gold text-bg-main font-bold text-xs shadow-sm hover:scale-[1.02] transition-all"
          >
            {migrating ? "Syncing..." : "Sync Guest Data Now →"}
          </button>
        </div>
      )}

      {/* Main Profile Info Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Left Column: Avatar & Summary */}
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-5 text-center flex flex-col items-center">
          <div className="w-24 h-24 rounded-2xl bg-card-elevated border-2 border-brand-blue flex items-center justify-center text-4xl shadow-glow">
            👨‍✈️
          </div>

          <div>
            <h2 className="text-lg font-black text-text-primary">{profile.full_name}</h2>
            <p className="text-xs text-text-muted mt-0.5">{profile.email || user?.email || "Cadet Pilot"}</p>
            <div className="mt-2 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-brand-blue/15 text-brand-blue border border-brand-blue/30 text-[10px] font-extrabold uppercase tracking-wider">
              <span>✈️</span>
              <span>{profile.role === "admin" ? "Flight Examiner / Admin" : "Student Pilot (CPL)"}</span>
            </div>
          </div>

          <div className="w-full pt-4 border-t border-border-charcoal space-y-2.5 text-xs text-left">
            <div className="flex justify-between">
              <span className="text-text-muted">Total Points:</span>
              <span className="font-bold text-brand-gold">⭐ {profile.total_points || 0} pts</span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-muted">Recovered Questions:</span>
              <span className="font-bold text-brand-teal">✓ {profile.recovered_questions || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-muted">Study Streak:</span>
              <span className="font-bold text-brand-blue">🔥 {profile.study_streak || 1} days</span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-muted">Account Registered:</span>
              <span className="font-bold text-text-secondary">
                {profile.created_at ? new Date(profile.created_at).toLocaleDateString("en-IN", { month: "short", year: "numeric" }) : "Active"}
              </span>
            </div>
          </div>
        </div>

        {/* Right Column: Editable Details & Study Preferences */}
        <div className="md:col-span-2 space-y-6">
          <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-5">
            <h2 className="text-base font-bold text-text-primary border-b border-border-charcoal pb-3">
              Pilot Credentials &amp; Study Configuration
            </h2>

            <form onSubmit={handleUpdateProfile} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
                  Full Name (as per DGCA Pariksha)
                </label>
                <input
                  type="text"
                  required
                  value={profile.full_name}
                  onChange={(e) => setProfile({ ...profile, full_name: e.target.value })}
                  className="w-full px-4 py-2.5 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary text-xs focus:outline-none focus:border-brand-blue"
                />
              </div>

              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
                  Email Address
                </label>
                <input
                  type="email"
                  disabled
                  value={profile.email || user?.email || ""}
                  className="w-full px-4 py-2.5 rounded-xl bg-card-elevated/50 border border-border-charcoal text-text-muted text-xs cursor-not-allowed"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
                    Target DGCA Exam Date
                  </label>
                  <input
                    type="date"
                    value={preferences.target_exam_date}
                    onChange={(e) => setPreferences({ ...preferences, target_exam_date: e.target.value })}
                    className="w-full px-4 py-2.5 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary text-xs focus:outline-none focus:border-brand-blue"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
                    Daily Question Target
                  </label>
                  <select
                    value={preferences.daily_goal_questions}
                    onChange={(e) => setPreferences({ ...preferences, daily_goal_questions: Number(e.target.value) })}
                    className="w-full px-4 py-2.5 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary text-xs focus:outline-none focus:border-brand-blue"
                  >
                    <option value={10}>10 Questions / day</option>
                    <option value={20}>20 Questions / day</option>
                    <option value={30}>30 Questions / day (Standard)</option>
                    <option value={50}>50 Questions / day (Intensive)</option>
                  </select>
                </div>
              </div>

              <button
                type="submit"
                disabled={saving}
                className="px-6 py-2.5 rounded-xl bg-brand-blue hover:bg-brand-skyDark text-bg-main font-bold text-xs shadow-sm transition-all"
              >
                {saving ? "Saving Changes..." : "Save Preferences"}
              </button>
            </form>
          </div>

          {/* Change Password Card */}
          <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-4">
            <h2 className="text-base font-bold text-text-primary border-b border-border-charcoal pb-3">
              Change Security Password
            </h2>

            {passMsg && (
              <div
                className={`p-3 rounded-xl text-xs font-bold ${
                  passMsg.type === "success"
                    ? "bg-brand-teal/15 text-brand-teal border border-brand-teal/30"
                    : "bg-brand-red/15 text-brand-red border border-brand-red/30"
                }`}
              >
                {passMsg.text}
              </div>
            )}

            <form onSubmit={handleChangePassword} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
                    New Password
                  </label>
                  <input
                    type="password"
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full px-4 py-2.5 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary text-xs focus:outline-none focus:border-brand-blue"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1.5">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full px-4 py-2.5 rounded-xl bg-card-elevated border border-border-charcoal text-text-primary text-xs focus:outline-none focus:border-brand-blue"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={passLoading}
                className="px-5 py-2.5 rounded-xl bg-surface-interactive hover:bg-surface-hover text-text-primary font-bold text-xs border border-border-charcoal transition-all"
              >
                {passLoading ? "Updating..." : "Update Security Password"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

