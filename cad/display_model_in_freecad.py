# =============================================================================
# FREECAD GUI DISPLAY & COLORING MACRO
# File: cad/display_model_in_freecad.py
# 使い方: FreeCAD GUIを起動し、メニューの「マクロ」→「マクロ...」から本スクリプトを実行、
#         または「ファイル」→「開く」で本ファイルを開いて「緑色の再生ボタン(F6)」を押すと、
#         全パーツが色分け（木材・バッフル・ポート・ガスケット）され、画面中央に綺麗に表示されます。
# =============================================================================

import os
import FreeCAD
import FreeCADGui

# 1. ドキュメントを開く
fcstd_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "speaker_enclosure.FCStd")
if not FreeCAD.ActiveDocument or FreeCAD.ActiveDocument.Name != "SpeakerEnclosure_SplitModular":
    if os.path.exists(fcstd_path):
        doc = FreeCAD.openDocument(fcstd_path)
    else:
        doc = FreeCAD.ActiveDocument
else:
    doc = FreeCAD.ActiveDocument

if doc:
    print("Setting up visual materials and camera for:", doc.Name)
    
    # 2. カラーパレット定義 (R, G, B)
    COLOR_WOOD = (0.86, 0.72, 0.53)        # バーチ合板色（木目）
    COLOR_BAFFLE = (0.22, 0.22, 0.25)      # フロントバッフル（チャコール）
    COLOR_SUB_BAFFLE = (0.15, 0.45, 0.65)  # サブバッフルプレート（ブルー）
    COLOR_PORT = (0.85, 0.35, 0.15)        # バスレフポート（オレンジ）
    COLOR_GASKET = (0.10, 0.10, 0.10)      # EVAガスケット（ブラック）
    COLOR_BRACE = (0.75, 0.60, 0.42)       # 内部ブレース（濃い木目）

    # 3. 各パーツの表示(Visibility)と色(ShapeColor)を設定
    for obj in doc.Objects:
        vo = obj.ViewObject
        if not vo:
            continue
            
        name = obj.Name
        if name in [
            "Split_Main_Front_Baffle", "Top_Panel", "Bottom_Panel",
            "Left_Side_Panel", "Right_Side_Panel", "Rear_Panel", "Internal_Window_Brace",
            "Active_Upper_Plate_U2", "Active_Upper_Gasket",
            "Active_Lower_Plate_P2", "Active_Lower_Gasket", "Active_Port_Tube_120mm"
        ]:
            vo.Visibility = True
            if "Baffle" in name:
                vo.ShapeColor = COLOR_BAFFLE
            elif "Upper_Plate" in name or "Lower_Plate" in name:
                vo.ShapeColor = COLOR_SUB_BAFFLE
            elif "Port" in name:
                vo.ShapeColor = COLOR_PORT
            elif "Gasket" in name:
                vo.ShapeColor = COLOR_GASKET
            elif "Brace" in name:
                vo.ShapeColor = COLOR_BRACE
            else:
                vo.ShapeColor = COLOR_WOOD
        else:
            vo.Visibility = False

    try:
        FreeCADGui.activeDocument().activeView().viewIsometric()
        FreeCADGui.activeDocument().activeView().fitAll()
        FreeCADGui.updateGui()
        print("FreeCAD 3D View successfully initialized with material colors and camera focus!")
    except Exception as e:
        print("View update notice:", e)
