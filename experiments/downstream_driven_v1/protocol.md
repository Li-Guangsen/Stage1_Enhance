# Downstream-driven Stage1 Variant Protocol

Date: 2026-05-25

This protocol is for diagnostic variants only. It does not replace the locked
Stage1 paper mainline:

- locked config: `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- locked result: `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`

## Motivation

Completed fixed-detector diagnostics show that the legacy Stage1 enhanced
outputs hurt downstream edge detection under both DiffusionEdge baseline 50k and
MSFI 50k. The new variants therefore prioritize downstream edge preservation:
keep the raw spatial/luminance structure close to the detector training domain
and transfer only mild color/illumination information from Stage1.

## Variants

| Variant | Config | Intended role |
|---|---|---|
| `edge_preserve_original_control` | `configs/edge_preserve_original_control.json` | Chain sanity check. Final equals resized original. |
| `edge_preserve_raw_bph_mild_v1` | `configs/edge_preserve_raw_bph_mild_v1.json` | Mild Lab blend: original luminance dominant, small BPH chroma transfer. |
| `edge_preserve_raw_bph_moderate_v1` | `configs/edge_preserve_raw_bph_moderate_v1.json` | Moderate Lab blend for testing the damage/benefit boundary. |
| `generic_luma_clahe_mild_v1` | `configs/generic_luma_clahe_mild_v1.json` | Generic luminance-only CLAHE control. Tests whether P4/P5C signals are Stage1/BPH-specific or just generic contrast perturbation. |
| `generic_luma_gamma_mild_v1` | `configs/generic_luma_gamma_mild_v1.json` | Generic luminance-only gamma/contrast control. Tests whether P4/P5C signals are Stage1/BPH-specific or just generic brightness perturbation. |
| `edge_safe_gamma_bph_v1` | `configs/edge_safe_gamma_bph_v1.json` | Hybrid candidate after P4/P7: raw-domain mild gamma/contrast plus small BPH chroma transfer, skipping legacy high-frequency/fusion/final stages. |
| `boundary_aware_luma_bph_v1` | `configs/boundary_aware_luma_bph_v1.json` | Boundary-aware candidate after the harm/degradation diagnostic: raw-domain clipped luminance adjustment, low-gradient background smoothing, high-gradient masked unsharp support, and mild BPH chroma transfer. |
| `skeleton_safe_luma_bph_v1` | `configs/skeleton_safe_luma_bph_v1.json` | Skeleton-safe smooth-only candidate after the P10 proxy: no luminance enhancement or unsharp, very small BPH chroma transfer, low-gradient smoothing, and a tighter luma-delta cap. |
| `degradation_aware_pyramid_frequency_v1` | `configs/degradation_aware_pyramid_frequency_v1.json` | First multi-module downstream-driven candidate after P11: per-image luma score search, Retinex/CLAHE/gamma branches, raw/BPH detail support, edge/background masks, background-aware chroma transfer, and luma-delta cap. |
| `calibrated_pyramid_frequency_v1` | `configs/calibrated_pyramid_frequency_v1.json` | P13 calibrated variant after P12: keeps the degradation-aware multi-branch search but lowers luma/chroma/detail strength and adds raw-edge rescue/global raw blending to recover AP/AC while keeping pseudo-edge suppression. |
| `weak_boundary_pyramid_fusion_v1` | `configs/weak_boundary_pyramid_fusion_v1.json` | P14 weak-boundary local-fusion variant after P13: combines a skeleton-safe raw/BPH base with a degradation-aware pyramid-frequency candidate only in low-contrast weak-boundary regions, with pseudo-edge suppression, raw-edge rescue and luma-delta caps. |
| `c01_microstructure_csp_v1` | `configs/c01_microstructure_csp_v1.json` | P16 first candidate from the 2026-05-26 downstream-driven method synthesis: clipped gray-world/color compensation, bright/dark local feature residuals, weak-structure residuals, texture-risk guard, and fallback to near-raw when gradient/local-variance guard fails. |
| `topology_guarded_microfusion_v1` | `configs/topology_guarded_microfusion_v1.json` | P17 topology-guarded candidate: uses P16 microstructure-CSP as base, injects P15 weak-boundary fusion only in stable low-risk boundary regions, and adds pseudo-edge/spur suppression plus per-image gradient guards. |
| `topology_pruned_microfusion_v1` | `configs/topology_pruned_microfusion_v1.json` | P18 topology-pruned candidate: wraps the P17 topology-guarded candidate with detector-domain pseudo-edge component pruning outside raw edge support, then applies global/background gradient fallback guards. |
| `baseline_stabilized_microfusion_v1` | `configs/baseline_stabilized_microfusion_v1.json` | P19 baseline-stabilized candidate: reuses the topology-pruned framework but softens component pruning, widens raw-edge support, and tightens candidate-side gradient/variance guards to reduce DiffusionEdge baseline false-edge/endpoints damage without over-pruning true weak boundaries. |
| `endpoint_stabilized_weak_boundary_v1` | `configs/endpoint_stabilized_weak_boundary_v1.json` | P20 endpoint-stabilized candidate: wraps a weak-boundary branch with raw/base pullback for newly introduced off-support components, thin spurs and high-risk background gradients to test whether baseline-side endpoints can be reduced without returning to legacy Final damage. |
| `balanced_weak_boundary_pyramid_fusion_v1` | `configs/balanced_weak_boundary_pyramid_fusion_v1.json` | P21 balanced weak-boundary candidate: interpolates the P14 weak-boundary local-fusion signal and the later raw-near guard settings, aiming to preserve the P14/P20 rescue effect while reducing baseline-side endpoint damage. |
| `ac_guarded_weak_boundary_fusion_v1` | `configs/ac_guarded_weak_boundary_fusion_v1.json` | P22 AC/false-edge guarded weak-boundary candidate: wraps the P21-like weak-boundary signal with off-support pseudo-edge pruning, support-gradient floor, raw/base pullback and luma-delta fallback guards. |
| `precision_rebalanced_ac_guarded_weak_boundary_fusion_v1` | `configs/precision_rebalanced_ac_guarded_weak_boundary_fusion_v1.json` | P23 precision-rebalanced AC/false-edge guarded candidate: rebalances P22 toward baseline-side AC/endpoints while keeping support unsharp disabled after proxy endpoint risk. |
| `false_edge_floor_ac_guarded_weak_boundary_fusion_v1` | `configs/false_edge_floor_ac_guarded_weak_boundary_fusion_v1.json` | P24 false-edge-floor candidate: tightens P23 background/off-support false-edge suppression; useful as a false-edge diagnostic but causes a large MSFI AP drop. |
| `ap_preserving_ac_guarded_weak_boundary_fusion_v1` | `configs/ap_preserving_ac_guarded_weak_boundary_fusion_v1.json` | P25 AP-preserving pullback from P24 toward P23: recovers MSFI AP and metric-near-raw status, but baseline structure proxy remains mixed. |
| `dual_anchor_false_edge_floor_v1` | `configs/dual_anchor_false_edge_floor_v1.json` | P26 dual-anchor false-edge floor candidate: wraps a P25-like weak-boundary anchor with detector-domain off-support/small-component/line-risk suppression; rescues legacy damage but remains mixed on MSFI AC and baseline false-edge/endpoints. |
| `raw_detail_lowfreq_chroma_v1` | `configs/raw_detail_lowfreq_chroma_v1.json` | P27 raw-detail low-frequency chroma candidate: preserves raw high-frequency/luma detail and adjusts only low-frequency illumination/chroma from BPH evidence; reaches metric-near-raw on both fixed detectors, but baseline structure proxy remains mixed. |

## First evaluation scope

Start with the MyEdge 168-image ALGAE test split because it has GT edge maps and
can close the downstream metric loop quickly. If a variant is not at least
edge-safe on 168 images, do not run the 2770-image full pool.

Suggested first Stage1 command shape:

```powershell
python main.py `
  --input-dir D:\Desktop\MyEdgeCodex\input_test\algae `
  --output-dir experiments\downstream_driven_v1\outputs\myedge168\<variant> `
  --params-json experiments\downstream_driven_v1\configs\<variant>.json
```

## Success gates

- Sanity gate: `edge_preserve_original_control` should reproduce the raw
  detector anchor within evaluation noise.
- Edge-safe gate: a variant should avoid the large ODS/OIS/AP/AC drop seen in
  legacy `Final`.
- Positive gate: a variant can only be called downstream-improving if it beats
  the raw fixed-detector anchor on the reported downstream metrics without a
  material AP/AC regression.

## Hard stops

- Do not overwrite the locked full506 mainline outputs.
- Do not run the 2770-image full pool until a 168-image GT run gives a useful
  downstream signal.
- Do not write these variants as paper results until the MyEdge sampling/eval
  outputs, report assets, and Stage1/MyEdge status documents are synchronized.

## Executed status on 2026-05-25

Implemented in `main.py` without changing the locked formal mainline:

- `pipeline.save_intermediate_stages=false` for fast diagnostic variants.
- `final.mode=original`, used by `edge_preserve_original_control`.
- `final.mode=edge_preserve_blend`, used by mild/moderate raw-BPH blends.
- `final.mode=generic_luma_clahe`, used by a luminance-only CLAHE generic control.
- `final.mode=generic_luma_gamma`, used by a luminance-only gamma/contrast generic control.
- `final.mode=edge_safe_gamma_bph`, used by the hybrid gamma+BPH candidate.

Stage1 168-image outputs were generated under:

- `experiments/downstream_driven_v1/outputs/myedge168/edge_preserve_original_control`
- `experiments/downstream_driven_v1/outputs/myedge168/edge_preserve_raw_bph_mild_v1`
- `experiments/downstream_driven_v1/outputs/myedge168/edge_preserve_raw_bph_moderate_v1`
- `experiments/downstream_driven_v1/outputs/myedge168/generic_luma_clahe_mild_v1`
- `experiments/downstream_driven_v1/outputs/myedge168/generic_luma_gamma_mild_v1`

MyEdge fixed-MSFI P4 results were synchronized at
`D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\downstream_variant_p4_results_20260525.md`.

| Input variant | ODS | OIS | AP | AC |
|---|---:|---:|---:|---:|
| historical raw MSFI anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| edge_preserve_original_control | 0.783082 | 0.794168 | 0.337353 | 0.7972 |
| edge_preserve_raw_bph_mild_v1 | 0.782743 | 0.793599 | 0.345909 | 0.7957 |
| edge_preserve_raw_bph_moderate_v1 | 0.782999 | 0.794527 | 0.345952 | 0.7952 |
| legacy_stage1_final_p1 | 0.588287 | 0.671357 | 0.263997 | 0.7403 |

Interpretation boundary:

- Legacy Stage1 Final clearly hurts fixed-detector downstream edge metrics.
- `edge_preserve_raw_bph_moderate_v1` largely removes that damage and is close
  to the raw anchor.
- Against the same-round original-control run, the moderate variant improves
  OIS/AP but has a small AC drop.
- This is an edge-safe candidate, not stable evidence that Stage1 enhancement
  beats raw input.

The selected moderate variant was also run on `full502_clean_v1` without
overwriting formal outputs:

- Output root: `experiments/downstream_driven_v1/outputs/full502/edge_preserve_raw_bph_moderate_v1`
- Final PNG count: `502`
- Final JPG count: `502`

Do not run the 2770-image pool from this protocol until repeat/control and
generic enhancement controls confirm a stable positive downstream signal.

## Generic controls P7 fixed-detector status on 2026-05-25

The two generic luminance-only controls were generated for the MyEdge 168-image
split without changing the locked Stage1 mainline:

- `generic_luma_clahe_mild_v1`: Final PNG `168`, Final JPG `168`, OpenCV decode failures `0`.
- `generic_luma_gamma_mild_v1`: Final PNG `168`, Final JPG `168`, OpenCV decode failures `0`.

MyEdge fixed-detector sampling/eval/show and report-asset sync are complete:

- MSFI result summary: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\generic_control_p7_msfi_results_20260525.md`
- DiffusionEdge baseline result summary: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\generic_control_p7_baseline_results_20260525.md`
- Structure proxy summary: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\generic_control_p7_structure_metrics_20260525.md`
- Paired structure review: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\generic_control_p7_structure_paired_review_20260525.md`
- MSFI preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\generic_control_p7_msfi_preflight_20260525.md`
- DiffusionEdge baseline preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\generic_control_p7_baseline_preflight_20260525.md`

P7 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI generic CLAHE | 0.781721 | 0.793016 | 0.345003 | 0.7934 |
| MSFI generic gamma | 0.782883 | 0.794223 | 0.345982 | 0.7952 |
| MSFI legacy Stage1 Final | 0.588287 | 0.671357 | 0.263997 | 0.7403 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline generic CLAHE | 0.769295 | 0.784093 | 0.366887 | 0.7915 |
| DiffusionEdge baseline generic gamma | 0.771645 | 0.782024 | 0.371366 | 0.7936 |
| DiffusionEdge baseline legacy Stage1 Final | 0.530094 | 0.567910 | 0.224073 | 0.7349 |

Boundary:

- P7 is a 168-image lightweight luminance-only control diagnostic.
- Generic gamma is near raw under MSFI and has a small ODS/OIS/AP positive signal
  under DiffusionEdge baseline, while AC remains below raw.
- P7 structure proxy and paired review are complete. MSFI/gamma vs raw has
  F1/precision/recall/false-edge/components/endpoints deltas of
  `+0.000692/+0.003978/-0.002338/-0.003978/-0.4290/-1.1210`;
  DiffusionEdge baseline/gamma remains mixed with
  `-0.000688/-0.004253/+0.002480/+0.004253/-0.1828/+0.2251`.
- P8 repeat/control has now been executed for P4/P5C/P7. It supports
  repeatability of the main P4/P5C/P7 rows, but generic gamma controls remain
  competitive and baseline-side structure remains mixed.
- Do not claim stable Stage1 downstream benefit from P7.

## Edge-safe Gamma+BPH candidate status on 2026-05-25

After the legacy `Final` negative diagnostics and the P4/P7 near-raw signals, a
new non-mainline candidate was added:

- Config: `configs/edge_safe_gamma_bph_v1.json`
- Final mode: `edge_safe_gamma_bph`
- Smoke status: `edge_safe_gamma_bph_v1_smoke_status_20260525.md`
- MyEdge168 Stage1 status:
  `edge_safe_gamma_bph_v1_myedge168_stage1_status_20260525.md`
- Smoke output root:
  `experiments/downstream_driven_v1/outputs/smoke_myedge168/edge_safe_gamma_bph_v1`
- MyEdge168 output root:
  `experiments/downstream_driven_v1/outputs/myedge168/edge_safe_gamma_bph_v1`

This mode keeps the raw luminance structure close to the detector input domain,
adds only mild gamma/contrast adjustment to raw Lab luminance, and transfers a
small amount of BPH Lab chroma. It intentionally skips IMF1Ray, RGHS, CLAHE,
Fusion and the legacy Final stage.

Smoke result:

| Output | Count |
| --- | ---: |
| Final PNG | 2 |
| Final JPG | 2 |
| non-Final stage files | 0 |
| decoded Final PNG sample | 2 |

MyEdge168 Stage1 output result:

| Output | Count |
| --- | ---: |
| Final PNG | 168 |
| Final JPG | 168 |
| non-Final stage files | 0 |
| decoded Final PNG | 168 |

Boundary:

- This is Stage1 code-path and I/O readiness only.
- No MyEdge sampling, WSL `eval.py`, WSL `show.py`, ODS/OIS/AP/AC, structure
  proxy, or training was run.
- The 168-image Stage1 outputs are ready for MyEdge-side staging, sampling and
  evaluation under fixed MSFI and DiffusionEdge baseline detectors.
- Do not run full502/full2770 from this smoke alone.

## Repeat-control P8 status on 2026-05-26

MyEdge-side P8 repeat/control assets and results:

- Run sheet: `D:\Desktop\MyEdgeCodex\docs\research_contracts\stage1_repeat_control_p8_run_sheet_v1.md`
- Preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\stage1_repeat_control_p8_preflight_20260525.md`
- Preflight JSON: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\stage1_repeat_control_p8_preflight_20260525.json`
- Result intake script: `D:\Desktop\MyEdgeCodex\docs\paper_assets\scripts\sync_stage1_repeat_control_p8_results.py`
- Result intake: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\stage1_repeat_control_p8_results_20260525.md`
- Structure proxy: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\stage1_repeat_control_p8_structure_metrics_20260525.md`
- Gate: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\stage1_repeat_control_p8_gate_20260525.md`
- Eval/show script: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\run_stage1_repeat_control_p8_eval_show_20260525.sh`

P8 covers 5 input variants x 2 fixed detectors, for 10 planned runs:

- Input variants: `edge_preserve_original_control`,
  `edge_preserve_raw_bph_mild_v1`, `edge_preserve_raw_bph_moderate_v1`,
  `generic_luma_clahe_mild_v1`, `generic_luma_gamma_mild_v1`.
- Fixed detectors: `msfi_50k` and `diffusionedge_baseline_50k`.
- Scope: MyEdge 168-image ALGAE test split.
- Current result intake status: `complete_with_report_assets`; 10 P8 runs are
  complete.
- Structure proxy status: `complete`.
- Gate decision: `repeat_stable_but_control_competitive_no_stage1_specific_upgrade`.

Boundary:

- This is an executed 168-image repeat/control diagnostic, not a new Stage1
  formal mainline.
- P8 upgrades the main P4/P5C/P7 rows from one-shot outputs to
  repeat-supported diagnostics, but it does not prove Stage1-specific positive
  downstream benefit.
- Do not expand any P8 row to full502/full2770 from this gate.
- Multi-run WSL commands must use the generated `.sh` script or another script
  file. Do not wrap Bash variables/arrays/loops in a PowerShell double-quoted
  `$cmd`, because PowerShell will expand `$run`, `$root`, `$PY`, and similar
  Bash variables before WSL receives the command.

## Boundary-aware Luma-BPH P10 candidate status on 2026-05-25

After the harm/degradation diagnostic showed that legacy `Final` damages
low-contrast, blurred-contour, false-edge-background, thin-structure, and
overlap/clutter automatic candidates, a new non-mainline candidate was added:

- Config: `configs/boundary_aware_luma_bph_v1.json`
- Final mode: `boundary_aware_luma_bph`
- MyEdge168 Stage1 status:
  `boundary_aware_luma_bph_v1_myedge168_stage1_status_20260525.md`
- MyEdge168 output root:
  `experiments/downstream_driven_v1/outputs/myedge168/boundary_aware_luma_bph_v1`

This mode keeps raw spatial structure close to the fixed-detector input domain.
It applies clipped mild gamma/contrast in Lab luminance, lightly smooths
low-gradient background with bilateral filtering, adds masked unsharp support
only at higher-gradient pixels, limits the maximum Lab luminance delta, and
transfers only a small amount of BPH chroma. It intentionally skips IMF1Ray,
RGHS, CLAHE, Fusion and the legacy Final stage.

Stage1 output result:

| Output | Count |
| --- | ---: |
| Final PNG | 168 |
| Final JPG | 168 |
| non-Final stage files | 0 |
| decoded Final PNG | 168 |

MyEdge-side P10 preflight assets have been generated:

- Preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\boundary_aware_luma_bph_p10_preflight_20260525.md`
- Preflight JSON: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\boundary_aware_luma_bph_p10_preflight_20260525.json`
- Eval/show script: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\run_boundary_aware_luma_bph_p10_eval_show_20260525.sh`
- Result intake: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\boundary_aware_luma_bph_p10_results_20260525.md`
- Structure proxy intake: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\boundary_aware_luma_bph_p10_structure_metrics_20260525.md`
- Scope: 1 input variant x 2 fixed detectors, 168-image MyEdge ALGAE split.
- Current status: both planned runs are `ready_for_sampling_after_confirmation=True`.
- Current result intake status: `ready_not_executed`; both P10 runs are `not_started`.
- Current structure proxy status: `blocked_by_missing_p10_core_results`; no
  structure metrics are generated while P10 MAT/eval outputs are missing.
- Planned output roots do not exist.

Execution update:

- MyEdge fixed-detector P10 sampling/eval/show, result intake, structure proxy,
  and downstream gate were later completed.
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\boundary_aware_luma_bph_p10_results_20260525.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\boundary_aware_luma_bph_p10_structure_metrics_20260525.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\boundary_aware_luma_bph_p10_downstream_gate_20260525.md`

P10 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI boundary_aware_luma_bph_v1 | 0.783227 | 0.794862 | 0.345977 | 0.7938 |
| DiffusionEdge baseline boundary_aware_luma_bph_v1 | 0.771931 | 0.783864 | 0.371160 | 0.7936 |

P10 gate decision: `candidate_rescues_legacy_but_not_near_raw`. It rescues the
legacy Final damage but is weaker than P11 on the MSFI and baseline-side
structure trade-off, so it is not a new mainline candidate.

## Skeleton-safe Luma-BPH P11 candidate status on 2026-05-25

After the P10 proxy improved F1 and false-edge ratio but still increased
skeleton endpoints, a stricter non-mainline candidate was added:

- Config: `configs/skeleton_safe_luma_bph_v1.json`
- Final mode: `boundary_aware_luma_bph`
- Smoke status:
  `skeleton_safe_luma_bph_v1_smoke_status_20260525.md`
- MyEdge168 Stage1 status:
  `skeleton_safe_luma_bph_v1_myedge168_stage1_status_20260525.md`
- Smoke output root:
  `experiments/downstream_driven_v1/outputs/smoke_myedge168/skeleton_safe_luma_bph_v1`
- MyEdge168 output root:
  `experiments/downstream_driven_v1/outputs/myedge168/skeleton_safe_luma_bph_v1`

This variant keeps raw luminance almost unchanged, disables unsharp support,
uses only low-gradient bilateral smoothing, and transfers a very small amount
of BPH chroma. It intentionally skips IMF1Ray, RGHS, CLAHE, Fusion and the
legacy Final stage.

Smoke result:

| Output | Count |
| --- | ---: |
| Final PNG | 2 |
| Final JPG | 2 |
| non-Final stage files | 0 |
| decoded Final PNG sample | 2 |

MyEdge168 Stage1 output result:

| Output | Count |
| --- | ---: |
| Final PNG | 168 |
| Final JPG | 168 |
| non-Final stage files | 0 |
| decoded Final PNG | 168 |

MyEdge fixed-detector P11 execution is complete:

- MSFI result summary:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\skeleton_safe_luma_bph_p11_results_20260525.md`
- Structure proxy summary:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\skeleton_safe_luma_bph_p11_structure_metrics_20260525.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\skeleton_safe_luma_bph_p11_downstream_gate_20260525.md`

P11 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI skeleton_safe_luma_bph_v1 | 0.784173 | 0.795553 | 0.346803 | 0.7947 |
| MSFI legacy Stage1 Final | 0.588287 | 0.671357 | 0.263997 | 0.7403 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline skeleton_safe_luma_bph_v1 | 0.773642 | 0.782955 | 0.374479 | 0.7934 |
| DiffusionEdge baseline legacy Stage1 Final | 0.530094 | 0.567910 | 0.224073 | 0.7349 |

Structure proxy and gate reading:

- MSFI P11 is raw-near and structure non-worse: dF1 `+0.0016`,
  dFalse-edge ratio `-0.0025`, dEndpoints/kpx `-0.6906`.
- DiffusionEdge baseline P11 rescues the legacy Final damage but remains mixed:
  dF1 `+0.0005`, dFalse-edge ratio `+0.0009`, dEndpoints/kpx `+0.1523`.
- Gate decision: `candidate_rescues_legacy_but_not_near_raw`.

Boundary:

- P11 clearly rescues the large legacy `Final` damage on both fixed detectors.
- P11 cannot yet be written as stable downstream improvement because the
  DiffusionEdge baseline-side structure gate is mixed and AC remains below raw.
- Do not run full502/full2770 from this candidate before repeat/control or a
  second candidate check resolves the baseline-side trade-off.

Stage1-side GT edge proxy prescreen is complete and updated:

- Script: `metrics/scripts/build_stage1_myedge168_gt_edge_proxy_prescreen.py`
- Report: `docs/stage1_myedge168_gt_edge_proxy_prescreen_20260525_cn.md`
- Scope: 168-image MyEdge coupling split, 10 input variants, 1680 per-image proxy rows, failures 0.
- Method: Sobel/Otsu image-gradient proxy matched to GT edge maps with 2 px tolerance.
- Key reading: legacy Stage1 `Final` is `proxy_negative_or_risky`; P10
  `boundary_aware_luma_bph_v1` is `proxy_edge_safe_candidate` with dF1
  `+0.001657`, dFalse-edge ratio `-0.001868`, and dEndpoints/kpx `+0.363361`;
  P11 `skeleton_safe_luma_bph_v1` is the current first `proxy_positive_candidate`
  with dF1 `+0.001075`, dFalse-edge ratio `-0.001783`, dEndpoints/kpx
  `-1.302699`, and mean luma delta `0.557185` versus raw.

Boundary:

- This is Stage1 code-path, I/O, and MyEdge preflight readiness only.
- No MyEdge sampling, WSL `eval.py`, WSL `show.py`, ODS/OIS/AP/AC, structure
  metrics, or training was run.
- The Stage1-side GT edge proxy is a prescreen only and cannot be reported as
  detector downstream performance.
- Do not claim downstream benefit until fixed-detector sampling/eval/show,
  result intake, structure proxy and review are complete.
- Do not run full502/full2770 from this candidate before the 168-image fixed
  detector gate is reviewed.

MyEdge-side P11 assets:

- Preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\skeleton_safe_luma_bph_p11_preflight_20260525.md`
- Preflight JSON:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\skeleton_safe_luma_bph_p11_preflight_20260525.json`
- Eval/show script:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\run_skeleton_safe_luma_bph_p11_eval_show_20260525.sh`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\skeleton_safe_luma_bph_p11_results_20260525.md`
- Structure proxy intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\skeleton_safe_luma_bph_p11_structure_metrics_20260525.md`
- Current result intake status: `complete_with_report_assets`; both P11 runs
  have 168 PNG/MAT/NMS outputs and report assets.
- Current structure proxy status: `complete`; structure metrics are generated
  from existing MAT outputs and GT.
- Current downstream gate: `candidate_rescues_legacy_but_not_near_raw`.

## P9/P10/P12 fixed-detector status update on 2026-05-25

P9 `edge_safe_gamma_bph_v1` was executed as a lightweight gamma/BPH control
after the updated objective was tightened:

- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\edge_safe_gamma_bph_p9_results_20260525.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\edge_safe_gamma_bph_p9_structure_metrics_20260525.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\edge_safe_gamma_bph_p9_downstream_gate_20260525.md`

P9 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI edge_safe_gamma_bph_v1 | 0.782174 | 0.793542 | 0.345858 | 0.7948 |
| DiffusionEdge baseline edge_safe_gamma_bph_v1 | 0.770501 | 0.781812 | 0.371082 | 0.7939 |

P9 gate decision: `candidate_metric_near_raw_structure_mixed`. Treat it as a
control, not as the downstream-driven mainline.

P12 `degradation_aware_pyramid_frequency_v1` was added and executed as the
first multi-module downstream-driven candidate after the user allowed large code
changes but required the 168-image fixed-detector gate before any 2770-pool
run:

- Config: `configs/degradation_aware_pyramid_frequency_v1.json`
- Final mode: `degradation_aware_pyramid_frequency_bph`
- Stage1 MyEdge168 status:
  `degradation_aware_pyramid_frequency_v1_myedge168_stage1_status_20260525.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\degradation_aware_pyramid_frequency_p12_preflight_20260525.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\degradation_aware_pyramid_frequency_p12_results_20260525.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\degradation_aware_pyramid_frequency_p12_structure_metrics_20260525.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\degradation_aware_pyramid_frequency_p12_downstream_gate_20260525.md`
- MyEdge-side generic preflight script:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\scripts\prepare_stage1_single_candidate_assets.py`

P12 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI degradation_aware_pyramid_frequency_v1 | 0.786357 | 0.798143 | 0.344136 | 0.7925 |
| MSFI legacy Stage1 Final | 0.588287 | 0.671357 | 0.263997 | 0.7403 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline degradation_aware_pyramid_frequency_v1 | 0.774611 | 0.788854 | 0.376262 | 0.7886 |
| DiffusionEdge baseline legacy Stage1 Final | 0.530094 | 0.567910 | 0.224073 | 0.7349 |

P12 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.000537 | -0.008386 | -1.176925 |
| DiffusionEdge baseline | +0.000003 | -0.000900 | -0.292032 |

P12 gate decision: `candidate_rescues_legacy_but_not_near_raw`. It is better
than legacy Final and has non-worse structure proxies on both detectors, but it
does not pass the strong gate because AP/AC trade-offs remain. Do not write P12
as stable Stage1 downstream improvement.

P12 enhancement-metric checks were also completed without overwriting formal
outputs:

- Stage1 full502 output:
  `experiments/downstream_driven_v1/outputs/full502/degradation_aware_pyramid_frequency_v1`
- full502 metric output:
  `metrics/outputs/evaluate_protocol_v2/downstream_driven_p12_full502_20260525`
- compare496 metric output:
  `metrics/outputs/evaluate_protocol_v2/downstream_driven_p12_compare496_20260525`

P12 vs formal Final on `full502_clean_v1`:

| Method | Count | EME | EMEE | Entropy | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P12 | 502 | 3.1175 | 0.4706 | 4.1219 | 38.9595 | 3.3848 | 0.9941 | 41.3295 | 2.2684 | 8.4089 |
| FormalFinal | 502 | 11.5985 | 0.9510 | 5.6563 | 544.5511 | 14.8472 | 0.7689 | 17.5534 | 4.0918 | 23.9227 |

P12 vs formal Final on `compare9_complete496_v1`:

| Method | Count | EME | EMEE | Entropy | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P12 | 496 | 3.0130 | 0.4652 | 4.1129 | 37.4205 | 3.3176 | 0.9941 | 41.3560 | 2.2933 | 8.2337 |
| FormalFinal | 496 | 11.5094 | 0.9459 | 5.6527 | 543.0379 | 14.8101 | 0.7689 | 17.6237 | 4.1371 | 23.7718 |

Interpretation:

- Legacy Stage1 Final clearly caused fixed-detector downstream edge metric
  drops.
- P9/P10/P11/P12 all rescue the legacy collapse to different degrees.
- P12 is conservative in enhancement metrics: very high MS_SSIM/PSNR relative
  to original, but much weaker EME/Contrast/AvgGra/UCIQE/UIQM than FormalFinal.
- The current actionable direction is not to expand P12/P13/P14 to 2770; either
  run P8 repeat/control, freeze degradation strata for analysis, or define a
  new candidate that can recover baseline-side AC/false-edge trade-offs without
  returning to the legacy visual-enhancement collapse.

WSL rule reinforced:

- Multi-run MyEdge `eval.py`/`show.py` must use generated `.sh` scripts.
- Do not embed Bash variables, arrays, or loops in a PowerShell double-quoted
  `$cmd` passed to `wsl bash -lc "$cmd"`; PowerShell expands `$run`, `$root`,
  `$PY`, and `${run}` before Bash sees them.

## P13 calibrated pyramid-frequency status on 2026-05-25

P13 `calibrated_pyramid_frequency_v1` was added after P12 to test whether raw
edge rescue and global raw blending could recover AP/AC without returning to
the legacy Final collapse:

- Config: `configs/calibrated_pyramid_frequency_v1.json`
- Stage1 status:
  `calibrated_pyramid_frequency_v1_myedge168_stage1_status_20260525.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\calibrated_pyramid_frequency_p13_preflight_20260525.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\calibrated_pyramid_frequency_p13_results_20260525.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\calibrated_pyramid_frequency_p13_structure_metrics_20260525.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\calibrated_pyramid_frequency_p13_downstream_gate_20260525.md`

P13 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI calibrated_pyramid_frequency_v1 | 0.784769 | 0.796472 | 0.345621 | 0.7932 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline calibrated_pyramid_frequency_v1 | 0.774132 | 0.786695 | 0.369667 | 0.7917 |

P13 gate decision: `candidate_rescues_legacy_but_not_near_raw`. It rescues the
legacy Final damage, but it is not a strong pass. Compared with P12, P13 recovers
some MSFI AP/AC trade-off but loses P12's stronger ODS/OIS and baseline AP.

P13 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P13 / full502_clean_v1 | 502 | 2.8379 | 31.6862 | 3.0918 | 0.9974 | 46.7696 | 2.2573 | 7.8690 |
| P13 / compare9_complete496_v1 | 496 | 2.7324 | 30.2551 | 3.0258 | 0.9974 | 46.7865 | 2.2820 | 7.6897 |

Interpretation:

- P13 is more conservative than P12 and much weaker than FormalFinal on
  EME/Contrast/AvgGra/UCIQE/UIQM.
- `MS_SSIM` and `PSNR` are still relative structure consistency to original,
  not GT enhancement quality.
- Do not run P13 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P14 weak-boundary pyramid-fusion status on 2026-05-25

P14 `weak_boundary_pyramid_fusion_v1` was added after P13 to test whether a
local weak-boundary fusion can preserve the P11 skeleton-safe behavior while
adding more task-driven enhancement only where the raw/BPH gradient and local
contrast masks indicate weak cellular boundaries:

- Config: `configs/weak_boundary_pyramid_fusion_v1.json`
- Stage1 status:
  `weak_boundary_pyramid_fusion_v1_myedge168_stage1_status_20260525.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\weak_boundary_pyramid_fusion_p14_preflight_20260525.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\weak_boundary_pyramid_fusion_p14_results_20260525.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\weak_boundary_pyramid_fusion_p14_structure_metrics_20260525.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\weak_boundary_pyramid_fusion_p14_downstream_gate_20260525.md`

P14 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI weak_boundary_pyramid_fusion_v1 | 0.784373 | 0.795164 | 0.346405 | 0.7940 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline weak_boundary_pyramid_fusion_v1 | 0.773454 | 0.784037 | 0.372930 | 0.7935 |

P14 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0017 | -0.0151 | -1.4952 |
| DiffusionEdge baseline | +0.0013 | +0.0034 | -0.1187 |

P14 gate decision: `candidate_rescues_legacy_but_not_near_raw`. It rescues the
legacy Final collapse. MSFI is raw-near and structure non-worse, but the
DiffusionEdge baseline side is still not raw-near/non-worse because AC remains
below raw and false-edge ratio is slightly higher than raw.

P14 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P14 / full502_clean_v1 | 502 | 2.6005 | 26.9240 | 2.7764 | 0.9981 | 47.6219 | 2.2432 | 7.3917 |
| P14 / compare9_complete496_v1 | 496 | 2.4955 | 25.5663 | 2.7122 | 0.9981 | 47.6324 | 2.2674 | 7.2119 |

Interpretation:

- P14 is even more conservative than P13/P12 in Stage1 enhancement metrics.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- P14 can be kept as a diagnostic candidate that rescues the legacy damage, but
  it is not a strong pass and should not be expanded to the 2770-image full pool.

## P15 structure-guarded weak-boundary status on 2026-05-26

P15 `structure_guarded_weak_boundary_v1` was added after P14 to test whether
stronger background guarding, pseudo-edge suppression and raw strong-edge rescue
can improve the baseline-side AC / false-edge trade-off without returning to the
legacy Final collapse:

- Config: `configs/structure_guarded_weak_boundary_v1.json`
- Stage1 status:
  `structure_guarded_weak_boundary_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\structure_guarded_weak_boundary_p15_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\structure_guarded_weak_boundary_p15_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\structure_guarded_weak_boundary_p15_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\structure_guarded_weak_boundary_p15_downstream_gate_20260526.md`

P15 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI structure_guarded_weak_boundary_v1 | 0.784104 | 0.795471 | 0.347023 | 0.7951 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline structure_guarded_weak_boundary_v1 | 0.773201 | 0.782997 | 0.365411 | 0.7953 |

P15 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0033 | -0.0123 | -1.6983 |
| DiffusionEdge baseline | +0.0013 | +0.0017 | +0.1126 |

P15 gate decision: `candidate_metric_near_raw_structure_mixed`. It rescues the
legacy Final collapse and is metric-near-raw on both fixed detectors. The MSFI
side is structure non-worse, but the DiffusionEdge baseline side remains mixed
because false-edge ratio and endpoints are slightly worse than raw.

P15 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P15 / full502_clean_v1 | 502 | 2.5211 | 25.4229 | 2.6947 | 0.9982 | 47.5609 | 2.2555 | 7.2461 |
| P15 / compare9_complete496_v1 | 496 | 2.4151 | 24.1041 | 2.6313 | 0.9981 | 47.5692 | 2.2799 | 7.0637 |

Interpretation:

- P15 is slightly better than P14 on MSFI AP/AC and baseline AC, but it loses
  P14's baseline AP and still has baseline-side structure trade-off.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- P15 remains a non-mainline diagnostic candidate. Do not write it as stable
  Stage1 downstream improvement, and do not expand it to the 2770-image full pool
  from this gate alone.

## P16 C01 microstructure-CSP status on 2026-05-26

P16 `c01_microstructure_csp_v1` implements the first candidate selected by
`docs/downstream_driven_v1_method_design_synthesis_20260526_cn.md`. The intent
is to test a raw-dominant, structure-constrained enhancement path with mild
color stabilization, local bright/dark residual compensation, weak-structure
rescue, background smoothing and explicit gradient/variance guards:

- Config: `configs/c01_microstructure_csp_v1.json`
- Stage1 status:
  `c01_microstructure_csp_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\c01_microstructure_csp_p16_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\c01_microstructure_csp_p16_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\c01_microstructure_csp_p16_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\c01_microstructure_csp_p16_downstream_gate_20260526.md`

P16 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI c01_microstructure_csp_v1 | 0.783352 | 0.795226 | 0.346031 | 0.7948 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline c01_microstructure_csp_v1 | 0.771525 | 0.783504 | 0.370706 | 0.7941 |

P16 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0010 | -0.0101 | -1.2432 |
| DiffusionEdge baseline | -0.0016 | +0.0071 | +0.0941 |

P16 gate decision: `candidate_metric_near_raw_structure_mixed`. It rescues the
legacy Final collapse and is metric-near-raw on both fixed detectors. The MSFI
side is structure non-worse, but the DiffusionEdge baseline side remains mixed.

P16 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P16 / full502_clean_v1 | 502 | 2.6576 | 28.1097 | 2.9418 | 0.9987 | 49.4034 | 2.2439 | 7.5138 |
| P16 / compare9_complete496_v1 | 496 | 2.5661 | 26.6626 | 2.8745 | 0.9987 | 49.4311 | 2.2685 | 7.3591 |

Interpretation:

- P16 is slightly stronger than P15 in EME, Contrast, AvgGra and UIQM while
  keeping high relative structure consistency to original.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- P16 remains a non-mainline diagnostic candidate. Do not write it as stable
  Stage1 downstream improvement, and do not expand it to the 2770-image full pool
  from this gate alone.

## P17 topology-guarded microfusion status on 2026-05-26

P17 `topology_guarded_microfusion_v1` was added after P16 to test whether the
DiffusionEdge baseline-side structure trade-off can be reduced by fusing a
conservative P16 base with P15-style weak-boundary support under explicit
background pseudo-edge and spur guards.

- Config: `configs/topology_guarded_microfusion_v1.json`
- Stage1 status:
  `topology_guarded_microfusion_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\topology_guarded_microfusion_p17_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\topology_guarded_microfusion_p17_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\topology_guarded_microfusion_p17_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\topology_guarded_microfusion_p17_downstream_gate_20260526.md`

P17 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI topology_guarded_microfusion_v1 | 0.784021 | 0.795041 | 0.346753 | 0.7945 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline topology_guarded_microfusion_v1 | 0.771878 | 0.781854 | 0.364359 | 0.7958 |

P17 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0021 | -0.0165 | -1.2064 |
| DiffusionEdge baseline | +0.0005 | +0.0031 | +0.0958 |

P17 gate decision: `candidate_metric_near_raw_structure_mixed`. It rescues the
legacy Final collapse and is metric-near-raw on both fixed detectors. MSFI is
structure non-worse; DiffusionEdge baseline F1 is slightly better than raw, but
false-edge ratio and endpoints remain slightly worse than raw, so P17 is not a
strong pass.

P17 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P17 / full502_clean_v1 | 502 | 2.5393 | 25.6767 | 2.7598 | 0.9989 | 47.7074 | 2.2295 | 7.3876 |
| P17 / compare9_complete496_v1 | 496 | 2.4391 | 24.3284 | 2.6952 | 0.9989 | 47.7089 | 2.2538 | 7.2173 |

Interpretation:

- P17 improves MSFI structure proxy versus raw and slightly improves baseline
  F1, but it does not solve the baseline false-edge/endpoints trade-off.
- Relative to P16, P17 lowers full502 EME/Contrast/AvgGra/UIQM while improving
  MSFI structure proxy; it is therefore useful failure/mixed evidence, not a
  new formal Stage1 mainline.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not expand P17 to the 2770-image full pool from this gate alone.

## P18 topology-pruned microfusion status on 2026-05-26

P18 `topology_pruned_microfusion_v1` was added after P17 to test whether the
remaining DiffusionEdge baseline-side pseudo-edge/endpoints trade-off can be
reduced by pruning candidate-added small edge components outside raw edge
support before the final output is handed to the fixed detectors.

- Config: `configs/topology_pruned_microfusion_v1.json`
- Stage1 status:
  `topology_pruned_microfusion_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\topology_pruned_microfusion_p18_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\topology_pruned_microfusion_p18_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\topology_pruned_microfusion_p18_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\topology_pruned_microfusion_p18_downstream_gate_20260526.md`

P18 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI topology_pruned_microfusion_v1 | 0.783694 | 0.794872 | 0.346526 | 0.7946 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline topology_pruned_microfusion_v1 | 0.772249 | 0.781858 | 0.363790 | 0.7946 |

P18 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0014 | -0.0153 | -1.2397 |
| DiffusionEdge baseline | -0.0006 | +0.0041 | +0.4725 |

P18 gate decision: `candidate_metric_near_raw_structure_mixed`. It rescues the
legacy Final collapse and is metric-near-raw on both fixed detectors. MSFI is
structure non-worse, but DiffusionEdge baseline F1, false-edge ratio and
endpoints remain slightly worse than raw, so P18 is not a strong pass.

P18 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P18 / full502_clean_v1 | 502 | 2.5688 | 26.2070 | 2.7968 | 0.9988 | 48.3252 | 2.2321 | 7.4075 |
| P18 / compare9_complete496_v1 | 496 | 2.4731 | 24.8484 | 2.7316 | 0.9988 | 48.3345 | 2.2563 | 7.2484 |

Interpretation:

- P18 improves MSFI structure proxy versus raw and improves baseline ODS/OIS/AP,
  but it does not solve the baseline false-edge/endpoints trade-off.
- Relative to P17, P18 improves baseline ODS/OIS slightly but worsens baseline
  structure proxy; it is useful mixed evidence, not a new formal Stage1
  mainline.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not expand P18 to the 2770-image full pool from this gate alone.

## P19 baseline-stabilized microfusion status on 2026-05-26

P19 `baseline_stabilized_microfusion_v1` was added after P18 to test a softer
baseline-side stabilization policy. It keeps the P18 detector-domain pruning
concept, but widens raw-edge support, reduces pruning strength, lowers global
raw/base blending, and tightens candidate gradient/variance guards to avoid
P18's baseline-side F1/endpoints regression.

- Config: `configs/baseline_stabilized_microfusion_v1.json`
- Stage1 status:
  `baseline_stabilized_microfusion_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\baseline_stabilized_microfusion_p19_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\baseline_stabilized_microfusion_p19_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\baseline_stabilized_microfusion_p19_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\baseline_stabilized_microfusion_p19_downstream_gate_20260526.md`

P19 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI baseline_stabilized_microfusion_v1 | 0.783842 | 0.795042 | 0.346413 | 0.7959 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline baseline_stabilized_microfusion_v1 | 0.772365 | 0.782127 | 0.364005 | 0.7941 |

P19 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0015 | -0.0158 | -1.4579 |
| DiffusionEdge baseline | -0.0002 | +0.0037 | +0.1113 |

P19 gate decision: `candidate_metric_near_raw_structure_mixed`. It rescues the
legacy Final collapse and is metric-near-raw on both fixed detectors. MSFI is
structure non-worse. DiffusionEdge baseline remains mixed, but relative to P18
the baseline endpoint delta drops from `+0.4725` to `+0.1113`, so P19 is a
useful partial improvement, not a strong pass.

P19 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P19 / full502_clean_v1 | 502 | 2.5649 | 26.1325 | 2.7940 | 0.9989 | 48.0644 | 2.2332 | 7.4023 |
| P19 / compare9_complete496_v1 | 496 | 2.4682 | 24.7803 | 2.7290 | 0.9989 | 48.0723 | 2.2573 | 7.2415 |

Interpretation:

- P19 confirms that softer pruning can reduce the P18 baseline endpoint penalty,
  but it still does not make the DiffusionEdge baseline structure proxy non-worse.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P19 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P20 endpoint-stabilized weak-boundary status on 2026-05-26

P20 `endpoint_stabilized_weak_boundary_v1` was added after P19 to test whether
explicit endpoint / spur suppression around a weak-boundary branch could reduce
the remaining DiffusionEdge baseline-side false-edge and endpoint trade-off.
It pulls newly introduced off-support components, thin line-like spurs and
high-risk background gradients back toward raw/base before the fixed detectors
see the image.

- Config: `configs/endpoint_stabilized_weak_boundary_v1.json`
- Stage1 status:
  `endpoint_stabilized_weak_boundary_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\endpoint_stabilized_weak_boundary_p20_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\endpoint_stabilized_weak_boundary_p20_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\endpoint_stabilized_weak_boundary_p20_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\endpoint_stabilized_weak_boundary_p20_downstream_gate_20260526.md`

P20 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI endpoint_stabilized_weak_boundary_v1 | 0.783300 | 0.794816 | 0.346679 | 0.7945 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline endpoint_stabilized_weak_boundary_v1 | 0.772955 | 0.782373 | 0.364863 | 0.7950 |

P20 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0023 | -0.0032 | -0.6257 |
| DiffusionEdge baseline | +0.0004 | +0.0034 | +0.3098 |

P20 gate decision: `candidate_metric_near_raw_structure_mixed`. It rescues the
legacy Final collapse and is metric-near-raw on both fixed detectors. MSFI is
structure non-worse. DiffusionEdge baseline F1 is slightly positive, but
false-edge ratio and endpoints remain worse than raw; relative to P19, the
baseline endpoint penalty is worse (`+0.3098` vs `+0.1113` endpoints/kpx), so
P20 is not an improvement over the best recent candidate.

P20 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P20 / full502_clean_v1 | 502 | 2.5018 | 25.3270 | 2.6663 | 0.9986 | 47.0734 | 2.2316 | 7.2074 |
| P20 / compare9_complete496_v1 | 496 | 2.3983 | 24.0276 | 2.6034 | 0.9986 | 47.0799 | 2.2559 | 7.0297 |

Interpretation:

- P20 confirms that explicit endpoint pullback can keep MSFI structure non-worse,
  but it does not solve the DiffusionEdge baseline false-edge/endpoints trade-off.
- Relative to P19, P20 is weaker on the baseline-side endpoint proxy and lower
  on Stage1 enhancement metrics, so it should be recorded as mixed/failure-to-
  improve diagnostic evidence.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P20 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P21 balanced weak-boundary pyramid-fusion status on 2026-05-26

P21 `balanced_weak_boundary_pyramid_fusion_v1` was added after P20 to test a
balanced interpolation between the P14 weak-boundary local-fusion signal and the
later raw-near guard settings. It reuses the existing
`weak_boundary_pyramid_fusion_bph` code path and does not change the locked
formal Stage1 mainline.

- Config: `configs/balanced_weak_boundary_pyramid_fusion_v1.json`
- Stage1 status:
  `balanced_weak_boundary_pyramid_fusion_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\balanced_weak_boundary_pyramid_fusion_p21_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\balanced_weak_boundary_pyramid_fusion_p21_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\balanced_weak_boundary_pyramid_fusion_p21_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\balanced_weak_boundary_pyramid_fusion_p21_downstream_gate_20260526.md`

P21 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI balanced_weak_boundary_pyramid_fusion_v1 | 0.784437 | 0.795026 | 0.346698 | 0.7946 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline balanced_weak_boundary_pyramid_fusion_v1 | 0.773458 | 0.783512 | 0.364882 | 0.7927 |

P21 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0033 | -0.0118 | -1.4988 |
| DiffusionEdge baseline | +0.0016 | +0.0019 | -0.3079 |

P21 gate decision: `candidate_rescues_legacy_but_not_near_raw`. It rescues the
legacy Final collapse and slightly improves ODS/OIS/AP versus raw under both
fixed detectors. MSFI is structure non-worse. DiffusionEdge baseline F1 and
endpoints improve versus raw, but false-edge ratio and AC remain worse than raw,
so P21 is still diagnostic evidence rather than a stable downstream-improving
candidate.

P21 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P21 / full502_clean_v1 | 502 | 2.5482 | 25.8441 | 2.7231 | 0.9983 | 47.6669 | 2.2421 | 7.2925 |
| P21 / compare9_complete496_v1 | 496 | 2.4420 | 24.5117 | 2.6595 | 0.9982 | 47.6755 | 2.2663 | 7.1100 |

Interpretation:

- P21 is stronger than P20 on DiffusionEdge baseline ODS/OIS and endpoint proxy,
  but weaker on baseline AC and still slightly worse on false-edge ratio.
- P21 remains below a stable positive downstream claim because the two-detector
  gate is not all-detector near-raw / structure-nonworse.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P21 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P22 AC-guarded weak-boundary status on 2026-05-26

P22 `ac_guarded_weak_boundary_fusion_v1` was added after P21 to test whether
explicit AC/false-edge guards can retain the P21 weak-boundary rescue while
reducing detector-side pseudo-edge and endpoint penalties. It adds
`final.mode=ac_guarded_weak_boundary_bph` and does not change the locked formal
Stage1 mainline.

- Config: `configs/ac_guarded_weak_boundary_fusion_v1.json`
- Stage1 status:
  `ac_guarded_weak_boundary_fusion_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ac_guarded_weak_boundary_fusion_p22_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ac_guarded_weak_boundary_fusion_p22_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ac_guarded_weak_boundary_fusion_p22_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ac_guarded_weak_boundary_fusion_p22_downstream_gate_20260526.md`

P22 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI ac_guarded_weak_boundary_fusion_v1 | 0.785414 | 0.796161 | 0.346719 | 0.7946 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline ac_guarded_weak_boundary_fusion_v1 | 0.773537 | 0.783375 | 0.365145 | 0.7936 |

P22 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.002431 | -0.011902 | -1.341618 |
| DiffusionEdge baseline | +0.000807 | +0.002607 | +0.292560 |

P22 gate decision: `candidate_rescues_legacy_but_not_near_raw`. It rescues the
legacy Final collapse and improves ODS/OIS/AP versus raw under both fixed
detectors. MSFI is structure non-worse. DiffusionEdge baseline AC remains
`0.0033` below raw and misses the current near-raw AC tolerance by `0.0003`;
baseline false-edge ratio and endpoints also remain worse than raw. P22 is
therefore diagnostic evidence, not a stable downstream-improving candidate.

P22 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P22 / full502_clean_v1 | 502 | 2.5276 | 25.6124 | 2.7088 | 0.9982 | 47.5735 | 2.2331 | 7.2513 |
| P22 / compare9_complete496_v1 | 496 | 2.4225 | 24.2955 | 2.6455 | 0.9982 | 47.5803 | 2.2574 | 7.0715 |

Interpretation:

- P22 improves MSFI ODS/OIS/AP relative to P21 and improves baseline AC relative
  to P21, but baseline AC is still just outside the current near-raw gate.
- P22 does not solve the DiffusionEdge baseline false-edge/endpoints trade-off.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P22 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P23 precision-rebalanced AC-guarded weak-boundary status on 2026-05-26

P23 `precision_rebalanced_ac_guarded_weak_boundary_fusion_v1` keeps the P22
`final.mode=ac_guarded_weak_boundary_bph` code path but retunes it toward
baseline-side AC/endpoints and disables the support-unsharp probe after the
first P23 proxy run showed endpoint risk. It does not change the locked formal
Stage1 mainline.

- Config:
  `configs/precision_rebalanced_ac_guarded_weak_boundary_fusion_v1.json`
- Stage1 status:
  `precision_rebalanced_ac_guarded_weak_boundary_fusion_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\precision_rebalanced_ac_guarded_weak_boundary_fusion_p23_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\precision_rebalanced_ac_guarded_weak_boundary_fusion_p23_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\precision_rebalanced_ac_guarded_weak_boundary_fusion_p23_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\precision_rebalanced_ac_guarded_weak_boundary_fusion_p23_downstream_gate_20260526.md`

P23 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI precision_rebalanced_ac_guarded_weak_boundary_fusion_v1 | 0.784316 | 0.795027 | 0.346775 | 0.7943 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline precision_rebalanced_ac_guarded_weak_boundary_fusion_v1 | 0.774055 | 0.783496 | 0.364761 | 0.7941 |

P23 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.002786 | -0.012410 | -1.666384 |
| DiffusionEdge baseline | +0.000775 | +0.002434 | -0.184626 |

P23 gate decision: `candidate_metric_near_raw_structure_mixed`. It rescues the
legacy Final collapse and is metric-near-raw on both fixed detectors. Relative
to P22, P23 brings DiffusionEdge baseline AC inside the current near-raw
tolerance and makes baseline endpoints better than raw. It still does not solve
the baseline false-edge trade-off: false-edge ratio remains worse than raw by
`+0.002434`, so this is not a strong pass.

P23 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P23 / full502_clean_v1 | 502 | 2.5292 | 25.5004 | 2.7276 | 0.9984 | 47.8089 | 2.2260 | 7.2777 |
| P23 / compare9_complete496_v1 | 496 | 2.4225 | 24.1971 | 2.6647 | 0.9984 | 47.8155 | 2.2503 | 7.0959 |

Interpretation:

- P23 is the current better candidate than P22 for the baseline-side AC/endpoint
  issue, but it remains structure-mixed because baseline false-edge ratio is
  still worse than raw.
- MSFI side is structure non-worse.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P23 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P24 false-edge-floor AC-guarded weak-boundary status on 2026-05-26

P24 `false_edge_floor_ac_guarded_weak_boundary_fusion_v1` keeps the P23
`final.mode=ac_guarded_weak_boundary_bph` code path but tightens background
false-edge pullback, added-edge guards and support-unsharp suppression. It does
not change the locked formal Stage1 mainline.

- Config:
  `configs/false_edge_floor_ac_guarded_weak_boundary_fusion_v1.json`
- Stage1 status:
  `false_edge_floor_ac_guarded_weak_boundary_fusion_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\false_edge_floor_ac_guarded_weak_boundary_fusion_p24_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\false_edge_floor_ac_guarded_weak_boundary_fusion_p24_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\false_edge_floor_ac_guarded_weak_boundary_fusion_p24_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\false_edge_floor_ac_guarded_weak_boundary_fusion_p24_downstream_gate_20260526.md`

P24 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI false_edge_floor_ac_guarded_weak_boundary_fusion_v1 | 0.783622 | 0.794154 | 0.338141 | 0.7944 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline false_edge_floor_ac_guarded_weak_boundary_fusion_v1 | 0.773402 | 0.782923 | 0.364694 | 0.7943 |

P24 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0021 | -0.0172 | -1.3104 |
| DiffusionEdge baseline | +0.0004 | +0.0018 | -0.3238 |

P24 gate decision: `candidate_rescues_legacy_but_not_near_raw`. It rescues the
legacy Final collapse and improves the Stage1-side image-gradient proxy versus
P23, but it is weaker than P23 as a downstream candidate because MSFI AP drops
to `0.338141` and no longer satisfies the metric-near-raw gate. Baseline-side
false-edge ratio is improved relative to P23 but remains worse than raw by
`+0.0018`.

P24 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P24 / full502_clean_v1 | 502 | 2.5225 | 25.4295 | 2.7316 | 0.9984 | 48.2797 | 2.2307 | 7.2742 |
| P24 / compare9_complete496_v1 | 496 | 2.4149 | 24.1189 | 2.6682 | 0.9984 | 48.2816 | 2.2550 | 7.0911 |

Interpretation:

- P24 is useful as a false-edge-floor diagnostic, not as the next best
  downstream candidate.
- P23 remains the stronger current candidate on fixed-detector metric gate;
  P24 shows that more aggressive false-edge suppression can trade off MSFI AP.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P24 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P25 AP-preserving AC-guarded weak-boundary status on 2026-05-26

P25 `ap_preserving_ac_guarded_weak_boundary_fusion_v1` keeps the P23/P24
`final.mode=ac_guarded_weak_boundary_bph` code path. It pulls the P24
false-edge-floor settings back toward P23 to preserve MSFI AP while retaining a
mild added-edge/background guard. It does not change the locked formal Stage1
mainline.

- Config:
  `configs/ap_preserving_ac_guarded_weak_boundary_fusion_v1.json`
- Stage1 status:
  `ap_preserving_ac_guarded_weak_boundary_fusion_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ap_preserving_ac_guarded_weak_boundary_fusion_p25_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ap_preserving_ac_guarded_weak_boundary_fusion_p25_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ap_preserving_ac_guarded_weak_boundary_fusion_p25_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ap_preserving_ac_guarded_weak_boundary_fusion_p25_downstream_gate_20260526.md`

P25 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI ap_preserving_ac_guarded_weak_boundary_fusion_v1 | 0.783769 | 0.794450 | 0.346594 | 0.7943 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline ap_preserving_ac_guarded_weak_boundary_fusion_v1 | 0.773193 | 0.782810 | 0.364847 | 0.7945 |

P25 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.002119 | -0.016326 | -1.378609 |
| DiffusionEdge baseline | +0.000227 | +0.002878 | +0.055596 |

P25 gate decision: `candidate_metric_near_raw_structure_mixed`. It preserves
AP better than P24 and keeps both fixed detectors metric-near-raw, but the
DiffusionEdge baseline structure proxy remains mixed because false-edge ratio
and endpoints are still worse than raw. This means the P23/P24/P25 trade-off is
not solved by mild parameter rebalancing alone.

P25 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P25 / full502_clean_v1 | 502 | 2.5277 | 25.4723 | 2.7238 | 0.9985 | 47.8810 | 2.2260 | 7.2773 |
| P25 / compare9_complete496_v1 | 496 | 2.4205 | 24.1705 | 2.6609 | 0.9985 | 47.8872 | 2.2503 | 7.0943 |

Interpretation:

- P25 is useful as an AP-preserving diagnostic after P24, not as a strong pass.
- P23 remains the stronger current fixed-detector metric candidate; P24 remains
  the cleaner false-edge diagnostic.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P25 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P26 dual-anchor false-edge floor status on 2026-05-26

P26 `dual_anchor_false_edge_floor_v1` adds a detector-domain dual-anchor
false-edge floor on top of a P25-like weak-boundary anchor. It does not change
the locked formal Stage1 mainline.

- Config:
  `configs/dual_anchor_false_edge_floor_v1.json`
- Stage1 status:
  `dual_anchor_false_edge_floor_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\dual_anchor_false_edge_floor_p26_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\dual_anchor_false_edge_floor_p26_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\dual_anchor_false_edge_floor_p26_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\dual_anchor_false_edge_floor_p26_downstream_gate_20260526.md`

P26 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI dual_anchor_false_edge_floor_v1 | 0.784101 | 0.794815 | 0.346741 | 0.7937 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline dual_anchor_false_edge_floor_v1 | 0.773399 | 0.783027 | 0.364636 | 0.7953 |

P26 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.002691 | -0.012214 | -1.631014 |
| DiffusionEdge baseline | +0.000129 | +0.003102 | +0.375864 |

P26 gate decision: `candidate_rescues_legacy_but_not_near_raw`. It rescues
legacy Final damage and improves MSFI-side structure proxy, but MSFI AC falls
outside near-raw tolerance and baseline false-edge/endpoints remain worse than
raw.

P26 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P26 / full502_clean_v1 | 502 | 2.5452 | 25.6891 | 2.7712 | 0.9985 | 48.1879 | 2.2262 | 7.3170 |
| P26 / compare9_complete496_v1 | 496 | 2.4381 | 24.3824 | 2.7084 | 0.9985 | 48.1988 | 2.2504 | 7.1345 |

Interpretation:

- P26 is useful as a false-edge-floor diagnostic, not as a strong pass.
- It is weaker than P23/P25 on gate status because MSFI AC misses near-raw.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P26 on the 2770-image full pool or write it as a stable
  downstream-improving Stage1 mainline.

## P27 raw-detail low-frequency chroma status on 2026-05-26

P27 `raw_detail_lowfreq_chroma_v1` uses a different mechanism from the
P23-P26 weak-boundary/floor family: it preserves raw high-frequency/luma detail
and adjusts only low-frequency illumination/chroma with BPH evidence. It does
not change the locked formal Stage1 mainline.

- Config:
  `configs/raw_detail_lowfreq_chroma_v1.json`
- Stage1 status:
  `raw_detail_lowfreq_chroma_v1_myedge168_stage1_status_20260526.md`
- MyEdge preflight:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\raw_detail_lowfreq_chroma_p27_preflight_20260526.md`
- Result intake:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\raw_detail_lowfreq_chroma_p27_results_20260526.md`
- Structure proxy:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\raw_detail_lowfreq_chroma_p27_structure_metrics_20260526.md`
- Downstream gate:
  `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\raw_detail_lowfreq_chroma_p27_downstream_gate_20260526.md`

P27 mat-eval results:

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI raw_detail_lowfreq_chroma_v1 | 0.783329 | 0.794822 | 0.346115 | 0.7951 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline raw_detail_lowfreq_chroma_v1 | 0.772587 | 0.782971 | 0.372084 | 0.7949 |

P27 structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.000577 | -0.013685 | -1.160557 |
| DiffusionEdge baseline | -0.000099 | +0.003972 | -0.176182 |

P27 gate decision: `candidate_metric_near_raw_structure_mixed`. It rescues the
legacy Final collapse and reaches metric-near-raw on both fixed detectors. It
is not a strong pass because DiffusionEdge baseline false-edge ratio remains
worse than raw, even though endpoints improve.

P27 enhancement checks:

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P27 / full502_clean_v1 | 502 | 2.5540 | 26.2208 | 2.7684 | 0.9990 | 51.0216 | 2.2259 | 7.2528 |
| P27 / compare9_complete496_v1 | 496 | 2.4436 | 24.8752 | 2.7023 | 0.9990 | 50.9524 | 2.2503 | 7.0609 |

Interpretation:

- P27 is stronger than P26 on gate status and returns both detectors to
  metric-near-raw.
- MSFI-side structure proxy is non-worse; baseline-side structure remains mixed
  because false-edge ratio is `+0.003972` vs raw.
- P27 should be kept as a candidate-pass diagnostic, not as a stable
  downstream-improving Stage1 mainline.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not run P27 on the 2770-image full pool from this gate alone.
