# topology_locked_visual_chroma_full_flow_v1 myedge168_v1_grayplane090_anchorfix status

Date: 2026-05-27

## Summary

- Status: `stage1_output_complete_proxy_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\myedge168_v1.txt`
- Output root: `experiments\topology_locked_visual_chroma_full_flow_v1\outputs\myedge168_v1_grayplane090_anchorfix`
- Expected images: `168`
- Observed runtime: `76.2` sec total, `0.45` sec/image
- Projected 168 runtime: `1.3` min
- Decision: `proxy_prescreen_required_before_fixed_detector`

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
| chazhuang.3 | 0.025 | 0.014 | 63.201 | 1.000 | 1.000 |
| chazhuang.4 | 15.669 | 2.011 | 23.118 | 1.012 | 1.011 |
| chazhuang.6 | 0.069 | 0.009 | 58.605 | 1.001 | 1.000 |
| chichaoyiwan.1 | 21.427 | 0.883 | 20.058 | 1.007 | 1.014 |
| chichaoyiwan.16 | 21.145 | 0.823 | 20.105 | 0.962 | 0.997 |
| chichaoyiwan.2 | 20.798 | 0.991 | 20.175 | 1.012 | 1.010 |
| chichaoyiwan.3 | 20.989 | 0.864 | 20.143 | 0.969 | 0.985 |
| chichaoyiwan.4 | 20.834 | 0.984 | 20.168 | 0.979 | 1.005 |
| chichaoyiwan.5 | 14.742 | 1.844 | 21.876 | 0.998 | 1.020 |
| chichaoyiwan.6 | 9.449 | 1.325 | 27.656 | 0.928 | 0.987 |
| chichaoyiwan.7 | 9.668 | 1.414 | 27.487 | 0.941 | 0.986 |
| donghaiyuanjia.12 | 14.368 | 3.034 | 22.029 | 1.004 | 1.005 |
| donghaiyuanjia.13 | 12.754 | 2.980 | 23.118 | 1.002 | 0.996 |
| donghaiyuanjia.14 | 14.407 | 3.268 | 22.037 | 1.009 | 0.997 |
| donghaiyuanjia.15 | 14.400 | 3.019 | 22.034 | 1.000 | 1.001 |
| donghaiyuanjia.16 | 18.226 | 3.443 | 20.227 | 0.877 | 0.978 |
| donghaiyuanjia.17 | 18.011 | 3.275 | 20.326 | 0.969 | 0.990 |
| donghaiyuanjia.18 | 17.922 | 3.944 | 20.347 | 1.027 | 0.983 |
| donghaiyuanjia.19 | 14.337 | 3.023 | 21.941 | 1.004 | 0.995 |
| donghaiyuanjia.20 | 19.940 | 3.035 | 19.447 | 1.022 | 1.000 |
| donghaiyuanjia.21 | 19.648 | 3.058 | 19.504 | 1.033 | 1.000 |
| donghaiyuanjia.22 | 19.799 | 3.102 | 19.463 | 1.050 | 1.000 |
| donghaiyuanjia.24 | 22.372 | 1.718 | 18.749 | 1.131 | 1.013 |
| donghaiyuanjia.26 | 21.719 | 3.980 | 18.801 | 1.004 | 0.995 |
| duolie.5 | 12.742 | 1.742 | 25.315 | 0.998 | 0.998 |
| duolie.6 | 12.260 | 1.602 | 25.611 | 0.997 | 0.998 |
| duolie.7 | 12.074 | 1.670 | 25.761 | 0.995 | 1.000 |
| duolie.8 | 11.262 | 1.612 | 26.377 | 0.991 | 0.999 |
| duowenqigou.3 | 2.636 | 0.791 | 37.445 | 0.990 | 1.004 |
| duowenqigou.4 | 2.876 | 0.907 | 36.785 | 0.988 | 0.997 |
| fanquyuanjia.3 | 17.603 | 3.268 | 20.377 | 1.003 | 1.005 |
| fanquyuanjia.4 | 14.703 | 3.055 | 23.776 | 1.008 | 0.980 |
| gutiao.2 | 13.249 | 1.777 | 24.247 | 0.997 | 0.984 |
| hailianzao.10 | 6.104 | 0.693 | 29.610 | 1.015 | 1.035 |
| hailianzao.6 | 1.235 | 0.316 | 40.623 | 1.003 | 1.000 |
| hailianzao.7 | 1.432 | 0.403 | 40.547 | 1.006 | 1.007 |
| hailianzao.8 | 14.663 | 1.615 | 22.042 | 1.003 | 0.995 |
| haiyangkadun.10 | 9.939 | 2.791 | 26.343 | 0.947 | 0.999 |
| haiyangkadun.11 | 9.938 | 2.750 | 26.367 | 0.936 | 0.999 |
| haiyangkadun.12 | 9.952 | 2.688 | 26.349 | 0.917 | 1.004 |
| haiyangkadun.13 | 16.085 | 2.320 | 23.193 | 0.988 | 1.000 |
| haiyangkadun.14 | 16.133 | 2.124 | 23.170 | 0.974 | 0.992 |
| haiyangkadun.15 | 15.513 | 2.287 | 23.644 | 0.964 | 0.993 |
| haiyangkadun.16 | 13.829 | 2.058 | 24.616 | 0.968 | 0.992 |
| haiyangkadun.19 | 3.920 | 1.124 | 34.988 | 0.991 | 1.007 |
| haiyangkadun.20 | 13.590 | 2.357 | 23.893 | 1.001 | 1.018 |
| haiyangkadun.9 | 9.955 | 2.756 | 26.327 | 0.949 | 1.001 |
| haiyangyuanjia.6 | 6.170 | 1.143 | 28.659 | 0.994 | 1.003 |
| haiyangyuanjia.7 | 5.950 | 0.519 | 31.019 | 0.971 | 1.001 |
| haiyangyuanjia.8 | 4.654 | 0.688 | 32.747 | 1.003 | 1.023 |
| jianci.4 | 14.555 | 2.002 | 23.948 | 1.004 | 1.003 |
| jianci.5 | 12.364 | 2.020 | 26.066 | 1.010 | 1.009 |
| jianci.6 | 0.664 | 0.587 | 48.473 | 1.004 | 1.003 |
| jiaomaozao.13 | 0.764 | 0.229 | 43.549 | 1.004 | 1.004 |
| jiaomaozao.14 | 0.800 | 0.183 | 43.867 | 1.002 | 1.002 |
| jiaomaozao.17 | 2.232 | 0.338 | 36.791 | 0.997 | 1.006 |
| jiaomaozao.18 | 0.598 | 0.148 | 46.338 | 1.001 | 1.003 |
| jiaomaozao.19 | 1.223 | 0.298 | 41.277 | 1.001 | 1.002 |
| jiaomaozao.26 | 1.921 | 0.274 | 40.090 | 0.998 | 0.998 |
| jiaomaozao.27 | 0.417 | 0.112 | 46.988 | 1.006 | 1.006 |
| jiaomaozao.28 | 0.888 | 0.209 | 41.723 | 1.002 | 1.008 |
| jiaomaozao.29 | 9.284 | 2.804 | 28.525 | 0.977 | 0.991 |
| juciqigou.3 | 4.064 | 0.308 | 33.180 | 1.002 | 1.005 |
| kailun.2 | 9.685 | 0.358 | 26.558 | 1.006 | 1.005 |
| lianzhuang.4 | 9.659 | 1.416 | 27.508 | 0.998 | 0.996 |
| lianzhuang.5 | 8.487 | 0.995 | 28.399 | 1.000 | 1.004 |
| lianzhuang.6 | 8.796 | 1.051 | 28.094 | 0.996 | 0.999 |
| lianzhuangluojia.10 | 3.132 | 0.477 | 35.320 | 0.959 | 1.011 |
| lianzhuangluojia.11 | 7.941 | 0.852 | 29.291 | 0.987 | 1.009 |
| lianzhuangluojia.12 | 11.170 | 2.751 | 26.418 | 0.998 | 0.995 |
| lianzhuangluojia.13 | 4.703 | 1.216 | 33.652 | 0.986 | 1.000 |
| lianzhuangluojia.14 | 4.566 | 1.164 | 33.820 | 0.987 | 1.001 |
| lianzhuangluojia.8 | 20.872 | 1.090 | 20.104 | 1.000 | 1.037 |
| lianzhuangluojia.9 | 3.089 | 0.514 | 35.389 | 1.000 | 1.020 |
| limayuanjia.10 | 10.432 | 2.920 | 26.184 | 0.990 | 0.991 |
| limayuanjia.11 | 9.746 | 2.910 | 26.203 | 0.982 | 0.995 |
| limayuanjia.12 | 10.680 | 3.057 | 25.679 | 0.972 | 0.996 |
| limayuanjia.13 | 10.348 | 2.865 | 26.217 | 0.985 | 0.992 |
| limayuanjia.14 | 10.217 | 1.387 | 26.981 | 0.983 | 1.000 |
| limayuanjia.15 | 11.027 | 1.373 | 26.269 | 0.997 | 0.998 |
| limayuanjia.16 | 16.523 | 2.885 | 23.107 | 0.993 | 0.987 |
| limayuanjia.18 | 12.660 | 1.934 | 25.120 | 0.995 | 0.998 |
| limayuanjia.9 | 12.360 | 3.555 | 24.533 | 0.986 | 0.978 |
| lingxinghaixian.5 | 13.977 | 2.004 | 25.066 | 1.009 | 1.011 |
| lingxinghaixian.6 | 13.659 | 1.921 | 23.509 | 1.009 | 1.017 |
| luojiazao.4 | 3.604 | 0.550 | 33.693 | 1.008 | 1.023 |
| luojiazao.5 | 3.512 | 0.699 | 33.597 | 1.023 | 1.016 |
| luojiazao.6 | 6.763 | 0.808 | 28.868 | 1.004 | 1.018 |
| luoshijiaomao.3 | 6.334 | 1.325 | 30.760 | 0.995 | 1.000 |
| luoshijiaomao.4 | 5.498 | 1.062 | 30.632 | 0.996 | 0.998 |
| mashi.2 | 9.547 | 0.291 | 26.395 | 1.000 | 1.006 |
| mishikailun.8 | 3.880 | 0.382 | 32.086 | 1.002 | 1.009 |
| nilingxing.3 | 2.910 | 0.272 | 37.796 | 1.001 | 0.999 |
| nilingxing.4 | 4.248 | 0.480 | 34.544 | 1.005 | 0.997 |
| paige.4 | 0.466 | 0.141 | 47.569 | 1.002 | 1.001 |
| paige.5 | 13.373 | 1.998 | 25.335 | 1.023 | 1.017 |
| qiangzhuang.12 | 7.839 | 2.076 | 27.368 | 1.024 | 1.002 |
| qiangzhuang.13 | 7.824 | 1.982 | 27.355 | 1.051 | 1.005 |
| qiangzhuang.14 | 7.777 | 1.919 | 27.397 | 1.053 | 1.002 |
| qiangzhuang.15 | 7.796 | 1.966 | 27.390 | 1.038 | 1.004 |
| qiangzhuang.16 | 7.549 | 1.796 | 27.582 | 1.081 | 1.013 |
| qiangzhuang.17 | 29.688 | 3.029 | 17.102 | 1.024 | 1.024 |
| qiangzhuang.18 | 14.555 | 2.054 | 21.773 | 0.989 | 1.011 |
| qiangzhuang.19 | 14.520 | 2.096 | 21.785 | 0.998 | 1.010 |
| qiangzhuang.20 | 14.506 | 2.042 | 21.791 | 0.990 | 1.011 |
| qiangzhuang.21 | 14.502 | 2.082 | 21.815 | 0.976 | 1.006 |
| qiangzhuang.22 | 14.512 | 2.086 | 21.812 | 0.977 | 1.006 |
| qiangzhuang.25 | 14.547 | 2.115 | 21.798 | 0.974 | 1.005 |
| qiangzhuang.26 | 14.558 | 2.091 | 21.797 | 0.973 | 1.011 |
| qiangzhuang.28 | 14.520 | 2.139 | 21.812 | 0.993 | 1.008 |
| qiuxing.3 | 2.892 | 1.020 | 36.920 | 0.977 | 1.002 |
| qiuxing.4 | 12.853 | 1.239 | 24.886 | 1.034 | 1.004 |
| redai.3 | 9.644 | 2.123 | 27.781 | 0.996 | 0.988 |
| redai.4 | 11.506 | 2.847 | 26.074 | 1.006 | 0.991 |
| ribenxing.3 | 3.886 | 0.541 | 33.396 | 1.001 | 1.002 |
| ribenxing.4 | 10.176 | 1.315 | 27.152 | 0.971 | 0.990 |
| rouruo.3 | 0.611 | 0.260 | 47.477 | 0.984 | 1.001 |
| rouruo.4 | 9.107 | 1.210 | 27.891 | 0.990 | 0.989 |
| sanjiaoji.10 | 8.978 | 0.205 | 27.243 | 1.002 | 1.002 |
| sanjiaoji.9 | 8.862 | 0.195 | 27.356 | 0.997 | 0.999 |
| shikelipu.4 | 2.673 | 0.454 | 38.515 | 1.011 | 1.000 |
| shikelipu.5 | 11.333 | 2.730 | 26.214 | 1.005 | 0.989 |
| suojiao.6 | 13.081 | 1.861 | 23.278 | 0.970 | 0.995 |
| tama.10 | 22.516 | 3.912 | 18.717 | 1.006 | 0.982 |
| tama.11 | 7.479 | 0.335 | 28.785 | 0.931 | 0.988 |
| tama.12 | 17.971 | 3.644 | 20.459 | 1.052 | 0.980 |
| tama.13 | 4.436 | 0.268 | 32.901 | 1.039 | 1.009 |
| tama.14 | 7.467 | 0.316 | 28.795 | 0.932 | 0.988 |
| tama.16 | 0.508 | 0.149 | 48.655 | 1.022 | 1.006 |
| tama.8 | 22.531 | 3.907 | 18.702 | 0.979 | 0.981 |
| tama.9 | 7.466 | 0.339 | 28.799 | 0.929 | 0.987 |
| tiaowenhuangou.4 | 13.436 | 2.821 | 24.869 | 0.996 | 0.986 |
| tiaowenhuangou.5 | 13.412 | 2.830 | 24.892 | 0.993 | 0.986 |
| tiaowenhuangou.6 | 7.459 | 1.038 | 29.626 | 0.998 | 1.004 |
| weiruan.7 | 12.023 | 1.611 | 25.744 | 0.992 | 0.993 |
| weiruan.8 | 13.345 | 1.777 | 24.857 | 0.998 | 0.993 |
| weixiaoyuanjia.13 | 14.314 | 2.102 | 21.952 | 0.993 | 1.010 |
| weixiaoyuanjia.14 | 14.742 | 2.148 | 21.857 | 0.995 | 1.005 |
| weixiaoyuanjia.15 | 14.440 | 1.995 | 21.868 | 0.956 | 1.007 |
| weixiaoyuanjia.16 | 14.774 | 1.919 | 21.817 | 0.968 | 1.014 |
| weixiaoyuanjia.17 | 14.760 | 1.935 | 21.799 | 0.983 | 1.017 |
| weixiaoyuanjia.18 | 14.756 | 2.054 | 21.841 | 0.981 | 1.011 |
| weixiaoyuanjia.19 | 14.761 | 1.587 | 21.761 | 0.999 | 1.012 |
| weixiaoyuanjia.20 | 14.425 | 1.871 | 21.872 | 0.981 | 1.016 |
| weixiaoyuanjia.21 | 22.273 | 3.988 | 18.815 | 0.933 | 0.887 |
| weixiaoyuanjia.22 | 21.972 | 4.006 | 18.873 | 1.080 | 0.896 |
| weixiaoyuanjia.23 | 21.766 | 3.984 | 18.774 | 1.006 | 0.988 |
| weixiaoyuanjia.24 | 21.975 | 3.982 | 18.718 | 1.003 | 0.986 |
| weixiaoyuanjia.26 | 22.228 | 3.686 | 18.681 | 0.897 | 0.983 |
| weixiaoyuanjia.28 | 14.742 | 1.678 | 21.773 | 0.974 | 1.019 |
| xinyue.4 | 14.371 | 1.619 | 22.028 | 1.062 | 1.015 |
| xinyue.5 | 12.253 | 1.402 | 25.520 | 1.012 | 0.999 |
| xinyue.6 | 14.238 | 1.644 | 22.138 | 1.004 | 1.012 |
| xuanlianjiaomao.3 | 0.681 | 0.258 | 47.081 | 1.011 | 1.006 |
| xuanlianjiaomao.4 | 0.619 | 0.116 | 47.192 | 1.011 | 1.009 |
| xuehong.10 | 7.772 | 2.085 | 29.263 | 0.980 | 0.998 |
| xuehong.11 | 8.558 | 2.386 | 28.309 | 0.975 | 0.991 |
| xuehong.12 | 8.579 | 2.361 | 28.274 | 0.969 | 0.991 |
| xuehong.13 | 8.561 | 2.377 | 28.321 | 0.974 | 0.992 |
| xuehong.14 | 8.601 | 2.364 | 28.258 | 0.970 | 0.991 |
| xuehong.16 | 13.364 | 2.836 | 22.922 | 1.006 | 1.012 |
| xuehong.8 | 6.617 | 1.835 | 30.697 | 0.992 | 0.999 |
| xuehong.9 | 8.563 | 2.366 | 28.301 | 0.973 | 0.992 |
| yuanhai.6 | 15.116 | 1.768 | 21.743 | 0.909 | 1.005 |
| yuanhai.7 | 13.118 | 1.268 | 22.920 | 1.086 | 1.020 |
| yuanhai.8 | 14.815 | 2.058 | 21.842 | 0.976 | 1.000 |
| yuanjiazao.6 | 5.673 | 0.565 | 29.131 | 1.002 | 1.026 |
| yuanjiazao.8 | 8.347 | 0.405 | 27.136 | 0.997 | 1.012 |

Mean metrics:

- mean_abs_bgr_delta: `10.8746`
- mean_abs_luma_delta: `1.7165`
- mean_abs_chroma_delta: `7.4630`
- psnr_vs_raw: `27.7738`
- grad_mean_ratio: `0.9943`
- luma_std_ratio: `1.0002`

## Stage Metrics CSV

- `topology_locked_visual_chroma_full_flow_v1_myedge168_v1_grayplane090_anchorfix_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chazhuang.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chazhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chazhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chichaoyiwan.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chichaoyiwan.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chichaoyiwan.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chichaoyiwan.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chichaoyiwan.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chichaoyiwan.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chichaoyiwan.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\chichaoyiwan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\donghaiyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\duolie.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\duolie.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\duolie.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\duolie.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\duowenqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\duowenqigou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\fanquyuanjia.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\fanquyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\gutiao.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\hailianzao.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\hailianzao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\hailianzao.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\hailianzao.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangkadun.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangyuanjia.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangyuanjia.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\haiyangyuanjia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jianci.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jianci.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jianci.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.27_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\jiaomaozao.29_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\juciqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\kailun.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuang.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuangluojia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuangluojia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuangluojia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuangluojia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuangluojia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuangluojia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lianzhuangluojia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\limayuanjia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lingxinghaixian.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\lingxinghaixian.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\luojiazao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\luojiazao.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\luojiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\luoshijiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\luoshijiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\mashi.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\mishikailun.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\nilingxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\nilingxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\paige.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\paige.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.25_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiangzhuang.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiuxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\qiuxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\redai.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\redai.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\ribenxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\ribenxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\rouruo.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\rouruo.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\sanjiaoji.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\sanjiaoji.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\shikelipu.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\shikelipu.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\suojiao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tama.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tama.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tama.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tama.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tama.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tama.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tama.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tama.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tiaowenhuangou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tiaowenhuangou.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\tiaowenhuangou.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weiruan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weiruan.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.23_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\weixiaoyuanjia.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xinyue.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xinyue.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xinyue.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuanlianjiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuanlianjiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuehong.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuehong.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuehong.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuehong.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuehong.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuehong.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuehong.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\xuehong.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\yuanhai.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\yuanhai.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\yuanhai.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\yuanjiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090_anchorfix\yuanjiazao.8_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
