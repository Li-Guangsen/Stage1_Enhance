# MyEdge 166 Complete-Case Enhancement Metrics Baseline v2

- Created at: `2026-05-28T01:50:32`
- Run root: `D:\Desktop\Stage1Codex\experiments\myedge168_compare9_rerun_20260527`
- Output dir: `D:\Desktop\Stage1Codex\experiments\myedge168_compare9_rerun_20260527\metrics\enhancement_metrics_eaai_aligned_v2`
- Scope: enhancement metrics only. No DiffusionEdge/MSFI inference, no `eval.py`, no `show.py`, no 502/496, no 2770.
- Data source: `D:/Desktop/MyEdgeCodex/input_test/algae`, 168 raw images. Primary comparison and future downstream validation use the 166 complete-case subset.
- Main table policy: 9 enhancement methods on 166 complete-case stems. The two MyEdge raw samples missing from WWPF, `chazhuang.3.jpg` and `chazhuang.6.jpg`, are excluded from every method in the main table instead of being handled as method-specific missing rows.
- Downstream alignment policy: future fixed-detector DiffusionEdge/MSFI validation for Stage1 candidates should use the same 166 complete-case stems, so enhancement screening and downstream validation share one primary image set.
- Supplement table policy: raw + 8 complete methods on all 168 stems, excluding WWPF.
- Main enhancement metrics: `UIQM`, `UCIQE`, `SSEQ`, `SIFT_MATCH_RATIO`.
- Diagnostic metrics: `EME`, `EMEE`, `Entropy`, `Contrast`, `AvgGra`.
- Structure consistency guards: `MS_SSIM`, `PSNR`.
- `SSEQ` is `SSEQ_reimplementation_feature_mean`, not an EAAI private-code reproduction.
- `SIFT_MATCH_RATIO` is raw-enhanced OpenCV SIFT matching with Lowe ratio 0.75; raw anchor is `NA`.

## Outputs

- `mean_metrics_9method_complete_case_166.csv/md`
- `mean_metrics_8method_no_wwpf_168.csv/md`
- `per_image_metrics_166.csv`
- `per_image_metrics_168_no_wwpf.csv`
- `rank_summary_166.csv/md`
- `screening_rule_summary_166.csv/md`
- `diagnostic_methods.md`
- `metric_definitions.json`
- `summary.json`

## Main Table Exclusion

The 166-stem main table is the official enhancement-metric comparison table for this MyEdge 168 rerun. It excludes these two source images from all methods:

- `D:/Desktop/MyEdgeCodex/input_test/algae/chazhuang.3.jpg`
- `D:/Desktop/MyEdgeCodex/input_test/algae/chazhuang.6.jpg`

This keeps `Ours`, all external enhancement baselines, and WWPF on the same image set. The no-WWPF 168-stem table remains a supplementary reference only.

## Future Candidate Screening Rule

A future Stage1 enhancement candidate should not have 3 or more of the 4 main enhancement metrics in the bottom third: `UIQM`, `UCIQE`, `SSEQ`, `SIFT_MATCH_RATIO`. This is only the first enhancement-quality screen; fixed-detector MyEdge downstream validation on the same 166 complete-case remains the final criterion.

`HLRP` and `Histoformer` are high-noise diagnostic references. They remain in the numeric table for traceability but are excluded from the primary screening conclusion.

## Current Methods Under This Rule

| method | role | main_metric_bottom_third_count | screening_status |
| --- | --- | --- | --- |
| ABC-Former | enhancement_reference | 3 | fails_future_candidate_rule |
| HVDualformer | enhancement_reference | 3 | fails_future_candidate_rule |
| SGUIE-Net | enhancement_reference | 2 | passes_future_candidate_rule |
| HLRP | enhancement_high_noise_diagnostic | 1 | diagnostic_not_primary_screening |
| Histoformer | enhancement_high_noise_diagnostic | 1 | diagnostic_not_primary_screening |
| Ours | legacy_ours_reference | 1 | passes_future_candidate_rule |
| WWPF | enhancement_incomplete_166_of_168 | 1 | passes_future_candidate_rule |
| CBF | enhancement_reference | 0 | passes_future_candidate_rule |
| GDCP | enhancement_reference | 0 | passes_future_candidate_rule |
