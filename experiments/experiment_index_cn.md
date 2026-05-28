# Stage1Codex Experiment Index

更新时间：2026-05-27

本文件是 `experiments/` 的导航索引。它只记录 purpose、status、decision 和 evidence links，不改变任何实验结论。

| Experiment | Purpose | Status | Decision | Evidence links |
| --- | --- | --- | --- | --- |
| `optimization_v1` | 正式 Stage1 主线配置锁定与历史搜索背景 | formal source configuration | keep as formal source asset | `experiments/optimization_v1/configs/locked_full506_final_mainline.json` |
| `h2-full506-direct` | 正式增强源结果副本 | formal source output root | keep as source asset, not paper metric count | `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline` |
| `downstream_driven_v1` | P12-P28 fixed-detector downstream-driven 候选集合 | archived diagnostic candidates | archive_diagnostic, no same-family iteration | `experiments/downstream_driven_v1/README.md` |
| `downstream_driven_v2` | D01 mechanism-complete weak diagnostic candidate | archived weak candidate | archive_diagnostic, not strong pass | `experiments/downstream_driven_v2/README.md` |
| `full_flow_downstream_stage1_mainline_v1` | FF01 完整增强主线恢复轨道 | fixed-detector validated, rescue-only | archive_diagnostic | `experiments/full_flow_downstream_stage1_mainline_v1/README.md` |
| `full_flow_downstream_stage1_mainline_v2` | FF02 detector-compatible full-flow redesign | fixed-detector validated, rescue-only | archive_diagnostic | `experiments/full_flow_downstream_stage1_mainline_v2/README.md` |
| `topology_locked_visual_chroma_full_flow_v1` | TLVC01 topology-locked visual-chroma correction | fixed-detector validated, rescue-only | archive_diagnostic | `experiments/topology_locked_visual_chroma_full_flow_v1/README.md` |
| `e01_task_guided_family` | E01 HAB task-guided complete enhancement method family | E01-A and E01-B fixed-detector validated, both failure / rescue-only | close current E01 family phase; recommend sidecar adaptation over E01-A/E01-B patching; no 502/496/2770 in current phase | `experiments/e01_task_guided_family/run_sheet_e01_a.md`; `experiments/e01_task_guided_family/run_sheet_e01_b.md`; `docs/evidence/e01_task_guided_family/e01_a_fixed_detector_gate_report_20260527_cn.md`; `docs/evidence/e01_task_guided_family/e01_b_fixed_detector_gate_report_20260527_cn.md`; `docs/evidence/e01_task_guided_family/e01_family_stage_summary_20260527_cn.md` |
| `full-algae-dewatermark-v1` | 2770/cv2-readable full-pool manifest/readiness work | readiness only | not formal result | `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt` |
| `h1-graypixel-bph-ablation` | 早期灰像素/BPH ablation | historical / archived | audit only | historical asset |
| `h2-fusion-ablation` | 早期 fusion ablation | historical / archived | audit only | historical asset |
| `h2-rghs-clahe-fusion-tuning` | 早期 RGHS/CLAHE/fusion tuning | historical / archived | audit only | historical asset |
| `h3-homomorphic-refinement` | 早期 homomorphic refinement | historical / archived | audit only | historical asset |
| `main_c25_smoke` | 旧 C25 smoke/background run | historical / archived | audit only | historical asset |

## Fixed Boundaries

- `D01` 只能写作 `mechanism-complete weak diagnostic candidate`。
- `FF01`、`FF02`、`TLVC01` 均为 `candidate_rescues_legacy_but_not_near_raw`，不能写成 downstream positive gain。
- `FA01` 位于 `docs/evidence/`，是 failure audit 与 sidecar export preparation，不是 experiments candidate。
- `E01` 是新的 task-guided method family；E01-A 与 E01-B 已完成两个机制不同的 168 fixed-detector gate，均归档为 failure / rescue-only，不能写成成功。E01 family 本阶段完成条件已满足，但没有产生强成功、可接受成功或最低安全 candidate。
- `2770` full-pool readiness 不能替代 168 fixed-detector downstream validation。
