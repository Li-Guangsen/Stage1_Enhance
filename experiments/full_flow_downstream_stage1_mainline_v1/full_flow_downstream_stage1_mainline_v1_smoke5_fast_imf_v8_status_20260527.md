# full_flow_downstream_stage1_mainline_v1 smoke5_fast_imf_v8 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_fast_imf_v8_visual_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v8`
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
| chazhuang.1 | 6.023 | 1.035 | 29.689 | 1.004 | 1.002 |
| haiyangkadun.18 | 3.034 | 1.083 | 37.659 | 1.038 | 1.029 |
| lingxinghaixian.6 | 10.435 | 2.125 | 26.746 | 1.031 | 1.004 |
| tama.14 | 5.073 | 1.042 | 32.158 | 1.210 | 1.064 |
| zhaixi.3 | 9.831 | 0.085 | 27.547 | 1.031 | 1.037 |

Mean metrics:

- mean_abs_bgr_delta: `6.8792`
- mean_abs_luma_delta: `1.0740`
- mean_abs_chroma_delta: `5.8035`
- psnr_vs_raw: `30.7597`
- grad_mean_ratio: `1.0628`
- luma_std_ratio: `1.0273`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v8_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v8\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v8\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v8\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v8\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v8\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
