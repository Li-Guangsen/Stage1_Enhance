# Stage1 -> MyEdge coupling status snapshot

日期：2026-05-25

本文是 Stage1Codex 侧对 MyEdgeCodex 当前 Stage1 coupling 资产的只读镜像摘要，不是实验结果。

## Summary

- MyEdge root: `D:\Desktop\MyEdgeCodex`
- Overall status: `complete_with_report_assets`
- No training/sampling/eval executed by this script: `True`

## 168-image Manifest

- Rows: `168`
- GT missing: `0`
- All Stage1 stages complete: `True`
- MSFI raw-reference missing: `0`
- DiffusionEdge raw-reference missing: `0`
- Staging note: `Stage1 Final files carry _Final suffix; future detector input staging must use original stem filenames to keep eval GT matching.`

## P1 Preflight

- Staging exists: `True`
- Staging file count: `168`
- Write staging executed: `False`
- Missing Stage1 Final: `0`
- Missing GT: `0`
- Duplicate target filenames: `0`
- Ready for MSFI P1 after approval: `True`
- Ready for DiffusionEdge baseline P1 after approval: `True`

## P1 Result Intake

- Intake status: `complete_with_report_assets`
- Expected count: `168`
- P1 roots exist: `True`
- P1 metrics present: `True`

| Run | Detector | Status | Root exists | mat-eval | nms-eval | AC |
|---|---|---|---:|---|---|---|
| `stage1_final_to_msfi_50k` | Ours / MSFI 50k | `complete_with_report_assets` | `True` | `{'threshold': 0.24, 'ods': 0.588287, 'ois': 0.671357, 'ap': 0.263997}` | `{'threshold': 0.17, 'ods': 0.569307, 'ois': 0.65192, 'ap': 0.22154}` | `0.7403` |
| `stage1_final_to_diffusionedge_baseline_50k` | DiffusionEdge baseline 50k | `complete_with_report_assets` | `True` | `{'threshold': 0.46, 'ods': 0.530094, 'ois': 0.56791, 'ap': 0.224073}` | `{'threshold': 0.39, 'ods': 0.523548, 'ois': 0.497877, 'ap': 0.211365}` | `0.7349` |

## Report Asset Sync

- Sync status: `complete_with_report_assets`
- Write assets: `False`

## Boundary

- 该快照只读取 MyEdgeCodex 已存在的 planning / intake / report asset 文件。
- 当前 P1 已完成 report asset sync；P1 指标只能在 168 张、Stage1 Final 输入、固定 detector 的边界内引用。
- P1 结果不能外推为 full2770、full502 或所有 Stage1 阶段的下游收益。
- 若要证明 Stage1 不是普通 preprocessing，下一步仍需 stage-wise / generic enhancement control / degradation subset 矩阵。
