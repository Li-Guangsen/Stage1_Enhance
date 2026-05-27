# topology_locked_visual_chroma_full_flow_v1 myedge168_v1_grayplane090 status

Date: 2026-05-27

## Summary

- Status: `stage1_output_complete_proxy_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\myedge168_v1.txt`
- Output root: `experiments\topology_locked_visual_chroma_full_flow_v1\outputs\myedge168_v1_grayplane090`
- Expected images: `168`
- Observed runtime: `75.2` sec total, `0.45` sec/image
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
| chazhuang.4 | 15.112 | 2.017 | 23.546 | 1.011 | 1.010 |
| chazhuang.6 | 0.069 | 0.009 | 58.605 | 1.001 | 1.000 |
| chichaoyiwan.1 | 20.314 | 0.919 | 20.603 | 1.047 | 1.013 |
| chichaoyiwan.16 | 19.884 | 0.932 | 20.706 | 1.026 | 0.999 |
| chichaoyiwan.2 | 19.489 | 1.016 | 20.804 | 1.047 | 1.014 |
| chichaoyiwan.3 | 19.716 | 0.915 | 20.750 | 1.014 | 0.995 |
| chichaoyiwan.4 | 19.538 | 0.995 | 20.792 | 1.002 | 1.006 |
| chichaoyiwan.5 | 14.089 | 1.634 | 22.218 | 0.973 | 1.015 |
| chichaoyiwan.6 | 9.404 | 1.181 | 27.709 | 0.954 | 0.987 |
| chichaoyiwan.7 | 9.666 | 1.413 | 27.491 | 0.940 | 0.983 |
| donghaiyuanjia.12 | 14.012 | 2.627 | 22.336 | 0.866 | 1.004 |
| donghaiyuanjia.13 | 14.594 | 2.393 | 21.929 | 1.006 | 1.016 |
| donghaiyuanjia.14 | 14.040 | 2.877 | 22.350 | 0.953 | 0.999 |
| donghaiyuanjia.15 | 13.991 | 2.884 | 22.375 | 0.943 | 0.999 |
| donghaiyuanjia.16 | 39.264 | 21.004 | 15.522 | 0.950 | 0.913 |
| donghaiyuanjia.17 | 38.793 | 20.705 | 15.606 | 0.911 | 0.896 |
| donghaiyuanjia.18 | 41.244 | 25.433 | 15.350 | 0.931 | 0.890 |
| donghaiyuanjia.19 | 39.313 | 17.260 | 15.175 | 0.993 | 0.964 |
| donghaiyuanjia.20 | 17.604 | 2.163 | 20.461 | 1.020 | 1.006 |
| donghaiyuanjia.21 | 17.271 | 3.000 | 20.561 | 1.002 | 0.997 |
| donghaiyuanjia.22 | 17.433 | 2.619 | 20.522 | 0.936 | 0.999 |
| donghaiyuanjia.24 | 21.022 | 1.085 | 19.564 | 1.036 | 1.015 |
| donghaiyuanjia.26 | 38.786 | 20.029 | 15.489 | 0.824 | 0.894 |
| duolie.5 | 12.590 | 1.724 | 25.422 | 1.000 | 0.996 |
| duolie.6 | 12.100 | 1.598 | 25.726 | 0.999 | 0.997 |
| duolie.7 | 11.913 | 1.662 | 25.877 | 0.996 | 0.996 |
| duolie.8 | 11.097 | 1.603 | 26.506 | 0.993 | 0.996 |
| duowenqigou.3 | 2.467 | 0.765 | 38.818 | 0.990 | 1.000 |
| duowenqigou.4 | 2.726 | 0.872 | 37.625 | 0.988 | 0.995 |
| fanquyuanjia.3 | 29.615 | 4.591 | 16.043 | 0.989 | 0.997 |
| fanquyuanjia.4 | 21.540 | 3.752 | 20.491 | 0.859 | 0.940 |
| gutiao.2 | 12.690 | 1.780 | 24.682 | 0.996 | 0.983 |
| hailianzao.10 | 5.814 | 0.576 | 30.680 | 1.012 | 1.030 |
| hailianzao.6 | 0.911 | 0.296 | 44.211 | 1.001 | 0.999 |
| hailianzao.7 | 1.225 | 0.388 | 43.167 | 1.003 | 1.004 |
| hailianzao.8 | 13.714 | 1.594 | 22.667 | 1.008 | 0.999 |
| haiyangkadun.10 | 24.904 | 6.051 | 17.549 | 0.993 | 0.996 |
| haiyangkadun.11 | 25.787 | 7.965 | 17.284 | 0.973 | 0.988 |
| haiyangkadun.12 | 25.107 | 6.186 | 17.742 | 0.968 | 0.999 |
| haiyangkadun.13 | 15.156 | 2.058 | 23.706 | 0.990 | 0.997 |
| haiyangkadun.14 | 15.762 | 2.062 | 23.373 | 0.974 | 0.988 |
| haiyangkadun.15 | 15.278 | 2.261 | 23.775 | 0.980 | 0.990 |
| haiyangkadun.16 | 13.650 | 2.017 | 24.728 | 0.982 | 0.988 |
| haiyangkadun.19 | 3.786 | 1.053 | 35.582 | 0.989 | 1.001 |
| haiyangkadun.20 | 12.775 | 2.262 | 24.605 | 0.998 | 1.014 |
| haiyangkadun.9 | 24.667 | 6.042 | 17.839 | 0.994 | 0.995 |
| haiyangyuanjia.6 | 5.964 | 1.093 | 29.239 | 0.994 | 1.000 |
| haiyangyuanjia.7 | 5.939 | 0.507 | 31.038 | 0.973 | 0.998 |
| haiyangyuanjia.8 | 4.443 | 0.517 | 33.383 | 1.013 | 1.017 |
| jianci.4 | 14.223 | 2.003 | 24.220 | 1.005 | 1.003 |
| jianci.5 | 12.299 | 2.021 | 26.104 | 1.010 | 1.009 |
| jianci.6 | 0.647 | 0.585 | 49.084 | 1.004 | 1.003 |
| jiaomaozao.13 | 0.569 | 0.215 | 47.114 | 1.001 | 1.002 |
| jiaomaozao.14 | 0.640 | 0.170 | 47.258 | 1.001 | 1.001 |
| jiaomaozao.17 | 1.771 | 0.304 | 39.545 | 0.996 | 1.004 |
| jiaomaozao.18 | 0.493 | 0.142 | 49.174 | 1.000 | 1.001 |
| jiaomaozao.19 | 0.947 | 0.284 | 44.617 | 1.000 | 1.000 |
| jiaomaozao.26 | 1.732 | 0.230 | 41.409 | 0.998 | 0.999 |
| jiaomaozao.27 | 0.352 | 0.103 | 50.142 | 1.003 | 1.003 |
| jiaomaozao.28 | 0.735 | 0.190 | 45.188 | 1.001 | 1.005 |
| jiaomaozao.29 | 11.866 | 3.997 | 26.512 | 1.013 | 0.995 |
| juciqigou.3 | 3.900 | 0.285 | 34.010 | 1.002 | 1.003 |
| kailun.2 | 9.604 | 0.343 | 26.657 | 1.006 | 1.004 |
| lianzhuang.4 | 9.544 | 1.379 | 27.596 | 0.996 | 0.992 |
| lianzhuang.5 | 8.445 | 0.955 | 28.446 | 0.998 | 0.999 |
| lianzhuang.6 | 8.716 | 1.016 | 28.168 | 0.996 | 0.996 |
| lianzhuangluojia.10 | 3.113 | 0.475 | 35.358 | 0.958 | 1.006 |
| lianzhuangluojia.11 | 7.928 | 0.841 | 29.290 | 0.986 | 1.004 |
| lianzhuangluojia.12 | 11.026 | 2.693 | 26.510 | 0.997 | 0.991 |
| lianzhuangluojia.13 | 4.529 | 1.165 | 34.432 | 0.984 | 0.997 |
| lianzhuangluojia.14 | 4.394 | 1.116 | 34.628 | 0.986 | 0.998 |
| lianzhuangluojia.8 | 19.490 | 1.063 | 20.766 | 0.998 | 1.031 |
| lianzhuangluojia.9 | 3.005 | 0.506 | 35.582 | 0.999 | 1.014 |
| limayuanjia.10 | 29.535 | 6.663 | 15.243 | 0.979 | 1.038 |
| limayuanjia.11 | 23.692 | 6.169 | 17.340 | 0.949 | 0.987 |
| limayuanjia.12 | 26.765 | 7.308 | 17.440 | 0.933 | 0.915 |
| limayuanjia.13 | 27.262 | 9.875 | 16.179 | 0.955 | 0.981 |
| limayuanjia.14 | 10.045 | 1.365 | 27.141 | 0.985 | 0.995 |
| limayuanjia.15 | 10.995 | 1.347 | 26.297 | 0.998 | 0.993 |
| limayuanjia.16 | 20.952 | 3.737 | 21.070 | 0.999 | 0.955 |
| limayuanjia.18 | 12.413 | 1.905 | 25.316 | 0.994 | 0.994 |
| limayuanjia.9 | 28.202 | 5.469 | 15.571 | 0.979 | 1.042 |
| lingxinghaixian.5 | 13.681 | 2.015 | 25.279 | 1.009 | 1.008 |
| lingxinghaixian.6 | 13.597 | 1.925 | 23.762 | 1.011 | 1.018 |
| luojiazao.4 | 3.115 | 0.448 | 35.396 | 1.004 | 1.019 |
| luojiazao.5 | 3.197 | 0.639 | 35.041 | 1.020 | 1.011 |
| luojiazao.6 | 4.992 | 0.684 | 31.393 | 0.999 | 1.013 |
| luoshijiaomao.3 | 6.214 | 1.303 | 30.860 | 0.994 | 1.000 |
| luoshijiaomao.4 | 5.403 | 1.046 | 30.687 | 0.993 | 0.997 |
| mashi.2 | 9.438 | 0.259 | 26.497 | 0.999 | 1.004 |
| mishikailun.8 | 3.518 | 0.331 | 33.526 | 1.000 | 1.007 |
| nilingxing.3 | 2.915 | 0.271 | 37.815 | 1.001 | 1.001 |
| nilingxing.4 | 4.183 | 0.490 | 34.701 | 1.003 | 0.996 |
| paige.4 | 0.420 | 0.136 | 49.391 | 1.001 | 1.000 |
| paige.5 | 13.042 | 2.032 | 25.603 | 1.043 | 1.026 |
| qiangzhuang.12 | 34.165 | 9.466 | 15.420 | 1.005 | 1.002 |
| qiangzhuang.13 | 34.421 | 10.241 | 15.400 | 1.098 | 1.001 |
| qiangzhuang.14 | 33.382 | 8.774 | 15.443 | 1.059 | 1.002 |
| qiangzhuang.15 | 32.769 | 8.174 | 15.547 | 1.061 | 1.004 |
| qiangzhuang.16 | 34.840 | 11.835 | 15.434 | 1.050 | 0.985 |
| qiangzhuang.17 | 27.032 | 2.105 | 18.125 | 1.008 | 1.034 |
| qiangzhuang.18 | 13.576 | 2.062 | 22.294 | 0.986 | 1.007 |
| qiangzhuang.19 | 13.535 | 2.090 | 22.303 | 1.004 | 1.009 |
| qiangzhuang.20 | 13.502 | 2.035 | 22.308 | 0.997 | 1.010 |
| qiangzhuang.21 | 13.528 | 2.113 | 22.333 | 1.006 | 1.007 |
| qiangzhuang.22 | 13.523 | 2.083 | 22.332 | 1.014 | 1.007 |
| qiangzhuang.25 | 13.557 | 2.084 | 22.322 | 0.999 | 1.006 |
| qiangzhuang.26 | 13.566 | 2.090 | 22.324 | 1.000 | 1.009 |
| qiangzhuang.28 | 13.545 | 2.124 | 22.332 | 1.003 | 1.005 |
| qiuxing.3 | 2.860 | 1.017 | 37.169 | 0.977 | 0.995 |
| qiuxing.4 | 12.753 | 1.249 | 24.966 | 1.037 | 1.001 |
| redai.3 | 9.495 | 2.075 | 27.910 | 0.998 | 0.987 |
| redai.4 | 11.316 | 2.811 | 26.213 | 1.004 | 0.990 |
| ribenxing.3 | 3.824 | 0.538 | 33.505 | 0.999 | 1.000 |
| ribenxing.4 | 10.123 | 1.333 | 27.201 | 0.972 | 0.990 |
| rouruo.3 | 0.586 | 0.258 | 48.538 | 0.984 | 0.999 |
| rouruo.4 | 9.023 | 1.191 | 27.958 | 0.991 | 0.989 |
| sanjiaoji.10 | 8.986 | 0.201 | 27.248 | 1.002 | 1.001 |
| sanjiaoji.9 | 8.863 | 0.189 | 27.371 | 0.997 | 0.999 |
| shikelipu.4 | 8.849 | 1.667 | 28.412 | 1.015 | 0.974 |
| shikelipu.5 | 11.102 | 2.664 | 26.402 | 1.006 | 0.990 |
| suojiao.6 | 12.760 | 1.921 | 23.571 | 0.991 | 1.003 |
| tama.10 | 37.201 | 13.420 | 15.225 | 1.004 | 0.957 |
| tama.11 | 7.478 | 0.334 | 28.785 | 0.930 | 0.986 |
| tama.12 | 38.815 | 17.853 | 15.252 | 0.965 | 0.921 |
| tama.13 | 4.417 | 0.265 | 32.922 | 1.038 | 1.005 |
| tama.14 | 7.466 | 0.316 | 28.796 | 0.931 | 0.987 |
| tama.16 | 0.409 | 0.147 | 51.223 | 1.021 | 1.004 |
| tama.8 | 37.722 | 14.920 | 15.233 | 0.907 | 0.943 |
| tama.9 | 7.464 | 0.339 | 28.800 | 0.928 | 0.985 |
| tiaowenhuangou.4 | 20.325 | 4.285 | 21.294 | 1.006 | 0.956 |
| tiaowenhuangou.5 | 20.241 | 4.256 | 21.336 | 1.005 | 0.956 |
| tiaowenhuangou.6 | 7.357 | 1.016 | 29.779 | 0.998 | 0.998 |
| weiruan.7 | 11.882 | 1.614 | 25.853 | 0.991 | 0.991 |
| weiruan.8 | 13.195 | 1.760 | 24.961 | 0.998 | 0.992 |
| weixiaoyuanjia.13 | 13.550 | 2.174 | 22.440 | 0.961 | 1.001 |
| weixiaoyuanjia.14 | 13.868 | 1.829 | 22.299 | 0.957 | 1.008 |
| weixiaoyuanjia.15 | 13.615 | 2.000 | 22.367 | 0.938 | 1.004 |
| weixiaoyuanjia.16 | 13.953 | 1.828 | 22.264 | 0.986 | 1.012 |
| weixiaoyuanjia.17 | 13.927 | 1.844 | 22.260 | 0.962 | 1.013 |
| weixiaoyuanjia.18 | 13.917 | 1.856 | 22.288 | 0.978 | 1.010 |
| weixiaoyuanjia.19 | 14.011 | 1.608 | 22.208 | 0.970 | 1.008 |
| weixiaoyuanjia.20 | 13.713 | 1.983 | 22.361 | 0.947 | 1.009 |
| weixiaoyuanjia.21 | 39.417 | 21.209 | 15.350 | 0.897 | 0.829 |
| weixiaoyuanjia.22 | 40.472 | 22.402 | 15.196 | 0.983 | 0.858 |
| weixiaoyuanjia.23 | 40.161 | 21.758 | 15.251 | 1.042 | 0.927 |
| weixiaoyuanjia.24 | 39.017 | 19.167 | 15.355 | 0.898 | 0.926 |
| weixiaoyuanjia.26 | 38.993 | 18.638 | 15.307 | 0.972 | 0.924 |
| weixiaoyuanjia.28 | 13.934 | 1.819 | 22.267 | 0.975 | 1.010 |
| xinyue.4 | 13.875 | 1.617 | 22.343 | 0.989 | 1.003 |
| xinyue.5 | 11.997 | 1.405 | 25.706 | 1.009 | 0.998 |
| xinyue.6 | 13.776 | 1.688 | 22.455 | 0.926 | 0.989 |
| xuanlianjiaomao.3 | 0.636 | 0.252 | 48.909 | 1.010 | 1.004 |
| xuanlianjiaomao.4 | 0.580 | 0.110 | 49.231 | 1.010 | 1.005 |
| xuehong.10 | 7.677 | 2.087 | 29.358 | 0.983 | 0.993 |
| xuehong.11 | 8.409 | 2.389 | 28.439 | 0.979 | 0.989 |
| xuehong.12 | 8.428 | 2.357 | 28.410 | 0.972 | 0.988 |
| xuehong.13 | 8.410 | 2.374 | 28.453 | 0.978 | 0.989 |
| xuehong.14 | 8.454 | 2.357 | 28.390 | 0.973 | 0.988 |
| xuehong.16 | 19.008 | 4.306 | 19.329 | 0.959 | 0.938 |
| xuehong.8 | 6.324 | 1.799 | 31.118 | 0.993 | 0.995 |
| xuehong.9 | 8.411 | 2.365 | 28.433 | 0.977 | 0.989 |
| yuanhai.6 | 14.402 | 1.578 | 22.156 | 0.992 | 1.010 |
| yuanhai.7 | 16.252 | 1.949 | 21.163 | 1.010 | 1.011 |
| yuanhai.8 | 14.260 | 1.995 | 22.196 | 0.992 | 0.998 |
| yuanjiazao.6 | 5.335 | 0.486 | 30.440 | 1.001 | 1.022 |
| yuanjiazao.8 | 8.242 | 0.346 | 27.293 | 0.999 | 1.009 |

Mean metrics:

- mean_abs_bgr_delta: `13.9662`
- mean_abs_luma_delta: `3.3951`
- mean_abs_chroma_delta: `9.6317`
- psnr_vs_raw: `26.9028`
- grad_mean_ratio: `0.9882`
- luma_std_ratio: `0.9924`

## Stage Metrics CSV

- `topology_locked_visual_chroma_full_flow_v1_myedge168_v1_grayplane090_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chazhuang.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chazhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chazhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chichaoyiwan.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chichaoyiwan.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chichaoyiwan.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chichaoyiwan.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chichaoyiwan.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chichaoyiwan.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chichaoyiwan.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\chichaoyiwan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\donghaiyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\duolie.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\duolie.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\duolie.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\duolie.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\duowenqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\duowenqigou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\fanquyuanjia.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\fanquyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\gutiao.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\hailianzao.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\hailianzao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\hailianzao.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\hailianzao.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangkadun.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangyuanjia.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangyuanjia.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\haiyangyuanjia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jianci.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jianci.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jianci.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.27_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\jiaomaozao.29_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\juciqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\kailun.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuang.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuangluojia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuangluojia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuangluojia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuangluojia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuangluojia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuangluojia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lianzhuangluojia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\limayuanjia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lingxinghaixian.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\lingxinghaixian.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\luojiazao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\luojiazao.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\luojiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\luoshijiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\luoshijiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\mashi.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\mishikailun.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\nilingxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\nilingxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\paige.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\paige.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.25_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiangzhuang.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiuxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\qiuxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\redai.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\redai.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\ribenxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\ribenxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\rouruo.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\rouruo.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\sanjiaoji.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\sanjiaoji.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\shikelipu.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\shikelipu.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\suojiao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tama.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tama.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tama.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tama.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tama.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tama.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tama.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tama.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tiaowenhuangou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tiaowenhuangou.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\tiaowenhuangou.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weiruan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weiruan.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.23_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\weixiaoyuanjia.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xinyue.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xinyue.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xinyue.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuanlianjiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuanlianjiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuehong.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuehong.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuehong.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuehong.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuehong.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuehong.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuehong.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\xuehong.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\yuanhai.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\yuanhai.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\yuanhai.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\yuanjiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_grayplane090\yuanjiazao.8_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
