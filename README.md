# Stage1Codex 项目说明

## 1. 项目概览

本仓库当前用于水下图像增强实验，工作主线是围绕一条七阶段增强流水线做受控调参与评测：

`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`

其中：

- `BPH`：前置白平衡
- `IMF1Ray`：基于 IMF1 + Rayleigh 的高频细节增强分支
- `RGHS`：历史名 `RGHS`，当前实际是白平衡安全对比增强分支
- `CLAHE`：历史名 `CLAHE`，当前实际是 CLAHE 引导的局部可见性增强分支
- `Fused`：三分支融合结果
- `Final`：后处理细化后的最终输出

当前仓库重点不是重新搭框架，而是在现有方法链路上做分阶段消融、全量评测和可复现实验收口。

## 1.1 阶段命名说明

当前仓库里有两套并行存在的“名字”：

- 一套是历史沿用的阶段名，用在代码入口、结果目录和实验记录里，便于兼容既有资产
- 另一套是真实功能描述，用来帮助理解各模块到底在做什么

当前按真实功能理解，三条中间分支更准确的描述是：

- `IMF1Ray`：在 Lab 的 `L` 通道上提 IMF1 / 高频响应，再做 Rayleigh 匹配，属于高频细节增强分支
- `RGHS`：主函数实际是 `wb_safe_contrast`，属于白平衡安全对比增强分支
- `CLAHE`：不是直接导出普通 CLAHE，而是先推导增益图、再做引导滤波和平滑后处理，属于 CLAHE 引导的局部可见性增强分支

当前阶段名、配置字段名和结果目录名继续保留历史名 `RGHS / CLAHE`；实现文件已
分别重命名为 `wb_safe_contrast.py` 与 `clahe_guided_visibility.py`，以便让
代码层表达更贴近真实功能。

## 1.2 模块速查表

| 阶段 | 主实现文件 | 主要职责 | 调参时优先关注 |
|---|---|---|---|
| `BPH` | `lgsbph.py` | 先把偏色和通道失衡压回稳定起点 | 灰像素筛选、ACCC 步长、亮度回调 |
| `IMF1Ray` | `pybemd.py` | 生成高频细节与边缘响应分支 | IMF1 提取尺度、细节注入、Rayleigh 收口 |
| `RGHS` | `wb_safe_contrast.py` | 提供主体层次、亮度托底与色彩稳定 | 对比力度、平坦区抑制、色度保护 |
| `CLAHE` | `clahe_guided_visibility.py` | 提供局部可见性、背景与暗部补偿 | CLAHE 尺度、增益上下界、后端 Lab 微调 |
| `Fused` | `fusion_three.py` | 按职责分工融合三条分支的亮度结构 | 分支权重、层级门控、保底与偏置 |
| `Final` | `lvbo.py` | 对融合结果做最后一层亮度收口 | 同态滤波参数、亮度匹配、轻度熵增强 |

## 1.3 调参理解补充

- `BPH` 的任务是先把颜色拉回可控区间，不要把最终观感增强的压力提前压到这一层。
- `IMF1Ray / RGHS / CLAHE` 三条分支更适合各司其职地调，不要指望某一条单独把所有问题都解决。
- `Fused` 更像“分工协调层”，关键不是谁绝对更强，而是谁该在什么频段和区域发言。
- `Final` 更像“收口层”，优先做温和整理；如果要靠它去硬救上游问题，通常说明前面分支还没调到位。

## 1.4 配置字段对照

`main.py --params-json ...` 读取的 JSON，当前按下面这套顶层结构接线：

| 顶层 key | 对应阶段 | 消费函数 | 说明 |
|---|---|---|---|
| `bph` | `BPH` | `lgs_accc_bgr_improved` | 前置白平衡参数 |
| `imf1ray` | `IMF1Ray` | `imf1Ray_from_bgr` | 默认先带 `aggressive=true`，再叠加 JSON 覆写 |
| `rghs` | `RGHS` | `wb_safe_contrast` | 白平衡安全对比增强参数 |
| `clahe` | `CLAHE` | `clahe_3ch_wb_safe` | CLAHE 引导局部可见性参数 |
| `fusion` | `Fused` | `fuse_three_images_bgr` | 三分支融合参数 |
| `final` | `Final` | `_final_refine` | 收口层参数，额外受 `mode` 控制 |

`final.mode` 当前支持：

- `homomorphic`
- `entropy`
- `homomorphic_entropy`
- `none`

补充约定：

- 省略某个顶层 key，表示该阶段直接使用代码默认参数
- 当前主流程不会消费的顶层 key 会被忽略
- `RGHS / CLAHE` 这两个名字在配置里继续保留历史名，对应的实现文件分别是 `wb_safe_contrast.py` 与 `clahe_guided_visibility.py`

一个最小骨架示例如下：

```json
{
  "bph": {},
  "imf1ray": {
    "aggressive": true
  },
  "rghs": {},
  "clahe": {},
  "fusion": {},
  "final": {
    "mode": "homomorphic"
  }
}
```

如果使用 `homomorphic_entropy`，则 `final` 结构会变成：

```json
{
  "final": {
    "mode": "homomorphic_entropy",
    "gamma_low": 0.5,
    "gamma_high": 2.1,
    "cutoff_freq": 48,
    "entropy": {
      "p_low": 1.0,
      "p_high": 99.0,
      "clahe_clip": 1.25,
      "mix_global": 0.35,
      "mix_local": 0.2,
      "chroma_gain": 1.02
    }
  }
}
```

## 1.5 当前代码整理状态

除实验本身之外，当前仓库已经完成一轮“说明层整理”。这轮整理的目标不是改算法，
而是把现有主线的真实职责、命名关系和配置接线写清楚，方便后续继续调参。

当前这轮整理已经完成的内容包括：

- 统一梳理七阶段流水线的职责说明，明确 `BPH / IMF1Ray / RGHS / CLAHE / Fused / Final`
  各自负责什么
- 将更贴近真实功能的实现文件名落地到代码层：
  - `RGHS` 主实现文件为 `wb_safe_contrast.py`
  - `CLAHE` 主实现文件为 `clahe_guided_visibility.py`
- 保留 `RGHS.py` 与 `CLAHE.py` 两个兼容薄封装，避免旧导入路径立刻失效
- 为 `lgsbph.py`、`pybemd.py`、`wb_safe_contrast.py`、`clahe_guided_visibility.py`、
  `fusion_three.py`、`lvbo.py`、`main.py` 增补模块说明、参数分组说明和调参理解说明
- 在 `main.py` 中补齐 `params-json` 的顶层 key 到各阶段消费函数的接线关系
- 在 README 中补齐：
  - 阶段命名说明
  - 模块速查表
  - 调参理解补充
  - 配置字段对照

这轮整理明确保持不变的边界包括：

- 不修改增强算法内核逻辑
- 不修改当前已接受实验结果
- 不改阶段名、结果目录名、配置字段名里的历史名称 `RGHS / CLAHE`
- 不自动改写 `main.py` 默认运行配置

因此，当前仓库里要同时接受两层命名：

- 代码实现层更偏真实功能：`wb_safe_contrast.py`、`clahe_guided_visibility.py`
- 实验与资产层继续保留历史阶段名：`RGHS`、`CLAHE`

按当前主线理解：

- 如果你在看“代码怎么实现”，优先看新的主实现文件名
- 如果你在看“实验结果怎么组织”，优先沿用阶段名和 `selection.json`
- 如果你在看“这套链路当前接受什么”，优先以
  `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
  和 `experiments/h2-full506-direct/selection.json` 为准

## 2. 当前进度

截至 `2026-04-17`，当前最重要的研究状态如下：

- H1 白平衡调参主线已完成 `full506` 正式评测
- 正式数据基于 `Original` 全量 `506` 张图像
- 四套正式方法均完成 `506/506 complete-case`
- 自动综合分 `metric_winner`：`r2_02_G_P`
- 人工最终锁定 winner：`r2_05_G_P_A_B`
- H2 `RGHS -> CLAHE -> Fusion` 顺序调参已完成一次 `full506` 直跑
- H2 直跑复用了锁定主线的 `BPH / IMF1Ray` 结果，不再重算前两级
- H2 当前接受的阶段 winner 为：
  - `RGHS = rghs_s07`
  - `CLAHE = clahe_s05`
  - `Fusion = fusion_s10`
- 当前接受的整条主线组合为：
  - `BPH = r2_05_G_P_A_B`
  - `IMF1Ray = locked_mainline 既有输出`
  - `RGHS = rghs_s07`
  - `CLAHE = clahe_s05`
  - `Fusion = fusion_s10`
  - `Final = r4_03`
- 上述当前接受组合已固化为统一配置：
  - `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 上述当前接受组合的完整七阶段正式结果目录已整理为：
  - `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 对应正式评测收口目录已整理为：
  - `experiments/h2-full506-direct/outputs/full506/eval`
- H2 评测从 `rghs_final_backstop` 之后已经去掉 `SIFT_KP`
- 当前已确认先采用 `fusion_s10`，但需明确：它在 `MS_SSIM / PSNR` 上提升明显，同时 `UCIQE / UIQM` 有较大回撤；后续若继续开 Fusion，应把视觉项退化纳入硬约束

当前人工锁定结论是：

- 后续如果继续做“前置白平衡”相关调参，默认使用 `r2_05_G_P_A_B`
- 自动结果仍保留在评测文件中，便于审计和回看

原因是：

- `r2_05_G_P_A_B` 相对 baseline 同时提升了 `MS-SSIM` 和 `PSNR`
- 在“同时双增”的候选里，它的综合分回撤最小
- 抽样诊断图未见明显系统性偏红、偏黄、偏紫等偏色

当前已完成的主线收口工作包括：

- 已将 “H1 `r2_05_G_P_A_B` + 下游 `r4_03`” 整理为正式锁定配置 `experiments/optimization_v1/configs/locked_full506_mainline.json`
- 已将这套已确认结果复制到正式展示目录 `experiments/h1-graypixel-bph-ablation/outputs/full506/runs/full506_locked_mainline`
- 已同步更新 README、H1 分析文档、优化分析文档、`selection.json` 和研究日志，统一当前主线命名
- 当前仍不改写 `main.py` 默认入口，避免在后续调参尚未完全收口前过早固化默认运行配置

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

### 3.1 H2 full506 顺序调参当前结论

本轮 H2 的执行方式不是三层联调，而是条件固定的顺序优化：

1. 先固定 `BPH / IMF1Ray`
2. 单独调 `RGHS`
3. 再固定 `RGHS winner`，单独调 `CLAHE`
4. 最后固定 `RGHS winner + CLAHE winner`，单独调 `Fusion`

当前接受的阶段结论如下：

| 阶段 | 当前接受 winner | 官方判优对象 | 相对 locked_mainline 的四指标变化 |
|---|---|---|---|
| `RGHS` | `rghs_s07` | `RGHS` | `ΔMS_SSIM=+0.09836`，`ΔPSNR=+1.57805 dB`，`ΔUCIQE=+0.06798`，`ΔUIQM=-4.30762` |
| `CLAHE` | `clahe_s05` | `CLAHE` | `ΔMS_SSIM=+0.03508`，`ΔPSNR=+0.72397 dB`，`ΔUCIQE=+0.02273`，`ΔUIQM=-1.11937` |
| `Fusion` | `fusion_s10` | `Final` | `ΔMS_SSIM=+0.06751`，`ΔPSNR=+1.43617 dB`，`ΔUCIQE=-0.62345`，`ΔUIQM=-5.03317` |

补充说明：

- `rghs_s07` 在 `RGHS official` 和 `Final backstop` 两侧都排第 `1`
- `clahe_s05` 在 `CLAHE official` 排第 `1`，并通过 `Final backstop`，因此不顺延到 `clahe_s08`
- `fusion_s10` 是当前按既定排序规则选出的 winner；它明显偏向前两优先指标，不代表视觉项也同步更优

H2 关键文件：

- 编排脚本：`experiments/h2-full506-direct/run_full506_direct.py`
- 最终选择：`experiments/h2-full506-direct/selection.json`
- 中文分析：`experiments/h2-full506-direct/analysis.md`
- `RGHS` 排名：`experiments/h2-full506-direct/scores/rghs_official/ranked.json`
- `CLAHE` 排名：`experiments/h2-full506-direct/scores/clahe_official/ranked.json`
- `Fusion` 排名：`experiments/h2-full506-direct/scores/fusion_final/ranked.json`
- `Fusion` 逐图指标：`experiments/h2-full506-direct/scores/fusion_final/per_image_metrics.csv`

## 4. 仓库结构

当前常用目录和文件如下：

- `main.py`
  - 主增强入口，读取输入图像并生成 `BPH / IMF1Ray / RGHS / CLAHE / Fused / Final`
- `lgsbph.py`
  - 前置白平衡相关实现
- `pybemd.py`
  - `IMF1Ray` 相关实现，本质是 IMF1 + Rayleigh 的高频细节增强分支
- `wb_safe_contrast.py`
  - `RGHS` 分支主实现文件；真实功能是白平衡安全对比增强
- `RGHS.py`
  - 兼容旧导入的薄封装，内部转发到 `wb_safe_contrast.py`
- `clahe_guided_visibility.py`
  - `CLAHE` 分支主实现文件；真实功能是 CLAHE 引导的局部可见性增强
- `CLAHE.py`
  - 兼容旧导入的薄封装，内部转发到 `clahe_guided_visibility.py`
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

当前已经确认的主线结果副本位于：

```text
experiments/h1-graypixel-bph-ablation/outputs/full506/runs/full506_locked_mainline
```

只有在确实需要从原图重新复现这套锁定组合时，才显式传入锁定配置文件：

```bat
cmd.exe /D /S /C "call D:\miniconda3\Scripts\activate.bat D:\miniconda3 && call conda activate D:\Desktop\EdgeDetection\my_env && python main.py --params-json experiments\optimization_v1\configs\locked_full506_mainline.json"
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

## 6. 当前建议组合与锁定配置

如果后续要继续基于当前结论推进，当前建议采用两层“主线基线 + H2 当前接受结果”的方式理解：

- H1 / 基线锁定：
  - 前置白平衡 winner：`r2_05_G_P_A_B`
  - 历史候选参数文件：`experiments/h1-graypixel-bph-ablation/outputs/full506/candidate_params/r2_05_G_P_A_B.json`
  - 下游旧基线固定配置：`experiments/optimization_v1/configs/best_full506_r4_03.json`
  - H1 锁定基线配置：`experiments/optimization_v1/configs/locked_full506_mainline.json`
  - H1 锁定结果副本目录：`experiments/h1-graypixel-bph-ablation/outputs/full506/runs/full506_locked_mainline`
- H2 / 当前接受结果：
  - `RGHS = rghs_s07`
  - `CLAHE = clahe_s05`
  - `Fusion = fusion_s10`
  - H2 当前统一锁定配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
  - H2 当前正式结果目录：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
  - H2 最终状态文件：`experiments/h2-full506-direct/selection.json`
  - H2 阶段参数目录：`experiments/h2-full506-direct/configs/`

换句话说，当前建议的组合是：

- 前面白平衡用 `r2_05_G_P_A_B`
- `IMF1Ray` 继续复用 `full506_locked_mainline` 结果
- `RGHS` 用 `rghs_s07`
- `CLAHE` 用 `clahe_s05`
- `Fusion` 用 `fusion_s10`
- `Final` / 最终细化继续沿用 `r4_03`

补充说明：

- `locked_full506_mainline.json` 仍表示 H1 白平衡锁定后的旧主线基线，不包含本轮 H2 的 `rghs / clahe / fusion` winner
- 当前 README 已接受 `fusion_s10` 作为 Fusion 阶段当前采用结果，并已将整套 H2 链路固化为新的统一锁定配置文件
- 当前不会自动改写 `main.py` 的默认 `--params-json`；当前统一配置已单独固化，但仍保持显式传参优先
- 历史结果树和评测表中仍保留原候选名，用于审计与回溯；正式说明中优先引用 `selection.json` 与当前接受组合

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
- `candidate_params/full506_locked_mainline.json`
- `runs/full506_locked_mainline`

补充说明：

- `selection.json` 同时保留自动 winner 和人工最终 winner
- 当前最终锁定字段是 `final_winner = r2_05_G_P_A_B`

H2 `full506` 直跑调参的关键收口文件位于：

```text
experiments/h2-full506-direct/
```

重点包括：

- `selection.json`
- `analysis.md`
- `outputs/full506/eval`
- `outputs/full506/runs/full506_final_mainline`
- `outputs/full506/runs/full506_final_mainline/artifact_manifest.json`
- `configs/rghs/rghs_s07.json`
- `configs/clahe/clahe_s05.json`
- `configs/fusion/fusion_s10.json`
- `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- `scores/rghs_official/ranked.json`
- `scores/rghs_final_backstop/ranked.json`
- `scores/clahe_official/ranked.json`
- `scores/clahe_final_backstop/ranked.json`
- `scores/fusion_final/ranked.json`
- `scores/fusion_final/per_image_metrics.csv`

补充说明：

- H2 的基线对比对象是 `runs/full506_locked_mainline`
- H2 当前接受的最终阶段 winner 是 `fusion_s10`
- H2 的最终依赖关系以 `experiments/h2-full506-direct/selection.json` 为准

## 8. 文档说明

当前项目内主要维护两份中文主文档：

- `experiments/h1-graypixel-bph-ablation/analysis.md`
  - 针对 H1 白平衡实验的阶段性结论、结果表和判定说明
- `experiments/h2-full506-direct/analysis.md`
  - 针对 H2 `RGHS / CLAHE / Fusion` 顺序调参的阶段 winner、full506 排名和当前接受结论
- `research-log.md`
  - 研究过程时间线，只追加，不回写历史条目

论文写作相关资产当前集中在以下文件：

- `related-work-underwater-enhancement.md`
  - 相关工作整理稿，含比较表、中文综述段落、英文骨架与短版写法
- `method-underwater-enhancement.md`
  - 与当前代码实现严格对齐的 method section 长稿
- `method-underwater-enhancement-paper-ready.md`
  - 更接近论文正文的 method 精简稿、英文骨架、图注草稿与实验过渡句
- `method-figure-underwater-enhancement.md`
  - 方法总览图的结构说明、图注草稿与正文引用句
- `paper/figures/underwater_method_overview.mmd`
  - 方法总览图完整版 Mermaid 源文件
- `paper/figures/underwater_method_overview_simple.mmd`
  - 当前更适合先提交和后续微调的简化版 Mermaid 源文件
- `paper/figures/underwater_method_overview.svg`
  - 方法总览图完整版导出图
- `paper/figures/underwater_method_overview_simple.svg`
  - 方法总览图简化版导出图，当前更推荐优先引用

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

## 10. Codex 协作中的 Skill / MCP 使用

当前线程与桌面环境里已经接通了 Codex 的本地 shell / 文件编辑能力，以及若干 plugin、skill、MCP 能力。对本项目的使用约定如下：

1. 本地实验优先：
   - 代码阅读、脚本改动、长时间运行、日志监控、结果汇总，优先使用本地 shell 与文件工具
   - 不把 MCP / skill 当作项目运行前置，也不在每次开工前重复做可见性验证
2. 按需使用，而不是机械调用：
   - 涉及 GitHub 同步、PR、review、issue 时，优先使用现有 GitHub plugin / skill
   - 涉及外部资料、官方文档、时效性信息时，再使用对应 MCP 或 web 能力
   - 涉及自动化或周期任务时，再使用 automation / 相关 skill
3. 本项目当前最相关的实际使用方式：
   - 本轮 H2 `full506` 直跑主要依赖本地 shell、文件读取、状态文件与日志监控完成
   - `selection.json`、`analysis.md`、评分表与日志作为实验收口资产保留
   - Git 状态检查与后续提交 / 推送继续按需执行
4. 对文档的约定：
   - 研究结论、当前接受 winner、阶段依赖关系，应优先写入 README 与对应实验目录文档
   - MCP / skill 的使用只记录“项目里如何按需用”，不在 README 中展开罗列全部平台能力清单

补充记录一下，本项目到目前为止真实用过、且和后续延续最相关的能力主要是：

- 本地 shell / 文件编辑
  - 用于代码阅读、实验编排、结果汇总、日志整理、README 与分析文档维护
- `ml-paper-writing` skill
  - 用于把当前代码真实实现压成 method section 长稿、精简稿、图注草稿和 related work 写作骨架
- Notion plugin / MCP
  - 用于把项目主页、文献库、研究笔记、实验记录、任务计划、论文写作这些结构化页面同步起来
  - 已同步过的方法与写作页面，后续可继续更新，但新线程默认先以本地 README 和文档为主
- Zotero / 文献检索与整理
  - 用于整理当前 related work 阅读集、比较表和写作底稿所依赖的论文池
  - 当前已从 Zotero 阅读集沉淀出本地文件 `related-work-underwater-enhancement.md`，所以新线程若只是继续写综述，优先先看本地文件，不必一上来就重新调 Zotero
- web / 外部检索
  - 只在需要补时效性资料、官方文档或文献核实时再用，不作为日常实验推进前置

当前已建好的 Notion 项目主页入口为：

- `https://www.notion.so/344bb1f4e23e8190a24adc78e66587ff`

但对新线程来说，更推荐的接手顺序仍然是：

1. 先读本地 `README.md`
2. 再读 `research-log.md`
3. 按任务类型进入对应实验目录或论文写作文档
4. 只有在需要继续同步知识库时再回到 Notion

## 11. 新线程快速接手 / 历史工作记录摘要

如果后续新开线程，希望在不回看长对话的情况下直接继续，建议先按下面这组摘要接手。

### 11.1 已完成到什么程度

- 已确认当前项目主线是七阶段增强流水线：
  - `Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`
- H1 白平衡 `full506` 正式实验已完成：
  - 自动 `metric_winner = r2_02_G_P`
  - 人工最终锁定 `final_winner = r2_05_G_P_A_B`
- H2 `RGHS -> CLAHE -> Fusion` 顺序调参 `full506` 已完成一轮正式收口：
  - `RGHS = rghs_s07`
  - `CLAHE = clahe_s05`
  - `Fusion = fusion_s10`
- 当前整条接受主线已经固化为：
  - `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 当前正式展示结果目录已经整理为：
  - `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`

### 11.2 已经做过哪些关键工作

- 实验侧：
  - 完成 `pilot92-v1` 与后续 `full506` 协议切换
  - 完成后处理 / 收口搜索，锁定 `r4_03`
  - 完成 H1 白平衡 full506 正式实验与人工定胜
  - 完成 H2 `RGHS / CLAHE / Fusion` 顺序调参与阶段 winner 收口
- 代码整理侧：
  - 保留历史阶段名 `RGHS / CLAHE`
  - 但将真实实现文件明确为 `wb_safe_contrast.py` 与 `clahe_guided_visibility.py`
  - 在 `main.py`、README 与模块头注释里补齐了配置接线和职责说明
- 论文写作侧：
  - 已完成 `related-work-underwater-enhancement.md`
  - 已完成 `method-underwater-enhancement.md`
  - 已完成 `method-underwater-enhancement-paper-ready.md`
  - 已完成 `method-figure-underwater-enhancement.md`
  - 已完成 `paper/figures/underwater_method_overview*.{mmd,svg,png}` 图稿资产
- Zotero / 文献整理侧：
  - 已围绕当前 Zotero 阅读集整理出传统水下增强、HAB 显微增强谱系、深度模型和白平衡 / 直方图建模四组 related work 比较材料
  - 当前与 Zotero 最直接对应的本地落地文件是 `related-work-underwater-enhancement.md`
- Notion 同步侧：
  - 已搭好项目主页、文献库、研究笔记、实验记录、任务计划、论文写作五类主库
  - 已同步核心文献、related work 草稿、method 草稿、方法图说明和阶段总结页

按时间顺序压缩理解，这些工作大致是这样推进的：

- `2026-04-11`
  - 完成项目 bootstrap、代码通读、H1/H2/H3 假设成型、`pilot92-v1` 受控评测子集锁定
- `2026-04-12`
  - 新增 protocol-v2 评测 / 打分流程，并在 pilot 上完成第一轮后处理 / 收口搜索
- `2026-04-13`
  - 将主线切到 `full506`，锁定下游 `r4_03`，并搭好 H1 白平衡编排与 explore64/round1/round2/full506 流程
- `2026-04-15`
  - 完成 H1 `full506` 正式实验，人工最终锁定 `r2_05_G_P_A_B`，并整理出 `locked_full506_mainline.json`
- `2026-04-16`
  - 完成 H2 `RGHS -> CLAHE -> Fusion` 顺序调参与 `full506` 直跑收口，接受 `rghs_s07 / clahe_s05 / fusion_s10`
- `2026-04-17`
  - 完成命名整理（`wb_safe_contrast.py` / `clahe_guided_visibility.py`）、related work / method / 方法图资产整理，以及 README / research-log / research-state 的统一同步

### 11.3 新线程应该先看哪些文件

如果是继续实验：

- `experiments/h1-graypixel-bph-ablation/analysis.md`
- `experiments/h2-full506-direct/analysis.md`
- `experiments/h2-full506-direct/selection.json`
- `experiments/optimization_v1/configs/locked_full506_final_mainline.json`

如果是继续读代码或改实现：

- `main.py`
- `lgsbph.py`
- `pybemd.py`
- `wb_safe_contrast.py`
- `clahe_guided_visibility.py`
- `fusion_three.py`
- `lvbo.py`

如果是继续写论文：

- `related-work-underwater-enhancement.md`
- `method-underwater-enhancement.md`
- `method-underwater-enhancement-paper-ready.md`
- `method-figure-underwater-enhancement.md`
- `paper/figures/underwater_method_overview_simple.mmd`

如果是继续整理文献或知识库：

- 先看本地 `related-work-underwater-enhancement.md`
- 再看 `research-log.md` 里最近的写作与同步记录
- 只有在需要补新论文、核对元数据或继续同步结构化页面时，再回到 Zotero / Notion

### 11.4 新线程默认遵守的工作约定

- 不要默认重跑整套 `full506`；先检查现有 `selection.json`、`analysis.md` 和结果目录
- 不要把 `main.py` 默认参数直接改成当前锁定配置，除非明确决定把它升格为主默认入口
- 结果命名、阶段目录和配置字段里继续沿用历史名 `RGHS / CLAHE`
- 说明文档、阶段结论、接受 winner 与后续计划，优先回写到 README 和对应实验分析文档
- 若要继续同步 Notion，以本地已确认文档为源，不要让 Notion 反过来覆盖本地结论

### 11.5 当前最自然的后续方向

- 实验方向：
  - 若继续调参，优先重开 `Fusion`，并把 `UCIQE / UIQM` 退化纳入硬约束
- 写作方向：
  - 继续把 method 精简稿扩成论文正文
  - 将 related work 与 method 图正式接入论文主稿
- 知识库方向：
  - 继续把新的阶段总结、实验记录和写作页同步到 Notion
  - 文献库 `Concepts` 多选标签仍是后续可补但不阻塞主线的尾项

## 12. 当前下一步

当前 H2 顺序调参已完成一次 `full506` 收口，README 中已接受：

- `RGHS = rghs_s07`
- `CLAHE = clahe_s05`
- `Fusion = fusion_s10`

若继续沿当前主线推进，后续更合理的方向是：

1. 若继续调参，优先只重开 `Fusion`
   - 当前 `fusion_s10` 在 `MS_SSIM / PSNR` 上提升明显
   - 但 `UCIQE / UIQM` 回撤过大，后续应把视觉项退化纳入硬约束或 guardrail
2. 如需继续整理主线：
   - 维护 `locked_full506_final_mainline.json` 与 `full506_final_mainline` 的正式别名关系
   - 如有新一轮接受结果，再生成新的统一锁定配置与正式结果别名
   - 仍避免直接改写 `main.py` 默认入口，除非明确决定升格为主默认配置
3. 如需提高可读性：
   - 可在后续单独整理 `RGHS / CLAHE / Fused / Final` 的历史遗留命名
   - 同步更新 README、实验分析文档和研究日志中的显示名
