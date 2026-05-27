# Topology-locked visual-chroma full-flow v1 method design

日期：2026-05-27

## 1. 定位

`topology_locked_visual_chroma_full_flow_v1` 是 FA01 之后允许开启的 Stage1-only 新方法族入口，不是 FF03、P29 或 D02 小修。

它的目标仍服务原始问题：保留灰像素/BPH、IMF/频域、多分支融合、滤波/收口等完整增强骨架，同时重新处理 fixed raw-trained detector 对 raw luma topology 的强偏好。

## 2. FA01 约束

FA01 已证明：

- P27/D01 接近 raw，但视觉增强太弱，不能满足“参考论文式完整增强流程”目标。
- FF01/FF02 恢复完整流程，但 direct replacement 在 fixed MSFI 和 fixed DiffusionEdge 下明显低于 raw。
- FF02 mean grad ratio 小于 `1` 仍然掉 ODS/AP，说明失败不只是全局锐化过强，而是 luma/detail topology、低频/色度分布迁移和 detector raw-distribution bias 的组合。

因此，新方法族不能继续 threshold / guard / fallback / raw-pullback；必须改变“增强证据如何进入 Final”的结构。

## 3. 核心假设

固定 detector 的主要风险来自 Lab-L topology drift，而不是所有视觉增强本身。

所以本方法采用：

`full Stage1 branch evidence -> topology-locked Lab-L + visual-chroma enhancement`

具体含义：

- Lab-L：以 raw luma 为 topology anchor，只允许低频 BPH illumination delta 和弱边界区域的 bounded residual 进入。
- Lab-a/b：由 BPH gray-pixel color formation 主导，少量吸收 RGHS/CLAHE/IMF 分支的色度证据。
- 背景区域：用 FA01 background risk 抑制 luma residual，避免生成 detector false-edge。
- Final：关闭 entropy/homomorphic closure，只保留轻量 bilateral finish 和 bounded output selection。

## 4. 模块结构

阶段保持完整：

1. `BPH`: gray-pixel color formation / white-balance anchor。
2. `IMF1Ray`: frequency/detail evidence branch。
3. `RGHS`: WB-safe contrast evidence branch。
4. `CLAHE`: local visibility evidence branch。
5. `Fused`: topology-locked visual-chroma fusion。
6. `Final`: bounded output selection 后的 detector-sensitive direct replacement candidate。

## 5. 与 FF01/FF02 的差异

| 项目 | FF01/FF02 | topology-locked visual-chroma v1 |
|---|---|---|
| luma residual | 分支残差仍进入 Final | 只在 weak-boundary support 中小幅进入 |
| 色度增强 | 与结构 fusion 同时发生 | 色度与 luma topology 解耦 |
| 背景处理 | guard / suppression | 背景 luma residual near-zero |
| 目标 | 完整增强 direct replacement | 完整增强外观 + raw-compatible topology |
| 风险 | false-edge / endpoints | 视觉增强可能仍不够强，或 detector 仍受色度分布影响 |

## 6. 当前配置入口

- config: `experiments/topology_locked_visual_chroma_full_flow_v1/configs/topology_locked_visual_chroma_full_flow_v1.json`
- smoke manifest: `experiments/topology_locked_visual_chroma_full_flow_v1/manifests/smoke5_highrisk_v1.txt`
- code mode: `final.mode=topology_locked_visual_chroma_full_flow_v1`

## 7. Gate

### Smoke gate

必须满足：

- 5 个 high-risk 样本六阶段 JPG/PNG 输出完整，decode 失败为 `0`。
- 平均每张耗时外推 168 不超过 `10` 分钟。
- Final mean_abs_chroma_delta 明显高于 P27/D01，不能只是 near-raw。
- Final grad_mean_ratio、luma_std_ratio 和 high-risk panel 不能出现 FF01/FF02 式背景伪结构。

### 168 fixed-detector gate

只有 smoke gate 通过后才允许执行：

- 168 Stage1 enhancement。
- fixed MSFI 50k sampling/eval/show。
- fixed DiffusionEdge baseline 50k sampling/eval/show。
- structure proxy 和 downstream gate。

判断仍沿用既有三级 gate：

- 最低通过：相对 legacy Stage1 Final 显著恢复，两个 detector 都不崩。
- 候选通过：至少一个 detector raw-near 或优于 raw，另一个 detector 无明显 AP/AC/structure proxy 崩坏。
- 强通过：两个 detector 都 raw-near 或优于 raw，false-edge ratio、endpoints、F1 proxy 不劣于 raw。

## 8. 停止条件

任一条件满足即停止本方法族，不继续改成同族小修：

- smoke 输出视觉上接近 raw，不能满足完整增强目标。
- high-risk panel 出现明显背景伪结构。
- 168 fixed-detector 仍为 `candidate_rescues_legacy_but_not_near_raw`。
- 168 structure proxy 两个 detector 均 worse than raw。

若停止，则回到 MyEdge/MSFI sidecar adaptation route，不再继续 Stage1-only direct replacement。

## 9. 2026-05-27 执行结论

TLVC01 已完成 168 fixed-detector 闭环，结论是 `candidate_rescues_legacy_but_not_near_raw`，不是候选通过或强通过。

关键事实：

- 正确 168 输入必须使用 `D:/Desktop/MyEdgeCodex/input_test/algae`。先前用 Stage1 仓库 `data/inputImg/Original` 会引入 raw-copy protocol mismatch，并导致 proxy 假失败。
- 使用 MyEdge raw 输入并启用 raw gray-plane projection 后，Stage1/MyEdge168 GT edge proxy 与 raw 完全一致：F1 `0.581331`、false-edge ratio `0.523693`、endpoints/kpx `56.100962`。
- fixed MSFI 50k: TLVC01 ODS/OIS/AP/AC 为 `0.782936/0.794718/0.345209/0.793200`，接近 raw 但 MSFI AC 低于 strict raw-near 容差。
- fixed DiffusionEdge baseline 50k: TLVC01 ODS/OIS/AP/AC 为 `0.768593/0.779518/0.362225/0.798500`，指标接近 raw，但 structure proxy 为 mixed：dF1 `-0.0030`、dFalse-edge `+0.0047`、dEndpoints `+0.3836`。
- TLVC01 比 FF01/FF02 安全，但弱于 P27/D01 的 DiffusionEdge AP 证据；它证明 raw-topology lock 可降低 direct replacement 风险，却没有达成明确 downstream 正收益。

因此，本方法族按停止条件归档，不继续做 TLVC02 式 threshold / guard / raw-pullback 小修。下一步应转向 `raw 主输入 + Stage1 complete enhancement sidecar/evidence maps + MyEdge/MSFI adaptation`，并与 fixed-detector direct replacement 证据严格分离。
