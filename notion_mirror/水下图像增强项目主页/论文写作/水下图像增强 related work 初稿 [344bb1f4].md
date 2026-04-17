# 水下图像增强 related work 初稿

- **Notion URL**: https://www.notion.so/344bb1f4e23e813daf65ea3e3477674d
- **Ancestor Path**: 水下图像增强项目主页 / 论文写作
- **Exported On**: 2026-04-17

## Properties
- **内容摘要**: 已完成一版文献对比表、完整版中文相关工作、短版中文和英文骨架，当前主文件保存在本地仓库根目录 related-work-underwater-enhancement.md。
- **条目**: 水下图像增强 related work 初稿
- **状态**: 草稿中
- **类型**: related work

## Content
# Underwater Image Enhancement Related Work Draft

Last updated: 2026-04-17

This note consolidates the current Zotero reading set for the HAB underwater microscopic image enhancement project. It is organized for two direct uses:

1. quick comparison when selecting baselines;
2. direct reuse in the related work section of the paper.

## Scope

- Target problem: underwater image enhancement with emphasis on HAB microscopic imagery
- Source groups in Zotero:
  - `同方向师兄`
  - `对比方法`
- Current writing angle from local project notes:
  - task-specific white balance and color correction
  - complementary detail and contrast branches
  - feature-aware multi-scale fusion
  - downstream edge-oriented validation

## Comparison Table

| Key | Paper | Venue | Bucket | Core idea | Main value for our paper | Main limitation / caution |
| --- | --- | --- | --- | --- | --- | --- |
| `AFLVZ4KR` | *Color Balance and Fusion for Underwater Image Enhancement* | IEEE TIP 2018 | Traditional baseline | Color compensation, white balance, derived-image weighting, multi-scale fusion | Classic underwater enhancement baseline; useful for showing early fusion logic | Strong visual enhancement but limited semantic or task-specific modeling |
| `V87JDUST` | *Generalization of the Dark Channel Prior for Single Image Restoration* | IEEE TIP 2018 | Physical-prior baseline | Generalized dark channel prior, ambient light estimation, transmission recovery, adaptive color correction | Represents physically motivated restoration line | Prior-based restoration may struggle under diverse microscopic degradations |
| `PWKRPBPJ` | *Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors* | IEEE TIP 2022 | Optimization baseline | Retinex variational model with hyper-Laplacian reflectance priors | Strong reference for optimization-based enhancement and reflectance modeling | Optimization pipeline is elegant but less naturally aligned with downstream edge tasks |
| `U6DBLZMV` | *Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion* | IEEE TCSVT 2024 | Traditional baseline | Attenuation-guided correction, contrast enhancement, weighted wavelet fusion | Modern traditional fusion baseline closer to current comparison standards | Still mainly a hand-crafted pipeline; limited high-level feature reasoning |
| `DQIVG34J` | *Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion* | Applied Intelligence 2023 | Senior work / lineage | Homomorphic filtering, empirical mode feature extraction, dual-image wavelet fusion | Establishes the decomposition-and-fusion lineage in HAB microscopy | Should be cited as lineage, not as an identical implementation of the current repo |
| `GS2RFTEL` | *Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion* | Multimedia Tools and Applications 2023 | Senior work / lineage | Cyclic color compensation plus three-image multi-scale fusion | Important historical baseline for HAB microscopic enhancement with downstream validation | Current repo is already more complex than the published pipeline description |
| `LTE9U599` | *Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy* | Image and Vision Computing 2025 | Senior work / closest reference | Adaptive white balance color compensation, attention guidance, image pyramid fusion, edge-oriented evaluation | Closest structural reference for connecting enhancement quality to edge-sensitive downstream tasks | Still should not be described as a literal template for the present method |
| `P4E22T2E` | *SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception* | IEEE TIP 2022 | Deep-learning baseline | Semantic attention with region-wise enhancement and multi-scale perception | Represents semantic-guided deep enhancement | Requires paired-data assumptions and stronger data dependence than traditional methods |
| `V5H7FQTY` | *Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement* | IEEE Journal of Oceanic Engineering 2025 | Transformer baseline | Histogram-based transformer with GAN refinement | Strong modern baseline for global distribution modeling in underwater enhancement | More generic underwater enhancement, less tied to microscopy-specific structure |
| `LF9HP7DR` | *ABC-Former: Auxiliary Bimodal Cross-domain Transformer with Interactive Channel Attention for White Balance* | CVPR 2025 | Transferable reference | Histogram plus image bimodal transformer for white balance | Useful for arguing that global color statistics and channel interaction matter | White-balance paper, not a canonical underwater enhancement method |
| `TEKJDF6M` | *HVDualformer: Histogram-Vision Dual Transformer for White Balance* | AAAI 2025 | Transferable reference | Histogram-vision dual transformer for white balance correction | Supports the value of histogram-aware color modeling | Also belongs to white-balance correction rather than standard underwater enhancement |

## Recommended Related Work Structure

### 1. Traditional Underwater Image Enhancement

Recommended references:

- `AFLVZ4KR`
- `V87JDUST`
- `PWKRPBPJ`
- `U6DBLZMV`

Writing goal:

- establish the early problem setting of color distortion, low contrast, scattering, and absorption;
- show the three dominant traditional lines: fusion, physical priors, and optimization / Retinex;
- prepare the motivation for stronger task-aware or feature-aware enhancement.

### 2. HAB Microscopic Image Enhancement Lineage

Recommended references:

- `DQIVG34J`
- `GS2RFTEL`
- `LTE9U599`

Writing goal:

- present a coherent local research line specific to HAB microscopic images;
- justify why the present project is rooted in algae-oriented enhancement rather than generic underwater photography;
- show the progression from decomposition and fusion to color compensation, and then to white-balance-guided fusion with downstream edge validation.

### 3. Deep Learning Based Enhancement

Recommended references:

- `P4E22T2E`
- `V5H7FQTY`

Writing goal:

- explain how semantic cues, learned global distributions, and transformers extend beyond hand-crafted pipelines;
- position modern baselines as stronger in representation learning but more dependent on data and training distribution.

### 4. White Balance and Histogram Modeling as Transferable Ideas

Recommended references:

- `LF9HP7DR`
- `TEKJDF6M`

Writing goal:

- explicitly state that these are not standard underwater enhancement baselines;
- use them to support the argument that histogram-aware and color-aware transformer modeling is relevant to severe color cast correction;
- provide conceptual support for color correction design choices without overstating task overlap.

## Related Work Draft in Chinese

### 相关工作

水下图像增强的核心目标是缓解由光吸收、散射和波长依赖衰减带来的颜色失真、低对比度和细节模糊问题。早期研究主要依赖颜色补偿、多尺度融合和成像先验建模来恢复视觉质量。Ancuti 等在 *Color Balance and Fusion for Underwater Image Enhancement* 中通过颜色补偿、白平衡与多尺度融合构建了经典的单幅图像增强框架，为后续融合类方法提供了代表性范式。Peng 等在 *Generalization of the Dark Channel Prior for Single Image Restoration* 中从成像模型出发，对暗通道先验进行了更一般化的推广，通过环境光估计、透射率恢复和自适应颜色校正实现退化图像恢复。进一步地，Zhuang 等在 *Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors* 中将 Retinex 变分建模与高阶反射先验结合，增强了结构与细节恢复能力。此类传统方法通常具有较强可解释性，但对复杂场景下高层语义一致性和任务相关特征的建模能力仍然有限。

围绕有害藻华显微图像这一更具体的应用场景，已有工作逐步形成了较清晰的技术演进脉络。Wu 等在 *Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion* 中使用经验模态分解与小波融合来提升藻类显微图像的纹理清晰度和整体对比度，代表了分解驱动的早期思路。随后，Wu 等在 *Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion* 中进一步引入循环颜色补偿和多尺度融合机制，将增强效果与边缘检测、关键点匹配等下游表现联系起来。Fan 等在 *Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy* 中又将自适应白平衡颜色补偿、注意力引导和图像金字塔融合作为统一框架，并通过边缘检测相关实验验证增强结果对后续视觉任务的促进作用。上述研究说明，针对 HAB 显微图像的增强不应仅停留在主观视觉改善层面，而应与细胞边缘、纹理和形态信息的可分辨性紧密结合。

随着深度学习的发展，水下图像增强方法开始更加关注高层语义信息和全局分布建模。Qi 等提出的 *SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception* 利用语义引导和多尺度感知模块，在有限训练样本条件下提升局部区域增强的一致性与鲁棒性。Peng 等提出的 *Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement* 则从直方图分布学习的角度出发，使用 Transformer 建模高对比度与颜色校正图像的全局统计特征，并结合生成式细化模块进一步优化结果。这类方法相较传统管线在复杂颜色偏移和结构恢复方面具有更强表达能力，但其效果通常更加依赖训练数据覆盖范围和分布匹配程度。

除直接面向水下增强的研究外，白平衡校正与直方图建模方向同样为颜色失真校正提供了重要启发。Chiu 等在 CVPR 2025 提出的 *ABC-Former* 通过联合直方图与图像输入进行跨域建模，并利用通道交互注意力提升白平衡校正精度。Peng 和 Chen 在 AAAI 2025 提出的 *HVDualformer* 则进一步通过 histogram-vision dual transformer 统一颜色分布特征与视觉特征。虽然这两类方法并非标准的水下图像增强模型，但它们表明，全局颜色统计、直方图表示以及通道交互建模对严重颜色偏移场景具有重要价值，这对于水下显微图像中的颜色补偿与白平衡设计具有直接借鉴意义。

综合来看，现有研究大致可以归纳为三条主线：一是基于颜色补偿、融合和成像先验的传统增强方法；二是面向具体水下显微任务、强调下游边缘或结构可见性的任务驱动方法；三是依托语义建模、Transformer 和直方图分布学习的深度增强方法。与这些工作相比，当前项目更关注将任务相关的白平衡与颜色校正、互补的细节与对比分支、多尺度融合机制以及面向边缘敏感任务的验证方式整合到同一框架中，从而在保持结构真实性的前提下提升藻类显微图像的可判读性。

## Practical Notes for Paper Drafting

- Use the first paragraph to summarize the traditional landscape.
- Use the second paragraph to highlight the HAB-specific lineage; this is the section that makes the project feel grounded and local rather than generic.
- Use the third paragraph to introduce modern deep models without letting them dominate the story.
- Use the fourth paragraph to justify borrowing ideas from white-balance and histogram modeling.
- Use the final paragraph as the bridge into the method section.

## Suggested Next Step

Turn this note into:

1. a shorter conference-paper related work section of about 500 to 800 Chinese characters; or
2. a bilingual version with Chinese drafting text and English claim sentences for direct LaTeX insertion.

## Short Chinese Version for Paper

水下图像增强旨在缓解由光吸收、散射和波长依赖衰减引起的颜色失真、低对比度和细节模糊。早期方法主要依赖颜色补偿、多尺度融合和成像先验建模。典型代表包括基于颜色平衡与多尺度融合的单幅增强方法，以及基于暗通道先验和 Retinex 变分建模的恢复方法。这类方法具有较强可解释性，但在复杂退化场景下对高层语义信息和任务相关特征的建模能力有限。

针对有害藻华显微图像，相关研究逐渐形成了从分解融合到颜色补偿再到白平衡引导增强的演进路线。已有工作通过经验模态分解与小波融合提升藻类纹理细节，通过循环颜色补偿和多尺度融合改善整体对比度，并进一步结合自适应白平衡、注意力引导和金字塔融合，将增强效果与边缘检测、关键点匹配等下游任务联系起来。这说明 HAB 显微图像增强不仅需要改善视觉质量，更需要服务于细胞边缘和形态结构的清晰表达。

近年来，深度学习方法开始引入语义引导、全局分布学习和 Transformer 建模。语义注意力网络能够通过多尺度感知提升区域增强的一致性，基于直方图的 Transformer 则可从全局统计分布角度建模颜色校正过程。此外，白平衡校正领域的直方图与通道交互建模方法也为严重颜色偏移场景提供了有价值的启发。与现有研究相比，本文更关注将任务相关的白平衡与颜色校正、互补的细节与对比分支、多尺度融合机制以及面向边缘敏感任务的验证方式整合到统一框架中。

## English Draft for LaTeX Adaptation

### Related Work (English Draft)

Underwater image enhancement aims to alleviate color distortion, low contrast, and detail degradation caused by wavelength-dependent absorption and scattering. Early methods mainly relied on color compensation, multi-scale fusion, and image formation priors. Representative examples include fusion-based enhancement pipelines, generalized dark channel prior models, and Retinex-based optimization frameworks. These methods are generally interpretable, but they are limited in modeling high-level semantics and task-relevant structures under complex degradations.

For HAB microscopic imagery, prior studies have formed a more task-specific development line. Earlier work explored empirical mode decomposition and wavelet fusion to recover fine algae structures. Subsequent work introduced cyclic color compensation and multi-scale fusion, and further connected enhancement quality to downstream tasks such as edge detection and keypoint matching. More recent work combined adaptive white-balance color compensation, attention-guided processing, and pyramid fusion, showing that enhancement for HAB microscopy should be evaluated not only by visual quality but also by its utility for biological structure perception.

Recent deep models have extended underwater enhancement with semantic guidance, global distribution learning, and transformer-based design. Semantic attention networks improve region-wise consistency through multi-scale perception, while histogram-based transformers model global color statistics for enhanced correction quality. In addition, recent white-balance correction models suggest that histogram-aware and channel-interactive representations are valuable for severe color-cast removal, even though they are not designed specifically for underwater microscopy.

Compared with previous work, our project is more concerned with integrating task-aware white balance and color correction, complementary detail and contrast branches, multi-scale fusion, and edge-oriented validation into a unified enhancement framework. This positioning connects traditional enhancement logic, HAB-specific application needs, and modern representation learning in a single project narrative.
