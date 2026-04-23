# 项目当前状态总览（中文）

更新时间：2026-04-24

## 1. 项目目标

当前项目目标是面向有害藻华水下显微图像，形成一条可复现、可引用、口径统一的正式增强主线，并用统一协议完成：

- 主线阶段进度评测
- 我们的方法与 8 个外部对比方法的公平比较
- 与论文主稿一致的项目状态和方法索引文档

## 2. 正式主线

当前唯一正式配置：

- 配置文件：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 正式结果副本：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 正式评测入口：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png`

正式运行提醒：

- 当前正式主线必须显式传 `locked_full506_final_mainline.json`
- 直接运行 `main.py` 默认参数不会自动落到当前正式论文主线
- 当前保持 `main.py` 默认入口不变，只把正式入口单独锁定到正式配置与正式结果副本

正式主线阶段组合为：

- `BPH = r2_05_G_P_A_B`
- `IMF1Ray = locked existing output`
- `RGHS = rghs_s07`
- `CLAHE = clahe_s05`
- `Fusion = fusion_s10`
- `Final = r4_03 / homomorphic_entropy`

## 3. 当前结论

### H1

- 白平衡主线已经锁定为 `r2_05_G_P_A_B`
- 当前最稳表述是“稳态前置白平衡入口”，而不是单独的最终观感增强模块

### H2

- 顺序锁定结果已经完成：
  - `RGHS = rghs_s07`
  - `CLAHE = clahe_s05`
  - `Fusion = fusion_s10`
- 当前最有辨识度的代码级创新仍是三分支职责分离与亮度域特征门控融合

### H3

- 最终收口固定为 `r4_03 / homomorphic_entropy`
- 该阶段当前应写成稳定收口层，不应过度写成主要创新

## 4. 正式评测协议

### 正式清洁主集

- manifest：`metrics/manifests/full502_clean_v1.txt`
- count：`502`
- 含义：从 `data/inputImg/Original` 清洗出的正式原图集合

### 正式主表口径

- manifest：`metrics/manifests/compare9_complete496_v1.txt`
- count：`496`
- 含义：`Ours + 8 baselines` 的 complete-case 交集

### 正式输出目录

- 阶段进度表：`metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
- 外部对比总表：`metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`

补充边界：

- 当前正式结果目录已经可直接阅读
- 但若要重跑 `official_compare9_complete496`，仍依赖 `metrics/configs/official_method_registry.json` 中登记的外部方法结果目录
- 这些外部方法目录目前是当前工作站上的绝对路径资产，不等于仓库内自带资源

## 5. 阶段进度结果（full502）

来自 `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502/mean_metrics_table.md`：

| Method | Count | EME | EMEE | Entropy | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BPH | 502 | 2.5648 | 0.4398 | 3.8823 | 26.0604 | 2.7963 | 0.9988 | 53.3849 | 2.2208 | 6.9856 |
| IMF1Ray | 502 | 5.1882 | 0.5884 | 4.4209 | 197.6841 | 6.8659 | 0.7724 | 22.1834 | 2.1772 | 12.1591 |
| RGHS | 502 | 10.9913 | 0.9283 | 5.9490 | 301.0964 | 9.9259 | 0.6862 | 14.9905 | 2.0247 | 23.0155 |
| CLAHE | 502 | 9.9239 | 0.8641 | 5.8573 | 214.0305 | 9.0657 | 0.7196 | 16.6094 | 2.2651 | 19.8615 |
| Fused | 502 | 7.4765 | 0.7142 | 5.8658 | 184.7186 | 8.3886 | 0.7571 | 17.9232 | 1.9437 | 17.2491 |
| Final | 502 | 11.5985 | 0.9510 | 5.6563 | 544.5511 | 14.8472 | 0.7689 | 17.5534 | 4.0918 | 23.9227 |

当前可直接使用的解释：

- `Final` 在 `EME/EMEE/Contrast/AvgGra/UCIQE/UIQM` 上相对前序阶段提升明显
- `Fused -> Final` 的主要收益体现在对比与无参考视觉指标整理
- `MS_SSIM/PSNR` 不应被单独解读为“越高越好”，当前项目更关注结构可读性与综合增强表现

## 6. 仍缺证据

- 仍缺与当前正式主线严格对齐的下游边缘验证总表
- 仍缺 paper-ready 的代表性 qualitative panel、失败案例与运行时间说明
- 仍缺数据采集条件、覆盖范围和公开性说明

### planned downstream handoff contract

这部分是未来下游验证的推荐接口，不表示当前已经有结果：

- 正式输入增强结果：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`
- 正式输入原图：`data/inputImg/Original`
- 正式样本清单：`metrics/manifests/full502_clean_v1.txt`
- 推荐输出目录：`metrics/outputs/downstream_edge_validation/official_full502_mainline`
- 最低产物集合：
  - `summary.md` 或 `summary.csv`
  - `per_image_metrics.csv`
  - manifest 副本或 manifest 引用说明
  - 一段写清 `Original` vs `Ours Final` 的方法说明

## 7. 入口索引

- 方法注册表：`metrics/configs/official_method_registry.json`
- manifest 生成：`metrics/scripts/build_official_manifests.py`
- 正式运行脚本：`metrics/scripts/run_official_evaluations.ps1`
- 正式阶段结果：`metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
- 正式对比结果：`metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`
