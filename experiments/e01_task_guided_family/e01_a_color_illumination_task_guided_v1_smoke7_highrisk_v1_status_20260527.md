# E01-A color illumination task guided smoke7_highrisk_v1 status

Date: 2026-05-27

## Summary

- Status: `smoke_completed_visual_risk_accepted`
- Manifest: `experiments\e01_task_guided_family\manifests\smoke7_highrisk_v1.txt`
- Output root: `experiments\e01_task_guided_family\outputs\smoke7_highrisk_v1\e01_a_color_illumination_task_guided_v1`
- Expected images: `7`
- Observed runtime: `5.4` sec total, `0.78` sec/image
- Projected 168 runtime: `2.2` min
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
| donghaiyuanjia.26 | 17.894 | 1.318 | 21.061 | 0.990 | 0.999 |
| jianci.4 | 6.924 | 0.869 | 30.548 | 1.021 | 1.023 |
| tama.14 | 4.124 | 0.999 | 34.013 | 1.000 | 0.999 |
| weixiaoyuanjia.21 | 18.040 | 1.787 | 21.141 | 1.046 | 1.003 |
| weixiaoyuanjia.26 | 18.818 | 1.921 | 20.797 | 0.982 | 0.987 |
| xuehong.13 | 5.175 | 0.950 | 32.179 | 1.004 | 1.000 |
| xuehong.9 | 5.172 | 0.950 | 32.171 | 1.003 | 1.001 |

Mean metrics:

- mean_abs_bgr_delta: `10.8782`
- mean_abs_luma_delta: `1.2563`
- mean_abs_chroma_delta: `5.6267`
- psnr_vs_raw: `27.4159`
- grad_mean_ratio: `1.0064`
- luma_std_ratio: `1.0019`

## Visual Risk Review

- Reviewed panels: `donghaiyuanjia.26`, `weixiaoyuanjia.21`, `tama.14`, `xuehong.13`.
- No obvious FF/TLVC-like background false-edge burst was observed in the high-risk smoke panels.
- Weak object boundaries remained visible; the candidate mainly changed color/illumination and kept luma structure close to raw.
- This permits the planned 168 fixed-detector preflight; it does not establish downstream success.

## Stage Metrics CSV

- `e01_a_color_illumination_task_guided_v1_smoke7_highrisk_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_v1\donghaiyuanjia.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_v1\jianci.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_v1\tama.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_v1\weixiaoyuanjia.21_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_v1\weixiaoyuanjia.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_v1\xuehong.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\smoke7_highrisk_v1\xuehong.9_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
