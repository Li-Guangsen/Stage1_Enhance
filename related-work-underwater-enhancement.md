# 水下图像增强相关工作草稿

最后更新：2026-04-23

本文档整理当前 Zotero 阅读集中与 HAB 水下显微图像增强项目直接相关的文献，用于两个目的：

1. 为 baseline 选择提供快速对照；
2. 为论文相关工作小节提供可直接改写的素材。

## 覆盖范围

- 目标问题：以 HAB 水下显微图像为重点的水下图像增强
- Zotero 来源分组：
  - `同方向师兄`
  - `对比方法`
- 当前本地写作角度：
  - 面向任务的白平衡与颜色校正
  - 互补的细节分支与对比分支
  - 特征感知的多尺度融合
  - 面向下游边缘任务的验证

## 当前证据层级

- 已整理的论文可用材料：
  - `paper/comparison_methods_related_work_pack_cn.md`
- 当前正式实验对比集合：
  - 深度白平衡方法：`HVDualformer`、`ABC-Former`
  - 传统或非深度水下增强方法：`GDCP`、`CBF`、`HLRP`、`WWPF`
  - 深度水下增强方法：`SGUIE-Net`、`Histoformer`
- 当前仅用于综述扩展的方法：
  - 传统白平衡：`MaxRGB`、`Gray-World`、`Shades of Gray`、`Gray-Edge`
  - 传统水下增强：`UDCP`、`IBLA`、`VRE`
  - 深度水下增强：`WaterNet`、`UWCNN`
- 写作规则：
  - `HVDualformer` 和 `ABC-Former` 可以保留在实验对比中，因为它们已经按当前协议跑通；但在相关工作中必须描述为白平衡方法，而不是标准水下增强模型。

## 文献对照表

| Key | 论文 | 来源 | 类别 | 核心思路 | 对本文的主要价值 | 局限或写作注意点 |
| --- | --- | --- | --- | --- | --- | --- |
| `AFLVZ4KR` | *Color Balance and Fusion for Underwater Image Enhancement* | IEEE TIP 2018 | 传统 baseline | 颜色补偿、白平衡、派生图像加权与多尺度融合 | 经典水下增强 baseline，可用于说明早期融合逻辑 | 视觉增强效果强，但语义建模和任务特异性有限 |
| `V87JDUST` | *Generalization of the Dark Channel Prior for Single Image Restoration* | IEEE TIP 2018 | 物理先验 baseline | 广义暗通道先验、环境光估计、透射率恢复与自适应颜色校正 | 代表物理建模驱动的恢复路线 | 先验方法面对多样显微退化时可能不稳定 |
| `PWKRPBPJ` | *Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors* | IEEE TIP 2022 | 优化模型 baseline | 结合高阶反射率先验的 Retinex 变分模型 | 可支撑优化型增强与反射率建模的综述 | 流程优雅，但与下游边缘任务的自然连接较弱 |
| `U6DBLZMV` | *Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion* | IEEE TCSVT 2024 | 传统 baseline | 衰减引导校正、对比度增强与加权小波融合 | 现代传统融合 baseline，更接近当前对比标准 | 仍以手工流程为主，高层特征推理有限 |
| `DQIVG34J` | *Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion* | Applied Intelligence 2023 | 师兄工作 / 技术谱系 | 同态滤波、经验模态特征提取与双图小波融合 | 建立 HAB 显微图像中“分解-融合”路线的来源 | 应作为谱系引用，不应写成当前仓库的同一实现 |
| `GS2RFTEL` | *Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion* | Multimedia Tools and Applications 2023 | 师兄工作 / 技术谱系 | 循环颜色补偿与三图多尺度融合 | 是 HAB 显微增强和下游验证的重要历史 baseline | 当前仓库流程已经比已发表描述更复杂 |
| `LTE9U599` | *Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy* | Image and Vision Computing 2025 | 师兄工作 / 最近参考 | 自适应白平衡颜色补偿、注意力引导、图像金字塔融合和边缘导向评估 | 最接近“增强质量服务于边缘敏感下游任务”的结构参考 | 仍不能描述为本文方法的直接模板 |
| `P4E22T2E` | *SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception* | IEEE TIP 2022 | 深度学习 baseline | 语义注意力、区域增强与多尺度感知 | 代表语义引导的深度水下增强路线 | 依赖配对数据和训练分布，数据需求强于传统方法 |
| `V5H7FQTY` | *Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement* | IEEE Journal of Oceanic Engineering 2025 | Transformer baseline | 基于直方图的 Transformer 与 GAN 细化 | 是全局分布建模方向的强现代 baseline | 更偏通用水下增强，与显微结构的绑定较弱 |
| `LF9HP7DR` | *ABC-Former: Auxiliary Bimodal Cross-domain Transformer with Interactive Channel Attention for White Balance* | CVPR 2025 | 可迁移参考 | 直方图与图像双模态 Transformer，用于白平衡 | 支撑“全局颜色统计和通道交互很重要”的论证 | 属于白平衡论文，不是标准水下增强方法 |
| `TEKJDF6M` | *HVDualformer: Histogram-Vision Dual Transformer for White Balance* | AAAI 2025 | 可迁移参考 | 面向白平衡校正的直方图-视觉双 Transformer | 支撑直方图感知颜色建模的价值 | 同样应归入白平衡校正，而不是水下增强 |

## 推荐相关工作结构

### 1. 传统水下图像增强

推荐引用：

- `AFLVZ4KR`
- `V87JDUST`
- `PWKRPBPJ`
- `U6DBLZMV`

写作目标：

- 建立颜色失真、低对比度、散射和吸收等早期问题设定；
- 说明传统方法中三条主要路线：融合、物理先验、优化 / Retinex；
- 为后续引出更强的任务感知或特征感知增强动机铺垫。

### 2. HAB 显微图像增强技术谱系

推荐引用：

- `DQIVG34J`
- `GS2RFTEL`
- `LTE9U599`

写作目标：

- 呈现一条面向 HAB 显微图像的本地研究线索；
- 说明当前项目扎根于藻类显微增强，而不是泛化的水下摄影增强；
- 展示从分解融合、颜色补偿，到白平衡引导融合和下游边缘验证的演进。

### 3. 基于深度学习的水下增强

推荐引用：

- `P4E22T2E`
- `V5H7FQTY`

写作目标：

- 说明语义线索、学习到的全局分布和 Transformer 如何突破手工流程；
- 将现代 baseline 定位为表达能力更强、但更依赖数据与训练分布的方法。

### 4. 可迁移的白平衡与直方图建模思想

推荐引用：

- `LF9HP7DR`
- `TEKJDF6M`

写作目标：

- 明确说明这些方法不是标准水下增强 baseline；
- 借它们支撑“直方图感知和颜色感知 Transformer 建模与严重偏色校正相关”的论点；
- 为颜色校正设计提供概念支持，但不夸大任务重合度。

## 仅用于综述扩展的方法

### 传统白平衡启发式方法

- `MaxRGB`：假设白色表面产生最大通道响应，并按通道最大值进行校正。
- `Gray-World`：假设自然场景平均反射率为无彩色，并按全局均值校正通道。
- `Shades of Gray`：用 Minkowski 范数形式扩展 `Gray-World`。
- `Gray-Edge`：从导数统计而不是原始像素值中估计光照。

### 其他水下增强参考

- `WaterNet`：来自 *An Underwater Image Enhancement Benchmark Dataset and Beyond*，代表基准数据集驱动的端到端深度融合路线。
- `UWCNN`：来自 *Underwater Scene Prior Inspired Deep Underwater Image and Video Enhancement*，代表水下场景先验引导的轻量 CNN 增强路线。
- `UDCP`：来自 *Transmission Estimation in Underwater Single Images*，代表水下暗通道和透射率估计路线。
- `IBLA`：代表基于图像模糊度与光吸收的水下图像恢复路线。
- `VRE`：在重新核验标准题录前，只保留为占位标签。

## 可用于实验部分的对比方法段落

当前外部对比集合共包含八种方法，可分为三组。第一组为深度白平衡方法，包括 `HVDualformer` 和 `ABC-Former`。虽然它们不是标准水下增强模型，但由于它们直接面向严重偏色校正，且已经按当前协议完成运行，因此保留为深度白平衡 baseline。第二组为传统或非深度水下增强方法，包括 `GDCP`、`CBF`、`HLRP` 和 `WWPF`，分别覆盖物理先验恢复、经典融合、优化型增强和现代传统融合。第三组为深度水下增强方法，包括 `SGUIE-Net` 和 `Histoformer`，分别代表语义引导增强和直方图 Transformer 增强。八种方法中，有七种方法能够为全部 502 张清洁输入图像生成结果，而官方 `WWPF` 包仅生成 496 张有效输出。因此，最终公平定量比较应基于 496 张 complete-case 子集计算，而不是基于各方法自己的样本数分别比较。

## 相关工作中文草稿

### 相关工作

水下图像增强旨在缓解由光吸收、散射和波长依赖衰减引起的颜色失真、低对比度和细节退化。早期研究主要围绕颜色补偿、多尺度融合和成像先验展开。除经典的颜色平衡与多尺度融合路线外，*Transmission Estimation in Underwater Single Images* 提出的水下暗通道先验、以及基于 image blurriness and light absorption 的恢复模型，分别代表了 transmission 估计和 IFM 型恢复思路。随后，*Generalization of the Dark Channel Prior for Single Image Restoration* 进一步推广了暗通道先验，*Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors* 将 Retinex 变分建模与高阶反射率先验结合，*Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion* 则展示了颜色校正、全局/局部对比增强与小波融合的现代传统扩展。总体来看，这类方法具有较强可解释性，但往往难以同时兼顾颜色稳定、局部可见性和任务相关结构表达。

围绕有害藻华显微图像这一具体场景，已有工作逐渐形成了从分解融合到颜色补偿再到白平衡引导融合的技术谱系。早期工作利用经验模态分解与小波融合提升藻类显微图像的纹理清晰度，随后又将循环颜色补偿与多尺度融合结合，并把增强结果与边缘检测、关键点匹配等下游任务联系起来。更近的工作进一步将自适应白平衡颜色补偿、注意力引导和金字塔融合整合到统一框架中，说明 HAB 显微增强不仅应关注主观视觉质量，还应服务于细胞边缘、纹理和形态结构的可辨识性。

随着深度学习的发展，水下增强开始更加重视高层语义和全局分布建模。`WaterNet` 通过多路预处理结果的端到端融合建立了基准数据集驱动的增强范式，`UWCNN` 则体现了结合水下场景先验和轻量 CNN 的早期深度增强路线。进一步地，*SGUIE-Net* 通过语义注意力和多尺度感知提升区域增强一致性，*Histoformer* 使用直方图 Transformer 与生成式细化模块建模颜色和对比度的全局统计特征。这些方法在复杂退化场景下具有更强表达能力，但通常更依赖训练数据分布。

除直接面向水下增强的研究外，白平衡校正与颜色统计建模同样为严重偏色场景提供了重要启发。传统白平衡方法如 `MaxRGB`、`Gray-World`、`Shades of Gray` 和 `Gray-Edge` 代表了颜色恒常假设的经典谱系。近年来，`ABC-Former` 和 `HVDualformer` 等深度白平衡模型进一步表明，直方图表示、全局颜色统计和通道交互建模对于颜色偏移校正十分关键。虽然这些方法并非标准的水下增强模型，但它们为水下显微图像中的颜色补偿与白平衡设计提供了直接的可迁移思路。与现有工作相比，当前项目更关注将稳态前置白平衡、互补三分支增强、亮度域特征门控融合以及面向结构可读性的设计动机整合到同一条可复现实验主线中。

## 论文写作注意事项

- 第一段用于概括传统水下增强路线。
- 第二段突出 HAB 显微图像增强谱系，这是让项目显得扎根于具体场景而不是泛泛而谈的关键。
- 第三段介绍现代深度模型，但不要让深度模型主导全文叙事。
- 第四段解释为什么可以借鉴白平衡和直方图建模思想。
- 最后一段作为过渡，引出本文方法。

## 建议下一步

可将本文档进一步整理为：

1. 约 500 到 800 字的会议论文相关工作短版；
2. 中文草稿为主、英文 claim 句为辅的双语版本，用于后续 LaTeX 写作。

## 论文短版中文相关工作

水下图像增强旨在缓解由光吸收、散射和波长依赖衰减引起的颜色失真、低对比度和细节模糊。早期方法主要依赖颜色补偿、多尺度融合和成像先验建模。典型代表包括基于颜色平衡与多尺度融合的单幅增强方法，以及基于暗通道先验和 Retinex 变分建模的恢复方法。这类方法具有较强可解释性，但在复杂退化场景下对高层语义信息和任务相关特征的建模能力有限。

针对有害藻华显微图像，相关研究逐渐形成了从分解融合到颜色补偿再到白平衡引导增强的演进路线。已有工作通过经验模态分解与小波融合提升藻类纹理细节，通过循环颜色补偿和多尺度融合改善整体对比度，并进一步结合自适应白平衡、注意力引导和金字塔融合，将增强效果与边缘检测、关键点匹配等下游任务联系起来。这说明 HAB 显微图像增强不仅需要改善视觉质量，更需要服务于细胞边缘和形态结构的清晰表达。

近年来，深度学习方法开始引入语义引导、全局分布学习和 Transformer 建模。语义注意力网络能够通过多尺度感知提升区域增强的一致性，基于直方图的 Transformer 则可从全局统计分布角度建模颜色校正过程。此外，白平衡校正领域的直方图与通道交互建模方法也为严重颜色偏移场景提供了有价值的启发。与现有研究相比，本文更关注将任务相关的白平衡与颜色校正、互补的细节与对比分支、多尺度融合机制以及面向边缘敏感任务的验证方式整合到统一框架中。

## 英文辅助稿（仅供后续 LaTeX 英文改写）

### 相关工作（英文辅助稿）

Underwater image enhancement aims to alleviate color distortion, low contrast, and detail degradation caused by wavelength-dependent absorption and scattering. Early methods mainly relied on color compensation, multi-scale fusion, and image formation priors. Representative examples include fusion-based enhancement pipelines, generalized dark channel prior models, and Retinex-based optimization frameworks. These methods are generally interpretable, but they are limited in modeling high-level semantics and task-relevant structures under complex degradations.

For HAB microscopic imagery, prior studies have formed a more task-specific development line. Earlier work explored empirical mode decomposition and wavelet fusion to recover fine algae structures. Subsequent work introduced cyclic color compensation and multi-scale fusion, and further connected enhancement quality to downstream tasks such as edge detection and keypoint matching. More recent work combined adaptive white-balance color compensation, attention-guided processing, and pyramid fusion, showing that enhancement for HAB microscopy should be evaluated not only by visual quality but also by its utility for biological structure perception.

Recent deep models have extended underwater enhancement with semantic guidance, global distribution learning, and transformer-based design. Semantic attention networks improve region-wise consistency through multi-scale perception, while histogram-based transformers model global color statistics for enhanced correction quality. In addition, recent white-balance correction models suggest that histogram-aware and channel-interactive representations are valuable for severe color-cast removal, even though they are not designed specifically for underwater microscopy.

Compared with previous work, our project is more concerned with integrating task-aware white balance and color correction, complementary detail and contrast branches, multi-scale fusion, and edge-oriented validation into a unified enhancement framework. This positioning connects traditional enhancement logic, HAB-specific application needs, and modern representation learning in a single project narrative.
