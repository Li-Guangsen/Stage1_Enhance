# full_flow_downstream_stage1_mainline_v1 smoke5_fast_imf_v7 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_fast_imf_v7_visual_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v7`
- Expected images: `5`
- Observed runtime: `3.0` sec total, `0.60` sec/image
- Projected 168 runtime: `1.7` min
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
| chazhuang.1 | 8.192 | 7.229 | 27.977 | 1.156 | 1.119 |
| haiyangkadun.18 | 11.304 | 8.436 | 26.604 | 1.456 | 1.257 |
| lingxinghaixian.6 | 8.716 | 9.905 | 27.893 | 1.257 | 1.342 |
| tama.14 | 7.725 | 5.054 | 28.013 | 2.527 | 1.551 |
| zhaixi.3 | 8.370 | 9.973 | 27.864 | 1.145 | 1.274 |

Mean metrics:

- mean_abs_bgr_delta: `8.8612`
- mean_abs_luma_delta: `8.1192`
- mean_abs_chroma_delta: `5.8543`
- psnr_vs_raw: `27.6698`
- grad_mean_ratio: `1.5081`
- luma_std_ratio: `1.3086`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v7_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v7\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v7\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v7\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v7\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v7\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
