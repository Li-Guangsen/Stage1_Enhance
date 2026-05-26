# Stage1 Calibrated Pyramid-Frequency P13 Status

Date: 2026-05-25

Variant: `calibrated_pyramid_frequency_v1`

Config: `experiments/downstream_driven_v1/configs/calibrated_pyramid_frequency_v1.json`

Output root: `experiments/downstream_driven_v1/outputs/myedge168/calibrated_pyramid_frequency_v1`

Scope: MyEdge ALGAE 168-image test split only.

## Stage1 Output Check

| Output | Count |
| --- | ---: |
| Final PNG | 168 |
| Final JPG | 168 |
| non-Final stage files | 0 |
| decoded Final PNG | 168 |

## MyEdge Fixed-Detector Result

| Detector / input | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P13 calibrated pyramid-frequency | 0.784769 | 0.796472 | 0.345621 | 0.7932 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline P13 calibrated pyramid-frequency | 0.774132 | 0.786695 | 0.369667 | 0.7917 |

Downstream gate: `candidate_rescues_legacy_but_not_near_raw`.

## Structure Proxy Delta vs Raw

| Detector | dF1 | dPrecision | dRecall | dFalse-edge | dComponents/kpx | dEndpoints/kpx |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MSFI | +0.0013 | +0.0106 | -0.0073 | -0.0106 | -0.3301 | -1.2913 |
| DiffusionEdge baseline | -0.0002 | +0.0012 | -0.0011 | -0.0012 | -0.5689 | -1.2643 |

## Enhancement-Metric Checks

`full502_clean_v1`:

| Method | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P13 | 502 | 2.8379 | 31.6862 | 3.0918 | 0.9974 | 46.7696 | 2.2573 | 7.8690 |
| P12 | 502 | 3.1175 | 38.9595 | 3.3848 | 0.9941 | 41.3295 | 2.2684 | 8.4089 |
| FormalFinal | 502 | 11.5985 | 544.5511 | 14.8472 | 0.7689 | 17.5534 | 4.0918 | 23.9227 |

`compare9_complete496_v1`:

| Method | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P13 | 496 | 2.7324 | 30.2551 | 3.0258 | 0.9974 | 46.7865 | 2.2820 | 7.6897 |
| P12 | 496 | 3.0130 | 37.4205 | 3.3176 | 0.9941 | 41.3560 | 2.2933 | 8.2337 |
| FormalFinal | 496 | 11.5094 | 543.0379 | 14.8101 | 0.7689 | 17.6237 | 4.1371 | 23.7718 |

## Boundary

- P13 rescues the legacy Stage1 Final collapse but is not a strong pass.
- Compared with P12, P13 recovers some AP/AC trade-off but gives up P12's stronger ODS/OIS and baseline AP.
- P13 is more conservative than P12 in enhancement metrics and much weaker than FormalFinal in EME/Contrast/AvgGra/UCIQE/UIQM.
- `MS_SSIM` and `PSNR` here remain relative structure consistency to original, not GT enhancement quality.
- Do not expand P13 to the 2770-image full pool and do not write it as a stable downstream-improving mainline.
