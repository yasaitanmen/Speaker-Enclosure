# 02. Modular Speaker Enclosure Technical Specifications (3.2L & 5.5L DBR)

**Project:** Universal Modular Speaker Development Platform (2" to 4" Drivers)  
**Document ID:** SPK-MOD-035-DOC-02  
**Revision:** 10.0 (Unified 3.2L Compact & 5.5L Deep-Bass DBR Symmetrical Platforms)  
**Date:** 2026-08-29  
**Target Category:** Nearfield Monitoring & Extended Deep-Bass Development  
**3.2L FreeCAD Script:** [`cad/build_freecad_model.py`](file:///c:/Users/haman/Speaker/cad/build_freecad_model.py) | **FCStd:** [`cad/speaker_enclosure.FCStd`](file:///c:/Users/haman/Speaker/cad/speaker_enclosure.FCStd) | **STEP:** [`cad/speaker_enclosure.step`](file:///c:/Users/haman/Speaker/cad/speaker_enclosure.step) | **2D Cutlist:** [`cad/cutlist_drawings.svg`](file:///c:/Users/haman/Speaker/cad/cutlist_drawings.svg)  
**5.5L DBR FreeCAD Script:** [`cad/build_freecad_model_5.5L.py`](file:///c:/Users/haman/Speaker/cad/build_freecad_model_5.5L.py) | **FCStd:** [`cad/speaker_enclosure_5.5L.FCStd`](file:///c:/Users/haman/Speaker/cad/speaker_enclosure_5.5L.FCStd) | **STEP:** [`cad/speaker_enclosure_5.5L.step`](file:///c:/Users/haman/Speaker/cad/speaker_enclosure_5.5L.step) | **2D Cutlist:** [`cad/cutlist_drawings_5.5L.svg`](file:///c:/Users/haman/Speaker/cad/cutlist_drawings_5.5L.svg)  

---

## 1. System Architecture Overview

The platform features two modular enclosure architectures that share **100% interchangeable Upper Driver Baffle Plates (Plates U1, U2, U3, U4)**:

| Specification | Model A: 3.2L Compact Reference | Model B: 5.5L Deep-Bass DBR |
| :--- | :--- | :--- |
| **Primary Target** | Desktop Nearfield Reference Monitor | Extended Deep-Bass & High-SPL Desktop Sub/Sat |
| **Outer Box Dimensions** | $136\text{ mm (W)} \times 230\text{ mm (H)} \times 190\text{ mm (D)}$ | $136\text{ mm (W)} \times 310\text{ mm (H)} \times 210\text{ mm (D)}$ |
| **Gross Enclosure Volume** | $3.41\text{ Liters}$ | $5.90\text{ Liters}$ |
| **Net Working Volume ($V_b$)**| $3.02 - 3.15\text{ Liters}$ ($V_{eff} \approx 3.4\text{ L}$) | $5.45\text{ Liters}$ ($V_1 = 2.2\text{ L}, V_2 = 3.25\text{ L}$) |
| **Acoustic Topology** | Sealed, Single Bass-Reflex, Slit, PR | **Double Bass-Reflex (DBR)**, Sealed, Slit, PR |
| **Bass Extension ($F_b$ / $f_L$)**| $F_b = 64.5 - 72.5\text{ Hz}$ ($F_3 \approx 58\text{ Hz}$) | $f_L = 39.5 - 44.0\text{ Hz}, f_H = 92 - 98\text{ Hz}$ ($F_3 \approx 38\text{ Hz}$) |
| **Internal Bracing** | Tie-Beam Window Brace ($112 \times 12 \times 134\text{ mm}$) | DBR Partition Brace ($112 \times 12 \times 154\text{ mm}$ + $\varnothing 30\text{x}80\text{mm}$ port) |
| **Upper Driver Plate** | **$112 \times 136 \times 12\text{ mm}$ (100% COMMON)** | **$112 \times 136 \times 12\text{ mm}$ (100% COMMON)** |
| **Lower Acoustic Module** | $112 \times 70 \times 12\text{ mm}$ | $112 \times 150 \times 12\text{ mm}$ (Expanded 45mm Flared Port) |
| **Front & Rear Symmetry** | Symmetrical "日" Ladder Frames ($Z=16..28$ & $162..174$) | Symmetrical "日" Ladder Frames ($Z=16..28$ & $182..194$) |

---

## 2. 5.5L Deep-Bass Double Bass-Reflex (DBR) Mechanical Details

```
+-----------------------------------------------------------------------------+
|              5.5L DEEP-BASS DOUBLE BASS-REFLEX (DBR) SCHEMATIC              |
+-----------------------------------------------------------------------------+
|                                                                             |
|      +---------------------------------------------------------------+      |
|      |               TOP PANEL (136 x 210 mm Full Depth)             |      |
|      +---------------------------------------------------------------+      |
|      | [4mm Recess]                                     [4mm Recess] |      |
|      |  +---------------------------+       +---------------------+  |      |
|      |  | FRONT UPPER (112x136x12)  |       | REAR UPPER SOLID    |  |      |
|      |  | [Upper Window: 90x106mm]  |       | (112x136x12 mm)     |  |      |
|      |  | (CHAMBER 1: V1 ~ 2.2 L)   |       | [NO HOLES]          |  |      |
|      |  +===========================+ <===> +=====================+  |      |
|      |  | 40mm FRONT CROSSBAR       | DBR   | 40mm REAR CROSSBAR  |  |      |
|      |  | (Y=142..182mm, c=162)     | TIE   | (Y=142..182mm, c=162|  |      |
|      |  | (Z = 16 to 28 mm)         | BRACE | (Z = 182 to 194 mm) |  |      |
|      |  |                           | [1st  |                     |  |      |
|      |  |                           | Port: |                     |  |      |
|      |  |                           | Ø30x80|                     |  |      |
|      |  +===========================+  mm]  +=====================+  |      |
|      |  | FRONT LOWER (112x150x12)  |       | REAR LOWER SOLID    |  |      |
|      |  | [Lower Window: 90x110mm]  |       | (112x150x12 mm)     |  |      |
|      |  | [2nd Port: Ø45x120 mm]    |       | [NO HOLES]          |  |      |
|      |  | (CHAMBER 2: V2 ~ 3.25 L)  |       |                     |  |      |
|      |  +---------------------------+       +---------------------+  |      |
|      +---------------------------------------------------------------+      |
|      |             BOTTOM PANEL (136 x 210 mm Full Depth)            |      |
|      +---------------------------------------------------------------+      |
|                                                                             |
+-----------------------------------------------------------------------------+
```

### 2.1 Symmetrical "日" Ladder Inner Frame ($112.0 \times 286.0 \times 12.0\text{ mm}$)
- **Upper Window Opening:** $90.0\text{ mm (W)} \times 106.0\text{ mm (H)}$ ($Y_{global} = 182.0\text{ mm}$ to $288.0\text{ mm}$, center $Y = 235.0\text{ mm}$).
- **Center 40mm Dividing Crossbar:** $112.0\text{ mm (W)} \times 40.0\text{ mm (H)}$ ($Y_{global} = 142.0\text{ mm}$ to $182.0\text{ mm}$, centered at split seam $Y = 162.0\text{ mm}$).
- **Lower Window Opening:** $90.0\text{ mm (W)} \times 110.0\text{ mm (H)}$ ($Y_{global} = 22.0\text{ mm}$ to $132.0\text{ mm}$, center $Y = 77.0\text{ mm}$).
- **Fastener Pattern (8x M4 Nut Seats):**
  - Upper Plate: $(X = 68 \pm 47.0\text{ mm}, Y_{global} = 285.0\text{ mm} \text{ and } 172.0\text{ mm})$ — **100% identical to 3.2L plate**.
  - Lower Plate: $(X = 68 \pm 47.0\text{ mm}, Y_{global} = 152.0\text{ mm} \text{ and } 24.0\text{ mm})$.

---

### 2.2 5.5L Swappable Lower Acoustic Modules ($112.0 \times 150.0 \times 12.0\text{ mm}$)
- **Module 5.5L-P1 (Sealed / Blank):** Solid blank plate (**NO HOLES**).
- **Module 5.5L-P2 (2nd External Bass-Reflex Port):** Central socket $\varnothing 53.0\text{ mm}$ cutout, $\varnothing 65.0 \times 3.0\text{ mm}$ rebate for $\varnothing 45.0\text{ mm}$ flared port tube ($L = 120.0\text{ mm}$), yielding $f_L = 42.0\text{ Hz}$ / $f_H = 95.0\text{ Hz}$.
- **Module 5.5L-P3 (Slit Duct Port):** $90.0 \times 18.0\text{ mm}$ slit opening ($S_v = 16.2\text{ cm}^2$) with $130.0\text{ mm}$ duct housing, yielding $f_L = 44.0\text{ Hz}$.
- **Module 5.5L-P4 (4"–5" Passive Radiator):** Cutout $\varnothing 96.0\text{ mm}$, rebate $\varnothing 118.0 \times 4.0\text{ mm}$ for 4"–5" PR ($f_L \approx 36 - 40\text{ Hz}$).

---

## 3. Production Bill of Materials (BOM)

### 3.1 5.5L DBR Cabinet Panels (12.0 mm Baltic Birch / MDF)

| ID | Panel Name | Qty | Dimensions | Machining Specifications |
| :--- | :--- | :---: | :--- | :--- |
| **PAN-55L-TOP** | **Top / Bottom Panels** | 2 | $136 \times 12 \times 210\text{ mm}$ | Full depth wrapper with dual $3.0\text{ mm} \times 45^\circ$ front & rear chamfers. |
| **PAN-55L-SIDES**| **Left / Right Sides** | 2 | $12 \times 286 \times 210\text{ mm}$ | Side walls with dual chamfers and $154\text{ mm}$ DBR dado at $Y = 162.0\text{ mm}$ ($Z = 28..182\text{ mm}$). |
| **PAN-55L-FRAME**| **5.5L "日" Frames** | 2 | $112 \times 286 \times 12\text{ mm}$ | Front ($Z=16..28$) & Rear ($Z=182..194$) frames with 40mm center crossbars. |
| **PAN-55L-DBR** | **DBR Partition Brace** | 1 | $112 \times 12 \times 154\text{ mm}$ | Houses 1st internal port pipe ($\varnothing 30\text{ mm} \times 80\text{ mm}$), links front & rear bars. |
| **MOD-U1..U4** | **12mm Upper Plates** | 4 | $112 \times 136 \times 12\text{ mm}$ | **100% COMMON with 3.2L model** (Plates U1, U2, U3, U4). |
| **MOD-55L-P1..P4**| **5.5L Lower Modules** | 4 | $112 \times 150 \times 12\text{ mm}$ | 5.5L DBR Modules (Sealed, 45mm Port, Slit, 4-5" PR). |
| **MOD-55L-REAR**| **Rear Solid Blanks** | 2 | $112 \times 136$ & $112 \times 150\text{ mm}$ | Upper & Lower Solid Blank plates (**NO HOLES**). |
| **GSK-55L-EVA** | **5.5L Dual Gaskets** | 4 Sets| $112 \times 286 \times 1.5\text{ mm}$ | Dual-Window EVA Foam gaskets. |
| **FST-M4IN** | **M4 Brass Inserts** | 16 | M4 $\times 8.0\text{ mm}$ | 8 Front Inserts + 8 Rear Inserts. |
| **FST-M4SC** | **M4 Screws** | 16 | M4 $\times 20.0\text{ mm}$ | 8 Front Screws + 8 Rear Screws. |

---

## 4. Production Files Summary

### 3.2L Compact Model:
- **FreeCAD Script:** [`cad/build_freecad_model.py`](file:///c:/Users/haman/Speaker/cad/build_freecad_model.py)
- **Native FCStd Project:** [`cad/speaker_enclosure.FCStd`](file:///c:/Users/haman/Speaker/cad/speaker_enclosure.FCStd)
- **STEP 3D CAD:** [`cad/speaker_enclosure.step`](file:///c:/Users/haman/Speaker/cad/speaker_enclosure.step)
- **2D Cutlist SVG:** [`cad/cutlist_drawings.svg`](file:///c:/Users/haman/Speaker/cad/cutlist_drawings.svg)
- **STLs:** [`cad/stl/`](file:///c:/Users/haman/Speaker/cad/stl/)

### 5.5L Deep-Bass DBR Model:
- **FreeCAD Script:** [`cad/build_freecad_model_5.5L.py`](file:///c:/Users/haman/Speaker/cad/build_freecad_model_5.5L.py)
- **Native FCStd Project:** [`cad/speaker_enclosure_5.5L.FCStd`](file:///c:/Users/haman/Speaker/cad/speaker_enclosure_5.5L.FCStd)
- **STEP 3D CAD:** [`cad/speaker_enclosure_5.5L.step`](file:///c:/Users/haman/Speaker/cad/speaker_enclosure_5.5L.step)
- **2D Cutlist SVG:** [`cad/cutlist_drawings_5.5L.svg`](file:///c:/Users/haman/Speaker/cad/cutlist_drawings_5.5L.svg) (via [`cad/generate_svg_5.5L.js`](file:///c:/Users/haman/Speaker/cad/generate_svg_5.5L.js))
- **STLs:** [`cad/stl/5.5L/`](file:///c:/Users/haman/Speaker/cad/stl/5.5L/)
