# Stage1Codex Evidence Navigation Index

更新时间：2026-05-27

本文件是 `docs/evidence/` 的导航索引。它只说明证据放在哪里、如何解释，不新增实验结论。

## 1. 根目录入口

根目录保留状态与治理入口：

- `docs/current_experiment_status_cn.md`：当前停止点和禁止写法。
- `docs/evidence_asset_inventory_cn.md`：资产分层与 claim 边界主表。
- `docs/project_handoff_guide_cn.md`：接手顺序与事实层级。
- `docs/project_status_overview_cn.md`：项目全局状态。
- `docs/cleanup_inventory_20260527_cn.md`：本次整理前证据冻结快照。

## 2. Evidence 子目录

| 目录 | 内容 | 解释边界 |
| --- | --- | --- |
| `docs/evidence/full_flow_recovery/` | Stage1 完整增强主线恢复计划、FF01/FF02 method design、失败审计入口 | 方法纠偏与失败证据，不是 downstream positive gain |
| `docs/evidence/fa01_family_audit/` | FA01 family-level failure audit、detector sensitivity hypotheses、high-risk index、correlation audit、visual/error-map review | 诊断与假设来源，不是新候选、训练结果或 fixed-detector 正收益 |
| `docs/evidence/stage1_myedge_coupling/` | MyEdge/MSFI sidecar adaptation protocol、Stage1 sidecar map definition、no-training sidecar smoke、TLVC01 后长期目标 | readiness / design evidence，不代表已训练或已验证 |
| `docs/evidence/tlvc01_topology_locked/` | TLVC01 method design 与 topology-locked proxy prescreen reports | TLVC01 是 rescue-only 纠偏证据，不是 candidate pass |
| `docs/evidence/e01_task_guided_family/` | E01 task-guided complete enhancement family design、E01-A/E01-B gate report、E01 family stage summary | E01-A/E01-B 均已归档为 failure / rescue-only；E01 family 本阶段完成两个机制不同 gate 但没有 downstream success |

## 3. 当前关键证据入口

- TLVC01 method design：`docs/evidence/tlvc01_topology_locked/topology_locked_visual_chroma_full_flow_v1_method_design_cn.md`
- TLVC01 proxy prescreen：`docs/evidence/tlvc01_topology_locked/proxy_prescreen/`
- TLVC01 Stage1 status：`experiments/topology_locked_visual_chroma_full_flow_v1/topology_locked_visual_chroma_full_flow_v1_fixed_detector_tlvc01_status_20260527.md`
- FF01 method design：`docs/evidence/full_flow_recovery/full_flow_downstream_stage1_mainline_v1_method_design_cn.md`
- FF02 method design：`docs/evidence/full_flow_recovery/full_flow_downstream_stage1_mainline_v2_method_design_cn.md`
- FA01 audit summary：`docs/evidence/fa01_family_audit/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
- FA01 sidecar protocol：`docs/evidence/stage1_myedge_coupling/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`
- Long-horizon goal：`docs/evidence/stage1_myedge_coupling/stage1_long_horizon_goal_after_tlvc01_20260527_cn.md`
- E01 family design：`docs/evidence/e01_task_guided_family/e01_task_guided_complete_enhancement_family_design_cn.md`
- E01-A method design：`docs/evidence/e01_task_guided_family/e01_a_color_illumination_task_guided_design_cn.md`
- E01-A fixed-detector gate report：`docs/evidence/e01_task_guided_family/e01_a_fixed_detector_gate_report_20260527_cn.md`
- E01-B method design：`docs/evidence/e01_task_guided_family/e01_b_wavelet_pyramid_weak_boundary_design_cn.md`
- E01-B fixed-detector gate report：`docs/evidence/e01_task_guided_family/e01_b_fixed_detector_gate_report_20260527_cn.md`
- E01 family stage summary：`docs/evidence/e01_task_guided_family/e01_family_stage_summary_20260527_cn.md`

## 4. Fixed Interpretation

- D01/P12-P28/FF01/FF02/TLVC01 都不能写成 strong pass 或稳定 downstream 正收益。
- FA01 visual/error-map review 与 sidecar smoke 不是新候选，也不是 MyEdge/MSFI adaptation 结果。
- E01-A 已完成 168 fixed-detector gate，但未达到 E01 minimum-safe：MSFI AC 超出 strict raw-near 容差；只能写成 failure / rescue-only，不能写成成功。
- E01-B 已完成 168 fixed-detector gate，但未达到 E01 acceptable success：DiffusionEdge AP 有正收益，MSFI AP 掉出 strict raw-near；只能写成 failure / rescue-only，不能写成成功。
- E01 family 本阶段已完成两个机制不同 candidate 的 168 gate，但没有强成功、可接受成功或最低安全 candidate。
- Proxy prescreen、structure proxy、readiness-only 和 2770 full-pool readiness 不能替代 168 fixed-detector downstream validation。
- 当前长期方向是 raw 主输入 + Stage1 sidecar evidence + MyEdge/MSFI adaptation；任何训练或 checkpoint 改动都需要单独授权。
