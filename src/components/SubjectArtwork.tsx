import React from "react";

interface SubjectArtworkProps {
  subject: string;
  className?: string;
}

export default function SubjectArtwork({ subject, className = "w-full h-32" }: SubjectArtworkProps) {
  if (subject === "Air Navigation") {
    return (
      <svg
        viewBox="0 0 400 180"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMidYMid slice"
        className={className}
      >
        <defs>
          <linearGradient id="navGradLuxe" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#141E2C" />
            <stop offset="50%" stopColor="#1B283D" />
            <stop offset="100%" stopColor="#101824" />
          </linearGradient>
        </defs>
        <rect width="400" height="180" fill="url(#navGradLuxe)" />
        {/* Nav Chart Graticule */}
        <path d="M0 30 Q200 50 400 30 M0 75 Q200 95 400 75 M0 120 Q200 140 400 120 M0 160 Q200 180 400 160" stroke="#48A9FF" strokeWidth="0.8" strokeOpacity="0.25" fill="none" />
        <path d="M70 0 Q90 90 70 180 M150 0 Q170 90 150 180 M230 0 Q250 90 230 180 M310 0 Q330 90 310 180" stroke="#48A9FF" strokeWidth="0.8" strokeOpacity="0.25" fill="none" />
        {/* Compass Rose */}
        <g transform="translate(300, 90)">
          <circle r="55" stroke="#48A9FF" strokeWidth="1.2" strokeOpacity="0.35" fill="none" />
          <circle r="42" stroke="#A58BFA" strokeWidth="0.8" strokeOpacity="0.4" strokeDasharray="3 3" fill="none" />
          <polygon points="0,-40 6,-8 0,0 -6,-8" fill="#F2B94B" />
          <polygon points="0,40 6,8 0,0 -6,8" fill="#48A9FF" opacity="0.45" />
          <polygon points="40,0 8,6 0,0 8,-6" fill="#48A9FF" opacity="0.45" />
          <polygon points="-40,0 -8,6 0,0 -8,-6" fill="#48A9FF" opacity="0.45" />
          <circle r="3" fill="#F2B94B" />
          <text x="0" y="-44" fill="#F2B94B" fontSize="10" fontWeight="900" textAnchor="middle">N</text>
        </g>
        {/* Flight Track & Waypoints */}
        <path d="M35 140 L120 95 L210 115 L310 55" stroke="#3ED1B0" strokeWidth="2.2" strokeDasharray="6 4" fill="none" opacity="0.9" />
        <circle cx="35" cy="140" r="4.5" fill="#3ED1B0" stroke="#101116" strokeWidth="2" />
        <circle cx="120" cy="95" r="4.5" fill="#48A9FF" stroke="#101116" strokeWidth="2" />
        <circle cx="210" cy="115" r="4.5" fill="#3ED1B0" stroke="#101116" strokeWidth="2" />
        <circle cx="310" cy="55" r="5" fill="#F2B94B" stroke="#101116" strokeWidth="2" />
        {/* Aircraft heading */}
        <g transform="translate(120, 95) rotate(-35)">
          <path d="M0 -12 L3 -2 L10 2 L3 3 L2 9 L5 11 L0 10 L-5 11 L-2 9 L-3 3 L-10 2 L-3 -2 Z" fill="#F5F6FA" opacity="0.95" />
        </g>
      </svg>
    );
  }

  if (subject === "Air Regulations") {
    return (
      <svg
        viewBox="0 0 400 180"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMidYMid slice"
        className={className}
      >
        <defs>
          <linearGradient id="regGradLuxe" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#25172E" />
            <stop offset="50%" stopColor="#321D3F" />
            <stop offset="100%" stopColor="#180F1E" />
          </linearGradient>
        </defs>
        <rect width="400" height="180" fill="url(#regGradLuxe)" />
        {/* Runway 27L Perspective */}
        <polygon points="140,180 260,180 215,50 185,50" fill="#242A35" stroke="#394452" strokeWidth="1" />
        <line x1="200" y1="170" x2="200" y2="145" stroke="#F5F6FA" strokeWidth="3" />
        <line x1="200" y1="130" x2="200" y2="110" stroke="#F5F6FA" strokeWidth="2.5" />
        <line x1="200" y1="95" x2="200" y2="80" stroke="#F5F6FA" strokeWidth="2" />
        <line x1="200" y1="70" x2="200" y2="60" stroke="#F5F6FA" strokeWidth="1.5" />
        <g fill="#F5F6FA" opacity="0.85">
          <rect x="155" y="155" width="5" height="16" />
          <rect x="165" y="155" width="5" height="16" />
          <rect x="175" y="155" width="5" height="16" />
          <rect x="220" y="155" width="5" height="16" />
          <rect x="230" y="155" width="5" height="16" />
          <rect x="240" y="155" width="5" height="16" />
        </g>
        <text x="200" y="146" fill="#F2B94B" fontSize="12" fontWeight="900" textAnchor="middle">27L</text>
        <circle cx="150" cy="175" r="3" fill="#3ED1B0" />
        <circle cx="162" cy="175" r="3" fill="#3ED1B0" />
        <circle cx="238" cy="175" r="3" fill="#3ED1B0" />
        <circle cx="250" cy="175" r="3" fill="#3ED1B0" />
        {/* Control Tower silhouette */}
        <g transform="translate(325, 35)">
          <rect x="6" y="18" width="12" height="45" fill="#2C3441" stroke="#394452" strokeWidth="1" />
          <polygon points="2,18 22,18 18,6 6,6" fill="#343E4B" stroke="#A58BFA" strokeWidth="1" />
          <circle cx="12" cy="4" r="3" fill="#A58BFA" />
          <polygon points="12,4 -75,-20 -85,20" fill="#A58BFA" opacity="0.12" />
        </g>
      </svg>
    );
  }

  if (subject === "Aviation Meteorology") {
    return (
      <svg
        viewBox="0 0 400 180"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMidYMid slice"
        className={className}
      >
        <defs>
          <linearGradient id="metGradLuxe" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#122533" />
            <stop offset="50%" stopColor="#193345" />
            <stop offset="100%" stopColor="#0E1B24" />
          </linearGradient>
        </defs>
        <rect width="400" height="180" fill="url(#metGradLuxe)" />
        {/* Isobar Curves */}
        <path d="M-20 45 Q120 15 240 55 T420 35" stroke="#3ED1B0" strokeWidth="1" strokeOpacity="0.3" fill="none" />
        <path d="M-20 85 Q140 50 260 95 T420 75" stroke="#3ED1B0" strokeWidth="1.2" strokeOpacity="0.4" fill="none" />
        <path d="M-20 125 Q160 90 280 135 T420 115" stroke="#3ED1B0" strokeWidth="1" strokeOpacity="0.3" fill="none" />
        {/* High Pressure Datum */}
        <g transform="translate(80, 55)">
          <circle r="15" fill="#48A9FF" opacity="0.18" />
          <text x="0" y="5" fill="#48A9FF" fontSize="13" fontWeight="900" textAnchor="middle">H</text>
          <text x="0" y="18" fill="#B8C3D2" fontSize="7" textAnchor="middle">1024</text>
        </g>
        {/* Low Pressure Datum */}
        <g transform="translate(325, 120)">
          <circle r="15" fill="#F16D75" opacity="0.18" />
          <text x="0" y="5" fill="#F16D75" fontSize="13" fontWeight="900" textAnchor="middle">L</text>
          <text x="0" y="18" fill="#B8C3D2" fontSize="7" textAnchor="middle">996</text>
        </g>
        {/* Cumulonimbus Anvil Cloud with Lightning */}
        <g transform="translate(200, 60)" opacity="0.95">
          <path d="M-55 30 Q-70 15 -48 3 Q-44 -18 -18 -18 Q-10 -35 15 -35 Q38 -35 45 -18 Q70 -14 65 7 Q75 22 60 30 Z" fill="#2C3441" stroke="#3ED1B0" strokeWidth="1.2" />
          <path d="M-22 -18 L-50 -35 L60 -35 L28 -18 Z" fill="#343E4B" stroke="#3ED1B0" strokeWidth="1" opacity="0.95" />
          <polygon points="6,32 -5,48 3,49 -8,66 10,42 1,41" fill="#F2B94B" />
        </g>
      </svg>
    );
  }

  if (subject === "Technical General") {
    return (
      <svg
        viewBox="0 0 400 180"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMidYMid slice"
        className={className}
      >
        <defs>
          <linearGradient id="genGradLuxe" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#142820" />
            <stop offset="50%" stopColor="#1C382D" />
            <stop offset="100%" stopColor="#0E1E18" />
          </linearGradient>
        </defs>
        <rect width="400" height="180" fill="url(#genGradLuxe)" />
        {/* Turbojet Engine cross-section */}
        <g transform="translate(180, 90)">
          <path d="M-100 -50 C-35 -55 35 -50 95 -35 L80 35 C35 50 -35 55 -100 50 Z" fill="none" stroke="#394452" strokeWidth="1.4" strokeDasharray="4 2" />
          <ellipse cx="-68" cy="0" rx="15" ry="15" fill="#2C3441" stroke="#3ED1B0" strokeWidth="1.8" />
          <circle cx="-68" cy="0" r="4.5" fill="#3ED1B0" />
          {/* Propeller Blades */}
          <path d="M-68 -15 C-64 -38 -50 -48 -45 -50 M-68 15 C-64 38 -50 48 -45 50" stroke="#3ED1B0" strokeWidth="2.2" fill="none" />
          <rect x="-52" y="-9" width="115" height="18" rx="3" fill="#242A35" stroke="#3ED1B0" strokeWidth="1.4" />
          <line x1="-12" y1="-28" x2="-12" y2="28" stroke="#3ED1B0" strokeWidth="2" />
          <line x1="14" y1="-24" x2="14" y2="24" stroke="#3ED1B0" strokeWidth="2" />
          <line x1="40" y1="-20" x2="40" y2="20" stroke="#48A9FF" strokeWidth="1.8" />
          <polygon points="62,-10 110,-5 98,0 110,5 62,10" fill="#F2B94B" opacity="0.75" />
        </g>
      </svg>
    );
  }

  if (subject === "Technical Specific") {
    return (
      <svg
        viewBox="0 0 400 180"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMidYMid slice"
        className={className}
      >
        <defs>
          <linearGradient id="specGradLuxe" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#2E1C16" />
            <stop offset="50%" stopColor="#40261E" />
            <stop offset="100%" stopColor="#1B100C" />
          </linearGradient>
          <clipPath id="specAdiClipLuxe">
            <circle r="44" />
          </clipPath>
        </defs>
        <rect width="400" height="180" fill="url(#specGradLuxe)" />
        {/* Cockpit Instrument Panel Housing */}
        <rect x="75" y="16" width="250" height="148" rx="10" fill="#1C2029" stroke="#394452" strokeWidth="1.8" />
        {/* Artificial Horizon (ADI) */}
        <g transform="translate(200, 90)">
          <g clipPath="url(#specAdiClipLuxe)">
            <rect x="-48" y="-48" width="96" height="48" fill="#1E88E5" opacity="0.8" />
            <rect x="-48" y="0" width="96" height="48" fill="#8D6E63" opacity="0.85" />
            <line x1="-48" y1="0" x2="48" y2="0" stroke="#F5F6FA" strokeWidth="1.8" />
            <line x1="-12" y1="-14" x2="12" y2="-14" stroke="#F5F6FA" strokeWidth="1.3" />
            <line x1="-12" y1="14" x2="12" y2="14" stroke="#F5F6FA" strokeWidth="1.3" />
          </g>
          <circle r="44" stroke="#F2B94B" strokeWidth="1.8" fill="none" />
          <path d="M-22 0 L-7 0 L-4 6 L0 1.5 L4 6 L7 0 L22 0" stroke="#F2B94B" strokeWidth="2.6" fill="none" />
          <circle cx="0" cy="0" r="2" fill="#F2B94B" />
        </g>
        {/* Airspeed Tape on Left */}
        <g transform="translate(90, 30)">
          <rect x="0" y="0" width="28" height="120" fill="#242A35" stroke="#394452" strokeWidth="1" />
          <line x1="24" y1="95" x2="24" y2="50" stroke="#F5F6FA" strokeWidth="2" />
          <line x1="24" y1="75" x2="24" y2="25" stroke="#3ED1B0" strokeWidth="2" />
          <line x1="24" y1="25" x2="24" y2="12" stroke="#F2B94B" strokeWidth="2" />
          <polygon points="2,55 18,55 24,60 18,65 2,65" fill="#48A9FF" />
          <text x="10" y="62" fill="#F5F6FA" fontSize="8" fontWeight="800" textAnchor="middle">120</text>
        </g>
        {/* Altimeter Tape on Right */}
        <g transform="translate(282, 30)">
          <rect x="0" y="0" width="32" height="120" fill="#242A35" stroke="#394452" strokeWidth="1" />
          <polygon points="30,55 12,55 6,60 12,65 30,65" fill="#48A9FF" />
          <text x="20" y="62" fill="#F5F6FA" fontSize="7.5" fontWeight="800" textAnchor="middle">4500</text>
        </g>
      </svg>
    );
  }

  // RTR
  return (
    <svg
      viewBox="0 0 400 180"
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="xMidYMid slice"
      className={className}
    >
      <defs>
        <linearGradient id="rtrGradLuxe" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#132433" />
          <stop offset="50%" stopColor="#1B3247" />
          <stop offset="100%" stopColor="#0E1B26" />
        </linearGradient>
      </defs>
      <rect width="400" height="180" fill="url(#rtrGradLuxe)" />
      {/* Radio Antenna Mast & Radiating RF Waves */}
      <g transform="translate(200, 140)">
        <polygon points="-7,0 7,0 2,-80 -2,-80" fill="#2C3441" stroke="#3ED1B0" strokeWidth="1.2" />
        <line x1="-20" y1="-26" x2="20" y2="-26" stroke="#3ED1B0" strokeWidth="1.5" />
        <line x1="-14" y1="-52" x2="14" y2="-52" stroke="#3ED1B0" strokeWidth="1.5" />
        <circle cx="0" cy="-80" r="4" fill="#F2B94B" />
        <path d="M-26 -80 A26 26 0 0 1 26 -80" stroke="#3ED1B0" strokeWidth="1.8" fill="none" opacity="0.85" />
        <path d="M-48 -80 A48 48 0 0 1 48 -80" stroke="#3ED1B0" strokeWidth="1.4" fill="none" opacity="0.6" strokeDasharray="4 2" />
        <path d="M-72 -80 A72 72 0 0 1 72 -80" stroke="#48A9FF" strokeWidth="1.1" fill="none" opacity="0.35" strokeDasharray="6 3" />
      </g>
      {/* 121.500 Guard Frequency Display */}
      <g transform="translate(65, 42)">
        <rect x="0" y="0" width="76" height="30" rx="4" fill="#1C2029" stroke="#3ED1B0" strokeWidth="1.2" />
        <text x="38" y="20" fill="#3ED1B0" fontSize="12" fontWeight="900" textAnchor="middle" fontFamily="monospace">121.500</text>
      </g>
      {/* Squawk 7700 Emergency Transponder Display */}
      <g transform="translate(260, 42)">
        <rect x="0" y="0" width="76" height="30" rx="4" fill="#1C2029" stroke="#F2B94B" strokeWidth="1.2" />
        <text x="38" y="20" fill="#F2B94B" fontSize="12" fontWeight="900" textAnchor="middle" fontFamily="monospace">SQ 7700</text>
      </g>
    </svg>
  );
}
