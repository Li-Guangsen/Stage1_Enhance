# Underwater Image Enhancement Related Work Draft

Last updated: 2026-04-23

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

## Current Evidence Levels

- Full paper-ready package:
  - `paper/comparison_methods_related_work_pack_cn.md`
- Current formal experimental comparison set:
  - deep white-balance methods: `HVDualformer`, `ABC-Former`
  - traditional / non-deep underwater enhancement methods: `GDCP`, `CBF`, `HLRP`, `WWPF`
  - deep underwater enhancement methods: `SGUIE-Net`, `Histoformer`
- Current review-only expansion set:
  - traditional white balance: `MaxRGB`, `Gray-World`, `Shades of Gray`, `Gray-Edge`
  - traditional underwater enhancement: `UDCP`, `IBLA`, `VRE`
  - deep underwater enhancement: `WaterNet`, `UWCNN`
- Writing rule:
  - `HVDualformer` and `ABC-Former` can stay in the experiment section because they have been run in the current protocol, but in related work they must still be described as white-balance methods rather than standard underwater enhancement models.

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

## Expanded Review-Only Methods

### Traditional White Balance Heuristics

- `MaxRGB`: assumes a white surface produces maximal channel responses and corrects channels by maxima.
- `Gray-World`: assumes the average reflectance of a natural scene is achromatic and corrects channels by global means.
- `Shades of Gray`: extends `Gray-World` with a Minkowski-norm formulation.
- `Gray-Edge`: estimates illumination from derivative statistics rather than raw pixel values.

### Additional Underwater Enhancement References

- `WaterNet`: introduced in *An Underwater Image Enhancement Benchmark Dataset and Beyond*; represents end-to-end deep fusion on benchmark-driven training.
- `UWCNN`: introduced in *Underwater Scene Prior Inspired Deep Underwater Image and Video Enhancement*; represents lightweight CNN enhancement guided by underwater scene priors.
- `UDCP`: introduced in *Transmission Estimation in Underwater Single Images*; represents the underwater dark-channel and transmission-estimation line.
- `IBLA`: represents the image-blurriness-and-light-absorption restoration line in underwater image enhancement.
- `VRE`: keep as a placeholder label only until the exact canonical paper is re-verified.

## Experiment-Ready Comparison Methods Paragraph

The current external comparison set contains eight methods organized into three groups. The first group is deep white-balance methods, including `HVDualformer` and `ABC-Former`. Although they are not standard underwater enhancement models, they are kept as deep white-balance baselines because they directly target severe color-cast correction and have been run under the current protocol. The second group is traditional or non-deep underwater enhancement methods, including `GDCP`, `CBF`, `HLRP`, and `WWPF`, which cover physical-prior restoration, classical fusion, optimization-based enhancement, and modern traditional fusion. The third group is deep underwater enhancement methods, including `SGUIE-Net` and `Histoformer`, representing semantic-guided enhancement and histogram-transformer enhancement, respectively. Among these methods, seven generate results for all 502 cleaned input images, while the official `WWPF` package only produces 496 valid outputs. Therefore, any final fair quantitative comparison should be computed on the 496-image complete-case subset rather than on method-specific sample counts.

## Related Work Draft in Chinese

### 相关工作

水下图像增强旨在缓解由光吸收、散射和波长依赖衰减引起的颜色失真、低对比度和细节退化。早期研究主要围绕颜色补偿、多尺度融合和成像先验展开。除经典的颜色平衡与多尺度融合路线外，*Transmission Estimation in Underwater Single Images* 提出的水下暗通道先验、以及基于 image blurriness and light absorption 的恢复模型，分别代表了 transmission 估计和 IFM 型恢复思路。随后，*Generalization of the Dark Channel Prior for Single Image Restoration* 进一步推广了暗通道先验，*Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors* 将 Retinex 变分建模与高阶反射率先验结合，*Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion* 则展示了颜色校正、全局/局部对比增强与小波融合的现代传统扩展。总体来看，这类方法具有较强可解释性，但往往难以同时兼顾颜色稳定、局部可见性和任务相关结构表达。

围绕有害藻华显微图像这一具体场景，已有工作逐渐形成了从分解融合到颜色补偿再到白平衡引导融合的技术谱系。早期工作利用经验模态分解与小波融合提升藻类显微图像的纹理清晰度，随后又将循环颜色补偿与多尺度融合结合，并把增强结果与边缘检测、关键点匹配等下游任务联系起来。更近的工作进一步将自适应白平衡颜色补偿、注意力引导和金字塔融合整合到统一框架中，说明 HAB 显微增强不仅应关注主观视觉质量，还应服务于细胞边缘、纹理和形态结构的可辨识性。

随着深度学习的发展，水下增强开始更加重视高层语义和全局分布建模。`WaterNet` 通过多路预处理结果的端到端融合建立了基准数据集驱动的增强范式，`UWCNN` 则体现了结合水下场景先验和轻量 CNN 的早期深度增强路线。进一步地，*SGUIE-Net* 通过语义注意力和多尺度感知提升区域增强一致性，*Histoformer* 使用直方图 Transformer 与生成式细化模块建模颜色和对比度的全局统计特征。这些方法在复杂退化场景下具有更强表达能力，但通常更依赖训练数据分布。

除直接面向水下增强的研究外，白平衡校正与颜色统计建模同样为严重偏色场景提供了重要启发。传统白平衡方法如 `MaxRGB`、`Gray-World`、`Shades of Gray` 和 `Gray-Edge` 代表了颜色恒常假设的经典谱系。近年来，`ABC-Former` 和 `HVDualformer` 等深度白平衡模型进一步表明，直方图表示、全局颜色统计和通道交互建模对于颜色偏移校正十分关键。虽然这些方法并非标准的水下增强模型，但它们为水下显微图像中的颜色补偿与白平衡设计提供了直接的可迁移思路。与现有工作相比，当前项目更关注将稳态前置白平衡、互补三分支增强、亮度域特征门控融合以及面向结构可读性的设计动机整合到同一条可复现实验主线中。

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
