# topology_locked_visual_chroma_full_flow_v1 smoke5_highrisk_v1 status

Date: 2026-05-27

## Summary

- Status: `smoke_complete`
- Manifest: `experiments\topology_locked_visual_chroma_full_flow_v1\manifests\smoke5_highrisk_v1.txt`
- Output root: `experiments\topology_locked_visual_chroma_full_flow_v1\outputs\smoke5_highrisk_v1`
- Expected images: `5`
- Observed runtime: `2.5` sec total, `0.49` sec/image
- Projected 168 runtime: `1.4` min
- Decision: `pass_to_broader_smoke_not_168_yet`

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
| weixiaoyuanjia.26 | 31.013 | 0.997 | 16.435 | 0.997 | 0.999 |
| xuehong.9 | 7.731 | 0.962 | 28.271 | 1.004 | 1.000 |
| donghaiyuanjia.26 | 29.981 | 0.995 | 16.582 | 0.997 | 0.999 |
| tama.14 | 7.769 | 0.925 | 28.574 | 1.153 | 1.005 |
| jianci.4 | 14.411 | 0.098 | 23.992 | 1.016 | 1.028 |

Mean metrics:

- mean_abs_bgr_delta: `18.1808`
- mean_abs_luma_delta: `0.7953`
- mean_abs_chroma_delta: `10.4539`
- psnr_vs_raw: `22.7709`
- grad_mean_ratio: `1.0333`
- luma_std_ratio: `1.0063`

## Stage Metrics CSV

- `topology_locked_visual_chroma_full_flow_v1_smoke5_highrisk_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke5_highrisk_v1\weixiaoyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke5_highrisk_v1\xuehong.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke5_highrisk_v1\donghaiyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke5_highrisk_v1\tama.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke5_highrisk_v1\jianci.4_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
