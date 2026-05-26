# downstream_driven_v1 Method Design Inputs

Date: 2026-05-26

## Purpose

This document archives three external Web AI answers for designing the `downstream_driven_v1` Stage1 enhancement pipeline.

These answers are raw method-design inputs. They are not verified project facts and must not be treated as experimental conclusions.

## Usage Boundary

- Use these answers as method-design and related-work input only.
- Do not treat any paper, metric, code link, or claim as verified until checked against DOI / arXiv / official page / GitHub.
- Project conclusions must still come from local manifests, run reports, eval files, result tables, logs, and structure proxy outputs.
- Gengkun Wu / G. Wu / 吴庚坤 papers may be used as anchor references for HAB task framing, degradation analysis, enhancement-flow design, metric design, and overlap-risk control.
- However, new candidate literature and first-round candidate pipelines should not be dominated by additional Gengkun Wu papers.
- The two known Wu et al. 2026 papers should be treated as nearest-neighbor anchors, not as project evidence or copied pipelines.

---

## Answer 1


# 第一部分：文献与项目检索 + 核验

## 0. 已知锚点文献，仅作为风险锚点，不计入新增候选

| 锚点                                                                                                                                                                                                                                                       | 核验状态                                                                                                                                                                                                                                         | 对当前任务的作用                                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Enhanced edge detection of harmful algal Blooms using diffusion probability models and Sobel-convolutional attention mechanisms**, Expert Systems with Applications, 2026, DOI: **10.1016/j.eswa.2025.129663**                                         | 已核到 ScienceDirect 条目、题名、作者、DOI、期刊卷期。作者含 **Gengkun Wu**，因此不进入新增候选。该文直接涉及 HAB 显微边缘、blurred contours、impurity bubbles、flagella、diffusion edge detection、Sobel-convolutional attention，以及 HAB-specific enhancement/pyramid fusion 思路。([科学直接][1]) | 作为 **MyEdgeCodex / MSFI 的近邻锚点**。提醒你避免把 Stage1 写成主创新，也避免重复 HAB diffusion-edge 主线。   |
| **Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy**, Image and Vision Computing, 2025, DOI: **10.1016/j.imavis.2025.105466** | 已核到题名、期刊、DOI、作者信息。作者含 **Geng-Kun Wu**，因此只作为锚点。该文涉及 submarine algal microscopy、adaptive color compensation/correction、pyramid image fusion、edge-related evaluation。([科学直接][2])                                                                | 对 Candidate 2 的 HAB-style pyramid fusion 有参考价值，但不能作为新增候选主要来源。                      |
| **Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network**, Engineering Applications of Artificial Intelligence, 2026                                                                           | 只核到 ScienceDirect 搜索条目和摘要片段；打开详情受限，DOI、完整作者、代码状态本轮未完整核验，标记为 **partially verified**。条目描述包含 HAB microscopy、task-oriented enhancement-segmentation、wavelength-selective color attenuation、low contrast、scattering blur。([科学直接][3])              | 作为 **excluded anchor / related only**。可借鉴“增强—分割耦合”的叙事，但不作为 Codex 第一轮 candidate 来源。 |

---

## 1. 新增候选文献 / 项目表，排除 Wu 作者群

### 结论先行

当前最适合你第一轮 Codex 的不是深度 UIE，而是这几类模块：

1. **clipped color compensation + mild local contrast + edge-preserving guard**：低风险建立恢复 baseline。
2. **pyramid / multiscale fusion**：作为第二阶段增强能力更强的候选。
3. **wavelet / frequency decomposition**：和 MSFI spatial-frequency 叙事最自然，但伪边风险更高。
4. **edge-preserving smoothing / texture suppression**：更适合作为 false-edge guard 或失败诊断模块，而不是单独美化增强。
5. **task-friendly / semantic UIE deep methods**：适合作 related work 或 external baseline，不建议第一轮 Codex 实现。

| #  | 论文 / 项目与核验链接                                                                                                                                                                                                            | 对象 / 分类 / 学习属性                                                                                           | 主要模块与可迁移点                                                                                                                                           | 为什么可能利于 downstream edge                                                                                           | 风险                                                                | 优先级与候选方向                                                                         |                       |
| -- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------- |
| 1  | **Underwater Image Enhancement via Minimal Color Loss and Locally Adaptive Contrast Enhancement**, IEEE TIP 2022, DOI: **10.1109/TIP.2022.3177129**。官方项目和代码可核验。([Chongyi Li][4])                                        | underwater；**A/B 类**；非深度学习；不需要训练；适合 OpenCV / numpy 实现。                                                   | minimal color loss、maximum attenuation map guided fusion、locally adaptive contrast enhancement、local mean/variance。                                 | 温和颜色恢复 + 局部对比恢复，有机会提高弱边界梯度而不大幅改变检测器输入分布；论文还报告过对 segmentation / keypoint / saliency 等下游任务的帮助。([PubMed][5])         | 局部对比过强会放大悬浮颗粒、气泡边缘、背景纹理。                                          | **高**。color-compensation、gamma/contrast、conservative baseline、external baseline。 |                       |
| 2  | **Underwater Image Enhancement via Piecewise Color Correction and Dual Prior Optimized Contrast Enhancement**, IEEE SPL 2023, DOI: **10.1109/LSP.2023.3255005**。GitHub 项目可核验。([IEEE信号处理学会][6])                          | underwater；**B/C 类**；非深度学习；不需要训练；可用 OpenCV / numpy 近似。                                                   | piecewise color correction、dual-prior contrast、HSV V 通道 base/detail 分解、texture/spatial priors。                                                      | V 通道细节增强 + spatial/texture prior 可以为弱边界增加局部可分性，同时比全局直方图更可控。                                                       | texture prior 若无 guard，会把背景颗粒当作细节增强。                              | **高-中**。color-compensation、edge-aware contrast、texture-prior candidate。          |                       |
| 3  | **Underwater Image Enhancement Based on Multi-Scale Fusion and Global Stretching of Dual-Model**, Mathematics 2021, DOI: **10.3390/math9060595**。([MDPI][7])                                                            | underwater；**B/C 类**；非深度学习；不需要训练；适合 OpenCV / numpy。                                                      | white balance、RGB full-channel global stretching、Lab L selective stretching、contrast / spatial saliency weight、multi-scale fusion。                  | 可作为 HAB-style pyramid fusion 的非 Wu 来源：用多输入、多权重融合缓解低对比、色偏、照明不均。                                                    | saliency / contrast 权重容易偏好气泡、杂质和高纹理背景。                            | **高**。pyramid-fusion、white-balance、contrast candidate。                           |                       |
| 4  | **HFM: A hybrid fusion method for underwater image enhancement**, Engineering Applications of Artificial Intelligence 2024 / online 2023, DOI: **10.1016/j.engappai.2023.107219**。代码可核验。([科学直接][8])                     | underwater；**A/B 类**；非深度学习 / MATLAB 项目；不需要训练；OpenCV 可近似。                                                 | gray-world、nonlinear color mapping、type-II fuzzy visibility recovery、curve transformation contrast、perceptual fusion。                               | 对散射、低可见度、局部对比恢复有帮助；适合做 external baseline 或 fusion 机制参考。                                                           | visibility / contrast 模块偏强时会造成 halo、伪边、detector gradient shift。   | **中-高**。pyramid-fusion、dehazing/descattering、external baseline。                  |                       |
| 5  | **L2UWE: Low-Light Underwater Image Enhancement Using Local Contrast and Multi-Scale Fusion**, CVPRW / NTIRE 2020, arXiv: **2005.13736**，代码可核验。([CVF开放获取][9])                                                           | low-light underwater；**B/C 类**；非深度学习；不需要训练；可 OpenCV / numpy。                                             | local contrast illumination model、detail enhancement image、darkness removal image、multi-scale fusion、luminance / saliency / local contrast weights。 | 可迁移到 HAB 的非均匀照明、低亮度、弱局部结构恢复。                                                                                      | saliency / local contrast 权重会增强背景悬浮物；darkness removal 可能改变边缘阈值分布。 | **高-中**。illumination-correction、pyramid-fusion、external baseline。                |                       |
| 6  | **Adaptive underwater image enhancement based on color compensation and fusion**, Signal, Image and Video Processing 2023, DOI: **10.1007/s11760-022-02435-5**。([Springer][10])                                         | underwater；**B/C 类**；非深度学习；不需要训练；可实现。                                                                    | adaptive color compensation、color correction、local adaptive contrast、multi-scale fusion。                                                            | 与 HAB 显微色彩衰减、低对比、散射感退化对应；可作为非 Wu 的 fusion 参考。                                                                     | adaptive compensation 若过度，会造成颜色过校正和背景伪边。                          | **中**。color-compensation、pyramid-fusion。                                         |                       |
| 7  | **Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion**, IEEE TCSVT 2024。代码 / 项目可核验；DOI 本轮从非官方引用中见到 **10.1109/TCSVT.2023.3299314**，但未从 IEEE 页面直接展开，标记为 **DOI partially verified**。([GitHub][11]) | underwater；**B/C 类**；非深度学习；不需要训练；DWT 可快速实现。                                                              | attenuation-map color correction、maximum entropy contrast、fast integration local contrast、weighted wavelet fusion、高低频分离。                            | 与 MSFI spatial-frequency 叙事非常匹配：LL 做照明 / 颜色，LH/HL 做弱边界，HH 做噪声抑制。                                                  | 高频增强最容易放大颗粒、气泡、纹理伪边；可能增加 endpoints 和 fragmentation。               | **高**，但不做第一轮。wavelet/frequency candidate。                                        |                       |
| 8  | **An improved semi-supervised segmentation of the retinal vasculature using curvelet-based contrast adjustment and generalized linear model**, Heliyon 2024, DOI: **10.1016/j.heliyon.2024.e38027**。([科学直接][12])        | biomedical microscopy-like / retinal vessel；**A 类**；低学习依赖，GLM 需要训练，但 curvelet/CLAHE preprocessing 可独立实现。 | curvelet-based contrast adjustment、CLAHE、Gabor features、morphology cleaning、automatic threshold。                                                    | retinal vessel 与 HAB flagella / filament-like structures 都涉及细长弱结构；curvelet / directional multiscale 对弱边界方向性有参考价值。 | 细长结构增强也会增强划痕、悬浮颗粒链、背景纹理；CLAHE 过强会伪边。                              | **中-高**。wavelet/frequency、edge-aware preprocessing、related + module source。      |                       |
| 9  | **Pre-processing Image using Brightening, CLAHE and RETINEX**, arXiv 2020, arXiv: **2003.10822**，代码可核验。([arXiv][13])                                                                                                    | general enhancement for edge preprocessing；**A/C 类**；非深度学习；不需要训练；可直接实现。                                  | brightening、CLAHE、Retinex，并用 Canny edge detection 评价 preprocessing。                                                                                 | 对你的任务有直接警示意义：增强不能只看视觉，要看边缘检测输出；CLAHE 可能有效，Retinex 可能降低 sharpness。                                                 | arXiv 项目，非高等级期刊；方法简单；但很适合作为 first candidate 的模块约束证据。              | **高**。CLAHE/Retinex caution、gamma/contrast candidate。                            |                       |
| 10 | **A generalized framework for edge-preserving and structure-preserving image smoothing**, AAAI 2020, DOI: **10.1609/aaai.v34i07.6830**；扩展版 arXiv / 代码可核验。([AAAI Publications][14])                                      | structure-aware smoothing；**B 类**；非深度学习优化；不需要训练；完整复现略重，但可用 guided / bilateral 近似。                        | edge-preserving smoothing、structure-preserving smoothing、texture removal。                                                                           | 可作为 false-edge suppression 的理论来源：先抑制背景纹理，再做温和结构增强。                                                                | 过平滑会损伤 flagella、边界端点和弱边界连续性。                                      | **高-中**。texture-suppression、false-edge suppression、edge-preserving guard。        |                       |
| 11 | **Fast Global Image Smoothing Based on Quasi Weighted Least Squares**, IJCV 2024, DOI: **10.1007/s11263-024-02105-8**，代码可核验。([Springer][15])                                                                            | structure-aware smoothing；**B 类**；非深度学习；不需要训练；当前阶段建议只做近似。                                                | quasi-WLS、global image smoothing、edge-aware decomposition。                                                                                          | 背景纹理抑制 + 结构保留，可降低 background edge noise。                                                                          | 完整算法实现成本高；WLS 参数不当会抹掉弱边界。                                         | **中**。texture-suppression、false-edge suppression；Codex 第一轮不建议完整复现。               |                       |
| 12 | **Image smoothing method based on global gradient sparsity and local relative gradient constraint optimization**, Scientific Reports 2024, DOI: **10.1038/s41598-024-65886-5**。([Nature][16])                           | structure / texture smoothing；**B 类**；非深度学习优化；不需要训练；完整实现成本中等。                                            | global gradient sparsity、local relative gradient constraint、texture suppression。                                                                    | 可为“背景纹理不是边界”的 proxy 设计提供机制依据。                                                                                     | 弱边界也可能被视为小梯度纹理而被抑制。                                               | **中**。related + false-edge suppression module。                                   |                       |
| 13 | **DI-Retinex: Digital-Imaging Retinex Theory for Low-Light Image Enhancement**, IJCV 2025, DOI: **10.1007/s11263-025-02542-z**，arXiv / GitHub 可核验。([Springer][17])                                                      | low-light / Retinex；**A/B 类**；低学习 / 深度混合；通常需要模型推理；不适合第一轮从零实现。                                            | Retinex under digital imaging、noise、quantization、dynamic range、pixel-wise brightness/contrast。                                                      | 可作为 Retinex 风险控制参考：低频照明校正可能有益，但必须管控噪声和局部梯度偏移。                                                                     | Retinex 容易 halo、噪声放大、局部结构断裂；可能造成 detector distribution shift。     | **中**。related / future external baseline，不建议 Codex 第一轮。                          |                       |
| 14 | **Automatic enhancement preprocessing for segmentation of low quality cell images**, Scientific Reports 2024, DOI: **10.1038/s41598-024-53411-7**，代码可核验。([Nature][18])                                                  | cell microscopy；**A 类**；深度 / task-driven；需要训练或已训模型；不适合第一轮。                                               | automatic enhancement preprocessing、segmentation-driven feature maps、low-quality cell image enhancement。                                            | 强支持你的叙事：增强应服务下游 segmentation / boundary，而不是视觉指标。                                                                  | 会引入训练、网络结构、domain shift，掩盖 Stage1 可解释性。                           | **中**。related-work / future baseline。                                            |                       |
| 15 | **LCSeg-Net: A low-contrast images semantic segmentation model with structural and frequency spectrum information**, Pattern Recognition 2024, DOI: **10.1016/j.patcog.2024.110428**。([科学直接][19])                       | low-contrast segmentation；**A 类**；深度模型；需要训练；不适合当前 Stage1 实现。                                             | structural information、frequency spectrum、low-contrast segmentation。                                                                                | 支持“结构 + 频域信息对低对比边界有用”的叙事，可为 MSFI 和 Stage1 frequency candidate 连接。                                                 | 不是增强前处理；训练成本高；不应用来替代 MSFI 主创新。                                    | **中**。related-work only / frequency motivation。                                  |                       |
| 16 | **Task-Friendly Underwater Image Enhancement for Machine Vision Applications**, IEEE TGRS 2024, DOI: **10.1109/TGRS.2023.3340244**，GitHub 可核验。([DBLP][20])                                                              | task-friendly UIE；**A 类**；深度 / CycleGAN-like；需要训练或权重；不建议第一轮。                                             | task-friendly enhancement、machine vision oriented UIE。                                                                                              | 直接支持 downstream-driven 立场。                                                                                        | 黑盒、训练依赖、权重可用性问题、domain mismatch；容易喧宾夺主。                           | **中-低**。external baseline / related only。                                        |                       |
| 17 | **Semantic Attention Guided Underwater Image Enhancement with Multi-Scale Perception**, IEEE TIP 2022, DOI: **10.1109/TIP.2022.3216208**，arXiv / GitHub 可核验。([arXiv][21])                                               | underwater semantic UIE；**A/B 类**；深度模型；需要语义或训练；不适合第一轮。                                                   | semantic attention、multi-scale perception、region-wise degradation。                                                                                  | 可为 edge/background mask 和 region-aware enhancement 提供 related work 支撑。                                            | HAB 无可靠语义标签；黑盒增强会影响 fixed detector 可解释性。                          | **低-中**。related-work only。                                                       |                       |
| 18 | **Semantic-aware Texture-Structure Feature Collaboration for Underwater Image Enhancement**, ICRA 2022, arXiv: **2211.10608**，GitHub 可核验。([GitHub][22])                                                                 | underwater / texture-structure；**A/B 类**；深度模型；需要训练；不适合第一轮。                                               | texture-structure feature collaboration、semantic-aware enhancement、salient-object downstream。                                                       | “texture vs structure”概念对 false-edge suppression 非常有用。                                                            | 实现复杂，依赖训练和语义；不适合可解释 Stage1 v1。                                    | **中-低**。related-work only / concept source。                                      |                       |
| 19 | **ZS2Net: Frequency-aware Semantic Segmentation for Zooplankton Microscopic Image**, Expert Systems with Applications 2026                                                                                              | 只核到 ScienceDirect / AMiner 条目；DOI 与代码本轮未完整核验，标记 **partially verified**。([科学直接][23])                      | zooplankton microscopy segmentation；**A 类**；深度 segmentation；需要训练；不适合 Stage1 v1。                                                                     | frequency-aware segmentation、zooplankton microscopic image。                                                       | 与 HAB 显微弱边界相近，可支撑 frequency-aware related work。                   | 核验不足；不是增强；不建议 Codex 实现。                                                          | **低-中**。related only。 |

---

# 第二部分：方法机制分析

## 2.1 Color channel compensation / white balance

**增强对象**：颜色通道均衡、色偏、通道衰减、局部色彩不一致。

**对应 HAB 退化**：wavelength-selective color attenuation、color inconsistency、低对比藻体结构被背景色偏淹没。

**对 fixed DiffusionEdge / MSFI 的可能正效应**：

* 恢复某些被衰减通道中的边界梯度。
* 降低不同图像之间的颜色分布漂移，使 fixed detector 的输入分布更接近 raw 或训练期分布。
* 对 MSFI 的 spatial-frequency 分支，温和通道补偿可提升低频色彩 / 亮度一致性，不直接强推高频噪声。

**可能提升指标的原因**：

* AP：弱边界响应从低置信区间提升到可排序区间。
* ODS / OIS：全局或图像级最佳阈值更容易覆盖弱边界。
* AC：边缘定位一致性可能改善，尤其是藻体轮廓与背景色差恢复时。
* F1 proxy：边界 recall 提升，precision 不一定损失。

**主要风险**：

* 灰世界或 full-channel stretching 太强，会改变藻体内部纹理、气泡边缘、背景颗粒的颜色梯度。
* 颜色过校正会造成 detector-sensitive local gradient distribution shift。
* RGB 独立增强可能制造虚假 chromatic edges。

**适合作用**：独立 candidate 的前置模块；第一轮应使用 **clipped gray-world / clipped channel gain**，不要用激进颜色映射。

---

## 2.2 Gamma / contrast stretching / CLAHE / local contrast

**增强对象**：亮度、局部对比度、弱梯度、暗区结构。

**对应 HAB 退化**：low contrast、blurred contours、weak boundaries、illumination unevenness。

**对 detector 的可能正效应**：

* DiffusionEdge / MSFI 这类边缘模型通常对局部梯度和结构连续性敏感。温和局部对比增强可让弱边界跨过检测阈值。
* 对 OIS 可能更明显，因为每张图像可由最佳阈值利用增强后的局部梯度。
* 对 AP 可能提升，因为弱边界置信排序更稳定。

**风险机制**：

* CLAHE 本质上会增强局部 histogram 差异；背景颗粒、杂质、气泡边缘会同步变强。
* tile size / clip limit 不当会产生 block artifact 或局部 halo。
* 强 contrast stretching 会增加 endpoints：边界被分段增强，局部断裂更明显。
* Retinex 类方法若未控制噪声，容易降低 sharpness 或产生 halo；已有 Canny preprocessing 项目也把 CLAHE / Retinex 放在边缘检测角度比较，而不是只看视觉效果。([arXiv][13])

**适合作用**：第一轮可用，但必须 mild。建议先限制在 **Lab L 通道、clipLimit ≤ 1.2、gamma 0.95–1.05、percentile stretch 1–99**。

---

## 2.3 Retinex / low-light / illumination correction / dehazing-descattering

**增强对象**：低频照明、暗区、散射、haze-like degradation、global visibility。

**对应 HAB 退化**：scattering blur、uneven illumination、整体低可见度。

**可能正效应**：

* 去除低频照明偏置后，边界响应的相对对比度更稳定。
* 对 MSFI 的 low-frequency / high-frequency 分离叙事有支持价值。
* 对背景不均匀导致的 false positive 可能有抑制作用。

**风险机制**：

* Retinex / dehaze 经常会把噪声、颗粒和气泡边界当作 reflectance detail。
* illumination correction 过强会使藻体内部纹理被误认为边界。
* haze removal 的自然图像假设未必适合显微图像；HAB 显微图像中的“散射感”不等价于自然场景大气散射。
* 对 fixed detector 输入分布影响较大，容易出现 raw 不如、legacy 也未恢复的中间失败态。

**适合作用**：不建议第一轮作为主模块。可以在 Candidate 2 或 Candidate 3 中作为低频分支的 mild correction。

---

## 2.4 Pyramid / multiscale fusion

**增强对象**：多输入版本之间的颜色、亮度、对比、细节、曝光、saliency 综合。

**对应 HAB 退化**：颜色衰减、低对比、照明不均、散射模糊、局部结构不清晰。

**可能正效应**：

* 多尺度融合可避免单一增强策略过度支配。
* contrast / exposure / saliency / edge weight maps 可以把增强集中在候选结构区域。
* 对 ODS / OIS / AP 的提升可能来自弱边界在不同尺度上变得更连续。

**风险机制**：

* saliency / contrast weight map 不知道“藻体边界”和“气泡 / 杂质边缘”的区别。
* Laplacian pyramid 高频层若权重过高，会明显增加 false-edge ratio 和 endpoints。
* 融合输出可能视觉更好，但 detector 对局部梯度分布更敏感，导致 downstream 下降。

**适合作用**：第二优先 candidate。必须加入 **background impurity suppression / false-edge guard**，且 weight map 不允许无限调参。

---

## 2.5 Wavelet / frequency-domain enhancement

**增强对象**：低频照明 / 颜色，LH / HL 方向边界，HH 高频噪声。

**对应 HAB 退化**：weak boundaries、flagella / filament-like tiny structures、blurred contours、background impurities。

**可能正效应**：

* LL 分支做颜色 / illumination correction，避免直接冲击边缘。
* LH / HL 分支增强横纵方向弱边界，可提高 weak boundary recall。
* HH 分支抑制噪声和颗粒纹理，可控制 false-edge ratio。
* 该路线与 **MSFI spatial-frequency weak-boundary diffusion edge detection** 的主创新叙事天然一致。

**风险机制**：

* 高频增强会把气泡边缘、悬浮颗粒、背景纹理同步增强。
* DWT block/ringing artifact 可能造成断裂和 endpoint 增加。
* LH / HL 增益过高会提升 OIS，却损伤 AP / AC，因为排序和定位变不稳定。

**适合作用**：第三优先 candidate。适合作为投稿中“frequency-aware supporting Stage1”的 ablation，但不建议第一轮就上。

---

## 2.6 Edge-preserving smoothing / texture suppression

**增强对象**：背景纹理、细碎噪声、非结构性小梯度，同时保留主结构边界。

**对应 HAB 退化**：background impurities、suspended particles、bubble edges、background texture being enhanced as edges。

**可能正效应**：

* 降低 background edge noise。
* 降低 false-edge ratio。
* 与 conservative sharpening 组合时，可以减少“先锐化后伪边爆炸”。

**风险机制**：

* 过平滑会损伤 flagella、细丝、边界端点。
* guided / bilateral 参数不当会造成局部梯度平台化，导致 weak boundary fragmentation。
* smoothing 本身可能提升 precision，但降低 recall，AP 不一定提升。

**适合作用**：更适合作为 **guard module**，不是单独 enhancement 主线。

---

## 2.7 Task-driven / semantic / deep UIE

**增强对象**：任务相关特征、语义区域、下游可检测结构。

**对应 HAB 退化**：理论上对应所有退化，但依赖训练数据和任务标签。

**正效应**：

* 支持你的基本论点：enhancement 应该由 downstream task 选择，而不是视觉指标选择。
* task-friendly UIE、automatic enhancement preprocessing for segmentation、semantic attention UIE 都能作为 related work 支撑。([DBLP][20])

**风险机制**：

* 需要训练或外部权重。
* 黑盒增强会喧宾夺主，影响 MSFI 主创新。
* domain shift 极大：自然水下 / 低光图像的语义先验不等于 HAB 显微图像。
* 不利于 Codex 快速实现、消融、回滚、解释。

**适合作用**：related work / external baseline。当前阶段不作为 Stage1Codex 主候选。

---

# 第三部分：3–5 个 downstream_driven_v1 candidate pipeline

## Candidate 1：Conservative Color-Structure Preserving Candidate

**优先级**：第一优先。
**是否进入 168 GT downstream gate**：是。
**是否先上 502/496**：否；只有 168 gate 至少最低通过后，再做 502/496 enhancement metrics / complete-case。

### 主要参考

MLLE、PCDE、CLAHE/Retinex edge preprocessing、edge-preserving smoothing。([Chongyi Li][4])

### 方法动机

旧 Stage1 已经证明会损伤 fixed downstream edge detector。第一步不是追求最强视觉增强，而是建立一个 **低风险、结构保持、可回滚、可消融** 的恢复 baseline。

### 模块顺序

1. **degradation diagnosis**

   * 记录 RGB mean/std、Lab L percentile、saturation、Laplacian sharpness、Sobel density、Canny density、HF energy、clipping ratio。
   * 不修改图像，只生成诊断 JSON / CSV。

2. **mild clipped color channel compensation**

   * gray-world / channel mean compensation。
   * 每通道 gain clip：`[1 / gain_clip, gain_clip]`。
   * 推荐 `gain_clip ∈ {1.10, 1.20}`。

3. **mild luminance correction**

   * 只在 Lab L 或 HSV V 通道操作。
   * percentile stretch：固定 `[1, 99]`。
   * gamma：`{1.00, 0.95}`。
   * CLAHE 可选：`clipLimit ∈ {0, 1.2}`，tile size 固定 `8×8` 或 `16×16`。

4. **edge-preserving smoothing**

   * bilateral 或 guided filter。
   * 推荐固定：radius `3`，`sigmaColor 10–25` 或 guided eps `1e-3–1e-2`。
   * 只作为背景纹理抑制，不做强去噪。

5. **conservative sharpening**

   * 只对 L 通道或 grayscale detail。
   * unsharp sigma `1.0–1.5`。
   * amount `{0, 0.15}`。
   * 由 Sobel stable map / saturation mask / texture mask gate，不对全图强锐化。

6. **false-edge guard**

   * 若 enhanced edge density / raw edge density 过大，标记 high-risk。
   * 若 endpoints proxy 或 background edge noise proxy 明显上升，判为失败或降级。

### 小网格搜索

最多 8 个固定参数组合，不允许自由搜索：

| 参数               | 候选             |
| ---------------- | -------------- |
| `gain_clip`      | `1.10`, `1.20` |
| `gamma`          | `1.00`, `0.95` |
| `clahe_clip`     | `0`, `1.2`     |
| `sharpen_amount` | `0`, `0.15`    |

不要全组合爆炸式搜索；用 8 个命名 preset。

### 必须固定

* 不使用 Retinex。
* 不使用 dehazing。
* 不使用 pyramid fusion。
* 不使用 wavelet。
* 不训练 detector。
* 不改 DiffusionEdge / MSFI。
* 不进入 2770 full-pool。

### 预期解决的 HAB 退化

* 温和颜色衰减。
* 低对比弱边界。
* 轻度照明不均。
* 局部结构不清晰。
* 旧 Stage1 过度增强导致的 detector 输入分布偏移。

### 主要风险

* CLAHE 造成背景伪边。
* mild sharpen 仍可能增加 endpoints。
* channel compensation 对色彩很偏的图像可能过校正。

### 失败时观察

* DiffusionEdge AP / AC 是否继续低于 legacy Stage1 Final。
* MSFI 是否单独崩。
* false-edge ratio、endpoints、background edge noise 是否明显高于 raw。
* 弱边界是否更碎，而不是更连续。

---

## Candidate 2：HAB-style Pyramid Fusion Candidate

**优先级**：第二优先。
**是否进入 168 GT downstream gate**：Candidate 1 不足或最低通过后再进入。
**是否适合 502/496**：只有 downstream gate 至少最低通过后。

### 主要参考

MFGS、HFM、L2UWE、MLLE、PCDE；Wu 相关 HAB fusion 只作为 excluded anchor，不作为新增来源。([MDPI][7])

### 方法动机

通过多输入、多尺度、多权重融合，改善颜色衰减、低对比、照明不均和散射感，同时避免单一 CLAHE / Retinex 的过强副作用。

### 模块顺序

1. degradation diagnosis。
2. clipped cyclic / gray-world color compensation。
3. 生成 2–3 个候选输入：

   * WB + mild global stretch。
   * gamma / local contrast version。
   * visibility / detail version。
4. weight maps：

   * contrast weight。
   * exposure weight。
   * saliency weight。
   * edge confidence weight，上限约束。
   * background impurity inverse weight。
5. Gaussian weight pyramid + Laplacian image pyramid。
6. pyramid reconstruction。
7. false-edge guard + downstream gate。

### 推荐参数

| 参数                        | 范围                |
| ------------------------- | ----------------- |
| pyramid levels            | `3`, `4`          |
| contrast weight exponent  | `0.5`, `1.0`      |
| exposure weight exponent  | `0.5`, `1.0`      |
| edge weight cap           | `0.15–0.25`       |
| CLAHE clip                | `0`, `1.2`, `1.5` |
| background inverse weight | `0`, `0.25`       |

### 风险

* 融合权重偏好气泡和颗粒。
* high-frequency Laplacian 层增强导致 false-edge ratio 和 endpoints 上升。
* 视觉更好但 detector 更差。

---

## Candidate 3：Wavelet / Frequency Structure Candidate

**优先级**：第三优先，但与 MSFI 投稿叙事强相关。
**是否进入 168 gate**：适合，但建议在 Candidate 1 之后。
**是否适合 502/496**：只有 downstream gate 通过后。

### 主要参考

Weighted Wavelet Visual Perception Fusion、retinal curvelet preprocessing、LCSeg-Net frequency motivation。([GitHub][11])

### 方法动机

显式分离低频颜色 / 照明与高频结构。增强真实弱边界，抑制 HH 噪声和杂质。

### 模块顺序

1. RGB → Lab，主要处理 L 通道。
2. DWT decomposition：`haar` 或 `db2`。
3. LL：mild gamma / illumination correction。
4. LH / HL：weak-boundary gain。
5. HH：noise damping。
6. inverse DWT。
7. guided filtering。
8. optional conservative sharpen。
9. downstream gate。

### 推荐参数

| 参数             | 范围                     |
| -------------- | ---------------------- |
| wavelet        | `haar`, `db2`          |
| level          | `1`, `2`               |
| LH / HL gain   | `1.05`, `1.10`, `1.20` |
| HH damping     | `0.6`, `0.8`, `1.0`    |
| LL gamma       | `1.00`, `0.95`         |
| sharpen amount | `0`, `0.10`            |

### 必须固定

* 不对 HH 增强，只允许等于或小于 1。
* 不做全图强锐化。
* 不允许超过 12 个参数组合。

### 风险

* 高频伪边。
* ringing artifact。
* 端点增加。
* flagella 可能被增强，但背景细丝 / 杂质也会被增强。

---

## Candidate 4：Edge-aware False-edge Suppression Candidate

**优先级**：备用 / guard candidate。
**定位**：更像失败后的修复方向，而不是第一条增强主线。

### 主要参考

edge-preserving / structure-preserving smoothing、Q-WLS、global gradient sparsity smoothing、texture-structure separation related work。([AAAI Publications][14])

### 模块顺序

1. multi-scale Sobel / Canny stable edge confidence。
2. local entropy / LoG / small component background texture mask。
3. guided / bilateral smoothing on background-dominant areas。
4. gated sharpening only on stable structure。
5. morphology residual analysis。
6. endpoint / fragmentation proxy。
7. downstream gate。

### 推荐参数

| 参数                        | 范围                                                    |
| ------------------------- | ----------------------------------------------------- |
| Sobel scale               | `1`, `2`, `4`                                         |
| guided radius             | `3`, `5`                                              |
| texture entropy threshold | data-driven percentile `70–90%`                       |
| small component area      | dataset-scale fixed, e.g. `< 10–30 px` for proxy only |
| sharpen amount            | `0`, `0.10`                                           |

### 风险

* 删除真实 flagella。
* 弱边界被误判为背景纹理。
* precision 提升但 recall 下降。

---

## Candidate 5：Downstream-gated Parameter Search Candidate

**优先级**：不是独立图像处理方法，而是所有 candidate 的选择机制。
**定位**：用于防止 Codex 无限调参或按视觉指标选模型。

### 模块顺序

1. fixed small parameter grid。
2. enhancement metrics。
3. fixed DiffusionEdge inference。
4. fixed MSFI inference。
5. AP / ODS / OIS / AC。
6. F1 proxy。
7. false-edge ratio。
8. endpoints。
9. background edge noise proxy。
10. Pareto selection。
11. gate decision。
12. research-log.md 同步。

### 核心约束

* 每轮一个 candidate。
* 每轮一个 gate。
* 不允许手工看结果后追加无限参数。
* 失败候选保留为证据。
* 不以 502/496 替代 168 downstream。
* 不进 2770 full-pool。

---

# 第四部分：Codex 执行规划

下面是建议直接交给 Codex 的 prompt。第一轮只做 **Candidate 1：Conservative Color-Structure Preserving Candidate**。

---

```text
任务背景：
我们正在重构 HAB 显微图像 Stage1 enhancement，用于服务 fixed downstream edge detectors，包括 DiffusionEdge 和 MSFI。目标不是视觉美化，也不是替代 MSFI 主创新，而是建立一条 downstream_driven_v1 的结构保持型增强前处理主线。

当前只实现一个 candidate：
Candidate 1 = Conservative Color-Structure Preserving Stage1 enhancement。

参考机制来源：
1. MLLE: Minimal Color Loss + Locally Adaptive Contrast Enhancement, IEEE TIP 2022.
2. PCDE: Piecewise Color Correction + Dual Prior Optimized Contrast Enhancement, IEEE SPL 2023.
3. CLAHE / Retinex edge preprocessing project, arXiv 2020, 用作边缘检测导向的 preprocessing caution。
4. Edge-preserving / structure-preserving smoothing，用作 false-edge guard，不做复杂完整复现。

总原则：
- 单候选。
- 单 gate。
- 单 run directory。
- 可回滚。
- 不自由重构。
- 不无限调参。
- 失败也记录。
- 不覆盖任何已有正式资产。

严禁改动或覆盖：
1. 旧 Stage1 正式主线代码、配置和输出。
2. 任何 GT 文件。
3. 任何 detector 权重。
4. 任何 MAT 文件。
5. 任何正式 output_test 资产。
6. 任何既有结果表、日志、manifest。
7. 2770 full-pool 相关输入、输出和结果。
8. DiffusionEdge / MSFI 模型结构、权重和推理逻辑。
9. 任何 raw baseline 和 legacy Stage1 Final baseline 文件。

新增路径建议，若已存在必须自动加 suffix 或直接报错，不允许覆盖：
- <REPO_ROOT>/stage1_downstream_driven_v1/
- <REPO_ROOT>/stage1_downstream_driven_v1/candidates/conservative_cs_v1.py
- <REPO_ROOT>/stage1_downstream_driven_v1/metrics/enhancement_metrics.py
- <REPO_ROOT>/stage1_downstream_driven_v1/metrics/structure_proxy_metrics.py
- <REPO_ROOT>/stage1_downstream_driven_v1/configs/conservative_cs_v1_168gt.yaml
- <REPO_ROOT>/stage1_downstream_driven_v1/configs/downstream_gate_conservative_cs_v1.yaml
- <REPO_ROOT>/runs/stage1_downstream_driven_v1/conservative_cs_v1_168gt_<YYYYMMDD_HHMMSS>/

输入：
- 使用已有 168 张带 GT split。
- 从配置读取 input image directory、GT directory、raw baseline results、legacy Stage1 Final results、DiffusionEdge wrapper、MSFI wrapper。
- 不假设固定本地路径；所有路径必须来自 YAML config 或命令行参数。

输出：
run_dir 内必须包含：
1. config_frozen.yaml
2. manifest_input.csv
3. manifest_outputs.csv
4. enhanced/<param_id>/<image_name>.png
5. metrics/enhancement_metrics_per_image.csv
6. metrics/enhancement_metrics_summary.csv
7. metrics/structure_proxy_per_image.csv
8. metrics/structure_proxy_summary.csv
9. downstream/diffusionedge/<param_id>/...
10. downstream/msfi/<param_id>/...
11. downstream/downstream_metrics_summary.csv
12. gate/gate_decision.json
13. gate/gate_decision.md
14. logs/run.log
15. logs/no_overwrite_check.txt
16. failure_notes.md
17. research_log_patch.md

实现模块顺序：
A. Degradation diagnosis
- 对 raw image 记录：
  - RGB mean/std
  - Lab L mean/std/p1/p50/p99
  - saturation mean/std
  - clipping ratio at 0 and 255
  - grayscale entropy
  - Laplacian variance
  - Sobel edge density
  - Canny edge density
  - high-frequency energy ratio
- 只记录，不修改图像。

B. Mild clipped color channel compensation
- 使用 gray-world/channel-mean compensation。
- target_mean = mean of three channel means。
- per-channel gain = target_mean / channel_mean。
- gain clip:
  - lower = 1 / gain_clip
  - upper = gain_clip
- gain_clip 只允许 preset 中的 1.10 或 1.20。
- 输出必须 clip 到 uint8 range。
- 禁止 full histogram equalization on RGB channels。

C. Mild luminance correction
- 转到 Lab 或 HSV，只处理 L/V 通道。
- percentile stretch 固定为 [1, 99]。
- gamma 只允许 preset 中的 1.00 或 0.95。
- CLAHE 只允许 clipLimit = 0 或 1.2。
- tileGridSize 固定为 8x8。
- CLAHE clipLimit = 0 表示禁用 CLAHE。
- 禁止 Retinex。
- 禁止 dehazing。
- 禁止全局强对比增强。

D. Edge-preserving smoothing
- 使用 guided filter 或 bilateral filter；如果项目中没有 guided filter 依赖，则使用 OpenCV bilateralFilter。
- 固定参数：
  - bilateral diameter = 3
  - sigmaColor = 15
  - sigmaSpace = 3
- 只作为轻度背景纹理抑制。
- 禁止强 blur。

E. Conservative sharpening
- 只在 luminance/detail 上做 unsharp mask。
- sigma 固定 1.2。
- sharpen_amount 只允许 0 或 0.15。
- 若 sharpen_amount = 0，跳过 sharpen。
- sharpen 后必须计算 edge density increase。
- 若 Sobel edge density ratio > 1.25 或 Canny edge density ratio > 1.25，则标记 high_risk，不删除输出，但 gate 中记录风险。

F. False-edge guard and proxy metrics
- 对每个输出计算：
  - Sobel edge density ratio vs raw
  - Canny edge density ratio vs raw
  - high-frequency energy ratio vs raw
  - clipping increase vs raw
  - skeleton endpoints count if skeletonization available
  - endpoints ratio vs raw if raw proxy可算
  - background edge noise proxy if GT/background mask可用
  - false-edge ratio using GT dilation if GT edge mask可用
  - weak-boundary coverage proxy if GT edge mask可用
- 如果某些 proxy 因依赖缺失不能计算，必须在 missing_metrics 字段中记录，不允许伪造。

参数 preset：
只允许以下 8 个 param_id，不允许扩展：

1. cs_v1_p01_wb110_gamma100_clahe0_sharp0
   - gain_clip=1.10, gamma=1.00, clahe_clip=0, sharpen_amount=0

2. cs_v1_p02_wb110_gamma095_clahe0_sharp0
   - gain_clip=1.10, gamma=0.95, clahe_clip=0, sharpen_amount=0

3. cs_v1_p03_wb110_gamma100_clahe12_sharp0
   - gain_clip=1.10, gamma=1.00, clahe_clip=1.2, sharpen_amount=0

4. cs_v1_p04_wb110_gamma100_clahe0_sharp015
   - gain_clip=1.10, gamma=1.00, clahe_clip=0, sharpen_amount=0.15

5. cs_v1_p05_wb110_gamma095_clahe12_sharp0
   - gain_clip=1.10, gamma=0.95, clahe_clip=1.2, sharpen_amount=0

6. cs_v1_p06_wb110_gamma095_clahe0_sharp015
   - gain_clip=1.10, gamma=0.95, clahe_clip=0, sharpen_amount=0.15

7. cs_v1_p07_wb120_gamma100_clahe0_sharp0
   - gain_clip=1.20, gamma=1.00, clahe_clip=0, sharpen_amount=0

8. cs_v1_p08_wb120_gamma095_clahe12_sharp015_highrisk
   - gain_clip=1.20, gamma=0.95, clahe_clip=1.2, sharpen_amount=0.15
   - 这个 preset 必须标记 high-risk preset，不能作为最终推荐，除非 downstream 明显强通过且 proxy 不劣化。

fixed downstream detector：
- 使用已有 fixed DiffusionEdge 推理脚本 / wrapper。
- 使用已有 fixed MSFI 推理脚本 / wrapper。
- 不得修改模型、权重、阈值搜索逻辑、后处理逻辑。
- 若 wrapper path 不存在，停止 downstream 部分，记录错误；不得伪造 downstream metrics。

需要记录的 downstream metrics：
- DiffusionEdge:
  - AP
  - ODS
  - OIS
  - AC
  - F1 proxy
  - PR curve path if available
- MSFI:
  - AP
  - ODS
  - OIS
  - AC
  - F1 proxy
  - PR curve path if available

需要记录的 structure proxy：
- false-edge ratio
- endpoints count
- endpoints ratio vs raw
- background edge noise proxy
- weak boundary fragmentation proxy
- weak boundary coverage proxy
- Sobel density ratio
- Canny density ratio
- high-frequency energy ratio
- clipping ratio increase
- visual_notes field, initially empty unless automated risk flags触发

baseline 比较：
- raw baseline results 从配置读取。
- legacy Stage1 Final results 从配置读取。
- 不重算、不覆盖。
- 如果 baseline 缺失，gate 输出 status = incomplete_baseline，不得判定通过。

raw-near 定义：
- 对 AP / ODS / OIS：
  raw_near = candidate >= raw - max(0.005, 0.01 * abs(raw))
- 对 AC：
  raw_near = candidate >= raw - max(0.005, 0.01 * abs(raw))
- 对 proxy：
  near_raw_proxy = ratio <= 1.05
  acceptable_proxy = ratio <= 1.15
  catastrophic_proxy = ratio > 1.25

legacy recovery 定义：
- 当 raw > legacy 时：
  recovery_rate = (candidate - legacy) / (raw - legacy)
- 当 raw <= legacy 时：
  不计算 recovery_rate，以 no_collapse 和 raw_near 判断。

Gate 规则：
1. 最低通过 minimum_pass：
   - DiffusionEdge 和 MSFI 都不崩。
   - 不低于 legacy Stage1 Final 明显范围。
   - 当 raw > legacy 时，两个 detector 在 AP 或 ODS 上至少恢复 50% legacy-to-raw loss。
   - false-edge ratio、endpoints ratio、background edge noise proxy 不超过 raw 的 1.25。
   - 没有 catastrophic risk flag。

2. 候选通过 candidate_pass：
   - 至少一个 detector 在 AP/ODS/OIS 中达到 raw-near 或优于 raw。
   - 另一个 detector 不出现 AP/AC/ODS/OIS 明显崩坏。
   - false-edge ratio、endpoints ratio、background edge noise proxy 不超过 raw 的 1.15。
   - F1 proxy 不低于 raw 的 0.95。
   - 不是只靠 high-risk preset 的单 detector 偶然涨点。

3. 强通过 strong_pass：
   - DiffusionEdge 和 MSFI 都达到 raw-near 或优于 raw。
   - false-edge ratio 不劣于 raw 超过 5%。
   - endpoints 不劣于 raw 超过 5%。
   - F1 proxy 不劣于 raw 超过 5%。
   - background edge noise proxy 不劣于 raw 超过 5%。
   - 无明显 over-sharpen / background pseudo-edge risk flag。
   - 最佳参数不是 p08 high-risk preset，除非其它低风险 preset 也接近。

4. 失败 fail：
   - 相对 legacy Stage1 Final 没有恢复。
   - 任一 detector 明显崩坏。
   - enhancement metrics 变好但 downstream edge metrics 变差。
   - false-edge ratio > 1.25 raw。
   - endpoints ratio > 1.25 raw。
   - background edge noise 明显增加。
   - weak boundary fragmentation 增加。
   - 单 detector 偶然涨点，另一个 detector 明显恶化。
   - 参数选择明显过拟合或不可解释。

成功 / 失败后的动作：
- 所有失败 candidate 必须保留 enhanced images、metrics、gate_decision、failure_notes。
- 若 minimum_pass：
  - 冻结当前最佳 param_id。
  - 下一轮只做模块级 ablation，不扩大参数搜索。
  - 可准备 502/496 enhancement metrics complete-case，但不得替代 168 downstream。
- 若 candidate_pass：
  - 冻结最佳 param_id。
  - 做 168 split module ablation。
  - 做 502/496 complete-case enhancement metrics。
  - 准备和 external methods 的 complete-case 对照。
- 若 strong_pass：
  - 冻结 conservative_cs_v1 作为 downstream_driven_v1 初版。
  - 准备投稿证据链。
  - 仍不得直接进入 2770 full-pool；需要单独新任务、新配置、新 run plan。
- 若 fail：
  - 不删除结果。
  - 在 research-log.md 记录失败原因。
  - 下一候选建议按失败类型选择：
    - false-edge/endpoints 上升：转 Candidate 4 false-edge suppression。
    - proxy 安全但恢复不足：转 Candidate 2 pyramid fusion。
    - 颜色已恢复但弱边界仍弱：转 Candidate 3 wavelet/frequency。

research-log.md 同步：
- 不直接覆盖已有段落。
- 追加新条目：
  - 日期时间
  - candidate name
  - run dir
  - config path
  - input split
  - parameter presets
  - best param_id
  - enhancement metrics summary
  - DiffusionEdge metrics
  - MSFI metrics
  - structure proxy metrics
  - gate result
  - failure or success interpretation
  - evidence files
  - next action
- 同时生成 research_log_patch.md，方便人工审查后合并。

最终禁止：
- 禁止进入 2770 full-pool。
- 禁止覆盖旧 Stage1 正式主线。
- 禁止覆盖 GT、权重、MAT、正式 output_test 资产。
- 禁止覆盖既有结果。
- 禁止训练 detector。
- 禁止新增无限参数搜索。
```

---

# 第五部分：风险控制与 gate 细化

## 5.1 推荐统一符号

对每个 detector `d ∈ {DiffusionEdge, MSFI}`，每个指标 `m ∈ {AP, ODS, OIS, AC}`：

* `R[d,m]`：raw baseline。
* `L[d,m]`：legacy Stage1 Final。
* `C[d,m]`：candidate。
* `RR[d,m] = (C[d,m] - L[d,m]) / (R[d,m] - L[d,m])`，仅当 `R[d,m] > L[d,m]` 时定义。

推荐阈值：

| 概念                  | 建议定义                                                 |
| ------------------- | ---------------------------------------------------- |
| raw-near            | `C >= R - max(0.005, 0.01 * abs(R))`                 |
| obvious collapse    | `C < R - max(0.02, 0.05 * abs(R))`，或 `C < L - 0.005` |
| proxy near raw      | proxy ratio `<= 1.05`                                |
| proxy acceptable    | proxy ratio `<= 1.15`                                |
| proxy catastrophic  | proxy ratio `> 1.25`                                 |
| recovery meaningful | `RR >= 0.5` on AP or ODS when raw > legacy           |

---

## 5.2 最低通过 minimum_pass

满足全部条件：

1. **两个 detector 都不崩**
   DiffusionEdge 和 MSFI 均无 AP / ODS / OIS / AC obvious collapse。

2. **相对 legacy Stage1 Final 有恢复**
   当 raw 明显优于 legacy 时，candidate 至少在 AP 或 ODS 上恢复 50% legacy-to-raw loss。

3. **proxy 不灾难性恶化**

   * false-edge ratio `<= 1.25 × raw`
   * endpoints `<= 1.25 × raw`
   * background edge noise `<= 1.25 × raw`
   * F1 proxy `>= 0.90 × raw`

4. **无明显视觉结构灾难**
   自动或人工 notes 中不能出现大范围过锐化、气泡边缘爆炸、弱边界断裂。

最低通过的含义：
它不是最终成功，只说明该 candidate 有恢复价值，值得做模块 ablation 或转入更精确 gate。

---

## 5.3 候选通过 candidate_pass

满足全部条件：

1. **至少一个 detector raw-near 或优于 raw**
   AP / ODS / OIS 至少一个关键指标 raw-near 或更好。

2. **另一个 detector 不崩**
   不能出现 AP / AC / ODS / OIS 明显下降。

3. **proxy 可接受**

   * false-edge ratio `<= 1.15 × raw`
   * endpoints `<= 1.15 × raw`
   * background edge noise `<= 1.15 × raw`
   * F1 proxy `>= 0.95 × raw`

4. **不是单 detector 偶然涨点**
   如果 DiffusionEdge 涨但 MSFI 明显降，或反之，不能 candidate_pass。

5. **参数可解释**
   最佳 preset 不能是唯一高风险极端参数；至少相邻温和参数也应接近。

候选通过的含义：
可以冻结该参数，进入 168 ablation，并开始 502/496 enhancement complete-case 对照。

---

## 5.4 强通过 strong_pass

满足全部条件：

1. DiffusionEdge 和 MSFI 均 raw-near 或优于 raw。
2. AP / ODS / OIS / AC 没有 detector-specific collapse。
3. false-edge ratio 不劣于 raw 超过 5%。
4. endpoints 不劣于 raw 超过 5%。
5. background edge noise 不劣于 raw 超过 5%。
6. F1 proxy 不劣于 raw 超过 5%。
7. 弱边界没有明显 fragmentation。
8. 背景颗粒、气泡、杂质没有被系统性增强成边。
9. 参数不是过拟合搜索结果。
10. 结论能被模块 ablation 解释。

强通过的含义：
可以把该策略冻结为 `downstream_driven_v1` Stage1 支撑主线，并进入投稿证据链整理。仍不建议立即进入 2770 full-pool；需要单独冻结配置和 run plan。

---

## 5.5 失败 fail

出现任一情况即可失败：

* 相对 legacy Stage1 Final 没有恢复。
* 任一 detector 明显崩坏。
* 视觉增强指标提升，但 downstream AP / ODS / OIS / AC 下降。
* false-edge ratio `> 1.25 × raw`。
* endpoints `> 1.25 × raw`。
* background edge noise 明显上升。
* 气泡、杂质、背景颗粒被增强为伪边。
* 弱边界断裂或 fragmentation 增加。
* 只对单 detector 偶然涨点，另一个 detector 恶化。
* 最佳结果只来自极端参数，且不可解释。
* 结果没有 manifest、config、log、evidence file，无法复现。

失败处理：

* 不删除。
* 不覆盖。
* 写入 research-log.md。
* 作为“为什么不采用该增强方向”的投稿负证据。

---

## 5.6 建议结果记录表字段

| 字段                                  | 说明                                                            |
| ----------------------------------- | ------------------------------------------------------------- |
| `candidate_name`                    | conservative_cs_v1 / pyramid_fusion_v1 / wavelet_frequency_v1 |
| `run_dir`                           | 新 run 目录                                                      |
| `code_commit`                       | git commit hash                                               |
| `config_path`                       | frozen config                                                 |
| `config_hash`                       | 配置 hash                                                       |
| `input_split`                       | 168 GT split / 502 / 496                                      |
| `dataset_manifest`                  | 输入 manifest 路径与 hash                                          |
| `parameter_id`                      | preset ID                                                     |
| `parameter_setting`                 | gain_clip, gamma, CLAHE, sharpen 等                            |
| `enhancement_metrics`               | entropy, contrast, sharpness, UCIQE/UIQM if available         |
| `raw_baseline_source`               | raw result table path                                         |
| `legacy_stage1_source`              | legacy result table path                                      |
| `DiffusionEdge_AP`                  | fixed detector AP                                             |
| `DiffusionEdge_ODS`                 | fixed detector ODS                                            |
| `DiffusionEdge_OIS`                 | fixed detector OIS                                            |
| `DiffusionEdge_AC`                  | fixed detector AC                                             |
| `MSFI_AP`                           | fixed detector AP                                             |
| `MSFI_ODS`                          | fixed detector ODS                                            |
| `MSFI_OIS`                          | fixed detector OIS                                            |
| `MSFI_AC`                           | fixed detector AC                                             |
| `F1_proxy`                          | aggregate and per detector if available                       |
| `false_edge_ratio`                  | relative to raw and GT dilation                               |
| `endpoints`                         | skeleton endpoint count and ratio                             |
| `background_edge_noise_proxy`       | background edge density outside GT dilation                   |
| `fragmentation_proxy`               | component count / broken edge proxy                           |
| `weak_boundary_coverage_proxy`      | GT boundary coverage                                          |
| `visual_notes`                      | 自动 flag + 人工 notes                                            |
| `compared_with_raw`                 | better / raw-near / worse                                     |
| `compared_with_legacy_stage1_final` | recovered / not recovered                                     |
| `gate_result`                       | fail / minimum_pass / candidate_pass / strong_pass            |
| `gate_reason`                       | 结构化原因                                                         |
| `evidence_files`                    | CSV, JSON, PR curves, examples, logs                          |
| `next_action`                       | ablation / switch candidate / complete-case / freeze          |

---

# 第六部分：最终排序与明确建议

## 6.1 最推荐优先参考的 3–5 篇论文 / 项目

按当前 Stage1Codex 可执行价值排序：

1. **MLLE, IEEE TIP 2022**
   最适合 Candidate 1。原因是非深度、模块明确、代码可查、颜色损失控制 + 局部对比增强，且有下游任务相关报告。([Chongyi Li][4])

2. **PCDE, IEEE SPL 2023**
   piecewise color correction + dual-prior contrast 对 HAB 色偏和弱边界都有启发；可拆成简单模块。([IEEE信号处理学会][6])

3. **MFGS, Mathematics 2021**
   white balance + stretching + multiscale fusion 是 Candidate 2 的非 Wu 主要来源。([MDPI][7])

4. **L2UWE, CVPRW / NTIRE 2020**
   local contrast + multi-scale fusion 对低光 / 低对比 / 照明不均很有参考价值，且非深度。([CVF开放获取][9])

5. **Weighted Wavelet Visual Perception Fusion, IEEE TCSVT 2024**
   是 Candidate 3 的关键频域来源；但 DOI 本轮未完全从 IEEE 官方展开，应在写论文前再核一次。([GitHub][11])

补充：edge-preserving smoothing / Q-WLS / global gradient sparsity smoothing 更适合作 false-edge suppression 机制支撑，而不是第一轮主线。([AAAI Publications][14])

---

## 6.2 最推荐优先实现的 3 个 candidate pipeline

1. **Candidate 1：Conservative Color-Structure Preserving**

   * 第一优先。
   * 低风险。
   * 最适合证明“旧 Stage1 失败后，新 Stage1 可以恢复 downstream”。
   * 最容易做模块 ablation。

2. **Candidate 2：HAB-style Pyramid Fusion**

   * 第二优先。
   * 增强能力更强。
   * 适合在 Candidate 1 恢复不足但 proxy 安全时切换。

3. **Candidate 3：Wavelet / Frequency Structure**

   * 第三优先。
   * 与 MSFI spatial-frequency 叙事最匹配。
   * 伪边风险更高，所以不建议第一轮。

Candidate 4 更像 guard / failure repair；Candidate 5 是选择机制，不是单独增强方法。

---

## 6.3 第一个应该交给 Codex 实现哪个 candidate？

**实现 Candidate 1：Conservative Color-Structure Preserving Candidate。**

原因：

* 你已经知道旧 Stage1 会损伤 downstream；第一步应验证“温和结构保持增强是否能恢复 raw-near”，而不是直接上复杂融合或深度模型。
* 它的每个模块都能被 OpenCV / numpy / skimage 快速实现。
* 参数少，能严格 gate。
* 失败也能解释：是颜色补偿无效、局部对比过强、sharpen 增加伪边，还是 smoothing 损伤弱结构。
* 不会抢 MSFI 主创新位置。

---

## 6.4 为什么它比直接复现深度学习 UIE SOTA 更适合当前阶段？

深度 UIE SOTA 当前不适合第一轮，原因很明确：

1. 需要训练或外部权重，容易引入不可控变量。
2. domain shift 大：自然水下图像不等于 HAB 显微图像。
3. 黑盒增强会让 reviewer 质疑到底是 MSFI 有效，还是 Stage1 大模型改变了输入。
4. 消融成本高，不利于证明“结构保持型 Stage1 支撑主创新”。
5. fixed downstream detector 的验证目标要求控制变量，深度 UIE 会破坏控制变量。
6. 你的目标是 **downstream-driven Stage1 support**，不是再发一篇 UIE SOTA。

---

## 6.5 哪些方法适合作为 external baseline？

适合作为 external baseline，但不一定作为第一轮 Codex 主线：

* MLLE。
* PCDE。
* MFGS。
* HFM。
* L2UWE。
* Adaptive color compensation + fusion。
* Weighted Wavelet Visual Perception Fusion。
* DI-Retinex，若有可用代码 / 权重且只作 baseline。

这些 baseline 的用途是：

* 502/496 complete-case enhancement metrics。
* 168 downstream sanity comparison。
* 投稿 related / comparison。
* 证明你的 downstream_driven_v1 不是靠视觉指标选出来的。

---

## 6.6 哪些方法只适合 related work，不建议 Codex 当前实现？

* TFUIE：task-friendly UIE 叙事有用，但深度 / 训练 / 权重依赖强。([DBLP][20])
* SGUIE-Net：semantic attention 很有启发，但 HAB 显微无现成语义先验。([arXiv][21])
* STSC：texture-structure collaboration 概念有用，但不是第一轮可解释 Stage1。([GitHub][22])
* AEP cell microscopy：task-driven preprocessing 论点强，但需要训练，适合写 related / future baseline。([Nature][18])
* LCSeg-Net：结构 + 频域 segmentation 相关性强，但不是增强 pipeline。([科学直接][19])
* ZS2Net：zooplankton microscopy frequency-aware segmentation 有相关性，但本轮 DOI / 代码未完整核验，只作 related。([科学直接][23])

---

## 6.7 最可能对 HAB weak-boundary edge detection 有效的传统模块

按优先级：

1. **clipped gray-world / channel compensation**

   * 修正色偏，但不强行重塑颜色分布。

2. **Lab L mild percentile stretch**

   * 增强亮度对比，不破坏 RGB 色彩结构。

3. **low-clip CLAHE**

   * 只在温和参数下使用；clipLimit 不建议超过 1.2–1.5。

4. **guided / bilateral filtering**

   * 用作背景纹理抑制和 false-edge guard。

5. **gated unsharp mask**

   * 只做小 amount，且需要 edge-density / endpoint guard。

6. **DWT LL/LH/HL/HH 分离**

   * LL 做照明，LH/HL 做弱边界，HH 做噪声抑制。

7. **Gaussian / Laplacian pyramid fusion**

   * 适合第二阶段，但必须有 background inverse weight 和 false-edge gate。

8. **morphology / skeleton endpoint proxy**

   * 更适合作评估和 guard，不建议直接删除结构。

---

## 6.8 最应该避免的增强方向

1. 强 CLAHE。
2. RGB 通道独立全局 histogram equalization。
3. 强 Retinex / dehaze。
4. 强 saturation boost。
5. 全图强 unsharp mask。
6. 无 guard 的 high-frequency enhancement。
7. 只按 UIQM / UCIQE / entropy / NIQE 选参数。
8. 只对单 detector 涨点的 detector-specific tuning。
9. GAN / Transformer 黑盒 UIE 作为第一阶段主线。
10. 任何会覆盖旧 Stage1、GT、权重、MAT、output_test、2770 full-pool 的改动。

---

## 6.9 如果第一个 candidate 失败，第二步切换到哪里？

按失败模式切换：

| Candidate 1 失败模式                                     | 下一步                                                 |
| ---------------------------------------------------- | --------------------------------------------------- |
| false-edge ratio / endpoints / background noise 明显上升 | 转 **Candidate 4：Edge-aware False-edge Suppression** |
| proxy 安全，但 AP / ODS / OIS 恢复不足                       | 转 **Candidate 2：HAB-style Pyramid Fusion**          |
| 颜色和亮度恢复，但 weak boundary 仍断裂 / recall 不足              | 转 **Candidate 3：Wavelet / Frequency Structure**     |
| DiffusionEdge 涨、MSFI 崩，或反之                           | 停止该参数族，检查 detector-specific distribution shift      |
| enhancement metrics 好但 downstream 差                  | 记录为负证据，停止视觉指标导向策略                                   |

---

## 6.10 如果第一个 candidate 达到不同 gate，分别怎么推进？

| 结果                 | 下一步                                                                                                                               |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| **fail**           | 保留结果，写 failure_notes 和 research-log；按失败模式切换 Candidate 2 / 3 / 4。                                                                  |
| **minimum_pass**   | 冻结最佳 preset；做模块 ablation：无 WB、无 gamma、无 CLAHE、无 sharpen、无 smoothing；暂不扩大参数。可以做 502/496 enhancement metrics sanity check，但不作为成功证据。 |
| **candidate_pass** | 冻结参数；做 168 full ablation + 502/496 complete-case enhancement metrics；加入 external baseline 对照；整理投稿支撑证据。                            |
| **strong_pass**    | 冻结为 `downstream_driven_v1` 初版；写入方法主线；准备完整 evidence chain。进入 2770 前仍需单独审批式 run plan。                                               |

---

## 6.11 是否应该进入 502/496 complete-case？

**现在不应该先进入。**

进入条件：

* Candidate 1 在 168 GT downstream gate 至少 **minimum_pass**。
* 最好达到 **candidate_pass**。
* 参数已冻结。
* 502/496 只用于 enhancement metrics 和 external method complete-case，对 downstream 结论不替代 168。

---

## 6.12 是否应该进入 2770 full-pool？

**当前不应该进入 2770 full-pool。**

进入条件至少包括：

1. 168 GT split 达到 candidate_pass 或 strong_pass。
2. 完成模块 ablation。
3. 完成 502/496 complete-case。
4. 参数冻结。
5. manifest、config、run_dir、research-log 完整。
6. 明确不会覆盖旧 Stage1、GT、权重、MAT、output_test、既有结果。
7. 单独创建 2770 run plan。

---

## 6.13 最终投稿证据链建议

投稿叙事应保持主次清楚：

### 主创新

**MSFI spatial-frequency weak-boundary diffusion edge detection**

### 支撑创新

**Stage1 task-driven structure-preserving enhancement as downstream input support**

### 证据链

1. 旧 Stage1 Final 负向诊断已经锁定，不重复证明。
2. 文献说明：视觉增强 ≠ downstream edge improvement。
3. 设计少量可解释 Stage1 candidates。
4. 固定 DiffusionEdge / MSFI，不改 detector。
5. 168 GT split 上比较 raw、legacy Stage1 Final、candidate。
6. 记录 AP / ODS / OIS / AC。
7. 记录 false-edge ratio、endpoints、background edge noise、fragmentation。
8. 做模块 ablation 证明哪个模块有效。
9. 失败 candidate 也保留，证明不是 cherry-picking。
10. 502/496 只作为 enhancement complete-case，不替代 downstream。
11. 2770 full-pool 不提前使用，避免数据池污染。
12. 最终把 Stage1 写成 **supporting preprocessing**，不是替代 MSFI 的大增强模型。

---

# 最终明确建议

第一轮执行：

**Codex 只实现 Candidate 1：Conservative Color-Structure Preserving Candidate。**

不要现在做：

* 深度 UIE 复现。
* Retinex / dehaze 主线。
* 大规模 pyramid fusion 参数搜索。
* wavelet 高频增强大网格。
* 502/496 替代 downstream。
* 2770 full-pool。

第一轮成功标准不是“图像更好看”，而是：

1. 相对 legacy Stage1 Final 有恢复；
2. DiffusionEdge 和 MSFI 都不崩；
3. 至少一个 detector raw-near 或更好；
4. false-edge ratio、endpoints、background edge noise 不恶化；
5. 结果能被模块机制解释；
6. 形成可写入 paper 的 downstream-driven Stage1 证据链。

[1]: https://www.sciencedirect.com/science/article/abs/pii/S0957417425032786 "https://www.sciencedirect.com/science/article/abs/pii/S0957417425032786"
[2]: https://www.sciencedirect.com/science/article/pii/S026288562500054X "https://www.sciencedirect.com/science/article/pii/S026288562500054X"
[3]: https://www.sciencedirect.com/science/article/pii/S0952197626012303 "https://www.sciencedirect.com/science/article/pii/S0952197626012303"
[4]: https://li-chongyi.github.io/proj_MMLE "https://li-chongyi.github.io/proj_MMLE"
[5]: https://pubmed.ncbi.nlm.nih.gov/35657839/ "https://pubmed.ncbi.nlm.nih.gov/35657839/"
[6]: https://signalprocessingsociety.org/newsletter/2025/04/underwater-image-enhancement-robust-yet-efficient-dual-prior-optimized-method "https://signalprocessingsociety.org/newsletter/2025/04/underwater-image-enhancement-robust-yet-efficient-dual-prior-optimized-method"
[7]: https://www.mdpi.com/2227-7390/9/6/595 "https://www.mdpi.com/2227-7390/9/6/595"
[8]: https://www.sciencedirect.com/science/article/pii/S0952197623014033 "https://www.sciencedirect.com/science/article/pii/S0952197623014033"
[9]: https://openaccess.thecvf.com/content_CVPRW_2020/html/w31/Marques_L2UWE_A_Framework_for_the_Efficient_Enhancement_of_Low-Light_Underwater_CVPRW_2020_paper.html "https://openaccess.thecvf.com/content_CVPRW_2020/html/w31/Marques_L2UWE_A_Framework_for_the_Efficient_Enhancement_of_Low-Light_Underwater_CVPRW_2020_paper.html"
[10]: https://link.springer.com/article/10.1007/s11760-022-02435-5 "https://link.springer.com/article/10.1007/s11760-022-02435-5"
[11]: https://github.com/Li-Chongyi/WWPF_code "https://github.com/Li-Chongyi/WWPF_code"
[12]: https://www.sciencedirect.com/science/article/pii/S2405844024140583 "https://www.sciencedirect.com/science/article/pii/S2405844024140583"
[13]: https://arxiv.org/abs/2003.10822 "https://arxiv.org/abs/2003.10822"
[14]: https://ojs.aaai.org/index.php/AAAI/article/view/6830 "https://ojs.aaai.org/index.php/AAAI/article/view/6830"
[15]: https://link.springer.com/article/10.1007/s11263-024-02105-8 "https://link.springer.com/article/10.1007/s11263-024-02105-8"
[16]: https://www.nature.com/articles/s41598-024-65886-5 "https://www.nature.com/articles/s41598-024-65886-5"
[17]: https://link.springer.com/article/10.1007/s11263-025-02542-z "https://link.springer.com/article/10.1007/s11263-025-02542-z"
[18]: https://www.nature.com/articles/s41598-024-53411-7 "https://www.nature.com/articles/s41598-024-53411-7"
[19]: https://www.sciencedirect.com/science/article/pii/S0031320324001791 "https://www.sciencedirect.com/science/article/pii/S0031320324001791"
[20]: https://dblp.dagstuhl.de/rec/journals/tgrs/YuSWH24.html "https://dblp.dagstuhl.de/rec/journals/tgrs/YuSWH24.html"
[21]: https://arxiv.org/abs/2201.02832 "https://arxiv.org/abs/2201.02832"
[22]: https://github.com/wdhudiekou/STSC "https://github.com/wdhudiekou/STSC"
[23]: https://www.sciencedirect.com/science/article/pii/S0957417426009851 "https://www.sciencedirect.com/science/article/pii/S0957417426009851"


---

## Answer 2


# 一、最推荐参考文献 / 项目池

## 1.1 最推荐优先参考的 5 篇，不含 Geng-Kun Wu

### Top-1：A generalized framework for edge-preserving and structure-preserving image smoothing

**期刊 / 年份**：IEEE TPAMI 2021。
**作者**：Wei Liu, Pingping Zhang, Yinjie Lei, Xiaolin Huang, Jie Yang, Michael Ng。
**源码**：官方 GitHub 有 MATLAB / C++ 代码。GitHub README 明确写明该仓库释放的是 TPAMI 2021 和 AAAI 2020 两版 *edge-preserving and structure-preserving image smoothing* 代码。([GitHub][1])
**期刊水平**：TPAMI 在 SCImago 多个计算机视觉 / AI / 软件相关类别中长期为 Q1。([Scimago Journal Rank][2])
**对你最有价值的模块**：edge-preserving smoothing、structure-preserving smoothing、texture removal、detail enhancement。
**推荐用途**：第一优先，不作为外部增强 SOTA，而作为 **false-edge suppression / background texture suppression / conservative structure guard** 的理论和模块来源。
**为什么适合 HAB Stage1**：HAB 显微边缘任务的核心不是“增强所有高频”，而是压背景纹理、保真实弱边界。这个工作正好解决“平滑背景但保持结构”的问题。

---

### Top-2：Label-free microscopic cell images adaptive enhancement via weighted fusion of bright, dark, and weak structure features

**期刊 / 年份**：Biomedical Signal Processing and Control 2024。
**作者**：Yongzhao Du, Bo Liu, Haixin Chen, Yuqing Fu。
**源码**：我没有检索到可靠官方源码；但方法模块清晰，Codex 可重写。
**期刊水平**：Biomedical Signal Processing and Control 在 Biomedical Engineering、Health Informatics、Signal Processing 等类别标为 Q1。([Research Journal Rank][3])
**方法要点**：local sliding-window bright/dark feature、guided filtering、multi-scale Gaussian filtering、weak structure feature、weighted fusion；论文摘要明确针对 label-free microscopy 的 low contrast、weak edges、blurry details，并强调 structure protecting 与 uniform background。([科学直接][4])
**推荐用途**：第一优先的显微图像机制参考。
**为什么适合 HAB Stage1**：它不是普通 UIE，而是显微细胞弱结构增强，和 HAB weak boundary / fragile algal structures / background impurity suppression 最接近。

---

### Top-3：Underwater Image Enhancement via Minimal Color Loss and Locally Adaptive Contrast Enhancement

**期刊 / 年份**：IEEE TIP 2022。
**作者**：Weidong Zhang, Peixian Zhuang, Hai-Han Sun, Guohou Li, Sam Kwong, Chongyi Li。
**源码**：官方 MATLAB 代码仓库可用，README 写明包含 MMLE / MLLE 代码和运行方式。([GitHub][5])
**DOI**：`10.1109/TIP.2022.3177129`，PubMed / DBLP 均可核验。([PubMed][6])
**期刊水平**：IEEE TIP 为 Q1；SCImago 页面显示 TIP 在多个计算机图形、软件等类别为 Q1。([Scimago Journal Rank][7])
**方法要点**：minimal color loss、locally adaptive contrast enhancement、Lab color balance、local mean / variance via integral image；论文还报告增强可改善 underwater segmentation、keypoint detection、saliency detection。([PubMed][6])
**推荐用途**：Stage1 的 **mild color compensation + local contrast** 模块来源。
**注意**：不要全量照搬。对 HAB 显微图像，只取 capped color correction 和 local contrast 的保守版本。

---

### Top-4：A Perception-Aware Decomposition and Fusion Framework for Underwater Image Enhancement

**期刊 / 年份**：IEEE TCSVT 2023。
**作者**：Yaozu Kang, Qiuping Jiang, Chongyi Li, Wenqi Ren, Hantao Liu, Pengjun Wang。
**DOI**：`10.1109/TCSVT.2022.3208100`。([Orca][8])
**源码**：GitHub 有 SPDF zip，但仓库规模较小；README 明确介绍 contrast-corrected image、detail-sharpened image、mean intensity / contrast / structure decomposition and fusion。([GitHub][9])
**期刊水平**：TCSVT 为 Q1。([Scimago Journal Rank][10])
**方法要点**：structural patch decomposition、perception-aware fusion、mean/contrast/structure 分量分离。
**推荐用途**：第二优先。适合设计 **structure-aware pyramid / patch decomposition fusion**，但需要加 false-edge guard。
**为什么适合 HAB Stage1**：它不是单纯直方图增强，而是把 mean / contrast / structure 分开处理，适合低频照明与高频边界解耦。

---

### Top-5：TEBCF: Real-World Underwater Image Texture Enhancement Model Based on Blurriness and Color Fusion

**期刊 / 年份**：IEEE TGRS 2022。
**作者**：Jieyu Yuan, Zhanchuan Cai, Wei Cao。
**DOI**：`10.1109/TGRS.2021.3110575`。([矿物数据库][11])
**源码**：官方 / 作者 GitHub 有 MATLAB 实现，README 明确列出论文题名、TGRS、DOI 和 `demo.m` 运行方式。([GitHub][12])
**期刊水平**：TGRS 为 Q1。([Scimago Journal Rank][13])
**方法要点**：blurriness-aware texture enhancement、color fusion、multi-scale fusion、morphological/color compensation。
**推荐用途**：第三优先，作为 **texture-aware fusion / blur-aware enhancement** 参考。
**风险**：HAB 显微背景颗粒、气泡、杂质可能被当作 texture 增强，需要严格 false-edge proxy。

---

## 1.2 扩展 Q1 候选表

| 方法                                                    |                                                                                       Q1 / 源码状态 |  分类 | 是否建议 Codex 当前实现                     | 可迁移模块                                                                      | 主要风险                                           |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------------: | --: | ----------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------- |
| TPAMI 2021 generalized smoothing                      |                                                         TPAMI Q1；官方 MATLAB/C++ 代码 ([GitHub][1]) |   B | **强烈建议抽模块实现**                       | edge-preserving smoothing、structure-preserving smoothing、texture removal   | 移植原代码成本较高；建议用 guided / bilateral / WLS 近似      |
| BSPC 2024 label-free microscopy weak-structure fusion |                                                                     BSPC Q1；未发现官方源码 ([科学直接][4]) | A/B | **建议 Codex 重写简化版**                  | bright/dark feature、weak structure feature、guided filter、多尺度 Gaussian      | weak structure 权重过强会放大背景伪边                     |
| TIP 2022 MLLE / MMLE                                  |                                                               TIP Q1；官方 MATLAB 代码 ([GitHub][5]) | A/B | **建议抽保守模块，不全量照搬**                   | minimal color loss、local adaptive contrast、Lab color balance               | 色彩过校正、局部对比过增强                                  |
| TCSVT 2023 SPDF                                       |                                                               TCSVT Q1；GitHub zip ([GitHub][9]) |   B | 第二优先                                | mean / contrast / structure decomposition-fusion                           | 分解/融合复杂，容易消融不清                                 |
| TGRS 2022 TEBCF                                       |                                                             TGRS Q1；官方 MATLAB 代码 ([GitHub][12]) | B/C | 第三优先                                | blur-aware texture enhancement、color fusion                                | texture enhancement 可能制造伪边                     |
| JOE 2022 ACDC                                         |                                                         IEEE JOE Q1；官方 MATLAB 代码 ([GitHub][14]) | B/C | 可作 external classical baseline      | attenuated color channel correction、detail-preserved contrast              | underwater channel attenuation prior 对显微图像未必成立 |
| TCSVT 2024 ICSP                                       |                                                         TCSVT Q1；官方 MATLAB 代码和数据 ([GitHub][15]) |   B | 备用                                  | illumination channel sparsity prior、non-uniform illumination correction    | 变分恢复可能产生 halo；照明先验需显微重写                        |
| TCSVT 2024 WWPF                                       |                                                            TCSVT Q1；官方 GitHub 代码 ([GitHub][16]) | B/C | 备用                                  | weighted wavelet visual perception fusion、low/high-frequency fusion        | 高频增强可能放大气泡、杂质、背景颗粒                             |
| TPAMI 2021 Zero-DCE++                                 |                                                             TPAMI Q1；代码和模型公开 ([Chongyi Li][17]) | C/A | 只作 external baseline                | zero-reference curve enhancement、lightweight low-light correction          | deep curve 输出可能导致 detector distribution shift  |
| TIP 2023 DehazeFormer                                 |                                                              TIP Q1；PyTorch 代码公开 ([GitHub][18]) |   C | related / external baseline，不建议当前主线 | dehazing / haze-like restoration                                           | 需要训练或预训练；去雾先验不适合显微时风险大                         |
| IJCV 2024 HCLR-Net                                    |                                                           IJCV Q1；PyTorch 代码公开 ([Springer][19]) | A/C | external baseline only              | contrastive regularization、texture restoration                             | 训练依赖重；容易喧宾夺主                                   |
| IJCV 2025 HUPE                                        |                  IJCV Q1；GitHub 公开；论文强调 visual quality 与 downstream task balance ([GitHub][20]) |   A | related / external baseline         | semantic collaborative learning、Fourier reversible mapping                 | 太大，容易把 Stage1 变成主创新                            |
| JOE 2024 Histoformer                                  |                             IEEE JOE Q1；GitHub 公开；DOI `10.1109/JOE.2024.3474919` ([GitHub][21]) |   C | external baseline only              | histogram-based transformer、color distribution learning                    | 深度模型；直方图目标可能不等于边缘友好                            |
| Communications Medicine 2025 UniMIE                   | Communications Medicine Q1；GitHub 公开；training-free diffusion medical enhancement ([GitHub][22]) | A/C | related only，不建议当前 Codex 实现         | medical image enhancement、downstream medical tasks、training-free diffusion | 扩散模型重；生成式先验可能改写细弱边界                            |

---

# 二、方法机制分析：排除 Geng-Kun Wu 后，哪些机制最值得迁移

## 2.1 显微弱结构增强：最贴近 HAB 的机制

**来源**：BSPC 2024 label-free microscopy weak-structure fusion。
**增强对象**：弱边界、暗/亮细节、局部结构、背景均匀性。
**对应 HAB 退化**：

* weak boundaries；
* blurred cell contours；
* fragile algal structures；
* flagella / filament-like structures；
* low contrast；
* uneven background。

**对 DiffusionEdge / MSFI 的潜在收益**：

* 提高 GT edge band 内的边界响应覆盖率；
* 可能提升 ODS / OIS，因为弱边界更连续；
* 对 MSFI frequency branch 有利，因为它不是盲目高频增强，而是带背景抑制的弱结构提取。

**风险**：

* weak structure feature 如果没有 texture-risk 抑制，会把背景颗粒也当成结构；
* guided filtering 太强会抹掉细丝；
* 多尺度 Gaussian 的尺度过大可能造成弱边界变厚，影响 AC。

**结论**：适合做 **Candidate 1 主体**，但必须加 false-edge guard。

---

## 2.2 结构保持平滑：最适合做伪边控制

**来源**：TPAMI 2021 generalized smoothing。
**增强对象**：不是直接增强边缘，而是抑制不稳定纹理、背景噪声、局部高频颗粒，同时尽量保持大结构边界。
**对应 HAB 退化**：

* suspended particles；
* impurity bubbles；
* background texture being enhanced as edges；
* detector-sensitive local gradient shift。

**对 downstream 的潜在收益**：

* 降低 false-edge ratio；
* 降低 endpoints；
* 降低 background edge noise；
* 让 AP 的 precision 端更稳。

**风险**：

* 对真实细弱结构和噪声的区分困难；
* 过强 smoothing 会造成 boundary fragmentation；
* 不能作为单独增强方法，需要和 residual injection 配合。

**结论**：适合作为所有 candidate 的 **guard module**。

---

## 2.3 颜色补偿 + 局部对比：适合保守使用

**来源**：TIP 2022 MLLE、JOE 2022 ACDC。
**增强对象**：颜色偏移、局部亮度、局部对比。
**对应 HAB 退化**：

* wavelength-selective color attenuation；
* color inconsistency；
* low contrast；
* mild scattering blur。

**对 downstream 的潜在收益**：

* RGB 输入分布更稳定；
* 局部边界梯度更可见；
* 对 AP / ODS 可能有帮助。

**风险**：

* 颜色补偿过强会改写 detector 输入分布；
* local contrast enhancement 容易拉起背景杂质；
* Lab-a/b balancing 对 HAB 显微颜色不一定成立。

**结论**：只能做 **mild capped module**，不建议一上来使用原论文完整强增强。

---

## 2.4 Perception-aware / structure decomposition fusion：适合第二轮

**来源**：TCSVT 2023 SPDF。
**增强对象**：mean intensity、contrast、structure 三个分量。
**对应 HAB 退化**：

* 低频照明不均；
* 局部对比不足；
* 弱结构模糊。

**对 downstream 的潜在收益**：

* 分开处理低频和结构信息；
* 可解释性强；
* 适合做 ablation：mean-only、contrast-only、structure-only。

**风险**：

* structure 分量一旦融合权重大，会增强伪边；
* 分解过程比 Candidate 1 复杂；
* 不适合作第一轮恢复 baseline。

**结论**：适合 **Candidate 2**，在 C01 通过最低 gate 后再上。

---

## 2.5 Wavelet / frequency fusion：适合 MSFI 叙事，但风险更高

**来源**：TCSVT 2024 WWPF、TCSVT 2024 ICSP。
**增强对象**：LL 低频照明、LH/HL 方向边界、HH 高频噪声。
**对应 HAB 退化**：

* illumination nonuniformity；
* weak boundary；
* high-frequency impurity noise；
* scattering-like blur。

**对 downstream 的潜在收益**：

* 与 MSFI spatial-frequency 主线叙事自然兼容；
* 可把 Stage1 定义为 frequency-conditioned preprocessing；
* 可能提升 weak-boundary F1 proxy。

**风险**：

* HH 抑制可能删除 flagella；
* LH/HL boost 可能增强气泡边缘；
* inverse DWT 可能产生 ringing；
* 若过度调参，容易变成 detector overfitting。

**结论**：适合 **第三优先**，不适合第一轮。

---

## 2.6 深度 UIE / diffusion / transformer：适合 baseline，不适合主线

**来源**：Zero-DCE++、DehazeFormer、HCLR-Net、HUPE、Histoformer、UniMIE。
这些工作大多有代码，且期刊层级高；其中 Zero-DCE++ 是 TPAMI，DehazeFormer 是 TIP，HCLR-Net / HUPE 是 IJCV，Histoformer 是 IEEE JOE，UniMIE 是 Communications Medicine。([Chongyi Li][17])

**为什么不作为 Stage1 主线**：

* 输出分布不可控；
* 难以解释具体是哪一个增强机制改善 / 损伤 edge detector；
* 可能把论文主创新从 MSFI 转移到 Stage1；
* 对 HAB 显微弱边界可能产生 hallucination、halo、texture rewriting；
* 很难做干净的模块级 ablation。

**结论**：只作为 **external baseline / related work**，不交给 Codex 当前实现为主线。

---

# 三、重新设计的 downstream_driven_v1 candidate pipeline

## Candidate 1：C01-Q1-MicroStructure-CSP，第一优先

### 参考来源

* BSPC 2024 label-free microscopy weak-structure fusion；
* TPAMI 2021 structure-preserving smoothing；
* TIP 2022 MLLE 的 mild color / local contrast 思路。

### 方法动机

旧 Stage1 Final 已经证明强增强会损伤 fixed downstream detector。第一轮应建立一个 **显微弱结构友好、背景伪边受控、颜色/对比仅温和修正** 的恢复 baseline。

### 模块顺序

1. **degradation diagnosis**

   * RGB mean/std；
   * channel imbalance；
   * Lab-L illumination nonuniformity；
   * raw Sobel gradient density；
   * local variance texture risk；
   * saturation ratio。

2. **mild capped gray-world / minimal color-loss approximation**

   * RGB gain 只允许 `[0.90, 1.10]`；
   * 若 channel imbalance 小于阈值，跳过；
   * 不做 red-channel aggressive compensation。

3. **bright / dark local feature extraction**

   * 参考显微弱结构增强；
   * local window 建议 `15 / 31`；
   * bright residual = local bright detail；
   * dark residual = local dark detail；
   * 两者只做小权重融合。

4. **weak structure feature**

   * Lab-L 上使用 guided filter 或 bilateral filter 得到 base；
   * multi-scale Gaussian residual 提取弱结构；
   * structure confidence = multi-scale Sobel consistency；
   * texture risk = local variance / isolated high-frequency residual。

5. **conservative fusion**

   * output_L = raw_L + α1 * local contrast residual + α2 * weak structure residual；
   * residual 权重乘以 `(1 - texture_risk)`；
   * α1、α2 都很小。

6. **false-edge guard**

   * 若 enhanced gradient density、HF energy、background local variance 超过 raw 的 `1.10×`，自动 fallback：

     1. 关 weak structure residual；
     2. 关 local contrast residual；
     3. 只保留 mild WB；
     4. 仍失败则回退 raw-copy，并记录失败。

### 参数范围

* `wb_gain_cap`: `[0.90, 1.10]` 固定；
* `window_size`: `{15, 31}`；
* `guided_radius`: `{5}` 固定；
* `guided_eps`: `{1e-3}` 固定；
* `alpha_contrast`: `{0.00, 0.05, 0.10}`；
* `alpha_structure`: `{0.00, 0.05, 0.10}`；
* `guard_ratio`: `1.10` 固定。

### 小网格

最多 `2 × 3 × 3 = 18` 个配置。
不允许 Codex 自由增加参数。

### 预期收益

* 恢复 weak boundary continuity；
* 降低 background edge noise；
* 提升 F1 proxy / AC；
* 相对 legacy Stage1 Final 有恢复价值。

### 主要风险

* 提升幅度可能小；
* flagella 可能被 smoothing 抹掉；
* weak structure residual 仍可能增强杂质。

### 优先级

**第一优先，直接进入 168 GT split downstream gate。**

---

## Candidate 2：C02-MLLE-SPDF Conservative Fusion，第二优先

### 参考来源

* TIP 2022 MLLE；
* TCSVT 2023 SPDF；
* JOE 2022 ACDC。

### 模块顺序

1. capped color correction；
2. Lab-L local adaptive contrast；
3. 生成两个分支：

   * contrast-corrected branch；
   * detail-preserved branch；
4. 近似 SPDF：

   * mean layer；
   * contrast layer；
   * structure layer；
5. structure layer 加 texture penalty；
6. weighted fusion；
7. false-edge guard。

### 推荐参数

* color gain cap：`[0.90, 1.10]`；
* contrast alpha：`{0.05, 0.10, 0.15}`；
* structure alpha：`{0.00, 0.05, 0.10}`；
* pyramid / decomposition level：固定 `3`；
* texture penalty：固定 `0.5`。

### 优先级

**第二优先。**
当 C01 稳定但提升不足时启用。

---

## Candidate 3：C03-Wavelet Visual-Structure Guard，第三优先

### 参考来源

* TCSVT 2024 WWPF；
* TCSVT 2024 ICSP；
* TPAMI structure-preserving smoothing。

### 模块顺序

1. mild WB；
2. Lab-L；
3. single-level DWT；
4. LL：轻度 illumination correction；
5. LH / HL：weak-boundary directional boost；
6. HH：soft threshold noise suppression；
7. inverse DWT；
8. raw blending；
9. guided cleanup；
10. false-edge guard。

### 参数

* wavelet：固定 Haar；
* level：固定 1；
* LH/HL boost：`{1.00, 1.05, 1.10}`；
* HH threshold：`{0.5σ, 0.75σ}`；
* raw blend：`{0.6, 0.8}`。

### 优先级

**第三优先。**
适合支撑 MSFI spatial-frequency 叙事，但不适合第一轮。

---

## Candidate 4：C04-Texture / Bubble False-Edge Suppression，故障修复候选

### 参考来源

* TPAMI structure-preserving smoothing；
* TEBCF texture / blurriness modeling。

### 模块顺序

1. multi-scale edge stability；
2. local variance texture risk；
3. isolated component / morphology residual；
4. suppress unstable high-frequency residual；
5. only inject residual on stable edge confidence；
6. endpoint / background noise proxy report。

### 使用场景

不是第一轮主线。
当 C01 / C02 出现 false-edge ratio、endpoints、background edge noise 恶化时再启用。

---

## Candidate 5：External Q1 Baseline Sweep，不作为主线

### 候选

* Zero-DCE++；
* DehazeFormer；
* HCLR-Net；
* HUPE；
* Histoformer；
* UniMIE。

### 原则

* 只用官方 pretrained / default inference；
* 不训练；
* 不调参；
* 不进入 Stage1 主线；
* 只作为 external baseline；
* 全部必须通过 fixed DiffusionEdge / MSFI downstream gate。

---

# 四、第一个交给 Codex 的任务：C01-Q1-MicroStructure-CSP

下面是可以直接复制给 Codex 的 prompt。

```text
你现在在 HAB 显微图像 downstream edge detection 仓库中工作。本轮目标是新增一条可回滚的 Stage1 enhancement candidate，名称为：

C01-Q1-MicroStructure-CSP

该 candidate 排除 Geng-Kun Wu 相关文献作为方法来源。参考机制来自：
1. TPAMI 2021 generalized edge-preserving / structure-preserving smoothing；
2. BSPC 2024 label-free microscopic cell weak-structure enhancement；
3. TIP 2022 MLLE 的 mild color correction / local adaptive contrast 思路。

目标：
构建一条保守、显微弱结构友好、背景伪边受控的 Stage1 enhancement pipeline，使其服务 fixed DiffusionEdge / fixed MSFI downstream edge detector。不要追求视觉好看，不要最大化普通增强指标。

本轮只实现一个 candidate：
C01-Q1-MicroStructure-CSP。

严禁：
- 不修改旧 Stage1 Final；
- 不覆盖旧 Stage1 正式输出；
- 不覆盖 GT；
- 不覆盖 detector 权重；
- 不覆盖 MAT；
- 不覆盖正式 output_test；
- 不覆盖既有结果表；
- 不进入 2770 full-pool；
- 不训练 DiffusionEdge；
- 不训练 MSFI；
- 不加入 deep UIE model；
- 不实现 pyramid fusion、wavelet fusion、Retinex heavy、dehazing；
- 不自由扩展参数搜索；
- 不根据单张图手动调参。

新增路径建议：
stage1_downstream_driven_v1/
  enhancers/
    c01_microstructure_csp.py
  configs/
    c01_microstructure_csp.yaml
  metrics/
    enhancement_metrics.py
    structure_proxy.py
  scripts/
    run_c01_microstructure_csp.py
    eval_c01_downstream_gate.py
  README_C01.md

新 run 目录：
runs/downstream_driven_v1/c01_microstructure_csp/YYYYMMDD_HHMMSS/

run 目录必须包含：
- manifest.json
- config_resolved.yaml
- enhanced_images/<config_id>/
- metrics/diagnosis.csv
- metrics/enhancement_metrics.csv
- metrics/structure_proxy_raw_vs_enhanced.csv
- metrics/downstream_diffusionedge.csv
- metrics/downstream_msfi.csv
- metrics/gate_summary.csv
- visual_panels/
- gate_report.md
- failure_notes.md, if failed
- command_log.txt
- git_status.txt
- environment.txt

输入：
- 只使用 168 GT split raw images；
- 保持原始文件名；
- 内部转 float32 [0,1]；
- 输出 RGB uint8；
- 输出到新 run dir。

模块 0：degradation diagnosis
每张图记录：
- RGB mean/std；
- channel imbalance；
- Lab-L mean/std；
- illumination nonuniformity = std(large Gaussian blur of L)；
- Sobel gradient mean / p95；
- gradient density；
- local variance mean / p95；
- saturation ratio；
- image size。

模块 1：mild capped gray-world / minimal color-loss approximation
- 计算 RGB channel means；
- target = mean(channel_means)；
- gain = target / channel_mean；
- clip gain 到 [0.90, 1.10]；
- 若 channel imbalance < 0.03，跳过 WB；
- 不使用 red-channel aggressive compensation。

模块 2：local bright / dark detail features
- 在 Lab-L 上处理；
- window_size 只允许 15 或 31；
- 用 local mean / local max / local min 或 morphology approximation 提取 bright/detail 和 dark/detail；
- 只输出 residual，不直接强增强。

模块 3：weak structure feature
- 使用 guided filter；如果没有 guided filter，则使用 bilateral filter fallback；
- guided_radius 固定 5；
- guided_eps 固定 1e-3；
- multi-scale Gaussian residual scales 固定 [1.0, 2.0, 4.0]；
- structure_confidence = multi-scale Sobel consistency, normalized to [0,1]；
- texture_risk = normalized local variance plus isolated high-frequency residual；
- residual_weight = structure_confidence * (1 - texture_risk)。

模块 4：conservative fusion
- output_L = L + alpha_contrast * contrast_residual + alpha_structure * residual_weight * weak_structure_residual；
- clip to [0,1]；
- 合回 Lab，再转 RGB；
- 不做 RGB 三通道 CLAHE；
- 不做 unsharp mask。

参数网格：
window_size: [15, 31]
alpha_contrast: [0.00, 0.05, 0.10]
alpha_structure: [0.00, 0.05, 0.10]

总配置数最多 18 个。
固定参数：
wb_gain_cap: [0.90, 1.10]
channel_imbalance_skip_threshold: 0.03
guided_radius: 5
guided_eps: 1e-3
gaussian_scales: [1.0, 2.0, 4.0]
false_edge_guard_ratio: 1.10

模块 5：false-edge guard
对 raw 与 enhanced 比较：
- gradient_density；
- high_frequency_energy；
- local_variance_p95；
- saturation_ratio；
若 enhanced 任一风险指标超过 raw 的 1.10 倍：
fallback 1：alpha_structure = 0
fallback 2：alpha_contrast = 0
fallback 3：只保留 mild WB
fallback 4：raw-copy
每张图记录 fallback_level。

enhancement metrics：
对 raw 和 enhanced 均计算：
- entropy；
- RMS contrast；
- Lab-L mean/std；
- gradient mean/p95；
- high-frequency energy；
- local variance mean/p95；
- saturation ratio；
- fallback_level。

fixed downstream evaluation：
- 使用仓库已有 fixed DiffusionEdge 推理和评估脚本；
- 使用仓库已有 fixed MSFI 推理和评估脚本；
- 不训练、不改权重、不改模型结构；
- 每个 config_id 单独输出 prediction 到新 run dir；
- 读取 raw baseline 和 legacy Stage1 Final baseline；若路径缺失，写 missing_baseline，不伪造。

downstream metrics：
- DiffusionEdge AP / ODS / OIS / AC；
- MSFI AP / ODS / OIS / AC；
- F1 proxy；
- false-edge ratio；
- endpoints；
- background edge noise proxy；
- weak-boundary fragmentation proxy。

structure proxy 定义：
- false-edge ratio = predicted edge pixels outside dilated GT edge band / total predicted edge pixels；
- endpoints = skeleton endpoint count / predicted edge length；
- background edge noise = predicted edge density outside dilated GT edge band；
- weak-boundary fragmentation = GT edge band coverage and connected component fragmentation；
- 每个 detector 分开统计。

gate：
最低通过：
- 相对 legacy Stage1 Final 有明显恢复；
- DiffusionEdge 和 MSFI 都不崩；
- false-edge ratio、endpoints、background edge noise 不明显劣于 raw。

候选通过：
- 至少一个 detector 达到 raw-near 或优于 raw；
- 另一个 detector AP / AC / F1 proxy 不明显崩；
- false-edge ratio 和 endpoints 不超过 raw 的 1.10 倍；
- 不是单 detector 偶然涨点。

强通过：
- 两个 detector 都 raw-near 或优于 raw；
- false-edge ratio、endpoints、F1 proxy、background edge noise 均不劣于 raw；
- visual panels 无明显背景伪边、气泡伪边、弱边界断裂。

失败：
- 相对 legacy Stage1 Final 没恢复；
- 任一 detector 明显崩；
- 视觉指标提升但 downstream edge metrics 变差；
- false-edge ratio / endpoints / background edge noise 明显增加；
- 弱边界断裂；
- flagella / filament-like tiny structures 被抹掉；
- 参数结果不可解释。

research-log.md：
在文末追加：
- date/time；
- candidate name；
- run dir；
- commit hash；
- config path；
- input split；
- parameter grid；
- detector versions / weights；
- best config；
- gate result；
- raw vs legacy vs candidate summary；
- failure reason or next action；
- evidence file paths。

成功后的下一步：
- 最低通过：只做 C01 ablation，不进入 502/496，不进入 2770；
- 候选通过：锁定 best config，可进入 502/496 enhancement complete-case；
- 强通过：准备 downstream_driven_v1 evidence package，但仍不自动进入 2770。

最终交付：
- 新代码；
- 新 config；
- 新 run dir；
- CSV metrics；
- gate_report.md；
- research-log.md 追加；
- 不覆盖任何旧资产。
```

---

# 五、downstream gate 细化

## 5.1 Baseline 三角比较

每个 candidate 必须同时比较：

1. **raw input**；
2. **legacy Stage1 Final**；
3. **new C01 / C02 / C03 candidate**。

不要只比较 candidate vs legacy。
真正投稿时必须证明：

* candidate 相对 legacy 有恢复；
* candidate 相对 raw 不显著伤 downstream；
* candidate 对两个 detector 都稳；
* 结构代理没有被视觉指标掩盖。

---

## 5.2 最低通过

必须满足：

* DiffusionEdge 不崩；
* MSFI 不崩；
* 相对 legacy Stage1 Final 恢复至少一半以上的损失；
* AP / AC / F1 proxy 不能继续表现 legacy 的负向影响；
* false-edge ratio ≤ raw 的 `1.10×`；
* endpoints ≤ raw 的 `1.10×`；
* background edge noise ≤ raw 的 `1.10×`；
* visual panel 没有明显气泡伪边、杂质伪边、弱边界断裂。

动作：

* 记录为 recovery candidate；
* 不进入 2770；
* 不进入 502/496；
* 下一轮只做 targeted ablation。

---

## 5.3 候选通过

必须满足：

* 至少一个 detector raw-near 或优于 raw；
* 另一个 detector 没有 AP / AC / F1 proxy 明显崩坏；
* false-edge ratio 和 endpoints 不超过 raw 的 `1.10×`；
* weak-boundary fragmentation 不劣于 legacy；
* 参数来自固定网格；
* 不是单 detector 偶然涨点。

动作：

* 可以进入 502/496 complete-case；
* 可以和 C02 做单候选对比；
* 仍不进入 2770。

---

## 5.4 强通过

必须满足：

* DiffusionEdge 和 MSFI 都 raw-near 或优于 raw；
* AP / ODS / OIS / AC 形成 Pareto 不劣；
* F1 proxy 不劣于 raw；
* false-edge ratio 不劣于 raw；
* endpoints 不劣于 raw；
* background edge noise 不劣于 raw；
* visual panels 无明显过锐化、halo、ringing、气泡伪边、弱边界断裂；
* paired image-level analysis 显示不是少数图像驱动。

动作：

* 锁定为 downstream_driven_v1 Stage1 candidate；
* 准备 evidence package；
* 可做 502/496 complete-case；
* 2770 full-pool 仍需单独 gate。

---

## 5.5 失败

任一成立即可失败：

* 相对 legacy 没恢复；
* 任一 detector 明显崩；
* 视觉指标变好但 downstream 变差；
* false-edge ratio 明显增加；
* endpoints 明显增加；
* background edge noise 明显增加；
* 气泡、颗粒、杂质被增强成边；
* flagella / filament 被抹掉；
* weak boundary fragmentation 增加；
* 只对一个 detector 涨点，另一个 detector 明显恶化；
* 参数结果不可解释；
* 覆盖了旧资产。

失败动作：

* 保留 run；
* 写 `failure_notes.md`；
* 更新 `research-log.md`；
* 作为投稿负证据，说明为什么普通增强 / 强结构增强不适合 fixed downstream edge detection。

---

# 六、最终排序与执行建议

## 6.1 最推荐优先参考的 3–5 篇

按“能否帮助 Codex 构造可验证 Stage1 candidate”排序：

1. **TPAMI 2021 generalized edge-/structure-preserving smoothing**
   用于 background texture suppression、false-edge guard、structure-preserving smoothing。([GitHub][1])

2. **BSPC 2024 label-free microscopic weak-structure enhancement**
   用于显微弱边界 / 弱结构增强，是最贴近 HAB microscopy 的非 Geng-Kun Wu 参考。([科学直接][4])

3. **TIP 2022 MLLE / MMLE**
   用于 mild color correction 和 local adaptive contrast，不全量照搬。([GitHub][5])

4. **TCSVT 2023 SPDF**
   用于 mean / contrast / structure decomposition fusion。([GitHub][9])

5. **TGRS 2022 TEBCF**
   用于 blur-aware texture enhancement 和 color fusion，但必须加 false-edge guard。([GitHub][12])

---

## 6.2 最推荐优先实现的 3 个 pipeline

1. **C01-Q1-MicroStructure-CSP**
   第一优先。目标是先建立 conservative recovery baseline。

2. **C02-MLLE-SPDF Conservative Fusion**
   第二优先。当 C01 稳定但提升不足时，用 structure-aware decomposition fusion 提升幅度。

3. **C03-Wavelet Visual-Structure Guard**
   第三优先。用于强化 MSFI spatial-frequency 叙事，但必须防伪边。

---

## 6.3 第一个应该交给 Codex 的 candidate

**C01-Q1-MicroStructure-CSP。**

理由：

* 直接针对显微弱结构；
* 不依赖 Geng-Kun Wu 文献；
* 不需要训练；
* 机制可解释；
* 可用 OpenCV / numpy / skimage 重写；
* 适合做 clean ablation；
* 不会喧宾夺主；
* 失败也能形成有效证据。

---

## 6.4 哪些方法适合作 external baseline

适合：

* Zero-DCE++；
* DehazeFormer；
* HCLR-Net；
* HUPE；
* Histoformer；
* UniMIE；
* MLLE / ACDC / TEBCF 原始官方代码输出。

但规则是：

* 不训练；
* 不调参；
* 不作为 Stage1 主线；
* 输出只进入 fixed DiffusionEdge / MSFI downstream gate；
* 若视觉指标提升但 edge gate 失败，记录为负证据。

---

## 6.5 哪些方法只适合 related work，不建议当前实现

不建议当前 Codex 作为主线实现：

* HUPE：虽然 task-aware，但 semantic collaborative learning 太重；
* HCLR-Net：需要训练 / 对比学习；
* Histoformer：histogram transformer + GAN refinement，输出分布不可控；
* DehazeFormer：dehazing prior 对显微液体环境未必成立；
* UniMIE：training-free diffusion 很有 related work 价值，但扩散生成式先验可能改写细弱边界；
* Zero-DCE++：可作 baseline，但 curve enhancement 对 edge detector 的局部梯度分布影响不可控。

---

## 6.6 最可能有效的传统模块

按推荐顺序：

1. guided / bilateral / WLS-like edge-preserving smoothing；
2. local bright / dark feature residual；
3. multi-scale weak-structure residual；
4. capped gray-world / minimal color-loss approximation；
5. Lab-L mild local contrast；
6. texture-risk weighted residual injection；
7. false-edge guard；
8. low-frequency illumination correction；
9. LH/HL directional weak-boundary boost；
10. HH soft-threshold noise suppression。

---

## 6.7 最应该避免的方向

当前应避免：

* aggressive Retinex；
* high clipLimit CLAHE；
* strong unsharp mask；
* aggressive red-channel compensation；
* dehazing / transmission map 强恢复；
* 直接最大化 entropy / contrast；
* pyramid fusion 无 texture penalty；
* wavelet 高频全局增强；
* deep UIE 输出直接作为主线；
* 根据单 detector 涨点调参；
* 使用 GT 参与 enhancement mask；
* 进入 2770 full-pool。

---

## 6.8 如果 C01 失败，第二步怎么做

按失败模式切换：

* **false-edge ratio / endpoints / background noise 变差**：转 C04 false-edge suppression；
* **两个 detector 都稳定但提升太小**：转 C02 MLLE-SPDF conservative fusion；
* **弱边界仍断裂，MSFI frequency branch 不受益**：转 C03 wavelet visual-structure guard；
* **只有一个 detector 涨点**：暂停调参，做 detector sensitivity analysis；
* **C01 接近 raw 但无明显提升**：保留为 safe baseline，再比较 C02。

---

## 6.9 是否进入 502/496 complete-case

**C01 未达到候选通过前，不进入。**

进入条件：

* 至少 candidate pass；
* fixed DiffusionEdge / MSFI gate 完整；
* structure proxy 没有明显恶化；
* best config 已锁定。

502/496 只用于：

* enhancement metrics；
* complete-case consistency；
* external baseline 对照；

不能替代 168 GT split downstream gate。

---

## 6.10 是否进入 2770 full-pool

**当前不进入。**

进入 2770 的最低条件：

* 168 GT split 强通过；
* 502/496 complete-case 无明显结构风险；
* best config 固定；
* evidence package 完整；
* 新 run 目录；
* 不覆盖旧 full-pool 结果；
* 单独开 full-pool gate。

---

# 最终结论

排除 Geng-Kun Wu 后，最稳的 Stage1 路线不是继续找 HAB 专属 SOTA，而是转向 **Q1 顶刊中的显微弱结构增强 + 结构保持平滑 + 保守颜色/对比修正 + downstream gate**。

第一步应执行：

> **C01-Q1-MicroStructure-CSP**
> 以 BSPC 2024 显微弱结构增强为显微机制源，以 TPAMI 2021 structure-preserving smoothing 为伪边控制源，以 TIP 2022 MLLE 的保守颜色/局部对比思想为轻量补偿源，在 168 GT split 上用 fixed DiffusionEdge / MSFI 做 downstream gate。

这条线最符合你当前目标：
**Stage1 只做 downstream-driven structure-preserving input support；MSFI spatial-frequency weak-boundary diffusion edge detection 仍是主创新。**

[1]: https://github.com/wliusjtu/Generalized-Smoothing-Framework "GitHub - wliusjtu/Generalized-Smoothing-Framework: This is the released code for the following papers: A generalized framework for edge-preserving and structure-preserving image smoothing. Liu W, et al., TPAMI 2021, AAAI 2020 · GitHub"
[2]: https://www.scimagojr.com/journalsearch.php?q=24254&tip=sid&utm_source=chatgpt.com "IEEE Transactions on Pattern Analysis and Machine Intelligence"
[3]: https://researchjournalrank.com/journal/biomedical-signal-processing-and-control "Biomedical Signal Processing and Control — SJR 1.336, Q1, H-Index 141 | Research Journal Rank"
[4]: https://www.sciencedirect.com/science/article/abs/pii/S1746809424000314?utm_source=chatgpt.com "Label-free microscopic cell images adaptive enhancement via weighted ..."
[5]: https://github.com/Li-Chongyi/MMLE_code "GitHub - Li-Chongyi/MMLE_code: MMLE_Code_TIP2022 · GitHub"
[6]: https://pubmed.ncbi.nlm.nih.gov/35657839/?utm_source=chatgpt.com "Underwater Image Enhancement via Minimal Color Loss and Locally ..."
[7]: https://www.scimagojr.com/journalsearch.php?q=25534&tip=sid&utm_source=chatgpt.com "IEEE Transactions on Image Processing - Scimago Journal & Country Rank"
[8]: https://orca.cardiff.ac.uk/id/eprint/154044/?utm_source=chatgpt.com "A perception-aware decomposition and fusion framework for underwater ..."
[9]: https://github.com/59Kkk/SPDF "GitHub - 59Kkk/SPDF · GitHub"
[10]: https://www.scimagojr.com/journalsearch.php?q=26027&tip=sid&utm_source=chatgpt.com "IEEE Transactions on Circuits and Systems for Video Technology"
[11]: https://zh.mindat.org/reference.php?id=15557431&utm_source=chatgpt.com "Yuan, Jieyu, Cai, Zhanchuan, Cao, Wei (2022) TEBCF: Real-World ..."
[12]: https://github.com/bilityniu/TEBCF_tgrs "GitHub - bilityniu/TEBCF_tgrs: [TGRS 2021] TEBCF: Real-World Underwater Image Texture Enhancement Model Based on Blurriness and Color Fusion · GitHub"
[13]: https://www.scimagojr.com/journalsearch.php?q=17360&tip=sid&utm_source=chatgpt.com "IEEE Transactions on Geoscience and Remote Sensing"
[14]: https://github.com/Li-Chongyi/JOE2021_ACDC "GitHub - Li-Chongyi/JOE2021_ACDC: This repository provides the matlab code of our work on underwater image enhancement · GitHub"
[15]: https://github.com/Hou-Guojia/ICSP "GitHub - Hou-Guojia/ICSP · GitHub"
[16]: https://github.com/Li-Chongyi/WWPF_code/blob/main/README.md "WWPF_code/README.md at main · Li-Chongyi/WWPF_code · GitHub"
[17]: https://li-chongyi.github.io/Proj_Zero-DCE%2B%2B.html "Learning to Enhance Low-Light Image via Zero-Reference Deep Curve Estimation"
[18]: https://github.com/IDKiro/DehazeFormer "GitHub - IDKiro/DehazeFormer: Vision Transformers for Single Image Dehazing · GitHub"
[19]: https://link.springer.com/article/10.1007/s11263-024-01987-y?utm_source=chatgpt.com "HCLR-Net: Hybrid Contrastive Learning Regularization with Locally ..."
[20]: https://github.com/ZengxiZhang/HUPE/?utm_source=chatgpt.com "GitHub - ZengxiZhang/HUPE: Extention version of the paper \"Waterflow ..."
[21]: https://github.com/ytpeng-aimlab/Histoformer?utm_source=chatgpt.com "GitHub - ytpeng-aimlab/Histoformer: Histoformer-Histogram-based ..."
[22]: https://github.com/Feynben/UniMIE?utm_source=chatgpt.com "GitHub - Feynben/UniMIE: Communications Medicine 2025"


---

## Answer 3



## 第一部分：文献与项目检索 + 核验

### 1.1 两个 HAB 锚点核验结论

你给出的两个锚点方向基本成立，但需要区分“已核验”和“仍需 BibTeX 精确确认”的部分。

**ESWA 2026 HAB diffusion edge detection** 已核验：题名为 *Enhanced Edge Detection of Harmful Algal Blooms Using Diffusion Probability Models and Sobel-Convolutional Attention Mechanisms*，来源为 *Expert Systems with Applications*，卷 298，Article 129663，DOI 为 `10.1016/j.eswa.2025.129663`；检索结果显示其针对 HAB 边缘检测中的 blurred cell contours、impurity bubbles 等问题，并结合 diffusion probability model 与 Sobel-convolutional attention。项目页存在，但 README 表示代码和数据仍在整理后公开，不应把它当作当前可直接复现代码源。([科学直接][1])

**EAAI 2026 HAB enhancement-segmentation coupling** 也已核验：题名为 *Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network*，来源为 *Engineering Applications of Artificial Intelligence*，ScienceDirect 条目显示其关注 wavelength-selective color attenuation、low contrast、scattering blur 对 HAB 显微分割的影响，并提出 enhancement-and-segmentation framework。可访问检索片段显示 PII 为 `S0952197626012303`、Article 114948，但 DOI 没有在抓取片段中直接暴露；正式投稿前建议从 ScienceDirect 导出 BibTeX 再锁定 DOI。([科学直接][2])

---

### 1.2 候选论文 / 项目表

| #  | 论文 / 项目核验信息                                                                                                                                                                                                                                                                                                                                                                         | 对象、分类、学习属性                                                                           | 主要模块与可迁移部分                                                                                                                                   | 对 downstream edge detection 的价值、风险、优先级                                                                                                                                                                                 |
| -- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | *Enhanced Edge Detection of Harmful Algal Blooms Using Diffusion Probability Models and Sobel-Convolutional Attention Mechanisms*，2026，*Expert Systems with Applications*，DOI `10.1016/j.eswa.2025.129663`；项目页存在但代码尚未完整释放。([科学直接][1])                                                                                                                                               | HAB edge detection；**A 类**；深度方法，需要训练；不适合作为 Stage1 Codex 直接实现。                        | diffusion edge detection、Sobel-convolutional attention、HAB weak contour / impurity bubble 问题定义。                                              | **高优先级 related work**。最适合作为 MyEdgeCodex / MSFI 主线近邻文献，而不是 Stage1 enhancement 候选。风险：若把它当 Stage1，会喧宾夺主。方向：related-work only / downstream detector context。                                                               |
| 2  | *Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network*，2026，*Engineering Applications of Artificial Intelligence*，Article 114948；官方条目已核验，DOI 需 BibTeX 再确认。([科学直接][2])                                                                                                                                                    | HAB microscopy segmentation；**A 类**；包含增强 + 分割网络；增强部分可能低学习依赖，分割部分需要训练。                | wavelength-selective color attenuation、low contrast、scattering blur 诊断；pyramid fusion enhancement；dual-branch segmentation。                  | **高优先级方法来源**。增强机制非常贴近 downstream_driven_v1，但不要复现其 segmentation network。风险：pyramid fusion 可能增强背景杂质。方向：HAB-style pyramid-fusion candidate。                                                                               |
| 3  | *Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy*，2025，*Image and Vision Computing*，DOI `10.1016/j.imavis.2025.105466`。检索片段显示 AWBCC、IPF、gray-world、MCCAG、ECH 等模块，并报告对 edge detection / keypoint matching 有帮助。([X-MOL][3])                               | submarine algal microscopy；**A/B 类**；基本属于非深度或低学习依赖；无需训练；OpenCV/numpy 可近似实现。          | adaptive white balance color compensation、gray-world、maximum color channel attention guidance、empirical contrast enhancement、pyramid fusion。 | **高优先级**。适合作为 Candidate 2 的主要来源。风险：多模块叠加容易过增强，可能放大气泡边缘和背景颗粒。方向：color-compensation / pyramid-fusion / external baseline。                                                                                                |
| 4  | *Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion*，2024，*Multimedia Tools and Applications*，DOI `10.1007/s11042-023-16258-0`。官方摘要显示其针对 HAB 图像 color distortion、blurred details，采用 cyclic color compensation、three-image multi-scale fusion、redefined weight maps。([Springer][4])                                            | ocean HAB underwater images；**A/B 类**；非深度；无需训练；OpenCV/numpy 可实现。                     | cyclic color compensation、多输入图像生成、多尺度融合、weight maps、低频伪影控制。                                                                                  | **高优先级**。非常适合迁移到 Stage1 的颜色补偿 + pyramid fusion。风险：cyclic compensation 可能导致颜色过校正；weight map 可能偏向背景高频。方向：color-compensation / pyramid-fusion candidate。                                                                  |
| 5  | *Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion*，2023，*Applied Intelligence*，DOI `10.1007/s10489-023-04502-x`。摘要显示其针对 seawater impurities、suspended particle deposits、high-speed cell motions 导致的 blurred cell textures / poor clarity，结合 homomorphic filtering、EMD、CLAHS、dual-image wavelet fusion。([Springer][5]) | HAB image enhancement；**A/B 类**；非深度；无需训练；numpy / pywt / skimage 可实现。                 | homomorphic filtering、EMD feature map、CLAHS/CLAHE、wavelet fusion、高低频分离。                                                                      | **高优先级但风险高**。适合 Candidate 3 wavelet/frequency。风险：HH 高频会把悬浮颗粒和杂质增强成伪边；EMD 实现复杂度高于 wavelet。方向：wavelet/frequency candidate。                                                                                               |
| 6  | *SFMnet: Edge detection of HABs based on spatial feature mapping encoder-decoder network*，2024，*Ocean Engineering*，DOI `10.1016/j.oceaneng.2024.118547`。检索结果显示其包含 HAB 图像增强算法和深度边缘检测模型。([科学直接][6])                                                                                                                                                                                   | HAB edge detection；**A 类**；深度网络，需要训练；不适合当前 Stage1 Codex 直接实现。                        | underwater restoration、depth/transmission 估计、spatial feature mapping edge detector。                                                          | **中高优先级 related work**。可用于论证 HAB edge detection 的退化背景，但不建议作为 Stage1 candidate。风险：物理深度 / transmission prior 对显微图像未必成立。方向：related-work only / external context。                                                          |
| 7  | *Label-free microscopic cell images adaptive enhancement via weighted fusion of bright, dark, and weak structure features*，2024，*Biomedical Signal Processing and Control*，DOI `10.1016/j.bspc.2024.105973`。摘要显示其针对 low contrast、weak edges、blurry details，使用局部 sliding-window bright/dark detail、guided filtering、多尺度 Gaussian filtering 和 weighted fusion。([CoLab][7])            | microscopy / cell image enhancement；**B 类**；非深度；无需训练；非常适合 OpenCV/numpy/skimage。      | bright feature、dark feature、weak structure feature、guided filtering、multi-scale Gaussian、weighted fusion、background uniformity。              | **第一优先级核心来源**。与 HAB weak boundary、fragile structures、background impurity suppression 高度匹配。风险：弱结构权重设计不当会平滑 flagella / filament。方向：conservative color-structure preserving / texture-suppression / edge-aware candidate。 |
| 8  | *Automatic enhancement preprocessing for segmentation of low quality cell images*，2024，*Scientific Reports*。论文明确将 enhancement preprocessing 用于 low-quality cell image segmentation，并报告对 cell membrane 等分割有帮助。([Nature][8])                                                                                                                                                          | cell image segmentation preprocessing；**A 类**；深度模型，需要训练；不适合当前直接实现。                   | task-oriented preprocessing、feature aggregation、低质量图像到易识别图像的变换。                                                                              | **中优先级 related work**。适合支持“增强必须由下游任务验证”的叙事。风险：需要训练，无法作为快速 Stage1 模块。方向：task-driven related-work only。                                                                                                                  |
| 9  | *Feature Preserving Smoothing Provides Simple and Effective Data Augmentation for Medical Image Segmentation*，2020，MICCAI，DOI `10.1007/978-3-030-59710-8_12`。论文指出 feature-preserving smoothing 可减少噪声和高频纹理，同时保留语义边界。([Springer][9])                                                                                                                                                  | medical segmentation / preprocessing；**A/B 类**；非深度预处理；无需训练；OpenCV 可近似实现。             | feature-preserving smoothing、texture suppression、boundary preservation。                                                                      | **高优先级模块来源**。适合 false-edge suppression 和 conservative smoothing。风险：过强平滑会消除细丝、鞭毛和弱边界端点。方向：edge-preserving smoothing / texture-suppression candidate。                                                                    |
| 10 | *Retinex-Centered Contrast Enhancement Method for Histopathology Images with Weighted CLAHE*，2022，*Arabian Journal for Science and Engineering*，DOI `10.1007/s13369-021-06421-w`。论文使用 HSV/V-channel multi-scale Retinex 与 L*a*b* luminosity weighted CLAHE 增强组织图像亮度和局部细节。([Springer][10])                                                                                           | histopathology enhancement；**B/C 类**；非深度；无需训练；skimage/OpenCV 易实现。                    | MSR Retinex、weighted CLAHE、亮度通道增强、局部细节增强。                                                                                                    | **中优先级**。适合低对比和照明不均，但必须极保守。风险：CLAHE/Retinex 极易增加背景纹理和 halo。方向：Retinex/CLAHE candidate。                                                                                                                                 |
| 11 | *Underwater image enhancement via adaptive white-balancing and multi-restored image fusion*，2024，Springer 期刊，DOI `10.1007/s10043-024-00941-0`。摘要显示其包含 adaptive color compensation、Gray World 选择性校正、ambient light / transmission 估计、多恢复结果融合和 gradient matrix weight。([Springer][11])                                                                                                 | underwater image enhancement；**B/C 类**；低学习依赖；无需训练；部分模块可实现。                           | adaptive white balance、color unevenness 判断、multi-restored image fusion、gradient weight。                                                      | **中优先级**。可迁移颜色不一致校正和梯度权重融合。风险：transmission / ambient light prior 对显微图像可能失真。方向：white-balance / pyramid-fusion / external baseline。                                                                                      |
| 12 | *An Adaptive Underwater Image Enhancement Framework via Multi-Domain Fusion and Color Compensation*，2025，arXiv `2503.03640`。摘要显示其组合 CLAHE、Gamma、Retinex、Gaussian/bilateral/guided filtering、Fourier/wavelet filtering 和自适应颜色补偿。([arXiv][12])                                                                                                                                        | underwater enhancement / fusion；**C 类**；主要是可组合传统模块；无需训练；Codex 可快速搭建近似版。              | CLAHE、Gamma、Retinex、spatial filtering、frequency filtering、color compensation。                                                                | **中优先级模块清单**。适合作为 pipeline 设计参考，不建议完整照搬。风险：模块太多，消融不清晰。方向：multi-domain module map / related-work。                                                                                                                       |
| 13 | *Enhanced Edge-Perceptual Guided Image Filtering*，2023，arXiv `2310.10387`，DOI `10.48550/arXiv.2310.10387`。论文在 guided filtering 中加入一阶 edge-protect constraint 和 residual constraint。([arXiv][13])                                                                                                                                                                                    | edge-preserving filtering；**B/C 类**；非深度；无需训练；可用 guided filter + residual guard 近似。   | edge-aware guided filtering、residual constraint、detail enhancement、多尺度曝光融合。                                                                  | **中高优先级模块来源**。适合 conservative sharpening 和 false-edge guard。风险：实现原文完整优化较费时；建议先近似。方向：edge-aware sharpening / false-edge suppression。                                                                                    |
| 14 | *A generalized framework for edge-preserving and structure-preserving image smoothing*，AAAI 2020 / TPAMI 2021；官方 GitHub 提供 MATLAB/C++ 代码。([GitHub][14])                                                                                                                                                                                                                             | general edge/structure-preserving smoothing；**B/C 类**；非深度；无需训练；Python 复刻有成本。         | edge-preserving smoothing、structure-preserving smoothing、texture removal。                                                                    | **中优先级备用模块**。适合背景纹理抑制。风险：原代码非 Python，Codex 直接移植成本高。方向：texture-suppression / related-work / backup implementation。                                                                                                      |
| 15 | *Downstream Task Inspired Underwater Image Enhancement: A Perception-Aware Study from Dataset Construction to Network Design*，2026，arXiv / code project DTIUIE。论文明确指出 UIE 常被用作 segmentation / detection 预处理，而视觉增强 SOTA 不一定改善下游任务；项目提供代码。([arXiv][15])                                                                                                                               | underwater enhancement for downstream tasks；**A 类**；深度模型，需要训练或预训练；不适合当前 Stage1 主线实现。 | task-inspired UIE、downstream segmentation/detection evaluation、task-aware dataset。                                                           | **高优先级叙事来源**。可用于支撑 fixed downstream gate 的必要性。风险：作为 Stage1 会变成大模型增强主创新。方向：task-driven related-work / external baseline。                                                                                                |
| 16 | *Segmentation-Driven Image Enhancement Based on Deep Reinforcement Learning*，2024，ECAI，DOI `10.3233/FAIA240488`。论文用多个传统滤波器作为 action，由 RL 按 segmentation mIoU 控制滤波权重。                                                                                                                                                                                                                | defect segmentation preprocessing；**A 类**；RL，需要训练；不适合当前实现。                           | segmentation-driven filter selection、weighted classical filters、task metric feedback。                                                        | **中优先级思想来源**。适合启发 Candidate 5：不用 RL，用固定小网格 + downstream gate。风险：RL 过重，且易过拟合。方向：automatic parameter-search related-work。                                                                                                |
| 17 | *WWE-UIE: A Wavelet & White Balance Efficient Network for Underwater Image Enhancement*，2026，WACV / arXiv，代码可用。论文包含 adaptive white balance、wavelet enhancement block、Sobel gradient-aware module。([arXiv][16])                                                                                                                                                                      | underwater enhancement；**A/B 类**；轻量深度网络；需要预训练或训练；Codex 不应从零实现。                       | white balance、wavelet decomposition、Sobel gradient-aware gating。                                                                             | **中优先级 external baseline / related work**。模块思想可迁移，但不建议作为 Stage1 主线。风险：网络输出分布可能对 fixed HAB detector 产生未知 shift。方向：external baseline / related-work。                                                                     |
| 18 | *Underwater Scene Enhancement via Adaptive Color Analysis and Multi-Space Fusion*，2025，IEEE Journal of Oceanic Engineering，DOI `10.1109/JOE.2025.3591405`；项目 CDEF 提供 MATLAB 代码。([GitHub][17])                                                                                                                                                                                       | underwater enhancement；**B/C 类**；偏传统 / 低学习依赖；MATLAB 代码可作外部 baseline。                 | adaptive color-tone analysis、degradation compensation、YUV multi-scale exposure pyramid fusion、dehazing/sharpening。                           | **中优先级 external baseline**。可作为 classical fusion baseline。风险：海水成像假设与 HAB 显微成像不完全匹配。方向：external baseline / pyramid-fusion reference。                                                                                     |

---

## 第二部分：方法机制分析

### 2.1 颜色补偿 / 白平衡 / 通道补偿

**增强对象**：RGB 通道均值、通道比例、颜色一致性、部分亮度偏差。
**对应 HAB 退化**：wavelength-selective color attenuation、color inconsistency、染色或显微照明导致的通道偏移。HAB 与 underwater microscopy 文献均明确关注颜色衰减和色彩失真问题。([科学直接][2])

**对 fixed DiffusionEdge / MSFI 的潜在正作用**：

* 边缘检测器虽然最终关注梯度，但 RGB 到特征空间的早期响应会受通道偏移影响。
* 温和通道补偿可让藻体边界与背景之间的 luminance/chrominance contrast 更稳定。
* 对 AP / AC 可能有帮助，因为弱边界候选更容易从背景中分离。

**主要风险**：

* 通道 gain 过大时，背景杂质、气泡边缘、染色噪声也会被拉开。
* red / blue channel compensation 若照搬 underwater UIE，可能不适合显微图像，造成颜色过校正。
* 对 detector 来说，颜色分布 shift 可能比视觉改善更危险。

**当前建议**：只作为 **mild capped module**，不作为强增强主角。优先使用 gray-world / capped channel gain，gain cap 建议 `0.85–1.15`，最多不超过 `0.80–1.20`。

---

### 2.2 Gamma / contrast stretching / CLAHE / Retinex

**增强对象**：亮度、局部对比、低频照明、暗区可见性、局部梯度。
**对应 HAB 退化**：low contrast、uneven illumination、scattering-like blur、弱边界对比不足。Retinex + weighted CLAHE 在 histopathology 中用于改善低亮度、低对比和局部细节；HAB pyramid / fusion 方向也强调 low contrast 和 scattering blur。([Springer][10])

**潜在正作用**：

* 弱边界的局部梯度增强，可能提升 ODS / OIS。
* 如果 AP 曲线在中低阈值区域 recall 不足，轻度局部对比增强可能提高 AP。
* 对 MSFI 的 spatial-frequency 分支可能有利，因为低频照明和高频边界更可分。

**主要风险**：

* CLAHE clipLimit 过高会把背景颗粒增强成伪边。
* Retinex 容易产生 halo，造成边界两侧虚假梯度。
* Gamma 过强会压缩或拉伸局部灰度，使 fixed detector 的输入分布偏移。
* 最容易导致 false-edge ratio、background edge noise、endpoints 增加。

**当前建议**：只使用 **mild luminance-only enhancement**。不要在 RGB 三通道直接做强 CLAHE。推荐 Lab-L 或 HSV-V 通道，`clipLimit <= 1.0 or 1.5`，gamma 搜索只在 `0.95–1.05` 或 `0.90–1.10` 内。

---

### 2.3 去雾 / descattering / transmission-map restoration

**增强对象**：散射雾化、低频 veil、背景 haze、远近深度相关衰减。
**对应 HAB 退化**：scattering blur、显微液体介质中的低对比 haze-like degradation。

**潜在正作用**：

* 如果 HAB 图像确实存在均匀 veil，轻度去雾可增加藻体边界与背景差异。
* 可能提高边缘 detector 的 confidence map。

**主要风险**：

* underwater dehazing 的 dark channel / red channel / transmission 先验对显微图像未必成立。
* transmission map 错误会导致 halo、局部过锐化和颜色漂移。
* 气泡、悬浮颗粒可能被解释为结构或深度变化，导致强伪边。

**当前建议**：不作为第一轮 candidate。若使用，只能做 very mild low-frequency correction，不做 aggressive dehazing。

---

### 2.4 Edge-preserving smoothing / texture suppression

**增强对象**：背景高频纹理、噪声、局部随机颗粒，同时保留较稳定边界。
**对应 HAB 退化**：background impurities、suspended particles、impurity bubbles、background texture being enhanced as edges。医学图像 segmentation 的 feature-preserving smoothing 已被用于降低高频纹理并保持语义边界。([Springer][9])

**潜在正作用**：

* 降低 false-edge ratio 和 background edge noise。
* 减少 AP 曲线中的 false positive。
* 对 AC 可能更有帮助，因为边缘图与 GT 结构更一致。

**主要风险**：

* flagella、filament-like tiny structures 与噪声在频率上相似，可能被一起平滑掉。
* 过强 smoothing 会导致 weak boundary fragmentation 或 endpoint 增加。
* 如果 smoothing 后再 sharpening，可能产生假轮廓。

**当前建议**：作为 Candidate 1 的核心保护模块。使用 guided filter / bilateral filter / rolling-guidance-style approximation，但强度必须小，并保留 raw residual。

---

### 2.5 Pyramid fusion / multi-scale fusion

**增强对象**：多尺度亮度、颜色、对比、显著性、曝光、边缘权重。
**对应 HAB 退化**：颜色衰减、低对比、照明不均、散射模糊、局部弱边界。HAB cyclic color compensation + multi-scale fusion、submarine algal microscopy AWBCC + pyramid image fusion、EAAI HAB enhancement-segmentation 都直接支持该方向。([Springer][4])

**潜在正作用**：

* 多输入变体可分别解决颜色、亮度、局部对比。
* Laplacian pyramid 可把边界细节从高频层注入，同时避免全局过亮。
* 如果加入 edge / texture guard，有机会形成比单一 CLAHE 更稳定的 Pareto 改善。

**主要风险**：

* weight map 容易选择高频背景杂质。
* 融合后边缘分布变化大，fixed detector 可能崩。
* 多模块不消融会导致论文叙事不清。

**当前建议**：作为第二优先 pipeline。必须设置 background impurity suppression 和 false-edge guard。

---

### 2.6 Wavelet / frequency-domain structure enhancement

**增强对象**：LL 低频照明、LH/HL 方向性边界、HH 高频噪声和颗粒。
**对应 HAB 退化**：low-frequency illumination shift、weak boundary、scattering blur、细小结构与噪声混杂。HAB EMD + wavelet fusion 明确把 wavelet fusion 用于 HAB 图像增强。([Springer][5])

**潜在正作用**：

* 低频照明和高频结构可分开处理，适合 MSFI spatial-frequency 叙事。
* LH / HL 可增强方向性边界，HH 可做软阈值抑制噪声。
* 对 weak-boundary F1 proxy 可能有利。

**主要风险**：

* HH 抑制过强会损失 flagella / filament。
* LH/HL boost 会增强气泡边缘和颗粒边缘。
* inverse DWT 可能产生 ringing 或 block artifact。
* 对 DiffusionEdge 输入分布可能产生非自然纹理。

**当前建议**：第三优先或备用。适合当 Candidate 1 稳定但提升不足时使用。

---

### 2.7 Edge-aware false-edge suppression / morphology residual

**增强对象**：真实藻体边界与背景伪边的区分。
**对应 HAB 退化**：impurity bubbles、background impurities、suspended particles、false-edge amplification、endpoint increase。

**潜在正作用**：

* 降低 background edge noise。
* 减少 endpoints 和碎裂边缘。
* 对 AC 和 precision 端有帮助。

**主要风险**：

* morphology mask 可能把真实小结构误判为杂质。
* 稳定边界通常更粗，而 weak boundary 本身不稳定，过强筛选会漏检。
* 如果依赖 GT 设计 mask，会造成不可部署或评估泄漏。

**当前建议**：作为 Candidate 4，或作为 Candidate 1 / 2 的 guard module。不要在 enhancement 阶段使用 GT；GT 只能用于 downstream gate 计算 proxy。

---

### 2.8 Downstream-gated parameter search

**增强对象**：不是图像本身，而是增强参数选择机制。
**对应问题**：视觉指标与下游 segmentation/detection/edge detection 不一致。DTI-UIE 和低光照增强综述都指出，视觉质量更好的增强并不必然带来下游任务收益。([arXiv][15])

**潜在正作用**：

* 直接用 fixed DiffusionEdge / MSFI 选择 Pareto candidate。
* 避免把 UIQM、UCIQE、entropy、NIQE 当最终目标。
* 失败配置也能作为负证据。

**主要风险**：

* 168 GT split 上过拟合。
* 只对单 detector 偶然涨点。
* 参数网格过大导致不可解释。

**当前建议**：必须存在，但只能是 **small predefined grid + fixed gate**，不能变成无限调参。

---

## 第三部分：3–5 个 downstream_driven_v1 candidate pipeline

### Candidate 1：C01-Conservative Color-Structure Preserving，第一优先

**主要参考**：label-free microscopic cell weighted fusion、feature-preserving smoothing、Retinex/weighted CLAHE、HAB color compensation 文献。([CoLab][7])

**方法动机**：旧 Stage1 Final 已证明会损伤 fixed downstream detector。因此第一轮不应追求强增强，而应先建立一个“不会破坏边缘分布”的保守恢复 baseline。

**模块顺序**：

1. **Degradation diagnosis**

   * 统计 RGB mean/std、channel imbalance、Lab-L illumination nonuniformity、raw Sobel gradient density、local variance texture proxy。
   * 只记录，不作为复杂学习决策。

2. **Mild capped gray-world / channel compensation**

   * RGB gain 按 gray-world 估计，但 gain 限制在 `[0.85, 1.15]`。
   * 若 channel imbalance 很小，直接跳过。

3. **Luminance-only mild gamma / contrast**

   * 转 Lab，仅处理 L。
   * gamma grid：`[0.95, 1.00, 1.05]`。
   * CLAHE clipLimit grid：`[0.0, 1.0]`；`0.0` 表示禁用 CLAHE。
   * tileGrid 固定 `8×8`。
   * percentile stretch 只允许 `1–99%`，blend 固定 `<=0.10`，默认可关闭。

4. **Edge-preserving smoothing**

   * guided filter 或 bilateral filter 得到 base。
   * guided radius 固定 `5`，eps 固定 `1e-3` 或按 `[0,1]` 归一化后的 `1e-4–1e-3`。
   * 不做强 denoise。

5. **Conservative structure residual**

   * residual = enhanced_L - guided_base。
   * 只在 structure confidence 较高、texture/background proxy 较低区域注入。
   * sharpen_alpha grid：`[0.0, 0.15]`。
   * 暂不使用 `0.25`，避免第一轮过锐化。

6. **False-edge guard**

   * 比较 output 与 raw 的 gradient density、high-frequency ratio、local variance background proxy。
   * 若 output 的 proxy 超过 raw 的 `1.10×`，自动降级到更保守版本：先关 sharpening，再关 CLAHE，最后回退到 mild WB + gamma。

**推荐小网格搜索**：

* `gamma ∈ {0.95, 1.00, 1.05}`
* `clahe_clip ∈ {0.0, 1.0}`
* `sharpen_alpha ∈ {0.0, 0.15}`
* 总计 `3 × 2 × 2 = 12` 个配置。

**必须固定，避免无限调参**：

* WB gain cap：`±15%`
* guided radius：`5`
* guided eps：固定一个值
* CLAHE tileGrid：`8×8`
* gradient guard 阈值：`1.10× raw`
* 不加入 dehazing、不加入 Retinex heavy mode、不加入深度网络。

**输入输出格式**：

* 输入：raw RGB images，保持原始文件名。
* 输出：RGB uint8 PNG/TIF，另存到新 run dir。
* 同步输出 per-image JSON/CSV：diagnosis、参数、fallback 状态、enhancement proxy。

**预期解决的 HAB 退化**：

* mild color inconsistency；
* low contrast；
* weak boundaries；
* uneven illumination 的轻度版本；
* background texture over-enhancement 风险。

**对 downstream edge detection 有利的原因**：

* 不剧烈改变 detector 输入分布。
* 增强弱边界但不过度拉背景纹理。
* 通过 false-edge guard 控制 endpoints 和 background edge noise。

**主要风险**：

* 提升幅度可能小。
* 对严重 scattering blur 或颜色衰减不足。
* 若 guard 太严格，可能接近 raw，缺乏显著改善。

**失败时观察**：

* AP 是否仍低于 raw 很多；
* MSFI 是否比 DiffusionEdge 更敏感；
* false-edge ratio 是否虽然没涨但 recall 不足；
* weak boundary fragmentation 是否仍高。

**优先级**：第一优先。
**是否进入 168 GT split downstream gate**：是，直接进入。
**是否进入 502/496 complete-case**：只有达到候选通过或强通过后再进入；最低通过阶段不建议扩展。

---

### Candidate 2：C02-HAB-Style Pyramid Fusion，第二优先

**主要参考**：EAAI 2026 HAB pyramid enhancement-segmentation、MTA cyclic color compensation + multi-scale fusion、IVC AWBCC + IPF。([科学直接][2])

**方法动机**：HAB 显微图像同时存在颜色衰减、低对比、照明不均、散射模糊和 fragile structure。单一 gamma 或 CLAHE 难以覆盖这些退化，多输入 pyramid fusion 可以把不同增强分支按权重组合。

**模块顺序**：

1. degradation diagnosis；
2. cyclic / capped color compensation；
3. 生成 3 个输入分支：

   * WB/color corrected branch；
   * mild gamma/contrast branch；
   * edge-preserving smoothed + weak sharpen branch；
4. 计算 weight maps：

   * contrast weight；
   * exposure weight；
   * saliency weight；
   * edge weight；
   * texture/background penalty weight；
5. Gaussian pyramid 分解 weight maps；
6. Laplacian pyramid 分解 image branches；
7. pyramid fusion；
8. guided filter cleanup；
9. false-edge guard。

**推荐参数范围**：

* color gain cap：`±20%`
* gamma：`[0.90, 1.00, 1.10]`
* CLAHE clipLimit：`[0.5, 1.0, 1.5]`
* pyramid levels：`3–5`，第一轮固定 `4`
* edge weight coefficient：`0.2–0.5`
* texture penalty coefficient：`0.3–0.7`

**小网格搜索**：

* gamma branch strength；
* CLAHE clip；
* texture penalty coefficient。

**必须固定**：

* pyramid levels；
* branch 数量；
* weight map 公式；
* 不允许 Codex 添加新分支；
* 不允许加入 deep UIE model。

**适用退化**：

* color attenuation；
* low contrast；
* uneven illumination；
* scattering-like blur；
* weak structure visibility。

**下游价值**：

* 可能比 Candidate 1 提供更明显 recall 提升。
* 若 texture penalty 有效，可同时控制 false edge。

**主要风险**：

* weight map 选择背景颗粒；
* pyramid fusion 产生 halo；
* 过多模块导致消融复杂。

**优先级**：第二优先。
**168 gate**：适合，但建议在 Candidate 1 后。
**502/496**：候选通过后再做 complete-case。

---

### Candidate 3：C03-Wavelet / Frequency Structure，第三优先

**主要参考**：HAB EMD + wavelet fusion、WWE-UIE 的 white-balance + wavelet + Sobel gradient-aware 思想。([Springer][5])

**方法动机**：MSFI 主线包含 spatial-frequency weak-boundary detection，Stage1 可以做轻量低频 / 高频分离，让输入更适合 MSFI，但不能替代 MSFI。

**模块顺序**：

1. mild WB；
2. Lab-L 或 grayscale luminance；
3. single-level 或 two-level DWT；
4. LL：mild gamma / illumination correction；
5. LH/HL：weak boundary boost；
6. HH：soft threshold suppression；
7. inverse DWT；
8. guided filter cleanup；
9. conservative sharpening；
10. false-edge guard。

**推荐参数范围**：

* wavelet：第一轮固定 Haar；备用 db2。
* decomposition level：固定 `1`，备用 `2`。
* LH/HL boost：`1.05–1.20`
* HH threshold：`0.5σ–1.0σ`
* LL gamma：`0.95–1.05`
* output blend with raw：`0.5–0.8`

**小网格搜索**：

* LH/HL boost；
* HH threshold；
* raw blend ratio。

**必须固定**：

* 不引入 EMD 第一轮实现；
* 不做复杂 Fourier filter search；
* 不加入 detector feedback inside enhancement。

**适用退化**：

* weak boundary；
* low-frequency illumination inconsistency；
* high-frequency noise / suspended particles；
* blurred contours 的轻度恢复。

**下游价值**：

* 对 MSFI 的 frequency branch 叙事高度一致。
* 可能提升 weak-boundary F1 proxy。

**主要风险**：

* 高频伪边；
* ringing；
* flagella 被 HH threshold 删除；
* 对 DiffusionEdge 输入分布产生不自然纹理。

**优先级**：第三优先或备用。
**168 gate**：适合，但不应先于 Candidate 1。
**502/496**：仅候选通过后进行。

---

### Candidate 4：C04-Edge-Aware False-Edge Suppression，故障修复型候选

**主要参考**：feature-preserving smoothing、edge-perceptual guided filtering、structure-preserving smoothing。([Springer][9])

**方法动机**：如果 Candidate 1/2 提升了视觉指标但 false-edge ratio、endpoints、background edge noise 变差，需要一个专门抑制伪边的 Stage1 variant。

**模块顺序**：

1. raw multi-scale Sobel/Canny edge stability map；
2. local variance / texture map；
3. bubble / particle morphological residual proxy；
4. guided/bilateral background smoothing；
5. edge-aware residual sharpen，仅作用在 stable edge confidence 区域；
6. suppress unstable isolated high-frequency residual；
7. output edge-risk report。

**推荐参数范围**：

* stable edge threshold：top `20–40%` gradient but multi-scale consistent；
* local variance threshold：top `10–20%` as risky texture；
* morphology kernel：`3, 5, 7`，第一轮固定 `5`；
* sharpen alpha：`0.10–0.20`。

**小网格搜索**：

* stable edge threshold；
* sharpen alpha；
* background smoothing strength。

**必须固定**：

* 不使用 GT 生成 enhancement mask；
* 不使用 detector prediction 反向修改 image；
* 不做 per-image manual tuning。

**适用退化**：

* impurity bubbles；
* suspended particles；
* background texture；
* false-edge amplification。

**下游价值**：

* 主要提升 precision / AC；
* 降低 endpoints；
* 避免 weak boundary 被背景噪声淹没。

**主要风险**：

* 把真实细丝误当伪边；
* weak boundary 本身不稳定，可能被抑制；
* 若过强，会导致 recall 和 AP 降低。

**优先级**：备用 / 错误修复型。
**168 gate**：当 false-edge failure 明确时进入。
**502/496**：不建议单独先做。

---

### Candidate 5：C05-Downstream-Gated Parameter Search，选择机制而非增强算法

**主要参考**：DTI-UIE、SDIE、低光照 downstream review。([arXiv][15])

**方法动机**：让参数由 fixed DiffusionEdge / MSFI gate 选择，而不是由视觉指标选择。

**模块顺序**：

1. 固定一个 candidate enhancement，例如 C01；
2. 固定小网格；
3. 对 168 GT split 生成增强图；
4. fixed DiffusionEdge inference；
5. fixed MSFI inference；
6. 计算 AP / ODS / OIS / AC / F1 proxy；
7. 计算 false-edge ratio / endpoints / background edge noise / fragmentation；
8. Pareto selection；
9. 写 manifest、CSV、gate report、research-log。

**推荐参数范围**：只使用当前 candidate 的预定义网格。
**禁止**：Bayesian search、PSO 大搜索、RL、per-image detector feedback、无限调参。
**优先级**：所有 candidate 都应配套，但不单独作为 Stage1 方法。
**168 gate**：必须使用。
**502/496**：只做通过后的完整增强指标对照。

---

## 第四部分：Codex 执行规划：第一个 candidate 的可复制 prompt

下面是建议直接交给 Codex 的 prompt。它只实现 **C01-Conservative Color-Structure Preserving**，只跑一个 downstream gate，不进入 2770 full-pool。

```text
你现在在一个已有 HAB 显微图像边缘检测仓库中工作。目标不是重构旧 Stage1，也不是实现大型 UIE SOTA，而是新增一个可回滚的 downstream_driven_v1 Stage1 enhancement candidate，用于服务 fixed DiffusionEdge / fixed MSFI downstream edge validation。

本轮只做一个 candidate：
C01-Conservative Color-Structure Preserving Enhancement。

背景：
- 旧 Stage1 Final 已经完成负向诊断并锁定，不要重复证明旧 Stage1 失败。
- 旧 Stage1 Final 在 fixed DiffusionEdge/MSFI 下游边缘检测中会损伤结果。
- 新任务是新增一条保守、结构保持、可消融、可验证的 Stage1 candidate，使增强结果服务 fixed downstream edge detector。
- Stage1 只是 MSFI spatial-frequency weak-boundary diffusion edge detection 的输入支撑，不是主创新。
- 所有实验结论以本地落盘文件、manifest、CSV、日志、fixed downstream evaluation 为准。

参考方法来源：
- label-free microscopic cell image enhancement using bright/dark/weak-structure weighted fusion；
- feature-preserving smoothing for medical image segmentation；
- mild color compensation / gray-world white balance；
- conservative luminance gamma / CLAHE；
- guided / bilateral edge-preserving smoothing；
- false-edge guard。

本轮必须遵守：
1. 单候选：只实现 C01，不实现 pyramid fusion、wavelet、Retinex heavy、dehazing、deep UIE。
2. 单 gate：只在 168 GT split 上做 fixed DiffusionEdge + fixed MSFI downstream gate。
3. 单 run 目录：所有输出写到新的 run 目录。
4. 可回滚：只新增文件或新增配置，不覆盖旧文件。
5. 不自由重构：不要重构已有训练、评估、数据加载、旧 Stage1 代码。
6. 不无限调参：只跑下面指定的小网格。
7. 失败也记录：失败不是删除结果，而是写入 gate_report.md 和 research-log.md。

严禁改动或覆盖：
- 旧 Stage1 正式主线；
- 旧 Stage1 Final 输出；
- GT；
- detector 权重；
- MAT 文件；
- 正式 output_test 资产；
- 既有结果表；
- 2770 full-pool 任何结果；
- DiffusionEdge / MSFI 模型结构和权重；
- 训练脚本默认行为。

禁止进入：
- 2770 full-pool；
- detector retraining；
- large-scale UIE training；
- 502/496 complete-case，除非本轮 168 gate 已经达到 candidate pass 或 strong pass。当前任务默认不跑 502/496。

请先检查仓库结构，找到：
- raw 168 GT split 图像路径；
- 168 GT edge annotation 路径；
- fixed DiffusionEdge 推理/评估脚本；
- fixed MSFI 推理/评估脚本；
- legacy Stage1 Final 结果表；
- raw baseline 结果表；
- research-log.md 或等价实验日志。

如果找不到某个路径：
- 不要猜测并覆盖；
- 在 run 目录写 missing_paths_report.md；
- 在 research-log.md 记录阻塞项；
- 保持新增代码可运行单元测试。

建议新增文件路径：
- stage1_downstream_driven_v1/
  - __init__.py
  - enhancers/
    - __init__.py
    - conservative_csp.py
  - configs/
    - c01_conservative_csp.yaml
  - metrics/
    - enhancement_metrics.py
    - structure_proxy.py
  - scripts/
    - run_c01_conservative_csp.py
    - eval_c01_downstream_gate.py
  - README_c01.md

建议新 run 目录：
runs/downstream_driven_v1/c01_conservative_csp/YYYYMMDD_HHMMSS/

run 目录必须包含：
- manifest.json
- config_resolved.yaml
- enhanced_images/<config_id>/
- metrics/enhancement_metrics.csv
- metrics/structure_proxy_raw_vs_enhanced.csv
- metrics/downstream_diffusionedge.csv
- metrics/downstream_msfi.csv
- metrics/gate_summary.csv
- visual_panels/
- gate_report.md
- failure_notes.md，若失败
- command_log.txt
- git_status.txt
- environment.txt

C01 enhancement 具体实现：

输入：
- RGB image，uint8 或 16bit 均可读取；
- 内部统一转换为 float32 [0, 1]；
- 输出保持 RGB uint8；
- 文件名保持一致，写入新目录。

模块 0：degradation diagnosis
对每张图记录：
- RGB mean/std；
- channel imbalance = max(channel_mean) - min(channel_mean)；
- Lab-L mean/std；
- illumination nonuniformity = std(large_gaussian_blur(L))；
- raw Sobel gradient mean / percentile95；
- local variance mean / percentile95；
- saturation mean；
- image size；
写入 diagnosis.csv。

模块 1：mild capped gray-world / channel compensation
- 计算每个 RGB channel 的 mean；
- gray-world target = mean of channel means；
- gain = target / channel_mean；
- gain clip 到 [0.85, 1.15]；
- 如果 channel imbalance < 0.03，则跳过 WB；
- 输出 wb_rgb。

模块 2：luminance-only mild gamma / CLAHE
- 转 Lab；
- 只处理 L channel；
- gamma 参数来自 grid；
- CLAHE 只在 clahe_clip > 0 时启用；
- CLAHE tileGridSize 固定为 (8, 8)；
- 不在 RGB 三通道直接 CLAHE；
- 不做 heavy Retinex；
- 不做 dehazing。

模块 3：edge-preserving smoothing
- 对 enhanced L 使用 guided filter；如果仓库没有 guided filter，实现 fallback bilateral filter；
- guided radius 固定 5；
- guided eps 固定 1e-3，输入归一化 [0,1]；
- 得到 base_L；
- residual = enhanced_L - base_L。

模块 4：conservative structure residual injection
- 计算 raw/enhanced Sobel gradient；
- 计算 structure_confidence：归一化 Sobel gradient，限制在 [0,1]；
- 计算 texture_risk：local variance top quantile 或 high-frequency residual top quantile；
- residual_weight = structure_confidence * (1 - texture_risk)；
- output_L = enhanced_L + sharpen_alpha * residual_weight * residual；
- output_L clip 到 [0,1]；
- sharpen_alpha 来自 grid。

模块 5：false-edge guard
对每张图比较 raw 与 output：
- gradient_density = mean(Sobel_mag > percentile_raw_75)
- high_frequency_energy = mean(abs(L - gaussian_blur(L)))
- local_variance_p95
如果 output 的任一 proxy > raw * 1.10：
- fallback 1：sharpen_alpha = 0；
- 若仍超阈值，fallback 2：关闭 CLAHE；
- 若仍超阈值，fallback 3：只保留 mild WB + gamma；
记录 fallback_level 到 CSV。
不要用 GT 或 detector prediction 修改增强图。

参数搜索范围：
只允许以下 12 个配置：
- gamma: [0.95, 1.00, 1.05]
- clahe_clip: [0.0, 1.0]
- sharpen_alpha: [0.0, 0.15]

固定参数：
- wb_gain_clip: [0.85, 1.15]
- channel_imbalance_skip_threshold: 0.03
- guided_radius: 5
- guided_eps: 1e-3
- clahe_tile_grid: [8, 8]
- false_edge_guard_ratio: 1.10
- no dehazing
- no Retinex heavy
- no wavelet
- no pyramid fusion
- no deep model
- no detector retraining

增强指标输出：
对 raw 与 enhanced 均计算并写 CSV：
- mean/std per RGB channel；
- Lab-L mean/std；
- entropy；
- RMS contrast；
- gradient mean / p95；
- high-frequency energy；
- local variance mean / p95；
- optional NIQE/BRISQUE only if仓库已有实现，否则不要新引入复杂依赖；
- per-image fallback_level；
- config_id。

需要运行 fixed downstream detector：
- 使用仓库已有 fixed DiffusionEdge 推理/评估脚本；
- 使用仓库已有 fixed MSFI 推理/评估脚本；
- 不训练、不改权重、不改模型结构；
- 每个 config_id 单独输出 detector prediction 到新 run dir；
- 不覆盖任何已有 prediction。

downstream metrics 必须记录：
- DiffusionEdge AP / ODS / OIS / AC；
- MSFI AP / ODS / OIS / AC；
- 若仓库已有 F1 或 PR curve，也记录；
- raw baseline 与 legacy Stage1 Final baseline 从已有结果表读取并写入 gate_summary.csv；
- 若读取不到 baseline，记录 missing_baseline，不要伪造。

structure proxy 必须记录：
基于 detector prediction 与 168 GT edge：
- F1 proxy；
- false-edge ratio：预测边缘中落在 dilated GT edge band 外的比例；
- endpoints：对二值预测边缘 skeleton 计算 endpoint count，并按 edge length 归一化；
- background edge noise proxy：dilated GT band 外的 predicted edge density；
- weak-boundary fragmentation proxy：GT edge band 内预测覆盖率和连通片段数；
- 每个 detector 分开记录。

gate 判断：
最低通过：
- 相对 legacy Stage1 Final 有明确恢复；
- DiffusionEdge 和 MSFI 都不崩；
- false-edge ratio / endpoints / background edge noise 没有明显恶化。

候选通过：
- 至少一个 detector 达到 raw-near 或优于 raw；
- 另一个 detector AP / AC / structure proxy 不明显崩坏；
- false-edge ratio 与 endpoints 不超过 raw 的 1.10×；
- 不是单 detector 偶然涨点。

强通过：
- 两个 detector 都 raw-near 或优于 raw；
- false-edge ratio、endpoints、F1 proxy、background edge noise 均不劣于 raw；
- sampled visual panels 中没有明显背景伪边放大和弱边界断裂。

失败：
- 相对 legacy Stage1 Final 没恢复；
- 任一 detector 明显崩坏；
- 视觉指标提升但 downstream 变差；
- false-edge ratio 或 endpoints 明显增加；
- 背景颗粒、气泡、杂质被增强成伪边；
- 弱边界断裂；
- 只有单 detector 涨点，另一个 detector 明显恶化；
- 参数过拟合或结果不可解释。

gate_report.md 必须包含：
- best config_id；
- 每个 config_id 的 DiffusionEdge/MSFI 指标表；
- raw baseline、legacy Stage1 Final、C01 best 的对比；
- enhancement metrics 表；
- structure proxy 表；
- visual notes；
- gate result；
- failure reason 或 next action；
- evidence file paths。

research-log.md 同步：
在文末追加一个新条目，包含：
- 日期时间；
- candidate name；
- run dir；
- commit hash；
- config path；
- input split；
- 参数网格；
- 是否完成 DiffusionEdge/MSFI gate；
- gate result；
- 主要指标摘要；
- 失败或成功原因；
- 下一步建议。
不要修改历史日志内容。

成功时下一步：
- 若最低通过：记录为恢复型候选，下一轮只做一个针对性 ablation，不进入 full-pool。
- 若候选通过：锁定 C01 best config，下一轮可做 502/496 enhancement complete-case 对照或与 C02 比较。
- 若强通过：锁定为 downstream_driven_v1 Stage1 candidate，准备完整 evidence package；仍然不要自动进入 2770 full-pool。

最终交付：
- 新增代码；
- 新配置；
- run 目录；
- CSV metrics；
- gate_report.md；
- research-log.md 追加条目；
- 不覆盖任何旧资产。
```

---

## 第五部分：风险控制与 downstream gate 细化

### 5.1 先定义 baseline 与容忍区间

每个 candidate 都必须同时对比三组：

1. **Raw input**
2. **Legacy Stage1 Final**
3. **New candidate**

建议定义：

* `raw-near`：

  * AP / AC 与 raw 差距不超过 `0.01 absolute` 或 `2% relative`；
  * ODS / OIS / F1 proxy 与 raw 差距不超过 `0.005 absolute` 或 `1% relative`；
  * 若你已有历史方差，应以本地 bootstrap / paired image-level variance 为准。

* `明显崩坏`：

  * 任一 detector 的 AP 或 AC 相对 raw 下降超过 `0.02 absolute` 或 `5% relative`；
  * ODS / OIS 下降超过 `0.01 absolute`；
  * false-edge ratio、endpoints、background edge noise 任一超过 raw 的 `1.10×`；
  * sampled visual panel 出现明显背景伪边、气泡伪边、弱边界断裂。

* `legacy recovery`：
  如果 legacy Stage1 Final 明显低于 raw，则 candidate 至少应恢复 legacy-to-raw 损失的 `50%`，才算“有恢复价值”。
  例如某 detector AP：raw = 0.60，legacy = 0.50，则最低通过建议 candidate AP ≥ 0.55。
  若不同指标方向不一致，以 AP / AC / F1 proxy / false-edge ratio 的 Pareto 结果为主。

---

### 5.2 四级 gate

#### Gate 0：最低通过

判定条件：

* 相对 legacy Stage1 Final 有明确恢复；
* DiffusionEdge 不崩；
* MSFI 不崩；
* AP / AC 至少不继续表现出 legacy Stage1 Final 的负向损伤；
* false-edge ratio 不超过 raw 的 `1.10×`；
* endpoints 不超过 raw 的 `1.10×`；
* background edge noise 没有明显增加；
* visual panel 没有明显过锐化、气泡伪边、杂质伪边、弱边界断裂。

结论动作：

* 记录为 **recovery candidate**。
* 不进入 2770。
* 不急于 502/496 complete-case。
* 下一轮只做一个 targeted ablation，例如关 CLAHE、关 sharpening、关 WB。

---

#### Gate 1：候选通过

判定条件：

* 至少一个 detector 达到 raw-near 或优于 raw；
* 另一个 detector 没有 AP / AC / F1 proxy 明显崩坏；
* 两个 detector 的 false-edge ratio 均不超过 raw 的 `1.10×`；
* endpoints 不超过 raw 的 `1.10×`；
* background edge noise 不明显增加；
* weak boundary fragmentation 不劣于 legacy Stage1 Final，最好接近 raw；
* improvement 不能只来自单 detector 偶然涨点；
* 参数配置在 12 个预定义配置内，不是人为挑图调参。

结论动作：

* 记录为 **valid Stage1 candidate**。
* 可以进入 502/496 complete-case 做 enhancement metrics / external baseline 对照。
* 可以与 Candidate 2 或 Candidate 3 做下一轮单候选比较。
* 仍不进入 2770 full-pool。

---

#### Gate 2：强通过

判定条件：

* DiffusionEdge 和 MSFI 均 raw-near 或优于 raw；
* AP / ODS / OIS / AC 至少形成 Pareto 不劣；
* F1 proxy 不劣于 raw；
* false-edge ratio 不劣于 raw，或下降；
* endpoints 不劣于 raw，或下降；
* background edge noise 不劣于 raw；
* weak boundary fragmentation 不劣于 raw；
* visual panel 中没有明显：

  * 背景颗粒增强为伪边；
  * 气泡轮廓被过度增强；
  * 藻体弱边界断裂；
  * flagella / filament-like structure 被抹掉；
  * halo / ringing / over-sharpening；
* paired image-level 结果显示不是少数样本驱动。

结论动作：

* 锁定为 `downstream_driven_v1 Stage1 candidate`。
* 准备完整 evidence package。
* 可以做 502/496 complete-case。
* 是否进入 2770 full-pool仍应作为单独 decision gate，不在本轮自动进入。

---

#### Gate 3：失败

任一情况成立即可判失败或阶段性失败：

* 相对 legacy Stage1 Final 没有恢复；
* 任一 detector 明显崩坏；
* 只提升 entropy、contrast、UCIQE、UIQM 等视觉指标，但 downstream AP / AC / F1 proxy 变差；
* false-edge ratio 明显劣化；
* endpoints 明显增加；
* background edge noise 明显增加；
* 背景颗粒、气泡、杂质被增强成伪边；
* weak boundary fragmentation 增加；
* flagella / filament-like tiny structures 被抹掉；
* 只对单 detector 涨点，另一个 detector 明显恶化；
* 参数选择依赖少数样本，缺乏可解释性；
* Codex 修改了旧主线、旧结果、权重、GT 或正式资产。

失败动作：

* 不删除 run。
* 写 `failure_notes.md`。
* 在 `research-log.md` 记录失败原因。
* 将该 candidate 纳入投稿负证据：说明为什么普通视觉增强或某类结构增强不适合 fixed downstream edge detection。

---

### 5.3 建议结果记录表字段

| 字段                                | 说明                                                               |
| --------------------------------- | ---------------------------------------------------------------- |
| candidate_name                    | 例如 `C01-Conservative-CSP`                                        |
| run_dir                           | 新 run 目录完整路径                                                     |
| commit_hash                       | 当前代码版本                                                           |
| config_path                       | resolved config                                                  |
| input_split                       | `168_gt_split` / `502_complete_case` / `496_complete_case`       |
| image_count                       | 实际处理图像数                                                          |
| parameter_setting                 | gamma、CLAHE、sharpen_alpha、WB cap 等                               |
| fallback_count                    | false-edge guard 触发次数                                            |
| enhancement_metrics               | entropy、contrast、Lab-L std、gradient p95、HF energy、local variance |
| DiffusionEdge_AP                  | fixed DiffusionEdge AP                                           |
| DiffusionEdge_ODS                 | fixed DiffusionEdge ODS                                          |
| DiffusionEdge_OIS                 | fixed DiffusionEdge OIS                                          |
| DiffusionEdge_AC                  | fixed DiffusionEdge AC                                           |
| MSFI_AP                           | fixed MSFI AP                                                    |
| MSFI_ODS                          | fixed MSFI ODS                                                   |
| MSFI_OIS                          | fixed MSFI OIS                                                   |
| MSFI_AC                           | fixed MSFI AC                                                    |
| F1_proxy                          | 基于 GT edge band 的 proxy                                          |
| false_edge_ratio                  | GT dilated edge band 外的 edge ratio                               |
| endpoints                         | skeleton endpoint count / edge length                            |
| background_edge_noise_proxy       | background 区域 predicted edge density                             |
| weak_boundary_fragmentation_proxy | GT edge band 内 coverage / component fragmentation                |
| compared_with_raw                 | `better / raw-near / worse`                                      |
| compared_with_legacy_stage1       | recovery percentage                                              |
| visual_notes                      | 过锐化、气泡伪边、弱边界断裂等                                                  |
| gate_result                       | fail / minimum pass / candidate pass / strong pass               |
| evidence_files                    | CSV、manifest、visual panels、logs                                  |
| next_action                       | stop / ablate / switch / complete-case / lock                    |

---

## 第六部分：最终排序与明确建议

### 6.1 最推荐优先参考的 3–5 篇论文 / 项目

**第一组：直接支撑 Stage1 candidate 设计**

1. **Label-free microscopic cell images adaptive enhancement via weighted fusion of bright, dark, and weak structure features**
   最适合作为 Candidate 1 的核心来源，因为它处理的是显微图像 weak edge / blurry detail / background uniformity，而不是自然图像美化。([CoLab][7])

2. **Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network**
   最贴近 HAB downstream segmentation coupling，可作为 Candidate 2 和投稿中“Stage1 task-driven support”的近邻证据。([科学直接][2])

3. **Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion**
   适合提取 cyclic color compensation、multi-scale fusion、weight map 设计，但需要防止伪边增强。([Springer][4])

4. **Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion**
   适合支撑 wavelet/frequency candidate，与 MSFI spatial-frequency 叙事兼容。([Springer][5])

5. **Enhanced edge detection of HABs using diffusion probability models and Sobel-convolutional attention**
   不作为 Stage1，但作为 MyEdgeCodex / MSFI 主创新的近邻 related work 非常重要。([科学直接][1])

---

### 6.2 最推荐优先实现的 3 个 candidate pipeline

1. **C01-Conservative Color-Structure Preserving**
   第一优先。目标是先建立不破坏 fixed detector 的保守恢复 baseline。

2. **C02-HAB-Style Pyramid Fusion**
   第二优先。若 C01 稳定但提升不足，用 pyramid fusion 改善颜色、低对比和照明问题。

3. **C03-Wavelet / Frequency Structure**
   第三优先。若需要强化 MSFI spatial-frequency 叙事，进入 frequency-aware enhancement。

C04 是故障修复型，主要在 false-edge ratio / endpoints 出问题时启用。C05 是所有候选的选择机制，不是独立增强主线。

---

### 6.3 第一个应该交给 Codex 实现哪个 candidate？

**C01-Conservative Color-Structure Preserving。**

理由很直接：

* legacy Stage1 Final 已经证明“强增强可能损伤 downstream edge detection”；
* 第一轮目标不是追求视觉效果，而是恢复 downstream 可用性；
* C01 不需要训练、不需要外部权重、不需要配对数据；
* C01 可用 OpenCV / numpy / skimage 快速实现；
* C01 每个模块都能消融；
* C01 的失败也有解释价值：说明仅靠温和颜色 / 亮度 / 结构保持是否不足；
* C01 不会抢 MSFI 主创新叙事。

---

### 6.4 为什么它比直接复现深度学习 UIE SOTA 更适合当前阶段？

深度 UIE SOTA 的问题不是“效果不好”，而是当前阶段不匹配：

* 需要训练、预训练或复杂依赖；
* 输出分布可能对 fixed DiffusionEdge / MSFI 产生不可控 shift；
* 很难把提升或失败归因到颜色、频率、边界、背景抑制中的某个模块；
* 容易把论文主创新从 MSFI edge detection 转移到 Stage1 大模型增强；
* 视觉增强指标与 downstream segmentation/detection/edge detection 经常不一致，这一点已有 task-driven UIE 文献明确指出。([arXiv][15])

C01 的优势是：**低风险、可解释、可消融、可回滚、可快速失败、可形成证据链**。

---

### 6.5 哪些方法适合作为 external baseline？

适合作 external baseline，但不建议作为 Stage1 主线：

1. **CDEF / Adaptive Color Analysis and Multi-Space Fusion**
   有 MATLAB 项目，可作为 classical underwater fusion baseline。([GitHub][17])

2. **WWE-UIE**
   有代码，包含 white balance、wavelet、Sobel gradient-aware module，适合作轻量 deep UIE baseline，但不要作为主线。([arXiv][16])

3. **HUPE / DTI-UIE 类 task-aware UIE**
   适合作 related/external comparison，前提是有可用预训练或合理复现实验；不建议当前 Codex 从零训练。([arXiv][18])

4. **OpenCV-style WB + CLAHE + gamma + sharpen baseline**
   适合作弱 baseline，但必须用 downstream gate 评估，不应以视觉效果为准。OpenCV 的 underwater enhancement guide 列出了 white balance、red channel restoration、CLAHE、dehazing、sharpening、gamma 等常见模块。([OpenCV][19])

---

### 6.6 哪些方法只适合写 related work，不建议当前 Codex 实现？

* ESWA 2026 HAB diffusion edge detector：适合作 MyEdgeCodex / MSFI 相关工作，不是 Stage1。
* SFMnet：深度 edge detector + restoration 假设较重，当前不建议复现。
* Scientific Reports 2024 AEP：task-oriented preprocessing 叙事有价值，但需要训练。
* SDIE / RL-based enhancement：思想有价值，但 RL 过重。
* Transformer / GAN / CNN end-to-end UIE：当前优先级低，除非作为 external baseline 且有稳定代码和预训练模型。

---

### 6.7 最可能对 HAB weak-boundary edge detection 有效的传统模块

按当前可行性排序：

1. **mild capped gray-world / white balance**
2. **Lab-L mild gamma**
3. **very conservative CLAHE**
4. **guided filter / bilateral edge-preserving smoothing**
5. **structure residual with edge-confidence weighting**
6. **false-edge guard based on gradient / local variance**
7. **Laplacian pyramid fusion with texture penalty**
8. **DWT LL/LH/HL/HH 分离**
9. **HH soft-threshold noise suppression**
10. **morphological residual for bubbles / particles，但必须谨慎**

---

### 6.8 最应该避免的增强方向

当前阶段应避免：

* high clipLimit CLAHE；
* aggressive Retinex；
* aggressive dehazing / transmission map restoration；
* strong unsharp masking；
* red channel over-compensation；
* RGB 三通道独立强拉伸；
* 无 guard 的 Laplacian pyramid fusion；
* 直接最大化 entropy / contrast / UIQM / UCIQE；
* 根据单 detector 涨点选参数；
* per-image manual tuning；
* 使用 GT 参与 enhancement mask；
* 任何覆盖旧主线、旧结果或 full-pool 的操作。

---

### 6.9 如果第一个 candidate 失败，第二步切换到哪里？

按失败类型决定：

* **如果 false-edge ratio / endpoints / background edge noise 变差**：切换到 **C04 Edge-Aware False-Edge Suppression**。
* **如果两个 detector 都稳定但提升很小**：切换到 **C02 HAB-Style Pyramid Fusion**。
* **如果弱边界仍明显断裂、MSFI frequency branch 受益不足**：切换到 **C03 Wavelet / Frequency Structure**。
* **如果只有 DiffusionEdge 或只有 MSFI 涨点**：不扩展，先做 failure analysis，检查 detector-sensitive distribution shift。

---

### 6.10 如果第一个 candidate 达到不同 gate，分别怎么推进？

**最低通过**：

* 记录为 recovery candidate；
* 不进入 502/496；
* 不进入 2770；
* 下一轮只做一个 targeted ablation，例如：

  * 关 CLAHE；
  * 关 sharpening；
  * 只保留 WB + gamma；
  * 加入更严格 false-edge guard。

**候选通过**：

* 锁定 best config；
* 进入 502/496 complete-case 做 enhancement metrics 和 external baseline 对照；
* 同时保留 168 downstream gate 为主证据；
* 下一轮可以比较 C02，但不能同时大改 C01。

**强通过**：

* 锁定为 `downstream_driven_v1 Stage1 candidate`；
* 汇总 evidence package；
* 做 502/496 complete-case；
* 准备投稿叙事：Stage1 是 structure-preserving downstream support，主创新仍是 MSFI；
* 2770 full-pool 仍需单独 gate 和新 run 目录，不自动进入。

---

### 6.11 是否应该进入 502/496 complete-case？

**现在不应直接进入。**

只有当 C01 在 168 GT split 上达到 **候选通过** 或 **强通过** 后，才进入 502/496 complete-case。502/496 的作用是：

* enhancement metrics；
* complete-case external baseline；
* 图像质量和稳定性补充；
* 不能替代 downstream edge validation。

---

### 6.12 是否应该进入 2770 full-pool？

**当前阶段不应该。**

进入 2770 full-pool 的最低前提：

* 168 GT split 强通过；
* 502/496 complete-case 没有暴露明显伪边 / 颜色漂移 / 结构损伤；
* `downstream_driven_v1` config 已锁定；
* manifest、run dir、research-log、evidence package 完整；
* 新 run 目录，不覆盖任何旧 full-pool 资产。

---

### 6.13 最终执行建议

当前最稳妥路线是：

1. **先实现 C01-Conservative Color-Structure Preserving**；
2. 只在 **168 GT split** 上跑 fixed DiffusionEdge / MSFI gate；
3. 用 AP / ODS / OIS / AC + F1 proxy + false-edge ratio + endpoints + background edge noise 做判断；
4. 失败也保留为证据；
5. 通过后再考虑 C02 或 502/496；
6. 暂不进入 2770 full-pool。

投稿叙事应收束为：

> MSFI 是主创新，解决 HAB weak-boundary diffusion edge detection。
> Stage1 downstream_driven_v1 是支撑创新，提供 task-driven structure-preserving enhancement，使输入更适合 fixed downstream edge detector。
> Stage1 的价值不由视觉好看证明，而由 fixed DiffusionEdge / MSFI downstream gate、结构 proxy、失败候选记录和 Pareto evidence chain 证明。

[1]: https://www.sciencedirect.com/journal/expert-systems-with-applications/vol/298/part/PA?utm_source=chatgpt.com "Expert Systems with Applications | Vol 298, Part A, 1 March 2026 ..."
[2]: https://www.sciencedirect.com/science/article/pii/S0952197626012303?utm_source=chatgpt.com "Microscopic image segmentation of harmful algal blooms using pyramid ..."
[3]: https://www.x-mol.com/paper/1894987079363420160?utm_source=chatgpt.com "Innovative underwater image enhancement algorithm ..."
[4]: https://link.springer.com/article/10.1007/s11042-023-16258-0 "Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion | Multimedia Tools and Applications | Springer Nature Link"
[5]: https://link.springer.com/article/10.1007/s10489-023-04502-x?utm_source=chatgpt.com "Numerical computation of ocean HABs image enhancement based on ..."
[6]: https://www.sciencedirect.com/science/article/abs/pii/S0029801824018857?utm_source=chatgpt.com "SFMnet: Edge detection of HABs based on spatial feature ... - ScienceDirect"
[7]: https://colab.ws/articles/10.1016%2Fj.bspc.2024.105973?utm_source=chatgpt.com "Label-free microscopic cell images adaptive enhancement via weighted ..."
[8]: https://www.nature.com/articles/s41598-024-53411-7 "Automatic enhancement preprocessing for segmentation of low quality cell images | Scientific Reports"
[9]: https://link.springer.com/chapter/10.1007/978-3-030-59710-8_12 "Feature Preserving Smoothing Provides Simple and Effective Data Augmentation for Medical Image Segmentation | Springer Nature Link"
[10]: https://link.springer.com/article/10.1007/s13369-021-06421-w "Retinex-Centered Contrast Enhancement Method for Histopathology Images with Weighted CLAHE | Arabian Journal for Science and Engineering | Springer Nature Link"
[11]: https://link.springer.com/article/10.1007/s10043-024-00941-0?utm_source=chatgpt.com "Underwater image enhancement via adaptive white-balancing ... - Springer"
[12]: https://arxiv.org/abs/2503.03640?utm_source=chatgpt.com "An Adaptive Underwater Image Enhancement Framework via Multi-Domain Fusion and Color Compensation"
[13]: https://arxiv.org/abs/2310.10387 "[2310.10387] Enhanced Edge-Perceptual Guided Image Filtering"
[14]: https://github.com/wliusjtu/Generalized-Smoothing-Framework "GitHub - wliusjtu/Generalized-Smoothing-Framework: This is the released code for the following papers: A generalized framework for edge-preserving and structure-preserving image smoothing. Liu W, et al., TPAMI 2021, AAAI 2020 · GitHub"
[15]: https://arxiv.org/html/2603.01767v1 "Downstream Task Inspired Underwater Image Enhancement: A Perception-Aware Study from Dataset Construction to Network Design"
[16]: https://arxiv.org/abs/2511.16321 "[2511.16321] WWE-UIE: A Wavelet & White Balance Efficient Network for Underwater Image Enhancement"
[17]: https://github.com/bilityniu/CDEF?utm_source=chatgpt.com "GitHub - bilityniu/CDEF: [JOE 2025] Underwater Scene Enhancement via ..."
[18]: https://arxiv.org/abs/2411.18296?utm_source=chatgpt.com "HUPE: Heuristic Underwater Perceptual Enhancement with Semantic Collaborative Learning"
[19]: https://opencv.org/underwater-image-enhancement-using-opencv/ "Guide to Underwater Image Enhancement Using OpenCV - OpenCV"
