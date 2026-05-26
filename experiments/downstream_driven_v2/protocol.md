# downstream_driven_v2 Protocol

Date: 2026-05-26

`downstream_driven_v2` is a non-mainline Stage1 enhancement workspace for downstream edge-detection-oriented candidates. It does not replace the locked official Stage1 configuration or the official 502/496 evaluation results.

## Fixed Scope

- Core validation split: MyEdge 168-image ALGAE split with GT.
- Fixed detectors: MSFI 50k and DiffusionEdge baseline 50k.
- No detector retraining.
- No checkpoint change.
- No GT change.
- No eval-protocol change.
- No 2770 full-pool run unless a later candidate passes explicit criteria and receives explicit approval.

## Official Stage1 Boundaries

- Official Stage1 config remains `experiments/optimization_v1/configs/locked_full506_final_mainline.json`.
- Official Stage1 result remains `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`.
- Official stage metric protocol remains `full502_clean_v1`.
- Official external comparison protocol remains `compare9_complete496_v1`.

## D01 Candidate

- Variant: `d01_structure_flow_v1`
- Config: `experiments/downstream_driven_v2/configs/d01_structure_flow_v1.json`
- Final mode: `downstream_d01_structure_flow_bph`
- Stage1 output: `experiments/downstream_driven_v2/outputs/myedge168/d01_structure_flow_v1`
- Stage1 status: `experiments/downstream_driven_v2/d01_structure_flow_v1_myedge168_stage1_status_20260526.md`
- Method/audit note: `docs/downstream_driven_v2_d01_method_design_and_audit_20260526_cn.md`

## D01 Gate

D01 is considered mechanism-complete but not a strong downstream pass.

- Strict script decision: `candidate_rescues_legacy_but_not_near_raw`
- Goal-level decision: weak/borderline candidate pass, not strong
- Expansion status: no full502, no compare496, no 2770

## WSL Execution Rule

Any multi-command MyEdge eval/show workflow must use a `.sh` script executed from WSL. Do not embed Bash variables, arrays, or loops in PowerShell double-quoted command strings.
