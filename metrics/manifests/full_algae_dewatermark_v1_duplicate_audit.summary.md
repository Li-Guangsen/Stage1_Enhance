# full_algae_dewatermark_v1 duplicate / near-duplicate audit

日期：2026-05-25

本文是完整增强图像池的只读内容重复审计，不是增强实验结果。

## Summary

- Total image rows: `2777`
- Candidate rows: `2774`
- Hash-readable rows: `2777`
- Candidate hash-readable rows: `2774`
- Decoder counts: `{'cv2': 2773, 'pillow_fallback': 4}`
- Exact file duplicate groups: `3`
- Exact file duplicate images: `6`
- Candidate exact file duplicate images: `6`
- Exact grayscale-image duplicate groups: `3`
- Exact grayscale-image duplicate images: `6`
- Candidate exact grayscale-image duplicate images: `6`
- Near-duplicate thresholds: `pHash <= 4`, `dHash <= 8`
- Near-duplicate candidate pairs total: `30`
- Near-duplicate candidate pairs reported: `30`
- Near-duplicate report truncated: `False`

## Outputs

- per-image audit: `metrics\manifests\full_algae_dewatermark_v1_duplicate_audit.tsv`
- exact duplicate groups: `metrics\manifests\full_algae_dewatermark_v1_duplicate_audit_exact_duplicate_groups.tsv`
- near duplicate pairs: `metrics\manifests\full_algae_dewatermark_v1_duplicate_audit_near_duplicate_pairs.tsv`
- summary json: `metrics\manifests\full_algae_dewatermark_v1_duplicate_audit.summary.json`

## Boundary

- Exact file duplicate means byte-level SHA-256 equality.
- Exact grayscale-image duplicate means decoded grayscale pixels are identical after decoder normalization.
- Near-duplicate pairs are only manual-review candidates; they are not automatic deletion or exclusion decisions.
- This audit does not replace `full502_clean_v1` or `compare9_complete496_v1`, and it does not run Stage1 full-pool enhancement.
