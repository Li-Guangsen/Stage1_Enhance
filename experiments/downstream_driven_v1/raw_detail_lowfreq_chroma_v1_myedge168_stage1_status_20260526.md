# P27 raw_detail_lowfreq_chroma_v1 status

Date: 2026-05-26

This is a non-mainline downstream-driven Stage1 candidate. It does not replace
the locked paper mainline config or outputs.

- Variant: `raw_detail_lowfreq_chroma_v1`
- Config: `experiments/downstream_driven_v1/configs/raw_detail_lowfreq_chroma_v1.json`
- Final mode: `raw_detail_lowfreq_chroma_bph`
- Stage1 MyEdge168 output: `experiments/downstream_driven_v1/outputs/myedge168/raw_detail_lowfreq_chroma_v1`
- Stage1 full502 output: `experiments/downstream_driven_v1/outputs/full502/raw_detail_lowfreq_chroma_v1`
- Stage1 proxy prescreen: `docs/stage1_myedge168_gt_edge_proxy_prescreen_p27_20260526_cn.md`
- MyEdge preflight: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/raw_detail_lowfreq_chroma_p27_preflight_20260526.md`
- MyEdge results: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/raw_detail_lowfreq_chroma_p27_results_20260526.md`
- MyEdge structure proxy: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/raw_detail_lowfreq_chroma_p27_structure_metrics_20260526.md`
- MyEdge downstream gate: `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/raw_detail_lowfreq_chroma_p27_downstream_gate_20260526.md`
- full502 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p27_full502_20260526`
- compare496 metrics: `metrics/outputs/evaluate_protocol_v2/downstream_driven_p27_compare496_20260526`

## Scope

- 168-image MyEdge ALGAE split with GT edge maps for fixed-detector downstream validation.
- `full502_clean_v1` and `compare9_complete496_v1` only for Stage1 enhancement metrics.
- No 2770-image full-pool run.
- No overwrite of formal Stage1 mainline assets.
- No MyEdge training or checkpoint changes.

## Readiness

| Asset | Count / status |
|---|---:|
| MyEdge168 Final PNG | 168 |
| MyEdge168 Final JPG | 168 |
| full502 Final PNG | 502 |
| full502 Final JPG | 502 |
| MyEdge sampling/eval/show | complete |
| Result intake | `complete_with_report_assets` |
| Structure proxy | `complete` |
| Downstream gate | `candidate_metric_near_raw_structure_mixed` |

## Stage1 Proxy Prescreen

P27 is an edge-safe proxy candidate rather than a proxy-positive candidate.

| Metric vs raw proxy | Delta |
|---|---:|
| F1 | +0.000228 |
| False-edge ratio | -0.000344 |
| Endpoints/kpx | +0.076285 |

## Fixed-detector Metrics

| Detector/input | ODS | OIS | AP | AC |
|---|---:|---:|---:|---:|
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P27 | 0.783329 | 0.794822 | 0.346115 | 0.7951 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline P27 | 0.772587 | 0.782971 | 0.372084 | 0.7949 |

## Structure Proxy vs Raw

| Detector | dF1 | dFalse-edge | dEndpoints/kpx | Structure non-worse |
|---|---:|---:|---:|---|
| MSFI | +0.000577 | -0.013685 | -1.160557 | true |
| DiffusionEdge baseline | -0.000099 | +0.003972 | -0.176182 | false |

## Enhancement Metrics

`MS_SSIM` and `PSNR` are relative structure consistency to the original image,
not GT enhancement quality.

| Protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `full502_clean_v1` | 502 | 2.554038 | 26.220755 | 2.768436 | 0.999026 | 51.021551 | 2.225860 | 7.252755 |
| `compare9_complete496_v1` | 496 | 2.443638 | 24.875176 | 2.702260 | 0.999019 | 50.952416 | 2.250301 | 7.060930 |

## Interpretation

- P27 uses a new mechanism: raw high-frequency/luma detail is preserved while
  only low-frequency illumination/chroma is adjusted from BPH-like evidence.
- It clearly rescues the legacy Stage1 Final downstream collapse.
- It reaches metric-near-raw on both fixed detectors and is stronger than P26
  on gate decision.
- It is not a strong pass: DiffusionEdge baseline structure proxy remains mixed
  because false-edge ratio is worse than raw by `+0.003972`, although endpoints
  improve.
- P27 should be kept as a candidate-pass diagnostic, not as a stable
  downstream-improving Stage1 mainline.
- Do not expand P27 to the 2770-image full pool from this gate alone.
