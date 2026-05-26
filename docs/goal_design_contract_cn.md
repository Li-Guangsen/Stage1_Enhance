# 目标设计契约

更新时间：2026-05-26

本文件定义 Stage1 downstream-driven 任务里什么算完成，什么只能算诊断。它优先级高于聊天中的宽泛长期目标。

## 不能标记为完成的情况

以下状态都不能写成目标完成或正式增强主线：

- `candidate_rescues_legacy_but_not_near_raw`
- `candidate_metric_near_raw_structure_mixed`
- `mechanism-complete weak candidate`
- proxy-only result
- readiness-only result
- 只接近 raw，但没有可解释增强强度、消融和 downstream 证据
- 只在一个 detector 上涨点，另一个 detector 出现 AP、AC、false-edge、endpoints 或 F1 proxy 崩坏
- 2770 full-pool 只跑通，但 168 fixed-detector 没有 strong/pass 证据

## 最低完成条件

一个候选最多只能标为阶段性完成，除非同时满足：

1. 有明确 method design，不是继续小修小补。
2. 有完整 run sheet，包含 hypothesis、code entry、config、input split、output root、commands、runtime、metrics、stop condition 和 decision。
3. 168 张带 GT split 完成 fixed DiffusionEdge/MSFI downstream validation。
4. 结果包含 ODS/OIS/AP/AC、结构 proxy、false-edge ratio、endpoints、F1 proxy 和 visual notes。
5. 与 raw、legacy Stage1 Final、当前最好候选都有明确比较。
6. 结论写清楚属于最低通过、候选通过、强通过还是失败。
7. 证据路径落到 manifest、run report、eval/show log、结果表、结构 proxy 和状态文档。

## Gate 语义

- 最低通过：相对 legacy Final 显著恢复，两个 detector 都不崩。
- 候选通过：至少一个 detector 达到 raw-near 或优于 raw，另一个 detector 无明显 AP/AC/结构 proxy 崩坏。
- 强通过：两个 detector 都 raw-near 或优于 raw，且 false-edge ratio、endpoints、F1 proxy 不劣于 raw。
- 失败：没有恢复 legacy 损伤、任一 detector 崩坏、只提升视觉指标但 downstream 变差，或参数/机制不可解释。

失败候选也必须记录，不能删除、覆盖或用下一轮结果掩盖。
