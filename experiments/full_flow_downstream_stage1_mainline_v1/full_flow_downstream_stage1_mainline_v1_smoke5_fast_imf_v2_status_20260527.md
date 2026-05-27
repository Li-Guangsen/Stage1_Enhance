# full_flow_downstream_stage1_mainline_v1 fast-IMF v2 smoke5 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_fast_imf_v2_visual_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v2`
- Expected images: `5`
- Observed runtime: `3.2` sec total, `0.64` sec/image
- Projected 168 runtime: `1.8` min
- Decision: `visual_review_before_168_gate`

## Output Completeness

| Format | Stage | Count |
|---|---|---:|
| jpg | BPH | 5 |
| jpg | IMF1Ray | 5 |
| jpg | RGHS | 5 |
| jpg | CLAHE | 5 |
| jpg | Fused | 5 |
| jpg | Final | 5 |
| png | BPH | 5 |
| png | IMF1Ray | 5 |
| png | RGHS | 5 |
| png | CLAHE | 5 |
| png | Fused | 5 |
| png | Final | 5 |

- Missing files: `0`
- Decode failures: `0`

## Raw-vs-Final Smoke Metrics

| Stem | mean abs BGR delta | mean abs L delta | PSNR vs raw | grad mean ratio | luma std ratio |
|---|---:|---:|---:|---:|---:|
| chazhuang.1 | 8.136 | 8.890 | 28.461 | 1.127 | 1.139 |
| haiyangkadun.18 | 12.510 | 9.675 | 25.799 | 1.487 | 1.311 |
| lingxinghaixian.6 | 8.916 | 9.937 | 27.182 | 1.266 | 1.361 |
| tama.14 | 8.895 | 3.876 | 27.375 | 2.131 | 1.425 |
| zhaixi.3 | 6.673 | 9.967 | 28.742 | 1.147 | 1.281 |

Mean metrics:

- mean_abs_bgr_delta: `9.0260`
- mean_abs_luma_delta: `8.4691`
- mean_abs_chroma_delta: `6.0868`
- psnr_vs_raw: `27.5119`
- grad_mean_ratio: `1.4317`
- luma_std_ratio: `1.3033`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v2_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf_v2\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf_v2\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf_v2\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf_v2\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf_v2\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- Runtime is compatible with 168-image enhancement, but human/visual review is still required before fixed-detector validation.
