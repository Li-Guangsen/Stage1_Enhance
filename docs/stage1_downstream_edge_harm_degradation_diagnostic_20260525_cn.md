# Stage1 下游边缘负向与退化场景诊断（只读）

生成日期：2026-05-25

## 结论边界

- 本报告只读汇总已经落盘的 Stage1 / MyEdge 结果文件。
- 未运行 Stage1 增强、MyEdge sampling、WSL `eval.py`、WSL `show.py`、训练或指标重算。
- 退化场景来自 MyEdge 侧 `auto_proxy_quantile_20260525` 自动候选标签，当前仍是 `pending_manual_review`；它可以用于定位和排队人工复核，不能写成最终人工退化分层结论。
- P6/P7 结构 proxy 不是 ODS/OIS/AP/AC 的替代，只用于解释边界连续性、伪边、断裂和定位误差方向。

## 证据入口

- Stage1 stage/metric delta: `docs/stage1_downstream_edge_metric_deltas_20260525.csv`
- MyEdge degradation candidates: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/degradation_subset_candidates_20260525.csv`
- MyEdge failure candidates: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/degradation_subset_candidates_20260525.failure_cases.csv`
- P6 per-image structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/downstream_variant_structure_p6_metrics_20260525.per_image.csv`
- P7 per-image structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/generic_control_p7_structure_metrics_20260525.per_image.csv`
- 聚合 CSV: `docs/stage1_downstream_edge_harm_degradation_proxy_deltas_20260525.csv`

## 1. 阶段与指标：旧 Stage1 增强在哪里伤害下游

下表来自 Stage1 侧 `stage1_downstream_edge_metric_deltas_20260525.csv`，比较各阶段相对 Raw anchor 的 ODS/OIS/AP/AC delta。

| Detector | Stage | status | lowered metrics | delta ODS | delta OIS | delta AP | delta AC |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| DiffusionEdge baseline 50k | BPH | all_metrics_lower | 4 | -0.057602 | -0.057554 | -0.024519 | -0.002700 |
| DiffusionEdge baseline 50k | IMF1Ray | all_metrics_lower | 4 | -0.083358 | -0.057610 | -0.007664 | -0.055200 |
| DiffusionEdge baseline 50k | RGHS | all_metrics_lower | 4 | -0.158287 | -0.126236 | -0.076658 | -0.045000 |
| DiffusionEdge baseline 50k | CLAHE | all_metrics_lower | 4 | -0.186068 | -0.114773 | -0.097130 | -0.043500 |
| DiffusionEdge baseline 50k | Fused | all_metrics_lower | 4 | -0.141426 | -0.090194 | -0.060454 | -0.043000 |
| DiffusionEdge baseline 50k | Final | all_metrics_lower | 4 | -0.240427 | -0.212076 | -0.138992 | -0.062000 |
| MSFI 50k | BPH | all_metrics_lower | 4 | -0.044290 | -0.041806 | -0.035289 | -0.002646 |
| MSFI 50k | IMF1Ray | mostly_lower | 3 | -0.051780 | -0.040181 | 0.005027 | -0.039546 |
| MSFI 50k | RGHS | all_metrics_lower | 4 | -0.111807 | -0.070284 | -0.049157 | -0.034946 |
| MSFI 50k | CLAHE | all_metrics_lower | 4 | -0.143621 | -0.073397 | -0.066026 | -0.021846 |
| MSFI 50k | Fused | all_metrics_lower | 4 | -0.113581 | -0.073158 | -0.054729 | -0.028546 |
| MSFI 50k | Final | all_metrics_lower | 4 | -0.195240 | -0.122856 | -0.081902 | -0.056546 |

最明显的负向项：

- `ODS` 最大下降：DiffusionEdge baseline 50k / Final，delta `-0.240427`。
- `OIS` 最大下降：DiffusionEdge baseline 50k / Final，delta `-0.212076`。
- `AP` 最大下降：DiffusionEdge baseline 50k / Final，delta `-0.138992`。
- `AC` 最大下降：DiffusionEdge baseline 50k / Final，delta `-0.062000`。

当前可写结论：旧 Stage1 的后半段增强，尤其 `RGHS -> CLAHE -> Fused -> Final`，在两个固定检测器下都显著拉低 ODS/OIS/AP/AC；`BPH` 和 `IMF1Ray` 损伤较小但也不是稳定正向。MSFI 侧 `IMF1Ray` 的 AP 例外不能抵消 ODS/OIS/AC 的下降。

## 2. 自动退化标签下的结构 proxy 损伤

下表按自动退化候选标签聚合 per-image 结构 proxy delta。`boundary_*` 为 candidate - raw，负值通常更差；`false_edge`、`missed_gt`、`components`、`endpoints`、`p95 distance` 为正值通常更差。多标签样本会计入多个标签，因此 count 是 multilabel count。

| Comparison | Tag | n | delta F1 | delta precision | delta recall | delta false-edge | delta endpoints/kpx | delta p95 pred-GT dist |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| legacy_final_vs_raw_msfi | low_contrast_boundary | 42 | -0.263324 | -0.319551 | -0.068732 | 0.319551 | 118.236795 | 84.920756 |
| legacy_final_vs_raw_msfi | blurred_contour | 42 | -0.415835 | -0.540822 | -0.066611 | 0.540822 | 130.808726 | 120.101831 |
| legacy_final_vs_raw_msfi | false_edge_background | 42 | -0.060919 | -0.069396 | -0.107960 | 0.069396 | 59.703645 | 37.016169 |
| legacy_final_vs_raw_msfi | thin_structure | 42 | -0.149314 | -0.172870 | -0.125719 | 0.172870 | 98.823788 | 52.426741 |
| legacy_final_vs_raw_msfi | overlap_clutter | 49 | -0.124840 | -0.167756 | -0.088694 | 0.167756 | 89.714842 | 49.995883 |
| legacy_final_vs_raw_msfi | unassigned_proxy | 45 | -0.192544 | -0.240714 | -0.078054 | 0.240714 | 79.980030 | 66.694326 |
| legacy_final_vs_raw_baseline | low_contrast_boundary | 42 | -0.320395 | -0.395484 | -0.159483 | 0.395484 | 226.411145 | 96.350600 |
| legacy_final_vs_raw_baseline | blurred_contour | 42 | -0.506474 | -0.647815 | -0.133973 | 0.647815 | 250.637302 | 146.326210 |
| legacy_final_vs_raw_baseline | false_edge_background | 42 | -0.111051 | -0.144580 | -0.130451 | 0.144580 | 201.821717 | 33.575770 |
| legacy_final_vs_raw_baseline | thin_structure | 42 | -0.197146 | -0.243976 | -0.165038 | 0.243976 | 224.709310 | 58.185322 |
| legacy_final_vs_raw_baseline | overlap_clutter | 49 | -0.189814 | -0.264850 | -0.115011 | 0.264850 | 219.772904 | 69.668343 |
| legacy_final_vs_raw_baseline | unassigned_proxy | 45 | -0.327783 | -0.446757 | -0.141385 | 0.446757 | 232.137165 | 102.252773 |

当前可写结论：在自动候选标签下，legacy Stage1 Final 的损伤不是只发生在某一个孤立样本；低对比边界、模糊轮廓、背景伪边、细结构和重叠/杂质类候选中均出现 F1/precision 下降和 false-edge/endpoints 增加。该结论仍需人工冻结退化标签后才能升级为正式 per-stratum 结果。

## 3. Top failure candidate 的标签集中情况

下面只统计每类 top-20 failure/success candidate 的自动标签，帮助决定人工复核优先级。

| Category | rows | mean delta F1 | mean delta precision | mean delta false-edge | top tags | top stems |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| legacy_final_damage_baseline | 20 | -0.564554 | -0.689224 | 0.689224 | blurred_contour:12, low_contrast_boundary:7, unassigned_proxy:6, thin_structure:2 | tama.11, qiangzhuang.16, qiangzhuang.14, qiangzhuang.19, lianzhuangluojia.10 |
| legacy_final_damage_msfi | 20 | -0.669890 | -0.768375 | 0.768375 | blurred_contour:13, low_contrast_boundary:7, unassigned_proxy:5, overlap_clutter:3 | weixiaoyuanjia.21, tama.9, weixiaoyuanjia.22, donghaiyuanjia.26, tama.14 |
| p4_moderate_failure_msfi | 20 | -0.012415 | -0.009739 | 0.009739 | overlap_clutter:8, false_edge_background:7, low_contrast_boundary:6, thin_structure:6 | lingxinghaixian.5, hailianzao.8, haiyangkadun.13, lianzhuangluojia.13, shikelipu.4 |
| p4_moderate_success_msfi | 20 | 0.017041 | 0.026955 | -0.026955 | unassigned_proxy:9, false_edge_background:5, thin_structure:5, overlap_clutter:4 | shikelipu.5, duowenqigou.4, mishikailun.8, xuanlianjiaomao.4, qiangzhuang.12 |
| p5c_mild_failure_baseline | 20 | -0.021121 | -0.037399 | 0.037399 | false_edge_background:7, unassigned_proxy:6, low_contrast_boundary:5, thin_structure:5 | chazhuang.6, qiangzhuang.17, gutiao.2, limayuanjia.18, weixiaoyuanjia.21 |
| p5c_mild_success_baseline | 20 | 0.016404 | 0.011367 | -0.011367 | low_contrast_boundary:10, blurred_contour:8, thin_structure:6, overlap_clutter:6 | qiangzhuang.19, kailun.2, qiangzhuang.28, rouruo.3, sanjiaoji.10 |
| p7_gamma_failure_baseline | 20 | -0.017650 | -0.030202 | 0.030202 | unassigned_proxy:6, false_edge_background:5, overlap_clutter:5, blurred_contour:5 | chazhuang.6, duowenqigou.4, limayuanjia.18, qiangzhuang.17, haiyangkadun.13 |
| p7_gamma_failure_msfi | 20 | -0.010281 | -0.009563 | 0.009563 | false_edge_background:8, thin_structure:6, low_contrast_boundary:6, blurred_contour:5 | hailianzao.8, haiyangkadun.13, lingxinghaixian.5, chazhuang.6, shikelipu.4 |
| p7_gamma_success_baseline | 20 | 0.014486 | 0.012671 | -0.012671 | blurred_contour:8, low_contrast_boundary:7, thin_structure:5, unassigned_proxy:3 | kailun.2, qiangzhuang.28, sanjiaoji.10, duowenqigou.3, xuehong.12 |
| p7_gamma_success_msfi | 20 | 0.012076 | 0.019481 | -0.019481 | false_edge_background:7, thin_structure:6, overlap_clutter:5, low_contrast_boundary:5 | duowenqigou.4, donghaiyuanjia.15, qiangzhuang.28, limayuanjia.11, shikelipu.5 |

## 4. 对下一版 Stage1 boundary-aware 实现的约束

基于当前只读诊断，下一版 Stage1 不能再追求通用增强强度，而应把 hard guardrail 改成下游边界结构：

- 不再以 `Final` 的强对比、强梯度、强无参考视觉指标作为优先目标。
- 优先保留 Raw 的边界分布，只允许 mild luminance adjustment 和受控 chroma transfer。
- 对低对比/模糊边界样本，目标是提升 recall 但不能牺牲 precision 到产生大量伪边。
- 对背景伪边/细结构样本，目标是降低 false-edge 和 endpoint fragmentation，而不是简单增强高频。
- 成功门槛不能是“接近 Raw”，而应至少在 fixed MSFI 与 DiffusionEdge baseline 中同时出现 ODS/OIS/AC 或结构 proxy 的稳定正向信号；P9 仍需 sampling/eval/show 后才能判断。

## 5. 仍缺

- 人工冻结退化标签；当前标签只是自动 proxy。
- P8 repeat/control 与 P9 `edge_safe_gamma_bph_v1` 的 fixed-detector sampling/eval/show 和结果同步。
- 真正连续 PR 曲线、阈值校准、MSFI 组件消融/替换、效率和人工确认的失败案例图组。
- 在 P9 或后续候选没有稳定超过 Raw 前，不进入 2770 full-pool。
