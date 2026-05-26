# Stage1 full2770 cv2-readable candidate execution readiness pack

日期：2026-05-25

本文是 Stage1 侧 2770 张 OpenCV 可读候选完整增强长跑的执行准备包。它只读取现有 manifest、审计、smoke、预算、run script 和 intake 状态，不运行 `main.py`，不创建 full2770 输出根目录，不生成增强图像，也不重算指标。

## Summary

- Overall status: `candidate_full2770_ready_after_explicit_approval_clean_protocol_blocked`
- Candidate run ready after explicit approval: `True`
- Expected images: `2770`
- Expected output files: `33240`
- Current intake status: `not_started`
- Output dir exists: `False`
- Present output files: `0`
- Free space on project drive: `96.15` GiB
- No experiment executed by this script: `True`

## Clean Protocol Gate

- Reviewed clean status: `blocked_pending_manual_review`
- Manual review pending rows: `544`
- Manual review invalid rows: `0`
- Can generate clean manifest: `False`
- Reviewed clean manifest exists: `False`

解释：`cv2readable2770` 可以作为候选覆盖长跑准备，但 reviewed clean full-pool protocol 仍被人工复核阻塞；两者不能混写。

## Current Evidence

- Source root: `D:\Desktop\去水印所有藻类图像`
- Manifest: `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt`
- Decode summary: `metrics/manifests/full_algae_dewatermark_v1_decode_audit.summary.json`
- Smoke summary: `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_summary.md`
- Budget: `experiments/full-algae-dewatermark-v1/run_budget_estimate.md`
- Run script: `experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1`
- Intake status: `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.json`

## Preconditions

| ID | Requirement | Satisfied | Evidence | Blocking rule if failed |
|---|---|---|---|---|
| F01 | External source root is available | `yes` | D:\Desktop\去水印所有藻类图像 | Stop before long run; the external full algae image pool is not accessible. |
| F02 | cv2-readable candidate manifest exists with 2770 unique rows | `yes` | `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt`; raw=2770; unique=2770; duplicates=0; first=1、Akashiwo sanguinea-血红哈卡藻/0012_Akashiwo-sanguinea.jpg; last=9、Gymnodinium catenatum-链状裸甲藻/vera_veloso_gymnodinium_catenatum_cruz_xxw_20070621133158_small.jpg | Stop before long run; rebuild or inspect the manifest. |
| F03 | Decode audit supports the cv2-readable candidate split | `yes` | `metrics/manifests/full_algae_dewatermark_v1_decode_audit.summary.json`; candidate_rows=2774; readable=2770; decode_failures=4 | Stop before long run; decode audit and manifest counts disagree. |
| F04 | Locked final mainline config and resumable run script are present and aligned | `yes` | config=`experiments/optimization_v1/configs/locked_full506_final_mainline.json`; run_script=`experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1`; has_locked_config=True; has_manifest=True; has_skip_existing=True | Stop before long run; the run script must explicitly pass the locked config and candidate manifest. |
| F05 | Smoke and completeness assets exist | `yes` | `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_summary.md`; `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_limit10_locked_final_mainline_completeness.json`; all_complete=True | Stop before 2770 run; rerun or inspect smoke if completeness is not true. |
| F06 | Budget, summarizer and intake scripts are present | `yes` | `experiments/full-algae-dewatermark-v1/run_budget_estimate.md`; `metrics/scripts/summarize_stage1_run_outputs.py`; `metrics/scripts/intake_stage1_fullpool_run_outputs.py` | Stop before long run; post-run intake must be available before execution. |
| F07 | Full2770 output root is not started | `yes` | output=experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline; output_exists=False; intake_status=not_started; present_output_files=0; expected_output_files=33240 | Stop and inspect existing outputs before starting or resuming the run. |
| F08 | Minimum disk-space recommendation is currently met | `yes` | free_space_gib=96.15; minimum_recommended_gib=5; preferred_with_future_artifacts_gib=8-10 | Stop before long run or free space; expected output is about 3.04 GiB plus logs/future artifacts. |

## Future Execution Sequence

以下步骤只是未来执行顺序。S1 是长时间高风险运行，必须先得到用户明确授权。

### S0 - Optional read-only preflight refresh

- Risk level: `read_only`
- Expected evidence: Updated intake status remains not_started before execution.
- Stop rule: If output root exists unexpectedly, stop and inspect before running main.py.

```text
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\intake_stage1_fullpool_run_outputs.py
```

### S1 - Run Stage1 cv2-readable 2770 candidate full run

- Risk level: `high_risk_long_run`
- Expected evidence: full2770_locked_final_mainline output root, logs/full2770_locked_final_mainline.log, six stages x JPG/PNG outputs.
- Stop rule: Requires explicit user authorization; stop if free disk is below 5 GiB or the planned output root already contains mixed outputs.

```text
powershell -ExecutionPolicy Bypass -File experiments\full-algae-dewatermark-v1\run_full_cv2readable2770_locked.ps1
```

### S2 - Read-only post-run intake

- Risk level: `read_only_after_long_run`
- Expected evidence: Intake status reaches core_outputs_complete or complete_with_log_and_run_report.
- Stop rule: Do not write completion claims while status is not_started or incomplete_or_in_progress.

```text
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\intake_stage1_fullpool_run_outputs.py
```

### S3 - Write run_report only after core outputs are complete

- Risk level: `guarded_report_write`
- Expected evidence: output_dir/run_report.md exists and intake status reaches complete_with_log_and_run_report.
- Stop rule: The intake script refuses to write run_report unless core outputs are complete.

```text
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\intake_stage1_fullpool_run_outputs.py --write-run-report
```

### S4 - Decide whether to promote any full-pool evidence

- Risk level: `human_decision`
- Expected evidence: README/status/research-state/research-log updated only after intake and human review.
- Stop rule: Do not replace full502_clean_v1 or compare9_complete496_v1 without a separately accepted protocol.

```text
manual review plus document update; no command
```

## Acceptance Criteria

- Manifest raw and unique rows are exactly 2770.
- Run command explicitly passes locked_full506_final_mainline.json and full_algae_dewatermark_v1_cv2_readable_candidate.txt.
- Log exists at experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline/logs/full2770_locked_final_mainline.log.
- Each of six stages has 2770 JPG and 2770 PNG outputs, for 33240 files total.
- Final PNG decode sample succeeds after post-run intake.
- run_report.md is generated only after core outputs are complete.
- State docs and research-log are updated only after intake proves completion.

## Paper Claim Boundary

- Current status can only be written as candidate full2770 ready after explicit approval, not executed.
- The four GIF89a-content files remain outside the cv2-readable run unless converted through a separate reviewed decision.
- Manual review still blocks a reviewed clean full-pool manifest.
- Full2770 coverage evidence does not replace the current formal full502_clean_v1 and compare9_complete496_v1 paper result protocols.
- Full2770 enhancement outputs alone do not prove downstream edge gains; MyEdge GT validation is still required.

## Hard Stops

- Do not run the full2770 PowerShell script without explicit user authorization.
- Do not use the candidate cv2-readable run as a reviewed clean manifest.
- Do not claim 2770 completion before intake reaches complete_with_log_and_run_report.
- Do not overwrite current formal 502/496 result directories.
