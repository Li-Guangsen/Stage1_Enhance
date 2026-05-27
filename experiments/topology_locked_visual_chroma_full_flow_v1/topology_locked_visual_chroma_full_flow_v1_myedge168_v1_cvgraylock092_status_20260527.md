# topology_locked_visual_chroma_full_flow_v1 myedge168_v1_cvgraylock092 status

Date: 2026-05-27

## Summary

- Status: `stage1_output_complete_proxy_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\myedge168_v1.txt`
- Output root: `experiments\topology_locked_visual_chroma_full_flow_v1\outputs\myedge168_v1_cvgraylock092`
- Expected images: `168`
- Observed runtime: `74.2` sec total, `0.44` sec/image
- Projected 168 runtime: `1.2` min
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
| chazhuang.4 | 15.058 | 2.340 | 23.623 | 1.053 | 1.027 |
| chazhuang.6 | 0.069 | 0.009 | 58.605 | 1.001 | 1.000 |
| chichaoyiwan.1 | 18.965 | 0.950 | 21.269 | 1.033 | 1.009 |
| chichaoyiwan.16 | 18.513 | 1.016 | 21.388 | 1.024 | 1.004 |
| chichaoyiwan.2 | 18.148 | 1.023 | 21.492 | 1.042 | 1.013 |
| chichaoyiwan.3 | 18.351 | 1.003 | 21.433 | 1.012 | 1.003 |
| chichaoyiwan.4 | 18.199 | 0.997 | 21.478 | 1.003 | 1.002 |
| chichaoyiwan.5 | 13.321 | 1.953 | 22.744 | 0.960 | 1.002 |
| chichaoyiwan.6 | 9.270 | 1.272 | 27.819 | 0.957 | 0.989 |
| chichaoyiwan.7 | 9.614 | 1.386 | 27.531 | 0.980 | 0.988 |
| donghaiyuanjia.12 | 13.342 | 2.965 | 22.860 | 0.951 | 0.999 |
| donghaiyuanjia.13 | 13.291 | 2.993 | 22.947 | 0.987 | 0.998 |
| donghaiyuanjia.14 | 13.372 | 2.978 | 22.875 | 0.992 | 0.995 |
| donghaiyuanjia.15 | 13.326 | 2.960 | 22.904 | 0.975 | 0.997 |
| donghaiyuanjia.16 | 38.228 | 20.917 | 15.776 | 0.942 | 0.905 |
| donghaiyuanjia.17 | 37.794 | 20.328 | 15.853 | 0.923 | 0.905 |
| donghaiyuanjia.18 | 40.190 | 24.977 | 15.609 | 0.911 | 0.888 |
| donghaiyuanjia.19 | 38.551 | 17.120 | 15.364 | 0.975 | 0.959 |
| donghaiyuanjia.20 | 14.947 | 1.919 | 21.830 | 0.944 | 1.004 |
| donghaiyuanjia.21 | 14.613 | 2.084 | 21.954 | 1.020 | 1.004 |
| donghaiyuanjia.22 | 14.772 | 2.006 | 21.910 | 0.959 | 1.001 |
| donghaiyuanjia.24 | 19.490 | 0.393 | 20.614 | 0.978 | 1.019 |
| donghaiyuanjia.26 | 37.856 | 19.999 | 15.712 | 0.840 | 0.899 |
| duolie.5 | 12.458 | 1.801 | 25.526 | 0.991 | 0.989 |
| duolie.6 | 11.950 | 1.655 | 25.836 | 0.993 | 0.991 |
| duolie.7 | 11.777 | 1.692 | 25.983 | 0.993 | 0.991 |
| duolie.8 | 10.950 | 1.627 | 26.628 | 0.988 | 0.990 |
| duowenqigou.3 | 2.358 | 0.749 | 39.822 | 0.990 | 0.996 |
| duowenqigou.4 | 2.580 | 0.851 | 38.132 | 0.992 | 0.994 |
| fanquyuanjia.3 | 14.384 | 2.867 | 22.053 | 1.003 | 1.005 |
| fanquyuanjia.4 | 20.957 | 3.716 | 20.758 | 0.856 | 0.939 |
| gutiao.2 | 12.065 | 1.721 | 25.174 | 0.996 | 0.983 |
| hailianzao.10 | 5.519 | 0.503 | 31.746 | 1.009 | 1.024 |
| hailianzao.6 | 0.565 | 0.208 | 48.981 | 1.000 | 1.001 |
| hailianzao.7 | 0.960 | 0.354 | 46.087 | 1.001 | 1.001 |
| hailianzao.8 | 12.586 | 1.503 | 23.404 | 1.007 | 1.000 |
| haiyangkadun.10 | 24.726 | 6.036 | 17.673 | 0.993 | 0.994 |
| haiyangkadun.11 | 25.418 | 7.681 | 17.440 | 0.963 | 0.989 |
| haiyangkadun.12 | 24.856 | 6.085 | 17.884 | 0.974 | 0.997 |
| haiyangkadun.13 | 14.096 | 2.009 | 24.324 | 0.996 | 0.998 |
| haiyangkadun.14 | 15.356 | 2.128 | 23.598 | 0.988 | 0.989 |
| haiyangkadun.15 | 15.018 | 2.202 | 23.912 | 0.974 | 0.986 |
| haiyangkadun.16 | 13.470 | 2.057 | 24.840 | 0.978 | 0.983 |
| haiyangkadun.19 | 3.662 | 1.147 | 35.980 | 0.992 | 0.992 |
| haiyangkadun.20 | 12.006 | 2.057 | 25.388 | 0.988 | 1.010 |
| haiyangkadun.9 | 24.354 | 6.030 | 17.989 | 0.994 | 0.993 |
| haiyangyuanjia.6 | 5.780 | 1.109 | 29.717 | 0.991 | 0.998 |
| haiyangyuanjia.7 | 5.762 | 0.490 | 31.426 | 0.969 | 0.994 |
| haiyangyuanjia.8 | 4.353 | 0.538 | 33.639 | 1.002 | 1.013 |
| jianci.4 | 13.793 | 1.905 | 24.551 | 1.036 | 1.001 |
| jianci.5 | 12.037 | 2.003 | 26.323 | 1.015 | 1.014 |
| jianci.6 | 0.639 | 0.586 | 49.296 | 1.004 | 1.003 |
| jiaomaozao.13 | 0.358 | 0.160 | 51.705 | 1.000 | 1.000 |
| jiaomaozao.14 | 0.510 | 0.158 | 49.961 | 1.000 | 1.000 |
| jiaomaozao.17 | 1.320 | 0.287 | 43.164 | 0.998 | 1.004 |
| jiaomaozao.18 | 0.405 | 0.139 | 51.227 | 0.999 | 0.999 |
| jiaomaozao.19 | 0.716 | 0.330 | 47.854 | 1.001 | 1.000 |
| jiaomaozao.26 | 1.670 | 0.228 | 42.098 | 0.998 | 1.000 |
| jiaomaozao.27 | 0.281 | 0.075 | 53.085 | 0.999 | 1.000 |
| jiaomaozao.28 | 0.572 | 0.166 | 49.054 | 0.999 | 1.002 |
| jiaomaozao.29 | 11.827 | 4.024 | 26.540 | 1.002 | 0.995 |
| juciqigou.3 | 3.742 | 0.311 | 34.624 | 1.002 | 1.002 |
| kailun.2 | 9.487 | 0.302 | 26.769 | 0.998 | 0.999 |
| lianzhuang.4 | 9.498 | 1.416 | 27.664 | 1.002 | 0.988 |
| lianzhuang.5 | 8.363 | 0.992 | 28.545 | 1.003 | 0.995 |
| lianzhuang.6 | 8.636 | 1.059 | 28.271 | 0.997 | 0.992 |
| lianzhuangluojia.10 | 3.023 | 0.264 | 35.400 | 0.911 | 0.995 |
| lianzhuangluojia.11 | 7.841 | 1.014 | 29.439 | 0.992 | 0.996 |
| lianzhuangluojia.12 | 10.839 | 2.662 | 26.644 | 1.003 | 0.990 |
| lianzhuangluojia.13 | 4.455 | 1.135 | 34.814 | 0.994 | 0.994 |
| lianzhuangluojia.14 | 4.305 | 1.122 | 35.068 | 0.998 | 0.995 |
| lianzhuangluojia.8 | 18.054 | 1.072 | 21.502 | 1.009 | 1.024 |
| lianzhuangluojia.9 | 2.830 | 0.071 | 35.656 | 0.992 | 0.997 |
| limayuanjia.10 | 29.125 | 6.614 | 15.344 | 0.980 | 1.036 |
| limayuanjia.11 | 23.300 | 5.801 | 17.499 | 0.950 | 0.990 |
| limayuanjia.12 | 26.436 | 6.944 | 17.601 | 0.946 | 0.919 |
| limayuanjia.13 | 26.913 | 9.828 | 16.277 | 0.954 | 0.979 |
| limayuanjia.14 | 9.843 | 1.414 | 27.328 | 0.982 | 0.987 |
| limayuanjia.15 | 10.899 | 1.321 | 26.370 | 0.994 | 0.989 |
| limayuanjia.16 | 20.816 | 3.685 | 21.126 | 1.001 | 0.955 |
| limayuanjia.18 | 12.016 | 1.853 | 25.607 | 0.991 | 0.989 |
| limayuanjia.9 | 27.749 | 5.439 | 15.680 | 0.977 | 1.038 |
| lingxinghaixian.5 | 13.122 | 2.010 | 25.647 | 1.013 | 1.013 |
| lingxinghaixian.6 | 12.947 | 1.902 | 24.334 | 1.013 | 1.021 |
| luojiazao.4 | 2.517 | 0.430 | 37.766 | 0.999 | 1.012 |
| luojiazao.5 | 2.910 | 0.702 | 36.470 | 1.011 | 1.003 |
| luojiazao.6 | 3.067 | 0.418 | 35.499 | 1.004 | 1.010 |
| luoshijiaomao.3 | 6.088 | 1.365 | 30.934 | 0.990 | 0.993 |
| luoshijiaomao.4 | 5.321 | 1.090 | 30.721 | 0.974 | 0.988 |
| mashi.2 | 9.288 | 0.331 | 26.599 | 0.997 | 1.000 |
| mishikailun.8 | 3.300 | 0.465 | 35.058 | 1.010 | 1.003 |
| nilingxing.3 | 2.934 | 0.215 | 37.736 | 1.003 | 1.006 |
| nilingxing.4 | 4.012 | 0.465 | 34.997 | 1.006 | 0.998 |
| paige.4 | 0.390 | 0.124 | 50.484 | 1.000 | 0.999 |
| paige.5 | 12.519 | 1.977 | 25.968 | 1.020 | 1.023 |
| qiangzhuang.12 | 33.597 | 9.479 | 15.569 | 1.020 | 1.002 |
| qiangzhuang.13 | 33.665 | 10.237 | 15.608 | 1.099 | 1.000 |
| qiangzhuang.14 | 32.663 | 8.736 | 15.640 | 1.089 | 1.002 |
| qiangzhuang.15 | 31.970 | 8.173 | 15.767 | 1.065 | 1.002 |
| qiangzhuang.16 | 34.171 | 11.657 | 15.625 | 1.003 | 0.980 |
| qiangzhuang.17 | 23.883 | 1.874 | 19.390 | 0.891 | 1.023 |
| qiangzhuang.18 | 12.707 | 2.041 | 22.841 | 0.992 | 1.000 |
| qiangzhuang.19 | 12.678 | 2.119 | 22.856 | 1.005 | 1.002 |
| qiangzhuang.20 | 12.673 | 2.205 | 22.894 | 0.983 | 1.004 |
| qiangzhuang.21 | 12.707 | 2.099 | 22.885 | 0.976 | 1.000 |
| qiangzhuang.22 | 12.710 | 2.096 | 22.883 | 0.982 | 1.000 |
| qiangzhuang.25 | 12.722 | 2.107 | 22.878 | 0.978 | 0.999 |
| qiangzhuang.26 | 12.728 | 2.066 | 22.875 | 0.979 | 1.002 |
| qiangzhuang.28 | 12.716 | 2.140 | 22.878 | 0.995 | 0.999 |
| qiuxing.3 | 2.733 | 0.784 | 37.443 | 0.986 | 1.006 |
| qiuxing.4 | 12.539 | 1.294 | 25.125 | 1.027 | 0.995 |
| redai.3 | 9.351 | 2.129 | 28.039 | 0.991 | 0.983 |
| redai.4 | 11.047 | 2.781 | 26.424 | 1.006 | 0.990 |
| ribenxing.3 | 3.775 | 0.407 | 33.457 | 0.990 | 1.000 |
| ribenxing.4 | 10.024 | 1.313 | 27.283 | 0.978 | 0.989 |
| rouruo.3 | 0.560 | 0.257 | 49.261 | 0.982 | 0.997 |
| rouruo.4 | 8.902 | 1.239 | 28.067 | 0.994 | 0.990 |
| sanjiaoji.10 | 9.010 | 0.217 | 27.256 | 0.994 | 0.998 |
| sanjiaoji.9 | 8.886 | 0.219 | 27.388 | 0.993 | 0.997 |
| shikelipu.4 | 8.826 | 1.669 | 28.444 | 1.014 | 0.973 |
| shikelipu.5 | 10.826 | 2.620 | 26.598 | 1.004 | 0.990 |
| suojiao.6 | 12.500 | 1.688 | 23.940 | 0.957 | 0.984 |
| tama.10 | 36.245 | 12.905 | 15.433 | 0.983 | 0.962 |
| tama.11 | 7.536 | 0.195 | 28.782 | 0.982 | 0.982 |
| tama.12 | 37.821 | 17.325 | 15.469 | 0.973 | 0.931 |
| tama.13 | 4.425 | 0.351 | 32.986 | 1.033 | 0.999 |
| tama.14 | 7.522 | 0.192 | 28.793 | 0.991 | 0.983 |
| tama.16 | 0.310 | 0.144 | 52.828 | 1.021 | 1.002 |
| tama.8 | 36.791 | 14.552 | 15.448 | 0.926 | 0.948 |
| tama.9 | 7.520 | 0.202 | 28.797 | 0.977 | 0.982 |
| tiaowenhuangou.4 | 20.222 | 4.245 | 21.335 | 1.006 | 0.955 |
| tiaowenhuangou.5 | 20.145 | 4.222 | 21.375 | 1.004 | 0.955 |
| tiaowenhuangou.6 | 7.126 | 1.075 | 30.037 | 1.003 | 0.992 |
| weiruan.7 | 11.776 | 1.662 | 25.950 | 0.990 | 0.988 |
| weiruan.8 | 13.063 | 1.820 | 25.060 | 0.994 | 0.989 |
| weixiaoyuanjia.13 | 12.778 | 2.398 | 23.019 | 0.945 | 0.989 |
| weixiaoyuanjia.14 | 13.064 | 1.983 | 22.862 | 0.980 | 1.001 |
| weixiaoyuanjia.15 | 12.857 | 2.197 | 22.935 | 0.925 | 0.995 |
| weixiaoyuanjia.16 | 13.169 | 2.022 | 22.822 | 0.978 | 1.003 |
| weixiaoyuanjia.17 | 13.119 | 2.044 | 22.830 | 0.969 | 1.002 |
| weixiaoyuanjia.18 | 13.116 | 1.995 | 22.846 | 0.986 | 1.002 |
| weixiaoyuanjia.19 | 13.263 | 1.915 | 22.736 | 0.979 | 0.997 |
| weixiaoyuanjia.20 | 12.913 | 2.301 | 22.930 | 0.948 | 0.997 |
| weixiaoyuanjia.21 | 38.373 | 20.630 | 15.572 | 0.889 | 0.896 |
| weixiaoyuanjia.22 | 39.727 | 22.526 | 15.373 | 1.015 | 0.913 |
| weixiaoyuanjia.23 | 38.959 | 20.972 | 15.499 | 0.966 | 0.925 |
| weixiaoyuanjia.24 | 38.196 | 19.160 | 15.565 | 0.896 | 0.924 |
| weixiaoyuanjia.26 | 37.857 | 18.293 | 15.548 | 0.920 | 0.920 |
| weixiaoyuanjia.28 | 13.108 | 2.090 | 22.849 | 0.963 | 0.996 |
| xinyue.4 | 13.191 | 2.078 | 22.859 | 0.942 | 0.986 |
| xinyue.5 | 11.709 | 1.448 | 25.896 | 1.003 | 0.998 |
| xinyue.6 | 13.085 | 1.656 | 22.909 | 0.908 | 0.990 |
| xuanlianjiaomao.3 | 0.562 | 0.236 | 50.179 | 1.009 | 1.001 |
| xuanlianjiaomao.4 | 0.490 | 0.106 | 50.881 | 1.010 | 1.003 |
| xuehong.10 | 7.511 | 2.060 | 29.479 | 0.975 | 0.988 |
| xuehong.11 | 8.230 | 2.388 | 28.582 | 0.979 | 0.985 |
| xuehong.12 | 8.241 | 2.362 | 28.554 | 0.977 | 0.984 |
| xuehong.13 | 8.228 | 2.387 | 28.598 | 0.980 | 0.985 |
| xuehong.14 | 8.268 | 2.363 | 28.535 | 0.979 | 0.985 |
| xuehong.16 | 18.626 | 4.266 | 19.509 | 0.959 | 0.938 |
| xuehong.8 | 5.885 | 1.700 | 31.568 | 0.990 | 0.991 |
| xuehong.9 | 8.223 | 2.367 | 28.579 | 0.976 | 0.985 |
| yuanhai.6 | 13.591 | 1.984 | 22.713 | 0.985 | 0.992 |
| yuanhai.7 | 13.680 | 1.972 | 22.661 | 0.991 | 0.988 |
| yuanhai.8 | 13.452 | 2.033 | 22.770 | 0.973 | 0.991 |
| yuanjiazao.6 | 5.149 | 0.390 | 31.723 | 1.000 | 1.016 |
| yuanjiazao.8 | 8.212 | 0.381 | 27.377 | 1.006 | 1.006 |

Mean metrics:

- mean_abs_bgr_delta: `13.3684`
- mean_abs_luma_delta: `3.3544`
- mean_abs_chroma_delta: `9.2322`
- psnr_vs_raw: `27.5202`
- grad_mean_ratio: `0.9864`
- luma_std_ratio: `0.9901`

## Stage Metrics CSV

- `topology_locked_visual_chroma_full_flow_v1_myedge168_v1_cvgraylock092_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chazhuang.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chazhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chazhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chichaoyiwan.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chichaoyiwan.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chichaoyiwan.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chichaoyiwan.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chichaoyiwan.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chichaoyiwan.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chichaoyiwan.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\chichaoyiwan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\donghaiyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\duolie.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\duolie.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\duolie.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\duolie.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\duowenqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\duowenqigou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\fanquyuanjia.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\fanquyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\gutiao.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\hailianzao.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\hailianzao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\hailianzao.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\hailianzao.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangkadun.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangyuanjia.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangyuanjia.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\haiyangyuanjia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jianci.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jianci.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jianci.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.27_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\jiaomaozao.29_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\juciqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\kailun.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuang.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuangluojia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuangluojia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuangluojia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuangluojia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuangluojia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuangluojia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lianzhuangluojia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\limayuanjia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lingxinghaixian.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\lingxinghaixian.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\luojiazao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\luojiazao.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\luojiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\luoshijiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\luoshijiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\mashi.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\mishikailun.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\nilingxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\nilingxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\paige.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\paige.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.25_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiangzhuang.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiuxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\qiuxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\redai.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\redai.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\ribenxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\ribenxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\rouruo.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\rouruo.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\sanjiaoji.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\sanjiaoji.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\shikelipu.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\shikelipu.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\suojiao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tama.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tama.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tama.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tama.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tama.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tama.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tama.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tama.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tiaowenhuangou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tiaowenhuangou.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\tiaowenhuangou.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weiruan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weiruan.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.23_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\weixiaoyuanjia.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xinyue.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xinyue.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xinyue.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuanlianjiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuanlianjiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuehong.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuehong.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuehong.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuehong.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuehong.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuehong.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuehong.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\xuehong.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\yuanhai.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\yuanhai.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\yuanhai.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\yuanjiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_cvgraylock092\yuanjiazao.8_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
