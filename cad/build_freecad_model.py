#!/usr/bin/env python3
# =============================================================================
# FREECAD 3D SOLID AUTOMATION - SYMMETRICAL DUAL-FACE "日" LADDER FRAME ARCHITECTURE
# Project: Symmetrical Dual-Face Reference Desktop Speaker (2" to 4" Drivers)
# File: cad/build_freecad_model.py
# Description: Generates full 3D solid parametric models using FreeCAD's native
#              Python API (FreeCAD, Part, Mesh) for:
#              - Front & Rear Symmetrical Architecture:
#                * Front "日" Inner Frame: 112x206x12mm at Z=16..28mm (40mm crossbar at Y=62..102mm)
#                * Rear "日" Inner Frame: 112x206x12mm at Z=162..174mm (40mm crossbar at Y=62..102mm)
#                * Internal Window Brace: 112x12x134mm at Y=82mm spanning Z=28..162mm, directly linking
#                  front and rear 40mm crossbars.
#                * Front Baffles (Z=4..16mm): Upper U1..U4 (112x136x12mm) + Lower P1..P4 (112x70x12mm)
#                * Rear Baffles (Z=174..186mm): Upper Solid Blank (112x136x12mm, NO HOLES) +
#                  Lower Solid Blank (112x70x12mm, NO HOLES)
#                * Outer Box Panels (136x12x190mm Top/Btm, 12x206x190mm Sides)
#              Exports:
#              - Native FreeCAD project: cad/speaker_enclosure.FCStd
#              - STEP 3D CAD interchange: cad/speaker_enclosure.step
#              - Production STLs in cad/stl/ for 3D printing and CNC milling.
# =============================================================================

import os
import sys
import math
import FreeCAD
import Part
import Mesh

print("=================================================================")
print("STARTING FREECAD SYMMETRICAL DUAL-FACE '日' FRAME 3D GENERATION")
print("FreeCAD Version:", ".".join(FreeCAD.Version()[:3]))
print("=================================================================")

# Output Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STL_DIR = os.path.join(SCRIPT_DIR, "stl")
os.makedirs(STL_DIR, exist_ok=True)

FCSTD_PATH = os.path.join(SCRIPT_DIR, "speaker_enclosure.FCStd")
STEP_PATH = os.path.join(SCRIPT_DIR, "speaker_enclosure.step")

# =============================================================================
# GEOMETRIC UTILITY FUNCTIONS
# =============================================================================

def make_rounded_rect_face(w, h, r, z_pos=0.0):
    """Creates a 2D rounded rectangular face in the XY plane at z_pos."""
    p1 = FreeCAD.Vector(-w/2 + r, -h/2, z_pos)
    p2 = FreeCAD.Vector(w/2 - r, -h/2, z_pos)
    p3 = FreeCAD.Vector(w/2, -h/2 + r, z_pos)
    p4 = FreeCAD.Vector(w/2, h/2 - r, z_pos)
    p5 = FreeCAD.Vector(w/2 - r, h/2, z_pos)
    p6 = FreeCAD.Vector(-w/2 + r, h/2, z_pos)
    p7 = FreeCAD.Vector(-w/2, h/2 - r, z_pos)
    p8 = FreeCAD.Vector(-w/2, -h/2 + r, z_pos)

    e1 = Part.makeLine(p1, p2)
    e2 = Part.Edge(Part.Arc(p2, FreeCAD.Vector(w/2 - r + r*math.cos(-math.pi/4), -h/2 + r + r*math.sin(-math.pi/4), z_pos), p3))
    e3 = Part.makeLine(p3, p4)
    e4 = Part.Edge(Part.Arc(p4, FreeCAD.Vector(w/2 - r + r*math.cos(math.pi/4), h/2 - r + r*math.sin(math.pi/4), z_pos), p5))
    e5 = Part.makeLine(p5, p6)
    e6 = Part.Edge(Part.Arc(p6, FreeCAD.Vector(-w/2 + r + r*math.cos(3*math.pi/4), h/2 - r + r*math.sin(3*math.pi/4), z_pos), p7))
    e7 = Part.makeLine(p7, p8)
    e8 = Part.Edge(Part.Arc(p8, FreeCAD.Vector(-w/2 + r + r*math.cos(-3*math.pi/4), -h/2 + r + r*math.sin(-3*math.pi/4), z_pos), p1))

    wire = Part.Wire([e1, e2, e3, e4, e5, e6, e7, e8])
    return Part.Face(wire)

def make_rounded_rect_solid(w, h, r, depth, z_start=0.0):
    """Creates a 3D solid rounded rectangular prism extruded along +Z."""
    face = make_rounded_rect_face(w, h, r, z_start)
    return face.extrude(FreeCAD.Vector(0, 0, depth))

def make_hybrid_split_plate_face(w, h, r_top, r_btm, z_pos=0.0):
    """Creates a 2D rectangular face with distinct top and bottom corner radii."""
    p1 = FreeCAD.Vector(-w/2 + r_btm, -h/2, z_pos)
    p2 = FreeCAD.Vector(w/2 - r_btm, -h/2, z_pos)
    p3 = FreeCAD.Vector(w/2, -h/2 + r_btm, z_pos)
    p4 = FreeCAD.Vector(w/2, h/2 - r_top, z_pos)
    p5 = FreeCAD.Vector(w/2 - r_top, h/2, z_pos)
    p6 = FreeCAD.Vector(-w/2 + r_top, h/2, z_pos)
    p7 = FreeCAD.Vector(-w/2, h/2 - r_top, z_pos)
    p8 = FreeCAD.Vector(-w/2, -h/2 + r_btm, z_pos)

    e1 = Part.makeLine(p1, p2)
    if r_btm > 0.1:
        e2 = Part.Edge(Part.Arc(p2, FreeCAD.Vector(w/2 - r_btm + r_btm*math.cos(-math.pi/4), -h/2 + r_btm + r_btm*math.sin(-math.pi/4), z_pos), p3))
    else:
        e2 = Part.makeLine(p2, p3)
    e3 = Part.makeLine(p3, p4)
    if r_top > 0.1:
        e4 = Part.Edge(Part.Arc(p4, FreeCAD.Vector(w/2 - r_top + r_top*math.cos(math.pi/4), h/2 - r_top + r_top*math.sin(math.pi/4), z_pos), p5))
    else:
        e4 = Part.makeLine(p4, p5)
    e5 = Part.makeLine(p5, p6)
    if r_top > 0.1:
        e6 = Part.Edge(Part.Arc(p6, FreeCAD.Vector(-w/2 + r_top + r_top*math.cos(3*math.pi/4), h/2 - r_top + r_top*math.sin(3*math.pi/4), z_pos), p7))
    else:
        e6 = Part.makeLine(p6, p7)
    e7 = Part.makeLine(p7, p8)
    if r_btm > 0.1:
        e8 = Part.Edge(Part.Arc(p8, FreeCAD.Vector(-w/2 + r_btm + r_btm*math.cos(-3*math.pi/4), -h/2 + r_btm + r_btm*math.sin(-3*math.pi/4), z_pos), p1))
    else:
        e8 = Part.makeLine(p8, p1)

    wire = Part.Wire([e1, e2, e3, e4, e5, e6, e7, e8])
    return Part.Face(wire)

def export_mesh_stl(shape, filepath, deflection=0.04):
    """Tessellates a FreeCAD solid shape and exports as binary STL."""
    mesh = Mesh.Mesh(shape.tessellate(deflection))
    mesh.write(filepath)
    print(f"Exported STL: {os.path.basename(filepath)} ({os.path.getsize(filepath):,} bytes)")

# =============================================================================
# MODEL INITIALIZATION & PARAMETERS
# =============================================================================

doc = FreeCAD.newDocument("SpeakerEnclosure_Symmetrical_DualFace_Ladder")

# Outer Cabinet Dimensions (mm)
W_OUT = 136.0
H_OUT = 230.0
D_OUT = 190.0
T_PANEL = 12.0

# Inner Dimensions (mm)
W_IN = W_OUT - 2 * T_PANEL  # 112.0 mm
H_IN = H_OUT - 2 * T_PANEL  # 206.0 mm

# Symmetrical Dual-Face Z Positions (mm)
# Front:
FRONT_RECESS         = 4.0                     # Z=0..4mm
Z_FRONT_SWAP_START   = 4.0                     # Z=4mm
Z_FRONT_SWAP_END     = 16.0                    # Z=16mm (12mm thick)
Z_FRONT_FRAME_START  = 16.0                    # Z=16mm
Z_FRONT_FRAME_END    = 28.0                    # Z=28mm (12mm thick)

# Cavity & Brace:
Z_CAVITY_START       = 28.0                    # Z=28mm
Z_CAVITY_END         = 162.0                   # Z=162mm
D_INTERNAL_CAVITY    = Z_CAVITY_END - Z_CAVITY_START  # 134.0 mm

# Rear:
Z_REAR_FRAME_START   = 162.0                   # Z=162mm
Z_REAR_FRAME_END     = 174.0                   # Z=174mm (12mm thick)
Z_REAR_SWAP_START    = 174.0                   # Z=174mm
Z_REAR_SWAP_END      = 186.0                   # Z=186mm (12mm thick)
REAR_RECESS          = 4.0                     # Z=186..190mm

# "日" Wide 56mm Ladder Frame Parameters (mm)
UPPER_WIN_W   = 84.0
UPPER_WIN_H   = 96.0
UPPER_WIN_Y   = 158.0   # Spans Y=110.0 to Y=206.0 (Center Y=158.0)
UPPER_WIN_R   = 5.0

CROSSBAR_W    = 112.0
CROSSBAR_H    = 56.0    # Spans Y=54.0 to Y=110.0 (Center Y=82.0, providing 28mm solid meat above and below seam)

LOWER_WIN_W   = 84.0
LOWER_WIN_H   = 30.0
LOWER_WIN_Y   = 39.0    # Spans Y=24.0 to Y=54.0 (Center Y=39.0)
LOWER_WIN_R   = 5.0

SPLIT_JOINT_Y = 82.0    # Horizontal split line (Center of 56mm Crossbar)

# Swappable Upper Driver Plate (112 x 136 x 12mm)
UPPER_PLATE_W = 112.0
UPPER_PLATE_H = 136.0
UPPER_PLATE_T = 12.0
UPPER_POS_Y   = 150.0   # Spans Y=82.0 to Y=218.0 (Center Y=150.0)
DRIVER_POS_Y  = 155.0   # Acoustic driver center

# Swappable Lower Acoustic Module (112 x 70 x 12mm)
LOWER_PLATE_W = 112.0
LOWER_PLATE_H = 70.0
LOWER_PLATE_T = 12.0
LOWER_POS_Y   = 47.0    # Spans Y=12.0 to Y=82.0 (Center Y=47.0)
ACOUSTIC_POS_Y= 47.0    # Acoustic center

GASKET_THICK  = 1.5

# 8x M4 Insert Nut Coordinates (Global X, Y on Inner Frame)
# Upper Plate: Top (Y=205), Bottom on Crossbar (Y=96, 14mm above seam on 56mm crossbar)
# Lower Plate: Top on Crossbar (Y=68, 14mm below seam on 56mm crossbar), Bottom (Y=24)
NUT_COORDS = [
    (-42.0, 205.0), (42.0, 205.0),
    (-42.0, 96.0),  (42.0, 96.0),
    (-42.0, 68.0),  (42.0, 68.0),
    (-42.0, 24.0),  (42.0, 24.0)
]

# -----------------------------------------------------------------------------
# 1. OUTER CABINET PANELS (FULL DEPTH 190mm)
# -----------------------------------------------------------------------------
print("\nModeling Outer Cabinet Panels (190mm Full Depth with Front & Rear Chamfers)...")

# Top Panel (136 x 12 x 190mm)
top_panel = Part.makeBox(W_OUT, T_PANEL, D_OUT, FreeCAD.Vector(0, H_OUT - T_PANEL, 0))
top_chamfer_front = Part.makeBox(W_OUT + 10, 10, 10, FreeCAD.Vector(-5, H_OUT - 3, -7))
top_chamfer_front.rotate(FreeCAD.Vector(0, H_OUT, 0), FreeCAD.Vector(1, 0, 0), -45)
top_chamfer_rear = Part.makeBox(W_OUT + 10, 10, 10, FreeCAD.Vector(-5, H_OUT - 3, D_OUT - 3))
top_chamfer_rear.rotate(FreeCAD.Vector(0, H_OUT, D_OUT), FreeCAD.Vector(1, 0, 0), 45)
top_panel = top_panel.cut(top_chamfer_front).cut(top_chamfer_rear)
obj_top = doc.addObject("Part::Feature", "Top_Panel")
obj_top.Shape = top_panel
obj_top.Label = "Top Panel (136x12x190mm)"

# Bottom Panel (136 x 12 x 190mm)
btm_panel = Part.makeBox(W_OUT, T_PANEL, D_OUT, FreeCAD.Vector(0, 0, 0))
btm_chamfer_front = Part.makeBox(W_OUT + 10, 10, 10, FreeCAD.Vector(-5, -7, -7))
btm_chamfer_front.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 45)
btm_chamfer_rear = Part.makeBox(W_OUT + 10, 10, 10, FreeCAD.Vector(-5, -7, D_OUT - 3))
btm_chamfer_rear.rotate(FreeCAD.Vector(0, 0, D_OUT), FreeCAD.Vector(1, 0, 0), -45)
btm_panel = btm_panel.cut(btm_chamfer_front).cut(btm_chamfer_rear)
obj_btm = doc.addObject("Part::Feature", "Bottom_Panel")
obj_btm.Shape = btm_panel
obj_btm.Label = "Bottom Panel (136x12x190mm)"

# Left Side Panel (12 x 206 x 190mm)
left_side = Part.makeBox(T_PANEL, H_IN, D_OUT, FreeCAD.Vector(0, T_PANEL, 0))
left_chamfer_front = Part.makeBox(10, H_OUT + 10, 10, FreeCAD.Vector(-7, -5, -7))
left_chamfer_front.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 45)
left_chamfer_rear = Part.makeBox(10, H_OUT + 10, 10, FreeCAD.Vector(-7, -5, D_OUT - 3))
left_chamfer_rear.rotate(FreeCAD.Vector(0, 0, D_OUT), FreeCAD.Vector(0, 1, 0), -45)
# Dado for Window Brace (3mm deep x 12mm high at Y=82mm from Z=28 to Z=162)
left_dado = Part.makeBox(3.0, 12.0, D_INTERNAL_CAVITY, FreeCAD.Vector(T_PANEL - 3.0, SPLIT_JOINT_Y - 6.0, Z_CAVITY_START))
left_side = left_side.cut(left_chamfer_front).cut(left_chamfer_rear).cut(left_dado)
obj_left = doc.addObject("Part::Feature", "Left_Side_Panel")
obj_left.Shape = left_side
obj_left.Label = "Left Side Panel (12x206x190mm)"

# Right Side Panel (12 x 206 x 190mm)
right_side = Part.makeBox(T_PANEL, H_IN, D_OUT, FreeCAD.Vector(W_OUT - T_PANEL, T_PANEL, 0))
right_chamfer_front = Part.makeBox(10, H_OUT + 10, 10, FreeCAD.Vector(W_OUT - 3, -5, -7))
right_chamfer_front.rotate(FreeCAD.Vector(W_OUT, 0, 0), FreeCAD.Vector(0, 1, 0), -45)
right_chamfer_rear = Part.makeBox(10, H_OUT + 10, 10, FreeCAD.Vector(W_OUT - 3, -5, D_OUT - 3))
right_chamfer_rear.rotate(FreeCAD.Vector(W_OUT, 0, D_OUT), FreeCAD.Vector(0, 1, 0), 45)
right_dado = Part.makeBox(3.0, 12.0, D_INTERNAL_CAVITY, FreeCAD.Vector(W_OUT - T_PANEL, SPLIT_JOINT_Y - 6.0, Z_CAVITY_START))
right_side = right_side.cut(right_chamfer_front).cut(right_chamfer_rear).cut(right_dado)
obj_right = doc.addObject("Part::Feature", "Right_Side_Panel")
obj_right.Shape = right_side
obj_right.Label = "Right Side Panel (12x206x190mm)"

# -----------------------------------------------------------------------------
# 2. "日" LADDER INNER FIXED BAFFLE FRAMES (FRONT Z=16..28 & REAR Z=162..174)
# -----------------------------------------------------------------------------
print("\nModeling Symmetrical '日' Ladder Inner Frames (Front Z=16..28mm & Rear Z=162..174mm)...")

def make_ladder_frame(z_start, insert_dir=1):
    frame_blank = Part.makeBox(W_IN, H_IN, T_PANEL, FreeCAD.Vector(T_PANEL, T_PANEL, z_start))
    upper_win_cut = make_rounded_rect_solid(UPPER_WIN_W, UPPER_WIN_H, UPPER_WIN_R, T_PANEL + 2.0, z_start=z_start - 1.0)
    upper_win_cut.translate(FreeCAD.Vector(W_OUT/2, UPPER_WIN_Y, 0))
    lower_win_cut = make_rounded_rect_solid(LOWER_WIN_W, LOWER_WIN_H, LOWER_WIN_R, T_PANEL + 2.0, z_start=z_start - 1.0)
    lower_win_cut.translate(FreeCAD.Vector(W_OUT/2, LOWER_WIN_Y, 0))
    frame_cut = frame_blank.cut(upper_win_cut).cut(lower_win_cut)

    # 8x M4 Insert Nut Seats (Ø5.8mm x 9mm deep)
    for sx, gy in NUT_COORDS:
        if insert_dir == 1: # Front face entry (Z=z_start)
            h = Part.makeCylinder(5.8/2, 9.0, FreeCAD.Vector(W_OUT/2 + sx, gy, z_start - 0.1), FreeCAD.Vector(0, 0, 1))
        else: # Rear face entry (Z=z_start + T_PANEL)
            h = Part.makeCylinder(5.8/2, 9.0, FreeCAD.Vector(W_OUT/2 + sx, gy, z_start + T_PANEL + 0.1), FreeCAD.Vector(0, 0, -1))
        frame_cut = frame_cut.cut(h)
    return frame_cut

front_frame_shape = make_ladder_frame(Z_FRONT_FRAME_START, insert_dir=1)
obj_front_frame = doc.addObject("Part::Feature", "Front_Inner_Ladder_Frame")
obj_front_frame.Shape = front_frame_shape
obj_front_frame.Label = "Front Inner Ladder Frame (112x206x12mm at Z=16..28mm)"

rear_frame_shape = make_ladder_frame(Z_REAR_FRAME_START, insert_dir=-1)
obj_rear_frame = doc.addObject("Part::Feature", "Rear_Inner_Ladder_Frame")
obj_rear_frame.Shape = rear_frame_shape
obj_rear_frame.Label = "Rear Inner Ladder Frame (112x206x12mm at Z=162..174mm)"

# -----------------------------------------------------------------------------
# 3. INTERNAL WINDOW BRACE (112 x 12 x 134mm at Y=82mm, Z=28 to 162mm)
# -----------------------------------------------------------------------------
print("Modeling Internal Window Brace (112x12x134mm directly linking Front & Rear 40mm Crossbars)...")

brace_solid = Part.makeBox(W_IN, T_PANEL, D_INTERNAL_CAVITY, FreeCAD.Vector(T_PANEL, SPLIT_JOINT_Y - T_PANEL/2, Z_CAVITY_START))
# Window cutout: 64mm (W) x 86mm (D)
brace_cut_face = make_rounded_rect_face(64.0, 86.0, 15.0, z_pos=0.0)
brace_cutter = brace_cut_face.extrude(FreeCAD.Vector(0, 0, T_PANEL + 4.0))
brace_cutter.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 90)
brace_cutter.translate(FreeCAD.Vector(W_OUT/2, SPLIT_JOINT_Y + T_PANEL/2 + 2.0, (Z_CAVITY_START + Z_CAVITY_END)/2))
window_brace = brace_solid.cut(brace_cutter)

obj_brace = doc.addObject("Part::Feature", "Internal_Window_Brace")
obj_brace.Shape = window_brace
obj_brace.Label = "Internal Window Brace (112x12x134mm linking Crossbars)"

# -----------------------------------------------------------------------------
# 4. FRONT HEAVY-DUTY 12MM UPPER DRIVER PLATES (U1..U4 - 112 x 136 x 12mm)
# -----------------------------------------------------------------------------
print("\nModeling Heavy-Duty 12mm Upper Driver Plates (U1 to U4, 112x136x12mm)...")

def make_upper_driver_12mm_base():
    face = make_hybrid_split_plate_face(UPPER_PLATE_W, UPPER_PLATE_H, r_top=4.0, r_btm=0.5, z_pos=0.0)
    plate = face.extrude(FreeCAD.Vector(0, 0, UPPER_PLATE_T))
    # 4x M4 Countersunk Holes: Top (Y_local = +55mm), Bottom on Crossbar (Y_local = -58mm)
    for sx in [-47.0, 47.0]:
        for sy in [55.0, -58.0]:
            h_thru = Part.makeCylinder(4.2/2, UPPER_PLATE_T + 2.0, FreeCAD.Vector(sx, sy, -1.0), FreeCAD.Vector(0, 0, 1))
            h_cs = Part.makeCone(8.5/2, 4.2/2, 2.5, FreeCAD.Vector(sx, sy, 0.0), FreeCAD.Vector(0, 0, 1))
            plate = plate.cut(h_thru).cut(h_cs)
    return plate

# PLATE U1: 2" - 2.5" Drivers
u1_solid = make_upper_driver_12mm_base()
u1_reb = Part.makeCylinder(68.0/2, 3.0 + 0.1, FreeCAD.Vector(0, 5.0, -0.05), FreeCAD.Vector(0, 0, 1))
u1_thru = Part.makeCylinder(56.0/2, UPPER_PLATE_T + 0.2, FreeCAD.Vector(0, 5.0, -0.1), FreeCAD.Vector(0, 0, 1))
u1_chamfer = Part.makeCone(56.0/2, 72.0/2, UPPER_PLATE_T - 3.0 + 0.1, FreeCAD.Vector(0, 5.0, 3.0), FreeCAD.Vector(0, 0, 1))
u1_solid = u1_solid.cut(u1_reb).cut(u1_thru).cut(u1_chamfer)
for a in [45, 135, 225, 315]:
    rad = math.radians(a)
    h = Part.makeCylinder(3.5/2, UPPER_PLATE_T + 2.0, FreeCAD.Vector((62/2)*math.cos(rad), 5.0 + (62/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
    u1_solid = u1_solid.cut(h)

obj_u1 = doc.addObject("Part::Feature", "Upper_Plate_U1_2inch")
obj_u1.Shape = u1_solid
obj_u1.Label = "Upper Plate U1 (112x136x12mm 2-2.5 Inch)"

# PLATE U2: 3" - 3.5" Benchmark Drivers
u2_solid = make_upper_driver_12mm_base()
u2_reb = Part.makeCylinder(96.0/2, 3.5 + 0.1, FreeCAD.Vector(0, 5.0, -0.05), FreeCAD.Vector(0, 0, 1))
u2_thru = Part.makeCylinder(76.0/2, UPPER_PLATE_T + 0.2, FreeCAD.Vector(0, 5.0, -0.1), FreeCAD.Vector(0, 0, 1))
u2_chamfer = Part.makeCone(76.0/2, 96.0/2, UPPER_PLATE_T - 3.5 + 0.1, FreeCAD.Vector(0, 5.0, 3.5), FreeCAD.Vector(0, 0, 1))
u2_solid = u2_solid.cut(u2_reb).cut(u2_thru).cut(u2_chamfer)
for a in [45, 135, 225, 315]:
    rad = math.radians(a)
    h = Part.makeCylinder(4.2/2, UPPER_PLATE_T + 2.0, FreeCAD.Vector((86/2)*math.cos(rad), 5.0 + (86/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
    u2_solid = u2_solid.cut(h)

obj_u2 = doc.addObject("Part::Feature", "Upper_Plate_U2_3inch")
obj_u2.Shape = u2_solid
obj_u2.Label = "Upper Plate U2 (112x136x12mm 3-3.5 Inch Benchmark)"

# PLATE U3: 3.5" - 4" Woofers
u3_solid = make_upper_driver_12mm_base()
u3_reb = Part.makeCylinder(108.0/2, 3.5 + 0.1, FreeCAD.Vector(0, 5.0, -0.05), FreeCAD.Vector(0, 0, 1))
u3_thru = Part.makeCylinder(96.0/2, UPPER_PLATE_T + 0.2, FreeCAD.Vector(0, 5.0, -0.1), FreeCAD.Vector(0, 0, 1))
u3_chamfer = Part.makeCone(96.0/2, 104.0/2, UPPER_PLATE_T - 3.5 + 0.1, FreeCAD.Vector(0, 5.0, 3.5), FreeCAD.Vector(0, 0, 1))
u3_solid = u3_solid.cut(u3_reb).cut(u3_thru).cut(u3_chamfer)
for a in [45, 135, 225, 315]:
    rad = math.radians(a)
    h = Part.makeCylinder(4.2/2, UPPER_PLATE_T + 2.0, FreeCAD.Vector((104/2)*math.cos(rad), 5.0 + (104/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
    u3_solid = u3_solid.cut(h)

obj_u3 = doc.addObject("Part::Feature", "Upper_Plate_U3_4inch")
obj_u3.Shape = u3_solid
obj_u3.Label = "Upper Plate U3 (112x136x12mm 4 Inch Woofer)"

# PLATE U4 / REAR UPPER SOLID BLANK (112 x 136 x 12mm, NO HOLES)
u4_solid = make_upper_driver_12mm_base()
obj_u4 = doc.addObject("Part::Feature", "Upper_Plate_U4_Blank")
obj_u4.Shape = u4_solid
obj_u4.Label = "Upper Plate U4 / Rear Upper Solid (112x136x12mm)"

# -----------------------------------------------------------------------------
# 5. FRONT & REAR HEAVY-DUTY 12MM LOWER MODULES (P1..P4 - 112 x 70 x 12mm)
# -----------------------------------------------------------------------------
print("\nModeling Heavy-Duty 12mm Lower Acoustic Modules (P1 to P4, 112x70x12mm)...")

def make_lower_acoustic_12mm_base():
    face = make_hybrid_split_plate_face(LOWER_PLATE_W, LOWER_PLATE_H, r_top=0.5, r_btm=4.0, z_pos=0.0)
    plate = face.extrude(FreeCAD.Vector(0, 0, LOWER_PLATE_T))
    # 4x M4 Countersunk Holes: Top on Crossbar (Y_local = +25mm), Bottom (Y_local = -23mm)
    for sx in [-47.0, 47.0]:
        for sy in [25.0, -23.0]:
            h_thru = Part.makeCylinder(4.2/2, LOWER_PLATE_T + 2.0, FreeCAD.Vector(sx, sy, -1.0), FreeCAD.Vector(0, 0, 1))
            h_cs = Part.makeCone(8.5/2, 4.2/2, 2.5, FreeCAD.Vector(sx, sy, 0.0), FreeCAD.Vector(0, 0, 1))
            plate = plate.cut(h_thru).cut(h_cs)
    return plate

# MODULE P1 / REAR LOWER SOLID BLANK (112 x 70 x 12mm, NO HOLES)
p1_solid = make_lower_acoustic_12mm_base()
obj_p1 = doc.addObject("Part::Feature", "Lower_Plate_P1_Sealed")
obj_p1.Shape = p1_solid
obj_p1.Label = "Lower Module P1 / Rear Lower Solid (112x70x12mm)"

# MODULE P2: Front Cylindrical Port Socket Plate
p2_solid = make_lower_acoustic_12mm_base()
p2_reb = Part.makeCylinder(53.0/2, 2.5 + 0.1, FreeCAD.Vector(0, 0, -0.05), FreeCAD.Vector(0, 0, 1))
p2_thru = Part.makeCylinder(41.5/2, LOWER_PLATE_T + 0.2, FreeCAD.Vector(0, 0, -0.1), FreeCAD.Vector(0, 0, 1))
p2_solid = p2_solid.cut(p2_reb).cut(p2_thru)
for a in [0, 120, 240]:
    rad = math.radians(a)
    h = Part.makeCylinder(3.2/2, LOWER_PLATE_T + 2.0, FreeCAD.Vector((47/2)*math.cos(rad), (47/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
    p2_solid = p2_solid.cut(h)

obj_p2 = doc.addObject("Part::Feature", "Lower_Plate_P2_Port_Socket")
obj_p2.Shape = p2_solid
obj_p2.Label = "Lower Module P2 (112x70x12mm Port Socket)"

# MODULE P3: Integrated Slit Duct Port Plate (90 x 14mm opening with 120mm duct)
p3_solid = make_lower_acoustic_12mm_base()
slit_opening = make_rounded_rect_solid(90.0, 14.0, 3.0, 122.0, z_start=-1.0)
duct_housing = make_rounded_rect_solid(94.0, 18.0, 4.5, 114.0, z_start=12.0)
p3_solid = p3_solid.fuse(duct_housing).cut(slit_opening)
obj_p3 = doc.addObject("Part::Feature", "Lower_Plate_P3_Slit_Port")
obj_p3.Shape = p3_solid
obj_p3.Label = "Lower Module P3 (112x70x12mm Slit Duct)"

# MODULE P4: Passive Radiator Mount Plate
p4_solid = make_lower_acoustic_12mm_base()
p4_reb = Part.makeCylinder(96.0/2, 3.5 + 0.1, FreeCAD.Vector(0, 0, -0.05), FreeCAD.Vector(0, 0, 1))
p4_thru = Part.makeCylinder(76.0/2, LOWER_PLATE_T + 0.2, FreeCAD.Vector(0, 0, -0.1), FreeCAD.Vector(0, 0, 1))
p4_solid = p4_solid.cut(p4_reb).cut(p4_thru)
for a in [45, 135, 225, 315]:
    rad = math.radians(a)
    h = Part.makeCylinder(4.2/2, LOWER_PLATE_T + 2.0, FreeCAD.Vector((86/2)*math.cos(rad), (86/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
    p4_solid = p4_solid.cut(h)

obj_p4 = doc.addObject("Part::Feature", "Lower_Plate_P4_Passive_Rad")
obj_p4.Shape = p4_solid
obj_p4.Label = "Lower Module P4 (112x70x12mm Passive Radiator)"

# -----------------------------------------------------------------------------
# 6. MODULAR CYLINDRICAL FLARED PORT TUBES (80mm, 120mm, 150mm)
# -----------------------------------------------------------------------------
print("\nModeling Modular Flared Port Tubes...")

def make_flared_port_tube(length):
    outer_cyl = Part.makeCylinder(41.0/2, length, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    flange = Part.makeCylinder(53.0/2, 2.5, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    inner_air = Part.makeCylinder(35.0/2, length + 2.0, FreeCAD.Vector(0, 0, -1.0), FreeCAD.Vector(0, 0, 1))
    port_tube = outer_cyl.fuse(flange).cut(inner_air)
    for a in [0, 120, 240]:
        rad = math.radians(a)
        h = Part.makeCylinder(3.2/2, 5.0, FreeCAD.Vector((47/2)*math.cos(rad), (47/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
        port_tube = port_tube.cut(h)
    return port_tube

tube_80 = make_flared_port_tube(80.0)
obj_t80 = doc.addObject("Part::Feature", "Port_Tube_80mm")
obj_t80.Shape = tube_80

tube_120 = make_flared_port_tube(120.0)
obj_t120 = doc.addObject("Part::Feature", "Port_Tube_120mm")
obj_t120.Shape = tube_120

tube_150 = make_flared_port_tube(150.0)
obj_t150 = doc.addObject("Part::Feature", "Port_Tube_150mm")
obj_t150.Shape = tube_150

# -----------------------------------------------------------------------------
# 7. AIRTIGHT EVA GASKETS & ASSEMBLED CHASSIS
# -----------------------------------------------------------------------------
print("\nCreating Gasket Seals & Symmetrical Assembled State...")

# "日" Shaped Dual-Window Perimeter Gasket with 40mm Center Bar (112x206x1.5mm)
frame_gasket = make_rounded_rect_solid(W_IN, H_IN, 4.0, GASKET_THICK, z_start=0.0)
gsk_upper_cut = make_rounded_rect_solid(UPPER_WIN_W, UPPER_WIN_H, UPPER_WIN_R, 3.0, z_start=-0.5)
gsk_upper_cut.translate(FreeCAD.Vector(0, UPPER_WIN_Y - (T_PANEL + H_IN/2), 0))
gsk_lower_cut = make_rounded_rect_solid(LOWER_WIN_W, LOWER_WIN_H, LOWER_WIN_R, 3.0, z_start=-0.5)
gsk_lower_cut.translate(FreeCAD.Vector(0, LOWER_WIN_Y - (T_PANEL + H_IN/2), 0))
frame_gasket = frame_gasket.cut(gsk_upper_cut).cut(gsk_lower_cut)

obj_gsk = doc.addObject("Part::Feature", "Ladder_Frame_Gasket_EVA")
obj_gsk.Shape = frame_gasket

# Position active front modules:
u2_placed = u2_solid.copy()
u2_placed.translate(FreeCAD.Vector(W_OUT/2, UPPER_POS_Y, Z_FRONT_SWAP_START))
obj_u2_active = doc.addObject("Part::Feature", "Active_Front_Upper_Plate_U2")
obj_u2_active.Shape = u2_placed

p2_placed = p2_solid.copy()
p2_placed.translate(FreeCAD.Vector(W_OUT/2, LOWER_POS_Y, Z_FRONT_SWAP_START))
obj_p2_active = doc.addObject("Part::Feature", "Active_Front_Lower_Plate_P2")
obj_p2_active.Shape = p2_placed

front_gsk_placed = frame_gasket.copy()
front_gsk_placed.translate(FreeCAD.Vector(W_OUT/2, T_PANEL + H_IN/2, Z_FRONT_SWAP_END - GASKET_THICK))
obj_front_gsk_active = doc.addObject("Part::Feature", "Active_Front_Gasket")
obj_front_gsk_active.Shape = front_gsk_placed

tube120_placed = tube_120.copy()
tube120_placed.translate(FreeCAD.Vector(W_OUT/2, ACOUSTIC_POS_Y, Z_FRONT_SWAP_START))
obj_tube120_active = doc.addObject("Part::Feature", "Active_Port_Tube_120mm")
obj_tube120_active.Shape = tube120_placed

# Position active rear solid modules:
rear_upper_placed = u4_solid.copy()
# Rotate 180 deg around Y axis for rear face mounting
rear_upper_placed.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 180)
rear_upper_placed.translate(FreeCAD.Vector(W_OUT/2, UPPER_POS_Y, Z_REAR_SWAP_END))
obj_rear_upper_active = doc.addObject("Part::Feature", "Active_Rear_Upper_Solid_Plate")
obj_rear_upper_active.Shape = rear_upper_placed

rear_lower_placed = p1_solid.copy()
rear_lower_placed.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 180)
rear_lower_placed.translate(FreeCAD.Vector(W_OUT/2, LOWER_POS_Y, Z_REAR_SWAP_END))
obj_rear_lower_active = doc.addObject("Part::Feature", "Active_Rear_Lower_Solid_Plate")
obj_rear_lower_active.Shape = rear_lower_placed

rear_gsk_placed = frame_gasket.copy()
rear_gsk_placed.translate(FreeCAD.Vector(W_OUT/2, T_PANEL + H_IN/2, Z_REAR_FRAME_END))
obj_rear_gsk_active = doc.addObject("Part::Feature", "Active_Rear_Gasket")
obj_rear_gsk_active.Shape = rear_gsk_placed

doc.recompute()

# =============================================================================
# EXPORTING STEP 3D CAD & PRODUCTION STLS
# =============================================================================
print("\n" + "="*65)
print("EXPORTING SYMMETRICAL DUAL-FACE 3D PRODUCTION ARTIFACTS")
print("="*65)

# 1. Complete Assembled Enclosure STEP
assembly_export_objs = [
    obj_top, obj_btm, obj_left, obj_right,
    obj_front_frame, obj_rear_frame, obj_brace,
    obj_u2_active, obj_p2_active, obj_front_gsk_active, obj_tube120_active,
    obj_rear_upper_active, obj_rear_lower_active, obj_rear_gsk_active
]
Part.export(assembly_export_objs, STEP_PATH)
print(f"Exported STEP 3D CAD: {STEP_PATH} ({os.path.getsize(STEP_PATH):,} bytes)")

# 2. Individual Component STLs for 3D Printing & CNC
stl_export_map = {
    "upper_plate_u1_2inch.stl": u1_solid,
    "upper_plate_u2_3inch.stl": u2_solid,
    "upper_plate_u3_4inch.stl": u3_solid,
    "upper_plate_u4_blank.stl": u4_solid,
    "rear_upper_solid_plate.stl": u4_solid,
    "lower_plate_p1_sealed.stl": p1_solid,
    "rear_lower_solid_plate.stl": p1_solid,
    "lower_plate_p2_port_socket.stl": p2_solid,
    "lower_plate_p3_slit_port.stl": p3_solid,
    "lower_plate_p4_passive_rad.stl": p4_solid,
    "port_tube_80mm.stl": tube_80,
    "port_tube_120mm.stl": tube_120,
    "port_tube_150mm.stl": tube_150,
    "inner_ladder_baffle_frame.stl": front_frame_shape,
    "window_brace.stl": window_brace,
    "ladder_frame_gasket_eva.stl": frame_gasket,
}

for filename, shape in stl_export_map.items():
    filepath = os.path.join(STL_DIR, filename)
    export_mesh_stl(shape, filepath, deflection=0.04)

# 3. Save Native FreeCAD Document (.FCStd)
doc.saveAs(FCSTD_PATH)
print(f"\nSaved Native FreeCAD Project: {FCSTD_PATH} ({os.path.getsize(FCSTD_PATH):,} bytes)")

print("\n=================================================================")
print("FREECAD SYMMETRICAL DUAL-FACE AUTOMATION COMPLETED SUCCESSFULLY!")
print("=================================================================")
