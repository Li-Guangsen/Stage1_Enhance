# full_flow_downstream_stage1_mainline_v2 ff02_smoke25_v1 status

Date: 2026-05-27

## Summary

- Status: `complete_broader_smoke_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke25_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v2\outputs\smoke25_v1`
- Expected images: `25`
- Observed runtime: `11.6` sec total, `0.46` sec/image
- Projected 168 runtime: `1.3` min
- Decision: `review_before_168`

## Output Completeness

| Format | Stage | Count |
|---|---|---:|
| jpg | BPH | 25 |
| jpg | IMF1Ray | 25 |
| jpg | RGHS | 25 |
| jpg | CLAHE | 25 |
| jpg | Fused | 25 |
| jpg | Final | 25 |
| png | BPH | 25 |
| png | IMF1Ray | 25 |
| png | RGHS | 25 |
| png | CLAHE | 25 |
| png | Fused | 25 |
| png | Final | 25 |

- Missing files: `0`
- Decode failures: `0`

## Raw-vs-Final Smoke Metrics

| Stem | mean abs BGR delta | mean abs L delta | PSNR vs raw | grad mean ratio | luma std ratio |
|---|---:|---:|---:|---:|---:|
| chazhuang.1 | 6.836 | 1.081 | 28.702 | 0.893 | 0.997 |
| chichaoyiwan.17 | 19.331 | 1.032 | 20.765 | 0.911 | 1.059 |
| donghaiyuanjia.13 | 13.969 | 0.817 | 21.673 | 1.084 | 1.034 |
| donghaiyuanjia.4 | 13.473 | 1.157 | 21.756 | 1.044 | 1.039 |
| duolie.2 | 1.314 | 0.981 | 42.991 | 0.929 | 1.000 |
| hailianzao.10 | 4.995 | 1.168 | 32.474 | 0.877 | 0.985 |
| haiyangkadun.18 | 3.611 | 1.081 | 36.181 | 0.917 | 1.004 |
| haiyangyuanjia.4 | 3.838 | 0.815 | 30.606 | 0.882 | 0.988 |
| jiaomaozao.16 | 1.972 | 1.287 | 39.689 | 0.843 | 0.964 |
| jiaomaozao.7 | 1.167 | 1.024 | 44.692 | 0.892 | 0.985 |
| lianzhuangluojia.11 | 7.033 | 1.069 | 30.464 | 1.042 | 1.011 |
| limayuanjia.16 | 15.930 | 1.208 | 23.138 | 0.901 | 0.996 |
| lingxinghaixian.5 | 13.310 | 0.141 | 25.333 | 1.037 | 1.035 |
| mishikailun.10 | 13.220 | 0.650 | 24.226 | 0.803 | 1.010 |
| qiangzhuang.1 | 19.182 | 1.001 | 20.311 | 0.937 | 1.003 |
| qiangzhuang.29 | 3.559 | 0.890 | 33.861 | 0.932 | 0.996 |
| ribenxing.2 | 9.566 | 1.161 | 27.647 | 0.930 | 1.009 |
| shikelipu.1 | 9.158 | 1.118 | 28.099 | 0.891 | 1.002 |
| tama.13 | 4.565 | 0.844 | 32.528 | 0.987 | 0.994 |
| tiaowenhuangou.5 | 15.218 | 1.417 | 23.427 | 0.826 | 0.967 |
| weixiaoyuanjia.17 | 13.720 | 1.165 | 22.221 | 0.961 | 1.013 |
| weixiaoyuanjia.5 | 3.016 | 1.014 | 36.130 | 0.932 | 1.004 |
| xuehong.12 | 7.094 | 1.192 | 29.389 | 0.866 | 0.997 |
| yuanhai.13 | 14.992 | 1.119 | 21.647 | 1.096 | 1.023 |
| zhaixi.3 | 10.942 | 0.335 | 26.715 | 0.913 | 0.988 |

Mean metrics:

- mean_abs_bgr_delta: `9.2405`
- mean_abs_luma_delta: `0.9906`
- mean_abs_chroma_delta: `6.4325`
- psnr_vs_raw: `28.9867`
- grad_mean_ratio: `0.9331`
- luma_std_ratio: `1.0041`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v2_ff02_smoke25_v1_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\chichaoyiwan.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\donghaiyuanjia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\donghaiyuanjia.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\duolie.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\hailianzao.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\haiyangyuanjia.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\jiaomaozao.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\jiaomaozao.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\lianzhuangluojia.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\limayuanjia.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\lingxinghaixian.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\mishikailun.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\qiangzhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\qiangzhuang.29_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\ribenxing.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\shikelipu.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\tama.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\tiaowenhuangou.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\weixiaoyuanjia.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\weixiaoyuanjia.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\xuehong.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\yuanhai.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v2\diagnostics\ff02_smoke25_v1\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
