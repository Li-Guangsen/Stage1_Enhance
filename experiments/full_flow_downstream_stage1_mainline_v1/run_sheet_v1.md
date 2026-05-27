# full_flow_downstream_stage1_mainline_v1 Run Sheet

状态：fixed-detector v8 completed / archive diagnostic

日期：2026-05-27

## 1. 基本信息

- run_id: `FF01`
- candidate_id: `full_flow_downstream_stage1_mainline_v1`
- family: `full_flow_downstream_stage1`
- protocol: `full_flow_downstream_stage1_mainline_v1`
- owner: `Codex + human review`
- status: `complete_rescue_only_not_raw_near`

## 2. 假设

- hypothesis: 保留 Stage1 灰像素、IMF/频域、多分支可见性/对比、融合和滤波收口创新骨架，并加入 downstream-aware 退化诊断、背景/纹理风险抑制和 bounded fusion 后，可以获得比 D01 更真实的视觉增强，同时避免 legacy Final 的 fixed-detector 崩塌。
- expected downstream effect: 至少达到 candidate pass；理想情况是在 MSFI 50k 和 DiffusionEdge baseline 50k 上同时 raw-near 或优于 raw，并降低 false-edge / endpoints 风险。
- expected enhancement effect: 相对 raw、D01、P27 有更明显视觉增强；具备补跑 `full502_clean_v1` 和 `compare9_complete496_v1` 的增强指标价值。
- known risk: 完整增强流程可能再次造成 detector distribution shift；IMF/CLAHE/Final closure 是伪边和 AC 下降高风险模块。

## 3. 方法设计

- method summary: `Original -> degradation diagnosis -> gray-pixel color formation -> IMF/frequency detail branch -> WB-safe contrast branch -> local visibility branch -> downstream-aware gated fusion -> bounded filtering/illumination closure -> Final`
- reference inputs:
  - `docs/full_flow_downstream_stage1_mainline_v1_method_design_cn.md`
  - `docs/stage1_full_enhancement_mainline_recovery_plan_cn.md`
  - `docs/downstream_driven_v1_method_design_inputs_20260526.md`
  - `docs/downstream_driven_v1_method_design_synthesis_20260526_cn.md`
  - `docs/stage1_downstream_edge_harm_degradation_diagnostic_20260525_cn.md`
- modules:
  - M0 degradation diagnosis
  - M1 gray-pixel color formation
  - M2 IMF / frequency detail branch
  - M3 WB-safe contrast branch
  - M4 local visibility branch
  - M5 downstream-aware gated fusion
  - M6 bounded filtering and illumination closure
- ablation switches:
  - `enable_degradation_diagnosis`
  - `enable_gray_pixel_bph`
  - `enable_imf_detail_branch`
  - `enable_wavelet_detail_branch`
  - `enable_wb_safe_contrast_branch`
  - `enable_local_visibility_branch`
  - `enable_downstream_aware_fusion`
  - `enable_final_closure`
  - `enable_texture_risk_suppression`
  - `enable_raw_anchor_constraint`
  - `enable_bounded_fusion_selection`
  - `enable_bounded_output_selection`
- why this is not the same family as the previous failed/mixed candidate: 本 run 不是 D01/P27 的 raw-near / low-frequency chroma / guard 回调，而是恢复完整 Stage1 增强骨架；raw anchor 只作为结构约束，不作为主输出目标。

## 4. 代码与配置

- code entry: `main.py final.mode=full_flow_downstream_stage1_mainline_v1`
- new module: `stage1_full_flow_mainline.py`
- config path: `experiments/full_flow_downstream_stage1_mainline_v1/configs/full_flow_downstream_stage1_mainline_v1.json`
- new files:
  - `stage1_full_flow_mainline.py`
  - `experiments/full_flow_downstream_stage1_mainline_v1/configs/full_flow_downstream_stage1_mainline_v1.json`
  - `experiments/full_flow_downstream_stage1_mainline_v1/run_sheet_v1.md`
  - smoke/status files after execution
- modified files:
  - `main.py` only to add explicit dispatch, if implementation proceeds
- protected files that must not be touched:
  - `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
  - `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
  - P12-P28/D01 outputs
  - MyEdge checkpoint, GT, MAT, eval protocol, official output roots
  - 2770 full-pool outputs

## 5. 输入与输出

- input split for smoke: 2-5 representative images from existing local manifests, exact list to be recorded before execution.
- input split for downstream gate: MyEdge 168-image ALGAE split with GT.
- input manifest: to be copied/recorded in the candidate status before execution.
- output root: `experiments/full_flow_downstream_stage1_mainline_v1/outputs/`
- output stages:
  - `BPHColor`
  - `IMFDetail`
  - `SafeContrast`
  - `LocalVisibility`
  - `Fused`
  - `Final`
  - optional diagnostics for weights/maps
- logs/status:
  - `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v8_status_20260527.md`
  - `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v8_status_20260527.json`
  - `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v8_metrics_20260527.csv`
  - `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_smoke5_fast_imf_v8_stage_metrics_20260527.csv`
  - `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_smoke25_fast_imf_v8_status_20260527.md`
  - `experiments/full_flow_downstream_stage1_mainline_v1/full_flow_downstream_stage1_mainline_v1_smoke25_fast_imf_v8_metrics_20260527.csv`
- manifest:
  - planned per-run manifest copy under `experiments/full_flow_downstream_stage1_mainline_v1/manifests/`

## 6. 命令与环境

Smoke 已执行；所有命令均只写入本实验隔离目录，不覆盖正式主线、旧候选或 MyEdge 资产。

- Windows PowerShell command:
  - `D:\Desktop\EdgeDetection\my_env\python.exe main.py --input-dir data\inputImg\Original --manifest experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt --output-dir experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v8 --params-json experiments\full_flow_downstream_stage1_mainline_v1\configs\full_flow_downstream_stage1_mainline_v1.json`
  - `D:\Desktop\EdgeDetection\my_env\python.exe experiments\full_flow_downstream_stage1_mainline_v1\scripts\summarize_smoke_run.py --run-id smoke5_fast_imf_v8 --status complete_smoke_fast_imf_v8_visual_review_pending --decision visual_review_before_168_gate --input-dir data\inputImg\Original --manifest experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt --output-root experiments\full_flow_downstream_stage1_mainline_v1\outputs\smoke5_v1_fast_imf_v8 --runtime-sec 3.0`
- WSL command/script: completed through `.sh`; any future multi-run eval/show must continue using `.sh`, not PowerShell double-quoted Bash strings
- WSL eval/show executed:
  - `wsl bash /mnt/d/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/run_full_flow_downstream_stage1_mainline_v1_v8_eval_show_20260527.sh`
- Python interpreter: Stage1 execution environment as recorded by current project docs; YAML/CSV/document checks use `D:/Desktop/DeepLearning/my_env/python.exe`
- expected runtime:
  - first full-quality smoke: observed about 35 sec/image due to aggressive IMF1Ray EMD, too slow for 168
  - fast-IMF smoke target: under 2 sec/image
  - 168 Stage1 enhancement target: ideally under 10 minutes
  - fixed-detector evaluation: pending MyEdge side run plan

## 6.1 Smoke Iteration Summary

- `smoke5_v1`: aggressive IMF，约 `35.98` 秒/张，外推 168 约 `100.7` 分钟，`tama.14` 出现明显块状/背景伪边，禁止进入 168。
- `smoke5_fast_imf_v2`: fast IMF + bounded selection，约 `0.64` 秒/张，但 `tama.14` Final grad ratio 仍约 `2.131`，需继续修正。
- `smoke5_fast_imf_v3` 到 `v6`: 分别验证 support-map pullback、低块感 RGHS/CLAHE 和更严格 support floor；均因 `tama.14` 背景伪结构或 Final 伪边升高而不采用。
- `smoke5_fast_imf_v7`: 新增 `direct_weighted` 融合后端，`tama.14` Fused grad ratio 降至约 `1.210`，但 entropy final closure 重新引入伪边。
- `smoke5_fast_imf_v8`: 默认关闭 entropy final closure，Final 等于 direct-weighted Fused + bounded selection；5 张输出完整，耗时约 `3.0` 秒，外推 168 约 `1.7` 分钟。Final 平均 BGR delta `6.8792`、L delta `1.0740`、grad ratio `1.0628`、luma std ratio `1.0273`。这是当前可继续做 broader smoke 的版本，但还不是 downstream result。
- `smoke25_fast_imf_v8`: 25 张 broader smoke 输出完整，耗时约 `11.6` 秒，外推 168 约 `1.3` 分钟。Final 平均 BGR delta `7.0538`、L delta `1.0849`、grad ratio `1.0366`、luma std ratio `1.0443`；最高 grad ratio 为 `tama.13` 的约 `1.099`。抽查最高梯度和最低增强 panel 后，未见 v1-v7 那种大块背景伪结构，但视觉增强偏保守，主要体现为颜色/色度一致性和轻量结构保持。
- `myedge168_v8`: 168 张 Stage1 输出完整，Final PNG/JPG 各 `168`，decode 失败 `0`，耗时约 `74.9` 秒，平均 BGR delta `8.6772`、L delta `2.0101`、grad ratio `1.0646`、luma std ratio `1.0798`。但 high-risk `weixiaoyuanjia.21` Final grad ratio 约 `1.9137`。
- fixed-detector validation: fixed MSFI 50k 为 ODS/OIS/AP/AC `0.739726/0.753251/0.310442/0.790100`，fixed DiffusionEdge baseline 50k 为 `0.717475/0.727626/0.336548/0.794400`。两者都救回 legacy Stage1 Final，但都明显低于 raw anchor，不是 raw-near。

## 7. 指标与证据

- enhancement metrics:
  - visual sanity first
  - if gate allows, `full502_clean_v1`
  - if gate allows, `compare9_complete496_v1`
- downstream metrics:
  - ODS
  - OIS
  - AP
  - AC
- structure proxy:
  - F1 proxy
  - false-edge ratio
  - endpoints/kpx
  - background edge noise proxy if available
- visual samples:
  - raw / legacy Final / P27 / D01 / new Final side-by-side
  - low contrast boundary
  - blurred contour
  - false-edge background
  - thin structure
  - overlap/clutter
- evidence files:
  - config
  - run manifest
  - stage1 status `.md/.json`
  - MyEdge preflight
  - `eval_bdry.txt`
  - `show.log`
  - result intake
  - structure proxy report
  - gate decision
  - enhancement metric outputs if run

## 8. Stop Condition

- stop if:
  - visual output remains near raw and cannot support complete enhancement claims
  - any stage output is missing or decode fails
  - smoke shows obvious color cast, halo, overexposure, background particle explosion, bubble false edges, or weak-boundary breakage
  - 168 fixed-detector gate is mixed/weak and failure mechanism repeats D01/P27
  - implementation becomes a guard/fallback/raw-pullback patch loop
- archive if:
  - downstream fails but evidence clearly explains why complete enhancement conflicts with frozen detector
  - enhancement metrics are weak and visual quality does not justify further work
- iterate only if:
  - method remains a full enhancement flow
  - failure analysis identifies one module-level cause
  - next iteration changes mechanism, not just a threshold
  - run sheet and registry are updated before execution

## 9. Decision

- gate result: `candidate_rescues_legacy_but_not_near_raw`
- compared with raw: lower on both detectors; MSFI dODS `-0.043801`, dAP `-0.035457`; DiffusionEdge baseline dODS `-0.053046`, dAP `-0.026517`.
- compared with legacy Final: substantially recovers legacy collapse on both detectors.
- compared with P27: worse; P27 is metric-near-raw mixed, FF01/v8 is rescue-only.
- compared with D01: worse or no better; D01 is also rescue-only but has stronger fixed-detector metrics and less severe MSFI structure loss.
- compared with current best candidate: below P27/P28/D01 on downstream evidence.
- decision: `archive_diagnostic_stop_before_502_496_2770`
- next action:
  1. Do not promote FF01/v8 to full502/compare496/2770 as a candidate-passing route.
  2. Use FF01/v8 as evidence that restoring the full enhancement chain can still conflict with frozen detector distribution.
  3. Only continue if the next iteration changes the method-level mechanism, not thresholds, guards, fallback, or raw pullback.
