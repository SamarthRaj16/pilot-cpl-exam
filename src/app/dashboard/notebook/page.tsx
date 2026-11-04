"use client";

import React, { useState, useEffect } from "react";
import rawQuestions from "@/data/questions.json";

export default function MistakeNotebookPage() {
  const [filterStatus, setFilterStatus] = useState<"all" | "unresolved" | "resolved">("unresolved");
  const [selectedSubject, setSelectedSubject] = useState<string>("");
  const [mistakes, setMistakes] = useState<any[]>([]);

  const LETTERS = ["A", "B", "C", "D"];

  useEffect(() => {
    // Load mistakes from localStorage or DB
    try {
      const stored = localStorage.getItem("cpl_mistakes");
      if (stored) {
        setMistakes(JSON.parse(stored));
      } else {
        // Sample seed if empty
        const sampleMistakes = [
          {
            id: "NAV-001",
            question: "Compass deviation is the angle between",
            options: [
              "true north and magnetic north",
              "grid north and true north",
              "aircraft heading and track",
              "magnetic north and compass north",
            ],
            correctChoice: 3,
            userChoice: 0,
            subject: "Air Navigation",
            topic: "Aircraft Magnetism and the Compasses",
            explanation:
              "Deviation is the angle between magnetic north and compass north, produced by magnetic influences within the aircraft.",
            source: "R.K. Bali Air Navigation / Oxford ATPL Gen Nav",
            status: "unresolved",
            incorrectCount: 2,
            correctedCount: 0,
            date: "Today",
          },
          {
            id: "MET-004",
            question: "When an aircraft altimeter subscale is set to QNH, the altimeter indicates:",
            options: [
              "Height above the aerodrome elevation",
              "Altitude above Mean Sea Level (MSL)",
              "Pressure altitude relative to the 1013.25 hPa datum",
              "True height above the instantaneous ground level (AGL)",
            ],
            correctChoice: 1,
            userChoice: 2,
            subject: "Aviation Meteorology",
            topic: "Atmospheric Pressure",
            explanation:
              "QNH is station pressure reduced to MSL using standard ISA temperature lapse rates. Setting QNH indicates altitude above Mean Sea Level (MSL).",
            source: "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure'",
            status: "unresolved",
            incorrectCount: 1,
            correctedCount: 0,
            date: "Yesterday",
          },
        ];
        setMistakes(sampleMistakes);
      }
    } catch {
      // Ignored
    }
  }, []);

  const handleToggleResolved = (id: string) => {
    const updated = mistakes.map((m) => {
      if (m.id === id) {
        return {
          ...m,
          status: m.status === "unresolved" ? "resolved" : "unresolved",
        };
      }
      return m;
    });
    setMistakes(updated);
    try {
      localStorage.setItem("cpl_mistakes", JSON.stringify(updated));
    } catch {
      // Ignored
    }
  };

  const filtered = mistakes.filter((m) => {
    if (filterStatus !== "all" && m.status !== filterStatus) return false;
    if (selectedSubject && m.subject !== selectedSubject) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-border-charcoal">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <span>📓</span> Personal Mistake Notebook
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Auto-catalog of previously missed questions with attempt counts and concept tracking
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setFilterStatus("unresolved")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              filterStatus === "unresolved"
                ? "bg-brand-red text-white shadow-glow"
                : "bg-card-elevated border border-border-charcoal text-text-secondary"
            }`}
          >
            Unresolved ({mistakes.filter((m) => m.status === "unresolved").length})
          </button>
          <button
            onClick={() => setFilterStatus("resolved")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              filterStatus === "resolved"
                ? "bg-brand-green text-black shadow-glow"
                : "bg-card-elevated border border-border-charcoal text-text-secondary"
            }`}
          >
            Resolved ({mistakes.filter((m) => m.status === "resolved").length})
          </button>
          <button
            onClick={() => setFilterStatus("all")}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              filterStatus === "all"
                ? "bg-brand-purple text-white shadow-glow"
                : "bg-card-elevated border border-border-charcoal text-text-secondary"
            }`}
          >
            All ({mistakes.length})
          </button>
        </div>
      </div>

      {/* Mistake Items */}
      {filtered.length === 0 ? (
        <div className="bg-card-primary border border-border-charcoal rounded-2xl p-12 text-center text-text-muted space-y-2">
          <div className="text-4xl mb-2">🎉</div>
          <h4 className="text-sm font-bold text-white">No mistakes in this filter!</h4>
          <p className="text-xs">Great job — keep practicing to maintain high accuracy.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filtered.map((item) => (
            <div
              key={item.id}
              className="bg-card-primary border border-border-charcoal rounded-2xl p-6 shadow-card space-y-4"
            >
              <div className="flex items-center justify-between text-xs font-bold">
                <span className="text-text-muted uppercase tracking-wider">
                  {item.id} &bull; {item.subject} &bull; {item.topic}
                </span>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] uppercase font-black px-2 py-0.5 rounded bg-brand-red/20 text-brand-red border border-brand-red/30">
                    {item.incorrectCount} Incorrect Attempts
                  </span>
                  <span className="text-[10px] uppercase font-black px-2 py-0.5 rounded bg-brand-green/20 text-brand-green border border-brand-green/30">
                    {item.correctedCount} Corrected
                  </span>
                </div>
              </div>

              <h4 className="text-sm sm:text-base font-bold text-white leading-relaxed">
                {item.question}
              </h4>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-medium">
                <div className="p-3 rounded-xl bg-brand-red/10 border border-brand-red/30 text-brand-red">
                  <span className="font-extrabold block text-[10px] uppercase mb-0.5">
                    Your Previous Mistake:
                  </span>
                  {LETTERS[item.userChoice]}. {item.options[item.userChoice]}
                </div>
                <div className="p-3 rounded-xl bg-brand-green/10 border border-brand-green/30 text-brand-green">
                  <span className="font-extrabold block text-[10px] uppercase mb-0.5">
                    Authoritative Correct Answer:
                  </span>
                  {LETTERS[item.correctChoice]}. {item.options[item.correctChoice]}
                </div>
              </div>

              <div className="p-4 rounded-xl bg-card-elevated border border-border-charcoal text-xs text-text-secondary leading-relaxed">
                <strong className="text-white block mb-1">Authoritative Explanation:</strong>
                {item.explanation}
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-border-charcoal/50 text-xs">
                <span className="text-[11px] font-bold text-text-muted">
                  📚 Source: {item.source}
                </span>

                <button
                  onClick={() => handleToggleResolved(item.id)}
                  className={`px-3 py-1.5 rounded-lg font-bold text-xs border transition-all ${
                    item.status === "resolved"
                      ? "bg-brand-green text-black border-brand-green"
                      : "border-border-charcoal text-text-secondary hover:text-white"
                  }`}
                >
                  {item.status === "resolved" ? "✓ Mark as Resolved" : "Mark as Understood"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
