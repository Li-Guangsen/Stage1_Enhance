# 投稿级图表规划（中文）

更新时间：2026-05-24

本文档只规划投稿级图表，不生成新图、不运行图表脚本、不产生新实验结果。所有图表都必须引用当前正式主线、正式 manifest 和正式结果表。

## 1. 图表口径

- 正式配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 正式结果：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 阶段表口径：`full502_clean_v1`
- 主比较口径：`compare9_complete496_v1`
- 方法总览现有基础资产：`paper/figures/underwater_method_overview.svg`、`paper/figures/underwater_method_overview_simple.svg`

必须遵守：

- 不把 `full506` 写成当前正式主表口径；它只表示历史搜索与锁定背景。
- 不把未来下游验证画成已经完成的结果。
- 不把 `RGHS` / `CLAHE` 作为无解释缩写直接放进论文主图；图中应写真实职责。
- 不把 `MS_SSIM` / `PSNR` 解释为相对增强真值的质量指标。

## 2. 建议图表清单

| 编号 | 类型 | 目的 | 当前状态 | 后续动作 |
| --- | --- | --- | --- | --- |
| Fig. 1 | 方法总览图 | 展示稳态前置白平衡、三分支、特征门控融合和轻量收口 | 已有 SVG/PNG/Mermaid 初稿 | 后续只需人工检查排版与缩略图是否需要加入 |
| Fig. 2 | 阶段 qualitative panel | 展示 `Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final` 的视觉演化 | 已生成候选 panel | 当前候选位于 `metrics/outputs/downstream_edge_validation/official_full502_mainline/stage_full502_proxy/qualitative_panels`，仍需人工筛图 |
| Fig. 3 | 外部主比较 qualitative panel | 展示 `Ours` 与稳健外部方法、`WWPF`、失败案例方法的差异 | 已生成候选 panel | 当前候选位于 `metrics/outputs/downstream_edge_validation/official_full502_mainline/compare9_complete496_proxy/qualitative_panels`，仍需人工筛图 |
| Fig. 4 | 失败案例图组 | 说明 `HLRP` / `Histoformer` 在当前 HAB 显微协议下的偏色、噪声或结构失真 | 已生成 proxy 候选 | 必须写清这是当前协议下的复现观察；最终入稿前仍需人工确认 |
| Fig. 5 | 主表图示化 | 将正式主比较表转成排序图或分组柱状图 | 只规划 | 后续基于已有 `mean_metrics_table.md` 生成，不重新评测 |
| Table 1 | 阶段进度表 | 引用 `official_stage_progress_full502` | 已有正式表 | 后续排版成论文表 |
| Table 2 | 9 方法主比较表 | 引用 `official_compare9_complete496` | 已有正式表 | 后续排版成论文表，保留全部 9 方法 |

## 3. 图组选择原则

### 阶段图组

输入必须来自：

- 原图：`data/inputImg/Original`
- 正式结果：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png`
- 样本清单：`metrics/manifests/full502_clean_v1.txt`

展示顺序固定为：

`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`

图注应强调：

- `BPH` 是稳态前置白平衡入口。
- `IMF1Ray`、白平衡安全对比分支、CLAHE 引导局部可见性分支分别承担不同职责。
- `Fused` 是亮度域特征门控融合，不是 RGB 均值融合。
- `Final` 是轻量收口，不是主要创新模块。

### 外部主比较图组

输入必须来自 `compare9_complete496_v1` 的 complete-case 样本。建议展示：

- `Original`
- `Ours`
- 至少 2 个稳健方法：如 `GDCP`、`CBF`、`SGUIE-Net`
- `WWPF`：作为激进但可接受的强基线
- `HLRP` 或 `Histoformer`：作为当前协议下的失败案例或补充分析

不建议把 `HVDualformer` 和 `ABC-Former` 写成标准水下增强方法；若放入图组，应标注为白平衡方法。

## 4. 图注写法模板

### 方法总览图

`图 X. 本文提出的分阶段增强框架总览。输入图像首先经过灰像素引导的前置白平衡模块，以稳定颜色起点；随后，从白平衡结果并行生成 IMF1-Rayleigh 高频细节分支、白平衡安全对比分支和 CLAHE 引导的局部可见性分支；三条分支在亮度空间中通过特征门控的拉普拉斯金字塔融合进行协同整合，并经过轻量照明与对比收口得到最终输出。下游边缘验证作为未来任务化评估路径单独呈现，不属于增强算子本体。`

### 阶段图组

`图 X. 当前正式主线在 HAB 显微图像上的阶段化增强示例。各列依次展示原图、前置白平衡、IMF1-Rayleigh 细节分支、白平衡安全对比分支、CLAHE 引导局部可见性分支、特征门控融合和最终收口结果。该图用于说明不同阶段的职责分工，不代表下游边缘验证已经完成。`

### 外部主比较图组

`图 X. 当前 compare9_complete496_v1 口径下的外部方法定性对比示例。WWPF 保留为激进但可接受的强基线；HLRP 与 Histoformer 的异常表现仅作为当前 HAB 显微图像协议下的复现观察，不构成对原方法在一般水下场景中的否定。`

## 5. 后续执行检查清单

- 选图必须来自正式 manifest 对应样本。
- 所有定性图必须保留样本名和来源路径记录。
- 图中不得出现未解释的历史阶段名。
- 主表图示化只能基于已有正式结果表，不能重新计算或替换正式结果。
- 生成图后必须更新证据包、中文主稿和 `research-log.md`。

## 6. 当前已生成的候选图组

第一版候选图组由 `metrics/scripts/run_downstream_edge_proxy_stage1.py` 自动生成，用于 Stage1 enhancement-to-edge 支撑包：

- 阶段图候选：`duolie.5`、`juciqigou.2`、`weiruan.2`、`weiruan.4`
- 外部对比/失败案例候选：`lianzhuang.2`、`qiangzhuang.13`、`qiangzhuang.8`、`xuanlianjiaomao.6`
- 输出位置：`metrics/outputs/downstream_edge_validation/official_full502_mainline`

这些图是候选图，不是最终投稿图。正式使用前必须人工检查边界、杂质、伪边缘和排版。
