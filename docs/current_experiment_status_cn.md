# 当前实验状态与停止点

更新时间：2026-05-26

本文件是 Stage1Codex 当前实验状态的一页式事实入口。它用于阻止后续 agent 把弱候选、proxy、readiness 或 2770 资产准备误写成目标完成。

## 当前执行优先级

当前优先级是实验治理与候选归档，而不是继续派生新的 `Pxx/Dxx` 候选。新增候选前必须先完成 method review、run sheet、isolated output root、config、log、status 和 decision。

## 已锁定事实

- 旧 Stage1 `Final` 在 fixed DiffusionEdge baseline 50k 和 fixed MSFI 50k 下会明显损伤下游边缘检测，已经作为 legacy negative baseline 固定。
- Raw 输入是当前 fixed-detector 下游验证的强 anchor。
- P12-P28 是候选、对照、失败或诊断证据集合，不是正式增强主线。
- D01 `d01_structure_flow_v1` 是 `mechanism-complete weak candidate`，不是强通过，不是正式主线，也不能写成 Stage1 稳定提升下游。
- `candidate_rescues_legacy_but_not_near_raw`、`candidate_metric_near_raw_structure_mixed` 都不能标记为目标完成。
- 2770 full-pool readiness 只说明工程入口可准备，不等于 downstream validation。

## 数据口径

| 口径 | 当前用途 | 不能替代什么 |
| --- | --- | --- |
| 168 张带 GT split | fixed DiffusionEdge/MSFI 下游验证核心口径 | 不能被 502/496 或 2770 替代 |
| full502_clean_v1 | Stage1 正式小口径增强指标、阶段输出和历史主线资产 | 不能替代下游边缘验证 |
| compare9_complete496_v1 | 与外部增强方法 complete-case 对照 | 不能替代下游边缘验证 |
| 2770/cv2-readable full-pool | 工程稳定性、qualitative pool、后续可选全量增强 | clean protocol 未冻结前不能作为正式统计结果 |

## 当前停止点

在没有新的 method review 和 run sheet 前，不应继续创建 P29/D02 或同族 guard/fallback/raw-pullback 变体。下一步应先审计已有 P12-P28/D01 的生命周期状态，决定归档、重构或停止。
