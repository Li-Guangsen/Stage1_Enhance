# P18 Topology-Pruned Microfusion Status

Date: 2026-05-26

## Scope

- Variant: `topology_pruned_microfusion_v1`
- Config: `experiments/downstream_driven_v1/configs/topology_pruned_microfusion_v1.json`
- Stage1 168 output: `experiments/downstream_driven_v1/outputs/myedge168/topology_pruned_microfusion_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/topology_pruned_microfusion_v1`
- MyEdge preflight/result/structure/gate:
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_pruned_microfusion_p18_preflight_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_pruned_microfusion_p18_results_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_pruned_microfusion_p18_structure_metrics_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_pruned_microfusion_p18_downstream_gate_20260526.md`

## Fixed-Detector Result

| Detector | ODS | OIS | AP | AC | dF1 | dFalse-edge | dEndpoints/kpx |
|---|---:|---:|---:|---:|---:|---:|---:|
| MSFI 50k | 0.783694 | 0.794872 | 0.346526 | 0.7946 | +0.001417 | -0.015329 | -1.239722 |
| DiffusionEdge baseline 50k | 0.772249 | 0.781858 | 0.363790 | 0.7946 | -0.000592 | +0.004148 | +0.472544 |

Gate decision: `candidate_metric_near_raw_structure_mixed`.

Interpretation: P18 rescues the legacy Stage1 Final collapse and is near raw on both fixed detectors. MSFI structure proxy is non-worse and improves false-edge/endpoints versus raw, but DiffusionEdge baseline structure proxy remains slightly worse than raw, so this is not a strong pass.

## Enhancement Metrics

| Scope | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `full502_clean_v1` | 502 | 2.568776 | 26.207006 | 2.796752 | 0.998837 | 48.325180 | 2.232123 | 7.407511 |
| `compare9_complete496_v1` | 496 | 2.473128 | 24.848358 | 2.731603 | 0.998831 | 48.334516 | 2.256301 | 7.248430 |

`MS_SSIM` and `PSNR` are relative structural consistency to original, not enhanced-ground-truth quality.

## Boundary

- P18 is a non-mainline diagnostic candidate, not the locked Stage1 paper mainline.
- Do not claim stable Stage1 downstream benefit from P18.
- Do not enter or authorize Stage1 2770 full-pool from this gate.
- No GT, weights, MAT, formal output roots, or locked mainline results were overwritten.
