// Script to generate high precision CAD cutlist SVG for Symmetrical Dual-Face Modular Baffle Architecture
const fs = require('fs');
const path = require('path');

const width = 2600;
const height = 1750;

let svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">
<defs>
  <style>
    .bg { fill: #0b0f19; }
    .grid-line { stroke: #1e293b; stroke-width: 1; stroke-dasharray: 4,4; }
    .frame-border { fill: none; stroke: #38bdf8; stroke-width: 2.5; }
    .title-block { fill: #0f172a; stroke: #38bdf8; stroke-width: 1.5; }
    .section-box { fill: #0f172a; stroke: #1e293b; stroke-width: 1.5; rx: 8px; }
    .sec-header { fill: #1e293b; stroke: #38bdf8; stroke-width: 1; }
    
    .obj-outline { fill: none; stroke: #38bdf8; stroke-width: 2; stroke-linejoin: round; }
    .obj-fill { fill: #1e293b; stroke: #38bdf8; stroke-width: 2; }
    .obj-hidden { fill: none; stroke: #94a3b8; stroke-width: 1.5; stroke-dasharray: 6,4; }
    .obj-cutout { fill: #0b0f19; stroke: #f43f5e; stroke-width: 1.8; }
    .obj-rebate { fill: none; stroke: #fbbf24; stroke-width: 1.5; stroke-dasharray: 4,3; }
    .obj-brace { fill: #1e1b4b; stroke: #a855f7; stroke-width: 2; }
    
    .obj-plate-u1 { fill: #082f49; stroke: #38bdf8; stroke-width: 2; }
    .obj-plate-u2 { fill: #2e1065; stroke: #fbbf24; stroke-width: 2; }
    .obj-plate-u3 { fill: #4c0519; stroke: #f43f5e; stroke-width: 2; }
    .obj-plate-u4 { fill: #1e293b; stroke: #94a3b8; stroke-width: 2; }
    
    .obj-plate-p1 { fill: #1e293b; stroke: #94a3b8; stroke-width: 2; }
    .obj-plate-p2 { fill: #0c4a6e; stroke: #0284c7; stroke-width: 2; }
    .obj-plate-p3 { fill: #064e3b; stroke: #10b981; stroke-width: 2; }
    .obj-plate-p4 { fill: #581c87; stroke: #c084fc; stroke-width: 2; }
    .obj-port { fill: #0284c7; fill-opacity: 0.15; stroke: #0284c7; stroke-width: 2; }
    
    .centerline { stroke: #ef4444; stroke-width: 1; stroke-dasharray: 12,3,3,3; }
    .dim-line { stroke: #94a3b8; stroke-width: 1; marker-start: url(#arr-start); marker-end: url(#arr-end); }
    .dim-ext { stroke: #64748b; stroke-width: 0.8; stroke-dasharray: 2,2; }
    .dim-text { font-family: 'Consolas', 'Courier New', monospace; font-size: 11px; fill: #38bdf8; text-anchor: middle; }
    .dim-text-sm { font-family: 'Consolas', 'Courier New', monospace; font-size: 9.5px; fill: #cbd5e1; text-anchor: middle; }
    
    .lbl-title { font-family: 'Segoe UI', Arial, sans-serif; font-size: 22px; font-weight: 700; fill: #f8fafc; }
    .lbl-subtitle { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13.5px; font-weight: 600; fill: #38bdf8; }
    .lbl-sec { font-family: 'Segoe UI', Arial, sans-serif; font-size: 14.5px; font-weight: 700; fill: #38bdf8; text-transform: uppercase; letter-spacing: 1px; }
    .lbl-item { font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; font-weight: 600; fill: #f1f5f9; }
    .lbl-subitem { font-family: 'Consolas', monospace; font-size: 10.5px; fill: #94a3b8; }
    .lbl-val { font-family: 'Consolas', monospace; font-size: 11px; fill: #fbbf24; }
    .lbl-note { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: #cbd5e1; }
    
    .table-hdr { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: 700; fill: #38bdf8; }
    .table-row { font-family: 'Consolas', monospace; font-size: 10.5px; fill: #e2e8f0; }
    .table-cell-bg { fill: #1e293b; }
    .table-cell-alt { fill: #0f172a; }
  </style>

  <marker id="arr-end" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M 0 1 L 10 5 L 0 9 z" fill="#94a3b8"/>
  </marker>
  <marker id="arr-start" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="6" markerHeight="6" orient="auto">
    <path d="M 10 1 L 0 5 L 10 9 z" fill="#94a3b8"/>
  </marker>

  <pattern id="hatch-wood" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="10" stroke="#334155" stroke-width="1.5" />
  </pattern>
  <pattern id="hatch-damping" width="8" height="8" patternTransform="rotate(30 0 0)" patternUnits="userSpaceOnUse">
    <path d="M 0,0 Q 2,4 4,0 T 8,0" fill="none" stroke="#f59e0b" stroke-width="1" />
  </pattern>
</defs>

<!-- BACKGROUND -->
<rect width="${width}" height="${height}" class="bg" />

<!-- DRAWING SHEET BORDER -->
<rect x="25" y="25" width="${width-50}" height="${height-50}" class="frame-border" />
<rect x="30" y="30" width="${width-60}" height="${height-60}" stroke="#1e293b" stroke-width="1" fill="none" />

<!-- HEADER & TITLE BLOCK -->
<g transform="translate(50, 45)">
  <rect x="0" y="0" width="2500" height="80" class="title-block" rx="6" />
  <text x="25" y="34" class="lbl-title">SYMMETRICAL DUAL-FACE "日" LADDER FRAME MODULAR SPEAKER ENCLOSURE</text>
  <text x="25" y="60" class="lbl-subtitle">SYMMETRICAL FRONT &amp; REAR "日" FRAMES (112x206x12mm) • 40mm CROSSBARS • TIE-BEAM BRACE (D=134mm) • WORKING DRAWINGS</text>
  
  <line x1="1400" y1="10" x2="1400" y2="70" stroke="#334155" stroke-width="1" />
  
  <text x="1420" y="30" class="lbl-subitem">NET VOLUME:   <tspan class="lbl-val">3.02 - 3.15 L NET (3.41L GROSS, 3.4L EFF)</tspan></text>
  <text x="1420" y="50" class="lbl-subitem">OUTER BOX:    <tspan class="lbl-val">136mm (W) x 230mm (H) x 190mm (D)</tspan></text>
  <text x="1420" y="68" class="lbl-subitem">SYMMETRY:     <tspan class="lbl-val">Front: Z=0..28mm • Cavity: Z=28..162mm • Rear: Z=162..190mm</tspan></text>

  <line x1="2040" y1="10" x2="2040" y2="70" stroke="#334155" stroke-width="1" />

  <text x="2060" y="30" class="lbl-subitem">REAR PLATES: <tspan class="lbl-val">Solid Blanks (112x136 &amp; 112x70, NO HOLES)</tspan></text>
  <text x="2060" y="50" class="lbl-subitem">DRAWING NO:  <tspan class="lbl-val">SPK-SYMM-035-DWG-09</tspan>  REV: <tspan class="lbl-val">9.0</tspan></text>
  <text x="2060" y="68" class="lbl-subitem">DATE:        <tspan class="lbl-val">2026-08-29</tspan>  UNITS: <tspan class="lbl-val">MILLIMETERS (mm)</tspan></text>
</g>
`;

function hDim(x1, x2, y, text, extY1, extY2) {
  let s = '';
  if (extY1 !== undefined && extY2 !== undefined) {
    s += `<line x1="${x1}" y1="${extY1}" x2="${x1}" y2="${extY2}" class="dim-ext" />`;
    s += `<line x1="${x2}" y1="${extY1}" x2="${x2}" y2="${extY2}" class="dim-ext" />`;
  }
  s += `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" class="dim-line" />`;
  s += `<rect x="${(x1+x2)/2 - 25}" y="${y - 9}" width="50" height="15" fill="#0b0f19" opacity="0.85" rx="3" />`;
  s += `<text x="${(x1+x2)/2}" y="${y + 3}" class="dim-text">${text}</text>`;
  return s;
}

function vDim(y1, y2, x, text, extX1, extX2) {
  let s = '';
  if (extX1 !== undefined && extX2 !== undefined) {
    s += `<line x1="${extX1}" y1="${y1}" x2="${extX2}" y2="${y1}" class="dim-ext" />`;
    s += `<line x1="${extX1}" y1="${y2}" x2="${extX2}" y2="${y2}" class="dim-ext" />`;
  }
  s += `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" class="dim-line" />`;
  s += `<rect x="${x - 24}" y="${(y1+y2)/2 - 8}" width="48" height="15" fill="#0b0f19" opacity="0.85" rx="3" />`;
  s += `<text x="${x}" y="${(y1+y2)/2 + 3.5}" class="dim-text">${text}</text>`;
  return s;
}

function centerCross(cx, cy, r) {
  return `<line x1="${cx - r}" y1="${cy}" x2="${cx + r}" y2="${cy}" class="centerline" />
          <line x1="${cx}" y1="${cy - r}" x2="${cx}" y2="${cy + r}" class="centerline" />`;
}

// =============================================================================
// SECTION 1: ASSEMBLED FRONT VIEW & SAGITTAL SECTION
// =============================================================================
svg += `
<!-- SECTION 1 CONTAINER -->
<g transform="translate(50, 140)">
  <rect x="0" y="0" width="1120" height="740" class="section-box" />
  <rect x="0" y="0" width="1120" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">1. SYMMETRICAL DUAL-FACE ELEVATION &amp; SAGITTAL CROSS-SECTION (SCALE 1:2)</text>
`;

const s1 = 1.35;
const ox_front = 70;
const oy_front = 80;

// FRONT ELEVATION
svg += `
  <g transform="translate(${ox_front}, ${oy_front})">
    <text x="${136*s1/2}" y="-15" class="lbl-item" text-anchor="middle">FRONT ELEVATION (ACTIVE MODULAR BAFFLES)</text>
    
    <!-- Outer Cabinet Box Rim (136x230mm) -->
    <rect x="0" y="0" width="${136*s1}" height="${230*s1}" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5" rx="3" />
    
    <!-- Swappable Upper Driver Plate U2 (112 x 136 x 12mm) -->
    <rect x="${12*s1}" y="${12*s1}" width="${112*s1}" height="${136*s1}" rx="${4*s1}" class="obj-plate-u2" />
    
    <!-- Swappable Lower Acoustic Plate P2 (112 x 70 x 12mm) -->
    <rect x="${12*s1}" y="${148*s1}" width="${112*s1}" height="${70*s1}" rx="${4*s1}" class="obj-plate-p2" />

    <!-- Split Joint Line at Y=148mm from top (Y=82mm global) -->
    <line x1="${12*s1}" y1="${148*s1}" x2="${(136-12)*s1}" y2="${148*s1}" stroke="#f43f5e" stroke-width="2" />
    <text x="${68*s1}" y="${148*s1 - 4}" class="dim-text-sm" fill="#f43f5e">Split Seam (Y=82mm)</text>

    <!-- 8x M4 Screws -->
    ${[
      [-47, 25], [47, 25],   // Upper top (Y=205 => Y=25 from top)
      [-47, 138], [47, 138], // Upper btm on 40mm crossbar (Y=92 => Y=138 from top, 10mm above seam)
      [-47, 158], [47, 158], // Lower top on 40mm crossbar (Y=72 => Y=158 from top, 10mm below seam)
      [-47, 206], [47, 206]  // Lower btm (Y=24 => Y=206 from top)
    ].map(p => {
      return `<circle cx="${(68 + p[0])*s1}" cy="${p[1]*s1}" r="${4.5*s1/2}" fill="#fbbf24" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <!-- Driver U2 Cutouts at Y=75mm from top (Y=155mm global) -->
    <circle cx="${68*s1}" cy="${75*s1}" r="${96*s1/2}" class="obj-rebate" />
    <circle cx="${68*s1}" cy="${75*s1}" r="${76*s1/2}" class="obj-cutout" />
    <circle cx="${68*s1}" cy="${75*s1}" r="${64*s1/2}" fill="#0f172a" stroke="#475569" stroke-width="1.2" />
    <circle cx="${68*s1}" cy="${75*s1}" r="${22*s1/2}" fill="#334155" stroke="#fbbf24" stroke-width="1" />
    ${centerCross(68*s1, 75*s1, 55*s1)}

    <!-- Port P2 Cutouts at Y=183mm from top (Y=47mm global) -->
    <circle cx="${68*s1}" cy="${183*s1}" r="${53*s1/2}" class="obj-rebate" />
    <circle cx="${68*s1}" cy="${183*s1}" r="${41*s1/2}" class="obj-cutout" />
    <circle cx="${68*s1}" cy="${183*s1}" r="${35*s1/2}" fill="#0b0f19" stroke="#38bdf8" stroke-width="1.5" />
    ${centerCross(68*s1, 183*s1, 28*s1)}

    <!-- Dimensions -->
    ${hDim(0, 136*s1, -30, '136.0 mm (W)', -40, 0)}
    ${hDim(12*s1, (136-12)*s1, 245*s1, '112.0 mm (Plate Width)', 230*s1, 255*s1)}
    ${vDim(0, 75*s1, -40, '75.0', 0, -45)}
    ${vDim(75*s1, 148*s1, -40, '73.0 mm', 75*s1, -45)}
    ${vDim(148*s1, 183*s1, -40, '35.0 mm', 148*s1, -45)}
    ${vDim(183*s1, 230*s1, -40, '47.0 mm', 183*s1, -45)}
    ${vDim(0, 230*s1, -75, '230.0 mm (H)', 0, -80)}
  </g>
`;

// SIDE SAGITTAL SECTION (Symmetrical Dual-Face with Tie-Beam Brace)
const ox_sec = 410;
const oy_sec = 80;

svg += `
  <g transform="translate(${ox_sec}, ${oy_sec})">
    <text x="${190*s1/2}" y="-15" class="lbl-item" text-anchor="middle">SECTION X-X (SYMMETRICAL DUAL-FACE + TIE-BEAM BRACE)</text>
    
    <rect x="0" y="0" width="${190*s1}" height="${230*s1}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" />
    
    <!-- Top / Bottom Panels -->
    <rect x="0" y="0" width="${190*s1}" height="${12*s1}" fill="url(#hatch-wood)" stroke="#38bdf8" stroke-width="1.5" />
    <rect x="0" y="${(230-12)*s1}" width="${190*s1}" height="${12*s1}" fill="url(#hatch-wood)" stroke="#38bdf8" stroke-width="1.5" />

    <!-- Front 12mm Swappable Plates (Z=4..16mm) -->
    <rect x="${4*s1}" y="${12*s1}" width="${12*s1}" height="${136*s1}" fill="#2e1065" stroke="#fbbf24" stroke-width="1.5" />
    <rect x="${4*s1}" y="${148*s1}" width="${12*s1}" height="${70*s1}" fill="#0c4a6e" stroke="#0284c7" stroke-width="1.5" />

    <!-- Front "日" Ladder Frame (Z=16..28mm) -->
    <rect x="${16*s1}" y="${12*s1}" width="${12*s1}" height="${10*s1}" fill="url(#hatch-wood)" stroke="#fbbf24" stroke-width="1.5" />
    <rect x="${16*s1}" y="${128*s1}" width="${12*s1}" height="${40*s1}" fill="url(#hatch-wood)" stroke="#f43f5e" stroke-width="1.5" />
    <rect x="${16*s1}" y="${208*s1}" width="${12*s1}" height="${10*s1}" fill="url(#hatch-wood)" stroke="#fbbf24" stroke-width="1.5" />

    <!-- Front Port Tube -->
    <rect x="${16*s1}" y="${(183-41/2)*s1}" width="${108*s1}" height="${41*s1}" class="obj-port" rx="3" />
    <rect x="${16*s1}" y="${(183-35/2)*s1}" width="${108*s1}" height="${35*s1}" fill="#0b0f19" stroke="#38bdf8" stroke-width="1" />

    <!-- Internal Window Brace (Length=134mm from Z=28 to Z=162 linking Front & Rear 40mm Crossbars at Y=148mm from top => Y=82mm global) -->
    <rect x="${28*s1}" y="${(148-6)*s1}" width="${24*s1}" height="${12*s1}" class="obj-brace" />
    <rect x="${(162-24)*s1}" y="${(148-6)*s1}" width="${24*s1}" height="${12*s1}" class="obj-brace" />
    <line x1="${(28+24)*s1}" y1="${148*s1}" x2="${(162-24)*s1}" y2="${148*s1}" stroke="#a855f7" stroke-width="1.5" stroke-dasharray="4,4" />

    <!-- Rear "日" Ladder Frame (Z=162..174mm) -->
    <rect x="${162*s1}" y="${12*s1}" width="${12*s1}" height="${10*s1}" fill="url(#hatch-wood)" stroke="#fbbf24" stroke-width="1.5" />
    <rect x="${162*s1}" y="${128*s1}" width="${12*s1}" height="${40*s1}" fill="url(#hatch-wood)" stroke="#f43f5e" stroke-width="1.5" />
    <rect x="${162*s1}" y="${208*s1}" width="${12*s1}" height="${10*s1}" fill="url(#hatch-wood)" stroke="#fbbf24" stroke-width="1.5" />

    <!-- Rear 12mm Solid Blank Plates (Z=174..186mm, NO HOLES) -->
    <rect x="${174*s1}" y="${12*s1}" width="${12*s1}" height="${136*s1}" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5" />
    <rect x="${174*s1}" y="${148*s1}" width="${12*s1}" height="${70*s1}" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5" />

    <!-- Damping -->
    <rect x="${30*s1}" y="${14*s1}" width="${130*s1}" height="${15*s1}" fill="url(#hatch-damping)" />

    <!-- Dimensions -->
    ${hDim(0, 190*s1, -30, '190.0 mm (D)', -40, 0)}
    ${hDim(4*s1, 28*s1, 245*s1, '24mm Front Baffle', 12*s1, 255*s1)}
    ${hDim(28*s1, 162*s1, 245*s1, '134.0 mm Cavity', (230-12)*s1, 255*s1)}
    ${hDim(162*s1, 186*s1, 245*s1, '24mm Rear Baffle', 12*s1, 255*s1)}
  </g>

  <!-- HIGHLIGHTS -->
  <g transform="translate(760, 80)">
    <text x="0" y="15" class="lbl-subtitle">SYMMETRICAL DUAL-FACE ADVANTAGES</text>
    <text x="0" y="45" class="lbl-note">• <tspan fill="#38bdf8">100% Symmetrical Chassis:</tspan> Front and Rear feature identical</text>
    <text x="12" y="65" class="lbl-note">"日" ladder frames (112x206x12mm) and 4.0mm inset recesses.</text>
    <text x="0" y="95" class="lbl-note">• <tspan fill="#a855f7">Tie-Beam Tension/Compression Brace:</tspan> 112x12x134mm brace</text>
    <text x="12" y="115" class="lbl-note">directly ties the front 40mm crossbar to the rear 40mm crossbar.</text>
    <text x="0" y="145" class="lbl-note">• <tspan fill="#fbbf24">Universal Modular Reversibility:</tspan> Rear face comes equipped with</text>
    <text x="12" y="165" class="lbl-note">solid blanks (NO HOLES), but accepts ANY sub-baffle module.</text>
    <text x="0" y="195" class="lbl-note">• <tspan fill="#f43f5e">Future Testing Flexibility:</tspan> Easily test rear passive radiators,</text>
    <text x="12" y="215" class="lbl-note">rear flared ports, or isobaric/bipolar dual-driver configurations.</text>
  </g>
</g>
`;

// =============================================================================
// SECTION 2: UPPER DRIVER PLATES & REAR SOLID UPPER (112 x 136 x 12 mm)
// =============================================================================
svg += `
<!-- SECTION 2 CONTAINER -->
<g transform="translate(1200, 140)">
  <rect x="0" y="0" width="1350" height="370" class="section-box" />
  <rect x="0" y="0" width="1350" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">2. 12mm UPPER DRIVER PLATES &amp; REAR SOLID UPPER (112.0 x 136.0 x 12.0 mm)</text>
`;

const su = 1.20;

// PLATE U1
svg += `
  <g transform="translate(45, 55)">
    <text x="${112*su/2}" y="-10" class="lbl-item" text-anchor="middle">PLATE U1: 2" - 2.5" DRIVERS</text>
    <text x="${112*su/2}" y="${136*su + 18}" class="lbl-subitem" text-anchor="middle">PLS / W2 / ND65 (Cutout Ø56, Reb Ø68)</text>
    
    <rect x="0" y="0" width="${112*su}" height="${136*su}" rx="${4*su}" class="obj-plate-u1" />
    
    ${[[-47, -55], [47, -55], [-47, 58], [47, 58]].map(p => {
      return `<circle cx="${(112/2 + p[0])*su}" cy="${(136/2 + p[1])*su}" r="${4.5*su/2}" fill="#38bdf8" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <circle cx="${112*su/2}" cy="${(136/2 - 5)*su}" r="${68*su/2}" class="obj-rebate" />
    <circle cx="${112*su/2}" cy="${(136/2 - 5)*su}" r="${56*su/2}" class="obj-cutout" />
    ${centerCross(112*su/2, (136/2 - 5)*su, 40*su)}

    <text x="${112*su/2}" y="${(136/2 - 5)*su - 38}" class="dim-text-sm" fill="#fbbf24">Rebate: Ø68 x 3mm</text>
    <text x="${112*su/2}" y="${(136/2 - 5)*su + 4}" class="dim-text-sm" fill="#f43f5e">Cutout: Ø56mm</text>
  </g>
`;

// PLATE U2
svg += `
  <g transform="translate(370, 55)">
    <text x="${112*su/2}" y="-10" class="lbl-item" text-anchor="middle">PLATE U2: 3" - 3.5" BENCHMARK</text>
    <text x="${112*su/2}" y="${136*su + 18}" class="lbl-subitem" text-anchor="middle">W3-881 / ND91 / Alpair 5.3 / 10F</text>
    
    <rect x="0" y="0" width="${112*su}" height="${136*su}" rx="${4*su}" class="obj-plate-u2" />
    
    ${[[-47, -55], [47, -55], [-47, 58], [47, 58]].map(p => {
      return `<circle cx="${(112/2 + p[0])*su}" cy="${(136/2 + p[1])*su}" r="${4.5*su/2}" fill="#fbbf24" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <circle cx="${112*su/2}" cy="${(136/2 - 5)*su}" r="${96*su/2}" class="obj-rebate" />
    <circle cx="${112*su/2}" cy="${(136/2 - 5)*su}" r="${76*su/2}" class="obj-cutout" />
    <circle cx="${112*su/2}" cy="${(136/2 - 5)*su}" r="${96*su/2}" stroke="#a855f7" stroke-width="1" stroke-dasharray="2,2" fill="none" />
    ${centerCross(112*su/2, (136/2 - 5)*su, 50*su)}

    <text x="${112*su/2}" y="${(136/2 - 5)*su - 48}" class="dim-text-sm" fill="#fbbf24">Rebate: Ø96 x 3.5mm</text>
    <text x="${112*su/2}" y="${(136/2 - 5)*su + 4}" class="dim-text-sm" fill="#f43f5e">Cutout: Ø76mm</text>
  </g>
`;

// PLATE U3
svg += `
  <g transform="translate(695, 55)">
    <text x="${112*su/2}" y="-10" class="lbl-item" text-anchor="middle">PLATE U3: 3.5" - 4" WOOFERS</text>
    <text x="${112*su/2}" y="${136*su + 18}" class="lbl-subitem" text-anchor="middle">TCP115 / W4-1337 / CHR-70</text>
    
    <rect x="0" y="0" width="${112*su}" height="${136*su}" rx="${4*su}" class="obj-plate-u3" />
    
    ${[[-47, -55], [47, -55], [-47, 58], [47, 58]].map(p => {
      return `<circle cx="${(112/2 + p[0])*su}" cy="${(136/2 + p[1])*su}" r="${4.5*su/2}" fill="#f43f5e" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <circle cx="${112*su/2}" cy="${(136/2 - 5)*su}" r="${108*su/2}" class="obj-rebate" />
    <circle cx="${112*su/2}" cy="${(136/2 - 5)*su}" r="${96*su/2}" class="obj-cutout" />
    ${centerCross(112*su/2, (136/2 - 5)*su, 54*su)}

    <text x="${112*su/2}" y="${(136/2 - 5)*su - 42}" class="dim-text-sm" fill="#fbbf24">Rebate: Ø108 x 3.5mm</text>
    <text x="${112*su/2}" y="${(136/2 - 5)*su + 4}" class="dim-text-sm" fill="#f43f5e">Cutout: Ø96mm</text>
  </g>
`;

// REAR UPPER SOLID BLANK (NO HOLES)
svg += `
  <g transform="translate(1020, 55)">
    <text x="${112*su/2}" y="-10" class="lbl-item" text-anchor="middle">REAR UPPER SOLID BLANK</text>
    <text x="${112*su/2}" y="${136*su + 18}" class="lbl-subitem" text-anchor="middle">Installed on Rear (NO HOLES)</text>
    
    <rect x="0" y="0" width="${112*su}" height="${136*su}" rx="${4*su}" class="obj-plate-u4" />
    
    ${[[-47, -55], [47, -55], [-47, 58], [47, 58]].map(p => {
      return `<circle cx="${(112/2 + p[0])*su}" cy="${(136/2 + p[1])*su}" r="${4.5*su/2}" fill="#94a3b8" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    ${centerCross(112*su/2, 136*su/2, 45*su)}
    <text x="${112*su/2}" y="${136*su/2}" class="dim-text-sm" fill="#94a3b8">SOLID 12mm BLANK (NO HOLES)</text>
  </g>
</g>
`;

// =============================================================================
// SECTION 3: LOWER ACOUSTIC MODULES & REAR SOLID LOWER (112 x 70 x 12 mm)
// =============================================================================
svg += `
<!-- SECTION 3 CONTAINER -->
<g transform="translate(1200, 530)">
  <rect x="0" y="0" width="1350" height="350" class="section-box" />
  <rect x="0" y="0" width="1350" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">3. 12mm LOWER ACOUSTIC MODULES &amp; REAR SOLID LOWER (112.0 x 70.0 x 12.0 mm)</text>
`;

const sp = 1.20;

// REAR LOWER SOLID BLANK (NO HOLES)
svg += `
  <g transform="translate(45, 60)">
    <text x="${112*sp/2}" y="-10" class="lbl-item" text-anchor="middle">REAR LOWER SOLID BLANK</text>
    <text x="${112*sp/2}" y="${70*sp + 18}" class="lbl-subitem" text-anchor="middle">Installed on Rear (NO HOLES)</text>
    
    <rect x="0" y="0" width="${112*sp}" height="${70*sp}" rx="${4*sp}" class="obj-plate-p1" />
    
    ${[[-47, -25], [47, -25], [-47, 23], [47, 23]].map(p => {
      return `<circle cx="${(112/2 + p[0])*sp}" cy="${(70/2 + p[1])*sp}" r="${4.5*sp/2}" fill="#94a3b8" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    ${centerCross(112*sp/2, 70*sp/2, 25*sp)}
    <text x="${112*sp/2}" y="${70*sp/2 + 4}" class="dim-text-sm" fill="#e2e8f0">SOLID 12mm (NO HOLES)</text>
  </g>
`;

// MODULE P2: PORT SOCKET
svg += `
  <g transform="translate(370, 60)">
    <text x="${112*sp/2}" y="-10" class="lbl-item" text-anchor="middle">MODULE P2: FRONT PORT</text>
    <text x="${112*sp/2}" y="${70*sp + 18}" class="lbl-subitem" text-anchor="middle"><tspan fill="#38bdf8">Fb = 70.8 Hz</tspan> (Ø35 x 120mm)</text>
    
    <rect x="0" y="0" width="${112*sp}" height="${70*sp}" rx="${4*sp}" class="obj-plate-p2" />
    
    ${[[-47, -25], [47, -25], [-47, 23], [47, 23]].map(p => {
      return `<circle cx="${(112/2 + p[0])*sp}" cy="${(70/2 + p[1])*sp}" r="${4.5*sp/2}" fill="#0284c7" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <circle cx="${112*sp/2}" cy="${70*sp/2}" r="${53*sp/2}" class="obj-rebate" />
    <circle cx="${112*sp/2}" cy="${70*sp/2}" r="${41*sp/2}" class="obj-cutout" />
    <circle cx="${112*sp/2}" cy="${70*sp/2}" r="${35*sp/2}" fill="#0b0f19" stroke="#38bdf8" stroke-width="1.2" />
    ${centerCross(112*sp/2, 70*sp/2, 25*sp)}

    <text x="${112*sp/2}" y="${70*sp/2 + 4}" class="dim-text-sm" fill="#38bdf8">Ø35mm Socket</text>
  </g>
`;

// MODULE P3: SLIT DUCT
svg += `
  <g transform="translate(695, 60)">
    <text x="${112*sp/2}" y="-10" class="lbl-item" text-anchor="middle">MODULE P3: SLIT DUCT</text>
    <text x="${112*sp/2}" y="${70*sp + 18}" class="lbl-subitem" text-anchor="middle"><tspan fill="#10b981">Fb = 72.5 Hz</tspan> (90 x 14 x 120mm)</text>
    
    <rect x="0" y="0" width="${112*sp}" height="${70*sp}" rx="${4*sp}" class="obj-plate-p3" />
    
    ${[[-47, -25], [47, -25], [-47, 23], [47, 23]].map(p => {
      return `<circle cx="${(112/2 + p[0])*sp}" cy="${(70/2 + p[1])*sp}" r="${4.5*sp/2}" fill="#10b981" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <rect x="${(112-90)*sp/2}" y="${(70-14)*sp/2}" width="${90*sp}" height="${14*sp}" rx="${3*sp}" class="obj-cutout" />
    ${centerCross(112*sp/2, 70*sp/2, 25*sp)}

    <text x="${112*sp/2}" y="${70*sp/2 + 4}" class="dim-text-sm" fill="#fbbf24">90 x 14mm Slit</text>
  </g>
`;

// MODULE P4: PASSIVE RADIATOR
svg += `
  <g transform="translate(1020, 60)">
    <text x="${112*sp/2}" y="-10" class="lbl-item" text-anchor="middle">MODULE P4: PASSIVE RAD</text>
    <text x="${112*sp/2}" y="${70*sp + 18}" class="lbl-subitem" text-anchor="middle"><tspan fill="#c084fc">Fb ~ 55-65 Hz</tspan> (3-3.5" PR)</text>
    
    <rect x="0" y="0" width="${112*sp}" height="${70*sp}" rx="${4*sp}" class="obj-plate-p4" />
    
    ${[[-47, -25], [47, -25], [-47, 23], [47, 23]].map(p => {
      return `<circle cx="${(112/2 + p[0])*sp}" cy="${(70/2 + p[1])*sp}" r="${4.5*sp/2}" fill="#c084fc" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <circle cx="${112*sp/2}" cy="${70*sp/2}" r="${76*sp/2}" class="obj-cutout" />
    <circle cx="${112*sp/2}" cy="${70*sp/2}" r="${52*sp/2}" fill="#581c87" stroke="#c084fc" stroke-width="1.2" />
    ${centerCross(112*sp/2, 70*sp/2, 25*sp)}

    <text x="${112*sp/2}" y="${70*sp/2 + 4}" class="dim-text-sm" fill="#e2e8f0">PR Ø76mm</text>
  </g>
</g>
`;

// =============================================================================
// SECTION 4: 2D CNC CUTLIST & PANEL SPECIFICATIONS
// =============================================================================
svg += `
<!-- SECTION 4 CONTAINER -->
<g transform="translate(50, 910)">
  <rect x="0" y="0" width="1380" height="780" class="section-box" />
  <rect x="0" y="0" width="1380" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">4. CABINET PANELS CNC CUTLIST (12.0mm BIRCH PLYWOOD / MDF)</text>
`;

const s4 = 1.15;

// PANEL 1: "日" LADDER INNER FIXED BAFFLE FRAMES (2x - FRONT & REAR)
svg += `
  <g transform="translate(35, 65)">
    <text x="${112*s4/2}" y="-12" class="lbl-item" text-anchor="middle">PANEL 1: "日" LADDER FRAMES (2x - FRONT &amp; REAR)</text>
    <text x="${112*s4/2}" y="${206*s4 + 18}" class="lbl-subitem" text-anchor="middle">112 x 206 x 12.0 mm (Z=16..28 &amp; Z=162..174)</text>
    
    <rect x="0" y="0" width="${112*s4}" height="${206*s4}" class="obj-fill" rx="2" />
    
    <!-- Upper Window: 90 x 106mm -->
    <rect x="${(112-90)*s4/2}" y="${10*s4}" width="${90*s4}" height="${106*s4}" rx="${5*s4}" class="obj-cutout" />

    <!-- Center Dividing Crossbar: 112 x 40mm -->
    <rect x="0" y="${116*s4}" width="${112*s4}" height="${40*s4}" fill="#334155" stroke="#f43f5e" stroke-width="1.2" opacity="0.4" />

    <!-- Lower Window: 90 x 40mm -->
    <rect x="${(112-90)*s4/2}" y="${156*s4}" width="${90*s4}" height="${40*s4}" rx="${5*s4}" class="obj-cutout" />

    <!-- 8x M4 Insert Seats -->
    ${[
      [-47, 13], [47, 13],
      [-47, 126], [47, 126],
      [-47, 146], [47, 146],
      [-47, 194], [47, 194]
    ].map(p => {
      return `<circle cx="${(56 + p[0])*s4}" cy="${p[1]*s4}" r="${5.8*s4/2}" fill="#fbbf24" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <text x="${56*s4}" y="${63*s4}" class="dim-text-sm" fill="#f43f5e">Upper: 90 x 106 mm</text>
    <text x="${56*s4}" y="${136*s4 + 3.5}" class="dim-text-sm" fill="#fbbf24">40mm Crossbar (Y=82)</text>
    <text x="${56*s4}" y="${176*s4}" class="dim-text-sm" fill="#f43f5e">Lower: 90 x 40 mm</text>

    ${hDim(0, 112*s4, -22, '112.0 mm', -25, 0)}
    ${vDim(0, 206*s4, 130*s4, '206.0 mm', 112*s4, 135*s4)}
  </g>
`;

// PANEL 2: TOP / BTM (136x190mm)
svg += `
  <g transform="translate(280, 65)">
    <text x="${136*s4/2}" y="-12" class="lbl-item" text-anchor="middle">PANEL 2: TOP / BTM (2x)</text>
    <text x="${136*s4/2}" y="${190*s4 + 18}" class="lbl-subitem" text-anchor="middle">136 x 190 x 12.0 mm (Dual Chamfers)</text>
    
    <rect x="0" y="0" width="${136*s4}" height="${190*s4}" class="obj-fill" rx="2" />
    <line x1="0" y1="${3*s4}" x2="${136*s4}" y2="${3*s4}" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3" />
    <line x1="0" y1="${(190-3)*s4}" x2="${136*s4}" y2="${(190-3)*s4}" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3" />

    ${hDim(0, 136*s4, -25, '136.0 mm (W)', -30, 0)}
    ${vDim(0, 190*s4, 155*s4, '190.0 mm (D)', 136*s4, 160*s4)}
  </g>
`;

// PANEL 3: SIDES (206x190mm)
svg += `
  <g transform="translate(560, 65)">
    <text x="${190*s4/2}" y="-12" class="lbl-item" text-anchor="middle">PANEL 3: SIDES (2x)</text>
    <text x="${190*s4/2}" y="${206*s4 + 18}" class="lbl-subitem" text-anchor="middle">190 x 206 x 12.0 mm (Dado Z=28..162)</text>
    
    <rect x="0" y="0" width="${190*s4}" height="${206*s4}" class="obj-fill" rx="2" />
    <line x1="${3*s4}" y1="0" x2="${3*s4}" y2="${206*s4}" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3" />
    <line x1="${(190-3)*s4}" y1="0" x2="${(190-3)*s4}" y2="${206*s4}" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3" />
    <rect x="${28*s4}" y="${(206-82-6)*s4}" width="${134*s4}" height="${12*s4}" fill="#312e81" stroke="#818cf8" stroke-width="1" stroke-dasharray="3,3" />
    <text x="${190*s4/2}" y="${(206-82+3)*s4}" class="dim-text-sm" fill="#c7d2fe">3mm Dado (Z=28..162mm)</text>

    ${hDim(0, 190*s4, -25, '190.0 mm (D)', -30, 0)}
    ${vDim(0, 206*s4, 210*s4, '206.0 mm (H)', 190*s4, 215*s4)}
  </g>
`;

// PANEL 4: INTERNAL TIE-BEAM WINDOW BRACE (112x134mm)
svg += `
  <g transform="translate(900, 65)">
    <text x="${112*s4/2}" y="-12" class="lbl-item" text-anchor="middle">PANEL 4: TIE-BEAM BRACE (1x)</text>
    <text x="${112*s4/2}" y="${134*s4 + 18}" class="lbl-subitem" text-anchor="middle">112 x 134 x 12.0 mm (Cutout 64x86)</text>
    
    <rect x="0" y="0" width="${112*s4}" height="${134*s4}" class="obj-brace" rx="2" />
    <rect x="${24*s4}" y="${24*s4}" width="${64*s4}" height="${86*s4}" rx="${15*s4}" fill="#0b0f19" stroke="#f43f5e" stroke-width="1.8" />
    
    <text x="${112*s4/2}" y="${134*s4/2}" class="dim-text-sm" fill="#f43f5e">64 x 86 mm Cutout</text>

    ${hDim(0, 112*s4, -22, '112.0 mm', -25, 0)}
  </g>
</g>
`;

// =============================================================================
// SECTION 5: MATRIX & BOM
// =============================================================================
svg += `
<!-- SECTION 5 CONTAINER -->
<g transform="translate(1460, 910)">
  <rect x="0" y="0" width="1090" height="780" class="section-box" />
  <rect x="0" y="0" width="1090" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">5. SYMMETRICAL DUAL-FACE SYSTEM MATRIX &amp; BOM SCHEDULE</text>

  <g transform="translate(20, 50)">
    <text x="0" y="15" class="lbl-subtitle">A. UPPER / LOWER COMBINATION ACOUSTIC MATRIX</text>
    <rect x="0" y="25" width="1050" height="24" fill="#1e293b" rx="3" />
    <text x="15" y="41" class="table-hdr">FRONT UPPER</text>
    <text x="170" y="41" class="table-hdr">FRONT LOWER</text>
    <text x="325" y="41" class="table-hdr">REAR CONFIG</text>
    <text x="510" y="41" class="table-hdr">TUNING (Fb)</text>
    <text x="660" y="41" class="table-hdr">SONIC CHARACTER / USE CASE</text>
  </g>
`;

const splitRows = [
  { up: 'Plate U1 (2"-2.5")', low: 'Module P1 (Sealed)', rear: 'Solid Blanks', fb: 'Qtc ~ 0.72', note: 'Ultra-compact desk monitor, fast transients' },
  { up: 'Plate U1 (2"-2.5")', low: 'Module P2 (Short 80)', rear: 'Solid Blanks', fb: 'Fb = 84.5 Hz', note: 'Elevated SPL & high power handling' },
  { up: 'Plate U2 (3"-3.5")', low: 'Module P2 (Std 120)', rear: 'Solid Blanks', fb: 'Fb = 70.8 Hz', note: 'Audiophile Reference nearfield benchmark' },
  { up: 'Plate U2 (3"-3.5")', low: 'Module P3 (Slit Duct)', rear: 'Solid Blanks', fb: 'Fb = 72.5 Hz', note: 'Zero port chuffing, linear laminar airflow' },
  { up: 'Plate U2 (3"-3.5")', low: 'Module P1 (Sealed)', rear: 'Rear Module P4 (PR)', fb: 'Fb ~ 58-65 Hz', note: 'Rear PR alignment, zero pipe resonance' },
  { up: 'Plate U3 (3.5"-4")', low: 'Module P2 (Long 150)', rear: 'Solid Blanks', fb: 'Fb = 64.5 Hz', note: 'Extended sub-bass down to 48Hz' },
  { up: 'Plate U3 (3.5"-4")', low: 'Module P3 (Slit Duct)', rear: 'Solid Blanks', fb: 'Fb = 70.0 Hz', note: 'Punchy bass dynamics for 4" long-throw' },
];

splitRows.forEach((r, idx) => {
  const y = 120 + idx * 28;
  const bg = idx % 2 === 0 ? 'table-cell-bg' : 'table-cell-alt';
  svg += `
  <g transform="translate(20, ${y})">
    <rect x="0" y="0" width="1050" height="25" class="${bg}" rx="3" />
    <text x="15" y="17" class="table-row" fill="#fbbf24">${r.up}</text>
    <text x="170" y="17" class="table-row" fill="#38bdf8">${r.low}</text>
    <text x="325" y="17" class="table-row" fill="#cbd5e1">${r.rear}</text>
    <text x="510" y="17" class="table-row" fill="#a855f7" font-weight="700">${r.fb}</text>
    <text x="660" y="17" class="table-row" fill="#f8fafc" font-size="9.5px">${r.note}</text>
  </g>
  `;
});

// BOM TABLE
svg += `
  <g transform="translate(20, 330)">
    <text x="0" y="15" class="lbl-subtitle">B. SYMMETRICAL DUAL-FACE SYSTEM BOM SCHEDULE</text>
    <rect x="0" y="25" width="1050" height="24" fill="#1e293b" rx="3" />
    <text x="15" y="41" class="table-hdr">PART ID</text>
    <text x="95" y="41" class="table-hdr">COMPONENT</text>
    <text x="240" y="41" class="table-hdr">QTY</text>
    <text x="290" y="41" class="table-hdr">SPECIFICATION / MATERIAL</text>
    <text x="660" y="41" class="table-hdr">FUNCTION &amp; MOUNTING</text>
  </g>
`;

const splitBom = [
  { id: 'PAN-TOP/BTM', name: 'Top / Bottom Panels', qty: '2', spec: '136 x 190 x 12.0mm (Birch Plywood / MDF)', fn: 'Continuous wrapper with dual 45° chamfers' },
  { id: 'PAN-SIDES', name: 'Left / Right Sides', qty: '2', spec: '190 x 206 x 12.0mm (Birch Plywood / MDF)', fn: 'Side walls with 134mm brace dado at Y=82mm' },
  { id: 'PAN-FRAME', name: '"日" Ladder Frames', qty: '2', spec: '112 x 206 x 12.0mm (40mm Center Crossbar)', fn: 'Front (Z=16..28) & Rear (Z=162..174) frames' },
  { id: 'PAN-BRACE', name: 'Tie-Beam Window Brace', qty: '1', spec: '112 x 134 x 12.0mm (Cutout 64x86mm)', fn: 'Directly links front & rear 40mm crossbars' },
  { id: 'MOD-U1..U4', name: '12mm Upper Plates', qty: '4', spec: '112 x 136 x 12.0mm (6061 Aluminum / Birch)', fn: 'Front swappable plates for 2", 3", 4" & Blank' },
  { id: 'MOD-P1..P4', name: '12mm Lower Modules', qty: '4', spec: '112 x 70 x 12.0mm (6061 Aluminum / PETG)', fn: 'Front swappable Sealed, Port, Slit, PR' },
  { id: 'MOD-REAR-U', name: 'Rear Upper Solid Blank', qty: '1', spec: '112 x 136 x 12.0mm (Birch / Aluminum, NO HOLES)', fn: 'Rear upper chamber sealing plate' },
  { id: 'MOD-REAR-P', name: 'Rear Lower Solid Blank', qty: '1', spec: '112 x 70 x 12.0mm (Birch / Aluminum, NO HOLES)', fn: 'Rear lower chamber sealing plate' },
  { id: 'GSK-LADDER', name: 'Dual-Face Gaskets', qty: '4 Sets', spec: '112 x 206 x 1.5mm Dual-Window EVA (40mm bar)', fn: 'Front & rear airtight hermetic sealing' },
  { id: 'FST-M4IN', name: 'M4 Brass Inserts', qty: '16', spec: 'M4 x 8.0mm Heat-Set Brass Inserts', fn: '8 front inserts + 8 rear inserts' },
  { id: 'FST-M4SC', name: 'M4 Screws', qty: '16', spec: 'M4 x 20mm Countersunk Socket Screws', fn: '8 front screws + 8 rear screws' },
];

splitBom.forEach((r, idx) => {
  const y = 395 + idx * 29;
  const bg = idx % 2 === 0 ? 'table-cell-bg' : 'table-cell-alt';
  svg += `
  <g transform="translate(20, ${y})">
    <rect x="0" y="0" width="1050" height="25" class="${bg}" rx="3" />
    <text x="15" y="17" class="table-row" fill="#38bdf8">${r.id}</text>
    <text x="95" y="17" class="table-row" fill="#f8fafc" font-weight="600">${r.name}</text>
    <text x="240" y="17" class="table-row" fill="#fbbf24">${r.qty}</text>
    <text x="290" y="17" class="table-row" fill="#cbd5e1">${r.spec}</text>
    <text x="660" y="17" class="table-row" fill="#94a3b8" font-size="9.5px">${r.fn}</text>
  </g>
  `;
});

svg += `</g>`;
svg += `\n</svg>`;

const outputPath = path.join(__dirname, '..', 'cad', 'cutlist_drawings.svg');
fs.writeFileSync(outputPath, svg, 'utf8');
console.log('Successfully generated Symmetrical Dual-Face cutlist_drawings.svg at:', outputPath);
