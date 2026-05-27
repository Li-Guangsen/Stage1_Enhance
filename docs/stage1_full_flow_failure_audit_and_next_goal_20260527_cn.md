# Stage1 full-flow failure audit and next long-horizon goal

日期：2026-05-27

## 1. 纠正结论

D01、FF01 和 FF02 都不能写成已经达成“完整创新增强流程 + 明显视觉增强 + 增强指标竞争力 + downstream 正收益”的目标。

当前事实：

- D01：机制较完整但视觉接近 raw，未运行 502/496 外部增强对比，fixed-detector gate 为 `candidate_rescues_legacy_but_not_near_raw`。
- FF01：恢复完整增强骨架，但 168 fixed-detector 明显低于 raw，structure proxy worse than raw。
- FF02：做了 detector-compatible 机制级重设计，视觉差异和色度恢复更明显，但 168 fixed-detector 仍明显低于 raw，structure proxy 仍 worse than raw。

因此，Stage1-only fixed-detector downstream-positive 目标当前没有被证明。继续同族 FF03 小修没有证据价值。

## 2. 长期目标

新的长期目标不是继续堆 `Pxx/Dxx/FFxx` 小候选，而是形成一条可投稿的双层证据链：

`MSFI spatial-frequency weak-boundary diffusion` 作为主创新；`Stage1 task-driven structure-preserving enhancement / input formation` 作为受控输入支撑、失败分析和可解释增强模块。

这个目标允许两种合法结论：

1. Stage1 full-flow enhancement 在 fixed raw-trained detector 下无法产生稳定正收益，主要价值是揭示 detector raw-distribution bias，并支持 MyEdge/MSFI 侧适配设计。
2. 若要证明 Stage1 downstream 正收益，必须进入新的方法族或 detector-adaptation 协议，而不是在 fixed detector 上继续对增强输出做小幅回拉。

## 3. 下一阶段总任务

阶段名：`FA01 full-flow failure audit and adaptation decision`

目标：解释为什么 FF01/FF02 的完整增强流程不能超过 raw，并决定下一步是新 Stage1 方法族，还是 MyEdge/MSFI 侧适配。

输入证据：

- raw anchor
- legacy Stage1 Final negative baseline
- P27 near-raw diagnostic
- D01 mechanism-complete weak diagnostic
- FF01 complete full-flow diagnostic
- FF02 detector-compatible full-flow diagnostic

禁止动作：

- 不创建 FF03 小修。
- 不以 502/496 或 2770 替代 168 downstream gate。
- 不把 rescue-only 结果写成 downstream-positive。
- 不重训练 detector，除非进入单独的 MyEdge/MSFI adaptation protocol 并另立 run sheet。

## 4. FA01 工作包

### WP1 Family-level failure audit

产物：

- `docs/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
- per-candidate comparison table：raw、legacy Final、P27、D01、FF01、FF02。

最低内容：

- ODS/OIS/AP/AC 相对 raw 和 legacy 的 delta。
- structure proxy：F1、false-edge、endpoints。
- Stage1 enhancement proxy：BGR/L/chroma delta、grad ratio、luma std ratio、PSNR vs raw。
- 视觉风险样本：`tama.14`、`weixiaoyuanjia.21`、`jianci.4` 等。
- 结论必须回答：是亮度 topology drift、色度迁移、背景 false-edge、弱边界损失，还是 detector raw-distribution bias 主导失败。

### WP2 Detector-sensitivity hypothesis test design

产物：

- `docs/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md`

需要预注册 3-5 个假设，例如：

- H1：fixed detectors 对 raw luma topology 的偏好强于对视觉增强质量的响应。
- H2：色度恢复本身不是主要问题，luma/detail topology drift 才是 AP/false-edge 下降主因。
- H3：完整增强流程带来的局部背景纹理清晰化会被 detector 当作候选边。
- H4：若 detector 训练/适配时见过 Stage1-style input，Stage1 full-flow 可能从负向转为正向。

每个假设必须有可执行测量和停止条件。

### WP3 MyEdge/MSFI adaptation protocol

产物：

- MyEdge 侧单独 run sheet。
- 只在用户明确授权后执行训练或 adaptation。

可选方向：

- input-domain augmentation：raw + FF02/P27/D01 混合输入增强，用于 MSFI 训练稳定性。
- two-input or consistency branch：raw edge topology branch + Stage1 enhanced weak-boundary branch。
- spatial-frequency weak-boundary diffusion 中加入 Stage1 branch consistency loss。

边界：

- 这不再是 fixed-detector validation；必须明确写成 detector-adaptation protocol。
- 不能用 adaptation 结果反向声称 fixed detector 已受益。

### WP4 New Stage1 method family decision

只有 WP1/WP2 证明仍存在 Stage1-only 机会时才允许开启。

新方法族必须满足：

- 与 FF01/FF02 机制不同，不是 threshold/guard/fallback/raw-pullback。
- 先写 method design、run sheet、config、ablation table。
- 先做小规模视觉与 proxy sanity，再进入 168。
- 168 candidate pass 前不进入 502/496 或 2770。

可能方向：

- edge-neutral color enhancement only：强化颜色和低频照明，但显式保持 raw luma topology。
- raw-detector dual representation：输出增强图像用于视觉，另生成 detector-compatible luma for downstream。
- weak-boundary evidence sidecar：Stage1 不直接替换输入，而是给 MyEdge/MSFI 提供 sidecar weak-boundary map。

## 5. 验收标准

FA01 完成必须回答：

- FF01/FF02 为什么没有达到 candidate pass。
- 哪些模块最可能造成 detector 指标下降。
- P27/D01 为什么更接近 raw 但不满足完整增强目标。
- 继续 Stage1-only 是否还有研究价值。
- 若目标是投稿证据链，下一步应优先推进 Stage1 新方法族，还是 MyEdge/MSFI 侧 adaptation。

完成前不得创建新的 `FF03`、`P29` 或 `D02`。

## 6. 当前推荐决策

当前证据更支持先做 FA01，而不是继续 Stage1-only 候选。

理由：

- FF01 和 FF02 已覆盖“完整增强流程”和“detector-compatible 机制级重设计”两类关键尝试。
- 两者都救回 legacy Final，但都明显低于 raw。
- FF02 视觉和色度增强更明显，却没有改善 downstream main metrics，说明 fixed detector 对增强分布不友好。
- 投稿主创新应回到 MSFI spatial-frequency weak-boundary diffusion；Stage1 应转为 input formation / failure-analysis support，或进入明确的 detector-adaptation 协议。
