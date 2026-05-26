# 实验停止规则

更新时间：2026-05-26

本文件定义必须暂停的情况。出现以下任一情况，agent 应停止继续派生候选，改为审计、归档或请求重新设计目标。

## 必须停止

- 同一 family 连续出现两个 `candidate_metric_near_raw_structure_mixed` 或 `candidate_rescues_legacy_but_not_near_raw`。
- 新候选只是 guard、fallback、raw-pullback、阈值微调或亮度/色度小改，没有新的机制解释。
- 只得到 raw-near，但增强强度、视觉机制和下游收益都无法形成论文级叙事。
- 代码新增规模明显膨胀，但没有对应 ablation switch、run sheet 和 decision。
- untracked 输出资产快速堆积，且 registry/status 没有同步。
- proxy 指标被当作 fixed-detector 结论。
- 502/496 或 2770 被当作 168 downstream validation 的替代。
- 任务准备结项，但当前 gate 仍是 weak/mixed/proxy/readiness。

## 暂停后的动作

1. 汇总当前 family 的候选、指标和失败机制。
2. 更新 `metrics/experiment_registry.csv` 与 `metrics/candidate_registry.csv`。
3. 在 `research-log.md` 追加停止原因。
4. 只有在新的 method design 和 run sheet 完成后，才能继续实验。
