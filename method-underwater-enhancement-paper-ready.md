# Paper-Ready Method Section Draft

Last updated: 2026-04-17

This file is a tighter, paper-oriented rewrite of the code-aligned method notes in `method-underwater-enhancement.md`. It is intended to be closer to a conference-paper `Method` section and easier to adapt into LaTeX or Notion.

## Suggested Section Title

`3 Method`

Alternative working title:

`A Stage-Wise Task-Oriented Enhancement Framework for Underwater HAB Microscopic Imagery`

## Chinese Paper-Ready Draft

### 3 方法

本文提出一套面向有害藻华水下显微图像的分阶段增强框架，其目标是在缓解颜色偏移、局部低对比度和照明不均匀的同时，提高细胞边缘和纹理结构的可辨识性。与将单一增强算子直接作用于整幅图像的做法不同，本文采用“前置稳定化、分支互补增强、结构化融合、轻量收口”的总体设计。具体而言，方法首先使用灰像素引导的前置白平衡模块将输入图像拉回更稳定的颜色起点；随后，从白平衡结果并行生成高频细节、主体对比和局部可见性三条互补分支；接着，在亮度空间中根据频率层级和区域特征对三条分支进行门控融合；最后，通过轻量照明与对比收口得到最终输出。该框架既保留了传统增强链路的可解释性，也使整个方法更自然地服务于边缘敏感的下游分析任务。

#### 3.1 灰像素引导的前置白平衡

前置白平衡模块负责将严重偏色和通道失衡压回稳定区域，而不是提前承担最终视觉增强任务。具体来说，本文首先在 Lab 空间中选取近中性且位于中等亮度范围的像素，以估计当前输入的全局颜色偏移，并据此执行一次受限的通道预增益补偿。考虑到水下成像中红通道衰减更明显，方法允许红通道拥有略高的补偿上限，但整体增益仍被严格限制在安全区间内。随后，方法在预补偿结果上执行 ACCC 风格的循环补偿，但仅在中亮度区域统计通道均值，并对每轮补偿量施加截断与步长控制，从而降低深阴影、高光区域和极端颜色块对结果的破坏。最后，为避免前置校正过度改变后续分支的亮度起点，模块对整体亮度执行回调约束，使该阶段的作用集中在“颜色稳定化”而不是“强观感增强”。这一设计使前置白平衡成为整个框架的稳态入口，也为后续三分支的职责分离提供了更可靠的输入基础。

#### 3.2 IMF1-Rayleigh 高频细节分支

在获得白平衡结果后，本文首先构建 IMF1-Rayleigh 高频细节分支，用于恢复细胞边缘和细纹理信息。该分支在 Lab 的亮度通道上执行二维经验模态分解，并提取第一 IMF 作为高频候选响应。考虑到显微图像中的细胞边界和局部纹理对尺度十分敏感，方法允许在 EMD 求解阶段单独对亮度图做重采样，以提高 IMF1 提取质量而不过度增加整条流水线的代价。得到 IMF1 后，方法对其进行标准差归一化和双曲正切限幅，再通过 guided filter 将高频响应约束到原始亮度结构上，以抑制离散噪声和不稳定伪高频。随后，本文结合多尺度高通响应、局部方差和梯度信息，对纹理丰富且边界明显的区域增强细节注入强度，并以 Rayleigh 匹配重整亮度分布。通过这一路径，细节分支主要提供高频清晰度、边缘响应和纹理表达，而不负责全局亮度托底或背景区域补偿。

#### 3.3 互补的对比与局部可见性分支

除细节分支外，本文还设计了两条互补的亮度增强分支，分别负责主体层次和局部可见性。第一条为白平衡安全对比分支。该分支在 Lab 空间中对亮度通道执行分位拉伸、轻度平滑和局部对比增强，并通过双边滤波减轻块效应。为避免在大面积平坦区域中引入虚假结构，方法进一步依据梯度强度构造平坦区抑制权重，使增强更集中于真实结构区域。同时，为防止局部亮度增强重新破坏前置白平衡建立的颜色稳定性，该分支根据亮度变化比对色度进行自适应压缩，并通过色域守护与后端 Lab 微调抑制颜色越界。因此，这一分支在当前框架中主要承担主体层次增强、亮度托底和色彩锚定的角色。

第二条为 CLAHE 引导的局部可见性分支。这里的关键不在于直接输出原始 CLAHE 图像，而在于把 CLAHE 当作局部亮度增益的提议器。具体而言，方法先对三个通道分别施加 CLAHE，再根据增强前后的亮度变化估计局部增益图，并对其上下界进行约束。随后，方法以原始亮度为引导，对增益图进行 guided filter 平滑，使局部增亮沿真实结构传播，而不是沿 CLAHE 网格边界扩散。由于该增益最终以近线性 RGB 的等比例方式作用于三个通道，因此它能在提升暗部与背景可见性的同时，尽量保持前置白平衡建立的颜色关系。与对比分支相比，这一路径更偏向于中层与背景区域的可见性补偿，而不是主体亮度锚定。

#### 3.4 特征门控的三分支融合

在得到三条功能互补的增强结果后，本文在亮度空间中执行特征门控的三分支融合。与直接在 RGB 域做均值融合不同，本文首先将三条分支统一映射到 Lab 的亮度通道，并分别计算梯度、局部纹理、高频显著性和曝光适宜度等特征图，构造各自的基础权重。由于三条分支承担的职责并不相同，权重设计也采用非对称方式：细节分支更依赖梯度和纹理，对比分支更依赖曝光与主体层次，局部可见性分支更依赖显著性和中层对比。随后，方法进一步利用局部方差、前景背景差异和局部对比度对三路权重施加区域偏置，使细节分支在结构丰富区域拥有更高发言权，使局部可见性分支在背景和低对比区域承担更多补偿，而使对比分支维持全局亮度锚点功能。

为了保证这种职责分配在不同频率层上都稳定有效，本文进一步在拉普拉斯金字塔域执行分层融合。细节分支主要参与高频层，局部可见性分支主要参与中频层，而对比分支则在低频层中占据更重要地位。同时，方法为局部可见性分支设置中高频保底占比，避免低频锚点分支在中频层完全吞掉背景与暗部补偿效果。所有权重图在进入层级归一化前，都通过 guided filter 对齐到对比分支的亮度结构，从而减少融合边界中的不连续现象。融合完成后，本文再对重建亮度执行温和的分位拉伸和 S 型收口，以进一步提升整体通透感。需要强调的是，该阶段融合的核心是亮度结构而不是颜色本身，最终色度默认仍以对比分支为锚点，以降低跨分支混色带来的偏色风险。

#### 3.5 最终照明与对比收口

融合结果进入最终阶段后，本文不再重新构造新的主体结构，而是仅执行轻量照明与对比收口。当前实现支持基于 Lab 亮度通道的同态滤波、基于分位拉伸和弱 CLAHE 的熵增强，以及两者串联的组合模式。主线配置采用“先同态、后熵增强”的两步式处理：前者主要用于压制低频照明不均匀并适度强化细节，后者主要用于提升全局亮度分布和局部对比，同时用轻微色度补偿维持最终观感。这样的设计使最终阶段更适合作为稳定收口模块，而不是方法创新的主要承载点。从实验组织角度看，这一定位也与本文的消融逻辑一致，即 H1 主要验证前置白平衡，H2 主要验证三分支与融合机制，H3 仅验证最终收口对整体表现的附加增益。

#### 3.6 方法定位

综合来看，本文真正想强调的并不是某个单一增强算子的局部改造，而是一套面向 HAB 显微图像任务需求的结构化增强框架。前置白平衡模块提供稳定输入，细节、对比和局部可见性三条分支分别承担互补职责，融合阶段根据频率层级和区域特征进行门控分配，最终收口阶段则负责温和整理照明与对比。由此，方法能够在保持结构真实性和颜色稳定性的前提下，提高显微藻类图像的可判读性，并为后续边缘敏感分析提供更友好的输入表示。

## Condensed Chinese Version

本文提出一套面向有害藻华水下显微图像的分阶段增强框架。方法首先利用灰像素引导的前置白平衡模块稳定颜色起点，并通过受限预增益、截断式循环补偿和亮度回调抑制严重偏色。随后，从白平衡结果并行生成三条互补分支：IMF1-Rayleigh 高频细节分支用于恢复细胞边缘与细纹理，白平衡安全对比分支用于提供主体层次和色彩锚定，CLAHE 引导的局部可见性分支用于补偿背景与暗部可见性。最后，方法在 Lab 亮度空间中构造梯度、纹理、显著性和曝光等特征权重，并在拉普拉斯金字塔域按频率层级执行门控融合，再通过轻量同态与熵增强模块完成照明与对比收口。

与将同一种增强机制统一施加于整幅图像的做法不同，本文强调分支间的职责分工与结构化协同。前置白平衡负责稳定输入，细节分支负责高频清晰度，对比分支负责主体层次与颜色锚定，局部可见性分支负责背景和暗部补偿，而最终模块只承担温和收口而不重新定义主要结构。这一设计既符合当前代码实现，也更适合支持后续围绕白平衡、三分支融合和最终收口的分阶段消融实验。

## English Paper Skeleton

### 3 Method

We propose a stage-wise enhancement framework for underwater HAB microscopic imagery, designed to improve color recovery, local visibility, structural readability, and downstream edge-oriented usability in a unified pipeline. Instead of applying a single enhancement operator to the entire image, the framework follows a stabilize-enhance-fuse-refine design: it first normalizes the input by a gray-pixel-guided pre-white-balance module, then constructs three complementary enhancement branches for detail recovery, contrast support, and local visibility compensation, and finally performs feature-gated fusion followed by lightweight illumination and contrast refinement.

#### 3.1 Gray-Pixel-Guided Pre-White-Balance

The pre-white-balance module is designed as an upstream stabilization stage rather than a final visual enhancement block. It first estimates the dominant color cast from near-neutral pixels in a middle-luminance range and performs constrained channel-wise pre-gain correction. A clipped and step-controlled ACCC-style cyclic compensation is then applied only on mid-luminance regions, which reduces over-correction caused by highlights, shadows, or extreme color patches. A final brightness restoration step keeps the output close to the original luminance scale, making this stage serve as a stable entry point for all subsequent branches.

#### 3.2 IMF1-Rayleigh Detail Branch

The first branch focuses on high-frequency detail recovery. We extract the first empirical mode from the luminance channel and optionally resample the luminance image during EMD solving to better capture scale-sensitive microscopic structures. The extracted response is normalized, softly bounded, and aligned to the underlying luminance structure by guided filtering. We further modulate the detail injection using multi-scale high-pass responses, local variance, and edge-aware weighting, and then apply Rayleigh luminance matching to improve detail visibility and luminance distribution. This branch is mainly responsible for edge sharpness and fine texture recovery.

#### 3.3 Complementary Contrast and Local Visibility Branches

To complement the detail branch, we construct two additional luminance-oriented branches. The white-balance-safe contrast branch enhances subject-level contrast in Lab space with percentile stretching, local contrast enhancement, flat-region suppression, adaptive chroma protection, and gamut-aware correction, thereby providing global luminance anchoring and stable color support. The CLAHE-guided local visibility branch does not directly output raw CLAHE results; instead, it estimates a smooth local gain map from CLAHE-induced brightness changes and applies the gain in a white-balance-preserving manner. This design makes it more suitable for background and low-visibility compensation than for subject anchoring.

#### 3.4 Feature-Gated Three-Branch Fusion

The three branches are fused in the luminance domain rather than naively averaged in RGB space. We compute branch-specific weights from gradient, texture, saliency, exposure, local variance, and region-dependent cues, and then perform Laplacian-pyramid fusion with level-aware gating. The detail branch mainly contributes to high-frequency layers, the local visibility branch mainly contributes to mid-frequency layers, and the contrast branch anchors low-frequency structure and chroma. Guided filtering is used to align all weight maps to a common luminance structure before normalization, which helps maintain fusion continuity across spatial regions and pyramid levels.

#### 3.5 Final Refinement

The final stage is a lightweight refinement block rather than the main source of structural enhancement. It applies homomorphic illumination correction and entropy-oriented luminance adjustment in sequence to reduce uneven illumination, improve global luminance distribution, and gently refine local contrast. This makes the final stage suitable for controlled output stabilization and consistent with the paper's ablation logic, where the major emphasis remains on upstream normalization and feature-gated multi-branch enhancement.

## Figure Caption Draft

`Overview of the proposed stage-wise enhancement framework. The input image is first stabilized by gray-pixel-guided pre-white-balance, then processed by three complementary branches for detail recovery, contrast anchoring, and local visibility compensation. The branch outputs are fused by feature-gated Laplacian-pyramid fusion in the luminance domain, followed by lightweight illumination and contrast refinement.`

## Transition Sentence to Experiments

`Based on this design, the experiments are organized to separately evaluate the contribution of upstream white-balance stabilization, complementary branch fusion, and final lightweight refinement under a unified full506 protocol.`

## Notes

- This version is intentionally more concise than `method-underwater-enhancement.md`.
- The paper should still describe `RGHS` and `CLAHE` by function rather than by historical name.
- The task-facing “downstream edge-oriented validation” is better presented in the experiments section than as part of the enhancement operator itself.
