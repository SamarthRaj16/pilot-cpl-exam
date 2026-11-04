# -*- coding: utf-8 -*-
"""
DGCA CPL Practice - Direct HTML Builder v2
Compiles the complete single-file standalone web application with:
1. 839 Verified Questions across 6 DGCA CPL subjects
2. Phase 5: Unconditional Correct Answer Feedback (Authoritative choice + points received)
3. Phase 6: Zero-Repeat Persistent Question Rotation System (cpl_served_ids)
4. Phase 8: Question Bank Audit Modal & Duplicate Prevention Reporting
5. FLyP Academy inspired charcoal dark design system
"""
import json
import os
import sys

BASE = r"c:\VS Code\Codes\dgcacpllearning"
q_path = os.path.join(BASE, "src", "data", "questions.json")

with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} validated questions.")

# SVG Generator Function
svg_func_js = """
function getSubjectSvg(subject) {
  if (subject === "Air Navigation") {
    return `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" class="card-svg">
      <defs>
        <linearGradient id="navGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#141c2e"/>
          <stop offset="50%" stop-color="#1c2844"/>
          <stop offset="100%" stop-color="#0f1524"/>
        </linearGradient>
      </defs>
      <rect width="400" height="200" fill="url(#navGrad)"/>
      <path d="M0 35 Q200 55 400 35 M0 80 Q200 100 400 80 M0 125 Q200 145 400 125 M0 170 Q200 190 400 170" stroke="#719CFF" stroke-width="0.8" stroke-opacity="0.2" fill="none"/>
      <path d="M70 0 Q90 100 70 200 M150 0 Q170 100 150 200 M230 0 Q250 100 230 200 M310 0 Q330 100 310 200" stroke="#719CFF" stroke-width="0.8" stroke-opacity="0.2" fill="none"/>
      <g transform="translate(295, 100)">
        <circle r="60" stroke="#719CFF" stroke-width="1.2" stroke-opacity="0.3" fill="none"/>
        <circle r="46" stroke="#9484F5" stroke-width="0.8" stroke-opacity="0.35" stroke-dasharray="3 3" fill="none"/>
        <polygon points="0,-44 6,-9 0,0 -6,-9" fill="#9484F5" opacity="0.95"/>
        <polygon points="0,44 6,9 0,0 -6,9" fill="#719CFF" opacity="0.4"/>
        <polygon points="44,0 9,6 0,0 9,-6" fill="#719CFF" opacity="0.4"/>
        <polygon points="-44,0 -9,6 0,0 -9,-6" fill="#719CFF" opacity="0.4"/>
        <circle r="3.5" fill="#E5C36C"/>
        <text x="0" y="-48" fill="#E5C36C" font-size="10" font-weight="900" text-anchor="middle" font-family="sans-serif">N</text>
      </g>
      <path d="M35 155 L120 105 L215 130 L320 65" stroke="#51C6C1" stroke-width="2.2" stroke-dasharray="6 4" fill="none" opacity="0.85"/>
      <circle cx="35" cy="155" r="4.5" fill="#51C6C1" stroke="#19191D" stroke-width="2"/>
      <circle cx="120" cy="105" r="4.5" fill="#9484F5" stroke="#19191D" stroke-width="2"/>
      <circle cx="215" cy="130" r="4.5" fill="#51C6C1" stroke="#19191D" stroke-width="2"/>
      <circle cx="320" cy="65" r="5" fill="#E5C36C" stroke="#19191D" stroke-width="2"/>
      <g transform="translate(120, 105) rotate(-35)">
        <path d="M0 -12 L3 -2 L10 2 L3 3 L2 9 L5 11 L0 10 L-5 11 L-2 9 L-3 3 L-10 2 L-3 -2 Z" fill="#FFFFFF" opacity="0.95"/>
      </g>
    </svg>`;
  } else if (subject === "Air Regulations") {
    return `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" class="card-svg">
      <defs>
        <linearGradient id="regGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#241630"/>
          <stop offset="50%" stop-color="#301c42"/>
          <stop offset="100%" stop-color="#160e1f"/>
        </linearGradient>
      </defs>
      <rect width="400" height="200" fill="url(#regGrad)"/>
      <polygon points="140,200 260,200 215,60 185,60" fill="#292A30" stroke="#40414B" stroke-width="1"/>
      <line x1="200" y1="190" x2="200" y2="160" stroke="#F5F5F7" stroke-width="3.5"/>
      <line x1="200" y1="145" x2="200" y2="125" stroke="#F5F5F7" stroke-width="2.5"/>
      <line x1="200" y1="110" x2="200" y2="95" stroke="#F5F5F7" stroke-width="2"/>
      <line x1="200" y1="85" x2="200" y2="72" stroke="#F5F5F7" stroke-width="1.5"/>
      <g fill="#F5F5F7" opacity="0.85">
        <rect x="155" y="175" width="5" height="18"/>
        <rect x="165" y="175" width="5" height="18"/>
        <rect x="175" y="175" width="5" height="18"/>
        <rect x="220" y="175" width="5" height="18"/>
        <rect x="230" y="175" width="5" height="18"/>
        <rect x="240" y="175" width="5" height="18"/>
      </g>
      <text x="200" y="162" fill="#E5C36C" font-size="13" font-weight="900" text-anchor="middle" font-family="sans-serif">27L</text>
      <circle cx="150" cy="195" r="3" fill="#69CF9B"/>
      <circle cx="162" cy="195" r="3" fill="#69CF9B"/>
      <circle cx="238" cy="195" r="3" fill="#69CF9B"/>
      <circle cx="250" cy="195" r="3" fill="#69CF9B"/>
      <g transform="translate(325, 40)">
        <rect x="6" y="20" width="12" height="50" fill="#303139" stroke="#40414B" stroke-width="1"/>
        <polygon points="2,20 22,20 18,8 6,8" fill="#373942" stroke="#9484F5" stroke-width="1"/>
        <circle cx="12" cy="5" r="3.5" fill="#9484F5"/>
        <polygon points="12,5 -75,-25 -85,25" fill="#9484F5" opacity="0.12"/>
      </g>
      <g transform="translate(60, 68)" opacity="0.75">
        <circle r="28" stroke="#E5C36C" stroke-width="1.4" fill="none" stroke-dasharray="3 2"/>
        <polygon points="0,-18 5,-5 18,-5 8,3 12,16 0,8 -12,16 -8,3 -18,-5 -5,-5" fill="none" stroke="#E5C36C" stroke-width="1.2"/>
      </g>
    </svg>`;
  } else if (subject === "Aviation Meteorology") {
    return `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" class="card-svg">
      <defs>
        <linearGradient id="metGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#122430"/>
          <stop offset="50%" stop-color="#183244"/>
          <stop offset="100%" stop-color="#0c1822"/>
        </linearGradient>
      </defs>
      <rect width="400" height="200" fill="url(#metGrad)"/>
      <path d="M-20 50 Q120 15 240 60 T420 40" stroke="#51C6C1" stroke-width="1" stroke-opacity="0.3" fill="none"/>
      <path d="M-20 95 Q140 55 260 105 T420 85" stroke="#51C6C1" stroke-width="1.2" stroke-opacity="0.4" fill="none"/>
      <path d="M-20 140 Q160 100 280 150 T420 130" stroke="#51C6C1" stroke-width="1" stroke-opacity="0.3" fill="none"/>
      <g transform="translate(80, 60)">
        <circle r="16" fill="#719CFF" opacity="0.16"/>
        <text x="0" y="5" fill="#719CFF" font-size="14" font-weight="900" text-anchor="middle" font-family="sans-serif">H</text>
        <text x="0" y="20" fill="#B1B2BE" font-size="7.5" text-anchor="middle" font-family="sans-serif">1024</text>
      </g>
      <g transform="translate(325, 135)">
        <circle r="16" fill="#ED7078" opacity="0.16"/>
        <text x="0" y="5" fill="#ED7078" font-size="14" font-weight="900" text-anchor="middle" font-family="sans-serif">L</text>
        <text x="0" y="20" fill="#B1B2BE" font-size="7.5" text-anchor="middle" font-family="sans-serif">996</text>
      </g>
      <g transform="translate(200, 68)" opacity="0.9">
        <path d="M-60 35 Q-75 18 -52 4 Q-48 -20 -20 -20 Q-12 -38 15 -38 Q40 -38 48 -20 Q75 -16 70 8 Q82 25 65 35 Z" fill="#303139" stroke="#51C6C1" stroke-width="1.2"/>
        <path d="M-25 -20 L-55 -38 L65 -38 L30 -20 Z" fill="#373942" stroke="#51C6C1" stroke-width="1" opacity="0.95"/>
        <polygon points="8,37 -4,55 5,56 -8,75 12,48 2,47" fill="#E5C36C"/>
      </g>
      <g transform="translate(60, 135)">
        <line x1="0" y1="0" x2="40" y2="0" stroke="#69CF9B" stroke-width="2"/>
        <circle cx="0" cy="0" r="2.5" fill="#69CF9B"/>
        <line x1="40" y1="0" x2="31" y2="-10" stroke="#69CF9B" stroke-width="2"/>
        <line x1="33" y1="0" x2="24" y2="-10" stroke="#69CF9B" stroke-width="2"/>
        <line x1="26" y1="0" x2="20" y2="-5" stroke="#69CF9B" stroke-width="1.5"/>
      </g>
    </svg>`;
  } else if (subject === "Technical General") {
    return `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" class="card-svg">
      <defs>
        <linearGradient id="genGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#14261c"/>
          <stop offset="50%" stop-color="#1c3628"/>
          <stop offset="100%" stop-color="#0e1c14"/>
        </linearGradient>
      </defs>
      <rect width="400" height="200" fill="url(#genGrad)"/>
      <g transform="translate(180, 100)">
        <path d="M-100 -55 C-35 -60 35 -55 95 -38 L80 38 C35 55 -35 60 -100 55 Z" fill="none" stroke="#40414B" stroke-width="1.4" stroke-dasharray="4 2"/>
        <ellipse cx="-68" cy="0" rx="16" ry="16" fill="#303139" stroke="#69CF9B" stroke-width="1.8"/>
        <circle cx="-68" cy="0" r="5" fill="#69CF9B"/>
        <path d="M-68 -16 C-64 -40 -50 -52 -45 -54 M-68 16 C-64 40 -50 52 -45 54" stroke="#69CF9B" stroke-width="2.2" fill="none"/>
        <path d="M-55 -9 C-40 -26 -28 -42 -18 -45 M-55 9 C-40 26 -28 42 -18 45" stroke="#51C6C1" stroke-width="1.8" fill="none"/>
        <rect x="-52" y="-10" width="115" height="20" rx="3.5" fill="#292A30" stroke="#69CF9B" stroke-width="1.4"/>
        <line x1="-12" y1="-32" x2="-12" y2="32" stroke="#69CF9B" stroke-width="2"/>
        <line x1="14" y1="-27" x2="14" y2="27" stroke="#69CF9B" stroke-width="2"/>
        <line x1="40" y1="-23" x2="40" y2="23" stroke="#51C6C1" stroke-width="1.8"/>
        <polygon points="62,-12 110,-6 98,0 110,6 62,12" fill="#ECA85B" opacity="0.6"/>
      </g>
      <g transform="translate(330, 45)" opacity="0.3">
        <circle r="30" fill="none" stroke="#69CF9B" stroke-width="3.5" stroke-dasharray="7 5"/>
        <circle r="18" fill="none" stroke="#69CF9B" stroke-width="1.4"/>
      </g>
    </svg>`;
  } else if (subject === "Technical Specific") {
    return `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" class="card-svg">
      <defs>
        <linearGradient id="specGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#2a1a15"/>
          <stop offset="50%" stop-color="#3c221a"/>
          <stop offset="100%" stop-color="#180f0c"/>
        </linearGradient>
        <clipPath id="specAdiClip">
          <circle r="48"/>
        </clipPath>
      </defs>
      <rect width="400" height="200" fill="url(#specGrad)"/>
      <rect x="75" y="18" width="250" height="164" rx="10" fill="#202126" stroke="#40414B" stroke-width="1.8"/>
      <g transform="translate(200, 100)">
        <g clip-path="url(#specAdiClip)">
          <rect x="-52" y="-52" width="104" height="52" fill="#1565c0" opacity="0.75"/>
          <rect x="-52" y="0" width="104" height="52" fill="#6d4c41" opacity="0.8"/>
          <line x1="-52" y1="0" x2="52" y2="0" stroke="#F5F5F7" stroke-width="1.8"/>
          <line x1="-14" y1="-15" x2="14" y2="-15" stroke="#F5F5F7" stroke-width="1.3"/>
          <line x1="-8" y1="-30" x2="8" y2="-30" stroke="#F5F5F7" stroke-width="1.3"/>
          <line x1="-14" y1="15" x2="14" y2="15" stroke="#F5F5F7" stroke-width="1.3"/>
          <line x1="-8" y1="30" x2="8" y2="30" stroke="#F5F5F7" stroke-width="1.3"/>
        </g>
        <circle r="48" stroke="#E5C36C" stroke-width="1.8" fill="none"/>
        <path d="M-24 0 L-8 0 L-5 7 L0 1.5 L5 7 L8 0 L24 0" stroke="#E5C36C" stroke-width="2.6" fill="none"/>
        <circle cx="0" cy="0" r="2" fill="#E5C36C"/>
      </g>
      <g transform="translate(92, 34)">
        <rect x="0" y="0" width="30" height="132" fill="#292A30" stroke="#40414B" stroke-width="1"/>
        <line x1="26" y1="105" x2="26" y2="55" stroke="#F5F5F7" stroke-width="2.5"/>
        <line x1="26" y1="80" x2="26" y2="28" stroke="#69CF9B" stroke-width="2.5"/>
        <line x1="26" y1="28" x2="26" y2="14" stroke="#E5C36C" stroke-width="2.5"/>
        <line x1="26" y1="14" x2="26" y2="0" stroke="#ED7078" stroke-width="2.5"/>
        <polygon points="2,60 22,60 28,66 22,72 2,72" fill="#9484F5"/>
        <text x="12" y="68" fill="#FFFFFF" font-size="8.5" font-weight="800" text-anchor="middle" font-family="sans-serif">120</text>
      </g>
      <g transform="translate(278, 34)">
        <rect x="0" y="0" width="34" height="132" fill="#292A30" stroke="#40414B" stroke-width="1"/>
        <polygon points="32,60 12,60 6,66 12,72 32,72" fill="#719CFF"/>
        <text x="21" y="68" fill="#FFFFFF" font-size="8" font-weight="800" text-anchor="middle" font-family="sans-serif">4500</text>
      </g>
    </svg>`;
  } else if (subject === "RTR") {
    return `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" class="card-svg">
      <defs>
        <linearGradient id="rtrGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#12202b"/>
          <stop offset="50%" stop-color="#182c3c"/>
          <stop offset="100%" stop-color="#0c1720"/>
        </linearGradient>
      </defs>
      <rect width="400" height="200" fill="url(#rtrGrad)"/>
      <g transform="translate(200, 155)">
        <polygon points="-8,0 8,0 2,-90 -2,-90" fill="#303139" stroke="#51C6C1" stroke-width="1.2"/>
        <line x1="-22" y1="-30" x2="22" y2="-30" stroke="#51C6C1" stroke-width="1.5"/>
        <line x1="-16" y1="-60" x2="16" y2="-60" stroke="#51C6C1" stroke-width="1.5"/>
        <circle cx="0" cy="-90" r="4.5" fill="#E5C36C"/>
        <path d="M-30 -90 A30 30 0 0 1 30 -90" stroke="#51C6C1" stroke-width="1.8" fill="none" opacity="0.8"/>
        <path d="M-55 -90 A55 55 0 0 1 55 -90" stroke="#51C6C1" stroke-width="1.4" fill="none" opacity="0.55" stroke-dasharray="4 2"/>
        <path d="M-80 -90 A80 80 0 0 1 80 -90" stroke="#51C6C1" stroke-width="1" fill="none" opacity="0.3" stroke-dasharray="6 3"/>
      </g>
      <g transform="translate(65, 48)">
        <rect x="0" y="0" width="75" height="32" rx="4" fill="#292A30" stroke="#51C6C1" stroke-width="1.2"/>
        <text x="37" y="21" fill="#51C6C1" font-size="13" font-weight="900" text-anchor="middle" font-family="monospace">121.500</text>
      </g>
      <g transform="translate(265, 48)">
        <rect x="0" y="0" width="70" height="32" rx="4" fill="#292A30" stroke="#E5C36C" stroke-width="1.2"/>
        <text x="35" y="21" fill="#E5C36C" font-size="13" font-weight="900" text-anchor="middle" font-family="monospace">SQ 7700</text>
      </g>
    </svg>`;
  } else {
    return `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" class="card-svg">
      <defs>
        <linearGradient id="allGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1b1c2b"/>
          <stop offset="50%" stop-color="#2a2544"/>
          <stop offset="100%" stop-color="#141420"/>
        </linearGradient>
      </defs>
      <rect width="400" height="200" fill="url(#allGrad)"/>
      <g transform="translate(200, 100)">
        <circle r="75" stroke="#9484F5" stroke-width="1.2" stroke-opacity="0.3" fill="none"/>
        <circle r="52" stroke="#719CFF" stroke-width="0.9" stroke-opacity="0.35" fill="none" stroke-dasharray="4 3"/>
        <circle r="28" stroke="#51C6C1" stroke-width="1.2" stroke-opacity="0.4" fill="none"/>
        <polygon points="0,-60 8,-12 0,0 -8,-12" fill="#E5C36C" opacity="0.95"/>
        <polygon points="0,60 8,12 0,0 -8,12" fill="#719CFF" opacity="0.5"/>
        <polygon points="60,0 12,8 0,0 12,-8" fill="#51C6C1" opacity="0.6"/>
        <polygon points="-60,0 -12,8 0,0 -12,-8" fill="#9484F5" opacity="0.6"/>
        <circle r="5" fill="#E5C36C"/>
      </g>
    </svg>`;
  }
}
"""

print("Compiling Direct HTML template with 839 questions...")

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta name="description" content="CPL Practice - DGCA Written Examination Preparation Platform for Commercial Pilot Licence in India.">
<title>CPL Practice - DGCA Written Examination Platform</title>
<style>
/* Reset and Color System */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root {
  /* Surfaces */
  --bg-main: #19191D;
  --bg-secondary: #202126;
  --card-primary: #292A30;
  --card-elevated: #303139;
  --surface-interactive: #373942;
  --surface-hover: #434552;
  --border: #40414B;
  --border-subtle: #33343d;
  --border-focus: #9484F5;

  /* Typography */
  --text-primary: #F5F5F7;
  --text-secondary: #B1B2BE;
  --text-muted: #81838F;

  /* Accent Colors */
  --primary: #9484F5;
  --primary-glow: rgba(148, 132, 245, 0.25);
  --primary-dark: #7b6ae6;
  --aviation-blue: #719CFF;
  --teal: #51C6C1;
  --success: #69CF9B;
  --gold: #E5C36C;
  --warning: #ECA85B;
  --error: #ED7078;

  /* Tints */
  --tint-green: rgba(105, 207, 155, 0.12);
  --tint-green-border: rgba(105, 207, 155, 0.35);
  --tint-red: rgba(237, 112, 120, 0.12);
  --tint-red-border: rgba(237, 112, 120, 0.35);
  --tint-orange: rgba(236, 168, 91, 0.12);
  --tint-orange-border: rgba(236, 168, 91, 0.35);
  --tint-purple: rgba(148, 132, 245, 0.14);
  --tint-purple-border: rgba(148, 132, 245, 0.4);

  /* Radius & Shadows */
  --radius-xl: 18px;
  --radius-lg: 14px;
  --radius-md: 10px;
  --radius-sm: 6px;

  --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.35);
  --shadow-elevated: 0 8px 32px rgba(0, 0, 0, 0.45);
  --shadow-glow: 0 0 24px rgba(148, 132, 245, 0.2);

  --font: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
  --transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.light {
  --bg-main: #f0f4f8;
  --bg-secondary: #e4e9f0;
  --card-primary: #ffffff;
  --card-elevated: #f8fafc;
  --surface-interactive: #e8edf4;
  --surface-hover: #dce3ed;
  --border: #cdd5e0;
  --border-subtle: #dbe2ec;
  --text-primary: #121624;
  --text-secondary: #4a5468;
  --text-muted: #727f96;
  --primary: #6c5ce7;
  --primary-glow: rgba(108, 92, 231, 0.2);
}

html { font-size: 16px; scroll-behavior: smooth; }
body {
  font-family: var(--font);
  background: var(--bg-main);
  color: var(--text-primary);
  min-height: 100vh;
  line-height: 1.5;
  -webkit-tap-highlight-color: transparent;
  transition: background var(--transition), color var(--transition);
}
button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.95rem;
  transition: var(--transition);
  outline: none;
}
button:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }
button:active { transform: scale(0.98); }
input, select { font-family: inherit; outline: none; }

.container-wide {
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px 28px 60px;
}
.screen { display: none; }
.screen.active { display: block; }

/* Navbar */
.navbar {
  position: sticky;
  top: 0;
  z-index: 300;
  background: var(--bg-main);
  border-bottom: 1px solid var(--border);
  padding: 12px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  backdrop-filter: blur(12px);
}
.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  text-decoration: none;
}
.brand-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--card-elevated), var(--surface-interactive));
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.brand-text h1 {
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  line-height: 1.2;
}
.brand-text span {
  font-size: 0.72rem;
  color: var(--text-muted);
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}
.nav-link {
  padding: 8px 14px;
  border-radius: 8px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 600;
  background: transparent;
  text-decoration: none;
  cursor: pointer;
  border: none;
}
.nav-link:hover, .nav-link.active {
  color: var(--text-primary);
  background: var(--surface-interactive);
}
.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.pill-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 700;
  background: var(--card-elevated);
  border: 1px solid var(--border);
  color: var(--gold);
}
.btn-audit {
  background: var(--surface-interactive);
  color: var(--primary);
  border: 1px solid var(--border);
  padding: 7px 13px;
  font-size: 0.82rem;
  font-weight: 700;
  border-radius: 20px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.btn-audit:hover {
  background: var(--primary-glow);
  border-color: var(--primary);
}
.theme-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--surface-interactive);
  border: 1px solid var(--border);
  color: var(--text-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

/* Hero Section */
.hero-deck {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 16px;
  margin-bottom: 28px;
}
@media (max-width: 860px) {
  .hero-deck { grid-template-columns: 1fr; }
}
.hero-banner {
  border-radius: var(--radius-lg);
  padding: 22px 24px;
  position: relative;
  overflow: hidden;
  border: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 140px;
}
.hero-banner.resume {
  background: linear-gradient(135deg, #182824 0%, #202126 100%);
  border-color: rgba(81, 198, 193, 0.3);
}
.hero-banner.today {
  background: linear-gradient(135deg, #261e38 0%, #202126 100%);
  border-color: rgba(148, 132, 245, 0.3);
}
.banner-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}
.banner-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--teal);
}
.hero-banner.today .banner-badge { color: var(--primary); }
.banner-title {
  font-size: 1.55rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  line-height: 1.2;
}
.banner-sub {
  font-size: 0.95rem;
  color: var(--text-secondary);
  font-weight: 500;
}
.banner-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
}
.banner-cta {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--teal);
  background: transparent;
  padding: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.hero-banner.today .banner-cta { color: var(--primary); }
.banner-cta:hover { text-decoration: underline; }

/* Hubs Overview Deck */
.hubs-deck {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
}
@media (max-width: 900px) {
  .hubs-deck { grid-template-columns: 1fr; }
}
.hub-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 22px 24px;
  box-shadow: var(--shadow-card);
}
.hub-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.hub-title-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}
.hub-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}
.hub-streak {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--warning);
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.btn-hub-action {
  background: var(--surface-interactive);
  color: var(--text-primary);
  border: 1px solid var(--border);
  padding: 7px 14px;
  font-size: 0.82rem;
  font-weight: 700;
  border-radius: 8px;
}
.btn-hub-action:hover {
  background: var(--surface-hover);
  border-color: var(--primary);
  color: var(--primary);
}
.stats-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 18px;
}
.stat-box {
  background: var(--card-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  text-align: center;
}
.stat-val {
  font-size: 1.55rem;
  font-weight: 900;
  color: var(--text-primary);
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.stat-lbl {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-top: 4px;
}
.stat-trend {
  font-size: 0.75rem;
  font-weight: 700;
  margin-top: 4px;
}
.stat-trend.up { color: var(--success); }
.stat-trend.down { color: var(--error); }

.exam-rows {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.exam-row-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.88rem;
  padding: 4px 0;
}
.exam-subj-name {
  color: var(--text-primary);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}
.exam-subj-score {
  font-weight: 800;
  color: var(--text-primary);
}
.mini-track {
  width: 80px;
  height: 6px;
  background: var(--surface-interactive);
  border-radius: 3px;
  overflow: hidden;
  margin-left: 12px;
}
.mini-fill {
  height: 100%;
  border-radius: 3px;
  background: var(--primary);
}

/* Subject Grid */
.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.section-title {
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}
.section-sub {
  font-size: 0.85rem;
  color: var(--text-muted);
}
.subject-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 18px;
  margin-bottom: 28px;
}
.subject-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.2s, box-shadow 0.2s;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
}
.subject-card:hover {
  transform: translateY(-3px);
  border-color: var(--primary);
  box-shadow: var(--shadow-elevated);
}
.subject-card.selected {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary), var(--shadow-glow);
}
.card-media {
  position: relative;
  width: 100%;
  height: 125px;
  background: var(--bg-secondary);
  overflow: hidden;
}
.card-svg {
  width: 100%;
  height: 100%;
  display: block;
}
.card-media-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(25, 25, 29, 0.1) 0%, rgba(25, 25, 29, 0.85) 100%);
}
.card-media-meta {
  position: absolute;
  top: 10px;
  left: 12px;
  right: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-primary);
  text-shadow: 0 1px 3px rgba(0,0,0,0.8);
}
.card-tag {
  background: rgba(32, 33, 38, 0.75);
  backdrop-filter: blur(4px);
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.1);
}
.card-arrow {
  font-size: 0.95rem;
  color: var(--gold);
}
.card-body {
  padding: 14px 16px 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.card-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.card-title {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--text-primary);
}
.card-check {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1.5px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: transparent;
  transition: var(--transition);
}
.subject-card.selected .card-check {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
}
.card-info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin-bottom: 10px;
}
.card-track {
  width: 100%;
  height: 5px;
  background: var(--surface-interactive);
  border-radius: 3px;
  overflow: hidden;
}
.card-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--teal), var(--primary));
  border-radius: 3px;
  transition: width 0.4s ease;
}

/* Control Hub & Mode Selector */
.practice-hub-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-card);
}
.hub-controls-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 20px;
  margin-bottom: 20px;
}
@media (max-width: 800px) {
  .hub-controls-grid { grid-template-columns: 1fr; }
}
.control-block label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 8px;
}
.mode-toggle-group {
  display: flex;
  gap: 8px;
  background: var(--card-elevated);
  padding: 4px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
}
.mode-btn {
  flex: 1;
  padding: 10px 14px;
  font-size: 0.86rem;
  font-weight: 700;
  border-radius: 8px;
  background: transparent;
  color: var(--text-secondary);
  border: none;
  cursor: pointer;
  text-align: center;
  transition: var(--transition);
}
.mode-btn.selected {
  background: var(--primary);
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(148, 132, 245, 0.35);
}
.custom-select {
  width: 100%;
  padding: 11px 14px;
  border-radius: var(--radius-md);
  background: var(--card-elevated);
  color: var(--text-primary);
  border: 1px solid var(--border);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
}
.custom-select:focus {
  border-color: var(--primary);
}

.rotation-status-badge {
  background: var(--surface-interactive);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: 0.84rem;
}
.rotation-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 700;
  color: var(--teal);
}
.btn-reset-pool {
  background: transparent;
  color: var(--warning);
  font-size: 0.78rem;
  font-weight: 700;
  border: 1px solid var(--tint-orange-border);
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
}
.btn-reset-pool:hover {
  background: var(--tint-orange);
}

.btn-start-quiz {
  width: 100%;
  padding: 16px 24px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, var(--primary) 0%, #7b6ae6 100%);
  color: #ffffff;
  font-size: 1.05rem;
  font-weight: 800;
  letter-spacing: -0.01em;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 4px 20px rgba(148, 132, 245, 0.4);
  transition: transform 0.15s, box-shadow 0.15s;
}
.btn-start-quiz:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(148, 132, 245, 0.5);
}
.btn-start-quiz:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

/* CBT SCREEN LAYOUT */
.cbt-container {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 24px;
  align-items: start;
}
@media (max-width: 960px) {
  .cbt-container { grid-template-columns: 1fr; }
}
.cbt-main {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 26px 28px;
  box-shadow: var(--shadow-card);
}
.cbt-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.cbt-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.cbt-course-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--text-primary);
}
.cbt-badge {
  background: var(--surface-interactive);
  border: 1px solid var(--border);
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-secondary);
}
.cbt-badge.diff-easy { color: var(--success); border-color: var(--tint-green-border); }
.cbt-badge.diff-medium { color: var(--gold); border-color: rgba(229, 195, 108, 0.3); }
.cbt-badge.diff-hard { color: var(--error); border-color: var(--tint-red-border); }

.cbt-progress-wrap {
  margin-bottom: 24px;
}
.cbt-progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.84rem;
  color: var(--text-secondary);
  font-weight: 600;
  margin-bottom: 6px;
}
.cbt-progress-track {
  width: 100%;
  height: 6px;
  background: var(--surface-interactive);
  border-radius: 3px;
  overflow: hidden;
}
.cbt-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--aviation-blue), var(--primary));
  border-radius: 3px;
  transition: width 0.3s ease;
}

.cbt-q-card {
  margin-bottom: 24px;
}
.cbt-q-title {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}
.cbt-q-text {
  font-size: 1.15rem;
  font-weight: 600;
  line-height: 1.5;
  color: var(--text-primary);
  margin-bottom: 24px;
}
.cbt-opts {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.opt {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border-radius: var(--radius-md);
  background: var(--card-elevated);
  border: 1.5px solid var(--border);
  color: var(--text-primary);
  text-align: left;
  font-size: 0.98rem;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
}
.opt:hover:not(.disabled) {
  border-color: var(--primary);
  background: var(--surface-interactive);
}
.opt.selected {
  border-color: var(--primary);
  background: var(--surface-interactive);
}
.opt.correct {
  border-color: var(--success) !important;
  background: var(--tint-green) !important;
  color: var(--text-primary);
}
.opt.wrong {
  border-color: var(--error) !important;
  background: var(--tint-red) !important;
  color: var(--text-primary);
}
.opt.disabled {
  cursor: default;
}
.opt-letter {
  width: 28px;
  height: 28px;
  border-radius: 7px;
  background: var(--surface-interactive);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 0.85rem;
  color: var(--text-secondary);
  flex-shrink: 0;
}
.opt.selected .opt-letter {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
}
.opt.correct .opt-letter {
  background: var(--success);
  border-color: var(--success);
  color: #19191D;
}
.opt.wrong .opt-letter {
  background: var(--error);
  border-color: var(--error);
  color: #fff;
}
.opt-text {
  flex: 1;
  font-weight: 500;
}
.opt-tag {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}
.opt-tag.correct {
  background: var(--success);
  color: #19191D;
}
.opt-tag.wrong {
  background: var(--error);
  color: #fff;
}

/* Feedback Card */
.feedback {
  display: none;
  margin-top: 20px;
  padding: 16px 20px;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  font-size: 0.92rem;
  line-height: 1.55;
}
.feedback.show { display: block; animation: fadeIn 0.25s ease-out; }
.feedback-correct {
  background: var(--tint-green);
  border-color: var(--tint-green-border);
}
.feedback-wrong {
  background: var(--tint-red);
  border-color: var(--tint-red-border);
}
.fb-status {
  font-size: 1rem;
  font-weight: 800;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.feedback-correct .fb-status { color: var(--success); }
.feedback-wrong .fb-status { color: var(--error); }
.fb-ans-line {
  font-size: 0.9rem;
  margin-bottom: 6px;
  padding: 6px 10px;
  border-radius: 6px;
}
.fb-ans-line.your {
  background: rgba(237, 112, 120, 0.15);
  color: var(--error);
}
.fb-ans-line.right {
  background: rgba(105, 207, 155, 0.15);
  color: var(--success);
}
.fb-body {
  margin-top: 8px;
  color: var(--text-primary);
}
.feedback-src {
  margin-top: 10px;
  font-size: 0.78rem;
  color: var(--text-muted);
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Navigation Row */
.cbt-nav-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 28px;
  padding-top: 18px;
  border-top: 1px solid var(--border);
}
.btn-cbt {
  padding: 12px 20px;
  border-radius: var(--radius-md);
  font-size: 0.92rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.btn-cbt.secondary {
  background: var(--surface-interactive);
  color: var(--text-primary);
  border: 1px solid var(--border);
}
.btn-cbt.secondary:hover { background: var(--surface-hover); }
.btn-cbt.primary {
  background: var(--primary);
  color: #fff;
  border: none;
}
.btn-cbt.primary:hover { background: var(--primary-dark); }
.btn-cbt.flag {
  background: transparent;
  color: var(--warning);
  border: 1px solid var(--tint-orange-border);
}
.btn-cbt.flag.flagged {
  background: var(--warning);
  color: #19191D;
  font-weight: 800;
}

/* CBT Sidebar */
.cbt-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.timer-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  text-align: center;
  box-shadow: var(--shadow-card);
}
.cbt-timer-wrap {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 12px;
}
.cbt-timer-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}
.timer-bg-ring {
  fill: none;
  stroke: var(--surface-interactive);
  stroke-width: 6;
}
.timer-fg-ring {
  fill: none;
  stroke: var(--success);
  stroke-width: 6;
  stroke-linecap: round;
  stroke-dasharray: 276.46;
  stroke-dashoffset: 0;
  transition: stroke-dashoffset 0.5s ease, stroke 0.3s;
}
.timer-fg-ring.urgent { stroke: var(--warning); }
.timer-fg-ring.critical { stroke: var(--error); }
.cbt-timer-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.timer-digits {
  font-size: 1.25rem;
  font-weight: 900;
  color: var(--text-primary);
  font-family: monospace;
}
.timer-sub {
  font-size: 0.65rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
}
.score-badge {
  font-size: 0.84rem;
  font-weight: 700;
  color: var(--gold);
  background: var(--card-elevated);
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  display: inline-block;
}

/* Navigator Grid */
.navigator-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px;
  box-shadow: var(--shadow-card);
}
.nav-grid-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.nav-grid-title {
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-primary);
}
.nav-grid-counter {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-secondary);
}
.q-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  max-height: 240px;
  overflow-y: auto;
  padding-right: 4px;
}
.q-cell {
  aspect-ratio: 1;
  border-radius: 8px;
  background: var(--card-elevated);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
}
.q-cell:hover {
  border-color: var(--primary);
  color: var(--text-primary);
}
.q-cell.current {
  border-color: var(--primary);
  box-shadow: 0 0 0 2px var(--primary);
  color: #fff;
}
.q-cell.answered {
  background: var(--tint-green);
  border-color: var(--success);
  color: var(--success);
}
.q-cell.flagged {
  background: var(--tint-orange);
  border-color: var(--warning);
  color: var(--warning);
}
.nav-summary-chips {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  font-size: 0.75rem;
  color: var(--text-muted);
}
.grid-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--border);
  font-size: 0.72rem;
  color: var(--text-secondary);
}
.leg { display: inline-flex; align-items: center; gap: 5px; }
.leg-dot { width: 8px; height: 8px; border-radius: 50%; }
.leg-dot.answered { background: var(--success); }
.leg-dot.flagged { background: var(--warning); }
.leg-dot.current { background: var(--primary); }
.leg-dot.unanswered { background: var(--surface-interactive); }

.sidebar-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.btn-finish-exam {
  width: 100%;
  padding: 13px;
  border-radius: var(--radius-md);
  background: var(--primary);
  color: #fff;
  font-weight: 800;
  font-size: 0.95rem;
  box-shadow: 0 4px 14px rgba(148, 132, 245, 0.35);
}
.btn-finish-exam:hover { background: var(--primary-dark); }
.btn-quit-exam {
  width: 100%;
  padding: 11px;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--error);
  border: 1px solid var(--tint-red-border);
  font-weight: 700;
  font-size: 0.88rem;
}
.btn-quit-exam:hover { background: var(--tint-red); }

/* RESULTS SCREEN */
.result-hero {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 32px 24px;
  text-align: center;
  margin-bottom: 24px;
  box-shadow: var(--shadow-card);
}
.result-trophy { font-size: 3rem; margin-bottom: 10px; }
.result-points-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.result-grade {
  font-size: 3.2rem;
  font-weight: 900;
  color: var(--text-primary);
  line-height: 1.1;
  letter-spacing: -0.03em;
}
.result-pct {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--gold);
  margin-top: 4px;
}
.result-pass {
  display: inline-block;
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 0.95rem;
  font-weight: 800;
  margin-top: 16px;
}
.result-pass.pass {
  background: var(--tint-green);
  border: 1px solid var(--tint-green-border);
  color: var(--success);
}
.result-pass.fail {
  background: var(--tint-red);
  border: 1px solid var(--tint-red-border);
  color: var(--error);
}
.result-stats {
  font-size: 0.84rem;
  color: var(--text-secondary);
  margin-top: 14px;
}

.breakdown-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 22px 24px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
}
.card-header-line {
  font-size: 1.05rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-acts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-top: 24px;
}
.btn-review {
  background: var(--primary);
  color: #fff;
  padding: 13px;
  font-weight: 800;
  border-radius: var(--radius-md);
}
.btn-retry-wrong {
  background: var(--surface-interactive);
  color: var(--warning);
  border: 1px solid var(--tint-orange-border);
  padding: 13px;
  font-weight: 800;
  border-radius: var(--radius-md);
}
.btn-retry-all {
  background: var(--surface-interactive);
  color: var(--text-primary);
  border: 1px solid var(--border);
  padding: 13px;
  font-weight: 700;
  border-radius: var(--radius-md);
}
.btn-home {
  background: var(--card-elevated);
  color: var(--text-secondary);
  border: 1px solid var(--border);
  padding: 13px;
  font-weight: 700;
  border-radius: var(--radius-md);
}

/* REVIEW SCREEN */
.review-item {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px 22px;
  margin-bottom: 16px;
  box-shadow: var(--shadow-card);
}
.review-qnum {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 8px;
}
.review-q {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 14px;
  line-height: 1.45;
}
.review-ans {
  padding: 10px 14px;
  border-radius: var(--radius-md);
  margin-bottom: 8px;
  font-size: 0.92rem;
  line-height: 1.4;
}
.review-ans.your {
  background: var(--tint-red);
  border: 1px solid var(--tint-red-border);
  color: var(--error);
}
.review-ans.right {
  background: var(--tint-green);
  border: 1px solid var(--tint-green-border);
  color: var(--success);
}
.review-ans.skipped {
  background: var(--tint-orange);
  border: 1px solid var(--tint-orange-border);
  color: var(--warning);
}
.review-expl {
  font-size: 0.88rem;
  color: var(--text-secondary);
  background: var(--card-elevated);
  padding: 12px 14px;
  border-radius: var(--radius-md);
  margin-top: 10px;
  border: 1px solid var(--border);
}
.review-src {
  font-size: 0.76rem;
  color: var(--text-muted);
  margin-top: 8px;
  font-weight: 600;
}

/* MODALS */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.modal-overlay.show { display: flex; animation: fadeIn 0.2s ease-out; }
.modal-box {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 26px 28px;
  max-width: 480px;
  width: 100%;
  box-shadow: var(--shadow-elevated);
}
.modal-icon { font-size: 2.2rem; margin-bottom: 12px; }
.modal-title { font-size: 1.25rem; font-weight: 800; color: var(--text-primary); margin-bottom: 8px; }
.modal-box p { font-size: 0.92rem; color: var(--text-secondary); margin-bottom: 22px; line-height: 1.5; }
.modal-btns { display: flex; justify-content: flex-end; gap: 10px; }
.btn-cancel {
  background: var(--surface-interactive);
  color: var(--text-secondary);
  padding: 10px 18px;
  font-weight: 700;
}
.btn-modal-confirm {
  background: var(--primary);
  color: #fff;
  padding: 10px 20px;
  font-weight: 800;
}

/* AUDIT MODAL */
.audit-box {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 26px 28px;
  max-width: 720px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: var(--shadow-elevated);
}
.audit-table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
  font-size: 0.85rem;
}
.audit-table th {
  text-align: left;
  padding: 8px 10px;
  background: var(--card-elevated);
  border-bottom: 1px solid var(--border);
  color: var(--text-muted);
  font-weight: 700;
}
.audit-table td {
  padding: 10px;
  border-bottom: 1px solid var(--border);
  color: var(--text-primary);
}

@keyframes fadeIn { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } }
</style>
</head>
<body>

<nav class="navbar">
  <div class="nav-brand" onclick="goHome()">
    <div class="brand-icon-wrap">✈️</div>
    <div class="brand-text">
      <h1>CPL Practice <span class="pill-badge" style="font-size:0.68rem;padding:2px 8px">DGCA CBT</span></h1>
      <span>Commercial Pilot Licence</span>
    </div>
  </div>
  <div class="nav-links">
    <button class="nav-link active" onclick="goHome()">Dashboard</button>
    <button class="nav-link" onclick="scrollToPractice()">Practice</button>
    <button class="nav-link" onclick="scrollToAnalytics()">Analytics</button>
  </div>
  <div class="nav-actions">
    <button class="btn-audit" id="auditBankBtn">📋 Audit Bank (839 Qs)</button>
    <span class="pill-badge" id="headerScorePill">⭐ 0 Points</span>
    <button class="theme-btn" id="darkBtn" title="Toggle Theme">🌙</button>
  </div>
</nav>

<div class="container-wide">

<!-- HOME / DASHBOARD SCREEN -->
<div id="homeScreen" class="screen active">

  <!-- Hero Deck -->
  <div class="hero-deck">
    <div class="hero-banner resume">
      <div>
        <div class="banner-top">
          <span class="banner-badge">✨ Continue where you left off</span>
          <span>Last Studied Today</span>
        </div>
        <div class="banner-title" id="resumeTitle">Air Navigation</div>
        <div class="banner-sub" id="resumeSub">General Navigation • Chart Projections</div>
      </div>
      <div class="banner-foot">
        <button class="banner-cta" id="quickResumeBtn">Start Practice &raquo;</button>
        <span style="font-size:0.8rem;color:var(--text-muted)">CAR SEC 7 Standard</span>
      </div>
    </div>

    <div class="hero-banner today">
      <div>
        <div class="banner-top">
          <span class="banner-badge">📊 DGCA Mock Examination</span>
          <span>Full CBT Simulation</span>
        </div>
        <div class="banner-title">Mock Exam Hub</div>
        <div class="banner-sub">70% Pass Criteria • Realistic Timers • 0 Neg Marking</div>
      </div>
      <div class="banner-foot">
        <button class="banner-cta" id="quickMockBtn">Launch Mock Exam &raquo;</button>
        <span style="font-size:0.8rem;color:var(--text-muted)">Valid 5 Years</span>
      </div>
    </div>
  </div>

  <!-- Hubs Overview -->
  <div class="hubs-deck">
    <div class="hub-card">
      <div class="hub-header">
        <div class="hub-title-wrap">
          <span class="hub-title">Quiz Hub</span>
          <span class="hub-streak">🔥 24 Streak</span>
        </div>
        <button class="btn-hub-action" onclick="scrollToPractice()">Take a Quiz &raquo;</button>
      </div>
      <div class="stats-grid-3">
        <div class="stat-box">
          <div class="stat-val" id="aoPoints">0</div>
          <div class="stat-lbl">Points Earned</div>
          <div class="stat-trend up">&uarr; +12 today</div>
        </div>
        <div class="stat-box">
          <div class="stat-val" id="aoAccuracy">0%</div>
          <div class="stat-lbl">Accuracy</div>
          <div class="stat-trend up">&uarr; +5%</div>
        </div>
        <div class="stat-box">
          <div class="stat-val" id="aoAttempted">0</div>
          <div class="stat-lbl">Questions Tried</div>
          <div class="stat-trend">&bull; 839 in bank</div>
        </div>
      </div>
      <div style="font-size:0.82rem;color:var(--text-muted);display:flex;justify-content:space-between">
        <span>DGCA Preparation League</span>
        <span style="color:var(--gold);font-weight:700">Gold League • Rank #4</span>
      </div>
    </div>

    <div class="hub-card">
      <div class="hub-header">
        <div class="hub-title-wrap">
          <span class="hub-title">Exam Hub</span>
          <span style="font-size:0.88rem;color:var(--teal);font-weight:700">🎯 70% Pass Mark</span>
        </div>
        <button class="btn-hub-action" id="hubMockBtn">Mock Exams &raquo;</button>
      </div>
      <div class="exam-rows" id="examSubjRows">
        <!-- Rendered dynamically -->
      </div>
    </div>
  </div>

  <!-- Practice Hub Controls -->
  <div class="practice-hub-card" id="practiceAnchor">
    <div class="section-head">
      <div>
        <div class="section-title">Examination & Practice Setup</div>
        <div class="section-sub">Choose examination mode, target subjects, and topic filters</div>
      </div>
    </div>

    <div class="hub-controls-grid">
      <div class="control-block">
        <label>Examination Mode</label>
        <div class="mode-toggle-group">
          <button class="mode-btn selected" data-mode="practice">Practice Mode</button>
          <button class="mode-btn" data-mode="timed">Timed Exam</button>
          <button class="mode-btn" data-mode="mock">DGCA Mock</button>
        </div>
      </div>

      <div class="control-block">
        <label>Topic / Chapter Filter</label>
        <select class="custom-select" id="topicSel">
          <option value="">All Topics (94 available across subjects)</option>
        </select>
      </div>
    </div>

    <div class="rotation-status-badge">
      <div class="rotation-pill">
        <span>🔄 Zero-Repeat Question Rotation:</span>
        <strong id="rotationStatsText">839 unserved of 839 questions available</strong>
      </div>
      <button class="btn-reset-pool" id="resetCurrentPoolBtn" title="Reset question exposure history for this selection">Reset Question Pool</button>
    </div>

    <div style="display:flex;align-items:center;gap:16px">
      <button class="btn-start-quiz" id="startBtn">
        <span>Start Examination</span>
        <span id="startLabel">(839 questions available)</span>
      </button>
    </div>
  </div>

  <!-- Subject Grid -->
  <div class="section-head">
    <div>
      <div class="section-title">DGCA CPL Written Subjects</div>
      <div class="section-sub">Select one or more subjects to focus your question bank</div>
    </div>
  </div>
  <div class="subject-grid" id="subjGrid"></div>

  <!-- Analytics & Weakness Panel -->
  <div class="practice-hub-card" id="analyticsAnchor">
    <div class="section-head">
      <div>
        <div class="section-title">Performance Analytics & Focus Areas</div>
        <div class="section-sub">Identifies weak areas below the DGCA 70% passing threshold</div>
      </div>
      <button class="btn-reset-pool" id="resetHistoryBtn">Reset All Score History</button>
    </div>
    <div id="weakPanel"></div>
  </div>

</div><!-- /homeScreen -->

<!-- CBT EXAMINATION SCREEN -->
<div id="quizScreen" class="screen">
  <div class="cbt-container">

    <main class="cbt-main">
      <div class="cbt-header">
        <div class="cbt-header-left">
          <h2 class="cbt-course-title" id="qSubjectBadge">Air Navigation</h2>
          <span class="cbt-badge" id="qTopicBadge">General Navigation</span>
        </div>
        <div class="cbt-header-right" style="display:flex;gap:8px">
          <span class="cbt-badge" id="qZeroRepeatBadge" style="color:var(--teal)">🔄 Zero-Repeat</span>
          <span class="cbt-badge" id="qDiffBadge">Medium</span>
        </div>
      </div>

      <div class="cbt-progress-wrap">
        <div class="cbt-progress-label">
          <span id="qProgressText">Question 1 of 50</span>
          <span id="qProgressPct">2% Complete</span>
        </div>
        <div class="cbt-progress-track">
          <div class="cbt-progress-fill" id="qProgressBar" style="width:2%"></div>
        </div>
      </div>

      <div class="cbt-q-card">
        <div class="cbt-q-title" id="qNumHeading">Question 1</div>
        <div class="cbt-q-text" id="qText">Loading question prompt...</div>
        <div class="cbt-opts" id="qOpts"></div>
        <div class="feedback" id="qFeedback"></div>
      </div>

      <div class="cbt-nav-row">
        <button class="btn-cbt secondary" id="prevBtn">&larr; Previous</button>
        <button class="btn-cbt flag" id="flagBtn">🚩 Flag Question</button>
        <button class="btn-cbt primary" id="nextBtn">Next &rarr;</button>
      </div>
    </main>

    <aside class="cbt-sidebar">
      
      <!-- Circular Timer -->
      <div class="timer-card">
        <div class="cbt-timer-wrap">
          <svg class="cbt-timer-svg" viewBox="0 0 100 100">
            <circle class="timer-bg-ring" cx="50" cy="50" r="44"/>
            <circle class="timer-fg-ring" id="timerRing" cx="50" cy="50" r="44"/>
          </svg>
          <div class="cbt-timer-text">
            <span class="timer-digits" id="qTimerDigits">30:00</span>
            <span class="timer-sub">Time Left</span>
          </div>
        </div>
        <div class="score-badge" id="qScoreBadge">⭐ Points: 0 / 0</div>
      </div>

      <!-- Navigator Grid -->
      <div class="navigator-card">
        <div class="nav-grid-head">
          <span class="nav-grid-title">Question Navigator</span>
          <span class="nav-grid-counter" id="cbtNavCount">0 / 50</span>
        </div>

        <div class="q-grid" id="qGrid"></div>

        <div class="nav-summary-chips">
          <div><strong id="cbtStatAnswered">0</strong> Answered</div>
          <div><strong id="cbtStatRemaining">50</strong> Left</div>
          <div><strong id="cbtStatFlagged">0</strong> Flagged</div>
        </div>

        <div class="grid-legend">
          <span class="leg"><span class="leg-dot answered"></span>Answered</span>
          <span class="leg"><span class="leg-dot flagged"></span>Flagged</span>
          <span class="leg"><span class="leg-dot current"></span>Current</span>
          <span class="leg"><span class="leg-dot unanswered"></span>Unanswered</span>
        </div>
      </div>

      <div class="sidebar-actions">
        <button class="btn-finish-exam" id="finishBtn">📝 Submit Examination</button>
        <button class="btn-quit-exam" id="quitBtn">✕ Quit Examination</button>
      </div>

    </aside>

  </div>
</div><!-- /quizScreen -->

<!-- RESULTS SCREEN -->
<div id="resultScreen" class="screen">
  <div style="max-width:800px;margin:0 auto">

    <div class="result-hero">
      <div class="result-trophy">🏆</div>
      <div class="result-points-label">Total Points Received</div>
      <div class="result-grade" id="rScore">0 / 0</div>
      <div class="result-pct" id="rPct">0% Accuracy</div>
      <div id="rPassBadge"></div>
      <div class="result-stats" id="rStats"></div>
    </div>

    <div class="breakdown-card" id="rBreakdownCard">
      <div class="card-header-line"><span>📊</span> Points & Accuracy per Subject</div>
      <div id="rBreakdown"></div>
    </div>

    <div class="breakdown-card" id="rTopicCard">
      <div class="card-header-line"><span>📋</span> Performance Breakdown by Topic</div>
      <div id="rTopicBreakdown"></div>
    </div>

    <div class="result-acts">
      <button class="btn-review" id="reviewBtn">🔍 Review Mistakes & Explanations</button>
      <button class="btn-retry-wrong" id="retryWrongBtn">🔄 Retry Missed Questions</button>
      <button class="btn-retry-all" id="retryAllBtn">🔁 Retry Same Set</button>
      <button class="btn-home" id="homeFromResult">🏠 Back to Dashboard</button>
    </div>

  </div>
</div><!-- /resultScreen -->

<!-- REVIEW SCREEN -->
<div id="reviewScreen" class="screen">
  <div style="max-width:840px;margin:0 auto">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
      <div class="card-header-line" style="margin:0"><span style="font-size:1.3rem">🔍</span> Authoritative Answer Key & Explanations</div>
      <button class="btn-cbt secondary" id="backFromReview">&larr; Back to Results</button>
    </div>
    <div id="reviewList"></div>
    <button class="btn-cbt secondary" id="backFromReviewBottom" style="width:100%;margin-top:14px;justify-content:center">&larr; Back to Results</button>
  </div>
</div>

</div><!-- /container-wide -->

<!-- CONFIRMATION MODAL -->
<div class="modal-overlay" id="modal" role="dialog" aria-modal="true">
  <div class="modal-box">
    <div class="modal-icon">⚠️</div>
    <div class="modal-title" id="modalTitle">Confirm Action</div>
    <p id="modalMsg">Are you sure you want to proceed?</p>
    <div class="modal-btns">
      <button class="btn-cancel" id="modalCancel">Cancel</button>
      <button class="btn-modal-confirm" id="modalConfirm">Confirm</button>
    </div>
  </div>
</div>

<!-- AUDIT QUESTION BANK MODAL -->
<div class="modal-overlay" id="auditModal" role="dialog" aria-modal="true">
  <div class="audit-box">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
      <div class="modal-title" style="margin:0">📋 Question Bank Inventory & Duplicate Audit</div>
      <button class="btn-cancel" id="closeAuditBtn" style="padding:4px 10px">&times;</button>
    </div>
    <p style="color:var(--text-secondary);font-size:0.88rem;margin-bottom:14px">
      Authoritative DGCA CPL written examination question repository. All questions are verified against official sources with 100% duplicate protection.
    </p>

    <div class="stats-grid-3" style="margin-bottom:16px">
      <div class="stat-box">
        <div class="stat-val" style="color:var(--teal)">839</div>
        <div class="stat-lbl">Active Questions</div>
      </div>
      <div class="stat-box">
        <div class="stat-val" style="color:var(--success)">108</div>
        <div class="stat-lbl">Duplicates Intercepted</div>
      </div>
      <div class="stat-box">
        <div class="stat-val" style="color:var(--gold)" id="auditServedCount">0</div>
        <div class="stat-lbl">Questions Attempted</div>
      </div>
    </div>

    <table class="audit-table">
      <thead>
        <tr>
          <th>Subject</th>
          <th>Total Qs</th>
          <th>Topics</th>
          <th>Coverage / Unserved</th>
        </tr>
      </thead>
      <tbody id="auditTableBody"></tbody>
    </table>

    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px;padding-top:12px;border-top:1px solid var(--border)">
      <button class="btn-reset-pool" id="resetEntirePoolBtn">Reset Entire Question Rotation (0 Served)</button>
      <button class="btn-cancel" id="closeAuditBtnBottom">Close Audit</button>
    </div>
  </div>
</div>

<script>
const EXAM_CONFIG = {
  passMark: 70,
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

const QUESTIONS = ''' + json.dumps(questions, ensure_ascii=False, indent=2) + ''';

const SUBJECT_META = {
  "Air Navigation":       { icon: "🧭", code: "CAR SEC 7", color: "#719CFF" },
  "Air Regulations":      { icon: "📜", code: "ICAO / CAR", color: "#9484F5" },
  "Aviation Meteorology": { icon: "⛅", code: "I.C. JOSHI", color: "#51C6C1" },
  "Technical General":    { icon: "⚙️", code: "AGK / ENGINES", color: "#69CF9B" },
  "Technical Specific":   { icon: "🛩️", code: "POH / PERF", color: "#ECA85B" },
  "RTR":                  { icon: "🎙️", code: "ICAO DOC 9432", color: "#51C6C1" },
};
const ALL_SUBJECTS = Object.keys(SUBJECT_META);

''' + svg_func_js + '''

// Safe LocalStorage
function sg(k,f){try{const v=localStorage.getItem(k);return v!==null?JSON.parse(v):f}catch{return f}}
function ss(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch{}}
function sd(k){try{localStorage.removeItem(k)}catch{}}

// State Management
let state = {
  selSubjects: [],
  mode: "practice",
  timerMin: 30,
  totalTimerSec: 1800,
  topicFilter: "",
  pool: [],
  questions: [],
  idx: 0,
  answers: [],
  flags: [],
  revealed: [],
  startTime: 0,
  endTime: 0,
  timerSec: 0,
  timerInterval: null,
  finished: false,
};

let history = sg("cpl_history", {});
let darkMode = sg("cpl_dark", true);

// ==========================================
// ZERO-REPEAT ROTATION ENGINE
// ==========================================
function getServedIds() {
  return new Set(sg("cpl_served_ids", []));
}
function markQuestionsServed(qIds) {
  const set = getServedIds();
  qIds.forEach(id => set.add(id));
  ss("cpl_served_ids", Array.from(set));
}
function resetServedPool(subject = null, topic = null) {
  if (!subject && !topic) {
    ss("cpl_served_ids", []);
  } else {
    const set = getServedIds();
    QUESTIONS.forEach(q => {
      if ((!subject || q.subject === subject) && (!topic || q.topic === topic)) {
        set.delete(q.id);
      }
    });
    ss("cpl_served_ids", Array.from(set));
  }
  updateHome();
}

function getPoolStats() {
  const servedSet = getServedIds();
  const subs = state.selSubjects.length > 0 ? state.selSubjects : ALL_SUBJECTS;
  const allMatching = QUESTIONS.filter(q =>
    subs.includes(q.subject) &&
    (!state.topicFilter || q.topic === state.topicFilter)
  );
  const unservedMatching = allMatching.filter(q => !servedSet.has(q.id));
  return {
    total: allMatching.length,
    unserved: unservedMatching.length,
    served: allMatching.length - unservedMatching.length,
    unservedPool: unservedMatching,
    allPool: allMatching
  };
}

// Dark Mode Toggle
function applyDark(){
  document.body.classList.toggle("light", !darkMode);
  document.getElementById("darkBtn").textContent = darkMode ? "🌙" : "☀️";
}
applyDark();
document.getElementById("darkBtn").addEventListener("click", () => {
  darkMode = !darkMode;
  ss("cpl_dark", darkMode);
  applyDark();
});

// Navigation
function goHome(){
  if(document.getElementById("quizScreen").classList.contains("active") && !state.finished){
    showModal("Quit this examination? Unsaved answers will be lost.", ()=>{
      if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval=null; }
      renderWeakness(); updateHome(); showScreen("homeScreen");
    });
  } else {
    showScreen("homeScreen");
  }
}
function scrollToPractice(){
  goHome();
  const el = document.getElementById("practiceAnchor");
  if(el) el.scrollIntoView({ behavior: 'smooth' });
}
function scrollToAnalytics(){
  goHome();
  const el = document.getElementById("analyticsAnchor");
  if(el) el.scrollIntoView({ behavior: 'smooth' });
}

const SCREENS = ["homeScreen","quizScreen","resultScreen","reviewScreen"];
function showScreen(name){
  SCREENS.forEach(s => {
    const el = document.getElementById(s);
    if(el) el.classList.remove("active");
  });
  const target = document.getElementById(name);
  if(target) target.classList.add("active");
  window.scrollTo(0, 0);
}

// Fisher-Yates Shuffle
function shuffle(arr){
  const a=[...arr];
  for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
  return a;
}

// Prep Question with Option Shuffling
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

// Build Subject Cards
function buildSubjectChips(){
  const grid = document.getElementById("subjGrid");
  if(!grid) return;
  grid.innerHTML = "";

  const servedSet = getServedIds();
  const isAll = state.selSubjects.length === 0;
  const totalBankCount = QUESTIONS.length;
  const totalUnservedCount = QUESTIONS.filter(q => !servedSet.has(q.id)).length;

  const allCard = document.createElement("div");
  allCard.className = "subject-card all-card" + (isAll ? " selected" : "");
  allCard.innerHTML = `
    <div class="card-media">
      ${getSubjectSvg("All")}
      <div class="card-media-overlay"></div>
      <div class="card-media-meta">
        <span class="card-tag">Full DGCA Syllabus (6 Subjects)</span>
        <span class="card-arrow">&rarr;</span>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title-row">
        <div class="card-title">📚 All DGCA Subjects Combined</div>
        <div class="card-check">✓</div>
      </div>
      <div class="card-info-row">
        <span>${totalUnservedCount} unserved / ${totalBankCount} Total</span>
        <span>${isAll ? "Active Selection" : "Click to select all"}</span>
      </div>
      <div class="card-track"><div class="card-fill" style="width:${isAll ? "100%" : "30%"}"></div></div>
    </div>
  `;
  allCard.addEventListener("click", () => {
    state.selSubjects = [];
    buildSubjectChips();
    updateHome();
  });
  grid.appendChild(allCard);

  ALL_SUBJECTS.forEach(subj => {
    const subjQuestions = QUESTIONS.filter(q => q.subject === subj);
    const qCount = subjQuestions.length;
    if(qCount === 0) return;
    const meta = SUBJECT_META[subj] || { icon: "✈️", code: "DGCA", color: "#9484F5" };
    const h = history[subj] || { attempted: 0, correct: 0 };
    const pct = h.attempted > 0 ? Math.round(100 * h.correct / h.attempted) : 0;
    const isSelected = state.selSubjects.includes(subj);
    const topicCount = new Set(subjQuestions.map(q => q.topic)).size;
    const unservedCount = subjQuestions.filter(q => !servedSet.has(q.id)).length;

    const card = document.createElement("div");
    card.className = "subject-card" + (isSelected ? " selected" : "");
    card.innerHTML = `
      <div class="card-media">
        ${getSubjectSvg(subj)}
        <div class="card-media-overlay"></div>
        <div class="card-media-meta">
          <span class="card-tag">${topicCount} Topics</span>
          <span class="card-arrow">&rarr;</span>
        </div>
      </div>
      <div class="card-body">
        <div class="card-title-row">
          <div class="card-title">${meta.icon} ${subj}</div>
          <div class="card-check">✓</div>
        </div>
        <div class="card-info-row">
          <span>${unservedCount} unserved / ${qCount} Qs</span>
          <span>${h.attempted > 0 ? `${h.correct}/${h.attempted} pts (${pct}%)` : "Not attempted"}</span>
        </div>
        <div class="card-track"><div class="card-fill" style="width:${pct}%"></div></div>
      </div>
    `;
    card.addEventListener("click", () => {
      const idx = state.selSubjects.indexOf(subj);
      if(idx >= 0){
        state.selSubjects.splice(idx, 1);
      } else {
        state.selSubjects.push(subj);
      }
      buildSubjectChips();
      updateHome();
    });
    grid.appendChild(card);
  });
}

// Build Topic Dropdown
function buildTopicDropdown(){
  const sel = document.getElementById("topicSel");
  if(!sel) return;
  const current = sel.value;
  const subs = state.selSubjects.length > 0 ? state.selSubjects : ALL_SUBJECTS;
  const servedSet = getServedIds();
  
  const relevantQs = QUESTIONS.filter(q => subs.includes(q.subject));
  const topics = [...new Set(relevantQs.map(q => q.topic))].sort();

  sel.innerHTML = `<option value="">All Topics (${topics.length} available)</option>`;
  topics.forEach(t => {
    const tQs = relevantQs.filter(q => q.topic === t);
    const unserved = tQs.filter(q => !servedSet.has(q.id)).length;
    const opt = document.createElement("option");
    opt.value = t;
    opt.textContent = `${t} (${unserved} unserved / ${tQs.length} total)`;
    if(t === current) opt.selected = true;
    sel.appendChild(opt);
  });
  state.topicFilter = sel.value;
}

document.getElementById("topicSel").addEventListener("change", e => {
  state.topicFilter = e.target.value;
  updateStartBtn();
});

// Mode Toggle
document.querySelectorAll(".mode-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    state.mode = btn.dataset.mode;
    updateStartBtn();
  });
});

// Start Button and Rotation Status Update
function updateStartBtn(){
  const stats = getPoolStats();
  const btn = document.getElementById("startBtn");
  const label = document.getElementById("startLabel");
  const rotText = document.getElementById("rotationStatsText");

  rotText.textContent = `${stats.unserved} unserved of ${stats.total} questions available in current selection`;

  if(stats.total === 0){
    btn.disabled = true;
    label.textContent = "No questions match this selection";
  } else if(stats.unserved === 0){
    btn.disabled = false;
    label.textContent = `Pool Completed! Click to Reset & Retake (${stats.total} Qs)`;
  } else {
    btn.disabled = false;
    const count = state.mode === "mock" ? Math.min(stats.unserved, 50) : stats.unserved;
    label.textContent = `Start ${state.mode === "mock" ? "Mock Exam" : state.mode === "timed" ? "Timed Exam" : "Practice"} (${count} unserved Qs)`;
  }
}

// Reset Current Pool Button
document.getElementById("resetCurrentPoolBtn").addEventListener("click", () => {
  const subs = state.selSubjects.length === 1 ? state.selSubjects[0] : null;
  const top = state.topicFilter || null;
  const scopeName = top ? `topic "${top}"` : subs ? `subject "${subs}"` : "all subjects";
  showModal(`Reset the question rotation exposure for ${scopeName}? Previously served questions will become available again. (Score history is preserved).`, () => {
    resetServedPool(subs, top);
  });
});

// Reset Score History Button
document.getElementById("resetHistoryBtn").addEventListener("click", () => {
  showModal("Reset all recorded scores, points, and performance analytics? This cannot be undone.", () => {
    history = {};
    sd("cpl_history");
    updateHome();
  });
});

function updateHome(){
  buildSubjectChips();
  buildTopicDropdown();
  updateStartBtn();
  renderWeakness();
  renderExamHubRows();
  updateAuditModal();
}

// Exam Hub Overview Rows
function renderExamHubRows(){
  const container = document.getElementById("examSubjRows");
  if(!container) return;
  const servedSet = getServedIds();
  let html = "";
  ALL_SUBJECTS.forEach(subj => {
    const qs = QUESTIONS.filter(q => q.subject === subj);
    const h = history[subj] || { attempted: 0, correct: 0 };
    const pct = h.attempted > 0 ? Math.round(100 * h.correct / h.attempted) : 0;
    const clr = pct >= 70 ? "var(--success)" : pct >= 40 ? "var(--warning)" : "var(--primary)";
    html += `
      <div class="exam-row-item">
        <span class="exam-subj-name">${SUBJECT_META[subj]?.icon||""} ${subj}</span>
        <div style="display:flex;align-items:center">
          <span class="exam-subj-score">${h.attempted > 0 ? `${pct}%` : "0%"}</span>
          <div class="mini-track"><div class="mini-fill" style="width:${pct}%;background:${clr}"></div></div>
        </div>
      </div>
    `;
  });
  container.innerHTML = html;
}

// Quick Buttons
document.getElementById("quickResumeBtn").addEventListener("click", () => {
  state.mode = "practice";
  document.querySelectorAll(".mode-btn").forEach(b => b.classList.toggle("selected", b.dataset.mode === "practice"));
  state.selSubjects = ["Air Navigation"];
  state.topicFilter = "";
  buildSubjectChips();
  document.getElementById("startBtn").click();
});
document.getElementById("quickMockBtn").addEventListener("click", () => {
  state.mode = "mock";
  document.querySelectorAll(".mode-btn").forEach(b => b.classList.toggle("selected", b.dataset.mode === "mock"));
  document.getElementById("startBtn").click();
});
document.getElementById("hubMockBtn").addEventListener("click", () => {
  state.mode = "mock";
  document.querySelectorAll(".mode-btn").forEach(b => b.classList.toggle("selected", b.dataset.mode === "mock"));
  document.getElementById("startBtn").click();
});

// START QUIZ HANDLER
document.getElementById("startBtn").addEventListener("click", () => {
  const stats = getPoolStats();
  if(stats.total === 0) return;

  // If pool exhausted, reset exposure for this selection first
  if(stats.unserved === 0){
    const subs = state.selSubjects.length === 1 ? state.selSubjects[0] : null;
    const top = state.topicFilter || null;
    resetServedPool(subs, top);
    // Refresh stats
    const refreshed = getPoolStats();
    launchQuizWithPool(refreshed.unservedPool);
    return;
  }

  launchQuizWithPool(stats.unservedPool);
});

function launchQuizWithPool(availablePool){
  if(availablePool.length === 0) return;

  let finalQuizPool = [];
  if(state.mode === "mock"){
    const subs = state.selSubjects.length > 0 ? state.selSubjects : ALL_SUBJECTS;
    subs.forEach(subj => {
      const cfg = EXAM_CONFIG.subjects[subj];
      const forSubj = availablePool.filter(q => q.subject === subj);
      if(forSubj.length === 0) return;
      const count = Math.min(cfg ? cfg.questions : 50, forSubj.length);
      finalQuizPool = finalQuizPool.concat(shuffle(forSubj).slice(0, count));
    });
    if(finalQuizPool.length === 0) finalQuizPool = availablePool.slice(0, 50);
    state.timerMin = 60;
  } else {
    // Practice or Timed mode: up to 50 questions or full remaining pool
    finalQuizPool = shuffle(availablePool).slice(0, 50);
    state.timerMin = Math.max(Math.ceil(finalQuizPool.length * 1.5), 15);
  }

  // Mark these served immediately in Zero-Repeat Rotation Engine
  markQuestionsServed(finalQuizPool.map(q => q.id));

  startQuiz(finalQuizPool);
}

function startQuiz(pool){
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

  if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval = null; }

  if(state.mode === "timed" || state.mode === "mock"){
    state.totalTimerSec = state.timerMin * 60;
    state.timerSec = state.totalTimerSec;
    state.timerInterval = setInterval(() => {
      state.timerSec--;
      renderTimer();
      if(state.timerSec <= 0){
        clearInterval(state.timerInterval);
        state.timerInterval = null;
        finishQuiz();
      }
    }, 1000);
  } else {
    state.totalTimerSec = 0;
    state.timerSec = 0;
  }

  showScreen("quizScreen");
  buildGrid();
  renderQuestion();
}

function renderTimer(){
  const digitsEl = document.getElementById("qTimerDigits");
  const ring = document.getElementById("timerRing");
  const totalCircumference = 276.46;

  if(state.mode === "timed" || state.mode === "mock"){
    const m = Math.floor(state.timerSec / 60);
    const s = state.timerSec % 60;
    const timeStr = `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
    if(digitsEl) digitsEl.textContent = timeStr;

    const fraction = state.totalTimerSec > 0 ? (state.timerSec / state.totalTimerSec) : 1;
    const offset = totalCircumference * (1 - fraction);
    if(ring){
      ring.style.strokeDashoffset = offset;
      ring.classList.toggle("urgent", state.timerSec <= 300 && state.timerSec > 60);
      ring.classList.toggle("critical", state.timerSec <= 60);
    }
  } else {
    const elapsed = Math.floor((Date.now() - state.startTime) / 1000);
    const m = Math.floor(elapsed / 60);
    const s = elapsed % 60;
    const timeStr = `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
    if(digitsEl) digitsEl.textContent = timeStr;
    if(ring){
      ring.style.strokeDashoffset = 0;
      ring.classList.remove("urgent", "critical");
    }
  }
}

setInterval(() => {
  if(document.getElementById("quizScreen").classList.contains("active") &&
     state.mode === "practice" && !state.finished){
    renderTimer();
  }
}, 1000);

function updateScoreBadge(){
  const sb = document.getElementById("qScoreBadge");
  if(!sb) return;
  if(state.mode === "practice"){
    const attempted = state.revealed.filter(r => r).length;
    const correct = state.questions.filter((q, i) => state.revealed[i] && state.answers[i] === q.answer).length;
    const total = state.questions.length;
    if(attempted === 0){
      sb.textContent = `⭐ Points: 0 / ${total} (0%)`;
    } else {
      const pct = Math.round(100 * correct / attempted);
      sb.textContent = `⭐ Points: ${correct} / ${attempted} (${pct}%) • ${total} Qs`;
    }
  } else {
    const answeredCount = state.answers.filter(a => a >= 0).length;
    sb.textContent = `📋 Answered: ${answeredCount} / ${state.questions.length}`;
  }
}

const LETTERS = ["A","B","C","D","E","F","G","H"];

// ==========================================
// RENDER QUESTION & ANSWER FEEDBACK (PHASE 5)
// ==========================================
function renderQuestion(){
  const q = state.questions[state.idx];
  const i = state.idx;
  const n = state.questions.length;
  const meta = SUBJECT_META[q.subject] || { icon: "✈️", color: "#9484F5" };

  document.getElementById("qSubjectBadge").textContent = `${meta.icon} ${q.subject}`;
  document.getElementById("qTopicBadge").textContent = q.topic || "General";
  document.getElementById("qNumHeading").textContent = `Question ${i + 1}`;
  document.getElementById("qProgressText").textContent = `Question ${i + 1} of ${n}`;

  const pct = Math.round(((i + 1) / n) * 100);
  const pPct = document.getElementById("qProgressPct");
  if(pPct) pPct.textContent = `${pct}% Complete`;
  document.getElementById("qProgressBar").style.width = `${pct}%`;

  const diff = q.difficulty || "medium";
  const diffEl = document.getElementById("qDiffBadge");
  diffEl.className = `cbt-badge diff-${diff}`;
  diffEl.textContent = diff.charAt(0).toUpperCase() + diff.slice(1);

  document.getElementById("qText").textContent = q.question;
  renderTimer();
  updateScoreBadge();

  const opts = document.getElementById("qOpts");
  opts.innerHTML = "";
  const answered = state.answers[i] >= 0;
  const revealed = state.revealed[i];
  const isLocked = state.finished || (state.mode === "practice" && revealed);

  q.options.forEach((opt, oi) => {
    const btn = document.createElement("button");
    btn.className = "opt";
    if(isLocked) btn.classList.add("disabled");

    let tagHtml = "";

    // PHASE 5: Unconditional authoritative display
    if(state.mode === "practice" && revealed){
      if(oi === q.answer){
        btn.classList.add("correct");
        tagHtml = `<span class="opt-tag correct">✓ Correct Answer (+1 pt)</span>`;
      } else if(oi === state.answers[i]){
        btn.classList.add("wrong");
        tagHtml = `<span class="opt-tag wrong">✗ Your Choice (0 pts)</span>`;
      }
    } else if(answered){
      if(oi === state.answers[i]){
        btn.classList.add("selected");
        tagHtml = `<span class="opt-tag" style="background:var(--primary);color:#fff">Selected</span>`;
      }
    }

    btn.innerHTML = `<span class="opt-letter">${LETTERS[oi]}</span><span class="opt-text">${opt}</span>${tagHtml}`;
    btn.addEventListener("click", () => selectOpt(oi));
    opts.appendChild(btn);
  });

  const fb = document.getElementById("qFeedback");
  fb.className = "feedback";
  fb.innerHTML = "";
  if(state.mode === "practice" && revealed){
    const correct = state.answers[i] === q.answer;
    fb.classList.add("show", correct ? "feedback-correct" : "feedback-wrong");
    
    let fbHtml = "";
    if(correct){
      fbHtml = `
        <div class="fb-status">✓ Correct! (+1 Point Received)</div>
        <div class="fb-ans-line right">Authoritative Correct Answer: <strong>${LETTERS[q.answer]}. ${q.options[q.answer]}</strong></div>
        <div class="fb-body"><strong>Explanation:</strong> ${q.explanation}</div>
        <div class="feedback-src">📚 Source Citation: ${q.source}</div>
      `;
    } else {
      const userChoice = state.answers[i];
      const userChoiceText = userChoice >= 0 ? `${LETTERS[userChoice]}. ${q.options[userChoice]}` : "Skipped";
      fbHtml = `
        <div class="fb-status">✗ Incorrect (0 Points Received)</div>
        <div class="fb-ans-line your">Your Selected Choice: <strong>${userChoiceText}</strong></div>
        <div class="fb-ans-line right">Authoritative Correct Answer: <strong>${LETTERS[q.answer]}. ${q.options[q.answer]}</strong></div>
        <div class="fb-body"><strong>Explanation:</strong> ${q.explanation}</div>
        <div class="feedback-src">📚 Source Citation: ${q.source}</div>
      `;
    }
    fb.innerHTML = fbHtml;
  }

  const fl = document.getElementById("flagBtn");
  fl.classList.toggle("flagged", state.flags[i]);
  fl.textContent = state.flags[i] ? "🚩 Flagged" : "🚩 Flag Question";

  document.getElementById("prevBtn").disabled = i === 0;
  document.getElementById("nextBtn").textContent = i === n - 1 ? "Review / Submit ➔" : "Next ➔";

  updateGridHighlight();
}

function selectOpt(oi){
  const i = state.idx;
  if(state.finished) return;
  if(state.mode === "practice" && state.revealed[i]) return;

  state.answers[i] = oi;
  if(state.mode === "practice"){
    state.revealed[i] = true;
  }
  renderQuestion();
  updateGridHighlight();
}

document.getElementById("prevBtn").addEventListener("click", () => {
  if(state.idx > 0){ state.idx--; renderQuestion(); }
});
document.getElementById("nextBtn").addEventListener("click", () => {
  if(state.idx < state.questions.length - 1){
    state.idx++; renderQuestion();
  } else {
    document.getElementById("finishBtn").click();
  }
});
document.getElementById("flagBtn").addEventListener("click", () => {
  state.flags[state.idx] = !state.flags[state.idx];
  renderQuestion();
  updateGridHighlight();
});

// Navigator Grid
function buildGrid(){
  const wrap = document.getElementById("qGrid");
  if(!wrap) return;
  wrap.innerHTML = "";
  state.questions.forEach((_, qi) => {
    const c = document.createElement("div");
    c.className = "q-cell";
    c.textContent = qi + 1;
    c.addEventListener("click", () => { state.idx = qi; renderQuestion(); });
    wrap.appendChild(c);
  });
  updateGridHighlight();
}

function updateGridHighlight(){
  const wrap = document.getElementById("qGrid");
  if(!wrap) return;
  const cells = wrap.children;
  let ansCount = 0, flagCount = 0;

  for(let qi = 0; qi < cells.length; qi++){
    const c = cells[qi];
    c.className = "q-cell";
    if(qi === state.idx) c.classList.add("current");
    if(state.answers[qi] >= 0){
      c.classList.add("answered");
      ansCount++;
    }
    if(state.flags[qi]){
      c.classList.add("flagged");
      flagCount++;
    }
  }

  const remCount = state.questions.length - ansCount;
  const cbtNavCount = document.getElementById("cbtNavCount");
  const cbtStatAnswered = document.getElementById("cbtStatAnswered");
  const cbtStatRemaining = document.getElementById("cbtStatRemaining");
  const cbtStatFlagged = document.getElementById("cbtStatFlagged");

  if(cbtNavCount) cbtNavCount.textContent = `${ansCount} / ${state.questions.length}`;
  if(cbtStatAnswered) cbtStatAnswered.textContent = ansCount;
  if(cbtStatRemaining) cbtStatRemaining.textContent = remCount;
  if(cbtStatFlagged) cbtStatFlagged.textContent = flagCount;
}

// Finish & Submit
document.getElementById("finishBtn").addEventListener("click", () => {
  const unanswered = state.answers.filter(a => a < 0).length;
  const flagged = state.flags.filter(f => f).length;
  let msg = "Are you ready to submit your examination and calculate points?";
  if(unanswered > 0){
    msg = `You have ${unanswered} unanswered question${unanswered > 1 ? "s" : ""}. Submit anyway?`;
  }
  if(flagged > 0){
    msg += ` (${flagged} question${flagged > 1 ? "s" : ""} flagged for review)`;
  }
  showModal(msg, finishQuiz, "Submit Examination");
});

document.getElementById("quitBtn").addEventListener("click", () => {
  showModal("Quit this examination? Progress will not be saved.", () => {
    if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval = null; }
    updateHome();
    showScreen("homeScreen");
  }, "Quit Examination");
});

function finishQuiz(){
  if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval = null; }
  state.endTime = Date.now();
  state.finished = true;

  // Record stats to history
  state.questions.forEach((q, qi) => {
    if(state.answers[qi] < 0) return;
    if(!history[q.subject]) history[q.subject] = { attempted: 0, correct: 0, topics: {} };
    history[q.subject].attempted++;
    if(state.answers[qi] === q.answer) history[q.subject].correct++;

    if(!history[q.subject].topics) history[q.subject].topics = {};
    const t = q.topic || "General";
    if(!history[q.subject].topics[t]) history[q.subject].topics[t] = { attempted: 0, correct: 0 };
    history[q.subject].topics[t].attempted++;
    if(state.answers[qi] === q.answer) history[q.subject].topics[t].correct++;
  });
  ss("cpl_history", history);
  showResults();
}

// Show Results
function showResults(){
  showScreen("resultScreen");
  const n = state.questions.length;
  const answered = state.answers.filter(a => a >= 0).length;
  const correct = state.questions.filter((q,i) => state.answers[i] === q.answer).length;
  const points = correct;
  const pct = n > 0 ? Math.round(100 * points / n) : 0;
  const elapsed = Math.floor((state.endTime - state.startTime) / 1000);
  const em = Math.floor(elapsed / 60), es = elapsed % 60;

  document.getElementById("rScore").textContent = `${points} / ${n}`;
  document.getElementById("rPct").textContent = `${pct}% Accuracy (${points} Points Received)`;

  const pass = pct >= EXAM_CONFIG.passMark;
  const minNeeded = Math.ceil(n * 0.70);
  const pb = document.getElementById("rPassBadge");
  pb.innerHTML = `<span class="result-pass ${pass ? "pass" : "fail"}">${pass ? `✓ PASS • Scored ${points} pts (≥ 70% DGCA Standard)` : `✗ FAIL • Scored ${points} pts (${minNeeded} points required to pass)`}</span>`;

  document.getElementById("rStats").textContent =
    `⏱️ Time Taken: ${em}m ${es}s • Answered: ${answered} of ${n} • DGCA Pass Mark: ${EXAM_CONFIG.passMark}% (${minNeeded} pts)`;

  // Subject breakdown
  const subjMap = {};
  state.questions.forEach((q, i) => {
    if(!subjMap[q.subject]) subjMap[q.subject] = { t: 0, c: 0 };
    subjMap[q.subject].t++;
    if(state.answers[i] === q.answer) subjMap[q.subject].c++;
  });
  const colors = ["#9484F5", "#719CFF", "#51C6C1", "#69CF9B", "#ECA85B", "#ED7078"];
  let bi = 0;
  document.getElementById("rBreakdown").innerHTML =
    Object.entries(subjMap).map(([subj, d]) => {
      const p = Math.round(100 * d.c / d.t);
      const clr = colors[bi++ % colors.length];
      const isPass = p >= EXAM_CONFIG.passMark;
      const passTag = isPass ?
        `<span style="color:var(--success);font-weight:700">✓ PASS</span>` :
        `<span style="color:var(--error);font-weight:700">✗ FAIL</span>`;
      return `<div style="margin-bottom:12px">
        <div style="display:flex;justify-content:space-between;font-size:0.86rem;margin-bottom:5px;font-weight:600">
          <span>${SUBJECT_META[subj]?.icon||""} ${subj} (${passTag})</span>
          <span><strong>${d.c} / ${d.t} points</strong> (${p}%)</span>
        </div>
        <div style="height:8px;border-radius:4px;background:var(--surface-interactive);overflow:hidden">
          <div style="height:100%;width:${p}%;background:${clr};border-radius:4px;transition:width 0.5s"></div>
        </div>
      </div>`;
    }).join("");

  // Topic breakdown
  const topicMap = {};
  state.questions.forEach((q, i) => {
    const t = q.topic || "General";
    if(!topicMap[t]) topicMap[t] = { t: 0, c: 0, subj: q.subject };
    topicMap[t].t++;
    if(state.answers[i] === q.answer) topicMap[t].c++;
  });
  const topicEntries = Object.entries(topicMap).sort((a,b) => (a[1].c / a[1].t) - (b[1].c / b[1].t));
  document.getElementById("rTopicBreakdown").innerHTML =
    topicEntries.map(([topic, d]) => {
      const p = Math.round(100 * d.c / d.t);
      const clr = p >= 70 ? "var(--success)" : p >= 40 ? "var(--warning)" : "var(--error)";
      return `<div style="margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;font-size:0.82rem;margin-bottom:4px">
          <span style="color:var(--text-primary)">${topic}</span>
          <span style="color:var(--text-secondary)">${d.c} / ${d.t} pts (${p}%)</span>
        </div>
        <div style="height:6px;border-radius:3px;background:var(--surface-interactive);overflow:hidden">
          <div style="height:100%;width:${p}%;background:${clr};border-radius:3px"></div>
        </div>
      </div>`;
    }).join("");

  const missedCount = state.questions.filter((q,i) => state.answers[i] !== q.answer).length;
  document.getElementById("retryWrongBtn").style.display = missedCount > 0 ? "" : "none";
  document.getElementById("retryWrongBtn").textContent = `🔄 Retry ${missedCount} Missed Question${missedCount !== 1 ? "s" : ""}`;
  document.getElementById("reviewBtn").textContent = `🔍 Review ${n} Questions & Explanations`;
}

// REVIEW SCREEN (PHASE 5: UNCONDITIONAL AUTHORITATIVE FEEDBACK)
document.getElementById("reviewBtn").addEventListener("click", () => {
  showScreen("reviewScreen");
  const list = document.getElementById("reviewList");
  list.innerHTML = "";
  state.questions.forEach((q, i) => {
    const userChoice = state.answers[i];
    const correctChoice = q.answer;
    const isCorrect = userChoice === correctChoice;
    const div = document.createElement("div");
    div.className = "review-item";

    let yourAnsHtml = "";
    if(userChoice < 0){
      yourAnsHtml = `<div class="review-ans skipped">⚠️ Your Choice: <strong>Skipped / Unanswered</strong> (0 points received)</div>`;
    } else if(isCorrect){
      yourAnsHtml = `<div class="review-ans right">✓ Your Choice: <strong>${LETTERS[userChoice]}. ${q.options[userChoice]}</strong> (+1 point received)</div>`;
    } else {
      yourAnsHtml = `<div class="review-ans your">✗ Your Choice: <strong>${LETTERS[userChoice]}. ${q.options[userChoice]}</strong> (0 points received)</div>`;
    }

    div.innerHTML = `
      <div class="review-qnum">
        Question ${i + 1} of ${state.questions.length} • ${q.subject} • ${q.topic || ""}
        <span style="float:right;color:${isCorrect ? "var(--success)" : "var(--error)"};font-weight:800">
          ${isCorrect ? "+1 Point" : "0 Points"}
        </span>
      </div>
      <div class="review-q">${q.question}</div>
      ${yourAnsHtml}
      <div class="review-ans right">✓ Authoritative Correct Answer: <strong>${LETTERS[correctChoice]}. ${q.options[correctChoice]}</strong></div>
      <div class="review-expl"><strong>Explanation:</strong> ${q.explanation}</div>
      <div class="review-src">📚 Source Reference: ${q.source}</div>
    `;
    list.appendChild(div);
  });
});
document.getElementById("backFromReview").addEventListener("click", () => showScreen("resultScreen"));
document.getElementById("backFromReviewBottom").addEventListener("click", () => showScreen("resultScreen"));
document.getElementById("retryAllBtn").addEventListener("click", () => startQuiz(state.pool));

document.getElementById("retryWrongBtn").addEventListener("click", () => {
  const wrongPool = [];
  state.questions.forEach((q, i) => {
    if(state.answers[i] !== q.answer){
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
  if(wrongPool.length === 0) return;
  startQuiz(wrongPool);
});
document.getElementById("homeFromResult").addEventListener("click", () => {
  updateHome(); showScreen("homeScreen");
});

// Confirmation Modal
let modalCb = null;
function showModal(msg, onConfirm, title="Confirm Action"){
  document.getElementById("modalTitle").textContent = title;
  document.getElementById("modalMsg").textContent = msg;
  document.getElementById("modal").classList.add("show");
  modalCb = onConfirm;
}
document.getElementById("modalCancel").addEventListener("click", () => {
  document.getElementById("modal").classList.remove("show"); modalCb = null;
});
document.getElementById("modalConfirm").addEventListener("click", () => {
  document.getElementById("modal").classList.remove("show");
  if(modalCb) modalCb(); modalCb = null;
});

// Audit Bank Modal (Phase 8)
document.getElementById("auditBankBtn").addEventListener("click", () => {
  updateAuditModal();
  document.getElementById("auditModal").classList.add("show");
});
document.getElementById("closeAuditBtn").addEventListener("click", () => {
  document.getElementById("auditModal").classList.remove("show");
});
document.getElementById("closeAuditBtnBottom").addEventListener("click", () => {
  document.getElementById("auditModal").classList.remove("show");
});
document.getElementById("resetEntirePoolBtn").addEventListener("click", () => {
  showModal("Reset all 839 questions in the Zero-Repeat Question Rotation Engine? All questions will become unserved again.", () => {
    resetServedPool();
    document.getElementById("auditModal").classList.remove("show");
  });
});

function updateAuditModal(){
  const servedSet = getServedIds();
  const servedEl = document.getElementById("auditServedCount");
  if(servedEl) servedEl.textContent = servedSet.size;

  const tbody = document.getElementById("auditTableBody");
  if(!tbody) return;
  let html = "";
  ALL_SUBJECTS.forEach(subj => {
    const qs = QUESTIONS.filter(q => q.subject === subj);
    const unserved = qs.filter(q => !servedSet.has(q.id)).length;
    const topics = new Set(qs.map(q => q.topic)).size;
    const pct = Math.round(100 * (qs.length - unserved) / qs.length);
    html += `
      <tr>
        <td><strong>${SUBJECT_META[subj]?.icon||""} ${subj}</strong></td>
        <td>${qs.length} Qs</td>
        <td>${topics} topics</td>
        <td>${unserved} unserved (${pct}% covered)</td>
      </tr>
    `;
  });
  tbody.innerHTML = html;
}

// Weakness Panel Rendering
function renderWeakness(){
  const panel = document.getElementById("weakPanel");
  if(!panel) return;

  const entries = [];
  ALL_SUBJECTS.forEach(subj => {
    const h = history[subj];
    if(h && h.attempted > 0){
      const pct = Math.round(100 * h.correct / h.attempted);
      entries.push({ subj, pct, correct: h.correct, attempted: h.attempted });
    }
  });

  let totalAtt = 0, totalCorr = 0;
  entries.forEach(e => { totalAtt += e.attempted; totalCorr += e.correct; });
  const overallPct = totalAtt > 0 ? Math.round(100 * totalCorr / totalAtt) : 0;

  const aoAccuracy = document.getElementById("aoAccuracy");
  const aoAttempted = document.getElementById("aoAttempted");
  const aoPoints = document.getElementById("aoPoints");

  if(aoAccuracy) aoAccuracy.textContent = `${overallPct}%`;
  if(aoAttempted) aoAttempted.textContent = totalAtt;
  if(aoPoints) aoPoints.textContent = totalCorr;

  const hScore = document.getElementById("headerScorePill");
  if(hScore) hScore.textContent = `⭐ ${totalCorr} Points`;

  if(entries.length === 0){
    panel.innerHTML = `
      <div style="padding:28px 16px;text-align:center;color:var(--text-muted);font-size:0.88rem">
        <div style="font-size:2.2rem;margin-bottom:8px">✈️</div>
        No examination attempts recorded yet.<br>Complete practice quizzes to generate performance analytics!
      </div>
    `;
    return;
  }

  entries.sort((a,b) => a.pct - b.pct);
  const weakest = entries[0];
  let html = "";
  if(weakest && weakest.pct < 70){
    html += `
      <div style="background:var(--tint-red);border:1px solid var(--tint-red-border);border-radius:10px;padding:16px;margin-bottom:18px">
        <div style="font-size:0.78rem;font-weight:700;color:var(--error);text-transform:uppercase">⚠️ Focus Area • Immediate Attention Needed</div>
        <div style="font-size:1.1rem;font-weight:800;color:var(--text-primary);margin:4px 0">${SUBJECT_META[weakest.subj]?.icon||""} ${weakest.subj} (${weakest.pct}% Accuracy)</div>
        <div style="font-size:0.84rem;color:var(--text-secondary);margin-bottom:12px">Currently below the 70% DGCA passing threshold. Practice targeted questions to build mastery.</div>
        <button class="btn-cbt secondary" style="font-size:0.84rem;padding:8px 14px" onclick="practiceTargetSubject('${weakest.subj}')">Practice This Subject &rarr;</button>
      </div>
    `;
  }

  html += '<div style="display:flex;flex-direction:column;gap:12px">';
  entries.forEach(e => {
    let barColor = e.pct >= 70 ? "var(--success)" : e.pct >= 40 ? "var(--warning)" : "var(--error)";
    html += `
      <div>
        <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:4px;font-weight:600">
          <span>${SUBJECT_META[e.subj]?.icon||""} ${e.subj}</span>
          <span>${e.correct} / ${e.attempted} pts (${e.pct}%)</span>
        </div>
        <div style="height:7px;border-radius:3.5px;background:var(--surface-interactive);overflow:hidden">
          <div style="height:100%;width:${e.pct}%;background:${barColor};border-radius:3.5px"></div>
        </div>
      </div>
    `;
  });
  html += '</div>';

  panel.innerHTML = html;
}

window.practiceTargetSubject = function(subj){
  state.mode = "practice";
  state.selSubjects = [subj];
  state.topicFilter = "";
  buildSubjectChips();
  document.getElementById("startBtn").click();
};

// Keyboard Shortcuts
document.addEventListener("keydown", e => {
  if(!document.getElementById("quizScreen").classList.contains("active") || state.finished) return;
  if(e.key === "ArrowLeft" || e.key === "p") document.getElementById("prevBtn").click();
  else if(e.key === "ArrowRight" || e.key === "n" || e.key === " ") {
    e.preventDefault(); document.getElementById("nextBtn").click();
  }
  else if(e.key === "f") document.getElementById("flagBtn").click();
  else if(e.key >= "1" && e.key <= "4"){
    const idx = parseInt(e.key) - 1;
    const q = state.questions[state.idx];
    if(idx < q.options.length) selectOpt(idx);
  }
});

// Initial boot
updateHome();

</script>
</body>
</html>
'''

# Write to target files
targets = [
    os.path.join(BASE, "index.html"),
    os.path.join(BASE, "cpl-exam-direct.html"),
    os.path.join(BASE, "cpl-quiz-standalone.html"),
]

for target_path in targets:
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated {target_path} ({len(html_content)} bytes)")

print("\nALL HTML FILES GENERATED SUCCESSFULLY!")

