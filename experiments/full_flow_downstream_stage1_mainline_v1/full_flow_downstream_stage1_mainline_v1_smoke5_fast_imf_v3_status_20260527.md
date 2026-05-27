# full_flow_downstream_stage1_mainline_v1 smoke5_fast_imf_v3 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_fast_imf_v3_visual_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v3`
- Expected images: `5`
- Observed runtime: `3.1` sec total, `0.62` sec/image
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
| chazhuang.1 | 9.013 | 6.029 | 27.500 | 1.113 | 1.087 |
| haiyangkadun.18 | 5.330 | 2.123 | 31.849 | 1.562 | 1.174 |
| lingxinghaixian.6 | 11.665 | 8.961 | 25.100 | 1.242 | 1.331 |
| tama.14 | 8.824 | 4.152 | 27.198 | 5.248 | 1.447 |
| zhaixi.3 | 10.082 | 6.052 | 27.149 | 1.180 | 1.221 |

Mean metrics:

- mean_abs_bgr_delta: `8.9829`
- mean_abs_luma_delta: `5.4634`
- mean_abs_chroma_delta: `7.4986`
- psnr_vs_raw: `27.7594`
- grad_mean_ratio: `2.0691`
- luma_std_ratio: `1.2517`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v3_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v3\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v3\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v3\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v3\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_fast_imf_v3\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
