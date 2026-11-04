"use client";

import React, { useEffect, useState, useRef } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();

  const [studentName, setStudentName] = useState("Cadet Pilot");
  const [isAdmin, setIsAdmin] = useState(false);
  const [totalPoints, setTotalPoints] = useState(0);

  // Dropdown states for desktop
  const [practiceOpen, setPracticeOpen] = useState(false);
  const [progressOpen, setProgressOpen] = useState(false);
  // Mobile drawer state
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const practiceRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function loadUser() {
      try {
        const supabase = createClient();
        const {
          data: { user },
        } = await supabase.auth.getUser();

        if (user) {
          const { data: profile } = await supabase
            .from("profiles")
            .select("full_name, role, total_points")
            .eq("id", user.id)
            .single();

          if (profile) {
            setStudentName(profile.full_name || "Cadet Pilot");
            setIsAdmin(profile.role === "admin");
            setTotalPoints(profile.total_points || 0);
          }
        }
      } catch {
        // Fallback to offline / guest mode
      }
    }
    loadUser();
  }, []);

  // Close dropdowns on outside click or route change
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (practiceRef.current && !practiceRef.current.contains(e.target as Node)) {
        setPracticeOpen(false);
      }
      if (progressRef.current && !progressRef.current.contains(e.target as Node)) {
        setProgressOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    setPracticeOpen(false);
    setProgressOpen(false);
    setMobileMenuOpen(false);
  }, [pathname]);

  const handleSignOut = async () => {
    try {
      const supabase = createClient();
      await supabase.auth.signOut();
      router.push("/auth/login");
      router.refresh();
    } catch {
      router.push("/auth/login");
    }
  };

  const isPracticeActive =
    pathname.startsWith("/dashboard/custom-practice") ||
    pathname.startsWith("/dashboard/exam");

  const isProgressActive =
    pathname.startsWith("/dashboard/notebook") ||
    pathname.startsWith("/dashboard/revision") ||
    pathname.startsWith("/dashboard/readiness");

  const isResourcesActive = pathname.startsWith("/dashboard/library");
  const isPlannerActive = pathname.startsWith("/dashboard/planner");
  const isDashboardActive = pathname === "/dashboard";

  return (
    <div className="min-h-screen bg-bg-main text-text-primary flex flex-col font-sans">
      {/* Top Navigation Bar - Midnight Aviation */}
      <header className="sticky top-0 z-40 bg-bg-main/95 backdrop-blur-md border-b border-border-charcoal px-4 sm:px-6 py-2.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
          
          {/* Logo & Platform Badge */}
          <Link href="/dashboard" className="flex items-center gap-2.5 text-decoration-none group">
            <div className="w-8 h-8 rounded-lg bg-card-elevated border border-border-charcoal flex items-center justify-center text-lg shadow-card group-hover:border-brand-sky transition-colors">
              ✈️
            </div>
            <div>
              <div className="text-sm font-bold tracking-tight text-text-primary flex items-center gap-1.5 leading-none">
                CPL Practice
                <span className="text-[9px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-brand-sky/10 text-brand-sky border border-brand-sky/25">
                  DGCA CBT
                </span>
              </div>
              <div className="text-[10px] text-text-muted mt-0.5 leading-none">
                Commercial Pilot Licence
              </div>
            </div>
          </Link>

          {/* Grouped Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1 text-xs font-semibold">
            {/* Dashboard */}
            <Link
              href="/dashboard"
              className={`px-3 py-1.5 rounded-lg transition-colors ${
                isDashboardActive
                  ? "bg-card-elevated text-brand-sky font-bold shadow-sm"
                  : "text-text-secondary hover:text-text-primary hover:bg-surface-interactive/40"
              }`}
            >
              Dashboard
            </Link>

            {/* Practice Dropdown */}
            <div className="relative" ref={practiceRef}>
              <button
                type="button"
                onClick={() => {
                  setPracticeOpen(!practiceOpen);
                  setProgressOpen(false);
                }}
                className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition-colors ${
                  isPracticeActive || practiceOpen
                    ? "bg-card-elevated text-brand-sky font-bold shadow-sm"
                    : "text-text-secondary hover:text-text-primary hover:bg-surface-interactive/40"
                }`}
              >
                <span>Practice</span>
                <span className={`text-[10px] transition-transform ${practiceOpen ? "rotate-180" : ""}`}>▾</span>
              </button>

              {practiceOpen && (
                <div className="absolute left-0 mt-1.5 w-52 bg-card-primary border border-border-charcoal rounded-xl shadow-elevated p-1.5 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
                  <Link
                    href="/dashboard/custom-practice"
                    className="flex flex-col px-3 py-2 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors"
                  >
                    <span className="font-bold text-xs text-text-primary">Custom Practice</span>
                    <span className="text-[10px] text-text-muted">Multi-topic quiz builder</span>
                  </Link>
                  <Link
                    href="/dashboard#subjects"
                    className="flex flex-col px-3 py-2 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors"
                  >
                    <span className="font-bold text-xs text-text-primary">Subject Practice</span>
                    <span className="text-[10px] text-text-muted">Direct syllabus chapters</span>
                  </Link>
                  <Link
                    href="/dashboard/exam?mode=mock"
                    className="flex flex-col px-3 py-2 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors"
                  >
                    <span className="font-bold text-xs text-text-primary">Mock Examination</span>
                    <span className="text-[10px] text-text-muted">50-question DGCA simulation</span>
                  </Link>
                </div>
              )}
            </div>

            {/* Progress Dropdown */}
            <div className="relative" ref={progressRef}>
              <button
                type="button"
                onClick={() => {
                  setProgressOpen(!progressOpen);
                  setPracticeOpen(false);
                }}
                className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition-colors ${
                  isProgressActive || progressOpen
                    ? "bg-card-elevated text-brand-sky font-bold shadow-sm"
                    : "text-text-secondary hover:text-text-primary hover:bg-surface-interactive/40"
                }`}
              >
                <span>Progress</span>
                <span className={`text-[10px] transition-transform ${progressOpen ? "rotate-180" : ""}`}>▾</span>
              </button>

              {progressOpen && (
                <div className="absolute left-0 mt-1.5 w-56 bg-card-primary border border-border-charcoal rounded-xl shadow-elevated p-1.5 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
                  <Link
                    href="/dashboard/notebook"
                    className="flex flex-col px-3 py-2 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors"
                  >
                    <span className="font-bold text-xs text-text-primary">Mistake Notebook</span>
                    <span className="text-[10px] text-text-muted">All active mistake questions</span>
                  </Link>
                  <Link
                    href="/dashboard/revision"
                    className="flex flex-col px-3 py-2 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors"
                  >
                    <span className="font-bold text-xs text-text-primary">Spaced Revision</span>
                    <span className="text-[10px] text-text-muted">Interval-based memory retention</span>
                  </Link>
                  <Link
                    href="/dashboard/readiness"
                    className="flex flex-col px-3 py-2 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors"
                  >
                    <span className="font-bold text-xs text-text-primary">Exam Readiness</span>
                    <span className="text-[10px] text-text-muted">Predicted pass probability</span>
                  </Link>
                </div>
              )}
            </div>

            {/* Resources */}
            <Link
              href="/dashboard/library"
              className={`px-3 py-1.5 rounded-lg transition-colors ${
                isResourcesActive
                  ? "bg-card-elevated text-brand-sky font-bold shadow-sm"
                  : "text-text-secondary hover:text-text-primary hover:bg-surface-interactive/40"
              }`}
            >
              Resources
            </Link>

            {/* Planner */}
            <Link
              href="/dashboard/planner"
              className={`px-3 py-1.5 rounded-lg transition-colors ${
                isPlannerActive
                  ? "bg-card-elevated text-brand-sky font-bold shadow-sm"
                  : "text-text-secondary hover:text-text-primary hover:bg-surface-interactive/40"
              }`}
            >
              Planner
            </Link>

            {/* Admin (if applicable) */}
            {isAdmin && (
              <Link
                href="/admin"
                className="px-2.5 py-1 rounded-lg text-brand-gold bg-brand-gold/10 border border-brand-gold/25 hover:bg-brand-gold/20 ml-1 font-bold"
              >
                Admin
              </Link>
            )}
          </nav>

          {/* Right: Points, Profile, Sign Out */}
          <div className="flex items-center gap-2.5">
            {/* Points Indicator */}
            <div className="hidden sm:inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-card-primary border border-border-charcoal text-xs font-semibold text-brand-gold">
              <span>⭐</span>
              <span>{totalPoints} pts</span>
            </div>

            {/* Pilot Profile */}
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-lg bg-card-primary border border-border-charcoal text-xs font-medium text-text-primary">
              <span className="w-1.5 h-1.5 rounded-full bg-brand-teal"></span>
              <span className="max-w-[110px] truncate">{studentName}</span>
            </div>

            {/* Sign Out */}
            <button
              onClick={handleSignOut}
              className="text-xs font-semibold text-text-muted hover:text-brand-red px-2.5 py-1 rounded-lg border border-border-charcoal hover:border-brand-red/30 transition-colors"
              title="Sign Out"
            >
              Exit
            </button>

            {/* Mobile Hamburger Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-1.5 rounded-lg border border-border-charcoal text-text-secondary hover:text-text-primary hover:bg-card-elevated"
              aria-label="Toggle Navigation Menu"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-2 pt-2 border-t border-border-charcoal pb-3 space-y-1 text-xs">
            <Link
              href="/dashboard"
              className={`block px-3 py-2 rounded-lg font-semibold ${
                isDashboardActive ? "bg-card-elevated text-brand-sky" : "text-text-secondary hover:text-white"
              }`}
            >
              Dashboard
            </Link>
            <div className="pt-2 px-3 text-[10px] font-bold uppercase tracking-wider text-text-muted">Practice</div>
            <Link
              href="/dashboard/custom-practice"
              className="block px-3 py-1.5 rounded-lg text-text-secondary hover:text-white pl-5"
            >
              &bull; Custom Practice (Multi-Topic)
            </Link>
            <Link
              href="/dashboard#subjects"
              className="block px-3 py-1.5 rounded-lg text-text-secondary hover:text-white pl-5"
            >
              &bull; Subject Practice
            </Link>
            <Link
              href="/dashboard/exam?mode=mock"
              className="block px-3 py-1.5 rounded-lg text-text-secondary hover:text-white pl-5"
            >
              &bull; DGCA Mock Exam (50 Qs)
            </Link>

            <div className="pt-2 px-3 text-[10px] font-bold uppercase tracking-wider text-text-muted">Progress</div>
            <Link
              href="/dashboard/notebook"
              className="block px-3 py-1.5 rounded-lg text-text-secondary hover:text-white pl-5"
            >
              &bull; Mistake Notebook
            </Link>
            <Link
              href="/dashboard/revision"
              className="block px-3 py-1.5 rounded-lg text-text-secondary hover:text-white pl-5"
            >
              &bull; Spaced Revision
            </Link>
            <Link
              href="/dashboard/readiness"
              className="block px-3 py-1.5 rounded-lg text-text-secondary hover:text-white pl-5"
            >
              &bull; Exam Readiness
            </Link>

            <div className="pt-2 px-3 text-[10px] font-bold uppercase tracking-wider text-text-muted">Tools</div>
            <Link
              href="/dashboard/library"
              className="block px-3 py-1.5 rounded-lg text-text-secondary hover:text-white pl-5"
            >
              &bull; Reference Library
            </Link>
            <Link
              href="/dashboard/planner"
              className="block px-3 py-1.5 rounded-lg text-text-secondary hover:text-white pl-5"
            >
              &bull; Study Planner
            </Link>
          </div>
        )}
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">
        {children}
      </main>

      {/* Footer - Minimal Midnight Aviation */}
      <footer className="border-t border-border-charcoal py-4 px-6 text-center text-[11px] text-text-muted bg-bg-secondary/40">
        <p>CPL Practice &bull; DGCA India Commercial Pilot Licence Examination Preparation</p>
      </footer>
    </div>
  );
}
