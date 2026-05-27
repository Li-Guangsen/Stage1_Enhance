# full_flow_downstream_stage1_mainline_v2 Run Sheet

状态：complete / rescue-only diagnostic archived

日期：2026-05-27

## 1. 基本信息

- run_id: `FF02`
- candidate_id: `full_flow_downstream_stage1_mainline_v2`
- family: `full_flow_downstream_stage1`
- protocol: `full_flow_downstream_stage1_mainline_v2`
- owner: `Codex + human review`
- status: `complete_rescue_only_archived_diagnostic`

## 2. 假设

- hypothesis: 将完整 Stage1 增强改为 detector-compatible feature formation，拆分 color lane 与 structure lane，可以保留可见颜色/低频增强，同时避免 FF01/v8 的背景 false-edge 和 topology drift。
- expected downstream effect: 至少达到 P27/P28 的 metric-near-raw mixed 水平；理想情况是两路 detector raw-near 且 structure proxy 非劣。
- expected enhancement effect: 视觉颜色/色度恢复强于 P27/D01 near-raw family；如果 168 gate 达到候选通过，再补 502/496 增强指标。
- known risk: 如果 frozen detector 对任何非 raw luma/chroma shift 都敏感，FF02 仍可能失败；失败时应停止 Stage1 下游收益主张，而不是继续小修。

## 3. 方法设计

- method design: `docs/evidence/full_flow_recovery/full_flow_downstream_stage1_mainline_v2_method_design_cn.md`
- method summary: `Original -> detector-sensitive diagnosis -> BPH color lane -> IMF/RGHS/CLAHE evidence branches -> color/structure decoupling -> topology-compatible fusion -> bounded filtering closure -> Final`
- why this is not FF01 patching: FF02 不从 FF01 Final 做回拉，不调 FF01 阈值；它改写分支进入 Final 的机制，先拆 color lane / structure lane，再限制 detector-sensitive luma topology。

## 4. 代码与配置

- code entry: `main.py final.mode=full_flow_downstream_stage1_mainline_v2`
- module: `stage1_full_flow_mainline.py`
- planned config: `experiments/full_flow_downstream_stage1_mainline_v2/configs/full_flow_downstream_stage1_mainline_v2.json`
- output root: `experiments/full_flow_downstream_stage1_mainline_v2/outputs/`
- protected assets:
  - `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
  - `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
  - P12-P28/D01/FF01 outputs
  - MyEdge checkpoint, GT, MAT, eval protocol and official output roots

## 5. Ablation switches

- `enable_detector_sensitive_diagnosis`
- `enable_gray_pixel_color_lane`
- `enable_frequency_detail_evidence`
- `enable_contrast_evidence`
- `enable_visibility_evidence`
- `enable_color_structure_decoupling`
- `enable_topology_compatible_fusion`
- `enable_background_luma_suppression`
- `enable_bounded_filtering_closure`

## 6. Executed Commands

Smoke5:

```powershell
D:\Desktop\EdgeDetection\my_env\python.exe main.py --input-dir data\inputImg\Original --manifest experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt --output-dir experiments\full_flow_downstream_stage1_mainline_v2\outputs\smoke5_v1 --params-json experiments\full_flow_downstream_stage1_mainline_v2\configs\full_flow_downstream_stage1_mainline_v2.json
```

Smoke summary:

```powershell
D:\Desktop\EdgeDetection\my_env\python.exe experiments\full_flow_downstream_stage1_mainline_v1\scripts\summarize_smoke_run.py --run-id ff02_smoke5_v1 --status complete_smoke_review_pending --decision review_before_168 --input-dir data\inputImg\Original --manifest experiments\full_flow_downstream_stage1_mainline_v1\manifests\smoke5_v1.txt --output-root experiments\full_flow_downstream_stage1_mainline_v2\outputs\smoke5_v1 --runtime-sec TBD
```

## 7. Smoke Gate

Continue only if:

- all expected stage outputs are complete;
- no decode failures;
- runtime projection for 168 is acceptable;
- high-risk panels do not show FF01/v8 background pseudo edges;
- visual difference is not just raw-copy;
- grad ratio and luma std ratio are below FF01 high-risk behavior.

Stop if:

- output resembles FF01/v8 failure;
- only way to stabilize is raw-pullback/guard/fallback;
- visual enhancement is weaker than near-raw family.

## 8. 168 / 502 / 2770 Boundary

- 168 fixed-detector validation is the first real downstream gate.
- 502/496 only after 168 candidate pass or explicit failure-analysis decision.
- 2770 remains blocked unless 168 candidate/strong pass and clean protocol/readiness allow.

## 9. Results

Stage1 168:

- output root: `experiments/full_flow_downstream_stage1_mainline_v2/outputs/myedge168/full_flow_downstream_stage1_mainline_v2`
- Final PNG/JPG: `168/168`
- decode failures: `0`
- runtime: `77.5` sec
- mean BGR/L/chroma delta: `11.7138/1.3708/7.9785`
- grad ratio / luma std ratio: `0.9450/1.0132`

Fixed-detector:

| Detector | ODS | OIS | AP | AC | Delta ODS vs raw | Delta AP vs raw |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MSFI FF02 | 0.737952 | 0.751109 | 0.303208 | 0.792000 | -0.045575 | -0.042691 |
| DiffusionEdge FF02 | 0.711020 | 0.720141 | 0.320951 | 0.794000 | -0.059501 | -0.042114 |

Structure proxy vs raw:

| Detector | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | ---: | ---: | ---: |
| MSFI FF02 | -0.0507 | +0.0734 | +2.0630 |
| DiffusionEdge FF02 | -0.0666 | +0.0890 | +3.7585 |

## 10. Current Decision

- current decision: `archive_diagnostic`
- downstream gate: `candidate_rescues_legacy_but_not_near_raw`
- next action: stop same-family full-flow downstream-positive iteration; do failure audit before any new method family.
- blocked actions: no 502/496 promotion route, no 2770 readiness/full-pool route, no FF03 threshold/guard/fallback/raw-pullback patch.

Evidence:

- Stage1 status: `experiments/full_flow_downstream_stage1_mainline_v2/full_flow_downstream_stage1_mainline_v2_ff02_myedge168_v1_status_20260527.md`
- Fixed-detector status: `experiments/full_flow_downstream_stage1_mainline_v2/full_flow_downstream_stage1_mainline_v2_fixed_detector_ff02_status_20260527.md`
- MyEdge gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v2_ff02_downstream_gate_20260527.md`
