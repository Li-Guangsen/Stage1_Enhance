# E01-B wavelet-pyramid weak-boundary fusion design

日期：2026-05-27

## 1. Candidate 定义

- candidate id: `E01-B`
- implementation mode: `e01_b_wavelet_pyramid_weak_boundary_v1`
- primary hypothesis: FF01/FF02 失败不等于频域/多尺度思想无效，关键问题是旧 IMF/融合没有把 weak-boundary directional bands 与 HH/background texture 分开。若用 wavelet-like band reconstruction 只增强 stable LH/HL weak-boundary evidence、抑制 HH texture，并保留 raw 作为 detector-facing detail anchor，可能在 168 fixed-detector 上达到 raw-near 或给 AP 带来正收益。
- dominant mechanism: multi-scale / pyramid / wavelet fusion dominant。
- validation scope: 只做 168 张带 GT split 的 fixed MSFI 50k 与 fixed DiffusionEdge baseline 50k gate；不运行 502/496，不运行 2770。

## 2. 针对的 HAB 显微退化

E01-B 针对：

- 弱边界方向性不稳定：小型藻体、透明边界、低对比轮廓在 raw 中存在但不连续。
- 背景纹理与气泡/污点误增强：FF01/FF02 的 false-edge 和 endpoint fragmentation 表明背景 high-frequency texture 不能无差别增强。
- 低频照明轻微漂移：需要一点 LL-level correction，但不能像旧完整增强那样重写拓扑。
- 色度偏移：只允许 mild chroma lane，避免 E01-A/TLVC01 中 AC/分布漂移问题扩大。

## 3. 为什么不是 FF03/TLVC02/P29/D02

- 不是 FF03：不沿用 FF01/FF02 的 BPH/IMF/RGHS/CLAHE 三分支 direct weighted fusion，也不是调 fusion weights；主表示改为 Haar/wavelet-like LL/LH/HL/HH band reconstruction。
- 不是 TLVC02：不把 final gray/topology plane 锁回 raw，也不把 raw topology lock 当作主机制；它允许受限方向 band 重构。
- 不是 P29/D02：不从 P27/D01 或 raw-near candidates 做 guard/fallback/raw pullback；B 的 primary mechanism 是 band-selective weak-boundary reconstruction。
- 不是低幅度 raw-near 修补：即使 bounded reconstruction 会限制风险，candidate 的核心证据是 frequency-band 分解、directional-band 注入和 HH texture suppression，而不是单纯降低增强幅度。

## 4. 模块链

`Original -> BPH mild color prior -> degradation diagnosis -> Haar band decomposition -> LL illumination field -> LH/HL weak-boundary directional boost -> HH texture suppression -> background-risk control -> mild chroma reconstruction -> guided/bounded finish -> Final`

### 4.1 Degradation diagnosis

- multi-scale Scharr edge support：估计 stable edge support。
- local/std contrast：识别弱边界需求。
- background texture risk：在 raw weak-edge 但 local texture 高的位置抑制新边。
- saturation risk：间接通过 BPH 和 bounded reconstruction 控制极端色度。

### 4.2 Color / illumination correction

- LL band 使用 BPH luma 的低频差分，`ll_alpha` 和 `ll_max_delta` 均受限。
- chroma lane 只用 mild BPH ab delta，`wavelet_chroma_alpha` 与 `wavelet_max_chroma_delta` 显著低于 E01-A。

### 4.3 Structure and weak-boundary enhancement

- 对 raw L 与 CLAHE-driver L 做单层 Haar 分解。
- 只在 LH/HL directional bands 中注入 capped residual。
- directional gate 同时受 weak_need、edge_support 和 background_risk 控制。

### 4.4 Background false-edge risk control

- HH band 默认不增强；在 background_risk 高的位置 soft suppress raw HH。
- pixel-level reconstruction delta 再乘以 background suppression map，避免 FF01/FF02 式背景 false-edge burst。

### 4.5 Task-guided fusion and final reconstruction

- 任务引导来自 fixed-detector 失败证据，而不是 GT mask：优先保持 raw-compatible topology，定向补 weak boundary，抑制 false-edge/endpoints 风险。
- final bounded reconstruction 限制 mean luma/chroma delta、gradient ratio 和 luma std ratio。

## 5. 消融开关

完整消融只在 E01-B 达到最低安全或更高后执行。预注册开关：

- `enable_ll_illumination_field`
- `enable_directional_weak_boundary_boost`
- `enable_hh_texture_suppression`
- `enable_wavelet_background_control`
- `enable_mild_chroma_lane`
- `enable_wavelet_guided_finish`
- `enable_bounded_reconstruction`

失败时只保留关键配置、失败指标和归因，不做完整消融。

## 6. 预期 downstream 影响

- MSFI：期望减少 legacy Final 的 false-edge/endpoints 崩塌，同时比 E01-A 更稳住 AC，因为 luma/chroma 改变量更小。
- DiffusionEdge baseline：若 LH/HL weak-boundary support 有效，AP 或 OIS 可能略高于 raw；若 detector 偏好 raw distribution，则应至少 strict raw-near。
- Structure proxy：期望 MSFI non-worse；DiffusionEdge 至少 not-collapsed。

## 7. 失败风险

- LH/HL residual 可能把背景方向纹理误当作弱边界，导致 false-edge ratio 和 endpoints 上升。
- HH suppression 可能削弱真实微细轮廓，导致 recall/F1 下降。
- LL/chroma 虽然受限，仍可能带来 AC 下降，复现 E01-A 的 near-miss failure。
- 若两个 detector 仍只接受 raw distribution，E01-B 可能只是 rescue legacy 而不能 raw-near。

## 8. 成功/失败判定

沿用 E01 family run sheet 中已锁定阈值：

- 强成功：两个 detector 都 detector-positive，structure proxy 不崩。
- 可接受成功：至少一个 detector detector-positive，另一个 strict raw-near，structure proxy 不崩。
- 最低安全：两个 detector strict raw-near，structure proxy 不崩。
- 失败：低于 raw-near、只 rescue legacy、proxy-only、visual-only 或 structure collapse。
