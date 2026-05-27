# full_flow_downstream_stage1_mainline_v2 FF02 fixed-detector status

Date: 2026-05-27

## Summary

- Candidate: `FF02`
- Variant: `full_flow_downstream_stage1_mainline_v2`
- Role: detector-compatible full-flow redesign after FF01/v8 failure.
- Status: `complete_rescue_only_archived_diagnostic`
- Downstream gate: `candidate_rescues_legacy_but_not_near_raw`
- Decision: `archive_diagnostic`

FF02 completed the intended correction step: it restored a complete Stage1 enhancement flow with color/structure decoupling, topology-compatible fusion, and bounded closure, then ran the 168 fixed-detector validation. The result is not a downstream success. It rescues the legacy Stage1 Final collapse, but both fixed detectors remain clearly below raw and both structure proxies are worse than raw.

## Protected Assets

This run did not overwrite:

- `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- P12-P28, D01, or FF01 outputs
- MyEdge checkpoints, GT, MAT protocol, or official output roots

## Stage1 168 Output

- Manifest: `experiments/full_flow_downstream_stage1_mainline_v1/manifests/myedge168_v1.txt`
- Output root: `experiments/full_flow_downstream_stage1_mainline_v2/outputs/myedge168/full_flow_downstream_stage1_mainline_v2`
- Final PNG: `168`
- Final JPG: `168`
- Decode failures: `0`
- Runtime: `77.5` sec total, about `0.46` sec/image

Mean raw-vs-Final metrics:

| Metric | Value |
| --- | ---: |
| mean_abs_bgr_delta | 11.7138 |
| mean_abs_luma_delta | 1.3708 |
| mean_abs_chroma_delta | 7.9785 |
| psnr_vs_raw | 27.2740 |
| grad_mean_ratio | 0.9450 |
| luma_std_ratio | 1.0132 |

High-risk samples remain present. `tama.14` has grad ratio `1.4455`; `weixiaoyuanjia.21` has BGR delta `29.757`, luma delta `3.312`, chroma delta `15.21`, grad ratio `1.2476`, and luma std ratio `1.2136`. Branch-level RGHS/CLAHE also produced Lab clipping warnings during the 168 run, which is recorded as branch risk even though output completeness passed.

## Fixed-Detector Metrics

| Detector/Input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI legacy Final | 0.588287 | 0.671357 | 0.263997 | 0.740300 |
| MSFI FF02 | 0.737952 | 0.751109 | 0.303208 | 0.792000 |
| DiffusionEdge raw | 0.770521 | 0.779986 | 0.363065 | 0.796900 |
| DiffusionEdge legacy Final | 0.530094 | 0.567910 | 0.224073 | 0.734900 |
| DiffusionEdge FF02 | 0.711020 | 0.720141 | 0.320951 | 0.794000 |

Deltas vs raw:

| Detector | dODS | dOIS | dAP | dAC |
| --- | ---: | ---: | ---: | ---: |
| MSFI FF02 | -0.045575 | -0.043104 | -0.042691 | -0.004846 |
| DiffusionEdge FF02 | -0.059501 | -0.059845 | -0.042114 | -0.002900 |

FF02 therefore does not meet raw-near criteria on either detector.

## Structure Proxy

| Detector | dF1 vs raw | dFalse-edge vs raw | dEndpoints/kpx vs raw | Structure non-worse |
| --- | ---: | ---: | ---: | --- |
| MSFI FF02 | -0.0507 | +0.0734 | +2.0630 | false |
| DiffusionEdge FF02 | -0.0666 | +0.0890 | +3.7585 | false |

The structure proxy is slightly less bad than FF01 on false-edge/endpoints, but still fails the non-worse condition and cannot support a positive downstream claim.

## Comparison

- Relative to raw: FF02 is clearly worse on both detectors and both structure proxies.
- Relative to legacy Stage1 Final: FF02 rescues the severe legacy collapse, so it is useful negative/control evidence.
- Relative to FF01: FF02 slightly improves structure proxy deltas, but worsens fixed-detector ODS/OIS/AP on both detectors.
- Relative to P27/P28: FF02 is below the metric-near-raw mixed diagnostic family and cannot replace P27 as the near-raw reference.
- Relative to D01: FF02 has a fuller enhancement-flow mechanism, but still does not produce downstream positive gain.

## Decision

FF02 is archived as diagnostic evidence. It is not a candidate pass, not a strong pass, not a formal Stage1 mainline, and not evidence that a complete Stage1 enhancement flow improves fixed-detector downstream edge detection.

Do not enter 502/496 or 2770 as a candidate-passing route from FF02. Do not continue FF03 as a same-family threshold, guard, fallback, or raw-pullback patch. The next valid step is a method-level failure audit and a strategic decision: either create a genuinely new method family with a predeclared mechanism, or shift the downstream-positive claim to MyEdge/MSFI-side adaptation.

## Evidence Files

- Method design: `docs/full_flow_downstream_stage1_mainline_v2_method_design_cn.md`
- Run sheet: `experiments/full_flow_downstream_stage1_mainline_v2/run_sheet_v1.md`
- Config: `experiments/full_flow_downstream_stage1_mainline_v2/configs/full_flow_downstream_stage1_mainline_v2.json`
- Stage1 168 status: `experiments/full_flow_downstream_stage1_mainline_v2/full_flow_downstream_stage1_mainline_v2_ff02_myedge168_v1_status_20260527.md`
- MyEdge preflight: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_preflight_20260527.md`
- MyEdge result intake: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_results_20260527.md`
- Structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_structure_metrics_20260527.md`
- Downstream gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_downstream_gate_20260527.md`
