# H2 RGHS/CLAHE/Fusion 顺序优化

- **Notion URL**: https://www.notion.so/344bb1f4e23e8154a98bca37f9ee96a3
- **Ancestor Path**: 水下图像增强项目主页 / 实验记录
- **Exported On**: 2026-04-17

## Properties
- **配置路径**: experiments/h2-full506-direct/analysis.md ; experiments/optimization_v1/configs/locked_full506_final_mainline.json
- **结果摘要**: H2 full506 直跑调参已完成；当前接受 winner 为 RGHS=rghs_s07、CLAHE=clahe_s05、Fusion=fusion_s10，并已固化为 locked_full506_final_mainline.json。
- **阶段**: 消融
- **状态**: 已完成
- **日期**: 2026-04-16
- **实验名称**: H2 RGHS/CLAHE/Fusion 顺序优化

## Content
# H2 full506 直跑调参
## 当前状态
- 总状态：`completed`
- 基线配置：`experiments/optimization_v1/configs/locked_full506_mainline.json`
- 当前接受统一配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 当前正式结果目录：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 当前正式评测目录：`experiments/h2-full506-direct/outputs/full506/eval`
## 当前接受 winner
- `RGHS = rghs_s07`
- `CLAHE = clahe_s05`
- `Fusion = fusion_s10`
## 阶段结论
### RGHS
- winner：`rghs_s07`
- 参数文件：`experiments/h2-full506-direct/configs/rghs/rghs_s07.json`
- 官方胜出：ΔMS-SSIM=`0.09836`，ΔPSNR=`1.57805 dB`，ΔUCIQE=`0.06798`，ΔUIQM=`-4.30762`
### CLAHE
- winner：`clahe_s05`
- 参数文件：`experiments/h2-full506-direct/configs/clahe/clahe_s05.json`
- 官方胜出：ΔMS-SSIM=`0.03508`，ΔPSNR=`0.72397 dB`，ΔUCIQE=`0.02273`，ΔUIQM=`-1.11937`
### FUSION
- winner：`fusion_s10`
- 参数文件：`experiments/h2-full506-direct/configs/fusion/fusion_s10.json`
- 官方胜出：ΔMS-SSIM=`0.06751`，ΔPSNR=`1.43617 dB`，但 `UCIQE / UIQM` 出现明显回撤
## 当前解释
当前 H2 的结论不是三层联调，而是在固定上游 `BPH / IMF1Ray` 的前提下做顺序优化：先选 `RGHS`，再选 `CLAHE`，最后选 `Fusion`。其中 `fusion_s10` 在结构相关指标上提升明显，但视觉项回撤较大，因此如果后续继续开 H2，最优先重开的应当是 Fusion 阶段，并把视觉项退化纳入更强硬的护栏。
## 关键文件
- 分析文档：`experiments/h2-full506-direct/analysis.md`
- 最终状态：`experiments/h2-full506-direct/selection.json`
- 主线锁定配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
