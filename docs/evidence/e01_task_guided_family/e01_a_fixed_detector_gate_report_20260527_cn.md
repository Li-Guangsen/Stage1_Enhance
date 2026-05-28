# E01-A 168 fixed-detector gate report

日期：2026-05-27

## 结论

E01-A `e01_a_color_illumination_task_guided_v1` 在 168 张带 GT split 上归档为 **failure / rescues legacy but misses E01 minimum-safe by MSFI AC**。

这不是强成功、不是可接受成功、也不是最低安全。原因是：按 E01 run sheet 预先锁定的 raw-near tolerance，MSFI 的 AC 为 `0.793000`，相对 raw anchor `0.796846` 下降 `0.003846`，超过允许下降 `0.003`。DiffusionEdge baseline 满足 raw-near；两路 structure proxy 均未崩，但 E01 最低安全要求两个 detector 都严格 raw-near。

## 固定阈值口径

- Raw-near tolerance：ODS/OIS 不低于 raw `0.002`；AP/AC 不低于 raw `0.003`。
- Detector-positive：ODS 至少高于 raw `0.002` 或 AP 至少高于 raw `0.003`，且 AP/AC 保持 strict raw-near。
- Structure not-collapsed：dF1 >= `-0.005`，dFalse-edge <= `+0.010`，dEndpoints/kpx <= `+1.000`。

这些阈值已在运行 168 前写入 `experiments/e01_task_guided_family/run_sheet_e01_a.md`，本报告未根据结果回调阈值。

## Downstream 指标

| Detector | Raw ODS/OIS/AP/AC | Legacy Final ODS/OIS/AP/AC | E01-A ODS/OIS/AP/AC | E01 判定 |
|---|---:|---:|---:|---|
| MSFI 50k | `0.783527/0.794213/0.345899/0.796846` | `0.588287/0.671357/0.263997/0.740300` | `0.782764/0.794572/0.345966/0.793000` | rescues legacy; not strict raw-near because AC delta = `-0.003846` |
| DiffusionEdge baseline 50k | `0.770521/0.779986/0.363065/0.796900` | `0.530094/0.567910/0.224073/0.734900` | `0.769800/0.780356/0.362762/0.794900` | strict raw-near; no positive gain |

## Structure proxy

| Detector | dF1 | dFalse-edge | dEndpoints/kpx | E01 structure status |
|---|---:|---:|---:|---|
| MSFI 50k | `+0.0011` | `-0.0106` | `-1.6609` | not-collapsed and non-worse |
| DiffusionEdge baseline 50k | `-0.0019` | `+0.0047` | `+0.5710` | not-collapsed; not non-worse |

## 相对历史候选

- 相对 raw：E01-A 未取得 detector-positive。DiffusionEdge baseline raw-near；MSFI 因 AC 超阈值未达到 strict raw-near。
- 相对 legacy Stage1 Final：两路 detector 都大幅 rescue legacy Final 崩塌，但 rescue legacy 不能写成成功。
- 相对 FF01/FF02：E01-A 明显更接近 raw，且 structure proxy 不崩；但仍没有达到 E01 minimum-safe。
- 相对 TLVC01 / 当前最安全 archived diagnostic reference：E01-A 与 TLVC01 同属 rescue-only / near-raw 边缘状态；E01-A 的 DiffusionEdge ODS/OIS/AP 略高于 TLVC01，但 AC 更低，不能据此写成稳定收益。

## 证据资产

- E01 family design：`docs/evidence/e01_task_guided_family/e01_task_guided_complete_enhancement_family_design_cn.md`
- E01-A method design：`docs/evidence/e01_task_guided_family/e01_a_color_illumination_task_guided_design_cn.md`
- E01-A run sheet：`experiments/e01_task_guided_family/run_sheet_e01_a.md`
- Smoke status：`experiments/e01_task_guided_family/e01_a_color_illumination_task_guided_v1_smoke7_highrisk_v1_status_20260527.md`
- Stage1 168 output status：`experiments/e01_task_guided_family/e01_a_color_illumination_task_guided_v1_myedge168_stage1_outputs_v1_status_20260527.md`
- MyEdge result intake：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/e01_a_color_illumination_task_guided_e01a_results_20260527.md`
- MyEdge structure proxy：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/e01_a_color_illumination_task_guided_e01a_structure_metrics_20260527.md`
- MyEdge old gate aid：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/e01_a_color_illumination_task_guided_e01a_downstream_gate_20260527.md`

## 决策

E01 family 不应停止，也不应把 E01-A 做成低幅度 raw-near 修补。下一步应继续机制不同的 E01-B：multi-scale / pyramid / wavelet fusion dominant candidate。E01-A 的 color-illumination primary hypothesis 暂不做机制级修正，除非后续 E01-B/E01-C 显示完整增强 family 普遍只差 AC raw-near。

边界：本阶段未运行 502/496、未运行 2770、未训练 MyEdge/MSFI adaptation；不得声称增强指标优于外部方法，不得声称形成正式增强指标主表。
