# full_flow_downstream_stage1_mainline_v1 v8 fixed-detector status

日期：2026-05-27

## 结论

`full_flow_downstream_stage1_mainline_v1_v8` 已完成 168 张 MyEdge ALGAE split 的 Stage1 增强、fixed MSFI 50k / fixed DiffusionEdge baseline 50k 采样、WSL `eval.py` / `show.py`、result intake、structure proxy 和 downstream gate。

严格结论：`candidate_rescues_legacy_but_not_near_raw`。它救回了旧 Stage1 Final 的下游崩塌，但没有达到 raw-near，更没有证明完整增强流程带来明确下游正收益。当前版本不能进入 502/496 enhancement comparison 或 2770 readiness/full-pool enhancement，除非后续明确作为 failure-analysis 对照而非候选通过路径。

## 方法版本

- candidate id: `FF01`
- variant: `full_flow_downstream_stage1_mainline_v1_v8`
- code entry: `main.py final.mode=full_flow_downstream_stage1_mainline_v1`
- module: `stage1_full_flow_mainline.py`
- config: `experiments/full_flow_downstream_stage1_mainline_v1/configs/full_flow_downstream_stage1_mainline_v1.json`
- Stage1 output root: `experiments/full_flow_downstream_stage1_mainline_v1/outputs/myedge168/full_flow_downstream_stage1_mainline_v1_v8`
- Stage1 status: `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_myedge168_v8_status_20260527.md`

## Stage1 168 输出

| Item | Value |
|---|---:|
| Expected images | 168 |
| Final PNG | 168 |
| Final JPG | 168 |
| Decode failures | 0 |
| Runtime total | 74.9 sec |
| Sec / image | 0.45 |
| Mean BGR delta | 8.6772 |
| Mean L delta | 2.0101 |
| Mean chroma delta | 5.8024 |
| Mean grad ratio | 1.0646 |
| Mean luma std ratio | 1.0798 |

高风险样本包括 `weixiaoyuanjia.21`，其 Final grad ratio 约 `1.9137`，说明完整流程的颜色/可见性分支仍可能放大背景纹理或 detector-sensitive pseudo structure。

## Fixed-detector 结果

| Detector | Variant | ODS | OIS | AP | AC |
|---|---|---:|---:|---:|---:|
| MSFI 50k raw anchor | raw | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI 50k legacy Stage1 Final | legacy | 0.588287 | 0.671357 | 0.263997 | 0.740300 |
| MSFI 50k FF01/v8 | full-flow v8 | 0.739726 | 0.753251 | 0.310442 | 0.790100 |
| DiffusionEdge baseline raw anchor | raw | 0.770521 | 0.779986 | 0.363065 | 0.796900 |
| DiffusionEdge baseline legacy Stage1 Final | legacy | 0.530094 | 0.567910 | 0.224073 | 0.734900 |
| DiffusionEdge baseline FF01/v8 | full-flow v8 | 0.717475 | 0.727626 | 0.336548 | 0.794400 |

Delta vs raw:

| Detector | dODS | dOIS | dAP | dAC |
|---|---:|---:|---:|---:|
| MSFI 50k | -0.043801 | -0.040962 | -0.035457 | -0.006746 |
| DiffusionEdge baseline 50k | -0.053046 | -0.052360 | -0.026517 | -0.002500 |

## Structure proxy

| Detector | dF1 | dPrecision | dRecall | dFalse-edge | dComponents | dEndpoints |
|---|---:|---:|---:|---:|---:|---:|
| MSFI 50k | -0.053426 | -0.079593 | -0.016788 | +0.079593 | +0.147606 | +1.891529 |
| DiffusionEdge baseline 50k | -0.067472 | -0.095084 | -0.028845 | +0.095084 | +0.599154 | +4.291561 |

结构 proxy 不是非劣，两个 detector 都显示 F1/precision 下降、false-edge ratio 上升、endpoints 上升。

## 与 P27/P28/D01 的关系

- P27 gate: `candidate_metric_near_raw_structure_mixed`，两个 detector metric-near-raw；FF01/v8 低于 P27。
- P28 gate: `candidate_metric_near_raw_structure_mixed`，两个 detector metric-near-raw；FF01/v8 低于 P28。
- D01 gate: `candidate_rescues_legacy_but_not_near_raw`；FF01/v8 同属 rescue-only，但 MSFI/DiffusionEdge 指标和结构 proxy 均弱于 D01。
- 因此 FF01/v8 不是当前最好下游候选，也不能作为 D01 的成功替代。

## Evidence files

- MyEdge result intake: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v1_v8_results_20260527.md`
- MyEdge structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v1_v8_structure_metrics_20260527.md`
- MyEdge downstream gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v1_v8_downstream_gate_20260527.md`
- MSFI output root: `D:/Desktop/MyEdgeCodex/output_test/stage1_coupling/msfi_50k/full_flow_downstream_full_flow_downstream_stage1_mainline_v1_v8_168_ffds_v8_20260527`
- DiffusionEdge output root: `D:/Desktop/MyEdgeCodex/output_test/stage1_coupling/diffusionedge_baseline_50k/full_flow_downstream_full_flow_downstream_stage1_mainline_v1_v8_168_ffds_v8_20260527`

## Decision

- archive status: `archive_diagnostic`
- may iterate: `no`, unless the next step is a method-level redesign rather than threshold/guard/pullback tuning.
- 502/496: blocked for candidate-promotion purposes.
- 2770: blocked.
- next technical direction: analyze why the full enhancement branches cause detector distribution shift, then decide whether to redesign the flow around detector-compatible feature formation or stop Stage1 enhancement as a downstream-gain claim.
