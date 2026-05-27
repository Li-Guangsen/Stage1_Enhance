# full_flow_downstream_stage1_mainline_v2

## Purpose

FF02 是 FF01 失败后的 detector-compatible 机制级重设计，强调 color-structure decoupling、topology-compatible fusion 和 bounded closure。

## Status

- FF02 已完成 Stage1 smoke、168 enhancement 和 fixed MSFI/DiffusionEdge validation。
- Gate 仍为 `candidate_rescues_legacy_but_not_near_raw`。
- 相比 FF01 稍微降低部分 structure risk，但 ODS/OIS/AP 仍低于 raw，structure proxy 两路均 worse than raw。

## Decision

`archive_diagnostic`。不得继续 FF03 小修，也不得写成 downstream positive gain。

## Evidence Links

- Method design: `docs/evidence/full_flow_recovery/full_flow_downstream_stage1_mainline_v2_method_design_cn.md`
- Run sheet: `experiments/full_flow_downstream_stage1_mainline_v2/run_sheet_v1.md`
- Config: `experiments/full_flow_downstream_stage1_mainline_v2/configs/full_flow_downstream_stage1_mainline_v2.json`
- Fixed-detector status: `experiments/full_flow_downstream_stage1_mainline_v2/full_flow_downstream_stage1_mainline_v2_fixed_detector_ff02_status_20260527.md`
- MyEdge gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_downstream_gate_20260527.md`
