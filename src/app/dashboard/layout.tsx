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

  // Close dropdowns on outside click
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
    pathname.startsWith("/dashboard/syllabus") ||
    pathname.startsWith("/dashboard/notebook") ||
    pathname.startsWith("/dashboard/revision") ||
    pathname.startsWith("/dashboard/readiness");

  const isResourcesActive = pathname.startsWith("/dashboard/library");
  const isPlannerActive = pathname.startsWith("/dashboard/planner");
  const isDashboardActive = pathname === "/dashboard";

  return (
    <div className="min-h-screen bg-bg-main text-text-primary flex flex-col font-sans selection:bg-brand-blue/30 selection:text-white">
      {/* Top Navigation Bar - Aviation Luxe Header */}
      <header className="sticky top-0 z-40 bg-bg-header/95 backdrop-blur-md border-b border-border-charcoal px-4 sm:px-6 py-3 shadow-md">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
          
          {/* Brand Logo & Aviation Badge */}
          <Link href="/dashboard" className="flex items-center gap-3 text-decoration-none group">
            <div className="w-9 h-9 rounded-xl bg-card-elevated border border-border-charcoal flex items-center justify-center text-xl shadow-card group-hover:border-brand-blue transition-all group-hover:shadow-glow">
              ✈️
            </div>
            <div>
              <div className="text-base font-extrabold tracking-tight text-text-primary flex items-center gap-2 leading-none">
                CPL Practice
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-brand-blue/15 text-brand-blue border border-brand-blue/30">
                  DGCA CBT
                </span>
              </div>
              <div className="text-[11px] text-text-muted mt-1 leading-none font-medium">
                Commercial Pilot Licence Platform
              </div>
            </div>
          </Link>

          {/* Grouped Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1.5 text-xs font-semibold">
            {/* Dashboard */}
            <Link
              href="/dashboard"
              className={`px-3.5 py-2 rounded-lg transition-all ${
                isDashboardActive
                  ? "bg-card-elevated text-brand-blue font-bold shadow-sm border border-brand-blue/30"
                  : "text-text-secondary hover:text-text-primary hover:bg-card-primary"
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
                className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg transition-all ${
                  isPracticeActive || practiceOpen
                    ? "bg-card-elevated text-brand-blue font-bold shadow-sm border border-brand-blue/30"
                    : "text-text-secondary hover:text-text-primary hover:bg-card-primary"
                }`}
              >
                <span>Practice</span>
                <span className={`text-[10px] transition-transform ${practiceOpen ? "rotate-180" : ""}`}>▾</span>
              </button>

              {practiceOpen && (
                <div className="absolute left-0 mt-2 w-56 bg-card-primary border border-border-charcoal rounded-xl shadow-elevated p-2 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
                  <Link
                    href="/dashboard/custom-practice"
                    className="flex flex-col px-3 py-2.5 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors group"
                  >
                    <span className="font-bold text-xs text-text-primary group-hover:text-brand-blue">Custom Practice</span>
                    <span className="text-[10px] text-text-muted mt-0.5">Multi-topic quiz builder</span>
                  </Link>
                  <Link
                    href="/dashboard#subjects"
                    className="flex flex-col px-3 py-2.5 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors group"
                  >
                    <span className="font-bold text-xs text-text-primary group-hover:text-brand-blue">Subject Practice</span>
                    <span className="text-[10px] text-text-muted mt-0.5">Direct syllabus chapters</span>
                  </Link>
                  <Link
                    href="/dashboard/exam?mode=mock"
                    className="flex flex-col px-3 py-2.5 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors group"
                  >
                    <span className="font-bold text-xs text-text-primary group-hover:text-brand-gold">Mock Examination</span>
                    <span className="text-[10px] text-text-muted mt-0.5">50-question DGCA simulation</span>
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
                className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg transition-all ${
                  isProgressActive || progressOpen
                    ? "bg-card-elevated text-brand-blue font-bold shadow-sm border border-brand-blue/30"
                    : "text-text-secondary hover:text-text-primary hover:bg-card-primary"
                }`}
              >
                <span>Progress</span>
                <span className={`text-[10px] transition-transform ${progressOpen ? "rotate-180" : ""}`}>▾</span>
              </button>

              {progressOpen && (
                <div className="absolute left-0 mt-2 w-64 bg-card-primary border border-border-charcoal rounded-xl shadow-elevated p-2 z-50 animate-in fade-in slide-in-from-top-1 duration-150">
                  <Link
                    href="/dashboard/syllabus"
                    className="flex flex-col px-3 py-2.5 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors group border-b border-border-charcoal/60 mb-1"
                  >
                    <span className="font-bold text-xs text-brand-blue flex items-center justify-between">
                      <span>Syllabus Tracker</span>
                      <span className="text-[10px] px-1.5 py-0.2 bg-brand-blue/20 rounded">95 Topics</span>
                    </span>
                    <span className="text-[10px] text-text-muted mt-0.5">Theory, Practice & Mock checklists</span>
                  </Link>
                  <Link
                    href="/dashboard/notebook"
                    className="flex flex-col px-3 py-2.5 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors group"
                  >
                    <span className="font-bold text-xs text-text-primary group-hover:text-brand-red">Mistake Notebook</span>
                    <span className="text-[10px] text-text-muted mt-0.5">All active mistake questions</span>
                  </Link>
                  <Link
                    href="/dashboard/revision"
                    className="flex flex-col px-3 py-2.5 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors group"
                  >
                    <span className="font-bold text-xs text-text-primary group-hover:text-brand-teal">Spaced Revision</span>
                    <span className="text-[10px] text-text-muted mt-0.5">Interval memory retention</span>
                  </Link>
                  <Link
                    href="/dashboard/readiness"
                    className="flex flex-col px-3 py-2.5 rounded-lg hover:bg-card-elevated text-text-secondary hover:text-text-primary transition-colors group"
                  >
                    <span className="font-bold text-xs text-text-primary group-hover:text-brand-gold">Exam Readiness</span>
                    <span className="text-[10px] text-text-muted mt-0.5">Predicted pass probability</span>
                  </Link>
                </div>
              )}
            </div>

            {/* Resources */}
            <Link
              href="/dashboard/library"
              className={`px-3.5 py-2 rounded-lg transition-all ${
                isResourcesActive
                  ? "bg-card-elevated text-brand-blue font-bold shadow-sm border border-brand-blue/30"
                  : "text-text-secondary hover:text-text-primary hover:bg-card-primary"
              }`}
            >
              Resources
            </Link>

            {/* Planner */}
            <Link
              href="/dashboard/planner"
              className={`px-3.5 py-2 rounded-lg transition-all ${
                isPlannerActive
                  ? "bg-card-elevated text-brand-blue font-bold shadow-sm border border-brand-blue/30"
                  : "text-text-secondary hover:text-text-primary hover:bg-card-primary"
              }`}
            >
              Planner
            </Link>

            {/* Admin (if applicable) */}
            {isAdmin && (
              <Link
                href="/admin"
                className="px-3 py-1.5 rounded-lg text-brand-gold bg-brand-gold/15 border border-brand-gold/30 hover:bg-brand-gold/25 ml-1 font-bold"
              >
                Admin
              </Link>
            )}
          </nav>

          {/* Right: Points, Profile, Sign Out */}
          <div className="flex items-center gap-3">
            {/* Amber Gold Points Indicator */}
            <div className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-card-primary border border-brand-gold/30 text-xs font-bold text-brand-gold shadow-sm">
              <span>⭐</span>
              <span>{totalPoints} pts</span>
            </div>

            {/* Pilot Status Tag / Profile Link */}
            <Link
              href="/dashboard/profile"
              className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-card-primary hover:bg-card-elevated border border-border-charcoal hover:border-brand-blue/50 text-xs font-semibold text-text-primary transition-all group"
              title="View Pilot Profile & Settings"
            >
              <span className="w-2 h-2 rounded-full bg-brand-teal animate-pulse"></span>
              <span className="max-w-[120px] truncate group-hover:text-brand-blue">{studentName}</span>
              <span className="text-[10px] text-text-muted">⚙️</span>
            </Link>

            {/* Exit Action */}
            <button
              onClick={handleSignOut}
              className="text-xs font-semibold text-text-muted hover:text-brand-red px-3 py-1.5 rounded-lg border border-border-charcoal hover:border-brand-red/40 transition-colors"
              title="Sign Out"
            >
              Exit
            </button>

            {/* Mobile Hamburger Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg border border-border-charcoal text-text-secondary hover:text-text-primary hover:bg-card-elevated"
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
          <div className="md:hidden mt-3 pt-3 border-t border-border-charcoal pb-3 space-y-1 text-xs">
            <Link
              href="/dashboard"
              className={`block px-3 py-2 rounded-lg font-semibold ${
                isDashboardActive ? "bg-card-elevated text-brand-blue" : "text-text-secondary hover:text-white"
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
              href="/dashboard/syllabus"
              className="block px-3 py-1.5 rounded-lg text-brand-blue font-bold pl-5"
            >
              &bull; Syllabus Tracker (95 Topics)
            </Link>
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
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-border-charcoal py-5 px-6 text-center text-xs text-text-muted bg-bg-header/50">
        <p>CPL Practice &bull; DGCA India Commercial Pilot Licence Written Examination Platform</p>
      </footer>
    </div>
  );
}
