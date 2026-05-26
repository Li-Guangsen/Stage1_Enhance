# 水下图像增强论文证据包（中文）

更新时间：2026-04-24

说明：本证据包当前只把仓库内已版本化的本地文件、正式 manifest、正式结果表和本地可读草稿当作论文事实源。历史 Notion 页面、聊天历史、在线页面、个人记忆和未落盘事实均不作为当前事实来源；如需使用其中任何信息，必须先落到本仓库并重新核验。凡无法直接确认之处，均用 `[Inference]` 或 `[Missing]` 标明，不把推断写成事实。

当前中文主稿入口为 `paper/underwater_image_enhancement_draft_cn.md`，状态为中文投稿主稿 v1.0。该文件已从早期 `Part E / Part H` 双版本草稿收束为单一当前主稿；历史分版只作为 git 历史背景，不再作为当前写作入口。

## Part A. 资源访问情况

### A1. 本地工作区访问情况

- 已访问项目总览与论文草稿类文件：`README.md`、`method-underwater-enhancement-paper-ready.md`、`method-underwater-enhancement.md`、`method-figure-underwater-enhancement.md`、`related-work-underwater-enhancement.md`、`research-log.md`、`research-state.yaml`。[Local]
- 已访问核心实现文件：`main.py`、`lgsbph.py`、`pybemd.py`、`wb_safe_contrast.py`、`clahe_guided_visibility.py`、`fusion_three.py`、`lvbo.py`。[Local]
- 已访问关键配置与结果文件：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`、`experiments/h2-full506-direct/outputs/full506/eval/analysis.md`、`experiments/h2-full506-direct/outputs/full506/eval/selection.json`、`experiments/h1-graypixel-bph-ablation/outputs/full506/eval/summary.json`、`experiments/h1-graypixel-bph-ablation/outputs/full506/selection.json`、`metrics/score_protocol_v2.py`、`experiments/h1-graypixel-bph-ablation/analysis.md`、`metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502/summary.json`、`metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/summary.json`、`docs/project_status_overview_cn.md`、`docs/comparison_methods_results_index_cn.md`。[Local]
- 已访问 Stage1 enhancement-to-edge 支撑包：`docs/stage1_enhancement_to_edge_support_cn.md`、`metrics/scripts/run_downstream_edge_proxy_stage1.py`、`metrics/outputs/downstream_edge_validation/official_full502_mainline/index.md`、`stage_full502_proxy/summary.md`、`compare9_complete496_proxy/summary.md`。[Local]
- 已核对当前正式增强与正式评测环境口径：conda 根目录为 `D:\miniconda3`，正式增强与评测环境为 `D:\Desktop\EdgeDetection\my_env`；该环境已通过 `main.py + evaluate_protocol_v2.py` 的 smoke 验证。[Local]
- 已访问已有图示与图稿资产：`paper/figures/underwater_method_overview*.{mmd,svg,png}`，并新增生成 `paper/figures/fig_h1_h2_metric_summary.{png,svg}` 的脚本与输出。[Local]
- 已查看部分定性材料：H1 诊断对比图和 H2 当前主线输出图各至少 1 张，用于核对“有输出资产”这一事实，但当前尚未形成可直接进论文的精选定性图组。[Local]

### A2. 非仓库来源处理规则

- 历史 Notion 页面、聊天历史、在线页面和个人记忆不作为当前论文事实源。
- 本证据包早期版本中曾记录过 Notion 访问情况；这些记录仅能作为“历史访问痕迹”，不能直接支撑当前论文主张。
- 如果后续确实需要引用 Notion 或在线页面中的信息，必须先把对应事实同步到仓库内已版本化文件，再在本证据包中重新标注为 `[Local]`。

### A3. Zotero 访问情况

- 已成功访问 Zotero 集合：
  - `同方向师兄已发表`
  - `水下图像增强/同方向师兄`
  - `水下图像增强/对比方法`。[Zotero]
- 已核验两篇同方向一区 HAB / 赤潮核心参考：
  - ESWA 2026：`Enhanced edge detection of harmful algal Blooms using diffusion probability models and Sobel-convolutional attention mechanisms`，Zotero keys `9MCJDQGE` / `AKGYHG77`。[Zotero]
  - EAAI 2026：`Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network`，Zotero key `ZMUBCGCD`。[Zotero]
- 已成功获取并核验以下条目的元数据或摘要：`AFLVZ4KR`、`V87JDUST`、`PWKRPBPJ`、`U6DBLZMV`、`DQIVG34J`、`GS2RFTEL`、`LTE9U599`、`P4E22T2E`、`V5H7FQTY`、`LF9HP7DR`、`TEKJDF6M`。[Zotero]
- 已核验到至少 13 篇核心论文的 Zotero 条目或本地题录线索；正式投稿前仍应确保引用条目可从本地 `.bib`、Zotero 导出或论文 PDF 中复核。[Zotero]

### A4. 访问失败或受限情况

- `rg.exe` 在当前 shell 中因权限问题未能正常启动，因此文件检索改用 PowerShell 递归与定向读取完成；这不影响本地事实核验。[Local]
- Zotero 根集合 `水下图像增强` 的直接递归读取未返回条目，但其两个子集合 `同方向师兄` 与 `对比方法` 可正常访问，未影响文献核验。[Zotero]
- 当前未访问远端 GitHub 仓库，因此本轮没有使用 `[GitHub]` 证据标签。[Missing]
- 当前仅在扩展综述集上使用 Web 核验 `WaterNet/UWCNN/UDCP/IBLA` 的原始论文定位；核心 8 篇仍主要由 Zotero 与本地 PDF 核验。[Web][Zotero][Local]

### A5. 对论文真实性影响最大的潜在阻塞

- 无法直接从已访问文件中确认正式数据的采集协议、设备说明、物种覆盖和公开性状态；这会影响实验部分的可复现性与数据说明完整度。[Local][Missing]
- 当前已经形成 `official_stage_progress_full502` 的阶段进度表、`official_compare9_complete496` 的 `9` 方法 complete-case 主表，以及 `official_full502_mainline` 无 GT 边缘结构 proxy 支撑包，因此“统一增强指标总表”已不再是主要阻塞。当前真正影响投稿充分性的，是 MyEdge / DiffusionEdge 带 GT 下游边缘验证、人工确认后的投稿级总图和完整运行资源说明。[Local]
- 当前“面向下游边缘友好验证”的叙事已经有第一版无 GT 边缘结构 proxy 支撑包，但面向 MyEdge / DiffusionEdge 的 ODS/OIS/AP/AC 等带 GT 边缘检测结果仍未在已访问结果文件中显式出现。[Local][Missing]

### A6. 主张-证据-边界矩阵

| 主张类型 | 可写程度 | 当前证据 | 写作边界 |
| --- | --- | --- | --- |
| 正式主线已锁定 | 可作为正文事实 | `experiments/optimization_v1/configs/locked_full506_final_mainline.json` 与 `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline` | 不能把默认 `python main.py` 写成正式主线；正式重跑必须显式传锁定配置 |
| 阶段进度表已完成 | 可作为正文事实 | `metrics/manifests/full502_clean_v1.txt` 与 `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502/mean_metrics_table.md` | 这是 502 张清洁主集的阶段表，不是外部方法 complete-case 主表 |
| `Ours + 8 baselines` 主比较表已完成 | 可作为正文事实 | `metrics/manifests/compare9_complete496_v1.txt` 与 `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/mean_metrics_table.md` | 这是 496 张 complete-case 交集；`WWPF` 的 496 张实现边界必须写明 |
| 方法具有边缘友好设计动机 | 可谨慎写作 | 方法结构、HAB 显微图像任务定位、正式阶段结果 | 不能写成“已完整证明下游边缘任务提升”，因为正式下游边缘验证总表尚未形成 |
| 本方法视觉自然度全面最优 | 不可写 | 当前 Fusion 和外部主表均显示结构指标与视觉指标存在 trade-off | 不能写“所有指标最优”或“全面领先外部 SOTA” |
| `MS_SSIM` / `PSNR` 表示增强真值质量 | 不可写 | 当前协议以原图为参考计算这些指标 | 只能解释为增强结果相对原图的结构一致性或保守相似性 |
| `HLRP` / `Histoformer` 普遍无效 | 不可写 | 当前主表与观察只覆盖 HAB 显微图像协议 | 只能写成当前协议下的失败案例或补充分析，不能泛化否定原方法 |
| 中文主稿已收口为单一当前版本 | 可作为写作状态事实 | `paper/underwater_image_enhancement_draft_cn.md` | 只能说明已形成中文投稿底稿 v1.0，不能写成投稿终稿或实验闭环已完成 |
| Stage1 已形成 enhancement-to-edge 支撑包 | 可作为衔接事实 | `metrics/outputs/downstream_edge_validation/official_full502_mainline` 与 `docs/stage1_enhancement_to_edge_support_cn.md` | 这是无 GT Sobel/Otsu 边缘结构 proxy，不能替代 MyEdge 的 ODS/OIS/AP/AC |
| 三份建议已收束跨项目定位 | 可作为项目策略事实 | `docs/stage1_myedge_three_suggestions_synthesis_cn.md` | 这是策略与写作边界，不是新增实验结果；不能把建议中的未落盘实验设想写成已完成事实 |

## Part B. 研究信息证据表

### 1. 任务名称

- 内容：面向有害藻华水下显微图像的分阶段增强与论文准备。
- 来源：`README.md`、`research-state.yaml` 与本地方法草稿。[Local]
- 可信度：已确认
- 备注：`research-state.yaml` 的项目标题为 “HAB Microscopic Image Enhancement and Edge-Detection-Oriented Validation”。[Local]

### 2. 研究目标

- 内容：在缓解颜色偏移、低对比度、细节模糊和照明不均匀的同时，提高结构可辨识性，并尽量服务于边缘敏感的下游分析。
- 来源：`method-underwater-enhancement*.md`、`research-state.yaml`、`docs/project_status_overview_cn.md`。[Local]
- 可信度：已确认
- 备注：当前最稳妥的表述是“结构可读性与边缘友好设计动机”，不宜直接写成“已完整证明下游边缘任务显著提升”。[Local][Inference]

### 3. 应用场景

- 内容：水下有害藻华（HAB）显微图像增强。
- 来源：`README.md`、`research-state.yaml`、本地 method/related work 草稿、多篇 HAB 方向 Zotero 文献。[Local][Zotero]
- 可信度：已确认
- 备注：从命名与文献脉络看，项目定位明显偏向显微图像而非一般水下自然场景照片。[Local][Zotero]

### 4. 主要问题与痛点

- 内容：颜色偏移、通道失衡、局部低对比度、细节模糊、照明不均匀，以及增强结果对结构真实性和下游边缘可读性的影响。
- 来源：本地 method/related work 草稿、Zotero 中传统/深度水下增强文献摘要。[Local][Zotero]
- 可信度：已确认
- 备注：痛点描述与水下散射/吸收的一般叙事一致，但本项目更强调显微结构和边缘可辨识性。[Zotero][Inference]

### 5. 方法总体框架

- 内容：`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`；其中论文叙事更适合将 `Final` 之后的边缘友好验证视为外部任务化评估路径，而非增强算子本体。
- 来源：`main.py`、`README.md`、`method-figure-underwater-enhancement.md`、`docs/project_handoff_guide_cn.md`。[Local]
- 可信度：已确认
- 备注：代码层的实际“增强算子”是输入后的六个操作阶段；下游验证只能作为外部任务化评估规划，不属于当前增强算子本体。[Local]

### 6. 核心模块

- 内容：
  - `BPH`：灰像素引导预白平衡 + clipped ACCC + 亮度回调
  - `IMF1Ray`：EMD 提 IMF1 + 高频/边缘增强 + Rayleigh 匹配
  - `RGHS`：历史名保留，真实功能为白平衡安全对比增强
  - `CLAHE`：历史名保留，真实功能为 CLAHE 引导的局部可见性增强
  - `Fused`：亮度域特征门控三分支融合
  - `Final`：同态与熵增强式收口。[Local]
- 来源：对应代码文件头说明、函数注释和本地 method 草稿。[Local]
- 可信度：已确认
- 备注：`RGHS` 和 `CLAHE` 不能在论文中被写成“标准 RGHS 模块”和“普通 CLAHE 输出”。[Local]

### 7. 输入与输出

- 内容：输入为单幅彩色水下图像，统一来自 `data/inputImg/Original`。当前正式阶段进度评测使用 `metrics/manifests/full502_clean_v1.txt` 中的 `502` 张清洁样本，正式外部主比较使用 `metrics/manifests/compare9_complete496_v1.txt` 中的 `496` 张 complete-case 样本；输出为六阶段增强结果，其中 `Final` 的正式结果入口为 `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`。
- 来源：`main.py`、`summary.json`、`selection.json`。[Local]
- 可信度：已确认
- 备注：当前主流程默认将输入 resize 到 `320x320`，除非显式传 `--no-resize`。配置名保留 `full506` 只是历史锁定背景，不代表当前论文正式主表仍采用 `506` 口径。[Local]

### 8. 训练策略 / 参数化策略 / 调参方式

- 内容：无监督、无训练；主要通过阶段化参数搜索与顺序锁定完成。
  - H1：白平衡候选搜索与人工锁定
  - H2：固定上游后依次锁定 `RGHS -> CLAHE -> Fusion`
  - H3：此前完成后处理/收口搜索，当前主线采用 `r4_03` 的 `homomorphic_entropy` 收口。[Local]
- 来源：`research-log.md`、`research-state.yaml`、`selection.json`、`analysis.md`。[Local]
- 可信度：已确认
- 备注：当前综合分脚本 `metrics/score_protocol_v2.py` 用于内部调参与排序，不宜直接作为论文主结果指标叙事。[Local][Inference]

### 9. 损失函数

- 内容：不存在训练损失函数；当前工作是传统/混合增强管线调参与评测。
- 来源：代码与实验组织文件均未出现训练循环或损失定义。[Local]
- 可信度：已确认
- 备注：若后续加入深度下游验证网络，应另行区分增强方法与下游模型训练设置。[Inference]

### 10. 推理流程

- 内容：原图先经 `BPH` 归一化，再从 `bph_bgr` 并行生成 `IMF1Ray`、`RGHS`、`CLAHE` 三路结果；`fusion_three.py` 仅融合三路分支得到 `Fused`；`_final_refine` 根据 `final.mode` 生成 `Final`。
- 来源：`main.py` 的 `process_one_image()` 与 `_final_refine()`。[Local]
- 可信度：已确认
- 备注：当前默认 `imf1ray` 会先以 `aggressive=True` 起步，再叠加 JSON 覆写。[Local]

### 11. 数据来源或数据集

- 内容：当前正式评测数据分为两层：`full502-clean-v1` 来自 `metrics/manifests/full502_clean_v1.txt`，包含 `502` 张清洁样本；`compare9-complete496-v1` 来自 `metrics/manifests/compare9_complete496_v1.txt`，包含 `496` 张 complete-case 样本。历史上还存在 `pilot92-v1` 子集，以及用于候选搜索和锁定的 `full506` 资产。
- 来源：`research-state.yaml`、`summary.json`、`README.md`。[Local]
- 可信度：已确认
- 备注：正式论文写作应以 `full502` 阶段表和 `496` 主比较表为当前口径；数据采集设备、采样时间、物种分布、是否公开等信息在本轮已访问资料中仍缺失。[Missing]

### 12. 评价指标

- 内容：当前仓库中实际计算过的指标包括 `EME`、`EMEE`、`Entropy`、`Contrast`、`AvgGra`、`SIFT_KP`、`MS_SSIM`、`PSNR`、`UCIQE`、`UIQM`；其中 H2 后期已明确不再将 `SIFT_KP` 作为当前主线收口后的常规评测项。在当前正式写作中，`MS_SSIM` 与 `PSNR` 均以原始输入图像为参考计算，更适合解释为增强结果相对原图的结构一致性，而不是相对增强真值的质量指标。
- 来源：`summary.json`、`metrics/score_protocol_v2.py`、`README.md`、`analysis.md`。[Local]
- 可信度：已确认
- 备注：从项目状态看，当前更强调结构相关指标（如 `MS_SSIM`、`PSNR`、`AvgGra`）与视觉指标的平衡，而不是单一无参考分数；其中 `MS_SSIM/PSNR` 的推荐解释是“与原图的结构一致性”。[Local][Inference]

### 13. 对比方法

- 内容：
  - 已确认的代码级对比主要是内部基线与阶段候选：
    - H1：`r2_00_baseline`、`r2_02_G_P`、`r2_05_G_P_A_B`、`r2_08_G_P_A2_B`
    - H2：`RGHS/CLAHE/Fusion` 各阶段候选与 `full506_locked_mainline` 的对比
  - 文献级外部方法当前已完成 `8` 个统一跑图结果：`HVDualformer`、`ABC-Former`、`GDCP`、`CBF`、`HLRP`、`SGUIE-Net`、`Histoformer`、`WWPF`；并已与 `Ours` 一起形成 `official_compare9_complete496` 的 `9` 方法 complete-case 主表。其中前 `7` 种外部方法覆盖 `502` 张清洗后输入，`WWPF` 官方包覆盖 `496` 张。[Local][Zotero]
- 来源：`summary.json`、`selection.json`、`related-work-underwater-enhancement.md`。[Local][Zotero]
- 可信度：已确认
- 备注：当前可以写成“已完成统一跑图与 `496` complete-case 总表”，但不能写成“已完成下游验证与投稿级完整图组”。正式主表数值应保留全部 `9` 方法；正文叙述层面则建议保留 WWPF 作为激进但可接受的强基线，同时把 HLRP 与 Histoformer 作为失败案例或补充分析处理。所有这类判断都应限定在当前 HAB 显微图像协议下，而不能写成对原论文方法整体有效性的否定。[Local][Missing]

### 14. 消融实验

- 内容：
  - H1：验证前置白平衡候选
  - H2：验证在固定上游前提下的 `RGHS -> CLAHE -> Fusion` 顺序优化
  - H3：已有后处理/收口搜索，但当前 paper-ready 结果更像主线锁定的背景，而不是一套完整独立章节。[Local]
- 来源：`research-log.md`、`README.md`、`research-state.yaml`。[Local]
- 可信度：已确认
- 备注：当前最完整、最适合写入论文的消融证据是 H1 与 H2；H3 可作为补充小节，但不宜写成主要创新验证。[Inference]

### 15. 定性结果

- 内容：仓库中存在 H1 诊断 comparison/edge/sheet 图，以及 H2 当前主线全部阶段输出；本地分析与日志记录过人工抽看结论。
- 来源：`experiments/h1-graypixel-bph-ablation/analysis.md`、本地诊断图目录、`research-log.md`。[Local]
- 可信度：高概率推断
- 备注：当前尚未看到已整理成论文版的代表性 qualitative panel，因此正文里只能谨慎写“已有诊断图支持人工复查”，不能写“系统性定性优势已完整展示”。[Missing]

### 16. 定量结果

- 内容：
  - H1：人工最终锁定 `r2_05_G_P_A_B`，相对 baseline 提升 `MS-SSIM +0.001028`、`PSNR +0.031596 dB`
  - H2：当前接受 `RGHS=rghs_s07`、`CLAHE=clahe_s05`、`Fusion=fusion_s10`
  - `fusion_s10` 相对 locked mainline 在 `MS_SSIM +0.06751`、`PSNR +1.43617 dB` 上提升明显，但 `UCIQE -0.62345`、`UIQM -5.03317` 回撤显著
  - 当前已形成 `official_stage_progress_full502` 的六阶段阶段表，以及 `official_compare9_complete496` 的 `9` 方法 complete-case 主表，可作为论文正式数值引用入口。[Local]
- 来源：H1 `summary.json` / `selection.json`，H2 `selection.json` / `analysis.md`。[Local]
- 可信度：已确认
- 备注：这一组结果很适合支撑“结构指标提升与视觉指标回撤并存”的克制讨论。对外部方法的推荐解读是：HVDualformer/ABC-Former 代表保守白平衡，GDCP/CBF/SGUIE-Net 代表中等增强强度，WWPF 代表激进但可接受的强基线，而 HLRP/Histoformer 更适合作为失真失败案例讨论。这里的“失败案例”仅指它们在当前 HAB 显微图像协议下的复现表现，不等于否定原方法在其他水下场景中的价值。[Local]

### 17. 可能创新点

- 内容：
  1. 灰像素引导预白平衡与 clipped ACCC 的稳态入口设计
  2. 面向职责分离的三分支结构：细节、对比、局部可见性
  3. 亮度域特征门控 + 拉普拉斯金字塔融合 + `RGHS` 色彩锚定
  4. 面向 HAB 显微场景的阶段化证据组织与边缘友好定位。[Local][Inference]
- 来源：代码实现、本地 method 草稿、研究状态总结。[Local]
- 可信度：前 3 项已确认；第 4 项为高概率推断
- 备注：最稳妥的写法是“结构化整合创新”而不是“单算子理论突破”。[Inference]

### 18. 当前证据不足处

- 内容：
  - 已有面向当前锁定主线的无 GT 边缘结构 proxy 支撑包，但缺少 MyEdge / DiffusionEdge 带 GT 下游边缘验证表
  - 缺少数据采集与公开性说明
  - 已生成自动候选定性图组和失败案例候选，但缺少人工确认后的投稿级定性图组、失败案例与完整运行资源说明
  - 缺少对正式主表结果的投稿级图示化呈现与讨论收束。[Local][Missing]
- 来源：已访问本地结果与 Zotero 题录；Zotero 仅提供文献而非复现实验。[Local][Zotero]
- 可信度：已确认
- 备注：这些缺口决定了当前稿件更适合“可继续打磨投稿的初稿”，而不是直接终稿。[Inference]

### 19. 不应过度声称的部分

- 内容：
  - 不应声称对外部 SOTA 已全面领先
  - 不应把 `Final` 收口层写成主要创新
  - 不应把 `RGHS`/`CLAHE` 历史名当作真实算法名
  - 不应把“边缘友好”直接写成已充分完成的下游任务增益结论
  - 不应把 `MS_SSIM/PSNR` 写成“相对增强真值质量”的结论性指标
  - 不应因为 WWPF 在部分无参考指标上较高就将其从主表删除
  - 不应把 HLRP 与 Histoformer 继续写成“稳健强基线”
  - 不应把当前 HAB 显微图像协议下的负面复现结果，写成对原论文方法普遍无效的否定性结论。[Local][Missing]
- 来源：代码职责、本地文档、研究状态里的 evidence gap。[Local]
- 可信度：已确认
- 备注：这些边界正是本稿需要主动克制的地方。[Inference]

### 20. 投稿最关键但目前缺失的信息

- 内容：
  1. 数据来源、采样条件和公开性说明
  2. 现主线下游边缘验证的正式结果
  3. 代表性定性可视化和失败案例
  4. 运行时间/资源开销说明
  5. 与当前 `9` 方法主表相配套的投稿级图示、排序解释与讨论收束。[Missing]
- 来源：本轮本地访问范围内均未见完整定稿版证据。[Local]
- 可信度：已确认
- 备注：如果目标期刊是 IEEE TIP / TCSVT / PR，这几项里至少前 3 项需要显著补强。[Inference]

## Appendix 1. Verified Reference Ledger

以下文献均已在 Zotero 中核验到题录；来源类型默认均为 `[Zotero]`。

1. `Color Balance and Fusion for Underwater Image Enhancement`
   - 作者：Codruta O. Ancuti, Cosmin Ancuti, Christophe De Vleeschouwer, Philippe Bekaert
   - 年份：2018
   - Zotero Key：`AFLVZ4KR`
   - DOI：`10.1109/TIP.2017.2759252`
   - 用途：经典传统融合基线；支撑“颜色补偿 + 多尺度融合”脉络。

2. `Generalization of the Dark Channel Prior for Single Image Restoration`
   - 作者：Yan-Tsung Peng, Keming Cao, Pamela C. Cosman
   - 年份：2018
   - Zotero Key：`V87JDUST`
   - DOI：`10.1109/TIP.2018.2813092`
   - 用途：支撑物理先验/成像模型恢复路线。

3. `Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors`
   - 作者：Peixian Zhuang, Jiamin Wu, Fatih Porikli, Chongyi Li
   - 年份：2022
   - Zotero Key：`PWKRPBPJ`
   - DOI：`10.1109/TIP.2022.3196546`
   - 用途：支撑 Retinex/优化建模路线。

4. `Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion`
   - 作者：Weidong Zhang 等
   - 年份：2024
   - Zotero Key：`U6DBLZMV`
   - DOI：`10.1109/TCSVT.2023.3299314`
   - 用途：现代传统融合基线参考。

5. `Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion`
   - 作者：Geng-Kun Wu, Bei-Ping Zhang, Jie Xu
   - 年份：2023
   - Zotero Key：`DQIVG34J`
   - DOI：`10.1007/s10489-023-04502-x`
   - 用途：支撑 HAB 显微方向中的 EMD/小波谱系，与当前 IMF1 分支的研究血缘相关。

6. `Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion`
   - 作者：Geng-Kun Wu, Jie Xu, Yi-Dan Zhang, Bei-Ping Zhang
   - 年份：2023
   - Zotero Key：`GS2RFTEL`
   - DOI：`10.1007/s11042-023-16258-0`
   - 用途：支撑 HAB 显微方向中的循环颜色补偿与多尺度融合脉络。

7. `Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy`
   - 作者：Yi-Ning Fan 等
   - 年份：2025
   - Zotero Key：`LTE9U599`
   - DOI：`10.1016/j.imavis.2025.105466`
   - 用途：当前项目最接近的公开结构参考，用于说明场景定位与差异化边界。

8. `SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception`
   - 作者：Qi Qi 等
   - 年份：2022
   - Zotero Key：`P4E22T2E`
   - DOI：`10.1109/TIP.2022.3216208`
   - 用途：深度学习增强代表，用于说明语义引导路线。

9. `Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement`
   - 作者：Yan-Tsung Peng 等
   - 年份：2025
   - Zotero Key：`V5H7FQTY`
   - DOI：`10.1109/JOE.2024.3474919`
   - 用途：Transformer/直方图建模代表，用于说明全局统计建模路线。

10. `ABC-Former: Auxiliary Bimodal Cross-domain Transformer with Interactive Channel Attention for White Balance`
    - 作者：Yu-Cheng Chiu 等
    - 年份：2025
    - Zotero Key：`LF9HP7DR`
    - DOI：`10.1109/CVPR52734.2025.01980`
    - 用途：白平衡与颜色分布建模参考；不宜写成标准水下增强基线。

11. `HVDualformer: Histogram-Vision Dual Transformer for White Balance`
    - 作者：Yan-Tsung Peng, Guan-Rong Chen
    - 年份：2025
    - Zotero Key：`TEKJDF6M`
    - DOI：`10.1609/aaai.v39i6.32697`
    - 用途：白平衡与 histogram-vision dual transformer 参考；用于支撑颜色建模论述。

## Part C. 论文定位与创新点提炼

### C1. 最合适的论文类型定位

最稳妥的定位不是“理论性重大突破”，而是：

`分阶段增强框架型 + 结构/分支职责分离型 + 特征门控融合型 + 面向 HAB 显微场景的工程整合型`

更具体地说：

- 论文主轴应写成：面向 HAB 水下显微图像的阶段化增强框架。[Local]
- 方法辨识度主要来自：职责化三分支和亮度域特征门控融合，而不是单独某个现成模块。[Local]
- “任务导向”可以写，但要克制；当前更适合表述为“面向边缘敏感分析的设计动机”，而不是“已完成大规模下游任务证明”。[Local][Missing]

### C2. 2-4 个最稳妥的贡献点

#### 直接证据支持的贡献

1. 提出一套面向 HAB 显微图像的阶段化增强框架，将前置白平衡、细节恢复、主体对比、局部可见性、特征门控融合和轻量收口串成可复现实验主线。[Local]
2. 设计了职责明确的三分支中间表示，并在亮度空间中通过特征门控与拉普拉斯金字塔完成结构融合，同时保留对比分支作为色彩锚点。[Local]
3. 建立了围绕 `full506` 的阶段化证据组织：H1 锁定前置白平衡，H2 顺序锁定 `RGHS/CLAHE/Fusion`，并明确暴露结构指标与视觉指标之间的真实权衡。[Local]

#### 可以谨慎表述的贡献

4. 方法面向边缘敏感的显微分析任务进行了设计取向上的适配，增强目标不只停留在主观观感，而是尽量服务于结构可读性。[Local][Inference]

### C3. 哪些内容可写成贡献

- `BPH` 不是普通 ACCC 的直接搬运，而是灰像素引导 + clipped ACCC + brightness restore 的稳态入口。[Local]
- `Fused` 不是均值混合，而是特征门控、多尺度、带色彩锚点的职责融合层。[Local]
- 当前实验过程强调“阶段依赖关系已锁定并可追溯”，这可以写成工程与复现实证优势，而非理论贡献。[Local]

### C4. 哪些内容只能写成实现细节或工程优势

- `Final` 里的同态 + 熵增强收口只能写成稳定输出的后处理设计，不宜升格为主要创新点。[Local]
- `imf1ray.aggressive=true`、具体 percentiles、clip limits、tile size 等更多属于配置实现细节。[Local]
- 现有 composite score 与 guardrail 机制更适合写成调参/筛选策略，而不是方法学核心贡献。[Local]

### C5. 审稿人最可能质疑什么

1. 与 2023/2025 的 HAB 方向前序工作相比，新意是否足够独立？[Zotero]
2. 既然外部方法主表已经形成，为什么当前仍缺少投稿级对比图组、排序解释和下游验证总表？[Local][Missing]
3. “边缘友好/任务导向”的说法是否已有足够下游实验支撑？[Missing]
4. `Fusion` 虽然提升结构指标，但 UCIQE/UIQM 明显回撤，是否意味着方法在视觉自然度上存在副作用？[Local]
5. 数据集是否公开、采集条件如何、是否具有期刊层面的可复现性？[Missing]

### C6. 应规避的夸张表述

- 避免写“显著优于现有方法”或“达到 SOTA”。[Missing]
- 避免写“本文提出全新的 RGHS/CLAHE 算法”。[Local]
- 避免把 `Final` 写成“关键创新模块”。[Local]
- 避免把“结构指标提升”直接等同于“下游边缘任务大幅提升”。[Inference]

## Part D. 中文论文大纲

### D1. 题目备选

1. 面向有害藻华水下显微图像的分阶段增强框架与结构化融合方法
2. 一种面向 HAB 水下显微图像的职责化三分支增强与特征门控融合方法
3. 面向边缘敏感分析的水下显微图像增强：前置白平衡、互补分支与结构化融合

### D2. 摘要写作要点

- 先交代场景：HAB 水下显微图像存在偏色、低对比度和结构可读性不足。
- 明确本文不是单算子增强，而是阶段化框架。
- 摘出 3 个最核心模块：稳态前置白平衡、职责化三分支、特征门控融合。
- 实验描述坚持事实：基于历史 `full506` 锁定证据与当前 `full502_clean_v1` / `compare9_complete496_v1` 正式口径完成阶段化和主比较证据，不虚构外部 benchmark 排名。
- 结尾写真实边界：当前结果支持结构指标改善与论文叙事，但投稿级图组、下游验证和数据/资源说明仍待补强。

### D3. 关键词

- 水下图像增强
- 有害藻华显微图像
- 白平衡校正
- 多分支融合
- 特征门控
- 结构可读性

### D4. 章节设计

#### 1 引言

- 写作目标：从场景问题出发，收束到“为什么单一增强算子不足，为什么需要职责化框架”。
- 主要证据依赖：本地 method/related work 草稿、HAB 方向 Zotero 文献。[Local][Zotero]
- 可直接落笔的内容：场景问题、传统方法局限、项目主线结构。
- 需谨慎措辞的内容：下游任务收益。
- 待补充项：若投稿时已补强下游实验，可在引言尾部再抬高任务导向比重。

#### 2 相关工作

- 写作目标：构造“传统水下增强 -> HAB 显微方向 -> 深度/Transformer -> 白平衡建模借鉴”的四段结构。
- 主要证据依赖：Zotero 核验账本、本地 related work 草稿与对比方法包。[Local][Zotero]
- 可直接落笔的内容：11 篇已核验文献的分组与用途。
- 需谨慎措辞的内容：不要把白平衡论文写成直接对比基线。
- 待补充项：若后续新增文献，可扩展近两年 Transformer 方向。

#### 3 方法

- 写作目标：按真实调用链和模块职责讲清楚“为什么这么拆、每条分支负责什么、如何融合、收口层怎么定位”。
- 主要证据依赖：`main.py` 与 6 个模块文件、method 草稿、方法图说明。[Local]
- 可直接落笔的内容：BPH、IMF1Ray、RGHS、CLAHE、Fused、Final。
- 需谨慎措辞的内容：避免把历史命名误当算法名。
- 待补充项：若后续需要公式，可从代码与原理再补公式化表达。

#### 4 实验

- 写作目标：如实呈现当前内部证据，说明 H1/H2 的结论、优点和 trade-off。
- 主要证据依赖：H1/H2 结果文件、`score_protocol_v2.py`、新增数据图。[Local]
- 可直接落笔的内容：历史 `full506` 搜索背景、`320x320` 设置、H1/H2 结果、Fusion trade-off。
- 需谨慎措辞的内容：external SOTA comparison、下游边缘验证。
- 待补充项：数据来源描述、外部基线、定性图组。

#### 5 讨论与局限性

- 写作目标：主动说明方法边界、指标权衡和实验缺口，降低审稿人反感。
- 主要证据依赖：H2 `fusion_s10` 的视觉项回撤、research-state 中的 evidence gaps。[Local]
- 可直接落笔的内容：内部指标与视觉指标不总一致，当前更像场景化工程整合。
- 需谨慎措辞的内容：泛化能力与公开数据结论。
- 待补充项：若后续加上更广泛数据，再扩展泛化讨论。

#### 6 结论

- 写作目标：收束为“提出了一套真实可复现的阶段化框架，并通过当前证据显示其有写成论文的价值，但仍有明确后续补强方向”。
- 主要证据依赖：Part B 与 Part F 风险清单。[Local][Inference]
- 可直接落笔的内容：框架总结与最重要的实证观察。
- 需谨慎措辞的内容：避免使用绝对化结论。
- 待补充项：投稿前可加入未来工作与扩展方向。

## Part F. 审稿人视角风险清单

### F1. 创新性风险

1. 与 `GS2RFTEL` 和 `LTE9U599` 同属 HAB 显微增强谱系，若正文只写“白平衡 + 融合 + 下游友好”，审稿人可能认为增量不够清晰。[Zotero][Local]
2. 如果不明确区分“历史命名”和“当前真实实现”，`RGHS` 与 `CLAHE` 会让人误判为现成模块拼接。[Local]

### F2. 实验充分性风险

1. 当前最扎实的仍是内部消融与锁定流程；虽然外部方法已完成统一跑图，并且 `496` complete-case 总表已经形成，但面向外部强基线的投稿级图组与讨论收束仍缺失。[Local][Missing]
2. `fusion_s10` 的结构指标收益伴随 UCIQE/UIQM 回撤，若不主动解释，会被质疑为“为某些指标过拟合”。[Local]
3. “边缘友好”叙事当前仍缺少与本轮锁定主线严格对齐的正式下游验证表。[Missing]

### F3. 写作逻辑风险

1. 项目层七阶段叙事和增强算子本体六阶段叙事容易混淆；若不统一，会导致方法图、方法节和实验节自相矛盾。[Local]
2. 内部 composite score 容易误导读者；如果不说明它只是调参工具，会削弱实验可信度。[Local]

### F4. 可复现性风险

1. `full506` 数据的来源、采样条件、公开性、标注状态在当前访问材料中仍未完整说明。[Missing]
2. 当前 repo 的默认 `main.py` 参数并不是接受主线，需要显式传 `locked_full506_final_mainline.json`；若正文不写清楚，复现实验会跑偏。[Local]
3. 当前正式增强与正式评测环境已经集中注明，并已通过 smoke 验证；但历史脚本环境、图表脚本环境和全仓统一依赖说明仍未完全收口。[Local][Missing]

## Part G. 修订说明

本轮根据审稿人视角，对中文主稿拟做如下修订：

1. 降低“任务导向/边缘友好”的声量，把它改写为设计动机与待补强方向，而不是已经完整闭合的主结论。
2. 明确区分“增强算子六阶段”和“项目级七阶段叙事”，避免结构自相矛盾。
3. 在实验部分直接写出 `fusion_s10` 的正负两面结果，不把它包装成无条件最优。
4. 将 internal composite score 从“结果结论”降级为“调参与筛选工具”。
5. 在讨论与局限性中提前承认外部强基线、下游验证和数据说明的缺口。
6. 对语言做一轮去模板化处理，删掉空泛的“显著”“充分证明”等套话。

## Part I. 投稿前待补充清单

### I1. 缺失实验

- 与 `AFLVZ4KR`、`V87JDUST`、`PWKRPBPJ`、`U6DBLZMV`、`P4E22T2E`、`V5H7FQTY` 以及深度白平衡方法 `LF9HP7DR`、`TEKJDF6M` 的投稿级结果图、排序解释与讨论收束。[Zotero][Missing]
- 面向当前锁定主线的下游边缘检测 / 关键点 / 结构任务验证表。[Missing]
- `Final` 模块单独增益的清晰消融表（尤其是 `homomorphic`、`entropy`、`homomorphic_entropy` 的对比）。[Local][Missing]

### I2. 缺失图表

- 代表性 qualitative panel：原图、BPH、三分支、Fused、Final、失败案例各 2-4 组。[Local][Missing]
- 外部方法主比较图组与当前内部消融总表的投稿级可视化版本。[Missing]
- 数据来源与实验流程示意图（若投稿期刊更看重 reproducibility，可单独补一张 protocol 图）。[Missing]

### I3. 缺失文献

- 当前 Zotero 已足够支撑初稿，但若投稿前要抬高“现代方法对比”，仍建议补 2024-2026 更靠近水下显微或任务导向增强的新文献。[Inference]

### I4. 缺失实现细节

- 数据采集条件、设备、是否公开、是否允许随稿共享。[Missing]
- 图表脚本环境、全仓统一依赖、耗时、硬件、单张/全量处理成本。[Missing]
- 是否所有实验都固定了 `320x320` resize，以及该设置对结果的影响。[Local][Missing]

### I5. 建议补做的消融

- 去掉 `BPH` 后三分支是否仍稳定。
- 去掉 `RGHS` 色彩锚点，仅做亮度混合是否会加剧偏色。
- 去掉 `clahe_floor_mid/high` 后是否出现中频补偿被吞的问题。
- `imf1ray` 的 `aggressive` 与非 aggressive 版本对结构/噪声权衡的影响。[Local][Inference]

### I6. 建议补做的强基线

- 经典传统：Ancuti 2018、Peng 2018、Zhuang 2022、Zhang 2024。[Zotero]
- 深度/Transformer：SGUIE-Net、Histoformer。[Zotero]
- 若白平衡作为辅助论据：ABC-Former、HVDualformer 用于 related work，不一定必须做复现。[Zotero][Inference]

### I7. 建议人工确认的关键点

- `full506` 数据是否可以在论文中公开描述，还是只能写成自建私有数据。
- 当前投稿目标期刊到底是 TIP、TCSVT、PR，还是先走相近中文/英文过渡投稿。
- 是否继续沿用 `fusion_s10` 作为最终主线，还是先按视觉护栏再重开一轮 Fusion。
- 是否需要把已有 method figure 再升级为包含中间缩略图的主图版本。[Local]

### I8. 目前只能谨慎表述的结论

- “方法对下游边缘任务有明确提升”只能写成设计目标与待补实验方向，不能写成已完全闭合结论。[Missing]
- “方法在视觉质量上全面更优”不能成立，因为 `fusion_s10` 的 UCIQE/UIQM 有明显回撤。[Local]
- “方法优于现有公开方法”目前缺少复现实验支撑，不能写。[Missing]
