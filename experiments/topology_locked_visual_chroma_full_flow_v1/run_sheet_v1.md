# Topology-locked visual-chroma full-flow v1 run sheet

Date: 2026-05-27

## 1. Status

- status: `complete_rescue_only_archived_diagnostic`
- candidate family: `Stage1-only new method family after FA01`
- not allowed name: `FF03`, `P29`, `D02`
- current role: archived diagnostic test of whether a complete Stage1 enhancement flow can keep raw-compatible luma topology under fixed detectors.

## 2. Inputs

- smoke raw input dir: `data/inputImg/Original`
- validated 168 raw input dir: `D:/Desktop/MyEdgeCodex/input_test/algae`
- smoke manifest: `experiments/topology_locked_visual_chroma_full_flow_v1/manifests/smoke5_highrisk_v1.txt`
- config: `experiments/topology_locked_visual_chroma_full_flow_v1/configs/topology_locked_visual_chroma_full_flow_v1.json`
- output root: `experiments/topology_locked_visual_chroma_full_flow_v1/outputs/smoke5_highrisk_v1`

Smoke stems:

- `weixiaoyuanjia.26`
- `xuehong.9`
- `donghaiyuanjia.26`
- `tama.14`
- `jianci.4`

## 3. Method Contract

This run must keep the full Stage1 branch skeleton:

`Original -> BPH -> IMF1Ray / RGHS / CLAHE -> Fused -> Final`

But it changes the Final formation contract:

- raw Lab-L is the topology anchor;
- BPH contributes bounded low-frequency illumination;
- IMF/RGHS/CLAHE contribute only bounded weak-boundary luma residuals;
- BPH/RGHS/CLAHE primarily drive chroma/color correction;
- background risk suppresses luma residuals;
- entropy/homomorphic closure is disabled.

## 4. Execution Commands

Windows PowerShell:

```powershell
$sw = [System.Diagnostics.Stopwatch]::StartNew()
D:\Desktop\DeepLearning\my_env\python.exe main.py `
  --input-dir data\inputImg\Original `
  --manifest experiments\topology_locked_visual_chroma_full_flow_v1\manifests\smoke5_highrisk_v1.txt `
  --output-dir experiments\topology_locked_visual_chroma_full_flow_v1\outputs\smoke5_highrisk_v1 `
  --params-json experiments\topology_locked_visual_chroma_full_flow_v1\configs\topology_locked_visual_chroma_full_flow_v1.json
$sw.Stop()
$sw.Elapsed.TotalSeconds
```

Then summarize with a local or generic smoke summarizer. The summary must include output completeness, decode failures, raw-vs-Final metrics and visual panels.

## 5. Smoke Gate

Pass only if:

- six-stage JPG/PNG outputs are complete for all smoke stems;
- decode failures are `0`;
- projected 168 runtime is no more than `10` minutes;
- visual/chroma delta is nontrivial and not raw-near;
- high-risk panels do not show FF01/FF02-style background false structure;
- grad/luma ratios stay close enough to raw to justify a 25-image broader smoke.

Fail if:

- output is visually near raw;
- luma topology drifts enough to suggest detector failure;
- background false-edge risk appears in `weixiaoyuanjia.26`, `tama.14`, or `jianci.4`;
- runtime exceeds the 10-minute projected 168 budget.

## 6. Boundary

TLVC01 has now completed fixed-detector validation through isolated MyEdge roots.

Do not run 502/496 or 2770 from TLVC01 as candidate promotion. Those remain blocked because the 168 downstream gate is `candidate_rescues_legacy_but_not_near_raw`.

## 7. Execution Result

Actual 168 output:

- output root: `experiments/topology_locked_visual_chroma_full_flow_v1/outputs/myedge168_v1_myedgeinput_grayplane090_anchorfix`
- status report: `experiments/topology_locked_visual_chroma_full_flow_v1/topology_locked_visual_chroma_full_flow_v1_myedge168_v1_myedgeinput_grayplane090_anchorfix_status_20260527.md`
- fixed-detector status: `experiments/topology_locked_visual_chroma_full_flow_v1/topology_locked_visual_chroma_full_flow_v1_fixed_detector_tlvc01_status_20260527.md`
- MyEdge result intake: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_results_20260527.md`
- MyEdge structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_structure_metrics_20260527.md`
- MyEdge downstream gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_downstream_gate_20260527.md`

Decision:

- TLVC01 rescues legacy Stage1 Final collapse on both fixed detectors.
- It is not a strict candidate pass because MSFI AC misses near-raw tolerance and DiffusionEdge structure proxy is mixed.
- Stop this Stage1-only direct replacement family here; do not create TLVC02 as a same-family small fix.
