# topology_locked_visual_chroma_full_flow_v1 smoke30_broader_v1_grayplane090 status

Date: 2026-05-27

## Summary

- Status: `smoke_complete_proxy_pending`
- Manifest: `experiments\topology_locked_visual_chroma_full_flow_v1\manifests\smoke30_broader_v1.txt`
- Output root: `experiments\topology_locked_visual_chroma_full_flow_v1\outputs\smoke30_broader_v1_grayplane090`
- Expected images: `30`
- Observed runtime: `13.1` sec total, `0.44` sec/image
- Projected 168 runtime: `1.2` min
- Decision: `run_168_proxy_if_visual_not_degraded`

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
| chazhuang.1 | 7.593 | 0.661 | 27.588 | 0.994 | 0.997 |
| chichaoyiwan.17 | 19.609 | 0.773 | 20.760 | 0.949 | 1.013 |
| donghaiyuanjia.13 | 14.594 | 2.393 | 21.929 | 1.006 | 1.016 |
| donghaiyuanjia.4 | 13.322 | 2.907 | 22.366 | 0.984 | 0.991 |
| duolie.2 | 1.272 | 0.268 | 38.339 | 1.000 | 0.995 |
| hailianzao.10 | 5.814 | 0.576 | 30.680 | 1.012 | 1.030 |
| haiyangkadun.18 | 4.006 | 1.157 | 35.003 | 0.998 | 1.001 |
| haiyangyuanjia.4 | 3.825 | 0.717 | 29.306 | 0.994 | 0.986 |
| jiaomaozao.16 | 1.823 | 0.303 | 41.602 | 1.003 | 1.001 |
| jiaomaozao.7 | 0.588 | 0.223 | 48.925 | 1.004 | 1.005 |
| lianzhuangluojia.11 | 7.928 | 0.841 | 29.290 | 0.986 | 1.004 |
| limayuanjia.16 | 20.952 | 3.737 | 21.070 | 0.999 | 0.955 |
| lingxinghaixian.5 | 13.681 | 2.015 | 25.279 | 1.009 | 1.008 |
| mishikailun.10 | 12.873 | 0.410 | 24.577 | 1.003 | 1.017 |
| qiangzhuang.1 | 19.339 | 1.952 | 19.972 | 0.985 | 1.000 |
| qiangzhuang.29 | 4.368 | 0.560 | 30.655 | 0.998 | 0.999 |
| ribenxing.2 | 11.221 | 2.109 | 26.537 | 0.998 | 0.993 |
| shikelipu.1 | 10.871 | 1.879 | 26.727 | 0.988 | 0.988 |
| tama.13 | 4.417 | 0.265 | 32.922 | 1.038 | 1.005 |
| tiaowenhuangou.5 | 20.241 | 4.256 | 21.336 | 1.005 | 0.956 |
| weixiaoyuanjia.17 | 13.927 | 1.844 | 22.260 | 0.962 | 1.013 |
| weixiaoyuanjia.5 | 3.225 | 0.471 | 34.634 | 0.992 | 0.995 |
| xuehong.12 | 8.428 | 2.357 | 28.410 | 0.972 | 0.988 |
| yuanhai.13 | 14.277 | 1.955 | 22.177 | 0.975 | 0.995 |
| zhaixi.3 | 11.168 | 2.213 | 26.862 | 0.997 | 1.030 |
| weixiaoyuanjia.26 | 38.993 | 18.638 | 15.307 | 0.972 | 0.924 |
| xuehong.9 | 8.411 | 2.365 | 28.433 | 0.977 | 0.989 |
| donghaiyuanjia.26 | 38.786 | 20.029 | 15.489 | 0.824 | 0.894 |
| tama.14 | 7.466 | 0.316 | 28.796 | 0.931 | 0.987 |
| jianci.4 | 14.223 | 2.003 | 24.220 | 1.005 | 1.003 |

Mean metrics:

- mean_abs_bgr_delta: `11.9081`
- mean_abs_luma_delta: `2.6731`
- mean_abs_chroma_delta: `7.8312`
- psnr_vs_raw: `27.3817`
- grad_mean_ratio: `0.9853`
- luma_std_ratio: `0.9926`

## Stage Metrics CSV

- `topology_locked_visual_chroma_full_flow_v1_smoke30_broader_v1_grayplane090_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\chazhuang.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\chichaoyiwan.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\donghaiyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\donghaiyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\duolie.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\hailianzao.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\haiyangkadun.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\haiyangyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\jiaomaozao.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\jiaomaozao.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\lianzhuangluojia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\limayuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\lingxinghaixian.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\mishikailun.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\qiangzhuang.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\qiangzhuang.29_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\ribenxing.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\shikelipu.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\tama.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\tiaowenhuangou.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\weixiaoyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\weixiaoyuanjia.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\xuehong.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\yuanhai.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\zhaixi.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\weixiaoyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\xuehong.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\donghaiyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\tama.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\smoke30_broader_v1_grayplane090\jianci.4_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
