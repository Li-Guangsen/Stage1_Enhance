# topology_locked_visual_chroma_full_flow_v1 smoke30_broader_v1 status

Date: 2026-05-27

## Summary

- Status: `smoke_complete_cv_gray_lock`
- Manifest: `experiments\topology_locked_visual_chroma_full_flow_v1\manifests\smoke30_broader_v1.txt`
- Output root: `experiments\topology_locked_visual_chroma_full_flow_v1\outputs\smoke30_broader_v1`
- Expected images: `30`
- Observed runtime: `12.9` sec total, `0.43` sec/image
- Projected 168 runtime: `1.2` min
- Decision: `rerun_168_proxy_before_myedge`

## Output Completeness

| Format | Stage | Count |
|---|---|---:|
| jpg | BPH | 30 |
| jpg | IMF1Ray | 30 |
| jpg | RGHS | 30 |
| jpg | CLAHE | 30 |
| jpg | Fused | 30 |
| jpg | Final | 30 |
| png | BPH | 30 |
| png | IMF1Ray | 30 |
| png | RGHS | 30 |
| png | CLAHE | 30 |
| png | Fused | 30 |
| png | Final | 30 |

- Missing files: `0`
- Decode failures: `0`

## Raw-vs-Final Smoke Metrics

| Stem | mean abs BGR delta | mean abs L delta | PSNR vs raw | grad mean ratio | luma std ratio |
|---|---:|---:|---:|---:|---:|
| chazhuang.1 | 7.536 | 0.717 | 27.608 | 0.994 | 0.996 |
| chichaoyiwan.17 | 18.189 | 0.996 | 21.453 | 1.003 | 1.011 |
| donghaiyuanjia.13 | 13.291 | 2.993 | 22.947 | 0.987 | 0.998 |
| donghaiyuanjia.4 | 12.407 | 2.907 | 22.920 | 0.981 | 0.986 |
| duolie.2 | 1.039 | 0.318 | 42.606 | 1.002 | 0.997 |
| hailianzao.10 | 5.519 | 0.503 | 31.746 | 1.009 | 1.024 |
| haiyangkadun.18 | 3.864 | 1.209 | 35.376 | 0.995 | 0.992 |
| haiyangyuanjia.4 | 3.604 | 0.690 | 29.839 | 0.991 | 0.986 |
| jiaomaozao.16 | 1.794 | 0.321 | 41.779 | 1.005 | 1.002 |
| jiaomaozao.7 | 0.429 | 0.158 | 50.951 | 1.001 | 0.998 |
| lianzhuangluojia.11 | 7.841 | 1.014 | 29.439 | 0.992 | 0.996 |
| limayuanjia.16 | 20.816 | 3.685 | 21.126 | 1.001 | 0.955 |
| lingxinghaixian.5 | 13.122 | 2.010 | 25.647 | 1.013 | 1.013 |
| mishikailun.10 | 12.810 | 0.391 | 24.673 | 1.007 | 1.011 |
| qiangzhuang.1 | 17.565 | 1.224 | 21.167 | 0.952 | 1.005 |
| qiangzhuang.29 | 3.937 | 0.487 | 32.646 | 1.000 | 1.001 |
| ribenxing.2 | 11.095 | 2.117 | 26.640 | 0.994 | 0.991 |
| shikelipu.1 | 10.744 | 1.799 | 26.836 | 0.990 | 0.983 |
| tama.13 | 4.425 | 0.351 | 32.986 | 1.033 | 0.999 |
| tiaowenhuangou.5 | 20.145 | 4.222 | 21.375 | 1.004 | 0.955 |
| weixiaoyuanjia.17 | 13.119 | 2.044 | 22.830 | 0.969 | 1.002 |
| weixiaoyuanjia.5 | 3.135 | 0.459 | 35.009 | 0.992 | 0.994 |
| xuehong.12 | 8.241 | 2.362 | 28.554 | 0.977 | 0.984 |
| yuanhai.13 | 13.547 | 1.942 | 22.691 | 0.999 | 0.993 |
| zhaixi.3 | 10.903 | 2.098 | 27.062 | 1.033 | 1.032 |
| weixiaoyuanjia.26 | 37.857 | 18.293 | 15.548 | 0.920 | 0.920 |
| xuehong.9 | 8.223 | 2.367 | 28.579 | 0.976 | 0.985 |
| donghaiyuanjia.26 | 37.856 | 19.999 | 15.712 | 0.840 | 0.899 |
| tama.14 | 7.522 | 0.192 | 28.793 | 0.991 | 0.983 |
| jianci.4 | 13.793 | 1.905 | 24.551 | 1.036 | 1.001 |

Mean metrics:

- mean_abs_bgr_delta: `11.4789`
- mean_abs_luma_delta: `2.6591`
- mean_abs_chroma_delta: `7.5182`
- psnr_vs_raw: `27.9695`
- grad_mean_ratio: `0.9895`
- luma_std_ratio: `0.9897`

## Stage Metrics CSV

- `topology_locked_visual_chroma_full_flow_v1_smoke30_broader_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\chazhuang.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\chichaoyiwan.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\donghaiyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\donghaiyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\duolie.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\hailianzao.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\haiyangkadun.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\haiyangyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\jiaomaozao.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\jiaomaozao.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\lianzhuangluojia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\limayuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\lingxinghaixian.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\mishikailun.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\qiangzhuang.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\qiangzhuang.29_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\ribenxing.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\shikelipu.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\tama.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\tiaowenhuangou.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\weixiaoyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\weixiaoyuanjia.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\xuehong.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\yuanhai.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\zhaixi.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\weixiaoyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\xuehong.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\donghaiyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\tama.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1\jianci.4_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
