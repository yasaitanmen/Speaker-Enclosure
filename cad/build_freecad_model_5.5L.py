#!/usr/bin/env python3
# =============================================================================
# FREECAD 3D SOLID AUTOMATION - 5.5L DEEP-BASS DOUBLE BASS-REFLEX (DBR) MODEL
# Project: 5.5L Deep-Bass DBR Reference Desktop Speaker (2" to 4" Drivers)
# File: cad/build_freecad_model_5.5L.py
# Description: Generates full 3D solid parametric models using FreeCAD's native
#              Python API (FreeCAD, Part, Mesh) for:
#              - Outer Box: W136mm x H310mm x D210mm (12mm MDF / Baltic Birch)
#              - Symmetrical Front & Rear "日" Ladder Frames: 112x286x12mm (Y_split=162mm)
#                * Upper Window: 90x106mm (Y: 182..288mm, center Y=235mm)
#                * Center 40mm Crossbar: 112x40mm (Y: 142..182mm, center Y=162mm)
#                * Lower Window: 90x110mm (Y: 22..132mm, center Y=77mm)
#              - Upper Driver Baffle Plate: 112x136x12mm (100% INTERCHANGEABLE with 3.2L model)
#              - Lower Acoustic Baffle Plate: 112x150x12mm (5.5L DBR Modules P1..P4)
#              - Internal DBR Partition Brace at Y=162mm (Z=28..182mm) with 1st internal port pipe
#                (ID 30mm x L 80mm).
#              Exports:
#              - Native FreeCAD project: cad/speaker_enclosure_5.5L.FCStd
#              - STEP 3D CAD interchange: cad/speaker_enclosure_5.5L.step
#              - Production STLs in cad/stl/5.5L/
# =============================================================================

import os
import sys
import math
import FreeCAD
import Part
import Mesh

print("=================================================================")
print("STARTING FREECAD 5.5L DEEP-BASS DBR SPEAKER 3D SOLID GENERATION")
print("FreeCAD Version:", ".".join(FreeCAD.Version()[:3]))
print("=================================================================")

# Output Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STL_DIR = os.path.join(SCRIPT_DIR, "stl", "5.5L")
os.makedirs(STL_DIR, exist_ok=True)

FCSTD_PATH = os.path.join(SCRIPT_DIR, "speaker_enclosure_5.5L.FCStd")
STEP_PATH = os.path.join(SCRIPT_DIR, "speaker_enclosure_5.5L.step")

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
# MODEL INITIALIZATION & PARAMETERS (5.5L DBR)
# =============================================================================

doc = FreeCAD.newDocument("SpeakerEnclosure_5_5L_DeepBass_DBR")

# Outer Cabinet Dimensions (mm)
W_OUT = 136.0
H_OUT = 310.0
D_OUT = 210.0
T_PANEL = 12.0

# Inner Dimensions (mm)
W_IN = W_OUT - 2 * T_PANEL  # 112.0 mm
H_IN = H_OUT - 2 * T_PANEL  # 286.0 mm

# Symmetrical Dual-Face Z Positions (mm)
FRONT_RECESS         = 4.0                     # Z=0..4mm
Z_FRONT_SWAP_START   = 4.0                     # Z=4mm
Z_FRONT_SWAP_END     = 16.0                    # Z=16mm (12mm thick)
Z_FRONT_FRAME_START  = 16.0                    # Z=16mm
Z_FRONT_FRAME_END    = 28.0                    # Z=28mm (12mm thick)

Z_CAVITY_START       = 28.0                    # Z=28mm
Z_CAVITY_END         = 182.0                   # Z=182mm
D_INTERNAL_CAVITY    = Z_CAVITY_END - Z_CAVITY_START  # 154.0 mm

Z_REAR_FRAME_START   = 182.0                   # Z=182mm
Z_REAR_FRAME_END     = 194.0                   # Z=194mm (12mm thick)
Z_REAR_SWAP_START    = 194.0                   # Z=194mm
Z_REAR_SWAP_END      = 206.0                   # Z=206mm (12mm thick)
REAR_RECESS          = 4.0                     # Z=206..210mm

# "日" 5.5L Ladder Frame Parameters (mm)
UPPER_WIN_W   = 90.0
UPPER_WIN_H   = 106.0
UPPER_WIN_Y   = 235.0   # Spans Y=182.0 to Y=288.0 (Center Y=235.0)
UPPER_WIN_R   = 5.0

CROSSBAR_W    = 112.0
CROSSBAR_H    = 40.0    # Spans Y=142.0 to Y=182.0 (Center Y=162.0)

LOWER_WIN_W   = 90.0
LOWER_WIN_H   = 110.0
LOWER_WIN_Y   = 77.0    # Spans Y=22.0 to Y=132.0 (Center Y=77.0)
LOWER_WIN_R   = 5.0

SPLIT_JOINT_Y = 162.0   # Horizontal split line (Center of 40mm Crossbar)

# Swappable Upper Driver Plate (112 x 136 x 12mm - 100% interchangeable with 3.2L)
UPPER_PLATE_W = 112.0
UPPER_PLATE_H = 136.0
UPPER_PLATE_T = 12.0
UPPER_POS_Y   = 230.0   # Spans Y=162.0 to Y=298.0 (Center Y=230.0)
DRIVER_POS_Y  = 235.0   # Acoustic driver center

# Swappable Lower Acoustic Module (112 x 150 x 12mm - 5.5L Expanded)
LOWER_PLATE_W = 112.0
LOWER_PLATE_H = 150.0
LOWER_PLATE_T = 12.0
LOWER_POS_Y   = 87.0    # Spans Y=12.0 to Y=162.0 (Center Y=87.0)
ACOUSTIC_POS_Y= 77.0    # Lower acoustic center

GASKET_THICK  = 1.5

# 8x M4 Insert Nut Coordinates (Global X, Y on 5.5L Inner Frame)
# Upper Plate: Top (Y=285), Bottom on Crossbar (Y=172, 10mm above seam)
# Lower Plate: Top on Crossbar (Y=152, 10mm below seam), Bottom (Y=24)
NUT_COORDS_55L = [
    (-47.0, 285.0), (47.0, 285.0),
    (-47.0, 172.0), (47.0, 172.0),
    (-47.0, 152.0), (47.0, 152.0),
    (-47.0, 24.0),  (47.0, 24.0)
]

# -----------------------------------------------------------------------------
# 1. OUTER CABINET PANELS (FULL DEPTH 210mm, HEIGHT 310mm)
# -----------------------------------------------------------------------------
print("\nModeling 5.5L Outer Cabinet Panels (210mm Full Depth with Dual Chamfers)...")

# Top Panel (136 x 12 x 210mm)
top_panel = Part.makeBox(W_OUT, T_PANEL, D_OUT, FreeCAD.Vector(0, H_OUT - T_PANEL, 0))
top_chamfer_front = Part.makeBox(W_OUT + 10, 10, 10, FreeCAD.Vector(-5, H_OUT - 3, -7))
top_chamfer_front.rotate(FreeCAD.Vector(0, H_OUT, 0), FreeCAD.Vector(1, 0, 0), -45)
top_chamfer_rear = Part.makeBox(W_OUT + 10, 10, 10, FreeCAD.Vector(-5, H_OUT - 3, D_OUT - 3))
top_chamfer_rear.rotate(FreeCAD.Vector(0, H_OUT, D_OUT), FreeCAD.Vector(1, 0, 0), 45)
top_panel = top_panel.cut(top_chamfer_front).cut(top_chamfer_rear)
obj_top = doc.addObject("Part::Feature", "Top_Panel")
obj_top.Shape = top_panel
obj_top.Label = "Top Panel (136x12x210mm)"

# Bottom Panel (136 x 12 x 210mm)
btm_panel = Part.makeBox(W_OUT, T_PANEL, D_OUT, FreeCAD.Vector(0, 0, 0))
btm_chamfer_front = Part.makeBox(W_OUT + 10, 10, 10, FreeCAD.Vector(-5, -7, -7))
btm_chamfer_front.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 45)
btm_chamfer_rear = Part.makeBox(W_OUT + 10, 10, 10, FreeCAD.Vector(-5, -7, D_OUT - 3))
btm_chamfer_rear.rotate(FreeCAD.Vector(0, 0, D_OUT), FreeCAD.Vector(1, 0, 0), -45)
btm_panel = btm_panel.cut(btm_chamfer_front).cut(btm_chamfer_rear)
obj_btm = doc.addObject("Part::Feature", "Bottom_Panel")
obj_btm.Shape = btm_panel
obj_btm.Label = "Bottom Panel (136x12x210mm)"

# Left Side Panel (12 x 286 x 210mm)
left_side = Part.makeBox(T_PANEL, H_IN, D_OUT, FreeCAD.Vector(0, T_PANEL, 0))
left_chamfer_front = Part.makeBox(10, H_OUT + 10, 10, FreeCAD.Vector(-7, -5, -7))
left_chamfer_front.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 45)
left_chamfer_rear = Part.makeBox(10, H_OUT + 10, 10, FreeCAD.Vector(-7, -5, D_OUT - 3))
left_chamfer_rear.rotate(FreeCAD.Vector(0, 0, D_OUT), FreeCAD.Vector(0, 1, 0), -45)
# Dado for DBR Partition (3mm deep x 12mm high at Y=162mm from Z=28 to Z=182)
left_dado = Part.makeBox(3.0, 12.0, D_INTERNAL_CAVITY, FreeCAD.Vector(T_PANEL - 3.0, SPLIT_JOINT_Y - 6.0, Z_CAVITY_START))
left_side = left_side.cut(left_chamfer_front).cut(left_chamfer_rear).cut(left_dado)
obj_left = doc.addObject("Part::Feature", "Left_Side_Panel")
obj_left.Shape = left_side
obj_left.Label = "Left Side Panel (12x286x210mm)"

# Right Side Panel (12 x 286 x 210mm)
right_side = Part.makeBox(T_PANEL, H_IN, D_OUT, FreeCAD.Vector(W_OUT - T_PANEL, T_PANEL, 0))
right_chamfer_front = Part.makeBox(10, H_OUT + 10, 10, FreeCAD.Vector(W_OUT - 3, -5, -7))
right_chamfer_front.rotate(FreeCAD.Vector(W_OUT, 0, 0), FreeCAD.Vector(0, 1, 0), -45)
right_chamfer_rear = Part.makeBox(10, H_OUT + 10, 10, FreeCAD.Vector(W_OUT - 3, -5, D_OUT - 3))
right_chamfer_rear.rotate(FreeCAD.Vector(W_OUT, 0, D_OUT), FreeCAD.Vector(0, 1, 0), 45)
right_dado = Part.makeBox(3.0, 12.0, D_INTERNAL_CAVITY, FreeCAD.Vector(W_OUT - T_PANEL, SPLIT_JOINT_Y - 6.0, Z_CAVITY_START))
right_side = right_side.cut(right_chamfer_front).cut(right_chamfer_rear).cut(right_dado)
obj_right = doc.addObject("Part::Feature", "Right_Side_Panel")
obj_right.Shape = right_side
obj_right.Label = "Right Side Panel (12x286x210mm)"

# -----------------------------------------------------------------------------
# 2. 5.5L SYMMETRICAL "日" LADDER INNER FRAMES (FRONT Z=16..28 & REAR Z=182..194)
# -----------------------------------------------------------------------------
print("\nModeling 5.5L Symmetrical '日' Ladder Inner Frames (112x286x12mm)...")

def make_ladder_frame_55L(z_start, insert_dir=1):
    frame_blank = Part.makeBox(W_IN, H_IN, T_PANEL, FreeCAD.Vector(T_PANEL, T_PANEL, z_start))
    upper_win_cut = make_rounded_rect_solid(UPPER_WIN_W, UPPER_WIN_H, UPPER_WIN_R, T_PANEL + 2.0, z_start=z_start - 1.0)
    upper_win_cut.translate(FreeCAD.Vector(W_OUT/2, UPPER_WIN_Y, 0))
    lower_win_cut = make_rounded_rect_solid(LOWER_WIN_W, LOWER_WIN_H, LOWER_WIN_R, T_PANEL + 2.0, z_start=z_start - 1.0)
    lower_win_cut.translate(FreeCAD.Vector(W_OUT/2, LOWER_WIN_Y, 0))
    frame_cut = frame_blank.cut(upper_win_cut).cut(lower_win_cut)

    for sx, gy in NUT_COORDS_55L:
        if insert_dir == 1:
            h = Part.makeCylinder(5.8/2, 9.0, FreeCAD.Vector(W_OUT/2 + sx, gy, z_start - 0.1), FreeCAD.Vector(0, 0, 1))
        else:
            h = Part.makeCylinder(5.8/2, 9.0, FreeCAD.Vector(W_OUT/2 + sx, gy, z_start + T_PANEL + 0.1), FreeCAD.Vector(0, 0, -1))
        frame_cut = frame_cut.cut(h)
    return frame_cut

front_frame_shape = make_ladder_frame_55L(Z_FRONT_FRAME_START, insert_dir=1)
obj_front_frame = doc.addObject("Part::Feature", "Front_Inner_Ladder_Frame_55L")
obj_front_frame.Shape = front_frame_shape
obj_front_frame.Label = "Front Inner Ladder Frame (112x286x12mm at Z=16..28mm)"

rear_frame_shape = make_ladder_frame_55L(Z_REAR_FRAME_START, insert_dir=-1)
obj_rear_frame = doc.addObject("Part::Feature", "Rear_Inner_Ladder_Frame_55L")
obj_rear_frame.Shape = rear_frame_shape
obj_rear_frame.Label = "Rear Inner Ladder Frame (112x286x12mm at Z=182..194mm)"

# -----------------------------------------------------------------------------
# 3. INTERNAL DBR PARTITION BRACE WITH 1ST INTERNAL PORT (ID 30mm x L 80mm)
# -----------------------------------------------------------------------------
print("Modeling Internal DBR Partition Brace (112x12x154mm at Y=162mm with ID 30mm Port)...")

dbr_partition_solid = Part.makeBox(W_IN, T_PANEL, D_INTERNAL_CAVITY, FreeCAD.Vector(T_PANEL, SPLIT_JOINT_Y - T_PANEL/2, Z_CAVITY_START))
# 1st Internal Port Duct Cutout & Pipe: ID 30mm, OD 36mm, Length 80mm (pointing down into Chamber 2)
port_hole = Part.makeCylinder(36.0/2, T_PANEL + 2.0, FreeCAD.Vector(W_OUT/2, SPLIT_JOINT_Y + T_PANEL/2 + 1.0, (Z_CAVITY_START + Z_CAVITY_END)/2), FreeCAD.Vector(0, -1, 0))
dbr_partition = dbr_partition_solid.cut(port_hole)

# Internal Port Pipe Tube (extends downward by 80mm - 12mm = 68mm)
pipe_outer = Part.makeCylinder(36.0/2, 80.0, FreeCAD.Vector(W_OUT/2, SPLIT_JOINT_Y + T_PANEL/2, (Z_CAVITY_START + Z_CAVITY_END)/2), FreeCAD.Vector(0, -1, 0))
pipe_inner = Part.makeCylinder(30.0/2, 84.0, FreeCAD.Vector(W_OUT/2, SPLIT_JOINT_Y + T_PANEL/2 + 2.0, (Z_CAVITY_START + Z_CAVITY_END)/2), FreeCAD.Vector(0, -1, 0))
pipe_solid = pipe_outer.cut(pipe_inner)
dbr_partition = dbr_partition.fuse(pipe_solid)

obj_dbr_brace = doc.addObject("Part::Feature", "Internal_DBR_Partition_Brace")
obj_dbr_brace.Shape = dbr_partition
obj_dbr_brace.Label = "Internal DBR Partition Brace (112x12x154mm at Y=162mm with 30mm Port)"

# -----------------------------------------------------------------------------
# 4. SWAPPABLE 12MM UPPER DRIVER PLATES (U1..U4 - 112 x 136 x 12mm)
# -----------------------------------------------------------------------------
print("\nModeling Swappable 12mm Upper Driver Plates (U1 to U4, 112x136x12mm)...")

def make_upper_driver_12mm_base():
    face = make_hybrid_split_plate_face(UPPER_PLATE_W, UPPER_PLATE_H, r_top=4.0, r_btm=0.5, z_pos=0.0)
    plate = face.extrude(FreeCAD.Vector(0, 0, UPPER_PLATE_T))
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

# PLATE U4 / REAR UPPER SOLID BLANK
u4_solid = make_upper_driver_12mm_base()
obj_u4 = doc.addObject("Part::Feature", "Upper_Plate_U4_Blank")
obj_u4.Shape = u4_solid
obj_u4.Label = "Upper Plate U4 / Rear Upper Solid (112x136x12mm)"

# -----------------------------------------------------------------------------
# 5. 5.5L SWAPPABLE 12MM LOWER ACOUSTIC MODULES (112 x 150 x 12mm)
# -----------------------------------------------------------------------------
print("\nModeling 5.5L Heavy-Duty 12mm Lower Acoustic Modules (112x150x12mm)...")

def make_lower_acoustic_55L_base():
    face = make_hybrid_split_plate_face(LOWER_PLATE_W, LOWER_PLATE_H, r_top=0.5, r_btm=4.0, z_pos=0.0)
    plate = face.extrude(FreeCAD.Vector(0, 0, LOWER_PLATE_T))
    # 4x M4 Countersunk Holes: Top on Crossbar (Y_local = +65mm), Bottom (Y_local = -63mm)
    for sx in [-47.0, 47.0]:
        for sy in [65.0, -63.0]:
            h_thru = Part.makeCylinder(4.2/2, LOWER_PLATE_T + 2.0, FreeCAD.Vector(sx, sy, -1.0), FreeCAD.Vector(0, 0, 1))
            h_cs = Part.makeCone(8.5/2, 4.2/2, 2.5, FreeCAD.Vector(sx, sy, 0.0), FreeCAD.Vector(0, 0, 1))
            plate = plate.cut(h_thru).cut(h_cs)
    return plate

# MODULE 5.5L-P1 / REAR LOWER SOLID BLANK (112 x 150 x 12mm, NO HOLES)
p1_55L_solid = make_lower_acoustic_55L_base()
obj_p1_55L = doc.addObject("Part::Feature", "Lower_Plate_55L_P1_Sealed")
obj_p1_55L.Shape = p1_55L_solid
obj_p1_55L.Label = "Lower Module 5.5L P1 / Rear Solid (112x150x12mm)"

# MODULE 5.5L-P2: 2nd External Bass-Reflex Port Socket (45mm Flared Port)
# Port center at Y_local = -10mm (Global Y = 77mm)
p2_55L_solid = make_lower_acoustic_55L_base()
p2_reb = Part.makeCylinder(65.0/2, 3.0 + 0.1, FreeCAD.Vector(0, -10.0, -0.05), FreeCAD.Vector(0, 0, 1))
p2_thru = Part.makeCylinder(53.0/2, LOWER_PLATE_T + 0.2, FreeCAD.Vector(0, -10.0, -0.1), FreeCAD.Vector(0, 0, 1))
p2_55L_solid = p2_55L_solid.cut(p2_reb).cut(p2_thru)
for a in [0, 120, 240]:
    rad = math.radians(a)
    h = Part.makeCylinder(3.5/2, LOWER_PLATE_T + 2.0, FreeCAD.Vector((59/2)*math.cos(rad), -10.0 + (59/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
    p2_55L_solid = p2_55L_solid.cut(h)

obj_p2_55L = doc.addObject("Part::Feature", "Lower_Plate_55L_P2_Port_Socket")
obj_p2_55L.Shape = p2_55L_solid
obj_p2_55L.Label = "Lower Module 5.5L P2 (112x150x12mm 45mm Port Socket)"

# MODULE 5.5L-P3: Slit Duct Port Plate (90 x 18mm opening with 130mm duct)
p3_55L_solid = make_lower_acoustic_55L_base()
slit_cut = make_rounded_rect_solid(90.0, 18.0, 4.0, 132.0, z_start=-1.0)
slit_cut.translate(FreeCAD.Vector(0, -10.0, 0))
duct_body = make_rounded_rect_solid(96.0, 24.0, 6.0, 120.0, z_start=12.0)
duct_body.translate(FreeCAD.Vector(0, -10.0, 0))
p3_55L_solid = p3_55L_solid.fuse(duct_body).cut(slit_cut)

obj_p3_55L = doc.addObject("Part::Feature", "Lower_Plate_55L_P3_Slit_Port")
obj_p3_55L.Shape = p3_55L_solid
obj_p3_55L.Label = "Lower Module 5.5L P3 (112x150x12mm Slit Duct)"

# MODULE 5.5L-P4: Large 4-5" Passive Radiator Mount Plate
p4_55L_solid = make_lower_acoustic_55L_base()
p4_reb = Part.makeCylinder(118.0/2, 4.0 + 0.1, FreeCAD.Vector(0, -10.0, -0.05), FreeCAD.Vector(0, 0, 1))
p4_thru = Part.makeCylinder(96.0/2, LOWER_PLATE_T + 0.2, FreeCAD.Vector(0, -10.0, -0.1), FreeCAD.Vector(0, 0, 1))
p4_55L_solid = p4_55L_solid.cut(p4_reb).cut(p4_thru)
for a in [45, 135, 225, 315]:
    rad = math.radians(a)
    h = Part.makeCylinder(4.2/2, LOWER_PLATE_T + 2.0, FreeCAD.Vector((108/2)*math.cos(rad), -10.0 + (108/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
    p4_55L_solid = p4_55L_solid.cut(h)

obj_p4_55L = doc.addObject("Part::Feature", "Lower_Plate_55L_P4_Passive_Rad")
obj_p4_55L.Shape = p4_55L_solid
obj_p4_55L.Label = "Lower Module 5.5L P4 (112x150x12mm 4-5 Inch PR)"

# -----------------------------------------------------------------------------
# 6. MODULAR 45MM FLARED PORT TUBES (FOR 5.5L DBR 2ND PORT)
# -----------------------------------------------------------------------------
print("\nModeling Modular 45mm Flared Port Tubes...")

def make_45mm_flared_port_tube(length):
    outer_cyl = Part.makeCylinder(52.0/2, length, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    flange = Part.makeCylinder(65.0/2, 3.0, FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1))
    inner_air = Part.makeCylinder(45.0/2, length + 2.0, FreeCAD.Vector(0, 0, -1.0), FreeCAD.Vector(0, 0, 1))
    port_tube = outer_cyl.fuse(flange).cut(inner_air)
    for a in [0, 120, 240]:
        rad = math.radians(a)
        h = Part.makeCylinder(3.5/2, 6.0, FreeCAD.Vector((59/2)*math.cos(rad), (59/2)*math.sin(rad), -1.0), FreeCAD.Vector(0, 0, 1))
        port_tube = port_tube.cut(h)
    return port_tube

tube_45_120 = make_45mm_flared_port_tube(120.0)
obj_t45_120 = doc.addObject("Part::Feature", "Port_Tube_45mm_120mm")
obj_t45_120.Shape = tube_45_120

# -----------------------------------------------------------------------------
# 7. AIRTIGHT EVA GASKETS & ASSEMBLED CHASSIS (5.5L)
# -----------------------------------------------------------------------------
print("\nCreating 5.5L Gasket Seals & Symmetrical Assembled State...")

# 5.5L Dual-Window Perimeter Gasket (112x286x1.5mm)
frame_gasket_55L = make_rounded_rect_solid(W_IN, H_IN, 4.0, GASKET_THICK, z_start=0.0)
gsk_upper_cut = make_rounded_rect_solid(UPPER_WIN_W, UPPER_WIN_H, UPPER_WIN_R, 3.0, z_start=-0.5)
gsk_upper_cut.translate(FreeCAD.Vector(0, UPPER_WIN_Y - (T_PANEL + H_IN/2), 0))
gsk_lower_cut = make_rounded_rect_solid(LOWER_WIN_W, LOWER_WIN_H, LOWER_WIN_R, 3.0, z_start=-0.5)
gsk_lower_cut.translate(FreeCAD.Vector(0, LOWER_WIN_Y - (T_PANEL + H_IN/2), 0))
frame_gasket_55L = frame_gasket_55L.cut(gsk_upper_cut).cut(gsk_lower_cut)

obj_gsk_55L = doc.addObject("Part::Feature", "Ladder_Frame_Gasket_55L_EVA")
obj_gsk_55L.Shape = frame_gasket_55L

# Position active front modules:
u2_placed = u2_solid.copy()
u2_placed.translate(FreeCAD.Vector(W_OUT/2, UPPER_POS_Y, Z_FRONT_SWAP_START))
obj_u2_active = doc.addObject("Part::Feature", "Active_Front_Upper_Plate_U2")
obj_u2_active.Shape = u2_placed

p2_placed = p2_55L_solid.copy()
p2_placed.translate(FreeCAD.Vector(W_OUT/2, LOWER_POS_Y, Z_FRONT_SWAP_START))
obj_p2_active = doc.addObject("Part::Feature", "Active_Front_Lower_Plate_P2_55L")
obj_p2_active.Shape = p2_placed

front_gsk_placed = frame_gasket_55L.copy()
front_gsk_placed.translate(FreeCAD.Vector(W_OUT/2, T_PANEL + H_IN/2, Z_FRONT_SWAP_END - GASKET_THICK))
obj_front_gsk_active = doc.addObject("Part::Feature", "Active_Front_Gasket_55L")
obj_front_gsk_active.Shape = front_gsk_placed

tube120_placed = tube_45_120.copy()
tube120_placed.translate(FreeCAD.Vector(W_OUT/2, ACOUSTIC_POS_Y, Z_FRONT_SWAP_START))
obj_tube120_active = doc.addObject("Part::Feature", "Active_Port_Tube_45mm_120mm")
obj_tube120_active.Shape = tube120_placed

# Position active rear solid modules:
rear_upper_placed = u4_solid.copy()
rear_upper_placed.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 180)
rear_upper_placed.translate(FreeCAD.Vector(W_OUT/2, UPPER_POS_Y, Z_REAR_SWAP_END))
obj_rear_upper_active = doc.addObject("Part::Feature", "Active_Rear_Upper_Solid_Plate")
obj_rear_upper_active.Shape = rear_upper_placed

rear_lower_placed = p1_55L_solid.copy()
rear_lower_placed.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 180)
rear_lower_placed.translate(FreeCAD.Vector(W_OUT/2, LOWER_POS_Y, Z_REAR_SWAP_END))
obj_rear_lower_active = doc.addObject("Part::Feature", "Active_Rear_Lower_Solid_Plate_55L")
obj_rear_lower_active.Shape = rear_lower_placed

rear_gsk_placed = frame_gasket_55L.copy()
rear_gsk_placed.translate(FreeCAD.Vector(W_OUT/2, T_PANEL + H_IN/2, Z_REAR_FRAME_END))
obj_rear_gsk_active = doc.addObject("Part::Feature", "Active_Rear_Gasket_55L")
obj_rear_gsk_active.Shape = rear_gsk_placed

doc.recompute()

# =============================================================================
# EXPORTING STEP 3D CAD & PRODUCTION STLS (5.5L)
# =============================================================================
print("\n" + "="*65)
print("EXPORTING 5.5L DEEP-BASS DBR 3D PRODUCTION ARTIFACTS")
print("="*65)

# 1. Complete Assembled Enclosure STEP
assembly_export_objs = [
    obj_top, obj_btm, obj_left, obj_right,
    obj_front_frame, obj_rear_frame, obj_dbr_brace,
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
    "lower_plate_55L_p1_sealed.stl": p1_55L_solid,
    "rear_lower_solid_plate_55L.stl": p1_55L_solid,
    "lower_plate_55L_p2_port_socket.stl": p2_55L_solid,
    "lower_plate_55L_p3_slit_port.stl": p3_55L_solid,
    "lower_plate_55L_p4_passive_rad.stl": p4_55L_solid,
    "port_tube_45mm_120mm.stl": tube_45_120,
    "inner_ladder_baffle_frame_55L.stl": front_frame_shape,
    "internal_dbr_partition_brace.stl": dbr_partition,
    "ladder_frame_gasket_55L_eva.stl": frame_gasket_55L,
}

for filename, shape in stl_export_map.items():
    filepath = os.path.join(STL_DIR, filename)
    export_mesh_stl(shape, filepath, deflection=0.04)

# 3. Save Native FreeCAD Document (.FCStd)
doc.saveAs(FCSTD_PATH)
print(f"\nSaved Native FreeCAD Project: {FCSTD_PATH} ({os.path.getsize(FCSTD_PATH):,} bytes)")

print("\n=================================================================")
print("FREECAD 5.5L DBR AUTOMATION COMPLETED SUCCESSFULLY!")
print("=================================================================")
