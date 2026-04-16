# Underwater Image Enhancement Method Draft

Last updated: 2026-04-17

This note is a code-aligned method draft for the current HAB underwater microscopic image enhancement project. It is meant for two direct uses:

1. drafting the method section of the paper;
2. keeping the writing aligned with the actual implementation in the repo.

## Writing Position

- Target task: underwater HAB microscopic image enhancement with emphasis on structure readability and downstream edge-sensitive analysis.
- Current enhancement chain:
  `Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`
- Recommended paper naming:
  - `BPH`: gray-pixel-guided pre-white-balance
  - `IMF1Ray`: IMF1-Rayleigh detail branch
  - `RGHS`: white-balance-safe contrast branch
  - `CLAHE`: CLAHE-guided local visibility branch
  - `Fused`: feature-gated three-branch fusion
  - `Final`: illumination and contrast refinement
- Important naming boundary:
  the historical stage names `RGHS` and `CLAHE` are still kept in code, configs, experiment folders, and result assets for compatibility, but the paper should describe them by their actual functions rather than present them as standard RGHS or plain CLAHE modules.
- Local main file for this draft:
  `D:\Desktop\Stage1Codex\method-underwater-enhancement.md`

## Code Anchor

| Stage | Main file | Practical role in the current repo |
| --- | --- | --- |
| `BPH` | `lgsbph.py` | stabilize color cast and channel imbalance before all later branches |
| `IMF1Ray` | `pybemd.py` | extract high-frequency detail, edge response, and luminance redistribution |
| `RGHS` | `wb_safe_contrast.py` | enhance subject contrast while protecting white-balance stability |
| `CLAHE` | `clahe_guided_visibility.py` | derive a smooth local visibility gain from CLAHE rather than output raw CLAHE directly |
| `Fused` | `fusion_three.py` | assign branch responsibility across pyramid levels and fuse luminance structure |
| `Final` | `lvbo.py` | perform homomorphic illumination cleanup and optional entropy-oriented Lab refinement |

## Chinese Full Draft

### 方法概述

本文围绕有害藻华水下显微图像的颜色偏移、局部低对比度、细节模糊和照明不均匀等问题，构建了一条分阶段、职责明确的增强框架。整体上，该框架不是依赖单一增强算子一次性完成所有视觉修复，而是先通过前置白平衡把输入拉回稳定起点，再并行生成高频细节、主体对比和局部可见性三条互补分支，随后在融合阶段按照频率层级和区域特征分配不同分支的发言权，最后通过轻量照明与对比收口得到最终结果。这样的设计使方法既保留传统可解释增强链路的可控性，又能把任务相关的结构细节和下游边缘可读性纳入统一优化目标。

### 3.1 灰像素引导的前置白平衡

给定输入图像，本文首先执行灰像素引导的前置白平衡模块。该模块并非直接照搬基础的循环颜色补偿过程，而是采用“三步式”稳健设计。第一步，在 Lab 空间中利用近中性且处于中等亮度范围的像素估计全局颜色偏移，并据此执行一次受限的通道预增益补偿，其中红通道允许稍大的补偿上限，以适应水下成像中更明显的红衰减。第二步，在预补偿结果上进行截断和步长受控的 ACCC 式循环补偿，但均值统计仅在中亮度区域进行，同时对每轮通道差值进行截断，以避免阴影、高光或极端颜色区域导致过补偿。第三步，模块对输出执行亮度回调，使白平衡阶段的职责保持在“颜色校正与起点稳定”，而不是提前承担最终增强观感。通过这种设计，前置白平衡既缓解了严重偏色，又降低了后续细节分支和融合阶段对颜色失衡的被动兜底压力。

### 3.2 IMF1-Rayleigh 高频细节分支

在完成前置白平衡后，方法从白平衡结果出发构建 IMF1-Rayleigh 高频细节分支。该分支首先在 Lab 的亮度通道上执行二维经验模态分解，提取第一 IMF 作为高频候选响应。考虑到显微图像中细胞边缘和局部纹理具有明显尺度敏感性，本文在 EMD 求解阶段支持对亮度图做单独重采样，从而以较低的系统开销提高 IMF1 提取质量。获得 IMF1 后，分支对其进行标准差归一化与双曲正切限幅，再通过 guided filter 约束高频响应与原始亮度结构对齐，以抑制孤立噪声和不稳定高频。与此同时，方法进一步结合多尺度高通响应与局部方差图，对纹理丰富区域赋予更高的细节注入强度，并通过 Scharr 梯度构造边缘聚焦权重，使增强主要集中在真实边界而非大面积平坦背景。最后，本文在注入后的亮度通道上执行 Rayleigh 匹配，借助分布重整提升整体通透感和亮度层次，再与原有色度信息合成得到该细节分支输出。整体上，该模块负责提供边缘、纹理和高频清晰度，而不直接承担大范围亮度托底和背景可见性修复。

### 3.3 白平衡安全对比分支与局部可见性分支

除高频细节之外，本文还设计了两条功能互补的亮度增强分支。第一条为白平衡安全对比分支。该分支在 Lab 空间内以亮度增强为主线：先对亮度通道进行分位拉伸和轻微平滑，再施加 CLAHE 增强，并通过双边滤波减轻块效应。随后，方法根据梯度强度构造平坦区抑制权重，使增强更偏向结构区域而避免在大面积平滑背景中放大伪对比。同时，为防止增强过程破坏前置白平衡建立的颜色稳定性，该分支依据亮度变化比自适应压缩色度，并进一步通过色域守护和后端 Lab 微调抑制颜色越界。由此，该分支在当前框架中的核心职责是提供主体层次、亮度托底和相对稳定的色彩锚点。

第二条为 CLAHE 引导的局部可见性分支。与传统做法不同，本文并不直接将三通道 CLAHE 结果作为独立增强输出，而是仅利用 CLAHE 前后亮度的变化关系估计局部增益图。具体而言，方法先对三个通道分别执行 CLAHE，再根据增强前后的 BT.709 亮度比值得到局部亮度增益，并对增益上下界进行约束。之后，以原始亮度作为引导，对增益图施加 guided filter 平滑，使局部增亮沿真实结构变化而不是沿块边界传播。为了维持白平衡稳定性，该增益在近线性 RGB 域中按比例作用于三个通道，而不是对色彩独立操作。最后，模块仅在 Lab 空间执行温和的亮度和色度收口。通过这种“CLAHE 只负责提出增益建议、真正输出来自平滑且白平衡安全的亮度缩放”的设计，该分支更适合承担背景、暗部和局部可见性补偿任务。

### 3.4 特征门控的三分支融合

在获得三条互补分支后，本文提出一套面向亮度结构分工的特征门控融合机制。该融合不是直接在 RGB 域对三张增强图做平均，而是首先把 IMF1Ray、白平衡安全对比和局部可见性三条分支统一映射到 Lab 的亮度通道上，并分别计算梯度、局部纹理、高频显著性和曝光适宜度等特征图，进而构造三组初始权重。由于不同分支的职责并不相同，权重设计并非对称：细节分支更依赖梯度和纹理，对比分支更依赖曝光与主体层次，局部可见性分支则更依赖显著性与中层对比。随后，方法进一步利用局部方差、前景背景差异和局部对比度，对三路权重施加区域偏置，使细节分支在结构丰富区域发言更强，局部可见性分支在背景和低对比区域承担更多补偿，而对比分支维持全局亮度锚点作用。

为了实现更稳定的多尺度职责分配，本文在拉普拉斯金字塔域执行分层融合。具体来说，细节分支主要参与高频层，局部可见性分支主要参与中频层，而对比分支在低频层中具有更高权重；同时，通过为局部可见性分支设置层内保底占比，避免低频锚点分支在中频层完全吞掉背景补偿效果。所有权重图都先通过 guided filter 对齐到对比分支的亮度结构，再参与层级归一化。融合完成后，方法对重建亮度做温和的分位拉伸与 S 型收口，以进一步提升整体通透感。需要强调的是，该融合阶段主要融合的是亮度结构而不是颜色本身，最终色度默认以白平衡安全对比分支为锚点，从而减少跨分支混色导致的偏色风险。

### 3.5 最终照明与对比收口

融合结果进入最终收口阶段后，本文采用轻量照明与对比细化，而不再重新生成新的主体结构。当前实现中，最终模块支持基于 Lab 亮度通道的同态滤波、基于亮度分位拉伸和弱 CLAHE 的熵增强，以及两者串联的组合模式。主线配置采用先同态、后熵增强的两步式处理：同态滤波负责压制低频照明不均匀并适度强化细节，同时通过亮度匹配把输出均值拉回接近融合输入；随后，熵增强仅在亮度通道上执行全局拉伸和弱局部对比提升，并配合轻微色度补偿提高最终观感指标。基于当前 full506 主线实验，最终锁定配置采用 `locked_full506_final_mainline.json` 中的六阶段组合，其核心思想并不是把最后一层写成新的主要创新点，而是将其定位为对前述三分支融合结果的稳定收口模块。

### 3.6 写作边界与方法定位

从论文写作角度看，本文的方法创新更适合被表述为“面向 HAB 显微图像的任务化增强框架”，而不是某个单独模块的孤立新算子。前置白平衡模块提供稳定起点，高频细节分支、对比分支和局部可见性分支分别承担互补职责，融合阶段再根据频率层级和区域特征进行门控分配，最终收口阶段保证亮度和观感的一致性。这样的表述既符合当前代码真实实现，也更容易与后续消融设计对应：H1 主要验证前置白平衡，H2 主要验证三分支与融合策略，H3 仅验证最终照明细化的附加价值。换句话说，论文中最值得强调的是“职责化分支设计 + 特征门控融合 + 下游边缘友好验证”的整体叙事，而不是把历史命名为 `RGHS` 或 `CLAHE` 的单个模块包装成标准现成方法。

## Chinese Short Draft

本文提出一套面向有害藻华水下显微图像的分阶段增强框架。该框架首先通过灰像素引导的前置白平衡模块稳定颜色起点，再从白平衡结果并行生成三条互补分支：IMF1-Rayleigh 高频细节分支用于强化边缘和纹理，白平衡安全对比分支用于提供主体层次和亮度托底，CLAHE 引导的局部可见性分支用于补偿暗部和背景可见性。随后，方法在 Lab 亮度空间中构造梯度、纹理、显著性和曝光等特征权重，并在拉普拉斯金字塔域按频率层级分配三条分支的职责，以实现面向亮度结构的特征门控融合。最后，本文利用轻量同态滤波和熵增强对融合结果进行照明与对比收口，同时保持颜色稳定性。

与将单一增强算子直接作用于整幅图像的做法不同，本文更强调各模块的职责分工与协同关系。前置白平衡负责把严重偏色拉回稳定区域，细节分支负责高频清晰度，对比分支负责主体层次和色彩锚定，局部可见性分支负责背景和暗部补偿，最终收口模块只承担温和整理而不重新定义主要结构。这一设计使方法既保留传统增强链路的可解释性，又能更自然地服务于边缘敏感的下游分析任务。

## English Skeleton

### Method Overview

We develop a stage-wise enhancement framework for underwater HAB microscopic imagery, aiming to address severe color cast, low local contrast, blurred fine structures, and uneven illumination. Rather than relying on a single global enhancement operator, the framework first stabilizes the color distribution by a gray-pixel-guided pre-white-balance module, then constructs three complementary branches for detail recovery, contrast support, and local visibility compensation, and finally performs feature-gated fusion followed by lightweight refinement.

### Pre-White-Balance Module

The pre-white-balance stage combines gray-pixel-guided global gain estimation with a clipped and step-controlled ACCC-style cyclic compensation procedure. Neutral pixels in a middle-luminance range are used to estimate the dominant color cast, and channel gains are constrained to avoid unstable over-correction. The subsequent iterative compensation is computed only on mid-luminance regions and uses clamped inter-channel differences, which makes the white-balance stage serve as a stable upstream normalization module rather than an overly aggressive visual enhancer.

### Three Complementary Enhancement Branches

Starting from the white-balanced image, the IMF1-Rayleigh branch extracts the first empirical mode component on the luminance channel, aligns the high-frequency response with the underlying structure by guided filtering, and injects detail with edge-aware weighting before applying Rayleigh luminance matching. In parallel, the white-balance-safe contrast branch performs luminance enhancement in Lab space with flat-region suppression, chroma protection, and gamut-aware correction to provide stable subject contrast and color anchoring. The CLAHE-guided local visibility branch does not directly output raw CLAHE results; instead, it derives a smooth luminance gain map from CLAHE-induced brightness changes and applies this gain in a white-balance-preserving manner.

### Feature-Gated Fusion and Final Refinement

The three branches are fused in the luminance domain rather than naively averaged in RGB space. We compute branch-specific weights from gradient, texture, saliency, exposure, local variance, and region-dependent cues, and then perform Laplacian pyramid fusion with level-aware branch gating: the detail branch mainly contributes to high-frequency layers, the local visibility branch mainly contributes to mid-frequency layers, and the contrast branch anchors low-frequency structure and chroma. A final refinement stage applies lightweight homomorphic illumination correction and entropy-oriented Lab adjustment, which acts as a controlled closing step instead of the main source of structural enhancement.

## Implementation Anchor

### Current Accepted Mainline

- main config:
  `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- upstream white balance:
  `r2_05_G_P_A_B`
- IMF1Ray:
  current mainline uses the aggressive detail preset and keeps the branch as the high-frequency detail path
- contrast branch:
  `rghs_s07`
- local visibility branch:
  `clahe_s05`
- fusion:
  `fusion_s10`
- final refinement:
  `r4_03` via `homomorphic_entropy`

### Not-for-Paper but Useful Reminder

- The implemented enhancement pipeline contains six operational stages after the input image.
- In project-level narrative, a seventh step, downstream edge-oriented validation, can be presented as the task-facing evaluation stage rather than as part of the enhancement operator itself.
- If the paper needs a cleaner name, a safe working title is:
  `A stage-wise task-oriented enhancement framework for underwater HAB microscopic imagery`.
