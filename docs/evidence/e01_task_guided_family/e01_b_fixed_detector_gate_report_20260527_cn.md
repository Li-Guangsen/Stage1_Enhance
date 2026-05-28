# E01-B 168 fixed-detector gate report

日期：2026-05-27

## 结论

E01-B `e01_b_wavelet_pyramid_weak_boundary_v1` 在 168 张带 GT split 上归档为 **failure / rescues legacy but not near raw**。

它不是强成功、不是可接受成功、也不是最低安全。主要原因是：E01-B 在 fixed DiffusionEdge baseline 50k 上取得 AP 正收益，但 fixed MSFI 50k 的 AP 为 `0.337598`，相对 raw anchor `0.345899` 下降 `0.008301`，明显超过预先锁定的 AP raw-near 容差 `0.003`。因此它不能满足“一个 detector positive，另一个 detector strict raw-near”的可接受成功条件。

Structure proxy 没有崩塌：两路 detector 的 dF1、dFalse-edge、dEndpoints/kpx 都在 E01 `not-collapsed` 容差内。但 DiffusionEdge 的 false-edge ratio 仍略高于 raw，MSFI AP 明显损失，说明 wavelet-pyramid weak-boundary 路线把部分弱边界信号推向 DiffusionEdge 可利用的排序收益，同时破坏了 MSFI 对 raw 分布的 AP 校准。

## 固定阈值口径

- Raw-near tolerance：ODS/OIS 不低于 raw `0.002`；AP/AC 不低于 raw `0.003`。
- Detector-positive：ODS 至少高于 raw `0.002` 或 AP 至少高于 raw `0.003`，且 AP/AC 保持 strict raw-near。
- Structure not-collapsed：dF1 >= `-0.005`，dFalse-edge <= `+0.010`，dEndpoints/kpx <= `+1.000`。

这些阈值已在运行 168 前写入 `experiments/e01_task_guided_family/run_sheet_e01_b.md`，本报告未根据结果回调阈值。

## Downstream 指标

| Detector | Raw ODS/OIS/AP/AC | Legacy Final ODS/OIS/AP/AC | E01-B ODS/OIS/AP/AC | E01 判定 |
|---|---:|---:|---:|---|
| MSFI 50k | `0.783527/0.794213/0.345899/0.796846` | `0.588287/0.671357/0.263997/0.740300` | `0.782154/0.793330/0.337598/0.795700` | rescues legacy; not strict raw-near because AP delta = `-0.008301` |
| DiffusionEdge baseline 50k | `0.770521/0.779986/0.363065/0.796900` | `0.530094/0.567910/0.224073/0.734900` | `0.770284/0.780779/0.372567/0.794800` | detector-positive by AP delta = `+0.009502`; AP/AC remain strict raw-near |

## Structure proxy

| Detector | dF1 | dFalse-edge | dEndpoints/kpx | E01 structure status |
|---|---:|---:|---:|---|
| MSFI 50k | `+0.0013` | `-0.0018` | `-0.2791` | not-collapsed and non-worse |
| DiffusionEdge baseline 50k | `-0.0014` | `+0.0036` | `-0.0882` | not-collapsed; not strict non-worse due false-edge increase |

## 相对历史候选

- 相对 raw：E01-B 不是整体 raw-near。DiffusionEdge baseline AP 有明确正收益，但 MSFI AP 低于 raw-near 阈值，不能写成可接受成功。
- 相对 legacy Stage1 Final：两路 detector 都大幅 rescue legacy Final 崩塌，但 rescue legacy 不能写成成功。
- 相对 E01-A：E01-B 明显提升 DiffusionEdge AP（`0.372567` vs `0.362762`），但牺牲 MSFI AP（`0.337598` vs `0.345966`）。E01-A 更接近 MSFI AP raw，E01-B 更偏 DiffusionEdge AP；二者都未达到 E01 minimum-safe。
- 相对当前最好 archived diagnostic reference P27：E01-B 未超过 P27 的整体 gate。P27 是 `candidate_metric_near_raw_structure_mixed`，E01-B 因 MSFI AP 掉出 raw-near 只能归档为 `candidate_rescues_legacy_but_not_near_raw`。E01-B 的 DiffusionEdge AP 略高于 P27，但 MSFI AP 明显更弱。
- 相对 FF01/FF02：E01-B 比 FF01/FF02 更接近 raw，且 structure proxy 没有 FF01/FF02 式崩塌；但它仍没有解决 fixed-detector 双路 raw-near/positive-gain 的核心约束。
- 相对 TLVC01：E01-B 有更强 DiffusionEdge AP，但 MSFI AP 比 TLVC01 更差，AC/structure trade-off 仍在；不能替代 TLVC01 的 topology-lock 诊断，也不能写成 downstream 正收益。

## 证据资产

- E01 family design：`docs/evidence/e01_task_guided_family/e01_task_guided_complete_enhancement_family_design_cn.md`
- E01-B method design：`docs/evidence/e01_task_guided_family/e01_b_wavelet_pyramid_weak_boundary_design_cn.md`
- E01-B run sheet：`experiments/e01_task_guided_family/run_sheet_e01_b.md`
- Smoke status：`experiments/e01_task_guided_family/e01_b_wavelet_pyramid_weak_boundary_v1_smoke7_highrisk_e01b_v1_status_20260527.md`
- Stage1 168 output status：`experiments/e01_task_guided_family/e01_b_wavelet_pyramid_weak_boundary_v1_myedge168_stage1_outputs_e01b_v1_status_20260527.md`
- MyEdge result intake：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/e01_b_wavelet_pyramid_weak_boundary_e01b_results_20260527.md`
- MyEdge structure proxy：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/e01_b_wavelet_pyramid_weak_boundary_e01b_structure_metrics_20260527.md`
- MyEdge gate aid：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/e01_b_wavelet_pyramid_weak_boundary_e01b_downstream_gate_20260527.md`

## 决策

E01-B 归档为失败候选，不做同一 primary hypothesis 的轻微参数、guard、fallback、raw pullback 或 topology-lock 修补。E01 family 已完成两个机制不同 candidate 的 168 fixed-detector gate，满足本阶段 family-level 阶段性完成条件，但没有产生强成功、可接受成功或最低安全 candidate。

当前不建议继续 E01-A/E01-B 小修。若继续 Stage1 direct image replacement，只应进入真正不同机制的 E01-C edge-aware structure route；但基于 E01-A/B、P27、FF01/FF02/TLVC01 的证据，更实际的下一步是把 raw 作为主输入，将 Stage1 输出转为 sidecar / auxiliary maps，并进入单独授权的 MyEdge/MSFI adaptation 设计。

边界：本阶段未运行 502/496、未运行 2770、未训练 MyEdge/MSFI adaptation；不得声称增强指标优于外部方法，不得声称形成正式增强指标主表。
