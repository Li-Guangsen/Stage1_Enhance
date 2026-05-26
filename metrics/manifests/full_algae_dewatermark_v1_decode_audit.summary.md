# full_algae_dewatermark_v1 decode / dimension audit

Generated at: `2026-05-24T23:17:59`

This is a data audit only. It does not run Stage1 enhancement, MyEdge evaluation, or any metric experiment.

## Summary

| Scope | Rows | Readable | Decode failures | Missing files | Width range | Height range |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| All images | 2777 | 2773 | 4 | 0 | 67-4096 | 54-4096 |
| Candidate images | 2774 | 2770 | 4 | 0 | 67-4096 | 54-4096 |
| Root-level images | 3 | 3 | 0 | 0 | 1144-1144 | 856-856 |

## Candidate Channel / Dtype Counts

- Channels: `{'3': 2514, '4': 256}`
- Dtypes: `{'uint8': 2770}`
- Color categories: `{'color_3ch': 2514, 'color_alpha_4ch': 256}`

## Candidate Top Shapes

| Shape | Count |
| --- | ---: |
| `450x450x3` | 781 |
| `600x800x4` | 107 |
| `675x900x3` | 53 |
| `548x752x3` | 38 |
| `375x500x3` | 34 |
| `350x400x3` | 34 |
| `400x533x3` | 31 |
| `580x800x3` | 31 |
| `1536x2048x3` | 26 |
| `297x396x3` | 26 |

## Outputs

- Per-image audit TSV: `full_algae_dewatermark_v1_decode_audit.tsv`
- Folder summary TSV: `full_algae_dewatermark_v1_decode_audit_folder_summary.tsv`
- Machine summary JSON: `full_algae_dewatermark_v1_decode_audit.summary.json`
- OpenCV-readable candidate manifest: `full_algae_dewatermark_v1_cv2_readable_candidate.txt`
- Decode failure list: `full_algae_dewatermark_v1_decode_failures.tsv`
