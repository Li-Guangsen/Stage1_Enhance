# full_flow_downstream_stage1_mainline_v1 smoke5_fast_imf_v4 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_fast_imf_v4_visual_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v4`
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
| chazhuang.1 | 8.296 | 9.003 | 28.290 | 1.109 | 1.149 |
| haiyangkadun.18 | 8.809 | 8.725 | 28.170 | 1.965 | 1.364 |
| lingxinghaixian.6 | 8.913 | 9.907 | 27.180 | 1.269 | 1.367 |
| tama.14 | 8.875 | 3.814 | 27.385 | 2.199 | 1.417 |
| zhaixi.3 | 6.669 | 9.952 | 28.734 | 1.154 | 1.286 |

Mean metrics:

- mean_abs_bgr_delta: `8.3126`
- mean_abs_luma_delta: `8.2801`
- mean_abs_chroma_delta: `6.1408`
- psnr_vs_raw: `27.9518`
- grad_mean_ratio: `1.5393`
- luma_std_ratio: `1.3167`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v4_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v4\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v4\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v4\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v4\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v4\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
