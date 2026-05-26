# downstream_driven_v2 D01 方法设计与阶段审计

日期：2026-05-26

## 1. 定位

`downstream_driven_v2` 是在停止 P12-P28 本地 guard / fallback / raw-pullback 小步迭代后，新开的一条 Stage1 增强机制线。D01 `d01_structure_flow_v1` 的目标不是继续追求无参考增强指标，也不是把旧 `Final` 修补到 2770 full-pool，而是在 168 张 MyEdge 带 GT split 上验证一条面向边缘检测的结构保持增强流是否能避免旧 Stage1 `Final` 对固定检测器造成的下游崩塌。

D01 只作为非正式 downstream-driven 候选，不替代当前正式增强主线：

- 正式配置仍是 `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 正式结果仍是 `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 阶段增强指标正式口径仍是 `full502_clean_v1`
- 外部主表正式口径仍是 `compare9_complete496_v1`

## 2. 设计来源与边界

D01 参考了以下本地可见材料：

- `docs/downstream_driven_v1_method_design_inputs_20260526.md`
- `docs/downstream_driven_v1_method_design_synthesis_20260526_cn.md`
- `literature/wu2026_eswa_hab_edge_detection.md`
- `literature/wu2026_eaai_hab_segmentation.md`
- 既有正式 Stage1 链路与 P1-P28 下游诊断结果

Wu / Gengkun Wu / 吴庚坤相关 HAB 论文只作为 `anchor / nearest-neighbor / overlap-risk reference` 使用，用于 HAB task framing、退化分析、enhancement-flow design、metric design 和写作边界。D01 不直接复刻其增强流程，也不把候选文献和第一轮 pipeline 设计交给该作者群体主导。

## 3. P12-P28 家族审计结论

P12-P28 的共同价值是形成负向与控制证据，而不是提供可直接上 2770 的候选。

| 家族 | 代表 | 经验结论 |
|---|---|---|
| 多尺度/频域增强较强候选 | P12-P14 | 可救回旧 Final 崩塌，但 AP/AC 或 baseline false-edge/endpoints trade-off 明显。 |
| raw-near / skeleton / topology guarded 候选 | P15-P20 | 两检测器指标多能接近 raw，但 baseline-side 结构 proxy 仍 mixed。 |
| AC / false-edge / dual-anchor guard 候选 | P21-P26 | 能改善部分 ODS/OIS/AP 或 proxy，但常牺牲 MSFI AP、AC 或 baseline false-edge。 |
| raw-detail low-frequency chroma 候选 | P27/P28 | 是较好的 raw-near/control 证据，但仍不是 strong pass；P27/P28 只能作为 audit/control evidence。 |

由此得到 D01 设计约束：

- 不继续叠加局部 guard patch。
- 保留 raw high-frequency / luma structure 为主锚。
- BPH 只能提供受限的颜色/低频证据。
- 所有改变必须经过 edge/background/texture-risk mask 与 bounded selection。
- fixed-detector 下游指标和结构 proxy 同时作为 gate，不能只看增强指标。

## 4. D01 模块

代码入口：

- `main.py`
- `final.mode=downstream_d01_structure_flow_bph`
- 配置：`experiments/downstream_driven_v2/configs/d01_structure_flow_v1.json`

D01 的模块均可通过配置开关控制：

| 模块 | 开关 | 作用 |
|---|---|---|
| capped color consistency | `enable_color_consistency` | 对通道均值不一致做有上限的白平衡，不允许大幅漂移。 |
| low-frequency correction | `enable_lowfreq_correction` | 只在低频照明/色度层面吸收 BPH 证据。 |
| local contrast | `enable_local_contrast` | 使用低强度 gamma/contrast/CLAHE 候选，避免过增强。 |
| structure branch | `enable_structure_branch` | 多尺度 Gaussian residual 形成结构分支。 |
| edge-guided fusion | `enable_edge_guided_fusion` | 基于 raw 梯度、背景和纹理风险调节融合强度。 |
| false-edge suppression | `enable_false_edge_suppression` | 在低支撑/高风险背景区域回撤候选变化。 |
| light structure sharpen | `enable_structure_sharpen` | 极轻量结构锐化，避免生成厚边缘。 |
| bounded selection | `enable_bounded_selection` | 在 `[0.5, 0.75, 1.0]` 等候选强度中选择最安全输出。 |

D01 只依赖 `Original + BPH`，不会触发 IMF1Ray / RGHS / CLAHE / Fused / legacy Final 全链路计算。

## 5. 168 张执行资产

Stage1 输出：

- 输出目录：`experiments/downstream_driven_v2/outputs/myedge168/d01_structure_flow_v1`
- Final PNG：`168`
- Final JPG：`168`
- 本轮耗时记录：约 `24.04` 秒

MyEdge staging / fixed-detector 资产：

- staging：`D:/Desktop/MyEdgeCodex/stage1_coupling_inputs/downstream_v2_d01_structure_flow_v1_168_d01_20260526`
- MSFI config：`D:/Desktop/MyEdgeCodex/configs/stage1_coupling/msfi_downstream_v2_d01_structure_flow_v1_168_d01_20260526.yaml`
- DiffusionEdge baseline config：`D:/Desktop/MyEdgeCodex/configs/stage1_coupling/diffusionedge_baseline_downstream_v2_d01_structure_flow_v1_168_d01_20260526.yaml`
- WSL eval/show 脚本：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/run_d01_structure_flow_d01_eval_show_20260526.sh`

## 6. Stage1 proxy prescreen

报告入口：

- `docs/stage1_myedge168_gt_edge_proxy_prescreen_d01_20260526_cn.md`
- `docs/stage1_myedge168_gt_edge_proxy_prescreen_d01_20260526_cn.json`

D01 在 Stage1 image-gradient-to-GT proxy 中的结论：

- decision：`proxy_edge_safe_candidate`
- dF1：`+0.000590`
- dPrecision：`+0.000672`
- dRecall：`-0.000025`
- dFalse-edge：`-0.000672`
- dEndpoints/kpx：`+0.482890`
- dMeanAbsLuma：`+0.771249`

解释：D01 的 Stage1 proxy 基本 edge-safe，但 endpoints 变差；它只支持进入 fixed-detector 验证，不能替代 MyEdge ODS/OIS/AP/AC。

## 7. Fixed-detector 结果

MyEdge 结果入口：

- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/d01_structure_flow_d01_results_20260526.md`
- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/d01_structure_flow_d01_structure_metrics_20260526.md`
- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/d01_structure_flow_d01_downstream_gate_20260526.md`

| Detector | Input | ODS | OIS | AP | AC |
|---|---|---:|---:|---:|---:|
| MSFI 50k | raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI 50k | legacy Final | 0.588287 | 0.671357 | 0.263997 | 0.7403 |
| MSFI 50k | D01 | 0.783871 | 0.795067 | 0.346008 | 0.7934 |
| DiffusionEdge baseline 50k | raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline 50k | legacy Final | 0.530094 | 0.567910 | 0.224073 | 0.7349 |
| DiffusionEdge baseline 50k | D01 | 0.771730 | 0.783218 | 0.371149 | 0.7948 |

结构 proxy delta vs raw：

| Detector | dF1 | dPrecision | dRecall | dFalse-edge | dEndpoints/kpx | Structure |
|---|---:|---:|---:|---:|---:|---|
| MSFI 50k | +0.000343 | +0.013767 | -0.012194 | -0.013767 | -1.140514 | non-worse |
| DiffusionEdge baseline 50k | -0.000327 | -0.005265 | +0.004194 | +0.005265 | +0.353641 | mixed |

## 8. Gate 结论

脚本 strict gate：

- decision：`candidate_rescues_legacy_but_not_near_raw`
- MSFI：rescues legacy = true，near raw = false，structure non-worse = true
- DiffusionEdge baseline：rescues legacy = true，near raw = true，structure non-worse = false

面向当前 goal 的解释：

- D01 已形成完整机制与完整 168 fixed-detector 证据链。
- D01 明显救回 legacy Stage1 `Final` 对两个固定检测器的下游崩塌。
- D01 在 DiffusionEdge baseline 上达到 metric-near-raw，并且 AP 高于 raw anchor。
- D01 在 MSFI 上 ODS/OIS/AP 略高于 raw anchor，但 AC 比 raw 低 `0.003446`，略超当前 `0.003` near-raw 容差。
- D01 的 MSFI 结构 proxy 是 non-worse，但 baseline-side false-edge/endpoints 仍 mixed。

因此 D01 只能写成 **mechanism-complete weak diagnostic candidate**，不能写成 **strong result** 或 **Stage1 稳定下游收益**。

## 9. 与 P27/P28 的关系

D01 不是 P27/P28 的直接参数回调。P27/P28 是 raw-near/control 诊断；D01 是基于 v1 综合建议、HAB 对标论文风险和 P12-P28 失败经验重建的模块化结构流。

但就当前结果而言：

- P27 仍是较好的 raw-near 诊断候选之一。
- D01 的机制更完整、更便于后续模块消融。
- D01 尚未在 gate 上超过 P27/P28 成为 strong candidate。

## 10. 范围锁定

本轮没有运行：

- `full502_clean_v1`
- `compare9_complete496_v1`
- 2770 full-pool
- MyEdge 训练
- checkpoint 更新
- GT 或 eval protocol 修改

后续若继续 D02，应优先做模块消融式收缩，而不是继续 local guard patch：

1. 关闭/缩小 baseline-side false-edge 风险最高模块。
2. 比较 `enable_local_contrast`、`enable_structure_sharpen`、`enable_false_edge_suppression` 和 `enable_bounded_selection` 的独立作用。
3. 只有 D02 在 168 split 上同时满足双检测器 metric-near-raw 与双检测器 structure non-worse，再考虑 502/496 增强指标补跑。
4. 不应从 D01 gate 直接进入 2770 full-pool。
