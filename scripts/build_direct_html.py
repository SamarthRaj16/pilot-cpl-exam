import json
import os
import sys

BASE = r"c:\VS Code\Codes\dgcacpllearning"
q_path = os.path.join(BASE, "src", "data", "questions.json")

with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions from {q_path}")

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta name="description" content="DGCA CPL Exam Practice — Authentic questions from official aviation textbooks and DGCA syllabus.">
<title>DGCA CPL Exam Practice | Pilot Ground School</title>
<style>
/* ── Reset & Variables ─────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#f0f4f8;--surface:#ffffff;--surface2:#e8ecf1;--surface3:#dde3ea;
  --text:#1a1e2e;--text2:#5a6070;--text3:#8892a0;
  --border:#cdd3db;--border2:#b8c0ca;
  --primary:#1565c0;--primary-light:#e3f0fd;--primary-dark:#0d47a1;--primary-text:#fff;
  --accent:#0288d1;
  --correct:#2e7d32;--correct-bg:#e8f5e9;--correct-border:#a5d6a7;
  --wrong:#c62828;--wrong-bg:#ffebee;--wrong-border:#ef9a9a;
  --flag:#e65100;--flag-bg:#fff3e0;--flag-border:#ffcc80;
  --warn:#f57c00;
  --radius:12px;--radius-sm:8px;--radius-xs:6px;
  --shadow:0 2px 8px rgba(0,0,0,.08);--shadow-md:0 4px 16px rgba(0,0,0,.12);
  --font:'Segoe UI',system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
  --transition:.18s ease;
}
.dark{
  --bg:#0d1117;--surface:#161b25;--surface2:#1e2534;--surface3:#252d3e;
  --text:#e2e8f0;--text2:#8892a8;--text3:#5a6478;
  --border:#2a3448;--border2:#374055;
  --primary:#3b82f6;--primary-light:#1a2a4a;--primary-dark:#60a5fa;
  --correct:#4caf50;--correct-bg:#0d2b0d;--correct-border:#2e5c2e;
  --wrong:#ef5350;--wrong-bg:#2b0d0d;--wrong-border:#5c2e2e;
  --flag:#ff9800;--flag-bg:#2b1c00;--flag-border:#5c3c00;
  --shadow:0 2px 8px rgba(0,0,0,.35);--shadow-md:0 4px 20px rgba(0,0,0,.5);
}

/* ── Base ──────────────────────────────────────────────── */
html{font-size:16px;scroll-behavior:smooth}
body{
  font-family:var(--font);background:var(--bg);color:var(--text);
  min-height:100dvh;transition:background var(--transition),color var(--transition);
  -webkit-tap-highlight-color:transparent;line-height:1.5;
}
button{
  font-family:inherit;cursor:pointer;border:none;border-radius:var(--radius-sm);
  font-size:.95rem;transition:all var(--transition);outline:none;
}
button:focus-visible{outline:2px solid var(--primary);outline-offset:2px}
button:active{transform:scale(.97)}
input{font-family:inherit;outline:none}
input:focus{border-color:var(--primary)!important}

/* ── Layout ────────────────────────────────────────────── */
.wrap{max-width:740px;margin:0 auto;padding:12px 14px 32px}

/* ── Sticky Header ─────────────────────────────────────── */
.hdr{
  position:sticky;top:0;z-index:200;
  background:var(--surface);border-bottom:1px solid var(--border);
  padding:10px 16px;
  display:flex;align-items:center;justify-content:space-between;gap:8px;
}
.hdr-brand{display:flex;align-items:center;gap:10px}
.hdr-brand h1{font-size:1.05rem;font-weight:700;color:var(--primary);white-space:nowrap}
.hdr-brand h1 span{font-weight:400;color:var(--text2);font-size:.82rem;display:block;line-height:1.2}
.hdr-right{display:flex;gap:8px;align-items:center;flex-shrink:0}
.icon-btn{
  width:38px;height:38px;border-radius:50%;
  background:var(--surface2);color:var(--text);
  display:flex;align-items:center;justify-content:center;font-size:1.1rem;
  flex-shrink:0;
}
.icon-btn:hover{background:var(--primary-light);color:var(--primary)}

/* ── Screens ───────────────────────────────────────────── */
.screen{display:none}
.screen.active{display:block}

/* ── Card ──────────────────────────────────────────────── */
.card{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:18px;margin-bottom:14px;
  box-shadow:var(--shadow);
}
.card-title{
  font-size:.88rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.06em;color:var(--text2);margin-bottom:12px;
  display:flex;align-items:center;gap:6px;
}
.card-title .ct-icon{font-size:1rem}

/* ── HOME SCREEN ───────────────────────────────────────── */
.subject-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.subj-chip{
  padding:11px 14px;border-radius:var(--radius-sm);
  background:var(--surface2);color:var(--text);border:2px solid transparent;
  font-size:.88rem;font-weight:500;text-align:left;
  min-height:48px;display:flex;align-items:center;gap:6px;
  transition:all var(--transition);
}
.subj-chip .sc-icon{font-size:1.1rem;flex-shrink:0}
.subj-chip:hover{border-color:var(--primary);background:var(--primary-light)}
.subj-chip.selected{border-color:var(--primary);background:var(--primary-light);color:var(--primary);font-weight:600}
.subj-chip .sc-count{margin-left:auto;font-size:.78rem;color:var(--text3);font-weight:400}
.subj-chip.selected .sc-count{color:var(--primary)}

.mode-row{display:flex;gap:10px;flex-wrap:wrap}
.mode-btn{
  flex:1;min-width:140px;padding:13px 16px;
  background:var(--surface2);color:var(--text);
  border:2px solid transparent;font-weight:600;font-size:.95rem;
  text-align:center;min-height:50px;
  display:flex;align-items:center;justify-content:center;gap:6px;
}
.mode-btn:hover{border-color:var(--primary);background:var(--primary-light)}
.mode-btn.selected{border-color:var(--primary);background:var(--primary-light);color:var(--primary)}

.topic-filter{margin-top:12px}
.topic-filter label{font-size:.88rem;color:var(--text2);display:block;margin-bottom:6px}
.topic-select{
  width:100%;padding:10px 12px;border-radius:var(--radius-sm);
  border:1px solid var(--border);background:var(--surface);color:var(--text);
  font-size:.9rem;appearance:none;cursor:pointer;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23888' stroke-width='1.5' fill='none'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 12px center;
  padding-right:32px;
}

.timer-row{
  display:none;align-items:center;gap:10px;flex-wrap:wrap;margin-top:12px;
}
.timer-row.show{display:flex}
.timer-row label{font-size:.88rem;color:var(--text2)}
.timer-row input{
  width:80px;padding:9px;border-radius:var(--radius-sm);
  border:1px solid var(--border);background:var(--surface);
  color:var(--text);font-size:1rem;text-align:center;
}
.timer-row input:focus{border-color:var(--primary)}

.start-btn{
  width:100%;padding:16px;font-size:1.1rem;font-weight:700;
  background:var(--primary);color:#fff;margin-top:4px;min-height:54px;
  border-radius:var(--radius);display:flex;align-items:center;justify-content:center;gap:8px;
  box-shadow:0 2px 8px rgba(21,101,192,.3);
}
.start-btn:hover:not(:disabled){background:var(--primary-dark);box-shadow:0 4px 16px rgba(21,101,192,.4)}
.start-btn:disabled{opacity:.45;cursor:not-allowed;transform:none}

.stats-row{
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:8px;
}
.stats-text{font-size:.85rem;color:var(--text2)}
.danger-btn{
  padding:9px 14px;background:var(--wrong-bg);color:var(--wrong);
  border:1px solid var(--wrong-border);font-size:.84rem;font-weight:600;
  min-height:38px;border-radius:var(--radius-xs);
}
.danger-btn:hover{background:var(--wrong);color:#fff}

.wb-item{margin-bottom:10px}
.wb-label{display:flex;justify-content:space-between;font-size:.84rem;margin-bottom:4px;font-weight:500}
.wb-label .wb-pct{
  padding:1px 8px;border-radius:10px;font-size:.78rem;font-weight:600;
}
.wb-track{height:9px;border-radius:5px;background:var(--surface3);overflow:hidden}
.wb-fill{height:100%;border-radius:5px;transition:width .5s ease}

/* ── QUIZ SCREEN ───────────────────────────────────────── */
.quiz-meta{
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:8px;margin-bottom:12px;
}
.qm-left{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.subj-badge{
  font-size:.78rem;font-weight:700;padding:4px 12px;border-radius:12px;
  background:var(--primary-light);color:var(--primary);white-space:nowrap;
}
.topic-badge{
  font-size:.78rem;padding:4px 10px;border-radius:12px;
  background:var(--surface2);color:var(--text2);max-width:220px;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
}
.qm-right{display:flex;align-items:center;gap:8px}
.score-badge{
  font-size:.84rem;font-weight:700;padding:4px 10px;border-radius:12px;
  background:var(--correct-bg);color:var(--correct);border:1px solid var(--correct-border);
  white-space:nowrap;
}
.quiz-timer{
  font-size:.95rem;font-weight:700;font-variant-numeric:tabular-nums;
  color:var(--text);padding:4px 10px;background:var(--surface2);border-radius:8px;
  white-space:nowrap;flex-shrink:0;border:1px solid var(--border);
}
.quiz-timer.urgent{background:var(--wrong-bg);color:var(--wrong);border-color:var(--wrong-border)}

.progress-line{
  display:flex;align-items:center;justify-content:space-between;
  font-size:.84rem;color:var(--text2);margin-bottom:8px;
}
.progress-bar-track{
  height:5px;border-radius:3px;background:var(--surface3);
  margin-bottom:16px;overflow:hidden;
}
.progress-bar-fill{height:100%;border-radius:3px;background:var(--primary);transition:width .3s}

.diff-badge{
  font-size:.72rem;font-weight:700;padding:2px 8px;border-radius:10px;
  text-transform:uppercase;letter-spacing:.04em;
}
.diff-easy{background:#e8f5e9;color:#2e7d32}
.diff-medium{background:#fff3e0;color:#e65100}
.diff-hard{background:#ffebee;color:#c62828}
.dark .diff-easy{background:#0d2b0d;color:#66bb6a}
.dark .diff-medium{background:#2b1c00;color:#ff9800}
.dark .diff-hard{background:#2b0d0d;color:#ef5350}

.q-text{
  font-size:1.05rem;font-weight:500;line-height:1.65;margin-bottom:18px;
  color:var(--text);
}

.opts{display:flex;flex-direction:column;gap:10px;margin-bottom:16px}
.opt{
  width:100%;text-align:left;padding:13px 14px;
  background:var(--surface2);color:var(--text);
  border:2px solid var(--border);font-size:.95rem;
  min-height:50px;display:flex;align-items:center;gap:12px;
  line-height:1.4;border-radius:var(--radius-sm);
  position:relative;
}
.opt-letter{
  flex-shrink:0;width:30px;height:30px;border-radius:50%;
  background:var(--surface);border:1.5px solid var(--border2);
  display:flex;align-items:center;justify-content:center;
  font-weight:700;font-size:.84rem;color:var(--text2);
  transition:all var(--transition);
}
.opt-text{flex:1}
.opt-tag{
  flex-shrink:0;font-size:.78rem;font-weight:700;padding:3px 8px;
  border-radius:10px;margin-left:auto;white-space:nowrap;
}
.opt-tag.correct{background:var(--correct);color:#fff}
.opt-tag.wrong{background:var(--wrong);color:#fff}

.opt:hover:not(.disabled){border-color:var(--primary);background:var(--primary-light)}
.opt:hover:not(.disabled) .opt-letter{border-color:var(--primary);color:var(--primary)}
.opt.selected{border-color:var(--primary);background:var(--primary-light)}
.opt.selected .opt-letter{background:var(--primary);border-color:var(--primary);color:#fff}
.opt.correct{border-color:var(--correct);background:var(--correct-bg)}
.opt.correct .opt-letter{background:var(--correct);border-color:var(--correct);color:#fff}
.opt.wrong{border-color:var(--wrong);background:var(--wrong-bg)}
.opt.wrong .opt-letter{background:var(--wrong);border-color:var(--wrong);color:#fff}
.opt.disabled{cursor:default}

.feedback{
  display:none;padding:14px 16px;border-radius:var(--radius-sm);
  margin-bottom:16px;font-size:.9rem;line-height:1.55;animation:fadeIn .2s ease;
}
@keyframes fadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
.feedback.show{display:block}
.feedback-correct{background:var(--correct-bg);border:1px solid var(--correct-border)}
.feedback-wrong{background:var(--wrong-bg);border:1px solid var(--wrong-border)}
.feedback strong{display:block;margin-bottom:5px;font-size:.95rem}
.feedback-src{font-size:.8rem;color:var(--text2);margin-top:7px;font-style:italic}

.quiz-acts{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.quiz-acts button{flex:1;min-width:80px;padding:12px 10px;font-weight:600;min-height:46px}
.btn-nav{background:var(--surface2);color:var(--text);border:1px solid var(--border)}
.btn-nav:hover{border-color:var(--primary);color:var(--primary);background:var(--primary-light)}
.btn-flag{background:var(--surface2);color:var(--flag);border:1px solid var(--border)}
.btn-flag:hover{background:var(--flag-bg);border-color:var(--flag)}
.btn-flag.flagged{background:var(--flag-bg);color:var(--flag);border-color:var(--flag);font-weight:700}
.btn-finish{background:var(--primary);color:#fff;border:1px solid var(--primary-dark)}
.btn-finish:hover{background:var(--primary-dark)}
.btn-quit{background:var(--surface2);color:var(--wrong);border:1px solid var(--border);font-size:.85rem}
.btn-quit:hover{background:var(--wrong-bg);border-color:var(--wrong)}

.grid-toggle{
  text-align:center;font-size:.85rem;font-weight:600;
  color:var(--primary);padding:8px 0;cursor:pointer;user-select:none;
}
.q-grid{display:none;flex-wrap:wrap;gap:6px;padding:8px 0;justify-content:center}
.q-grid.open{display:flex}
.q-cell{
  width:38px;height:38px;border-radius:var(--radius-xs);
  font-size:.8rem;font-weight:600;
  display:flex;align-items:center;justify-content:center;
  background:var(--surface2);color:var(--text);cursor:pointer;
  border:2px solid transparent;transition:all var(--transition);
}
.q-cell:hover{border-color:var(--primary)}
.q-cell.current{border-color:var(--primary);color:var(--primary);background:var(--primary-light)}
.q-cell.answered{background:var(--primary);color:#fff;border-color:var(--primary)}
.q-cell.flagged{background:var(--flag-bg);color:var(--flag);border-color:var(--flag)}
.q-cell.answered.flagged{background:var(--flag);color:#fff;border-color:var(--flag)}
.grid-legend{
  display:flex;gap:12px;flex-wrap:wrap;justify-content:center;
  font-size:.76rem;color:var(--text2);padding:4px 0 10px;
}
.leg{display:flex;align-items:center;gap:4px}
.leg-dot{width:12px;height:12px;border-radius:3px}
.leg-dot.answered{background:var(--primary)}
.leg-dot.flagged{background:var(--flag)}
.leg-dot.current{background:transparent;border:2px solid var(--primary)}
.leg-dot.unanswered{background:var(--surface3)}

/* ── RESULTS SCREEN ────────────────────────────────────── */
.result-hero{text-align:center;padding:26px 16px 22px}
.result-points-label{font-size:.84rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--text2);margin-bottom:6px}
.result-grade{font-size:3.5rem;font-weight:900;line-height:1;color:var(--primary)}
.result-pct{font-size:1.3rem;font-weight:700;color:var(--text);margin:6px 0 8px}
.result-pass{
  display:inline-block;padding:6px 20px;border-radius:14px;
  font-size:.95rem;font-weight:700;margin-top:4px;
}
.result-pass.pass{background:var(--correct-bg);color:var(--correct);border:1px solid var(--correct-border)}
.result-pass.fail{background:var(--wrong-bg);color:var(--wrong);border:1px solid var(--wrong-border)}
.result-stats{font-size:.86rem;color:var(--text2);margin-top:12px}

.breakdown-item{margin-bottom:12px}
.bd-label{display:flex;justify-content:space-between;font-size:.85rem;margin-bottom:4px;font-weight:500}
.bd-track{height:12px;border-radius:6px;background:var(--surface3);overflow:hidden}
.bd-fill{height:100%;border-radius:6px;transition:width .6s ease}

.result-acts{display:flex;flex-direction:column;gap:10px}
.result-acts button{
  width:100%;padding:14px;font-size:.98rem;font-weight:600;
  min-height:50px;border-radius:var(--radius);
}
.btn-review{background:var(--surface2);color:var(--text);border:1px solid var(--border)}
.btn-review:hover{border-color:var(--primary);color:var(--primary);background:var(--primary-light)}
.btn-retry-wrong{background:var(--flag-bg);color:var(--flag);border:1px solid var(--flag-border)}
.btn-retry-wrong:hover{background:var(--flag);color:#fff}
.btn-retry-all{background:var(--primary);color:#fff}
.btn-retry-all:hover{background:var(--primary-dark)}
.btn-home{background:var(--surface2);color:var(--text);border:1px solid var(--border)}
.btn-home:hover{border-color:var(--border2);background:var(--surface3)}

.pass-info{
  padding:12px 16px;border-radius:var(--radius-sm);
  background:var(--primary-light);border:1px solid var(--border);
  font-size:.86rem;color:var(--text);margin-bottom:14px;line-height:1.5;
}

/* ── REVIEW SCREEN ─────────────────────────────────────── */
.review-item{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:16px;margin-bottom:12px;
  box-shadow:var(--shadow);border-left:4px solid var(--wrong);
}
.review-qnum{font-size:.78rem;font-weight:700;color:var(--text2);margin-bottom:6px}
.review-q{font-weight:600;margin-bottom:10px;line-height:1.5;font-size:.97rem}
.review-ans{font-size:.88rem;margin-bottom:4px;line-height:1.4}
.review-ans.your{color:var(--wrong)}
.review-ans.right{color:var(--correct);font-weight:600}
.review-expl{
  font-size:.86rem;color:var(--text2);margin-top:9px;
  padding-top:9px;border-top:1px solid var(--border);line-height:1.5;
}
.review-src{font-size:.8rem;color:var(--text3);font-style:italic;margin-top:4px}
.back-btn{
  padding:12px 20px;background:var(--surface2);color:var(--text);
  font-weight:600;min-height:46px;border:1px solid var(--border);
  border-radius:var(--radius-sm);width:100%;margin-top:4px;
}
.back-btn:hover{border-color:var(--primary);color:var(--primary);background:var(--primary-light)}

/* ── MODAL ─────────────────────────────────────────────── */
.modal-overlay{
  display:none;position:fixed;inset:0;
  background:rgba(0,0,0,.5);z-index:500;
  align-items:center;justify-content:center;padding:20px;
}
.modal-overlay.show{display:flex}
.modal-box{
  background:var(--surface);border-radius:var(--radius);
  padding:26px;max-width:380px;width:100%;
  box-shadow:var(--shadow-md);text-align:center;
  border:1px solid var(--border);
}
.modal-box p{margin-bottom:20px;font-size:.97rem;line-height:1.5;color:var(--text)}
.modal-btns{display:flex;gap:10px;justify-content:center}
.modal-btns button{padding:11px 26px;font-weight:600;min-height:44px;min-width:90px}
.btn-cancel{background:var(--surface2);color:var(--text);border:1px solid var(--border)}
.btn-cancel:hover{border-color:var(--border2)}
.btn-modal-confirm{background:var(--wrong);color:#fff}
.btn-modal-confirm:hover{background:#b71c1c}

/* ── Responsive ────────────────────────────────────────── */
@media(max-width:520px){
  .wrap{padding:10px 10px 28px}
  .card{padding:14px}
  .q-text{font-size:1rem}
  .opt{padding:11px 12px;font-size:.9rem}
  .quiz-acts button{font-size:.85rem;padding:10px 6px}
  .q-cell{width:34px;height:34px;font-size:.76rem}
  .subject-grid{grid-template-columns:repeat(auto-fill,minmax(130px,1fr))}
}

/* ── Scrollbar ─────────────────────────────────────────── */
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}

.mt-8{margin-top:8px}.mt-12{margin-top:12px}.mt-16{margin-top:16px}
.txt-center{text-align:center}
.txt-muted{color:var(--text2);font-size:.88rem}
</style>
</head>
<body>

<!-- ── HEADER ─────────────────────────────────────────── -->
<header class="hdr">
  <div class="hdr-brand">
    <h1>✈ CPL Practice <span>DGCA Written Exam</span></h1>
  </div>
  <div class="hdr-right">
    <button class="icon-btn" id="darkBtn" title="Toggle dark mode" aria-label="Toggle dark mode">🌙</button>
  </div>
</header>

<div class="wrap">

<!-- ═══════════════════════════════════════════════════════
     HOME SCREEN
═══════════════════════════════════════════════════════ -->
<div id="homeScreen" class="screen active">

  <div class="card">
    <div class="card-title"><span class="ct-icon">📚</span> Select Subject</div>
    <div class="subject-grid" id="subjGrid"></div>
  </div>

  <div class="card">
    <div class="card-title"><span class="ct-icon">🎯</span> Quiz Mode</div>
    <div class="mode-row">
      <button class="mode-btn selected" data-mode="practice">📝 Practice <span style="display:block;font-size:.75rem;font-weight:400;color:var(--text2)">Instant feedback + points</span></button>
      <button class="mode-btn" data-mode="timed">⏱ Timed <span style="display:block;font-size:.75rem;font-weight:400;color:var(--text2)">Timed paper</span></button>
      <button class="mode-btn" data-mode="mock">📋 Mock Exam <span style="display:block;font-size:.75rem;font-weight:400;color:var(--text2)">DGCA CBT scheme</span></button>
    </div>
    <div class="timer-row" id="timerRow">
      <label for="timerMin">Duration (minutes):</label>
      <input type="number" id="timerMin" value="30" min="5" max="180">
    </div>
    <div class="topic-filter">
      <label for="topicSel">Filter by topic (optional):</label>
      <select class="topic-select" id="topicSel">
        <option value="">All topics</option>
      </select>
    </div>
  </div>

  <div class="card" id="weakCard" style="display:none">
    <div class="card-title"><span class="ct-icon">📊</span> Weak Areas (Based on Points Scored)</div>
    <div id="weakPanel"></div>
  </div>

  <button class="start-btn" id="startBtn" disabled>
    <span>🚀</span><span id="startLabel">Start Quiz</span>
  </button>

  <div class="card mt-12">
    <div class="stats-row">
      <span class="stats-text" id="statsLine">No attempts yet.</span>
      <button class="danger-btn" id="resetBtn">🗑 Reset Progress</button>
    </div>
  </div>

</div>

<!-- ═══════════════════════════════════════════════════════
     QUIZ SCREEN
═══════════════════════════════════════════════════════ -->
<div id="quizScreen" class="screen">

  <div class="quiz-meta">
    <div class="qm-left">
      <span class="subj-badge" id="qSubjectBadge"></span>
      <span class="topic-badge" id="qTopicBadge"></span>
    </div>
    <div class="qm-right">
      <span class="score-badge" id="qScoreBadge">🎯 Points: 0 / 0</span>
      <span class="quiz-timer" id="qTimer"></span>
    </div>
  </div>

  <div class="progress-line">
    <span id="qProgressText"></span>
    <span id="qDiffBadge"></span>
  </div>
  <div class="progress-bar-track"><div class="progress-bar-fill" id="qProgressBar"></div></div>

  <div class="q-text" id="qText"></div>
  <div class="opts" id="qOpts"></div>
  <div class="feedback" id="qFeedback"></div>

  <div class="quiz-acts">
    <button class="btn-nav" id="prevBtn">◀ Prev</button>
    <button class="btn-flag" id="flagBtn">🚩 Flag</button>
    <button class="btn-nav" id="nextBtn">Next ▶</button>
  </div>
  <div class="quiz-acts">
    <button class="btn-finish" id="finishBtn">✅ Finish Quiz</button>
    <button class="btn-quit" id="quitBtn">✖ Quit</button>
  </div>

  <div class="grid-toggle" id="gridToggle">▼ Question Navigator</div>
  <div class="q-grid" id="qGrid"></div>
  <div class="grid-legend" id="gridLegend" style="display:none">
    <span class="leg"><span class="leg-dot answered"></span>Answered</span>
    <span class="leg"><span class="leg-dot flagged"></span>Flagged</span>
    <span class="leg"><span class="leg-dot current"></span>Current</span>
    <span class="leg"><span class="leg-dot unanswered"></span>Unanswered</span>
  </div>

</div>

<!-- ═══════════════════════════════════════════════════════
     RESULTS SCREEN
═══════════════════════════════════════════════════════ -->
<div id="resultScreen" class="screen">

  <div class="card result-hero">
    <div class="result-points-label">Total Points Received</div>
    <div class="result-grade" id="rScore">0 / 0</div>
    <div class="result-pct" id="rPct">0%</div>
    <div id="rPassBadge"></div>
    <div class="result-stats" id="rStats"></div>
  </div>

  <div class="card" id="rBreakdownCard">
    <div class="card-title"><span class="ct-icon">📊</span> Points & Accuracy per Subject</div>
    <div id="rBreakdown"></div>
  </div>

  <div class="card" id="rTopicCard">
    <div class="card-title"><span class="ct-icon">📌</span> Points per Topic</div>
    <div id="rTopicBreakdown"></div>
  </div>

  <div class="pass-info" id="rPassInfo"></div>

  <div class="result-acts">
    <button class="btn-review" id="reviewBtn">🔍 Review Mistakes</button>
    <button class="btn-retry-wrong" id="retryWrongBtn">🔄 Retry Wrong Questions</button>
    <button class="btn-retry-all" id="retryAllBtn">🔁 Retry Same Set</button>
    <button class="btn-home" id="homeFromResult">🏠 Back to Home</button>
  </div>

</div>

<!-- ═══════════════════════════════════════════════════════
     REVIEW SCREEN
═══════════════════════════════════════════════════════ -->
<div id="reviewScreen" class="screen">
  <div class="card-title" style="margin-bottom:12px"><span class="ct-icon">🔍</span> Review Mistakes</div>
  <div id="reviewList"></div>
  <button class="back-btn" id="backFromReview">◀ Back to Results</button>
</div>

</div><!-- /wrap -->

<!-- ── MODAL ──────────────────────────────────────────── -->
<div class="modal-overlay" id="modal" role="dialog" aria-modal="true">
  <div class="modal-box">
    <p id="modalMsg"></p>
    <div class="modal-btns">
      <button class="btn-cancel" id="modalCancel">Cancel</button>
      <button class="btn-modal-confirm" id="modalConfirm">Confirm</button>
    </div>
  </div>
</div>

<script>
/* ══════════════════════════════════════════════════════
   EXAM CONFIG (Official DGCA Scheme)
══════════════════════════════════════════════════════ */
const EXAM_CONFIG = {
  passMark: 70, // DGCA requires 70% in each paper
  negativeMarking: false,
  subjects: {
    "Air Navigation":       { questions: 100, duration: 180 },
    "Aviation Meteorology": { questions: 50,  duration: 120 },
    "Air Regulations":      { questions: 50,  duration: 90  },
    "Technical General":    { questions: 100, duration: 150 },
    "Technical Specific":   { questions: 50,  duration: 90  },
    "RTR":                  { questions: 50,  duration: 60  },
  }
};

/* ══════════════════════════════════════════════════════
   EMBEDDED QUESTION BANK (230 questions across all 6 subjects)
══════════════════════════════════════════════════════ */
const QUESTIONS = ''' + json.dumps(questions, ensure_ascii=False, indent=2) + ''';

/* ══════════════════════════════════════════════════════
   SUBJECT META
══════════════════════════════════════════════════════ */
const SUBJECT_META = {
  "Air Navigation":       { icon: "🧭", color: "#1565c0" },
  "Air Regulations":      { icon: "📜", color: "#6a1b9a" },
  "Aviation Meteorology": { icon: "⛅", color: "#0277bd" },
  "Technical General":    { icon: "⚙️", color: "#2e7d32" },
  "Technical Specific":   { icon: "✈️", color: "#c62828" },
  "RTR":                  { icon: "📻", color: "#00838f" },
};
const ALL_SUBJECTS = Object.keys(SUBJECT_META);

/* ══════════════════════════════════════════════════════
   SAFE STORAGE
══════════════════════════════════════════════════════ */
function sg(k,f){try{const v=localStorage.getItem(k);return v!==null?JSON.parse(v):f}catch{return f}}
function ss(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch{}}
function sd(k){try{localStorage.removeItem(k)}catch{}}

/* ══════════════════════════════════════════════════════
   APP STATE
══════════════════════════════════════════════════════ */
let state = {
  selSubjects: [],  // empty = all
  mode: "practice",
  timerMin: 30,
  topicFilter: "",
  pool: [],           // original filtered questions
  questions: [],      // current quiz questions (shuffled options + order)
  idx: 0,
  answers: [],        // -1 = unanswered
  flags: [],
  revealed: [],       // practice mode: revealed
  startTime: 0,
  endTime: 0,
  timerSec: 0,
  timerInterval: null,
  gridOpen: false,
  finished: false,
};

let history = sg("cpl_history", {});
let darkMode = sg("cpl_dark", false);

/* ══════════════════════════════════════════════════════
   DARK MODE
══════════════════════════════════════════════════════ */
function applyDark(){
  document.body.classList.toggle("dark", darkMode);
  document.getElementById("darkBtn").textContent = darkMode ? "☀️" : "🌙";
}
applyDark();
document.getElementById("darkBtn").addEventListener("click", () => {
  darkMode = !darkMode; ss("cpl_dark", darkMode); applyDark();
});

/* ══════════════════════════════════════════════════════
   SCREEN MANAGER
══════════════════════════════════════════════════════ */
const SCREENS = ["homeScreen","quizScreen","resultScreen","reviewScreen"];
function showScreen(name){
  SCREENS.forEach(s => document.getElementById(s).classList.remove("active"));
  document.getElementById(name).classList.add("active");
  window.scrollTo(0,0);
}

/* ══════════════════════════════════════════════════════
   SHUFFLE & PREPARE QUESTION
══════════════════════════════════════════════════════ */
function shuffle(arr){
  const a=[...arr];
  for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
  return a;
}

function prepQ(q){
  const idxs = q.options.map((_,i)=>i);
  const sh = shuffle(idxs);
  const origAns = q.answerIndex !== undefined ? q.answerIndex : (q.answer !== undefined ? q.answer : 0);
  return {
    ...q,
    _origOptions: q._origOptions || q.options,
    _origAnswerIndex: origAns,
    options: sh.map(i=>q.options[i]),
    answer: sh.indexOf(origAns),
  };
}

/* ══════════════════════════════════════════════════════
   HOME — BUILD SUBJECT CHIPS
══════════════════════════════════════════════════════ */
function buildSubjectChips(){
  const grid = document.getElementById("subjGrid");
  grid.innerHTML = "";

  const allBtn = document.createElement("button");
  allBtn.className = "subj-chip" + (state.selSubjects.length===0?" selected":"");
  allBtn.innerHTML = `<span class="sc-icon">📚</span>All Subjects<span class="sc-count">${QUESTIONS.length}</span>`;
  allBtn.addEventListener("click", ()=>{ state.selSubjects=[]; buildSubjectChips(); updateHome(); });
  grid.appendChild(allBtn);

  ALL_SUBJECTS.forEach(subj => {
    const count = QUESTIONS.filter(q=>q.subject===subj).length;
    if(count===0) return;
    const meta = SUBJECT_META[subj]||{icon:"📖",color:"#555"};
    const btn = document.createElement("button");
    btn.className = "subj-chip" + (state.selSubjects.includes(subj)?" selected":"");
    btn.innerHTML = `<span class="sc-icon">${meta.icon}</span>${subj}<span class="sc-count">${count}</span>`;
    btn.addEventListener("click", ()=>{
      const i = state.selSubjects.indexOf(subj);
      if(i>=0) state.selSubjects.splice(i,1); else state.selSubjects.push(subj);
      buildSubjectChips(); updateHome();
    });
    grid.appendChild(btn);
  });
}

/* ══════════════════════════════════════════════════════
   HOME — TOPIC DROPDOWN
══════════════════════════════════════════════════════ */
function buildTopicDropdown(){
  const sel = document.getElementById("topicSel");
  const current = sel.value;
  const subs = state.selSubjects.length>0 ? state.selSubjects : ALL_SUBJECTS;
  const topics = [...new Set(QUESTIONS.filter(q=>subs.includes(q.subject)).map(q=>q.topic))].sort();
  sel.innerHTML = `<option value="">All topics</option>`;
  topics.forEach(t => {
    const opt = document.createElement("option");
    opt.value = t; opt.textContent = t;
    if(t===current) opt.selected=true;
    sel.appendChild(opt);
  });
  state.topicFilter = sel.value;
}

document.getElementById("topicSel").addEventListener("change", e => {
  state.topicFilter = e.target.value; updateStartBtn();
});

/* ══════════════════════════════════════════════════════
   HOME — MODE SELECTOR
══════════════════════════════════════════════════════ */
document.querySelectorAll(".mode-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach(b=>b.classList.remove("selected"));
    btn.classList.add("selected");
    state.mode = btn.dataset.mode;
    document.getElementById("timerRow").classList.toggle("show", state.mode==="timed");
    updateStartBtn();
  });
});

/* ══════════════════════════════════════════════════════
   HOME — START BTN & POOL
══════════════════════════════════════════════════════ */
function getFilteredPool(){
  const subs = state.selSubjects.length>0 ? state.selSubjects : ALL_SUBJECTS;
  return QUESTIONS.filter(q =>
    subs.includes(q.subject) &&
    (!state.topicFilter || q.topic === state.topicFilter)
  );
}

function updateStartBtn(){
  const pool = getFilteredPool();
  const n = pool.length;
  const btn = document.getElementById("startBtn");
  const label = document.getElementById("startLabel");
  btn.disabled = n===0;
  if(n===0) label.textContent = "No questions for this selection";
  else label.textContent = `Start Quiz (${n} question${n!==1?"s":""})`;
}

function updateHome(){
  buildTopicDropdown();
  updateStartBtn();
  renderWeakness();
  renderStats();
}

document.getElementById("startBtn").addEventListener("click", () => {
  const pool = getFilteredPool();
  if(pool.length===0) return;
  state.timerMin = parseInt(document.getElementById("timerMin").value)||30;

  if(state.mode === "mock"){
    const subs = state.selSubjects.length>0 ? state.selSubjects : ALL_SUBJECTS;
    let mockPool = [];
    subs.forEach(subj => {
      const cfg = EXAM_CONFIG.subjects[subj];
      const available = pool.filter(q=>q.subject===subj);
      if(available.length===0) return;
      const count = Math.min(cfg ? cfg.questions : 50, available.length);
      mockPool = mockPool.concat(shuffle(available).slice(0, count));
    });
    if(mockPool.length===0){ alert("No questions available."); return; }
    let totalMin = 0;
    subs.forEach(subj => {
      const cfg = EXAM_CONFIG.subjects[subj];
      if(cfg) totalMin += cfg.duration;
    });
    state.timerMin = Math.max(totalMin, 30);
    startQuiz(mockPool);
  } else {
    startQuiz(pool);
  }
});

/* ══════════════════════════════════════════════════════
   HOME — WEAKNESS & STATS
══════════════════════════════════════════════════════ */
function renderWeakness(){
  const card = document.getElementById("weakCard");
  const panel = document.getElementById("weakPanel");
  const entries = [];
  ALL_SUBJECTS.forEach(subj => {
    const h = history[subj];
    if(h && h.attempted>0){
      entries.push({subj, pct: Math.round(100*h.correct/h.attempted), correct:h.correct, attempted:h.attempted});
    }
  });
  if(entries.length===0){ card.style.display="none"; return; }
  card.style.display="";
  entries.sort((a,b)=>a.pct-b.pct);
  panel.innerHTML = entries.map(e => {
    const clr = e.pct>=70 ? "var(--correct)" : e.pct>=40 ? "var(--warn)" : "var(--wrong)";
    const bg = e.pct>=70 ? "var(--correct-bg)" : e.pct>=40 ? "var(--flag-bg)" : "var(--wrong-bg)";
    const meta = SUBJECT_META[e.subj]||{icon:"📖"};
    return `<div class="wb-item">
      <div class="wb-label">
        <span>${meta.icon} ${e.subj}</span>
        <span class="wb-pct" style="background:${bg};color:${clr}">${e.correct}/${e.attempted} pts (${e.pct}%)</span>
      </div>
      <div class="wb-track"><div class="wb-fill" style="width:${e.pct}%;background:${clr}"></div></div>
    </div>`;
  }).join("");
}

function renderStats(){
  let ta=0,tc=0;
  Object.values(history).forEach(h=>{ ta+=h.attempted; tc+=h.correct; });
  const el = document.getElementById("statsLine");
  if(ta===0){ el.textContent="No attempts yet."; return; }
  el.textContent=`${ta} questions attempted · Total points: ${tc}/${ta} (${Math.round(100*tc/ta)}% overall accuracy)`;
}

/* ══════════════════════════════════════════════════════
   RESET
══════════════════════════════════════════════════════ */
document.getElementById("resetBtn").addEventListener("click", ()=>{
  showModal("Reset ALL progress and points history? This cannot be undone.", ()=>{
    history={}; sd("cpl_history");
    renderWeakness(); renderStats();
  });
});

/* ══════════════════════════════════════════════════════
   START QUIZ
══════════════════════════════════════════════════════ */
function startQuiz(pool, retryWrong=false){
  state.pool = pool;
  const shuffled = shuffle(pool).map(prepQ);
  state.questions = shuffled;
  state.idx = 0;
  state.answers = new Array(shuffled.length).fill(-1);
  state.flags = new Array(shuffled.length).fill(false);
  state.revealed = new Array(shuffled.length).fill(false);
  state.startTime = Date.now();
  state.endTime = 0;
  state.finished = false;
  state.gridOpen = false;

  if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval=null; }

  if(state.mode==="timed" || state.mode==="mock"){
    state.timerSec = state.timerMin * 60;
    state.timerInterval = setInterval(()=>{
      state.timerSec--;
      renderTimer();
      if(state.timerSec<=0){ clearInterval(state.timerInterval); state.timerInterval=null; finishQuiz(); }
    }, 1000);
  } else {
    state.timerSec = 0;
  }

  showScreen("quizScreen");
  document.getElementById("qGrid").innerHTML = "";
  buildGrid();
  renderQuestion();
}

/* ══════════════════════════════════════════════════════
   TIMER & SCORE BAR
══════════════════════════════════════════════════════ */
function renderTimer(){
  const el = document.getElementById("qTimer");
  if(state.mode==="timed" || state.mode==="mock"){
    const m = Math.floor(state.timerSec/60);
    const s = state.timerSec%60;
    el.textContent = `⏱ ${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
    el.classList.toggle("urgent", state.timerSec<=60);
  } else {
    const elapsed = Math.floor((Date.now()-state.startTime)/1000);
    const m = Math.floor(elapsed/60);
    const s = elapsed%60;
    el.textContent = `⏱ ${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
    el.classList.remove("urgent");
  }
}

function updateScoreBadge(){
  const sb = document.getElementById("qScoreBadge");
  if(state.mode === "practice"){
    const attempted = state.revealed.filter(r => r).length;
    const correct = state.questions.filter((q, i) => state.revealed[i] && state.answers[i] === q.answer).length;
    const total = state.questions.length;
    if(attempted === 0){
      sb.textContent = `🎯 Points: 0 / ${total} (0%)`;
    } else {
      const pct = Math.round(100 * correct / attempted);
      sb.textContent = `🎯 Points: ${correct} / ${attempted} (${pct}%) · Total: ${total} Qs`;
    }
    sb.style.display = "";
  } else {
    const answeredCount = state.answers.filter(a => a >= 0).length;
    sb.textContent = `📝 Answered: ${answeredCount} / ${state.questions.length}`;
    sb.style.display = "";
  }
}

setInterval(()=>{
  if(document.getElementById("quizScreen").classList.contains("active") &&
     state.mode==="practice" && !state.finished) renderTimer();
}, 1000);

/* ══════════════════════════════════════════════════════
   RENDER QUESTION & OPTION STATES
══════════════════════════════════════════════════════ */
const LETTERS = ["A","B","C","D","E","F","G","H"];

function renderQuestion(){
  const q = state.questions[state.idx];
  const i = state.idx;
  const n = state.questions.length;
  const meta = SUBJECT_META[q.subject]||{icon:"📖",color:"#555"};

  document.getElementById("qSubjectBadge").textContent = `${meta.icon} ${q.subject}`;
  document.getElementById("qTopicBadge").textContent = q.topic||"";
  document.getElementById("qProgressText").textContent = `Question ${i+1} of ${n}`;
  document.getElementById("qProgressBar").style.width = `${((i+1)/n)*100}%`;

  const diff = q.difficulty||"medium";
  const diffEl = document.getElementById("qDiffBadge");
  diffEl.className = `diff-badge diff-${diff}`;
  diffEl.textContent = diff.charAt(0).toUpperCase()+diff.slice(1);

  document.getElementById("qText").textContent = `${i+1}. ${q.question}`;
  renderTimer();
  updateScoreBadge();

  const opts = document.getElementById("qOpts");
  opts.innerHTML = "";
  const answered = state.answers[i]>=0;
  const revealed = state.revealed[i];
  
  // In practice mode, lock once revealed. In timed/mock mode, allow changing until finished.
  const isLocked = state.finished || (state.mode==="practice" && revealed);

  q.options.forEach((opt, oi)=>{
    const btn = document.createElement("button");
    btn.className = "opt";
    if(isLocked) btn.classList.add("disabled");

    let tagHtml = "";

    if(state.mode==="practice" && revealed){
      if(oi===q.answer){
        btn.classList.add("correct");
        tagHtml = `<span class="opt-tag correct">✓ Correct (+1 pt)</span>`;
      } else if(oi===state.answers[i]){
        btn.classList.add("wrong");
        tagHtml = `<span class="opt-tag wrong">✗ Your Choice (0 pts)</span>`;
      }
    } else if(answered){
      if(oi===state.answers[i]){
        btn.classList.add("selected");
        tagHtml = `<span class="opt-tag" style="background:var(--primary);color:#fff">Selected</span>`;
      }
    }

    btn.innerHTML = `<span class="opt-letter">${LETTERS[oi]}</span><span class="opt-text">${opt}</span>${tagHtml}`;
    btn.addEventListener("click", ()=>selectOpt(oi));
    opts.appendChild(btn);
  });

  // Feedback Box (Practice Mode)
  const fb = document.getElementById("qFeedback");
  fb.className = "feedback";
  fb.innerHTML = "";
  if(state.mode==="practice" && revealed){
    const correct = state.answers[i]===q.answer;
    fb.classList.add("show", correct?"feedback-correct":"feedback-wrong");
    fb.innerHTML = `<strong>${correct ? "✅ Correct! (+1 Point Received)" : "❌ Incorrect (0 Points) — The correct answer is " + LETTERS[q.answer] + ": " + q.options[q.answer]}</strong>${q.explanation}<div class="feedback-src">📖 Source: ${q.source}</div>`;
  }

  // Flag button
  const fl = document.getElementById("flagBtn");
  fl.classList.toggle("flagged", state.flags[i]);
  fl.textContent = state.flags[i] ? "🚩 Flagged" : "🚩 Flag";

  document.getElementById("prevBtn").disabled = i===0;
  document.getElementById("nextBtn").textContent = i===n-1 ? "Review / Finish ▶" : "Next ▶";

  updateGridHighlight();
}

/* ══════════════════════════════════════════════════════
   SELECT OPTION
══════════════════════════════════════════════════════ */
function selectOpt(oi){
  const i = state.idx;
  if(state.finished) return;
  if(state.mode==="practice" && state.revealed[i]) return;

  state.answers[i] = oi;
  if(state.mode==="practice"){
    state.revealed[i] = true;
  }
  renderQuestion();
  updateGridHighlight();
}

/* ══════════════════════════════════════════════════════
   NAVIGATION
══════════════════════════════════════════════════════ */
document.getElementById("prevBtn").addEventListener("click", ()=>{
  if(state.idx>0){ state.idx--; renderQuestion(); }
});
document.getElementById("nextBtn").addEventListener("click", ()=>{
  if(state.idx<state.questions.length-1){
    state.idx++; renderQuestion();
  } else {
    // If on last question, click finish
    document.getElementById("finishBtn").click();
  }
});
document.getElementById("flagBtn").addEventListener("click", ()=>{
  state.flags[state.idx] = !state.flags[state.idx];
  renderQuestion(); updateGridHighlight();
});

/* ══════════════════════════════════════════════════════
   QUESTION GRID (NAVIGATOR)
══════════════════════════════════════════════════════ */
function buildGrid(){
  const wrap = document.getElementById("qGrid");
  wrap.innerHTML = "";
  state.questions.forEach((_, qi)=>{
    const c = document.createElement("div");
    c.className = "q-cell";
    c.textContent = qi+1;
    c.addEventListener("click", ()=>{ state.idx=qi; renderQuestion(); });
    wrap.appendChild(c);
  });
  updateGridHighlight();
}

function updateGridHighlight(){
  const cells = document.getElementById("qGrid").children;
  for(let qi=0;qi<cells.length;qi++){
    const c = cells[qi];
    c.className = "q-cell";
    if(qi===state.idx) c.classList.add("current");
    if(state.answers[qi]>=0) c.classList.add("answered");
    if(state.flags[qi]) c.classList.add("flagged");
  }
}

document.getElementById("gridToggle").addEventListener("click", ()=>{
  state.gridOpen = !state.gridOpen;
  const grid = document.getElementById("qGrid");
  const legend = document.getElementById("gridLegend");
  grid.classList.toggle("open", state.gridOpen);
  legend.style.display = state.gridOpen?"flex":"none";
  document.getElementById("gridToggle").textContent = state.gridOpen?"▲ Question Navigator":"▼ Question Navigator";
});

/* ══════════════════════════════════════════════════════
   FINISH & MODAL
══════════════════════════════════════════════════════ */
document.getElementById("finishBtn").addEventListener("click", ()=>{
  const unanswered = state.answers.filter(a=>a<0).length;
  const flagged = state.flags.filter(f=>f).length;
  let msg = "Submit your quiz and calculate points?";
  if(unanswered>0) msg=`You have ${unanswered} unanswered question${unanswered>1?"s":""}. Submit anyway?`;
  if(flagged>0) msg+=` (${flagged} flagged for review)`;
  showModal(msg, finishQuiz);
});

document.getElementById("quitBtn").addEventListener("click", ()=>{
  showModal("Quit this quiz? Progress will not be saved.", ()=>{
    if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval=null; }
    renderWeakness(); renderStats();
    showScreen("homeScreen");
  });
});

function finishQuiz(){
  if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval=null; }
  state.endTime = Date.now();
  state.finished = true;

  // Save history & points
  state.questions.forEach((q,qi)=>{
    if(state.answers[qi]<0) return;
    if(!history[q.subject]) history[q.subject]={attempted:0,correct:0,topics:{}};
    history[q.subject].attempted++;
    if(state.answers[qi]===q.answer) history[q.subject].correct++;

    if(!history[q.subject].topics) history[q.subject].topics={};
    const t = q.topic||"General";
    if(!history[q.subject].topics[t]) history[q.subject].topics[t]={attempted:0,correct:0};
    history[q.subject].topics[t].attempted++;
    if(state.answers[qi]===q.answer) history[q.subject].topics[t].correct++;
  });
  ss("cpl_history", history);
  showResults();
}

/* ══════════════════════════════════════════════════════
   RESULTS & POINTS BREAKDOWN
══════════════════════════════════════════════════════ */
function showResults(){
  showScreen("resultScreen");
  const n = state.questions.length;
  const answered = state.answers.filter(a=>a>=0).length;
  const correct = state.questions.filter((q,i)=>state.answers[i]===q.answer).length;
  const points = correct; // 1 mark per question
  const pct = n>0 ? Math.round(100*points/n) : 0;
  const elapsed = Math.floor((state.endTime-state.startTime)/1000);
  const em = Math.floor(elapsed/60), es = elapsed%60;

  document.getElementById("rScore").textContent = `${points} / ${n}`;
  document.getElementById("rPct").textContent = `${pct}% Accuracy (${points} Points Received)`;

  const pass = pct >= EXAM_CONFIG.passMark;
  const minNeeded = Math.ceil(n * 0.70);
  const pb = document.getElementById("rPassBadge");
  pb.innerHTML = `<span class="result-pass ${pass?"pass":"fail"}">${pass ? `✅ PASS — Scored ${points} pts (≥ 70% DGCA Requirement)` : `❌ FAIL — Scored ${points} pts (${minNeeded} points needed to pass)`}</span>`;

  document.getElementById("rStats").textContent =
    `⏱ Time Taken: ${em}m ${es}s · Answered: ${answered} of ${n} · Pass Criterion: ${EXAM_CONFIG.passMark}% (${minNeeded} pts required)`;

  // Subject breakdown with Points
  const subjMap = {};
  state.questions.forEach((q,i)=>{
    if(!subjMap[q.subject]) subjMap[q.subject]={t:0,c:0};
    subjMap[q.subject].t++;
    if(state.answers[i]===q.answer) subjMap[q.subject].c++;
  });
  const colors=["#1565c0","#6a1b9a","#0277bd","#2e7d32","#c62828","#00838f"];
  let bi=0;
  document.getElementById("rBreakdown").innerHTML =
    Object.entries(subjMap).map(([subj,d])=>{
      const p=Math.round(100*d.c/d.t);
      const clr=colors[bi++%colors.length];
      const isPass = p >= EXAM_CONFIG.passMark;
      const passTag = isPass ?
        `<span style="color:var(--correct);font-weight:700">✓ PASS</span>` :
        `<span style="color:var(--wrong);font-weight:700">✗ FAIL</span>`;
      return `<div class="breakdown-item">
        <div class="bd-label">
          <span>${SUBJECT_META[subj]?.icon||""} ${subj} (${passTag})</span>
          <span><strong>${d.c} / ${d.t} points</strong> (${p}%)</span>
        </div>
        <div class="bd-track"><div class="bd-fill" style="width:${p}%;background:${clr}"></div></div>
      </div>`;
    }).join("");

  // Topic breakdown with Points
  const topicMap = {};
  state.questions.forEach((q,i)=>{
    const t = q.topic||"General";
    if(!topicMap[t]) topicMap[t]={t:0,c:0,subj:q.subject};
    topicMap[t].t++;
    if(state.answers[i]===q.answer) topicMap[t].c++;
  });
  const topicEntries = Object.entries(topicMap).sort((a,b)=>(a[1].c/a[1].t)-(b[1].c/b[1].t));
  document.getElementById("rTopicBreakdown").innerHTML =
    topicEntries.map(([topic,d])=>{
      const p=Math.round(100*d.c/d.t);
      const clr = p>=70?"var(--correct)":p>=40?"var(--warn)":"var(--wrong)";
      return `<div class="breakdown-item">
        <div class="bd-label" style="font-size:.84rem">
          <span>${topic}</span>
          <span>${d.c} / ${d.t} pts (${p}%)</span>
        </div>
        <div class="bd-track" style="height:8px"><div class="bd-fill" style="width:${p}%;background:${clr}"></div></div>
      </div>`;
    }).join("");

  document.getElementById("rPassInfo").innerHTML =
    `ℹ️ <strong>DGCA Exam Scheme:</strong> Passing mark is <strong>70%</strong> in each paper independently. There is <strong>no negative marking</strong> (unattempted questions earn 0 marks). Results are valid for 5 years.`;

  const missedCount = state.questions.filter((q,i)=>state.answers[i]!==q.answer).length;
  document.getElementById("retryWrongBtn").style.display = missedCount>0?"":"none";
  document.getElementById("retryWrongBtn").textContent = `🔄 Retry ${missedCount} Missed Question${missedCount!==1?"s":""}`;
  document.getElementById("reviewBtn").style.display = missedCount>0?"":"none";
  document.getElementById("reviewBtn").textContent = `🔍 Review ${missedCount} Mistake${missedCount!==1?"s":""}`;
}

/* ══════════════════════════════════════════════════════
   REVIEW MISTAKES SCREEN
══════════════════════════════════════════════════════ */
document.getElementById("reviewBtn").addEventListener("click", ()=>{
  showScreen("reviewScreen");
  const list = document.getElementById("reviewList");
  list.innerHTML = "";
  state.questions.forEach((q,i)=>{
    if(state.answers[i]===q.answer) return;
    const userChoice = state.answers[i];
    const correctChoice = q.answer;
    const div = document.createElement("div");
    div.className = "review-item";
    const yourAnsText = userChoice >= 0 ?
      `❌ Your Choice: <strong>${LETTERS[userChoice]}. ${q.options[userChoice]}</strong> (0 points received)` :
      `⚠️ Your Choice: <strong>Unanswered / Skipped</strong> (0 points received)`;
    div.innerHTML = `
      <div class="review-qnum">Question ${i+1} of ${state.questions.length} · ${q.subject} · ${q.topic||""}</div>
      <div class="review-q">${q.question}</div>
      <div class="review-ans your">${yourAnsText}</div>
      <div class="review-ans right">✅ Correct Answer: <strong>${LETTERS[correctChoice]}. ${q.options[correctChoice]}</strong> (+1 point)</div>
      <div class="review-expl"><strong>Explanation:</strong> ${q.explanation}</div>
      <div class="review-src">📖 Reference: ${q.source}</div>`;
    list.appendChild(div);
  });
  if(!list.children.length){
    list.innerHTML = '<div class="txt-center" style="padding:30px"><div style="font-size:2.5rem">🎉</div><div class="txt-muted mt-8">Perfect score! 100% points received — no mistakes to review.</div></div>';
  }
});
document.getElementById("backFromReview").addEventListener("click", ()=>showScreen("resultScreen"));

/* ══════════════════════════════════════════════════════
   RETRY WRONG & RETRY ALL
══════════════════════════════════════════════════════ */
document.getElementById("retryAllBtn").addEventListener("click", ()=>startQuiz(state.pool));

document.getElementById("retryWrongBtn").addEventListener("click", ()=>{
  const wrongPool = [];
  state.questions.forEach((q,i)=>{
    if(state.answers[i]!==q.answer){
      wrongPool.push({
        id: q.id,
        subject: q.subject,
        topic: q.topic,
        difficulty: q.difficulty,
        question: q.question,
        options: q._origOptions || q.options,
        answerIndex: q._origAnswerIndex !== undefined ? q._origAnswerIndex : q.answer,
        explanation: q.explanation,
        source: q.source,
      });
    }
  });
  if(wrongPool.length===0) return;
  startQuiz(wrongPool, true);
});

document.getElementById("homeFromResult").addEventListener("click", ()=>{
  renderWeakness(); renderStats(); showScreen("homeScreen");
});

/* ══════════════════════════════════════════════════════
   MODAL DIALOG
══════════════════════════════════════════════════════ */
let modalCb = null;
function showModal(msg, onConfirm){
  document.getElementById("modalMsg").textContent = msg;
  document.getElementById("modal").classList.add("show");
  modalCb = onConfirm;
}
document.getElementById("modalCancel").addEventListener("click", ()=>{
  document.getElementById("modal").classList.remove("show"); modalCb=null;
});
document.getElementById("modalConfirm").addEventListener("click", ()=>{
  document.getElementById("modal").classList.remove("show");
  if(modalCb) modalCb(); modalCb=null;
});

/* ══════════════════════════════════════════════════════
   KEYBOARD SHORTCUTS
══════════════════════════════════════════════════════ */
document.addEventListener("keydown", e=>{
  if(!document.getElementById("quizScreen").classList.contains("active")||state.finished) return;
  if(e.key==="ArrowLeft"||e.key==="p") document.getElementById("prevBtn").click();
  else if(e.key==="ArrowRight"||e.key==="n"||e.key===" ") {
    e.preventDefault(); document.getElementById("nextBtn").click();
  }
  else if(e.key==="f") document.getElementById("flagBtn").click();
  else if(e.key>="1"&&e.key<="4"){
    const idx=parseInt(e.key)-1;
    const q=state.questions[state.idx];
    if(idx<q.options.length) selectOpt(idx);
  }
});

/* ══════════════════════════════════════════════════════
   INITIALIZATION
══════════════════════════════════════════════════════ */
buildSubjectChips();
updateHome();

</script>
</body>
</html>
'''

# Write to index.html (Root for Vercel / Web servers)
index_path = os.path.join(BASE, "index.html")
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Updated {index_path} ({len(html_content)} bytes)")

# Write to cpl-exam-direct.html (Direct offline usage)
direct_path = os.path.join(BASE, "cpl-exam-direct.html")
with open(direct_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Updated {direct_path} ({len(html_content)} bytes)")

# Also write to cpl-quiz-standalone.html
standalone_path = os.path.join(BASE, "cpl-quiz-standalone.html")
with open(standalone_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Updated {standalone_path} ({len(html_content)} bytes)")
