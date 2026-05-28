# E01-B wavelet pyramid weak boundary smoke7_highrisk_e01b_v1 status

Date: 2026-05-27

## Summary

- Status: `smoke_completed_visual_risk_accepted`
- Manifest: `experiments\e01_task_guided_family\manifests\smoke7_highrisk_v1.txt`
- Output root: `experiments\e01_task_guided_family\outputs\smoke7_highrisk_v1\e01_b_wavelet_pyramid_weak_boundary_v1`
- Expected images: `7`
- Observed runtime: `1.2` sec total, `0.17` sec/image
- Projected 168 runtime: `0.5` min
- Decision: `proceed_to_168_fixed_detector_preflight`

## Output Completeness

| Format | Stage | Count |
|---|---|---:|
| jpg | BPH | 7 |
| jpg | IMF1Ray | 7 |
| jpg | RGHS | 7 |
| jpg | CLAHE | 7 |
| jpg | Fused | 7 |
| jpg | Final | 7 |
| png | BPH | 7 |
| png | IMF1Ray | 7 |
| png | RGHS | 7 |
| png | CLAHE | 7 |
| png | Fused | 7 |
| png | Final | 7 |

- Missing files: `0`
- Decode failures: `0`

## Raw-vs-Final Smoke Metrics

| Stem | mean abs BGR delta | mean abs L delta | PSNR vs raw | grad mean ratio | luma std ratio |
|---|---:|---:|---:|---:|---:|
| donghaiyuanjia.26 | 8.059 | 0.905 | 27.571 | 0.985 | 1.005 |
| jianci.4 | 2.691 | 0.007 | 39.167 | 1.000 | 1.000 |
| tama.14 | 1.610 | 0.996 | 41.368 | 1.002 | 0.993 |
| weixiaoyuanjia.21 | 7.906 | 1.001 | 27.877 | 1.001 | 1.009 |
| weixiaoyuanjia.26 | 8.210 | 0.960 | 27.429 | 0.985 | 1.003 |
| xuehong.13 | 2.011 | 0.939 | 40.732 | 1.015 | 0.998 |
| xuehong.9 | 2.013 | 0.945 | 40.728 | 1.014 | 0.998 |

Mean metrics:

- mean_abs_bgr_delta: `4.6428`
- mean_abs_luma_delta: `0.8220`
- mean_abs_chroma_delta: `2.0263`
- psnr_vs_raw: `34.9818`
- grad_mean_ratio: `1.0005`
- luma_std_ratio: `1.0010`

## Visual Risk Review

- Reviewed panels: `donghaiyuanjia.26`, `weixiaoyuanjia.21`, `tama.14`, `xuehong.13`.
- `CLAHE` slot shows the intended noisy contrast driver, but `Final` is bounded by wavelet/background risk control.
- No obvious FF01/FF02-like background false-edge burst was observed in Final.
- Weak object boundaries remain visible; this permits 168 fixed-detector preflight but does not establish downstream success.

## Stage Metrics CSV

- `e01_b_wavelet_pyramid_weak_boundary_v1_smoke7_highrisk_e01b_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_e01b_v1\donghaiyuanjia.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_e01b_v1\jianci.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_e01b_v1\tama.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_e01b_v1\weixiaoyuanjia.21_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_e01b_v1\weixiaoyuanjia.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_e01b_v1\xuehong.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_e01b_v1\xuehong.9_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
