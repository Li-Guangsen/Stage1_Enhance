# full_flow_downstream_stage1_mainline_v1 smoke25_fast_imf_v8 status

Date: 2026-05-27

## Summary

- Status: `complete_smoke25_fast_imf_v8_review_pending`
- Manifest: `experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke25_v1.txt`
- Output root: `experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke25_v1_fast_imf_v8`
- Expected images: `25`
- Observed runtime: `11.6` sec total, `0.46` sec/image
- Projected 168 runtime: `1.3` min
- Decision: `inspect_worst_panels_before_168_gate`

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
| chazhuang.1 | 6.023 | 1.035 | 29.689 | 1.004 | 1.002 |
| chichaoyiwan.17 | 12.541 | 1.079 | 24.719 | 1.051 | 1.149 |
| donghaiyuanjia.13 | 9.976 | 1.719 | 26.177 | 1.094 | 1.089 |
| donghaiyuanjia.4 | 8.211 | 1.973 | 26.576 | 1.041 | 1.118 |
| duolie.2 | 1.201 | 0.921 | 43.121 | 1.023 | 1.009 |
| hailianzao.10 | 4.200 | 0.894 | 33.726 | 1.007 | 0.998 |
| haiyangkadun.18 | 3.034 | 1.083 | 37.659 | 1.038 | 1.029 |
| haiyangyuanjia.4 | 3.025 | 0.540 | 31.432 | 0.992 | 0.993 |
| jiaomaozao.16 | 1.657 | 0.960 | 41.096 | 1.022 | 1.020 |
| jiaomaozao.7 | 0.990 | 0.924 | 46.290 | 1.028 | 1.034 |
| lianzhuangluojia.11 | 5.749 | 1.096 | 32.199 | 1.046 | 1.054 |
| limayuanjia.16 | 13.181 | 1.847 | 24.929 | 1.040 | 1.014 |
| lingxinghaixian.5 | 11.613 | 0.138 | 26.543 | 1.077 | 1.095 |
| mishikailun.10 | 12.129 | 0.890 | 24.953 | 1.024 | 1.062 |
| qiangzhuang.1 | 11.959 | 1.177 | 24.545 | 1.009 | 1.016 |
| qiangzhuang.29 | 3.243 | 0.956 | 34.253 | 1.005 | 1.000 |
| ribenxing.2 | 7.866 | 1.204 | 29.383 | 1.041 | 1.077 |
| shikelipu.1 | 7.663 | 1.120 | 29.673 | 1.023 | 1.021 |
| tama.13 | 3.617 | 0.762 | 34.562 | 1.099 | 1.042 |
| tiaowenhuangou.5 | 12.870 | 1.973 | 25.069 | 1.009 | 0.996 |
| weixiaoyuanjia.17 | 8.577 | 1.130 | 26.143 | 1.078 | 1.091 |
| weixiaoyuanjia.5 | 2.663 | 1.053 | 37.362 | 1.034 | 1.025 |
| xuehong.12 | 5.478 | 1.310 | 31.865 | 1.030 | 1.024 |
| yuanhai.13 | 9.051 | 1.252 | 25.990 | 1.068 | 1.111 |
| zhaixi.3 | 9.831 | 0.085 | 27.547 | 1.031 | 1.037 |

Mean metrics:

- mean_abs_bgr_delta: `7.0538`
- mean_abs_luma_delta: `1.0849`
- mean_abs_chroma_delta: `4.8567`
- psnr_vs_raw: `31.0200`
- grad_mean_ratio: `1.0366`
- luma_std_ratio: `1.0443`

## Stage Metrics CSV

- `full_flow_downstream_stage1_mainline_v1_smoke25_fast_imf_v8_stage_metrics_20260527.csv`

## Visual Panels

- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\chazhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\chichaoyiwan.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\donghaiyuanjia.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\donghaiyuanjia.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\duolie.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\hailianzao.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\haiyangkadun.18_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\haiyangyuanjia.4_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\jiaomaozao.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\jiaomaozao.7_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\lianzhuangluojia.11_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\limayuanjia.16_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\lingxinghaixian.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\mishikailun.10_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\qiangzhuang.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\qiangzhuang.29_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\ribenxing.2_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\shikelipu.1_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\tama.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\tiaowenhuangou.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\weixiaoyuanjia.17_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\weixiaoyuanjia.5_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\xuehong.12_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\yuanhai.13_panel.jpg`
- `experiments\full_flow_downstream_stage1_mainline_v1\diagnostics\smoke25_fast_imf_v8\zhaixi.3_panel.jpg`

## Boundary

- This is a smoke run only, not a downstream result.
- It did not run MyEdge sampling, WSL eval/show, 502/496 metrics, or 2770 full-pool.
- The decision only controls whether a broader visual/proxy smoke or 168 fixed-detector validation can be considered.
