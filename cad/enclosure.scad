// =============================================================================
// SYMMETRICAL DUAL-FACE "日" LADDER FRAME SPEAKER ENCLOSURE (2" TO 4" DRIVERS)
// File: enclosure.scad
// Author: Speaker Mechanical & CAD Engineer
// Description: Symmetrical Dual-Face Modular Baffle Architecture:
//              - Front & Rear Identical "日" Inner Fixed Frames (112x206x12mm):
//                * Front Frame: Z=16..28mm (40mm crossbar at Y=62..102mm)
//                * Rear Frame:  Z=162..174mm (40mm crossbar at Y=62..102mm)
//                * Upper Window: 90.0 x 106.0 mm (Y: 102 to 208 mm, center Y=155 mm)
//                * Lower Window: 90.0 x 40.0 mm (Y: 22 to 62 mm, center Y=42 mm)
//              - Internal Window Brace: 112x12x134mm at Y=82mm (Z=28..162mm)
//                directly linking front and rear 40mm crossbars as a tie-beam.
//              - Front Baffles (Z=4..16mm): Upper U1..U4 + Lower P1..P4
//              - Rear Baffles (Z=174..186mm): Upper Solid Blank + Lower Solid Blank
//              - Symmetrical 4.0mm Inset Recesses on Front (Z=0..4) and Rear (Z=186..190)
// =============================================================================

/* [View Settings] */
// View Mode: 0=Assembled Solid, 1=Cutaway Section, 2=Exploded Assembly, 3=Transparent X-Ray, 4=2D CNC Cut Sheet
view_mode = 0; // [0:Assembled Solid, 1:Cutaway Section, 2:Exploded Assembly, 3:Transparent X-Ray, 4:2D CNC Cut Sheet]

// Explode distance multiplier (for exploded view)
explode_dist = 70; // [30:1:180]

// Cutaway axis: 0=Half X Sagittal, 1=Half Z Coronal, 2=Quarter Cut
cutaway_type = 0; // [0:Half X Sagittal, 1:Half Z Coronal, 2:Quarter Cut]

/* [Upper Module - Driver Section] */
// Active Front Driver Sub-Baffle Plate (12.0mm Thick):
// 1=Plate U1 (2-2.5" Drivers: Ø56mm cutout, Ø68mm rebate, PCD Ø62mm)
// 2=Plate U2 (3-3.5" Benchmark Drivers: Ø76mm cutout, Ø96mm rebate, PCD Ø86mm)
// 3=Plate U3 (3.5-4" Woofers: Ø96mm cutout, Ø108mm rebate, PCD Ø104mm)
// 4=Plate U4 (Blank Solid Driver Plate)
upper_module_plate = 2; // [1:Plate U1 (2-2.5 Inch), 2:Plate U2 (3-3.5 Inch Benchmark), 3:Plate U3 (3.5-4 Inch Woofer), 4:Plate U4 (Blank Plate)]

/* [Lower Module - Acoustic Alignment Section] */
// Active Front Lower Acoustic Alignment Module (12.0mm Thick):
// 1=Module P1: Sealed Plate (Solid blank for Acoustic Suspension)
// 2=Module P2: Front Bass-Reflex Port Plate (Holds interchangeable cylindrical tubes: 80mm/120mm/150mm)
// 3=Module P3: Slit Duct Port Plate (Integrated horizontal front slit port)
// 4=Module P4: Passive Radiator Mount Plate (3-4" passive radiator cutout)
lower_module_mode = 2; // [1:Module P1 (Sealed Acoustic Suspension), 2:Module P2 (Front Cylindrical Flared Port), 3:Module P3 (Slit Duct Port), 4:Module P4 (Passive Radiator)]

// Cylindrical port length for Module P2 (80mm, 120mm, 150mm)
p2_port_len = 120.0; // [80.0:Short (85Hz), 120.0:Standard (71Hz), 150.0:Long (65Hz)]

/* [Cabinet Core Dimensions (mm)] */
panel_t           = 12.0;  // Cabinet wall thickness (12mm Baltic Birch / MDF)
outer_w           = 136.0; // Outer cabinet width
outer_h           = 230.0; // Outer cabinet height
outer_d           = 190.0; // Outer cabinet depth

baffle_recess     = 4.0;   // Symmetrical recess depth on front and rear (mm)

/* [Heavy-Duty Dual-Layer Dimensions (mm)] */
swap_plate_t      = 12.0;  // Swappable baffle thickness (12mm)
frame_t           = 12.0;  // Inner fixed frame thickness (12mm)
total_baffle_t    = 24.0;  // 12mm swap + 12mm frame = 24mm clamping rim
gasket_t          = 1.5;   // Compressed gasket thickness (mm)

// "日" Wide 40mm Ladder Frame Dimensions (mm)
upper_win_w       = 90.0;
upper_win_h       = 106.0;
upper_win_y       = 155.0; // Center Y of upper window (spans Y=102..208)
crossbar_h        = 40.0;  // Height of crossbar (spans Y=62..102, center Y=82)
lower_win_w       = 90.0;
lower_win_h       = 40.0;
lower_win_y       = 42.0;  // Center Y of lower window (spans Y=22..62)

// Upper Driver Plate (112 x 136 x 12mm)
upper_plate_w     = 112.0;
upper_plate_h     = 136.0;
upper_pos_y       = 150.0; // Spans Y=82 to Y=218 (Center Y=150.0)
driver_pos_y      = 155.0; // Acoustic center of driver

// Lower Acoustic Plate (112 x 70 x 12mm)
lower_plate_w     = 112.0;
lower_plate_h     = 70.0;
lower_pos_y       = 47.0;  // Spans Y=12 to Y=82 (Center Y=47.0)
acoustic_pos_y    = 47.0;  // Acoustic center

split_joint_y     = 82.0;  // Horizontal split line (Center of Crossbar)

fastener_d        = 4.2;   // M4 countersunk screw clearance hole

/* [Internal Bracing Parameters] */
brace_enable      = true;
brace_pos_y       = 82.0;  // Aligned directly linking front and rear 40mm crossbars
brace_rim_w       = 24.0;
brace_corner_r    = 15.0;

/* [Rendering Quality] */
$fn = 64;

// =============================================================================
// DERIVED DIMENSIONS & ACOUSTIC CALCULATIONS
// =============================================================================
inner_w = outer_w - 2 * panel_t; // 112 mm
inner_h = outer_h - 2 * panel_t; // 206 mm

// Z-Coordinates:
z_front_swap_start  = baffle_recess;                               // 4.0 mm
z_front_swap_end    = baffle_recess + swap_plate_t;                // 16.0 mm
z_front_frame_start = z_front_swap_end;                            // 16.0 mm
z_front_frame_end   = z_front_swap_end + frame_t;                  // 28.0 mm

z_cavity_start      = z_front_frame_end;                           // 28.0 mm
z_cavity_end        = outer_d - baffle_recess - swap_plate_t - frame_t; // 162.0 mm
inner_d             = z_cavity_end - z_cavity_start;               // 134.0 mm

z_rear_frame_start  = z_cavity_end;                                // 162.0 mm
z_rear_frame_end    = z_rear_frame_start + frame_t;                // 174.0 mm
z_rear_swap_start   = z_rear_frame_end;                            // 174.0 mm
z_rear_swap_end     = z_rear_swap_start + swap_plate_t;            // 186.0 mm

v_gross_liters = ((inner_w * inner_h * inner_d) + 2 * (upper_win_w * upper_win_h * frame_t + lower_win_w * lower_win_h * frame_t)) / 1000000; // ~3.406 L

v_driver_liters = (upper_module_plate == 1) ? 0.100 :
                  (upper_module_plate == 2) ? 0.180 :
                  (upper_module_plate == 3) ? 0.260 : 0.050;

v_lower_liters  = (lower_module_mode == 1) ? 0.000 :
                  (lower_module_mode == 2) ? (PI * pow((35/2 + 3), 2) * (p2_port_len - swap_plate_t)) / 1000000 :
                  (lower_module_mode == 3) ? (90 * 18 * 120) / 1000000 : 0.060;

v_brace_liters  = ((inner_w * inner_d) - ((inner_w - 2*brace_rim_w) * (inner_d - 2*brace_rim_w) - 4*pow(brace_corner_r, 2) + PI*pow(brace_corner_r, 2))) * panel_t / 1000000; // ~0.100 L
v_net_liters    = v_gross_liters - (v_driver_liters + v_lower_liters + v_brace_liters);
v_effective     = v_net_liters * 1.08;

// Acoustic Tuning Calculation
speed_sound     = 343000; // mm/s
port_area_mm2   = (lower_module_mode == 2) ? PI * pow(35 / 2, 2) :
                  (lower_module_mode == 3) ? (90 * 14) : 0;
port_eff_len_mm = (lower_module_mode == 2) ? (p2_port_len + 1.7 * (35 / 2)) :
                  (lower_module_mode == 3) ? (120.0 + 0.85 * sqrt(1260 / PI)) : 1;
tuning_freq_hz  = (port_area_mm2 > 0) ? (speed_sound / (2 * PI)) * sqrt(port_area_mm2 / ((v_net_liters * 1000000) * port_eff_len_mm)) : 0;

echo("=================================================================");
echo(str("SYMMETRICAL DUAL-FACE '日' LADDER FRAME SYSTEM:"));
echo(str("Gross Enclosure Volume: ", v_gross_liters, " L"));
echo(str("Net Enclosure Volume:   ", v_net_liters, " L"));
echo(str("Effective Damped Vol:   ", v_effective, " L"));
echo(str("Internal Cavity Depth:  ", inner_d, " mm (Z=28 to 162mm)"));
echo(str("Front & Rear Frames:    Z=16..28mm & Z=162..174mm (40mm Crossbars)"));
if (lower_module_mode == 1) {
    echo("Acoustic Alignment:     Sealed (Acoustic Suspension, Qtc ~ 0.70)");
} else if (lower_module_mode == 2 || lower_module_mode == 3) {
    echo(str("Tuning Frequency (Fb):  ", tuning_freq_hz, " Hz"));
} else if (lower_module_mode == 4) {
    echo("Acoustic Alignment:     Passive Radiator (Fb ~ 58-65 Hz)");
}
echo("=================================================================");

// =============================================================================
// COLOR PALETTE
// =============================================================================
c_wood_cabinet  = [0.80, 0.66, 0.48, 1.0];
c_wood_baffle   = [0.86, 0.72, 0.54, 1.0];
c_brace         = [0.72, 0.56, 0.38, 1.0];
c_plate_u1      = [0.20, 0.65, 0.85, 1.0];
c_plate_u2      = [0.85, 0.75, 0.20, 1.0];
c_plate_u3      = [0.85, 0.30, 0.25, 1.0];
c_plate_u4      = [0.45, 0.45, 0.50, 1.0];
c_plate_p1      = [0.35, 0.40, 0.48, 1.0];
c_plate_p2      = [0.10, 0.55, 0.80, 1.0];
c_plate_p3      = [0.15, 0.70, 0.45, 1.0];
c_plate_p4      = [0.75, 0.40, 0.80, 1.0];
c_gasket        = [0.15, 0.15, 0.15, 1.0];
c_xray          = [0.82, 0.72, 0.58, 0.35];

// =============================================================================
// 2D HELPERS
// =============================================================================
module rounded_rect_2d(size, r) {
    w = size[0];
    h = size[1];
    translate([r, r])
        minkowski() {
            square([w - 2*r, h - 2*r]);
            circle(r = r);
        }
}

// =============================================================================
// 3D COMPONENT MODULES
// =============================================================================

module panel_top(transparent=false) {
    color(transparent ? c_xray : c_wood_cabinet)
    difference() {
        cube([outer_w, panel_t, outer_d]);
        // Front chamfer
        translate([-1, panel_t, 0])
            rotate([45, 0, 0])
                translate([0, -3, -3])
                    cube([outer_w + 2, 6, 6]);
        // Rear chamfer
        translate([-1, panel_t, outer_d])
            rotate([-45, 0, 0])
                translate([0, -3, -3])
                    cube([outer_w + 2, 6, 6]);
    }
}

module panel_bottom(transparent=false) {
    color(transparent ? c_xray : c_wood_cabinet)
    difference() {
        cube([outer_w, panel_t, outer_d]);
        // Front chamfer
        translate([-1, 0, 0])
            rotate([-45, 0, 0])
                translate([0, -3, -3])
                    cube([outer_w + 2, 6, 6]);
        // Rear chamfer
        translate([-1, 0, outer_d])
            rotate([45, 0, 0])
                translate([0, -3, -3])
                    cube([outer_w + 2, 6, 6]);
    }
}

module panel_left(transparent=false) {
    color(transparent ? c_xray : c_wood_cabinet)
    difference() {
        cube([panel_t, inner_h, outer_d]);
        // Front chamfer
        translate([0, -1, 0])
            rotate([0, 45, 0])
                translate([-3, 0, -3])
                    cube([6, inner_h + 2, 6]);
        // Rear chamfer
        translate([0, -1, outer_d])
            rotate([0, -45, 0])
                translate([-3, 0, -3])
                    cube([6, inner_h + 2, 6]);
        // Dado for brace at Y=82mm from Z=28 to Z=162mm
        translate([panel_t - 3.0, split_joint_y - panel_t/2 - panel_t, z_cavity_start])
            cube([4.0, panel_t, inner_d]);
    }
}

module panel_right(transparent=false) {
    color(transparent ? c_xray : c_wood_cabinet)
    difference() {
        cube([panel_t, inner_h, outer_d]);
        // Front chamfer
        translate([panel_t, -1, 0])
            rotate([0, -45, 0])
                translate([-3, 0, -3])
                    cube([6, inner_h + 2, 6]);
        // Rear chamfer
        translate([panel_t, -1, outer_d])
            rotate([0, 45, 0])
                translate([-3, 0, -3])
                    cube([6, inner_h + 2, 6]);
        // Dado for brace at Y=82mm from Z=28 to Z=162mm
        translate([-1.0, split_joint_y - panel_t/2 - panel_t, z_cavity_start])
            cube([4.0, panel_t, inner_d]);
    }
}

// -----------------------------------------------------------------------------
// "日" LADDER INNER FIXED BAFFLE FRAME (WIDE 40MM CROSSBAR)
// -----------------------------------------------------------------------------
module panel_ladder_frame(transparent=false) {
    color(transparent ? c_xray : c_wood_baffle)
    difference() {
        cube([inner_w, inner_h, frame_t]);

        // Upper Window: 90 x 106mm (Center Y=155mm global => Y=143mm local)
        translate([(inner_w - upper_win_w)/2, (upper_win_y - panel_t) - upper_win_h/2, -1.0])
            linear_extrude(height = frame_t + 2.0)
                rounded_rect_2d([upper_win_w, upper_win_h], 5.0);

        // Lower Window: 90 x 40mm (Center Y=42mm global => Y=30mm local)
        translate([(inner_w - lower_win_w)/2, (lower_win_y - panel_t) - lower_win_h/2, -1.0])
            linear_extrude(height = frame_t + 2.0)
                rounded_rect_2d([lower_win_w, lower_win_h], 5.0);

        // 8x M4 Insert Nut Seats (Ø5.8mm)
        // Upper: (±47, 205) and (±47, 92) => local Y = 193 and 80
        // Lower: (±47, 72) and (±47, 24)  => local Y = 60 and 12
        for (sx = [-47, 47]) {
            for (ly = [193, 80, 60, 12]) {
                translate([inner_w/2 + sx, ly, -1])
                    cylinder(d = 5.8, h = frame_t + 2);
            }
        }
    }
}

// -----------------------------------------------------------------------------
// INTERNAL WINDOW BRACE (112 x 12 x 134mm at Y=82mm, Z=28 to 162mm)
// -----------------------------------------------------------------------------
module panel_brace(transparent=false) {
    cutout_w_br = inner_w - 2 * brace_rim_w; // 64 mm
    cutout_d_br = inner_d - 2 * brace_rim_w; // 86 mm

    color(transparent ? c_xray : c_brace)
    difference() {
        cube([inner_w, panel_t, inner_d]);
        translate([brace_rim_w, -1, brace_rim_w])
            rotate([90, 0, 0])
                translate([0, 0, -(panel_t + 2)])
                    linear_extrude(height = panel_t + 2)
                        rounded_rect_2d([cutout_w_br, cutout_d_br], brace_corner_r);
    }
}

// -----------------------------------------------------------------------------
// HEAVY-DUTY 12MM UPPER DRIVER PLATES (U1..U4 - 112 x 136 x 12mm)
// -----------------------------------------------------------------------------
module upper_plate_template(plate_id) {
    difference() {
        translate([-upper_plate_w/2, -upper_plate_h/2, 0])
            linear_extrude(height = swap_plate_t)
                rounded_rect_2d([upper_plate_w, upper_plate_h], 4.0);

        // 4x M4 Countersunk Holes: Top (Y_local = +55mm), Bottom on Crossbar (Y_local = -58mm)
        for (sx = [-47, 47]) {
            for (sy = [55, -58]) {
                translate([sx, sy, -1]) {
                    cylinder(d = fastener_d, h = swap_plate_t + 2);
                    translate([0, 0, swap_plate_t + 1 - 2.5])
                        cylinder(d1 = fastener_d, d2 = 8.5, h = 2.6);
                }
            }
        }

        // Driver cutout centered at Y = +5.0mm relative to plate center
        if (plate_id == 1) {
            // PLATE U1: 2" - 2.5" DRIVERS
            translate([0, 5.0, -0.1]) cylinder(d = 68.0, h = 3.0 + 0.1);
            translate([0, 5.0, 2.9]) cylinder(d = 56.0, h = swap_plate_t - 3.0 + 0.2);
            translate([0, 5.0, 2.9]) cylinder(d1 = 56.0, d2 = 72.0, h = swap_plate_t - 3.0 + 0.2);
            for (i = [0 : 3]) {
                angle = 45 + i * 90;
                translate([(62/2)*cos(angle), 5.0 + (62/2)*sin(angle), -1])
                    cylinder(d = 3.5, h = swap_plate_t + 2);
            }
        } else if (plate_id == 2) {
            // PLATE U2: 3" - 3.5" BENCHMARK
            translate([0, 5.0, -0.1]) cylinder(d = 96.0, h = 3.5 + 0.1);
            translate([0, 5.0, 3.4]) cylinder(d = 76.0, h = swap_plate_t - 3.5 + 0.2);
            translate([0, 5.0, 3.4]) cylinder(d1 = 76.0, d2 = 96.0, h = swap_plate_t - 3.5 + 0.2);
            for (i = [0 : 3]) {
                angle = 45 + i * 90;
                translate([(86/2)*cos(angle), 5.0 + (86/2)*sin(angle), -1])
                    cylinder(d = 4.2, h = swap_plate_t + 2);
            }
        } else if (plate_id == 3) {
            // PLATE U3: 3.5" - 4" WOOFERS
            translate([0, 5.0, -0.1]) cylinder(d = 108.0, h = 3.5 + 0.1);
            translate([0, 5.0, 3.4]) cylinder(d = 96.0, h = swap_plate_t - 3.5 + 0.2);
            translate([0, 5.0, 3.4]) cylinder(d1 = 96.0, d2 = 104.0, h = swap_plate_t - 3.5 + 0.2);
            for (i = [0 : 3]) {
                angle = 45 + i * 90;
                translate([(104/2)*cos(angle), 5.0 + (104/2)*sin(angle), -1])
                    cylinder(d = 4.2, h = swap_plate_t + 2);
            }
        } else if (plate_id == 4) {
            // PLATE U4: BLANK SOLID (NO HOLES)
        }
    }
}

module upper_plate_mesh(plate_id) {
    c = (plate_id == 1) ? c_plate_u1 :
        (plate_id == 2) ? c_plate_u2 :
        (plate_id == 3) ? c_plate_u3 : c_plate_u4;
    color(c)
        upper_plate_template(plate_id);
}

// -----------------------------------------------------------------------------
// HEAVY-DUTY 12MM LOWER ACOUSTIC MODULES (P1..P4 - 112 x 70 x 12mm)
// -----------------------------------------------------------------------------
module lower_plate_template(mode) {
    difference() {
        translate([-lower_plate_w/2, -lower_plate_h/2, 0])
            linear_extrude(height = swap_plate_t)
                rounded_rect_2d([lower_plate_w, lower_plate_h], 4.0);

        // 4x M4 Countersunk Holes: Top on Crossbar (Y_local = +25mm), Bottom (Y_local = -23mm)
        for (sx = [-47, 47]) {
            for (sy = [25, -23]) {
                translate([sx, sy, -1]) {
                    cylinder(d = fastener_d, h = swap_plate_t + 2);
                    translate([0, 0, swap_plate_t + 1 - 2.5])
                        cylinder(d1 = fastener_d, d2 = 8.5, h = 2.6);
                }
            }
        }

        // Acoustic center at (0, 0)
        if (mode == 1) {
            // MODULE P1: SEALED (NO HOLES)
        } else if (mode == 2) {
            // MODULE P2: CYLINDRICAL PORT SOCKET
            translate([0, 0, -0.1]) cylinder(d = 53.0, h = 2.5 + 0.1);
            translate([0, 0, 2.4]) cylinder(d = 41.5, h = swap_plate_t - 2.5 + 0.2);
            for (i = [0 : 2]) {
                angle = i * 120;
                translate([(47/2)*cos(angle), (47/2)*sin(angle), -1])
                    cylinder(d = 3.2, h = swap_plate_t + 2);
            }
        } else if (mode == 3) {
            // MODULE P3: SLIT DUCT
            translate([-90/2, -14/2, -0.1])
                linear_extrude(height = swap_plate_t + 0.2)
                    rounded_rect_2d([90, 14], 3.0);
        } else if (mode == 4) {
            // MODULE P4: PASSIVE RADIATOR
            translate([0, 0, -0.1]) cylinder(d = 96.0, h = 3.5 + 0.1);
            translate([0, 0, 3.4]) cylinder(d = 76.0, h = swap_plate_t - 3.5 + 0.2);
            for (i = [0 : 3]) {
                angle = 45 + i * 90;
                translate([(86/2)*cos(angle), (86/2)*sin(angle), -1])
                    cylinder(d = 4.2, h = swap_plate_t + 2);
            }
        }
    }

    if (mode == 2) {
        color([0.10, 0.45, 0.70, 1.0]) {
            translate([0, 0, swap_plate_t]) {
                difference() {
                    union() {
                        cylinder(d = 41.0, h = p2_port_len - swap_plate_t);
                        translate([0, 0, p2_port_len - swap_plate_t - 6.0])
                            rotate_extrude()
                                translate([35/2 + 3.0, 0, 0])
                                    circle(r = 6.0);
                    }
                    translate([0, 0, -1]) cylinder(d = 35.0, h = p2_port_len + 2);
                    translate([0, 0, p2_port_len - swap_plate_t - 6.0])
                        rotate_extrude()
                            translate([35/2 + 6.0, 0, 0])
                                circle(r = 6.0);
                }
            }
        }
    } else if (mode == 3) {
        color([0.15, 0.70, 0.45, 1.0]) {
            translate([-90/2 - 2.0, -14/2 - 2.0, swap_plate_t]) {
                difference() {
                    cube([94.0, 18.0, 120.0 - swap_plate_t]);
                    translate([2.0, 2.0, -1])
                        cube([90.0, 14.0, 120.0 + 2]);
                }
            }
        }
    }
}

module lower_plate_mesh(mode) {
    c = (mode == 1) ? c_plate_p1 :
        (mode == 2) ? c_plate_p2 :
        (mode == 3) ? c_plate_p3 : c_plate_p4;
    color(c)
        lower_plate_template(mode);
}

// "日" Shaped Dual-Window EVA Gasket (Wide 40mm Crossbar)
module ladder_frame_gasket() {
    color(c_gasket)
    difference() {
        translate([-inner_w/2, -inner_h/2, 0])
            linear_extrude(height = gasket_t)
                rounded_rect_2d([inner_w, inner_h], 4.0);

        // Upper Window Cutout: 90 x 106mm
        translate([-upper_win_w/2, (upper_win_y - (panel_t + inner_h/2)) - upper_win_h/2, -0.5])
            linear_extrude(height = gasket_t + 1)
                rounded_rect_2d([upper_win_w, upper_win_h], 5.0);

        // Lower Window Cutout: 90 x 40mm
        translate([-lower_win_w/2, (lower_win_y - (panel_t + inner_h/2)) - lower_win_h/2, -0.5])
            linear_extrude(height = gasket_t + 1)
                rounded_rect_2d([lower_win_w, lower_win_h], 5.0);

        for (sx = [-47, 47]) {
            for (ly = [193 - (panel_t + inner_h/2), 80 - (panel_t + inner_h/2), 60 - (panel_t + inner_h/2), 12 - (panel_t + inner_h/2)]) {
                translate([sx, ly, -0.5])
                    cylinder(d = fastener_d + 1, h = gasket_t + 1);
            }
        }
    }
}

// =============================================================================
// COMPLETE ASSEMBLY
// =============================================================================
module assembled_enclosure(transparent=false) {
    translate([0, outer_h - panel_t, 0])
        panel_top(transparent);

    translate([0, 0, 0])
        panel_bottom(transparent);

    translate([0, panel_t, 0])
        panel_left(transparent);

    translate([outer_w - panel_t, panel_t, 0])
        panel_right(transparent);

    // Front "日" Ladder Frame at Z=16..28mm
    translate([panel_t, panel_t, z_front_frame_start])
        panel_ladder_frame(transparent);

    // Rear "日" Ladder Frame at Z=162..174mm
    translate([panel_t, panel_t, z_rear_frame_start])
        panel_ladder_frame(transparent);

    // Internal Window Brace at Y=82mm, Z=28..162mm
    if (brace_enable) {
        translate([panel_t, split_joint_y - panel_t/2, z_cavity_start])
            panel_brace(transparent);
    }

    // Front EVA Gasket
    translate([outer_w/2, panel_t + inner_h/2, z_front_swap_end - gasket_t])
        ladder_frame_gasket();

    // Front Swappable Upper Driver Plate at Z=4..16mm
    translate([outer_w/2, upper_pos_y, z_front_swap_start])
        upper_plate_mesh(upper_module_plate);

    // Front Swappable Lower Acoustic Module at Z=4..16mm
    translate([outer_w/2, lower_pos_y, z_front_swap_start])
        lower_plate_mesh(lower_module_mode);

    // Rear EVA Gasket
    translate([outer_w/2, panel_t + inner_h/2, z_rear_frame_end])
        ladder_frame_gasket();

    // Rear Upper Solid Blank Plate at Z=174..186mm (NO HOLES)
    translate([outer_w/2, upper_pos_y, z_rear_swap_end])
        rotate([0, 180, 0])
            upper_plate_mesh(4);

    // Rear Lower Solid Blank Plate at Z=174..186mm (NO HOLES)
    translate([outer_w/2, lower_pos_y, z_rear_swap_end])
        rotate([0, 180, 0])
            lower_plate_mesh(1);
}

// =============================================================================
// EXPLODED ASSEMBLY VIEW
// =============================================================================
module exploded_enclosure() {
    d = explode_dist;

    // Front Baffles
    translate([outer_w/2, upper_pos_y, z_front_swap_start - d * 1.8])
        upper_plate_mesh(upper_module_plate);

    translate([outer_w/2, lower_pos_y, z_front_swap_start - d * 1.8])
        lower_plate_mesh(lower_module_mode);

    translate([outer_w/2, panel_t + inner_h/2, z_front_swap_end - d * 1.2])
        ladder_frame_gasket();

    translate([panel_t, panel_t, z_front_frame_start - d * 0.7])
        panel_ladder_frame();

    // Rear Baffles
    translate([panel_t, panel_t, z_rear_frame_start + d * 0.7])
        panel_ladder_frame();

    translate([outer_w/2, panel_t + inner_h/2, z_rear_frame_end + d * 1.2])
        ladder_frame_gasket();

    translate([outer_w/2, upper_pos_y, z_rear_swap_end + d * 1.8])
        rotate([0, 180, 0])
            upper_plate_mesh(4);

    translate([outer_w/2, lower_pos_y, z_rear_swap_end + d * 1.8])
        rotate([0, 180, 0])
            lower_plate_mesh(1);

    // Outer Cabinet Wrapper
    translate([0, -d * 0.8, 0])
        panel_bottom();

    translate([0, outer_h - panel_t + d * 0.8, 0])
        panel_top();

    translate([-d * 0.8, panel_t, 0])
        panel_left();

    translate([outer_w - panel_t + d * 0.8, panel_t, 0])
        panel_right();

    // Center Window Brace
    if (brace_enable) {
        translate([panel_t, split_joint_y - panel_t/2, z_cavity_start])
            panel_brace();
    }
}

// =============================================================================
// MAIN EXECUTION
// =============================================================================
if (view_mode == 0) {
    assembled_enclosure(false);
} else if (view_mode == 1) {
    difference() {
        assembled_enclosure(false);
        translate([outer_w/2, -10, -50])
            cube([outer_w, outer_h + 20, outer_d + 100]);
    }
} else if (view_mode == 2) {
    exploded_enclosure();
} else if (view_mode == 3) {
    assembled_enclosure(true);
}
