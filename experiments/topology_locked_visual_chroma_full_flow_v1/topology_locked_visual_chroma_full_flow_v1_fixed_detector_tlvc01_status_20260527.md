# TLVC01 topology-locked visual-chroma fixed-detector status

Date: 2026-05-27

## Summary

- Status: `complete_rescue_only_archived_diagnostic`
- Candidate ID: `TLVC01`
- Method: `topology_locked_visual_chroma_full_flow_v1`
- Gate decision: `candidate_rescues_legacy_but_not_near_raw`
- Role: correction-run for a complete Stage1 flow with raw-compatible luma topology, not a successful downstream-positive mainline.

TLVC01 restores a complete Stage1 enhancement skeleton while forcing the final gray/topology plane back to the exact MyEdge raw input. This corrects the earlier protocol issue where `data/inputImg/Original` was not byte/visual-equivalent to the MyEdge raw anchor. It rescues the legacy Stage1 Final downstream collapse, but it does not outperform or clearly match the raw anchor under the current strict two-detector gate.

## Stage1 Run

- Input root: `D:/Desktop/MyEdgeCodex/input_test/algae`
- Manifest: `experiments/full_flow_downstream_stage1_mainline_v1/manifests/myedge168_v1.txt`
- Output root: `experiments/topology_locked_visual_chroma_full_flow_v1/outputs/myedge168_v1_myedgeinput_grayplane090_anchorfix`
- Config: `experiments/topology_locked_visual_chroma_full_flow_v1/configs/topology_locked_visual_chroma_full_flow_v1.json`
- Runtime: `92.9` sec total, about `0.55` sec/image
- Completeness: Final PNG/JPG `168/168`, six stage PNG/JPG complete, decode failures `0`

Mean 168 raw-vs-Final proxy:

| Metric | Value |
|---|---:|
| mean_abs_bgr_delta | 10.7667 |
| mean_abs_luma_delta | 1.7113 |
| mean_abs_chroma_delta | 7.3842 |
| PSNR vs raw | 27.9651 |
| grad_mean_ratio | 0.9956 |
| luma_std_ratio | 1.0000 |

The Stage1/MyEdge168 GT edge proxy prescreen is raw-equivalent after the MyEdge-input gray-plane anchor fix:

| Variant | F1 | False-edge ratio | Endpoints / 1k skeleton px | dF1 | dFalse-edge | dEndpoints |
|---|---:|---:|---:|---:|---:|---:|
| raw_input_anchor | 0.581331 | 0.523693 | 56.100962 | 0.000000 | 0.000000 | 0.000000 |
| topology_locked_visual_chroma_full_flow_v1_myedgeinput_grayplane090_anchorfix | 0.581331 | 0.523693 | 56.100962 | 0.000000 | 0.000000 | 0.000000 |

This proxy is a safety check only. It does not prove downstream detector gain.

## Fixed-Detector Metrics

MyEdge fixed-detector result intake:

- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_results_20260527.md`
- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_structure_metrics_20260527.md`
- `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/topology_locked_visual_chroma_tlvc01_downstream_gate_20260527.md`

| Detector | Variant | ODS | OIS | AP | AC |
|---|---|---:|---:|---:|---:|
| MSFI 50k | raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI 50k | legacy Stage1 Final | 0.588287 | 0.671357 | 0.263997 | 0.740300 |
| MSFI 50k | TLVC01 | 0.782936 | 0.794718 | 0.345209 | 0.793200 |
| DiffusionEdge baseline 50k | raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.796900 |
| DiffusionEdge baseline 50k | legacy Stage1 Final | 0.530094 | 0.567910 | 0.224073 | 0.734900 |
| DiffusionEdge baseline 50k | TLVC01 | 0.768593 | 0.779518 | 0.362225 | 0.798500 |

Strict near-raw tolerance is `ODS/OIS <= 0.002`, `AP <= 0.003`, `AC <= 0.003` below raw. TLVC01 misses the all-detector candidate gate because MSFI AC is below tolerance and DiffusionEdge structure proxy is mixed.

## Structure Proxy

| Detector | dF1 | dPrecision | dRecall | dFalse-edge | dComponents | dEndpoints | Non-worse |
|---|---:|---:|---:|---:|---:|---:|---:|
| MSFI 50k | +0.0002 | +0.0088 | -0.0077 | -0.0088 | -0.4787 | -1.4481 | True |
| DiffusionEdge baseline 50k | -0.0030 | -0.0047 | -0.0008 | +0.0047 | -0.0755 | +0.3836 | False |

## Comparison

| Reference | TLVC01 change |
|---|---|
| raw anchor | close but not strict pass; no clear positive downstream gain |
| legacy Stage1 Final | strongly rescues the locked Final collapse on both fixed detectors |
| P27 | more complete visual/chroma flow but weaker downstream metrics; P27 DiffusionEdge AP is `0.372084` vs TLVC01 `0.362225` |
| D01 | more complete visual/chroma flow but weaker DiffusionEdge AP; D01 DiffusionEdge AP is `0.371149` |
| FF02 | much safer than FF02 direct replacement, but still not downstream-positive |

## Decision

TLVC01 proves the corrected full-flow idea can preserve raw-like luma topology when generated from the exact MyEdge raw input, and it is a better diagnostic than FF01/FF02 direct replacement. It still fails the project target because it does not provide a clear fixed-detector downstream positive gain and remains below P27/D01 on the stronger DiffusionEdge AP evidence.

Stop this Stage1-only direct replacement family here. Do not run 502/496 or 2770 as a candidate-promotion route from TLVC01. The next valid long-horizon route is to keep Stage1 complete enhancement evidence as sidecar / auxiliary maps while raw remains the detector topology anchor, then test MyEdge/MSFI adaptation in a separate authorized protocol.

## Boundary

- No MyEdge checkpoint was changed.
- No detector was retrained.
- No GT or eval protocol was changed.
- No formal Stage1 locked mainline asset was overwritten.
- No 502/496 enhancement comparison was run for TLVC01.
- No 2770 full-pool enhancement was run.
