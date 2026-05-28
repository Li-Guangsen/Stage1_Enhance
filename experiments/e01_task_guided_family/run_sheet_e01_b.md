# E01-B wavelet-pyramid weak-boundary run sheet

Date: 2026-05-27

## 1. Scope

- Candidate: `E01-B`
- Mode: `e01_b_wavelet_pyramid_weak_boundary_v1`
- Primary hypothesis: wavelet-like LH/HL weak-boundary reconstruction plus HH texture suppression can preserve detector-compatible topology better than FF01/FF02 full-flow fusion and E01-A color/illumination dominant reconstruction.
- Current phase: 168-image MyEdge ALGAE fixed-detector validation only.
- Blocked: no `full502_clean_v1`, no `compare9_complete496_v1`, no 2770 full-pool, no MyEdge/MSFI training.

## 2. Pre-run locked baselines

### Raw baseline

| Detector | ODS | OIS | AP | AC |
|---|---:|---:|---:|---:|
| MSFI 50k raw | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| DiffusionEdge baseline 50k raw | 0.770521 | 0.779986 | 0.363065 | 0.796900 |

### Legacy Final baseline

| Detector | ODS | OIS | AP | AC |
|---|---:|---:|---:|---:|
| MSFI legacy Final | 0.588287 | 0.671357 | 0.263997 | 0.740300 |
| DiffusionEdge legacy Final | 0.530094 | 0.567910 | 0.224073 | 0.734900 |

### Raw-near tolerance

- ODS/OIS: candidate >= raw - `0.002`
- AP/AC: candidate >= raw - `0.003`
- Strict raw-near requires all four metrics for the same detector.

### Positive gain threshold

- detector-positive: ODS >= raw + `0.002` or AP >= raw + `0.003`, with AP/AC strict raw-near.
- strong success: both detectors detector-positive and structure proxy not-collapsed.
- acceptable success: one detector detector-positive, the other detector strict raw-near, and structure proxy not-collapsed.
- minimum safe: both detectors strict raw-near and structure proxy not-collapsed.
- failure: below raw-near, rescue-only, proxy-only, visual-only, or structure collapse.

### Structure proxy

- strict non-worse: dF1 >= `0`, dFalse-edge <= `0`, dEndpoints/kpx <= `0`.
- not-collapsed: dF1 >= `-0.005`, dFalse-edge <= `+0.010`, dEndpoints/kpx <= `+1.000`.

These thresholds are locked before E01-B 168 execution and must not be changed after seeing results.

## 3. Method and config

- family design: `docs/evidence/e01_task_guided_family/e01_task_guided_complete_enhancement_family_design_cn.md`
- method design: `docs/evidence/e01_task_guided_family/e01_b_wavelet_pyramid_weak_boundary_design_cn.md`
- code entry: `stage1_e01_task_guided_family.py`
- mode dispatch: `main.py final.mode=e01_b_wavelet_pyramid_weak_boundary_v1`
- config: `experiments/e01_task_guided_family/configs/e01_b_wavelet_pyramid_weak_boundary_v1.json`
- output root:
  - smoke: `experiments/e01_task_guided_family/outputs/smoke7_highrisk_v1/e01_b_wavelet_pyramid_weak_boundary_v1`
  - 168: `experiments/e01_task_guided_family/outputs/myedge168/e01_b_wavelet_pyramid_weak_boundary_v1`

## 4. Planned execution

1. Compile/code validation.
2. High-risk smoke on `experiments/e01_task_guided_family/manifests/smoke7_highrisk_v1.txt`.
3. Smoke completeness and raw-vs-Final risk summary.
4. Visual/structure risk review before 168.
5. 168 Stage1 enhancement from `D:/Desktop/MyEdgeCodex/input_test/algae` and `experiments/e01_task_guided_family/manifests/myedge168_v1.txt`.
6. MyEdge preflight/staging/config generation.
7. Fixed MSFI 50k and fixed DiffusionEdge baseline 50k sampling.
8. WSL eval/show via generated `.sh`.
9. Result intake, structure proxy, downstream gate.
10. Stage1 report, registry, current status, `research-state.yaml`, and `research-log.md` update.

## 5. Stop conditions

- Stop before 168 if smoke output is incomplete, decode fails, runtime projection exceeds 10 minutes, or high-risk panels show FF01/FF02-like background false-edge burst.
- Archive after 168 if E01-B is below raw-near, rescue-only, proxy-only, visual-only, or structure collapsed.
- If E01-B fails and E01-A already failed, either continue only to a genuinely different E01-C/E01-D mechanism after method review or close the current E01 phase if the accumulated evidence favors sidecar adaptation. The final post-gate decision is recorded below.

## 6. Decision

- gate result: `candidate_rescues_legacy_but_not_near_raw`
- E01 classification: `failure`
- compared with raw: DiffusionEdge baseline is detector-positive by AP (`+0.009502`), but MSFI AP drops by `-0.008301` and misses strict raw-near.
- compared with legacy Final: both detectors rescue legacy Stage1 Final collapse, but rescue-only is not success.
- compared with E01-A: E01-B improves DiffusionEdge AP but loses MSFI AP; neither candidate reaches E01 minimum-safe.
- compared with current best archived diagnostic reference P27: E01-B does not supersede P27 because P27 remains metric-near-raw structure-mixed while E01-B misses MSFI raw-near by AP.
- compared with FF01/FF02/TLVC01: E01-B is safer than FF01/FF02 structure-collapse failures and has stronger DiffusionEdge AP than TLVC01, but it remains a direct image-replacement failure.
- evidence report: `docs/evidence/e01_task_guided_family/e01_b_fixed_detector_gate_report_20260527_cn.md`
- family summary: `docs/evidence/e01_task_guided_family/e01_family_stage_summary_20260527_cn.md`
- decision: archive failure and close current E01 family phase after two mechanism-distinct 168 fixed-detector gates; recommend sidecar adaptation over E01-A/E01-B patching.
