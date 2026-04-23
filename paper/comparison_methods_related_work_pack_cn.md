# 对比方法与 Related Work 论文可用包（中文）

更新时间：2026-04-23

本文件用于统一当前项目中“实验对比方法”和“相关工作综述方法”的口径，直接服务于中文主稿写作。其目标有五个：

1. 锁定对比方法分类。
2. 提炼每篇核心论文的机制与写法边界。
3. 生成实验节可直接复用的“对比方法设置”段落。
4. 生成相关工作中文段落。
5. 审校当前主观评价是否越界。

## 1. 使用口径

当前材料分为两层：

- 核心已核验集：当前已实际跑图、且可由本地 PDF 或 Zotero 题录与摘要核验的 8 篇方法。
- 扩展综述集：用于补齐 related work 全景视角，但不自动进入主实验表。

当前写作中必须区分三种身份：

- 实验正式对比方法：已经统一生成输出结果的外部方法。
- 综述补全方法：用于 related work 的典型代表，但当前未进入统一跑图或未完成题录本地化整理。
- 场景谱系文献：用于说明 HAB 显微增强研究脉络，不应和“外部对比方法”混写。

当前正式实验口径还必须区分两套输出：

- 阶段进度表：`metrics/manifests/full502_clean_v1.txt` -> `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
- 外部主比较表：`metrics/manifests/compare9_complete496_v1.txt` -> `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`

因此，文稿中不再把历史 `full506` 搜索/锁定资产写成当前正式主表口径。

当前主表写作还需要额外固定三条叙述规则：

- 正式数值表保留全部 `9` 方法，不人为删除 `WWPF`、`HLRP` 或 `Histoformer`。
- `MS_SSIM` 与 `PSNR` 在本文中统一解释为增强结果相对原图的结构一致性，而不是相对增强真值的质量指标。
- 正文主讨论以 `Ours`、`HVDualformer`、`ABC-Former`、`GDCP`、`CBF`、`SGUIE-Net` 和 `WWPF` 为稳健方法集合展开；`HLRP` 与 `Histoformer` 虽保留在正式主表中，但应按失败案例或补充分析处理。
- 所有负面判断都必须加上场景限定语，即“在当前 HAB 水下显微图像协议下”，不能写成对原论文方法整体有效性的否定。

## 2. 统一分类口径

### 2.1 实验正式对比方法

| 分类层 | 方法 | 当前身份 | 说明 |
| --- | --- | --- | --- |
| 深度白平衡 | `HVDualformer`, `ABC-Former` | 已跑图 + 可写实验节 | 仍属于白平衡论文，不写成标准水下增强模型 |
| 传统/非深度水下增强 | `GDCP`, `CBF`, `HLRP`, `WWPF` | 已跑图 + 可写实验节 | 分别代表物理先验、融合、优化建模和现代传统融合 |
| 深度水下增强 | `SGUIE-Net`, `Histoformer` | 已跑图 + 可写实验节 | 分别代表语义引导增强与直方图 Transformer 增强 |

### 2.2 综述补全方法

| 分类层 | 方法 | 当前身份 | 说明 |
| --- | --- | --- | --- |
| 传统白平衡 | `MaxRGB`, `Gray-World`, `Shades of Gray`, `Gray-Edge` | 综述补充 | 经典启发式白平衡家族，用于说明颜色恒常假设脉络 |
| 传统/非深度水下增强 | `UDCP`, `IBLA`, `VRE` | 综述补充 | 其中 `VRE` 当前仅保留方法标签，尚未锁定唯一 canonical 题录 |
| 深度水下增强 | `WaterNet`, `UWCNN` | 综述补充 | 用于把深度增强谱系补齐到更完整的历史视角 |

### 2.3 场景谱系文献

这组文献不进入“对比方法分类表”，而用于 related work 中的 HAB 显微增强谱系：

- `Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion`
- `Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion`
- `Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy`

## 3. 核心已核验集：逐篇机制卡片

### 3.1 HVDualformer

- 方法类别：深度白平衡
- 论文目标：针对不同色温导致的颜色偏移，直接输出白平衡校正结果。
- 核心机制：使用 histogram-vision dual transformer 同时建模白平衡颜色直方图和视觉特征，以颜色统计特征调节图像特征。
- 论文中可用的一句话定位：HVDualformer 是一类基于直方图与视觉双路 Transformer 的深度白平衡方法，强调全局颜色分布与视觉内容的联合建模。
- 与本文的可比点：可用于说明严重偏色场景下，全局颜色统计建模确实重要。
- 不应误写的边界：它是白平衡校正论文，不是标准水下增强论文。
- 已核验来源：Zotero `TEKJDF6M`；本地 PDF `D:\Desktop\2025AAAI_HVDual_former\32697-Article Text-36765-1-2-20250410.pdf`

### 3.2 ABC-Former

- 方法类别：深度白平衡
- 论文目标：提高 sRGB 图像白平衡校正精度。
- 核心机制：联合 CIELab/RGB 直方图与 sRGB 输入，使用 Auxiliary Bimodal Cross-domain Transformer 和 Interactive Channel Attention 实现跨模态全局颜色知识迁移。
- 论文中可用的一句话定位：ABC-Former 是结合双模态直方图和图像输入的深度白平衡模型，突出跨域颜色信息与通道交互建模。
- 与本文的可比点：可支撑“颜色分布 + 通道交互”对颜色校正有效这一论点。
- 不应误写的边界：它不是为水下显微增强设计的专门模型。
- 已核验来源：Zotero `LF9HP7DR`；本地 PDF `D:\Desktop\2025CVPR_ABC-Former\Chiu_ABC-Former_Auxiliary_Bimodal_Cross-domain_Transformer_with_Interactive_Channel_Attention_for_CVPR_2025_paper.pdf`

### 3.3 GDCP

- 方法类别：传统/非深度水下增强中的物理先验恢复
- 论文目标：在散射介质中统一处理雾、沙尘、水下等退化图像的恢复问题。
- 核心机制：利用深度相关颜色变化估计环境光，定义 scene ambient light differential 估计 transmission，并结合自适应颜色校正推广暗通道先验。
- 论文中可用的一句话定位：GDCP 代表了从成像模型与广义暗通道先验出发的物理先验恢复路线。
- 与本文的可比点：可作为物理模型基线，与本文的多分支结构化增强形成对照。
- 不应误写的边界：它更接近恢复模型，而不是任务导向的显微增强框架。
- 已核验来源：Zotero `V87JDUST`；本地 PDF `D:\Desktop\2018_Generalization-of-the-Dark-Channel-Prior\Generalization_of_the_Dark_Channel_Prior_for_Single_Image_Restoration.pdf`

### 3.4 CBF

- 方法类别：传统/非深度水下增强中的经典融合方法
- 论文目标：在不依赖硬件和场景先验的前提下，实现单幅水下图像增强。
- 核心机制：从颜色补偿和白平衡版本中构造两幅导出图像及其权重图，通过多尺度融合传递边缘与颜色对比信息。
- 论文中可用的一句话定位：CBF 是经典的颜色补偿加多尺度融合单幅水下增强框架。
- 与本文的可比点：与本文共享“多分支派生图 + 融合”的总体范式。
- 不应误写的边界：它没有任务特化的结构分支职责设计。
- 已核验来源：Zotero `AFLVZ4KR`；本地 PDF `D:\Desktop\2018_Color-Balance-and-fusion-for-underwater-image-enhancement\Color_Balance_and_Fusion_for_Underwater_Image_Enhancement.pdf`

### 3.5 HLRP

- 方法类别：传统/非深度水下增强中的优化建模方法
- 论文目标：在 Retinex 变分增强中同时改善细节恢复与颜色自然性。
- 核心机制：在反射率上施加一阶和二阶梯度的 l1/2 超拉普拉斯先验，并与照明估计共同纳入 Retinex 变分模型，通过交替最小化求解。
- 论文中可用的一句话定位：HLRP 代表了 Retinex 变分建模与高阶反射率先验结合的优化增强路线。
- 与本文的可比点：可与本文的工程化结构框架形成“优化模型 vs 职责分离框架”对照。
- 不应误写的边界：它不是融合型流水线。
- 已核验来源：Zotero `PWKRPBPJ`

### 3.6 WWPF

- 方法类别：传统/非深度水下增强中的现代传统融合方法
- 论文目标：通过视觉感知导向的多阶段融合提升水下图像质量。
- 核心机制：先做衰减图引导颜色校正，再分别进行最大信息熵优化的全局对比增强与快速积分优化的局部对比增强，最后在小波域做加权视觉感知融合。
- 论文中可用的一句话定位：WWPF 是结合颜色校正、全局/局部对比增强和加权小波融合的现代传统增强方法。
- 与本文的可比点：与本文同属多阶段、非深度、融合型增强路线。
- 不应误写的边界：当前官方包仅能稳定生成 496 张输出，不能在论文里隐去这一实现边界。
- 已核验来源：Zotero `U6DBLZMV`

### 3.7 SGUIE-Net

- 方法类别：深度水下增强
- 论文目标：在有限配对样本下提升水下图像增强的一致性与鲁棒性。
- 核心机制：引入语义区域引导和多尺度感知，通过 semantic region-wise enhancement module 学习区域级增强特征，再与主分支融合。
- 论文中可用的一句话定位：SGUIE-Net 代表了通过语义引导和多尺度感知改进增强一致性的深度方法。
- 与本文的可比点：可对照“语义驱动深度增强”和“可解释三分支增强”两种路线。
- 不应误写的边界：它更依赖训练分布与配对监督资源。
- 已核验来源：Zotero `P4E22T2E`；本地 PDF `D:\Desktop\2022_SGUIE_Net_Simple\SGUIE-Net_Semantic_Attention_Guided_Underwater_Image_Enhancement_With_Multi-Scale_Perception.pdf`

### 3.8 Histoformer

- 方法类别：深度水下增强
- 论文目标：通过学习目标直方图分布改善水下图像的颜色与对比度。
- 核心机制：使用 histogram-based transformer 学习高对比度、颜色校正图像的目标直方图分布，并结合 GAN 细化模块优化像素质量。
- 论文中可用的一句话定位：Histoformer 代表了基于直方图分布学习与 Transformer 建模的现代水下增强路线。
- 与本文的可比点：可支撑“全局统计分布建模”与“任务化结构融合”之间的对照。
- 不应误写的边界：它是通用水下增强模型，不是显微任务特化方法。
- 已核验来源：Zotero `V5H7FQTY`；本地 PDF `D:\Desktop\2024_Histoformer-main\Histoformer_Histogram-Based_Transformer_for_Efficient_Underwater_Image_Enhancement.pdf`

## 4. 扩展综述集：简版卡片

### 4.1 传统白平衡方法

- `MaxRGB`：假设白色表面会在至少一个通道达到最大响应，属于最大值拉伸式启发式白平衡。
- `Gray-World`：假设自然图像平均反射率接近中性灰，通过通道均值增益进行全局校正。
- `Shades of Gray`：可视为 Gray-World 的 Minkowski 范数推广，兼顾均值与最大值行为。
- `Gray-Edge`：用图像导数统计而非像素值估计光源颜色，代表边缘域白平衡假设。

写作作用：用于说明深度白平衡之前的经典颜色恒常假设脉络。当前可作为综述背景，不进入主实验表。

### 4.2 深度水下增强补全

- `WaterNet`：来自 *An Underwater Image Enhancement Benchmark Dataset and Beyond*，以多种预处理结果为输入，使用端到端网络进行融合，是 UIEB 体系中的代表性深度增强基线。
- `UWCNN`：来自 *Underwater Scene Prior Inspired Deep Underwater Image and Video Enhancement*，属于轻量 CNN 路线，强调结合水下场景先验和合成训练数据提升增强表现。

写作作用：用于把“深度水下增强”扩成更完整的历史链条。当前没有进入统一跑图结果，不写入主实验表。

### 4.3 传统水下增强补全

- `UDCP`：来自 *Transmission Estimation in Underwater Single Images*，通过蓝绿通道构造水下暗通道并估计 transmission，是早期经典物理先验方法之一。
- `IBLA`：通常指基于 image blurriness and light absorption 的水下恢复路线，代表通过模糊与吸收信息估计深度和退化强度的 IFM 型方法。
- `VRE`：当前只有方法简称，尚未在本地或 Zotero 中锁定唯一 canonical 题录。

写作作用：`UDCP` 与 `IBLA` 可用于补强“物理先验/恢复”一支；`VRE` 在锁定准确题录前不写入正文强结论。

## 5. 实验节可直接使用的“对比方法设置”段落

### 5.1 长版

为覆盖颜色校正、传统增强和深度增强三类代表性路线，本文当前采用 8 种外部方法作为正式对比对象，并按四类分组组织。第一类为深度白平衡方法，包括 HVDualformer 和 ABC-Former，这两种方法均不属于标准水下增强模型，但由于其在严重颜色偏移校正中的代表性，本文将其作为深度白平衡对比方法单列。第二类为传统或非深度水下增强方法，包括 GDCP、CBF、HLRP 和 WWPF，分别对应物理先验恢复、经典融合、优化建模和现代传统融合路线。第三类为深度水下增强方法，包括 SGUIE-Net 和 Histoformer，分别代表语义引导增强和直方图 Transformer 增强。当前统一跑图结果表明，除 WWPF 官方包仅稳定生成 496 张输出外，其余 7 种方法均在清洗后的 502 张输入集上生成完整结果。因此，正式公平的定量对比已经在 `496` 张 complete-case 子集上统一完成，并输出到 `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`，以避免不同方法使用不一致样本均值带来的偏差。对于 MaxRGB、Gray-World、Shades of Gray、Gray-Edge、WaterNet、UWCNN、UDCP 和 IBLA 等方法，本文当前仅将其作为 related work 的综述补全方法，而不纳入本轮主实验表。

在正式主表叙述中，WWPF 应继续保留为激进但可接受的强基线，因为其在当前协议下仍具有可写的竞争力；相对地，HLRP 与 Histoformer 虽保留数值，但由于在显微场景复现实验中出现明显偏色、过噪和结构失真，更适合作为失败案例或补充分析，而不是与稳健方法作同等层级的正向讨论。需要明确的是，这一判断仅针对当前 HAB 显微图像协议下的复现表现，不应写成对原论文方法在一般水下图像增强场景中的否定。

### 5.2 短版

本文当前外部正式对比方法共 8 种，分为深度白平衡方法 HVDualformer、ABC-Former，传统/非深度水下增强方法 GDCP、CBF、HLRP、WWPF，以及深度水下增强方法 SGUIE-Net、Histoformer。需要说明的是，前两者在任务属性上属于白平衡模型，因此在相关工作中不与标准水下增强方法混写。当前统一跑图结果中，除 WWPF 官方包仅稳定生成 496 张输出外，其余方法均覆盖 502 张输入，因此正式公平指标统计已经基于 `496` 张 complete-case 子集完成。

正式数值表保留全部方法，但正文主讨论建议保留 WWPF 作为强基线，同时将 HLRP 与 Histoformer 转入失败案例或补充分析。所有此类表述都应加上“在当前 HAB 显微图像协议下”的场景限定。

## 6. Related Work 中文成稿

### 6.1 主稿长度版本

水下图像增强旨在缓解由光吸收、散射和波长依赖衰减引起的颜色失真、低对比度和细节退化。早期研究主要围绕颜色补偿、多尺度融合和成像先验展开。除经典的颜色平衡与多尺度融合路线外，Transmission Estimation in Underwater Single Images 提出的水下暗通道先验、以及基于 image blurriness and light absorption 的恢复模型，分别代表了 transmission 估计和 IFM 型恢复思路。随后，Generalization of the Dark Channel Prior for Single Image Restoration 进一步推广了暗通道先验，Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors 则将 Retinex 变分建模与高阶反射率先验结合起来，Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion 进一步展示了现代传统融合路线在颜色校正、全局/局部对比增强与小波融合上的延展。总体而言，这类方法具有较强可解释性，但往往难以同时兼顾颜色稳定、局部可见性和任务相关结构表达。

围绕有害藻华显微图像这一更具体的应用场景，已有工作逐渐形成了从分解融合到颜色补偿再到白平衡引导融合的技术谱系。早期工作利用经验模态分解与小波融合提升藻类显微图像的纹理清晰度，随后又将循环颜色补偿与多尺度融合结合，并把增强结果与边缘检测、关键点匹配等下游任务联系起来。更近的工作进一步将自适应白平衡颜色补偿、注意力引导和金字塔融合整合到统一框架中，说明 HAB 显微增强不仅应关注主观视觉质量，还应服务于细胞边缘、纹理和形态结构的可辨识性。

随着深度学习的发展，水下增强开始更加重视高层语义和全局分布建模。WaterNet 通过多路预处理结果的端到端融合建立了基准数据集驱动的增强范式，UWCNN 则体现了结合水下场景先验和轻量 CNN 的早期深度增强路线。进一步地，SGUIE-Net 通过语义注意力和多尺度感知提升区域增强一致性，Histoformer 则使用直方图 Transformer 与生成式细化模块建模颜色和对比度的全局统计特征。这些方法在复杂退化场景下具有更强表达能力，但通常更依赖训练数据分布。

除直接面向水下增强的研究外，白平衡校正与颜色统计建模同样为严重偏色场景提供了重要启发。传统白平衡方法如 MaxRGB、Gray-World、Shades of Gray 和 Gray-Edge 代表了颜色恒常假设的经典谱系。近年来，ABC-Former 和 HVDualformer 等深度白平衡模型进一步表明，直方图表示、全局颜色统计和通道交互建模对于颜色偏移校正十分关键。虽然这些方法并非标准的水下增强模型，但它们为水下显微图像中的颜色补偿与白平衡设计提供了直接的可迁移思路。与现有工作相比，本文更关注将稳态前置白平衡、互补三分支增强、亮度域特征门控融合以及面向结构可读性的设计动机整合到同一条可复现实验主线中。

### 6.2 精简版

水下图像增强研究大致可归纳为四条相关脉络。第一类是传统增强与恢复方法，包括颜色补偿与多尺度融合、暗通道与 transmission 估计、以及 Retinex 变分优化等路线，代表方法包括 CBF、UDCP、GDCP、IBLA、HLRP 和 WWPF。第二类是面向 HAB 显微图像的任务化增强谱系，其特点是不只追求视觉改善，还强调边缘、纹理和形态结构的可辨识性。第三类是深度水下增强方法，从 WaterNet、UWCNN 到 SGUIE-Net 和 Histoformer，逐步从数据驱动融合发展到语义与直方图统计建模。第四类是白平衡与颜色统计建模方法，既包括 MaxRGB、Gray-World、Shades of Gray、Gray-Edge 等经典启发式，也包括 ABC-Former 和 HVDualformer 等深度白平衡模型。本文在相关工作中将后一类明确视作颜色校正参考，而不把其混写为标准水下增强方法。

## 7. 你当前评价的审校结论

下表中的“可保留”指可以保留为论文归纳或当前实验观察，“需收紧”指不能直接写成原论文定位或过强结论。

| 方法 | 你当前评价中可保留的部分 | 需收紧的部分 | 推荐写法 |
| --- | --- | --- | --- |
| HVDualformer | “深度学习直方图+视觉双 Transformer 白平衡”与原论文定位一致；“当前实验中偏色明显”可作为复现实验观察保留 | 不能把高 `MS-SSIM/PSNR` 直接写成“整体更优” | HVDualformer 属于深度白平衡方法，在当前协议下与原图结构一致性较强，但增强幅度有限，因此更适合作为保守颜色校正基线。 |
| ABC-Former | “深度白平衡、双模态直方图与通道交互注意力”与原论文定位一致；“当前视觉改善不明显”可作为当前观察 | 不能把最高 `MS-SSIM/PSNR` 写成“增强最好” | ABC-Former 是结合双模态颜色统计与通道交互建模的深度白平衡方法，在当前协议下与原图最接近，但实际增强收益有限。 |
| GDCP | “物理模型/广义暗通道先验”与原论文定位一致；“当前噪点偏重、色彩自然性不足”可作为当前观察 | 不宜写成“全面胜出”或“传统方法最优” | GDCP 代表物理先验恢复路线，在当前协议下具有中等增强强度和相对稳定的结构一致性，但综合增强收益仍弱于本文方法。 |
| CBF | “全局白平衡 + 多尺度融合”与原论文定位一致；“整体较稳”可保留 | 不宜把较高 `Entropy` 直接写成“质量更好” | CBF 属于经典融合增强方法，在当前协议下表现较均衡，可作为传统融合路线的稳健基线。 |
| HLRP | “Retinex 变分 + 超拉普拉斯反射率先验”与原论文定位一致；“当前存在明显失真/噪声放大”可作为实验观察 | 不能继续写成“整体稳定”；也不宜用“无意义”这种过满措辞 | HLRP 属于优化建模增强方法，但在当前显微图像复现实验中出现明显噪声放大、结构失真和极低结构一致性，更适合作为失败案例或补充分析；这一判断仅针对当前 HAB 显微图像协议，不等于否定原方法在其他水下场景中的价值。 |
| SGUIE-Net | “语义注意力 + 多尺度 U-Net”与原论文定位一致；“当前表现较强”可作为实验观察 | 不宜写成“深度方法全面优于本文” | SGUIE-Net 是语义引导的深度水下增强方法，在当前协议下结构一致性较稳，但对比提升和整体增强收益仍弱于本文方法。 |
| Histoformer | “Transformer + 直方图建模”与原论文定位一致；“当前存在明显偏色和噪声放大”可作为实验观察 | 不能写成“MS-SSIM 与 PSNR 过低无意义” | Histoformer 是基于直方图分布学习的深度增强方法。当前复现实验中无参考分数部分较高，但偏色、过噪和结构失真明显，更适合作为失败案例或补充分析；这一判断仅针对当前 HAB 显微图像协议，不等于否定原方法在其他水下场景中的价值。 |
| WWPF | “多阶段增强 + 小波融合”与原论文定位一致；“当前结果较激进”可作为实验观察 | 不能因为其在部分无参考指标上较高就从主表删除；也不能隐去 496 张实现边界 | WWPF 属于现代传统融合方法，在当前复现实验中应保留为激进但可接受的强基线。它在部分无参考指标上具有竞争力，但结构一致性弱于本文方法，因此更适合写成“强但更激进的对手”；这一判断同样只针对当前 HAB 显微图像协议。 |

## 8. 写作时必须遵守的边界

- 不把 `HVDualformer / ABC-Former` 混写成标准水下增强方法。
- 不把当前跑图观察写成原论文作者结论。
- 不使用“全面胜出”“无意义”这类过满判断。
- 不把 `VRE` 写成已核验方法，除非后续补上唯一 canonical 题录。
- 不隐去 `WWPF` 官方实现只稳定覆盖 496 张样本这一事实。
- 不把 `MS_SSIM/PSNR` 混写成“相对增强真值质量”的指标。
- 不因为 `WWPF` 在部分无参考指标上高于本文方法就把它从主表删掉。
- 不把 `HLRP` 与 `Histoformer` 继续写成和主表稳健方法同层级的正向强基线。
- 不把当前 HAB 显微图像协议下的复现实验观察，写成对原论文方法整体无效的结论。

## 9. 最小引用账本

### 9.1 核心已核验集

- `TEKJDF6M`：HVDualformer: Histogram-Vision Dual Transformer for White Balance
- `LF9HP7DR`：ABC-Former: Auxiliary Bimodal Cross-domain Transformer with Interactive Channel Attention for White Balance
- `V87JDUST`：Generalization of the Dark Channel Prior for Single Image Restoration
- `AFLVZ4KR`：Color Balance and Fusion for Underwater Image Enhancement
- `PWKRPBPJ`：Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors
- `U6DBLZMV`：Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion
- `P4E22T2E`：SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception
- `V5H7FQTY`：Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement

### 9.2 扩展综述集的当前来源状态

- `WaterNet`：已通过原始论文 *An Underwater Image Enhancement Benchmark Dataset and Beyond* 核验方法定位。
- `UWCNN`：已通过原始论文 *Underwater Scene Prior Inspired Deep Underwater Image and Video Enhancement* 核验方法定位。
- `UDCP`：已通过原始论文 *Transmission Estimation in Underwater Single Images* 核验方法定位。
- `IBLA`：已通过以 image blurriness and light absorption 为核心的原始论文路线核验方法定位。
- `VRE`：待补 exact title、作者与年份。
