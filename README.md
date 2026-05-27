# Stage1Codex

Stage1Codex 是面向有害藻华（HAB）水下显微图像的分阶段增强与下游边缘验证支撑仓库，不是一般自然场景水下增强仓库。

当前项目已经从早期探索进入“正式增强资产 + 证据治理 + MyEdge/MSFI 论文支撑”的阶段。Stage1 的当前定位是为 MyEdge/MSFI 主论文提供 `task-driven structure-preserving input formation`，而不是单独硬推“增强 + 边缘检测 pipeline”主创新。

## 1. 必读入口

每次接手先读：

1. `AGENTS.md`
2. `docs/project_execution_rules_cn.md`
3. `docs/current_experiment_status_cn.md`
4. `docs/evidence/full_flow_recovery/stage1_full_enhancement_mainline_recovery_plan_cn.md`
5. `docs/evidence/full_flow_recovery/stage1_full_flow_failure_audit_and_next_goal_20260527_cn.md`
6. `docs/evidence/fa01_family_audit/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
7. `docs/evidence/fa01_family_audit/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md`
8. `docs/evidence/fa01_family_audit/fa01_high_risk_sample_evidence_index_20260527_cn.md`
9. `docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527_cn.md`
10. `docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527_cn.md`
11. `docs/evidence/stage1_myedge_coupling/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`
12. `docs/evidence/stage1_myedge_coupling/stage1_sidecar_map_definition_fa01_20260527_cn.md`
13. `docs/evidence/stage1_myedge_coupling/stage1_long_horizon_goal_after_tlvc01_20260527_cn.md`
14. `docs/evidence_asset_inventory_cn.md`
15. `docs/evidence_index_cn.md`
16. `metrics/registry_schema_cn.md`
17. `metrics/experiment_registry.csv`
18. `metrics/candidate_registry.csv`
19. `experiments/experiment_index_cn.md`
20. `docs/project_status_overview_cn.md`
21. `docs/project_handoff_guide_cn.md`
22. `research-state.yaml`

涉及正式结果、baseline 或主表时再读：

- `docs/comparison_methods_results_index_cn.md`
- `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502/mean_metrics_table.md`
- `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/mean_metrics_table.md`

涉及论文写作时再读：

- `paper/underwater_image_enhancement_draft_cn.md`
- `paper/underwater_image_enhancement_evidence_pack_cn.md`
- `method-underwater-enhancement.md`
- `method-underwater-enhancement-paper-ready.md`
- `related-work-underwater-enhancement.md`

## 2. 正式增强资产

当前 formal enhancement source asset 是：

- 配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 结果源目录：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 最终输出源：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`

注意：`full506_final_mainline` 是历史锁定后的源资产目录名，不是论文主表样本口径。

正式增强流程：

`Original -> BPH -> IMF1Ray / RGHS / CLAHE -> Fused -> Final`

论文中必须按真实职责解释阶段：

- `BPH`：灰像素引导的前置白平衡。
- `IMF1Ray`：IMF1-Rayleigh 高频细节分支。
- `RGHS`：白平衡安全对比分支，不是标准现成 RGHS 模块。
- `CLAHE`：CLAHE 引导的局部可见性分支，不是直接输出普通 CLAHE 图像。
- `Fused`：特征门控的三分支亮度结构融合。
- `Final`：轻量照明与对比收口。

## 3. 正式论文指标口径

当前论文统计只认两套 manifest：

- 阶段表：`full502_clean_v1`
  - manifest：`metrics/manifests/full502_clean_v1.txt`
  - 输出：`metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
- 主比较表：`compare9_complete496_v1`
  - manifest：`metrics/manifests/compare9_complete496_v1.txt`
  - 输出：`metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`

`compare9_complete496_v1` 覆盖 `Ours + 8 baselines`，其中 `WWPF` 官方实现稳定输出 496 张，因此正式公平比较使用 496 complete-case。

`MS_SSIM` 和 `PSNR` 只能解释为增强结果相对原图的结构一致性，不是相对增强真值的质量指标。

## 4. Downstream 诊断事实

在 MyEdge 168 张带 GT split、fixed MSFI 50k 和 fixed DiffusionEdge baseline 50k 口径下，locked Stage1 `Final` 是 downstream negative control：它明显降低 ODS/OIS/AP/AC。

因此，不能写：

- Stage1 locked Final 已稳定提升下游边缘检测。
- Stage1 已证明 ODS/OIS/AP/AC 正向收益。
- structure proxy 可替代 ODS/OIS/AP/AC。

当前 168 张带 GT split 是 downstream validation 核心；502/496 只用于 Stage1 增强指标和 complete-case 对照；2770 full-pool 不能替代 168 downstream validation。

## 5. 候选治理状态

当前优先级是实验治理与候选归档，不是继续派生 P29/D02。

唯一候选总账：

- `metrics/registry_schema_cn.md`
- `metrics/experiment_registry.csv`
- `metrics/candidate_registry.csv`

当前候选边界：

- P12-P28：`diagnostic candidates / archived evidence`。
- P28：`pending_audit`，不得继续迭代。
- D01：`mechanism-complete weak diagnostic candidate`，不是 strong pass、正式增强主线或稳定下游收益。
- D01 没有达成原始“完整创新增强流程 + 明显视觉增强 + 增强指标竞争力 + 下游正收益”目标；后续纠偏入口是 `docs/evidence/full_flow_recovery/stage1_full_enhancement_mainline_recovery_plan_cn.md`。
- `full_flow_downstream_stage1_mainline_v1` 是当前纠偏中的完整增强主线恢复轨道；截至 2026-05-27，FF01/v8 已完成 168 fixed-detector validation，但 gate 为 `candidate_rescues_legacy_but_not_near_raw`，低于 raw 且弱于 P27/P28/D01，不能写成下游正收益，也不能进入 502/496 或 2770 作为 candidate-passing route。
- `full_flow_downstream_stage1_mainline_v2` / FF02 是 FF01 失败后的 detector-compatible 机制级重设计；它完成了 168 fixed-detector validation，但 gate 仍为 `candidate_rescues_legacy_but_not_near_raw`，结构 proxy 两路都 worse than raw。FF02 只能作为 diagnostic evidence，不能继续同族小修，也不能写成完整增强主线成功。
- `topology_locked_visual_chroma_full_flow_v1` / TLVC01 是 FA01 后的 topology-locked 完整流程纠偏候选；它修正了 MyEdge raw input mismatch，完成 168 fixed-detector validation，gate 仍为 `candidate_rescues_legacy_but_not_near_raw`。TLVC01 比 FF01/FF02 安全，但没有超过 P27/D01 的 DiffusionEdge AP 证据，不能写成下游正收益，也不能进入 502/496 或 2770 作为 candidate-passing route。
- FA01 已完成 failure audit、high-risk index、per-image correlation 和 visual/error-map review：`docs/evidence/fa01_family_audit/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`、`docs/evidence/fa01_family_audit/fa01_high_risk_sample_evidence_index_20260527_cn.md`、`docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527_cn.md`、`docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527_cn.md` 和 `docs/evidence/fa01_family_audit/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md` 是下一阶段入口；不得新增 FF03/P29/D02 作为同族小修。
- TLVC01 后的长期目标入口是 `docs/evidence/stage1_myedge_coupling/stage1_long_horizon_goal_after_tlvc01_20260527_cn.md`：保留完整 Stage1 增强流程，但从 direct replacement 转为 raw 主输入旁路的 sidecar evidence / auxiliary maps，再由 MyEdge/MSFI adaptation 验证正收益。
- 当前推荐路线是 MyEdge/MSFI sidecar adaptation protocol 草案与 no-training map export smoke：`docs/evidence/stage1_myedge_coupling/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`、`docs/evidence/stage1_myedge_coupling/stage1_sidecar_map_definition_fa01_20260527_cn.md`。它们不是 fixed-detector 结果，也不授权训练。
- `candidate_rescues_legacy_but_not_near_raw` 和 `candidate_metric_near_raw_structure_mixed` 都不能写成目标完成。

新增候选前必须先有 method review、run sheet、isolated output root、config、log、status、decision 和 registry entry。

## 6. 2770 Full-Pool 状态

`full_algae_dewatermark_v1` 来自 `D:\Desktop\去水印所有藻类图像`，当前角色是 cv2-readable full-pool candidate / qualitative engineering pool。

当前已知状态：

- 顶层图像文件：2777
- 默认候选 manifest：2774
- OpenCV 可读候选：2770
- 人工复核：544 条 pending
- clean manifest：未生成
- full2770 run intake：`not_started`

2770 不能写成正式 full-pool 结果，也不能替代 502/496 正式口径或 168 downstream validation。

## 7. 参考论文边界

两篇 Wu et al. 2026 HAB 论文是 nearest-neighbor / overlap-risk anchor：

- `Enhanced edge detection of harmful algal Blooms using diffusion probability models and Sobel-convolutional attention mechanisms`
- `Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network`

它们用于 HAB task framing、degradation analysis、enhancement-flow design、metric design 和写作边界参考。当前仓库未证明 Stage1 2777/2774/2770 与 ESWA 676 或 EAAI 1026 有文件级 overlap、同一 split、同一 GT 或同一统计口径。

## 8. 历史资产

以下资产可用于审计，不是当前正式入口：

- `results_optimized_c25`
- 旧 `full506` 评测目录
- `metrics/archive/`
- `AIlog/`
- `notion_mirror/`
- 旧 pilot / H2 / H3 草案

不删除这些资产，但论文和实验说明必须回到当前 formal source asset、502/496 paper metric、168 downstream diagnostic 和 registry。

## 9. 当前禁止写法

不要写：

- “全面领先 SOTA”
- “所有指标最优”
- “Stage1 已稳定提升下游边缘检测”
- “D01/P27 是正式成功候选”
- “2770 是正式 full-pool 结果”
- “Wu 2026 数据集与本项目已证明完全相同”
- “HLRP/Histoformer 原方法普遍无效”

可写：

- Stage1 提供可复现的 formal enhancement source asset。
- 502/496 增强指标已完成。
- locked Final 在 168 fixed-detector downstream 口径下是 negative control。
- P12-P28/D01 是诊断候选与归档证据。
- Stage1 当前更适合作为 MyEdge/MSFI 主论文的结构保持增强输入支撑。
