# 当前实验状态与停止点

更新时间：2026-05-27

本文件是 Stage1Codex 当前实验状态的一页式事实入口。它用于阻止后续 agent 把弱候选、proxy、readiness 或 2770 资产准备误写成目标完成。

## 当前执行优先级

当前优先级是实验治理与候选归档，而不是继续派生新的 `Pxx/Dxx` 候选。新增候选前必须先完成 method review、run sheet、isolated output root、config、log、status 和 decision。

## 已锁定事实

- 旧 Stage1 `Final` 在 fixed DiffusionEdge baseline 50k 和 fixed MSFI 50k 下会明显损伤下游边缘检测，已经作为 legacy negative baseline 固定。
- Raw 输入是当前 fixed-detector 下游验证的强 anchor。
- P12-P28 是候选、对照、失败或诊断证据集合，不是正式增强主线。
- D01 `d01_structure_flow_v1` 是 `mechanism-complete weak candidate`，不是强通过，不是正式主线，也不能写成 Stage1 稳定提升下游。
- D01 没有达成原始“完整增强流程 + 明显视觉增强 + 增强指标竞争力 + 下游正收益”目标。它没有运行 502/496 外部增强对比，视觉上接近 raw，不能写成类似参考论文的完整创新增强流程。
- `candidate_rescues_legacy_but_not_near_raw`、`candidate_metric_near_raw_structure_mixed` 都不能标记为目标完成。
- 2770 full-pool readiness 只说明工程入口可准备，不等于 downstream validation。

## 目标纠偏

当前需要纠正上一轮 downstream-driven 工作的目标偏差：后续目标不是继续生成 raw-near、guard、fallback 或 raw-pullback 小候选，而是重新设计一条保留 Stage1 原始创新骨架的完整增强主线。

新的长期目标入口：

- `docs/stage1_full_enhancement_mainline_recovery_plan_cn.md`
- `docs/stage1_full_flow_failure_audit_and_next_goal_20260527_cn.md`
- `docs/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
- `docs/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md`
- `docs/fa01_high_risk_sample_evidence_index_20260527_cn.md`
- `docs/fa01_per_image_correlation_audit_20260527_cn.md`
- `docs/fa01_visual_error_map_review_20260527_cn.md`
- `docs/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`
- `docs/stage1_sidecar_map_definition_fa01_20260527_cn.md`
- `docs/stage1_long_horizon_goal_after_tlvc01_20260527_cn.md`
- `docs/full_flow_downstream_stage1_mainline_v1_method_design_cn.md`
- `experiments/full_flow_downstream_stage1_mainline_v1/run_sheet_v1.md`
- `docs/topology_locked_visual_chroma_full_flow_v1_method_design_cn.md`
- `experiments/topology_locked_visual_chroma_full_flow_v1/run_sheet_v1.md`

后续新主线必须从灰像素白平衡、IMF/频域细节、多分支可见性/对比、特征门控融合和滤波收口等完整增强流程出发，同时加入 downstream-aware 约束。若视觉增强接近 raw 或没有 502/496 增强指标对照潜力，不得写成完整增强主线。

当前已新增隔离代码入口：

- `stage1_full_flow_mainline.py`
- `experiments/full_flow_downstream_stage1_mainline_v1/configs/full_flow_downstream_stage1_mainline_v1.json`
- `main.py final.mode=full_flow_downstream_stage1_mainline_v1`
- `experiments/full_flow_downstream_stage1_mainline_v2/configs/full_flow_downstream_stage1_mainline_v2.json`
- `main.py final.mode=full_flow_downstream_stage1_mainline_v2`
- `experiments/topology_locked_visual_chroma_full_flow_v1/configs/topology_locked_visual_chroma_full_flow_v1.json`
- `main.py final.mode=topology_locked_visual_chroma_full_flow_v1`

该入口已完成 Stage1-only smoke、168 Stage1 增强和 fixed-detector validation。结论不是成功：`full_flow_downstream_stage1_mainline_v1_v8` 的 gate 为 `candidate_rescues_legacy_but_not_near_raw`，救回 legacy Stage1 Final 崩塌，但两路 fixed detector 都明显低于 raw anchor，不能写成完整增强主线成功或下游正收益。

当前 full-flow v8 停止点：

- `smoke5_v1` 证明 aggressive IMF 完整流程过慢且有 `tama.14` 背景块状伪边，禁止进入 168。
- `smoke5_fast_imf_v2` 把速度压到约 `0.64` 秒/张，但 `tama.14` Final grad ratio 仍约 `2.131`，视觉风险未解除。
- `smoke5_fast_imf_v3-v6` 验证局部 support/pullback 和低块感 RGHS/CLAHE 调整，均未稳定消除背景伪结构，不能作为 168 输入。
- `smoke5_fast_imf_v7` 新增 `direct_weighted` 融合后端，说明 Fused 可压住 `tama.14` 伪边，但 entropy final closure 会重新引入背景伪结构。
- `smoke5_fast_imf_v8` 当前作为下一步 broader smoke 版本：关闭 entropy final closure，保留 `BPH -> IMF/RGHS/CLAHE branches -> direct_weighted fusion -> bounded selection`；5 张输出完整，耗时约 `3.0` 秒，外推 168 约 `1.7` 分钟，平均 Final BGR delta `6.8792`、L delta `1.0740`、grad ratio `1.0628`、luma std ratio `1.0273`。
- `smoke25_fast_imf_v8` 已完成 25 张 broader Stage1-only smoke：25 张 x 6 stages 的 JPG/PNG 均完整，耗时约 `11.6` 秒，外推 168 约 `1.3` 分钟，平均 Final BGR delta `7.0538`、L delta `1.0849`、grad ratio `1.0366`、luma std ratio `1.0443`，最高 grad ratio 约 `1.099`。抽查高风险 panel 后，未见 v1-v7 的大块背景伪结构，但视觉增强偏保守。
- `myedge168_v8` 已完成 168 张 Stage1 输出：Final PNG/JPG 各 `168`，decode 失败 `0`，耗时约 `74.9` 秒，平均 BGR delta `8.6772`、L delta `2.0101`、grad ratio `1.0646`、luma std ratio `1.0798`。但 `weixiaoyuanjia.21` Final grad ratio 约 `1.9137`，提示完整流程仍会放大 detector-sensitive 背景纹理。
- fixed MSFI 50k 结果为 ODS/OIS/AP/AC `0.739726/0.753251/0.310442/0.790100`，相对 raw 分别为 `-0.043801/-0.040962/-0.035457/-0.006746`。
- fixed DiffusionEdge baseline 50k 结果为 ODS/OIS/AP/AC `0.717475/0.727626/0.336548/0.794400`，相对 raw 分别为 `-0.053046/-0.052360/-0.026517/-0.002500`。
- structure proxy 两个 detector 都不是 non-worse：MSFI dF1 `-0.053426`、dFalse-edge `+0.079593`、dEndpoints `+1.891529`；DiffusionEdge baseline dF1 `-0.067472`、dFalse-edge `+0.095084`、dEndpoints `+4.291561`。
- MyEdge evidence files: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v1_v8_results_20260527.md`、`full_flow_downstream_stage1_mainline_v1_v8_structure_metrics_20260527.md`、`full_flow_downstream_stage1_mainline_v1_v8_downstream_gate_20260527.md`。
- Stage1 conclusion file: `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_fixed_detector_v8_status_20260527.md`。
- FF01/v8 低于 P27/P28 的 `candidate_metric_near_raw_structure_mixed` 证据，也弱于或不优于 D01；不得进入 502/496 或 2770 作为 candidate-passing route。

当前 FF02 detector-compatible full-flow 停止点：

- FF02 是 FF01/v8 失败后的机制级重设计，不是阈值/guard/fallback/raw-pullback 小修；它保留灰像素颜色形成、IMF/频域 detail evidence、WB-safe contrast、CLAHE visibility、color/structure decoupling、topology-compatible fusion 和 bounded closure。
- `smoke25_v1` 已完成：25 张 x 6 stages 的 JPG/PNG 均完整，decode 失败 `0`，耗时约 `11.6` 秒，平均 BGR delta `9.2405`、L delta `0.9906`、chroma delta `6.4325`、grad ratio `0.9331`、luma std ratio `1.0041`；抽查 panel 未见 FF01/v1-v7 式大块背景伪结构。
- `myedge168_v1` 已完成 168 张 Stage1 输出：Final PNG/JPG 各 `168`，decode 失败 `0`，耗时约 `77.5` 秒，平均 BGR delta `11.7138`、L delta `1.3708`、chroma delta `7.9785`、PSNR `27.2740`、grad ratio `0.9450`、luma std ratio `1.0132`。但 `tama.14`、`weixiaoyuanjia.21` 等 high-risk 样本仍提示 detector-sensitive 结构风险。
- fixed MSFI 50k 结果为 ODS/OIS/AP/AC `0.737952/0.751109/0.303208/0.792000`，相对 raw 分别为 `-0.045575/-0.043104/-0.042691/-0.004846`。
- fixed DiffusionEdge baseline 50k 结果为 ODS/OIS/AP/AC `0.711020/0.720141/0.320951/0.794000`，相对 raw 分别为 `-0.059501/-0.059845/-0.042114/-0.002900`。
- structure proxy 两个 detector 都不是 non-worse：MSFI dF1 `-0.0507`、dFalse-edge `+0.0734`、dEndpoints `+2.0630`；DiffusionEdge baseline dF1 `-0.0666`、dFalse-edge `+0.0890`、dEndpoints `+3.7585`。
- MyEdge evidence files: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_results_20260527.md`、`full_flow_downstream_stage1_mainline_v2_ff02_structure_metrics_20260527.md`、`full_flow_downstream_stage1_mainline_v2_ff02_downstream_gate_20260527.md`。
- Stage1 conclusion file: `experiments/full_flow_downstream_stage1_mainline_v2/full_flow_downstream_stage1_mainline_v2_fixed_detector_ff02_status_20260527.md`。
- FF02 的 gate 仍为 `candidate_rescues_legacy_but_not_near_raw`。它比 FF01 稍微降低 structure proxy 风险，但 ODS/OIS/AP 反而更差；不得进入 502/496 或 2770 作为 candidate-passing route。

当前 TLVC01 topology-locked visual-chroma full-flow 停止点：

- TLVC01 是 FA01 之后的纠偏候选，不是 FF03/P29/D02 小修；它保留灰像素/BPH、IMF/频域、多分支融合和 bounded closure，但把 Final 的 gray/topology plane 锁回 exact MyEdge raw input，以测试“完整视觉/色度增强 + raw-compatible luma topology”。
- 重要协议修正：168 fixed-detector 候选必须从 `D:/Desktop/MyEdgeCodex/input_test/algae` 生成。使用 Stage1 仓库 `data/inputImg/Original` 会产生 raw-copy mismatch，并导致 proxy 假失败。
- `myedge168_v1_myedgeinput_grayplane090_anchorfix` 已完成 168 张 Stage1 输出：Final PNG/JPG 各 `168`，decode 失败 `0`，耗时约 `92.9` 秒；Final mean BGR/L/chroma delta 为 `10.7667/1.7113/7.3842`，grad ratio `0.9956`，luma std ratio `1.0000`。
- Stage1/MyEdge168 GT edge proxy 与 raw 完全一致：F1 `0.581331`、false-edge ratio `0.523693`、endpoints/kpx `56.100962`，这只是 fixed-detector 安全预筛，不是下游收益。
- fixed MSFI 50k 为 `0.782936/0.794718/0.345209/0.793200`，接近 raw，但 MSFI AC 低于 strict raw-near 容差。
- fixed DiffusionEdge baseline 50k 为 `0.768593/0.779518/0.362225/0.798500`，指标接近 raw，但 structure proxy mixed：dF1 `-0.0030`、dFalse-edge `+0.0047`、dEndpoints `+0.3836`。
- MyEdge evidence files: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_results_20260527.md`、`topology_locked_visual_chroma_tlvc01_structure_metrics_20260527.md`、`topology_locked_visual_chroma_tlvc01_downstream_gate_20260527.md`。
- Stage1 conclusion file: `experiments/topology_locked_visual_chroma_full_flow_v1/topology_locked_visual_chroma_full_flow_v1_fixed_detector_tlvc01_status_20260527.md`。
- TLVC01 的 gate 是 `candidate_rescues_legacy_but_not_near_raw`。它比 FF01/FF02 安全，但没有超过 P27/D01 的 DiffusionEdge AP 证据；不得进入 502/496 或 2770 作为 candidate-passing route。

## 数据口径

| 口径 | 当前用途 | 不能替代什么 |
| --- | --- | --- |
| 168 张带 GT split | fixed DiffusionEdge/MSFI 下游验证核心口径 | 不能被 502/496 或 2770 替代 |
| full502_clean_v1 | Stage1 正式小口径增强指标、阶段输出和历史主线资产 | 不能替代下游边缘验证 |
| compare9_complete496_v1 | 与外部增强方法 complete-case 对照 | 不能替代下游边缘验证 |
| 2770/cv2-readable full-pool | 工程稳定性、qualitative pool、后续可选全量增强 | clean protocol 未冻结前不能作为正式统计结果 |

## 当前停止点

当前停止点是 FF01/v8、FF02 与 TLVC01 均已归档为 diagnostic failure / rescue-only。下一步不能继续给 full-flow / topology-lock family 做小幅 threshold、guard、fallback 或 raw-pullback 修补；也不能把 TLVC01 写成完整增强主线成功。有效下一步只有两类：一是提出真正不同的新方法族并先过 method review；二是承认 fixed detector 当前更偏好 raw 分布，把 Stage1 完整增强证据改为 sidecar / auxiliary maps，并把正向收益目标转向 MyEdge/MSFI 侧适配。502/496 和 2770 仍阻塞，除非后续明确作为失败分析对照而非候选通过路径。

FA01 当前进度：

- WP1 family-level failure audit 已完成只读聚合，入口为 `docs/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`。
- 机器可读表位于 `docs/fa01_stage1_full_flow_family_audit_tables_20260527/`，覆盖 fixed-detector 主指标、structure proxy、168 raw-vs-Final enhancement proxy、502/496 边界。
- WP2 detector-sensitivity hypotheses 已预注册，入口为 `docs/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md`。
- high-risk sample evidence index 已完成，入口为 `docs/fa01_high_risk_sample_evidence_index_20260527_cn.md`，覆盖 `57` 个增强风险与 detector-adverse stems。
- per-image correlation audit 已完成，入口为 `docs/fa01_per_image_correlation_audit_20260527_cn.md`。结论：单一增强 proxy 无法解释 FF01/FF02 失败，FF02 在 mean grad ratio 低于 `1` 时仍掉 ODS/AP，色度/低频分布迁移、局部 topology drift 和 raw-distribution bias 需要联合解释。
- high-risk visual/error-map review 已完成，入口为 `docs/fa01_visual_error_map_review_20260527_cn.md`，生成 `11` 个重点样本 panel 和 pattern tag 表。它只整理既有证据，不是新候选或 detector rerun。
- MyEdge/MSFI sidecar adaptation protocol 草案已写入 `docs/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`，但未授权训练、未执行 adaptation。
- Stage1 sidecar map definition 与 no-training export smoke 已完成，入口为 `docs/stage1_sidecar_map_definition_fa01_20260527_cn.md`；5 个样本导出 topology anchor、color compensation、frequency detail、visibility、luma risk、false-edge risk 和 weak-boundary support maps。它只是导出准备，不是 downstream gain。
- 当前仍不新增 FF03/P29/D02。
