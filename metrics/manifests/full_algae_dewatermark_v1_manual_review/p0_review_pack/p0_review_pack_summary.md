# full_algae_dewatermark_v1 P0 review pack

日期：2026-05-25

本文是 P0 人工复核辅助包，不是最终人工决策，不修改 manifest，也不运行增强。

## Summary

- Decode failure P0 rows: `4`
- Exact duplicate P0 rows: `3`
- Total P0 rows: `7`
- Current review status: `recommendations_only_pending_manual_review`

## Outputs

- recommendations: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p0_review_pack\p0_review_recommendations.tsv`
- contact sheet: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p0_review_pack\p0_contact_sheet.png`
- summary json: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p0_review_pack\p0_review_pack_summary.json`

## Boundary

- `machine_suggestion` 只是复核建议，不是 `reviewer_decision`。
- 不得根据本包直接改写 manifest、删除原图或转换原图。
- 只有人工填写 review sheets 并通过 `validate_fullpool_manual_review.py` 后，才能进入清洗规则派生。
