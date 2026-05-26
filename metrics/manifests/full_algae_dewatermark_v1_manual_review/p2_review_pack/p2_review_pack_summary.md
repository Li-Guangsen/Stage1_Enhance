# full_algae_dewatermark_v1 P2 review pack

日期：2026-05-25

本文是 P2 人工复核辅助包，不是最终人工决策，不修改 manifest，也不运行增强。

## Summary

- Near duplicate P2 rows: `21`
- Quality outlier P2 rows: `382`
- Total P2 rows: `403`
- Current review status: `recommendations_only_pending_manual_review`

## Outputs

- recommendations: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_review_recommendations.tsv`
- near duplicate contact sheet: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_near_duplicate_contact_sheet.png`
- quality contact sheets:
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_001.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_002.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_003.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_004.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_005.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_006.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_007.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_008.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_009.png`
  - `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_quality_contact_sheet_010.png`
- summary json: `metrics\manifests\full_algae_dewatermark_v1_manual_review\p2_review_pack\p2_review_pack_summary.json`

## Boundary

- `machine_suggestion` 只是复核建议，不是 `reviewer_decision`。
- P2 质量异常更适合优先作为数据覆盖、退化分层、失败案例或有效难例候选，而不是自动排除。
- P2 近重复候选更适合优先形成未来 split leakage guard，而不是自动删除。
- 不得根据本包直接改写 manifest、删除原图或转换原图。
- 只有人工填写 review sheets 并通过 `validate_fullpool_manual_review.py` 后，才能进入清洗规则派生。
