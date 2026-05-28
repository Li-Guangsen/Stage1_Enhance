# E01 family stage summary

日期：2026-05-27

## 阶段结论

E01 HAB task-guided complete enhancement family 已满足本阶段完成条件：完成了 `E01-A` 与 `E01-B` 两个机制不同 candidate 的 168 fixed-detector gate。

但 E01 没有产生强成功、可接受成功或最低安全 candidate。本阶段只能写成 **two-candidate fixed-detector diagnostic completed without E01 success**。

## Candidate 判定

| Candidate | Primary hypothesis | Gate classification | 关键原因 |
|---|---|---|---|
| E01-A | color-illumination correction dominant | failure / rescues legacy but misses minimum-safe | MSFI AC delta `-0.003846` 超出 raw-near 容差 `0.003`；DiffusionEdge raw-near 但无 detector-positive |
| E01-B | multi-scale / wavelet weak-boundary fusion dominant | failure / rescues legacy but not near raw | DiffusionEdge AP delta `+0.009502`，但 MSFI AP delta `-0.008301` 超出 raw-near 容差 `0.003` |

## 最好 candidate

没有可作为 E01 success 的最好 candidate。

- 若只看 positive signal，E01-B 是 E01 family 内最有信息量的候选，因为它让 DiffusionEdge baseline AP 从 raw `0.363065` 提升到 `0.372567`。
- 若看双 detector 安全性，E01-A 更接近 raw，但仍因 MSFI AC 掉出 strict raw-near 而失败。
- 若看当前 archived diagnostic reference，P27 仍强于 E01-A/B 的 overall gate：P27 是 `candidate_metric_near_raw_structure_mixed`，E01-B 是 `candidate_rescues_legacy_but_not_near_raw`。

## 失败归因

E01-A 和 E01-B 共同说明：直接替换 raw 输入的 Stage1 image-replacement 策略能 rescue legacy Stage1 Final 的严重崩塌，但难以同时满足 fixed MSFI 和 fixed DiffusionEdge 对 raw 分布的 AP/AC 校准。

更具体地说：

- color/illumination dominant reconstruction 可以保持结构 proxy 不崩，但会触发 MSFI AC 边缘损失。
- wavelet-pyramid weak-boundary reconstruction 可以提高 DiffusionEdge AP，但会造成 MSFI AP 明显下降。
- 两条机制都没有出现 FF01/FF02 式结构崩塌，因此失败不是简单的背景伪边爆炸；更可能是 raw-distribution bias、detector-specific ranking calibration、色度/低频迁移与弱边界增强之间的耦合冲突。

## 下一步建议

不建议继续 E01-A/E01-B 的轻微参数、guard、fallback、raw pullback 或 topology-lock 修补。若要继续 image-replacement，只能进入机制真正不同的 E01-C edge-aware structure route；但基于当前两条 E01 机制、P27、FF01/FF02/TLVC01 的证据，更推荐停止 Stage1 direct image-replacement 策略，把 raw 保持为主输入，将 Stage1 输出改为 sidecar / auxiliary maps，并进入单独授权的 MyEdge/MSFI adaptation 设计。

边界：本阶段没有运行 502/496，没有运行 2770，没有训练或修改 MyEdge/MSFI checkpoint。不得声称 E01 增强指标优于外部方法，不得声称形成正式增强指标主表。
