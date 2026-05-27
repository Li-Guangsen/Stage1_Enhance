# full_flow_downstream_stage1_mainline_v1 myedge168_v8 status

Date: 2026-05-27

## Summary

- Status: `complete_myedge168_stage1_enhancement_preflight`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\myedge168_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\myedge168\full_flow_downstream_stage1_mainline_v1_v8`
- Expected images: `168`
- Observed runtime: `74.9` sec total, `0.45` sec/image
- Projected 168 runtime: `1.2` min
- Decision: `ready_for_myedge_fixed_detector_preflight`

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
| chazhuang.3 | 1.133 | 1.080 | 45.213 | 1.008 | 1.014 |
| chazhuang.4 | 11.969 | 1.099 | 25.710 | 1.054 | 1.025 |
| chazhuang.6 | 0.885 | 0.768 | 45.982 | 1.066 | 1.042 |
| chichaoyiwan.1 | 12.808 | 1.070 | 24.603 | 1.050 | 1.227 |
| chichaoyiwan.16 | 12.682 | 1.086 | 24.655 | 1.058 | 1.177 |
| chichaoyiwan.2 | 12.684 | 1.070 | 24.639 | 1.062 | 1.250 |
| chichaoyiwan.3 | 12.682 | 1.063 | 24.660 | 1.068 | 1.231 |
| chichaoyiwan.4 | 12.695 | 1.081 | 24.632 | 1.052 | 1.263 |
| chichaoyiwan.5 | 8.810 | 1.139 | 26.033 | 1.047 | 1.057 |
| chichaoyiwan.6 | 7.024 | 1.087 | 30.259 | 1.055 | 1.149 |
| chichaoyiwan.7 | 7.051 | 1.058 | 30.231 | 1.056 | 1.114 |
| donghaiyuanjia.12 | 10.204 | 2.015 | 26.033 | 1.130 | 1.147 |
| donghaiyuanjia.13 | 9.976 | 1.719 | 26.177 | 1.094 | 1.089 |
| donghaiyuanjia.14 | 10.018 | 1.775 | 26.088 | 1.096 | 1.097 |
| donghaiyuanjia.15 | 10.143 | 1.969 | 26.097 | 1.101 | 1.101 |
| donghaiyuanjia.16 | 22.658 | 8.276 | 19.467 | 1.126 | 1.255 |
| donghaiyuanjia.17 | 22.664 | 8.357 | 19.480 | 1.094 | 1.183 |
| donghaiyuanjia.18 | 22.315 | 9.725 | 19.765 | 1.428 | 1.278 |
| donghaiyuanjia.19 | 11.027 | 6.917 | 26.041 | 1.142 | 1.234 |
| donghaiyuanjia.20 | 10.035 | 2.095 | 25.461 | 1.054 | 1.060 |
| donghaiyuanjia.21 | 9.942 | 2.097 | 25.533 | 1.051 | 1.060 |
| donghaiyuanjia.22 | 10.322 | 3.069 | 25.671 | 1.055 | 1.102 |
| donghaiyuanjia.24 | 12.808 | 1.173 | 24.156 | 1.016 | 1.063 |
| donghaiyuanjia.26 | 22.586 | 7.475 | 19.334 | 1.077 | 1.220 |
| duolie.5 | 8.587 | 1.198 | 28.695 | 1.016 | 1.053 |
| duolie.6 | 8.226 | 1.099 | 29.042 | 1.013 | 1.049 |
| duolie.7 | 8.230 | 1.131 | 29.048 | 1.012 | 1.040 |
| duolie.8 | 7.909 | 1.072 | 29.372 | 1.013 | 1.039 |
| duowenqigou.3 | 1.803 | 1.020 | 42.072 | 1.003 | 1.011 |
| duowenqigou.4 | 1.904 | 0.996 | 40.982 | 1.004 | 1.015 |
| fanquyuanjia.3 | 9.890 | 2.125 | 25.225 | 1.010 | 1.018 |
| fanquyuanjia.4 | 14.161 | 1.075 | 23.770 | 0.981 | 0.998 |
| gutiao.2 | 9.366 | 1.110 | 27.335 | 1.022 | 1.018 |
| hailianzao.10 | 4.200 | 0.894 | 33.726 | 1.007 | 0.998 |
| hailianzao.6 | 1.115 | 0.993 | 45.190 | 1.021 | 1.025 |
| hailianzao.7 | 1.382 | 0.851 | 42.978 | 1.032 | 1.017 |
| hailianzao.8 | 9.350 | 1.230 | 25.982 | 1.019 | 1.000 |
| haiyangkadun.10 | 13.986 | 2.232 | 24.396 | 1.096 | 1.079 |
| haiyangkadun.11 | 14.026 | 3.252 | 24.570 | 1.033 | 1.085 |
| haiyangkadun.12 | 14.318 | 2.456 | 24.297 | 1.057 | 1.111 |
| haiyangkadun.13 | 14.660 | 1.036 | 23.771 | 1.066 | 1.045 |
| haiyangkadun.14 | 11.819 | 1.097 | 25.727 | 1.153 | 1.066 |
| haiyangkadun.15 | 10.574 | 1.190 | 26.805 | 1.089 | 1.031 |
| haiyangkadun.16 | 9.063 | 1.132 | 28.156 | 1.068 | 1.029 |
| haiyangkadun.19 | 2.789 | 1.097 | 38.511 | 1.033 | 1.028 |
| haiyangkadun.20 | 8.891 | 1.452 | 27.888 | 1.010 | 0.981 |
| haiyangkadun.9 | 14.044 | 2.197 | 24.362 | 1.060 | 1.069 |
| haiyangyuanjia.6 | 4.559 | 1.126 | 32.074 | 1.014 | 1.017 |
| haiyangyuanjia.7 | 4.376 | 0.930 | 33.985 | 1.020 | 1.008 |
| haiyangyuanjia.8 | 3.446 | 0.989 | 35.770 | 1.013 | 1.010 |
| jianci.4 | 12.305 | 0.214 | 25.414 | 1.211 | 1.181 |
| jianci.5 | 10.962 | 0.182 | 26.665 | 1.082 | 1.084 |
| jianci.6 | 0.942 | 0.972 | 46.138 | 1.014 | 1.014 |
| jiaomaozao.13 | 0.935 | 0.954 | 46.797 | 1.015 | 1.006 |
| jiaomaozao.14 | 1.116 | 0.928 | 45.323 | 1.013 | 1.020 |
| jiaomaozao.17 | 1.765 | 1.004 | 40.753 | 1.027 | 1.025 |
| jiaomaozao.18 | 1.004 | 0.969 | 46.129 | 1.027 | 1.029 |
| jiaomaozao.19 | 1.205 | 0.903 | 44.428 | 1.015 | 1.015 |
| jiaomaozao.26 | 1.550 | 1.068 | 41.834 | 1.010 | 1.003 |
| jiaomaozao.27 | 1.016 | 1.029 | 46.323 | 1.032 | 1.036 |
| jiaomaozao.28 | 1.245 | 0.924 | 44.444 | 1.019 | 1.030 |
| jiaomaozao.29 | 8.336 | 2.018 | 29.343 | 1.013 | 1.028 |
| juciqigou.3 | 3.025 | 1.052 | 36.999 | 1.014 | 1.019 |
| kailun.2 | 7.587 | 1.030 | 28.618 | 1.010 | 1.024 |
| lianzhuang.4 | 6.464 | 1.069 | 30.985 | 1.022 | 1.024 |
| lianzhuang.5 | 6.072 | 1.073 | 31.485 | 1.022 | 1.028 |
| lianzhuang.6 | 6.160 | 1.047 | 31.371 | 1.019 | 1.017 |
| lianzhuangluojia.10 | 2.395 | 0.997 | 36.810 | 1.182 | 1.062 |
| lianzhuangluojia.11 | 5.749 | 1.096 | 32.199 | 1.046 | 1.054 |
| lianzhuangluojia.12 | 7.354 | 1.570 | 29.843 | 1.048 | 1.053 |
| lianzhuangluojia.13 | 3.446 | 1.042 | 36.830 | 1.012 | 1.027 |
| lianzhuangluojia.14 | 3.322 | 1.032 | 37.056 | 1.011 | 1.028 |
| lianzhuangluojia.8 | 12.646 | 1.178 | 24.639 | 1.023 | 1.056 |
| lianzhuangluojia.9 | 2.485 | 0.964 | 36.825 | 1.092 | 1.023 |
| limayuanjia.10 | 13.566 | 2.955 | 24.578 | 1.018 | 1.065 |
| limayuanjia.11 | 13.200 | 2.464 | 24.669 | 1.019 | 1.045 |
| limayuanjia.12 | 14.351 | 2.859 | 23.825 | 0.999 | 0.992 |
| limayuanjia.13 | 13.007 | 4.440 | 25.164 | 1.007 | 1.040 |
| limayuanjia.14 | 6.827 | 1.091 | 30.513 | 1.029 | 1.030 |
| limayuanjia.15 | 7.261 | 1.099 | 29.921 | 1.029 | 1.031 |
| limayuanjia.16 | 13.181 | 1.847 | 24.929 | 1.040 | 1.014 |
| limayuanjia.18 | 8.384 | 1.083 | 28.673 | 1.017 | 1.006 |
| limayuanjia.9 | 13.785 | 2.775 | 24.495 | 1.019 | 1.063 |
| lingxinghaixian.5 | 11.613 | 0.138 | 26.543 | 1.077 | 1.095 |
| lingxinghaixian.6 | 10.435 | 2.125 | 26.746 | 1.031 | 1.004 |
| luojiazao.4 | 2.070 | 0.899 | 38.782 | 1.012 | 0.991 |
| luojiazao.5 | 2.740 | 0.985 | 37.382 | 1.019 | 1.001 |
| luojiazao.6 | 2.691 | 0.719 | 36.505 | 1.008 | 0.992 |
| luoshijiaomao.3 | 4.521 | 1.081 | 33.636 | 1.038 | 1.059 |
| luoshijiaomao.4 | 4.037 | 1.056 | 33.452 | 1.044 | 1.096 |
| mashi.2 | 7.338 | 1.032 | 28.741 | 1.009 | 1.019 |
| mishikailun.8 | 3.122 | 0.965 | 36.370 | 1.001 | 1.005 |
| nilingxing.3 | 2.709 | 0.739 | 37.575 | 1.063 | 1.063 |
| nilingxing.4 | 3.463 | 1.085 | 36.423 | 1.017 | 1.015 |
| paige.4 | 1.142 | 1.029 | 45.166 | 1.044 | 1.029 |
| paige.5 | 10.874 | 1.132 | 27.130 | 1.089 | 1.026 |
| qiangzhuang.12 | 9.850 | 4.071 | 25.808 | 1.118 | 1.233 |
| qiangzhuang.13 | 9.913 | 4.168 | 25.791 | 1.104 | 1.212 |
| qiangzhuang.14 | 9.769 | 3.402 | 25.643 | 1.132 | 1.200 |
| qiangzhuang.15 | 9.708 | 3.323 | 25.599 | 1.090 | 1.186 |
| qiangzhuang.16 | 10.211 | 4.218 | 25.821 | 1.148 | 1.251 |
| qiangzhuang.17 | 17.017 | 5.470 | 22.024 | 1.203 | 1.314 |
| qiangzhuang.18 | 8.485 | 1.291 | 26.038 | 1.154 | 1.204 |
| qiangzhuang.19 | 8.506 | 1.309 | 26.045 | 1.171 | 1.190 |
| qiangzhuang.20 | 8.525 | 1.314 | 26.047 | 1.167 | 1.171 |
| qiangzhuang.21 | 8.529 | 1.341 | 26.058 | 1.180 | 1.190 |
| qiangzhuang.22 | 8.532 | 1.386 | 26.076 | 1.170 | 1.164 |
| qiangzhuang.25 | 8.504 | 1.316 | 26.066 | 1.096 | 1.134 |
| qiangzhuang.26 | 8.548 | 1.394 | 26.081 | 1.158 | 1.160 |
| qiangzhuang.28 | 8.545 | 1.315 | 26.045 | 1.165 | 1.191 |
| qiuxing.3 | 1.904 | 1.006 | 40.468 | 1.016 | 1.136 |
| qiuxing.4 | 9.027 | 1.069 | 27.973 | 1.032 | 1.111 |
| redai.3 | 6.603 | 1.150 | 30.801 | 1.012 | 1.011 |
| redai.4 | 8.227 | 1.923 | 28.897 | 1.048 | 1.055 |
| ribenxing.3 | 3.168 | 1.083 | 35.787 | 1.036 | 1.062 |
| ribenxing.4 | 6.849 | 1.053 | 30.509 | 1.075 | 1.110 |
| rouruo.3 | 1.052 | 1.017 | 45.616 | 1.026 | 1.044 |
| rouruo.4 | 6.184 | 1.034 | 31.319 | 1.056 | 1.062 |
| sanjiaoji.10 | 6.818 | 1.011 | 29.602 | 1.013 | 1.032 |
| sanjiaoji.9 | 6.661 | 0.998 | 29.820 | 1.012 | 1.028 |
| shikelipu.4 | 5.305 | 1.031 | 32.757 | 1.011 | 1.018 |
| shikelipu.5 | 7.473 | 1.500 | 29.598 | 1.038 | 1.077 |
| suojiao.6 | 10.304 | 0.328 | 25.923 | 1.052 | 1.083 |
| tama.10 | 23.104 | 5.366 | 19.151 | 1.063 | 1.079 |
| tama.11 | 5.119 | 1.047 | 32.085 | 1.165 | 1.067 |
| tama.12 | 22.979 | 7.332 | 19.135 | 1.071 | 1.152 |
| tama.13 | 3.617 | 0.762 | 34.562 | 1.099 | 1.042 |
| tama.14 | 5.073 | 1.042 | 32.158 | 1.210 | 1.064 |
| tama.16 | 1.202 | 1.026 | 45.245 | 1.017 | 1.016 |
| tama.8 | 23.156 | 6.070 | 19.080 | 1.142 | 1.103 |
| tama.9 | 5.050 | 1.037 | 32.204 | 1.087 | 1.067 |
| tiaowenhuangou.4 | 12.936 | 1.969 | 25.017 | 1.009 | 0.996 |
| tiaowenhuangou.5 | 12.870 | 1.973 | 25.069 | 1.009 | 0.996 |
| tiaowenhuangou.6 | 5.327 | 1.026 | 32.661 | 1.016 | 1.009 |
| weiruan.7 | 8.104 | 1.106 | 29.153 | 1.011 | 1.024 |
| weiruan.8 | 8.985 | 1.209 | 28.255 | 1.014 | 1.031 |
| weixiaoyuanjia.13 | 8.324 | 1.162 | 26.224 | 1.092 | 1.109 |
| weixiaoyuanjia.14 | 8.461 | 1.117 | 26.202 | 1.078 | 1.092 |
| weixiaoyuanjia.15 | 8.388 | 1.150 | 26.156 | 1.060 | 1.084 |
| weixiaoyuanjia.16 | 8.533 | 1.141 | 26.146 | 1.090 | 1.104 |
| weixiaoyuanjia.17 | 8.577 | 1.130 | 26.143 | 1.078 | 1.091 |
| weixiaoyuanjia.18 | 8.479 | 1.177 | 26.190 | 1.085 | 1.113 |
| weixiaoyuanjia.19 | 8.726 | 1.146 | 26.077 | 1.081 | 1.100 |
| weixiaoyuanjia.20 | 8.530 | 1.235 | 26.200 | 1.065 | 1.074 |
| weixiaoyuanjia.21 | 27.499 | 12.542 | 18.138 | 1.914 | 1.559 |
| weixiaoyuanjia.22 | 43.868 | 28.858 | 14.691 | 0.985 | 0.899 |
| weixiaoyuanjia.23 | 22.984 | 8.455 | 19.309 | 1.164 | 1.326 |
| weixiaoyuanjia.24 | 22.613 | 7.551 | 19.294 | 1.176 | 1.313 |
| weixiaoyuanjia.26 | 22.860 | 7.392 | 19.182 | 1.116 | 1.199 |
| weixiaoyuanjia.28 | 8.647 | 1.109 | 26.109 | 1.088 | 1.082 |
| xinyue.4 | 8.599 | 1.165 | 26.139 | 1.095 | 1.214 |
| xinyue.5 | 9.291 | 1.021 | 27.839 | 1.015 | 1.051 |
| xinyue.6 | 8.711 | 1.149 | 26.279 | 1.089 | 1.284 |
| xuanlianjiaomao.3 | 0.809 | 0.759 | 47.332 | 1.034 | 1.036 |
| xuanlianjiaomao.4 | 0.817 | 0.779 | 47.367 | 1.017 | 1.040 |
| xuehong.10 | 5.286 | 1.109 | 32.156 | 1.019 | 1.029 |
| xuehong.11 | 5.424 | 1.265 | 31.902 | 1.028 | 1.021 |
| xuehong.12 | 5.478 | 1.310 | 31.865 | 1.030 | 1.024 |
| xuehong.13 | 5.388 | 1.230 | 31.956 | 1.030 | 1.024 |
| xuehong.14 | 5.498 | 1.312 | 31.839 | 1.028 | 1.026 |
| xuehong.16 | 10.330 | 1.847 | 25.323 | 0.999 | 0.992 |
| xuehong.8 | 4.240 | 1.027 | 34.173 | 1.008 | 1.006 |
| xuehong.9 | 5.427 | 1.260 | 31.893 | 1.027 | 1.021 |
| yuanhai.6 | 9.031 | 1.221 | 26.043 | 1.162 | 1.119 |
| yuanhai.7 | 9.146 | 1.141 | 25.964 | 1.204 | 1.152 |
| yuanhai.8 | 8.727 | 1.252 | 26.068 | 1.066 | 1.086 |
| yuanjiazao.6 | 3.857 | 0.977 | 33.794 | 1.015 | 1.000 |
| yuanjiazao.8 | 6.285 | 1.068 | 30.128 | 1.009 | 1.015 |

Mean metrics:

- mean_abs_bgr_delta: `8.6772`
- mean_abs_luma_delta: `2.0101`
- mean_abs_chroma_delta: `5.8024`
- psnr_vs_raw: `29.9656`
- grad_mean_ratio: `1.0646`
- luma_std_ratio: `1.0798`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_myedge168_v8_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chazhuang.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chazhuang.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chazhuang.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chichaoyiwan.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chichaoyiwan.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chichaoyiwan.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chichaoyiwan.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chichaoyiwan.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chichaoyiwan.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chichaoyiwan.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\chichaoyiwan.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.20_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.21_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.22_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.24_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\donghaiyuanjia.26_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\duolie.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\duolie.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\duolie.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\duolie.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\duowenqigou.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\duowenqigou.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\fanquyuanjia.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\fanquyuanjia.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\gutiao.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\hailianzao.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\hailianzao.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\hailianzao.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\hailianzao.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.20_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangkadun.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangyuanjia.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangyuanjia.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\haiyangyuanjia.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jianci.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jianci.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jianci.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.26_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.27_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.28_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\jiaomaozao.29_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\juciqigou.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\kailun.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuang.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuang.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuang.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuangluojia.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuangluojia.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuangluojia.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuangluojia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuangluojia.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuangluojia.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lianzhuangluojia.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\limayuanjia.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lingxinghaixian.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\lingxinghaixian.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\luojiazao.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\luojiazao.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\luojiazao.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\luoshijiaomao.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\luoshijiaomao.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\mashi.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\mishikailun.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\nilingxing.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\nilingxing.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\paige.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\paige.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.20_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.21_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.22_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.25_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.26_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiangzhuang.28_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiuxing.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\qiuxing.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\redai.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\redai.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\ribenxing.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\ribenxing.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\rouruo.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\rouruo.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\sanjiaoji.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\sanjiaoji.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\shikelipu.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\shikelipu.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\suojiao.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tama.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tama.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tama.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tama.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tama.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tama.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tama.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tama.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tiaowenhuangou.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tiaowenhuangou.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\tiaowenhuangou.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weiruan.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weiruan.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.15_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.19_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.20_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.21_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.22_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.23_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.24_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.26_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\weixiaoyuanjia.28_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xinyue.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xinyue.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xinyue.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuanlianjiaomao.3_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuanlianjiaomao.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuehong.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuehong.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuehong.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuehong.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuehong.14_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuehong.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuehong.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\xuehong.9_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\yuanhai.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\yuanhai.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\yuanhai.8_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\yuanjiazao.6_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\myedge168_v8\yuanjiazao.8_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
