# E01-A color-illumination task-guided candidate design

日期：2026-05-27

## 1. 基本信息

- candidate id: `E01-A`
- candidate name: `e01_a_color_illumination_task_guided_v1`
- family: `hab_task_guided_complete_enhancement`
- primary hypothesis: `color-illumination correction dominant`
- status: `method_design_before_code`

## 2. 针对的 HAB 显微退化

E01-A 针对以下退化：

- 水下显微图像的 channel imbalance 和 mild color attenuation；
- low-frequency illumination non-uniformity；
- weak boundary 被局部亮度/颜色不均匀压低；
- high-risk 背景、杂质、气泡或藻体内部纹理被 detector 当成 pseudo edges；
- FF02/TLVC01 中出现的 color/chroma shift 与 raw-distribution sensitivity。

## 3. 为什么不是 FF03/TLVC02/P29/D02

- 不是 FF03：E01-A 不继续 FF01/FF02 的 complete full-flow branch fusion，也不调整 FF02 的阈值、fallback 或 bounded scales。
- 不是 TLVC02：E01-A 不把 Final 的 gray/topology plane 投回 exact raw，不走 raw gray-plane topology lock。
- 不是 P29/D02：E01-A 不从 P27/D01 的 near-raw candidate 做低幅度色彩回拉；它重写为 color/illumination-first reconstruction，允许可见色度/照明变化，但必须用 raw high-frequency topology 约束 detector-sensitive 结构。
- 不是低幅度 raw-near 修补：目标不是把图像变得更接近 raw，而是测试“低频颜色/照明可变，高频结构稳定”的完整增强机制能否给 fixed detector 带来收益。

## 4. 方法链

`Original -> degradation diagnosis -> capped color formation -> low-frequency illumination field -> weak-boundary visibility support -> raw-detail-preserving reconstruction -> background risk suppression -> bounded final`

### 4.1 Degradation diagnosis

输入 raw image，估计：

- `raw_luma`
- channel imbalance / chroma magnitude；
- low-frequency illumination field；
- multi-scale edge confidence；
- local texture risk；
- background false-edge risk；
- weak-boundary support need。

### 4.2 颜色/照明校正

- 使用 mild gray-pixel/BPH color formation 作为 color lane。
- 在 Lab ab 空间限制色度变化，默认 `max_chroma_delta=18`。
- 在 luma 上只调整 low-frequency illumination，保留 raw high-frequency luma residual。
- 禁止 red-channel aggressive compensation。

### 4.3 结构与弱边界增强

- 从 raw luma 构造 high-frequency detail plane。
- 对低对比但有 multi-scale edge support 的区域加入小幅 weak-boundary luma residual。
- residual 必须乘以 `(1 - background_false_edge_risk)`。

### 4.4 背景伪边风险控制

- 在 weak raw-gradient 且 local texture 高的区域抑制新增 luma gradient。
- 对 high saturation / high chroma shift 区域降低色度注入。
- 最终 closure 使用 guided/bilateral-like smoothing 只作用于 background risk，而不是全局模糊。

### 4.5 任务引导融合与最终重建

- `Final_L = corrected_low_frequency_L + raw_high_frequency_L + gated_weak_boundary_residual - background_risk_suppression`
- `Final_ab = raw_ab + color_confidence * capped(BPH_ab - raw_ab)`
- 在输出前做 bounded check：mean luma delta、grad ratio、luma std ratio、chroma delta 超过预设上限时按固定 scales 向 reconstruction anchor 收缩。

## 5. Ablation switches

- `enable_degradation_diagnosis`
- `enable_color_illumination_lane`
- `enable_low_frequency_luma_correction`
- `enable_raw_detail_preservation`
- `enable_weak_boundary_support`
- `enable_background_false_edge_suppression`
- `enable_bounded_reconstruction`
- `enable_bilateral_finish`

完整消融只在 E01-A 达到最低安全或更高后执行；若失败，只保留关键配置、failure metrics、risk panels 和归因。

## 6. 预期 downstream 影响

预期正向：

- 相比 FF01/FF02，dFalse-edge 和 dEndpoints 应显著降低。
- 相比 TLVC01，允许 low-frequency/chroma 改善，可能提升 MSFI AC 或 DiffusionEdge AP。
- 至少应达到两个 detector strict raw-near，结构不崩；理想是一个 detector ODS/AP 达到 positive-gain threshold。

主要风险：

- 色度/低频变化仍可能触发 frozen detector distribution shift。
- raw high-frequency preservation 可能使视觉增强不足，落回 P27/D01 式 near-raw 弱候选。
- weak-boundary residual 若选错区域，会增加 background false edges。

## 7. 先验 stop condition

small smoke 阶段停止：

- 输出不完整或 decode 失败；
- high-risk panel 出现 FF01/FF02 式大块背景伪边；
- mean grad ratio > `1.12` 或任一 high-risk sample grad ratio > `1.30`；
- mean BGR delta < `3.0` 且 chroma delta < `1.5`，说明退化成 low-amplitude raw-near 修补；
- runtime 外推 168 超过 10 分钟。

168 gate 阶段停止：

- 任一 detector 低于 raw-near tolerance 且只 rescue legacy；
- structure proxy 不满足 `structure not-collapsed`；
- 只有 visual/proxy 好看但 ODS/OIS/AP/AC 低于 raw；
- 若失败，不直接派生 E01-A2，除非先写失败原因和机制级修正说明。

