# P24 false-edge-floor AC-guarded weak-boundary status

Date: 2026-05-26

Variant: `false_edge_floor_ac_guarded_weak_boundary_fusion_v1`

Config: `experiments/downstream_driven_v1/configs/false_edge_floor_ac_guarded_weak_boundary_fusion_v1.json`

Final mode: `ac_guarded_weak_boundary_bph`

## Scope

- MyEdge split: 168-image ALGAE split with GT.
- Fixed detectors: MSFI 50k and DiffusionEdge baseline 50k.
- Stage1 enhancement metrics: `full502_clean_v1` and `compare9_complete496_v1` only.
- Full-pool 2770: not entered.
- Formal Stage1 mainline and formal result directory were not overwritten.

## Assets

- Stage1 MyEdge168 output root: `experiments/downstream_driven_v1/outputs/myedge168/false_edge_floor_ac_guarded_weak_boundary_fusion_v1`
- Stage1 full502 output root: `experiments/downstream_driven_v1/outputs/full502/false_edge_floor_ac_guarded_weak_boundary_fusion_v1`
- Stage1 proxy prescreen: `docs/stage1_myedge168_gt_edge_proxy_prescreen_p24_20260526_cn.md`
- MyEdge preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\false_edge_floor_ac_guarded_weak_boundary_fusion_p24_preflight_20260526.md`
- MyEdge result intake: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\false_edge_floor_ac_guarded_weak_boundary_fusion_p24_results_20260526.md`
- MyEdge structure proxy: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\false_edge_floor_ac_guarded_weak_boundary_fusion_p24_structure_metrics_20260526.md`
- MyEdge downstream gate: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\false_edge_floor_ac_guarded_weak_boundary_fusion_p24_downstream_gate_20260526.md`
- full502 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p24_full502_20260526`
- compare496 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p24_compare496_20260526`

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
| `proxy_positive_candidate` | +0.001237 | -0.002226 | -0.907946 |

## Fixed-Detector Metrics

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P24 | 0.783622 | 0.794154 | 0.338141 | 0.7944 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline P24 | 0.773402 | 0.782923 | 0.364694 | 0.7943 |

## Structure Proxy Delta Vs Raw

| Detector | dF1 | dFalse-edge | dEndpoints/kpx | Structure non-worse |
| --- | ---: | ---: | ---: | ---: |
| MSFI | +0.0021 | -0.0172 | -1.3104 | true |
| DiffusionEdge baseline | +0.0004 | +0.0018 | -0.3238 | false |

## Enhancement Metrics

| Protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `full502_clean_v1` | 502 | 2.522499 | 25.429511 | 2.731607 | 0.998381 | 48.279730 | 2.230682 | 7.274187 |
| `compare9_complete496_v1` | 496 | 2.414914 | 24.118911 | 2.668172 | 0.998369 | 48.281558 | 2.255029 | 7.091136 |

## Interpretation

- P24 tightens the P23 false-edge floor and improves the Stage1-side image-gradient proxy relative to P23.
- Fixed-detector metrics do not improve over P23: MSFI AP drops to `0.338141`, and MSFI is no longer metric-near-raw under the current AP tolerance.
- DiffusionEdge baseline remains rescued versus legacy Final and near-raw on metrics, but its false-edge ratio is still worse than raw by `+0.0018`.
- P24 is therefore weaker than P23 as an immediate downstream candidate, despite cleaner false-edge/endpoints proxy.
- `MS_SSIM` and `PSNR` are relative structure consistency to the original images, not GT enhancement quality.
- Do not run P24 on the 2770-image full pool or write it as a stable downstream-improving Stage1 mainline.
