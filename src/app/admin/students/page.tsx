"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";

interface Student {
  id: string;
  email: string;
  full_name: string;
  role: string;
  account_status: string;
  study_streak?: number;
  total_points?: number;
  recovered_questions?: number;
  last_active_at?: string;
  created_at: string;
  suspended_at?: string;
  suspended_reason?: string;
  quizAttemptsCount?: number;
  syllabusCompletion?: number;
}

export default function AdminStudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<"all" | "active" | "suspended">("all");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  // Selected student for Profile Overview Modal
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);

  // Status Change Confirmation Modal
  const [pendingAction, setPendingAction] = useState<{
    student: Student;
    action: "activate" | "suspend";
    reason?: string;
  } | null>(null);
  const [actionReason, setActionReason] = useState("");
  const [actionLoading, setActionLoading] = useState(false);

  const fetchStudents = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        search,
        status: statusFilter,
        page: String(page),
        limit: "15",
      });
      const res = await fetch(`/api/admin/students?${params.toString()}`);
      const data = await res.json();
      if (data.students) {
        setStudents(data.students);
        setTotalPages(data.totalPages || 1);
        setTotalCount(data.totalCount || 0);
      }
    } catch {
      // Offline fallback
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, [search, statusFilter, page]);

  const handleConfirmAction = async () => {
    if (!pendingAction) return;
    setActionLoading(true);
    try {
      const res = await fetch("/api/admin/students", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          studentId: pendingAction.student.id,
          action: pendingAction.action,
          reason: actionReason || "Administrative policy update",
        }),
      });

      if (res.ok) {
        // Refresh local student list
        setStudents((prev) =>
          prev.map((s) =>
            s.id === pendingAction.student.id
              ? {
                  ...s,
                  account_status: pendingAction.action === "activate" ? "active" : "suspended",
                  suspended_reason:
                    pendingAction.action === "suspend" ? actionReason : undefined,
                }
              : s
          )
        );
        if (selectedStudent?.id === pendingAction.student.id) {
          setSelectedStudent((prev) =>
            prev
              ? {
                  ...prev,
                  account_status: pendingAction.action === "activate" ? "active" : "suspended",
                  suspended_reason:
                    pendingAction.action === "suspend" ? actionReason : undefined,
                }
              : null
          );
        }
      }
    } catch {
      // Ignored
    } finally {
      setActionLoading(false);
      setPendingAction(null);
      setActionReason("");
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <span>👨‍✈️</span> Student Account Management (Feature E3)
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Oversee pilot registrations, account states, flight records, and exam attempts
          </p>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs font-bold text-brand-gold bg-brand-gold/10 px-3 py-1.5 rounded-xl border border-brand-gold/30">
            Total Pilots: {totalCount}
          </span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl p-4 shadow-card flex flex-col md:flex-row gap-4 items-stretch md:items-center justify-between">
        {/* Search Input */}
        <div className="relative flex-1">
          <input
            type="text"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search by student name or email..."
            className="w-full bg-surface-primary border border-border-charcoal rounded-xl px-4 py-2 text-xs text-white placeholder-text-muted focus:outline-none focus:border-brand-gold"
          />
          {search && (
            <button
              onClick={() => setSearch("")}
              className="absolute right-3 top-2.5 text-xs text-text-muted hover:text-white"
            >
              ✕
            </button>
          )}
        </div>

        {/* Status Filter Tabs */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-surface-primary border border-border-charcoal self-start md:self-auto">
          {(["all", "active", "suspended"] as const).map((st) => (
            <button
              key={st}
              onClick={() => {
                setStatusFilter(st);
                setPage(1);
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold capitalize transition-all ${
                statusFilter === st
                  ? "bg-brand-gold text-bg-base shadow-sm font-black"
                  : "text-text-muted hover:text-white"
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {/* Student Table */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl shadow-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-border-charcoal bg-surface-primary text-[10px] uppercase font-black tracking-wider text-text-muted">
                <th className="py-3 px-4">Pilot Name</th>
                <th className="py-3 px-4">Email</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Registered</th>
                <th className="py-3 px-4">Last Active</th>
                <th className="py-3 px-4">Points</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-charcoal/60">
              {loading ? (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-text-muted">
                    Loading student records...
                  </td>
                </tr>
              ) : students.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-8 text-center text-text-muted">
                    No student records found matching filter criteria.
                  </td>
                </tr>
              ) : (
                students.map((student) => {
                  const isActive = student.account_status === "active";
                  return (
                    <tr
                      key={student.id}
                      className="hover:bg-surface-interactive/40 transition-colors"
                    >
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2.5">
                          <div className="w-7 h-7 rounded-lg bg-surface-interactive flex items-center justify-center font-bold text-white text-[11px] border border-border-charcoal">
                            {student.full_name?.charAt(0) || "P"}
                          </div>
                          <span className="font-bold text-white">{student.full_name}</span>
                        </div>
                      </td>

                      <td className="py-3 px-4 text-text-secondary font-mono">
                        {student.email}
                      </td>

                      <td className="py-3 px-4">
                        <span
                          className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider ${
                            isActive
                              ? "bg-brand-green/20 text-brand-green border border-brand-green/30"
                              : "bg-brand-red/20 text-brand-red border border-brand-red/30"
                          }`}
                        >
                          <span
                            className={`w-1.5 h-1.5 rounded-full ${
                              isActive ? "bg-brand-green" : "bg-brand-red"
                            }`}
                          />
                          {student.account_status}
                        </span>
                      </td>

                      <td className="py-3 px-4 text-text-muted">
                        {new Date(student.created_at).toLocaleDateString("en-IN", {
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                        })}
                      </td>

                      <td className="py-3 px-4 text-text-muted">
                        {student.last_active_at
                          ? new Date(student.last_active_at).toLocaleDateString("en-IN", {
                              month: "short",
                              day: "numeric",
                            })
                          : "Never"}
                      </td>

                      <td className="py-3 px-4 font-mono font-bold text-brand-gold">
                        {student.total_points || 0} pts
                      </td>

                      <td className="py-3 px-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => setSelectedStudent(student)}
                            className="px-2.5 py-1 rounded-lg bg-surface-interactive text-text-secondary hover:text-white text-[11px] font-bold border border-border-charcoal transition-all"
                          >
                            View
                          </button>

                          {isActive ? (
                            <button
                              onClick={() =>
                                setPendingAction({ student, action: "suspend" })
                              }
                              className="px-2.5 py-1 rounded-lg bg-brand-red/10 text-brand-red hover:bg-brand-red/20 text-[11px] font-bold border border-brand-red/30 transition-all"
                            >
                              Suspend
                            </button>
                          ) : (
                            <button
                              onClick={() =>
                                setPendingAction({ student, action: "activate" })
                              }
                              className="px-2.5 py-1 rounded-lg bg-brand-green/10 text-brand-green hover:bg-brand-green/20 text-[11px] font-bold border border-brand-green/30 transition-all"
                            >
                              Restore
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between p-4 border-t border-border-charcoal bg-surface-primary text-xs">
            <span className="text-text-muted">
              Page {page} of {totalPages}
            </span>
            <div className="flex items-center gap-2">
              <button
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="px-3 py-1 rounded-lg bg-surface-interactive border border-border-charcoal disabled:opacity-30"
              >
                &larr; Prev
              </button>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                className="px-3 py-1 rounded-lg bg-surface-interactive border border-border-charcoal disabled:opacity-30"
              >
                Next &rarr;
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Individual Student Profile Modal (Feature E3.B) */}
      {selectedStudent && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card-primary border border-border-charcoal rounded-3xl p-6 sm:p-8 max-w-lg w-full shadow-elevated space-y-6">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-2xl bg-brand-gold/10 border border-brand-gold/30 flex items-center justify-center text-xl font-black text-brand-gold">
                  {selectedStudent.full_name?.charAt(0) || "P"}
                </div>
                <div>
                  <h3 className="text-lg font-black text-white">
                    {selectedStudent.full_name}
                  </h3>
                  <span className="text-xs text-text-muted font-mono">
                    {selectedStudent.email}
                  </span>
                </div>
              </div>

              <button
                onClick={() => setSelectedStudent(null)}
                className="text-text-muted hover:text-white px-2 py-1 rounded-lg"
              >
                ✕
              </button>
            </div>

            {/* Profile Statistics Grid */}
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-surface-primary border border-border-charcoal space-y-1">
                <span className="text-text-muted text-[10px] uppercase font-bold">
                  Account Status
                </span>
                <div className="font-extrabold capitalize text-white">
                  {selectedStudent.account_status}
                </div>
              </div>

              <div className="p-3 rounded-xl bg-surface-primary border border-border-charcoal space-y-1">
                <span className="text-text-muted text-[10px] uppercase font-bold">
                  Study Streak
                </span>
                <div className="font-extrabold text-brand-gold">
                  🔥 {selectedStudent.study_streak || 0} Days
                </div>
              </div>

              <div className="p-3 rounded-xl bg-surface-primary border border-border-charcoal space-y-1">
                <span className="text-text-muted text-[10px] uppercase font-bold">
                  Total Points
                </span>
                <div className="font-extrabold text-brand-blue">
                  {selectedStudent.total_points || 0} pts
                </div>
              </div>

              <div className="p-3 rounded-xl bg-surface-primary border border-border-charcoal space-y-1">
                <span className="text-text-muted text-[10px] uppercase font-bold">
                  Recovered Mistakes
                </span>
                <div className="font-extrabold text-brand-green">
                  ✓ {selectedStudent.recovered_questions || 0} Qs
                </div>
              </div>
            </div>

            {/* Suspension note if applicable */}
            {selectedStudent.account_status === "suspended" && (
              <div className="p-3 rounded-xl bg-brand-red/10 border border-brand-red/30 space-y-1 text-xs">
                <span className="font-bold text-brand-red">Suspension Notice:</span>
                <p className="text-text-secondary text-[11px]">
                  {selectedStudent.suspended_reason || "Account suspended by administrator policy."}
                </p>
              </div>
            )}

            <div className="flex justify-end gap-3 pt-2">
              {selectedStudent.account_status === "active" ? (
                <button
                  onClick={() => {
                    const st = selectedStudent;
                    setSelectedStudent(null);
                    setPendingAction({ student: st, action: "suspend" });
                  }}
                  className="px-4 py-2 rounded-xl bg-brand-red/10 text-brand-red hover:bg-brand-red/20 text-xs font-bold border border-brand-red/30 transition-all"
                >
                  Suspend Pilot Account
                </button>
              ) : (
                <button
                  onClick={() => {
                    const st = selectedStudent;
                    setSelectedStudent(null);
                    setPendingAction({ student: st, action: "activate" });
                  }}
                  className="px-4 py-2 rounded-xl bg-brand-green text-bg-base hover:opacity-90 text-xs font-black transition-all"
                >
                  Restore Pilot Account
                </button>
              )}
              <button
                onClick={() => setSelectedStudent(null)}
                className="px-4 py-2 rounded-xl bg-surface-interactive text-text-secondary hover:text-white text-xs font-bold"
              >
                Close Overview
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Modal for Suspension / Activation */}
      {pendingAction && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-card-primary border border-border-charcoal rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-elevated space-y-4">
            <div className="text-3xl">
              {pendingAction.action === "suspend" ? "⚠️" : "🛡️"}
            </div>
            <h3 className="text-lg font-black text-white">
              {pendingAction.action === "suspend"
                ? `Suspend ${pendingAction.student.full_name}?`
                : `Restore ${pendingAction.student.full_name}?`}
            </h3>
            <p className="text-xs text-text-secondary leading-relaxed">
              {pendingAction.action === "suspend"
                ? "This will restrict the student from starting examinations or accessing private learning tools until restored. Data is fully preserved."
                : "This will restore active examination privileges for this pilot account."}
            </p>

            {pendingAction.action === "suspend" && (
              <div className="space-y-1">
                <label className="text-[10px] font-bold uppercase tracking-wider text-text-muted">
                  Reason for Suspension (Audit Log)
                </label>
                <input
                  type="text"
                  value={actionReason}
                  onChange={(e) => setActionReason(e.target.value)}
                  placeholder="e.g. Identity check, policy review..."
                  className="w-full bg-surface-primary border border-border-charcoal rounded-xl px-3 py-2 text-xs text-white placeholder-text-muted focus:outline-none focus:border-brand-gold"
                />
              </div>
            )}

            <div className="flex justify-end gap-3 pt-2">
              <button
                disabled={actionLoading}
                onClick={() => setPendingAction(null)}
                className="px-4 py-2 rounded-xl bg-surface-interactive text-text-secondary hover:text-white text-xs font-bold"
              >
                Cancel
              </button>
              <button
                disabled={actionLoading}
                onClick={handleConfirmAction}
                className={`px-5 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition-all ${
                  pendingAction.action === "suspend"
                    ? "bg-brand-red text-white hover:opacity-90"
                    : "bg-brand-green text-bg-base hover:opacity-90"
                }`}
              >
                {actionLoading ? "Processing..." : "Confirm"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

