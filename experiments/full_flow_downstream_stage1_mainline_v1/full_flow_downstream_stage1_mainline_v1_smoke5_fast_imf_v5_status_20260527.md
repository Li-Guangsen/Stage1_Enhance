# full_flow_downstream_stage1_mainline_v1 smoke5_fast_imf_v5 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_fast_imf_v5_visual_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v5`
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
| chazhuang.1 | 7.890 | 8.538 | 28.724 | 1.119 | 1.136 |
| haiyangkadun.18 | 9.149 | 6.565 | 27.892 | 1.746 | 1.293 |
| lingxinghaixian.6 | 9.460 | 9.936 | 27.442 | 1.262 | 1.358 |
| tama.14 | 8.859 | 3.775 | 27.372 | 2.330 | 1.409 |
| zhaixi.3 | 6.010 | 9.964 | 29.179 | 1.141 | 1.273 |

Mean metrics:

- mean_abs_bgr_delta: `8.2737`
- mean_abs_luma_delta: `7.7558`
- mean_abs_chroma_delta: `5.7553`
- psnr_vs_raw: `28.1218`
- grad_mean_ratio: `1.5195`
- luma_std_ratio: `1.2938`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v5_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v5\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v5\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v5\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v5\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v5\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
