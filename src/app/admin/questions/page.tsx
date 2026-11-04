"use client";

import React, { useState } from "react";
import rawQuestions from "@/data/questions.json";

export default function AdminQuestionsPage() {
  const [questions, setQuestions] = useState<any[]>(rawQuestions);
  const [search, setSearch] = useState("");
  const [selectedSubject, setSelectedSubject] = useState("");
  const [selectedDifficulty, setSelectedDifficulty] = useState("");
  const [showAddModal, setShowAddModal] = useState(false);

  // Form state
  const [newSubj, setNewSubj] = useState("Air Navigation");
  const [newTopic, setNewTopic] = useState("");
  const [newDiff, setNewDiff] = useState("medium");
  const [newQText, setNewQText] = useState("");
  const [newOpts, setNewOpts] = useState(["", "", "", ""]);
  const [newAnsIdx, setNewAnsIdx] = useState(0);
  const [newExpl, setNewExpl] = useState("");
  const [newSrc, setNewSrc] = useState("");
  const [formError, setFormError] = useState<string | null>(null);
  const [formSuccess, setFormSuccess] = useState<string | null>(null);

  const filtered = questions.filter((q) => {
    if (selectedSubject && q.subject !== selectedSubject) return false;
    if (selectedDifficulty && q.difficulty !== selectedDifficulty) return false;
    if (search) {
      const qText = q.question.toLowerCase();
      const id = q.id.toLowerCase();
      const topic = (q.topic || "").toLowerCase();
      const s = search.toLowerCase();
      if (!qText.includes(s) && !id.includes(s) && !topic.includes(s)) return false;
    }
    return true;
  });

  const handleAddQuestion = (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setFormSuccess(null);

    // Validate
    if (newOpts.some((o) => !o.trim())) {
      setFormError("All 4 options must be filled.");
      return;
    }

    // Duplicate check
    const normalized = newQText.toLowerCase().replace(/[^a-z0-9]/g, "");
    const exists = questions.some(
      (q) => q.question.toLowerCase().replace(/[^a-z0-9]/g, "") === normalized
    );
    if (exists) {
      setFormError("Duplicate Question! An identical or near-identical question already exists in the bank.");
      return;
    }

    const prefixMap: Record<string, string> = {
      "Air Navigation": "NAV",
      "Air Regulations": "REG",
      "Aviation Meteorology": "MET",
      "Technical General": "TG",
      "Technical Specific": "TS",
      RTR: "RTR",
    };
    const prefix = prefixMap[newSubj] || "Q";
    const newId = `${prefix}-${Date.now().toString().slice(-4)}`;

    const created = {
      id: newId,
      subject: newSubj,
      topic: newTopic || "General",
      difficulty: newDiff,
      question: newQText,
      options: newOpts,
      answerIndex: newAnsIdx,
      explanation: newExpl,
      source: newSrc,
    };

    setQuestions([created, ...questions]);
    setFormSuccess(`Question ${newId} created and validated successfully.`);
    setTimeout(() => {
      setShowAddModal(false);
      setFormSuccess(null);
      setNewQText("");
      setNewOpts(["", "", "", ""]);
      setNewExpl("");
      setNewSrc("");
    }, 1200);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-border-charcoal">
        <div>
          <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
            <span>📚</span> Question Bank Manager ({questions.length} Active)
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Manage validated questions, inspect source citations, and enforce duplicate prevention
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="px-4 py-2 rounded-xl bg-brand-purple hover:bg-brand-purpleDark text-white font-extrabold text-xs shadow-card transition-all flex items-center gap-1.5"
        >
          + Add Validated Question
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by ID, keyword, or topic..."
          className="px-4 py-2.5 rounded-xl bg-card-primary border border-border-charcoal text-text-primary placeholder:text-text-muted text-xs focus:outline-none focus:border-brand-purple"
        />

        <select
          value={selectedSubject}
          onChange={(e) => setSelectedSubject(e.target.value)}
          className="px-4 py-2.5 rounded-xl bg-card-primary border border-border-charcoal text-text-primary text-xs focus:outline-none"
        >
          <option value="">All Subjects</option>
          <option value="Air Navigation">Air Navigation</option>
          <option value="Air Regulations">Air Regulations</option>
          <option value="Aviation Meteorology">Aviation Meteorology</option>
          <option value="Technical General">Technical General</option>
          <option value="Technical Specific">Technical Specific</option>
          <option value="RTR">RTR</option>
        </select>

        <select
          value={selectedDifficulty}
          onChange={(e) => setSelectedDifficulty(e.target.value)}
          className="px-4 py-2.5 rounded-xl bg-card-primary border border-border-charcoal text-text-primary text-xs focus:outline-none"
        >
          <option value="">All Difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      {/* Questions Table */}
      <div className="bg-card-primary border border-border-charcoal rounded-2xl overflow-hidden shadow-card">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-card-elevated border-b border-border-charcoal text-text-muted uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="p-3.5">ID</th>
                <th className="p-3.5">Subject</th>
                <th className="p-3.5">Topic</th>
                <th className="p-3.5">Question Prompt</th>
                <th className="p-3.5">Diff</th>
                <th className="p-3.5">Key</th>
                <th className="p-3.5 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-charcoal/40 text-text-secondary">
              {filtered.slice(0, 50).map((q) => (
                <tr key={q.id} className="hover:bg-surface-interactive/30">
                  <td className="p-3.5 font-mono font-bold text-brand-purple">{q.id}</td>
                  <td className="p-3.5 font-semibold text-white">{q.subject}</td>
                  <td className="p-3.5">{q.topic}</td>
                  <td className="p-3.5 max-w-xs truncate text-text-primary font-medium">
                    {q.question}
                  </td>
                  <td className="p-3.5">
                    <span className="uppercase font-bold text-[10px] px-2 py-0.5 rounded bg-surface-interactive text-text-muted">
                      {q.difficulty}
                    </span>
                  </td>
                  <td className="p-3.5 font-bold text-brand-green">
                    {["A", "B", "C", "D"][q.answerIndex || q.answer_index || 0]}
                  </td>
                  <td className="p-3.5 text-right">
                    <span className="inline-block px-2 py-0.5 rounded bg-brand-green/20 text-brand-green font-bold text-[10px]">
                      Approved
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="p-3.5 text-center text-xs text-text-muted border-t border-border-charcoal bg-card-elevated">
          Showing {Math.min(50, filtered.length)} of {filtered.length} matching questions
        </div>
      </div>

      {/* Add Question Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card-primary border border-border-charcoal rounded-2xl p-6 max-w-xl w-full max-h-[90vh] overflow-y-auto shadow-elevated space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-charcoal">
              <h3 className="text-base font-extrabold text-white">Add Validated Question</h3>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-text-muted hover:text-white font-bold text-lg"
              >
                &times;
              </button>
            </div>

            {formError && (
              <div className="p-3 rounded-xl bg-brand-red/10 border border-brand-red/30 text-brand-red text-xs font-bold">
                {formError}
              </div>
            )}
            {formSuccess && (
              <div className="p-3 rounded-xl bg-brand-green/10 border border-brand-green/30 text-brand-green text-xs font-bold">
                {formSuccess}
              </div>
            )}

            <form onSubmit={handleAddQuestion} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-text-muted font-bold mb-1">Subject</label>
                  <select
                    value={newSubj}
                    onChange={(e) => setNewSubj(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-card-elevated border border-border-charcoal text-white"
                  >
                    <option value="Air Navigation">Air Navigation</option>
                    <option value="Air Regulations">Air Regulations</option>
                    <option value="Aviation Meteorology">Aviation Meteorology</option>
                    <option value="Technical General">Technical General</option>
                    <option value="Technical Specific">Technical Specific</option>
                    <option value="RTR">RTR</option>
                  </select>
                </div>

                <div>
                  <label className="block text-text-muted font-bold mb-1">Difficulty</label>
                  <select
                    value={newDiff}
                    onChange={(e) => setNewDiff(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg bg-card-elevated border border-border-charcoal text-white"
                  >
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-text-muted font-bold mb-1">Topic / Chapter Name</label>
                <input
                  type="text"
                  required
                  value={newTopic}
                  onChange={(e) => setNewTopic(e.target.value)}
                  placeholder="e.g. Departure / Atmospheric Pressure"
                  className="w-full px-3 py-2 rounded-lg bg-card-elevated border border-border-charcoal text-white"
                />
              </div>

              <div>
                <label className="block text-text-muted font-bold mb-1">Question Prompt</label>
                <textarea
                  required
                  rows={3}
                  value={newQText}
                  onChange={(e) => setNewQText(e.target.value)}
                  placeholder="Enter unambiguous, factually supported question..."
                  className="w-full px-3 py-2 rounded-lg bg-card-elevated border border-border-charcoal text-white"
                />
              </div>

              {/* 4 Options */}
              <div className="space-y-2">
                <label className="block text-text-muted font-bold">Options (4 Required)</label>
                {newOpts.map((opt, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <span className="w-5 font-bold text-center text-text-muted">
                      {["A", "B", "C", "D"][i]}
                    </span>
                    <input
                      type="text"
                      required
                      value={opt}
                      onChange={(e) => {
                        const copy = [...newOpts];
                        copy[i] = e.target.value;
                        setNewOpts(copy);
                      }}
                      placeholder={`Option ${["A", "B", "C", "D"][i]}`}
                      className="flex-1 px-3 py-1.5 rounded-lg bg-card-elevated border border-border-charcoal text-white"
                    />
                    <label className="flex items-center gap-1 cursor-pointer">
                      <input
                        type="radio"
                        name="correctAnswer"
                        checked={newAnsIdx === i}
                        onChange={() => setNewAnsIdx(i)}
                      />
                      <span className="text-[10px] text-brand-green font-bold">Correct</span>
                    </label>
                  </div>
                ))}
              </div>

              <div>
                <label className="block text-text-muted font-bold mb-1">
                  Authoritative Explanation
                </label>
                <textarea
                  required
                  rows={2}
                  value={newExpl}
                  onChange={(e) => setNewExpl(e.target.value)}
                  placeholder="Explain why the right answer is correct..."
                  className="w-full px-3 py-2 rounded-lg bg-card-elevated border border-border-charcoal text-white"
                />
              </div>

              <div>
                <label className="block text-text-muted font-bold mb-1">
                  Official Source Citation
                </label>
                <input
                  type="text"
                  required
                  value={newSrc}
                  onChange={(e) => setNewSrc(e.target.value)}
                  placeholder="e.g. I.C. Joshi Aviation Meteorology, Chapter 2"
                  className="w-full px-3 py-2 rounded-lg bg-card-elevated border border-border-charcoal text-white"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-border-charcoal">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-lg bg-surface-interactive text-text-secondary font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-lg bg-brand-purple hover:bg-brand-purpleDark text-white font-extrabold shadow-card"
                >
                  Save & Validate Question
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
