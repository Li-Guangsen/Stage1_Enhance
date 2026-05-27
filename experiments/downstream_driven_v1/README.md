# downstream_driven_v1

## Purpose

`downstream_driven_v1` 保存 P12-P28 fixed-detector downstream-driven 候选、对照、失败和诊断证据。该目录不是当前成功主线入口。

## Status

- P12-P28 已归档为 diagnostic candidates / archived evidence。
- P28 仍是 pending audit，不得继续迭代。
- raw-near、guard、fallback、raw-pullback 小候选不能继续同族派生。

## Decision

`archive_diagnostic`。后续不能从本目录直接派生 P29/D02/guard/fallback 小修；若提出新方法族，必须先有 method review、run sheet、config、isolated output root、status、decision 和 registry entry。

## Evidence Links

- Protocol: `experiments/downstream_driven_v1/protocol.md`
- Candidate registry: `metrics/candidate_registry.csv`
- Experiment registry: `metrics/experiment_registry.csv`
- Current status: `docs/current_experiment_status_cn.md`
