# MyEdge/MSFI Stage1 sidecar adaptation protocol draft

日期：2026-05-27

## 1. 状态

- status: `draft_protocol_not_executed`
- 来源：FA01 family failure audit、high-risk sample index、per-image correlation audit。
- 边界：本文件只是协议草案，不训练 detector，不改 checkpoint，不改 GT，不改 eval protocol，不创建新的 Stage1 candidate。

## 2. 动机

FA01 证明：

- P27/D01 只能通过 near-raw 保住 fixed detector，但不满足完整增强流程目标。
- FF01/FF02 保留完整增强骨架后 fixed detector 明显低于 raw。
- FF02 mean grad ratio 小于 `1` 仍更差，说明不能靠简单压梯度或 raw pullback 解决。

因此，下一条更合理路线不是继续把 Stage1 enhanced image 直接替换 raw input，而是在 MyEdge/MSFI 侧使用 Stage1 作为 sidecar evidence 或 adaptation input。

## 3. 核心假设

Stage1 的完整增强流程仍可能有价值，但价值不在于直接替换 raw 图像，而在于提供：

- weak-boundary visibility evidence；
- color/chroma confidence；
- frequency/detail evidence；
- background false-edge risk map；
- low-frequency illumination consistency map。

MyEdge/MSFI 保留 raw topology 作为主输入，同时读取 Stage1 evidence，才可能既保住 detector distribution，又利用增强流程的创新模块。

## 4. Protocol A：Raw + Stage1 Sidecar

输入：

- raw RGB image；
- Stage1 sidecar maps from FF02-style full flow:
  - BPH/gray-pixel color confidence；
  - IMF/frequency detail evidence；
  - WB-safe contrast evidence；
  - CLAHE local visibility evidence；
  - background risk / false-edge suppression mask。

模型改动：

- raw branch 不变，作为 topology anchor；
- 新增 lightweight sidecar encoder；
- 在 MSFI spatial-frequency weak-boundary diffusion 的 weak-boundary 或 frequency branch 中注入 sidecar evidence；
- fusion 处加入 confidence gate，禁止 sidecar 直接覆盖 raw edge topology。

训练/验证：

- 只在 MyEdge/MSFI repo 单独 run sheet 中执行；
- train split、checkpoint、seed、config、eval protocol 必须全部记录；
- raw-only baseline 必须同轮重跑或引用同轮 anchor；
- 168 fixed-detector 不能再作为 claim 口径，因为 adaptation 已不属于 fixed detector。

Gate：

- candidate pass：MSFI adapted model 在 168 split 上优于 raw-only adapted baseline，且 false-edge/endpoints 不劣化。
- strong pass：weak-boundary subset、high-risk subset 和 overall ODS/OIS/AP/AC 均改善。

## 5. Protocol B：Domain Augmentation

输入：

- raw image；
- P27 near-raw image；
- FF02 full-flow image；
- optional formal Final negative/control image。

训练策略：

- raw 为主；
- P27/FF02 作为 input-domain augmentation，不作为 eval-time 必需输入；
- 加入 consistency loss：raw prediction 与 augmented prediction 在 GT boundary 附近一致，background false-edge 不一致区域受惩罚。

目标：

- 让 detector 对 Stage1-style distribution shift 更稳；
- 验证 downstream 失败是否来自 frozen detector 未见过增强分布。

Gate：

- adapted model 在 raw eval 上不能低于 raw-only baseline；
- 在 FF02/P27 eval 上减少 false-edge 和 AP loss；
- 如果只提升 enhanced input 但损伤 raw input，不通过。

## 6. Protocol C：Dual-Input Inference

输入：

- raw RGB；
- Stage1 full-flow enhanced RGB 或 sidecar maps。

机制：

- raw branch 预测 topology-stable edge；
- Stage1 branch 预测 weak-boundary candidates；
- confidence fusion 只允许 Stage1 branch 在 low-confidence raw weak-boundary 区域补充，不允许背景区域新增强边。

优点：

- 保留完整 Stage1 增强流程和模块创新；
- 避免把 enhanced image 当作唯一输入造成 raw-distribution break；
- 与 MSFI spatial-frequency weak-boundary diffusion 主创新方向一致。

## 7. 必须先完成的 FA01 审计

执行任何 adaptation 前，必须先完成：

- high-risk visual/error-map review；
- per-image correlation audit 已完成初版，但需要人工确认 `weixiaoyuanjia.26`、`xuehong.9/13/11`、`donghaiyuanjia.26`、`weixiaoyuanjia.21`、`tama.14`；
- 明确 sidecar map 的生成方式和保存格式；
- MyEdge 侧 run sheet 和 config diff；
- 训练预算、checkpoint 命名、output root、eval script。

## 8. 禁止写法

不能写：

- adaptation 结果证明 fixed detector 已受益；
- sidecar route 等价于 Stage1-only downstream positive；
- FF02 是成功主线；
- 2770 readiness 可替代 168 validation；
- 502/496 增强指标可替代 downstream validation。

可写：

- Stage1 full-flow direct replacement failed under fixed raw-trained detectors。
- FA01 supports a shift from image replacement to task-driven sidecar evidence formation。
- MyEdge/MSFI adaptation is a separate downstream-learning protocol requiring new training/eval evidence。

## 9. 下一步

在用户明确授权训练前，只能做：

1. high-risk panel review；
2. sidecar map definition；
3. MyEdge repo run sheet 草案；
4. config skeleton；
5. no-training smoke for sidecar export completeness。
