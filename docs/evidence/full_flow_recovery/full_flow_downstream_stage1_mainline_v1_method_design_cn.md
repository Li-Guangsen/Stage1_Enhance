# full_flow_downstream_stage1_mainline_v1 方法设计

日期：2026-05-27

状态：planned / method design only。本文档不包含实验结果，不表示新候选已经实现、跑通或通过 gate。

## 1. 设计目标

`full_flow_downstream_stage1_mainline_v1` 的目标是恢复一条完整的 Stage1 创新型增强主线，而不是继续生成 raw-near、guard、fallback 或 raw-pullback 小候选。

目标输出应同时具备：

- 明显视觉增强。
- 可解释的完整增强流程。
- 可消融的模块边界。
- 502/496 增强指标对照潜力。
- 168 fixed-detector downstream validation 证据。

若一个实现只接近 raw、没有可见增强、没有增强指标竞争力，即使 fixed detector 不崩，也不能作为本目标完成。

## 2. 设计输入

主要输入：

- `docs/evidence/full_flow_recovery/stage1_full_enhancement_mainline_recovery_plan_cn.md`
- `docs/downstream_driven_v1_method_design_inputs_20260526.md`
- `docs/downstream_driven_v1_method_design_synthesis_20260526_cn.md`
- `docs/stage1_downstream_edge_harm_degradation_diagnostic_20260525_cn.md`
- `docs/current_experiment_status_cn.md`
- `metrics/experiment_registry.csv`
- `metrics/candidate_registry.csv`

参考边界：

- 两篇 Wu et al. 2026 HAB 论文只作为 anchor / nearest-neighbor / overlap-risk reference。
- Web AI 调研只作为 method design 和 related work 输入。
- 结论必须来自本地 manifest、run report、`eval_bdry.txt`、`show.log`、结构 proxy、增强指标和日志。

## 3. 与已有工作的关系

正式 Stage1 主线提供创新骨架：

`Original -> BPH -> IMF1Ray / RGHS / CLAHE -> Fused -> Final`

P12-P28/D01 提供失败模式和安全边界：

- 强增强会造成 fixed detector distribution shift。
- near-raw 可以救回 legacy collapse，但不能满足完整增强目标。
- baseline-side false-edge ratio、endpoints 和 AC 是高敏感项。
- 只调一个 guard 或 fallback 不能自然形成论文级方法。

新主线必须把旧正式增强骨架和 downstream-aware 约束结合起来，而不是二选一。

## 4. 核心假设

H1：只要把 Stage1 的完整增强链路从“视觉指标优先”改成“退化诊断 + downstream-aware branch fusion”，就可能在保留视觉增强的同时降低 fixed-detector 分布偏移。

H2：灰像素白平衡、IMF/频域细节、多分支可见性/对比和最终滤波收口仍然是本项目的主要创新资产；失败原因不是这些模块本身不可用，而是缺少对背景伪边、弱边界断裂和 detector-sensitive structure shift 的约束。

H0：如果完整增强流程在严格约束后仍不能超过 raw 或至少达到 candidate pass，则应承认 frozen detector 更偏好 raw 分布，并把 Stage1 的角色转为 enhancement-aware MyEdge/MSFI validation，而不是继续堆参数。

## 5. 总体流程

建议流程：

`Original`
`-> M0 degradation diagnosis`
`-> M1 gray-pixel color formation`
`-> M2 IMF / frequency detail branch`
`-> M3 WB-safe contrast branch`
`-> M4 local visibility branch`
`-> M5 downstream-aware gated fusion`
`-> M6 bounded filtering and illumination closure`
`-> Final`

每个模块必须可开关。每个模块输出应可保存到独立 stage，用于 502/496 增强指标和可视化审计。

## 6. 模块设计

### M0 degradation diagnosis

输入：

- `Original`
- 可选 `BPH` 预估结果

输出：

- color cast score
- luminance nonuniformity map
- raw edge confidence
- weak boundary need map
- texture / background risk map
- saturation / overexposure risk

约束：

- 不使用 GT。
- 不使用 detector 输出作为增强 mask。
- 只做无监督图像退化诊断。

用途：

- 控制分支强度。
- 控制融合权重。
- 标记需要保守处理的背景、颗粒、气泡和高纹理区域。

### M1 gray-pixel color formation

来源：

- Stage1 `BPH`
- 灰像素引导白平衡与受限颜色补偿

目标：

- 形成稳定颜色起点。
- 修正 HAB 显微图像的轻中度色偏。
- 不通过大幅通道独立拉伸制造 chromatic false edge。

关键开关：

- `enable_gray_pixel_bph`
- `enable_color_consistency`
- `wb_gain_cap`
- `max_chroma_delta`
- `skip_if_channel_imbalance_low`

消融：

- raw only
- BPH only
- BPH + color consistency

### M2 IMF / frequency detail branch

来源：

- Stage1 `IMF1Ray`
- Web 调研中的 wavelet / frequency / structure branch 建议

目标：

- 恢复弱边界和细结构可见性。
- 给 MSFI spatial-frequency weak-boundary 叙事提供输入侧支撑。

设计：

- 第一版保留 IMF1Ray 作为主路径。
- 可选 single-level wavelet / DoG residual 作为实验开关，不在第一版强制开启。
- 高频残差必须乘以 texture-risk suppression。

关键开关：

- `enable_imf_detail_branch`
- `enable_wavelet_detail_branch`
- `detail_alpha`
- `texture_penalty_alpha`
- `background_detail_suppress`

风险：

- 背景颗粒、气泡、杂质会被当作边缘增强。
- endpoints 和 false-edge ratio 可能上升。

### M3 WB-safe contrast branch

来源：

- Stage1 `RGHS` 的真实职责：白平衡安全对比分支。

目标：

- 提升主体与边界对比。
- 避免独立通道强拉伸和偏色。

关键开关：

- `enable_wb_safe_contrast_branch`
- `contrast_gain_cap`
- `safe_luma_stretch`
- `chroma_false_edge_guard`

消融：

- 无 contrast branch。
- 原 RGHS-like branch。
- downstream-safe contrast branch。

### M4 local visibility branch

来源：

- Stage1 `CLAHE` 的真实职责：CLAHE 引导的局部可见性分支。

目标：

- 改善低对比、模糊轮廓和局部可见性。
- 不把背景纹理和气泡边缘推成伪边。

关键开关：

- `enable_local_visibility_branch`
- `clahe_clip_limit`
- `clahe_tile_grid`
- `local_visibility_alpha`
- `background_visibility_suppress`

风险：

- 高 clipLimit 会造成 legacy Final 类似的 downstream 崩塌。
- tile artifact 或局部过增强会提高 false-edge。

### M5 downstream-aware gated fusion

来源：

- Stage1 `Fused`
- Web 调研中的 pyramid / multiscale / structure-aware fusion

目标：

- 保留三分支融合创新，而不是改成单一 low-frequency correction。
- 融合权重由退化诊断、raw edge confidence、texture risk 和 branch consistency 共同决定。

候选融合信号：

- color confidence
- structure confidence
- local visibility confidence
- texture risk
- background risk
- saturation risk

关键开关：

- `enable_downstream_aware_fusion`
- `fusion_mode`
- `edge_confidence_weight`
- `texture_risk_weight`
- `branch_consistency_weight`
- `raw_anchor_weight`

注意：

- raw anchor 是防止结构崩塌的约束，不是主贡献。
- 如果最终输出接近 raw，应判定为本目标失败或退回 method design。

### M6 bounded filtering and illumination closure

来源：

- Stage1 `Final`
- guided filter / bilateral filter / low-frequency Retinex-like closure / homomorphic filtering

目标：

- 做最终照明、对比和噪声收口。
- 控制 halo、ringing、over-sharpening 和 false-edge。

关键开关：

- `enable_final_closure`
- `closure_mode`
- `guided_filter_radius`
- `bilateral_sigma`
- `retinex_lowfreq_alpha`
- `max_luma_delta`
- `max_gradient_shift`

风险：

- 旧 Final 的 fixed-detector collapse 说明 final closure 是高风险阶段。
- 第一版必须保守，但不能退化到无视觉增强。

## 7. 必须保存的 stage 输出

新主线应保存以下 stage：

- `BPHColor`
- `IMFDetail`
- `SafeContrast`
- `LocalVisibility`
- `FusionWeights` 或对应可视化权重图
- `Fused`
- `Final`

如果权重图无法按现有评测脚本处理，可至少保存到独立 diagnostics 目录，不能混入 paper metric stage。

## 8. 消融设计

最低消融集：

| Ablation | 模块 |
| --- | --- |
| A0 | raw input |
| A1 | gray-pixel color formation only |
| A2 | A1 + IMF/frequency detail |
| A3 | A1 + WB-safe contrast |
| A4 | A1 + local visibility |
| A5 | A1 + M2 + M3 + M4 without downstream-aware fusion |
| A6 | A1 + M2 + M3 + M4 + downstream-aware fusion |
| A7 | full flow without final closure |
| A8 | full flow with bounded final closure |
| A9 | legacy locked Final reference |
| A10 | P27 diagnostic reference |
| A11 | D01 diagnostic reference |

第一轮不一定全部运行 fixed-detector，但代码和配置必须支持这些开关。

## 9. 验证协议

### 9.1 Smoke

目的：

- 验证路径、decode、输出目录和 stage 保存。
- 验证视觉上不是 raw-near。

失败条件：

- 输出接近 raw。
- 出现明显偏色、过曝、halo、气泡伪边、背景噪声爆炸。
- 任一 stage 输出缺失或不可解码。

### 9.2 168 fixed-detector gate

核心 split：

- MyEdge 168 张带 GT split。

固定 detector：

- MSFI 50k
- DiffusionEdge baseline 50k

禁止：

- 重新训练。
- 修改 checkpoint。
- 修改 GT。
- 修改 eval protocol。
- 修改 MyEdge 正式 output_test 资产。

比较对象：

- raw anchor
- legacy locked Stage1 Final
- P27
- D01
- 当前最好 archived diagnostic candidate

### 9.3 502/496 enhancement metrics

用途：

- Stage1 增强指标。
- 外部方法 complete-case 对照。
- 证明该方法不是 near-raw control。

边界：

- 不能替代 downstream validation。
- `MS_SSIM` / `PSNR` 仍解释为相对原图结构一致性。

### 9.4 2770 readiness

只在以下条件满足后考虑：

- 168 gate 达到 candidate pass 或 strong pass。
- 502/496 没有暴露明显结构损伤。
- full-pool clean/review 状态允许。
- 用户明确授权。

## 10. Gate 判定

最低通过：

- 相对 legacy Final 显著恢复。
- 两个 detector 不崩。
- 图像有明显增强，不是 raw-copy。

候选通过：

- 至少一个 detector raw-near 或优于 raw。
- 另一个 detector 无明显 AP/AC/结构 proxy 崩坏。
- 502/496 指标或视觉质量证明增强有实际价值。

强通过：

- 两个 detector 都 raw-near 或优于 raw。
- false-edge ratio、endpoints、F1 proxy 不劣于 raw。
- 增强指标具备竞争力。
- 可形成 paper-ready evidence package。

失败：

- near-raw 无增强。
- 视觉增强明显但 downstream 明显崩。
- 增强指标弱且下游无正收益。
- 模块不可解释或不可消融。

## 11. 第一版实现边界

第一版代码应优先实现完整骨架和开关，不追求一次性加入所有可选复杂模块。

必须有：

- M0-M6 主路径。
- 每个模块开关。
- stage 输出。
- isolated config。
- isolated output root。
- smoke status。

可延后：

- 完整 wavelet branch。
- Retinex-like closure 的多参数搜索。
- 复杂 pyramid weight visualization。
- 2770 full-pool。

## 12. 下一步

下一步应写 run sheet，然后再进入代码实现：

- run sheet：`experiments/full_flow_downstream_stage1_mainline_v1/run_sheet_v1.md`
- 计划配置目录：`experiments/full_flow_downstream_stage1_mainline_v1/configs/`
- 计划输出目录：`experiments/full_flow_downstream_stage1_mainline_v1/outputs/`

## 13. 2026-05-27 v8 fixed-detector 结果回填

`full_flow_downstream_stage1_mainline_v1_v8` 已完成 168 fixed-detector validation，严格 gate 为 `candidate_rescues_legacy_but_not_near_raw`。

关键事实：

- FF01/v8 形成了完整方法骨架，但没有达成本文档定义的成功条件。
- MSFI 50k FF01/v8 为 ODS/OIS/AP/AC `0.739726/0.753251/0.310442/0.790100`，低于 raw anchor `0.783527/0.794213/0.345899/0.796846`。
- DiffusionEdge baseline 50k FF01/v8 为 `0.717475/0.727626/0.336548/0.794400`，低于 raw anchor `0.770521/0.779986/0.363065/0.796900`。
- Structure proxy 两个 detector 都 worse than raw：F1 下降、false-edge ratio 上升、endpoints 上升。
- FF01/v8 弱于 P27/P28 的 metric-near-raw mixed 证据，也不能替代 D01。

当前解释：完整增强链路在 frozen detector 下仍产生明显 distribution shift。下一步只能做机制级重设计，不能继续围绕 FF01/v8 做 threshold、guard、fallback 或 raw-pullback 小修补。

结论文件：`experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_fixed_detector_v8_status_20260527.md`。
