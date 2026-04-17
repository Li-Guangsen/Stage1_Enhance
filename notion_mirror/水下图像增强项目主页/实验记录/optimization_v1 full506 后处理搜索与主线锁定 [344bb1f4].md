# optimization_v1 full506 后处理搜索与主线锁定

- **Notion URL**: https://www.notion.so/344bb1f4e23e81ba8fbcda37b35b47b6
- **Ancestor Path**: 水下图像增强项目主页 / 实验记录
- **Exported On**: 2026-04-17

## Properties
- **配置路径**: experiments/optimization_v1/configs/best_full506_r4_03.json ; experiments/optimization_v1/configs/locked_full506_mainline.json
- **结果摘要**: 在 full506 上完成四轮后处理/融合细化搜索后，选出 r4_03 作为当前 full506 指标最优配置；随后将 H1 的白平衡 winner 与 r4_03 组合锁定为 locked_full506_mainline.json。
- **阶段**: 主实验
- **状态**: 已完成
- **日期**: 2026-04-13
- **实验名称**: optimization_v1 full506 后处理搜索与主线锁定

## Content
## 结果概览
- 数据规模：506 / 506 complete-case
- 失败数：0
- 当前最优后处理：`r4_03`
- 当前锁定主线：`locked_full506_mainline.json`
## 锁定理由
在 full506 上完成四轮后处理/融合细化搜索后，`r4_03` 在当前指标组合下表现最好，因此被选为当前主线的后处理 winner。随后将 H1 的白平衡 winner 与 `r4_03` 组合，锁定为 `locked_full506_mainline.json`。
## 关键路径
- 最优配置：`experiments/optimization_v1/configs/best_full506_r4_03.json`
- 主线锁定：`experiments/optimization_v1/configs/locked_full506_mainline.json`
