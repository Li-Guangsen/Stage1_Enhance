# full_flow_downstream_stage1_mainline_v2 ff02_myedge168_v1 status

Date: 2026-05-27

## Summary

- Status: `complete_168_stage1_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\myedge168_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v2\outputs\myedge168\full_flow_downstream_stage1_mainline_v2`
- Expected images: `168`
- Observed runtime: `77.5` sec total, `0.46` sec/image
- Projected 168 runtime: `1.3` min
- Decision: `fixed_detector_preflight_pending`

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
| chazhuang.3 | 0.972 | 0.632 | 43.997 | 0.935 | 1.004 |
| chazhuang.4 | 14.976 | 0.112 | 23.508 | 0.953 | 1.003 |
| chazhuang.6 | 1.148 | 0.742 | 43.820 | 0.880 | 1.002 |
| chichaoyiwan.1 | 19.775 | 0.904 | 20.640 | 0.849 | 1.090 |
| chichaoyiwan.16 | 19.665 | 1.014 | 20.665 | 0.909 | 1.057 |
| chichaoyiwan.2 | 19.389 | 0.981 | 20.747 | 0.846 | 1.109 |
| chichaoyiwan.3 | 19.524 | 0.968 | 20.718 | 0.850 | 1.104 |
| chichaoyiwan.4 | 19.358 | 0.885 | 20.759 | 0.787 | 1.094 |
| chichaoyiwan.5 | 14.333 | 1.127 | 22.109 | 1.055 | 1.013 |
| chichaoyiwan.6 | 8.292 | 1.079 | 28.830 | 1.057 | 1.031 |
| chichaoyiwan.7 | 8.493 | 1.082 | 28.623 | 1.072 | 1.031 |
| donghaiyuanjia.12 | 14.175 | 1.074 | 21.555 | 1.093 | 1.050 |
| donghaiyuanjia.13 | 13.969 | 0.817 | 21.673 | 1.084 | 1.034 |
| donghaiyuanjia.14 | 14.090 | 1.011 | 21.640 | 1.065 | 1.029 |
| donghaiyuanjia.15 | 14.130 | 1.034 | 21.594 | 1.067 | 1.030 |
| donghaiyuanjia.16 | 30.003 | 6.348 | 16.209 | 1.049 | 1.055 |
| donghaiyuanjia.17 | 28.648 | 2.567 | 16.267 | 0.969 | 1.062 |
| donghaiyuanjia.18 | 27.766 | 3.240 | 16.089 | 1.077 | 1.094 |
| donghaiyuanjia.19 | 14.909 | 2.168 | 21.121 | 0.953 | 1.067 |
| donghaiyuanjia.20 | 16.364 | 1.195 | 20.727 | 0.952 | 1.007 |
| donghaiyuanjia.21 | 16.016 | 1.183 | 20.820 | 0.958 | 1.008 |
| donghaiyuanjia.22 | 16.158 | 1.210 | 20.768 | 0.947 | 1.023 |
| donghaiyuanjia.24 | 20.262 | 1.170 | 20.023 | 0.942 | 1.006 |
| donghaiyuanjia.26 | 29.264 | 2.581 | 16.586 | 0.869 | 1.071 |
| duolie.5 | 10.507 | 1.107 | 26.854 | 0.838 | 0.974 |
| duolie.6 | 10.191 | 1.078 | 27.093 | 0.831 | 0.960 |
| duolie.7 | 9.879 | 1.127 | 27.382 | 0.836 | 0.961 |
| duolie.8 | 9.446 | 1.111 | 27.780 | 0.837 | 0.961 |
| duowenqigou.3 | 2.295 | 1.312 | 39.272 | 0.846 | 0.961 |
| duowenqigou.4 | 2.665 | 1.329 | 37.947 | 0.845 | 0.945 |
| fanquyuanjia.3 | 15.744 | 1.404 | 20.733 | 0.890 | 0.990 |
| fanquyuanjia.4 | 16.860 | 1.294 | 22.284 | 0.882 | 0.986 |
| gutiao.2 | 10.946 | 1.145 | 25.975 | 0.923 | 1.001 |
| hailianzao.10 | 4.995 | 1.168 | 32.474 | 0.877 | 0.985 |
| hailianzao.6 | 1.393 | 1.153 | 42.616 | 0.884 | 0.967 |
| hailianzao.7 | 1.517 | 0.937 | 42.279 | 0.907 | 0.990 |
| hailianzao.8 | 12.832 | 1.252 | 23.120 | 0.881 | 0.977 |
| haiyangkadun.10 | 19.338 | 1.260 | 20.695 | 0.962 | 1.016 |
| haiyangkadun.11 | 19.539 | 1.289 | 20.662 | 0.966 | 1.025 |
| haiyangkadun.12 | 19.613 | 1.250 | 20.633 | 0.976 | 1.032 |
| haiyangkadun.13 | 16.373 | 1.061 | 22.814 | 1.139 | 1.020 |
| haiyangkadun.14 | 13.283 | 1.058 | 24.684 | 1.189 | 1.025 |
| haiyangkadun.15 | 12.693 | 1.021 | 25.179 | 1.077 | 1.013 |
| haiyangkadun.16 | 11.206 | 1.086 | 26.290 | 1.090 | 1.012 |
| haiyangkadun.19 | 3.399 | 1.091 | 36.764 | 0.903 | 1.004 |
| haiyangkadun.20 | 9.849 | 1.074 | 26.945 | 0.916 | 0.993 |
| haiyangkadun.9 | 19.388 | 1.254 | 20.690 | 0.964 | 1.012 |
| haiyangyuanjia.6 | 5.163 | 1.153 | 30.945 | 0.941 | 0.997 |
| haiyangyuanjia.7 | 5.298 | 1.141 | 32.369 | 0.897 | 0.988 |
| haiyangyuanjia.8 | 3.930 | 0.985 | 34.670 | 0.900 | 0.984 |
| jianci.4 | 14.213 | 0.226 | 24.086 | 1.238 | 1.126 |
| jianci.5 | 12.261 | 0.182 | 25.810 | 0.947 | 1.011 |
| jianci.6 | 1.634 | 1.088 | 40.894 | 0.833 | 0.957 |
| jiaomaozao.13 | 1.326 | 1.341 | 42.198 | 0.860 | 0.973 |
| jiaomaozao.14 | 1.854 | 1.354 | 39.964 | 0.845 | 0.923 |
| jiaomaozao.17 | 1.781 | 0.918 | 40.792 | 0.904 | 0.998 |
| jiaomaozao.18 | 1.472 | 1.002 | 42.142 | 0.870 | 0.951 |
| jiaomaozao.19 | 2.041 | 1.515 | 39.101 | 0.848 | 0.911 |
| jiaomaozao.26 | 2.044 | 1.140 | 39.569 | 0.876 | 0.990 |
| jiaomaozao.27 | 1.086 | 1.064 | 45.140 | 0.876 | 0.978 |
| jiaomaozao.28 | 1.798 | 1.071 | 40.948 | 0.849 | 0.940 |
| jiaomaozao.29 | 10.057 | 1.303 | 27.550 | 0.877 | 0.999 |
| juciqigou.3 | 4.390 | 1.008 | 33.809 | 0.906 | 0.970 |
| kailun.2 | 8.712 | 1.081 | 27.594 | 0.849 | 0.955 |
| lianzhuang.4 | 8.288 | 1.145 | 28.818 | 0.891 | 0.992 |
| lianzhuang.5 | 7.268 | 1.080 | 29.813 | 0.880 | 0.987 |
| lianzhuang.6 | 7.564 | 1.114 | 29.472 | 0.884 | 0.985 |
| lianzhuangluojia.10 | 3.167 | 0.603 | 34.156 | 1.006 | 0.991 |
| lianzhuangluojia.11 | 7.033 | 1.069 | 30.464 | 1.042 | 1.011 |
| lianzhuangluojia.12 | 8.984 | 1.234 | 27.832 | 0.882 | 0.994 |
| lianzhuangluojia.13 | 3.967 | 1.113 | 35.411 | 0.835 | 0.976 |
| lianzhuangluojia.14 | 3.967 | 1.084 | 35.421 | 0.834 | 0.982 |
| lianzhuangluojia.8 | 19.071 | 1.144 | 20.855 | 0.926 | 1.005 |
| lianzhuangluojia.9 | 2.909 | 0.906 | 34.867 | 1.179 | 1.006 |
| limayuanjia.10 | 20.854 | 1.463 | 20.312 | 0.926 | 1.016 |
| limayuanjia.11 | 18.159 | 1.322 | 20.900 | 0.943 | 1.010 |
| limayuanjia.12 | 21.409 | 1.302 | 20.000 | 0.928 | 0.996 |
| limayuanjia.13 | 20.729 | 1.445 | 20.413 | 0.944 | 1.016 |
| limayuanjia.14 | 8.505 | 1.112 | 28.619 | 0.958 | 1.004 |
| limayuanjia.15 | 9.492 | 1.118 | 27.607 | 0.959 | 1.005 |
| limayuanjia.16 | 15.930 | 1.208 | 23.138 | 0.901 | 0.996 |
| limayuanjia.18 | 10.204 | 1.170 | 26.952 | 0.920 | 0.996 |
| limayuanjia.9 | 18.337 | 1.396 | 20.903 | 0.929 | 1.016 |
| lingxinghaixian.5 | 13.310 | 0.141 | 25.333 | 1.037 | 1.035 |
| lingxinghaixian.6 | 12.998 | 0.277 | 23.903 | 0.974 | 0.984 |
| luojiazao.4 | 2.275 | 0.950 | 37.711 | 0.880 | 0.995 |
| luojiazao.5 | 2.909 | 0.986 | 36.996 | 0.899 | 0.997 |
| luojiazao.6 | 2.818 | 1.024 | 36.064 | 0.881 | 0.995 |
| luoshijiaomao.3 | 5.409 | 1.120 | 32.077 | 0.893 | 1.012 |
| luoshijiaomao.4 | 4.958 | 1.085 | 31.814 | 0.884 | 1.014 |
| mashi.2 | 8.778 | 1.043 | 27.467 | 0.852 | 0.961 |
| mishikailun.8 | 3.422 | 1.185 | 35.646 | 0.897 | 0.985 |
| nilingxing.3 | 2.881 | 0.736 | 37.164 | 0.831 | 1.006 |
| nilingxing.4 | 3.966 | 1.055 | 35.176 | 0.876 | 1.002 |
| paige.4 | 1.593 | 0.757 | 41.594 | 0.889 | 1.006 |
| paige.5 | 12.913 | 0.221 | 25.473 | 1.074 | 0.992 |
| qiangzhuang.12 | 15.285 | 1.299 | 20.962 | 0.981 | 1.089 |
| qiangzhuang.13 | 15.280 | 1.360 | 20.967 | 0.954 | 1.071 |
| qiangzhuang.14 | 15.208 | 1.189 | 20.968 | 0.971 | 1.062 |
| qiangzhuang.15 | 15.199 | 1.234 | 20.967 | 0.974 | 1.061 |
| qiangzhuang.16 | 15.792 | 1.946 | 21.074 | 0.939 | 1.069 |
| qiangzhuang.17 | 24.865 | 2.229 | 18.846 | 1.101 | 1.096 |
| qiangzhuang.18 | 14.553 | 1.144 | 21.523 | 1.032 | 1.047 |
| qiangzhuang.19 | 14.499 | 1.158 | 21.527 | 1.031 | 1.062 |
| qiangzhuang.20 | 14.473 | 1.178 | 21.537 | 1.036 | 1.063 |
| qiangzhuang.21 | 14.512 | 1.171 | 21.530 | 1.036 | 1.062 |
| qiangzhuang.22 | 14.511 | 1.165 | 21.533 | 1.015 | 1.047 |
| qiangzhuang.25 | 14.462 | 1.190 | 21.570 | 0.973 | 1.034 |
| qiangzhuang.26 | 14.494 | 1.174 | 21.549 | 1.004 | 1.049 |
| qiangzhuang.28 | 14.511 | 1.159 | 21.527 | 1.047 | 1.061 |
| qiuxing.3 | 2.476 | 0.985 | 39.183 | 0.766 | 1.023 |
| qiuxing.4 | 11.510 | 1.075 | 25.858 | 0.812 | 1.029 |
| redai.3 | 7.928 | 1.200 | 29.173 | 0.856 | 0.973 |
| redai.4 | 9.360 | 1.270 | 27.293 | 0.887 | 0.989 |
| ribenxing.3 | 3.640 | 1.056 | 34.530 | 0.877 | 0.998 |
| ribenxing.4 | 8.630 | 1.088 | 28.574 | 0.999 | 1.046 |
| rouruo.3 | 1.143 | 0.956 | 44.642 | 0.878 | 1.009 |
| rouruo.4 | 7.775 | 1.134 | 29.271 | 0.959 | 1.019 |
| sanjiaoji.10 | 7.989 | 1.104 | 28.407 | 0.841 | 0.934 |
| sanjiaoji.9 | 7.928 | 1.096 | 28.476 | 0.844 | 0.940 |
| shikelipu.4 | 6.374 | 1.088 | 31.116 | 0.853 | 0.995 |
| shikelipu.5 | 9.019 | 1.169 | 27.707 | 0.864 | 1.000 |
| suojiao.6 | 12.475 | 0.191 | 23.245 | 0.965 | 1.025 |
| tama.10 | 31.589 | 2.202 | 16.374 | 1.003 | 1.023 |
| tama.11 | 6.279 | 0.915 | 30.221 | 1.395 | 1.023 |
| tama.12 | 31.056 | 2.277 | 16.308 | 0.998 | 1.051 |
| tama.13 | 4.565 | 0.844 | 32.528 | 0.987 | 0.994 |
| tama.14 | 6.250 | 0.901 | 30.243 | 1.446 | 1.025 |
| tama.16 | 1.520 | 0.760 | 42.008 | 0.731 | 1.002 |
| tama.8 | 31.824 | 2.212 | 16.306 | 1.004 | 1.030 |
| tama.9 | 6.252 | 0.924 | 30.270 | 1.348 | 1.023 |
| tiaowenhuangou.4 | 15.273 | 1.425 | 23.395 | 0.825 | 0.969 |
| tiaowenhuangou.5 | 15.218 | 1.417 | 23.427 | 0.826 | 0.967 |
| tiaowenhuangou.6 | 6.213 | 1.087 | 31.260 | 0.874 | 0.994 |
| weiruan.7 | 10.050 | 1.128 | 27.206 | 0.857 | 0.976 |
| weiruan.8 | 11.028 | 1.127 | 26.415 | 0.855 | 0.979 |
| weixiaoyuanjia.13 | 14.033 | 1.159 | 21.945 | 0.991 | 1.023 |
| weixiaoyuanjia.14 | 13.696 | 1.141 | 22.232 | 0.979 | 1.022 |
| weixiaoyuanjia.15 | 13.524 | 1.145 | 22.215 | 0.980 | 1.021 |
| weixiaoyuanjia.16 | 13.761 | 1.141 | 22.228 | 0.992 | 1.021 |
| weixiaoyuanjia.17 | 13.720 | 1.165 | 22.221 | 0.961 | 1.013 |
| weixiaoyuanjia.18 | 13.681 | 1.153 | 22.231 | 0.980 | 1.025 |
| weixiaoyuanjia.19 | 13.910 | 1.156 | 22.145 | 0.996 | 1.026 |
| weixiaoyuanjia.20 | 13.579 | 1.178 | 22.239 | 0.965 | 1.015 |
| weixiaoyuanjia.21 | 29.757 | 3.312 | 16.630 | 1.248 | 1.214 |
| weixiaoyuanjia.22 | 43.011 | 27.338 | 14.827 | 1.080 | 0.962 |
| weixiaoyuanjia.23 | 31.011 | 2.838 | 16.187 | 1.032 | 1.099 |
| weixiaoyuanjia.24 | 30.774 | 2.467 | 16.329 | 1.010 | 1.093 |
| weixiaoyuanjia.26 | 30.956 | 2.372 | 16.318 | 1.000 | 1.060 |
| weixiaoyuanjia.28 | 14.510 | 1.160 | 21.842 | 0.992 | 1.019 |
| xinyue.4 | 13.459 | 1.154 | 22.542 | 0.926 | 1.083 |
| xinyue.5 | 10.819 | 1.013 | 26.466 | 0.849 | 0.997 |
| xinyue.6 | 13.517 | 1.155 | 22.656 | 0.975 | 1.087 |
| xuanlianjiaomao.3 | 0.928 | 0.912 | 46.465 | 0.883 | 0.990 |
| xuanlianjiaomao.4 | 0.866 | 0.862 | 47.011 | 0.866 | 1.006 |
| xuehong.10 | 6.400 | 1.191 | 30.430 | 0.867 | 0.997 |
| xuehong.11 | 7.086 | 1.179 | 29.387 | 0.868 | 0.999 |
| xuehong.12 | 7.094 | 1.192 | 29.389 | 0.866 | 0.997 |
| xuehong.13 | 7.099 | 1.182 | 29.384 | 0.867 | 0.999 |
| xuehong.14 | 7.106 | 1.192 | 29.372 | 0.864 | 0.998 |
| xuehong.16 | 15.150 | 1.309 | 21.006 | 0.868 | 0.994 |
| xuehong.8 | 5.009 | 1.279 | 32.639 | 0.855 | 0.975 |
| xuehong.9 | 7.088 | 1.183 | 29.383 | 0.870 | 0.999 |
| yuanhai.6 | 14.777 | 1.106 | 21.755 | 1.017 | 1.023 |
| yuanhai.7 | 14.964 | 1.093 | 21.698 | 1.056 | 1.035 |
| yuanhai.8 | 14.716 | 1.105 | 21.788 | 0.998 | 1.020 |
| yuanjiazao.6 | 4.759 | 1.129 | 32.359 | 0.925 | 0.991 |
| yuanjiazao.8 | 7.405 | 0.943 | 28.586 | 0.866 | 0.995 |

Mean metrics:

- mean_abs_bgr_delta: `11.7138`
- mean_abs_luma_delta: `1.3708`
- mean_abs_chroma_delta: `7.9785`
- psnr_vs_raw: `27.2740`
- grad_mean_ratio: `0.9450`
- luma_std_ratio: `1.0132`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v2_ff02_myedge168_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chazhuang.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chazhuang.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chazhuang.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chichaoyiwan.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chichaoyiwan.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chichaoyiwan.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chichaoyiwan.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chichaoyiwan.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chichaoyiwan.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chichaoyiwan.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\chichaoyiwan.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.20_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.21_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.22_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.24_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\donghaiyuanjia.26_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\duolie.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\duolie.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\duolie.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\duolie.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\duowenqigou.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\duowenqigou.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\fanquyuanjia.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\fanquyuanjia.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\gutiao.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\hailianzao.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\hailianzao.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\hailianzao.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\hailianzao.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.20_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangkadun.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangyuanjia.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangyuanjia.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\haiyangyuanjia.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jianci.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jianci.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jianci.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.26_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.27_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.28_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\jiaomaozao.29_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\juciqigou.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\kailun.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuang.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuang.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuang.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuangluojia.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuangluojia.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuangluojia.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuangluojia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuangluojia.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuangluojia.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lianzhuangluojia.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\limayuanjia.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lingxinghaixian.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\luojiazao.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\luojiazao.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\luojiazao.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\luoshijiaomao.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\luoshijiaomao.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\mashi.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\mishikailun.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\nilingxing.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\nilingxing.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\paige.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\paige.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.20_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.21_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.22_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.25_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.26_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiangzhuang.28_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiuxing.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\qiuxing.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\redai.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\redai.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\ribenxing.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\ribenxing.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\rouruo.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\rouruo.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\sanjiaoji.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\sanjiaoji.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\shikelipu.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\shikelipu.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\suojiao.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tama.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tama.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tama.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tama.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tama.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tama.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tama.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tiaowenhuangou.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tiaowenhuangou.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\tiaowenhuangou.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weiruan.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weiruan.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.20_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.21_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.22_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.23_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.24_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.26_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\weixiaoyuanjia.28_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xinyue.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xinyue.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xinyue.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuanlianjiaomao.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuanlianjiaomao.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuehong.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuehong.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuehong.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuehong.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuehong.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuehong.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuehong.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\xuehong.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\yuanhai.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\yuanhai.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\yuanhai.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\yuanjiazao.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_myedge168_v1\yuanjiazao.8_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
