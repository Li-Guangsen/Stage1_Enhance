# E01-B wavelet pyramid weak boundary myedge168_stage1_outputs_e01b_v1 status

Date: 2026-05-27

## Summary

- Status: `stage1_168_completed`
- Manifest: `experiments\e01_task_guided_family\manifests\myedge168_v1.txt`
- Output root: `experiments\e01_task_guided_family\outputs\myedge168\e01_b_wavelet_pyramid_weak_boundary_v1`
- Expected images: `168`
- Observed runtime: `13.8` sec total, `0.08` sec/image
- Projected 168 runtime: `0.2` min
- Decision: `proceed_to_fixed_detector_validation`

## Output Completeness

| Format | Stage | Count |
|---|---|---:|
| jpg | BPH | 168 |
| jpg | IMF1Ray | 168 |
| jpg | RGHS | 168 |
| jpg | CLAHE | 168 |
| jpg | Fused | 168 |
| jpg | Final | 168 |
| png | BPH | 168 |
| png | IMF1Ray | 168 |
| png | RGHS | 168 |
| png | CLAHE | 168 |
| png | Fused | 168 |
| png | Final | 168 |

- Missing files: `0`
- Decode failures: `0`

## Raw-vs-Final Smoke Metrics

| Stem | mean abs BGR delta | mean abs L delta | PSNR vs raw | grad mean ratio | luma std ratio |
|---|---:|---:|---:|---:|---:|
| chazhuang.3 | 0.821 | 0.778 | 48.983 | 1.006 | 0.994 |
| chazhuang.4 | 2.809 | 0.058 | 38.694 | 1.010 | 1.002 |
| chazhuang.6 | 0.001 | 0.001 | 77.913 | 1.000 | 1.000 |
| chichaoyiwan.1 | 3.329 | 0.997 | 35.904 | 1.005 | 1.009 |
| chichaoyiwan.16 | 3.346 | 0.996 | 35.880 | 1.005 | 1.007 |
| chichaoyiwan.2 | 3.276 | 0.997 | 36.005 | 1.002 | 1.008 |
| chichaoyiwan.3 | 3.219 | 0.999 | 36.134 | 1.003 | 1.009 |
| chichaoyiwan.4 | 3.209 | 0.999 | 36.140 | 1.004 | 1.010 |
| chichaoyiwan.5 | 2.546 | 0.999 | 38.225 | 1.002 | 1.001 |
| chichaoyiwan.6 | 3.018 | 0.981 | 37.433 | 0.991 | 0.993 |
| chichaoyiwan.7 | 3.176 | 0.983 | 37.102 | 0.991 | 0.992 |
| donghaiyuanjia.12 | 2.608 | 0.987 | 38.199 | 0.989 | 1.001 |
| donghaiyuanjia.13 | 2.622 | 0.999 | 38.476 | 1.002 | 1.002 |
| donghaiyuanjia.14 | 2.601 | 0.995 | 38.205 | 1.000 | 1.001 |
| donghaiyuanjia.15 | 2.627 | 0.991 | 38.373 | 0.998 | 1.001 |
| donghaiyuanjia.16 | 8.377 | 0.985 | 27.297 | 1.000 | 1.006 |
| donghaiyuanjia.17 | 8.358 | 0.970 | 27.361 | 1.011 | 1.000 |
| donghaiyuanjia.18 | 8.008 | 0.999 | 27.143 | 1.004 | 1.006 |
| donghaiyuanjia.19 | 2.664 | 0.997 | 37.350 | 1.003 | 1.003 |
| donghaiyuanjia.20 | 3.477 | 1.002 | 35.902 | 1.002 | 1.001 |
| donghaiyuanjia.21 | 3.360 | 1.002 | 36.196 | 1.001 | 1.001 |
| donghaiyuanjia.22 | 3.005 | 0.991 | 36.805 | 0.993 | 1.002 |
| donghaiyuanjia.24 | 4.521 | 0.999 | 33.304 | 1.004 | 1.001 |
| donghaiyuanjia.26 | 8.059 | 0.905 | 27.571 | 0.985 | 1.005 |
| duolie.5 | 3.121 | 0.961 | 37.432 | 0.999 | 0.997 |
| duolie.6 | 3.117 | 0.964 | 37.449 | 0.998 | 0.994 |
| duolie.7 | 3.054 | 0.961 | 37.593 | 0.998 | 0.992 |
| duolie.8 | 2.970 | 0.953 | 37.820 | 1.002 | 0.994 |
| duowenqigou.3 | 0.842 | 0.875 | 47.538 | 1.002 | 0.997 |
| duowenqigou.4 | 0.889 | 0.904 | 47.110 | 1.001 | 0.997 |
| fanquyuanjia.3 | 3.059 | 0.974 | 36.344 | 1.001 | 1.000 |
| fanquyuanjia.4 | 3.690 | 0.928 | 35.703 | 1.000 | 0.996 |
| gutiao.2 | 2.076 | 0.126 | 39.958 | 1.026 | 0.999 |
| hailianzao.10 | 1.680 | 0.734 | 41.346 | 1.010 | 0.994 |
| hailianzao.6 | 0.888 | 0.865 | 47.378 | 1.007 | 0.999 |
| hailianzao.7 | 0.917 | 0.554 | 46.381 | 1.051 | 1.000 |
| hailianzao.8 | 2.526 | 0.954 | 38.359 | 1.001 | 1.001 |
| haiyangkadun.10 | 2.949 | 0.982 | 36.749 | 1.011 | 1.002 |
| haiyangkadun.11 | 2.965 | 0.983 | 36.682 | 1.010 | 1.002 |
| haiyangkadun.12 | 2.953 | 0.977 | 36.796 | 1.004 | 1.003 |
| haiyangkadun.13 | 3.398 | 0.983 | 36.686 | 1.005 | 0.995 |
| haiyangkadun.14 | 3.232 | 0.962 | 37.135 | 1.013 | 0.997 |
| haiyangkadun.15 | 3.454 | 0.953 | 36.647 | 1.005 | 0.994 |
| haiyangkadun.16 | 3.083 | 0.965 | 37.533 | 1.011 | 0.993 |
| haiyangkadun.19 | 0.977 | 0.954 | 46.544 | 1.000 | 0.996 |
| haiyangkadun.20 | 3.120 | 0.701 | 36.899 | 1.000 | 0.990 |
| haiyangkadun.9 | 2.940 | 0.987 | 36.705 | 1.008 | 1.001 |
| haiyangyuanjia.6 | 2.101 | 0.931 | 39.848 | 1.001 | 0.998 |
| haiyangyuanjia.7 | 1.258 | 0.814 | 44.019 | 1.025 | 0.994 |
| haiyangyuanjia.8 | 1.601 | 0.622 | 42.303 | 1.038 | 1.005 |
| jianci.4 | 2.691 | 0.007 | 39.167 | 1.000 | 1.000 |
| jianci.5 | 2.911 | 0.031 | 38.370 | 1.001 | 0.998 |
| jianci.6 | 0.796 | 0.655 | 47.456 | 1.051 | 1.001 |
| jiaomaozao.13 | 0.820 | 0.837 | 48.112 | 1.007 | 0.996 |
| jiaomaozao.14 | 0.773 | 0.565 | 47.418 | 1.018 | 0.997 |
| jiaomaozao.17 | 1.062 | 0.670 | 45.279 | 1.034 | 0.999 |
| jiaomaozao.18 | 0.648 | 0.514 | 48.945 | 1.034 | 1.002 |
| jiaomaozao.19 | 0.977 | 0.670 | 45.977 | 1.009 | 0.997 |
| jiaomaozao.26 | 1.230 | 0.700 | 43.998 | 1.016 | 1.001 |
| jiaomaozao.27 | 0.885 | 0.894 | 47.865 | 1.015 | 0.996 |
| jiaomaozao.28 | 0.855 | 0.577 | 46.911 | 1.023 | 0.999 |
| jiaomaozao.29 | 2.179 | 0.966 | 39.818 | 1.005 | 1.000 |
| juciqigou.3 | 1.815 | 0.686 | 41.308 | 1.015 | 1.001 |
| kailun.2 | 2.807 | 0.637 | 37.524 | 1.029 | 1.006 |
| lianzhuang.4 | 2.714 | 0.949 | 38.552 | 1.000 | 0.992 |
| lianzhuang.5 | 1.981 | 0.950 | 40.270 | 1.001 | 0.992 |
| lianzhuang.6 | 2.062 | 0.937 | 40.020 | 1.001 | 0.993 |
| lianzhuangluojia.10 | 0.922 | 0.641 | 46.816 | 0.991 | 0.993 |
| lianzhuangluojia.11 | 2.038 | 0.983 | 41.177 | 1.003 | 0.992 |
| lianzhuangluojia.12 | 2.778 | 0.946 | 38.470 | 1.000 | 0.997 |
| lianzhuangluojia.13 | 1.171 | 0.893 | 45.081 | 1.005 | 0.998 |
| lianzhuangluojia.14 | 1.293 | 0.885 | 44.125 | 1.005 | 0.998 |
| lianzhuangluojia.8 | 3.177 | 0.994 | 36.278 | 1.001 | 1.000 |
| lianzhuangluojia.9 | 0.449 | 0.035 | 50.433 | 0.981 | 0.999 |
| limayuanjia.10 | 3.249 | 0.845 | 35.607 | 1.024 | 1.003 |
| limayuanjia.11 | 3.235 | 0.978 | 36.000 | 1.001 | 1.001 |
| limayuanjia.12 | 3.234 | 0.808 | 35.879 | 1.023 | 1.004 |
| limayuanjia.13 | 3.236 | 0.881 | 35.473 | 1.020 | 1.003 |
| limayuanjia.14 | 2.910 | 0.948 | 37.916 | 1.003 | 0.989 |
| limayuanjia.15 | 2.894 | 0.959 | 37.999 | 1.006 | 0.993 |
| limayuanjia.16 | 4.205 | 0.924 | 34.883 | 1.004 | 0.994 |
| limayuanjia.18 | 2.868 | 0.897 | 38.055 | 1.004 | 0.992 |
| limayuanjia.9 | 3.339 | 0.885 | 35.511 | 1.027 | 1.003 |
| lingxinghaixian.5 | 2.905 | 0.036 | 38.614 | 0.991 | 0.990 |
| lingxinghaixian.6 | 2.710 | 0.028 | 38.740 | 1.001 | 0.999 |
| luojiazao.4 | 1.337 | 0.837 | 43.461 | 1.007 | 0.988 |
| luojiazao.5 | 1.069 | 0.787 | 46.087 | 1.019 | 0.996 |
| luojiazao.6 | 1.341 | 0.705 | 43.115 | 1.008 | 0.993 |
| luoshijiaomao.3 | 1.694 | 0.934 | 41.884 | 1.012 | 1.003 |
| luoshijiaomao.4 | 1.997 | 0.955 | 40.512 | 1.008 | 1.000 |
| mashi.2 | 2.881 | 0.832 | 37.328 | 1.016 | 1.001 |
| mishikailun.8 | 1.127 | 0.786 | 45.066 | 0.996 | 0.995 |
| nilingxing.3 | 0.625 | 0.343 | 49.081 | 1.007 | 1.002 |
| nilingxing.4 | 1.297 | 0.924 | 44.013 | 1.002 | 1.003 |
| paige.4 | 0.107 | 0.053 | 57.815 | 1.003 | 1.000 |
| paige.5 | 2.945 | 0.021 | 38.269 | 1.000 | 0.998 |
| qiangzhuang.12 | 2.740 | 0.973 | 37.465 | 0.981 | 1.003 |
| qiangzhuang.13 | 2.820 | 0.987 | 37.438 | 0.991 | 1.004 |
| qiangzhuang.14 | 2.796 | 0.995 | 37.520 | 0.997 | 1.004 |
| qiangzhuang.15 | 2.806 | 0.995 | 37.446 | 0.997 | 1.003 |
| qiangzhuang.16 | 2.823 | 0.986 | 37.441 | 0.992 | 1.004 |
| qiangzhuang.17 | 4.667 | 0.999 | 33.505 | 1.003 | 1.004 |
| qiangzhuang.18 | 2.251 | 0.998 | 38.597 | 1.004 | 1.004 |
| qiangzhuang.19 | 2.267 | 0.999 | 38.510 | 1.003 | 1.003 |
| qiangzhuang.20 | 2.227 | 0.979 | 38.657 | 1.011 | 1.003 |
| qiangzhuang.21 | 2.251 | 0.991 | 38.615 | 1.005 | 1.003 |
| qiangzhuang.22 | 2.295 | 0.992 | 38.538 | 1.005 | 1.003 |
| qiangzhuang.25 | 2.262 | 0.992 | 38.593 | 1.004 | 1.002 |
| qiangzhuang.26 | 2.396 | 0.993 | 38.480 | 1.005 | 1.004 |
| qiangzhuang.28 | 2.328 | 0.996 | 38.541 | 1.005 | 1.004 |
| qiuxing.3 | 0.707 | 0.899 | 48.255 | 0.973 | 0.990 |
| qiuxing.4 | 2.839 | 0.964 | 38.125 | 1.010 | 0.996 |
| redai.3 | 2.215 | 0.947 | 40.545 | 0.998 | 0.995 |
| redai.4 | 2.561 | 0.948 | 39.071 | 1.005 | 0.997 |
| ribenxing.3 | 1.722 | 0.969 | 42.325 | 1.004 | 0.996 |
| ribenxing.4 | 2.756 | 0.967 | 38.294 | 1.013 | 1.002 |
| rouruo.3 | 0.881 | 0.937 | 47.664 | 1.018 | 1.006 |
| rouruo.4 | 2.249 | 0.967 | 39.537 | 1.006 | 1.000 |
| sanjiaoji.10 | 2.863 | 0.599 | 37.412 | 1.029 | 1.007 |
| sanjiaoji.9 | 2.836 | 0.582 | 37.501 | 1.030 | 1.007 |
| shikelipu.4 | 1.531 | 0.920 | 42.904 | 0.987 | 0.991 |
| shikelipu.5 | 2.585 | 0.972 | 38.932 | 1.002 | 1.001 |
| suojiao.6 | 3.029 | 0.086 | 38.088 | 1.007 | 0.998 |
| tama.10 | 7.745 | 1.002 | 28.021 | 1.002 | 1.001 |
| tama.11 | 1.560 | 0.995 | 41.555 | 1.002 | 0.993 |
| tama.12 | 8.202 | 0.998 | 27.430 | 0.999 | 1.002 |
| tama.13 | 1.431 | 0.907 | 42.769 | 1.046 | 0.991 |
| tama.14 | 1.610 | 0.996 | 41.368 | 1.002 | 0.993 |
| tama.16 | 0.138 | 0.040 | 56.730 | 1.016 | 1.000 |
| tama.8 | 8.059 | 1.002 | 27.606 | 1.002 | 1.002 |
| tama.9 | 1.571 | 0.996 | 41.546 | 1.002 | 0.993 |
| tiaowenhuangou.4 | 4.104 | 0.971 | 35.015 | 1.002 | 0.993 |
| tiaowenhuangou.5 | 4.089 | 0.969 | 35.047 | 1.001 | 0.993 |
| tiaowenhuangou.6 | 1.368 | 0.938 | 43.156 | 1.002 | 0.989 |
| weiruan.7 | 3.055 | 0.935 | 37.595 | 1.002 | 0.996 |
| weiruan.8 | 3.107 | 0.936 | 37.469 | 1.000 | 0.996 |
| weixiaoyuanjia.13 | 2.277 | 0.997 | 38.834 | 1.002 | 1.001 |
| weixiaoyuanjia.14 | 2.485 | 0.994 | 38.543 | 1.002 | 1.000 |
| weixiaoyuanjia.15 | 2.259 | 0.993 | 38.809 | 1.002 | 1.000 |
| weixiaoyuanjia.16 | 2.328 | 0.996 | 38.752 | 1.002 | 1.001 |
| weixiaoyuanjia.17 | 2.317 | 0.995 | 38.769 | 1.002 | 1.000 |
| weixiaoyuanjia.18 | 2.315 | 0.996 | 38.749 | 1.002 | 1.001 |
| weixiaoyuanjia.19 | 2.396 | 0.994 | 38.618 | 1.002 | 1.001 |
| weixiaoyuanjia.20 | 2.312 | 0.994 | 38.757 | 1.001 | 1.000 |
| weixiaoyuanjia.21 | 7.906 | 1.001 | 27.877 | 1.001 | 1.009 |
| weixiaoyuanjia.22 | 7.858 | 1.001 | 27.875 | 1.002 | 1.010 |
| weixiaoyuanjia.23 | 8.152 | 0.954 | 27.523 | 0.968 | 1.002 |
| weixiaoyuanjia.24 | 8.113 | 0.934 | 27.571 | 0.956 | 1.001 |
| weixiaoyuanjia.26 | 8.210 | 0.960 | 27.429 | 0.985 | 1.003 |
| weixiaoyuanjia.28 | 2.391 | 0.998 | 38.596 | 1.002 | 1.000 |
| xinyue.4 | 2.419 | 1.000 | 38.227 | 1.001 | 1.004 |
| xinyue.5 | 3.145 | 0.946 | 37.263 | 1.001 | 0.998 |
| xinyue.6 | 2.437 | 1.000 | 38.331 | 1.001 | 1.004 |
| xuanlianjiaomao.3 | 0.704 | 0.725 | 49.251 | 1.035 | 1.002 |
| xuanlianjiaomao.4 | 0.669 | 0.709 | 49.452 | 1.040 | 1.002 |
| xuehong.10 | 1.957 | 0.923 | 40.921 | 1.017 | 0.998 |
| xuehong.11 | 2.028 | 0.946 | 40.667 | 1.015 | 0.999 |
| xuehong.12 | 2.010 | 0.931 | 40.715 | 1.014 | 0.998 |
| xuehong.13 | 2.011 | 0.939 | 40.732 | 1.015 | 0.998 |
| xuehong.14 | 2.014 | 0.939 | 40.720 | 1.014 | 0.998 |
| xuehong.16 | 2.685 | 0.924 | 37.422 | 0.997 | 0.999 |
| xuehong.8 | 1.210 | 0.925 | 45.079 | 0.999 | 0.994 |
| xuehong.9 | 2.013 | 0.945 | 40.728 | 1.014 | 0.998 |
| yuanhai.6 | 2.335 | 0.997 | 38.764 | 1.001 | 1.000 |
| yuanhai.7 | 2.402 | 0.999 | 38.547 | 1.001 | 1.001 |
| yuanhai.8 | 2.384 | 0.998 | 38.587 | 1.001 | 1.000 |
| yuanjiazao.6 | 1.449 | 0.838 | 42.284 | 1.001 | 0.994 |
| yuanjiazao.8 | 2.667 | 0.889 | 38.129 | 1.007 | 0.999 |

Mean metrics:

- mean_abs_bgr_delta: `2.6889`
- mean_abs_luma_delta: `0.8504`
- mean_abs_chroma_delta: `1.6068`
- psnr_vs_raw: `39.5361`
- grad_mean_ratio: `1.0056`
- luma_std_ratio: `0.9993`

## Stage Metrics CSV

- `e01_b_wavelet_pyramid_weak_boundary_v1_myedge168_stage1_outputs_e01b_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chazhuang.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chazhuang.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chazhuang.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chichaoyiwan.1_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chichaoyiwan.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chichaoyiwan.2_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chichaoyiwan.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chichaoyiwan.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chichaoyiwan.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chichaoyiwan.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\chichaoyiwan.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.17_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.20_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.21_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.22_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.24_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\donghaiyuanjia.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\duolie.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\duolie.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\duolie.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\duolie.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\duowenqigou.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\duowenqigou.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\fanquyuanjia.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\fanquyuanjia.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\gutiao.2_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\hailianzao.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\hailianzao.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\hailianzao.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\hailianzao.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.20_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangkadun.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangyuanjia.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangyuanjia.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\haiyangyuanjia.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jianci.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jianci.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jianci.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.17_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.27_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.28_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\jiaomaozao.29_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\juciqigou.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\kailun.2_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuang.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuang.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuang.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuangluojia.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuangluojia.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuangluojia.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuangluojia.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuangluojia.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuangluojia.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lianzhuangluojia.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\limayuanjia.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lingxinghaixian.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\lingxinghaixian.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\luojiazao.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\luojiazao.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\luojiazao.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\luoshijiaomao.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\luoshijiaomao.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\mashi.2_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\mishikailun.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\nilingxing.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\nilingxing.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\paige.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\paige.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.17_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.20_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.21_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.22_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.25_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiangzhuang.28_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiuxing.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\qiuxing.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\redai.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\redai.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\ribenxing.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\ribenxing.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\rouruo.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\rouruo.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\sanjiaoji.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\sanjiaoji.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\shikelipu.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\shikelipu.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\suojiao.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tama.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tama.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tama.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tama.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tama.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tama.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tama.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tama.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tiaowenhuangou.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tiaowenhuangou.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\tiaowenhuangou.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weiruan.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weiruan.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.17_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.20_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.21_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.22_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.23_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.24_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\weixiaoyuanjia.28_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xinyue.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xinyue.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xinyue.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuanlianjiaomao.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuanlianjiaomao.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuehong.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuehong.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuehong.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuehong.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuehong.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuehong.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuehong.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\xuehong.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\yuanhai.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\yuanhai.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\yuanhai.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\yuanjiazao.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_e01b_v1\yuanjiazao.8_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
