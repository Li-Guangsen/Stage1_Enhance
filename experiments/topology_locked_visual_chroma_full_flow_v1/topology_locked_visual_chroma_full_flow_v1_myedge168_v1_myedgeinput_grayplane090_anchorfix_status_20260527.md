# topology_locked_visual_chroma_full_flow_v1 myedge168_v1_myedgeinput_grayplane090_anchorfix status

Date: 2026-05-27

## Summary

- Status: `fixed_detector_complete_rescue_only_archived_diagnostic`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\myedge168_v1.txt`
- Output root: `experiments\topology_locked_visual_chroma_full_flow_v1\outputs\myedge168_v1_myedgeinput_grayplane090_anchorfix`
- Expected images: `168`
- Observed runtime: `92.9` sec total, `0.55` sec/image
- Projected 168 runtime: `1.5` min
- Decision: `candidate_rescues_legacy_but_not_near_raw`
- Fixed-detector status: `experiments/topology_locked_visual_chroma_full_flow_v1/topology_locked_visual_chroma_full_flow_v1_fixed_detector_tlvc01_status_20260527.md`
- MyEdge result intake: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_results_20260527.md`
- MyEdge structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_structure_metrics_20260527.md`
- MyEdge downstream gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_downstream_gate_20260527.md`

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
| chazhuang.3 | 0.024 | 0.010 | 62.775 | 1.000 | 1.000 |
| chazhuang.4 | 15.683 | 2.111 | 23.195 | 0.998 | 1.013 |
| chazhuang.6 | 0.076 | 0.011 | 58.052 | 1.001 | 1.000 |
| chichaoyiwan.1 | 21.383 | 0.862 | 20.066 | 1.014 | 1.018 |
| chichaoyiwan.16 | 21.256 | 0.849 | 20.088 | 0.997 | 1.002 |
| chichaoyiwan.2 | 20.905 | 0.995 | 20.161 | 1.045 | 1.017 |
| chichaoyiwan.3 | 21.032 | 0.855 | 20.142 | 0.977 | 0.986 |
| chichaoyiwan.4 | 20.964 | 0.968 | 20.142 | 0.976 | 1.003 |
| chichaoyiwan.5 | 14.879 | 1.907 | 21.838 | 0.978 | 1.017 |
| chichaoyiwan.6 | 9.457 | 1.266 | 27.639 | 0.908 | 0.986 |
| chichaoyiwan.7 | 9.653 | 1.348 | 27.488 | 0.924 | 0.984 |
| donghaiyuanjia.12 | 14.438 | 3.121 | 22.028 | 1.015 | 1.004 |
| donghaiyuanjia.13 | 14.471 | 3.039 | 22.014 | 1.001 | 1.002 |
| donghaiyuanjia.14 | 14.284 | 3.077 | 22.034 | 1.014 | 0.997 |
| donghaiyuanjia.15 | 14.439 | 3.040 | 22.033 | 1.001 | 1.001 |
| donghaiyuanjia.16 | 18.083 | 3.540 | 20.279 | 0.922 | 0.974 |
| donghaiyuanjia.17 | 17.960 | 3.249 | 20.339 | 0.921 | 0.986 |
| donghaiyuanjia.18 | 17.787 | 3.962 | 20.392 | 1.068 | 0.986 |
| donghaiyuanjia.19 | 16.663 | 3.295 | 20.784 | 1.082 | 1.002 |
| donghaiyuanjia.20 | 19.732 | 3.078 | 19.499 | 1.039 | 0.999 |
| donghaiyuanjia.21 | 7.998 | 1.177 | 27.298 | 1.058 | 1.005 |
| donghaiyuanjia.22 | 19.469 | 3.254 | 19.587 | 1.056 | 0.999 |
| donghaiyuanjia.24 | 22.627 | 1.506 | 18.723 | 1.166 | 1.015 |
| donghaiyuanjia.26 | 21.830 | 3.988 | 18.766 | 1.003 | 0.989 |
| duolie.5 | 12.810 | 1.743 | 25.269 | 0.998 | 0.998 |
| duolie.6 | 12.349 | 1.638 | 25.561 | 0.994 | 0.995 |
| duolie.7 | 12.101 | 1.691 | 25.752 | 0.993 | 0.999 |
| duolie.8 | 11.314 | 1.615 | 26.339 | 0.991 | 0.997 |
| duowenqigou.3 | 2.678 | 0.783 | 37.288 | 0.990 | 1.005 |
| duowenqigou.4 | 2.905 | 0.914 | 36.737 | 0.990 | 0.997 |
| fanquyuanjia.3 | 14.365 | 3.287 | 21.841 | 0.993 | 0.993 |
| fanquyuanjia.4 | 14.425 | 2.989 | 23.917 | 1.007 | 0.979 |
| gutiao.2 | 13.204 | 1.758 | 24.275 | 0.998 | 0.985 |
| hailianzao.10 | 6.052 | 0.644 | 29.698 | 1.003 | 1.033 |
| hailianzao.6 | 1.229 | 0.284 | 41.093 | 0.996 | 0.996 |
| hailianzao.7 | 1.186 | 0.345 | 41.609 | 0.995 | 1.004 |
| hailianzao.8 | 14.449 | 1.804 | 22.099 | 1.003 | 0.995 |
| haiyangkadun.10 | 12.599 | 3.352 | 24.571 | 0.944 | 0.996 |
| haiyangkadun.11 | 10.523 | 2.947 | 26.188 | 0.990 | 0.998 |
| haiyangkadun.12 | 10.420 | 2.811 | 26.283 | 1.006 | 1.001 |
| haiyangkadun.13 | 16.104 | 2.289 | 23.177 | 1.000 | 1.000 |
| haiyangkadun.14 | 16.306 | 2.150 | 23.073 | 0.987 | 0.992 |
| haiyangkadun.15 | 15.486 | 2.294 | 23.659 | 0.968 | 0.993 |
| haiyangkadun.16 | 13.847 | 2.044 | 24.605 | 0.987 | 0.993 |
| haiyangkadun.19 | 3.932 | 1.131 | 34.976 | 0.984 | 1.007 |
| haiyangkadun.20 | 13.551 | 2.346 | 23.909 | 0.994 | 1.018 |
| haiyangkadun.9 | 9.929 | 2.716 | 26.442 | 0.958 | 1.001 |
| haiyangyuanjia.6 | 6.189 | 1.144 | 28.633 | 0.994 | 1.003 |
| haiyangyuanjia.7 | 5.958 | 0.543 | 31.014 | 0.966 | 1.001 |
| haiyangyuanjia.8 | 4.635 | 0.636 | 32.755 | 1.005 | 1.022 |
| jianci.4 | 14.356 | 2.005 | 23.981 | 1.001 | 1.002 |
| jianci.5 | 12.340 | 2.027 | 26.088 | 1.009 | 1.007 |
| jianci.6 | 0.626 | 0.389 | 48.701 | 0.996 | 1.001 |
| jiaomaozao.13 | 0.734 | 0.216 | 44.755 | 1.000 | 1.003 |
| jiaomaozao.14 | 0.760 | 0.196 | 45.128 | 1.000 | 0.999 |
| jiaomaozao.17 | 2.225 | 0.362 | 36.936 | 0.990 | 1.003 |
| jiaomaozao.18 | 0.645 | 0.176 | 46.726 | 0.998 | 1.000 |
| jiaomaozao.19 | 1.280 | 0.303 | 41.696 | 0.997 | 0.999 |
| jiaomaozao.26 | 1.943 | 0.287 | 39.996 | 0.997 | 0.998 |
| jiaomaozao.27 | 0.435 | 0.129 | 48.968 | 0.999 | 1.001 |
| jiaomaozao.28 | 0.947 | 0.225 | 42.200 | 0.998 | 1.003 |
| jiaomaozao.29 | 9.236 | 2.782 | 28.564 | 0.985 | 0.989 |
| juciqigou.3 | 4.226 | 0.308 | 32.932 | 1.000 | 1.005 |
| kailun.2 | 9.767 | 0.355 | 26.502 | 1.005 | 1.005 |
| lianzhuang.4 | 9.637 | 1.392 | 27.525 | 0.994 | 0.994 |
| lianzhuang.5 | 8.392 | 0.997 | 28.492 | 0.999 | 1.003 |
| lianzhuang.6 | 8.702 | 1.051 | 28.185 | 0.995 | 0.999 |
| lianzhuangluojia.10 | 3.038 | 0.605 | 35.511 | 0.873 | 1.013 |
| lianzhuangluojia.11 | 7.951 | 0.863 | 29.283 | 0.989 | 1.009 |
| lianzhuangluojia.12 | 11.173 | 2.739 | 26.417 | 0.994 | 0.995 |
| lianzhuangluojia.13 | 4.769 | 1.256 | 33.559 | 0.987 | 1.000 |
| lianzhuangluojia.14 | 4.641 | 1.183 | 33.691 | 0.987 | 1.001 |
| lianzhuangluojia.8 | 20.482 | 1.081 | 20.243 | 0.989 | 1.037 |
| lianzhuangluojia.9 | 1.069 | 0.308 | 42.960 | 0.959 | 1.003 |
| limayuanjia.10 | 10.520 | 2.975 | 26.063 | 0.989 | 0.994 |
| limayuanjia.11 | 10.554 | 2.956 | 26.126 | 0.982 | 0.995 |
| limayuanjia.12 | 10.413 | 2.959 | 26.165 | 0.988 | 0.993 |
| limayuanjia.13 | 10.600 | 3.002 | 26.010 | 0.991 | 0.995 |
| limayuanjia.14 | 10.216 | 1.366 | 26.977 | 0.974 | 1.000 |
| limayuanjia.15 | 11.074 | 1.400 | 26.240 | 0.991 | 0.997 |
| limayuanjia.16 | 16.490 | 2.868 | 23.121 | 0.997 | 0.987 |
| limayuanjia.18 | 12.653 | 1.934 | 25.126 | 0.994 | 0.998 |
| limayuanjia.9 | 12.903 | 3.401 | 24.286 | 0.982 | 0.982 |
| lingxinghaixian.5 | 13.524 | 1.993 | 25.316 | 1.010 | 1.011 |
| lingxinghaixian.6 | 13.807 | 1.759 | 23.454 | 0.989 | 1.013 |
| luojiazao.4 | 3.560 | 0.515 | 33.817 | 0.998 | 1.023 |
| luojiazao.5 | 3.524 | 0.627 | 33.677 | 1.016 | 1.018 |
| luojiazao.6 | 6.745 | 0.828 | 28.901 | 0.995 | 1.018 |
| luoshijiaomao.3 | 6.357 | 1.340 | 30.754 | 0.997 | 1.000 |
| luoshijiaomao.4 | 1.842 | 0.410 | 40.188 | 1.001 | 1.002 |
| mashi.2 | 9.588 | 0.287 | 26.359 | 1.000 | 1.007 |
| mishikailun.8 | 3.884 | 0.385 | 32.087 | 1.001 | 1.009 |
| nilingxing.3 | 3.016 | 0.305 | 37.558 | 0.995 | 0.998 |
| nilingxing.4 | 4.365 | 0.522 | 34.352 | 1.001 | 0.998 |
| paige.4 | 0.524 | 0.171 | 48.413 | 0.995 | 0.999 |
| paige.5 | 12.805 | 1.964 | 25.620 | 1.002 | 1.017 |
| qiangzhuang.12 | 7.778 | 1.982 | 27.419 | 1.011 | 1.000 |
| qiangzhuang.13 | 7.650 | 1.799 | 27.485 | 1.090 | 1.008 |
| qiangzhuang.14 | 7.724 | 1.935 | 27.467 | 1.060 | 1.004 |
| qiangzhuang.15 | 7.765 | 1.951 | 27.427 | 1.051 | 1.004 |
| qiangzhuang.16 | 7.700 | 1.916 | 27.456 | 1.054 | 1.006 |
| qiangzhuang.17 | 29.642 | 3.070 | 17.099 | 1.035 | 1.024 |
| qiangzhuang.18 | 14.629 | 2.154 | 21.760 | 0.972 | 1.007 |
| qiangzhuang.19 | 14.587 | 2.212 | 21.776 | 1.011 | 1.008 |
| qiangzhuang.20 | 14.576 | 2.199 | 21.767 | 1.004 | 1.009 |
| qiangzhuang.21 | 14.594 | 2.203 | 21.783 | 0.945 | 1.003 |
| qiangzhuang.22 | 14.557 | 2.267 | 21.787 | 0.989 | 1.002 |
| qiangzhuang.25 | 14.631 | 2.201 | 21.767 | 0.959 | 1.004 |
| qiangzhuang.26 | 14.639 | 2.196 | 21.767 | 0.948 | 1.005 |
| qiangzhuang.28 | 14.609 | 2.162 | 21.786 | 0.945 | 1.004 |
| qiuxing.3 | 2.891 | 1.017 | 36.973 | 0.975 | 1.001 |
| qiuxing.4 | 12.830 | 1.222 | 24.892 | 0.997 | 0.999 |
| redai.3 | 9.777 | 2.140 | 27.665 | 0.994 | 0.988 |
| redai.4 | 11.533 | 2.845 | 26.059 | 1.002 | 0.990 |
| ribenxing.3 | 3.898 | 0.546 | 33.372 | 1.000 | 1.004 |
| ribenxing.4 | 10.174 | 1.311 | 27.156 | 0.951 | 0.984 |
| rouruo.3 | 0.608 | 0.273 | 47.500 | 0.983 | 1.000 |
| rouruo.4 | 9.138 | 1.225 | 27.864 | 0.981 | 0.984 |
| sanjiaoji.10 | 9.015 | 0.229 | 27.222 | 1.001 | 1.001 |
| sanjiaoji.9 | 8.901 | 0.208 | 27.328 | 0.998 | 1.000 |
| shikelipu.4 | 7.668 | 1.065 | 29.470 | 1.004 | 0.995 |
| shikelipu.5 | 11.311 | 2.713 | 26.236 | 1.004 | 0.985 |
| suojiao.6 | 12.614 | 1.461 | 23.327 | 0.953 | 0.974 |
| tama.10 | 22.496 | 3.890 | 18.721 | 1.005 | 0.983 |
| tama.11 | 7.069 | 0.541 | 29.285 | 1.127 | 1.000 |
| tama.12 | 17.915 | 3.546 | 20.489 | 1.056 | 0.981 |
| tama.13 | 4.402 | 0.321 | 32.952 | 1.000 | 1.009 |
| tama.14 | 7.049 | 0.528 | 29.315 | 1.116 | 1.001 |
| tama.16 | 0.512 | 0.151 | 48.708 | 1.016 | 1.006 |
| tama.8 | 22.651 | 3.876 | 18.649 | 0.949 | 0.980 |
| tama.9 | 7.054 | 0.531 | 29.309 | 1.124 | 1.001 |
| tiaowenhuangou.4 | 13.550 | 2.843 | 24.797 | 0.995 | 0.986 |
| tiaowenhuangou.5 | 13.485 | 2.823 | 24.844 | 0.994 | 0.986 |
| tiaowenhuangou.6 | 7.458 | 1.020 | 29.628 | 0.998 | 1.005 |
| weiruan.7 | 12.261 | 1.696 | 25.593 | 0.990 | 0.992 |
| weiruan.8 | 13.531 | 1.800 | 24.743 | 0.999 | 0.993 |
| weixiaoyuanjia.13 | 14.378 | 2.133 | 21.909 | 0.995 | 1.010 |
| weixiaoyuanjia.14 | 14.289 | 2.383 | 21.951 | 0.967 | 1.000 |
| weixiaoyuanjia.15 | 14.371 | 2.123 | 21.902 | 0.986 | 1.006 |
| weixiaoyuanjia.16 | 14.825 | 1.982 | 21.806 | 0.989 | 1.012 |
| weixiaoyuanjia.17 | 14.756 | 1.930 | 21.800 | 0.956 | 1.014 |
| weixiaoyuanjia.18 | 14.745 | 1.892 | 21.809 | 0.970 | 1.013 |
| weixiaoyuanjia.19 | 14.686 | 1.698 | 21.805 | 0.955 | 1.008 |
| weixiaoyuanjia.20 | 14.402 | 2.019 | 21.896 | 0.980 | 1.011 |
| weixiaoyuanjia.21 | 22.435 | 3.693 | 18.808 | 1.022 | 0.973 |
| weixiaoyuanjia.22 | 22.153 | 4.053 | 18.848 | 1.007 | 0.916 |
| weixiaoyuanjia.23 | 21.932 | 3.984 | 18.728 | 1.001 | 0.982 |
| weixiaoyuanjia.24 | 21.868 | 3.988 | 18.755 | 0.999 | 0.980 |
| weixiaoyuanjia.26 | 22.416 | 3.603 | 18.725 | 0.835 | 0.973 |
| weixiaoyuanjia.28 | 14.455 | 1.924 | 21.871 | 0.971 | 1.012 |
| xinyue.4 | 12.537 | 1.478 | 23.227 | 1.010 | 1.011 |
| xinyue.5 | 12.237 | 1.395 | 25.528 | 1.011 | 1.001 |
| xinyue.6 | 14.255 | 1.786 | 22.141 | 0.982 | 1.005 |
| xuanlianjiaomao.3 | 0.248 | 0.038 | 51.123 | 1.000 | 1.004 |
| xuanlianjiaomao.4 | 0.609 | 0.111 | 47.197 | 1.007 | 1.008 |
| xuehong.10 | 7.769 | 2.089 | 29.263 | 0.977 | 0.998 |
| xuehong.11 | 8.618 | 2.407 | 28.234 | 0.966 | 0.991 |
| xuehong.12 | 8.590 | 2.380 | 28.269 | 0.967 | 0.991 |
| xuehong.13 | 8.633 | 2.396 | 28.230 | 0.966 | 0.991 |
| xuehong.14 | 8.600 | 2.382 | 28.264 | 0.965 | 0.991 |
| xuehong.16 | 13.507 | 2.908 | 22.907 | 1.007 | 1.010 |
| xuehong.8 | 6.620 | 1.842 | 30.664 | 0.991 | 0.998 |
| xuehong.9 | 8.641 | 2.402 | 28.218 | 0.968 | 0.991 |
| yuanhai.6 | 11.152 | 1.281 | 24.368 | 0.948 | 1.009 |
| yuanhai.7 | 13.051 | 1.301 | 22.968 | 1.111 | 1.019 |
| yuanhai.8 | 11.115 | 1.227 | 24.380 | 0.952 | 1.013 |
| yuanjiazao.6 | 5.724 | 0.578 | 29.014 | 0.993 | 1.025 |
| yuanjiazao.8 | 8.339 | 0.414 | 27.118 | 0.998 | 1.012 |

Mean metrics:

- mean_abs_bgr_delta: `10.7667`
- mean_abs_luma_delta: `1.7113`
- mean_abs_chroma_delta: `7.3842`
- psnr_vs_raw: `27.9651`
- grad_mean_ratio: `0.9956`
- luma_std_ratio: `1.0000`

## Stage Metrics CSV

- `topology_locked_visual_chroma_full_flow_v1_myedge168_v1_myedgeinput_grayplane090_anchorfix_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chazhuang.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chazhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chazhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chichaoyiwan.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chichaoyiwan.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chichaoyiwan.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chichaoyiwan.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chichaoyiwan.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chichaoyiwan.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chichaoyiwan.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\chichaoyiwan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\donghaiyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\duolie.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\duolie.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\duolie.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\duolie.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\duowenqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\duowenqigou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\fanquyuanjia.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\fanquyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\gutiao.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\hailianzao.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\hailianzao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\hailianzao.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\hailianzao.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangkadun.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangyuanjia.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangyuanjia.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\haiyangyuanjia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jianci.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jianci.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jianci.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.27_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\jiaomaozao.29_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\juciqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\kailun.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuang.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuangluojia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuangluojia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuangluojia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuangluojia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuangluojia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuangluojia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lianzhuangluojia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\limayuanjia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lingxinghaixian.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\lingxinghaixian.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\luojiazao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\luojiazao.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\luojiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\luoshijiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\luoshijiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\mashi.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\mishikailun.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\nilingxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\nilingxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\paige.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\paige.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.25_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiangzhuang.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiuxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\qiuxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\redai.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\redai.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\ribenxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\ribenxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\rouruo.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\rouruo.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\sanjiaoji.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\sanjiaoji.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\shikelipu.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\shikelipu.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\suojiao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tama.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tama.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tama.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tama.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tama.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tama.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tama.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tama.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tiaowenhuangou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tiaowenhuangou.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\tiaowenhuangou.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weiruan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weiruan.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.23_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\weixiaoyuanjia.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xinyue.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xinyue.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xinyue.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuanlianjiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuanlianjiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuehong.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuehong.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuehong.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuehong.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuehong.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuehong.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuehong.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\xuehong.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\yuanhai.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\yuanhai.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\yuanhai.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\yuanjiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1_myedgeinput_grayplane090_anchorfix\yuanjiazao.8_panel.jpg`

## Boundary

- This 168 Stage1 output has now been evaluated under fixed MSFI 50k and fixed DiffusionEdge baseline 50k.
- The downstream gate is `candidate_rescues_legacy_but_not_near_raw`; TLVC01 is archived diagnostic evidence, not a downstream-positive mainline.
- It did not modify MyEdge checkpoints, GT, or eval protocol.
- It did not run 502/496 metrics or 2770 full-pool.
