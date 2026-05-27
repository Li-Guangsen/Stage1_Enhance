# Stage1 完整增强主线纠偏与长期推进计划

日期：2026-05-27

本文档用于纠正 `downstream_driven_v2 / D01` 与原始目标之间的偏差，并重新定义后续长时间工作的可执行目标。它不是实验结果，也不授权直接新增 `Pxx/Dxx` 候选；后续任何代码、配置和实验仍必须先有 method design、run sheet、isolated output root、status、decision 和 registry entry。

## 1. 纠偏结论

D01 `d01_structure_flow_v1` 没有达成原始目标。

它当前只能写成：

- fixed-detector 诊断闭环已完成。
- 能救回 legacy Stage1 `Final` 的严重下游崩塌。
- 是 `mechanism-complete weak diagnostic candidate`。

不能写成：

- 完整 downstream-driven Stage1 增强主线重构已完成。
- 增强指标相对外部方法有明显提升。
- 对下游任务有明确、稳定、可投稿的正收益。
- 形成了类似参考论文的完整创新增强流程。
- 视觉结果具有充分增强差异。

关键原因：

- D01 未运行 `full502_clean_v1` / `compare9_complete496_v1`，没有外部增强方法对比资格。
- D01 fixed-detector gate 为 `candidate_rescues_legacy_but_not_near_raw`，不是 candidate pass 或 strong pass。
- D01 的输出接近 raw，视觉增强强度不足。
- D01 实际更像 raw-anchored conservative input formation，而不是保留灰像素、IMF/频域、多分支融合和滤波收口创新骨架的完整增强流程。

## 2. 原始目标重新表述

后续真正要达成的目标是：

> 构建一条完整、有创新模块、有明显视觉增强、有增强指标竞争力，并能在 HAB 168 fixed-detector downstream validation 中验证其下游价值的 Stage1 task-driven enhancement flow。

该目标必须同时满足三条线：

1. 方法线：保留并升级 Stage1 原有创新骨架，而不是退化成 near-raw 小扰动。
2. 增强线：输出应有可见增强和 502/496 增强指标对照潜力。
3. 下游线：168 张带 GT split 上 fixed MSFI 50k 与 fixed DiffusionEdge baseline 50k 必须给出明确 gate 判定。

## 3. 必须保留的 Stage1 创新骨架

后续新主线应从原 Stage1 正式流程出发，而不是从 D01 的 near-raw 结果出发。

基础骨架：

`Original -> BPH -> IMF1Ray / RGHS / CLAHE -> Fused -> Final`

论文职责解释：

- `BPH`：灰像素引导的前置白平衡与受限颜色补偿。
- `IMF1Ray`：IMF1-Rayleigh 高频细节分支。
- `RGHS`：白平衡安全对比分支。
- `CLAHE`：CLAHE 引导的局部可见性分支。
- `Fused`：特征门控的三分支亮度结构融合。
- `Final`：轻量滤波、照明和对比收口。

后续应做的是把这套骨架改造成 downstream-aware 完整增强流程，而不是绕开这些模块。

## 4. 方法来源

允许作为方法设计输入：

- `docs/downstream_driven_v1_method_design_inputs_20260526.md`
- `docs/downstream_driven_v1_method_design_synthesis_20260526_cn.md`
- 两篇 Wu et al. 2026 HAB anchor 论文
- Stage1 正式增强主线和已有灰像素 / IMF / 融合 / 滤波实现
- 非深度或低学习依赖水下增强、结构保持增强、多尺度/金字塔、小波/频域、Retinex、edge-preserving filtering、false-edge suppression 方向

使用边界：

- Web AI 和外部文献只作为 method design / related work 输入。
- Wu/Gengkun Wu 相关论文只能作为 anchor / nearest-neighbor / overlap-risk reference，不复刻其流程，不主导新增候选。
- 项目结论只能来自本地 manifest、run report、`eval_bdry.txt`、`show.log`、结构 proxy、增强指标和日志。

## 5. 长期工作目标

目标名：

`full_flow_downstream_stage1_mainline_v1`

目标定义：

构建一条完整 Stage1 增强主线，使其具备以下性质：

- 机制明确：每个模块有退化动机和输入/输出职责。
- 模块边界清晰：每个主要模块有开关或可消融参数。
- 视觉增强真实：不能只是 raw-near 或低幅度 photometric adjustment。
- 增强指标可竞争：后续必须能进入 `full502_clean_v1` 和 `compare9_complete496_v1` 对照。
- 下游验证严格：168 fixed-detector validation 是核心 gate。
- 证据可投稿：成功或失败都能进入 MSFI spatial-frequency weak-boundary diffusion 主论文的证据链。

## 6. 建议的新主线结构

新主线不应直接命名为 D02。先完成 method design 和 run sheet，再决定是否分配候选 ID。

建议结构：

1. degradation diagnosis
   - 色偏、亮度非均匀、低对比、模糊边界、背景颗粒/气泡、细结构风险。
   - 只用于无 GT 的增强控制；GT 只用于评估。

2. gray-pixel color formation
   - 以 BPH 为起点，但加入 gain cap、颜色一致性和物种/背景风险约束。
   - 目标是提供稳定颜色起点，而不是强制接近 raw。

3. IMF / frequency detail branch
   - 保留 IMF1Ray 高频细节思想。
   - 增加 background texture penalty，避免把颗粒和气泡增强为伪边。

4. WB-safe contrast branch
   - 保留 RGHS 真实职责：白平衡安全对比增强。
   - 限制 chromatic false edge 和 over-stretch。

5. local visibility branch
   - 保留 CLAHE-guided visibility，但改为低风险局部可见性候选。
   - 必须有 clipLimit、tile、background-risk guard 和 ablation switch。

6. downstream-aware gated fusion
   - 从原三分支融合升级为 edge / texture / background / degradation guided fusion。
   - 融合权重不能只追求 EME、Contrast、UIQM，应同时约束 false-edge 和 endpoints 风险。

7. final filtering and closure
   - 保留滤波/照明/对比收口。
   - 可插拔：guided filter、bilateral、Retinex-like low-frequency closure、Laplacian/wavelet closure。
   - 必须 bounded，避免 legacy Final 式下游崩塌。

## 7. 分阶段实施路线

### Phase 0：纠偏与目标锁定

输出：

- 本文档。
- `docs/current_experiment_status_cn.md` 中明确 D01 未达成原始完整主线目标。
- `research-state.yaml` 和 `research-log.md` 同步。

完成条件：

- 后续 agent 不能再把 D01 包装成完成。

### Phase 1：method design 与 run sheet

输出：

- `docs/full_flow_downstream_stage1_mainline_v1_method_design_cn.md`
- `experiments/full_flow_downstream_stage1_mainline_v1/run_sheet_v1.md`

内容必须包括：

- 模块图。
- 每个模块的输入、输出、开关、参数和风险。
- 与旧 formal Stage1、P12-P28、D01 的差异。
- 168 / 502 / 496 / 2770 的使用边界。
- stop condition。

### Phase 2：代码设计，不先跑实验

建议实现方式：

- 新增独立模块文件，例如 `stage1_full_flow_mainline.py`。
- `main.py` 只增加显式入口，不改变默认正式主线。
- 新配置放入 `experiments/full_flow_downstream_stage1_mainline_v1/configs/`。
- 输出根目录必须是 isolated output root。

禁止：

- 覆盖 `locked_full506_final_mainline.json`。
- 覆盖 `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`。
- 覆盖 P12-P28/D01 资产。
- 修改 MyEdge checkpoint、GT、MAT 或 eval protocol。

### Phase 3：增强 sanity 与视觉 gate

先做小规模 smoke，不直接进入长跑。

最低检查：

- 输出完整。
- decode 成功。
- 可见增强不接近 raw-only。
- 没有明显偏色、过曝、halo、气泡伪边、背景颗粒爆炸。

如果视觉上仍接近 raw，则停止，不进入 fixed-detector gate。

### Phase 4：168 fixed-detector validation

核心 gate：

- MSFI 50k fixed detector
- DiffusionEdge baseline 50k fixed detector
- 不训练、不改 checkpoint、不改 GT、不改 eval protocol

比较对象：

- raw anchor
- legacy Stage1 Final
- P27
- D01
- 当前最好 archived diagnostic candidate

指标：

- ODS / OIS / AP / AC
- structure proxy
- false-edge ratio
- endpoints/kpx
- F1 proxy
- visual notes

### Phase 5：502/496 增强指标

触发条件：

- 168 gate 达到 candidate pass 或 strong pass；或
- 视觉增强明显、方法机制完整，但 downstream mixed，需要补增强指标支持失败分析。

边界：

- 502/496 是增强指标和 complete-case 对照，不替代 downstream validation。

### Phase 6：2770 readiness / smoke / optional full-pool

触发条件：

- 168 gate candidate pass 或 strong pass。
- 168 总耗时不超过 10 分钟，或有明确工程预算。
- 502/496 没有暴露明显结构损伤。
- full-pool clean protocol / manual review 状态允许。
- 人工或用户明确授权。

边界：

- 2770 只能作为工程稳定性、qualitative candidates 和 failure candidates pool。
- clean protocol 未冻结前不能作为论文正式统计结果。

## 8. Gate 定义

最低通过：

- 相对 legacy Final 显著恢复。
- 两个 detector 都不崩。
- 视觉增强不是 raw-copy。
- 允许还未超过 raw，但必须有机制价值。

候选通过：

- 至少一个 detector raw-near 或优于 raw。
- 另一个 detector 无明显 AP、AC、F1 proxy、false-edge、endpoints 崩坏。
- 增强图像有清晰视觉收益。
- 502/496 指标具备补跑价值。

强通过：

- 两个 detector 都 raw-near 或优于 raw。
- false-edge ratio、endpoints、F1 proxy 不劣于 raw。
- 增强指标和视觉质量有竞争力。
- 可进入完整 evidence package。

失败：

- 视觉增强接近 raw，不能支撑完整增强论文目标。
- 只救回 legacy Final，但不接近 raw。
- 只有单 detector 涨点，另一个 detector 结构或 AP/AC 崩坏。
- 增强指标或定性图像明显弱，无法说明方法价值。
- 模块不可解释或不可消融。

## 9. 当前第一步实施动作

立即动作不是跑实验，而是：

1. 固化本纠偏文档。
2. 写 Phase 1 method design。
3. 写 run sheet。
4. 设计新模块文件与配置目录。
5. 之后才进入代码实现和 smoke。

这样做的原因是：前一轮已经证明无 method design / run sheet 约束下的长时间候选派生会偏离目标。新的长线工作必须先锁定“完整增强流程 + 下游正收益验证”这个目标，再推进实现。

## 10. 2026-05-27 FF01/v8 后状态

FF01/v8 已按本计划推进到 Phase 4，并完成 168 fixed-detector validation。结论为失败/诊断：

- Stage1 168 输出完整，耗时满足预算，但视觉增强偏保守且存在 high-risk 背景纹理放大样本。
- fixed MSFI 50k 和 fixed DiffusionEdge baseline 50k 都救回 legacy Stage1 Final，但都明显低于 raw anchor。
- downstream gate 为 `candidate_rescues_legacy_but_not_near_raw`。
- structure proxy 两个 detector 都 worse than raw。
- FF01/v8 弱于 P27/P28 的 metric-near-raw mixed 证据，也不能替代 D01。

因此 FF01/v8 不能进入 502/496 或 2770 作为 candidate-passing route，也不能写成完整增强主线成功。

## 11. FF01 之后的长期工作目标

接下来的长期目标不是继续 FF01/v8 的 threshold、guard、fallback 或 raw-pullback 调参，而是二选一：

1. 机制级重设计：设计 FF02 级别的 detector-compatible full enhancement flow。它必须仍保留灰像素、IMF/频域、多分支融合、滤波/收口的完整增强骨架，但核心创新要从“增强后再保护 detector”改成“detector-compatible feature formation”：先估计 detector-sensitive background / weak-boundary / chroma-luma 分布，再决定每个分支如何进入融合。
2. 收敛为负向结论：如果机制级重设计仍无法让 168 fixed-detector 达到 candidate pass，就承认当前 fixed detector 更偏好 raw 分布，把 Stage1 写成失败分析、受控输入形成或 MyEdge/MSFI 侧适配的动机，而不是继续包装 Stage1 增强收益。

FF02 开始前必须新增独立 method design、run sheet、config、output root 和 registry entry。FF02 的第一轮 smoke 必须同时检查：

- 视觉增强是否明显强于 P27/D01 near-raw family。
- background false-edge risk 是否低于 FF01/v8。
- 168 fixed-detector 是否至少达到 P27/P28 的 metric-near-raw mixed 水平。
- 是否有进入 502/496 的增强指标价值。

否则不继续开长时间实验。

## 12. 2026-05-27 FF02 结果与停止点

FF02 已按第 11 节的机制级重设计路线执行完一轮：新增独立 method design、run sheet、config、output root 和 registry entry，保留灰像素、IMF/频域、多分支融合、滤波/收口等完整增强骨架，并把核心机制改为 color lane / structure lane decoupling 与 topology-compatible fusion。

实际结果：

- 168 Stage1 输出完整，Final PNG/JPG 各 `168`，decode 失败 `0`，耗时约 `77.5` 秒。
- 增强幅度比 FF01/P27/D01 更明显：mean BGR delta `11.7138`、chroma delta `7.9785`，但 high-risk 样本仍存在 detector-sensitive 结构风险。
- fixed MSFI 50k 为 `0.737952/0.751109/0.303208/0.792000`，相对 raw ODS/AP 为 `-0.045575/-0.042691`。
- fixed DiffusionEdge baseline 50k 为 `0.711020/0.720141/0.320951/0.794000`，相对 raw ODS/AP 为 `-0.059501/-0.042114`。
- structure proxy 两路 detector 都 worse than raw：MSFI dF1 `-0.0507`、dFalse-edge `+0.0734`、dEndpoints `+2.0630`；DiffusionEdge dF1 `-0.0666`、dFalse-edge `+0.0890`、dEndpoints `+3.7585`。
- Gate 为 `candidate_rescues_legacy_but_not_near_raw`。

结论：

FF02 说明“机制完整 + 视觉增强更明显 + detector-compatible fusion”仍未让 168 fixed-detector 达到 candidate pass。它救回 legacy Final 崩塌，但没有 raw-near，也没有下游正收益。FF02 比 FF01 稍微降低 structure proxy 风险，但下游主指标更差，因此不能进入 502/496 或 2770 作为候选通过路径。

当前长期工作必须暂停 full-flow same-family 正向收益迭代。下一阶段先做 failure audit：

1. 对比 FF01、FF02、P27、D01，分离“视觉增强幅度”“色度迁移”“亮度 topology drift”“false-edge/endpoints”对两个 fixed detector 的影响。
2. 明确 frozen detector 是否本质偏好 raw distribution；若是，应把 Stage1 写成受控输入形成与负向诊断，而不是硬推 downstream-positive enhancement。
3. 若继续新候选，必须是新的方法族和预注册机制，不能是 FF03 式阈值、guard、fallback 或 raw-pullback 修补。
4. 若目标仍是最终投稿证据链，正向收益更可能需要 MyEdge/MSFI spatial-frequency weak-boundary diffusion 侧适配，而 Stage1 只作为 task-driven structure-preserving input formation 或 failure-analysis support。

状态入口：

- `experiments/full_flow_downstream_stage1_mainline_v2/full_flow_downstream_stage1_mainline_v2_fixed_detector_ff02_status_20260527.md`
- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_downstream_gate_20260527.md`
