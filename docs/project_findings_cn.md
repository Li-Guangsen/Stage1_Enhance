# 项目关键发现（中文）

更新时间：2026-04-24

本文档替代根目录旧版 `findings.md`。旧版英文文件是 2026-04-11 初始化 autoresearch 工作区时生成的早期快照，内容已归档到 `docs/archive-en/findings.en.md`，不再作为当前状态来源。

## 1. 当前研究问题

本项目研究对象是有害藻华水下显微图像增强。当前问题不是一般自然场景水下增强，而是如何在颜色恢复、细节可见性、结构稳定性和后续边缘敏感分析之间取得可复现、可写入论文的平衡。

## 2. 当前最重要发现

- 当前项目已经形成正式增强主线，不再是松散滤波器集合。
- 正式主线为 `Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`。
- 当前唯一正式配置是 `experiments/optimization_v1/configs/locked_full506_final_mainline.json`。
- 当前正式结果副本是 `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`。
- 当前正式阶段表使用 `full502_clean_v1`，正式外部主比较表使用 `compare9_complete496_v1`。
- `full506` 现在只表示历史搜索和锁定背景，不再是正式论文主表口径。

## 3. 方法层关键判断

- 最稳妥的论文定位是“面向 HAB 显微图像的分阶段增强框架”，不是单一算子的理论突破。
- `BPH` 的价值在于稳态前置白平衡入口，而不是直接决定最终观感。
- `IMF1Ray` 负责高频细节、细胞边界和纹理表达。
- `RGHS` 是历史阶段名，真实职责是白平衡安全对比分支。
- `CLAHE` 是历史阶段名，真实职责是 CLAHE 引导的局部可见性分支。
- `Fused` 是当前最有辨识度的结构模块：它不是 RGB 平均，而是亮度域特征门控和拉普拉斯金字塔融合。
- `Final` 是轻量照明与对比收口，不应写成主要创新点。

## 4. 实验层关键判断

- H1 白平衡最终人工锁定 `r2_05_G_P_A_B`，不是自动综合分最高的 `r2_02_G_P`。
- H2 当前接受结果为 `RGHS=rghs_s07`、`CLAHE=clahe_s05`、`Fusion=fusion_s10`。
- `fusion_s10` 带来明显结构指标收益，但伴随 `UCIQE/UIQM` 回撤；如果未来重开 Fusion，必须加入视觉护栏。
- 当前正式 `9` 方法 complete-case 主表已经形成，不应再写成“还没统一评测”。
- 当前真正缺的是下游边缘验证总表、投稿级定性图组、失败案例图组、数据采集说明和运行时间/资源说明。

## 5. 论文解释边界

- `MS_SSIM` 和 `PSNR` 在当前项目中表示增强结果相对原图的结构一致性，不是相对增强真值的质量指标。
- `HVDualformer` 和 `ABC-Former` 是白平衡方法，不能在 related work 中混写成标准水下增强模型。
- `WWPF` 必须保留在正式主表中，并说明官方实现稳定输出 496 张。
- `HLRP` 和 `Histoformer` 可作为当前 HAB 显微协议下的失败案例或补充分析，但不能写成对原论文方法普遍无效的否定。
- “边缘友好”目前更适合写成设计动机和待补强方向，不能写成已完成完整下游任务闭环。

## 6. 当前开放问题

- 如何补齐与当前正式主线严格对齐的下游边缘验证总表。
- 如何整理代表性 qualitative panel 和失败案例图组。
- 是否需要在加入视觉护栏后重开 Fusion 调参。
- 数据采集条件、覆盖范围、公开性和运行代价如何写成投稿级说明。

## 7. 相关入口

- 智能体执行规则：`AGENTS.md`
- 完整执行规则：`docs/project_execution_rules_cn.md`
- 项目交接指南：`docs/project_handoff_guide_cn.md`
- 当前状态总览：`docs/project_status_overview_cn.md`
- 对比方法与结果索引：`docs/comparison_methods_results_index_cn.md`
- 结构化状态源：`research-state.yaml`
