"use client";

import React, { useEffect, useState } from "react";
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
        // Fallback to guest mode
      }
    }
    loadUser();
  }, []);

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

  const navItems = [
    { label: "Dashboard", href: "/dashboard" },
    { label: "Custom Practice", href: "/dashboard/custom-practice" },
    { label: "Mistake Notebook", href: "/dashboard/notebook" },
    { label: "Spaced Revision", href: "/dashboard/revision" },
    { label: "Exam Readiness", href: "/dashboard/readiness" },
    { label: "Study Planner", href: "/dashboard/planner" },
    { label: "Reference Library", href: "/dashboard/library" },
  ];

  return (
    <div className="min-h-screen bg-bg-main text-text-primary flex flex-col">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 bg-bg-main/90 backdrop-blur-md border-b border-border-charcoal px-6 py-3.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
          <Link href="/dashboard" className="flex items-center gap-3 text-decoration-none">
            <div className="w-9 h-9 rounded-xl bg-card-elevated border border-border-charcoal flex items-center justify-center text-xl shadow-card">
              ✈️
            </div>
            <div>
              <div className="text-base font-extrabold tracking-tight flex items-center gap-2">
                CPL Practice
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-brand-purple/20 text-brand-purple border border-brand-purple/30">
                  DGCA CBT
                </span>
              </div>
              <div className="text-[10px] uppercase font-bold tracking-wider text-text-muted">
                Commercial Pilot Licence
              </div>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    isActive
                      ? "bg-surface-interactive text-white"
                      : "text-text-secondary hover:text-white hover:bg-surface-interactive/50"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
            {isAdmin && (
              <Link
                href="/admin"
                className="px-3 py-1.5 rounded-lg text-xs font-bold text-brand-gold bg-brand-gold/10 border border-brand-gold/30 hover:bg-brand-gold/20 ml-2"
              >
                ⚙️ Admin Panel
              </Link>
            )}
          </nav>

          {/* User Status / Actions */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-card-elevated border border-border-charcoal text-xs font-bold text-brand-gold">
              ⭐ {totalPoints} Points
            </div>

            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-card-elevated border border-border-charcoal text-xs font-bold text-text-primary">
              <span className="w-2 h-2 rounded-full bg-brand-green animate-pulse"></span>
              {studentName}
            </div>

            <button
              onClick={handleSignOut}
              className="px-3 py-1.5 rounded-lg text-xs font-bold text-text-muted hover:text-brand-red border border-border-charcoal hover:border-brand-red/30 transition-all"
              title="Sign Out"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-border-charcoal py-6 px-6 text-center text-xs text-text-muted bg-bg-secondary/50">
        <p>CPL Practice 2.0 &bull; DGCA India Commercial Pilot Licence Written Examination Simulator</p>
        <p className="mt-1">Compliant with CAR Section 7, Aircraft Rules 1937, and ICAO Doc 9432 Standards</p>
      </footer>
    </div>
  );
}

