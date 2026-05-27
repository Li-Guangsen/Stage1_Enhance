# full_flow_downstream_stage1_mainline_v2 ff02_smoke5_v1 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v2\outputs\smoke5_v1`
- Expected images: `5`
- Observed runtime: `2.7` sec total, `0.55` sec/image
- Projected 168 runtime: `1.5` min
- Decision: `review_before_168`

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
| chazhuang.1 | 6.836 | 1.081 | 28.702 | 0.893 | 0.997 |
| haiyangkadun.18 | 3.611 | 1.081 | 36.181 | 0.917 | 1.004 |
| lingxinghaixian.6 | 12.998 | 0.277 | 23.903 | 0.974 | 0.984 |
| tama.14 | 6.250 | 0.901 | 30.243 | 1.446 | 1.025 |
| zhaixi.3 | 10.942 | 0.335 | 26.715 | 0.913 | 0.988 |

Mean metrics:

- mean_abs_bgr_delta: `8.1275`
- mean_abs_luma_delta: `0.7351`
- mean_abs_chroma_delta: `6.8929`
- psnr_vs_raw: `29.1489`
- grad_mean_ratio: `1.0286`
- luma_std_ratio: `0.9997`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v2_ff02_smoke5_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke5_v1\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke5_v1\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke5_v1\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke5_v1\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke5_v1\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
