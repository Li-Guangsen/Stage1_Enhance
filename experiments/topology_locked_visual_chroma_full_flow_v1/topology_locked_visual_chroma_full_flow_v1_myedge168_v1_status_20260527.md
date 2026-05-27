# topology_locked_visual_chroma_full_flow_v1 myedge168_v1 status

Date: 2026-05-27

## Summary

- Status: `stage1_168_complete`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\myedge168_v1.txt`
- Output root: `experiments\topology_locked_visual_chroma_full_flow_v1\outputs\myedge168_v1`
- Expected images: `168`
- Observed runtime: `73.4` sec total, `0.44` sec/image
- Projected 168 runtime: `1.2` min
- Decision: `fixed_detector_preflight_required_not_downstream_result`

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
| chazhuang.3 | 0.191 | 0.139 | 54.761 | 1.019 | 1.009 |
| chazhuang.4 | 14.902 | 0.002 | 23.580 | 1.000 | 0.999 |
| chazhuang.6 | 0.013 | 0.004 | 67.110 | 1.001 | 1.000 |
| chichaoyiwan.1 | 18.956 | 0.978 | 21.271 | 0.976 | 0.996 |
| chichaoyiwan.16 | 18.525 | 0.981 | 21.385 | 0.984 | 0.998 |
| chichaoyiwan.2 | 18.157 | 0.996 | 21.489 | 0.996 | 0.999 |
| chichaoyiwan.3 | 18.354 | 0.994 | 21.432 | 0.992 | 0.998 |
| chichaoyiwan.4 | 18.198 | 0.999 | 21.478 | 1.000 | 1.000 |
| chichaoyiwan.5 | 13.004 | 0.996 | 22.550 | 1.001 | 1.000 |
| chichaoyiwan.6 | 9.179 | 0.999 | 27.860 | 1.000 | 0.999 |
| chichaoyiwan.7 | 9.484 | 0.998 | 27.583 | 0.998 | 0.999 |
| donghaiyuanjia.12 | 14.015 | 0.997 | 22.383 | 1.000 | 0.999 |
| donghaiyuanjia.13 | 13.965 | 0.996 | 22.461 | 1.001 | 0.999 |
| donghaiyuanjia.14 | 14.039 | 0.996 | 22.399 | 1.000 | 0.999 |
| donghaiyuanjia.15 | 14.001 | 0.995 | 22.421 | 1.000 | 1.000 |
| donghaiyuanjia.16 | 28.894 | 0.680 | 16.375 | 1.039 | 1.018 |
| donghaiyuanjia.17 | 28.655 | 0.781 | 16.444 | 1.004 | 1.007 |
| donghaiyuanjia.18 | 26.013 | 0.998 | 16.502 | 1.000 | 1.000 |
| donghaiyuanjia.19 | 13.947 | 0.998 | 21.763 | 1.000 | 1.000 |
| donghaiyuanjia.20 | 14.619 | 0.998 | 21.646 | 1.000 | 1.000 |
| donghaiyuanjia.21 | 14.262 | 0.997 | 21.748 | 0.999 | 1.000 |
| donghaiyuanjia.22 | 14.377 | 0.989 | 21.687 | 0.992 | 0.999 |
| donghaiyuanjia.24 | 22.969 | 1.023 | 19.046 | 1.001 | 1.008 |
| donghaiyuanjia.26 | 29.981 | 0.995 | 16.582 | 0.997 | 0.999 |
| duolie.5 | 12.145 | 0.965 | 25.577 | 1.000 | 1.000 |
| duolie.6 | 11.695 | 0.962 | 25.890 | 1.002 | 1.001 |
| duolie.7 | 11.513 | 0.976 | 26.032 | 1.001 | 1.000 |
| duolie.8 | 10.714 | 0.964 | 26.676 | 1.003 | 1.001 |
| duowenqigou.3 | 2.297 | 0.938 | 40.022 | 0.998 | 1.000 |
| duowenqigou.4 | 2.561 | 0.944 | 38.168 | 0.999 | 1.000 |
| fanquyuanjia.3 | 13.794 | 0.962 | 21.635 | 1.000 | 1.000 |
| fanquyuanjia.4 | 13.875 | 0.968 | 23.974 | 0.999 | 1.000 |
| gutiao.2 | 11.823 | 0.973 | 25.275 | 1.008 | 1.000 |
| hailianzao.10 | 5.297 | 0.864 | 31.680 | 1.002 | 0.992 |
| hailianzao.6 | 1.135 | 0.972 | 45.390 | 1.001 | 1.000 |
| hailianzao.7 | 1.388 | 0.831 | 43.062 | 1.003 | 1.002 |
| hailianzao.8 | 12.385 | 0.968 | 23.279 | 1.002 | 1.000 |
| haiyangkadun.10 | 18.525 | 0.997 | 21.293 | 1.000 | 0.999 |
| haiyangkadun.11 | 19.298 | 0.997 | 21.129 | 1.000 | 1.000 |
| haiyangkadun.12 | 18.978 | 0.997 | 21.178 | 1.000 | 0.999 |
| haiyangkadun.13 | 13.703 | 0.976 | 24.394 | 1.012 | 1.001 |
| haiyangkadun.14 | 14.938 | 0.976 | 23.672 | 1.017 | 1.000 |
| haiyangkadun.15 | 14.540 | 0.942 | 23.962 | 1.015 | 1.001 |
| haiyangkadun.16 | 13.084 | 0.992 | 24.887 | 1.006 | 1.000 |
| haiyangkadun.19 | 3.726 | 0.977 | 35.821 | 1.001 | 1.000 |
| haiyangkadun.20 | 12.027 | 0.646 | 25.174 | 0.999 | 0.992 |
| haiyangkadun.9 | 18.581 | 0.997 | 21.274 | 1.000 | 1.000 |
| haiyangyuanjia.6 | 5.789 | 0.988 | 29.645 | 1.001 | 1.000 |
| haiyangyuanjia.7 | 5.915 | 0.938 | 31.260 | 1.002 | 0.991 |
| haiyangyuanjia.8 | 4.214 | 0.987 | 33.965 | 1.000 | 0.999 |
| jianci.4 | 14.411 | 0.098 | 23.992 | 1.016 | 1.028 |
| jianci.5 | 12.704 | 0.002 | 25.642 | 1.001 | 1.000 |
| jianci.6 | 0.960 | 0.944 | 46.134 | 1.004 | 1.001 |
| jiaomaozao.13 | 0.929 | 0.946 | 47.330 | 1.001 | 1.000 |
| jiaomaozao.14 | 1.107 | 0.882 | 45.484 | 1.001 | 1.002 |
| jiaomaozao.17 | 1.794 | 0.957 | 40.505 | 1.005 | 1.001 |
| jiaomaozao.18 | 0.943 | 0.844 | 46.760 | 1.013 | 1.008 |
| jiaomaozao.19 | 1.283 | 0.949 | 43.997 | 1.002 | 1.001 |
| jiaomaozao.26 | 1.582 | 0.967 | 41.649 | 1.001 | 1.000 |
| jiaomaozao.27 | 0.949 | 0.959 | 47.488 | 1.007 | 1.001 |
| jiaomaozao.28 | 1.235 | 0.889 | 44.667 | 1.000 | 1.001 |
| jiaomaozao.29 | 10.986 | 0.986 | 26.677 | 1.000 | 1.001 |
| juciqigou.3 | 3.799 | 0.963 | 34.900 | 1.001 | 1.000 |
| kailun.2 | 9.219 | 0.958 | 26.910 | 1.001 | 1.000 |
| lianzhuang.4 | 9.322 | 0.879 | 27.722 | 0.992 | 0.995 |
| lianzhuang.5 | 8.344 | 0.931 | 28.554 | 0.995 | 0.996 |
| lianzhuang.6 | 8.570 | 0.875 | 28.300 | 0.997 | 0.995 |
| lianzhuangluojia.10 | 3.034 | 0.984 | 34.590 | 1.043 | 0.994 |
| lianzhuangluojia.11 | 7.831 | 0.980 | 29.443 | 1.005 | 1.000 |
| lianzhuangluojia.12 | 10.236 | 0.977 | 26.453 | 0.999 | 1.000 |
| lianzhuangluojia.13 | 4.522 | 0.941 | 34.605 | 1.004 | 1.001 |
| lianzhuangluojia.14 | 4.368 | 0.950 | 34.867 | 1.002 | 1.000 |
| lianzhuangluojia.8 | 18.079 | 0.997 | 21.494 | 1.000 | 1.000 |
| lianzhuangluojia.9 | 3.148 | 0.441 | 34.088 | 0.958 | 0.985 |
| limayuanjia.10 | 19.602 | 0.990 | 21.005 | 1.000 | 1.000 |
| limayuanjia.11 | 17.590 | 0.990 | 21.475 | 1.000 | 1.000 |
| limayuanjia.12 | 20.099 | 0.991 | 20.615 | 1.000 | 1.000 |
| limayuanjia.13 | 19.615 | 0.986 | 21.082 | 0.999 | 1.000 |
| limayuanjia.14 | 9.697 | 0.968 | 27.377 | 1.001 | 0.991 |
| limayuanjia.15 | 10.776 | 0.960 | 26.412 | 1.003 | 0.999 |
| limayuanjia.16 | 17.310 | 0.961 | 22.354 | 0.999 | 0.996 |
| limayuanjia.18 | 11.710 | 0.868 | 25.661 | 1.003 | 0.994 |
| limayuanjia.9 | 17.716 | 0.992 | 21.601 | 1.000 | 1.000 |
| lingxinghaixian.5 | 13.771 | 0.063 | 25.002 | 0.989 | 0.997 |
| lingxinghaixian.6 | 13.579 | 0.005 | 23.778 | 1.000 | 0.999 |
| luojiazao.4 | 2.663 | 0.821 | 36.703 | 1.000 | 0.986 |
| luojiazao.5 | 2.966 | 0.936 | 36.582 | 1.014 | 0.996 |
| luojiazao.6 | 3.094 | 0.612 | 34.644 | 1.003 | 0.990 |
| luoshijiaomao.3 | 6.228 | 0.976 | 30.680 | 1.001 | 1.000 |
| luoshijiaomao.4 | 5.372 | 0.989 | 30.636 | 0.999 | 0.999 |
| mashi.2 | 9.157 | 0.964 | 26.742 | 1.000 | 1.000 |
| mishikailun.8 | 3.422 | 0.827 | 35.048 | 0.998 | 0.998 |
| nilingxing.3 | 2.768 | 0.465 | 37.639 | 1.027 | 1.027 |
| nilingxing.4 | 4.188 | 0.989 | 34.760 | 1.000 | 1.001 |
| paige.4 | 1.073 | 0.933 | 45.856 | 1.017 | 1.002 |
| paige.5 | 13.175 | 0.004 | 25.252 | 1.001 | 0.999 |
| qiangzhuang.12 | 15.391 | 0.997 | 21.575 | 1.002 | 1.000 |
| qiangzhuang.13 | 15.605 | 0.995 | 21.541 | 1.003 | 1.000 |
| qiangzhuang.14 | 15.649 | 0.996 | 21.551 | 1.003 | 1.000 |
| qiangzhuang.15 | 15.444 | 0.993 | 21.577 | 1.004 | 1.000 |
| qiangzhuang.16 | 16.400 | 0.995 | 21.409 | 1.002 | 1.000 |
| qiangzhuang.17 | 24.178 | 0.996 | 19.326 | 1.002 | 1.000 |
| qiangzhuang.18 | 13.375 | 1.007 | 21.862 | 0.999 | 1.008 |
| qiangzhuang.19 | 12.198 | 0.695 | 22.498 | 1.037 | 1.018 |
| qiangzhuang.20 | 12.103 | 0.655 | 22.499 | 1.009 | 1.012 |
| qiangzhuang.21 | 12.171 | 0.733 | 22.502 | 0.967 | 1.005 |
| qiangzhuang.22 | 12.167 | 0.718 | 22.501 | 0.969 | 1.004 |
| qiangzhuang.25 | 12.189 | 0.751 | 22.510 | 0.992 | 1.005 |
| qiangzhuang.26 | 12.184 | 0.749 | 22.510 | 0.978 | 1.005 |
| qiangzhuang.28 | 12.220 | 0.688 | 22.501 | 1.012 | 1.011 |
| qiuxing.3 | 2.692 | 0.953 | 37.505 | 0.987 | 0.997 |
| qiuxing.4 | 12.406 | 0.958 | 25.168 | 1.010 | 1.001 |
| redai.3 | 8.963 | 0.944 | 28.004 | 1.001 | 1.001 |
| redai.4 | 10.412 | 0.974 | 26.204 | 1.004 | 1.001 |
| ribenxing.3 | 3.785 | 0.978 | 33.865 | 1.000 | 1.000 |
| ribenxing.4 | 9.892 | 0.944 | 27.327 | 1.022 | 1.003 |
| rouruo.3 | 0.974 | 0.962 | 46.653 | 1.010 | 1.004 |
| rouruo.4 | 8.819 | 0.968 | 28.106 | 0.999 | 0.999 |
| sanjiaoji.10 | 8.723 | 0.927 | 27.413 | 1.001 | 1.000 |
| sanjiaoji.9 | 8.603 | 0.919 | 27.545 | 1.001 | 1.000 |
| shikelipu.4 | 8.756 | 1.505 | 28.486 | 1.018 | 0.978 |
| shikelipu.5 | 10.206 | 0.960 | 26.379 | 1.002 | 1.001 |
| suojiao.6 | 12.999 | 0.374 | 23.534 | 1.031 | 1.033 |
| tama.10 | 31.381 | 0.997 | 16.517 | 1.001 | 1.000 |
| tama.11 | 7.782 | 0.927 | 28.564 | 1.146 | 1.005 |
| tama.12 | 31.240 | 0.998 | 16.441 | 1.000 | 1.000 |
| tama.13 | 4.738 | 0.994 | 32.480 | 1.008 | 0.997 |
| tama.14 | 7.769 | 0.925 | 28.574 | 1.153 | 1.005 |
| tama.16 | 1.123 | 0.938 | 45.895 | 1.051 | 1.000 |
| tama.8 | 31.424 | 0.997 | 16.496 | 1.001 | 1.000 |
| tama.9 | 7.770 | 0.943 | 28.575 | 1.088 | 1.004 |
| tiaowenhuangou.4 | 16.798 | 0.958 | 22.500 | 1.001 | 0.996 |
| tiaowenhuangou.5 | 16.785 | 0.952 | 22.510 | 1.001 | 0.996 |
| tiaowenhuangou.6 | 7.078 | 0.907 | 30.064 | 1.004 | 0.991 |
| weiruan.7 | 11.518 | 0.954 | 26.004 | 1.001 | 1.000 |
| weiruan.8 | 12.744 | 0.967 | 25.116 | 0.998 | 1.000 |
| weixiaoyuanjia.13 | 12.250 | 0.990 | 22.675 | 1.000 | 0.999 |
| weixiaoyuanjia.14 | 12.729 | 0.995 | 22.653 | 1.001 | 0.999 |
| weixiaoyuanjia.15 | 12.383 | 0.979 | 22.629 | 0.992 | 0.999 |
| weixiaoyuanjia.16 | 12.818 | 0.992 | 22.604 | 0.998 | 0.999 |
| weixiaoyuanjia.17 | 12.757 | 0.988 | 22.604 | 0.999 | 0.999 |
| weixiaoyuanjia.18 | 12.763 | 0.982 | 22.625 | 0.993 | 0.999 |
| weixiaoyuanjia.19 | 12.949 | 0.995 | 22.544 | 1.000 | 0.999 |
| weixiaoyuanjia.20 | 12.449 | 0.978 | 22.631 | 0.994 | 0.999 |
| weixiaoyuanjia.21 | 30.629 | 0.788 | 16.602 | 0.973 | 0.986 |
| weixiaoyuanjia.22 | 30.250 | 0.871 | 16.665 | 0.951 | 0.965 |
| weixiaoyuanjia.23 | 30.225 | 0.998 | 16.538 | 0.999 | 1.000 |
| weixiaoyuanjia.24 | 30.607 | 0.999 | 16.505 | 1.000 | 1.000 |
| weixiaoyuanjia.26 | 31.013 | 0.997 | 16.435 | 0.997 | 0.999 |
| weixiaoyuanjia.28 | 12.737 | 0.992 | 22.618 | 0.999 | 0.999 |
| xinyue.4 | 12.775 | 0.990 | 22.601 | 0.991 | 0.999 |
| xinyue.5 | 11.512 | 0.954 | 25.951 | 1.000 | 1.000 |
| xinyue.6 | 12.844 | 0.999 | 22.761 | 1.001 | 0.999 |
| xuanlianjiaomao.3 | 0.889 | 0.811 | 47.736 | 1.012 | 1.002 |
| xuanlianjiaomao.4 | 0.863 | 0.753 | 48.038 | 1.009 | 1.003 |
| xuehong.10 | 7.102 | 0.946 | 29.220 | 1.006 | 1.001 |
| xuehong.11 | 7.731 | 0.963 | 28.273 | 1.005 | 1.000 |
| xuehong.12 | 7.750 | 0.956 | 28.247 | 1.006 | 1.000 |
| xuehong.13 | 7.726 | 0.956 | 28.288 | 1.003 | 1.001 |
| xuehong.14 | 7.774 | 0.950 | 28.228 | 1.006 | 1.001 |
| xuehong.16 | 14.624 | 0.980 | 21.749 | 1.000 | 1.000 |
| xuehong.8 | 5.694 | 0.964 | 31.375 | 1.001 | 1.000 |
| xuehong.9 | 7.731 | 0.962 | 28.271 | 1.004 | 1.000 |
| yuanhai.6 | 13.260 | 0.994 | 22.520 | 1.000 | 0.999 |
| yuanhai.7 | 13.354 | 0.995 | 22.471 | 0.999 | 0.999 |
| yuanhai.8 | 13.103 | 0.996 | 22.559 | 1.001 | 0.999 |
| yuanjiazao.6 | 4.973 | 0.879 | 31.591 | 1.003 | 0.991 |
| yuanjiazao.8 | 8.320 | 0.975 | 27.532 | 1.001 | 1.000 |

Mean metrics:

- mean_abs_bgr_delta: `11.6000`
- mean_abs_luma_delta: `0.8939`
- mean_abs_chroma_delta: `7.9657`
- psnr_vs_raw: `27.5919`
- grad_mean_ratio: `1.0037`
- luma_std_ratio: `1.0000`

## Stage Metrics CSV

- `topology_locked_visual_chroma_full_flow_v1_myedge168_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chazhuang.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chazhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chazhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chichaoyiwan.1_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chichaoyiwan.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chichaoyiwan.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chichaoyiwan.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chichaoyiwan.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chichaoyiwan.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chichaoyiwan.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\chichaoyiwan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\donghaiyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\duolie.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\duolie.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\duolie.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\duolie.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\duowenqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\duowenqigou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\fanquyuanjia.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\fanquyuanjia.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\gutiao.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\hailianzao.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\hailianzao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\hailianzao.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\hailianzao.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangkadun.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangyuanjia.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangyuanjia.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\haiyangyuanjia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jianci.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jianci.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jianci.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.27_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\jiaomaozao.29_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\juciqigou.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\kailun.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuang.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuang.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuang.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuangluojia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuangluojia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuangluojia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuangluojia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuangluojia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuangluojia.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lianzhuangluojia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\limayuanjia.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lingxinghaixian.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\lingxinghaixian.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\luojiazao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\luojiazao.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\luojiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\luoshijiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\luoshijiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\mashi.2_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\mishikailun.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\nilingxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\nilingxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\paige.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\paige.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.25_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiangzhuang.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiuxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\qiuxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\redai.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\redai.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\ribenxing.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\ribenxing.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\rouruo.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\rouruo.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\sanjiaoji.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\sanjiaoji.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\shikelipu.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\shikelipu.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\suojiao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tama.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tama.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tama.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tama.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tama.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tama.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tama.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tama.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tiaowenhuangou.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tiaowenhuangou.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\tiaowenhuangou.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weiruan.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weiruan.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.15_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.17_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.18_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.19_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.20_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.21_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.22_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.23_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.24_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.26_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\weixiaoyuanjia.28_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xinyue.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xinyue.5_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xinyue.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuanlianjiaomao.3_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuanlianjiaomao.4_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuehong.10_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuehong.11_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuehong.12_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuehong.13_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuehong.14_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuehong.16_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuehong.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\xuehong.9_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\yuanhai.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\yuanhai.7_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\yuanhai.8_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\yuanjiazao.6_panel.jpg`
- `experiments\topology_locked_visual_chroma_full_flow_v1\diagnostics\myedge168_v1\yuanjiazao.8_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
