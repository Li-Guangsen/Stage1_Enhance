# P17 Topology-Guarded Microfusion Status

Date: 2026-05-26

## Scope

- Variant: `topology_guarded_microfusion_v1`
- Config: `experiments/downstream_driven_v1/configs/topology_guarded_microfusion_v1.json`
- Stage1 168 output: `experiments/downstream_driven_v1/outputs/myedge168/topology_guarded_microfusion_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/topology_guarded_microfusion_v1`
- MyEdge preflight/result/structure/gate:
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_guarded_microfusion_p17_preflight_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_guarded_microfusion_p17_results_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_guarded_microfusion_p17_structure_metrics_20260526.md`
  - `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_guarded_microfusion_p17_downstream_gate_20260526.md`

## Fixed-Detector Result

| Detector | ODS | OIS | AP | AC | dF1 | dFalse-edge | dEndpoints/kpx |
|---|---:|---:|---:|---:|---:|---:|---:|
| MSFI 50k | 0.784021 | 0.795041 | 0.346753 | 0.7945 | +0.002088 | -0.016451 | -1.206439 |
| DiffusionEdge baseline 50k | 0.771878 | 0.781854 | 0.364359 | 0.7958 | +0.000471 | +0.003138 | +0.095826 |

Gate decision: `candidate_metric_near_raw_structure_mixed`.

Interpretation: P17 rescues the legacy Stage1 Final collapse and is near raw on both fixed detectors. MSFI structure proxy is non-worse, but DiffusionEdge baseline false-edge ratio and endpoints remain slightly worse than raw, so this is not a strong pass.

## Enhancement Metrics

| Scope | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `full502_clean_v1` | 502 | 2.539264 | 25.676677 | 2.759750 | 0.998866 | 47.707367 | 2.229543 | 7.387601 |
| `compare9_complete496_v1` | 496 | 2.439145 | 24.328425 | 2.695200 | 0.998859 | 47.708913 | 2.253806 | 7.217338 |

`MS_SSIM` and `PSNR` are relative structural consistency to original, not enhanced-ground-truth quality.

## Boundary

- P17 is a non-mainline diagnostic candidate, not the locked Stage1 paper mainline.
- Do not claim stable Stage1 downstream benefit from P17.
- Do not enter or authorize Stage1 2770 full-pool from this gate.
- No GT, weights, MAT, formal output roots, or locked mainline results were overwritten.
