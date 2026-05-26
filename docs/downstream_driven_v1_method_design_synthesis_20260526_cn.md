# downstream_driven_v1 方法设计综合与执行约束

日期：2026-05-26

输入归档：`docs/downstream_driven_v1_method_design_inputs_20260526.md`

本文档把三份 Web AI 回答综合为 `downstream_driven_v1` 后续增强方法与代码修改的约束。三份回答只作为方法设计和 related work 输入；项目状态、实验结论和 gate 结果仍必须回到本地 manifest、结果表、run report、`eval_bdry.txt`、`show.log`、结构 proxy 文件和已同步文档。

本轮只做文档接收、去重、核验和方案设计；没有修改增强代码，没有运行 Stage1/MyEdge 实验，没有进入 `2770` full-pool。

## 1. 核验方式与边界

- DOI 核验：使用 Crossref works API 检查 DOI、题名和出版信息能否解析。
- arXiv 核验：使用 arXiv export API 检查 arXiv ID 和题名。
- GitHub 核验：只检查仓库 URL 可访问和返回 `200`，不等于确认代码可直接运行、权重可用或协议适配本项目。
- official link 核验：优先使用 DOI resolver、publisher page、arXiv、官方 GitHub；`utm_source=chatgpt.com` 链接不作为正式引用形态。
- 未核验内容：Web AI 对论文指标、期刊分区、代码可复现性、预训练权重、下游收益的摘要性表述，均不能直接写入论文结论。

## 2. Wu/Gengkun Wu 相关锚点文献

这些文献不删除，但必须单独标为 anchor / nearest-neighbor / overlap-risk reference。它们可以用于 HAB task framing、degradation analysis、enhancement-flow design、metric design 和写作边界参考；新增候选文献池和第一轮 candidate pipeline 不应由该作者群体主导，也不得直接复刻其增强流程。

| 文献 | 核验状态 | 当前作用 | 禁止用法 |
| --- | --- | --- | --- |
| Enhanced edge detection of harmful algal Blooms using diffusion probability models and Sobel-convolutional attention mechanisms, ESWA 2026, DOI `10.1016/j.eswa.2025.129663` | Crossref 已核到题名、ESWA、2026-03、DOI。 | MyEdge/MSFI 的最近邻 HAB diffusion edge detection anchor；用于说明重合风险和边界任务设定。 | 不作为 Stage1 增强 candidate；不把 Stage1 写成 HAB enhancement + diffusion edge pipeline 的主创新。 |
| Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network, EAAI 2026, DOI `10.1016/j.engappai.2026.114948` | Crossref 已核到题名、EAAI、2026-08、DOI；修正原输入中“DOI 需 BibTeX 再确认”的不确定表述。 | HAB task-oriented enhancement-segmentation coupling anchor；用于数据描述、退化因素、增强-下游耦合写法参考。 | 不复现其分割网络；不把未来下游验证写成已完成事实。 |
| Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy, IVC 2025, DOI `10.1016/j.imavis.2025.105466` | Crossref 已核到题名、IVC、2025-04、DOI。 | HAB/submarine algal microscopy enhancement-flow overlap-risk reference；可参考 AWB/color compensation/pyramid fusion 的风险边界。 | 不作为 C01 第一轮核心来源；不直接复刻 AWBCC + pyramid fusion 流程。 |
| Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion, MTAP 2023/2024, DOI `10.1007/s11042-023-16258-0` | Crossref 已核到题名、DOI。 | HAB color compensation + multiscale fusion overlap-risk reference。 | 不把 cyclic compensation + multiscale fusion 写成本项目新颖核心。 |
| Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion, Applied Intelligence 2023, DOI `10.1007/s10489-023-04502-x` | Crossref 已核到题名、DOI。 | HAB wavelet/frequency enhancement overlap-risk reference；可用于 C03 风险分析。 | 不在第一轮引入 EMD 复杂复刻；不把 wavelet 增强直接等同于 MSFI 创新。 |
| SFMnet: Edge detection of HABs based on spatial feature mapping encoder-decoder network, Ocean Engineering 2024, DOI `10.1016/j.oceaneng.2024.118547` | Crossref 已核到题名、DOI。 | HAB edge detection related work / detector-context reference。 | 不作为 Stage1 增强主线；不转移 MyEdge/MSFI 论文主创新。 |

## 3. 去重后的候选文献与项目池

### A 类：第一轮可迁移或直接约束 Stage1 的方法来源

| 来源 | 核验状态 | 可迁移模块 | 进入当前主线方式 |
| --- | --- | --- | --- |
| Label-free microscopic cell images adaptive enhancement via weighted fusion of bright, dark, and weak structure features, BSPC 2024, DOI `10.1016/j.bspc.2024.105973` | Crossref 已核 DOI/题名；官方代码未核到。 | bright/dark local feature、weak structure feature、guided filtering、多尺度 Gaussian、background uniformity。 | C01 核心思想来源：重写简化版，不照搬不可见代码。 |
| A Generalized Framework for Edge-Preserving and Structure-Preserving Image Smoothing, AAAI 2020 / TPAMI extension, DOI `10.1609/aaai.v34i07.6830`, GitHub `wliusjtu/Generalized-Smoothing-Framework` | Crossref 已核 DOI；GitHub `200`。 | edge-preserving smoothing、structure-preserving smoothing、texture removal。 | C01/C04 false-edge guard 的理论来源；实现先用 guided/bilateral 近似。 |
| Underwater Image Enhancement via Minimal Color Loss and Locally Adaptive Contrast Enhancement, TIP 2022, DOI `10.1109/TIP.2022.3177129`, GitHub `Li-Chongyi/MMLE_code` | Crossref 已核 DOI；GitHub `200`。 | capped color correction、minimal color loss、local adaptive contrast。 | C01 的 mild WB / local contrast 来源；只取保守模块。 |
| Feature Preserving Smoothing Provides Simple and Effective Data Augmentation for Medical Image Segmentation, MICCAI 2020, DOI `10.1007/978-3-030-59710-8_12` | Crossref 已核 DOI。 | feature-preserving smoothing、texture suppression、boundary preservation。 | C01/C04 支撑文献；不作为外部增强方法。 |
| Pre-processing Image using Brightening, CLAHE and RETINEX, arXiv `2003.10822` | arXiv 已核题名。 | edge-task preprocessing caution、CLAHE/Retinex 风险。 | 只用于约束：增强必须由 edge gate 检验。 |

### B 类：第二轮候选、备用模块或 external classical baseline

| 来源 | 核验状态 | 可迁移模块 | 当前处理 |
| --- | --- | --- | --- |
| A Perception-Aware Decomposition and Fusion Framework for UIE, TCSVT 2023, DOI `10.1109/TCSVT.2022.3208100`, GitHub `59Kkk/SPDF` | Crossref 已核 DOI；GitHub `200`。 | mean/contrast/structure decomposition, perception-aware fusion。 | C02 第二轮结构分解融合参考。 |
| HFM: A hybrid fusion method for UIE, EAAI 2024, DOI `10.1016/j.engappai.2023.107219` | Crossref 已核 DOI。 | gray-world、nonlinear color mapping、visibility recovery、perceptual fusion。 | external classical baseline / fusion 机制参考。 |
| Underwater Image Enhancement via Piecewise Color Correction and Dual Prior Optimized Contrast Enhancement, IEEE SPL 2023, DOI `10.1109/LSP.2023.3255005` | Crossref 已核 DOI。 | piecewise color correction、texture/spatial prior、V-channel detail。 | C02/C04 参考；避免无 guard texture prior。 |
| L2UWE, CVPRW 2020, arXiv `2005.13736` | arXiv 已核题名。 | local contrast illumination model、multi-scale fusion。 | 低光照/局部照明参考，不作为第一轮主线。 |
| Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion, TCSVT 2024, DOI `10.1109/TCSVT.2023.3299314`, GitHub `Li-Chongyi/WWPF_code` | Crossref 已核 DOI；GitHub `200`。 | wavelet low/high frequency fusion、visual perception weights。 | C03 参考；保留 WWPF，不删除。 |
| TEBCF, TGRS 2022, DOI `10.1109/TGRS.2021.3110575`, GitHub `bilityniu/TEBCF_tgrs` | Crossref 已核 DOI；GitHub `200`。 | blur-aware texture enhancement、color fusion。 | texture-aware fusion 参考；伪边风险高。 |
| ICSP / illumination channel sparsity prior, TCSVT 2024, GitHub `Hou-Guojia/ICSP` | GitHub `200`；DOI 在原输入中出现但本轮未作为核心 DOI 锁定。 | illumination correction、non-uniform illumination。 | 备用模块；不进第一轮。 |
| CDEF / Underwater Scene Enhancement via Adaptive Color Analysis and Multispace Fusion, JOE 2025, DOI `10.1109/JOE.2025.3591405`, GitHub `bilityniu/CDEF` | Crossref 已核 DOI；GitHub `200`。 | adaptive color-tone analysis、multi-space pyramid fusion。 | external baseline / C02 参考。 |

### C 类：related work 或 external baseline only

| 来源 | 核验状态 | 原因 |
| --- | --- | --- |
| Task-Friendly UIE for Machine Vision Applications, TGRS 2024, DOI `10.1109/TGRS.2023.3340244` | Crossref 已核 DOI。 | 强支持 downstream-driven 立场，但深度/训练依赖重。 |
| Downstream Task Inspired UIE, arXiv `2603.01767` | arXiv 已核题名。 | 作为 task-aware UIE 叙事来源；不从零训练。 |
| SGUIE-Net, arXiv `2201.02832`; STSC, arXiv `2211.10608`; HUPE, arXiv `2411.18296`; WWE-UIE, arXiv `2511.16321` | arXiv 已核题名；部分 GitHub URL 可访问。 | 深度模型或网络依赖重；只做 related/external baseline 候选。 |
| Histoformer, DehazeFormer, UniMIE, Zero-DCE++ | GitHub/项目页可访问性可核；未核验其对 HAB fixed detector 的收益。 | external baseline only；不作为 Stage1 主线。 |
| ZS2Net、若干 Q1/JCR/SJR 排名说法 | 原输入信息不足。 | 标为 unverified / related-only，不参与候选设计。 |

## 4. 可迁移模块清单

| 模块 | 迁移方式 | 对 downstream edge 的机会 | 主要风险 | 当前约束 |
| --- | --- | --- | --- | --- |
| 颜色补偿 / 通道补偿 | clipped gray-world / minimal color-loss approximation | 减少色偏导致的弱边界淹没。 | RGB 独立强拉伸制造 chromatic false edges。 | gain cap 第一轮固定 `[0.90, 1.10]`，最多不超过 `[0.85, 1.15]`。 |
| 白平衡 | mild capped WB，必要时跳过 | 稳定输入分布。 | 过度 WB 造成 detector distribution shift。 | 不用 red-channel aggressive compensation。 |
| Retinex | 仅作为低频照明参考 | 可能改善 uneven illumination。 | halo、噪声放大、局部虚假梯度。 | 第一轮不作为主模块。 |
| CLAHE | Lab-L / HSV-V 低强度 | 提升弱边界局部对比。 | 背景颗粒、气泡和杂质同步增强。 | `clipLimit <= 1.0/1.2`，默认可关闭。 |
| Gamma / contrast | luminance-only small grid | 保守改善局部梯度。 | 过拟合单 detector 或压缩弱边界。 | gamma 第一轮只用 `{0.95, 1.00, 1.05}`。 |
| 多尺度 / 金字塔融合 | 第二轮结构分解融合 | 低频照明和高频结构分离处理。 | weight map 偏好伪边。 | 必须加 texture penalty 和 raw blend。 |
| 小波 / 频域融合 | 第三轮 C03 | 与 MSFI spatial-frequency 叙事自然连接。 | HH/LH/HL 容易增强颗粒伪边。 | 不进第一轮；先单层 Haar + raw blend。 |
| edge-aware smoothing/sharpening | guided/bilateral base + small residual | 抑制背景纹理，保留稳定边界。 | 抹掉 flagella / filament-like weak structures。 | 只能温和，必须保留 raw residual。 |
| false-edge suppression | local variance、edge stability、gradient density guard | 降低 background edge noise、endpoints。 | 过筛导致 weak boundary 漏检。 | 不使用 GT 生成 enhancement mask；GT 只用于 gate。 |
| parameter search | small predefined grid + single gate | 避免视觉指标与下游指标错位。 | 168 split 过拟合、无限调参。 | 每轮单候选、单 gate；失败也记录。 |

## 5. downstream_driven_v1 candidate pipelines

评分范围为 1-5，数值越高越适合当前阶段；`edge safety` 分数越高表示 downstream edge 风险越低。

| 排名 | Candidate | Implementability | HAB fit | Edge safety | Enhancement metric potential | Novelty vs Wu et al. 2026 | 结论 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | C01 MicroStructure-CSP | 5 | 5 | 4 | 3 | 5 | 第一轮唯一推进：显微弱结构 + 背景伪边守卫，不由 Wu 流程主导。 |
| 2 | C02 Conservative MLLE/SPDF Structure Fusion | 4 | 4 | 3 | 4 | 4 | 若 C01 稳定但提升不足，再做结构分解融合。 |
| 3 | C04 False-Edge Suppression Repair | 5 | 4 | 5 | 2 | 5 | 不是独立增强主线；当 false-edge/endpoints 崩坏时作为修复候选。 |
| 4 | C03 Wavelet/Frequency Structure Guard | 3 | 4 | 2 | 4 | 4 | 与 MSFI 叙事契合，但高频伪边风险高，第三轮再进。 |
| 5 | C05 Downstream-Gated Parameter Search | 4 | 4 | 3 | 3 | 4 | 作为选择机制必须存在，但不能成为无限调参系统。 |

### C01 MicroStructure-CSP

目标：建立一个 `microstructure-aware / structure-preserving / false-edge guarded` 的 Stage1 非正式候选，先恢复 downstream 可用性，再追求增强指标。

核心流程：

1. degradation diagnosis：记录 RGB mean/std、channel imbalance、Lab-L nonuniformity、Sobel gradient density、local variance texture risk、saturation ratio。
2. mild capped gray-world：gain cap 固定 `[0.90, 1.10]`；channel imbalance 小时跳过。
3. local bright/dark feature：局部窗口 `{15, 31}` 提取亮/暗细节残差，低权重注入。
4. weak structure feature：Lab-L 上 guided/bilateral base + multi-scale Gaussian residual；用 multi-scale Sobel consistency 形成 structure confidence。
5. conservative fusion：`L_out = L_raw + alpha_c * contrast_residual + alpha_s * weak_structure_residual`，残差乘 `(1 - texture_risk)`。
6. false-edge guard：若 gradient density、HF energy 或 local variance 超过 raw 的 `1.10x`，逐级 fallback：关 weak-structure residual、关 contrast residual、只保留 mild WB、最后 raw-copy。

固定小网格：

- `window_size`: `{15, 31}`
- `alpha_contrast`: `{0.00, 0.05, 0.10}`
- `alpha_structure`: `{0.00, 0.05, 0.10}`
- `guided_radius`: `5`
- `guided_eps`: `1e-3`
- `guard_ratio`: `1.10`

最多 `18` 个配置，不允许无限扩展参数。

### C02 Conservative MLLE/SPDF Structure Fusion

流程：capped color correction -> Lab-L local adaptive contrast -> contrast-corrected branch/detail-preserved branch -> mean/contrast/structure decomposition -> texture penalty -> weighted fusion -> false-edge guard。

用途：C01 稳定但增强指标和弱边界收益不足时启用。

### C03 Wavelet/Frequency Structure Guard

流程：mild WB -> Lab-L -> single-level Haar DWT -> LL 轻照明校正 -> LH/HL 弱边界方向 boost -> HH soft threshold -> inverse DWT -> raw blend -> guided cleanup -> false-edge guard。

用途：需要强化 MSFI spatial-frequency 叙事时启用，不作为第一轮。

### C04 False-Edge Suppression Repair

流程：multi-scale edge stability -> local variance texture risk -> isolated component/morphology residual -> suppress unstable high-frequency residual -> only inject residual on stable edge confidence。

用途：当 C01/C02 出现 false-edge ratio、endpoints、background edge noise 恶化时启用。

### C05 Downstream-Gated Parameter Search

流程：预定义小网格 -> 168 GT split proxy precheck -> fixed MSFI + fixed DiffusionEdge gate -> 失败也记录 -> 通过后才进入 502/496。

用途：选择机制，不是独立增强算法。

## 6. 第一轮单候选执行计划

第一轮只推进一个 candidate：

- Candidate 名称：`c01_microstructure_csp_v1`
- 计划配置：`experiments/downstream_driven_v1/configs/c01_microstructure_csp_v1.json`
- 建议代码入口：新增可回滚 `final.mode=microstructure_csp_bph`
- Stage1 168 输出目录：`experiments/downstream_driven_v1/outputs/myedge168/c01_microstructure_csp_v1`
- MyEdge MSFI 计划 run：`D:/Desktop/MyEdgeCodex/output_test/stage1_coupling/msfi_50k/downstream_v1_c01_microstructure_csp_v1_168_p16_20260526`
- MyEdge DiffusionEdge baseline 计划 run：`D:/Desktop/MyEdgeCodex/output_test/stage1_coupling/diffusionedge_baseline_50k/downstream_v1_c01_microstructure_csp_v1_168_p16_20260526`
- MyEdge report asset 前缀：`D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/c01_microstructure_csp_p16_*`
- 若通过 candidate gate，才生成 `full502_clean_v1` 和 `compare9_complete496_v1` 的增强指标目录，例如 `metrics/outputs/evaluate_protocol_v2/downstream_driven_p16_full502_20260526` 与 `metrics/outputs/evaluate_protocol_v2/downstream_driven_p16_compare496_20260526`。

单 gate：`168` 张带 GT split 的 fixed-detector downstream gate。

- Raw anchors：继续使用 MyEdge 已锁定 raw anchor。
- Detectors：固定 MSFI 50k + 固定 DiffusionEdge baseline 50k。
- 指标：ODS/OIS/AP/AC + F1 proxy + false-edge ratio + endpoints/kpx + background edge noise proxy。
- minimum pass：相对 legacy Stage1 Final 明显恢复，且两个 detector 都不崩。
- candidate pass：至少一个 detector raw-near，另一个 detector 无明显 AP/AC/结构 proxy 崩坏。
- strong pass：两个 detector 都 raw-near 或优于 raw，且 false-edge ratio、endpoints、F1 proxy 不劣于 raw。
- fail：任一 detector 明显低于 legacy rescue 门槛，或 false-edge/endpoints 大幅恶化。

执行约束：

- 不覆盖正式配置 `experiments/optimization_v1/configs/locked_full506_final_mainline.json`。
- 不覆盖正式结果 `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`。
- 不覆盖旧 downstream-driven run 目录、GT、权重、MAT 或 MyEdge 正式资产。
- 多 run WSL eval/show 必须使用 `.sh`，不能把 Bash 变量/数组/循环塞进 PowerShell 双引号 `$cmd`。
- `502/496` 只在 168 gate 达到 candidate pass 或 strong pass 后用于 Stage1 增强指标与 external complete-case 对照。
- 不进入 `2770` full-pool，直到 168 strong/candidate、502/496 无明显风险、clean manifest 和人工复核条件都满足并得到显式授权。

## 7. 与当前本地状态的衔接

当前本地已完成的 P15 `structure_guarded_weak_boundary_v1` 只能写成 near-raw/mixed 诊断：MSFI 侧结构 non-worse，但 DiffusionEdge baseline 侧 false-edge/endpoints 仍 mixed。它不是稳定下游收益，也不是正式增强主线。

因此，`c01_microstructure_csp_v1` 的目标不是重复证明旧 Stage1 Final 会下降，也不是继续微调 P15 的小参数；它要把第一轮候选重心从“亮度/颜色微调”推进到“显微弱结构 + 背景伪边抑制 + 固定 gate”的可消融流程。

## 8. 168 / 502 / 496 / 2770 口径

- `168` 张带 GT split：唯一用于 fixed-detector downstream validation 的第一 gate。
- `full502_clean_v1`：只用于 Stage1 增强指标、阶段表或候选通过后的增强质量补充。
- `compare9_complete496_v1`：只用于外部方法 complete-case 对照和增强指标补充。
- `2770` full-pool：本轮不进入；没有 clean manifest / 人工复核 / gate 通过 / 显式授权前，不得启动。

## 9. 当前可写与不可写结论

可写：

- 三份 Web AI 回答已被转成方法设计输入，而不是项目事实源。
- Wu/Gengkun Wu 相关 HAB 论文被保留为 nearest-neighbor / overlap-risk anchor。
- 第一轮建议 candidate 是 `c01_microstructure_csp_v1`，它以非 Wu 的显微弱结构增强、结构保持平滑和保守颜色/对比模块为主。
- 168 GT split 是下游 fixed-detector gate；502/496 不是下游验证替代物。

不可写：

- 不能写 `c01_microstructure_csp_v1` 已实现、已跑通或已通过 gate。
- 不能写新增候选已提升 ODS/OIS/AP/AC。
- 不能写 502/496 或 2770 已证明下游收益。
- 不能把 Wu et al. 2026 的增强/边缘/分割流程复刻为当前项目主创新。
- 不能把 MS_SSIM / PSNR 写成相对增强真值质量；仍只能解释为相对原图结构一致性。

## 10. 二次只读复核记录

复核日期：2026-05-26。

本次复核仅用于确认本文档仍可作为后续增强代码修改和实验设计的约束；没有修改增强代码，没有运行 Stage1/MyEdge 实验，没有生成新指标，没有进入 `2770` full-pool。

复核结果：

- 已确认本文档覆盖用户要求的 10 项内容：去重、DOI/arXiv/GitHub/official link 核验边界、Wu/Gengkun Wu anchor 标注、A/B/C 分类、可迁移模块、C01-C05 candidate pipeline、排序、第一轮单候选执行计划、168/502/496/2770 口径和日志同步。
- 使用 Crossref works API 二次核验本文档中锁定的关键 DOI，`10.1016/j.eswa.2025.129663`、`10.1016/j.engappai.2026.114948`、`10.1016/j.imavis.2025.105466`、`10.1016/j.bspc.2024.105973`、`10.1109/TIP.2022.3177129`、`10.1109/TCSVT.2023.3299314` 等均能解析到对应题名与出版方。
- PowerShell 直接访问 arXiv export API 时出现网络超时；随后以 arXiv 论文页面为准复核核心 arXiv ID。该超时不改变本文档结论，但说明后续若需批量 arXiv 核验，应使用可重试脚本并保存核验日志。
- GitHub 可访问性仍只表示仓库页面可打开，不表示代码可运行、权重可用、协议适配本项目或能直接作为 external baseline。
- 原始三份 Web AI 回答仍只作为方法设计和 related work 输入；项目状态、实验结论和是否通过 gate，仍以本地 manifest、结果表、run report、`eval_bdry.txt`、`show.log` 和结构 proxy 文件为准。

执行边界维持不变：

- 第一轮方法设计仍以 `c01_microstructure_csp_v1` 为单候选、单 gate、单 run 目录计划；该候选在本文档语境中只是设计约束，不是实验结论。
- `168` 张带 GT split 仍是 fixed-detector downstream validation 的第一 gate。
- `full502_clean_v1` 和 `compare9_complete496_v1` 只用于 Stage1 增强指标与 external complete-case 对照，不能替代下游验证。
- `2770` full-pool 不进入；没有 clean manifest、人工复核、gate 通过和显式授权前不得启动。
