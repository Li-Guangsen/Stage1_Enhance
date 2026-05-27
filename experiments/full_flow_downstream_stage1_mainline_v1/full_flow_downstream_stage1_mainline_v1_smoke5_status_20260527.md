# full_flow_downstream_stage1_mainline_v1 smoke5 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke_runtime_too_slow_for_168_gate`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1`
- Expected images: `5`
- Observed runtime: `179.9` sec total, `35.98` sec/image
- Projected 168 runtime: `100.7` min
- Decision: `do_not_enter_168_gate_before_runtime_and_visual_review`

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
| chazhuang.1 | 8.081 | 8.851 | 28.522 | 1.130 | 1.136 |
| haiyangkadun.18 | 12.467 | 9.642 | 25.818 | 1.516 | 1.312 |
| lingxinghaixian.6 | 6.144 | 9.962 | 29.782 | 1.282 | 1.377 |
| tama.14 | 10.621 | 9.972 | 26.163 | 3.397 | 2.472 |
| zhaixi.3 | 6.471 | 9.971 | 29.616 | 1.149 | 1.282 |

Mean metrics:

- mean_abs_bgr_delta: `8.7569`
- mean_abs_luma_delta: `9.6795`
- mean_abs_chroma_delta: `4.1914`
- psnr_vs_raw: `27.9799`
- grad_mean_ratio: `1.6948`
- luma_std_ratio: `1.5157`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke5_v1\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The observed runtime is too slow for the current 168-image target; implementation/runtime must be reviewed before fixed-detector validation.
