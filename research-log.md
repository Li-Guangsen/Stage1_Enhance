# 研究日志

按时间顺序记录研究决策与行动，仅追加，不回写历史条目。

| 编号 | 日期 | 类型 | 摘要 |
|---|------|------|---------|
| 1 | 2026-04-11 | 启动 | 在 `D:\\Desktop\\Stage1Codex` 初始化 autoresearch 工作区，创建 research-state/log/findings 文件，并为本线程设置 20 分钟连续性心跳。 |
| 2 | 2026-04-11 | 启动 | 通读并对齐当前仓库代码（`main.py`, `lgsbph.py`, `pybemd.py`, `RGHS.py`, `CLAHE.py`, `fusion_three.py`, `lvbo.py`）、两篇本地参考论文以及既有项目指引日志。 |
| 3 | 2026-04-11 | 启动 | 确认当前工作方法是七阶段增强流水线：改进的灰像素引导白平衡 → IMF1Ray 细节分支 → RGHS 对比分支 → CLAHE 分支 → 特征门控三分支融合 → 同态细化。 |
| 4 | 2026-04-11 | 启动 | 围绕灰像素引导 clipped ACCC、特征门控融合和同态细化形成 H1-H3 初始假设，并在进一步扩展架构前锁定当前项目框架为“增强方法 + 下游边缘验证”。 |
| 5 | 2026-04-11 | 启动 | 将两篇本地论文记录为首批关键文献，并标记当前证据缺口：标准化评测子集、锁定的消融协议，以及更强的下游边缘验证实验。 |
| 6 | 2026-04-11 | 启动 | 围绕当前已完成增强结果 `results/png/Final` 定义的 92 张 pilot 子集，锁定第一版受控评测协议 `pilot92-v1`。 |
| 7 | 2026-04-11 | 启动 | 将消融优先级锁定为 H2（fusion）→ H1（white balance）→ H3（homomorphic refinement），因为 H2 在当前仓库里既是最强的代码级新意，也是最干净的首个实验入口。 |
| 8 | 2026-04-11 | 文献 | 为综述补充两篇邻近参考：2023 年 EMD-wavelet HAB enhancement 论文和 2024 年 Frontiers HAB edge-detection 论文。 |
| 9 | 2026-04-11 | 汇报 | 在 `to_human/` 生成 bootstrap 进度报告，方便人工在不读原始笔记的情况下查看当前研究状态。 |
| 10 | 2026-04-12 | 实验 | 新增 protocol-v2 评测/打分脚本，对 `main.py` 做参数化，并在 `pilot92-v1` 上评测当前各阶段输出，确认 `Final` 是现有阶段中的最佳输出。 |
| 11 | 2026-04-12 | 实验 | 基于现有 BPH/IMF1Ray/RGHS/CLAHE PNG 运行 17 个后阶段融合/细化候选搜索，选出 `c25_rghs_entropy_mid` 作为平衡型 pilot 优胜者，因为它在几乎追平最高综合分的同时，把 Mean_MS_SSIM 保持在 0.85 以上。 |
| 12 | 2026-04-13 | 实验 | 将调参切换到全量 506 张 `Original` 数据集。完成四轮 full506 后阶段细化搜索后，选出 `r4_03_gamma_050_210_48` 作为当前综合指标优胜者；其相对 `c25` 在 506/506 complete cases、零失败条件下表现更优，并将可复现实验配置保存到 `experiments/optimization_v1/configs/best_full506_r4_03.json`。 |
| 13 | 2026-04-13 | 实验 | 围绕固定下游 `r4_03` 实现 H1 白平衡调参 protocol v2：新增 `experiments/h1-graypixel-bph-ablation/run_bph_search.py`，将 H1 协议切换为面向 full506 的 explore64 → round1 → round2 → full506 编排，并把结构护栏和可视化诊断编码进整条流水线。 |
| 14 | 2026-04-13 | 实验 | 从全部 506 张原图构建分层 `explore64` manifest（`data/eval_subset_explore64_full506_bph_v1.txt`），并在 `bph00_baseline` 与 `bph10_gp_strict` 上完成 5 张样本的 smoke run。六阶段链路全部执行成功，clean protocol-v2 评测给出 5/5 complete cases、零失败。 |
| 15 | 2026-04-15 | 实验 | 完成 H1 白平衡 `full506` 正式实验，结果位于 `experiments/h1-graypixel-bph-ablation/outputs/full506`：四套方法全部在 `506/506 complete-case` 图像上完成评测、无失败、诊断图生成成功，且 `selection.json` 将 `r2_02_G_P` 记录为当前 metric winner。三个白平衡候选相对 `r2_00_baseline` 都通过了硬护栏和动态护栏；人工抽看诊断图未见明显系统性偏色，因此当前建议将 `r2_02_G_P` 锁定为 H1 白平衡赢家。 |
| 16 | 2026-04-15 | 决策 | 在保留自动评测结果 `metric_winner = r2_02_G_P` 的前提下，人工最终将 `r2_05_G_P_A_B` 锁定为 H1 白平衡正式胜者，并作为后续上游白平衡调参默认配置。锁定理由是：它相对 `r2_00_baseline` 同时提升了 `MS-SSIM` 与 `PSNR`，且在“双增”候选中综合分回撤最小，适合作为更稳的前置白平衡方案。 |
| 17 | 2026-04-15 | 文档 | 为当前主线补充显式锁定配置，最初用于统一表示“H1 `r2_05_G_P_A_B` + 下游 `r4_03`”组合；同时更新中文 README 与实验分析文档，明确该类锁定文件用于复现和引用，但不自动改写 `main.py` 的默认参数入口。该临时命名方案随后在同日整理为正式名称 `locked_full506_mainline.json`。 |
| 18 | 2026-04-15 | 文档 | 将主线锁定配置正式整理为 `experiments/optimization_v1/configs/locked_full506_mainline.json`，并把已确认结果复制到 `experiments/h1-graypixel-bph-ablation/outputs/full506/runs/full506_locked_mainline` 与 `candidate_params/full506_locked_mainline.json`。新的正式命名用于后续展示和文档引用；历史候选命名保留在评测和诊断文件中，用于审计链回溯。 |
| 19 | 2026-04-17 | 文档 | 将 `RGHS` 分支主实现文件从 `RGHS.py` 重命名为 `wb_safe_contrast.py`，以匹配其真实功能“白平衡安全对比增强分支”。阶段名 `RGHS` 仍保留在结果目录、配置字段和实验记录中；`RGHS.py` 仅作为兼容旧导入的薄封装保留。 |
| 20 | 2026-04-17 | 文档 | 将 `CLAHE` 分支主实现文件从 `CLAHE.py` 重命名为 `clahe_guided_visibility.py`，以匹配其真实功能“CLAHE 引导的局部可见性增强分支”。阶段名 `CLAHE` 仍保留在结果目录、配置字段和实验记录中；`CLAHE.py` 仅作为兼容旧导入的薄封装保留。 |
| 21 | 2026-04-17 | 文档 | 新增本地方法草稿 `method-underwater-enhancement.md`，按当前代码真实实现写出 method section 的中文完整版、中文短版与英文骨架，并同步到 Notion `论文写作` 数据库条目《水下图像增强 method section 草稿》；同时将该条目加入项目主页的当前重点页面。 |
| 22 | 2026-04-17 | 文档 | 在方法草稿基础上继续压缩出更接近论文成稿的版本 `method-underwater-enhancement-paper-ready.md`，整理出正式的 `3 Method` 小节结构、英文骨架、图注草稿与实验过渡句，并同步到 Notion `论文写作` 数据库条目《水下图像增强 method section 精简稿》；同时将其加入项目主页的当前重点页面。 |
| 23 | 2026-04-17 | 文档 | 新增方法总览图说明 `method-figure-underwater-enhancement.md`，统一方法图的结构布局、节点命名、应强调与应避免暗示的内容、图注草稿与正文引用句，并同步到 Notion `论文写作` 数据库条目《水下图像增强 方法总览图说明》；同时将其加入项目主页的当前重点页面。 |
| 24 | 2026-04-17 | 文档 | 将方法总览图说明进一步落成实际图稿：新增 Mermaid 源文件 `paper/figures/underwater_method_overview.mmd`，并成功导出 `paper/figures/underwater_method_overview.svg` 与 `paper/figures/underwater_method_overview.png`；同时同步到 Notion `论文写作` 数据库条目《水下图像增强 方法总览图初稿》，并加入项目主页重点页面。 |
| 25 | 2026-04-17 | 文档 | 为便于当前版本先提交，新增更轻量的图稿 `paper/figures/underwater_method_overview_simple.mmd`，并导出 `paper/figures/underwater_method_overview_simple.svg` 与 `paper/figures/underwater_method_overview_simple.png`。该版本保留方法主链、三分支、融合中心和外部下游验证路径，但去掉了框内细节说明，适合作为先行提交和后续微调底稿。 |
| 26 | 2026-04-17 | 文献 | 新增 `related-work-underwater-enhancement.md`，围绕当前 Zotero 阅读集整理传统水下增强、HAB 显微增强谱系、深度模型以及白平衡/直方图建模的相关工作比较表、中文综述段落、英文骨架和短版写法，作为论文相关工作起草底稿。 |
| 27 | 2026-04-17 | 文档 | 统一补齐项目记录层：将 README、`research-state.yaml`、H2 中间阶段分析文档与当前接受主线对齐，明确 `locked_full506_final_mainline.json` 为当前接受配置，并把 method / related work / 方法图资产纳入仓库级文档导航。 |
