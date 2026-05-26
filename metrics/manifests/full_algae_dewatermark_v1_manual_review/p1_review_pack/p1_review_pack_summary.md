# full_algae_dewatermark_v1 P1 review pack

日期：2026-05-25

本文是 P1 人工复核辅助包，不是最终人工决策，不修改 manifest，也不运行增强。

## Summary

- Near duplicate P1 rows: `9`
- Quality outlier P1 rows: `125`
- Total P1 rows: `134`
- Current review status: `recommendations_only_pending_manual_review`

## Outputs

- recommendations: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p1_review_pack\p1_review_recommendations.tsv`
- near duplicate contact sheet: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p1_review_pack\p1_near_duplicate_contact_sheet.png`
- quality contact sheets:
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p1_review_pack\p1_quality_contact_sheet_001.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p1_review_pack\p1_quality_contact_sheet_002.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p1_review_pack\p1_quality_contact_sheet_003.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p1_review_pack\p1_quality_contact_sheet_004.png`
- summary json: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p1_review_pack\p1_review_pack_summary.json`

## Boundary

- `machine_suggestion` 只是复核建议，不是 `reviewer_decision`。
- P1 质量异常更适合优先作为退化分层或失败案例候选，而不是自动排除。
- 不得根据本包直接改写 manifest、删除原图或转换原图。
- 只有人工填写 review sheets 并通过 `validate_fullpool_manual_review.py` 后，才能进入清洗规则派生。
