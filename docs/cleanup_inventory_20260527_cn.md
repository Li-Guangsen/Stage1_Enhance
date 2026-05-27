# Stage1Codex 整理前证据冻结快照

更新时间：2026-05-27

本文件记录目录整理前的工作区状态和证据边界。它用于给后续移动、归档和索引重建提供可回滚锚点；不新增实验结论，不覆盖旧结果，不删除任何证据资产。

## 1. 工作区状态

整理前只读盘点结论：

- `docs/`：约 161 个文件、6 个子目录。
- `experiments/`：13 个实验目录。
- `git status --short --untracked-files=all`：约 1577 条变更记录。
- 已修改 tracked 文件：13 个，覆盖 `AGENTS.md`、`README.md`、状态文档、registry、`main.py`、脚本、`research-state.yaml` 和 `research-log.md`。
- 新增 docs 证据主要来自 FA01、FF01/FF02/TLVC01、proxy prescreen 和 long-horizon plan。
- 新增 experiments 证据主要来自 `full_flow_downstream_stage1_mainline_v1`、`full_flow_downstream_stage1_mainline_v2` 和 `topology_locked_visual_chroma_full_flow_v1`。

生成图像处理原则：

- `experiments/**/outputs/**` 仍按 `.gitignore` 保持本地生成资产，不纳入版本库。
- `experiments/**/diagnostics/**/*.jpg|jpeg|png` 是本地诊断面板，约 121 MB，本轮只保留在工作区，不纳入版本库。
- `docs/evidence/stage1_myedge_coupling/fa01_stage1_sidecar_map_smoke_20260527/` 与 `docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/` 是小型证据包，可作为 FA01 可见证据纳入版本化记忆。

## 2. 证据批次分组

### TLVC01

TLVC01 是 topology-locked visual-chroma 完整流程纠偏证据，不是 downstream positive gain。

Stage1 侧主要入口：

- `docs/evidence/tlvc01_topology_locked/topology_locked_visual_chroma_full_flow_v1_method_design_cn.md`
- `experiments/topology_locked_visual_chroma_full_flow_v1/run_sheet_v1.md`
- `experiments/topology_locked_visual_chroma_full_flow_v1/configs/topology_locked_visual_chroma_full_flow_v1.json`
- `experiments/topology_locked_visual_chroma_full_flow_v1/topology_locked_visual_chroma_full_flow_v1_fixed_detector_tlvc01_status_20260527.md`
- `docs/evidence/tlvc01_topology_locked/proxy_prescreen/stage1_myedge168_gt_edge_proxy_prescreen_topology_locked_visual_chroma_v1_myedgeinput_grayplane090_anchorfix_20260527_cn.md`

MyEdge 侧固定 detector 证据入口：

- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_results_20260527.md`
- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_structure_metrics_20260527.md`
- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_downstream_gate_20260527.md`

固定结论：

- TLVC01 修正了 MyEdge raw input mismatch。
- 168 输出完整，耗时约 92.9 秒，Final PNG/JPG 各 168。
- gate 为 `candidate_rescues_legacy_but_not_near_raw`。
- TLVC01 不能写成下游正收益、candidate pass、502/496 推广入口或 2770 full-pool 推广入口。

### FA01

FA01 是 family-level failure audit 和 sidecar export preparation，不是新候选、训练结果或 fixed-detector 正收益证据。

主要入口：

- `docs/evidence/fa01_family_audit/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
- `docs/evidence/fa01_family_audit/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md`
- `docs/evidence/fa01_family_audit/fa01_high_risk_sample_evidence_index_20260527_cn.md`
- `docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527_cn.md`
- `docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527_cn.md`
- `docs/evidence/stage1_myedge_coupling/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`
- `docs/evidence/stage1_myedge_coupling/stage1_sidecar_map_definition_fa01_20260527_cn.md`

固定结论：

- FA01 汇总 FF01/FF02/P27/D01 的 failure pattern、detector sensitivity 和 sidecar map export path。
- FA01 未授权 MyEdge training/adaptation。
- FA01 sidecar smoke 只验证可导出 map，不是 downstream gain。

### FF01/FF02/D01/P12-P28

这些结果只能作为 archived diagnostic evidence。

- D01：`mechanism-complete weak diagnostic candidate`，未达成完整创新增强流程、明显视觉增强、增强指标竞争力或下游正收益。
- FF01/FF02：完整增强主线恢复轨道的诊断失败证据，均为 `candidate_rescues_legacy_but_not_near_raw`。
- P12-P28：候选、对照、失败或诊断证据集合，不是正式增强主线。

## 3. 下一主线边界

当前下一主线不是 TLVC02/FF03/P29/D02 小修，也不是继续堆 guard/fallback/raw-pullback 候选。

当前推荐方向是：

- 保留 Stage1 完整增强流程的可解释模块和 sidecar evidence maps。
- 保持 raw 作为 MyEdge/MSFI 主输入。
- 将 Stage1 输出作为 auxiliary evidence / risk maps / weak-boundary support maps。
- 在得到明确授权后，才进入 MyEdge/MSFI adaptation training 或 ablation。

未授权事项：

- 不改 MyEdge checkpoint。
- 不重训 DiffusionEdge/MSFI。
- 不改 GT、eval protocol 或 existing output_test 资产。
- 不把 proxy-only、readiness-only 或 2770 readiness 写成下游正收益。
