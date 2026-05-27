# FA01 detector-sensitivity hypotheses

日期：2026-05-27

## 1. 状态

- status: `hypotheses_pre_registered_no_experiment_run`
- 输入依据：`docs/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
- 边界：本文件只定义下一阶段测量问题，不授权训练 detector，不授权 FF03/P29/D02，不替代 method design 或 run sheet。

## 2. H1 Raw-topology dominance

**Hypothesis.** 当前 fixed MSFI 50k 和 fixed DiffusionEdge baseline 50k 对 raw luma topology 的依赖强于对视觉增强质量的响应。只要输入改变了 detector 已学习的 raw edge statistics，就可能损伤 ODS/AP，即使人眼视觉增强更明显。

**Current evidence.**

- P27/D01 低增强幅度时接近 raw。
- FF01/FF02 完整流程更明显，但 ODS/AP 明显下降。
- FF02 mean grad ratio `0.9450`，仍比 FF01 更差，说明不是单纯梯度放大。

**Measurement plan.**

- 用 FA01 per-image 表对 `BGR/L/chroma delta`、`grad ratio`、`luma std ratio` 与 MyEdge per-image error map/proxy 做相关分析。
- 重点检查 `tama.*`、`weixiaoyuanjia.21`、`jianci.4` 是否在 detector 输出中出现 off-GT false-edge 增加。

**Stop condition.**

- 如果完整增强幅度越大，detector false-edge/AP 越差，且 P27/D01 raw-like 输入稳定，则 Stage1 fixed-detector 正收益路线停止，转 MyEdge/MSFI adaptation。

## 3. H2 Chroma/low-frequency shift sensitivity

**Hypothesis.** 色度和低频照明迁移本身会触发 fixed detector 的特征分布漂移；即使 luma 梯度没有整体放大，detector 中间响应仍可能产生假边或弱边界错配。

**Current evidence.**

- FF02 chroma delta `7.9785` 高于 FF01 `5.8024`、D01 `1.2302`、P27 `0.8445`。
- FF02 grad ratio 小于 `1`，但 ODS/AP 比 FF01 更差。

**Measurement plan.**

- 只读分析 FF01/FF02/P27/D01 的 per-image chroma delta 与 fixed-detector false-edge proxy delta。
- 若需要新增候选，必须先写新 method design，且只能做 `color-only / luma-frozen` ablation，不得称为 FF03 小修。

**Stop condition.**

- 如果 chroma/low-frequency shift 与 detector 下降强相关，则 Stage1 输出不应直接替换 raw detector input；转向 dual-input 或 sidecar。

## 4. H3 Background false-edge amplification

**Hypothesis.** 完整增强流程在 HAB 显微背景、藻体内部纹理、杂质和光照碎片上生成 detector-sensitive pseudo edges，导致 AP 与 structure proxy 下降。

**Current evidence.**

- legacy Final false-edge/endpoints 激增。
- FF01 high-risk：`weixiaoyuanjia.21`、`donghaiyuanjia.18`、`jianci.4`。
- FF02 high-risk：`tama.14`、`tama.11`、`tama.9`、`weixiaoyuanjia.21`。

**Measurement plan.**

- 建立 high-risk sample panel index，统一查看 raw、GT、legacy、P27、D01、FF01、FF02、detector white/overlay/error maps。
- 按 background false edge、missed weak boundary、fragmentation、over-smoothing 分四类标注。

**Stop condition.**

- 如果 false-edge 主要来自背景纹理增强，而不是 GT weak boundary 恢复，则 Stage1 full-flow 不能继续以 fixed detector 输入替换为目标。

## 5. H4 Weak-boundary sidecar may be better than image replacement

**Hypothesis.** Stage1 的价值可能不在于输出一张替代 raw 的 enhanced image，而在于生成 weak-boundary / visibility / frequency evidence sidecar，给 MyEdge/MSFI 主模型使用。

**Current evidence.**

- P27/D01 替换输入时只能保守 near-raw。
- FF01/FF02 替换输入时损伤 fixed detectors。
- 用户原始目标需要完整增强流程和创新模块；sidecar 可保留模块贡献，同时避免破坏 raw input distribution。

**Measurement plan.**

- 设计 MyEdge/MSFI 侧 adaptation protocol：raw image 保留为主输入，Stage1 branch 输出 weak-boundary map / chroma confidence / frequency detail map。
- 只在单独 run sheet 和用户授权后训练或适配。

**Stop condition.**

- 如果 fixed-detector replacement 继续失败，但 sidecar/adaptation 可提升 weak-boundary performance，则 Stage1 论文定位改为 task-driven evidence formation。

## 6. H5 Stage1-only fixed-detector positive gain may be infeasible

**Hypothesis.** 在不训练 detector、不改 checkpoint、不改 GT、不改 protocol 的条件下，完整 Stage1 enhancement 直接替换 raw 输入，可能无法稳定取得 downstream positive gain。

**Current evidence.**

- 旧 Final、FF01、FF02 三个完整/较完整增强流都失败。
- P27/D01 near-raw/mixed 不是用户目标里的完整视觉增强流程。

**Measurement plan.**

- 完成 H1-H3 的只读审计后，如果证据一致，停止 Stage1-only fixed-detector candidate loop。
- 后续只允许两条路线：新的方法族且机制完全不同；或 MyEdge/MSFI adaptation。

**Stop condition.**

- H1-H3 均支持 raw-distribution bias 时，禁止继续 FF03/P29/D02 小修。

## 7. 下一步执行建议

优先级：

1. 做 high-risk sample evidence panel index，不跑新实验。
2. 做 per-image correlation audit，不跑新 detector。
3. 写 MyEdge/MSFI adaptation run sheet 草案，但不执行训练。
4. 用户确认后再决定是否进入 detector-adaptation 实验。

## 8. 2026-05-27 初步测量回填

已完成：

- high-risk sample evidence index：`docs/fa01_high_risk_sample_evidence_index_20260527_cn.md`
- per-image correlation audit：`docs/fa01_per_image_correlation_audit_20260527_cn.md`
- MyEdge/MSFI sidecar adaptation protocol draft：`docs/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`

对假设的影响：

- H1 仍成立，但不是唯一因素；raw topology 重要，但不能单独解释 FF02。
- H2 证据增强：FF02 chroma/BGR delta 更高、mean grad ratio 更低，但 ODS/AP 更差。
- H3 证据增强：FF01/FF02 false-edge adverse cases 出现 `weixiaoyuanjia.26`、`xuehong.9/13/11`、`donghaiyuanjia.26`、`weixiaoyuanjia.21` 等重复簇。
- H4 优先级提高：Stage1 sidecar / dual-input 比直接替换 raw input 更合理。
- H5 尚不能作为最终结论，但当前证据继续反对 FF03/P29/D02 同族小修。
