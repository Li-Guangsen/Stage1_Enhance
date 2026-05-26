# full_algae_dewatermark_v1 manual review decision template

日期：2026-05-25

本文档说明配套 TSV 模板的用途。模板用于人工填写决策，不是自动决策，不修改 review sheets，也不生成 clean manifest。

## Outputs

- Decision template: `metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_decision_template.tsv`
- Summary JSON: `metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_decision_template_20260525.json`

## Summary

- Template rows: `544`
- Expected review rows: `544`
- Template status: `ready_for_human_fill`
- Priority counts: `{'P0': 7, 'P1': 134, 'P2': 403}`

## How To Fill

- 只填写以下列：`review_status_to_apply`、`reviewer_decision_to_apply`、`decision_reason_to_apply`、`reviewer_to_apply`、`review_date_to_apply`、`reviewer_notes`。
- `review_status_to_apply` 可填 `reviewed` 或 `needs_followup`；如果要保持未处理，留空。
- `reviewer_decision_to_apply` 必须来自同一行的 `allowed_decisions`。
- `review_date_to_apply` 使用 `YYYY-MM-DD`。
- 填完后先 dry-run，不要直接 apply。

```bat
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\apply_fullpool_manual_review_decisions.py
```

只有 dry-run 无 invalid 后，才可以显式加 `--apply` 写回 review sheets。写回后仍必须运行 `validate_fullpool_manual_review.py` 和 `derive_fullpool_review_artifacts.py`。

## Boundary

- 本模板不替代人工判断。
- 本模板中的 `machine_suggestion` 不是 `reviewer_decision`。
- 任何决策在显式 `--apply` 前都不会写回 review sheets。
