# full_flow_downstream_stage1_mainline_v1 fast-IMF smoke5 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_fast_imf_ready_for_visual_review_not_168_gate`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf`
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
| chazhuang.1 | 8.136 | 8.890 | 28.461 | 1.127 | 1.139 |
| haiyangkadun.18 | 12.510 | 9.675 | 25.799 | 1.487 | 1.311 |
| lingxinghaixian.6 | 6.156 | 9.968 | 29.766 | 1.282 | 1.384 |
| tama.14 | 8.325 | 5.473 | 27.780 | 2.670 | 1.673 |
| zhaixi.3 | 6.475 | 9.972 | 29.621 | 1.149 | 1.283 |

Mean metrics:

- mean_abs_bgr_delta: `8.3203`
- mean_abs_luma_delta: `8.7955`
- mean_abs_chroma_delta: `4.3665`
- psnr_vs_raw: `28.2854`
- grad_mean_ratio: `1.5430`
- luma_std_ratio: `1.3580`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1_fast_imf\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- Runtime is now compatible with a 168-image smoke budget, but visual review is still required before fixed-detector validation.
