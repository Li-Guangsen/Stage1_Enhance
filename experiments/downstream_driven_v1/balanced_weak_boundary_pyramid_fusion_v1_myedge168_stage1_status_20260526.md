# P21 Balanced Weak Boundary Pyramid Fusion Status

Date: 2026-05-26

## Scope

- Variant: `balanced_weak_boundary_pyramid_fusion_v1`
- Config: `experiments/downstream_driven_v1/configs/balanced_weak_boundary_pyramid_fusion_v1.json`
- Stage1 168 output: `experiments/downstream_driven_v1/outputs/myedge168/balanced_weak_boundary_pyramid_fusion_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/balanced_weak_boundary_pyramid_fusion_v1`
- MyEdge preflight/result/structure/gate:
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/balanced_weak_boundary_pyramid_fusion_p21_preflight_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/balanced_weak_boundary_pyramid_fusion_p21_results_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/balanced_weak_boundary_pyramid_fusion_p21_structure_metrics_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/balanced_weak_boundary_pyramid_fusion_p21_downstream_gate_20260526.md`

## Fixed-Detector Result

| Detector | ODS | OIS | AP | AC | dF1 | dFalse-edge | dEndpoints/kpx |
|---|---:|---:|---:|---:|---:|---:|---:|
| MSFI 50k | 0.784437 | 0.795026 | 0.346698 | 0.7946 | +0.0033 | -0.0118 | -1.4988 |
| DiffusionEdge baseline 50k | 0.773458 | 0.783512 | 0.364882 | 0.7927 | +0.0016 | +0.0019 | -0.3079 |

Gate decision: `candidate_rescues_legacy_but_not_near_raw`.

Interpretation: P21 rescues the legacy Stage1 Final collapse and slightly improves ODS/OIS/AP versus raw under both fixed detectors, but it is not a strong pass. MSFI structure proxy is non-worse. DiffusionEdge baseline F1 and endpoints improve versus raw, but false-edge ratio and AC remain worse than raw, so the all-detector near-raw / structure-nonworse gate still fails.

## Stage1 GT Edge Proxy Prescreen

- Report: `docs/stage1_myedge168_gt_edge_proxy_prescreen_p21_20260526_cn.md`
- Decision: `proxy_positive_candidate`
- Delta vs raw: dF1 `+0.002041`, dFalse-edge `-0.003159`, dEndpoints/kpx `-0.249596`.

## Enhancement Metrics

| Scope | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `full502_clean_v1` | 502 | 2.548187 | 25.844089 | 2.723090 | 0.998257 | 47.666919 | 2.242093 | 7.292509 |
| `compare9_complete496_v1` | 496 | 2.441982 | 24.511738 | 2.659520 | 0.998245 | 47.675527 | 2.266312 | 7.109971 |

`MS_SSIM` and `PSNR` are relative structural consistency to original, not enhanced-ground-truth quality.

## Boundary

- P21 is a non-mainline downstream-driven diagnostic candidate, not the locked Stage1 paper mainline.
- P21 does not prove stable Stage1 downstream benefit: DiffusionEdge baseline AC and false-edge ratio remain worse than raw.
- Relative to P20, P21 improves baseline endpoints and ODS/OIS, but worsens baseline AC and still does not pass all-detector structure gate.
- Do not expand to Stage1 2770 full-pool from this gate.
- No GT, weights, MAT, formal output roots, or locked mainline results were overwritten.
