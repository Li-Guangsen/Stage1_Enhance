# P25 AP-preserving AC-guarded weak-boundary status

Date: 2026-05-26

Variant: `ap_preserving_ac_guarded_weak_boundary_fusion_v1`

Config: `experiments/downstream_driven_v1/configs/ap_preserving_ac_guarded_weak_boundary_fusion_v1.json`

Final mode: `ac_guarded_weak_boundary_bph`

## Scope

- MyEdge split: 168-image ALGAE split with GT.
- Fixed detectors: MSFI 50k and DiffusionEdge baseline 50k.
- Stage1 enhancement metrics: `full502_clean_v1` and `compare9_complete496_v1` only.
- Full-pool 2770: not entered.
- Formal Stage1 mainline and formal result directory were not overwritten.

## Assets

- Stage1 MyEdge168 output root: `experiments/downstream_driven_v1/outputs/myedge168/ap_preserving_ac_guarded_weak_boundary_fusion_v1`
- Stage1 full502 output root: `experiments/downstream_driven_v1/outputs/full502/ap_preserving_ac_guarded_weak_boundary_fusion_v1`
- Stage1 proxy prescreen: `docs/stage1_myedge168_gt_edge_proxy_prescreen_p25_20260526_cn.md`
- MyEdge preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ap_preserving_ac_guarded_weak_boundary_fusion_p25_preflight_20260526.md`
- MyEdge result intake: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ap_preserving_ac_guarded_weak_boundary_fusion_p25_results_20260526.md`
- MyEdge structure proxy: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ap_preserving_ac_guarded_weak_boundary_fusion_p25_structure_metrics_20260526.md`
- MyEdge downstream gate: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ap_preserving_ac_guarded_weak_boundary_fusion_p25_downstream_gate_20260526.md`
- full502 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p25_full502_20260526`
- compare496 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p25_compare496_20260526`

## Readiness

| Item | Status |
| --- | ---: |
| MyEdge168 Final PNG | 168 |
| MyEdge168 Final JPG | 168 |
| full502 Final PNG | 502 |
| full502 Final JPG | 502 |
| MyEdge sampling | done |
| WSL eval/show | done |
| Result intake | `complete_with_report_assets` |
| Structure proxy | `complete` |
| Downstream gate | `candidate_metric_near_raw_structure_mixed` |

## Stage1 GT Edge Proxy Prescreen

| Decision | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| `proxy_positive_candidate` | +0.000280 | -0.000856 | -0.613632 |

## Fixed-Detector Metrics

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P25 | 0.783769 | 0.794450 | 0.346594 | 0.7943 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline P25 | 0.773193 | 0.782810 | 0.364847 | 0.7945 |

## Structure Proxy Delta Vs Raw

| Detector | dF1 | dFalse-edge | dEndpoints/kpx | Structure non-worse |
| --- | ---: | ---: | ---: | ---: |
| MSFI | +0.002119 | -0.016326 | -1.378609 | true |
| DiffusionEdge baseline | +0.000227 | +0.002878 | +0.055596 | false |

## Enhancement Metrics

| Protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `full502_clean_v1` | 502 | 2.527725 | 25.472260 | 2.723817 | 0.998485 | 47.881003 | 2.226039 | 7.277322 |
| `compare9_complete496_v1` | 496 | 2.420458 | 24.170473 | 2.660853 | 0.998475 | 47.887220 | 2.250298 | 7.094304 |

## Interpretation

- P25 is an AP-preserving pullback from P24 toward P23. It recovers MSFI AP from the P24 drop and keeps both detectors metric-near-raw.
- The candidate is still not a strong pass: DiffusionEdge baseline structure proxy remains mixed, with false-edge ratio and endpoints both worse than raw.
- P23 remains the stronger immediate fixed-detector metric candidate. P24 remains the cleaner false-edge diagnostic. P25 shows the AP/false-edge trade-off has not been solved by mild parameter rebalancing alone.
- `MS_SSIM` and `PSNR` are relative structure consistency to the original images, not GT enhancement quality.
- Do not run P25 on the 2770-image full pool or write it as a stable downstream-improving Stage1 mainline.
