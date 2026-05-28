# E01 task-guided family

本目录保存 E01 HAB task-guided complete enhancement 方法族的 run sheet、configs、manifests、logs 和 isolated outputs。

当前状态：

- `E01-A` / `e01_a_color_illumination_task_guided_v1` 已完成 168 fixed-detector gate，归档为 failure / rescue-only，不能写成成功。
- `E01-B` / `e01_b_wavelet_pyramid_weak_boundary_v1` 已完成 168 fixed-detector gate，归档为 failure / rescue-only，不能写成成功。
- E01 family 本阶段已完成两个机制不同 candidate 的 168 gate，但没有产生强成功、可接受成功或最低安全 candidate。
- 固定 gate 阈值已在 `run_sheet_e01_a.md` 和 `run_sheet_e01_b.md` 中锁定。
- 当前阶段只允许 smoke、168 enhancement、fixed MSFI/DiffusionEdge validation、structure proxy 和 gate。
- 不运行 502/496，也不运行 2770 full-pool。

证据入口：

- family design: `docs/evidence/e01_task_guided_family/e01_task_guided_complete_enhancement_family_design_cn.md`
- E01-A design: `docs/evidence/e01_task_guided_family/e01_a_color_illumination_task_guided_design_cn.md`
- E01-A run sheet: `experiments/e01_task_guided_family/run_sheet_e01_a.md`
- E01-A gate report: `docs/evidence/e01_task_guided_family/e01_a_fixed_detector_gate_report_20260527_cn.md`
- E01-B design: `docs/evidence/e01_task_guided_family/e01_b_wavelet_pyramid_weak_boundary_design_cn.md`
- E01-B run sheet: `experiments/e01_task_guided_family/run_sheet_e01_b.md`
- E01-B gate report: `docs/evidence/e01_task_guided_family/e01_b_fixed_detector_gate_report_20260527_cn.md`
- E01 family stage summary: `docs/evidence/e01_task_guided_family/e01_family_stage_summary_20260527_cn.md`

边界：

- E01 不是 FF03/TLVC02/P29/D02。
- E01-A 已完成 downstream gate 但未达到 E01 minimum-safe；不能写成 downstream success。
- E01-B 已完成 downstream gate 但未达到 E01 acceptable success；不能写成 downstream success。
- `candidate_rescues_legacy_but_not_near_raw`、proxy-only、visual-only 或 readiness-only 都不能写成 E01 成功。
