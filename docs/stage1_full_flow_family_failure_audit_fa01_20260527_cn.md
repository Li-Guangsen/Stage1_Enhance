# FA01 Stage1 full-flow family failure audit

日期：2026-05-27

## 1. 状态

- FA01 WP1 status: `complete_readonly_family_audit`
- 范围：MyEdge 168 带 GT split，fixed MSFI 50k，fixed DiffusionEdge baseline 50k。
- 输入：raw anchor、legacy Stage1 Final、P27、D01、FF01/v8、FF02。
- 边界：本审计只读取现有 Stage1 输出、MyEdge result intake、structure proxy 和正式增强指标表；没有运行增强、sampling、WSL eval/show、训练、502/496 重算或 2770。

机器可读聚合表：

- `docs/fa01_stage1_full_flow_family_audit_tables_20260527/fa01_fixed_detector_metrics.csv`
- `docs/fa01_stage1_full_flow_family_audit_tables_20260527/fa01_structure_proxy_metrics.csv`
- `docs/fa01_stage1_full_flow_family_audit_tables_20260527/fa01_enhancement_proxy_168_summary.csv`
- `docs/fa01_stage1_full_flow_family_audit_tables_20260527/fa01_enhancement_proxy_168_per_image.csv`
- `docs/fa01_stage1_full_flow_family_audit_tables_20260527/fa01_502_496_boundary.csv`
- `docs/fa01_stage1_full_flow_family_audit_tables_20260527/fa01_asset_index.json`

## 2. Fixed-detector 主指标

| Variant | MSFI dODS | MSFI dAP | MSFI dAC | DiffusionEdge dODS | DiffusionEdge dAP | DiffusionEdge dAC | 解释 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| legacy Stage1 Final | -0.195240 | -0.081902 | -0.056546 | -0.240427 | -0.138992 | -0.062000 | 旧 Final 是下游负向 baseline |
| P27 raw-detail lowfreq chroma | -0.000198 | +0.000216 | -0.001746 | +0.002066 | +0.009019 | -0.002000 | metric-near-raw mixed，当前 near-raw reference |
| D01 structure flow | +0.000344 | +0.000109 | -0.003446 | +0.001209 | +0.008084 | -0.002100 | 机制较完整但 AC/结构 mixed |
| FF01 full-flow v8 | -0.043801 | -0.035457 | -0.006746 | -0.053046 | -0.026517 | -0.002500 | 完整流程恢复失败，明显低于 raw |
| FF02 detector-compatible | -0.045575 | -0.042691 | -0.004846 | -0.059501 | -0.042114 | -0.002900 | 机制级重设计仍失败，AP 更差 |

结论：P27/D01 能接近 raw，是因为增强非常保守；FF01/FF02 恢复完整流程后，两路 fixed detector 都明显掉点。FF02 不是 FF01 的 detector-compatible 修复成功，而是确认了 full-flow enhancement 在当前 fixed detector 下仍产生 distribution shift。

## 3. Structure proxy

| Variant | Detector | dF1 | dFalse-edge | dEndpoints/kpx | 解释 |
| --- | --- | ---: | ---: | ---: | --- |
| legacy Stage1 Final | MSFI | -0.210736 | +0.266940 | +90.920500 | 结构崩坏 |
| legacy Stage1 Final | DiffusionEdge | -0.296935 | +0.395444 | +223.747620 | 结构崩坏 |
| P27 raw-detail lowfreq chroma | MSFI | +0.000577 | -0.013685 | -1.160557 | MSFI structure non-worse |
| P27 raw-detail lowfreq chroma | DiffusionEdge | -0.000099 | +0.003972 | -0.176182 | baseline false-edge mixed |
| D01 structure flow | MSFI | +0.000343 | -0.013767 | -1.140514 | MSFI structure non-worse |
| D01 structure flow | DiffusionEdge | -0.000327 | +0.005265 | +0.353641 | baseline false-edge/endpoints mixed |
| FF01 full-flow v8 | MSFI | -0.053426 | +0.079593 | +1.891529 | 两路 worse than raw |
| FF01 full-flow v8 | DiffusionEdge | -0.067472 | +0.095084 | +4.291561 | 两路 worse than raw |
| FF02 detector-compatible | MSFI | -0.050686 | +0.073386 | +2.062959 | 较 FF01 false-edge 略低，但仍失败 |
| FF02 detector-compatible | DiffusionEdge | -0.066633 | +0.089035 | +3.758488 | 较 FF01 false-edge/endpoints 略低，但仍失败 |

结论：FF02 的 topology-compatible fusion 确实把部分 FF01 structure proxy 风险压低，但压低幅度不足以接近 P27/D01，更不足以 raw-non-worse。FF02 的 ODS/AP 下降还更大，说明结构 proxy 改善不是 downstream main metric 改善的充分条件。

## 4. 168 raw-vs-Final enhancement proxy

| Variant | BGR delta | L delta | Chroma delta | PSNR vs raw | Grad ratio | Luma std ratio | 高风险样本 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| legacy Stage1 Final | 38.0401 | 31.0400 | 12.5705 | 15.6397 | 8.1200 | 3.5872 | `tama.14`、`tama.9`、`tama.11` |
| P27 raw-detail lowfreq chroma | 2.1238 | 1.4878 | 0.8445 | 38.0760 | 1.2599 | 0.9837 | `tama.14`、`tama.11`、`tama.9` |
| D01 structure flow | 2.7677 | 1.5978 | 1.2302 | 36.3954 | 1.2931 | 0.9770 | `tama.14`、`tama.11`、`tama.9` |
| FF01 full-flow v8 | 8.6772 | 2.0101 | 5.8024 | 29.9656 | 1.0646 | 1.0798 | `weixiaoyuanjia.21`、`donghaiyuanjia.18`、`jianci.4` |
| FF02 detector-compatible | 11.7138 | 1.3708 | 7.9785 | 27.2740 | 0.9450 | 1.0132 | `tama.14`、`tama.11`、`tama.9`、`weixiaoyuanjia.21` |

解释：

- legacy Final 的失败是强增强导致的结构/梯度崩坏，证据非常明确。
- P27/D01 的 detector 结果好，但 BGR/chroma delta 很低，视觉上接近 raw，不能满足“像参考论文那样完整增强流程”的目标。
- FF01/FF02 才接近用户原始想要的完整流程方向，但 fixed detector 明显不接受。
- FF02 的平均 grad ratio 小于 `1`，却仍造成更差 ODS/AP，说明失败不能只归因于 raw 图像梯度放大。更可能是 color/chroma/low-frequency distribution shift、局部 topology drift 与 frozen detector raw-distribution bias 共同作用。

## 5. 502/496 增强指标边界

| Variant | full502 | compare496 | 解释 |
| --- | --- | --- | --- |
| P27 | available | available | 502/496 已跑，但指标明显保守：full502 EME `2.5540`、Contrast `26.2208`、AvgGra `2.7684`、UCIQE `2.2259`、UIQM `7.2528` |
| D01 | not run | not run | 未过强 gate，且未形成明显视觉增强主线 |
| FF01 | not run | not run | 168 downstream failed，不进入候选通过路线 |
| FF02 | not run | not run | 168 downstream failed，不进入候选通过路线 |

正式增强主线 `Final` 在 full502 上 EME `11.5985`、Contrast `544.5511`、AvgGra `14.8472`、UCIQE `4.0918`、UIQM `23.9227`；compare496 `Ours` 为 EME `11.5094`、Contrast `543.0379`、AvgGra `14.8101`、UCIQE `4.1371`、UIQM `23.7718`。因此 P27 的 502/496 增强指标不具备替代 formal enhancement mainline 的视觉/指标强度。FF01/FF02 因 168 gate 失败，不能为了补论文指标而进入 502/496 候选推广。

## 6. Failure attribution

当前证据支持以下归因强度：

1. **legacy Final harm is real and severe.** 两个 detector 都大幅低于 raw，structure proxy false-edge/endpoints 激增。
2. **near-raw safety works but does not satisfy the original enhancement goal.** P27/D01 保住 fixed detector 的方式本质上是限制增强幅度；这解释了为什么它们不能承担“完整创新增强流程”主线。
3. **full-flow completeness conflicts with fixed-detector raw distribution.** FF01/FF02 保留完整增强骨架后都明显掉点，即便 FF02 用 detector-compatible fusion 重新组织 color lane / structure lane。
4. **failure is not only gradient amplification.** FF02 的 mean grad ratio 为 `0.9450`，但 AP/ODS 仍比 FF01 更差；色度/低频分布迁移和 detector 内部响应漂移需要单独审计。
5. **structure proxy is necessary but not sufficient.** FF02 比 FF01 的 false-edge proxy 略好，但 downstream main metrics 更差；后续不能只用 proxy 决策。

## 7. Decision

FA01 WP1 的结论是：当前 Stage1-only fixed-detector downstream-positive 目标未达成，且不应继续 FF03 同族小修。

FA01 WP2 已进入初步测量：

- Detector-sensitivity hypotheses：`docs/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md`
- High-risk sample index：`docs/fa01_high_risk_sample_evidence_index_20260527_cn.md`
- Per-image correlation audit：`docs/fa01_per_image_correlation_audit_20260527_cn.md`
- MyEdge/MSFI sidecar adaptation protocol draft：`docs/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`

下一步应继续 high-risk visual/error-map review 和 sidecar map definition。若要追求下游正收益，更可能需要 detector 侧见过 Stage1-style input 或使用 Stage1 sidecar/dual-input，而不是继续替换 fixed detector 的 raw 输入。
