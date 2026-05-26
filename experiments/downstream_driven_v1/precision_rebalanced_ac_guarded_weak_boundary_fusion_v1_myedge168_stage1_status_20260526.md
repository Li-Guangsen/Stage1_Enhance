# P23 precision-rebalanced AC-guarded weak-boundary status

Date: 2026-05-26

Variant: `precision_rebalanced_ac_guarded_weak_boundary_fusion_v1`

Config: `experiments/downstream_driven_v1/configs/precision_rebalanced_ac_guarded_weak_boundary_fusion_v1.json`

Final mode: `ac_guarded_weak_boundary_bph`

## Scope

- MyEdge split: 168-image ALGAE split with GT.
- Fixed detectors: MSFI 50k and DiffusionEdge baseline 50k.
- Stage1 enhancement metrics: `full502_clean_v1` and `compare9_complete496_v1` only.
- Full-pool 2770: not entered.
- Formal Stage1 mainline and formal result directory were not overwritten.

## Assets

- Stage1 MyEdge168 output root: `experiments/downstream_driven_v1/outputs/myedge168/precision_rebalanced_ac_guarded_weak_boundary_fusion_v1`
- Stage1 full502 output root: `experiments/downstream_driven_v1/outputs/full502/precision_rebalanced_ac_guarded_weak_boundary_fusion_v1`
- Stage1 proxy prescreen: `docs/stage1_myedge168_gt_edge_proxy_prescreen_p23_20260526_cn.md`
- MyEdge preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\precision_rebalanced_ac_guarded_weak_boundary_fusion_p23_preflight_20260526.md`
- MyEdge result intake: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\precision_rebalanced_ac_guarded_weak_boundary_fusion_p23_results_20260526.md`
- MyEdge structure proxy: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\precision_rebalanced_ac_guarded_weak_boundary_fusion_p23_structure_metrics_20260526.md`
- MyEdge downstream gate: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\precision_rebalanced_ac_guarded_weak_boundary_fusion_p23_downstream_gate_20260526.md`
- full502 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p23_full502_20260526`
- compare496 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p23_compare496_20260526`

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
| `proxy_positive_candidate` | +0.000077 | -0.000591 | -0.321220 |

## Fixed-Detector Metrics

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P23 | 0.784316 | 0.795027 | 0.346775 | 0.7943 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline P23 | 0.774055 | 0.783496 | 0.364761 | 0.7941 |

## Structure Proxy Delta Vs Raw

| Detector | dF1 | dFalse-edge | dEndpoints/kpx | Structure non-worse |
| --- | ---: | ---: | ---: | ---: |
| MSFI | +0.002786 | -0.012410 | -1.666384 | true |
| DiffusionEdge baseline | +0.000775 | +0.002434 | -0.184626 | false |

## Enhancement Metrics

| Protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `full502_clean_v1` | 502 | 2.529201 | 25.500392 | 2.727611 | 0.998449 | 47.808939 | 2.226000 | 7.277708 |
| `compare9_complete496_v1` | 496 | 2.422525 | 24.197056 | 2.664676 | 0.998438 | 47.815505 | 2.250251 | 7.095914 |

## Interpretation

- P23 rescues the legacy Stage1 Final downstream collapse and is metric-near-raw on both fixed detectors.
- Relative to P22, P23 improves the DiffusionEdge baseline AC gate from outside tolerance to within the current near-raw tolerance, and flips baseline endpoints from worse than raw to better than raw.
- MSFI is structure non-worse.
- DiffusionEdge baseline remains structure-mixed because false-edge ratio is still worse than raw by `+0.002434`.
- P23 is therefore a candidate-level pass, not a strong pass and not a stable downstream-improving Stage1 mainline.
- `MS_SSIM` and `PSNR` are relative structure consistency to the original images, not GT enhancement quality.
- Do not run P23 on the 2770-image full pool from this gate alone.
