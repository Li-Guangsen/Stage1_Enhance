# full_flow_downstream_stage1_mainline_v1

## Purpose

FF01 恢复完整 Stage1 增强骨架：gray-pixel/BPH、IMF/frequency detail、WB-safe contrast、CLAHE visibility、direct weighted fusion 和 bounded selection。

## Status

- FF01/v8 已完成 Stage1 smoke、168 enhancement 和 fixed MSFI/DiffusionEdge validation。
- Gate 为 `candidate_rescues_legacy_but_not_near_raw`。
- 该路线救回 legacy Stage1 Final 崩塌，但两路 detector 仍低于 raw anchor，且 structure proxy worse than raw。

## Decision

`archive_diagnostic`。不得继续 FF01 同族小修，也不得进入 502/496 或 2770 作为 candidate-passing route。

## Evidence Links

- Method design: `docs/evidence/full_flow_recovery/full_flow_downstream_stage1_mainline_v1_method_design_cn.md`
- Run sheet: `experiments/full_flow_downstream_stage1_mainline_v1/run_sheet_v1.md`
- Config: `experiments/full_flow_downstream_stage1_mainline_v1/configs/full_flow_downstream_stage1_mainline_v1.json`
- Fixed-detector status: `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_fixed_detector_v8_status_20260527.md`
- MyEdge gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v1_v8_downstream_gate_20260527.md`
