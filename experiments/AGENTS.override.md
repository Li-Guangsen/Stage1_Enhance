# Stage1 experiments override

Scope: everything under `experiments/`.

This override is intentionally stricter than the repository root rules. It exists because the previous downstream-driven cycle produced many `Pxx/Dxx` candidates that were useful as diagnostics but did not converge to a stable enhancement method.

## 1. Stop State

- Current operational state: stop creating new candidates until the candidate has a method review, a run sheet, an isolated output root, a config, logs, a status file, and an explicit decision rule.
- D01 `d01_structure_flow_v1` is a `mechanism-complete weak candidate`, not a completed Stage1 method and not a formal downstream improvement.
- A `candidate_rescues_legacy_but_not_near_raw` or `candidate_metric_near_raw_structure_mixed` result is diagnostic evidence, not project success.

## 2. New Candidate Gate

Do not add another `Pxx`, `Dxx`, `guard`, `fallback`, `raw-pullback`, or same-family patch unless all of the following exist first:

1. A method design note explaining the mechanism and why it differs from the last family.
2. A filled run sheet based on `docs/experiment_run_sheet_template_cn.md`.
3. A config path and an isolated output root that will not overwrite legacy assets.
4. A fixed validation plan: smoke, MyEdge 166 complete-case enhancement, fixed detector handoff, result intake, structure proxy, decision. The 166 set excludes `chazhuang.3.jpg` and `chazhuang.6.jpg`; historical 168 runs remain historical diagnostics only.
5. A stop condition that defines when to archive the candidate instead of deriving another nearby variant.

## 3. Forbidden Patterns

- Do not keep deriving consecutive same-family variants only to reduce one mixed metric by a small amount.
- Do not treat proxy-only evidence as fixed-detector evidence.
- Do not treat 2770 full-pool readiness or enhancement metrics as downstream validation.
- Do not mark a long-running goal complete if the current result is weak, mixed, proxy-only, or merely near raw.
- Do not overwrite official mainline outputs, legacy candidates, GT, weights, MAT, MyEdge `output_test`, or existing run reports.

## 4. Required Experiment Record

Every experiment under this directory must end in one of these decisions:

- `archive_failure`
- `archive_diagnostic`
- `iterate_after_method_review`
- `promote_to_downstream_gate`
- `promote_after_strong_pass`

The decision must be recorded in a status file, `metrics/experiment_registry.csv`, `metrics/candidate_registry.csv`, and `research-log.md`.
