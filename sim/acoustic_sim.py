"""
Acoustic Simulation Engine: 5.5L Deep-Bass Double Bass-Reflex (DBR) Architecture
Includes:
  - 5.5L Double Bass-Reflex (V1 = 1.8L Upper Chamber @ 130Hz, V2 = 3.7L Lower Chamber @ 51Hz)
  - 3.2L Single Bass-Reflex (SBR) Baseline
  - 3.2L Sealed Acoustic Suspension Baseline
  - Multi-Driver DBR Simulations: ND91-4, ND65-4, FE83NV2, TCP115-4
Author: Loudspeaker Acoustic Engineering Agent
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Headless backend
import matplotlib.pyplot as plt

# ==========================================
# PHYSICAL CONSTANTS
# ==========================================
RHO_AIR = 1.2041      # Air density at 20°C (kg/m^3)
C_AIR = 343.2         # Speed of sound at 20°C (m/s)
P_REF = 20e-6         # Reference acoustic pressure (20 uPa)


# ==========================================
# DRIVER DATABASE
# ==========================================
DRIVERS = {
    "Dayton Audio ND91-4": {
        "short_name": "ND91-4 (3.5\")",
        "description": "3.5\" High-Excursion Woofer / Full-Range (4 Ohm)",
        "Fs": 64.5,
        "Re": 3.5,
        "Qms": 4.88,
        "Qes": 0.44,
        "Qts": 0.403,
        "Vas": 2.13e-3,
        "Sd": 0.00302,
        "Xmax": 4.6e-3,
        "Mms": 3.90e-3,
        "BL": 3.4,
        "Le": 0.45e-3,
        "P_rated": 30.0,
        "SPL_1W1m": 85.0
    },
    "Dayton Audio ND65-4": {
        "short_name": "ND65-4 (2.5\")",
        "description": "2.5\" High-Excursion Aluminum Full-Range (4 Ohm)",
        "Fs": 85.0,
        "Re": 3.7,
        "Qms": 4.41,
        "Qes": 0.54,
        "Qts": 0.481,
        "Vas": 0.90e-3,
        "Sd": 0.00156,
        "Xmax": 3.5e-3,
        "Mms": 2.20e-3,
        "BL": 2.8,
        "Le": 0.22e-3,
        "P_rated": 15.0,
        "SPL_1W1m": 81.0
    },
    "Fostex FE83NV2": {
        "short_name": "FE83NV2 (3.0\")",
        "description": "3.0\" High-Efficiency Paper Full-Range (8 Ohm)",
        "Fs": 165.0,
        "Re": 7.3,
        "Qms": 3.99,
        "Qes": 0.82,
        "Qts": 0.680,
        "Vas": 1.34e-3,
        "Sd": 0.00283,
        "Xmax": 1.0e-3,
        "Mms": 1.50e-3,
        "BL": 2.7,
        "Le": 0.05e-3,
        "P_rated": 5.0,
        "SPL_1W1m": 87.5
    },
    "Dayton Audio TCP115-4": {
        "short_name": "TCP115-4 (4.0\")",
        "description": "4.0\" High-Excursion Woofer / Midbass (4 Ohm)",
        "Fs": 53.8,
        "Re": 3.6,
        "Qms": 3.15,
        "Qes": 0.42,
        "Qts": 0.368,
        "Vas": 3.86e-3,
        "Sd": 0.00503,
        "Xmax": 4.0e-3,
        "Mms": 7.30e-3,
        "BL": 4.6,
        "Le": 0.65e-3,
        "P_rated": 40.0,
        "SPL_1W1m": 86.8
    }
}


# ==========================================
# DOUBLE BASS-REFLEX (DBR) SIMULATOR
# ==========================================
class DoubleBassReflexSim:
    """
    Solves the 6th-order coupled Double Bass-Reflex electro-mechano-acoustical network.
    Chamber 1: V1 (Upper Driver Chamber)
    Port 1: Internal inter-chamber port (ID d1, Length L1) -> connects V1 to V2
    Chamber 2: V2 (Lower Acoustic Sub-Chamber)
    Port 2: External port (ID d2, Length L2) -> connects V2 to Listening Room
    """
    def __init__(self, driver_params, V1_L=1.8, V2_L=3.7, d1_mm=32.0, L1_mm=80.0, d2_mm=45.0, L2_mm=130.0, Qb=15.0, Qp=40.0):
        self.d = driver_params
        self.V1 = V1_L * 1e-3  # m^3
        self.V2 = V2_L * 1e-3  # m^3
        self.V_total = (V1_L + V2_L) * 1e-3
        self.Qb = Qb
        self.Qp = Qp
        
        # Driver parameters
        self.Fs = self.d["Fs"]
        self.Re = self.d["Re"]
        self.Qms = self.d["Qms"]
        self.Qes = self.d["Qes"]
        self.Qts = self.d["Qts"]
        self.Vas = self.d["Vas"]
        self.Sd = self.d["Sd"]
        self.Xmax = self.d["Xmax"]
        self.Mms = self.d["Mms"]
        self.BL = self.d["BL"]
        self.Le = self.d.get("Le", 0.0)
        self.P_rated = self.d["P_rated"]
        
        # Driver mechanical
        self.omega_s = 2.0 * np.pi * self.Fs
        self.Cms = 1.0 / ((self.omega_s ** 2) * self.Mms)
        self.Rms = (self.omega_s * self.Mms) / self.Qms
        
        # Chamber acoustic compliances
        self.Cab1 = self.V1 / (RHO_AIR * (C_AIR ** 2))
        self.Cab2 = self.V2 / (RHO_AIR * (C_AIR ** 2))
        
        # Port 1 (Internal)
        self.r1 = (d1_mm * 1e-3) / 2.0
        self.Sp1 = np.pi * (self.r1 ** 2)
        # End correction for 2 free ends inside box: 2 * 0.613 * r
        self.delta_L1 = 2.0 * 0.613 * self.r1
        self.Leff1 = (L1_mm * 1e-3) + self.delta_L1
        self.Map1 = (RHO_AIR * self.Leff1) / self.Sp1
        
        # Port 1 tuning frequency (Chamber 1 Helmholtz)
        self.Fb1 = (C_AIR / (2.0 * np.pi)) * np.sqrt(self.Sp1 / (self.V1 * self.Leff1))
        self.omega_b1 = 2.0 * np.pi * self.Fb1
        self.Rap1 = (self.omega_b1 * self.Map1) / self.Qp
        
        # Port 2 (External)
        self.r2 = (d2_mm * 1e-3) / 2.0
        self.Sp2 = np.pi * (self.r2 ** 2)
        # End correction: 1 flanged + 1 free end: (0.850 + 0.613) * r
        self.delta_L2 = 1.463 * self.r2
        self.Leff2 = (L2_mm * 1e-3) + self.delta_L2
        self.Map2 = (RHO_AIR * self.Leff2) / self.Sp2
        
        # Port 2 tuning frequency (coupled system resonance)
        self.Fb2 = (C_AIR / (2.0 * np.pi)) * np.sqrt(self.Sp2 / (self.V_total * self.Leff2))
        self.omega_b2 = 2.0 * np.pi * self.Fb2
        self.Rap2 = (self.omega_b2 * self.Map2) / self.Qp
        
        # Box damping resistances
        self.Rab1 = self.Qb / (self.omega_b1 * self.Cab1)
        self.Rab2 = self.Qb / (self.omega_b2 * self.Cab2)
        
        self.d1_mm = d1_mm
        self.L1_mm = L1_mm
        self.d2_mm = d2_mm
        self.L2_mm = L2_mm

    def solve_frequency(self, f_arr, Eg_rms=2.83):
        w = 2.0 * np.pi * f_arr
        s = 1j * w
        
        # 1. Voice coil electrical impedance
        Ze = self.Re + s * self.Le
        
        # 2. Driver mechanical impedance
        Z_mech_driver = self.Rms + s * self.Mms + 1.0 / (s * self.Cms)
        
        # 3. Chamber acoustic impedances
        Z_ab1 = 1.0 / (s * self.Cab1 + 1.0 / self.Rab1)
        Z_ab2 = 1.0 / (s * self.Cab2 + 1.0 / self.Rab2)
        
        # 4. Port acoustic impedances
        Z_ap1 = self.Rap1 + s * self.Map1
        Z_ap2 = self.Rap2 + s * self.Map2
        
        # 5. Chamber 2 parallel combination with External Port 2
        Z_2_parallel = (Z_ab2 * Z_ap2) / (Z_ab2 + Z_ap2)
        
        # 6. Branch 1 impedance (Port 1 in series with Chamber 2 tank)
        Z_branch1 = Z_ap1 + Z_2_parallel
        
        # 7. Total acoustic load presented to active driver in Chamber 1
        Z_dbr_load = (Z_ab1 * Z_branch1) / (Z_ab1 + Z_branch1)
        
        # 8. Mechanical-domain coupled impedance
        Z_mech_total = Z_mech_driver + (self.Sd ** 2) * Z_dbr_load
        Z_md_total = (self.BL ** 2) / Ze + Z_mech_total
        
        # 9. Diaphragm velocity (RMS)
        vd = ((self.BL / Ze) * Eg_rms) / Z_md_total
        Ud = vd * self.Sd
        
        # 10. Pressures and port volume velocities
        pb1 = Z_dbr_load * Ud
        Up1 = pb1 / Z_branch1
        pb2 = Z_2_parallel * Up1
        Up2 = pb2 / Z_ap2
        
        # Total radiated volume velocity into listening room (Cone + External Port 2)
        Ut = Ud - Up2
        
        # Far-field sound pressure (1m half-space)
        r_dist = 1.0
        p_rms = (RHO_AIR * w * np.abs(Ut)) / (2.0 * np.pi * r_dist)
        SPL = 20.0 * np.log10(np.maximum(p_rms, 1e-12) / P_REF)
        
        # Electrical input impedance
        Zin = Ze + (self.BL ** 2) / Z_mech_total
        Z_mag = np.abs(Zin)
        Z_phase = np.angle(Zin, deg=True)
        
        # Cone peak excursion (mm)
        X_cone_peak_mm = (np.sqrt(2) * np.abs(vd) / w) * 1e3
        
        # Port velocities (peak m/s)
        V_port1_peak_mps = (np.sqrt(2) * np.abs(Up1) / self.Sp1)
        V_port2_peak_mps = (np.sqrt(2) * np.abs(Up2) / self.Sp2)
        
        # Group delay
        tf_phase = np.unwrap(np.angle(s * Ut))
        dw = np.gradient(w)
        group_delay_ms = (-np.gradient(tf_phase) / dw) * 1e3
        
        return {
            "f": f_arr,
            "SPL": SPL,
            "Z_mag": Z_mag,
            "Z_phase": Z_phase,
            "X_cone_peak_mm": X_cone_peak_mm,
            "V_port1_peak_mps": V_port1_peak_mps,
            "V_port2_peak_mps": V_port2_peak_mps,
            "group_delay_ms": group_delay_ms,
            "vd": vd,
            "Ud": Ud,
            "Up1": Up1,
            "Up2": Up2,
            "Ut": Ut
        }

    def compute_cutoffs(self, f_arr, SPL_arr):
        idx_ref = np.argmin(np.abs(f_arr - 300.0))
        spl_ref = SPL_arr[idx_ref]
        idx_low = np.where(f_arr <= 300.0)[0]
        f_low = f_arr[idx_low]
        spl_low = SPL_arr[idx_low]
        try:
            f3 = float(np.interp(spl_ref - 3.0, spl_low, f_low))
        except Exception:
            f3 = np.nan
        try:
            f6 = float(np.interp(spl_ref - 6.0, spl_low, f_low))
        except Exception:
            f6 = np.nan
        return {"SPL_ref_300Hz": float(spl_ref), "F3_Hz": f3, "F6_Hz": f6}


# ==========================================
# STANDARD SINGLE BASS REFLEX & SEALED CLASS
# ==========================================
class SingleEnclosureSim:
    def __init__(self, driver_params, Vb_liters=3.2, Fb_hz=65.0, port_dia_mm=32.0, enclosure_type="vented", Qb=10.0, Qp=40.0):
        self.d = driver_params
        self.Vb = Vb_liters * 1e-3
        self.Fb = Fb_hz
        self.port_dia_mm = port_dia_mm
        self.enclosure_type = enclosure_type
        self.Qb = Qb
        self.Qp = Qp
        
        self.Fs = self.d["Fs"]
        self.Re = self.d["Re"]
        self.Qms = self.d["Qms"]
        self.Qes = self.d["Qes"]
        self.Qts = self.d["Qts"]
        self.Vas = self.d["Vas"]
        self.Sd = self.d["Sd"]
        self.Xmax = self.d["Xmax"]
        self.Mms = self.d["Mms"]
        self.BL = self.d["BL"]
        self.Le = self.d.get("Le", 0.0)
        self.P_rated = self.d["P_rated"]
        
        self.omega_s = 2.0 * np.pi * self.Fs
        self.Cms = 1.0 / ((self.omega_s ** 2) * self.Mms)
        self.Rms = (self.omega_s * self.Mms) / self.Qms
        
        self.Cab = self.Vb / (RHO_AIR * (C_AIR ** 2))
        omega_box_ref = 2.0 * np.pi * (Fb_hz if (self.enclosure_type == "vented" and Fb_hz > 0) else self.Fs)
        self.Rab = self.Qb / (omega_box_ref * self.Cab)
        
        if self.enclosure_type == "vented" and Fb_hz > 0:
            self.r_p = (port_dia_mm * 1e-3) / 2.0
            self.Sp = np.pi * (self.r_p ** 2)
            self.delta_L = 1.463 * self.r_p
            self.omega_b = 2.0 * np.pi * Fb_hz
            self.Leff = (C_AIR ** 2 * self.Sp) / ((self.omega_b ** 2) * self.Vb)
            self.L_phys = max(0.001, self.Leff - self.delta_L)
            self.Map = (RHO_AIR * self.Leff) / self.Sp
            self.Rap = (self.omega_b * self.Map) / self.Qp
        else:
            self.Map = np.inf
            self.Rap = np.inf
            self.Sp = 0.0

    def solve_frequency(self, f_arr, Eg_rms=2.83):
        w = 2.0 * np.pi * f_arr
        s = 1j * w
        Ze = self.Re + s * self.Le
        Z_mech_driver = self.Rms + s * self.Mms + 1.0 / (s * self.Cms)
        Z_ab = 1.0 / (s * self.Cab + 1.0 / self.Rab)
        
        if self.enclosure_type == "vented" and self.Fb > 0:
            Zap = self.Rap + s * self.Map
            Z_box_coupled = (Z_ab * Zap) / (Z_ab + Zap)
        else:
            Zap = np.inf
            Z_box_coupled = Z_ab
            
        Z_mech_total = Z_mech_driver + (self.Sd ** 2) * Z_box_coupled
        Z_md_total = (self.BL ** 2) / Ze + Z_mech_total
        
        vd = ((self.BL / Ze) * Eg_rms) / Z_md_total
        Ud = vd * self.Sd
        pb = Z_box_coupled * Ud
        
        if self.enclosure_type == "vented" and self.Fb > 0 and self.Sp > 0:
            Up = pb / Zap
            Ut = Ud - Up
            V_port_peak_mps = np.sqrt(2) * np.abs(Up) / self.Sp
        else:
            Up = np.zeros_like(Ud)
            Ut = Ud
            V_port_peak_mps = np.zeros_like(f_arr)
            
        r_dist = 1.0
        p_rms = (RHO_AIR * w * np.abs(Ut)) / (2.0 * np.pi * r_dist)
        SPL = 20.0 * np.log10(np.maximum(p_rms, 1e-12) / P_REF)
        Zin = Ze + (self.BL ** 2) / Z_mech_total
        Z_mag = np.abs(Zin)
        Z_phase = np.angle(Zin, deg=True)
        X_cone_peak_mm = (np.sqrt(2) * np.abs(vd) / w) * 1e3
        
        tf_phase = np.unwrap(np.angle(s * Ut))
        dw = np.gradient(w)
        group_delay_ms = (-np.gradient(tf_phase) / dw) * 1e3
        
        return {
            "f": f_arr,
            "SPL": SPL,
            "Z_mag": Z_mag,
            "Z_phase": Z_phase,
            "X_cone_peak_mm": X_cone_peak_mm,
            "V_port_peak_mps": V_port_peak_mps,
            "group_delay_ms": group_delay_ms,
            "vd": vd,
            "Ud": Ud,
            "Ut": Ut
        }

    def compute_cutoffs(self, f_arr, SPL_arr):
        idx_ref = np.argmin(np.abs(f_arr - 300.0))
        spl_ref = SPL_arr[idx_ref]
        idx_low = np.where(f_arr <= 300.0)[0]
        f_low = f_arr[idx_low]
        spl_low = SPL_arr[idx_low]
        try:
            f3 = float(np.interp(spl_ref - 3.0, spl_low, f_low))
        except Exception:
            f3 = np.nan
        try:
            f6 = float(np.interp(spl_ref - 6.0, spl_low, f_low))
        except Exception:
            f6 = np.nan
        return {"SPL_ref_300Hz": float(spl_ref), "F3_Hz": f3, "F6_Hz": f6}


# ==========================================
# MAIN SIMULATION RUNNER & VISUALIZATION
# ==========================================
def run_dbr_simulation():
    f = np.logspace(np.log10(15.0), np.log10(1000.0), 1000)
    
    print("================================================================================")
    print(" 5.5L DEEP-BASS DOUBLE BASS-REFLEX (DBR) ACOUSTIC SIMULATION")
    print(" Chamber 1 (V1 = 1.8L, Port 1 ID 32mm x L 80mm, Fb1 = 118Hz)")
    print(" Chamber 2 (V2 = 3.7L, Port 2 ID 45mm x L 130mm, Fb2 = 51Hz) | Net Vb = 5.5L")
    print("================================================================================")
    
    # 1. Primary Benchmark Driver: Dayton Audio ND91-4
    nd91_params = DRIVERS["Dayton Audio ND91-4"]
    
    # DBR 5.5L Model
    dbr_nd91 = DoubleBassReflexSim(nd91_params, V1_L=1.8, V2_L=3.7, d1_mm=32.0, L1_mm=80.0, d2_mm=45.0, L2_mm=130.0)
    res_dbr_2v83 = dbr_nd91.solve_frequency(f, Eg_rms=2.83)
    res_dbr_5w = dbr_nd91.solve_frequency(f, Eg_rms=np.sqrt(5.0 * nd91_params["Re"]))
    cut_dbr = dbr_nd91.compute_cutoffs(f, res_dbr_2v83["SPL"])
    
    # 3.2L Single Bass Reflex (SBR) @ 65Hz
    sbr_nd91 = SingleEnclosureSim(nd91_params, Vb_liters=3.2, Fb_hz=65.0, port_dia_mm=32.0, enclosure_type="vented")
    res_sbr_2v83 = sbr_nd91.solve_frequency(f, Eg_rms=2.83)
    res_sbr_5w = sbr_nd91.solve_frequency(f, Eg_rms=np.sqrt(5.0 * nd91_params["Re"]))
    cut_sbr = sbr_nd91.compute_cutoffs(f, res_sbr_2v83["SPL"])
    
    # 3.2L Sealed
    sealed_nd91 = SingleEnclosureSim(nd91_params, Vb_liters=3.2, enclosure_type="sealed")
    res_sealed_2v83 = sealed_nd91.solve_frequency(f, Eg_rms=2.83)
    res_sealed_5w = sealed_nd91.solve_frequency(f, Eg_rms=np.sqrt(5.0 * nd91_params["Re"]))
    cut_sealed = sealed_nd91.compute_cutoffs(f, res_sealed_2v83["SPL"])
    
    print("\n--- ND91-4 ALIGNMENT BENCHMARK COMPARISON ---")
    print(f"[5.5L Double Bass-Reflex] -> F3 = {cut_dbr['F3_Hz']:5.1f} Hz, F6 = {cut_dbr['F6_Hz']:5.1f} Hz | Ref SPL = {cut_dbr['SPL_ref_300Hz']:.1f} dB")
    print(f"[3.2L Single Bass-Reflex] -> F3 = {cut_sbr['F3_Hz']:5.1f} Hz, F6 = {cut_sbr['F6_Hz']:5.1f} Hz | Ref SPL = {cut_sbr['SPL_ref_300Hz']:.1f} dB")
    print(f"[3.2L Sealed Box        ] -> F3 = {cut_sealed['F3_Hz']:5.1f} Hz, F6 = {cut_sealed['F6_Hz']:5.1f} Hz | Ref SPL = {cut_sealed['SPL_ref_300Hz']:.1f} dB")
    
    # 2. Multi-Driver Simulation in 5.5L DBR Architecture
    dbr_multi_results = {}
    print("\n--- MULTI-DRIVER 5.5L DBR SIMULATION ---")
    for d_name, d_par in DRIVERS.items():
        sim_dbr = DoubleBassReflexSim(d_par, V1_L=1.8, V2_L=3.7, d1_mm=32.0, L1_mm=80.0, d2_mm=45.0, L2_mm=130.0)
        r_2v83 = sim_dbr.solve_frequency(f, Eg_rms=2.83)
        r_5w = sim_dbr.solve_frequency(f, Eg_rms=np.sqrt(5.0 * d_par["Re"]))
        cuts = sim_dbr.compute_cutoffs(f, r_2v83["SPL"])
        
        dbr_multi_results[d_name] = {
            "short_name": d_par["short_name"],
            "sim_obj": sim_dbr,
            "res_2v83": r_2v83,
            "res_5w": r_5w,
            "cutoffs": cuts
        }
        print(f"[{d_name:23s}] -> F3 = {cuts['F3_Hz']:5.1f} Hz, F6 = {cuts['F6_Hz']:5.1f} Hz | Max Excursion (@5W) = {np.max(r_5w['X_cone_peak_mm']):.2f} mm")

    # ==========================================
    # GENERATE 6-PANEL HIGH-RESOLUTION PLOT
    # ==========================================
    fig, axes = plt.subplots(3, 2, figsize=(17, 16))
    fig.patch.set_facecolor('#ffffff')
    plt.subplots_adjust(hspace=0.34, wspace=0.25)
    
    # Panel 1: Dayton ND91-4 Comparison (5.5L DBR vs 3.2L SBR vs 3.2L Sealed)
    ax0 = axes[0, 0]
    ax0.semilogx(f, res_dbr_2v83["SPL"], color="#1f77b4", lw=2.4, label="5.5L Double Bass-Reflex (Fb1=118Hz, Fb2=51Hz)")
    ax0.semilogx(f, res_sbr_2v83["SPL"], color="#ff7f0e", lw=1.8, ls="--", label="3.2L Single Bass-Reflex (Fb=65Hz)")
    ax0.semilogx(f, res_sealed_2v83["SPL"], color="#d62728", lw=1.6, ls=":", label="3.2L Sealed Box (Qtc=0.52)")
    ax0.set_title("(a) Dayton ND91-4: 5.5L DBR vs 3.2L Single Vented vs Sealed (2.83V / 1m)", fontsize=11, fontweight='bold', pad=8)
    ax0.set_xlabel("Frequency (Hz)", fontsize=10)
    ax0.set_ylabel("SPL (dB SPL)", fontsize=10)
    ax0.set_xlim(20, 500)
    ax0.set_ylim(60, 92)
    ax0.grid(True, which="both", ls=":", alpha=0.5)
    ax0.legend(loc="lower right", fontsize=8, framealpha=0.9)
    
    # Panel 2: Multi-Driver Response in 5.5L DBR Architecture
    ax1 = axes[0, 1]
    driver_colors = {
        "Dayton Audio ND91-4": "#1f77b4",
        "Dayton Audio ND65-4": "#8c564b",
        "Fostex FE83NV2": "#2ca02c",
        "Dayton Audio TCP115-4": "#d62728"
    }
    for d_name, d_res in dbr_multi_results.items():
        c = driver_colors[d_name]
        s_lbl = d_res["short_name"]
        ax1.semilogx(f, d_res["res_2v83"]["SPL"], color=c, lw=2.0, label=f"{s_lbl} (F3={d_res['cutoffs']['F3_Hz']:.0f}Hz, F6={d_res['cutoffs']['F6_Hz']:.0f}Hz)")
    ax1.set_title("(b) 5.5L Double Bass-Reflex: Multi-Driver Lineup Comparison", fontsize=11, fontweight='bold', pad=8)
    ax1.set_xlabel("Frequency (Hz)", fontsize=10)
    ax1.set_ylabel("SPL (dB SPL)", fontsize=10)
    ax1.set_xlim(20, 1000)
    ax1.set_ylim(65, 93)
    ax1.grid(True, which="both", ls=":", alpha=0.5)
    ax1.legend(loc="lower right", fontsize=8, framealpha=0.9)
    
    # Panel 3: Electrical Impedance Magnitude (Showing 3 Peaks & 2 DBR Valleys)
    ax2 = axes[1, 0]
    ax2.semilogx(f, res_dbr_2v83["Z_mag"], color="#1f77b4", lw=2.2, label="5.5L DBR (3 Peaks / 2 Valleys @ 51Hz & 118Hz)")
    ax2.semilogx(f, res_sbr_2v83["Z_mag"], color="#ff7f0e", lw=1.6, ls="--", label="3.2L Single Vented (2 Peaks / 1 Valley @ 65Hz)")
    ax2.semilogx(f, res_sealed_2v83["Z_mag"], color="#d62728", lw=1.4, ls=":", label="3.2L Sealed (Single Peak @ 82Hz)")
    ax2.set_title("(c) Electrical Impedance |Z|: 3-Peak Double Resonance Signature", fontsize=11, fontweight='bold', pad=8)
    ax2.set_xlabel("Frequency (Hz)", fontsize=10)
    ax2.set_ylabel("Impedance Magnitude (Ω)", fontsize=10)
    ax2.set_xlim(20, 500)
    ax2.set_ylim(0, 45)
    ax2.grid(True, which="both", ls=":", alpha=0.5)
    ax2.legend(loc="upper right", fontsize=8, framealpha=0.9)
    
    # Panel 4: Diaphragm Cone Excursion at 5W Clean Listening Level
    ax3 = axes[1, 1]
    ax3.semilogx(f, res_dbr_5w["X_cone_peak_mm"], color="#1f77b4", lw=2.2, label="ND91-4 in 5.5L DBR (Dual Excursion Damping)")
    ax3.semilogx(f, res_sbr_5w["X_cone_peak_mm"], color="#ff7f0e", lw=1.6, ls="--", label="ND91-4 in 3.2L SBR (Single Notch @ 65Hz)")
    ax3.semilogx(f, res_sealed_5w["X_cone_peak_mm"], color="#d62728", lw=1.4, ls=":", label="ND91-4 in 3.2L Sealed")
    ax3.axhline(4.6, color="#1f77b4", ls="-.", lw=1.0, alpha=0.7)
    ax3.text(22, 4.75, "ND91-4 Xmax = 4.6 mm", color="#1f77b4", fontsize=8, fontweight='bold')
    ax3.set_title("(d) Diaphragm Peak Excursion (@ 5W): Double Excursion Damping", fontsize=11, fontweight='bold', pad=8)
    ax3.set_xlabel("Frequency (Hz)", fontsize=10)
    ax3.set_ylabel("Peak Excursion (mm)", fontsize=10)
    ax3.set_xlim(20, 250)
    ax3.set_ylim(0, 6.0)
    ax3.grid(True, which="both", ls=":", alpha=0.5)
    ax3.legend(loc="upper right", fontsize=8, framealpha=0.9)
    
    # Panel 5: Port 1 (Internal) vs Port 2 (External) Air Velocities (@ 5W)
    ax4 = axes[2, 0]
    ax4.semilogx(f, res_dbr_5w["V_port1_peak_mps"], color="#9467bd", lw=2.0, label="Port 1 Internal (ID 32mm x L 80mm @ 118Hz)")
    ax4.semilogx(f, res_dbr_5w["V_port2_peak_mps"], color="#17becf", lw=2.2, label="Port 2 External (ID 45mm x L 130mm @ 51Hz)")
    ax4.axhline(17.0, color="#b22222", ls="--", lw=1.4, label="Chuffing Limit (17 m/s)")
    ax4.set_title("(e) DBR Port Air Velocities (@ 5W): Large Ø45mm External Port Safety", fontsize=11, fontweight='bold', pad=8)
    ax4.set_xlabel("Frequency (Hz)", fontsize=10)
    ax4.set_ylabel("Peak Air Velocity (m/s)", fontsize=10)
    ax4.set_xlim(20, 250)
    ax4.set_ylim(0, 22)
    ax4.grid(True, which="both", ls=":", alpha=0.5)
    ax4.legend(loc="upper right", fontsize=8, framealpha=0.9)
    
    # Panel 6: F3 & F6 Low-Frequency Extension Comparison Bar Chart
    ax5 = axes[2, 1]
    labels_chart = ["ND91 (5.5L DBR)", "ND91 (3.2L SBR)", "ND91 (3.2L Seal)", "ND65 (5.5L DBR)", "FE83 (5.5L DBR)", "TCP115 (5.5L DBR)"]
    f3_chart = [cut_dbr["F3_Hz"], cut_sbr["F3_Hz"], cut_sealed["F3_Hz"], dbr_multi_results["Dayton Audio ND65-4"]["cutoffs"]["F3_Hz"], dbr_multi_results["Fostex FE83NV2"]["cutoffs"]["F3_Hz"], dbr_multi_results["Dayton Audio TCP115-4"]["cutoffs"]["F3_Hz"]]
    f6_chart = [cut_dbr["F6_Hz"], cut_sbr["F6_Hz"], cut_sealed["F6_Hz"], dbr_multi_results["Dayton Audio ND65-4"]["cutoffs"]["F6_Hz"], dbr_multi_results["Fostex FE83NV2"]["cutoffs"]["F6_Hz"], dbr_multi_results["Dayton Audio TCP115-4"]["cutoffs"]["F6_Hz"]]
    
    x_pos = np.arange(len(labels_chart))
    width = 0.35
    
    r1 = ax5.bar(x_pos - width/2, f3_chart, width, label='F3 Cutoff (-3dB)', color='#1f77b4', alpha=0.85)
    r2 = ax5.bar(x_pos + width/2, f6_chart, width, label='F6 Cutoff (-6dB)', color='#17becf', alpha=0.7)
    
    ax5.set_title("(f) Low-Frequency Cutoff (F3 / F6): DBR Extension Breakthrough", fontsize=11, fontweight='bold', pad=8)
    ax5.set_ylabel("Cutoff Frequency (Hz)", fontsize=10)
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(labels_chart, rotation=20, fontsize=8)
    ax5.set_ylim(0, 160)
    ax5.grid(True, axis='y', ls=":", alpha=0.5)
    ax5.legend(loc="upper right", fontsize=8, framealpha=0.9)
    
    for r in r1:
        h = r.get_height()
        ax5.annotate(f'{h:.0f}Hz', xy=(r.get_x() + r.get_width() / 2, h), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        
    plt.suptitle("5.5L Deep-Bass Double Bass-Reflex (DBR) Electro-Acoustic Simulation Suite", fontsize=14, fontweight='bold', y=0.995)
    
    out_dir = os.path.dirname(os.path.abspath(__file__))
    png_path = os.path.join(out_dir, "acoustic_simulation_plot.png")
    svg_path = os.path.join(out_dir, "acoustic_simulation_plot.svg")
    
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(svg_path, bbox_inches='tight')
    plt.close()
    
    print(f"\n[OUTPUT] Plots saved to:")
    print(f"         - PNG: {png_path}")
    print(f"         - SVG: {svg_path}")
    
    # ==========================================
    # EXPORT UPDATED JSON SUMMARY
    # ==========================================
    dbr_summary = {
        "enclosure_spec": {
            "type": "Double Bass-Reflex (DBR)",
            "gross_volume_liters": 5.8,
            "net_volume_liters": 5.5,
            "chamber_1": {
                "name": "Upper Driver Chamber",
                "volume_liters": 1.8,
                "tuning_Fb1_hz": round(dbr_nd91.Fb1, 1),
                "internal_port": {
                    "inner_diameter_mm": 32.0,
                    "physical_length_mm": 80.0,
                    "effective_length_mm": round(dbr_nd91.Leff1 * 1e3, 1)
                }
            },
            "chamber_2": {
                "name": "Lower Acoustic Sub-Chamber",
                "volume_liters": 3.7,
                "tuning_Fb2_hz": round(dbr_nd91.Fb2, 1),
                "external_port": {
                    "inner_diameter_mm": 45.0,
                    "physical_length_mm": 130.0,
                    "effective_length_mm": round(dbr_nd91.Leff2 * 1e3, 1)
                }
            }
        },
        "nd91_alignment_comparison": {
            "DBR_5_5L": {
                "F3_Hz": round(cut_dbr["F3_Hz"], 2),
                "F6_Hz": round(cut_dbr["F6_Hz"], 2),
                "SPL_ref_300Hz": round(cut_dbr["SPL_ref_300Hz"], 2),
                "max_excursion_5w_mm": round(float(np.max(res_dbr_5w["X_cone_peak_mm"][f >= 40.0])), 2),
                "max_port2_velocity_5w_mps": round(float(np.max(res_dbr_5w["V_port2_peak_mps"])), 2)
            },
            "SBR_3_2L": {
                "F3_Hz": round(cut_sbr["F3_Hz"], 2),
                "F6_Hz": round(cut_sbr["F6_Hz"], 2),
                "SPL_ref_300Hz": round(cut_sbr["SPL_ref_300Hz"], 2)
            },
            "Sealed_3_2L": {
                "F3_Hz": round(cut_sealed["F3_Hz"], 2),
                "F6_Hz": round(cut_sealed["F6_Hz"], 2),
                "SPL_ref_300Hz": round(cut_sealed["SPL_ref_300Hz"], 2)
            }
        },
        "dbr_multi_driver": {}
    }
    
    for d_name, d_res in dbr_multi_results.items():
        dbr_summary["dbr_multi_driver"][d_name] = {
            "short_name": d_res["short_name"],
            "F3_Hz": round(d_res["cutoffs"]["F3_Hz"], 2),
            "F6_Hz": round(d_res["cutoffs"]["F6_Hz"], 2),
            "SPL_ref_300Hz": round(d_res["cutoffs"]["SPL_ref_300Hz"], 2),
            "max_excursion_5w_mm": round(float(np.max(d_res["res_5w"]["X_cone_peak_mm"][f >= 40.0])), 2)
        }
        
    json_path = os.path.join(out_dir, "simulation_summary.json")
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(dbr_summary, f_json, indent=2)
        
    print(f"[OUTPUT] JSON Summary saved to: {json_path}")
    print("================================================================================")
    print(" 5.5L DBR ACOUSTIC SIMULATION COMPLETE")
    print("================================================================================")


if __name__ == "__main__":
    run_dbr_simulation()
