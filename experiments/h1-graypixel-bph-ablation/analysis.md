# H1 分析

## 当前状态

本轮已完成 H1 白平衡 `full506` 正式评测与结果收口，当前结论为：

- 正式结论基于 `Original` 全量 `506` 张
- `full506` 完成 `506/506 complete-case`，`failed=0`
- 自动 `metric_winner` 为 `r2_02_G_P`
- 人工最终锁定 winner 为 `r2_05_G_P_A_B`
- 三个白平衡候选相对 baseline 均通过硬护栏与动态护栏
- 本轮抽看诊断图未见明显系统性偏色；考虑到后续要把赢家直接作为前置白平衡配置，当前改为人工锁定 `r2_05_G_P_A_B`，理由是它相对 baseline 同时提升 `MS-SSIM` 与 `PSNR`，且在“双增”候选里综合分回撤最小

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

| 方法 | 综合分 | MS-SSIM | 相对 baseline | PSNR | 相对 baseline | 硬护栏 | 动态护栏 |
|---|---:|---:|---:|---:|---:|---|---|
| `r2_00_baseline` | `0.0000` | `0.700122` | `0.000000` | `16.084406` | `0.000000 dB` | `pass` | `pass` |
| `r2_02_G_P` | `0.0221` | `0.699999` | `-0.000122` | `16.104605` | `+0.020199 dB` | `pass` | `pass` |
| `r2_05_G_P_A_B` | `-0.0413` | `0.701150` | `+0.001028` | `16.116002` | `+0.031596 dB` | `pass` | `pass` |
| `r2_08_G_P_A2_B` | `-0.1201` | `0.700453` | `+0.000331` | `16.102306` | `+0.017901 dB` | `pass` | `pass` |

当前排序：

1. `r2_02_G_P`
2. `r2_00_baseline`
3. `r2_05_G_P_A_B`
4. `r2_08_G_P_A2_B`

补充说明：

- `summary.txt` / `summary.json` 显示四套方法均为 `Count: 506`
- `failed_files.csv` 只有表头，无实际失败样本
- `selection.json` 记录的 `metric_winner` 为 `r2_02_G_P`
- `selection.json` 同时补充记录了人工锁定结果：`final_winner = r2_05_G_P_A_B`
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

脚本中的 `metric_winner` 是“综合分 + 护栏”意义下的机器初选，因此自动结果仍是 `r2_02_G_P`。但本轮人工决策不再单纯按综合分锁定，而是优先选择“相对 baseline 同时提升 `MS-SSIM` 与 `PSNR`”的候选，并要求综合分回撤保持可接受。在这个口径下：

- `r2_05_G_P_A_B`：`MS-SSIM` 与 `PSNR` 均优于 baseline，且在双增候选里综合分回撤最小
- `r2_08_G_P_A2_B`：同样双增，但综合分回撤更大
- `r2_02_G_P`：综合分最佳，但 `MS-SSIM` 较 baseline 有极小回落

因此，本项目当前人工最终锁定 `r2_05_G_P_A_B` 为 H1 白平衡正式胜者；后续若继续做上游白平衡相关调参，默认以该配置作为前置白平衡基线。

## 主链路锁定配置

为避免后续继续推进时反复手动拼接“上游白平衡 + 下游细化”参数，当前已补充显式锁定的主链路配置文件：

- `experiments/optimization_v1/configs/locked_full506_mainline.json`

同时，已将当前确认结果复制到正式命名的结果目录：

- `experiments/h1-graypixel-bph-ablation/outputs/full506/runs/full506_locked_mainline`
- `experiments/h1-graypixel-bph-ablation/outputs/full506/candidate_params/full506_locked_mainline.json`

该文件表示的组合是：

- `bph`：采用 H1 人工最终锁定 winner `r2_05_G_P_A_B`
- `fusion/final`：采用当前 full506 下游固定配置 `r4_03`

补充说明：

- 该锁定文件与正式命名的结果副本用于主线复现与后续文档统一引用，不代表新增实验结论
- 历史候选名 `r2_05_G_P_A_B` 仍保留在评测表、诊断索引和原始结果树中，用于审计与回溯
- 当前不会自动修改 `main.py` 的默认参数入口；如需按主线锁定组合运行，应显式传入该 `params-json`

## smoke 观察

- `bph10_gp_strict` 在 5 张 smoke 样本上相对 baseline 的综合分为 `-0.1750`
- 两者都没有链路级失败
- `wb_safe_contrast.py`（旧 `RGHS.py`）在 Lab 转 RGB 时出现少量 `negative Z clipped to zero` 警告，但不影响本轮 BPH 编排执行；后续若诊断图显示异常偏色，再回头单独排查该分支
