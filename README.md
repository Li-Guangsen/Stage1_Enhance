# Stage1Codex 项目说明

## 1. 项目概览

本仓库当前用于水下图像增强实验，工作主线是围绕一条七阶段增强流水线做受控调参与评测：

`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`

其中：

- `BPH`：前置白平衡
- `IMF1Ray`：细节增强分支
- `RGHS`：对比度增强分支
- `CLAHE`：局部对比度增强分支
- `Fused`：三分支融合结果
- `Final`：后处理细化后的最终输出

当前仓库重点不是重新搭框架，而是在现有方法链路上做分阶段消融、全量评测和可复现实验收口。

## 2. 当前进度

截至 `2026-04-15`，当前最重要的研究状态如下：

- H1 白平衡调参主线已完成 `full506` 正式评测
- 正式数据基于 `Original` 全量 `506` 张图像
- 四套正式方法均完成 `506/506 complete-case`
- 自动综合分 `metric_winner`：`r2_02_G_P`
- 人工最终锁定 winner：`r2_05_G_P_A_B`

当前人工锁定结论是：

- 后续如果继续做“前置白平衡”相关调参，默认使用 `r2_05_G_P_A_B`
- 自动结果仍保留在评测文件中，便于审计和回看

原因是：

- `r2_05_G_P_A_B` 相对 baseline 同时提升了 `MS-SSIM` 和 `PSNR`
- 在“同时双增”的候选里，它的综合分回撤最小
- 抽样诊断图未见明显系统性偏红、偏黄、偏紫等偏色

## 3. H1 full506 当前结论

`experiments/h1-graypixel-bph-ablation/outputs/full506/eval` 中的核心结果如下：

| 方法 | 综合分 | MS-SSIM | 相对 baseline | PSNR | 相对 baseline |
|---|---:|---:|---:|---:|---:|
| `r2_00_baseline` | `0.0000` | `0.700122` | `0.000000` | `16.084406` | `0.000000 dB` |
| `r2_02_G_P` | `0.0221` | `0.699999` | `-0.000122` | `16.104605` | `+0.020199 dB` |
| `r2_05_G_P_A_B` | `-0.0413` | `0.701150` | `+0.001028` | `16.116002` | `+0.031596 dB` |
| `r2_08_G_P_A2_B` | `-0.1201` | `0.700453` | `+0.000331` | `16.102306` | `+0.017901 dB` |

配套状态文件：

- 自动 + 人工最终选择：`experiments/h1-graypixel-bph-ablation/outputs/full506/selection.json`
- 人工最终选中参数：`experiments/h1-graypixel-bph-ablation/outputs/full506/candidate_params/r2_05_G_P_A_B.json`
- 分析说明：`experiments/h1-graypixel-bph-ablation/analysis.md`
- 研究时间线：`research-log.md`

## 4. 仓库结构

当前常用目录和文件如下：

- `main.py`
  - 主增强入口，读取输入图像并生成 `BPH / IMF1Ray / RGHS / CLAHE / Fused / Final`
- `lgsbph.py`
  - 前置白平衡相关实现
- `pybemd.py`
  - `IMF1Ray` 相关实现
- `RGHS.py`
  - `RGHS` 分支实现
- `CLAHE.py`
  - `CLAHE` 分支实现
- `fusion_three.py`
  - 三分支融合实现
- `lvbo.py`
  - `Final` 阶段细化实现
- `metrics/`
  - protocol-v2 评测与打分脚本、输出结果
- `experiments/optimization_v1/`
  - 后阶段融合/细化调参实验
- `experiments/h1-graypixel-bph-ablation/`
  - H1 白平衡调参编排、结果和分析
- `data/inputImg/Original/`
  - 当前 full506 原图输入目录
- `docs/archive-en/`
  - 英文原稿归档

## 5. 环境与运行方式

当前约定工作目录：

```bat
D:\Desktop\Stage1Codex
```

当前约定 Python 环境：

```bat
D:\Desktop\EdgeDetection\my_env
```

推荐运行 Python 的方式：

```bat
cmd.exe /D /S /C "call D:\miniconda3\Scripts\activate.bat D:\miniconda3 && call conda activate D:\Desktop\EdgeDetection\my_env && python 脚本.py"
```

### 5.1 运行主增强流水线

默认情况下，`main.py` 会读取 `data/inputImg/Original`，并将结果写入 `results`：

```bat
cmd.exe /D /S /C "call D:\miniconda3\Scripts\activate.bat D:\miniconda3 && call conda activate D:\Desktop\EdgeDetection\my_env && python main.py"
```

常见参数：

- `--input-dir`
- `--output-dir`
- `--manifest`
- `--limit`
- `--params-json`
- `--skip-existing`
- `--resize-to`
- `--no-resize`

### 5.2 运行 H1 白平衡编排

H1 编排入口：

```bat
cmd.exe /D /S /C "call D:\miniconda3\Scripts\activate.bat D:\miniconda3 && call conda activate D:\Desktop\EdgeDetection\my_env && python experiments\h1-graypixel-bph-ablation\run_bph_search.py --stage full506"
```

该脚本当前负责：

- 构建或读取 `explore64` manifest
- 跑 `smoke / round1 / round2 / full506`
- 调用 protocol-v2 评测与打分
- 生成 `selection.json`、诊断图和汇总表

注意：

- `full506` 阶段内部调用 `main.py` 时带 `--skip-existing`
- 已完成的 baseline 不会被重复重算

## 6. 当前默认配置

如果后续要继续基于当前结论推进，默认基线如下：

- 前置白平衡 winner：`r2_05_G_P_A_B`
- 参数文件：`experiments/h1-graypixel-bph-ablation/outputs/full506/candidate_params/r2_05_G_P_A_B.json`
- 下游固定配置：`experiments/optimization_v1/configs/best_full506_r4_03.json`

换句话说，当前建议的组合是：

- 前面白平衡用 `r2_05_G_P_A_B`
- 后面融合与最终细化沿用 `r4_03`

## 7. 关键结果文件

H1 `full506` 的关键收口文件位于：

```text
experiments/h1-graypixel-bph-ablation/outputs/full506/
```

重点包括：

- `eval/summary.txt`
- `eval/summary.json`
- `eval/per_image_metrics.csv`
- `eval/composite_scores.csv`
- `eval/guardrail_scores.csv`
- `selection.json`
- `candidate_params/r2_05_G_P_A_B.json`

补充说明：

- `selection.json` 同时保留自动 winner 和人工最终 winner
- 当前最终锁定字段是 `final_winner = r2_05_G_P_A_B`

## 8. 文档说明

当前项目内主要维护两份中文主文档：

- `experiments/h1-graypixel-bph-ablation/analysis.md`
  - 针对 H1 白平衡实验的阶段性结论、结果表和判定说明
- `research-log.md`
  - 研究过程时间线，只追加，不回写历史条目

英文原稿已归档到：

- `docs/archive-en/research-log.en.md`
- `docs/archive-en/experiments/h1-graypixel-bph-ablation/analysis.en.md`

## 9. Git 约定

当前仓库是本地轻量 Git 仓库，`.gitignore` 的基本策略是：

- 忽略大体积数据和大结果树
- 保留源码、实验脚本、文档
- 允许纳入小型汇总文件，例如：
  - `selection.json`
  - `summary.json`
  - `summary.txt`
  - `composite_scores.csv`
  - `guardrail_scores.csv`
  - `per_image_metrics.csv`

这意味着：

- 大图像结果目录通常不进 Git
- 关键评测结论和实验收口状态会进 Git，便于追踪

## 10. 下一步建议

如果继续沿当前主线推进，建议顺序如下：

1. 以后续调参统一以 `r2_05_G_P_A_B` 作为前置白平衡基线
2. 不要混入新的大规模实验线，先在现有主链路上做受控增量修改
3. 每完成一轮正式评测，就同步更新：
   - `experiments/h1-graypixel-bph-ablation/analysis.md`
   - `research-log.md`
   - 对应实验目录下的 `selection.json` 和汇总文件

如果后续把本仓库接到远程仓库，建议优先保持这个 README、`analysis.md`、`research-log.md` 和各阶段小型评测汇总文件同步更新。
