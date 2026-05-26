# full_algae_dewatermark_v1 derived review artifacts

日期：2026-05-25

本文是人工复核决策派生清单的状态报告，不是清洗结果本身，也不运行增强。

## Summary

- Overall status: `pending_manual_review`
- Can generate clean manifest: `False`
- Total review rows: `544`
- Pending rows: `544`
- Needs-followup rows: `0`
- Invalid rows: `0`
- Unresolved decision rows: `0`
- Conversion candidates: `0`
- Exclusion rows: `0`
- Deduplicate drop rows: `0`
- Split guard rows: `0`
- Subset label rows: `0`
- Reviewed clean manifest: `not_generated`

## Boundary

- 只有 `overall_status=complete_validated` 时，本脚本才生成 reviewed clean manifest。
- `pending_manual_review` 或 `review_ready_with_followups` 时，只能查看状态和空/部分派生表，不能作为清洗完成证据。
- 本脚本不修改原图、不转换文件、不运行 Stage1，也不替代 `full502_clean_v1` / `compare9_complete496_v1`。
