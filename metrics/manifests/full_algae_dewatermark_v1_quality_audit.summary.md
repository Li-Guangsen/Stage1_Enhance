# full_algae_dewatermark_v1 quality outlier audit

日期：2026-05-25

本文是完整增强图像池的只读质量异常审计，不是增强实验结果。

## Summary

- Total image rows: `2777`
- Candidate rows: `2774`
- Quality-readable rows: `2777`
- Candidate quality-readable rows: `2774`
- Decoder counts: `{'cv2': 2773, 'pillow_fallback': 4}`
- Outlier percentile: `2.0`
- Candidate outlier rows: `507`
- Outlier flag counts: `{'high_aspect_ratio': 56, 'high_luminance': 56, 'high_saturation': 56, 'large_resolution': 62, 'low_aspect_ratio': 56, 'low_contrast': 56, 'low_laplacian_sharpness': 56, 'low_luminance': 56, 'low_saturation': 56, 'low_tenengrad_edges': 56, 'small_resolution': 56}`

## Outputs

- per-image quality audit: `metrics\manifests\full_algae_dewatermark_v1_quality_audit.tsv`
- outlier candidates: `metrics\manifests\full_algae_dewatermark_v1_quality_audit_outliers.tsv`
- summary json: `metrics\manifests\full_algae_dewatermark_v1_quality_audit.summary.json`

## Boundary

- Outlier thresholds are percentile-based over candidate images.
- Flags indicate samples for manual review, not automatic deletion or exclusion.
- This audit does not replace `full502_clean_v1` or `compare9_complete496_v1`, and it does not run Stage1 full-pool enhancement.
