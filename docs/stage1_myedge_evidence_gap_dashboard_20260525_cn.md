# Stage1Codex + MyEdgeCodex evidence gap dashboard

日期：2026-05-25

本文是跨项目投稿证据缺口 dashboard，只读取本地 Stage1Codex 与 MyEdgeCodex 已有文件，不运行增强、训练、采样、评测或指标重算。

## Executive Summary

- Overall status: `major_evidence_gaps_remain`
- Stage1 full-pool manual review pending rows: `544`
- Stage1 reviewed clean manifest exists: `False`
- Stage1 full2770 run status: `not_started`
- MyEdge formal MSFI 50k: ODS `0.783527`, OIS `0.794213`, AP `0.345899`, AC `0.796846`
- MyEdge Stage1 coupling P1 status: `complete_with_report_assets`
- MyEdge Stage1 baseline stage-wise status: `complete_with_report_assets`
- MyEdge Stage1 MSFI stage-wise status: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 P4 status: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 baseline P5C status: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 structure P6 status: `complete`
- MyEdge downstream-driven Stage1 structure P6 paired review status: `complete`
- MyEdge generic enhancement controls P7 status: `complete_with_report_assets`

## Status Counts

| Status | Count |
|---|---:|
| `complete` | 6 |
| `complete_with_report_assets` | 7 |
| `missing_blocked_by_manual_review` | 1 |
| `not_started` | 1 |
| `partial_complete` | 1 |
| `pending_manual_review` | 1 |
| `planned_only` | 4 |

## Evidence Gap Matrix

| ID | Workstream | Requirement | Status | Priority | Evidence | Next action | Boundary |
|---|---|---|---|---|---|---|---|
| S1-01 | Stage1 formal protocol | 锁定正式增强主线配置与正式结果目录 | `complete` | `P0` | `experiments/optimization_v1/configs/locked_full506_final_mainline.json`; `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline` | 保持 502/496 正式论文口径，不用 full2770 替代当前主表。 | 正式主线必须显式使用 locked_full506_final_mainline.json；不能写成直接 python main.py。 |
| S1-02 | Stage1 formal protocol | full502_clean_v1 与 compare9_complete496_v1 的无 GT 结构代理支撑包 | `complete` | `P1` | `metrics/outputs/downstream_edge_validation/official_full502_mainline/stage_full502_proxy/summary.json`; `metrics/outputs/downstream_edge_validation/official_full502_mainline/compare9_complete496_proxy/summary.json` | 用作结构保持与选图支撑；带 GT 的 ODS/OIS/AP/AC 必须回到 MyEdge。 | 无 GT proxy 不是下游边缘检测正式结果。 |
| S1-03 | Stage1 full-pool dataset | 2777 图像池 manifest、decode、duplicate、quality audit | `complete` | `P0` | `docs/full_enhancement_dataset_inventory_cn.md`; `metrics/manifests/full_algae_dewatermark_v1.txt`; `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt` | 继续人工复核 544 条 issue；把 2777 图像池与参考论文数据子集关系写清。 | 2777 是增强候选池，不等同于 MyEdge 当前 168 张 GT test，也不自动等同于参考论文公开写法。 |
| S1-04 | Stage1 full-pool dataset | 人工复核决策、clean manifest、split leakage guard | `pending_manual_review` | `P0` | `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_validation_status_20260525.json`; pending=544; invalid=0; template=`metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_template.tsv` | 先由人填写 manual_review_decision_template.tsv，再 dry-run apply；无 invalid 后才允许 --apply。 | machine_suggestion 不是 reviewer_decision；不能据此生成 clean manifest。 |
| S1-05 | Stage1 full-pool dataset | reviewed clean manifest | `missing_blocked_by_manual_review` | `P0` | `metrics/manifests/full_algae_dewatermark_v1_manual_review/derived_review_artifacts/reviewed_cv2_clean_manifest.txt` (missing); can_generate=False | 等人工复核完成后运行 derive_fullpool_review_artifacts.py。 | 没有 clean manifest 前，不应用 reviewed pool 做正式长跑入口。 |
| S1-06 | Stage1 full-pool enhancement | 2770 OpenCV-readable full run | `not_started` | `P1` | `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.json`; output_exists=False; present=0/33240 | 人工复核优先；若授权长跑，再用 run_full_cv2readable2770_locked.ps1 并通过 intake 接收。 | full2770 只作为 coverage evidence；完成前不能写成已有结果。 |
| ME-01 | MyEdge main result | MSFI + EMA + slide/non-resize + 50k 正式主结果 | `complete` | `P0` | `docs/paper_assets/experiment_status.csv`; ODS=0.783527; OIS=0.794213; AP=0.345899; AC=0.796846 | 论文中写 mixed metric profile：ODS/OIS 高于 DiffusionEdge baseline，AP 低于 baseline，AC 基本持平。 | 不能写全面优于、SOTA 或所有指标最优。 |
| ME-02 | MyEdge comparison | DiffusionEdge baseline 50k 与正式对比方法主表 | `complete` | `P0` | formal/comparison mat rows=10; baseline_diffusionedge_50k_mat status=completed_local_wsl_reeval_unified_evidence_synced | 继续按 MyEdge claim-to-evidence 和 readiness checklist 控制表述。 | 不同 baseline 训练协议不完全相同；不能把 nominal exposure 写成 identical training。 |
| ME-03 | Stage1 -> MyEdge coupling | 168 张 Stage1 coupling manifest 与 P1 preflight | `complete_with_report_assets` | `P0` | `docs/stage1_myedge_coupling_status_20260525_cn.json`; rows=168; GT missing=0; P1 status=complete_with_report_assets | 若 P1 已完成，则只在 168 张 / Stage1 Final / fixed detector 边界内解释；下一步补 stage-wise 与 generic enhancement controls。 | P1 完成不等于 Stage1 全阶段、full502/full2770 或所有退化场景的下游收益。 |
| ME-04 | Stage1 -> MyEdge coupling | P1 fixed-detector Stage1 Final 下游评测结果 | `complete_with_report_assets` | `P0` | `output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524`; MSFI mat={'threshold': 0.24, 'ods': 0.588287, 'ois': 0.671357, 'ap': 0.263997}; AC=0.7403; `output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525`; Baseline mat={'threshold': 0.46, 'ods': 0.530094, 'ois': 0.56791, 'ap': 0.224073}; AC=0.7349 | 当前 P1 结果应写成 Stage1 Final fixed-detector 诊断：绝对指标低于 raw-anchor 正式结果，不能写 Stage1 已带来下游增益。 | P1 是第一轮诊断结果；还不能替代 stage-wise、generic controls、退化子集和形态一致性证据。 |
| ME-04B | Stage1 -> MyEdge coupling | DiffusionEdge baseline 固定检测器 Stage1 各阶段诊断矩阵 | `complete_with_report_assets` | `P0` | `docs/paper_assets/stage1_coupling/stagewise_baseline_p2_results_20260525.json`; Raw ODS/OIS/AP/AC=0.770521/0.779986/0.363065/0.7969; BPH ODS/OIS/AP/AC=0.712919/0.722432/0.338546/0.7942; IMF1Ray ODS/OIS/AP/AC=0.687163/0.722376/0.355401/0.7417; RGHS ODS/OIS/AP/AC=0.612234/0.65375/0.286407/0.7519; CLAHE ODS/OIS/AP/AC=0.584453/0.665213/0.265935/0.7534; Fused ODS/OIS/AP/AC=0.629095/0.689792/0.302611/0.7539; Final ODS/OIS/AP/AC=0.530094/0.56791/0.224073/0.7349 | 当前 baseline stage-wise 结果显示各 Stage1 阶段均低于 Raw anchor；下一步补 generic enhancement controls 与 MSFI stage-wise，定位是否为增强分布迁移或 detector-specific 问题。 | 该矩阵只覆盖 DiffusionEdge baseline；不能外推到 MSFI，也不能写 Stage1 正向下游收益。 |
| ME-04C | Stage1 -> MyEdge coupling | MSFI 固定检测器 Stage1 各阶段诊断矩阵 | `complete_with_report_assets` | `P0` | `docs/paper_assets/stage1_coupling/stagewise_msfi_p3_results_20260525.json`; Raw ODS/OIS/AP/AC=0.783527/0.794213/0.345899/0.796846; BPH ODS/OIS/AP/AC=0.739237/0.752407/0.31061/0.7942; IMF1Ray ODS/OIS/AP/AC=0.731747/0.754032/0.350926/0.7573; RGHS ODS/OIS/AP/AC=0.67172/0.723929/0.296742/0.7619; CLAHE ODS/OIS/AP/AC=0.639906/0.720816/0.279873/0.775; Fused ODS/OIS/AP/AC=0.669946/0.721055/0.29117/0.7683; Final ODS/OIS/AP/AC=0.588287/0.671357/0.263997/0.7403 | 当前 MSFI stage-wise 结果同样显示各 Stage1 阶段整体低于 Raw anchor；下一步应停止把旧 Stage1 写成正向下游收益，并转向 downstream-driven enhancement variant 设计和 generic controls。 | 该矩阵只覆盖 MSFI 50k 固定检测器和 168 张 MyEdge test split；不能外推到 full502/full2770，也不能写成 Stage1 正向下游收益。 |
| ME-04D | Stage1 -> MyEdge coupling | MSFI 固定检测器 downstream-driven edge-preserve Stage1 P4 变体诊断矩阵 | `complete_with_report_assets` | `P0` | `docs/paper_assets/stage1_coupling/downstream_variant_p4_results_20260525.json`; historical_raw_msfi_anchor ODS/OIS/AP/AC=0.783527/0.794213/0.345899/0.796846; edge_preserve_original_control ODS/OIS/AP/AC=0.783082/0.794168/0.337353/0.7972; edge_preserve_raw_bph_mild_v1 ODS/OIS/AP/AC=0.782743/0.793599/0.345909/0.7957; edge_preserve_raw_bph_moderate_v1 ODS/OIS/AP/AC=0.782999/0.794527/0.345952/0.7952; legacy_stage1_final_p1 ODS/OIS/AP/AC=0.588287/0.671357/0.263997/0.7403 | 当前 P4 结果显示 edge-preserve 变体已基本消除旧 Stage1 Final 的大幅下游损伤；后续应补 repeat/control 与 generic enhancement controls，再判断是否有稳定正向收益。 | 该矩阵只覆盖 168 张 MyEdge test split 和固定 MSFI 50k；edge_preserve_raw_bph_moderate_v1 只能写成接近 Raw / 同轮 original-control 下 AP/OIS 有改善的候选，不能写成稳定优于 raw 或 full502/full2770 已提升。 |
| ME-04E | Stage1 -> MyEdge coupling | DiffusionEdge baseline 固定检测器 downstream-driven edge-preserve Stage1 P5C 二次检测器诊断矩阵 | `complete_with_report_assets` | `P0` | `docs/paper_assets/stage1_coupling/downstream_variant_baseline_p5c_results_20260525.json`; historical_raw_diffusionedge_anchor ODS/OIS/AP/AC=0.770521/0.779986/0.363065/0.7969; edge_preserve_original_control ODS/OIS/AP/AC=0.77147/0.78149/0.362827/0.7934; edge_preserve_raw_bph_mild_v1 ODS/OIS/AP/AC=0.770699/0.782323/0.370985/0.7941; edge_preserve_raw_bph_moderate_v1 ODS/OIS/AP/AC=0.771168/0.782422/0.363047/0.794; legacy_stage1_final_p1 ODS/OIS/AP/AC=0.530094/0.56791/0.224073/0.7349 | 当前 P5C 结果显示 edge-preserve 变体在 DiffusionEdge baseline 下也基本消除旧 Stage1 Final 的下游损伤；后续应补 repeat/control、generic enhancement controls 和结构/伪边指标，再判断是否有稳定正向收益。 | 该矩阵只覆盖 168 张 MyEdge test split 和固定 DiffusionEdge baseline 50k；mild 的 AP/OIS 正向信号不能单独写成稳定 Stage1 下游收益，AC 仍低于 raw。 |
| ME-04F | Stage1 -> MyEdge coupling | P4/P5C 现有 MAT 输出的结构、断裂与伪边 proxy 诊断 P6 | `complete` | `P0` | `docs/paper_assets/stage1_coupling/downstream_variant_structure_p6_metrics_20260525.json`; paired=`docs/paper_assets/stage1_coupling/downstream_variant_structure_p6_paired_review_20260525.json`; msfi_p4/historical_raw_msfi_anchor F1/precision/recall/false-edge/components/endpoints=0.8554/0.8783/0.8507/0.1217/4.2507/9.4521; msfi_p4/edge_preserve_raw_bph_moderate_v1 F1/precision/recall/false-edge/components/endpoints=0.8568/0.8851/0.8471/0.1149/3.6899/8.0349; msfi_p4/legacy_stage1_final_p1 F1/precision/recall/false-edge/components/endpoints=0.6446/0.6114/0.7669/0.3886/63.2304/100.3726; diffusionedge_baseline_p5c/historical_raw_diffusionedge_anchor F1/precision/recall/false-edge/components/endpoints=0.8491/0.8794/0.8392/0.1206/4.6940/11.3757; diffusionedge_baseline_p5c/edge_preserve_raw_bph_mild_v1 F1/precision/recall/false-edge/components/endpoints=0.8475/0.8735/0.8416/0.1265/4.5799/11.6185; diffusionedge_baseline_p5c/legacy_stage1_final_p1 F1/precision/recall/false-edge/components/endpoints=0.5522/0.4840/0.7062/0.5160/140.1426/235.1233 | 当前 P6/P6B 可用于解释旧 Final 的伪边与碎裂问题，并说明 P4/MSFI moderate 的伪边、碎裂与逐图配对候选信号；下一步仍需 generic enhancement controls 和 repeat/control。 | P6 只读取已有 P4/P5C MAT 与 GT，按各 run ODS threshold 二值化，tolerance=2px；它是结构诊断 proxy，不替代 ODS/OIS/AP/AC，也不能外推到 full502/full2770。 |
| ME-04G | Stage1 -> MyEdge coupling | Generic luminance-only controls P7 诊断：CLAHE/gamma 两个非 BPH 轻量对照已完成固定 MSFI 与 DiffusionEdge baseline 评测 | `complete_with_report_assets` | `P0` | `docs/paper_assets/stage1_coupling/generic_control_p7_msfi_preflight_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_baseline_preflight_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_msfi_results_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_baseline_results_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_structure_metrics_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_structure_paired_review_20260525.json`; msfi_results=complete_with_report_assets; baseline_results=complete_with_report_assets; structure=complete; paired=complete; MSFI/historical_raw_msfi_anchor ODS/OIS/AP/AC=0.783527/0.794213/0.345899/0.796846; MSFI/generic_luma_clahe_mild_v1 ODS/OIS/AP/AC=0.781721/0.793016/0.345003/0.7934; MSFI/generic_luma_gamma_mild_v1 ODS/OIS/AP/AC=0.782883/0.794223/0.345982/0.7952; MSFI/legacy_stage1_final_p1 ODS/OIS/AP/AC=0.588287/0.671357/0.263997/0.7403; Baseline/historical_raw_diffusionedge_anchor ODS/OIS/AP/AC=0.770521/0.779986/0.363065/0.7969; Baseline/generic_luma_clahe_mild_v1 ODS/OIS/AP/AC=0.769295/0.784093/0.366887/0.7915; Baseline/generic_luma_gamma_mild_v1 ODS/OIS/AP/AC=0.771645/0.782024/0.371366/0.7936; Baseline/legacy_stage1_final_p1 ODS/OIS/AP/AC=0.530094/0.56791/0.224073/0.7349 | 当前 P7 结果应写成 generic luminance-only 轻量对照诊断：baseline/gamma 有 ODS/OIS/AP 小幅正向信号，MSFI/gamma 基本贴近 raw；P7 结构 proxy 与 paired review 已补，显示 MSFI/gamma 在 F1、precision、false-edge、碎裂和 endpoints 上有轻微信号，但 baseline/gamma 仍 mixed。下一步补 repeat/control，再判断是否进入更大口径。 | P7 只覆盖 168 张 MyEdge split 和两个轻量 luminance controls；尚不能写 Stage1 稳定提升下游，也不能替代 P4/P5C repeat 或 full502/full2770 证据。 |
| ME-05 | MyEdge ablation | MSFI component ablation | `planned_only` | `P1` | `docs/research_contracts/msfi_component_ablation_v1.md` | 完成 frequency token、spatial-frequency interaction、timestep gating、full MSFI 的组件级对比。 | 合同存在不等于实验完成；未完成前不能写 gating/频带 token 独立有效。 |
| ME-06 | MyEdge ablation | Sobel/CIAFF-like/Fourier/CBAM/SE/ECA/ASPP/FPN 替换模块对比 | `planned_only` | `P1` | `docs/research_contracts/msfi_replacement_module_v1.md` | 直接回应同方向 ESWA 参考论文的 Sobel/CIAFF 重合风险。 | 替换对比未完成前，只能说这是待补证据。 |
| ME-07 | MyEdge robustness | 低对比、弱边界、气泡/杂质、模糊边界等退化子集分析 | `planned_only` | `P1` | `docs/research_contracts/degradation_stratified_edge_analysis_v1.md` | 先用 Stage1 full-pool manual review 的子集标签沉淀候选，再在 MyEdge 侧形成带 GT 子集评测。 | 没有人工标签或子集协议时，不能泛化宣称复杂退化鲁棒。 |
| ME-08 | MyEdge paper assets | 效率、PR/AP trade-off、失败案例与投稿级 qualitative | `planned_only` | `P1` | `docs/research_contracts/paper_efficiency_pr_failure_analysis_v1.md` | 补 Params/FLOPs/FPS/显存、PR curve、TP/FP/FN overlay、failure cases。 | 没有效率实验前不能写更轻量、更快或部署优势。 |
| ME-09 | MyEdge paper assets | Figure 1/2 和 paper-ready result assets | `partial_complete` | `P2` | `docs/paper_assets/figures/figure1_overview.png`; `docs/paper_assets/figures/figure2_msfi_module.png`; `docs/paper_assets/paper_ready_results.md` | 继续补 Figure 3 qualitative、PR/失败案例、Stage1 coupling 图组。 | Figure 1/2 是方法图资产，不是新增实验结论。 |

## Recommended Long-Cycle Order

1. 完成人工复核：先 P0，再 P1，再 P2；只有人工决策完成后才派生 clean manifest 和 split leakage guard。
2. 已完成 MyEdge P1 fixed-detector coupling、DiffusionEdge baseline stage-wise、MSFI stage-wise 和 downstream-driven P4 诊断；当前旧 Stage1 增强不支持正向下游收益，P4 edge-preserve 变体只支持 edge-safe / 接近 raw 的候选结论。
3. P6 结构 proxy、P6B paired review、P7 结构 proxy 与 P7 paired review 均已完成；generic controls P7 已完成固定 MSFI 与 DiffusionEdge baseline 评测。当前 P7 显示轻量 generic gamma 在 baseline 侧有小幅 ODS/OIS/AP 信号、MSFI 侧基本贴近 raw，结构 proxy 上 MSFI/gamma 有轻微信号但 baseline/gamma 仍 mixed；仍需 repeat/control，不进入 full2770。
4. 再补 MyEdge 核心证据：MSFI 组件消融、替换模块、退化子集、PR/AP trade-off、效率和失败案例。
5. 最后再决定 Stage1 full2770 长跑是否启动；full2770 作为 coverage evidence，不替代当前 502/496 正式主表。

## Writing Boundary

- 主论文定位应以 MyEdge/MSFI 的 spatial-frequency weak-boundary diffusion 为主；Stage1 是 task-driven structure-preserving input formation。
- 当前不能把 Stage1 下游收益写成已完成 GT-based ODS/OIS/AP/AC 结论。
- 当前不能写 MSFI 全面领先；必须保留 AP 低于 DiffusionEdge baseline 的 trade-off。
- 合同文件、机助建议和 dashboard 都不是实验结果，只是后续工作入口。
