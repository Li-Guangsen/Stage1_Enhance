# MyEdge 168 Compare9 Rerun Report

Created at: 2026-05-27T22:15:02
Run root: `D:\Desktop\Stage1Codex\experiments\myedge168_compare9_rerun_20260527`

## Scope

- Data source: `D:/Desktop/MyEdgeCodex/input_test/algae`.
- This run regenerates enhancement outputs for the exact 168 MyEdge edge-detection test images.
- Old Stage1 502/496 outputs are not used as result sources because same-name files are not guaranteed to be byte-identical.
- No DiffusionEdge/MSFI sampling, `eval.py`, `show.py`, 502/496 complete-case, or 2770 full-pool run was executed.

## Inputs

- MyEdge raw images: 168
- Input manifest: `manifests/myedge168_input_manifest.csv`
- Copied raw input dir: `inputs/raw`

## Methods

| Method | Normalized outputs | Role |
|---|---:|---|
| Ours | 168 | primary/full record |
| HVDualformer | 168 | primary/full record |
| ABC-Former | 168 | primary/full record |
| GDCP | 168 | primary/full record |
| CBF | 168 | primary/full record |
| HLRP | 168 | high-noise diagnostic reference |
| SGUIE-Net | 168 | primary/full record |
| Histoformer | 168 | high-noise diagnostic reference |
| WWPF | 166 | primary/full record |

## Metrics

- Full 9-method complete-case metrics output: `D:\Desktop\Stage1Codex\experiments\myedge168_compare9_rerun_20260527\metrics\enhancement_metrics`
- Full 9-method complete-case size: 166 images. WWPF failed on 2 MyEdge raw inputs, so the all-method complete-case table excludes those 2 stems.
- 8-method no-WWPF 168-image metrics output: `D:\Desktop\Stage1Codex\experiments\myedge168_compare9_rerun_20260527\metrics\enhancement_metrics_no_wwpf_168`
- 8-method no-WWPF size: 168 images. This table is the full MyEdge 168 reference when WWPF is excluded.
- Metrics: EME, EMEE, Entropy, Contrast, AvgGra, MS_SSIM, PSNR, UCIQE, UIQM.
- MS_SSIM and PSNR are interpreted only as raw-reference structural consistency.

## WWPF Failure Note

- WWPF normalized outputs: 166 / 168.
- Missing stems: `chazhuang.3`, `chazhuang.6`.
- Log evidence: `logs/WWPF.log`.
- Observed MATLAB error: `Unrecognized function or variable 'Am'` inside the WWPF p-code path.
- WWPF remains in the full 9-method record as an incomplete diagnostic method. It is not used for the no-WWPF 168-image reference table.

## Logs

- Per-method logs: `logs/{method}.log`.
- MATLAB wrappers generated under `matlab_wrappers/`.

## EAAI-Aligned Enhancement Metrics v2

Updated at: 2026-05-28

- Output: `metrics/enhancement_metrics_eaai_aligned_v2`
- Scope: enhancement metrics only; no DiffusionEdge/MSFI inference, no `eval.py`, no `show.py`, no 502/496, no 2770.
- Recomputed metrics: `EME`, `EMEE`, `Entropy`, `Contrast`, `AvgGra`, `MS_SSIM`, `PSNR`, `UCIQE`, `UIQM`, `SSEQ`, `SIFT_GOOD_MATCHES`, `SIFT_MATCH_RATIO`.
- Main enhancement metrics for future candidate screening: `UIQM`, `UCIQE`, `SSEQ`, `SIFT_MATCH_RATIO`.
- `SSEQ` is documented as `SSEQ_reimplementation_feature_mean`, not an EAAI private-code reproduction.
- `SIFT_MATCH_RATIO` is raw-enhanced OpenCV SIFT matching with Lowe ratio `0.75`; raw anchor is `NA`.
- Main table: `metrics/enhancement_metrics_eaai_aligned_v2/mean_metrics_9method_complete_case_166.md`.
- Supplement table: `metrics/enhancement_metrics_eaai_aligned_v2/mean_metrics_8method_no_wwpf_168.md`.
- Screening summary: `metrics/enhancement_metrics_eaai_aligned_v2/screening_rule_summary_166.md`.
