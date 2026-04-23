# 项目交接指南（中文）

更新时间：2026-04-24

本文件面向第一次接手本仓库的人类或 AI。目标是用一份文档回答五个问题：

1. 这个项目现在做到哪一步了
2. 我们的方法当前正式锁定到什么版本
3. 正式结果和对比方法分别放在哪里
4. 当前论文口径怎么解释这些结果
5. 下游还怎么接、后续最重要的任务是什么

## 1. 项目目标与当前状态

当前项目对象是有害藻华水下显微图像，不是一般自然场景水下增强。

当前项目的正式目标是：

- 形成一条可复现、可引用、口径统一的正式增强主线
- 产出阶段进度表和外部主比较表
- 让论文主稿、状态文档和结果目录统一引用同一套正式结果

当前阶段可以概括为：

- 正式主线已锁定
- 正式阶段表已跑出
- 正式 `9` 方法主比较表已跑出
- 论文底稿、证据包和对比方法索引已基本成形
- 仍待补投稿闭环证据，尤其是下游边缘验证、paper-ready 图组和数据/运行说明

当前写作语言工作的默认重心先放在中文主稿；英文 outline、英文 related work 草稿和 Markdown-to-DOCX 工具主要作为辅助资产保留，而不是当前收口的主战场。

## 1.1 文档分工

为避免后续 README、状态快照和结果索引重复冲突，当前仓库按下面这套职责维护：

| 文档 | 当前职责 |
| --- | --- |
| `README.md` | 项目总入口，只讲正式口径、正式结果入口、阅读顺序和当前缺口 |
| `docs/project_handoff_guide_cn.md` | 交接主文档，面向新接手的人类或 AI 做全景说明 |
| `docs/project_status_overview_cn.md` | 正式状态快照，记录当前研究进度与仍缺证据 |
| `docs/comparison_methods_results_index_cn.md` | 主表、对比方法路径、处理策略和结果索引 |
| `research-state.yaml` | 结构化状态源，便于后续程序化读取与同步 |

## 2. 我们的方法怎么落地

当前正式增强链路为：

`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`

### 2.1 阶段与实现文件

| 阶段名 | 真实职责 | 关键实现文件 | 当前锁定结果 |
| --- | --- | --- | --- |
| `BPH` | 稳态前置白平衡入口 | `lgsbph.py` | `r2_05_G_P_A_B` |
| `IMF1Ray` | 高频细节与边缘响应分支 | `pybemd.py` | `locked existing output` |
| `RGHS` | 白平衡安全对比分支 | `wb_safe_contrast.py` | `rghs_s07` |
| `CLAHE` | CLAHE 引导的局部可见性分支 | `clahe_guided_visibility.py` | `clahe_s05` |
| `Fused` | 三分支亮度域特征门控融合 | `fusion_three.py` | `fusion_s10` |
| `Final` | 轻量照明与对比收口 | `lvbo.py` | `r4_03 / homomorphic_entropy` |

### 2.2 命名边界

需要特别注意：

- `RGHS` 与 `CLAHE` 是历史阶段名
- 论文里不能把它们直接照抄成“标准 RGHS 模块”或“普通 CLAHE 输出”
- 代码层更应该按真实职责理解：
  - `RGHS` = 白平衡安全对比增强
  - `CLAHE` = CLAHE 引导的局部可见性增强

### 2.3 当前正式主线入口

- 正式配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 正式结果副本：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 正式最终输出目录：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`

需要再强调一次：

- 当前正式主线不是“直接运行默认 `main.py`”
- 正式跑图时必须显式传 `--params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json`
- 当前不会把 `main.py` 默认入口改写成正式主线，避免历史流程与正式流程混在一起

## 3. 正式结果与数据口径

### 3.1 正式阶段口径

- manifest：`metrics/manifests/full502_clean_v1.txt`
- count：`502`
- 用途：阶段进度表
- 正式输出：`metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`

### 3.2 正式主表口径

- manifest：`metrics/manifests/compare9_complete496_v1.txt`
- count：`496`
- 用途：`Ours + 8 baselines` 的 complete-case 主比较表
- 正式输出：`metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`

### 3.3 为什么主表是 496

原因不是我们只想挑样本，而是：

- 7 个外部方法覆盖清洗后的 `502` 张输入
- `WWPF` 官方包只稳定输出 `496` 张
- 为避免不同方法按不同样本均值比较，正式主表统一采用 `496` 张 complete-case 交集

### 3.4 正式结果相关脚本

- 方法注册表：`metrics/configs/official_method_registry.json`
- manifest 生成：`metrics/scripts/build_official_manifests.py`
- 正式评测脚本：`metrics/scripts/run_official_evaluations.ps1`

这里要区分“读结果”和“重跑结果”：

- 当前仓库已经保存 `official_stage_progress_full502` 和 `official_compare9_complete496`，因此新接手者可以直接阅读正式数值结果
- 但如果要在本机重跑 `official_compare9_complete496`，仍依赖 `official_method_registry.json` 中登记的外部方法结果目录
- 这些外部方法目录目前是当前工作站上的绝对路径资产，不随本仓库本身打包分发
- 换句话说：主表是可读的，但 complete-case 主比较不保证在任意新机器上开箱即重跑

### 3.5 当前增强与评测环境

当前仓库还没有统一覆盖全部历史脚本的环境说明；下面这条说明只适用于当前正式增强与正式评测。

- conda 根目录：`D:\miniconda3`
- 当前增强与评测环境：`D:\Desktop\EdgeDetection\my_env`

推荐的交互式启动方式：

```bat
cmd.exe /K "D:\miniconda3\Scripts\activate.bat D:\Desktop\EdgeDetection\my_env"
```

推荐的一次性运行方式：

```bat
cmd.exe /D /S /C "call D:\miniconda3\Scripts\activate.bat D:\Desktop\EdgeDetection\my_env && python main.py --params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json"
```

当前已确认这条环境链路可以完成：

- 用 `locked_full506_final_mainline.json` 跑 `main.py`
- 用 `metrics/evaluate_protocol_v2.py` 跑 protocol-v2 评测
- 用 `metrics/scripts/run_official_evaluations.ps1` 触发正式评测入口

换句话说，这是一条已经通过 smoke 验证的“当前增强 + 当前评测”环境，不应自动外推到仓库里所有历史实验脚本。

### 3.6 新接手者的 5 分钟 sanity check

如果你只是想确认环境和主线没有跑偏，建议按这个顺序：

1. 激活环境

```bat
cmd.exe /K "D:\miniconda3\Scripts\activate.bat D:\Desktop\EdgeDetection\my_env"
```

2. 跑 1 张图的正式主线 smoke

```bat
python main.py --limit 1 --params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json --output-dir .tmp_smoke_env\results
```

3. 跑 1 张图的 protocol-v2 smoke

```bat
python metrics\evaluate_protocol_v2.py --quiet --limit 1 --original-dir data\inputImg\Original --result-dir .tmp_smoke_env\results\png\Final --method-name smoke_official_env --output-dir .tmp_smoke_env\eval
```

4. 清理临时目录 `.tmp_smoke_env`

如果你要重跑正式评测，则用：

```bat
powershell -ExecutionPolicy Bypass -File metrics\scripts\run_official_evaluations.ps1
```

但要先知道一件事：

- 该脚本会先重建正式 manifest
- 然后覆盖 `official_stage_progress_full502`
- 同时覆盖 `official_compare9_complete496`

## 4. 对比方法路径与处理策略

### 4.1 外部方法路径总表

| 方法 | 分类 | 输出目录 | 当前样本数 | 备注 |
| --- | --- | --- | ---: | --- |
| `HVDualformer` | 深度白平衡 | `D:\Desktop\2025AAAI_HVDual_former\lgsresults` | 502 | 白平衡方法，实验节保留 |
| `ABC-Former` | 深度白平衡 | `D:\Desktop\2025CVPR_ABC-Former\ABC-Former\lgsresults` | 502 | 白平衡方法，实验节保留 |
| `GDCP` | 传统/非深度水下增强 | `D:\Desktop\2018_Generalization-of-the-Dark-Channel-Prior\lgsresults` | 502 | 物理先验恢复 |
| `CBF` | 传统/非深度水下增强 | `D:\Desktop\2018_Color-Balance-and-fusion-for-underwater-image-enhancement\lgsresult` | 502 | 经典融合 |
| `HLRP` | 传统/非深度水下增强 | `D:\Desktop\2022_HLRP-main\HLRP_Code\lgsresult` | 502 | Retinex 变分优化 |
| `SGUIE-Net` | 深度水下增强 | `D:\Desktop\2022_SGUIE_Net_Simple\lgsresults` | 502 | 语义注意力增强 |
| `Histoformer` | 深度水下增强 | `D:\Desktop\2024_Histoformer-main\lgsresults` | 502 | 直方图 Transformer |
| `WWPF` | 传统/非深度水下增强 | `D:\Desktop\2024_WWPF_code\2023-WWPE\datasets\lgsresults` | 496 | 官方包只稳定输出 496 张 |

补充边界：

- 这些目录是当前工作站上的外部结果资产，而不是仓库内自带的相对路径资源
- 因此，新接手者即使能直接阅读正式主表，也不一定能在另一台机器上立即重跑外部方法 complete-case 比较
- 若要迁移到新机器，优先迁移的是这些结果目录或重新生成同名结果，而不是只复制仓库正文文件

更详细的论文名、主表数值和结论边界，直接看：

- `docs/comparison_methods_results_index_cn.md`

### 4.2 当前主表解释策略

当前正式主表保留全部 `9` 方法，不删方法，不改数值口径。

正文叙述时统一采用下面这套策略：

- `WWPF` 保留在主表中，作为激进但可接受的强基线
- `HLRP` 与 `Histoformer` 的数值保留在正式主表中，但正文层面按失败案例或补充分析处理
- `HVDualformer` 与 `ABC-Former` 是白平衡方法，不能在 related work 中混写成标准水下增强方法

### 4.3 负面结论的边界

所有负面结论都只适用于当前 HAB 显微图像协议：

- 只表示这些方法在本任务、本数据分布、本地复现实验条件下的适配性不同
- 不表示原论文方法在一般自然场景水下增强问题上无效

## 5. 当前论文口径怎么解释结果

### 5.1 指标解释

当前论文中：

- `MS_SSIM` 与 `PSNR` 表示增强结果相对原图的结构一致性
- 它们不是相对增强真值的质量指标
- 高 `MS_SSIM/PSNR` 更接近“改动保守、与原图相近”，不等于“增强更强”

### 5.2 当前结果的稳妥结论

当前更稳妥的写法是：

- 我们的方法不是与原图最接近的保守方案
- 但在当前 HAB 显微图像协议下，它在增强收益与结构稳定性之间取得了更均衡的表现

不应写成：

- “全面领先外部 SOTA”
- “所有指标最优”
- “HLRP/Histoformer 原方法无效”

## 6. 下游衔接

当前论文里“边缘友好 / 结构可读性”的叙事，还没有被正式下游验证总表完全闭环。

当前建议把未来下游验证理解成一份明确的 `planned downstream handoff contract`，而不是一句泛泛的“后面再做”。

### 6.1 未来下游验证的固定输入

- 正式输入增强结果：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`
- 正式输入原图：`data/inputImg/Original`
- 正式样本清单：`metrics/manifests/full502_clean_v1.txt`

### 6.2 未来下游验证的推荐输出位置

- 推荐输出目录：`metrics/outputs/downstream_edge_validation/official_full502_mainline`

这里的“推荐输出目录”只是未来交接接口，不表示该结果目前已经存在。

### 6.3 未来下游验证至少要产出的文件

- 一份汇总表：`summary.md` 或 `summary.csv`
- 一份逐图结果表：`per_image_metrics.csv`
- 一份 manifest 副本或清晰的 manifest 引用说明
- 一段方法说明，写清比较的是 `Original` vs `Ours Final`

### 6.4 这一步的作用

换句话说：

- 当前阶段已经不缺正式增强主表
- 当前真正缺的是“增强结果如何支撑下游任务”的正式闭环
- 当前主表已经闭环，下游边缘验证还没有闭环
- 这一步是未来任务，不是当前已完成事实

## 7. 后续任务清单

### 7.1 必须补

- 下游边缘验证总表
- 数据采集条件、覆盖范围和公开性说明
- 运行时间与资源说明

### 7.2 应补

- paper-ready 的 representative qualitative panel
- `WWPF / HLRP / Histoformer` 相关失败案例图组
- 投稿版主表结果分析图或排序图

### 7.3 可选

- 进一步 reopen `Fusion`

前提是：

- 必须引入视觉 guardrail
- 不能只追求 `MS_SSIM/PSNR`
- 必须同时约束 `UCIQE/UIQM` 的明显回撤

## 8. 不应误解的边界

- 当前项目对象是有害藻华水下显微图像，不是一般自然场景水下增强
- 当前正式主线是 `locked_full506_final_mainline.json` 对应的正式结果副本，不是旧 `c25`
- 当前正式主表口径是 `compare9_complete496_v1`，不是历史 `full506`
- 当前不是“还没统一评测”，而是“正式主表已形成、但下游闭环和投稿级图组/说明仍未补齐”
- `MS_SSIM/PSNR` 是结构一致性，不是增强真值质量
- `WWPF` 保留主表
- `HLRP/Histoformer` 只在当前 HAB 显微协议下视为失败案例或补充分析
- 这些结论不构成对原论文方法在其他场景中的否定

## 9. 继续阅读建议

如果你要继续推进论文或实验，推荐阅读顺序：

1. `docs/project_status_overview_cn.md`
2. `docs/comparison_methods_results_index_cn.md`
3. `research-state.yaml`
4. `paper/underwater_image_enhancement_draft_cn.md`
5. `paper/underwater_image_enhancement_evidence_pack_cn.md`

如果你要继续推进代码或下游实验，再看：

- `main.py`
- `lgsbph.py`
- `pybemd.py`
- `wb_safe_contrast.py`
- `clahe_guided_visibility.py`
- `fusion_three.py`
- `lvbo.py`

## 10. 历史资产怎么看

以下内容属于历史搜索、旧口径或归档资产：

- `results_optimized_c25`
- 旧 `full506` 评测输出
- `metrics/archive/`

这些内容可以用于回看和审计，但不再作为正式论文入口。
