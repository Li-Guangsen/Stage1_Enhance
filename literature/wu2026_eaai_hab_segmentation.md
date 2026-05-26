# Wu et al. 2026 EAAI：HAB 显微图像增强与双分支分割

更新时间：2026-05-24

本条目根据 Zotero 本地条目和 PDF 全文索引整理，是同方向师兄已发表一区赤潮 / HAB 主要参考论文之一。

## 1. 文献信息

- Title: `Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network`
- Authors: Gengkun Wu, Chao Cui, Yining Fan, Yubing Li, Xin Tian
- Venue: `Engineering Applications of Artificial Intelligence`
- Volume / Article: `177`, Article `114948`
- Year: 2026
- DOI: `10.1016/j.engappai.2026.114948`
- URL: `https://linkinghub.elsevier.com/retrieve/pii/S0952197626012303`
- Zotero item key: `ZMUBCGCD`
- Zotero citation key: `wu2026`

## 2. 论文内容概述

这篇论文不是单纯的 segmentation 论文，而是把 HAB 显微图像中的退化增强与下游分割耦合为一个工程应用框架。

论文主线包括：

- Enhancement：CCCC、PSCB 与 adaptive pyramid fusion，用于通道一致性、颜色衰减补偿和脆弱结构恢复。
- Segmentation：TCoF 双分支网络，结合 Transformer 全局语义与 CNN 边界细节。
- MFCM：用 CNN-derived boundary priors 显式引导 Transformer 跨尺度聚合。
- DASPP：针对细薄、弱边界和不规则藻类结构，修正标准 ASPP 的轮廓平滑偏置。
- 实验：在 AICO Lab HAB 数据集上报告分割指标，并补充增强、消融、效率、跨域和失败案例分析。

## 3. 对 Stage1Codex 的约束

这篇论文对当前项目的约束是：

- 不能把 “task-driven enhancement + downstream boundary task” 当成未经占据的新叙事。
- Stage1 的增强指标不能作为核心贡献终点；必须通过 edge-specific 下游证据说明它服务边界结构。
- 若总体论文走 EAAI 路线，摘要和贡献必须清楚拆开 AI contribution 与 engineering application contribution。
- 若引用这篇论文作为对标，需要强调本文任务从 segmentation mask 转向 edge continuity、pseudo-edge suppression、boundary recoverability 和 morphology consistency。

## 4. 后续待核验

- 正式文献笔记应继续摘录 TCoF、MFCM、DASPP、enhancement ablation、segmentation ablation、效率和 cross-dataset 结果。
- 若总体论文投 EAAI，应按这篇论文的工程证据链补齐数据采集、运行资源、跨域验证、失败案例和下游应用说明。
