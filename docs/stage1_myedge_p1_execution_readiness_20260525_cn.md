# Stage1-to-MyEdge P1 fixed-detector execution readiness pack

日期：2026-05-25

本文是 Stage1 侧的 MyEdge P1 执行准备包。它只读取现有状态文件并写入交接文档，不执行 staging、sampling、`eval.py`、`show.py`、report sync 或指标重算。

## Summary

- Overall status: `superseded_by_completed_p1`
- Expected image count: `168`
- No experiment executed by this script: `True`
- MyEdge high-risk confirmation phrase: `我确认执行高风险操作`
- Current P1 intake status: `complete_with_report_assets`
- Current intake run count: `2`
- Note: if overall status is `superseded_by_completed_p1`, use the coupling status snapshot and P1 run reports as result evidence.

## Current Evidence

- MyEdge command sheet: `docs/research_contracts/stage1_myedge_coupling_p1_execution_command_sheet_v1.md`
- Minimum matrix run sheet: `docs/research_contracts/stage1_myedge_coupling_minimum_matrix_run_sheet_v1.md`
- P1 preflight JSON: `docs/paper_assets/stage1_coupling/p1_preflight_20260524.json`
- P1 pending intake JSON: `docs/paper_assets/stage1_coupling/p1_results_intake_pending_20260525.json`
- P1 report sync status JSON: `docs/paper_assets/stage1_coupling/p1_report_asset_sync_status_20260525.json`
- Stage1 coupling snapshot: `docs/stage1_myedge_coupling_status_20260525_cn.json`
- Stage1 gate board: `docs/stage1_myedge_next_gate_board_20260525_cn.json`

## Baseline Checkpoint Record

| Item | Value |
|---|---|
| Size bytes | `4176168989` |
| SHA256 | `D78FC44ED04CA7495913D5DCF4088FBEDB5344CA7D5232426C68F05F1648507F` |
| Source | `docs/paper_assets/stage1_coupling/diffusionedge_baseline_p1_asset_freeze_20260525.md` |
| Recomputed by this script | `False` |

## Preconditions

| ID | Requirement | Satisfied | Evidence | Blocking rule if failed |
|---|---|---|---|---|
| P01 | Stage1/MyEdge coupling manifest exists and has 168 rows | `yes` | `docs/paper_assets/stage1_coupling/stage1_myedge_168_coupling_manifest_20260524.csv`; row_count=168 | Stop before staging or sampling; regenerate/read-only audit the manifest first. |
| P02 | All 168 Stage1 Final files and GT references are available | `yes` | missing_stage1_final=0; missing_gt=0; duplicate_target=0 | Stop before staging; inspect missing paths or duplicate target stems. |
| P03 | Staging root has not been populated | `no` | stage1_coupling_inputs/stage1_final_168_original_stem_20260524; exists=True; file_count=168 | Stop and inspect whether a prior staging run exists before writing/copying files. |
| P04 | MSFI P1 config template exists and planned output root is absent | `yes` | config=`configs/stage1_coupling/msfi_stage1_final_168_p1_20260524.yaml`; output=output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524; root_exists=False; root_nonempty=False | Stop before sampling; do not overwrite a populated MSFI P1 root. |
| P05 | DiffusionEdge baseline P1 config and frozen checkpoint evidence exist; planned output root is absent | `yes` | config=`configs/stage1_coupling/diffusionedge_baseline_stage1_final_168_p1_20260525.yaml`; freeze=`docs/paper_assets/stage1_coupling/diffusionedge_baseline_p1_asset_freeze_20260525.md`; checkpoint_size=4176168989; sha256=D78FC44ED04CA7495913D5DCF4088FBEDB5344CA7D5232426C68F05F1648507F; output=output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525; root_exists=False | Stop before baseline sampling; verify checkpoint size/hash or document any mismatch. |
| P06 | P1 intake and report sync are still not-started check artifacts | `no` | intake_status=complete_with_report_assets; intake_no_inference_or_eval=True; sync_status=complete_with_report_assets; sync_write_assets=False | Stop before writing paper claims; no P1 metric evidence exists yet. |
| P07 | Stage1-side gate board still marks MyEdge P1 as ready only after explicit approval | `no` | gate_board=`docs/stage1_myedge_next_gate_board_20260525_cn.json`; coupling_p1_status=complete_with_report_assets | Stop and reconcile Stage1/MyEdge status files before execution. |

## Future Execution Sequence

以下步骤只是未来执行顺序。除 S6 的只读 intake 外，任何 staging、sampling、WSL evaluation、report asset 写入都必须先回到 MyEdge 项目规则并获得明确高风险确认。

### S0 - Refresh P1 preflight/config templates and root checks

- Execution scope: `Windows PowerShell, D:/Desktop/MyEdgeCodex`
- Risk level: `guarded_write_config_only`
- Expected evidence: Updated config/preflight files and confirmed staging/output roots remain absent or empty.
- Stop rule: Do not proceed if root checks fail or config changes are unexpected.

```text
D:/Desktop/DeepLearning/my_env/python.exe docs/paper_assets/scripts/prepare_stage1_coupling_p1_assets.py --write-config
```

### S1 - Populate 168 Stage1 Final inputs under original MyEdge stems

- Execution scope: `Windows PowerShell, D:/Desktop/MyEdgeCodex`
- Risk level: `high_risk_writes_staging_files`
- Expected evidence: 168 PNG files under stage1_coupling_inputs/stage1_final_168_original_stem_20260524.
- Stop rule: Requires user phrase `我确认执行高风险操作`; stop if staged PNG count is not 168.

```text
D:/Desktop/DeepLearning/my_env/python.exe docs/paper_assets/scripts/prepare_stage1_coupling_p1_assets.py --write-config --write-staging
```

### S2 - Run Stage1 Final -> MSFI 50k sampling

- Execution scope: `Windows PowerShell, D:/Desktop/MyEdgeCodex`
- Risk level: `high_risk_sampling`
- Expected evidence: MSFI P1 png/mat counts are 168 and logs/sample.log exists.
- Stop rule: Requires user phrase `我确认执行高风险操作`; stop if png/mat counts differ from 168.

```text
$msfiRoot = "D:\Desktop\MyEdgeCodex\output_test\stage1_coupling\msfi_50k\stage1_final_168_p1_20260524"
New-Item -ItemType Directory -Force -Path "$msfiRoot\logs" | Out-Null
D:/Desktop/DeepLearning/my_env/python.exe sample_cond_ldm.py --cfg configs/stage1_coupling/msfi_stage1_final_168_p1_20260524.yaml 2>&1 |
  Tee-Object -FilePath "$msfiRoot\logs\sample.log"
```

### S3 - Run Stage1 Final -> DiffusionEdge baseline 50k sampling

- Execution scope: `Windows PowerShell, D:/Desktop/MyEdgeCodex`
- Risk level: `high_risk_sampling`
- Expected evidence: Baseline P1 png/mat counts are 168 and logs/sample.log exists.
- Stop rule: Requires user phrase `我确认执行高风险操作`; stop if checkpoint hash/size differs or png/mat counts differ from 168.

```text
$baseRoot = "D:\Desktop\MyEdgeCodex\output_test\stage1_coupling\diffusionedge_baseline_50k\stage1_final_168_p1_20260525"
New-Item -ItemType Directory -Force -Path "$baseRoot\logs" | Out-Null
D:/Desktop/DeepLearning/my_env/python.exe sample_cond_ldm.py --cfg configs/stage1_coupling/diffusionedge_baseline_stage1_final_168_p1_20260525.yaml 2>&1 |
  Tee-Object -FilePath "$baseRoot\logs\sample.log"
```

### S4 - Evaluate MSFI P1 with eval.py/show.py

- Execution scope: `WSL, /mnt/d/Desktop/MyEdgeCodex/eval-edge-py`
- Risk level: `high_risk_evaluation`
- Expected evidence: nms count 168, mat-eval/eval_bdry.txt, nms-eval/eval_bdry.txt, logs/eval.log and logs/show.log.
- Stop rule: Requires user phrase `我确认执行高风险操作`; stop if any eval/show artifact is missing.

```text
PY=/root/miniconda3/envs/myenv/bin/python; MSFI_ROOT=/mnt/d/Desktop/MyEdgeCodex/output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524; "$PY" eval.py ../output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524 -d ALGAE -nw -f 2>&1 | tee "$MSFI_ROOT/logs/eval.log"; "$PY" show.py ../output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524 -f 2>&1 | tee "$MSFI_ROOT/logs/show.log"
```

### S5 - Evaluate DiffusionEdge baseline P1 with eval.py/show.py

- Execution scope: `WSL, /mnt/d/Desktop/MyEdgeCodex/eval-edge-py`
- Risk level: `high_risk_evaluation`
- Expected evidence: nms count 168, mat-eval/eval_bdry.txt, nms-eval/eval_bdry.txt, logs/eval.log and logs/show.log.
- Stop rule: Requires user phrase `我确认执行高风险操作`; stop if any eval/show artifact is missing.

```text
PY=/root/miniconda3/envs/myenv/bin/python; BASE_ROOT=/mnt/d/Desktop/MyEdgeCodex/output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525; "$PY" eval.py ../output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525 -d ALGAE -nw -f 2>&1 | tee "$BASE_ROOT/logs/eval.log"; "$PY" show.py ../output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525 -f 2>&1 | tee "$BASE_ROOT/logs/show.log"
```

### S6 - Run read-only P1 results intake

- Execution scope: `Windows PowerShell, D:/Desktop/MyEdgeCodex`
- Risk level: `read_only_intake_after_results_exist`
- Expected evidence: A non-pending P1 intake report with both runs core_complete=true.
- Stop rule: Do not update paper claims unless intake confirms complete core outputs.

```text
D:/Desktop/DeepLearning/my_env/python.exe docs/paper_assets/scripts/intake_stage1_coupling_p1_results.py
```

### S7 - Generate visualization-only report assets after core results are ready

- Execution scope: `Windows PowerShell, D:/Desktop/MyEdgeCodex`
- Risk level: `guarded_report_asset_write`
- Expected evidence: white/overlay/error_map/manifest.csv/run_report.md for each P1 root.
- Stop rule: Only run after intake reports core_results_ready_for_report_sync or equivalent complete state.

```text
D:/Desktop/DeepLearning/my_env/python.exe docs/paper_assets/scripts/sync_stage1_coupling_p1_report_assets.py --write-assets
```

## Acceptance Criteria

- Staging directory contains exactly 168 PNG files with original MyEdge stems.
- Both P1 output roots contain exactly 168 PNG and 168 MAT files.
- Both P1 output roots contain exactly 168 NMS PNG files after WSL evaluation.
- Both P1 roots contain mat-eval/eval_bdry.txt and nms-eval/eval_bdry.txt.
- Both P1 roots contain logs/sample.log, logs/eval.log and logs/show.log.
- Read-only intake reports both runs core_complete=true with parsed ODS/OIS/AP and AC where available.
- Report sync is run only after core completion and then produces manifest.csv, run_report.md, white/, overlay/ and error_map/.

## Paper Claim Boundary

- Currently allowed: write that P1 is prepared and ready only after explicit high-risk approval.
- Currently forbidden: claim Stage1 Final improves ODS/OIS/AP/AC, false-edge suppression, morphology consistency or downstream edge detection.
- After results exist: compare Stage1 Final P1 only against existing raw-input anchors in MyEdge.
- If ODS/OIS improve but AP drops, write an operating-point/ranking trade-off, not comprehensive superiority.
- If only one detector benefits, write detector-specific or interaction-specific support only.

## Hard Stops

- Do not run S1-S5 without explicit MyEdge high-risk confirmation.
- Do not create or populate P1 output roots before confirming they are absent or empty.
- If P1 intake is complete_with_report_assets, treat this readiness pack as superseded and use the coupling status snapshot instead.
- Do not treat this readiness package as a result artifact.
