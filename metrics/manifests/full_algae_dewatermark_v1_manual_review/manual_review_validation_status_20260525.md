# full_algae_dewatermark_v1 manual review validation

日期：2026-05-25

本文是人工复核表的字段完整性校验，不是清洗结果，也不是增强实验结果。

## Summary

- Overall status: `pending_manual_review`
- Total rows: `544`
- Pending rows: `544`
- Reviewed rows: `0`
- Needs-followup rows: `0`
- Invalid rows: `0`
- Status counts: `{'pending': 544}`
- Issue type counts: `{'decode_failure': 4, 'exact_duplicate_group': 3, 'near_duplicate_pair': 30, 'quality_outlier': 507}`
- Priority counts: `{'P0': 7, 'P1': 134, 'P2': 403}`
- Invalid row report: `D:\Desktop\Stage1Codex\metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_invalid_rows_20260525.tsv`

## Boundary

- `pending_manual_review` 表示还不能生成清洗 manifest 或 split leakage guard。
- `complete_validated` 只表示人工复核字段完整且合法，不表示已经执行清洗或增强。
- 本报告不替代 `full502_clean_v1` 或 `compare9_complete496_v1`。
