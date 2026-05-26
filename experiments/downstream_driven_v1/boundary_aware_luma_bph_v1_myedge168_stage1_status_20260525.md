# Stage1 boundary_aware_luma_bph_v1 MyEdge168 Status

Date: 2026-05-25

This status records Stage1-side output readiness only. It does not include MyEdge sampling or edge metrics.

- Variant: `boundary_aware_luma_bph_v1`
- Config: `experiments/downstream_driven_v1/configs/boundary_aware_luma_bph_v1.json`
- Final mode: `boundary_aware_luma_bph`
- Smoke output root: `experiments/downstream_driven_v1/outputs/smoke_myedge168/boundary_aware_luma_bph_v1`
- MyEdge168 output root: `experiments/downstream_driven_v1/outputs/myedge168/boundary_aware_luma_bph_v1`

## Implementation intent

- Keep raw luminance structure close to the detector input domain.
- Apply clipped mild gamma/contrast, background bilateral smoothing, and high-gradient masked unsharp support in Lab luminance.
- Transfer only small BPH chroma; skip IMF1Ray/RGHS/CLAHE/Fusion/legacy Final.

## Counts

| Scope | Final PNG | Final JPG | non-Final files | decoded Final PNG | decode failures |
|---|---:|---:|---:|---:|---:|
| smoke | 2 | 2 | 0 | 2 | 0 |
| myedge168 | 168 | 168 | 0 | 168 | 0 |

## Boundary

- This is Stage1 code-path and I/O readiness only.
- No MyEdge sampling, WSL `eval.py`, WSL `show.py`, ODS/OIS/AP/AC, structure proxy, or training was run.
- Do not write this as downstream benefit before fixed-detector MyEdge evaluation and result intake are complete.
- Do not run 2770 full-pool from this candidate before the 168-image GT gate is reviewed.
