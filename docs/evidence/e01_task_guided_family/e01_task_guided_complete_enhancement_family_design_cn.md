# E01 HAB task-guided complete enhancement family design

日期：2026-05-27

## 1. 状态与范围

- family id: `E01`
- family name: `hab_task_guided_complete_enhancement`
- status: `family_design_locked_before_candidate_runs`
- validation scope: 只看 MyEdge 168 张带 GT split 的 fixed-detector downstream gate。
- blocked scope: 本阶段不运行 `full502_clean_v1`、`compare9_complete496_v1` 或 2770 full-pool。

本文件是 E01 方法族设计入口。它不是实验结果，不是 502/496 增强指标主表，也不授权 MyEdge/MSFI training 或 detector adaptation。后续每个 candidate 都必须先有独立 run sheet、config、isolated output root、small smoke、168 fixed-detector gate 和归档 decision。

## 2. 本地可见输入

E01 只使用本仓库和 MyEdge 本地已落盘证据作为事实来源：

- `docs/current_experiment_status_cn.md`
- `docs/evidence/full_flow_recovery/stage1_full_enhancement_mainline_recovery_plan_cn.md`
- `docs/evidence/full_flow_recovery/stage1_full_flow_failure_audit_and_next_goal_20260527_cn.md`
- `docs/evidence/fa01_family_audit/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
- `docs/evidence/fa01_family_audit/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md`
- `docs/evidence/fa01_family_audit/fa01_high_risk_sample_evidence_index_20260527_cn.md`
- `docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527_cn.md`
- `docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527_cn.md`
- `docs/stage1_myedge_three_suggestions_synthesis_cn.md`
- `docs/downstream_driven_v1_method_design_synthesis_20260526_cn.md`
- `literature/wu2026_eswa_hab_edge_detection.md`
- `literature/wu2026_eaai_hab_segmentation.md`
- `metrics/experiment_registry.csv`
- `metrics/candidate_registry.csv`
- `research-state.yaml`

已确认仓库中存在 Web 调研综合输入，因此本轮不把聊天记忆或泛泛背景当作“Web 调研建议”。若后续引用新的外部论文，必须另写本地 note 或更新 synthesis 文档。

## 3. 失败证据摘要

FA01 对 E01 的直接约束如下：

1. legacy Stage1 `Final` 是 severe downstream negative baseline：MSFI dODS `-0.195240`，DiffusionEdge dODS `-0.240427`。
2. P27/D01 靠 very small 168 enhancement delta 接近 raw，但不满足完整增强流程目标。
3. FF01/FF02 恢复完整增强流程后，两路 fixed detector 都明显低于 raw，且 structure proxy worse than raw。
4. FF02 mean grad ratio `< 1` 仍然掉 ODS/AP，说明失败不只是 global gradient amplification。
5. Visual/error-map review 显示 high-risk 失败由 boundary F1 loss、false-edge increase、endpoint fragmentation、luma/detail topology drift 和 color/chroma shift 共同造成。
6. TLVC01 证明 raw topology lock 可以显著降低 direct replacement 风险，但它仍是 `candidate_rescues_legacy_but_not_near_raw`，不是 downstream positive gain。

因此，E01 不能是 FF03/TLVC02/P29/D02，也不能是 guard、fallback、raw pullback、topology lock 或低幅度 raw-near 修补。E01 必须是新的 mechanism family：每个 candidate 的 primary hypothesis 和主要机制路线都不同。

## 4. 固定 baseline 与 gate

本节在任何 E01 candidate 168 运行前锁定。后续不得根据 candidate 结果修改。

### 4.1 Raw baseline

| Detector | ODS | OIS | AP | AC |
|---|---:|---:|---:|---:|
| MSFI 50k raw | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| DiffusionEdge baseline 50k raw | 0.770521 | 0.779986 | 0.363065 | 0.796900 |

### 4.2 Legacy Stage1 Final baseline

| Detector | ODS | OIS | AP | AC |
|---|---:|---:|---:|---:|
| MSFI legacy Final | 0.588287 | 0.671357 | 0.263997 | 0.740300 |
| DiffusionEdge legacy Final | 0.530094 | 0.567910 | 0.224073 | 0.734900 |

### 4.3 Raw-near tolerance

沿用既有 MyEdge fixed-detector gate：

- ODS: candidate >= raw - `0.002`
- OIS: candidate >= raw - `0.002`
- AP: candidate >= raw - `0.003`
- AC: candidate >= raw - `0.003`

`strict raw-near` 表示同一 detector 的 ODS/OIS/AP/AC 全部满足上述容差。

### 4.4 Positive-gain threshold

E01 将“明确正收益”定义为：

- detector-positive: 同一 detector 中 `ODS >= raw + 0.002` 或 `AP >= raw + 0.003`，且该 detector 的 AP/AC 均满足 strict raw-near；
- family strong success: MSFI 与 DiffusionEdge 两个 detector 都 detector-positive，且 structure proxy 不崩；
- acceptable success: 至少一个 detector detector-positive，另一个 detector strict raw-near，且 structure proxy 不崩。

### 4.5 Structure proxy gate

E01 同时记录两个层次：

- strict structure non-worse: dF1 >= `0`，dFalse-edge <= `0`，dEndpoints/kpx <= `0`。
- structure not-collapsed: dF1 >= `-0.005`，dFalse-edge <= `+0.010`，dEndpoints/kpx <= `+1.000`。

E01 成功判定至少要求两个 detector 都达到 `structure not-collapsed`；强成功优先要求 strict structure non-worse。若 AP/AC 轻微上涨但 false-edge/endpoints/F1 proxy 崩坏，仍判为失败。

## 5. E01 family-level method idea

E01 的共同接口是：

`Original -> degradation diagnosis -> candidate-specific evidence formation -> task-guided fusion/reconstruction -> false-edge/background control -> Final`

共同设计要求：

- 不使用 GT 生成增强 mask；GT 只用于 fixed-detector evaluation 和 structure proxy。
- 允许继承 gray-pixel/BPH、IMF/frequency、CLAHE visibility、fusion、filtering 作为思想，但不把旧 Stage1 骨架固定为必选链路。
- 每个 candidate 必须有 ablation switches；失败 candidate 不做完整消融，只保留关键配置、失败指标和归因。
- 每个 candidate 输出同一 Stage1 stage contract，便于 existing MyEdge preflight/intake scripts 消费：`BPH`、`IMF1Ray`、`RGHS`、`CLAHE`、`Fused`、`Final`。这些 stage 在 E01 中是 evidence slots，不等于旧模块职责。

## 6. Candidates

### E01-A color-illumination task-guided correction

- primary hypothesis: FF02/TLVC01 的失败主要来自 color/chroma 与 low-frequency illumination shift 触发 fixed-detector distribution drift；若只重构 color/illumination lane，同时保持 high-frequency luma topology 与 background gradients 稳定，可能获得下游 raw-near 甚至 positive gain。
- dominant mechanism: color-illumination correction dominant。
- key modules: capped BPH color formation、Lab ab color confidence、low-frequency illumination field、raw-detail-preserving reconstruction、background false-edge risk suppression。
- why not TLVC02: E01-A 不锁 raw gray plane，也不做 topology lock 小修；它允许低频照明与色度改变，但显式保留 raw high-frequency detail plane 并抑制背景风险。
- priority: `1`

### E01-B wavelet-pyramid weak-boundary fusion

- primary hypothesis: full-flow 失败不是“频域思想无效”，而是旧 IMF/融合没有区分 weak boundary directional bands 与 HH/background texture；single-level or two-level wavelet/pyramid fusion 只增强 stable LH/HL weak-boundary evidence、抑制 HH texture，可能提升 AP 而不增加 false-edge/endpoints。
- dominant mechanism: multi-scale / pyramid / wavelet fusion dominant。
- key modules: LL illumination correction、LH/HL directional weak-boundary boost、HH soft-threshold suppression、raw-detail residual blend、guided cleanup。
- why not FF03: 它不沿用 FF01/FF02 的三分支 direct weighted fusion，也不是调 fusion weights；primary representation 改为 frequency-band reconstruction。
- priority: `2`

### E01-C edge-aware structure reconstruction

- primary hypothesis: fixed detectors 的收益可能来自 weak-boundary continuity 而不是视觉增强强度；用 multi-scale edge confidence、structure-preserving smoothing 和 small residual reconstruction 直接提升弱边界连续性，同时避免背景新边，可能给至少一个 detector 带来 positive gain。
- dominant mechanism: edge-aware structure enhancement dominant。
- key modules: multi-scale Scharr/Canny consistency、feature-preserving smoothing、weak-boundary support residual、edge-width control、bounded reconstruction。
- why not Pxx guard family: E01-C 的主目标是重构 weak-boundary support，而不是在已有候选上加 AP/AC guard 或 raw pullback。
- priority: `3`

### E01-D false-edge/background texture controlled reconstruction

- primary hypothesis: FA01 high-risk 样本说明 false-edge and endpoint fragmentation 是 direct replacement 的关键失败机制；如果先抑制 background texture and isolated edge components，再只在 stable boundary support 上注入弱结构，可避免旧 Final/FF 的 false-edge collapse。
- dominant mechanism: false-edge suppression / background texture control dominant。
- key modules: local variance texture risk、weak raw-gradient background risk、morphology component suppression、risk-aware residual injection、bilateral/guided closure。
- why not low-amplitude raw-near repair: 它以 risk map 为 primary reconstruction driver，不是简单降低增强幅度。
- priority: `4`

## 7. Candidate order and stop rules

默认推进顺序：

1. `E01-A`：先测试 color/illumination shift 是否可以在 non-topology-lock 条件下保住 fixed detector。
2. `E01-B`：若 A 失败，测试 frequency-band reconstruction 是否能提供 weak-boundary benefit。
3. `E01-C` 或 `E01-D`：根据 A/B 的 structure proxy 失败模式选择。若 false-edge/endpoints 主导，优先 D；若 F1/recall/weak-boundary 主导，优先 C。

停止规则：

- 至少完成 2 个机制不同 candidate 的 168 fixed-detector gate，才可说 E01 family 达到最低阶段性完成。
- 任一 candidate 达到强成功或可接受成功，必须完成一次复核或必要消融后才能阶段性完成。
- 连续 3 个机制不同 candidate 失败后，停止 E01 并写 failure attribution summary。
- 每个 primary hypothesis 最多允许一次机制级修正；修正前必须解释上一轮失败原因。

## 8. 禁止解释

E01 本阶段不得写：

- E01 已证明增强指标优于外部方法。
- 502/496 主表已形成。
- 2770 full-pool 已完成。
- proxy-only 或 visual-only 是 downstream success。
- rescue legacy Final 等于成功。
- single-detector small gain 等于稳定正收益。
- 未授权训练时 MyEdge/MSFI adaptation 已完成。

