# P15 Structure-Guarded Weak-Boundary Stage1 Status

Date: 2026-05-26

## Scope

- Variant: `structure_guarded_weak_boundary_v1`
- Config: `experiments/downstream_driven_v1/configs/structure_guarded_weak_boundary_v1.json`
- Code path: existing `final.mode=weak_boundary_pyramid_fusion_bph`
- Stage1 MyEdge split output: `experiments/downstream_driven_v1/outputs/myedge168/structure_guarded_weak_boundary_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/structure_guarded_weak_boundary_v1`
- MyEdge preflight: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/structure_guarded_weak_boundary_p15_preflight_20260526.md`
- MyEdge result intake: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/structure_guarded_weak_boundary_p15_results_20260526.md`
- MyEdge structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/structure_guarded_weak_boundary_p15_structure_metrics_20260526.md`
- MyEdge downstream gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/structure_guarded_weak_boundary_p15_downstream_gate_20260526.md`

## Counts

| Asset | Count |
|---|---:|
| MyEdge split Final PNG | 168 |
| MyEdge split Final JPG | 168 |
| Full502 Final PNG | 502 |
| MyEdge MSFI MAT/PNG | 168 / 168 |
| MyEdge DiffusionEdge baseline MAT/PNG | 168 / 168 |

## Fixed-Detector Metrics

| Detector/input | ODS | OIS | AP | AC |
|---|---:|---:|---:|---:|
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P15 | 0.784104 | 0.795471 | 0.347023 | 0.795100 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.796900 |
| DiffusionEdge baseline P15 | 0.773201 | 0.782997 | 0.365411 | 0.795300 |

## Structure Proxy Delta vs Raw

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
|---|---:|---:|---:|
| MSFI | +0.0033 | -0.0123 | -1.6983 |
| DiffusionEdge baseline | +0.0013 | +0.0017 | +0.1126 |

## Enhancement Metrics

| Protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `full502_clean_v1` | 502 | 2.5211 | 25.4229 | 2.6947 | 0.9982 | 47.5609 | 2.2555 | 7.2461 |
| `compare9_complete496_v1` | 496 | 2.4151 | 24.1041 | 2.6313 | 0.9981 | 47.5692 | 2.2799 | 7.0637 |

## Decision Boundary

- Downstream gate: `candidate_metric_near_raw_structure_mixed`.
- P15 rescues the legacy Stage1 Final collapse and is near raw on both fixed detectors by metric tolerance.
- MSFI side is structure non-worse; DiffusionEdge baseline side remains mixed because false-edge ratio and endpoints are slightly worse than raw.
- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT enhancement quality.
- P15 is not a formal Stage1 mainline, not a stable downstream benefit claim, and must not be expanded to the 2770-image full pool from this gate alone.
