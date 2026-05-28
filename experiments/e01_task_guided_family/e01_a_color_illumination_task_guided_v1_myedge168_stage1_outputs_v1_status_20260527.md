# E01-A color illumination task guided myedge168_stage1_outputs_v1 status

Date: 2026-05-27

## Summary

- Status: `stage1_168_completed`
- Manifest: `experiments\e01_task_guided_family\manifests\myedge168_v1.txt`
- Output root: `experiments\e01_task_guided_family\outputs\myedge168\e01_a_color_illumination_task_guided_v1`
- Expected images: `168`
- Observed runtime: `15.0` sec total, `0.09` sec/image
- Projected 168 runtime: `0.3` min
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
| chazhuang.3 | 0.953 | 0.904 | 48.340 | 0.997 | 0.999 |
| chazhuang.4 | 7.612 | 0.429 | 29.873 | 1.004 | 0.997 |
| chazhuang.6 | 0.490 | 0.397 | 51.223 | 1.057 | 1.016 |
| chichaoyiwan.1 | 11.533 | 0.948 | 25.526 | 1.007 | 1.000 |
| chichaoyiwan.16 | 11.617 | 0.980 | 25.464 | 1.006 | 1.000 |
| chichaoyiwan.2 | 11.377 | 0.983 | 25.603 | 1.000 | 1.000 |
| chichaoyiwan.3 | 11.329 | 0.962 | 25.640 | 1.006 | 0.998 |
| chichaoyiwan.4 | 11.010 | 0.960 | 25.883 | 0.968 | 0.995 |
| chichaoyiwan.5 | 8.321 | 0.947 | 26.824 | 1.006 | 1.000 |
| chichaoyiwan.6 | 5.922 | 0.878 | 31.810 | 1.057 | 1.008 |
| chichaoyiwan.7 | 6.194 | 0.980 | 31.440 | 1.012 | 1.001 |
| donghaiyuanjia.12 | 7.650 | 0.306 | 28.073 | 0.997 | 1.021 |
| donghaiyuanjia.13 | 7.488 | 0.384 | 28.244 | 0.907 | 1.014 |
| donghaiyuanjia.14 | 7.369 | 0.978 | 28.148 | 1.010 | 1.002 |
| donghaiyuanjia.15 | 7.541 | 0.291 | 28.183 | 0.949 | 1.011 |
| donghaiyuanjia.16 | 16.710 | 1.328 | 20.865 | 1.028 | 1.012 |
| donghaiyuanjia.17 | 16.807 | 1.359 | 20.879 | 0.913 | 0.997 |
| donghaiyuanjia.18 | 18.786 | 1.966 | 19.386 | 1.007 | 1.000 |
| donghaiyuanjia.19 | 8.895 | 1.972 | 26.179 | 1.020 | 1.001 |
| donghaiyuanjia.20 | 9.737 | 1.965 | 26.118 | 1.020 | 0.999 |
| donghaiyuanjia.21 | 9.690 | 1.963 | 26.177 | 1.024 | 1.000 |
| donghaiyuanjia.22 | 9.384 | 1.996 | 26.237 | 1.001 | 0.999 |
| donghaiyuanjia.24 | 12.086 | 0.057 | 25.271 | 0.996 | 1.009 |
| donghaiyuanjia.26 | 17.894 | 1.318 | 21.061 | 0.990 | 0.999 |
| duolie.5 | 7.558 | 0.967 | 29.756 | 1.000 | 1.000 |
| duolie.6 | 7.193 | 0.964 | 30.162 | 1.000 | 1.000 |
| duolie.7 | 6.994 | 0.970 | 30.423 | 1.001 | 1.000 |
| duolie.8 | 6.438 | 0.964 | 31.179 | 1.000 | 1.000 |
| duowenqigou.3 | 1.391 | 0.961 | 44.240 | 0.998 | 1.000 |
| duowenqigou.4 | 1.657 | 0.942 | 42.242 | 0.999 | 1.000 |
| fanquyuanjia.3 | 8.616 | 1.422 | 27.351 | 0.999 | 1.003 |
| fanquyuanjia.4 | 7.805 | 1.084 | 29.110 | 1.001 | 0.998 |
| gutiao.2 | 8.042 | 0.959 | 28.653 | 0.995 | 0.998 |
| hailianzao.10 | 3.368 | 0.945 | 35.663 | 1.000 | 0.997 |
| hailianzao.6 | 1.133 | 0.963 | 45.170 | 1.001 | 1.000 |
| hailianzao.7 | 1.235 | 0.845 | 44.586 | 1.008 | 1.001 |
| hailianzao.8 | 8.137 | 0.956 | 27.035 | 1.001 | 1.000 |
| haiyangkadun.10 | 8.679 | 1.129 | 28.452 | 1.017 | 1.004 |
| haiyangkadun.11 | 8.707 | 1.130 | 28.434 | 1.023 | 1.005 |
| haiyangkadun.12 | 8.765 | 1.133 | 28.409 | 1.023 | 1.005 |
| haiyangkadun.13 | 8.640 | 0.970 | 28.373 | 1.009 | 1.001 |
| haiyangkadun.14 | 9.700 | 0.985 | 27.435 | 1.009 | 1.000 |
| haiyangkadun.15 | 9.256 | 0.968 | 27.946 | 1.009 | 1.000 |
| haiyangkadun.16 | 8.169 | 0.988 | 29.046 | 1.001 | 1.000 |
| haiyangkadun.19 | 1.994 | 0.971 | 41.646 | 0.995 | 1.000 |
| haiyangkadun.20 | 7.297 | 1.011 | 29.578 | 1.002 | 0.987 |
| haiyangkadun.9 | 8.679 | 1.118 | 28.454 | 1.023 | 1.005 |
| haiyangyuanjia.6 | 3.758 | 0.978 | 34.099 | 1.000 | 1.000 |
| haiyangyuanjia.7 | 4.282 | 0.864 | 34.198 | 0.999 | 0.992 |
| haiyangyuanjia.8 | 2.638 | 0.977 | 38.423 | 1.002 | 1.000 |
| jianci.4 | 6.924 | 0.869 | 30.548 | 1.021 | 1.023 |
| jianci.5 | 9.340 | 0.002 | 28.141 | 1.000 | 1.000 |
| jianci.6 | 0.994 | 0.925 | 46.413 | 1.004 | 1.001 |
| jiaomaozao.13 | 0.899 | 0.950 | 47.848 | 1.001 | 1.000 |
| jiaomaozao.14 | 1.069 | 0.916 | 46.187 | 0.998 | 1.000 |
| jiaomaozao.17 | 1.529 | 0.936 | 42.169 | 1.005 | 1.001 |
| jiaomaozao.18 | 0.965 | 0.935 | 47.113 | 0.999 | 1.001 |
| jiaomaozao.19 | 1.237 | 0.897 | 44.632 | 1.002 | 0.999 |
| jiaomaozao.26 | 1.356 | 0.964 | 43.167 | 1.000 | 1.000 |
| jiaomaozao.27 | 0.925 | 0.953 | 47.699 | 1.008 | 1.001 |
| jiaomaozao.28 | 1.244 | 0.902 | 44.774 | 0.999 | 0.999 |
| jiaomaozao.29 | 7.370 | 0.962 | 30.292 | 1.007 | 1.001 |
| juciqigou.3 | 2.819 | 0.958 | 37.730 | 1.001 | 1.000 |
| kailun.2 | 6.525 | 0.939 | 29.950 | 0.999 | 1.000 |
| lianzhuang.4 | 5.720 | 0.985 | 32.074 | 1.000 | 0.995 |
| lianzhuang.5 | 4.951 | 0.986 | 33.132 | 1.000 | 0.997 |
| lianzhuang.6 | 5.131 | 0.975 | 32.814 | 1.000 | 0.995 |
| lianzhuangluojia.10 | 2.125 | 0.968 | 39.039 | 0.978 | 0.992 |
| lianzhuangluojia.11 | 5.106 | 0.997 | 33.277 | 1.000 | 0.999 |
| lianzhuangluojia.12 | 6.287 | 0.976 | 30.919 | 0.998 | 0.999 |
| lianzhuangluojia.13 | 2.680 | 0.909 | 38.844 | 1.008 | 1.002 |
| lianzhuangluojia.14 | 2.558 | 0.912 | 39.077 | 1.009 | 1.002 |
| lianzhuangluojia.8 | 10.673 | 0.989 | 25.932 | 0.996 | 1.000 |
| lianzhuangluojia.9 | 2.308 | 0.957 | 38.204 | 1.006 | 0.984 |
| limayuanjia.10 | 10.084 | 1.654 | 26.874 | 1.029 | 1.000 |
| limayuanjia.11 | 10.298 | 1.833 | 26.884 | 1.004 | 0.994 |
| limayuanjia.12 | 10.096 | 1.601 | 26.964 | 1.026 | 0.999 |
| limayuanjia.13 | 10.336 | 1.608 | 26.751 | 1.030 | 1.000 |
| limayuanjia.14 | 6.054 | 0.967 | 31.512 | 0.996 | 0.992 |
| limayuanjia.15 | 6.543 | 0.993 | 30.811 | 0.997 | 0.999 |
| limayuanjia.16 | 11.771 | 1.072 | 25.759 | 1.003 | 0.997 |
| limayuanjia.18 | 6.969 | 0.899 | 30.256 | 1.005 | 0.994 |
| limayuanjia.9 | 10.224 | 1.686 | 26.868 | 1.037 | 1.001 |
| lingxinghaixian.5 | 9.137 | 0.005 | 28.617 | 0.998 | 0.998 |
| lingxinghaixian.6 | 6.583 | 0.893 | 30.881 | 1.007 | 1.004 |
| luojiazao.4 | 1.827 | 0.821 | 39.612 | 0.999 | 0.986 |
| luojiazao.5 | 1.940 | 0.666 | 40.616 | 1.030 | 1.000 |
| luojiazao.6 | 2.147 | 0.659 | 38.625 | 1.000 | 0.990 |
| luoshijiaomao.3 | 3.911 | 0.964 | 34.522 | 1.002 | 1.002 |
| luoshijiaomao.4 | 3.385 | 0.963 | 34.773 | 1.003 | 1.002 |
| mashi.2 | 6.411 | 0.964 | 29.937 | 0.999 | 1.000 |
| mishikailun.8 | 2.169 | 0.905 | 39.627 | 0.997 | 0.999 |
| nilingxing.3 | 2.648 | 0.316 | 38.198 | 1.003 | 1.022 |
| nilingxing.4 | 2.821 | 0.981 | 38.406 | 1.004 | 1.001 |
| paige.4 | 1.064 | 0.990 | 46.344 | 1.000 | 0.999 |
| paige.5 | 7.505 | 0.943 | 30.402 | 0.997 | 1.016 |
| qiangzhuang.12 | 9.022 | 1.982 | 26.085 | 0.989 | 0.998 |
| qiangzhuang.13 | 8.085 | 1.046 | 27.376 | 0.996 | 1.012 |
| qiangzhuang.14 | 9.196 | 1.990 | 26.096 | 0.996 | 0.998 |
| qiangzhuang.15 | 8.920 | 1.985 | 26.112 | 0.995 | 0.998 |
| qiangzhuang.16 | 8.083 | 1.052 | 27.380 | 0.999 | 1.012 |
| qiangzhuang.17 | 11.596 | 1.160 | 25.859 | 0.994 | 1.007 |
| qiangzhuang.18 | 7.685 | 0.997 | 26.860 | 1.002 | 0.999 |
| qiangzhuang.19 | 7.673 | 0.996 | 26.873 | 1.002 | 0.999 |
| qiangzhuang.20 | 7.664 | 0.996 | 26.871 | 1.001 | 0.999 |
| qiangzhuang.21 | 7.668 | 0.993 | 26.861 | 1.004 | 1.000 |
| qiangzhuang.22 | 7.666 | 0.994 | 26.861 | 1.004 | 1.000 |
| qiangzhuang.25 | 7.658 | 0.991 | 26.883 | 1.004 | 1.000 |
| qiangzhuang.26 | 7.673 | 0.993 | 26.865 | 1.004 | 1.000 |
| qiangzhuang.28 | 7.683 | 0.996 | 26.861 | 1.003 | 1.000 |
| qiuxing.3 | 1.476 | 0.921 | 43.098 | 0.977 | 0.996 |
| qiuxing.4 | 8.381 | 0.968 | 28.577 | 1.008 | 1.002 |
| redai.3 | 5.547 | 0.987 | 32.280 | 0.999 | 0.999 |
| redai.4 | 6.604 | 1.000 | 30.318 | 1.001 | 1.000 |
| ribenxing.3 | 2.397 | 0.967 | 38.425 | 1.007 | 1.001 |
| ribenxing.4 | 5.931 | 0.986 | 31.835 | 1.005 | 1.000 |
| rouruo.3 | 0.896 | 0.970 | 47.587 | 1.008 | 1.003 |
| rouruo.4 | 5.510 | 0.962 | 32.243 | 0.996 | 0.999 |
| sanjiaoji.10 | 5.915 | 0.942 | 30.847 | 1.000 | 0.999 |
| sanjiaoji.9 | 5.762 | 0.939 | 31.075 | 0.999 | 0.999 |
| shikelipu.4 | 4.736 | 0.988 | 33.672 | 0.999 | 0.998 |
| shikelipu.5 | 6.259 | 0.975 | 30.876 | 1.002 | 0.999 |
| suojiao.6 | 6.752 | 0.043 | 29.356 | 1.001 | 0.997 |
| tama.10 | 15.729 | 1.399 | 22.580 | 1.031 | 1.002 |
| tama.11 | 4.097 | 1.000 | 34.066 | 0.999 | 0.999 |
| tama.12 | 15.911 | 1.089 | 22.413 | 0.978 | 1.008 |
| tama.13 | 2.159 | 0.822 | 39.285 | 0.953 | 1.000 |
| tama.14 | 4.124 | 0.999 | 34.013 | 1.000 | 0.999 |
| tama.16 | 1.159 | 0.983 | 45.862 | 1.007 | 0.999 |
| tama.8 | 15.966 | 1.389 | 22.429 | 0.995 | 1.002 |
| tama.9 | 4.101 | 1.000 | 34.062 | 1.000 | 0.999 |
| tiaowenhuangou.4 | 11.546 | 1.176 | 25.842 | 1.000 | 0.996 |
| tiaowenhuangou.5 | 11.449 | 1.172 | 25.925 | 1.000 | 0.996 |
| tiaowenhuangou.6 | 4.519 | 0.957 | 33.974 | 1.000 | 0.990 |
| weiruan.7 | 7.224 | 0.956 | 30.115 | 1.001 | 1.000 |
| weiruan.8 | 7.853 | 0.951 | 29.395 | 1.002 | 1.001 |
| weixiaoyuanjia.13 | 7.700 | 0.957 | 26.972 | 1.025 | 1.002 |
| weixiaoyuanjia.14 | 7.703 | 0.968 | 26.971 | 1.019 | 1.001 |
| weixiaoyuanjia.15 | 7.740 | 0.970 | 26.967 | 1.017 | 1.001 |
| weixiaoyuanjia.16 | 7.946 | 0.960 | 26.936 | 1.023 | 1.001 |
| weixiaoyuanjia.17 | 7.929 | 0.955 | 26.950 | 1.016 | 1.001 |
| weixiaoyuanjia.18 | 7.913 | 0.977 | 26.947 | 1.010 | 1.000 |
| weixiaoyuanjia.19 | 8.036 | 0.971 | 26.911 | 1.016 | 1.001 |
| weixiaoyuanjia.20 | 7.791 | 0.948 | 26.984 | 1.023 | 1.002 |
| weixiaoyuanjia.21 | 18.040 | 1.787 | 21.141 | 1.046 | 1.003 |
| weixiaoyuanjia.22 | 17.724 | 1.557 | 21.278 | 1.071 | 0.975 |
| weixiaoyuanjia.23 | 18.369 | 1.789 | 20.903 | 0.933 | 0.983 |
| weixiaoyuanjia.24 | 18.370 | 1.797 | 20.903 | 0.901 | 0.977 |
| weixiaoyuanjia.26 | 18.818 | 1.921 | 20.797 | 0.982 | 0.987 |
| weixiaoyuanjia.28 | 7.803 | 0.973 | 26.966 | 1.018 | 1.000 |
| xinyue.4 | 8.033 | 0.912 | 26.858 | 1.074 | 1.013 |
| xinyue.5 | 6.779 | 0.964 | 30.583 | 1.003 | 1.001 |
| xinyue.6 | 8.140 | 0.950 | 26.933 | 1.045 | 1.011 |
| xuanlianjiaomao.3 | 0.868 | 0.876 | 48.055 | 1.002 | 1.000 |
| xuanlianjiaomao.4 | 0.834 | 0.870 | 48.360 | 0.991 | 1.000 |
| xuehong.10 | 4.663 | 0.955 | 33.341 | 0.998 | 1.000 |
| xuehong.11 | 5.171 | 0.950 | 32.162 | 1.004 | 1.000 |
| xuehong.12 | 5.186 | 0.944 | 32.166 | 1.004 | 1.000 |
| xuehong.13 | 5.175 | 0.950 | 32.179 | 1.004 | 1.000 |
| xuehong.14 | 5.187 | 0.947 | 32.171 | 1.004 | 1.000 |
| xuehong.16 | 8.003 | 1.163 | 27.700 | 1.004 | 0.994 |
| xuehong.8 | 3.871 | 0.950 | 35.052 | 0.996 | 0.999 |
| xuehong.9 | 5.172 | 0.950 | 32.171 | 1.003 | 1.001 |
| yuanhai.6 | 8.390 | 0.909 | 26.827 | 1.077 | 1.004 |
| yuanhai.7 | 5.874 | 0.321 | 29.869 | 0.839 | 1.010 |
| yuanhai.8 | 8.379 | 0.882 | 26.829 | 1.076 | 1.005 |
| yuanjiazao.6 | 3.112 | 0.902 | 35.762 | 0.999 | 0.992 |
| yuanjiazao.8 | 5.292 | 0.958 | 31.619 | 1.000 | 1.000 |

Mean metrics:

- mean_abs_bgr_delta: `6.9611`
- mean_abs_luma_delta: `1.0247`
- mean_abs_chroma_delta: `4.5844`
- psnr_vs_raw: `31.5832`
- grad_mean_ratio: `1.0029`
- luma_std_ratio: `1.0002`

## Stage Metrics CSV

- `e01_a_color_illumination_task_guided_v1_myedge168_stage1_outputs_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chazhuang.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chazhuang.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chazhuang.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chichaoyiwan.1_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chichaoyiwan.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chichaoyiwan.2_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chichaoyiwan.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chichaoyiwan.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chichaoyiwan.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chichaoyiwan.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\chichaoyiwan.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.17_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.20_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.21_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.22_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.24_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\donghaiyuanjia.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\duolie.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\duolie.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\duolie.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\duolie.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\duowenqigou.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\duowenqigou.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\fanquyuanjia.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\fanquyuanjia.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\gutiao.2_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\hailianzao.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\hailianzao.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\hailianzao.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\hailianzao.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.20_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangkadun.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangyuanjia.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangyuanjia.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\haiyangyuanjia.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jianci.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jianci.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jianci.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.17_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.27_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.28_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\jiaomaozao.29_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\juciqigou.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\kailun.2_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuang.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuang.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuang.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuangluojia.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuangluojia.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuangluojia.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuangluojia.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuangluojia.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuangluojia.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lianzhuangluojia.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\limayuanjia.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lingxinghaixian.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\lingxinghaixian.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\luojiazao.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\luojiazao.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\luojiazao.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\luoshijiaomao.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\luoshijiaomao.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\mashi.2_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\mishikailun.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\nilingxing.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\nilingxing.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\paige.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\paige.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.17_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.20_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.21_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.22_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.25_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiangzhuang.28_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiuxing.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\qiuxing.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\redai.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\redai.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\ribenxing.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\ribenxing.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\rouruo.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\rouruo.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\sanjiaoji.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\sanjiaoji.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\shikelipu.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\shikelipu.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\suojiao.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tama.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tama.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tama.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tama.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tama.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tama.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tama.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tama.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tiaowenhuangou.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tiaowenhuangou.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\tiaowenhuangou.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weiruan.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weiruan.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.15_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.17_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.18_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.19_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.20_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.21_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.22_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.23_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.24_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.26_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\weixiaoyuanjia.28_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xinyue.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xinyue.5_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xinyue.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuanlianjiaomao.3_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuanlianjiaomao.4_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuehong.10_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuehong.11_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuehong.12_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuehong.13_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuehong.14_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuehong.16_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuehong.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\xuehong.9_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\yuanhai.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\yuanhai.7_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\yuanhai.8_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\yuanjiazao.6_panel.jpg`
- `experiments\e01_task_guided_family\diagnostics\myedge168_stage1_outputs_v1\yuanjiazao.8_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
