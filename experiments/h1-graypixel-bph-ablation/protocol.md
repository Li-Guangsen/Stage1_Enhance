# H1 白平衡调参协议 v2

## 目标

在不改 `IMF1Ray / fusion / final` 逻辑的前提下，单独优化 `lgs_accc_bgr_improved()` 的 `bph` 参数，目标是提升 `full506` 主实验上的综合分，同时保住结构护栏并检查颜色稳定性。

## 本轮锁定条件

- 正式数据：`data/inputImg/Original` 全量 506 张
- 探索集：新建 `data/eval_subset_explore64_full506_bph_v1.txt`
- 下游固定：
  - `imf1ray` 保持当前默认调用方式
  - `rghs` 保持默认
  - `clahe` 保持默认
  - `fusion` 固定为 `{}`
  - `final` 固定为 [`best_full506_r4_03.json`](D:/Desktop/Stage1Codex/experiments/optimization_v1/configs/best_full506_r4_03.json) 中的 `final`
- 唯一变化项：`params-json` 中的 `bph`
- `pilot92` 不参与本轮参数决策，只保留为历史调试集

## 优化目标与护栏

- 主排序：综合分
- 结构护栏：
  - `MS-SSIM` 相对 baseline 下降不超过阈值
  - `PSNR` 相对 baseline 下降不超过阈值
- 颜色稳定性：通过 `visual_diagnostics.py` 抽样人工复核

## explore64 构造规则

- 基于 `Original` 原图的三个统计量分层抽样：
  - 平均亮度 `Y_mean`
  - 亮度标准差 `Y_std`
  - 平均色度幅值 `mean(sqrt((a-128)^2+(b-128)^2))`
- 每个统计量按 tertile 划分为 `low / mid / high`
- 形成 27 个桶，按桶轮转抽样，直到 64 张
- 不足部分按全局排序补齐
- 固定 `seed=20260413`

## Round 1：单因素粗搜

在 `explore64` 上运行 13 个候选：

1. `bph00_baseline`
2. `bph10_gp_strict`
3. `bph11_gp_mid`
4. `bph12_gp_loose`
5. `bph13_gp_narrow_mid`
6. `bph20_pregain_conservative`
7. `bph21_pregain_mid`
8. `bph22_pregain_aggressive`
9. `bph30_accc_conservative`
10. `bph31_accc_mid`
11. `bph32_accc_aggressive`
12. `bph40_brightness_tight`
13. `bph41_brightness_loose`

Round 1 规则：

- baseline：`bph00_baseline`
- 护栏：
  - `MS-SSIM` 相对 baseline 下降超过 `0.015` 直接淘汰
  - `PSNR` 相对 baseline 下降超过 `0.20 dB` 直接淘汰
- 每个参数家族仅保留 1 个优胜者；若该家族无合格候选，则沿用 baseline 默认值
- 对综合分前 4 名生成 8 张抽样诊断图

## Round 2：组合细搜

基于 Round 1 家族优胜者，在 `explore64` 上运行组合候选：

1. `r2_00_baseline`
2. `r2_01_G`
3. `r2_02_G_P`
4. `r2_03_G_A`
5. `r2_04_G_P_A`
6. `r2_05_G_P_A_B`
7. `r2_06_G2_P_A_B`
8. `r2_07_G_P2_A_B`
9. `r2_08_G_P_A2_B`

若“次优”与已选配置完全重复，则跳过重复项，不强行补新候选。

Round 2 规则：

- baseline：`r2_00_baseline`
- 护栏同 Round 1
- 保留综合分前 3 且满足护栏的候选进入 `full506`
- 对 `baseline + top3` 生成 12 张抽样诊断图

## Full506 正式评测

正式运行以下方法：

1. `r2_00_baseline`
2. Round 2 top1
3. Round 2 top2
4. Round 2 top3

正式 winner 规则：

- 主排序看综合分
- 必须同时满足：
  - 相对 baseline，`MS-SSIM` 下降不超过 `0.02`
  - 相对 baseline，`PSNR` 下降不超过 `0.20 dB`
  - 抽样诊断中没有明显系统性偏色
- 若无人满足，则结论为：白平衡暂未优于当前默认实现，保持现状

## 编排脚本

新增脚本：

- [`run_bph_search.py`](D:/Desktop/Stage1Codex/experiments/h1-graypixel-bph-ablation/run_bph_search.py)

支持阶段：

- `build-manifest`
- `smoke`
- `round1`
- `round2`
- `full506`
- `all`

所有运行通过现有 conda 环境执行，且长跑统一携带 `--skip-existing`，支持断点续跑。
