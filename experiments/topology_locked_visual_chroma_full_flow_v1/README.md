# topology_locked_visual_chroma_full_flow_v1

## Purpose

TLVC01 是 FA01 后的 topology-locked visual-chroma full-flow correction。它保留 Stage1 完整视觉/色度增强证据，但把 Final gray/topology plane 锁回 exact MyEdge raw input，以隔离 raw-copy mismatch 和 topology drift 风险。

## Status

- TLVC01 修正了 Stage1 `data/inputImg/Original` 与 MyEdge raw anchor 不一致的问题。
- Valid 168 run 必须从 `D:/Desktop/MyEdgeCodex/input_test/algae` 生成。
- 168 输出完整，Final PNG/JPG 各 168，耗时约 92.9 秒。
- Gate 为 `candidate_rescues_legacy_but_not_near_raw`，不是 candidate pass。

## Decision

`archive_diagnostic`。TLVC01 比 FF01/FF02 安全，但没有超过 P27/D01 的 DiffusionEdge AP 证据；不得继续 TLVC02/FF03/P29/D02 小修。

## Evidence Links

- Method design: `docs/evidence/tlvc01_topology_locked/topology_locked_visual_chroma_full_flow_v1_method_design_cn.md`
- Run sheet: `experiments/topology_locked_visual_chroma_full_flow_v1/run_sheet_v1.md`
- Config: `experiments/topology_locked_visual_chroma_full_flow_v1/configs/topology_locked_visual_chroma_full_flow_v1.json`
- Fixed-detector status: `experiments/topology_locked_visual_chroma_full_flow_v1/topology_locked_visual_chroma_full_flow_v1_fixed_detector_tlvc01_status_20260527.md`
- Proxy prescreen: `docs/evidence/tlvc01_topology_locked/proxy_prescreen/`
- MyEdge gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_downstream_gate_20260527.md`
