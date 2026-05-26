# D01 structure flow v1 MyEdge168 Stage1 Status

Date: 2026-05-26

## Summary

- Variant: `d01_structure_flow_v1`
- Protocol: `downstream_driven_v2`
- Config: `experiments/downstream_driven_v2/configs/d01_structure_flow_v1.json`
- Final mode: `downstream_d01_structure_flow_bph`
- Input split: `D:/Desktop/MyEdgeCodex/input_test/algae`
- Output root: `experiments/downstream_driven_v2/outputs/myedge168/d01_structure_flow_v1`
- Stage1 runtime: about `24.04` seconds
- Final PNG: `168`
- Final JPG: `168`

## MyEdge Fixed-detector Results

| Detector | ODS | OIS | AP | AC | Raw anchor ODS/OIS/AP/AC |
|---|---:|---:|---:|---:|---|
| MSFI 50k | 0.783871 | 0.795067 | 0.346008 | 0.7934 | 0.783527 / 0.794213 / 0.345899 / 0.796846 |
| DiffusionEdge baseline 50k | 0.771730 | 0.783218 | 0.371149 | 0.7948 | 0.770521 / 0.779986 / 0.363065 / 0.7969 |

## Structure Proxy Delta vs Raw

| Detector | dF1 | dFalse-edge | dEndpoints/kpx | Decision |
|---|---:|---:|---:|---|
| MSFI 50k | +0.000343 | -0.013767 | -1.140514 | structure non-worse |
| DiffusionEdge baseline 50k | -0.000327 | +0.005265 | +0.353641 | mixed |

## Gate

- Strict downstream gate: `candidate_rescues_legacy_but_not_near_raw`
- Goal-level interpretation: weak/borderline candidate pass, not strong
- Main reason: MSFI ODS/OIS/AP are near or slightly above raw but AC is lower than raw by `0.003446`; DiffusionEdge baseline is metric-near-raw but structure proxy remains mixed.

## Boundary

- D01 rescues legacy Stage1 Final fixed-detector collapse.
- D01 is not a stable downstream-improving Stage1 mainline.
- D01 did not run `full502_clean_v1`, `compare9_complete496_v1`, or 2770 full-pool.
- No MyEdge training, checkpoint, GT, or eval-protocol change was made.
