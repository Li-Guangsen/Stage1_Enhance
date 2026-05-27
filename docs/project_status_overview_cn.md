# 项目当前状态总览（中文）

更新时间：2026-05-27

## 0. 当前执行优先级

当前优先级是实验治理与候选归档，不是继续派生新的 `Pxx/Dxx` 候选。

必须停止的动作：

- 不直接创建 P29/D02。
- 不继续同族 `guard` / `fallback` / `raw-pullback` 小变体。
- 不把 `candidate_rescues_legacy_but_not_near_raw`、`candidate_metric_near_raw_structure_mixed`、proxy-only、readiness-only 或 D01 weak candidate 写成目标完成。
- 不用 502/496 或 2770 替代 168 张带 GT split 的 downstream validation。

治理入口：

- `docs/current_experiment_status_cn.md`
- `docs/goal_design_contract_cn.md`
- `docs/candidate_lifecycle_policy_cn.md`
- `docs/experiment_stop_rules_cn.md`
- `metrics/experiment_registry.csv`
- `metrics/candidate_registry.csv`

## 1. 当前项目定位

Stage1Codex 面向有害藻华（HAB）水下显微图像，不是一般自然场景水下增强仓库。

当前跨项目定位已经收束为：

`Stage1 provides task-driven structure-preserving input formation for MyEdge/MSFI.`

也就是说，Stage1 当前是 MyEdge/MSFI 主论文的结构保持增强输入支撑，不再作为独立“增强 + 边缘检测 pipeline”主创新推进。

两篇 Wu et al. 2026 HAB 论文是 nearest-neighbor / overlap-risk anchor，用于任务定义、退化分析、增强流程设计、指标设计和写作边界参考；当前仓库未证明本项目 2777/2774/2770 图像池与 ESWA 676 或 EAAI 1026 数据集存在文件级 overlap、同一 split 或同一 GT。

## 2. Formal Enhancement Source Asset

当前 formal enhancement source asset：

- 配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 结果源目录：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 最终输出源：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`

`full506_final_mainline` 是源资产路径名，不是论文统计样本数。

正式增强流程：

`Original -> BPH -> IMF1Ray / RGHS / CLAHE -> Fused -> Final`

论文中阶段职责必须写作：

- `BPH`：灰像素引导的前置白平衡。
- `IMF1Ray`：IMF1-Rayleigh 高频细节分支。
- `RGHS`：白平衡安全对比分支。
- `CLAHE`：CLAHE 引导的局部可见性分支。
- `Fused`：特征门控的三分支亮度结构融合。
- `Final`：轻量照明与对比收口。

## 3. Paper Metrics

当前正式论文指标只认两套口径：

| 口径 | 用途 | 输出目录 |
| --- | --- | --- |
| `full502_clean_v1` | 阶段进度表，502 张 | `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502` |
| `compare9_complete496_v1` | `Ours + 8 baselines` complete-case 主比较，496 张 | `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496` |

主表保留 9 个方法：

- `Ours`
- `HVDualformer`
- `ABC-Former`
- `GDCP`
- `CBF`
- `HLRP`
- `SGUIE-Net`
- `Histoformer`
- `WWPF`

解释边界：

- `MS_SSIM` / `PSNR` 是相对原图结构一致性，不是增强真值质量。
- `WWPF` 必须保留，并说明其官方实现稳定输出 496 张。
- `HLRP` / `Histoformer` 只能作为当前 HAB 显微协议下失败案例或补充分析，不能泛化否定原方法。
- `HVDualformer` / `ABC-Former` 是白平衡方法，不能混写成标准水下增强模型。

## 4. Downstream Diagnostic

当前 downstream 事实限定在 MyEdge 168 张带 GT split、fixed MSFI 50k 和 fixed DiffusionEdge baseline 50k。

已锁定事实：

- locked Stage1 `Final` 在该口径下明显降低 ODS/OIS/AP/AC。
- 因此同一 `Final` 在增强主表中是 formal enhancement output，在 MyEdge fixed-detector 诊断中是 legacy downstream negative control。
- Raw 输入是 fixed-detector downstream validation 的强 anchor。
- structure proxy、Sobel/Otsu proxy 和 paired proxy 只能作为 `diagnostic only, not downstream accuracy`。

不能外推：

- 不能把 168 split 结论外推到所有 downstream 设置。
- 不能把 502/496 增强指标写成 downstream validation。
- 不能把 2770 full-pool readiness 写成 downstream result。

## 5. Candidate Governance

P12-P28/D01 不是正式增强主线，而是 downstream diagnostic candidates / archived evidence。

唯一候选总账：

- `metrics/experiment_registry.csv`
- `metrics/candidate_registry.csv`

当前摘要：

- P12-P27：已完成候选或诊断，均未形成 strong pass。
- P28：`pending_audit`，不得继续迭代。
- D01：`mechanism-complete weak diagnostic candidate`，gate 为 `candidate_rescues_legacy_but_not_near_raw`，未运行 `full502_clean_v1`、`compare9_complete496_v1` 或 2770 full-pool。
- FF01/FF02：完整增强主线恢复轨道的两轮 full-flow 诊断。FF01/v8 和 FF02 都完成 168 fixed-detector validation，gate 均为 `candidate_rescues_legacy_but_not_near_raw`；FF02 是机制级重设计但仍低于 raw 且 structure proxy worse than raw，必须停止同族小修。
- TLVC01：topology-locked visual-chroma 完整流程纠偏候选，修正了 MyEdge raw input mismatch，完成 168 fixed-detector validation，gate 仍为 `candidate_rescues_legacy_but_not_near_raw`；比 FF01/FF02 安全，但没有超过 P27/D01 的 DiffusionEdge AP 证据，必须停止 Stage1-only direct replacement 小修。

后续若要新增候选，必须先创建候选专属 run sheet，来源模板为：

- `docs/experiment_run_sheet_template_cn.md`

## 6. Full-Pool / 2770 状态

`full_algae_dewatermark_v1` 是 cv2-readable full-pool candidate / qualitative engineering pool。

当前状态：

- 顶层图像文件：2777
- 默认候选 manifest：2774
- OpenCV 可读候选：2770
- 人工复核：544 条 pending
- clean manifest：未生成
- full2770 run intake：`not_started`

它不是正式 full-pool result，不替代 502/496 paper metrics，也不替代 168 downstream validation。

## 7. 当前还缺什么

真正缺口：

- MyEdge/MSFI 侧 MSFI 组件消融、替换模块对比、效率、失败案例和退化子集正式结果。
- 人工冻结退化/失败案例子集。
- 数据采集条件、物种覆盖、公开性和运行资源说明。
- paper-ready qualitative panel。
- 若未来继续 Stage1 候选，必须先 method review，而不是继续小参数 patch。
- FF01/FF02/P27/D01 family-level failure audit 已完成 WP1，入口为 `docs/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`；high-risk sample index、per-image correlation audit 和 visual/error-map review 也已完成，入口为 `docs/fa01_high_risk_sample_evidence_index_20260527_cn.md`、`docs/fa01_per_image_correlation_audit_20260527_cn.md` 与 `docs/fa01_visual_error_map_review_20260527_cn.md`。MyEdge/MSFI sidecar adaptation protocol 草案见 `docs/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`；Stage1 sidecar map definition 和 no-training export smoke 见 `docs/stage1_sidecar_map_definition_fa01_20260527_cn.md`；TLVC01 后长期目标见 `docs/stage1_long_horizon_goal_after_tlvc01_20260527_cn.md`，尚未授权训练。

不缺的是：

- formal enhancement source asset。
- `full502_clean_v1` 阶段表。
- `compare9_complete496_v1` 主比较表。
- P12-P28/D01 的诊断归档入口。

## 8. 历史资产读法

以下资产可用于审计，不是当前正式入口：

- `results_optimized_c25`
- 旧 `full506` 评测目录
- `metrics/archive/`
- `AIlog/`
- `notion_mirror/`
- 旧 pilot / H2 / H3 草案

如发现历史资产与当前文档冲突，以 `README.md`、`docs/current_experiment_status_cn.md`、registry、formal manifest、正式结果表和 run report 为准。
