# P20 Endpoint-Stabilized Weak Boundary Status

Date: 2026-05-26

## Scope

- Variant: `endpoint_stabilized_weak_boundary_v1`
- Config: `experiments/downstream_driven_v1/configs/endpoint_stabilized_weak_boundary_v1.json`
- Stage1 168 output: `experiments/downstream_driven_v1/outputs/myedge168/endpoint_stabilized_weak_boundary_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/endpoint_stabilized_weak_boundary_v1`
- MyEdge preflight/result/structure/gate:
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/endpoint_stabilized_weak_boundary_p20_preflight_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/endpoint_stabilized_weak_boundary_p20_results_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/endpoint_stabilized_weak_boundary_p20_structure_metrics_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/endpoint_stabilized_weak_boundary_p20_downstream_gate_20260526.md`

## Fixed-Detector Result

| Detector | ODS | OIS | AP | AC | dF1 | dFalse-edge | dEndpoints/kpx |
|---|---:|---:|---:|---:|---:|---:|---:|
| MSFI 50k | 0.783300 | 0.794816 | 0.346679 | 0.7945 | +0.0023 | -0.0032 | -0.6257 |
| DiffusionEdge baseline 50k | 0.772955 | 0.782373 | 0.364863 | 0.7950 | +0.0004 | +0.0034 | +0.3098 |

Gate decision: `candidate_metric_near_raw_structure_mixed`.

Interpretation: P20 rescues the legacy Stage1 Final collapse and is near raw on both fixed detectors. MSFI structure proxy is non-worse. DiffusionEdge baseline F1 is slightly positive, but false-edge ratio and endpoints remain worse than raw, and the endpoint penalty is larger than P19. P20 is therefore diagnostic evidence, not a stable downstream-improving candidate.

## Stage1 GT Edge Proxy Prescreen

- Report: `docs/stage1_myedge168_gt_edge_proxy_prescreen_p20_20260526_cn.md`
- Decision: `proxy_positive_candidate`
- Delta vs raw: dF1 `+0.000443`, dFalse-edge `-0.001100`, dEndpoints/kpx `-0.809646`.

## Enhancement Metrics

| Scope | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `full502_clean_v1` | 502 | 2.501818 | 25.327015 | 2.666317 | 0.998594 | 47.073449 | 2.231626 | 7.207419 |
| `compare9_complete496_v1` | 496 | 2.398330 | 24.027601 | 2.603413 | 0.998586 | 47.079864 | 2.255948 | 7.029696 |

`MS_SSIM` and `PSNR` are relative structural consistency to original, not enhanced-ground-truth quality.

## Boundary

- P20 is a non-mainline downstream-driven diagnostic candidate, not the locked Stage1 paper mainline.
- Do not claim stable Stage1 downstream benefit from P20.
- Relative to P19, P20 does not improve the baseline-side endpoint trade-off.
- Do not enter or authorize Stage1 2770 full-pool from this gate.
- No GT, weights, MAT, formal output roots, or locked mainline results were overwritten.
