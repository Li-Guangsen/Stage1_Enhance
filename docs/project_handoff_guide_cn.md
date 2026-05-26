# 项目交接指南（中文）

更新时间：2026-05-27

本文件面向第一次接手 `Stage1Codex` 的人类或 AI。目标是用最少入口说明当前项目事实层级，避免把正式增强资产、paper metrics、downstream 诊断、候选归档和 2770 readiness 混在一起。

## 1. 先读什么

接手顺序：

1. `AGENTS.md`
2. `README.md`
3. `docs/project_execution_rules_cn.md`
4. `docs/current_experiment_status_cn.md`
5. `docs/evidence_asset_inventory_cn.md`
6. `metrics/experiment_registry.csv`
7. `metrics/candidate_registry.csv`
8. `docs/project_status_overview_cn.md`
9. `research-state.yaml`

涉及主表和 baseline 时，再读：

- `docs/comparison_methods_results_index_cn.md`
- `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502/mean_metrics_table.md`
- `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/mean_metrics_table.md`

涉及论文写作时，再读：

- `paper/underwater_image_enhancement_draft_cn.md`
- `paper/underwater_image_enhancement_evidence_pack_cn.md`
- `method-underwater-enhancement.md`
- `method-underwater-enhancement-paper-ready.md`
- `related-work-underwater-enhancement.md`

## 2. 当前一句话状态

Stage1Codex 已完成 formal enhancement source asset、502 阶段表和 496 complete-case 主比较；但 locked Stage1 `Final` 在 MyEdge 168 fixed-detector downstream 口径下是 negative control。P12-P28/D01 已归档为 downstream diagnostic candidates，没有 strong pass。当前应先做治理、归档、证据边界和 MyEdge/MSFI 主论文支撑，而不是继续派生 P29/D02。

## 3. Formal Source Asset vs Paper Metric

不要把路径名和论文样本口径混在一起。

| 层级 | 当前事实 |
| --- | --- |
| formal enhancement source asset | `experiments/optimization_v1/configs/locked_full506_final_mainline.json` |
| formal output root | `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline` |
| paper stage metric | `full502_clean_v1`，输出到 `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502` |
| paper comparison metric | `compare9_complete496_v1`，输出到 `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496` |

`full506_final_mainline` 只是源资产目录名，不是正式主表 count。

## 4. 方法阶段怎么说

正式增强流程：

`Original -> BPH -> IMF1Ray / RGHS / CLAHE -> Fused -> Final`

论文中必须按真实职责描述：

- `BPH`：灰像素引导的前置白平衡。
- `IMF1Ray`：IMF1-Rayleigh 高频细节分支。
- `RGHS`：白平衡安全对比分支，不是标准 RGHS。
- `CLAHE`：CLAHE 引导的局部可见性分支，不是直接输出普通 CLAHE。
- `Fused`：特征门控的三分支亮度结构融合。
- `Final`：轻量照明与对比收口。

## 5. Downstream 结论边界

当前 downstream 诊断只覆盖：

- MyEdge 168 张带 GT split
- fixed MSFI 50k
- fixed DiffusionEdge baseline 50k

已锁定结论：

- locked Stage1 `Final` 在该口径下明显降低 ODS/OIS/AP/AC。
- Raw 是当前 fixed-detector 强 anchor。
- Pxx/D01 可以写成相对 legacy Final 的 diagnostic recovery，但不能写成 Stage1-specific stable downstream improvement。
- Sobel/Otsu proxy、structure proxy、paired proxy 均为 `diagnostic only, not downstream accuracy`。

## 6. Candidate Governance

候选状态唯一事实源：

- `metrics/experiment_registry.csv`
- `metrics/candidate_registry.csv`

当前候选状态：

- P12-P28：diagnostic candidates / archived evidence。
- P28：pending audit，不得继续迭代。
- D01：mechanism-complete weak diagnostic candidate，不是 strong pass 或正式主线。

继续实验前必须满足：

- method review
- run sheet
- isolated output root
- config
- logs
- status
- decision
- registry entry

run sheet 模板：

- `docs/experiment_run_sheet_template_cn.md`

## 7. 2770 Full-Pool

`full_algae_dewatermark_v1` 当前只是 cv2-readable full-pool candidate / qualitative engineering pool。

已知状态：

- 2777 顶层图像文件
- 2774 默认候选
- 2770 OpenCV 可读候选
- 544 条人工复核 pending
- clean manifest 未生成
- full run intake 为 `not_started`

不能写成正式 full-pool result，也不能替代 168 downstream validation。

## 8. 两篇 Wu 2026 论文怎么用

两篇 Wu et al. 2026 HAB 论文只能作为 nearest-neighbor / overlap-risk anchor：

- ESWA 2026 HAB enhancement + diffusion edge reference
- EAAI 2026 task-oriented enhancement + segmentation reference

可借鉴：

- HAB 任务 framing
- degradation analysis
- enhancement-flow design
- metric design
- 写作边界和最近邻风险说明

不可写：

- 本项目与其数据集已经证明完全相同。
- 本项目使用同一 split、同一 GT 或同一统计口径。
- Stage1 2777/2774/2770 已证明覆盖 ESWA 676 或 EAAI 1026。

数据关系以 `docs/reference_dataset_relation_audit_20260525_cn.md` 为准。

## 9. 主表解释边界

主表保留 9 方法，不删除 `WWPF`、`HLRP` 或 `Histoformer`。

统一解释：

- `MS_SSIM` / `PSNR` 是相对原图结构一致性。
- `WWPF` 是激进但可接受的强基线，官方实现稳定输出 496 张。
- `HLRP` / `Histoformer` 只在当前 HAB 显微协议下作为失败案例或补充分析。
- `HVDualformer` / `ABC-Former` 是白平衡方法。

不能写“全面领先 SOTA”或“所有指标最优”。

## 10. 历史资产

以下内容可审计，但不是当前入口：

- `results_optimized_c25`
- 旧 `full506` 评测
- `metrics/archive/`
- `AIlog/`
- `notion_mirror/`
- 旧 pilot / H2 / H3 草案

不要删除这些资产；只需在导航和论文口径中明确它们不是当前正式事实源。

## 11. 下一步建议

1. 先把治理文件和 registry 纳入版本化项目记忆。
2. 使用 registry 审计 P12-P28/D01 的归档状态。
3. 人工冻结退化/失败案例子集。
4. 在 MyEdge 侧补 MSFI 组件消融、替换模块对比、效率和失败案例。
5. 若要继续 Stage1 候选，先写 method review 和 run sheet，不直接派生 P29/D02。
