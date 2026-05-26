# C01 Microstructure-CSP P16 Stage1/MyEdge Status

Date: 2026-05-26

## Scope

- Variant: `c01_microstructure_csp_v1`
- Config: `experiments/downstream_driven_v1/configs/c01_microstructure_csp_v1.json`
- Stage1 MyEdge split output: `experiments/downstream_driven_v1/outputs/myedge168/c01_microstructure_csp_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/c01_microstructure_csp_v1`
- MyEdge preflight: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/c01_microstructure_csp_p16_preflight_20260526.md`
- MyEdge result intake: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/c01_microstructure_csp_p16_results_20260526.md`
- MyEdge structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/c01_microstructure_csp_p16_structure_metrics_20260526.md`
- MyEdge downstream gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/c01_microstructure_csp_p16_downstream_gate_20260526.md`

This is a non-mainline downstream-driven diagnostic candidate. It does not
replace `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
or the formal Stage1 result directory.

## Counts

| Asset | Count |
| --- | ---: |
| Stage1 MyEdge168 Final PNG | 168 |
| Stage1 MyEdge168 Final JPG | 168 |
| Stage1 full502 Final PNG | 502 |
| MyEdge MSFI MAT/PNG | 168 / 168 |
| MyEdge DiffusionEdge baseline MAT/PNG | 168 / 168 |

## Fixed-Detector Metrics

| Detector/input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI c01_microstructure_csp_v1 | 0.783352 | 0.795226 | 0.346031 | 0.7948 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline c01_microstructure_csp_v1 | 0.771525 | 0.783504 | 0.370706 | 0.7941 |

## Structure Proxy vs Raw

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI | +0.0010 | -0.0101 | -1.2432 |
| DiffusionEdge baseline | -0.0016 | +0.0071 | +0.0941 |

## Enhancement Metrics

| Protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| full502_clean_v1 | 502 | 2.6576 | 28.1097 | 2.9418 | 0.9987 | 49.4034 | 2.2439 | 7.5138 |
| compare9_complete496_v1 | 496 | 2.5661 | 26.6626 | 2.8745 | 0.9987 | 49.4311 | 2.2685 | 7.3591 |

## Gate

Decision: `candidate_metric_near_raw_structure_mixed`.

P16 rescues the legacy Stage1 Final collapse and is metric-near-raw on both
fixed detectors. The MSFI side is structure non-worse, but the DiffusionEdge
baseline side remains mixed because F1 is slightly lower and false-edge ratio
and endpoints are slightly higher than raw.

## Boundary

- `MS_SSIM` and `PSNR` are relative structure consistency to original, not GT
  enhancement quality.
- Do not write P16 as stable Stage1 downstream improvement.
- Do not enter the 2770-image full pool from this gate alone.
