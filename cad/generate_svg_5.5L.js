// Script to generate high precision CAD cutlist SVG for 5.5L Deep-Bass DBR Speaker Architecture
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
  <text x="25" y="34" class="lbl-title">5.5L DEEP-BASS DOUBLE BASS-REFLEX (DBR) SPEAKER ENCLOSURE</text>
  <text x="25" y="60" class="lbl-subtitle">W180 x H297 x D210mm • SYMMETRICAL "日" LADDER (112x286) • DBR PARTITION (ID 30mm PORT) • 100% COMMON UPPER PLATES</text>
  
  <line x1="1400" y1="10" x2="1400" y2="70" stroke="#334155" stroke-width="1" />
  
  <text x="1420" y="30" class="lbl-subitem">NET VOLUME:   <tspan class="lbl-val">5.45 L NET (V1=2.2L, V2=3.25L, ~6.0L EFF)</tspan></text>
  <text x="1420" y="50" class="lbl-subitem">OUTER BOX:    <tspan class="lbl-val">136mm (W) x 310mm (H) x 210mm (D)</tspan></text>
  <text x="1420" y="68" class="lbl-subitem">DBR TUNING:   <tspan class="lbl-val">f_L = 42.0 Hz, f_H = 95.0 Hz (Sub-Bass to 38Hz)</tspan></text>

  <line x1="2040" y1="10" x2="2040" y2="70" stroke="#334155" stroke-width="1" />

  <text x="2060" y="30" class="lbl-subitem">SPLIT LINE:  <tspan class="lbl-val">Y = 162.0 mm (40mm Center Crossbar)</tspan></text>
  <text x="2060" y="50" class="lbl-subitem">DRAWING NO:  <tspan class="lbl-val">SPK-DBR55-035-DWG-01</tspan>  REV: <tspan class="lbl-val">1.0</tspan></text>
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
// SECTION 1: ASSEMBLED FRONT VIEW & SAGITTAL SECTION (5.5L DBR)
// =============================================================================
svg += `
<!-- SECTION 1 CONTAINER -->
<g transform="translate(50, 140)">
  <rect x="0" y="0" width="1120" height="740" class="section-box" />
  <rect x="0" y="0" width="1120" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">1. 5.5L DBR ELEVATION &amp; SAGITTAL CROSS-SECTION (SCALE 1:2.2)</text>
`;

const s1 = 1.05;
const ox_front = 70;
const oy_front = 60;

// FRONT ELEVATION
svg += `
  <g transform="translate(${ox_front}, ${oy_front})">
    <text x="${136*s1/2}" y="-15" class="lbl-item" text-anchor="middle">FRONT ELEVATION (5.5L DBR ACTIVE BAFFLES)</text>
    
    <!-- Outer Cabinet Box Rim (136x310mm) -->
    <rect x="0" y="0" width="${136*s1}" height="${310*s1}" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5" rx="3" />
    
    <!-- Swappable Upper Driver Plate U2 (112 x 136 x 12mm) -->
    <rect x="${12*s1}" y="${12*s1}" width="${112*s1}" height="${136*s1}" rx="${4*s1}" class="obj-plate-u2" />
    
    <!-- Swappable Lower Acoustic Plate P2 (112 x 150 x 12mm) -->
    <rect x="${12*s1}" y="${148*s1}" width="${112*s1}" height="${150*s1}" rx="${4*s1}" class="obj-plate-p2" />

    <!-- Split Joint Line at Y=148mm from top (Y=162mm global) -->
    <line x1="${12*s1}" y1="${148*s1}" x2="${(136-12)*s1}" y2="${148*s1}" stroke="#f43f5e" stroke-width="2" />
    <text x="${68*s1}" y="${148*s1 - 4}" class="dim-text-sm" fill="#f43f5e">Split Seam (Y=162mm)</text>

    <!-- 8x M4 Screws -->
    ${[
      [-47, 25], [47, 25],   // Upper top (Y=285 => Y=25 from top)
      [-47, 138], [47, 138], // Upper btm on 40mm crossbar (Y=172 => Y=138 from top, 10mm above seam)
      [-47, 158], [47, 158], // Lower top on 40mm crossbar (Y=152 => Y=158 from top, 10mm below seam)
      [-47, 286], [47, 286]  // Lower btm (Y=24 => Y=286 from top)
    ].map(p => {
      return `<circle cx="${(68 + p[0])*s1}" cy="${p[1]*s1}" r="${4.5*s1/2}" fill="#fbbf24" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <!-- Driver U2 Cutouts at Y=75mm from top (Y=235mm global) -->
    <circle cx="${68*s1}" cy="${75*s1}" r="${96*s1/2}" class="obj-rebate" />
    <circle cx="${68*s1}" cy="${75*s1}" r="${76*s1/2}" class="obj-cutout" />
    <circle cx="${68*s1}" cy="${75*s1}" r="${64*s1/2}" fill="#0f172a" stroke="#475569" stroke-width="1.2" />
    <circle cx="${68*s1}" cy="${75*s1}" r="${22*s1/2}" fill="#334155" stroke="#fbbf24" stroke-width="1" />
    ${centerCross(68*s1, 75*s1, 55*s1)}

    <!-- 2nd External Port P2 Cutouts at Y=233mm from top (Y=77mm global) -->
    <circle cx="${68*s1}" cy="${233*s1}" r="${65*s1/2}" class="obj-rebate" />
    <circle cx="${68*s1}" cy="${233*s1}" r="${53*s1/2}" class="obj-cutout" />
    <circle cx="${68*s1}" cy="${233*s1}" r="${45*s1/2}" fill="#0b0f19" stroke="#38bdf8" stroke-width="1.5" />
    ${centerCross(68*s1, 233*s1, 35*s1)}

    <!-- Dimensions -->
    ${hDim(0, 136*s1, -30, '136.0 mm (W)', -40, 0)}
    ${hDim(12*s1, (136-12)*s1, 325*s1, '112.0 mm (Plate Width)', 310*s1, 335*s1)}
    ${vDim(0, 310*s1, -75, '310.0 mm (H)', 0, -80)}
  </g>
`;

// SIDE SAGITTAL SECTION (5.5L DBR Dual Chamber)
const ox_sec = 410;
const oy_sec = 60;

svg += `
  <g transform="translate(${ox_sec}, ${oy_sec})">
    <text x="${210*s1/2}" y="-15" class="lbl-item" text-anchor="middle">SECTION X-X (5.5L DBR DUAL ACOUSTIC CHAMBERS)</text>
    
    <rect x="0" y="0" width="${210*s1}" height="${310*s1}" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" />
    
    <!-- Top / Bottom Panels -->
    <rect x="0" y="0" width="${210*s1}" height="${12*s1}" fill="url(#hatch-wood)" stroke="#38bdf8" stroke-width="1.5" />
    <rect x="0" y="${(310-12)*s1}" width="${210*s1}" height="${12*s1}" fill="url(#hatch-wood)" stroke="#38bdf8" stroke-width="1.5" />

    <!-- Front 12mm Swappable Plates (Z=4..16mm) -->
    <rect x="${4*s1}" y="${12*s1}" width="${12*s1}" height="${136*s1}" fill="#2e1065" stroke="#fbbf24" stroke-width="1.5" />
    <rect x="${4*s1}" y="${148*s1}" width="${12*s1}" height="${150*s1}" fill="#0c4a6e" stroke="#0284c7" stroke-width="1.5" />

    <!-- Front "日" Ladder Frame (Z=16..28mm) -->
    <rect x="${16*s1}" y="${12*s1}" width="${12*s1}" height="${10*s1}" fill="url(#hatch-wood)" stroke="#fbbf24" stroke-width="1.5" />
    <rect x="${16*s1}" y="${128*s1}" width="${12*s1}" height="${40*s1}" fill="url(#hatch-wood)" stroke="#f43f5e" stroke-width="1.5" />
    <rect x="${16*s1}" y="${288*s1}" width="${12*s1}" height="${10*s1}" fill="url(#hatch-wood)" stroke="#fbbf24" stroke-width="1.5" />

    <!-- 1st Internal DBR Partition Brace (Z=28..182mm at Y=148mm from top => Y=162mm global) -->
    <rect x="${28*s1}" y="${(148-6)*s1}" width="${154*s1}" height="${12*s1}" class="obj-brace" />
    <!-- 1st Internal Port Duct (ID 30mm x L 80mm pointing into Chamber 2) -->
    <rect x="${(28+154/2-18)*s1}" y="${(148+6)*s1}" width="${36*s1}" height="${68*s1}" class="obj-port" />
    <rect x="${(28+154/2-15)*s1}" y="${(148+6)*s1}" width="${30*s1}" height="${68*s1}" fill="#0b0f19" stroke="#38bdf8" stroke-width="1" />
    <text x="${(28+154/2)*s1}" y="${(148+45)*s1}" class="dim-text-sm" fill="#38bdf8">1st Port (Ø30x80)</text>

    <!-- 2nd External Port Tube (45mm Flared Port x 120mm in Chamber 2) -->
    <rect x="${16*s1}" y="${(233-52/2)*s1}" width="${108*s1}" height="${52*s1}" class="obj-port" rx="3" />
    <rect x="${16*s1}" y="${(233-45/2)*s1}" width="${108*s1}" height="${45*s1}" fill="#0b0f19" stroke="#38bdf8" stroke-width="1" />
    <text x="${70*s1}" y="${233*s1 + 4}" class="dim-text-sm" fill="#fbbf24">2nd Port (Ø45x120)</text>

    <!-- Rear "日" Ladder Frame (Z=182..194mm) -->
    <rect x="${182*s1}" y="${12*s1}" width="${12*s1}" height="${10*s1}" fill="url(#hatch-wood)" stroke="#fbbf24" stroke-width="1.5" />
    <rect x="${182*s1}" y="${128*s1}" width="${12*s1}" height="${40*s1}" fill="url(#hatch-wood)" stroke="#f43f5e" stroke-width="1.5" />
    <rect x="${182*s1}" y="${288*s1}" width="${12*s1}" height="${10*s1}" fill="url(#hatch-wood)" stroke="#fbbf24" stroke-width="1.5" />

    <!-- Rear 12mm Solid Blank Plates (Z=194..206mm, NO HOLES) -->
    <rect x="${194*s1}" y="${12*s1}" width="${12*s1}" height="${136*s1}" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5" />
    <rect x="${194*s1}" y="${148*s1}" width="${12*s1}" height="${150*s1}" fill="#1e293b" stroke="#94a3b8" stroke-width="1.5" />

    <!-- Chamber Labels -->
    <text x="${105*s1}" y="${80*s1}" class="lbl-item" fill="#a855f7" text-anchor="middle">CHAMBER 1 (V1 ~ 2.2 L)</text>
    <text x="${140*s1}" y="${260*s1}" class="lbl-item" fill="#0284c7" text-anchor="middle">CHAMBER 2 (V2 ~ 3.25 L)</text>

    <!-- Damping -->
    <rect x="${30*s1}" y="${14*s1}" width="${150*s1}" height="${15*s1}" fill="url(#hatch-damping)" />

    <!-- Dimensions -->
    ${hDim(0, 210*s1, -30, '210.0 mm (D)', -40, 0)}
    ${hDim(4*s1, 28*s1, 325*s1, '24mm Front Baffle', 12*s1, 335*s1)}
    ${hDim(28*s1, 182*s1, 325*s1, '154.0 mm Cavity', (310-12)*s1, 335*s1)}
    ${hDim(182*s1, 206*s1, 325*s1, '24mm Rear Baffle', 12*s1, 335*s1)}
  </g>

  <!-- HIGHLIGHTS -->
  <g transform="translate(760, 80)">
    <text x="0" y="15" class="lbl-subtitle">5.5L DBR ARCHITECTURE HIGHLIGHTS</text>
    <text x="0" y="45" class="lbl-note">• <tspan fill="#38bdf8">Double Bass-Reflex (DBR):</tspan> Chamber 1 ($V_1 \approx 2.2\text{L}$) vents into</text>
    <text x="12" y="65" class="lbl-note">Chamber 2 ($V_2 \approx 3.25\text{L}$) via 1st port (Ø30x80mm), then to room</text>
    <text x="12" y="85" class="lbl-note">via 2nd external port (Ø45x120mm), achieving <tspan fill="#fbbf24">f_L = 42Hz</tspan>.</text>
    <text x="0" y="115" class="lbl-note">• <tspan fill="#f43f5e">100% Common Upper Plates:</tspan> Upper driver baffle (112x136x12mm)</text>
    <text x="12" y="135" class="lbl-note">is 100% interchangeable between 3.2L and 5.5L models!</text>
    <text x="0" y="165" class="lbl-note">• <tspan fill="#a855f7">Expanded Lower Module:</tspan> 112x150x12mm accommodates large</text>
    <text x="12" y="185" class="lbl-note">45mm flared ports, wide slit ducts, or 4-5" passive radiators.</text>
    <text x="0" y="215" class="lbl-note">• <tspan fill="#10b981">Ultra-Rigid DBR Partition:</tspan> Acts as both acoustic port divider</text>
    <text x="12" y="235" class="lbl-note">and structural tie-beam between front and rear 40mm crossbars.</text>
  </g>
</g>
`;

// =============================================================================
// SECTION 2: 5.5L 2D CNC CUTLIST & PANEL SPECIFICATIONS
// =============================================================================
svg += `
<!-- SECTION 2 CONTAINER -->
<g transform="translate(1200, 140)">
  <rect x="0" y="0" width="1350" height="740" class="section-box" />
  <rect x="0" y="0" width="1350" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">2. 5.5L DBR CABINET CNC CUTLIST (12.0mm BIRCH PLYWOOD / MDF)</text>
`;

const s4 = 1.05;

// PANEL 1: 5.5L "日" LADDER INNER FIXED BAFFLE FRAMES (2x)
svg += `
  <g transform="translate(35, 65)">
    <text x="${112*s4/2}" y="-12" class="lbl-item" text-anchor="middle">PANEL 1: 5.5L "日" LADDER FRAMES (2x)</text>
    <text x="${112*s4/2}" y="${286*s4 + 18}" class="lbl-subitem" text-anchor="middle">156 x 273 x 12.0 mm (Z=16..28 &amp; Z=182..194)</text>
    
    <rect x="0" y="0" width="${112*s4}" height="${286*s4}" class="obj-fill" rx="2" />
    
    <!-- Upper Window: 90 x 106mm -->
    <rect x="${(112-90)*s4/2}" y="${10*s4}" width="${90*s4}" height="${106*s4}" rx="${5*s4}" class="obj-cutout" />

    <!-- Center Dividing Crossbar: 112 x 40mm (Y=116..156 from top => Y=142..182 global) -->
    <rect x="0" y="${116*s4}" width="${112*s4}" height="${40*s4}" fill="#334155" stroke="#f43f5e" stroke-width="1.2" opacity="0.4" />

    <!-- Lower Window: 90 x 110mm (Y=166..276 from top => Y=22..132 global) -->
    <rect x="${(112-90)*s4/2}" y="${166*s4}" width="${90*s4}" height="${110*s4}" rx="${5*s4}" class="obj-cutout" />

    <!-- 8x M4 Insert Seats -->
    ${[
      [-47, 13], [47, 13],
      [-47, 126], [47, 126],
      [-47, 146], [47, 146],
      [-47, 274], [47, 274]
    ].map(p => {
      return `<circle cx="${(56 + p[0])*s4}" cy="${p[1]*s4}" r="${5.8*s4/2}" fill="#fbbf24" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <text x="${56*s4}" y="${63*s4}" class="dim-text-sm" fill="#f43f5e">Upper: 90 x 106 mm</text>
    <text x="${56*s4}" y="${136*s4 + 3.5}" class="dim-text-sm" fill="#fbbf24">40mm Crossbar (Y=162)</text>
    <text x="${56*s4}" y="${221*s4}" class="dim-text-sm" fill="#f43f5e">Lower: 90 x 110 mm</text>

    ${hDim(0, 112*s4, -22, '112.0 mm', -25, 0)}
    ${vDim(0, 286*s4, 130*s4, '286.0 mm', 112*s4, 135*s4)}
  </g>
`;

// PANEL 2: TOP / BTM (136x210mm)
svg += `
  <g transform="translate(260, 65)">
    <text x="${136*s4/2}" y="-12" class="lbl-item" text-anchor="middle">PANEL 2: TOP / BTM (2x)</text>
    <text x="${136*s4/2}" y="${210*s4 + 18}" class="lbl-subitem" text-anchor="middle">136 x 210 x 12.0 mm (Dual Chamfers)</text>
    
    <rect x="0" y="0" width="${136*s4}" height="${210*s4}" class="obj-fill" rx="2" />
    <line x1="0" y1="${3*s4}" x2="${136*s4}" y2="${3*s4}" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3" />
    <line x1="0" y1="${(210-3)*s4}" x2="${136*s4}" y2="${(210-3)*s4}" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3" />

    ${hDim(0, 136*s4, -25, '136.0 mm (W)', -30, 0)}
    ${vDim(0, 210*s4, 155*s4, '210.0 mm (D)', 136*s4, 160*s4)}
  </g>
`;

// PANEL 3: SIDES (286x210mm)
svg += `
  <g transform="translate(540, 65)">
    <text x="${210*s4/2}" y="-12" class="lbl-item" text-anchor="middle">PANEL 3: SIDES (2x)</text>
    <text x="${210*s4/2}" y="${286*s4 + 18}" class="lbl-subitem" text-anchor="middle">210 x 286 x 12.0 mm (Dado Z=28..182)</text>
    
    <rect x="0" y="0" width="${210*s4}" height="${286*s4}" class="obj-fill" rx="2" />
    <line x1="${3*s4}" y1="0" x2="${3*s4}" y2="${286*s4}" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3" />
    <line x1="${(210-3)*s4}" y1="0" x2="${(210-3)*s4}" y2="${286*s4}" stroke="#fbbf24" stroke-width="1.2" stroke-dasharray="3,3" />
    <rect x="${28*s4}" y="${(286-162-6)*s4}" width="${154*s4}" height="${12*s4}" fill="#312e81" stroke="#818cf8" stroke-width="1" stroke-dasharray="3,3" />
    <text x="${210*s4/2}" y="${(286-162+3)*s4}" class="dim-text-sm" fill="#c7d2fe">3mm Dado (Z=28..182mm)</text>

    ${hDim(0, 210*s4, -25, '210.0 mm (D)', -30, 0)}
    ${vDim(0, 286*s4, 230*s4, '286.0 mm (H)', 210*s4, 235*s4)}
  </g>
`;

// PANEL 4: INTERNAL DBR PARTITION BRACE (112x154mm)
svg += `
  <g transform="translate(890, 65)">
    <text x="${112*s4/2}" y="-12" class="lbl-item" text-anchor="middle">PANEL 4: DBR PARTITION (1x)</text>
    <text x="${112*s4/2}" y="${154*s4 + 18}" class="lbl-subitem" text-anchor="middle">112 x 154 x 12.0 mm (1st Port Ø30mm)</text>
    
    <rect x="0" y="0" width="${112*s4}" height="${154*s4}" class="obj-brace" rx="2" />
    <circle cx="${56*s4}" cy="${154*s4/2}" r="${36*s4/2}" class="obj-cutout" />
    <circle cx="${56*s4}" cy="${154*s4/2}" r="${30*s4/2}" fill="#0b0f19" stroke="#38bdf8" stroke-width="1.5" />
    ${centerCross(56*s4, 154*s4/2, 25*s4)}

    <text x="${112*s4/2}" y="${154*s4/2 + 28}" class="dim-text-sm" fill="#38bdf8">Ø30 x 80mm Port</text>

    ${hDim(0, 112*s4, -22, '112.0 mm', -25, 0)}
  </g>
</g>
`;

// =============================================================================
// SECTION 3: 5.5L LOWER ACOUSTIC MODULES (112 x 150 x 12 mm)
// =============================================================================
svg += `
<!-- SECTION 3 CONTAINER -->
<g transform="translate(50, 910)">
  <rect x="0" y="0" width="1380" height="780" class="section-box" />
  <rect x="0" y="0" width="1380" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">3. 5.5L LOWER ACOUSTIC MODULES &amp; REAR SOLID (112.0 x 150.0 x 12.0 mm)</text>
`;

const sp5 = 1.15;

// MODULE 5.5L-P1: SEALED / REAR SOLID
svg += `
  <g transform="translate(45, 65)">
    <text x="${112*sp5/2}" y="-10" class="lbl-item" text-anchor="middle">5.5L-P1 / REAR SOLID</text>
    <text x="${112*sp5/2}" y="${150*sp5 + 18}" class="lbl-subitem" text-anchor="middle">Solid 12mm Blank (NO HOLES)</text>
    
    <rect x="0" y="0" width="${112*sp5}" height="${150*sp5}" rx="${4*sp5}" class="obj-plate-p1" />
    
    ${[[-47, -65], [47, -65], [-47, 63], [47, 63]].map(p => {
      return `<circle cx="${(112/2 + p[0])*sp5}" cy="${(150/2 + p[1])*sp5}" r="${4.5*sp5/2}" fill="#94a3b8" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    ${centerCross(112*sp5/2, 150*sp5/2, 35*sp5)}
    <text x="${112*sp5/2}" y="${150*sp5/2 + 4}" class="dim-text-sm" fill="#e2e8f0">SOLID 12mm BLANK</text>
  </g>
`;

// MODULE 5.5L-P2: 45MM FLARED PORT
svg += `
  <g transform="translate(380, 65)">
    <text x="${112*sp5/2}" y="-10" class="lbl-item" text-anchor="middle">5.5L-P2: 45mm FLARED PORT</text>
    <text x="${112*sp5/2}" y="${150*sp5 + 18}" class="lbl-subitem" text-anchor="middle"><tspan fill="#38bdf8">f_L = 42.0 Hz</tspan> (Ø45 x 120mm Port)</text>
    
    <rect x="0" y="0" width="${112*sp5}" height="${150*sp5}" rx="${4*sp5}" class="obj-plate-p2" />
    
    ${[[-47, -65], [47, -65], [-47, 63], [47, 63]].map(p => {
      return `<circle cx="${(112/2 + p[0])*sp5}" cy="${(150/2 + p[1])*sp5}" r="${4.5*sp5/2}" fill="#0284c7" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <circle cx="${112*sp5/2}" cy="${(150/2 + 10)*sp5}" r="${65*sp5/2}" class="obj-rebate" />
    <circle cx="${112*sp5/2}" cy="${(150/2 + 10)*sp5}" r="${53*sp5/2}" class="obj-cutout" />
    <circle cx="${112*sp5/2}" cy="${(150/2 + 10)*sp5}" r="${45*sp5/2}" fill="#0b0f19" stroke="#38bdf8" stroke-width="1.2" />
    ${centerCross(112*sp5/2, (150/2 + 10)*sp5, 35*sp5)}

    <text x="${112*sp5/2}" y="${(150/2 + 10)*sp5 + 4}" class="dim-text-sm" fill="#38bdf8">Ø45mm Socket</text>
  </g>
`;

// MODULE 5.5L-P3: SLIT DUCT
svg += `
  <g transform="translate(715, 65)">
    <text x="${112*sp5/2}" y="-10" class="lbl-item" text-anchor="middle">5.5L-P3: SLIT DUCT</text>
    <text x="${112*sp5/2}" y="${150*sp5 + 18}" class="lbl-subitem" text-anchor="middle"><tspan fill="#10b981">f_L = 44.0 Hz</tspan> (90 x 18 x 130mm)</text>
    
    <rect x="0" y="0" width="${112*sp5}" height="${150*sp5}" rx="${4*sp5}" class="obj-plate-p3" />
    
    ${[[-47, -65], [47, -65], [-47, 63], [47, 63]].map(p => {
      return `<circle cx="${(112/2 + p[0])*sp5}" cy="${(150/2 + p[1])*sp5}" r="${4.5*sp5/2}" fill="#10b981" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <rect x="${(112-90)*sp5/2}" y="${(150/2 + 10 - 9)*sp5}" width="${90*sp5}" height="${18*sp5}" rx="${4*sp5}" class="obj-cutout" />
    ${centerCross(112*sp5/2, (150/2 + 10)*sp5, 35*sp5)}

    <text x="${112*sp5/2}" y="${(150/2 + 10)*sp5 + 4}" class="dim-text-sm" fill="#fbbf24">90 x 18mm Slit</text>
  </g>
`;

// MODULE 5.5L-P4: PASSIVE RADIATOR
svg += `
  <g transform="translate(1050, 65)">
    <text x="${112*sp5/2}" y="-10" class="lbl-item" text-anchor="middle">5.5L-P4: 4-5" PASSIVE RAD</text>
    <text x="${112*sp5/2}" y="${150*sp5 + 18}" class="lbl-subitem" text-anchor="middle"><tspan fill="#c084fc">f_L ~ 36-40 Hz</tspan> (4-5" PR)</text>
    
    <rect x="0" y="0" width="${112*sp5}" height="${150*sp5}" rx="${4*sp5}" class="obj-plate-p4" />
    
    ${[[-47, -65], [47, -65], [-47, 63], [47, 63]].map(p => {
      return `<circle cx="${(112/2 + p[0])*sp5}" cy="${(150/2 + p[1])*sp5}" r="${4.5*sp5/2}" fill="#c084fc" stroke="#000" stroke-width="0.8" />`;
    }).join('\n')}

    <circle cx="${112*sp5/2}" cy="${(150/2 + 10)*sp5}" r="${118*sp5/2}" class="obj-rebate" />
    <circle cx="${112*sp5/2}" cy="${(150/2 + 10)*sp5}" r="${96*sp5/2}" class="obj-cutout" />
    <circle cx="${112*sp5/2}" cy="${(150/2 + 10)*sp5}" r="${72*sp5/2}" fill="#581c87" stroke="#c084fc" stroke-width="1.2" />
    ${centerCross(112*sp5/2, (150/2 + 10)*sp5, 45*sp5)}

    <text x="${112*sp5/2}" y="${(150/2 + 10)*sp5 + 4}" class="dim-text-sm" fill="#e2e8f0">PR Ø96mm</text>
  </g>
</g>
`;

// =============================================================================
// SECTION 4: 5.5L SYSTEM MATRIX & BOM SCHEDULE
// =============================================================================
svg += `
<!-- SECTION 4 CONTAINER -->
<g transform="translate(1460, 910)">
  <rect x="0" y="0" width="1090" height="780" class="section-box" />
  <rect x="0" y="0" width="1090" height="35" class="sec-header" rx="6" />
  <text x="20" y="23" class="lbl-sec">4. 5.5L DBR SYSTEM MATRIX &amp; BOM SCHEDULE</text>

  <g transform="translate(20, 50)">
    <text x="0" y="15" class="lbl-subtitle">A. 5.5L DBR ACOUSTIC TUNING MATRIX</text>
    <rect x="0" y="25" width="1050" height="24" fill="#1e293b" rx="3" />
    <text x="15" y="41" class="table-hdr">DRIVER (UPPER)</text>
    <text x="170" y="41" class="table-hdr">LOWER MODULE</text>
    <text x="325" y="41" class="table-hdr">1ST INTERNAL PORT</text>
    <text x="510" y="41" class="table-hdr">DBR TUNING (f_L / f_H)</text>
    <text x="700" y="41" class="table-hdr">SONIC CHARACTER / BASS EXTENSION</text>
  </g>
`;

const dbrRows = [
  { up: 'Plate U2 (3" ND91)', low: '5.5L-P2 (45mm Port)', p1: 'Ø30 x 80mm', fb: '42.0 Hz / 95.0 Hz', note: 'Massive linear sub-bass extension down to 38Hz' },
  { up: 'Plate U2 (3" W3-881)', low: '5.5L-P3 (Slit Duct)', p1: 'Ø30 x 80mm', fb: '44.0 Hz / 98.0 Hz', note: 'Fast bass transient speed with zero chuffing' },
  { up: 'Plate U3 (4" TCP115)', low: '5.5L-P2 (45mm Port)', p1: 'Ø30 x 80mm', fb: '39.5 Hz / 92.0 Hz', note: 'Room-filling subwoofer-like desktop bass output' },
  { up: 'Plate U3 (4" W4-1337)', low: '5.5L-P4 (Passive Rad)', p1: 'Ø30 x 80mm', fb: '36.0 Hz / 88.0 Hz', note: 'Ultra-deep bass, zero pipe resonance / noise' },
  { up: 'Plate U1 (2.5" ND65)', low: '5.5L-P2 (45mm Port)', p1: 'Ø30 x 80mm', fb: '48.0 Hz / 105.0 Hz', note: 'Astonishing deep bass from micro 2.5" cone' },
];

dbrRows.forEach((r, idx) => {
  const y = 120 + idx * 28;
  const bg = idx % 2 === 0 ? 'table-cell-bg' : 'table-cell-alt';
  svg += `
  <g transform="translate(20, ${y})">
    <rect x="0" y="0" width="1050" height="25" class="${bg}" rx="3" />
    <text x="15" y="17" class="table-row" fill="#fbbf24">${r.up}</text>
    <text x="170" y="17" class="table-row" fill="#38bdf8">${r.low}</text>
    <text x="325" y="17" class="table-row" fill="#cbd5e1">${r.p1}</text>
    <text x="510" y="17" class="table-row" fill="#a855f7" font-weight="700">${r.fb}</text>
    <text x="700" y="17" class="table-row" fill="#f8fafc" font-size="9.5px">${r.note}</text>
  </g>
  `;
});

// BOM TABLE
svg += `
  <g transform="translate(20, 300)">
    <text x="0" y="15" class="lbl-subtitle">B. 5.5L DBR SYSTEM BOM SCHEDULE</text>
    <rect x="0" y="25" width="1050" height="24" fill="#1e293b" rx="3" />
    <text x="15" y="41" class="table-hdr">PART ID</text>
    <text x="95" y="41" class="table-hdr">COMPONENT</text>
    <text x="240" y="41" class="table-hdr">QTY</text>
    <text x="290" y="41" class="table-hdr">SPECIFICATION / MATERIAL</text>
    <text x="660" y="41" class="table-hdr">FUNCTION &amp; MOUNTING</text>
  </g>
`;

const dbrBom = [
  { id: 'PAN-55L-TOP', name: 'Top / Bottom Panels', qty: '2', spec: '136 x 210 x 12.0mm (Birch Plywood / MDF)', fn: 'Continuous outer wrapper (210mm depth)' },
  { id: 'PAN-55L-SIDES', name: 'Left / Right Sides', qty: '2', spec: '210 x 286 x 12.0mm (Birch Plywood / MDF)', fn: 'Side walls with 154mm DBR dado at Y=162mm' },
  { id: 'PAN-55L-FRAME', name: '5.5L "日" Frames', qty: '2', spec: '156 x 273 x 12.0mm (40mm Crossbar at Y=162)', fn: 'Front & rear symmetrical ladder frames' },
  { id: 'PAN-55L-DBR', name: 'DBR Partition Brace', qty: '1', spec: '112 x 154 x 12.0mm + ID 30x80mm pipe', fn: 'Ties front/rear bars, houses 1st port' },
  { id: 'MOD-U1..U4', name: '12mm Upper Plates', qty: '4', spec: '112 x 136 x 12.0mm (100% COMMON w/ 3.2L)', fn: 'Common swappable driver sub-baffles' },
  { id: 'MOD-55L-P1..P4', name: '5.5L Lower Modules', qty: '4', spec: '112 x 150 x 12.0mm (Sealed, Port, Slit, PR)', fn: 'Expanded 5.5L acoustic sub-baffles' },
  { id: 'MOD-55L-REAR-U', name: 'Rear Upper Solid', qty: '1', spec: '112 x 136 x 12.0mm (Solid Blank, NO HOLES)', fn: 'Rear upper chamber sealing' },
  { id: 'MOD-55L-REAR-P', name: 'Rear Lower Solid', qty: '1', spec: '112 x 150 x 12.0mm (Solid Blank, NO HOLES)', fn: 'Rear lower chamber sealing' },
  { id: 'GSK-55L-EVA', name: '5.5L Dual Gaskets', qty: '4 Sets', spec: '156 x 273 x 1.5mm Dual-Window EVA', fn: 'Front & rear airtight hermetic sealing' },
  { id: 'FST-M4IN', name: 'M4 Brass Inserts', qty: '16', spec: 'M4 x 8.0mm Heat-Set Brass Inserts', fn: '8 front inserts + 8 rear inserts' },
  { id: 'FST-M4SC', name: 'M4 Screws', qty: '16', spec: 'M4 x 20mm Countersunk Socket Screws', fn: '8 front screws + 8 rear screws' },
];

dbrBom.forEach((r, idx) => {
  const y = 365 + idx * 29;
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

const outputPath = path.join(__dirname, '..', 'cad', 'cutlist_drawings_5.5L.svg');
fs.writeFileSync(outputPath, svg, 'utf8');
console.log('Successfully generated 5.5L DBR cutlist_drawings_5.5L.svg at:', outputPath);
