# P22 ac_guarded_weak_boundary_fusion_v1 Stage1/MyEdge168 Status

Date: 2026-05-26

## Scope

- Variant: `ac_guarded_weak_boundary_fusion_v1`
- Config: `experiments/downstream_driven_v1/configs/ac_guarded_weak_boundary_fusion_v1.json`
- Code path: `final.mode=ac_guarded_weak_boundary_bph`
- Stage1 MyEdge split output: `experiments/downstream_driven_v1/outputs/myedge168/ac_guarded_weak_boundary_fusion_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/ac_guarded_weak_boundary_fusion_v1`
- MyEdge preflight: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ac_guarded_weak_boundary_fusion_p22_preflight_20260526.md`
- MyEdge fixed-detector results: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ac_guarded_weak_boundary_fusion_p22_results_20260526.md`
- MyEdge structure proxy: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ac_guarded_weak_boundary_fusion_p22_structure_metrics_20260526.md`
- MyEdge downstream gate: `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\ac_guarded_weak_boundary_fusion_p22_downstream_gate_20260526.md`
- `2770` full-pool: not entered.

## Stage1 Output Readiness

| Item | Count |
| --- | ---: |
| MyEdge168 Final PNG | 168 |
| MyEdge168 Final JPG | 168 |
| decoded MyEdge168 Final PNG | 168 |
| full502 Final PNG | 502 |
| full502 Final JPG | 502 |

## Stage1 Proxy Prescreen

The P22 Stage1-side Sobel/Otsu image-gradient proxy prescreen generated
`docs/stage1_myedge168_gt_edge_proxy_prescreen_p22_20260526_cn.md`.

| Decision | F1 | Precision | Recall | False-edge ratio | Components/kpx | Endpoints/kpx | Mean luma delta | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `proxy_positive_candidate` | 0.583110 | 0.479076 | 0.894917 | 0.520924 | 10.439433 | 55.842308 | 1.032475 | +0.001780 | -0.002768 | -0.258654 |

## Fixed-detector MyEdge Results

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P22 | 0.785414 | 0.796161 | 0.346719 | 0.7946 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline P22 | 0.773537 | 0.783375 | 0.365145 | 0.7936 |

P22 downstream gate decision: `candidate_rescues_legacy_but_not_near_raw`.

## Structure Proxy vs Raw

| Detector | dF1 | dPrecision | dRecall | dFalse-edge | dComponents/kpx | dEndpoints/kpx | Structure non-worse |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| MSFI | +0.002431 | +0.011902 | -0.006605 | -0.011902 | -0.614030 | -1.341618 | true |
| DiffusionEdge baseline | +0.000807 | -0.002607 | +0.003083 | +0.002607 | -0.151629 | +0.292560 | false |

## Enhancement Metrics

`MS_SSIM` and `PSNR` are relative structure consistency to the original images,
not GT enhancement quality.

| Method / protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P22 / full502_clean_v1 | 502 | 2.527595 | 25.612431 | 2.708753 | 0.998221 | 47.573541 | 2.233058 | 7.251289 |
| P22 / compare9_complete496_v1 | 496 | 2.422461 | 24.295492 | 2.645468 | 0.998209 | 47.580250 | 2.257428 | 7.071506 |

## Boundary

- P22 wraps the P21-like weak-boundary candidate with AC/false-edge-oriented guards: off-support pseudo-edge pruning, support-gradient floor, raw/base pullback, and luma-delta fallback.
- P22 improves MSFI ODS/OIS/AP versus raw and keeps MSFI structure proxy non-worse.
- P22 also improves DiffusionEdge baseline ODS/OIS/AP versus raw, but baseline AC remains lower than raw by `0.0033`; with the current `0.003` tolerance it misses the near-raw AC gate by `0.0003`.
- DiffusionEdge baseline false-edge ratio and endpoints remain worse than raw, so P22 is still diagnostic evidence rather than a stable downstream-improving Stage1 mainline.
- Do not run P22 on the 2770-image full pool or write it as stable Stage1 downstream benefit.
