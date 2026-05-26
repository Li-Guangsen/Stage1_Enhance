# P26 Dual-anchor false-edge floor status

Date: 2026-05-26

Variant: `dual_anchor_false_edge_floor_v1`

Config: `experiments/downstream_driven_v1/configs/dual_anchor_false_edge_floor_v1.json`

Final mode: `dual_anchor_false_edge_floor_bph`

## Scope

- MyEdge split: 168-image ALGAE split with GT.
- Fixed detectors: MSFI 50k and DiffusionEdge baseline 50k.
- Stage1 enhancement metrics: `full502_clean_v1` and `compare9_complete496_v1` only.
- Full-pool 2770: not entered.
- Formal Stage1 mainline and formal result directory were not overwritten.

## Assets

- Stage1 MyEdge168 output root: `experiments/downstream_driven_v1/outputs/myedge168/dual_anchor_false_edge_floor_v1`
- Stage1 full502 output root: `experiments/downstream_driven_v1/outputs/full502/dual_anchor_false_edge_floor_v1`
- Stage1 proxy prescreen: `docs/stage1_myedge168_gt_edge_proxy_prescreen_p26_20260526_cn.md`
- MyEdge preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\dual_anchor_false_edge_floor_p26_preflight_20260526.md`
- MyEdge result intake: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\dual_anchor_false_edge_floor_p26_results_20260526.md`
- MyEdge structure proxy: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\dual_anchor_false_edge_floor_p26_structure_metrics_20260526.md`
- MyEdge downstream gate: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\dual_anchor_false_edge_floor_p26_downstream_gate_20260526.md`
- full502 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p26_full502_20260526`
- compare496 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p26_compare496_20260526`

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
| Downstream gate | `candidate_rescues_legacy_but_not_near_raw` |

## Stage1 GT Edge Proxy Prescreen

| Decision | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| `proxy_positive_candidate` | +0.000093 | -0.000564 | -0.727718 |

## Fixed-Detector Metrics

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P26 | 0.784101 | 0.794815 | 0.346741 | 0.7937 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline P26 | 0.773399 | 0.783027 | 0.364636 | 0.7953 |

## Structure Proxy Delta Vs Raw

| Detector | dF1 | dFalse-edge | dEndpoints/kpx | Structure non-worse |
| --- | ---: | ---: | ---: | ---: |
| MSFI | +0.002691 | -0.012214 | -1.631014 | true |
| DiffusionEdge baseline | +0.000129 | +0.003102 | +0.375864 | false |

## Enhancement Metrics

| Protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `full502_clean_v1` | 502 | 2.545224 | 25.689059 | 2.771164 | 0.998480 | 48.187858 | 2.226195 | 7.316971 |
| `compare9_complete496_v1` | 496 | 2.438149 | 24.382367 | 2.708358 | 0.998469 | 48.198759 | 2.250437 | 7.134507 |

## Interpretation

- P26 adds a detector-domain dual-anchor false-edge floor on top of the P25-like weak-boundary anchor, trying to suppress off-support background and small/line-component risk areas without the P24 AP collapse.
- The candidate rescues legacy Stage1 Final collapse and improves MSFI-side structure proxy, but it is not a strong pass: MSFI AC falls just outside the near-raw tolerance and DiffusionEdge baseline structure proxy remains worse than raw on false-edge ratio and endpoints.
- P26 does not solve the baseline false-edge/endpoints problem; it should be kept as a failed/rescue diagnostic, not promoted as a stable downstream-improving Stage1 mainline.
- `MS_SSIM` and `PSNR` are relative structure consistency to the original images, not GT enhancement quality.
- Do not run P26 on the 2770-image full pool or write it as a stable downstream-improving Stage1 result.
