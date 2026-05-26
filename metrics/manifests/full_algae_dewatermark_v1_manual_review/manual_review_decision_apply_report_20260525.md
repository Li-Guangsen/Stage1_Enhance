# full_algae_dewatermark_v1 manual review decision apply report

日期：2026-05-25

Mode: `dry-run`

## Summary

- Status: `no_decisions_to_apply`
- Template rows: `544`
- Filled decision rows: `0`
- Valid decision rows: `0`
- Invalid decision rows: `0`
- Applied to review sheets: `False`
- Plan TSV: `metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_decision_apply_plan_20260525.tsv`
- Invalid TSV: `metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_decision_apply_invalid_20260525.tsv`

## Boundary

- 默认 dry-run 不写回任何 review sheet。
- 只有显式传 `--apply` 且无 invalid decision rows 时才会写回。
- 写回后仍必须运行 `validate_fullpool_manual_review.py` 和 `derive_fullpool_review_artifacts.py`。
- 本脚本不生成 clean manifest，不转换/删除原图，不运行增强。
