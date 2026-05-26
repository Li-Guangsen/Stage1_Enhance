# Stage1Codex + MyEdgeCodex next execution gate board

日期：2026-05-25

本文是长期收口目标的下一步执行门禁表。它只读取现有状态文件并写入计划文档，不运行增强、训练、采样、`eval.py`、`show.py` 或指标重算。

## Summary

- Overall status: `gated_long_cycle_incomplete`
- Gate count: `16`
- Manual review pending rows: `544`
- Reviewed clean manifest ready: `False`
- Stage1 full2770 status: `not_started`
- MyEdge P1 status: `complete_with_report_assets`
- MyEdge MSFI stage-wise status: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 P4 status: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 baseline P5C status: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 structure P6 status: `complete`
- MyEdge downstream-driven Stage1 structure P6 paired review status: `complete`
- MyEdge generic enhancement controls P7 status: `complete_with_report_assets`
- Ready/active gate IDs: `G04, G05, G05B, G05C, G05D, G05E, G05F, G05G, G10`

## Status Counts

| Status | Count |
|---|---:|
| `active_guarded` | 1 |
| `blocked_by_G01` | 1 |
| `blocked_pending_human_review` | 1 |
| `complete` | 2 |
| `complete_with_report_assets` | 6 |
| `not_started` | 1 |
| `planned_only` | 3 |
| `planned_only_needs_labels` | 1 |

## Gate Matrix

| Gate | Title | Status | Priority | Can do now | Required before execution | Evidence | Next action | Stop condition | Paper boundary |
|---|---|---|---|---|---|---|---|---|---|
| G01 | 完成 full-pool 人工复核决策 | `blocked_pending_human_review` | `P0` | 可以继续整理 review navigation；不能自动填 reviewer_decision。 | 人工填写 544 条 issue 的 review_status/reviewer_decision/decision_reason/reviewer/review_date，或填写统一模板后 dry-run apply。 | `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_validation_status_20260525.json`; pending=544; invalid=0; template=`metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_template.tsv`; queue=`metrics/manifests/full_algae_dewatermark_v1_manual_review/all_priority_review_queue.tsv` | 先处理 P0，再 P1，再 P2；完成后运行 validate_fullpool_manual_review.py。 | 如果还有 pending/invalid，停止派生 clean manifest、full-pool split 或 leakage guard。 | 不能把 machine_suggestion 写成 reviewer_decision；不能写数据已清洗完成。 |
| G02 | 派生 reviewed clean manifest 与 split leakage guard | `blocked_by_G01` | `P0` | 只能读取当前派生状态；不能生成 clean manifest。 | G01 校验完成：pending=0、invalid=0、无 unresolved decisions。 | `metrics/manifests/full_algae_dewatermark_v1_manual_review/derived_review_artifacts/review_artifacts_status_20260525.json`; can_generate_clean_manifest=False; clean=`metrics/manifests/full_algae_dewatermark_v1_manual_review/derived_review_artifacts/reviewed_cv2_clean_manifest.txt` (missing) | 人工复核完成后运行 derive_fullpool_review_artifacts.py，再检查 reviewed clean manifest 和 split guard。 | can_generate_clean_manifest=false 或 clean manifest missing 时停止使用 reviewed pool。 | 没有 clean manifest 前不能写 cleaned full-pool protocol 已完成。 |
| G03 | Stage1 2770 OpenCV-readable full run | `not_started` | `P1` | 不建议现在启动；只能维护 runbook/intake。 | 需要用户显式授权长跑；推荐先完成 G01/G02，或明确说明使用 cv2-readable candidate 而不是 reviewed clean manifest。 | `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.json`; run_script=`experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1`; output_exists=False | 若授权执行，必须显式使用 locked_full506_final_mainline.json，运行后先用 intake_stage1_fullpool_run_outputs.py 接收。 | 没有 complete_with_log_and_run_report 前，停止写 full2770 已完成。 | full2770 是 coverage evidence，不能替代 full502_clean_v1/compare9_complete496_v1 正式主表。 |
| G04 | Stage1 无 GT proxy 与选图支撑 | `complete` | `P2` | 可以继续用于筛选 qualitative/failure 候选。 | 不需要新增实验；但任何论文结论必须标注 no-GT proxy 边界。 | `metrics/outputs/downstream_edge_validation/official_full502_mainline/stage_full502_proxy/summary.json`; `metrics/outputs/downstream_edge_validation/official_full502_mainline/compare9_complete496_proxy/summary.json` | 从已有 proxy panels 中整理 paper-ready 候选清单，但不写 ODS/OIS/AP/AC。 | 发现想写下游提升时，停止并回到 MyEdge GT 评测。 | 无 GT proxy 不是边缘检测精度结果。 |
| G05 | MyEdge P1 fixed-detector Stage1 Final 下游验证 | `complete_with_report_assets` | `P0` | P1 已完成时可以进入结果解释与下一轮矩阵规划；未完成时只准备执行说明。 | 若未完成，需要用户授权 MyEdge sampling/eval；若已完成，需要按 intake/report assets 核对指标并保留固定 detector 边界。 | `docs/stage1_myedge_coupling_status_20260525_cn.json`; command_sheet=`docs/research_contracts/stage1_myedge_coupling_p1_execution_command_sheet_v1.md`; msfi_output=`output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524`; baseline_output=`output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525` | P1 完成后先写成诊断结果，再规划 Stage1 stage-wise / generic enhancement controls；未完成时按 command sheet 执行。 | 两个 P1 output roots 缺失或 intake=not_started 时，停止写任何 P1 指标；P1 完成后仍不能写成 full502/full2770 下游收益。 | P1 只是 Stage1 Final fixed-detector 诊断；当前结果不支持 Stage1 Final 提升边缘检测的正向结论。 |
| G05B | DiffusionEdge baseline Stage1 stage-wise 诊断 | `complete_with_report_assets` | `P0` | 已完成时可以进入 stage attribution 解释；未完成时先执行 BPH/IMF1Ray/RGHS/CLAHE/Fused 到 baseline 的固定检测器矩阵。 | 需要 168 张同 stem staging、固定 DiffusionEdge baseline checkpoint、每个 stage 的 sampling/eval/show/report assets。 | `docs/paper_assets/stage1_coupling/stagewise_baseline_p2_results_20260525.json` | 当前结果应写成 baseline 单检测器 stage attribution：各 Stage1 阶段均低于 Raw anchor，BPH 最接近 Raw，Final 最差；下一步补 generic controls 和 MSFI stage-wise。 | 结果缺失或 status 不是 complete_with_report_assets 时，停止写 stage-wise 指标；完成后仍不能外推到 MSFI 或所有检测器。 | 该矩阵不支持 Stage1 正向下游收益，只支持定位 Stage1 阶段对 DiffusionEdge baseline 的负向影响。 |
| G05C | MSFI Stage1 stage-wise 诊断 | `complete_with_report_assets` | `P0` | 已完成时可以与 baseline stage-wise 共同判断旧 Stage1 增强是否适合作为下游输入；未完成时先执行 BPH/IMF1Ray/RGHS/CLAHE/Fused 到 MSFI 的固定检测器矩阵。 | 需要 168 张同 stem staging、固定 MSFI 50k checkpoint、每个 stage 的 sampling/eval/show/report assets。 | `docs/paper_assets/stage1_coupling/stagewise_msfi_p3_results_20260525.json` | 当前结果应写成 MSFI 单检测器 stage attribution：各 Stage1 阶段整体低于 Raw anchor，Final 降幅最大；下一步转向 downstream-driven enhancement variant 和 generic controls。 | 结果缺失或 status 不是 complete_with_report_assets 时，停止写 MSFI stage-wise 指标；完成后仍不能外推到 full502/full2770。 | 该矩阵不支持 Stage1 正向下游收益，只支持旧增强方案对 MSFI 下游输入不匹配的诊断。 |
| G05D | Downstream-driven edge-preserve Stage1 P4 变体诊断 | `complete_with_report_assets` | `P0` | 已完成时可以把它写成旧增强损伤后的 edge-safe 候选诊断；不能写成稳定优于 raw。 | 需要固定 MSFI 50k、168 张同 stem staging、original-control 同轮对照、eval/show/report assets 和结果边界同步。 | `docs/paper_assets/stage1_coupling/downstream_variant_p4_results_20260525.json` | 当前 edge_preserve_raw_bph_moderate_v1 已接近 raw anchor，并在同轮 original-control 下提升 AP/OIS；下一步补 repeat/control、generic enhancement controls 和必要的 502 proxy，不进入 full2770。 | 若未完成 repeat/control 或 generic controls，停止写稳定正向下游收益；若 168 口径不优于 raw/control，不启动 full2770。 | P4 只支持旧 Stage1 Final 会伤害下游、新 edge-preserve 变体基本恢复到 raw 附近的候选结论；不能写成 full502/full2770 或所有 detector 的下游提升。 |
| G05E | Downstream-driven edge-preserve Stage1 P5C DiffusionEdge baseline 二次检测器诊断 | `complete_with_report_assets` | `P0` | 已完成时可以把它写成 P4 的第二检测器确认：edge-preserve 变体不是 MSFI-only；不能写成稳定正向收益。 | 需要固定 DiffusionEdge baseline 50k、168 张同 stem staging、eval/show/report assets 和结果边界同步。 | `docs/paper_assets/stage1_coupling/downstream_variant_baseline_p5c_results_20260525.json` | 当前 mild 在 DiffusionEdge baseline 下有 AP/OIS 正向信号，moderate 也接近 raw；下一步补 repeat/control、generic enhancement controls 和结构/伪边指标，不进入 full2770。 | 若未完成 repeat/control、generic controls 和结构指标，停止写稳定正向下游收益；若 168 口径不稳定，不启动 full2770。 | P5C 只支持 edge-preserve 方向具备第二检测器一致的 edge-safe 信号；AC 仍低于 raw，不能写成完整 task-driven enhancement 已证明。 |
| G05F | P4/P5C 结构、伪边、碎裂与 paired proxy 诊断 | `complete` | `P0` | 已完成时可以把它写成结构诊断 proxy：旧 Final 显著增加伪边与碎裂，P4/MSFI moderate 有伪边、碎裂和逐图配对候选信号。 | 需要已有 P4/P5C MAT、GT、各 run ODS threshold、tolerance=2px、summary/per-image/delta 输出和 paired review 输出。 | `docs/paper_assets/stage1_coupling/downstream_variant_structure_p6_metrics_20260525.json`; paired=`docs/paper_assets/stage1_coupling/downstream_variant_structure_p6_paired_review_20260525.json` | 基于 P6/P6B 解释旧 Stage1 下降原因，并设计 generic enhancement controls 与 repeat/control；不要重复跑 P4/P5C 首轮。 | 若未完成 generic controls 或 repeat/control，停止写稳定正向下游收益；若只看 P6/P6B proxy，不替代 ODS/OIS/AP/AC。 | P6/P6B 只覆盖 168 张 MyEdge split、既有 P4/P5C MAT 和结构 proxy；不能外推到 full502/full2770，也不能写成完整 task-driven enhancement 已证明。 |
| G05G | Generic enhancement controls P7 诊断 | `complete_with_report_assets` | `P0` | 已完成 Stage1 168 输出、MyEdge staging、固定 MSFI 与 DiffusionEdge baseline sampling/eval/show/report assets、P7 结构 proxy 和 P7 paired review；可以进入结果解释与 repeat/control 设计。 | 若继续新增 control 或 repeat，仍必须确认目标 output roots 为空且遵守 WSL 脚本封装规则。 | `docs/paper_assets/stage1_coupling/generic_control_p7_msfi_preflight_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_baseline_preflight_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_msfi_results_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_baseline_results_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_structure_metrics_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_structure_paired_review_20260525.json`; msfi_results=complete_with_report_assets; baseline_results=complete_with_report_assets; structure=complete; paired=complete | 将 P7 写成 168 张小口径 generic luminance-only control：gamma 在 baseline 侧有小幅 ODS/OIS/AP 信号，MSFI 侧基本贴近 raw；结构 proxy 显示 MSFI/gamma 有轻微信号但 baseline/gamma 仍 mixed；下一步补 repeat/control，不进入 full2770。 | 没有 repeat/control 或更大口径前，停止写稳定正向下游收益。 | P7 只能用于判断 P4/P5C 信号是否可能来自轻量亮度分布控制或 detector domain-shift；不能证明 Stage1 全流程或 full502/full2770 已提升下游。 |
| G06 | MSFI 组件消融 | `planned_only` | `P1` | 可以细化合同或检查资产；不能写组件独立有效。 | 需要 MyEdge 侧配置、训练/采样/评测授权和统一 intake。 | `docs/research_contracts/msfi_component_ablation_v1.md` | 完成 frequency token、spatial-frequency interaction、timestep gating、full MSFI 的组件级结果表。 | 没有消融结果前，停止写 gating/token 独立贡献已证明。 | 合同存在不等于实验完成。 |
| G07 | MSFI 替换模块对比 | `planned_only` | `P1` | 可以细化替换清单；不能写已回应 Sobel/CIAFF 风险。 | 需要 MyEdge 侧替换模块 run 授权与统一评测。 | `docs/research_contracts/msfi_replacement_module_v1.md` | 优先覆盖 Sobel/CIAFF-like/Fourier，再扩展 CBAM/SE/ECA/ASPP/FPN。 | 没有替换对比结果前，停止写 MSFI 优于这些替代机制。 | 替换对比是回应同方向 ESWA 重合风险的关键证据。 |
| G08 | 退化子集与失败案例协议 | `planned_only_needs_labels` | `P1` | 可以整理候选标签规则；不能写退化鲁棒性已证明。 | 需要人工复核质量异常/近重复后形成子集标签，或在 MyEdge 168 GT split 上另行建立可复核标签。 | `docs/research_contracts/degradation_stratified_edge_analysis_v1.md` | 先从 P1/P2 质量异常候选沉淀 low contrast、weak boundary、blur、bubble/impurity、thin structure 标签。 | 没有子集 manifest 和子集指标时，停止写复杂退化场景鲁棒。 | 质量异常候选不是自动低质量标签。 |
| G09 | 效率、PR/AP trade-off 与失败案例 | `planned_only` | `P1` | 可以维护图表计划；不能写速度/部署优势。 | 需要 MyEdge 侧 Params/FLOPs/FPS/显存、PR curve、TP/FP/FN overlay 和 failure panels。 | `docs/research_contracts/paper_efficiency_pr_failure_analysis_v1.md` | 优先补 AP 下降解释所需 PR curve，再补效率和 failure cases。 | 没有实测效率前，停止写更快、更轻量或部署友好。 | AP trade-off 必须诚实保留。 |
| G10 | 论文写作与状态同步 | `active_guarded` | `P0` | 可以继续更新中文主稿/证据包中的边界说明。 | 任何实验状态改变后必须同步 README、状态总览、交接指南、research-state.yaml 和 research-log.md。 | `docs/stage1_myedge_evidence_gap_dashboard_20260525_cn.json`; `docs/stage1_myedge_long_term_closure_plan_cn.md` | 所有新结果先落盘为 evidence，再进入论文 claim。 | 如果证据只是合同、建议或 dashboard，停止写成结果结论。 | 主稿应以 MyEdge/MSFI 为主线，Stage1 只作为结构保持输入支撑。 |

## Immediate Safe Work

1. 继续维护人工复核导航和状态校验，但不要自动填写 `reviewer_decision`。
2. 将 MyEdge P1、DiffusionEdge baseline stage-wise 和 MSFI stage-wise 都写成 fixed-detector 负向诊断结果，不写成旧 Stage1 下游收益证明。
3. 将 P4/P5C edge-preserve 变体写成 edge-safe 候选：已基本消除旧 Final 的大幅损伤，但尚不能声称稳定优于 raw。
4. P6 结构/伪边指标、P6B paired review、P7 结构 proxy 和 P7 paired review 已完成；generic controls P7 也已完成固定 MSFI 与 DiffusionEdge baseline 评测。下一步先做 repeat/control，再判断是否扩展口径。
5. 将 MSFI 消融、替换、退化分层、效率/PR/失败案例保留为 planned-only，直到结果文件落盘。
6. 论文写作只写已有事实：Stage1 proxy 是 no-GT 支撑，MyEdge MSFI 是 mixed metric profile，AP trade-off 必须保留。

## Hard Stops

- `manual_review_validation_status` 仍有 pending 时，不生成 clean manifest。
- `reviewed_cv2_clean_manifest.txt` 不存在时，不把 full-pool 写成已清洗协议。
- `full2770` intake 不是 `complete_with_log_and_run_report` 时，不写完整 2770 增强已完成。
- MyEdge P1 output roots 不存在或 intake 为 `not_started` 时，不写任何 P1 指标。
- MyEdge P1 完成后，也只能在 168 张 / Stage1 Final / fixed-detector 边界内解释，不能外推为 Stage1 已提升 ODS/OIS/AP/AC。
- MyEdge stage-wise 完成后，如果各增强阶段低于 Raw anchor，也只能写成负向诊断，不能换成正向叙事。
- P4/P5C 完成后，如果只接近 Raw 或仅部分指标优于 Raw，也只能写成 edge-safe 候选，不能换成稳定正向收益。
- P6/P6B 完成后，也只能写结构 proxy 与 paired diagnostic，不能替代 ODS/OIS/AP/AC 或 stable downstream benefit claim。
- MyEdge planned contracts 不能被写成已完成实验结果。
