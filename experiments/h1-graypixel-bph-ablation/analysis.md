# H1 Analysis

## 当前状态

本轮已完成 H1 白平衡调参编排代码与实验协议更新，目标切换为：

- 正式结论基于 `Original` 全量 506 张
- 探索阶段使用新的 `explore64` 分层抽样子集
- 下游固定为当前 `r4_03` 配置
- 本轮只调 `bph`，不联调 `imf1ray / fusion / final`

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
   - `full506`：`MS-SSIM` 降幅 `<= 0.02`，`PSNR` 降幅 `<= 0.20 dB`

## 待运行阶段

1. `build-manifest`
2. `smoke`
3. `round1`
4. `round2`
5. `full506`

## 输出位置

- 编排总目录：`experiments/h1-graypixel-bph-ablation/outputs`
- `explore64` 统计：`experiments/h1-graypixel-bph-ablation/outputs/explore64_manifest_stats.csv`
- Round 1：`experiments/h1-graypixel-bph-ablation/outputs/round1`
- Round 2：`experiments/h1-graypixel-bph-ablation/outputs/round2`
- Full506：`experiments/h1-graypixel-bph-ablation/outputs/full506`

## 结果判定说明

脚本中的 `metric_winner` 只是“综合分 + 护栏”意义下的机器初选。最终 winner 仍需结合抽样诊断图做人审，确认不存在系统性偏红、偏黄、偏紫等颜色失稳现象。

## smoke 观察

- `bph10_gp_strict` 在 5 张 smoke 样本上相对 baseline 的综合分为 `-0.1750`
- 两者都没有链路级失败
- `RGHS.py` 在 Lab 转 RGB 时出现少量 `negative Z clipped to zero` 警告，但不影响本轮 BPH 编排执行；后续若诊断图显示异常偏色，再回头单独排查该分支
