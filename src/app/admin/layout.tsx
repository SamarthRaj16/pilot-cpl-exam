"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  const adminNav = [
    { label: "Overview", href: "/admin" },
    { label: "Question Bank (839 Qs)", href: "/admin/questions" },
    { label: "Return to Pilot Portal", href: "/dashboard" },
  ];

  return (
    <div className="min-h-screen bg-bg-main text-text-primary flex flex-col">
      {/* Admin Top Bar */}
      <header className="bg-card-primary border-b border-border-charcoal px-6 py-3.5 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-brand-gold/20 border border-brand-gold/40 flex items-center justify-center text-sm font-bold text-brand-gold">
              ⚙️
            </div>
            <div>
              <h1 className="text-sm font-extrabold tracking-tight text-white flex items-center gap-2">
                CPL Practice Admin
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-brand-gold/20 text-brand-gold border border-brand-gold/30">
                  Staff Console
                </span>
              </h1>
            </div>
          </div>

          <nav className="flex items-center gap-2">
            {adminNav.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                    isActive
                      ? "bg-brand-gold text-black font-black"
                      : "text-text-secondary hover:text-white hover:bg-surface-interactive"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {children}
      </main>
    </div>
  );
}

