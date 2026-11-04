# -*- coding: utf-8 -*-
import json
import os
import sys

BASE = r"c:\VS Code\Codes\dgcacpllearning"
q_path = os.path.join(BASE, "src", "data", "questions.json")

with open(q_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions.")

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
      <rect x="65" y="30" width="270" height="78" rx="8" fill="#202126" stroke="#40414B" stroke-width="1.4"/>
      <rect x="80" y="42" width="112" height="54" rx="5" fill="#141a20" stroke="#51C6C1" stroke-width="1"/>
      <text x="90" y="58" fill="#81838F" font-size="8" font-weight="700" font-family="sans-serif">COMM 1 ACTIVE</text>
      <text x="90" y="85" fill="#51C6C1" font-size="19" font-weight="900" font-family="monospace">118.700</text>
      <rect x="208" y="42" width="112" height="54" rx="5" fill="#141a20" stroke="#40414B" stroke-width="1"/>
      <text x="218" y="58" fill="#81838F" font-size="8" font-weight="700" font-family="sans-serif">STANDBY</text>
      <text x="218" y="85" fill="#ECA85B" font-size="17" font-weight="800" font-family="monospace">121.500</text>
      <path d="M40 150 Q80 150 110 132 T170 168 T230 132 T290 168 T360 150" stroke="#9484F5" stroke-width="2.2" fill="none" opacity="0.85"/>
      <path d="M40 150 Q80 150 110 141 T170 159 T230 141 T290 159 T360 150" stroke="#51C6C1" stroke-width="1.3" fill="none" opacity="0.5"/>
      <g transform="translate(60, 150)">
        <circle r="10" fill="none" stroke="#719CFF" stroke-width="1" opacity="0.3"/>
        <circle r="18" fill="none" stroke="#719CFF" stroke-width="1" opacity="0.2"/>
        <circle r="26" fill="none" stroke="#719CFF" stroke-width="1" opacity="0.1"/>
      </g>
    </svg>`;
  } else {
    // All Subjects Master
    return `<svg viewBox="0 0 400 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" class="card-svg">
      <defs>
        <linearGradient id="allGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#1f1830"/>
          <stop offset="50%" stop-color="#2a1f44"/>
          <stop offset="100%" stop-color="#130e1f"/>
        </linearGradient>
        <linearGradient id="allSunset" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#9484F5" stop-opacity="0.35"/>
          <stop offset="50%" stop-color="#E5C36C" stop-opacity="0.25"/>
          <stop offset="100%" stop-color="#ED7078" stop-opacity="0.1"/>
        </linearGradient>
      </defs>
      <rect width="400" height="200" fill="url(#allGrad)"/>
      <rect x="0" y="45" width="400" height="65" fill="url(#allSunset)"/>
      <line x1="0" y1="110" x2="400" y2="110" stroke="#E5C36C" stroke-width="1" opacity="0.45"/>
      <polygon points="0,0 65,0 110,200 0,200" fill="#202126" stroke="#40414B" stroke-width="1.4"/>
      <polygon points="400,0 335,0 290,200 400,200" fill="#202126" stroke="#40414B" stroke-width="1.4"/>
      <polygon points="190,0 210,0 205,200 195,200" fill="#292A30" stroke="#40414B" stroke-width="1.4"/>
      <polygon points="45,168 355,168 370,200 30,200" fill="#292A30" stroke="#9484F5" stroke-width="1.4"/>
      <text x="200" y="190" fill="#E5C36C" font-size="10" font-weight="900" text-anchor="middle" font-family="sans-serif">ALL DGCA SYLLABUS PAPERS</text>
    </svg>`;
  }
}
"""

print("Writing direct HTML...")

html_part1 = '''<!DOCTYPE html>
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
  font-weight: 600;
  color: var(--primary);
  letter-spacing: 0.06em;
  text-transform: uppercase;
  display: block;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-secondary);
  padding: 4px;
  border-radius: 30px;
  border: 1px solid var(--border-subtle);
}
.nav-item {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-secondary);
  background: transparent;
  transition: var(--transition);
  display: flex;
  align-items: center;
  gap: 6px;
}
.nav-item:hover { color: var(--text-primary); }
.nav-item.active {
  background: var(--card-elevated);
  color: var(--primary);
  box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  border: 1px solid var(--border);
}
.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.nav-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  border-radius: 20px;
  background: var(--card-primary);
  border: 1px solid var(--border);
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
}
.nav-pill.gold {
  color: var(--gold);
  border-color: rgba(229, 195, 108, 0.35);
  background: rgba(229, 195, 108, 0.08);
}
.nav-pilot-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--aviation-blue));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  border: 2px solid var(--border);
  cursor: pointer;
}
.theme-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--card-primary);
  color: var(--text-primary);
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}
.theme-btn:hover { border-color: var(--primary); color: var(--primary); }

/* Dashboard Styles */
.welcome-section { margin-bottom: 24px; }
.welcome-header { margin-bottom: 20px; }
.welcome-title {
  font-size: 1.85rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.welcome-sub { font-size: 0.96rem; color: var(--text-secondary); }

.quick-banners {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-bottom: 24px;
}
.banner-card {
  padding: 20px 22px;
  border-radius: var(--radius-xl);
  border: 1px solid var(--border);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 120px;
  transition: var(--transition);
  cursor: pointer;
}
.banner-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-focus);
}
.banner-card.resume {
  background: linear-gradient(135deg, rgba(81, 198, 193, 0.14) 0%, rgba(41, 42, 48, 0.95) 75%);
  border-color: rgba(81, 198, 193, 0.3);
}
.banner-card.mock {
  background: linear-gradient(135deg, rgba(148, 132, 245, 0.14) 0%, rgba(41, 42, 48, 0.95) 75%);
  border-color: rgba(148, 132, 245, 0.3);
}
.banner-tag {
  font-size: 0.76rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.banner-card.resume .banner-tag { color: var(--teal); }
.banner-card.mock .banner-tag { color: var(--primary); }
.banner-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.banner-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.2;
}
.banner-desc { font-size: 0.82rem; color: var(--text-secondary); margin-top: 4px; }
.banner-btn {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.84rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}
.banner-card.resume .banner-btn { background: var(--teal); color: #102022; }
.banner-card.mock .banner-btn { background: var(--primary); color: #FFFFFF; }

.summary-stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}
.stat-box {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px 18px;
  position: relative;
  overflow: hidden;
}
.stat-box-title {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.stat-box-val {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}
.stat-box-sub { font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px; }

.dashboard-split {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 24px;
  align-items: start;
}
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
}
.section-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}
.section-sub { font-size: 0.84rem; color: var(--text-muted); }

/* Subject Cards (Ref 2 Style) */
.subject-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.subject-card {
  background: var(--card-primary);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
  display: flex;
  flex-direction: column;
}
.subject-card:hover {
  transform: translateY(-4px);
  border-color: var(--primary);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.4), var(--shadow-glow);
}
.subject-card.selected {
  border-color: var(--primary);
  background: var(--card-elevated);
  box-shadow: 0 0 0 2px var(--primary-glow), var(--shadow-card);
}
.card-media {
  height: 125px;
  position: relative;
  overflow: hidden;
  background: var(--bg-secondary);
}
.card-svg {
  width: 100%;
  height: 100%;
  display: block;
  transition: transform 0.4s ease;
}
.subject-card:hover .card-svg { transform: scale(1.05); }
.card-media-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(25,25,29,0.1) 0%, rgba(41,42,48,0.85) 85%, var(--card-primary) 100%);
  pointer-events: none;
}
.card-media-meta {
  position: absolute;
  top: 10px;
  left: 12px;
  right: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 2;
}
.card-tag {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-primary);
  background: rgba(25, 25, 29, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 3px 8px;
  border-radius: 8px;
  backdrop-filter: blur(8px);
}
.card-arrow {
  color: var(--primary);
  font-weight: 800;
  font-size: 1rem;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(25, 25, 29, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}
.subject-card:hover .card-arrow { transform: translateX(2px); }
.card-body {
  padding: 14px 16px 16px;
  display: flex;
  flex-direction: column;
  flex: 1;
  justify-content: space-between;
}
.card-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.card-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1.2;
}
.card-check {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  border: 2px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 800;
  color: transparent;
  transition: var(--transition);
}
.subject-card.selected .card-check {
  background: var(--primary);
  border-color: var(--primary);
  color: #FFFFFF;
}
.card-info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-secondary);
  margin-top: 4px;
}
.card-track {
  height: 4px;
  border-radius: 2px;
  background: var(--surface-interactive);
  margin-top: 10px;
  overflow: hidden;
}
.card-fill {
  height: 100%;
  border-radius: 2px;
  background: linear-gradient(90deg, var(--teal), var(--primary));
  transition: width 0.4s ease;
}
.subject-card.all-card { grid-column: span 3; }

/* Config Card */
.config-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 22px;
  margin-bottom: 24px;
  box-shadow: var(--shadow-card);
}
.mode-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}
.mode-btn {
  padding: 14px 16px;
  background: var(--card-elevated);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-weight: 700;
  font-size: 0.95rem;
  text-align: left;
  transition: var(--transition);
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.mode-btn:hover {
  border-color: var(--border-focus);
  background: var(--surface-interactive);
}
.mode-btn.selected {
  border-color: var(--primary);
  background: var(--tint-purple);
  color: var(--primary);
  box-shadow: 0 0 0 1px var(--primary);
}
.mode-btn span {
  font-size: 0.76rem;
  font-weight: 400;
  color: var(--text-secondary);
}
.mode-btn.selected span { color: var(--text-primary); }

.filter-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 14px;
  align-items: center;
  margin-bottom: 18px;
}
.topic-select {
  width: 100%;
  padding: 12px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--card-elevated);
  color: var(--text-primary);
  font-size: 0.9rem;
  cursor: pointer;
}
.timer-input-wrap {
  display: none;
  align-items: center;
  gap: 8px;
}
.timer-input-wrap.show { display: flex; }
.timer-input-wrap label { font-size: 0.85rem; color: var(--text-secondary); }
.timer-input-wrap input {
  width: 80px;
  padding: 10px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  background: var(--card-elevated);
  color: var(--text-primary);
  text-align: center;
  font-size: 0.95rem;
  font-weight: 700;
}
.start-btn {
  width: 100%;
  padding: 16px;
  font-size: 1.05rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary) 0%, var(--aviation-blue) 100%);
  color: #FFFFFF;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 4px 16px rgba(148, 132, 245, 0.35);
  transition: var(--transition);
}
.start-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(148, 132, 245, 0.5);
}
.start-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
}

/* Performance Analytics (Weak Areas Redesign) */
.analytics-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 22px;
  box-shadow: var(--shadow-card);
}
.analytics-header { margin-bottom: 16px; }
.analytics-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}
.analytics-sub { font-size: 0.82rem; color: var(--text-muted); margin-top: 4px; }
.analytics-overview {
  background: var(--card-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px;
  margin-bottom: 18px;
}
.ao-top {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
}
.ao-label { font-size: 0.85rem; font-weight: 700; color: var(--text-secondary); }
.ao-val { font-size: 1.45rem; font-weight: 900; color: var(--text-primary); }
.ao-track {
  height: 8px;
  border-radius: 4px;
  background: var(--surface-interactive);
  overflow: hidden;
  margin-bottom: 12px;
}
.ao-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--teal), var(--primary));
  transition: width 0.5s ease;
}
.ao-stats-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.ao-stats-row span strong { color: var(--text-primary); }

.spotlight-box {
  border-radius: var(--radius-lg);
  padding: 14px 16px;
  margin-bottom: 18px;
  border: 1px solid var(--border);
}
.spotlight-box.weak {
  background: var(--tint-orange);
  border-color: var(--tint-orange-border);
}
.spotlight-box.strong {
  background: var(--tint-green);
  border-color: var(--tint-green-border);
}
.spotlight-tag {
  font-size: 0.74rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}
.spotlight-box.weak .spotlight-tag { color: var(--warning); }
.spotlight-box.strong .spotlight-tag { color: var(--success); }
.spotlight-name {
  font-size: 1rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.spotlight-desc {
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.4;
  margin-bottom: 10px;
}
.spotlight-btn {
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  background: var(--warning);
  color: #1a1005;
  font-size: 0.82rem;
  font-weight: 700;
}
.spotlight-btn:hover { background: #f0b572; }

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 18px;
}
.breakdown-row { display: flex; flex-direction: column; gap: 5px; }
.br-head {
  display: flex;
  justify-content: space-between;
  font-size: 0.84rem;
  font-weight: 600;
}
.br-name {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-primary);
}
.br-score { color: var(--text-secondary); font-variant-numeric: tabular-nums; }
.br-badge {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 6px;
  margin-left: 6px;
}
.br-badge.strong { background: var(--tint-green); color: var(--success); }
.br-badge.average { background: rgba(81, 198, 193, 0.15); color: var(--teal); }
.br-badge.needs-imp { background: var(--tint-orange); color: var(--warning); }
.br-badge.critical { background: var(--tint-red); color: var(--error); }
.br-track {
  height: 6px;
  border-radius: 3px;
  background: var(--surface-interactive);
  overflow: hidden;
}
.br-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }

.reset-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid var(--border-subtle);
  font-size: 0.8rem;
  color: var(--text-muted);
}
.btn-reset {
  background: transparent;
  color: var(--error);
  font-size: 0.8rem;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(237, 112, 120, 0.3);
}
.btn-reset:hover { background: var(--tint-red); border-color: var(--error); }

/* CBT Exam Screen Styles (Ref 1) */
.cbt-container {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 24px;
  max-width: 1280px;
  margin: 0 auto;
  align-items: start;
}
.cbt-main { display: flex; flex-direction: column; }
.cbt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 14px;
}
.cbt-header-left {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.cbt-course-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text-primary);
}
.cbt-badge {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 12px;
  background: var(--card-primary);
  border: 1px solid var(--border);
  color: var(--text-secondary);
}
.cbt-badge.diff-easy { color: var(--success); border-color: var(--tint-green-border); }
.cbt-badge.diff-medium { color: var(--warning); border-color: var(--tint-orange-border); }
.cbt-badge.diff-hard { color: var(--error); border-color: var(--tint-red-border); }

.cbt-progress-wrap { margin-bottom: 20px; }
.cbt-progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.cbt-progress-track {
  height: 6px;
  border-radius: 3px;
  background: var(--surface-interactive);
  overflow: hidden;
}
.cbt-progress-fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--teal), var(--primary));
  transition: width 0.3s ease;
}

.cbt-q-card {
  background: var(--card-primary);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 30px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
}
.cbt-q-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 14px;
  letter-spacing: -0.01em;
}
.cbt-q-text {
  font-size: 1.12rem;
  line-height: 1.65;
  color: var(--text-primary);
  margin-bottom: 26px;
  font-weight: 450;
}

.cbt-opts {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 22px;
}
.opt {
  width: 100%;
  text-align: left;
  padding: 15px 18px;
  background: var(--card-elevated);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-lg);
  color: var(--text-primary);
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
  line-height: 1.45;
}
.opt:hover:not(.disabled) {
  border-color: var(--primary);
  background: var(--surface-interactive);
}
.opt-letter {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-weight: 800;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: var(--transition);
}
.opt-text { flex: 1; }
.opt-tag {
  font-size: 0.78rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 10px;
  margin-left: auto;
  white-space: nowrap;
}
.opt.selected {
  border-color: var(--primary);
  background: var(--tint-purple);
  box-shadow: 0 0 0 1px var(--primary);
}
.opt.selected .opt-letter {
  background: var(--primary);
  border-color: var(--primary);
  color: #FFFFFF;
}
.opt.correct {
  border-color: var(--success);
  background: var(--tint-green);
}
.opt.correct .opt-letter {
  background: var(--success);
  border-color: var(--success);
  color: #FFFFFF;
}
.opt-tag.correct { background: var(--success); color: #102014; }
.opt.wrong {
  border-color: var(--error);
  background: var(--tint-red);
}
.opt.wrong .opt-letter {
  background: var(--error);
  border-color: var(--error);
  color: #FFFFFF;
}
.opt-tag.wrong { background: var(--error); color: #FFFFFF; }
.opt.disabled { cursor: default; }

.feedback {
  display: none;
  padding: 18px 20px;
  border-radius: var(--radius-lg);
  margin-bottom: 20px;
  font-size: 0.94rem;
  line-height: 1.6;
  animation: fadeIn 0.2s ease;
}
@keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }
.feedback.show { display: block; }
.feedback-correct {
  background: var(--tint-green);
  border: 1px solid var(--tint-green-border);
}
.feedback-wrong {
  background: var(--tint-red);
  border: 1px solid var(--tint-red-border);
}
.feedback strong { display: block; margin-bottom: 6px; font-size: 1rem; }
.feedback-src {
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-style: italic;
}

.cbt-nav-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
}
.btn-cbt {
  padding: 13px 24px;
  font-weight: 700;
  font-size: 0.95rem;
  min-height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: 8px;
}
.btn-cbt.secondary {
  background: var(--card-primary);
  border: 1px solid var(--border);
  color: var(--text-primary);
}
.btn-cbt.secondary:hover {
  background: var(--surface-interactive);
  border-color: var(--border-focus);
}
.btn-cbt.primary {
  background: var(--primary);
  color: #FFFFFF;
  box-shadow: 0 4px 14px rgba(148, 132, 245, 0.35);
}
.btn-cbt.primary:hover { background: var(--primary-dark); }
.btn-cbt.flag {
  background: var(--card-primary);
  border: 1px solid var(--border);
  color: var(--warning);
}
.btn-cbt.flag:hover {
  background: var(--tint-orange);
  border-color: var(--warning);
}
.btn-cbt.flag.flagged {
  background: var(--tint-orange);
  border-color: var(--warning);
  color: var(--warning);
  font-weight: 800;
}

/* CBT Right Sidebar */
.cbt-sidebar {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.timer-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 22px;
  text-align: center;
  box-shadow: var(--shadow-card);
}
.cbt-timer-wrap {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: center;
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
  transition: stroke-dashoffset 1s linear, stroke 0.3s ease;
}
.timer-fg-ring.urgent { stroke: var(--warning); }
.timer-fg-ring.critical {
  stroke: var(--error);
  animation: pulse-ring 1s infinite alternate;
}
@keyframes pulse-ring {
  0% { stroke: var(--error); filter: drop-shadow(0 0 2px var(--error)); }
  100% { stroke: #ff9999; filter: drop-shadow(0 0 8px var(--error)); }
}
.cbt-timer-text {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.timer-digits {
  font-size: 1.3rem;
  font-weight: 900;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
  line-height: 1;
}
.timer-sub {
  font-size: 0.68rem;
  color: var(--text-muted);
  margin-top: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 700;
}
.score-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.84rem;
  font-weight: 700;
  background: var(--tint-green);
  color: var(--success);
  border: 1px solid var(--tint-green-border);
}

.navigator-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 22px;
  box-shadow: var(--shadow-card);
}
.nav-grid-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}
.nav-grid-title {
  font-size: 0.95rem;
  font-weight: 800;
  color: var(--text-primary);
}
.nav-grid-counter {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--primary);
  background: var(--tint-purple);
  padding: 2px 8px;
  border-radius: 10px;
}
.q-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-bottom: 16px;
  max-height: 280px;
  overflow-y: auto;
  padding-right: 4px;
}
.q-cell {
  aspect-ratio: 1;
  border-radius: 50%;
  font-size: 0.82rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface-interactive);
  color: var(--text-secondary);
  border: 2px solid transparent;
  cursor: pointer;
  transition: var(--transition);
}
.q-cell:hover {
  border-color: var(--primary);
  color: var(--text-primary);
}
.q-cell.current {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--tint-purple);
  box-shadow: 0 0 8px var(--primary-glow);
}
.q-cell.answered {
  background: var(--success);
  color: #0c1810;
  border-color: var(--success);
}
.q-cell.flagged {
  background: var(--warning);
  color: #1a1005;
  border-color: var(--warning);
}
.q-cell.answered.flagged {
  background: var(--warning);
  color: #1a1005;
  border: 2px solid var(--success);
}

.nav-summary-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}
.nav-chip {
  flex: 1;
  min-width: 80px;
  padding: 6px 8px;
  border-radius: var(--radius-sm);
  background: var(--card-elevated);
  font-size: 0.74rem;
  font-weight: 600;
  color: var(--text-secondary);
  text-align: center;
}
.nav-chip strong { color: var(--text-primary); }

.grid-legend {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
  font-size: 0.72rem;
  color: var(--text-muted);
  padding-top: 8px;
  border-top: 1px solid var(--border-subtle);
}
.leg { display: flex; align-items: center; gap: 4px; }
.leg-dot { width: 10px; height: 10px; border-radius: 50%; }
.leg-dot.answered { background: var(--success); }
.leg-dot.flagged { background: var(--warning); }
.leg-dot.current { background: transparent; border: 2px solid var(--primary); }
.leg-dot.unanswered { background: var(--surface-interactive); }

.sidebar-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.btn-finish-exam {
  width: 100%;
  padding: 14px;
  font-weight: 800;
  font-size: 0.98rem;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary), var(--aviation-blue));
  color: #FFFFFF;
  box-shadow: 0 4px 16px rgba(148, 132, 245, 0.35);
}
.btn-finish-exam:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(148, 132, 245, 0.45);
}
.btn-quit-exam {
  width: 100%;
  padding: 10px;
  font-weight: 600;
  font-size: 0.85rem;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-muted);
  border: 1px solid transparent;
}
.btn-quit-exam:hover {
  color: var(--error);
  border-color: rgba(237, 112, 120, 0.3);
  background: var(--tint-red);
}

/* Results Screen */
.result-hero {
  text-align: center;
  padding: 36px 20px 28px;
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  margin-bottom: 20px;
  box-shadow: var(--shadow-elevated);
}
.result-trophy { font-size: 2.8rem; margin-bottom: 10px; }
.result-points-label {
  font-size: 0.86rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin-bottom: 6px;
}
.result-grade {
  font-size: 3.8rem;
  font-weight: 900;
  line-height: 1;
  color: var(--primary);
  letter-spacing: -0.02em;
}
.result-pct {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 8px 0 12px;
}
.result-pass {
  display: inline-block;
  padding: 8px 24px;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 800;
  margin-top: 4px;
}
.result-pass.pass {
  background: var(--tint-green);
  color: var(--success);
  border: 1px solid var(--tint-green-border);
}
.result-pass.fail {
  background: var(--tint-red);
  color: var(--error);
  border: 1px solid var(--tint-red-border);
}
.result-stats {
  font-size: 0.88rem;
  color: var(--text-secondary);
  margin-top: 14px;
}

.breakdown-card {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 22px;
  margin-bottom: 18px;
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
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
}
.result-acts button {
  width: 100%;
  padding: 15px;
  font-size: 1rem;
  font-weight: 700;
  min-height: 52px;
  border-radius: var(--radius-lg);
}
.btn-review {
  background: var(--card-elevated);
  color: var(--text-primary);
  border: 1px solid var(--border);
}
.btn-review:hover {
  border-color: var(--primary);
  color: var(--primary);
}
.btn-retry-wrong {
  background: var(--tint-orange);
  color: var(--warning);
  border: 1px solid var(--tint-orange-border);
}
.btn-retry-wrong:hover {
  background: var(--warning);
  color: #1a1005;
}
.btn-retry-all {
  background: var(--primary);
  color: #FFFFFF;
}
.btn-retry-all:hover { background: var(--primary-dark); }
.btn-home {
  background: var(--card-primary);
  color: var(--text-secondary);
  border: 1px solid var(--border);
}
.btn-home:hover {
  color: var(--text-primary);
  border-color: var(--border-focus);
}

/* Review Screen */
.review-item {
  background: var(--card-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 14px;
  border-left: 4px solid var(--error);
  box-shadow: var(--shadow-card);
}
.review-qnum {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted);
  margin-bottom: 8px;
}
.review-q {
  font-size: 1.05rem;
  font-weight: 600;
  line-height: 1.5;
  color: var(--text-primary);
  margin-bottom: 14px;
}
.review-ans {
  font-size: 0.92rem;
  margin-bottom: 6px;
  line-height: 1.45;
}
.review-ans.your { color: var(--error); }
.review-ans.right { color: var(--success); font-weight: 700; }
.review-expl {
  font-size: 0.88rem;
  color: var(--text-secondary);
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--border-subtle);
  line-height: 1.55;
}
.review-src {
  font-size: 0.8rem;
  color: var(--text-muted);
  font-style: italic;
  margin-top: 6px;
}

/* Modal */
.modal-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(10, 10, 14, 0.75);
  z-index: 500;
  align-items: center;
  justify-content: center;
  padding: 20px;
  backdrop-filter: blur(8px);
}
.modal-overlay.show { display: flex; }
.modal-box {
  background: var(--card-primary);
  border-radius: var(--radius-xl);
  padding: 28px;
  max-width: 420px;
  width: 100%;
  box-shadow: var(--shadow-elevated);
  text-align: center;
  border: 1.5px solid var(--border);
}
.modal-icon { font-size: 2.2rem; margin-bottom: 10px; }
.modal-title { font-size: 1.25rem; font-weight: 800; color: var(--text-primary); margin-bottom: 8px; }
.modal-box p {
  margin-bottom: 22px;
  font-size: 0.95rem;
  line-height: 1.55;
  color: var(--text-secondary);
}
.modal-btns {
  display: flex;
  gap: 12px;
  justify-content: center;
}
.modal-btns button {
  padding: 12px 24px;
  font-weight: 700;
  min-height: 46px;
  min-width: 110px;
}
.btn-cancel {
  background: var(--card-elevated);
  color: var(--text-primary);
  border: 1px solid var(--border);
}
.btn-cancel:hover { border-color: var(--border-focus); }
.btn-modal-confirm {
  background: var(--primary);
  color: #FFFFFF;
}
.btn-modal-confirm:hover { background: var(--primary-dark); }

/* Responsive */
@media (max-width: 1080px) {
  .dashboard-split { grid-template-columns: 1fr; }
  .subject-grid { grid-template-columns: repeat(2, 1fr); }
  .subject-card.all-card { grid-column: span 2; }
  .summary-stats-row { grid-template-columns: repeat(2, 1fr); }
  .cbt-container { grid-template-columns: 1fr; }
}
@media (max-width: 720px) {
  .navbar { padding: 10px 16px; }
  .nav-links { display: none; }
  .container-wide { padding: 14px 14px 40px; }
  .quick-banners { grid-template-columns: 1fr; }
  .subject-grid { grid-template-columns: 1fr; }
  .subject-card.all-card { grid-column: span 1; }
  .mode-row { grid-template-columns: 1fr; }
  .filter-row { grid-template-columns: 1fr; }
  .cbt-q-card { padding: 20px; }
  .opt { padding: 13px 14px; font-size: 0.95rem; }
  .cbt-timer-wrap { width: 100px; height: 100px; }
  .timer-digits { font-size: 1.15rem; }
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-main); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--border-focus); }
</style>
</head>
<body>

<!-- Header -->
<header class="navbar">
  <div class="nav-brand" onclick="goHome()">
    <div class="brand-icon-wrap">✈️</div>
    <div class="brand-text">
      <h1>CPL PRACTICE</h1>
      <span>DGCA PILOT GROUND SCHOOL</span>
    </div>
  </div>

  <nav class="nav-links">
    <button class="nav-item active" onclick="goHome()"><span>📊</span> Dashboard</button>
    <button class="nav-item" onclick="scrollToPractice()"><span>📝</span> Practice</button>
    <button class="nav-item" onclick="scrollToAnalytics()"><span>📈</span> Analytics</button>
  </nav>

  <div class="nav-right">
    <div class="nav-pill gold" id="headerScorePill">⭐ 0 Points</div>
    <div class="nav-pilot-avatar" title="Commercial Pilot">👨‍✈️</div>
    <button class="theme-btn" id="darkBtn" title="Toggle theme" aria-label="Toggle theme">🌙</button>
  </div>
</header>

<div class="container-wide">

<!-- HOME / DASHBOARD SCREEN -->
<div id="homeScreen" class="screen active">

  <div class="welcome-section">
    <div class="welcome-header">
      <h2 class="welcome-title">Welcome back, Pilot!</h2>
      <p class="welcome-sub">Continue your journey towards your Commercial Pilot Licence (India DGCA).</p>
    </div>

    <!-- Quick Action Banners -->
    <div class="quick-banners">
      <div class="banner-card resume" id="quickResumeBanner">
        <div>
          <div class="banner-tag">Continue where you left off ✨</div>
          <div class="banner-title" id="quickResumeTitle">Air Navigation</div>
          <div class="banner-desc" id="quickResumeDesc">Practice mode with instant right/wrong feedback</div>
        </div>
        <div class="banner-main" style="margin-top:14px">
          <span style="font-size:0.8rem;color:var(--text-secondary)">50 Questions available</span>
          <button class="banner-btn" id="quickResumeBtn">Start Practice »</button>
        </div>
      </div>

      <div class="banner-card mock" id="quickMockBanner">
        <div>
          <div class="banner-tag">DGCA CBT Mock Examination 📋</div>
          <div class="banner-title">Official Exam Paper</div>
          <div class="banner-desc">Full computer-based test simulation · 70% Passing Standard</div>
        </div>
        <div class="banner-main" style="margin-top:14px">
          <span style="font-size:0.8rem;color:var(--text-secondary)">Strict timing · No answers revealed</span>
          <button class="banner-btn" id="quickMockBtn">Launch Mock Exam »</button>
        </div>
      </div>
    </div>

    <!-- 4 Summary Stats -->
    <div class="summary-stats-row">
      <div class="stat-box">
        <div class="stat-box-title">Questions Attempted</div>
        <div class="stat-box-val" id="summaryAttempted">0</div>
        <div class="stat-box-sub">Across all subjects</div>
      </div>
      <div class="stat-box">
        <div class="stat-box-title">Overall Accuracy</div>
        <div class="stat-box-val" id="summaryAccuracy">0%</div>
        <div class="stat-box-sub">Points accuracy rate</div>
      </div>
      <div class="stat-box">
        <div class="stat-box-title">Points Received</div>
        <div class="stat-box-val" id="summaryPoints">0 / 0</div>
        <div class="stat-box-sub">1 mark per correct answer</div>
      </div>
      <div class="stat-box">
        <div class="stat-box-title">DGCA Exam Status</div>
        <div class="stat-box-val" id="summaryReadiness" style="font-size:1.2rem;line-height:1.4">✈️ In Training</div>
        <div class="stat-box-sub">Pass Mark: 70% in each paper</div>
      </div>
    </div>
  </div>

  <div class="dashboard-split">
    
    <!-- Left Column: Image-Led Subject Cards & Mode Selector -->
    <div class="dashboard-left" id="practiceAnchor">
      <div class="section-head">
        <h3 class="section-title">Select Examination Subject</h3>
        <span class="section-sub">Choose one or multiple subjects</span>
      </div>

      <!-- 3-Column Subject Cards Grid -->
      <div class="subject-grid" id="subjGrid"></div>

      <!-- Quiz Configuration Card -->
      <div class="config-card">
        <div class="section-head" style="margin-bottom:12px">
          <h4 class="section-title" style="font-size:1.05rem">Quiz Mode & Parameters</h4>
        </div>
        <div class="mode-row">
          <button class="mode-btn selected" data-mode="practice">
            📝 Practice Mode
            <span>Instant feedback, points & sources</span>
          </button>
          <button class="mode-btn" data-mode="timed">
            ⏱ Timed Paper
            <span>User countdown timer</span>
          </button>
          <button class="mode-btn" data-mode="mock">
            📋 Mock Examination
            <span>Official DGCA CBT scheme (70% pass)</span>
          </button>
        </div>

        <div class="filter-row">
          <div>
            <select class="topic-select" id="topicSel">
              <option value="">All topics</option>
            </select>
          </div>
          <div class="timer-input-wrap" id="timerRow">
            <label for="timerMin">Timer (min):</label>
            <input type="number" id="timerMin" value="30" min="5" max="180">
          </div>
        </div>

        <button class="start-btn" id="startBtn" disabled>
          <span>🚀</span><span id="startLabel">Start Quiz</span>
        </button>
      </div>
    </div>

    <!-- Right Column: Performance Analytics -->
    <div class="dashboard-right" id="analyticsAnchor">
      <div class="analytics-card" id="weakCard">
        <div class="analytics-header">
          <div class="analytics-title"><span>📊</span> Performance Analytics</div>
          <div class="analytics-sub">Understand your strengths and areas needing focus.</div>
        </div>

        <div class="analytics-overview">
          <div class="ao-top">
            <span class="ao-label">Overall Accuracy</span>
            <span class="ao-val" id="aoAccuracy">0%</span>
          </div>
          <div class="ao-track"><div class="ao-fill" id="aoFill" style="width:0%"></div></div>
          <div class="ao-stats-row">
            <span>Attempted: <strong id="aoAttempted">0</strong></span>
            <span>Points: <strong id="aoPoints">0</strong></span>
            <span>Target: <strong>70%</strong></span>
          </div>
        </div>

        <div id="weakPanel"></div>

        <div class="reset-row">
          <span id="statsLine">No attempts recorded yet.</span>
          <button class="btn-reset" id="resetBtn">Reset History</button>
        </div>
      </div>
    </div>

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
        <div class="cbt-header-right">
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
        <button class="btn-cbt secondary" id="prevBtn">◀ Previous</button>
        <button class="btn-cbt flag" id="flagBtn">🚩 Flag Question</button>
        <button class="btn-cbt primary" id="nextBtn">Next ▶</button>
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
            <span class="timer-sub">Time Remaining</span>
          </div>
        </div>
        <span id="qTimer" style="display:none">⏱ 30:00</span>
        <div class="score-badge" id="qScoreBadge">🎯 Points: 0 / 0</div>
      </div>

      <!-- Navigator Grid -->
      <div class="navigator-card">
        <div class="nav-grid-head">
          <span class="nav-grid-title">Question Navigator</span>
          <span class="nav-grid-counter" id="cbtNavCount">0 / 50</span>
        </div>

        <div class="q-grid" id="qGrid"></div>

        <div class="nav-summary-chips">
          <div class="nav-chip"><strong id="cbtStatAnswered">0</strong> Answered</div>
          <div class="nav-chip"><strong id="cbtStatRemaining">50</strong> Left</div>
          <div class="nav-chip"><strong id="cbtStatFlagged">0</strong> Flagged</div>
        </div>

        <div class="grid-legend" id="gridLegend">
          <span class="leg"><span class="leg-dot answered"></span>Answered</span>
          <span class="leg"><span class="leg-dot flagged"></span>Flagged</span>
          <span class="leg"><span class="leg-dot current"></span>Current</span>
          <span class="leg"><span class="leg-dot unanswered"></span>Unanswered</span>
        </div>

        <div class="grid-toggle" id="gridToggle" style="display:none">Toggle Navigator</div>
      </div>

      <div class="sidebar-actions">
        <button class="btn-finish-exam" id="finishBtn">🚀 Submit Examination</button>
        <button class="btn-quit-exam" id="quitBtn">✖ Quit Examination</button>
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
      <div class="card-header-line"><span>📌</span> Points per Topic</div>
      <div id="rTopicBreakdown"></div>
    </div>

    <div class="card-header-line" style="font-size:0.88rem;color:var(--text-secondary);font-weight:400" id="rPassInfo"></div>

    <div class="result-acts">
      <button class="btn-review" id="reviewBtn">🔍 Review Mistakes</button>
      <button class="btn-retry-wrong" id="retryWrongBtn">🔄 Retry Wrong Questions</button>
      <button class="btn-retry-all" id="retryAllBtn">🔁 Retry Same Set</button>
      <button class="btn-home" id="homeFromResult">🏠 Back to Dashboard</button>
    </div>

  </div>
</div><!-- /resultScreen -->

<!-- REVIEW SCREEN -->
<div id="reviewScreen" class="screen">
  <div style="max-width:840px;margin:0 auto">
    <div class="card-header-line" style="margin-bottom:16px"><span style="font-size:1.3rem">🔍</span> Review Mistakes & Explanations</div>
    <div id="reviewList"></div>
    <button class="btn-cbt secondary" id="backFromReview" style="width:100%;margin-top:14px;justify-content:center">◀ Back to Results</button>
  </div>
</div>

</div><!-- /container-wide -->

<!-- MODAL -->
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
  "Technical Specific":   { icon: "✈️", code: "POH / PERF", color: "#ECA85B" },
  "RTR":                  { icon: "📻", code: "ICAO DOC 9432", color: "#51C6C1" },
};
const ALL_SUBJECTS = Object.keys(SUBJECT_META);

''' + svg_func_js + '''

function sg(k,f){try{const v=localStorage.getItem(k);return v!==null?JSON.parse(v):f}catch{return f}}
function ss(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch{}}
function sd(k){try{localStorage.removeItem(k)}catch{}}

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
  gridOpen: false,
  finished: false,
};

let history = sg("cpl_history", {});
let darkMode = sg("cpl_dark", true);

function applyDark(){
  document.body.classList.toggle("light", !darkMode);
  document.getElementById("darkBtn").textContent = darkMode ? "☀️" : "🌙";
}
applyDark();
document.getElementById("darkBtn").addEventListener("click", () => {
  darkMode = !darkMode;
  ss("cpl_dark", darkMode);
  applyDark();
});

function goHome(){
  if(document.getElementById("quizScreen").classList.contains("active") && !state.finished){
    showModal("Quit this examination? Unsaved progress will be lost.", ()=>{
      if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval=null; }
      renderWeakness(); renderStats(); showScreen("homeScreen");
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

function buildSubjectChips(){
  const grid = document.getElementById("subjGrid");
  if(!grid) return;
  grid.innerHTML = "";

  const isAll = state.selSubjects.length === 0;

  const allCard = document.createElement("div");
  allCard.className = "subject-card all-card" + (isAll ? " selected" : "");
  allCard.innerHTML = `
    <div class="card-media">
      ${getSubjectSvg("All")}
      <div class="card-media-overlay"></div>
      <div class="card-media-meta">
        <span class="card-tag">Full DGCA Syllabus</span>
        <span class="card-arrow">»</span>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title-row">
        <div class="card-title">📚 All DGCA Subjects Combined</div>
        <div class="card-check">✓</div>
      </div>
      <div class="card-info-row">
        <span>6 Subjects · 230 Questions</span>
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
    const qCount = QUESTIONS.filter(q => q.subject === subj).length;
    if(qCount === 0) return;
    const meta = SUBJECT_META[subj] || { icon: "📖", code: "DGCA", color: "#9484F5" };
    const h = history[subj] || { attempted: 0, correct: 0 };
    const pct = h.attempted > 0 ? Math.round(100 * h.correct / h.attempted) : 0;
    const isSelected = state.selSubjects.includes(subj);
    const topicCount = new Set(QUESTIONS.filter(q => q.subject === subj).map(q => q.topic)).size;

    const card = document.createElement("div");
    card.className = "subject-card" + (isSelected ? " selected" : "");
    card.innerHTML = `
      <div class="card-media">
        ${getSubjectSvg(subj)}
        <div class="card-media-overlay"></div>
        <div class="card-media-meta">
          <span class="card-tag">${topicCount} Topics</span>
          <span class="card-arrow">»</span>
        </div>
      </div>
      <div class="card-body">
        <div class="card-title-row">
          <div class="card-title">${meta.icon} ${subj}</div>
          <div class="card-check">✓</div>
        </div>
        <div class="card-info-row">
          <span>${qCount} Questions</span>
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

function buildTopicDropdown(){
  const sel = document.getElementById("topicSel");
  if(!sel) return;
  const current = sel.value;
  const subs = state.selSubjects.length > 0 ? state.selSubjects : ALL_SUBJECTS;
  const topics = [...new Set(QUESTIONS.filter(q => subs.includes(q.subject)).map(q => q.topic))].sort();
  sel.innerHTML = `<option value="">All Topics (${topics.length} available)</option>`;
  topics.forEach(t => {
    const opt = document.createElement("option");
    opt.value = t; opt.textContent = t;
    if(t === current) opt.selected = true;
    sel.appendChild(opt);
  });
  state.topicFilter = sel.value;
}

document.getElementById("topicSel").addEventListener("change", e => {
  state.topicFilter = e.target.value;
  updateStartBtn();
});

document.querySelectorAll(".mode-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".mode-btn").forEach(b => b.classList.remove("selected"));
    btn.classList.add("selected");
    state.mode = btn.dataset.mode;
    document.getElementById("timerRow").classList.toggle("show", state.mode === "timed");
    updateStartBtn();
  });
});

function getFilteredPool(){
  const subs = state.selSubjects.length > 0 ? state.selSubjects : ALL_SUBJECTS;
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
  btn.disabled = n === 0;
  if(n === 0){
    label.textContent = "No questions for this selection";
  } else {
    label.textContent = `Start ${state.mode === "mock" ? "Mock Exam" : state.mode === "timed" ? "Timed Exam" : "Practice"} (${n} questions)`;
  }
}

function updateHome(){
  buildTopicDropdown();
  updateStartBtn();
  renderWeakness();
  renderStats();
}

document.getElementById("quickResumeBtn").addEventListener("click", () => {
  state.mode = "practice";
  document.querySelectorAll(".mode-btn").forEach(b => b.classList.toggle("selected", b.dataset.mode === "practice"));
  let targetSubj = "Air Navigation";
  let minPct = 101;
  ALL_SUBJECTS.forEach(s => {
    const h = history[s];
    if(h && h.attempted > 0){
      const p = Math.round(100 * h.correct / h.attempted);
      if(p < minPct){ minPct = p; targetSubj = s; }
    }
  });
  state.selSubjects = [targetSubj];
  buildSubjectChips();
  const pool = getFilteredPool();
  startQuiz(pool);
});

document.getElementById("quickMockBtn").addEventListener("click", () => {
  state.mode = "mock";
  document.querySelectorAll(".mode-btn").forEach(b => b.classList.toggle("selected", b.dataset.mode === "mock"));
  document.getElementById("startBtn").click();
});

document.getElementById("startBtn").addEventListener("click", () => {
  const pool = getFilteredPool();
  if(pool.length === 0) return;
  state.timerMin = parseInt(document.getElementById("timerMin").value) || 30;

  if(state.mode === "mock"){
    const subs = state.selSubjects.length > 0 ? state.selSubjects : ALL_SUBJECTS;
    let mockPool = [];
    subs.forEach(subj => {
      const cfg = EXAM_CONFIG.subjects[subj];
      const available = pool.filter(q => q.subject === subj);
      if(available.length === 0) return;
      const count = Math.min(cfg ? cfg.questions : 50, available.length);
      mockPool = mockPool.concat(shuffle(available).slice(0, count));
    });
    if(mockPool.length === 0){ alert("No questions available."); return; }
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
  const aoFill = document.getElementById("aoFill");
  const aoAttempted = document.getElementById("aoAttempted");
  const aoPoints = document.getElementById("aoPoints");

  if(aoAccuracy) aoAccuracy.textContent = `${overallPct}%`;
  if(aoFill) aoFill.style.width = `${overallPct}%`;
  if(aoAttempted) aoAttempted.textContent = totalAtt;
  if(aoPoints) aoPoints.textContent = totalCorr;

  const hScore = document.getElementById("headerScorePill");
  if(hScore) hScore.textContent = `⭐ ${totalCorr} Points`;

  const sAtt = document.getElementById("summaryAttempted");
  const sAcc = document.getElementById("summaryAccuracy");
  const sPts = document.getElementById("summaryPoints");
  const sRead = document.getElementById("summaryReadiness");

  if(sAtt) sAtt.textContent = totalAtt;
  if(sAcc) sAcc.textContent = `${overallPct}%`;
  if(sPts) sPts.textContent = `${totalCorr} / ${totalAtt}`;
  if(sRead) {
    if(totalAtt === 0) sRead.textContent = "✈️ Ready to Begin";
    else if(overallPct >= 70) sRead.innerHTML = `<span style="color:var(--success)">✅ Exam Ready</span>`;
    else sRead.innerHTML = `<span style="color:var(--warning)">⏳ In Training</span>`;
  }

  if(entries.length === 0){
    panel.innerHTML = `
      <div style="padding:24px 16px;text-align:center;color:var(--text-muted);font-size:0.86rem">
        <div style="font-size:2rem;margin-bottom:8px">✈️</div>
        No examination attempts recorded yet.<br>Complete practice quizzes to generate performance analytics!
      </div>
    `;
    return;
  }

  entries.sort((a,b) => a.pct - b.pct);
  const weakest = entries[0];
  const strongest = entries[entries.length - 1];

  let html = "";
  if(weakest && weakest.pct < 70){
    html += `
      <div class="spotlight-box weak">
        <div class="spotlight-tag">⚠️ Focus Area — Action Needed</div>
        <div class="spotlight-name">${SUBJECT_META[weakest.subj]?.icon||""} ${weakest.subj} (${weakest.pct}% Accuracy)</div>
        <div class="spotlight-desc">Currently below the 70% DGCA passing requirement. Practice 15 targeted questions to boost mastery.</div>
        <button class="spotlight-btn" onclick="practiceTargetSubject('${weakest.subj}')">Practice This Subject »</button>
      </div>
    `;
  } else if(strongest) {
    html += `
      <div class="spotlight-box strong">
        <div class="spotlight-tag">🏆 Strongest Subject</div>
        <div class="spotlight-name">${SUBJECT_META[strongest.subj]?.icon||""} ${strongest.subj} (${strongest.pct}% Accuracy)</div>
        <div class="spotlight-desc">Exceeds the 70% DGCA threshold! Keep maintaining proficiency with occasional timed papers.</div>
      </div>
    `;
  }

  html += '<div class="breakdown-list">';
  entries.forEach(e => {
    let badgeClass = "strong";
    let badgeText = "Strong";
    let barColor = "var(--success)";
    if(e.pct < 35){ badgeClass = "critical"; badgeText = "Critical"; barColor = "var(--error)"; }
    else if(e.pct < 55){ badgeClass = "needs-imp"; badgeText = "Needs Focus"; barColor = "var(--warning)"; }
    else if(e.pct < 70){ badgeClass = "average"; badgeText = "Developing"; barColor = "var(--teal)"; }

    html += `
      <div class="breakdown-row">
        <div class="br-head">
          <span class="br-name">${SUBJECT_META[e.subj]?.icon||""} ${e.subj} <span class="br-badge ${badgeClass}">${badgeText}</span></span>
          <span class="br-score">${e.correct}/${e.attempted} pts (${e.pct}%)</span>
        </div>
        <div class="br-track"><div class="br-fill" style="width:${e.pct}%;background:${barColor}"></div></div>
      </div>
    `;
  });
  html += '</div>';

  panel.innerHTML = html;
}

window.practiceTargetSubject = function(subj){
  state.mode = "practice";
  state.selSubjects = [subj];
  buildSubjectChips();
  const pool = getFilteredPool();
  startQuiz(pool);
};

function renderStats(){
  let ta=0, tc=0;
  Object.values(history).forEach(h => { ta += h.attempted; tc += h.correct; });
  const el = document.getElementById("statsLine");
  if(el){
    if(ta === 0) el.textContent = "No attempts recorded yet.";
    else el.textContent = `${ta} questions attempted · Total Points: ${tc}/${ta} (${Math.round(100*tc/ta)}%)`;
  }
}

document.getElementById("resetBtn").addEventListener("click", () => {
  showModal("Reset all recorded progress, attempts, and points history? This cannot be undone.", () => {
    history = {};
    sd("cpl_history");
    renderWeakness();
    renderStats();
    buildSubjectChips();
  });
});

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
  document.getElementById("qGrid").innerHTML = "";
  buildGrid();
  renderQuestion();
}

function renderTimer(){
  const digitsEl = document.getElementById("qTimerDigits");
  const hiddenTimer = document.getElementById("qTimer");
  const ring = document.getElementById("timerRing");
  const totalCircumference = 276.46;

  if(state.mode === "timed" || state.mode === "mock"){
    const m = Math.floor(state.timerSec / 60);
    const s = state.timerSec % 60;
    const timeStr = `${String(m).padStart(2,"0")}:${String(s).padStart(2,"0")}`;
    if(digitsEl) digitsEl.textContent = timeStr;
    if(hiddenTimer) hiddenTimer.textContent = `⏱ ${timeStr}`;

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
    if(hiddenTimer) hiddenTimer.textContent = `⏱ ${timeStr}`;
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
      sb.textContent = `🎯 Points: 0 / ${total} (0%)`;
    } else {
      const pct = Math.round(100 * correct / attempted);
      sb.textContent = `🎯 Points: ${correct} / ${attempted} (${pct}%) · Total: ${total} Qs`;
    }
  } else {
    const answeredCount = state.answers.filter(a => a >= 0).length;
    sb.textContent = `📝 Answered: ${answeredCount} / ${state.questions.length}`;
  }
}

const LETTERS = ["A","B","C","D","E","F","G","H"];

function renderQuestion(){
  const q = state.questions[state.idx];
  const i = state.idx;
  const n = state.questions.length;
  const meta = SUBJECT_META[q.subject] || { icon: "📖", color: "#9484F5" };

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

    if(state.mode === "practice" && revealed){
      if(oi === q.answer){
        btn.classList.add("correct");
        tagHtml = `<span class="opt-tag correct">✓ Correct (+1 pt)</span>`;
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
    fb.innerHTML = `<strong>${correct ? "✅ Correct! (+1 Point Received)" : "❌ Incorrect (0 Points) — The correct answer is " + LETTERS[q.answer] + ": " + q.options[q.answer]}</strong>${q.explanation}<div class="feedback-src">📖 Source: ${q.source}</div>`;
  }

  const fl = document.getElementById("flagBtn");
  fl.classList.toggle("flagged", state.flags[i]);
  fl.textContent = state.flags[i] ? "🚩 Flagged" : "🚩 Flag Question";

  document.getElementById("prevBtn").disabled = i === 0;
  document.getElementById("nextBtn").textContent = i === n - 1 ? "Review / Submit ▶" : "Next ▶";

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
  if(cbtStatAnswered) cbtStatAnswered.textContent = `${ansCount} Answered`;
  if(cbtStatRemaining) cbtStatRemaining.textContent = `${remCount} Left`;
  if(cbtStatFlagged) cbtStatFlagged.textContent = `${flagCount} Flagged`;
}

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
    renderWeakness(); renderStats();
    showScreen("homeScreen");
  }, "Quit Examination");
});

function finishQuiz(){
  if(state.timerInterval){ clearInterval(state.timerInterval); state.timerInterval = null; }
  state.endTime = Date.now();
  state.finished = true;

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
  pb.innerHTML = `<span class="result-pass ${pass ? "pass" : "fail"}">${pass ? `✅ PASS — Scored ${points} pts (≥ 70% DGCA Requirement)` : `❌ FAIL — Scored ${points} pts (${minNeeded} points needed to pass)`}</span>`;

  document.getElementById("rStats").textContent =
    `⏱ Time Taken: ${em}m ${es}s · Answered: ${answered} of ${n} · Pass Criterion: ${EXAM_CONFIG.passMark}% (${minNeeded} pts required)`;

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

  document.getElementById("rPassInfo").innerHTML =
    `ℹ️ <strong>DGCA Exam Rules:</strong> Passing mark is <strong>70%</strong> in each paper independently. There is <strong>no negative marking</strong> (unattempted questions earn 0 marks). Results are valid for 5 years.`;

  const missedCount = state.questions.filter((q,i) => state.answers[i] !== q.answer).length;
  document.getElementById("retryWrongBtn").style.display = missedCount > 0 ? "" : "none";
  document.getElementById("retryWrongBtn").textContent = `🔄 Retry ${missedCount} Missed Question${missedCount !== 1 ? "s" : ""}`;
  document.getElementById("reviewBtn").style.display = missedCount > 0 ? "" : "none";
  document.getElementById("reviewBtn").textContent = `🔍 Review ${missedCount} Mistake${missedCount !== 1 ? "s" : ""}`;
}

document.getElementById("reviewBtn").addEventListener("click", () => {
  showScreen("reviewScreen");
  const list = document.getElementById("reviewList");
  list.innerHTML = "";
  state.questions.forEach((q, i) => {
    if(state.answers[i] === q.answer) return;
    const userChoice = state.answers[i];
    const correctChoice = q.answer;
    const div = document.createElement("div");
    div.className = "review-item";
    const yourAnsText = userChoice >= 0 ?
      `❌ Your Choice: <strong>${LETTERS[userChoice]}. ${q.options[userChoice]}</strong> (0 points received)` :
      `⚠️ Your Choice: <strong>Unanswered / Skipped</strong> (0 points received)`;
    div.innerHTML = `
      <div class="review-qnum">Question ${i + 1} of ${state.questions.length} · ${q.subject} · ${q.topic || ""}</div>
      <div class="review-q">${q.question}</div>
      <div class="review-ans your">${yourAnsText}</div>
      <div class="review-ans right">✅ Correct Answer: <strong>${LETTERS[correctChoice]}. ${q.options[correctChoice]}</strong> (+1 point)</div>
      <div class="review-expl"><strong>Explanation:</strong> ${q.explanation}</div>
      <div class="review-src">📖 Reference: ${q.source}</div>`;
    list.appendChild(div);
  });
  if(!list.children.length){
    list.innerHTML = '<div style="text-align:center;padding:40px"><div style="font-size:2.5rem">🎉</div><div style="color:var(--text-secondary);margin-top:10px">Perfect score! 100% points received — no mistakes to review.</div></div>';
  }
});
document.getElementById("backFromReview").addEventListener("click", () => showScreen("resultScreen"));

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
  startQuiz(wrongPool, true);
});

document.getElementById("homeFromResult").addEventListener("click", () => {
  renderWeakness(); renderStats(); showScreen("homeScreen");
});

let modalCb = null;
function showModal(msg, onConfirm, title="Confirm Action"){
  const mTitle = document.getElementById("modalTitle");
  if(mTitle) mTitle.textContent = title;
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

buildSubjectChips();
updateHome();

</script>
</body>
</html>
'''

# Write to target files
for filename in ["index.html", "cpl-exam-direct.html", "cpl-quiz-standalone.html"]:
    target_path = os.path.join(BASE, filename)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(html_part1)
    print(f"Generated {target_path} ({len(html_part1)} bytes)")

print("ALL HTML GENERATIONS COMPLETE!")
