# Stage1Codex 与 MyEdgeCodex 长周期收口计划

更新时间：2026-05-25

## 1. 总定位

当前长期目标不是把 Stage1Codex 单独写成“增强 + 边缘检测 pipeline”论文，而是形成两个项目各自收口、再做衔接的证据链：

- `MyEdgeCodex`：作为主论文核心，主创新放在 `MSFI` / spatial-frequency guided latent diffusion / weak-boundary edge detection。
- `Stage1Codex`：作为任务驱动的结构保持增强输入支撑，即 `task-driven structure-preserving input formation`，证明它能为 HAB 显微边界任务提供更稳定的结构输入。

写作上应避免：

- 把整体主线写成简单的“先增强，再检测”。
- 把白平衡、CLAHE、IMF、金字塔融合当作独立主创新硬推。
- 把 Stage1 当前无 GT proxy 结果写成已经完成 ODS/OIS/AP/AC 下游验证。
- 因为 MyEdge 的 ODS/OIS 提升而声称全面 SOTA；AP 下降必须诚实解释。

## 2. 当前状态快照

### Stage1Codex 已完成

- 正式增强主线已锁定：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 正式结果副本已固定：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 正式阶段评测已完成：`full502_clean_v1`，502 张。
- 正式外部主比较已完成：`compare9_complete496_v1`，496 张 complete-case。
- Stage1 无 GT 边缘结构代理支撑包已生成：
  - `metrics/outputs/downstream_edge_validation/official_full502_mainline`
  - 该支撑包用于结构保持和选图，不替代 MyEdge 带 GT 评测。
- 完整增强图像池已发现并完成第一轮 manifest 审计：
  - 源目录：`D:\Desktop\去水印所有藻类图像`
  - 图像总数：2777
  - 默认候选 manifest：2774
  - OpenCV 可读候选 manifest：2770
  - 严格重复候选：3 组 / 6 张；近重复候选：30 对
  - 质量异常人工复核候选：507 张
  - 人工复核入口：544 条 pending review issues
  - 人工复核校验：`pending_manual_review`，pending 544，invalid 0
  - P0 复核辅助包：7 条机助建议，状态 `recommendations_only_pending_manual_review`
  - P1 复核辅助包：134 条机助建议，状态 `recommendations_only_pending_manual_review`
  - P2 复核辅助包：403 条机助建议，状态 `recommendations_only_pending_manual_review`
  - 人工复核派生状态：`pending_manual_review`，当前未生成 clean manifest
  - 审计文档：`docs/full_enhancement_dataset_inventory_cn.md`
- Stage1 主入口已完成 full-pool I/O 兼容修正：
  - 支持中文路径安全读写。
  - 支持 manifest 中的子目录、空格和 `#`。
  - 支持 `.webp` 输入。
  - 子目录输入输出时保留子目录结构，避免重名覆盖。
- Stage1 full-pool smoke 已完成：
  - `smoke_limit1_locked_final_mainline`：1 张，六阶段 JPG/PNG 输出完整。
  - `smoke_limit10_locked_final_mainline`：10 张，六阶段 JPG/PNG 输出完整。
  - smoke summary：`experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_summary.md`
- Stage1 full-pool 运行预算已完成：
  - 预算文档：`experiments/full-algae-dewatermark-v1/run_budget_estimate.md`
  - 可恢复运行脚本：`experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1`
  - 完整性检查脚本：`metrics/scripts/summarize_stage1_run_outputs.py`
  - 只读接收脚本：`metrics/scripts/intake_stage1_fullpool_run_outputs.py`
  - 当前接收报告：`experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.md`
  - 当前接收状态：`not_started`，2770 张 full run 尚未启动。
  - 预计 2770 张耗时约 `46-60` 小时，六阶段 JPG/PNG 输出约 `3.04 GiB`，建议预留至少 `5 GiB`。
- Stage1 full2770 执行准备包已完成：
  - 准备包文档：`docs/stage1_full2770_execution_readiness_20260525_cn.md`
  - 生成脚本：`metrics/scripts/build_stage1_full2770_execution_readiness_pack.py`
  - 当前状态：`candidate_full2770_ready_after_explicit_approval_clean_protocol_blocked`
  - 候选长跑前置条件 8/8 满足，但 reviewed clean full-pool protocol 仍被 `544` 条人工复核 pending 阻塞。

### MyEdgeCodex 当前已知进展

根据本地 MyEdge 项目状态文档，当前主线是：

- 方法：`MSFI + EMA + slide/non-resize + 50k`
- checkpoint：`checkpoints/algae/model-10.pt`
- 输出：`output_test/MSFI/algae/ema_slide_50k`
- ALGAE test：168 张。
- Stage1 coupling 快照：`docs/stage1_myedge_coupling_status_20260525_cn.md`。
- 当前 168 张 coupling manifest 已对齐 GT 与 Stage1 六阶段，缺失均为 `0`。
- P1 fixed-detector validation 已完成 Stage1 Final -> MSFI 50k 与 Stage1 Final -> DiffusionEdge baseline 50k 两条路线的 staging、sampling、WSL `eval.py` / `show.py`、intake 和 report-asset sync；当前状态为 `complete_with_report_assets`。
- DiffusionEdge baseline 固定检测器 Stage1 stage-wise P2 诊断已完成 BPH、IMF1Ray、RGHS、CLAHE、Fused 与 Final 的 staging、sampling、WSL `eval.py` / `show.py`、intake 和 report-asset sync；当前状态为 `complete_with_report_assets`。
- MSFI 固定检测器 Stage1 stage-wise P3 诊断已完成 BPH、IMF1Ray、RGHS、CLAHE、Fused 与 Final 的 staging、sampling、WSL `eval.py` / `show.py`、intake 和 report-asset sync；当前状态为 `complete_with_report_assets`。
- Downstream-driven edge-preserve P4 诊断已完成 original-control、mild raw-BPH、moderate raw-BPH 三个变体的 staging、MSFI sampling、WSL `eval.py` / `show.py`、intake 和 report-asset sync；当前状态为 `complete_with_report_assets`。
- Downstream-driven edge-preserve P5C baseline-side 诊断已完成 original-control、mild raw-BPH、moderate raw-BPH 三个变体的 DiffusionEdge baseline sampling、WSL `eval.py` / `show.py`、intake 和 report-asset sync；当前状态为 `complete_with_report_assets`。
- Downstream-driven P6 结构/伪边 proxy 诊断已完成；它只读 P4/P5C 现有 MAT 与 GT，不运行训练、采样、`eval.py` 或 `show.py`，当前状态为 `complete`。
- Downstream-driven P6B paired review 已完成；它只读 P6 per-image CSV，做逐图配对、bootstrap CI 和 sign-test，不运行训练、采样、`eval.py` 或 `show.py`，当前状态为 `complete`。
- Generic controls P7 fixed-detector、结构/伪边 proxy 与 paired review 诊断已完成；Stage1 新增 `generic_luma_clahe_mild_v1` 与 `generic_luma_gamma_mild_v1` 两个非 BPH 亮度域对照，已在 MyEdge 168 split 上生成 Final PNG/JPG 各 `168`、decode failures `0`，并在 MyEdge 侧完成固定 MSFI 与 DiffusionEdge baseline 的 sampling、`eval.py`、`show.py`、report-asset sync 和结构 proxy。当前状态为 `complete_with_report_assets`；P7 可写成 168 张 lightweight luminance-only control 诊断，但不能写稳定下游收益。
- 新增 `edge_safe_gamma_bph_v1` 作为 P4/P7 之后的下一轮非正式 edge-safe 候选；它只做 raw 亮度轻量 gamma/contrast 与少量 BPH 色度迁移，跳过 IMF1Ray/RGHS/CLAHE/Fusion/legacy Final。当前已完成 2 张 smoke 与 168 张 MyEdge split Stage1 输出；168 张输出 Final PNG/JPG 各 `168`、非 Final 阶段文件 `0`、Final PNG 解码 `168/168`；这是 Stage1 输入资产 readiness，不是 MyEdge 下游指标结果。
- `edge_safe_gamma_bph_v1` 的 MyEdge P9 fixed-detector 预执行资产已生成；MyEdge 侧已完成 168 张同 stem staging、固定 MSFI 50k 与固定 DiffusionEdge baseline 50k 两个 sampling config、`edge_safe_gamma_bph_p9_preflight_20260525.{md,json}` 和 WSL eval/show `.sh`。当前两条 planned runs 均 `ready_for_sampling_after_confirmation=True`，planned output roots 均不存在；这是 P9 readiness，不是下游结果。
- 新增 `boundary_aware_luma_bph_v1` 作为 P10 非正式 boundary-aware 候选；它只用 raw+BPH，跳过 IMF1Ray/RGHS/CLAHE/Fusion/legacy Final，对 raw Lab 亮度做受限 gamma/contrast、低梯度背景轻微 bilateral smoothing 和高梯度 masked unsharp，并只迁移少量 BPH 色度。当前已完成 2 张 smoke 与 168 张 MyEdge split Stage1 输出；168 张输出 Final PNG/JPG 各 `168`、非 Final 阶段文件 `0`、Final PNG 解码 `168/168`；MyEdge 侧 P10 fixed-detector preflight、result intake 与 structure proxy intake 已生成，两条 planned runs 均 `ready_for_sampling_after_confirmation=True`，planned output roots 均不存在，result intake 状态为 `ready_not_executed`，structure proxy 状态为 `blocked_by_missing_p10_core_results`；这是 P10 readiness，不是下游结果。
- 新增 `skeleton_safe_luma_bph_v1` 作为 P11 非正式 skeleton-safe 候选；它复用 `boundary_aware_luma_bph` 代码路径，但关闭亮度增强和 unsharp，只保留极小 BPH 色度迁移与低梯度平滑。当前已完成 2 张 smoke 与 168 张 MyEdge split Stage1 输出；168 张输出 Final PNG/JPG 各 `168`、非 Final 阶段文件 `0`、Final PNG 解码 `168/168`。MyEdge 侧 fixed-detector P11 已完成 sampling/eval/show、result intake、结构 proxy 与 downstream gate。
- Stage1 侧 MyEdge168 GT edge proxy prescreen 已更新；`metrics/scripts/build_stage1_myedge168_gt_edge_proxy_prescreen.py` 只读 168 张 coupling manifest、raw、GT edge、旧 Final 和 downstream-driven 候选输出，生成 `docs/stage1_myedge168_gt_edge_proxy_prescreen_20260525_cn.md` / `.json` / `.summary.csv` / `.delta_vs_raw.csv` / `.per_image.csv`。当前覆盖 10 个输入版本、1680 行逐图 proxy、失败 0；旧 Final 是 `proxy_negative_or_risky`，P10 `boundary_aware_luma_bph_v1` 是 `proxy_edge_safe_candidate`，P11 `skeleton_safe_luma_bph_v1` 是当前第一项 `proxy_positive_candidate`，dF1 `+0.001075`、dFalse-edge ratio `-0.001783`、dEndpoints/kpx `-1.302699`。该预筛只支持 P11 fixed-detector 优先级，不是 ODS/OIS/AP/AC 证据。
- P4/P5C/P7 repeat-control P8 fixed-detector 诊断已完成；覆盖 `edge_preserve_original_control`、`edge_preserve_raw_bph_mild_v1`、`edge_preserve_raw_bph_moderate_v1`、`generic_luma_clahe_mild_v1`、`generic_luma_gamma_mild_v1` 五个输入变体与 MSFI 50k / DiffusionEdge baseline 50k 两个固定检测器，共 10 条 runs。当前结果接收状态为 `complete_with_report_assets`，结构 proxy 为 `complete`，gate 为 `repeat_stable_but_control_competitive_no_stage1_specific_upgrade`：P8 支持主要 edge-preserve/gamma 信号的 repeat-stable near-raw rescue，但 generic gamma control 竞争力强且 baseline-side structure 仍 mixed，因此不能升级为 Stage1-specific 稳定正向收益。
- Stage1 -> MyEdge 下游负向诊断总表已生成并随 P8 更新：`docs/stage1_downstream_edge_negative_diagnostic_20260525_cn.md`。它只读汇总已完成的 P2/P3/P4/P5C/P7/P8 结果，当前状态为 `negative_diagnostic_locked_p8_completed_control_competitive`；结论是 legacy Stage1 `Final` 在两个固定检测器下均明显降低 ODS/OIS/AP/AC，P8 说明近 raw rescue 具备 repeat 可信度，但 generic gamma control 竞争力强，不能写成 Stage1 特异正向下游收益。
- Stage1 下游边缘负向与退化场景诊断已生成：`docs/stage1_downstream_edge_harm_degradation_diagnostic_20260525_cn.md`。它只读聚合 stage-wise ODS/OIS/AP/AC delta、MyEdge P6/P7 per-image 结构 proxy 与自动退化候选标签，当前状态为 `readonly_harm_degradation_diagnostic_ready_auto_proxy_not_manual_strata`；结论是旧 `Final` 在 DiffusionEdge baseline 侧造成最大 ODS/OIS/AP/AC 下降，并且低对比、模糊、背景伪边、细结构、重叠/杂质自动候选中均出现 F1/precision 下降和 false-edge/endpoints 增加。退化标签仍未人工冻结，不能写成正式 per-stratum 结果。
- MyEdge PR / threshold trade-off 汇总已生成：`D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\pr_threshold_tradeoff_report_20260525.md`。它只读解析既有 `eval_bdry.txt` 与结果 JSON；当前可写结论是 MSFI raw 相比 DiffusionEdge baseline raw 具备 ODS/OIS operating-point gain，但 AP 更低，应解释为 ranking / calibration trade-off，不能写成 all-metric superiority。
- MyEdge PR / threshold operating-point 可视化已生成：`D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\pr_threshold_visual_status_20260525.md`。它输出 operating-point scatter 与 metric-delta profile，但由于现有 `eval_bdry.txt` 只有单行 summary，这些图不能称为连续 PR curve。
- Stage1 / MyEdge failure-case panel 候选包已生成：`D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\failure_case_panels_20260525\failure_case_panel_candidates_20260525.md`。它基于自动 success/failure 候选和既有 raw/GT/NMS/error-map 资产生成 40 个单图 panel 与 10 张 contact sheet，缺失资产 `0`；人工复核前不能写成最终失败案例图组。

当前可写的结果边界：

| 方法 | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| DiffusionEdge baseline 50k | 0.7705 | 0.7800 | 0.3631 | 0.7969 |
| MSFI + EMA + slide/non-resize + 50k | 0.7835 | 0.7942 | 0.3459 | 0.7968 |

当前 DiffusionEdge baseline stage-wise P2 诊断结果：

| 输入阶段 | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| Raw | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| BPH | 0.712919 | 0.722432 | 0.338546 | 0.7942 |
| IMF1Ray | 0.687163 | 0.722376 | 0.355401 | 0.7417 |
| RGHS | 0.612234 | 0.653750 | 0.286407 | 0.7519 |
| CLAHE | 0.584453 | 0.665213 | 0.265935 | 0.7534 |
| Fused | 0.629095 | 0.689792 | 0.302611 | 0.7539 |
| Final | 0.530094 | 0.567910 | 0.224073 | 0.7349 |

当前 MSFI stage-wise P3 诊断结果：

| 输入阶段 | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| Raw | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| BPH | 0.739237 | 0.752407 | 0.310610 | 0.7942 |
| IMF1Ray | 0.731747 | 0.754032 | 0.350926 | 0.7573 |
| RGHS | 0.671720 | 0.723929 | 0.296742 | 0.7619 |
| CLAHE | 0.639906 | 0.720816 | 0.279873 | 0.7750 |
| Fused | 0.669946 | 0.721055 | 0.291170 | 0.7683 |
| Final | 0.588287 | 0.671357 | 0.263997 | 0.7403 |

当前 downstream-driven edge-preserve P4 诊断结果：

| 输入变体 | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| historical raw MSFI anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| edge_preserve_original_control | 0.783082 | 0.794168 | 0.337353 | 0.7972 |
| edge_preserve_raw_bph_mild_v1 | 0.782743 | 0.793599 | 0.345909 | 0.7957 |
| edge_preserve_raw_bph_moderate_v1 | 0.782999 | 0.794527 | 0.345952 | 0.7952 |
| legacy_stage1_final_p1 | 0.588287 | 0.671357 | 0.263997 | 0.7403 |

当前 downstream-driven edge-preserve P5C baseline-side 诊断结果：

| 输入变体 | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| historical raw DiffusionEdge anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| edge_preserve_original_control | 0.771470 | 0.781490 | 0.362827 | 0.7934 |
| edge_preserve_raw_bph_mild_v1 | 0.770699 | 0.782323 | 0.370985 | 0.7941 |
| edge_preserve_raw_bph_moderate_v1 | 0.771168 | 0.782422 | 0.363047 | 0.7940 |
| legacy_stage1_final_p1 | 0.530094 | 0.567910 | 0.224073 | 0.7349 |

当前 downstream-driven P6 结构/伪边 proxy 诊断结果：

| 检测器 / 输入 | F1 proxy | Precision proxy | Recall proxy | False-edge ratio | Components/kpx | Endpoints/kpx |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MSFI raw | 0.8554 | 0.8783 | 0.8507 | 0.1217 | 4.2507 | 9.4521 |
| MSFI moderate P4 | 0.8568 | 0.8851 | 0.8471 | 0.1149 | 3.6899 | 8.0349 |
| MSFI legacy Final | 0.6446 | 0.6114 | 0.7669 | 0.3886 | 63.2304 | 100.3726 |
| DiffusionEdge raw | 0.8491 | 0.8794 | 0.8392 | 0.1206 | 4.6940 | 11.3757 |
| DiffusionEdge mild P5C | 0.8475 | 0.8735 | 0.8416 | 0.1265 | 4.5799 | 11.6185 |
| DiffusionEdge legacy Final | 0.5522 | 0.4840 | 0.7062 | 0.5160 | 140.1426 | 235.1233 |

因此，MyEdge 当前更适合写成：

- MSFI 对 ODS/OIS 有稳定提升。
- AP 下降，说明排序质量或阈值全域表现仍有 trade-off。
- AC 基本持平。
- 不写“全面领先”或“所有指标最优”。
- Stage1 baseline stage-wise 只能写成负向/诊断归因：各阶段均低于 Raw anchor，BPH 最接近 Raw，Final 最低。
- Stage1 MSFI stage-wise 也只能写成负向/诊断归因：所有增强阶段的 ODS/OIS/AC 均低于 Raw anchor，IMF1Ray 的 AP 略高于 Raw，但整体不支持旧 Stage1 增强的正向下游收益。
- Stage1 P4/P5C edge-preserve 只能写成候选诊断：旧 Stage1 Final 明显伤害下游，edge-preserve 变体在 MSFI 与 DiffusionEdge baseline 两个固定检测器下基本恢复到 raw 附近，但尚不能写成稳定优于 raw。
- Stage1 P6 只能写成结构 proxy 诊断：旧 Final 伪边和碎裂明显恶化；P4/MSFI moderate 有 precision、false-edge、fragmentation 和 endpoints 改善信号，但 recall 略低；baseline-side P5C 仍是 mixed signal。
- Stage1 P6B 只能写成 paired proxy 诊断：MSFI P4 moderate 的 precision、false-edge、F1、endpoints 有逐图配对候选信号，但 recall 下降；baseline-side P5C 仍是 mixed signal。
- Stage1 P7/P8 只能写成 lightweight control 与 repeat/control 诊断：两个 generic luminance-only controls 已完成 MyEdge 固定检测器评测、结构/伪边 proxy 与 paired review；P8 repeat/control 已完成 10 条固定检测器 repeat/control runs，并给出 `repeat_stable_but_control_competitive_no_stage1_specific_upgrade`。gamma 在 baseline 侧有小幅正向信号、MSFI 侧基本贴近 raw，P8 中 generic gamma control 竞争力强，baseline/gamma 结构 proxy 仍 mixed，因此不能写成 Stage1 稳定提升下游。
- Stage1 `edge_safe_gamma_bph_v1` 只能写成新候选 readiness：168 张 MyEdge split Stage1 输出已生成并解码通过，MyEdge P9 fixed-detector 预执行资产已准备好；但尚未完成 MyEdge sampling/eval/show 或任何 ODS/OIS/AP/AC 结果。
- Stage1 `boundary_aware_luma_bph_v1` 只能写成新候选 readiness 和 Stage1 侧 image-gradient proxy 候选：168 张 MyEdge split Stage1 输出已生成并解码通过，MyEdge P10 fixed-detector 预执行资产、result intake 和 structure proxy intake 已准备好，当前 `ready_not_executed` / `blocked_by_missing_p10_core_results`；Stage1 侧 GT edge proxy prescreen 显示它是 `proxy_edge_safe_candidate`，但尚未完成 MyEdge sampling/eval/show 或任何 ODS/OIS/AP/AC/检测器结构指标结果。
- Stage1 `skeleton_safe_luma_bph_v1` 可写成 P11 小口径 fixed-detector 候选诊断：168 张 MyEdge split 上，MSFI P11 为 ODS/OIS/AP/AC `0.784173/0.795553/0.346803/0.7947`，DiffusionEdge baseline P11 为 `0.773642/0.782955/0.374479/0.7934`；downstream gate 为 `candidate_rescues_legacy_but_not_near_raw`。它能说明该候选明显救回旧 Final 的大幅损伤，MSFI 侧接近/略优 raw，但 baseline 侧仍有 AC 和 endpoints trade-off，不能写成稳定正向收益。
- Stage1 P8 只能写成 repeat/control 小口径诊断：10 条 planned runs 已完成 sampling/eval/show、结果接收、结构 proxy 和 gate；它支持主要候选的 repeat-stable near-raw rescue，但由于 generic gamma control 竞争力强且 baseline-side structure mixed，不能写成 Stage1-specific 稳定收益证据。

### 跨项目证据缺口 dashboard

- Dashboard：`docs/stage1_myedge_evidence_gap_dashboard_20260525_cn.md`
- 生成脚本：`metrics/scripts/build_stage1_myedge_evidence_gap_dashboard.py`
- 当前总状态：`major_evidence_gaps_remain`
- 状态计数：`complete=6`、`complete_with_report_assets=7`、`pending_manual_review=1`、`missing_blocked_by_manual_review=1`、`not_started=1`、`planned_only=4`、`partial_complete=1`
- 关键结论：
  - Stage1 正式 502/496 口径和无 GT proxy 已完成。
  - Stage1 full-pool 人工复核仍有 `544` 条 pending，clean manifest 未生成，`full2770` 未开始。
  - MyEdge 正式 168 张 MSFI 主结果和主比较表已存在，Stage1 coupling P1 已完成但结果不支持 Stage1 Final 的正向下游增益。
  - DiffusionEdge baseline stage-wise P2 已完成，但各 Stage1 阶段均低于 Raw anchor；该结果只能作为 baseline 单检测器负向阶段归因。
  - MSFI stage-wise P3 已完成，所有增强阶段的 ODS/OIS/AC 均低于 Raw anchor；该结果只能作为 MSFI 单检测器负向阶段归因。
  - Downstream-driven P4/P5C 已完成，edge-preserve 变体在两个固定检测器下接近 raw anchor；P6/P6B 已补结构/伪边 proxy 和 paired review。该结果只能作为 edge-safe 候选和结构诊断，不是稳定正向收益。
  - MyEdge 的 MSFI 组件消融、替换模块、退化子集、效率/PR/失败案例仍主要是 planned-only 合同。
  - Dashboard 本身不是实验结果，不能用它声称 Stage1 已提升 ODS/OIS/AP/AC。

### 下一步执行门禁表

- Gate board：`docs/stage1_myedge_next_gate_board_20260525_cn.md`
- 生成脚本：`metrics/scripts/build_stage1_myedge_next_gate_board.py`
- 当前总状态：`gated_long_cycle_incomplete`
- 门禁数量：`16`
- 当前可安全推进：
  - G04：继续从已有 no-GT proxy 中整理 qualitative / failure 候选，但不能写 ODS/OIS/AP/AC。
  - G05：MyEdge P1 fixed-detector 已完成，可进入结果解释。
  - G05B：DiffusionEdge baseline stage-wise P2 已完成，可进入 baseline 单检测器 stage attribution 解释。
  - G05C：MSFI stage-wise P3 已完成，可进入 MSFI 单检测器 stage attribution 解释。
  - G05D：downstream-driven P4 已完成，可进入 edge-safe 候选解释和 P8 repeat/control 执行。
  - G05E：baseline-side P5C 已完成，可进入第二检测器 edge-safe 候选解释和 P8 repeat/control 执行。
  - G05F：P6 结构/伪边 proxy 与 P6B paired review 已完成，可进入结构诊断解释、generic controls 和 P8 repeat/control 执行。
  - G05G：generic controls P7 fixed-detector、结构/伪边 proxy 与 paired review 诊断已完成，可进入结果解释和 P8 repeat/control 执行，但当前还不能写成稳定正向收益。
  - G10：继续同步中文主稿和证据包中的边界说明。
- 当前硬停止：
  - G01/G02：人工复核仍 `544` pending，不能派生 clean manifest。
  - G03：Stage1 full2770 仍 `not_started`，未授权前不启动。
  - G06-G09：MSFI 消融、替换、退化分层、效率/PR/失败案例没有结果文件前，只能写 planned-only。

### MyEdge P1 执行结果与准备包状态

- Readiness pack：`docs/stage1_myedge_p1_execution_readiness_20260525_cn.md`
- 生成脚本：`metrics/scripts/build_stage1_myedge_p1_execution_readiness_pack.py`
- 当前准备包状态：`superseded_by_completed_p1`
- P1 intake / report sync 状态：`complete_with_report_assets`
- 当前只读结论：
  - 168 行 coupling manifest 存在。
  - Stage1 Final 源缺失 `0`，GT 缺失 `0`，重复目标文件名 `0`。
  - MSFI 50k 与 DiffusionEdge baseline 50k 的 P1 config template 均存在。
  - DiffusionEdge baseline checkpoint 冻结记录存在，记录 size `4176168989` bytes 与 SHA256 `D78FC44ED04CA7495913D5DCF4088FBEDB5344CA7D5232426C68F05F1648507F`。
  - P1 staging root 已有 `168` 张 Stage1 Final 输入。
  - 两个 P1 output roots 均已生成 `168` 个 PNG、`168` 个 MAT、`168` 个 NMS、`168` 个 white、`168` 个 overlay、`168` 个 error_map、manifest、run_report 和日志。
- P1 mat-eval 结果：
  - Stage1 Final -> MSFI 50k：ODS `0.588287`，OIS `0.671357`，AP `0.263997`，AC `0.7403`。
  - Stage1 Final -> DiffusionEdge baseline 50k：ODS `0.530094`，OIS `0.567910`，AP `0.224073`，AC `0.7349`。
- 硬边界：该结果低于 MyEdge raw-anchor 正式结果，只能写成 Stage1 Final fixed-detector 诊断/负向证据；不能写 Stage1 Final 已提升 ODS/OIS/AP/AC。

### Stage1 full2770 执行准备包

- Readiness pack：`docs/stage1_full2770_execution_readiness_20260525_cn.md`
- 生成脚本：`metrics/scripts/build_stage1_full2770_execution_readiness_pack.py`
- 当前总状态：`candidate_full2770_ready_after_explicit_approval_clean_protocol_blocked`
- 前置条件：8/8 satisfied。
- 当前只读结论：
  - `full_algae_dewatermark_v1_cv2_readable_candidate.txt` 存在，raw/unique 均为 `2770`。
  - decode audit 显示候选 `2774` 张中 `2770` 张 OpenCV 可读，4 张 `GIF89a` 内容文件未进入 cv2-readable candidate run。
  - 1 张和 10 张 smoke 已完成，10 张完整性 `all_complete=true`。
  - `run_full_cv2readable2770_locked.ps1` 显式使用 `locked_full506_final_mainline.json` 与 cv2-readable candidate manifest，并默认 `--skip-existing`。
  - planned full2770 output root 当前不存在，intake 状态仍为 `not_started`。
  - 当前磁盘空间满足最低 `5 GiB` 建议。
  - reviewed clean full-pool protocol 仍被 `544` 条人工复核 pending 阻塞，不能把候选长跑写成 clean protocol。
- 硬边界：该准备包不是执行记录，不授权 2770 张长跑；真正执行前必须得到用户明确授权，完成后必须先运行 `intake_stage1_fullpool_run_outputs.py`，并在状态达到 `complete_with_log_and_run_report` 后才能写 full2770 已完成。

### 论文主张证据总账

- Ledger：`docs/stage1_myedge_claim_evidence_ledger_20260525_cn.md`
- JSON：`docs/stage1_myedge_claim_evidence_ledger_20260525_cn.json`
- 生成脚本：`metrics/scripts/build_stage1_myedge_claim_evidence_ledger.py`
- 当前总状态：`claim_boundaries_locked_major_experiment_claims_pending`
- 主张计数：`22`
- 写作状态计数：`allowed_fact=3`、`allowed_with_boundary=14`、`readiness_only=1`、`planned_only_not_claimable=4`
- 当前可写：正式 Stage1 主线、`full502_clean_v1` 阶段表、`compare9_complete496_v1` 主表、MyEdge MSFI mixed metric profile、P1 fixed-detector 诊断、DiffusionEdge baseline stage-wise 诊断、MSFI stage-wise 诊断、Stage1 -> MyEdge 下游负向诊断总表、自动退化标签下的只读负向归因聚合、P4/P5C edge-safe 候选诊断、P6/P6B 结构 proxy 与 paired diagnostic、full2770 readiness、P7 generic controls 168 张 fixed-detector / structure proxy / paired review 诊断、Stage1 侧 MyEdge168 GT edge proxy prescreen、`edge_safe_gamma_bph_v1` 与 `boundary_aware_luma_bph_v1` 168 张 Stage1 输入资产 readiness、P8/P9/P10 fixed-detector readiness、P10 structure proxy blocked status，以及退化/失败案例自动候选和人工复核工作流已生成但待人工冻结。
- 当前可带边界写：两篇 Wu et al. 2026 参考论文的数据描述字段已经由 Zotero 本地缓存核验，但 Stage1 `2777/2774/2770` 与 ESWA `676` 或 EAAI `1026` 子集的文件级 overlap 仍缺。
- 当前不可写成结果：Stage1 已稳定提升 ODS/OIS/AP/AC、P4/P5C/P6/P6B/P7/P11 稳定优于 raw、Stage1 侧 image-gradient proxy 等同于 detector downstream result、`edge_safe_gamma_bph_v1` 或 `boundary_aware_luma_bph_v1` 已有下游收益、P8 repeat/control 已完成、P7 generic controls 或 P11 已有更大口径下游收益、MSFI 组件独立有效、MSFI 优于 Sobel/CIAFF-like/Fourier/attention 替换模块、退化子集鲁棒、人工失败案例图组已完成、效率/PR/失败案例已完成、Stage1 图像池与参考数据集存在精确重合。
- 硬边界：该 ledger 是写作和门禁资产，不运行实验，不产生新指标，不能替代 MyEdge P1、MSFI 消融或 full2770 长跑结果。

### 参考论文数据关系审计

- Audit：`docs/reference_dataset_relation_audit_20260525_cn.md`
- JSON：`docs/reference_dataset_relation_audit_20260525_cn.json`
- 生成脚本：`metrics/scripts/build_reference_dataset_relation_audit.py`
- 当前总状态：`reference_dataset_descriptions_verified_exact_overlap_missing`
- 已核验：ESWA 2026 边缘检测参考使用 `676` 张、`36` 类、`473/203` train/test，包含设备、倍率、明场、LabelMe 和双专家交叉核验描述；EAAI 2026 分割参考使用 `1026` 张和 `8:2` train/validation。
- 当前边界：这些字段可以作为本项目数据说明模板和证据链设计参考；不能声称 Stage1 完整图像池就是上述 676/1026 数据集，也不能继承它们的 split、GT 或标注协议。

### Stage1 / MyEdge 文件级关系审计

- Audit：`docs/stage1_myedge_file_relation_audit_20260525_cn.md`
- JSON：`docs/stage1_myedge_file_relation_audit_20260525_cn.json`
- 生成脚本：`metrics/scripts/build_stage1_myedge_file_relation_audit.py`
- 当前总状态：`stage1_myedge_168_outputs_aligned_raw_bytes_differ_or_unproven`
- 已确认：MyEdge coupling manifest 为 `168` 行，raw、GT、Stage1 六阶段输出均存在；`168/168` 按 stem 属于 `full502_clean_v1`，`166/168` 按 stem 属于 `compare9_complete496_v1`。
- 关键边界：MyEdge raw 与 Stage1 formal original 的 SHA256 相同数为 `0/168`，且与 `full_algae_dewatermark_v1` 的 `2774/2770` manifest 暂无文件名或 stem 直连。因此当前只能写 MyEdge 168 与 Stage1 formal outputs 可按 stem/path 衔接，不能写成同一原图文件、全池精确重合或完整数据同源闭环。

### Stage1 / MyEdge / full-pool 视觉关系审计

- Audit：`docs/stage1_myedge_visual_relation_audit_20260525_cn.md`
- JSON：`docs/stage1_myedge_visual_relation_audit_20260525_cn.json`
- 候选 TSV：`metrics/manifests/stage1_myedge_visual_relation_candidates_20260525.tsv`
- 生成脚本：`metrics/scripts/build_stage1_myedge_visual_relation_audit.py`
- 当前总状态：`visual_candidates_only_not_proven_provenance`
- 已确认：PIL 可读 MyEdge raw `168/168`、Stage1 formal original `502/502`、full-pool `2774/2774`。
- 视觉候选结果：MyEdge raw 与 Stage1 formal original 的 exact/strong 候选为 `123/168`；MyEdge raw -> full-pool top-1 strong 候选为 `8/168`；Stage1 formal 502 -> full-pool top-1 exact/strong 候选为 `40/502`。
- 关键边界：aHash/dHash/RMSE 只能作为人工 provenance 复核入口，不证明同一原图、同一 split、同一 GT、同一采集协议或参考论文数据集 overlap。

### Stage1 / MyEdge provenance 人工复核入口

- 协议：`docs/stage1_myedge_provenance_review_protocol_cn.md`
- 全量模板：`metrics/manifests/stage1_myedge_provenance_review/provenance_review_template.tsv`
- P0/P1 优先队列：`metrics/manifests/stage1_myedge_provenance_review/provenance_priority_review_queue.tsv`
- 入口摘要：`metrics/manifests/stage1_myedge_provenance_review/provenance_review_index_20260525.md`
- 校验状态：`metrics/manifests/stage1_myedge_provenance_review/provenance_review_validation_status_20260525.md`
- 生成脚本：`metrics/scripts/build_stage1_myedge_provenance_review_template.py`
- 校验脚本：`metrics/scripts/validate_stage1_myedge_provenance_review.py`
- 当前总状态：`pending_manual_provenance_review`
- 当前计数：全量 `1510` 行，P0/P1 `208` 行，`reviewer_decision` 已填写 `0` 行，pending `1510` 行，invalid `0` 行，paper-positive `0` 行。
- 关键边界：模板只是人工复核入口。未填写并通过校验前，不能用于论文数据来源、original-id 映射或 split leakage guard 结论。

### Stage1 / MyEdge provenance 派生入口

- 派生脚本：`metrics/scripts/derive_stage1_myedge_provenance_artifacts.py`
- 派生状态：`metrics/manifests/stage1_myedge_provenance_review/derived_provenance_artifacts/provenance_artifacts_status_20260525.md`
- 当前总状态：`pending_manual_provenance_review`
- 当前计数：pending `1510`，reviewed `0`，invalid `0`，positive relations `0`，paper-usable relations `0`，confirmed original IDs `0`，split leakage guard candidates `0`，`can_generate_final_provenance=false`。
- 关键边界：派生机制已经存在，但所有派生关系表当前为空；不能写成 provenance 已确认。

## 3. 长周期目标

形成一套可投稿前验收的双项目证据包：

1. Stage1 完成完整图像池的数据审计、增强协议和结构保持证据。
2. MyEdge 完成 MSFI 核心消融、替换对比、效率、失败案例和定性图组。
3. Stage1 与 MyEdge 通过固定 detector / 带 GT edge metrics 完成任务驱动增强证据闭环。
4. 中文主稿、证据包、图表计划、数据说明、实验协议和 research-log 全部同步，不依赖聊天历史。

## 4. 阶段计划

### Phase A：数据口径收口

目标：把“我们真实拥有的增强图像池”从聊天事实变成仓库事实。

已完成：

- 生成 `full_algae_dewatermark_v1` manifest 与审计资产。
- 明确 2777 图像总数、2774 默认候选、80 个顶层文件夹、根目录 3 张说明图。
- 记录重名 stem 风险。
- 完成 OpenCV decode / dimension / channel / dtype 审计：默认候选 2774 张中 2770 张可读，4 张伪 `.jpg` 实际为 `GIF89a`，需在 full-pool run 前转换或排除。
- 完成内容重复 / 近重复审计：全量 2777 张均可 hash，3 组严格重复、30 对近重复候选；结果只作为人工复核入口。
- 完成质量异常候选审计：全量 2777 张均可统计，2% 分位阈值生成 507 张人工复核候选；结果不作为自动排除依据。
- 完成人工复核 sheets 生成：4 个 decode failures、3 个 strict duplicate groups、30 对 near duplicate pairs、507 个 quality outliers 汇总为 544 条 pending review issues。
- 完成人工复核字段校验脚本和协议文档：当前校验状态为 `pending_manual_review`，544 pending，0 invalid；尚不能派生 clean manifest 或 split leakage guard。
- 完成 P0 复核辅助包：覆盖 4 个 decode failures 和 3 个 exact duplicate groups，生成 `p0_review_recommendations.tsv`、`p0_contact_sheet.png` 和摘要；`machine_suggestion` 不是人工决策。
- 完成 P1 复核辅助包：覆盖 9 条近重复强候选和 125 条质量异常关键候选，生成 `p1_review_recommendations.tsv`、近重复 contact sheet 和 4 张质量异常 contact sheet；`machine_suggestion` 不是人工决策。
- 完成 P2 复核辅助包：覆盖 21 条近重复候选和 382 条质量异常候选，生成 `p2_review_recommendations.tsv`、近重复 contact sheet、10 张质量异常 contact sheet 和 403 张逐项预览图；`machine_suggestion` 不是人工决策。
- 完成统一人工复核 dashboard：将 P0/P1/P2 机助建议整合为 `all_priority_review_queue.tsv` 共 544 行，并生成 `manual_review_dashboard_20260525.md`；统一队列只是人工复核入口，不是清洗结果。
- 完成人工决策模板和 dry-run 回写入口：生成 `manual_review_decision_template.tsv` 共 544 行；`apply_fullpool_manual_review_decisions.py` 当前 dry-run 状态为 `no_decisions_to_apply`，未写回任何 review sheet。
- 完成人工复核派生脚本和当前状态报告：`derive_fullpool_review_artifacts.py` 当前输出 `pending_manual_review`，不会生成 reviewed clean manifest。
- 完成 `main.py` full-pool I/O 兼容修正和静态验证：`full502_clean_v1` 仍为 502 张，OpenCV 可读候选 manifest 解析为 2770 张，首张中文路径图像可被新读图函数读取。
- 完成 Stage1 full-pool 1 张和 10 张 smoke：使用锁定配置、OpenCV 可读 manifest 和外部中文源目录；10 张 smoke 覆盖 4 通道输入、空格/括号文件名和嵌套输出路径。
- 完成 2770 张 full run 预算、可恢复运行入口、日志路径和只读接收入口；10 张 smoke 已用完整性检查脚本验证 `all_complete=true`，当前 full2770 接收状态为 `not_started`。
- 完成两篇 Wu et al. 2026 参考论文与 Stage1 完整图像池关系审计：参考论文数据描述字段已由 Zotero 本地缓存核验，当前 exact overlap 仍缺。
- 完成 Stage1 / MyEdge 文件级关系审计：MyEdge 168 行 raw/GT/Stage1 六阶段输出均存在，`168/168` 按 stem 属于 `full502_clean_v1`，`166/168` 按 stem 属于 `compare9_complete496_v1`；但 MyEdge raw 与 Stage1 formal original 的 SHA256 相同数为 `0/168`，且与 2774/2770 full-pool manifest 暂无文件名/stem 直连。
- 完成 Stage1 / MyEdge / full-pool 视觉关系审计：MyEdge raw 与 Stage1 formal original 多数存在视觉候选关系，但 full-pool 直连候选较少，只能作为人工 provenance 复核导航。
- 完成 Stage1 / MyEdge provenance 人工复核入口：1510 行模板和 208 行 P0/P1 优先队列已生成，当前全部 pending，尚无 paper-positive provenance 结论。
- 完成 Stage1 / MyEdge provenance 派生入口：状态为 `pending_manual_provenance_review`，当前所有 original-id map、paper-usable relation 和 split guard 派生表均为空。

仍需完成：

- 人工复核严格重复和近重复候选，并形成保留、去重或划分防泄漏规则。
- 先把 P0 机助建议转成人工确认或修正后的 `reviewer_decision`，再运行人工复核校验脚本。
- 继续处理 P1 机助建议，优先把质量异常样本标注为退化子集、失败案例候选或有效难例。
- 继续处理 P2 机助建议，优先把质量异常样本标注为数据覆盖、退化分层、失败案例候选或有效难例，把近重复候选转成 split leakage guard 决策。
- 如果使用统一模板，先填写 `manual_review_decision_template.tsv` 的 `*_to_apply` 字段，dry-run 无 invalid 后再显式 `--apply` 写回 review sheets。
- 明确当前 2777 图像池与两篇参考论文 676/1026 数据子集的文件级关系；当前只能写 `exact_overlap_missing`。
- 明确当前 MyEdge 168、Stage1 502、compare496 和完整 2774/2770 图像池之间的原始文件 provenance；当前只能写 stem/path 对齐，不能写同一原图文件。
- 基于 `stage1_myedge_visual_relation_candidates_20260525.tsv` 建立人工 original-id/provenance 表，确认哪些 full-pool 图像确实对应 Stage1 formal 或 MyEdge 样本。
- 填写 `stage1_myedge_provenance_review` 模板中的 P0/P1 优先队列，先确认 MyEdge raw 与 Stage1 original 的关系，再确认 full-pool strong candidates。
- 复核并校验通过后运行 `derive_stage1_myedge_provenance_artifacts.py`，只在 `can_generate_final_provenance=true` 后更新论文数据说明。
- 补齐论文数据描述所需的显微镜、相机、倍率、采集地点、物种数量、专家标注流程等字段。

产物：

- `docs/full_enhancement_dataset_inventory_cn.md`
- `metrics/manifests/full_algae_dewatermark_v1*.{txt,tsv,json}`
- `metrics/manifests/full_algae_dewatermark_v1_decode_audit.*`
- `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt`
- `metrics/manifests/full_algae_dewatermark_v1_decode_failures.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_duplicate_audit.*`
- `metrics/manifests/full_algae_dewatermark_v1_duplicate_audit_exact_duplicate_groups.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_duplicate_audit_near_duplicate_pairs.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_quality_audit.*`
- `metrics/manifests/full_algae_dewatermark_v1_quality_audit_outliers.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/`
- `docs/full_enhancement_dataset_manual_review_protocol_cn.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_dashboard_20260525.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/all_priority_review_queue.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_template.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_apply_report_20260525.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/derived_review_artifacts/`
- `metrics/scripts/intake_stage1_fullpool_run_outputs.py`
- `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.md`
- `docs/reference_dataset_relation_audit_20260525_cn.md`
- `docs/stage1_myedge_file_relation_audit_20260525_cn.md`
- `docs/stage1_myedge_visual_relation_audit_20260525_cn.md`
- `metrics/manifests/stage1_myedge_visual_relation_candidates_20260525.tsv`
- `docs/stage1_myedge_provenance_review_protocol_cn.md`
- `metrics/manifests/stage1_myedge_provenance_review/`
- `metrics/scripts/derive_stage1_myedge_provenance_artifacts.py`

### Phase B：Stage1 完整图像池增强协议

目标：在不破坏现有 502/496 正式口径的前提下，补齐完整图像池增强输出。

执行门槛：

- 必须处理 decode / dimension 审计暴露的 4 个 `GIF89a` 伪 `.jpg` 文件：要么转换为标准图像，要么使用 OpenCV 可读候选 manifest。
- 1 张和 10 张 smoke 已完成；2770 张完整运行预算已形成，运行前需安排约 46-60 小时窗口并预留至少 5 GiB 磁盘。
- 当前 full2770 接收状态为 `not_started`；长跑完成后必须先运行只读接收脚本，确认日志、六阶段 JPG/PNG 输出和抽样解码，再写入 run report。
- 必须显式使用 `experiments/optimization_v1/configs/locked_full506_final_mainline.json`。
- 输出必须写到新目录，不能覆盖现有正式结果副本。

建议输出：

- `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline`
- 或同等清晰的新目录名。

最低产物：

- 运行配置副本。
- 输入 manifest 副本或引用。
- 每阶段输出完整性报告。
- 失败文件清单。
- protocol-v2 全图池增强指标表。
- 与正式 502/496 的关系说明。
- 说明输出是否保留子目录结构，以及评测脚本如何按相对路径追踪样本。

注意：

- 完整图像池结果可以作为 coverage evidence。
- 在完成独立验收前，不能替代当前正式论文主表。

### Phase C：Stage1 任务驱动结构证据增强

目标：让 Stage1 不只是“视觉增强”，而是能支撑边界结构任务的输入形成模块。

已完成：

- `full502_clean_v1` 阶段级无 GT Sobel/Otsu proxy。
- `compare9_complete496_v1` 外部方法无 GT proxy。

仍需完成：

- 从 proxy 候选图中人工确认 paper-ready qualitative panels。
- 整理失败案例：过增强、伪边缘、断边、弱边界仍不可见、杂质/气泡干扰。
- 如果完整图像池增强完成，再生成完整图像池的结构 proxy，但明确它仍是无 GT 证据。

最低指标：

- 边缘响应密度。
- 连通域数量和面积分布。
- skeleton endpoint / branchpoint。
- 原图与增强图边缘差异。
- 局部放大图和 overlay 图。

### Phase D：MyEdge / MSFI 核心论文证据

目标：证明主创新不是“换个 attention”，而是空间-频域扩散对弱边界的有效建模。

必须补齐：

- MSFI 组件消融：
  - DiffusionEdge baseline。
  - + radial frequency token。
  - + spatial-frequency interaction。
  - + timestep-dependent gating。
  - full MSFI。
- 替换模块对比：
  - Sobel-like prior。
  - CIAFF-like block。
  - CBAM / SE / ECA。
  - ASPP / FPN。
  - simple Fourier filtering。
- AP trade-off 分析：
  - PR curve。
  - 不同阈值下 precision / recall。
  - ODS/OIS 提升与 AP 下降的原因解释。
- 效率分析：
  - Params。
  - FLOPs。
  - FPS / inference time。
  - sampling steps。
  - 显存与训练时间。
- 可解释性与可视化：
  - frequency-band response。
  - timestep gating curve。
  - edge response heatmap。
  - TP/FP/FN overlay。

不建议大改网络。优先补齐消融、替换、可视化和解释。

### Phase E：Stage1 -> MyEdge 固定 detector 下游验证

目标：证明 Stage1 是 task-driven enhancement，不是普通 preprocessing。

推荐协议：

- 输入组：
  - `Original`
  - `BPH`
  - `IMF1Ray`
  - `RGHS`
  - `CLAHE`
  - `Fused`
  - `Final`
  - 外部增强方法（保留 WWPF，HLRP/Histoformer 作为当前协议失败/补充案例）
- detector：
  - 固定 DiffusionEdge baseline。
  - 固定 MyEdge/MSFI。
- 样本：
  - 首先对齐 MyEdge 当前 168 张带 GT test split。
  - 再评估 Stage1 `full502_clean_v1` 中与 GT 可交集的样本。
  - 如果能确认 2777 图像池中哪些有 GT，再规划更大带 GT 子集。

指标：

- ODS / OIS / AP / AC。
- edge thickness。
- boundary F-score。
- fragmentation index。
- background false-edge rate。
- skeleton endpoint count。
- edge-to-GT distance / HD95。

验收标准：

- P1 已回答 `Original -> Stage1 Final` 的第一轮 fixed-detector 问题：当前 Stage1 Final 不支持正向边缘检测增益。
- DiffusionEdge baseline stage-wise P2 已回答 baseline 单检测器下各 Stage1 阶段的第一轮归因问题：Raw anchor 最高，BPH 最接近 Raw，Final 最低。
- MSFI stage-wise P3 已回答 Ours/MSFI 单检测器下旧增强阶段的归因问题：旧 Stage1 增强整体低于 Raw。
- Downstream-driven P4 已回答一个修正方向：保留 raw 亮度/空间结构、只轻量迁移 BPH 色彩/照明，可以基本消除旧 Final 的下游损伤。
- Downstream-driven P5C 已回答第二检测器一致性问题：在固定 DiffusionEdge baseline 50k 下，edge-preserve 变体同样基本消除旧 Final 的下游损伤，说明该方向不是 MSFI-only。
- Downstream-driven P6 已补第一版结构/伪边 proxy，P6B 已补 paired review：旧 Final 显著增加伪边和碎裂，P4/MSFI moderate 有伪边、碎裂和 paired proxy 候选信号但 recall 下降，baseline-side 仍是 mixed signal。
- P8 repeat/control 已完成执行前准备，但仍需真正运行 sampling/eval/show 并同步结果，才能回答改善是否在 repeat/control、退化分层与更正式形态指标下稳定。
- 退化/失败案例自动候选和人工复核工作流已生成，但仍需人工复核冻结；当前不能按自动标签做论文级 per-stratum 结论。
- 仍需回答增强是否在退化子集和形态一致性指标上稳定减少背景伪边。

当前可执行性状态：

- 168 张带 GT coupling asset 已完成 P1 intake 和 report asset sync。
- `Stage1 Final -> MSFI 50k` 和 `Stage1 Final -> DiffusionEdge baseline 50k` 两条 P1 路线均已有任务指标。
- DiffusionEdge baseline 的 Stage1 各阶段 P2 已完成，结果不支持 Stage1 各阶段相对 Raw 的正向下游增益。
- MSFI 的 Stage1 各阶段 P3 已完成，结果不支持旧 Stage1 各阶段相对 Raw 的正向下游增益。
- Downstream-driven P4/P5C/P6/P6B 已完成，edge-preserve 变体在两个固定 detector 下接近 raw anchor，并已有首轮结构/伪边 proxy 与 paired review；P7 generic controls 已完成 fixed-detector、结构/伪边 proxy 与 paired review 诊断；P8 repeat/control 已完成并给出 `repeat_stable_but_control_competitive_no_stage1_specific_upgrade`；P11 `skeleton_safe_luma_bph_v1` 已完成 fixed-detector、结构 proxy 和 downstream gate，结论为 `candidate_rescues_legacy_but_not_near_raw`。自动退化标签下的负向归因聚合已完成但仍待人工冻结；P9 `edge_safe_gamma_bph_v1` 和 P10 `boundary_aware_luma_bph_v1` 的状态需以后续状态表为准。下一步应优先人工冻结退化/失败案例候选，或定义能解决 baseline-side AC/false-edge/endpoints trade-off 的下一候选；成功前仍不进入 2770 full-pool。

### Phase F：退化子集与失败案例

目标：把问题定义和实验证据闭环到 HAB 显微图像的真实困难。

当前进展：MyEdge 侧已生成第一版自动代理候选 `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\degradation_subset_candidates_20260525.md`。它只读 168 张 coupling manifest、raw 图、GT edge 和 P6/P7 per-image proxy，输出 low contrast boundary、blurred contour、false edge background、thin structure、overlap clutter 等候选以及 10 类 success/failure top-20。该资产当前状态是 `proxy_candidates_ready_pending_manual_review`，只能作为人工复核入口。

进一步进展：MyEdge 侧已生成人工复核工作流 `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\degradation_review\degradation_failure_review_index_20260525.md`。当前 review template `368` 行，其中 stratum candidate `168` 行、success/failure candidate `200` 行，P0/P1 priority queue `211` 行；validation 为 `pending_manual_review`，reviewed `0`、invalid `0`；derived reviewed stratification / failure panel / paper-positive artifacts 仍为空。

推荐子集：

- low contrast。
- weak boundary。
- blurred contour。
- bubble / impurity。
- thin flagella or thin structures。
- over-enhancement sensitive cases。

最低产物：

- 自动候选表：已生成，但不能替代人工标签。
- 人工复核模板与校验/派生入口：已生成。
- 人工冻结后的子集 manifest：仍缺，当前派生表为空。
- 子集定义规则：已有代理阈值草案和人工复核字段，仍缺人工确认版。
- 每个子集的主指标表：仍缺。
- 典型成功案例与失败案例：已有候选 CSV，仍缺人工确认和 paper-ready 图组。

### Phase G：论文与文档收口

目标：让论文读者不需要聊天历史，也能理解数据、方法、结果和边界。

需要同步的文档：

- `README.md`
- `docs/project_handoff_guide_cn.md`
- `docs/project_status_overview_cn.md`
- `docs/comparison_methods_results_index_cn.md`
- `docs/full_enhancement_dataset_inventory_cn.md`
- `docs/stage1_myedge_long_term_closure_plan_cn.md`
- `docs/stage1_myedge_evidence_gap_dashboard_20260525_cn.md`
- `docs/stage1_myedge_next_gate_board_20260525_cn.md`
- `docs/stage1_myedge_p1_execution_readiness_20260525_cn.md`
- `docs/stage1_full2770_execution_readiness_20260525_cn.md`
- `docs/stage1_myedge_claim_evidence_ledger_20260525_cn.md`
- `paper/underwater_image_enhancement_draft_cn.md`
- `paper/underwater_image_enhancement_evidence_pack_cn.md`
- `research-state.yaml`
- `research-log.md`

论文结构建议：

- 主论文以 MyEdge/MSFI 为中心。
- Stage1 放在 structure-preserving input formation 或 enhancement-edge coupling 证据链中。
- 参考两篇同实验室一区论文的数据描述方式，但只写本地确认过的事实。
- 中文主稿优先，英文仅作为题名、摘要辅助、方法名或投稿英文稿准备。

## 5. 关键风险

| 风险 | 控制方式 |
| --- | --- |
| 2777 图像池被误写成已完成正式结果 | 明确其目前只是候选完整图像池，先审计后实验 |
| Stage1 被写成独立增强一区主创新 | 降级为 MyEdge 主论文的结构保持输入支撑 |
| 与 ESWA HAB edge paper 重合 | 主创新写 MSFI/spatial-frequency weak-boundary diffusion，不写 pipeline |
| 与 EAAI HAB segmentation paper 重合 | 任务限定为 crisp edge / boundary topology / morphology-aware edge analysis |
| MyEdge AP 下降被忽略 | 主动写成 ODS/OIS 与 AP 的 trade-off，并补 PR/阈值分析 |
| 数据描述借鉴过度 | 只借鉴结构，不照搬未核验的数据采集细节 |
| 正式结果被覆盖 | 所有新实验写新目录，正式 502/496 目录只读，除非用户明确授权重跑 |

## 6. 长期目标表述

当前 `/goal` 应聚焦为：

> 制定并推进 Stage1Codex 与 MyEdgeCodex 在 Stage1 下游负向结果后的长期收口计划：以 MyEdge/MSFI 边缘检测论文为主线，先将已完成的 Stage1->MyEdge 带 GT 验证落实为负向诊断证据，再用 502/168 小口径推进 downstream-driven / edge-safe enhancement、P7 generic controls、P8 repeat/control、MSFI 消融/替换、退化子集、效率/PR/失败案例等投稿证据链；成功前不扩展到 2770 full-pool，并同步维护仓库文档与 research-log.md。

## 7. 下一步三件事

1. 先处理 `full_algae_dewatermark_v1_manual_review/p0_review_pack/` 中 7 条 P0 机助建议，把人工确认或修正后的决策写回 review sheets；随后继续处理 544 条 pending review issues，并据此形成转换、排除、保留、去重或 split leakage guard 决策。
2. 基于已完成的 MyEdge P1、DiffusionEdge baseline stage-wise P2、MSFI stage-wise P3、downstream-driven P4、baseline-side P5C、P6 结构/伪边 proxy、P6B paired review、P7 generic controls fixed-detector / structure proxy / paired review、Stage1 侧 MyEdge168 GT edge proxy prescreen，以及自动退化标签下的负向归因聚合，P11 `skeleton_safe_luma_bph_v1` 的 fixed-detector planned runs 已执行完毕，result intake 为 `complete_with_report_assets`，structure proxy 为 `complete`，downstream gate 为 `candidate_rescues_legacy_but_not_near_raw`。下一步不是进入 2770，而是在 168 split 上做 P11 repeat/control 或回退评估 P10/P9，判断 baseline-side endpoints/AC trade-off 是采样波动、候选参数问题，还是固定 detector 对轻微增强分布不鲁棒。短期只用当前 502/168 口径验证，稳定成功前不进入 2770 张 full-pool。
3. 若允许 Stage1 长时间运行，按 `docs/stage1_full2770_execution_readiness_20260525_cn.md` 基于 `full_algae_dewatermark_v1_cv2_readable_candidate.txt` 执行 Stage1 2770 张 candidate full run，并写入 `full2770_locked_final_mainline` 新目录；运行后用只读接收脚本确认完整性，且不得把它写成 reviewed clean protocol。
