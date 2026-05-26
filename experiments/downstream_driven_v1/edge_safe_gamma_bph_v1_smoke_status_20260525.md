# Edge-safe Gamma+BPH v1 Smoke Status

Date: 2026-05-25

This is a Stage1-only smoke check for a new downstream-driven diagnostic
candidate. It does not replace the locked Stage1 paper mainline.

## Variant

- Config: `experiments/downstream_driven_v1/configs/edge_safe_gamma_bph_v1.json`
- Final mode: `edge_safe_gamma_bph`
- Output root: `experiments/downstream_driven_v1/outputs/smoke_myedge168/edge_safe_gamma_bph_v1`
- Input root: `D:\Desktop\MyEdgeCodex\input_test\algae`
- Scope: first `2` images only

## Implementation

`edge_safe_gamma_bph` keeps detector-visible structure close to the raw image:

- raw Lab luminance receives only mild gamma/contrast adjustment;
- raw Lab chroma receives only mild BPH chroma transfer;
- IMF1Ray, RGHS, CLAHE, Fusion and legacy Final are skipped.

## Smoke Result

| Output | Count |
|---|---:|
| Final PNG | 2 |
| Final JPG | 2 |
| non-Final stage files | 0 |
| decoded Final PNG sample | 2 |

## Boundary

- This is code-path and I/O readiness only.
- No MyEdge sampling, WSL `eval.py`, WSL `show.py`, training, ODS/OIS/AP/AC, or structure-proxy recomputation was run.
- Do not claim downstream improvement from this smoke.
- If promoted, this candidate should first run on the 168-image MyEdge split and then enter fixed-detector MyEdge evaluation; do not enter the 2770-image pool from this smoke alone.
