# Stage1 -> MyEdge Downstream Edge Negative Diagnostic

Generated at: `2026-05-26T01:56:56`

- Overall status: `negative_diagnostic_locked_p8_completed_control_competitive`
- Stage-wise delta rows: `12`
- Variant delta rows: `20`
- P8 repeat/control status: `complete_with_report_assets`

## Direct Answer

- 当前结论：旧 Stage1 增强，尤其 legacy `Final`，在 168 张 MyEdge 带 GT edge split 上确实导致下游边缘检测指标下降；该结论在固定 DiffusionEdge baseline 50k 和固定 MSFI 50k 两个检测器下都成立。
- P2：DiffusionEdge baseline fixed-detector P2 shows every Stage1 stage has lower ODS/OIS/AP/AC than Raw.
- P3：MSFI fixed-detector P3 shows every Stage1 stage has lower ODS/OIS/AC than Raw; IMF1Ray is the only AP exception, but its ODS/OIS/AC still drop.
- P4/P5C/P7：P4/P5C/P7 variants largely remove the legacy Final damage and P8 repeat/control supports repeat-stable near-raw rescue for main rows, but generic gamma controls are competitive and baseline-side structure remains mixed; therefore they are not stable Stage1-specific positive paper evidence.

## Legacy Final Harm

| Group | Detector | Comparison | Baseline | Candidate | Status | ODS | ΔODS | OIS | ΔOIS | AP | ΔAP | AC | ΔAC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stagewise | DiffusionEdge baseline 50k | stage_vs_raw | Raw | Final | all_metrics_lower | 0.530094 | -0.240427 | 0.567910 | -0.212076 | 0.224073 | -0.138992 | 0.734900 | -0.062000 |
| stagewise | MSFI 50k | stage_vs_raw | Raw | Final | all_metrics_lower | 0.588287 | -0.195240 | 0.671357 | -0.122856 | 0.263997 | -0.081902 | 0.740300 | -0.056546 |
| P4 downstream-driven variants | MSFI 50k | variant_vs_historical_raw | historical_raw_msfi_anchor | legacy_stage1_final_p1 | all_metrics_lower | 0.588287 | -0.195240 | 0.671357 | -0.122856 | 0.263997 | -0.081902 | 0.740300 | -0.056546 |
| P5C downstream-driven variants | DiffusionEdge baseline 50k | variant_vs_historical_raw | historical_raw_diffusionedge_anchor | legacy_stage1_final_p1 | all_metrics_lower | 0.530094 | -0.240427 | 0.567910 | -0.212076 | 0.224073 | -0.138992 | 0.734900 | -0.062000 |
| P7 generic controls | MSFI 50k | variant_vs_historical_raw | historical_raw_msfi_anchor | legacy_stage1_final_p1 | all_metrics_lower | 0.588287 | -0.195240 | 0.671357 | -0.122856 | 0.263997 | -0.081902 | 0.740300 | -0.056546 |
| P7 generic controls | DiffusionEdge baseline 50k | variant_vs_historical_raw | historical_raw_diffusionedge_anchor | legacy_stage1_final_p1 | all_metrics_lower | 0.530094 | -0.240427 | 0.567910 | -0.212076 | 0.224073 | -0.138992 | 0.734900 | -0.062000 |

## Stage-wise Diagnosis

| Group | Detector | Comparison | Baseline | Candidate | Status | ODS | ΔODS | OIS | ΔOIS | AP | ΔAP | AC | ΔAC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stagewise | DiffusionEdge baseline 50k | stage_vs_raw | Raw | BPH | all_metrics_lower | 0.712919 | -0.057602 | 0.722432 | -0.057554 | 0.338546 | -0.024519 | 0.794200 | -0.002700 |
| stagewise | DiffusionEdge baseline 50k | stage_vs_raw | Raw | IMF1Ray | all_metrics_lower | 0.687163 | -0.083358 | 0.722376 | -0.057610 | 0.355401 | -0.007664 | 0.741700 | -0.055200 |
| stagewise | DiffusionEdge baseline 50k | stage_vs_raw | Raw | RGHS | all_metrics_lower | 0.612234 | -0.158287 | 0.653750 | -0.126236 | 0.286407 | -0.076658 | 0.751900 | -0.045000 |
| stagewise | DiffusionEdge baseline 50k | stage_vs_raw | Raw | CLAHE | all_metrics_lower | 0.584453 | -0.186068 | 0.665213 | -0.114773 | 0.265935 | -0.097130 | 0.753400 | -0.043500 |
| stagewise | DiffusionEdge baseline 50k | stage_vs_raw | Raw | Fused | all_metrics_lower | 0.629095 | -0.141426 | 0.689792 | -0.090194 | 0.302611 | -0.060454 | 0.753900 | -0.043000 |
| stagewise | DiffusionEdge baseline 50k | stage_vs_raw | Raw | Final | all_metrics_lower | 0.530094 | -0.240427 | 0.567910 | -0.212076 | 0.224073 | -0.138992 | 0.734900 | -0.062000 |
| stagewise | MSFI 50k | stage_vs_raw | Raw | BPH | all_metrics_lower | 0.739237 | -0.044290 | 0.752407 | -0.041806 | 0.310610 | -0.035289 | 0.794200 | -0.002646 |
| stagewise | MSFI 50k | stage_vs_raw | Raw | IMF1Ray | mostly_lower | 0.731747 | -0.051780 | 0.754032 | -0.040181 | 0.350926 | 0.005027 | 0.757300 | -0.039546 |
| stagewise | MSFI 50k | stage_vs_raw | Raw | RGHS | all_metrics_lower | 0.671720 | -0.111807 | 0.723929 | -0.070284 | 0.296742 | -0.049157 | 0.761900 | -0.034946 |
| stagewise | MSFI 50k | stage_vs_raw | Raw | CLAHE | all_metrics_lower | 0.639906 | -0.143621 | 0.720816 | -0.073397 | 0.279873 | -0.066026 | 0.775000 | -0.021846 |
| stagewise | MSFI 50k | stage_vs_raw | Raw | Fused | all_metrics_lower | 0.669946 | -0.113581 | 0.721055 | -0.073158 | 0.291170 | -0.054729 | 0.768300 | -0.028546 |
| stagewise | MSFI 50k | stage_vs_raw | Raw | Final | all_metrics_lower | 0.588287 | -0.195240 | 0.671357 | -0.122856 | 0.263997 | -0.081902 | 0.740300 | -0.056546 |

## Edge-safe Candidate Rows

| Group | Detector | Comparison | Baseline | Candidate | Status | ODS | ΔODS | OIS | ΔOIS | AP | ΔAP | AC | ΔAC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P4 downstream-driven variants | MSFI 50k | variant_vs_historical_raw | historical_raw_msfi_anchor | edge_preserve_original_control | near_raw_edge_safe_candidate | 0.783082 | -0.000445 | 0.794168 | -0.000045 | 0.337353 | -0.008546 | 0.797200 | 0.000354 |
| P4 downstream-driven variants | MSFI 50k | variant_vs_historical_raw | historical_raw_msfi_anchor | edge_preserve_raw_bph_mild_v1 | near_raw_edge_safe_candidate | 0.782743 | -0.000784 | 0.793599 | -0.000614 | 0.345909 | 0.000010 | 0.795700 | -0.001146 |
| P4 downstream-driven variants | MSFI 50k | variant_vs_historical_raw | historical_raw_msfi_anchor | edge_preserve_raw_bph_moderate_v1 | near_raw_edge_safe_candidate | 0.782999 | -0.000528 | 0.794527 | 0.000314 | 0.345952 | 0.000053 | 0.795200 | -0.001646 |
| P5C downstream-driven variants | DiffusionEdge baseline 50k | variant_vs_historical_raw | historical_raw_diffusionedge_anchor | edge_preserve_original_control | near_raw_edge_safe_candidate | 0.771470 | 0.000949 | 0.781490 | 0.001504 | 0.362827 | -0.000238 | 0.793400 | -0.003500 |
| P5C downstream-driven variants | DiffusionEdge baseline 50k | variant_vs_historical_raw | historical_raw_diffusionedge_anchor | edge_preserve_raw_bph_mild_v1 | near_raw_edge_safe_candidate | 0.770699 | 0.000178 | 0.782323 | 0.002337 | 0.370985 | 0.007920 | 0.794100 | -0.002800 |
| P5C downstream-driven variants | DiffusionEdge baseline 50k | variant_vs_historical_raw | historical_raw_diffusionedge_anchor | edge_preserve_raw_bph_moderate_v1 | near_raw_edge_safe_candidate | 0.771168 | 0.000647 | 0.782422 | 0.002436 | 0.363047 | -0.000018 | 0.794000 | -0.002900 |
| P7 generic controls | MSFI 50k | variant_vs_historical_raw | historical_raw_msfi_anchor | generic_luma_clahe_mild_v1 | near_raw_edge_safe_candidate | 0.781721 | -0.001806 | 0.793016 | -0.001197 | 0.345003 | -0.000896 | 0.793400 | -0.003446 |
| P7 generic controls | MSFI 50k | variant_vs_historical_raw | historical_raw_msfi_anchor | generic_luma_gamma_mild_v1 | near_raw_edge_safe_candidate | 0.782883 | -0.000644 | 0.794223 | 0.000010 | 0.345982 | 0.000083 | 0.795200 | -0.001646 |
| P7 generic controls | DiffusionEdge baseline 50k | variant_vs_historical_raw | historical_raw_diffusionedge_anchor | generic_luma_gamma_mild_v1 | near_raw_edge_safe_candidate | 0.771645 | 0.001124 | 0.782024 | 0.002038 | 0.371366 | 0.008301 | 0.793600 | -0.003300 |

## Source Evidence

- Baseline stage-wise P2: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/stagewise_baseline_p2_results_20260525.md`
- MSFI stage-wise P3: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/stagewise_msfi_p3_results_20260525.md`
- MSFI downstream variants P4: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/downstream_variant_p4_results_20260525.md`
- DiffusionEdge baseline variants P5C: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/downstream_variant_baseline_p5c_results_20260525.md`
- P6B paired structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/downstream_variant_structure_p6_paired_review_20260525.md`
- P7 MSFI generic controls: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/generic_control_p7_msfi_results_20260525.md`
- P7 baseline generic controls: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/generic_control_p7_baseline_results_20260525.md`
- P7 paired structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/generic_control_p7_structure_paired_review_20260525.md`
- P8 repeat/control result intake: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/stage1_repeat_control_p8_results_20260525.md`

## Interpretation Boundaries

- This report reads existing MyEdge Stage1 coupling JSON/MD assets only.
- It does not run Stage1 enhancement, MyEdge sampling, WSL eval.py, WSL show.py, training, or metric recomputation.
- The 168-image MyEdge split has GT edge maps and is valid for diagnosis, but it is not the 2770 full-pool result.
- P8 repeat/control is complete as a 168-image fixed-detector diagnostic; it does not establish Stage1-specific positive downstream benefit because generic gamma controls are competitive and baseline-side structure remains mixed.
- Do not claim stable Stage1 downstream improvement until larger-scope evidence and manually frozen degradation/failure analysis are synchronized.

## Next Gate

- 不要重复跑 P1/P2/P3/P4/P5C/P6/P6B/P7 首轮。
- 下一步要么先人工复核退化/失败案例候选，要么在明确高风险确认后执行 P8 repeat/control。
- 成功前不要进入 2770 full-pool；当前 edge-safe 变体不能写成稳定优于 raw 的论文结论。
