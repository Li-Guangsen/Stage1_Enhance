# Wu et al. 2026 ESWA：HAB 显微图像增强与扩散边缘检测

更新时间：2026-05-24

本条目修正旧的 `Frontiers 2024` 记录。当前以 Zotero 本地条目和 PDF 全文索引为准。

## 1. 文献信息

- Title: `Enhanced edge detection of harmful algal Blooms using diffusion probability models and Sobel-convolutional attention mechanisms`
- Authors: Gengkun Wu, Yining Fan, Xin Tian, Chao Cui, Jiazheng Han
- Venue: `Expert Systems with Applications`
- Volume / Article: `298`, Article `129663`
- Year: 2026
- DOI: `10.1016/j.eswa.2025.129663`
- URL: `https://linkinghub.elsevier.com/retrieve/pii/S0957417425032786`
- Zotero item keys: `9MCJDQGE`、`AKGYHG77`（重复条目）
- Zotero citation key: `wu2026`

## 2. 论文内容概述

这篇论文是同方向 HAB / 赤潮显微图像边缘检测一区参考文献。它不是单纯的图像增强论文，而是把 HAB 显微图像退化、增强预处理和扩散式边缘检测组织成一个完整任务链。

论文主线包括：

- 面向 HAB 显微图像的专用增强预处理，用于改善对比度、边缘和纹理特征。
- 基于 VAE / DDPM 思路的 SIAnet 边缘检测网络。
- Cross-layer Integrated Attention Feature Fusion（CIAFF），用于跨层上下文聚合和噪声抑制。
- Learnable Sobel operator，用可训练 Sobel 结构先验补充边缘特征并加速训练。
- 实验围绕 HAB 边缘检测，并报告 ODS、OIS、AP 等边缘任务指标，同时补充 BSDS / BIPED 泛化。

## 3. 对 Stage1Codex 的约束

这篇论文对当前项目的意义不只是“支持下游边缘验证”，而是给出了明确重合风险：

- 不能再把总体论文简单写成“先增强，再边缘检测”的 pipeline。
- Stage1Codex 当前更适合定位为 `task-driven structure-preserving input formation`，即为 MyEdge 主论文提供结构保持增强输入与证据。
- 如果后续写 MyEdge 主论文，核心差异应落在 MSFI / spatial-frequency latent diffusion / weak-boundary frequency interaction，而不是泛泛地说使用扩散模型、Sobel 先验或注意力融合。
- Stage1 的无 GT 边缘结构 proxy 只能作为衔接证据，不能替代这类论文中带 GT 的 ODS / OIS / AP / AC 边缘检测评测。

## 4. 后续待核验

- 摘要中写到 `ODS = 0.645`、`OIS = 0.702`、`AP = 0.813`；后续正式文献笔记应继续核对全文表格中 AP / AC 指标是否存在表述不一致。
- 需要进一步摘录增强消融、CIAFF 消融、learnable Sobel 消融和复杂度结果，以便和 MyEdge 的 MSFI 消融形成直接对照。
- Zotero 中存在两个重复条目，后续整理引用库时应保留一个主条目并避免重复导出 BibTeX。
