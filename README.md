# 2〜4インチ モジュラー交換式スピーカーエンクロージャー設計プロジェクト

本プロジェクトは、**2〜4インチ（2", 2.5", 3", 3.5", 4"）** の複数のスピーカーユニットを1台のエンクロージャーで手軽に着脱・交換して聴き比べができる「**前後対称デュアル・モジュラー受枠 & 上下2分割バッフルシステム**」を搭載した高音質スピーカーエンクロージャーの完全な設計パッケージです。

音響解析（TSパラメータシミュレーション）、構造設計（FreeCAD 1.0 / STEP / STL / SVG木取り図）、Web 3Dビューワー、製作・BOMマニュアルを包括しています。

---

## 🌟 主な特長

1. **2大モデルの並行展開**:
   - **Model 1: 3.2L コンパクト机上版** ($136 \times 230 \times 190\text{ mm}$): デスクトップ・ニアフィールドに最適。
   - **Model 2: 5.5L 本格ダブルバスレフ (DBR) 版** ($136 \times 310 \times 210\text{ mm}$): 8cmユニット（F02408H2等）から 50Hz の超重低音を引き出す本格設計。
2. **上段ユニットバッフルの100%共通互換性**:
   - 上段ユニットバッフル ($112 \times 136 \times 12\text{ mm}$) は **3.2L版と5.5L版で完全同一規格**。一度作ったユニットプレートは両方の箱で使い回し可能。
3. **前後対称デュアル「日の字」型受枠 ＋ 重厚12mm二重構造**:
   - 前面・背面に幅40mmの極太中央横桟を備えた「日の字型インナー受枠」を配置。
   - 外周受け部は合計24mmの極厚ダブルバッフル構造となり、大振幅時の箱鳴り・たわみを徹底排除。
4. **背面拡張性（ソリッド密閉 ⇄ バイポーラ/プッシュプル/リアポート）**:
   - 初期状態は背面に穴なしソリッド密閉板を装着。将来的に背面にもユニットやパッシブラジエーター（PR）を即座に増設可能。
5. **インタラクティブ Web 3Dビューワー (`cad/3d_viewer.html`)**:
   - ブラウザ上で360度回転、ズーム、3.2L/5.5Lのリアルタイム切替、右側板の断面（Cutaway）表示、分解（Explode）表示に対応。

---

## 📐 ユニット & モジュール対応表

### 【上段】ユニット交換バッフル (12mm厚・共通規格 $112 \times 136\text{ mm}$)
- **Plate U1 (2"〜2.5")**: Dayton DMA45, ND65, Peerless PLS等
- **Plate U2 (3"〜3.5" 標準)**: 北日本音響 F02408H2 / F02408H0, Dayton ND91-4, PS95-8, MarkAudio Alpair 5v3, Fostex FE83NV2等
- **Plate U3 (3.5"〜4")**: Dayton TCP115, MarkAudio Pluvia 7, Fostex FE103NV2等
- **Plate U4 (ブランク)**: 自由加工・CNC用

### 【下段】音響形式交換バッフル (12mm厚)
- **Module P1 (完全密閉型)**: 穴なしソリッド密閉板 ($Q_{tc} \approx 0.70$)
- **Module P2 (バスレフポート)**: 3.2L版: $\varnothing 32\text{ mm} \times 120\text{ mm}$ ($F_b=95\text{Hz}$) / 5.5L版: 大口径 $\varnothing 45\text{ mm} \times 130\text{ mm}$ ($F_b=51\text{Hz}$)
- **Module P3 (前面スリットダクト)**: 前面開口スリット
- **Module P4 (パッシブラジエーター)**: 3〜4インチ パッシブラジエーター

---

## 📁 ディレクトリ構成

```
Speaker-Enclosure/
├── README.md                           # 本総合ガイド
├── docs/                               # 各分野の詳細技術ドキュメント
│   ├── 01_acoustic_design.md           # [音響設計書] 3.2L / 5.5L DBR 理論・シミュレーション
│   ├── 02_enclosure_drawings.md        # [構造・図面仕様書] 詳細寸法、前後対称日の字受枠、ネジ配置
│   └── 03_bom_and_assembly.md          # [製作・BOMマニュアル] 材料費、木工・3Dプリント・組立手順
├── sim/                                # 音響シミュレーションスクリプト & データ
│   ├── acoustic_sim.py                 # 9機種×多形式対応シミュレータ (Python 3)
│   ├── acoustic_simulation_plot.png    # 周波数応答・インピーダンス・変位・風速グラフ (PNG)
│   ├── acoustic_simulation_plot.svg    # ベクターグラフ (SVG)
│   └── simulation_summary.json         # 計算結果数値データ (JSON)
└── cad/                                # 3Dモデル & 2D製図データ
    ├── 3d_viewer.html                  # Three.js インタラクティブ 3D Web ビューワー
    ├── speaker_enclosure.FCStd         # 3.2L版 FreeCAD 1.0 ネイティブプロジェクト
    ├── speaker_enclosure_5.5L.FCStd    # 5.5L版 FreeCAD 1.0 ネイティブプロジェクト
    ├── speaker_enclosure.step          # 3.2L版 STEP 3D CAD 中間ファイル
    ├── speaker_enclosure_5.5L.step     # 5.5L版 STEP 3D CAD 中間ファイル
    ├── enclosure.scad                  # OpenSCAD パラメトリック3Dモデル
    ├── cutlist_drawings.svg            # 3.2L版 2D木取り図面 (SVG)
    ├── cutlist_drawings_5.5L.svg       # 5.5L版 2D木取り図面 (SVG)
    └── stl/                            # 3Dプリント用 STL メッシュ (全パーツ)
        └── 5.5L/                       # 5.5L版 専用 STL メッシュ
```

---

## 🚀 使い方

### 1. 3Dモデル・構造をブラウザで確認
ブラウザで [`cad/3d_viewer.html`](cad/3d_viewer.html) を開いてください。
- 左上のモデル選択で「3.2L コンパクト」と「5.5L 本格DBR」を瞬時に切り替え可能。
- 「✂️ 右側板 断面表示」ボタンで内部構造を確認可能。
- 「Explode」スライダーで各バッフルパーツの分解構造を確認可能。

### 2. FreeCAD 1.0 で 3Dソリッドを編集
FreeCAD 1.0 を起動し、[`cad/speaker_enclosure.FCStd`](cad/speaker_enclosure.FCStd) または [`cad/speaker_enclosure_5.5L.FCStd`](cad/speaker_enclosure_5.5L.FCStd) を開いてください。

### 3. 音響シミュレーションの再実行
```powershell
python sim/acoustic_sim.py
```
