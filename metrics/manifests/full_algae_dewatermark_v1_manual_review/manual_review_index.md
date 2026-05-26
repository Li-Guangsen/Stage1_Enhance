# full_algae_dewatermark_v1 manual review sheets

日期：2026-05-25

本文是完整增强图像池审计结果的人工复核入口，不是清洗结果，也不是增强实验结果。

## Summary

- Decode failure review rows: `4`
- Exact duplicate group review rows: `3`
- Near duplicate pair review rows: `30`
- Quality outlier review rows: `507`
- Unified review rows: `544`

## Outputs

- decode failures: `metrics\manifests\full_algae_dewatermark_v1_manual_review\decode_failures_review.tsv`
- exact duplicates: `metrics\manifests\full_algae_dewatermark_v1_manual_review\exact_duplicates_review.tsv`
- near duplicates: `metrics\manifests\full_algae_dewatermark_v1_manual_review\near_duplicates_review.tsv`
- quality outliers: `metrics\manifests\full_algae_dewatermark_v1_manual_review\quality_outliers_review.tsv`
- all issues: `metrics\manifests\full_algae_dewatermark_v1_manual_review\all_manual_review_issues.tsv`
- summary json: `metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_index.json`
- summary md: `metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_index.md`

## Review Rule

- 所有行默认 `review_status=pending`。
- 填写 `reviewer_decision` 前，不得修改 manifest、不得删除或转换原图。
- 任何清洗决策都必须保留 `decision_reason`、`reviewer` 和 `review_date`。
- 如果用于 MyEdge 训练/测试划分，严格重复和近重复至少应作为 split leakage guard。
- 这些 sheets 不替代 `full502_clean_v1` 或 `compare9_complete496_v1`。
