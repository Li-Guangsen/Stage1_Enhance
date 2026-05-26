# 三份建议综合落实：Stage1 与 MyEdge 的跨项目定位

更新时间：2026-05-24

本文档把 `D:\Desktop\suggestion-1.md`、`D:\Desktop\suggestion-2.md`、`D:\Desktop\suggestion-3.md` 三份建议综合落到本仓库内。三份建议本身来自仓库外部，不能直接作为项目事实源；本文档只保留其中与本仓库正式口径、Zotero 已核验文献和当前结果相一致的策略判断。

## 1. 共同结论

三份建议的共同判断高度一致：

- 方向仍有继续做的价值。
- 最大风险不是当前结果完全不可用，而是“图像增强 + 边缘检测 pipeline”这一问题定义已经被同方向两篇一区 HAB / 赤潮论文高度覆盖。
- 总体论文不应写成“Stage1 增强方法 + MyEdge 边缘检测方法”的机械拼接。
- 更稳妥的定位是：以 MyEdge / MSFI 为主创新，Stage1 降级为 `task-driven structure-preserving input formation`，即面向边界任务的结构保持增强输入形成。
- Stage1 必须通过下游边缘验证证明它不是普通 preprocessing；在本仓库中，目前已有无 GT proxy 支撑包，但仍缺带 GT 的 MyEdge / DiffusionEdge 正式边缘指标闭环。

推荐总体定位：

`Spatial-frequency guided latent diffusion for boundary-aware edge detection in degraded harmful algal bloom microscopy, supported by task-driven structure-preserving enhancement.`

中文可写为：

`面向退化有害藻华显微图像的空间-频域扩散式边界感知边缘检测，并以任务驱动的结构保持增强作为输入支撑。`

## 2. 两篇核心参考论文的约束

两篇同方向师兄已发表一区论文已经通过 Zotero 核验：

| 论文 | 期刊 | Zotero key | 对当前项目的约束 |
| --- | --- | --- | --- |
| `Enhanced edge detection of harmful algal Blooms using diffusion probability models and Sobel-convolutional attention mechanisms` | `Expert Systems with Applications`, 2026, 298:129663 | `9MCJDQGE` / `AKGYHG77` | 已覆盖 HAB 图像增强 + 扩散边缘检测 + Sobel / attention 先验。当前总体论文不能再写成普通 enhancement-to-edge pipeline。 |
| `Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network` | `Engineering Applications of Artificial Intelligence`, 2026, 177:114948 | `ZMUBCGCD` | 已覆盖 task-oriented enhancement + downstream boundary-sensitive segmentation。当前若讲任务驱动增强，必须拿出 edge-specific 证据，而不能只借用 segmentation 论文的叙事。 |

已落地的本地文献笔记：

- `literature/wu2026_eswa_hab_edge_detection.md`
- `literature/wu2026_eaai_hab_segmentation.md`

## 3. 对 Stage1Codex 的落实

Stage1Codex 当前不应继续按“独立增强一区主论文”推进。它在总体工作中的角色应固定为：

`task-driven structure-preserving input formation`

也就是：

- 提供正式锁定的增强输入：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`
- 提供阶段级输入：`BPH`、`IMF1Ray`、`RGHS`、`CLAHE`、`Fused`、`Final`
- 提供外部增强方法输入与 complete-case 对照
- 提供无 GT Sobel/Otsu 边缘结构 proxy、候选 qualitative panels 和失败案例筛查入口
- 为 MyEdge 的带 GT 边缘检测评测提供固定输入、manifest 和结果解释边界

当前 Stage1 已完成：

- 正式增强主线锁定
- `full502_clean_v1` 阶段表
- `compare9_complete496_v1` 外部主比较表
- `official_full502_mainline` 无 GT 边缘结构 proxy 支撑包

当前 Stage1 仍缺：

- 人工确认后的 paper-ready 定性图组
- 数据采集条件、物种覆盖、公开性和运行资源说明
- 与 MyEdge 结果回流后的最终总体证据整合

## 4. 对 MyEdge 的落实

MyEdge 应成为总体论文的主创新承载项目。三份建议共同要求 MyEdge 把主问题从“改进 DiffusionEdge”改成：

`frequency-aware weak-boundary denoising in latent diffusion`

也就是围绕显微弱边界、断边、伪边缘和空间-频域信息恢复来组织贡献。

MyEdge 必须优先补的证据：

1. MSFI 组件消融：frequency token、spatial-frequency attention、timestep gating、插入位置。
2. 与 DiffusionEdge / Sobel-like prior / CIAFF-like block / CBAM / SE / generic Fourier filtering 的替换对比。
3. 固定 detector 的 Stage1 enhancement-to-edge 总表：`Original`、各 Stage1 阶段、`Final`、外部增强方法全部输入同一 detector。
4. ODS、OIS、AP、AC 之外的边缘结构指标：断边率、伪边缘率、edge thickness、skeleton continuity、boundary distance。
5. 低对比、弱边界、气泡/杂质、模糊边界子集分析。
6. PR 曲线和 AP trade-off 解释，不能回避 AP 下降或 AC 持平。
7. Params、FLOPs、FPS、显存、采样步数和失败案例。

## 5. 论文写作禁区

不能写：

- “先增强，再边缘检测”的普通 pipeline。
- “Stage1 + MyEdge 两套方法拼接成一篇论文”。
- “Stage1 已证明 ODS/OIS/AP/AC 提升”。
- “MSFI 全面优于现有 SOTA”，尤其当 AP 或 AC 不占优时。
- “白平衡 + CLAHE + IMF/USM + Laplacian pyramid fusion 是主创新”。
- “HLRP / Histoformer 原方法普遍无效”。
- “MS_SSIM / PSNR 是增强真值质量”。

推荐写：

- Stage1 是结构保持输入形成，不是普通视觉美化。
- 增强质量应通过边界可恢复性、伪边缘抑制和形态一致性检验。
- MyEdge 的主创新是 MSFI 对显微弱边界的空间-频域建模，而不是泛泛使用 diffusion 或 attention。
- 指标画像必须诚实：ODS/OIS、AP、AC 分别解释，不用“全面领先”遮盖 trade-off。

## 6. 投稿方向判断

三份建议对 ESWA / EAAI 的倾向略有差异，但可合并为下面的决策规则：

- 若近期只能完成 MyEdge / MSFI 的方法消融和边缘主表，优先按 ESWA 的 `intelligent boundary perception system` 叙事准备，但必须明显区别于 ESWA 参考论文的 SIAnet / Sobel / CIAFF 路线。
- 若能补齐工程证据，包括数据采集说明、运行资源、跨域或公共验证、下游分类/计数/形态测量价值，则 EAAI 更稳。
- 当前 Stage1Codex 本身不建议单独硬投 ESWA / EAAI；它更适合作为总体论文中的结构保持增强证据章节。

## 7. 下一步执行顺序

在 Stage1Codex 中：

1. 人工筛选 `metrics/outputs/downstream_edge_validation/official_full502_mainline` 下的候选 panel。
2. 补数据来源、采集条件、物种覆盖、公开性、运行时间和资源说明模板。
3. 把 Stage1 支撑包交给 MyEdge，作为固定输入和 manifest 合同。

在 MyEdgeCodex 中：

1. 建立 MSFI 组件消融计划。
2. 建立 Stage1 / generic enhancement / external methods 输入同一 detector 的正式评测协议。
3. 生成带 GT 的 ODS/OIS/AP/AC 与边缘结构指标总表。

在总体论文层面：

1. 以 MyEdge / MSFI 为主创新。
2. 将 Stage1 写成 `task-driven structure-preserving enhancement evidence`。
3. 以两篇同方向一区论文作为最近邻约束，主动说明差异，而不是回避。
