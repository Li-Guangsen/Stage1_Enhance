# full_flow_downstream_stage1_mainline_v1 smoke5_fast_imf_v6 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_fast_imf_v6_visual_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v6`
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
| chazhuang.1 | 7.595 | 8.036 | 29.112 | 1.143 | 1.129 |
| haiyangkadun.18 | 11.620 | 8.750 | 26.368 | 1.496 | 1.272 |
| lingxinghaixian.6 | 8.434 | 9.946 | 28.528 | 1.264 | 1.360 |
| tama.14 | 9.054 | 4.990 | 27.003 | 3.465 | 1.582 |
| zhaixi.3 | 6.422 | 10.010 | 29.592 | 1.135 | 1.270 |

Mean metrics:

- mean_abs_bgr_delta: `8.6247`
- mean_abs_luma_delta: `8.3464`
- mean_abs_chroma_delta: `5.0946`
- psnr_vs_raw: `28.1204`
- grad_mean_ratio: `1.7007`
- luma_std_ratio: `1.3224`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v6_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v6\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v6\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v6\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v6\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v6\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
