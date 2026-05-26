# P19 Baseline-Stabilized Microfusion Status

Date: 2026-05-26

## Scope

- Variant: `baseline_stabilized_microfusion_v1`
- Config: `experiments/downstream_driven_v1/configs/baseline_stabilized_microfusion_v1.json`
- Stage1 168 output: `experiments/downstream_driven_v1/outputs/myedge168/baseline_stabilized_microfusion_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/baseline_stabilized_microfusion_v1`
- MyEdge preflight/result/structure/gate:
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/baseline_stabilized_microfusion_p19_preflight_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/baseline_stabilized_microfusion_p19_results_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/baseline_stabilized_microfusion_p19_structure_metrics_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/baseline_stabilized_microfusion_p19_downstream_gate_20260526.md`

## Fixed-Detector Result

| Detector | ODS | OIS | AP | AC | dF1 | dFalse-edge | dEndpoints/kpx |
|---|---:|---:|---:|---:|---:|---:|---:|
| MSFI 50k | 0.783842 | 0.795042 | 0.346413 | 0.7959 | +0.0015 | -0.0158 | -1.4579 |
| DiffusionEdge baseline 50k | 0.772365 | 0.782127 | 0.364005 | 0.7941 | -0.0002 | +0.0037 | +0.1113 |

Gate decision: `candidate_metric_near_raw_structure_mixed`.

Interpretation: P19 rescues the legacy Stage1 Final collapse and is near raw on both fixed detectors. MSFI structure proxy is non-worse. DiffusionEdge baseline remains mixed, but compared with P18 its baseline-side endpoint delta is reduced from `+0.472544` to `+0.1113` and F1 is closer to raw.

## Stage1 GT Edge Proxy Prescreen

- Report: `docs/stage1_myedge168_gt_edge_proxy_prescreen_p19_20260526_cn.md`
- Decision: `proxy_positive_candidate`
- Delta vs raw: dF1 `+0.001203`, dFalse-edge `-0.001847`, dEndpoints/kpx `-0.256934`.

## Enhancement Metrics

| Scope | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `full502_clean_v1` | 502 | 2.564854 | 26.132519 | 2.793966 | 0.998859 | 48.064374 | 2.233160 | 7.402334 |
| `compare9_complete496_v1` | 496 | 2.468217 | 24.780300 | 2.729021 | 0.998851 | 48.072270 | 2.257348 | 7.241535 |

`MS_SSIM` and `PSNR` are relative structural consistency to original, not enhanced-ground-truth quality.

## Boundary

- P19 is a non-mainline diagnostic candidate, not the locked Stage1 paper mainline.
- Do not claim stable Stage1 downstream benefit from P19.
- Do not enter or authorize Stage1 2770 full-pool from this gate.
- No GT, weights, MAT, formal output roots, or locked mainline results were overwritten.
