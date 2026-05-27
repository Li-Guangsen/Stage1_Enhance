# full_flow_downstream_stage1_mainline_v2 方法设计

日期：2026-05-27

## 1. 目标

`full_flow_downstream_stage1_mainline_v2` / `FF02` 是 FF01/v8 fixed-detector 失败后的机制级重设计。

目标不是继续调 FF01 的 threshold、guard、fallback 或 raw-pullback，而是把完整增强流程改成 detector-compatible feature formation：

`degradation diagnosis -> gray-pixel color formation -> frequency/detail branch -> contrast/visibility branches -> detector-sensitive support diagnosis -> color lane / structure lane decoupling -> topology-compatible fusion -> bounded filtering closure`

FF02 必须同时满足两个方向：

- 保留完整 Stage1 创新骨架：灰像素、IMF/频域、多分支融合、滤波/收口。
- 避免 FF01 的失败机制：背景纹理、CLAHE/IMF pseudo structure 和低置信分支边缘不能直接进入 detector 输入。

## 2. FF01 失败事实

FF01/v8 已完成 168 fixed-detector validation：

- MSFI 50k FF01/v8：ODS/OIS/AP/AC `0.739726/0.753251/0.310442/0.790100`，低于 raw anchor `0.783527/0.794213/0.345899/0.796846`。
- DiffusionEdge baseline FF01/v8：`0.717475/0.727626/0.336548/0.794400`，低于 raw anchor `0.770521/0.779986/0.363065/0.796900`。
- structure proxy 两路 detector 都 worse than raw：F1 下降，false-edge ratio 和 endpoints 上升。
- high-risk 样本 `weixiaoyuanjia.21` 的 Stage1 Final grad ratio 约 `1.9137`。

结论：FF01 完整流程没有失败在速度或输出完整性，而是失败在分支增强进入 Final 的方式。完整增强分支把背景纹理和 detector-sensitive pseudo edges 引入了 frozen detector 输入。

## 3. 核心假设

H1：HAB 显微图像的下游 detector 主要受 luma/edge topology 分布影响，对低频色度和温和照明修正更宽容。因此 Stage1 可以保留可见颜色增强，但必须把 structure lane 与 color lane 解耦。

H2：IMF/频域、CLAHE 和 WB-safe contrast 仍有价值，但它们不能作为 full-image luma replacement。它们只能在 detector-compatible support 上提供局部残差或 branch evidence。

H0：如果 FF02 仍无法达到至少 P27/P28 的 metric-near-raw mixed gate，则当前 fixed detector 应被视为 raw-distribution-biased，Stage1 不应继续包装为下游收益主线。

## 4. 与 FF01 的机制区别

| 项目 | FF01/v8 | FF02 |
|---|---|---|
| Fusion 目标 | 在 BPH/IMF/RGHS/CLAHE 分支中直接加权 | 先拆 color lane 与 structure lane，再做 detector-compatible fusion |
| 背景处理 | 风险 map 后验回拉 | 背景在结构通道中前置排除，只允许低频色度/照明进入 |
| IMF/CLAHE | 可直接影响 Final luma | 只能以 support-masked residual 进入 structure lane |
| Final closure | 后处理收口 | topology-compatible filtering closure，不能新增背景边 |
| 成功标准 | 原计划 full-flow | 至少达到 P27/P28 raw-near mixed 水平，同时视觉强于 near-raw family |

## 5. 模块设计

### M0 Detector-sensitive degradation diagnosis

输入 raw 图像，估计：

- `raw_edge_confidence`：高置信 raw 边缘。
- `weak_boundary_support`：弱边界但可能与 GT 有关的区域。
- `background_texture_risk`：背景颗粒、噪声、藻体内部纹理或光照碎片。
- `stable_object_support`：由 raw edge、local contrast 和 branch-consensus 构成的可增强结构域。
- `flat_background_mask`：结构增强禁止域。

### M1 Gray-pixel color formation

复用 BPH / gray-pixel color formation 作为颜色起点，但 FF02 不把 BPH luma 当成 detector luma 主体。BPH 主要提供：

- low-frequency illumination correction；
- Lab `a/b` 色度修正；
- color consistency anchor。

### M2 Frequency/detail evidence branch

IMF1-Rayleigh 或 fast frequency branch 仍运行，但只输出 detail evidence：

- 计算 detail residual；
- residual 仅在 `stable_object_support` 与 `weak_boundary_support` 中进入 structure lane；
- 背景和低置信纹理区域的 IMF residual 置零或强抑制。

### M3 WB-safe contrast branch

RGHS/WB-safe contrast 只提供：

- 中低频 luma contrast evidence；
- 主体区域的局部对比增强；
- 不允许在 `flat_background_mask` 中生成新边。

### M4 CLAHE local visibility branch

CLAHE 只用于弱边界的局部可见性证据：

- 输入到 weak-boundary lift；
- 不作为全局 luma 替换；
- 在 background texture risk 高的区域自动降权。

### M5 Color lane / structure lane decoupling

Color lane：

- 以 raw Lab 为基础；
- 只注入 BPH/branch 的 low-frequency chroma；
- 控制 chroma delta；
- 允许视觉上比 P27/D01 更明显的颜色恢复。

Structure lane：

- 以 raw luma topology 为基础；
- 注入 masked detail residual、contrast residual 和 visibility residual；
- 每类 residual 都有 support gate 和 max-delta；
- 背景只允许平滑照明，不允许新增 high-frequency edge。

### M6 Topology-compatible fusion

Final Lab：

- `L = raw_L + lowfreq_illumination_delta + support_masked_structure_residual`
- `a/b = raw_ab + bounded_lowfreq_chroma_delta`
- 在 background risk 高区域做 edge-preserving smoothing / luma residual suppression。

这不是 raw-copy：颜色/低频照明可以明显变化，但 detector-sensitive luma topology 必须接近 raw。

## 6. 可消融开关

FF02 必须保留以下开关：

- `enable_detector_sensitive_diagnosis`
- `enable_gray_pixel_color_lane`
- `enable_frequency_detail_evidence`
- `enable_contrast_evidence`
- `enable_visibility_evidence`
- `enable_color_structure_decoupling`
- `enable_topology_compatible_fusion`
- `enable_background_luma_suppression`
- `enable_bounded_filtering_closure`

## 7. Smoke gate

FF02 smoke 不能只看输出完整性，必须同时看：

- mean BGR/chroma delta 是否高于 near-raw family 的视觉差异；
- grad ratio 是否低于 FF01/v8 高风险；
- high-risk samples 是否没有背景块状 pseudo edges；
- stage panels 是否能解释 color lane 和 structure lane 的贡献。

## 8. 168 fixed-detector gate

最低继续条件：

- 输出完整；
- 相对 legacy Stage1 Final 明显恢复；
- 至少不低于 FF01/v8；
- structure proxy 不出现 FF01/v8 级别的 F1/false-edge/endpoints 崩坏。

候选通过：

- 至少达到 P27/P28 的 `candidate_metric_near_raw_structure_mixed` 水平；
- 视觉增强强于 P27/D01 near-raw family；
- 502/496 有补跑增强指标价值。

强通过：

- 两路 detector raw-near 或优于 raw；
- structure proxy 不劣于 raw；
- 视觉和增强指标可支撑完整 Stage1 方法主线。

## 9. 边界

- 不覆盖 FF01、P12-P28、D01、formal Stage1 mainline 或 MyEdge official outputs。
- 不训练 detector，不改 checkpoint，不改 GT，不改 eval protocol。
- FF02 不得退化为 raw-pullback / guard / fallback family。
- 502/496 和 2770 仍后置，不能替代 168 fixed-detector validation。

## 10. 2026-05-27 FF02 fixed-detector 结果回填

FF02 已完成 method design、独立 config、Stage1 168 输出、MyEdge fixed-detector sampling/eval/show、result intake、structure proxy 和 downstream gate。结论不是成功：

- Stage1 168 输出完整：Final PNG/JPG 各 `168`，decode 失败 `0`，耗时约 `77.5` 秒。
- Final 相对 raw 的 mean BGR delta `11.7138`、L delta `1.3708`、chroma delta `7.9785`、PSNR `27.2740`、grad ratio `0.9450`、luma std ratio `1.0132`。视觉差异比 FF01/P27/D01 更明显，但仍有 `tama.14`、`weixiaoyuanjia.21` 等 high-risk 样本。
- MSFI FF02 ODS/OIS/AP/AC 为 `0.737952/0.751109/0.303208/0.792000`，相对 raw 为 `-0.045575/-0.043104/-0.042691/-0.004846`。
- DiffusionEdge baseline FF02 ODS/OIS/AP/AC 为 `0.711020/0.720141/0.320951/0.794000`，相对 raw 为 `-0.059501/-0.059845/-0.042114/-0.002900`。
- Structure proxy 两路 detector 都 worse than raw：MSFI dF1 `-0.0507`、dFalse-edge `+0.0734`、dEndpoints `+2.0630`；DiffusionEdge dF1 `-0.0666`、dFalse-edge `+0.0890`、dEndpoints `+3.7585`。
- Gate 为 `candidate_rescues_legacy_but_not_near_raw`。FF02 救回 legacy Stage1 Final 崩塌，但没有 raw-near，也没有下游正收益。

FF02 相比 FF01 的有效改进主要在 structure proxy 风险略有降低，但 ODS/OIS/AP 反而更差。因此 FF02 不能进入 502/496 或 2770 作为 candidate-passing route，也不能继续同族 FF03 小修。下一步应先做 failure audit，明确 frozen detector 的 raw-distribution bias、完整增强流程的 distribution shift 和 MyEdge/MSFI 侧适配必要性。

证据入口：

- Stage1 status：`experiments/full_flow_downstream_stage1_mainline_v2/full_flow_downstream_stage1_mainline_v2_ff02_myedge168_v1_status_20260527.md`
- fixed-detector status：`experiments/full_flow_downstream_stage1_mainline_v2/full_flow_downstream_stage1_mainline_v2_fixed_detector_ff02_status_20260527.md`
- MyEdge results：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_results_20260527.md`
- structure proxy：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_structure_metrics_20260527.md`
- downstream gate：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_downstream_gate_20260527.md`
