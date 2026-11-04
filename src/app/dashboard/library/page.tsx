"use client";

import React, { useState } from "react";

export default function LibraryPage() {
  const [selectedSubject, setSelectedSubject] = useState("All");

  const DOCUMENTS = [
    {
      title: "DGCA CAR Section 7 — Flight Crew Licensing (Training & Exams)",
      subject: "Air Regulations",
      type: "Official Regulatory Document",
      source: "DGCA India Official Portal",
      url: "https://dgca.gov.in",
      desc: "Comprehensive standards on Commercial Pilot Licence exams, validity periods, re-attempt policies, and medical requirements.",
    },
    {
      title: "Bharatiya Vayuyan Adhiniyam 2024 Overview & Transition",
      subject: "Air Regulations",
      type: "Statutory Law Guide",
      source: "Ministry of Civil Aviation",
      url: "https://dgca.gov.in",
      desc: "Principal Indian statute replacing Aircraft Act 1934, safety oversight, and BCAS security authority structures.",
    },
    {
      title: "General Navigation — Formulas & Chart Projections Summary",
      subject: "Air Navigation",
      type: "Study Reference Sheet",
      source: "Oxford ATPL / R.K. Bali Summary",
      url: "#",
      desc: "Formula sheet for Convergency, Conversion Angle, Departure, 1-in-60 rule, and Point of Safe Return (PNR/CP).",
    },
    {
      title: "Aviation Meteorology — I.C. Joshi Core Concept Summaries",
      subject: "Aviation Meteorology",
      type: "Textbook Notes",
      source: "I.C. Joshi Aviation Meteorology",
      url: "#",
      desc: "Atmospheric pressure altimetry (QNH/QFE), lapse rates (DALR/SALR), stability, monsoon dynamics, and METAR/TAF decode keys.",
    },
    {
      title: "Aircraft General Knowledge — Piston Engines & Systems",
      subject: "Technical General",
      type: "Technical Systems Guide",
      source: "FAA-H-8083 / Oxford AGK",
      url: "#",
      desc: "Operating cycles of four-stroke aero engines, dual magneto ignition systems, carburettor icing, and pitot-static blockage behaviors.",
    },
    {
      title: "Training Aircraft V-Speeds and Operating Limitations Card",
      subject: "Technical Specific",
      type: "POH Quick Reference",
      source: "Cessna 172 / Light Twin Flight Manual",
      url: "#",
      desc: "Vs0, Vs1, Vr, Vx, Vy, Vfe, Va, Vno, Vne definitions, ASI color arc markings, and weight & balance datum fundamentals.",
    },
    {
      title: "ICAO Doc 9432 — Manual of Radiotelephony Standard Phraseology",
      subject: "RTR",
      type: "ICAO Official Standard",
      source: "ICAO / WPC RTR(A)",
      url: "https://www.icao.int",
      desc: "Standard phraseology, readback mandates, distress (MAYDAY) and urgency (PAN PAN) procedures, and SSR transponder squawk codes.",
    },
  ];

  const subjects = [
    "All",
    "Air Navigation",
    "Air Regulations",
    "Aviation Meteorology",
    "Technical General",
    "Technical Specific",
    "RTR",
  ];

  const filtered =
    selectedSubject === "All"
      ? DOCUMENTS
      : DOCUMENTS.filter((doc) => doc.subject === selectedSubject);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
          <span>📚</span> Aviation Reference Library
        </h2>
        <p className="text-xs text-text-muted mt-0.5">
          Curated collection of official regulatory publications, CAR circulars, syllabus notes, and formula sheets
        </p>
      </div>

      {/* Subject Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {subjects.map((s) => (
          <button
            key={s}
            onClick={() => setSelectedSubject(s)}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              selectedSubject === s
                ? "bg-brand-purple text-white shadow-glow"
                : "bg-card-primary border border-border-charcoal text-text-secondary hover:text-white"
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Documents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((doc, idx) => (
          <div
            key={idx}
            className="p-6 rounded-2xl bg-card-primary border border-border-charcoal shadow-card flex flex-col justify-between space-y-4 hover:border-brand-purple/50 transition-all"
          >
            <div>
              <div className="flex items-center justify-between text-[10px] uppercase font-bold tracking-wider mb-2">
                <span className="text-brand-purple px-2 py-0.5 rounded bg-brand-purple/10 border border-brand-purple/30">
                  {doc.subject}
                </span>
                <span className="text-text-muted">{doc.type}</span>
              </div>
              <h3 className="text-base font-extrabold text-white leading-snug">{doc.title}</h3>
              <p className="text-xs text-text-secondary mt-2 leading-relaxed">{doc.desc}</p>
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-border-charcoal/50 text-xs">
              <span className="text-[11px] font-bold text-text-muted">Source: {doc.source}</span>
              <a
                href={doc.url}
                target="_blank"
                rel="noreferrer"
                className="text-xs font-bold text-brand-teal hover:underline flex items-center gap-1"
              >
                Access Source &rarr;
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

