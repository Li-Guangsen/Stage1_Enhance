# 智能体执行入口规则

适用范围：整个 `Stage1Codex` 仓库。

本文件是下次 Codex / AI 接手本项目时必须先读的短规则入口。完整规则见 `docs/project_execution_rules_cn.md`。

## 1. 可见性原则

- 只把仓库内已版本化的本地文件当作项目记忆。
- 不依赖聊天历史、Notion 在线页面、Google Docs、个人记忆或网上公开泛知识。
- 如果某个事实没有落到本仓库文件里，就按“当前不可见”处理，不能当成已确认事实。

## 2. 每次任务的必读入口

每次开始任务前，至少先读：

1. `README.md`
2. `docs/project_execution_rules_cn.md`
3. `docs/project_handoff_guide_cn.md`
4. `docs/project_status_overview_cn.md`
5. `docs/current_experiment_status_cn.md`
6. `docs/goal_design_contract_cn.md`
7. `docs/candidate_lifecycle_policy_cn.md`
8. `docs/experiment_stop_rules_cn.md`
9. `research-state.yaml`

涉及结果、baseline、主表或对比方法时，还必须读：

- `docs/comparison_methods_results_index_cn.md`

涉及论文写作时，还必须读：

- `paper/underwater_image_enhancement_draft_cn.md`
- `paper/underwater_image_enhancement_evidence_pack_cn.md`
- `method-underwater-enhancement.md`
- `method-underwater-enhancement-paper-ready.md`
- `related-work-underwater-enhancement.md`

涉及 Stage1 -> MyEdge downstream-driven 候选、Pxx/Dxx、168 split、502/496 或 2770 时，还必须读：

- `docs/experiment_run_sheet_template_cn.md`
- `docs/stage1_to_myedge_downstream_workflow_cn.md`
- `docs/evidence_asset_inventory_cn.md`
- `docs/stage1_full_enhancement_mainline_recovery_plan_cn.md`
- `docs/stage1_full_flow_failure_audit_and_next_goal_20260527_cn.md`
- `docs/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
- `docs/stage1_detector_sensitivity_hypotheses_fa01_20260527_cn.md`
- `docs/fa01_high_risk_sample_evidence_index_20260527_cn.md`
- `docs/fa01_per_image_correlation_audit_20260527_cn.md`
- `docs/fa01_visual_error_map_review_20260527_cn.md`
- `docs/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`
- `docs/stage1_sidecar_map_definition_fa01_20260527_cn.md`
- `metrics/registry_schema_cn.md`
- `metrics/experiment_registry.csv`
- `metrics/candidate_registry.csv`

## 3. 实验治理硬规则

- 当前执行优先级是实验治理与候选归档，不是继续派生新的 `Pxx/Dxx` 候选。
- 没有 method design、run sheet、isolated output root、config、log、status 和 decision，不新增候选。
- `D01` 当前只能写作 `mechanism-complete weak candidate`，不是正式增强主线、不是 strong pass，也不是 Stage1 稳定下游收益。
- FF01/FF02 是完整增强主线恢复轨道的诊断失败证据；FF02 已完成机制级重设计但仍是 `candidate_rescues_legacy_but_not_near_raw`，不能继续同族小修或写成 downstream 正收益。
- TLVC01 是 topology-locked visual-chroma 完整流程纠偏证据；它修正 MyEdge raw input mismatch 但 gate 仍为 `candidate_rescues_legacy_but_not_near_raw`，不得继续 TLVC02/FF03/P29/D02 小修或写成 downstream 正收益。
- FA01 visual/error-map review 与 sidecar map smoke 是诊断/导出准备，不是新候选、训练结果或 fixed-detector 正收益证据。
- `candidate_rescues_legacy_but_not_near_raw`、`candidate_metric_near_raw_structure_mixed`、proxy-only、readiness-only 或 2770 full-pool readiness 都不能标记为目标完成。
- 168 张带 GT split 是 fixed-detector downstream validation 核心；502/496 只用于 Stage1 增强指标和 complete-case 对照；2770 不能替代 168 downstream validation。
- 不要继续连续派生同族 `guard` / `fallback` / `raw-pullback` 小变体。连续 mixed/weak 后必须停止、审计、归档或重写 method design。
- `experiments/` 下还有近场规则 `experiments/AGENTS.override.md`。在该目录工作时必须同时遵守。

## 4. 正式主线与运行规则

- 当前正式主线配置是 `experiments/optimization_v1/configs/locked_full506_final_mainline.json`。
- 正式结果副本是 `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`。
- 不要把直接运行 `python main.py` 当作正式论文主线。
- 涉及正式重跑时，必须显式传 `--params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json`。
- 正式阶段表口径是 `full502_clean_v1`；正式外部主比较口径是 `compare9_complete496_v1`。
- `full506` 只表示历史搜索与锁定背景，不再是当前论文正式主表口径。
- 跨项目调用 MyEdge WSL 评测时，不要把复杂 Bash 放进 PowerShell 双引号 `$cmd` 再 `wsl bash -lc "$cmd"`；简单命令用单引号 `wsl bash -lc '...'`，多 run / 数组 / 循环写成 `.sh` 后再从 WSL 执行。

## 5. 写作与解释规则

- 当前写作语言默认是中文主稿优先；英文只作为投稿辅助、论文题名、方法缩写或明确标注的英文辅助稿。
- `RGHS` 和 `CLAHE` 是历史阶段名，论文中必须写真实职责：白平衡安全对比分支、CLAHE 引导的局部可见性分支。
- `MS_SSIM` 和 `PSNR` 在当前项目中解释为增强结果相对原图的结构一致性，不是相对增强真值的质量指标。
- 不删除 `WWPF`，必须说明其官方实现稳定输出 496 张。
- `HLRP` 和 `Histoformer` 可作为当前 HAB 显微协议下的失败案例或补充分析，不能写成对原方法普遍无效的否定。
- `HVDualformer` 和 `ABC-Former` 是白平衡方法，不能在 related work 中混写成标准水下增强模型。

## 6. 多代理使用规则

- 对长上下文、跨目录、跨结果表或需要独立复核的复杂任务，可以使用主代理 + 子代理模式。
- 主代理负责读取入口规则、拆分任务、限定正式口径、汇总结论和最终验收，不能把项目口径判断完全外包给子代理。
- 子代理只处理边界清晰的局部任务，例如读取指定文件、核对指定结果、检查特定目录或做独立复核。
- 子代理结论必须回到主代理汇总；不得把子代理聊天历史、个人记忆或在线资料当作项目事实。
- 涉及文件修改、实验运行、正式结果覆盖或论文口径变更时，主代理仍必须执行状态维护规则。
- 子代理数量与深度按保守策略控制：默认每轮 1-3 个直接子代理，只有用户明确要求大规模并行复核时才扩展到最多 6 个；保持直接子代理深度，不允许子代理继续派生子代理。
- 如需在 Codex 配置中固化代理限制，建议保持 `[agents] max_threads <= 6`、`max_depth = 1`；提高深度必须先得到用户明确确认并写入日志。

## 7. 状态维护规则

- 任何改变项目状态的工作完成后，必须同步更新对应文档和 `research-log.md`。
- `research-log.md` 只追加，不回写历史条目。
- 如果发现 AI 执行不顺手或踩坑，任务结束时要把问题转成规则，补进 `docs/project_execution_rules_cn.md` 或本文件。
