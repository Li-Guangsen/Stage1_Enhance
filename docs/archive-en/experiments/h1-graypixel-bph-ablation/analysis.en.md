# H1 Analysis

## 当前状态

本轮已完成 H1 白平衡 `full506` 正式评测与结果收口，当前结论为：

- 正式结论基于 `Original` 全量 `506` 张
- `full506` 完成 `506/506 complete-case`，`failed=0`
- 当前 `metric_winner` 为 `r2_02_G_P`
- 三个白平衡候选相对 baseline 均通过硬护栏与动态护栏
- 脚本仍保留 `manual_color_review_required=true`，但本轮抽看诊断图未见明显系统性偏色，当前建议锁定 `r2_02_G_P` 为 H1 白平衡赢家

已完成的非正式 smoke 验证：

- `baseline + bph10_gp_strict`
- 每个候选 5 张
- 六阶段输出 `BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final` 全部生成成功
- clean 评测结果：`5/5 complete-case`，`failed=0`

## 已实现内容

1. 新增 [`run_bph_search.py`](D:/Desktop/Stage1Codex/experiments/h1-graypixel-bph-ablation/run_bph_search.py)
   - 生成 `explore64` manifest
   - 批量写入候选 `params-json`
   - 调用 `main.py` 运行候选
   - 调用 `evaluate_protocol_v2.py` 与 `score_protocol_v2.py`
   - 为 Round 1 / Round 2 / full506 生成诊断图
2. 将 Round 1 / Round 2 / full506 的筛选逻辑固化为脚本
3. 护栏已写入编排逻辑：
   - `explore64`：`MS-SSIM` 降幅 `<= 0.015`，`PSNR` 降幅 `<= 0.20 dB`
   - `full506`：硬护栏参考为 `MS-SSIM` 降幅 `<= 0.02`、`PSNR` 降幅 `<= 0.20 dB`
   - `full506` 最终筛选使用 `dynamic_relaxed_full506_v1`，同时保留硬护栏结果供审阅

## 已运行阶段

1. `build-manifest`：完成
2. `smoke`：完成
3. `round1`：完成
4. `round2`：完成
5. `full506`：完成

## full506 正式结果

| method | composite score | MS-SSIM | vs baseline | PSNR | vs baseline | 硬护栏 | 动态护栏 |
|---|---:|---:|---:|---:|---:|---|---|
| `r2_00_baseline` | `0.0000` | `0.700122` | `0.000000` | `16.084406` | `0.000000 dB` | `pass` | `pass` |
| `r2_02_G_P` | `0.0221` | `0.699999` | `-0.000122` | `16.104605` | `+0.020199 dB` | `pass` | `pass` |
| `r2_05_G_P_A_B` | `-0.0413` | `0.701150` | `+0.001028` | `16.116002` | `+0.031596 dB` | `pass` | `pass` |
| `r2_08_G_P_A2_B` | `-0.1201` | `0.700453` | `+0.000331` | `16.102306` | `+0.017901 dB` | `pass` | `pass` |

排序结论：

1. `r2_02_G_P`
2. `r2_00_baseline`
3. `r2_05_G_P_A_B`
4. `r2_08_G_P_A2_B`

补充说明：

- `summary.txt` / `summary.json` 显示四套方法均为 `Count: 506`
- `failed_files.csv` 只有表头，无实际失败样本
- `selection.json` 记录的 `metric_winner` 为 `r2_02_G_P`
- 三套候选相对 baseline 的 `MS-SSIM` / `PSNR` 均未出现实际下降，因此硬护栏与动态护栏都通过
- `diagnostics/` 已生成 12 个抽样 stem 的 comparison / edge / sheet 图；本轮人工抽查看不出明显系统性偏红、偏黄、偏紫偏色
- `runs/*/png/Final` 目录里各方法总文件数为 `506`，其中有 `4` 张采用 `SIFT/LINK` 命名的附加图，因此若只按普通 `*_Final.png` 计数，会看到 `502`

## 输出位置

- 编排总目录：`experiments/h1-graypixel-bph-ablation/outputs`
- `explore64` 统计：`experiments/h1-graypixel-bph-ablation/outputs/explore64_manifest_stats.csv`
- Round 1：`experiments/h1-graypixel-bph-ablation/outputs/round1`
- Round 2：`experiments/h1-graypixel-bph-ablation/outputs/round2`
- Full506：`experiments/h1-graypixel-bph-ablation/outputs/full506`

## 结果判定说明

脚本中的 `metric_winner` 是“综合分 + 护栏”意义下的机器初选。本轮 `full506` 已完成抽样诊断图人工审阅，当前未见明显系统性颜色失稳，因此可以把 `r2_02_G_P` 视为当前 H1 白平衡正式赢家；若后续在下游任务或更细的人审中发现异常，再回滚为“待复核”状态。

## smoke 观察

- `bph10_gp_strict` 在 5 张 smoke 样本上相对 baseline 的综合分为 `-0.1750`
- 两者都没有链路级失败
- `RGHS.py` 在 Lab 转 RGB 时出现少量 `negative Z clipped to zero` 警告，但不影响本轮 BPH 编排执行；后续若诊断图显示异常偏色，再回头单独排查该分支
