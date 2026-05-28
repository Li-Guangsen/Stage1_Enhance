# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. What this repo is

Stage1Codex is the enhancement + downstream-validation support repo for **HAB (harmful algal bloom) underwater microscopic images** — not general underwater enhancement. Its current cross-project role is to provide `task-driven structure-preserving input formation` for the MyEdge/MSFI paper, not to be pitched as a standalone "enhancement + edge-detection pipeline" innovation.

The project is past early exploration. It is now in a **governance-first state**: experiment registry, candidate archival, formal source assets, and paper-metric splits already exist and must not be conflated.

## 2. Mandatory entry-point docs

Before doing anything non-trivial, read these in order. `AGENTS.md` lists the full set; the minimum is:

1. `AGENTS.md` (short entry rules)
2. `README.md`
3. `docs/project_execution_rules_cn.md` (full rules — supersedes AGENTS.md when in doubt)
4. `docs/current_experiment_status_cn.md` (stop points + forbidden claims)
5. `docs/goal_design_contract_cn.md` (what counts as "done" vs "diagnostic")
6. `docs/candidate_lifecycle_policy_cn.md`
7. `docs/project_handoff_guide_cn.md`
8. `docs/project_status_overview_cn.md`
9. `research-state.yaml`
10. `metrics/experiment_registry.csv`, `metrics/candidate_registry.csv`, `metrics/registry_schema_cn.md`
11. `experiments/AGENTS.override.md` (strictly stricter rules for `experiments/`)

Working under `experiments/` requires obeying `experiments/AGENTS.override.md` in addition to root rules.

## 3. Pipeline architecture

Fixed stage order:

```
Original -> BPH -> IMF1Ray / RGHS / CLAHE -> Fused -> Final
```

Module map (top-level files are the canonical stage implementations — not `src/`):

| Stage | Module | Real responsibility (use this in writing) |
| --- | --- | --- |
| `BPH` | `lgsbph.py` (`lgs_accc_bgr_improved`) | gray-pixel-guided pre-white-balance |
| `IMF1Ray` | `pybemd.py` (`imf1Ray_from_bgr`) | IMF1-Rayleigh high-frequency detail branch |
| `RGHS` | `wb_safe_contrast.py` (`wb_safe_contrast`) | WB-safe contrast branch (NOT vanilla RGHS) |
| `CLAHE` | `clahe_guided_visibility.py` (`clahe_3ch_wb_safe`) | CLAHE-guided local visibility branch (NOT vanilla CLAHE) |
| `Fused` | `fusion_three.py` (`fuse_three_images_bgr`) | feature-gated three-branch luminance/structure fusion |
| `Final` | `lvbo.py` + dispatch in `main.py:_final_refine` | lightweight illumination + contrast closure |

`main.py` is the orchestrator. `final.mode` in the params JSON dispatches between many closure modes (homomorphic / entropy / `original` / `bph` / `full_flow_downstream_stage1_mainline_v1|v2` / `topology_locked_visual_chroma_full_flow_v1` / `e01_*` / etc.). Branch-specific code lives in:

- `stage1_full_flow_mainline.py` — FF01/FF02/TLVC01 full-flow modes
- `stage1_e01_task_guided_family.py` — E01-A / E01-B task-guided modes
- `stage1_downstream_candidates.py` — P12–P28 / D01 diagnostic modes and the `_final_source_requirements` helper consumed by `main.py`

Adding a new `final.mode` requires registering it in the dispatcher used by `_final_refine` and the `is_*_mode` predicates the module exports. Do not register new modes without satisfying the candidate gate in §6.

## 4. Running things

### Formal enhancement (paper mainline)

Never treat plain `python main.py` as the formal mainline — the default params JSON is `best_full506_r4_03.json`, which is historical. Formal runs must explicitly pass the locked config:

```
python main.py --params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json --input-dir <input> --output-dir <isolated_root>
```

Manifest-driven runs use `--manifest <path>`. `main.py` supports manifest paths relative to `input-dir`, recursive lookup by name or stem, `.webp`, nested outputs, and Unicode (CJK) paths via `np.fromfile` + `cv2.imdecode`. Use 1-image smokes (`--limit 1`) before full runs. Use `--skip-existing` for resumable long runs.

Long full-pool run entry: `experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1`. After it finishes, run `metrics/scripts/intake_stage1_fullpool_run_outputs.py` to generate the read-only intake report.

### Official evaluation (overwrites formal output dirs)

```
metrics/scripts/run_official_evaluations.ps1   # PowerShell wrapper
```

This rebuilds the manifests and **overwrites**:

- `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
- `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`

The `compare9_complete496` rerun depends on external-method output directories that are absolute paths on the current workstation and are not in the repo.

### MyEdge 166 enhancement metric baseline (current primary screening)

```
metrics/scripts/run_myedge168_compare9_rerun.py
metrics/scripts/evaluate_myedge168_enhancement_baseline_v2.py
```

Outputs land under `experiments/myedge168_compare9_rerun_20260527/`. Main table is the 166 complete-case (excludes `chazhuang.3.jpg` and `chazhuang.6.jpg`); supplement table is 168-minus-WWPF.

### Python environments (different per concern)

- Stage1 enhancement + protocol-v2 evaluation: `D:\Desktop\EdgeDetection\my_env\python.exe`
- Codex-side YAML / CSV / doc structure checks: `D:/Desktop/DeepLearning/my_env/python.exe`
- Never use bare `python` unless the task explicitly is about the system default.

### Shell context

The agent runs under bash on Windows (Git Bash MINGW64). When emitting commands for the user, state the context explicitly (Windows PowerShell, CMD, WSL, remote). For WSL eval/show:

- Simple commands: `wsl bash -lc '...'` with single quotes only.
- Multi-run / arrays / loops: write a `.sh` and call `wsl bash script.sh`. Do not embed complex Bash inside PowerShell double-quoted `$cmd` — PowerShell will pre-expand `$run`, `$root`, `$PY` before WSL sees them.

## 5. Formal asset vs paper-metric splits

These layers are distinct — never conflate them:

| Layer | Path / identifier |
| --- | --- |
| Formal source config | `experiments/optimization_v1/configs/locked_full506_final_mainline.json` |
| Formal source output root | `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline` |
| Paper stage table | `full502_clean_v1` → `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502` |
| Paper main comparison | `compare9_complete496_v1` → `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496` |
| Primary downstream validation (current) | MyEdge 166 complete-case (`metrics/manifests/myedge166_complete_case_20260528.csv`), excludes `chazhuang.3.jpg` and `chazhuang.6.jpg` |
| Historical downstream diagnostic | MyEdge 168 GT split |
| Engineering full-pool (readiness only) | `full_algae_dewatermark_v1` (2770 cv2-readable) |

`full506_final_mainline` is a source-asset directory name, not the paper sample count. 502/496 is for enhancement metrics only; 2770 cannot replace 166 downstream validation; 166 is the unified screening + fixed-detector validation split going forward.

## 6. Candidate governance (hard gate)

This is the most enforced rule in the repo. Do **not** create a new `Pxx` / `Dxx` / `FFxx` / `TLVCxx` / `Exx` candidate, and do not derive same-family `guard` / `fallback` / `raw-pullback` variants, unless all of these exist first:

1. A method review explaining the mechanism and how it differs from the last family.
2. A filled run sheet based on `docs/experiment_run_sheet_template_cn.md`.
3. Isolated config and output root (no overwriting legacy / official assets / GT / weights / MAT / MyEdge `output_test`).
4. Validation plan: smoke → MyEdge 166 enhance → fixed DiffusionEdge/MSFI → intake → structure proxy → decision.
5. A stop condition.
6. Registry entries in `metrics/experiment_registry.csv` and `metrics/candidate_registry.csv` per `metrics/registry_schema_cn.md`.

Every experiment must end in one of: `archive_failure`, `archive_diagnostic`, `iterate_after_method_review`, `promote_to_downstream_gate`, `promote_after_strong_pass`. Two consecutive same-family mixed/weak results forces a stop + method review or archival. Failed candidates are kept as evidence — never deleted, overwritten, or masked by later runs.

The following gates are **diagnostic only**, never "done":
`candidate_rescues_legacy_but_not_near_raw`, `candidate_metric_near_raw_structure_mixed`, `mechanism-complete weak candidate`, proxy-only, readiness-only.

Current archived diagnostic candidates: P12–P28, D01 (`d01_structure_flow_v1`), FF01, FF02, TLVC01, E01-A, E01-B. None of these are a Stage1 downstream success.

## 7. Forbidden writing patterns

Do not write any of:

- "Comprehensively beats SOTA" / "All metrics optimal"
- "Stage1 has stably improved downstream edge detection" (locked `Final` is a downstream negative control under the historical 168 fixed-detector regime)
- "D01 / P27 is a formal success candidate"
- "2770 is a formal full-pool result"
- "Wu 2026 datasets are confirmed identical to ours" (no file-level overlap proven)
- "HLRP / Histoformer are generally invalid" (they are HAB-microscopy-protocol failure cases only)

`MS_SSIM` and `PSNR` are explained as **structural consistency relative to the original image**, not quality vs. an enhancement ground truth. `WWPF` is kept and explained as a 496-image-stable strong baseline; do not delete it from comparisons.

## 8. Writing language

Chinese-first for the current paper-writing and evidence-alignment phase. English is reserved for paper title, method names, abbreviations, original-paper titles, code identifiers, and explicitly-labeled English auxiliary drafts. New project docs / status / rules default to Chinese.

## 9. State-update obligation

Any change to project state must propagate to:

- `research-log.md` — append-only, never rewrite history
- `research-state.yaml`
- `docs/project_handoff_guide_cn.md`, `docs/project_status_overview_cn.md`, `docs/current_experiment_status_cn.md` (when formal mainline / metric / split changes)
- `docs/comparison_methods_results_index_cn.md` (when comparison surface changes)
- Registries (`experiment_registry.csv`, `candidate_registry.csv`) for any candidate-level change

When a recurring problem surfaces, convert it into a rule and add it to `docs/project_execution_rules_cn.md` (and `AGENTS.md` if every agent must see it on first read).

## 10. Sub-agents

For long-context, cross-directory, or independent-review work, the main agent may delegate read-only checks to sub-agents. Limits: `max_threads <= 6`, `max_depth = 1` (direct children only — no grandchildren). Sub-agents do not own write actions, formal-mainline judgments, or state-doc updates; the main agent owns final decisions and registry/log writes.

## 11. Cross-repo coupling (external working directories)

This repo does not stand alone. Stage1 candidates only become validated through downstream fixed-detector runs in a sibling repo. Treat the following as load-bearing dependencies.

### 11.1 `D:\Desktop\MyEdgeCodex` — downstream coupling target (primary)

A separate research repo for HAB-microscopy edge detection, built on `2024_AAAI_DiffusionEdge`. Its core contribution is the `MSFI` block in the latent U-Net bottleneck. The current Stage1 cross-project role (`docs/project_status_overview_cn.md`): *Stage1 provides task-driven structure-preserving input formation for MyEdge/MSFI.*

Key directories there (all paths absolute on this workstation, **never modify without explicit user confirmation**):

| Path | Role |
| --- | --- |
| `D:/Desktop/MyEdgeCodex/input_test/algae/` | 168-image raw MyEdge split — source of the current 166 complete-case (excludes `chazhuang.3.jpg`, `chazhuang.6.jpg`) |
| `D:/Desktop/MyEdgeCodex/GT/ALGAE/` | edge GT for eval — protected, do not regenerate |
| `D:/Desktop/MyEdgeCodex/checkpoints/algae/model-10.pt` | `Ours / MSFI 50k` (a.k.a. `MSFI + EMA + slide/non-resize + 50k`) — current MSFI checkpoint |
| `D:/Desktop/MyEdgeCodex/checkpoints/first_stage_total_320.pt` | first-stage VAE |
| `D:/Desktop/MyEdgeCodex/baseline_diffusionedge/training_artifacts/model-10.pt` | DiffusionEdge baseline 50k checkpoint |
| `D:/Desktop/MyEdgeCodex/configs/algae_sample.yaml` | MSFI 50k sampling config |
| `D:/Desktop/MyEdgeCodex/configs/stage1_coupling/*.yaml` | per-Stage1-candidate sampling configs (MSFI side and `diffusionedge_baseline_*` side) |
| `D:/Desktop/MyEdgeCodex/stage1_coupling_inputs/` | Stage1 outputs staged here (by original MyEdge stem, NOT `_Final` suffix) |
| `D:/Desktop/MyEdgeCodex/output_test/MSFI/algae/ema_slide_50k/` | MSFI 50k formal output (raw anchor lives here) |
| `D:/Desktop/MyEdgeCodex/output_test/baseline_diffusionedge/50k_pre_refresh_20260522/` | DiffusionEdge baseline 50k formal output |
| `D:/Desktop/MyEdgeCodex/output_test/MSFI/algae/stage1_coupling/` | per-Stage1-candidate MSFI sampling output roots (`downstream_v1_<candidate>_168_<Pxx>_<date>`) |
| `D:/Desktop/MyEdgeCodex/output_test/baseline_diffusionedge/stage1_coupling/` | per-Stage1-candidate baseline sampling output roots |
| `D:/Desktop/MyEdgeCodex/eval-edge-py/` | WSL evaluator (Python + C++); `eval.py` produces `eval_bdry.txt`, `show.py` produces `show.log` + AC |
| `D:/Desktop/MyEdgeCodex/docs/paper_assets/stage1_coupling/` | Stage1-coupling planning, preflight, results, structure proxy, gate, run-report assets |
| `D:/Desktop/MyEdgeCodex/docs/research_contracts/` | per-candidate run sheets and execution command sheets |

Protected assets (per MyEdge `AGENTS.md` §3): `data/`, `GT/`, `checkpoints/`, `input_test/`, `output_test/`, `eval-edge-py/dataTest/`, `eval-edge-py/GT/`. Do not touch these from Stage1 work.

### 11.2 Standard coupling pipeline (Stage1 → MyEdge)

Per `docs/stage1_to_myedge_downstream_workflow_cn.md`. The chain is fixed; do not collapse steps or merge into one shell call:

1. Stage1 generates candidate `Final` outputs and filters to the **MyEdge 166 complete-case** (manifest: `metrics/manifests/myedge166_complete_case_20260528.csv`).
2. Read-only check stem / count / decode / manifest on the Stage1 side.
3. MyEdge-side staging into `stage1_coupling_inputs/...` by **original stem** (drop `_Final` suffix, or GT name-matching breaks).
4. Sample under fixed MSFI 50k **and** fixed DiffusionEdge baseline 50k. Sampling is run on Windows.
5. WSL `eval.py` / `show.py` is run **only via a `.sh` script** under `docs/paper_assets/stage1_coupling/run_<candidate>_eval_show_<date>.sh`, invoked as `wsl bash <script.sh>`. PowerShell pre-expands Bash variables — `$run`, `$root`, `$PY`, `${run}` — so embedding multi-run Bash in a PowerShell double-quoted `$cmd` produces empty paths and `command not found`. This is the single most common failure mode on this coupling.
6. Result intake via `docs/paper_assets/scripts/sync_*_results.py` (read-only by default; `--write-assets` writes `white/overlay/error_map/manifest.csv/run_report.md` into the run root).
7. Structure proxy via `docs/paper_assets/scripts/analyze_*_structure_metrics.py` — diagnostic only, never replaces ODS/OIS/AP/AC.
8. Gate decision written back to MyEdge `docs/paper_assets/stage1_coupling/<candidate>_downstream_gate_<date>.md` and to Stage1 status / registry / `research-log.md`.

During the fixed-detector phase, never modify: detector code, weights, GT, MAT outputs, eval protocol, or MyEdge formal result roots. Training / sampling / eval / show require explicit user confirmation per MyEdge `AGENTS.md` §3.

### 11.3 Where Stage1's MyEdge mirror docs come from

The Stage1-side snapshots are read-only mirrors of upstream MyEdge files. When updating them, pull from the source, do not author independently:

| Stage1 file (mirror) | MyEdge source |
| --- | --- |
| `docs/stage1_myedge_coupling_status_20260525_cn.md` | `docs/paper_assets/stage1_coupling/p1_results_intake_pending_20260525.md`, `p1_report_asset_sync_status_20260525.md`, and the per-Pxx `*_downstream_gate_*.md` files |
| FF01/FF02/TLVC01/E01 v8 evidence references in `docs/evidence/` | `docs/paper_assets/stage1_coupling/full_flow_downstream_stage1_mainline_v1_v8_results_20260527.md`, `*_structure_metrics_20260527.md`, `*_downstream_gate_20260527.md` (and analogous v2 / TLVC01 / E01-A / E01-B files) |

### 11.4 Other external dependencies

| Path | Role | Status |
| --- | --- | --- |
| `D:\Desktop\去水印所有藻类图像` | original source of `full_algae_dewatermark_v1` (2777 → 2774 → 2770 cv2-readable) | engineering pool, 544 manual reviews pending; cannot substitute for 166 downstream validation |
| `D:\Desktop\EdgeDetection\my_env\python.exe` | Stage1 enhancement + protocol-v2 evaluation interpreter | required for formal runs |
| `D:/Desktop/DeepLearning/my_env/python.exe` | Codex-side docs / YAML / CSV structure checks | required for lightweight checks |
| `D:\Desktop\DiffusionEdge` | original DiffusionEdge code path used as `PYTHONPATH` when sampling against the baseline 50k checkpoint (MyEdge wrapper has a key-mismatch failure mode, kept as a known-failure log) | invoked only by MyEdge baseline sampling |
| `D:/Desktop/Canny`, `D:/Desktop/RCF`, `D:/Desktop/BDCN`, `D:/Desktop/PiDiNet`, `D:/Desktop/TEED`, `D:/Desktop/DexiNed`, `D:/Desktop/LDC`, `D:/Desktop/EDTER` | external-method reproduction roots referenced by `compare9_complete496` and MyEdge baseline reproduction | absolute workstation paths, not in any repo |

None of these are version-controlled with Stage1Codex. Treat their absolute paths as machine-local invariants; do not hardcode them into new scripts without a config-driven override.

## 12. Historical assets — auditable, not entry points

Do not delete, but do not treat as current truth: `results_optimized_c25/`, old `full506` eval dirs, `metrics/archive/`, `AIlog/`, `notion_mirror/`, `tetetete/`, `to_human/`, `ablation/`, old pilot/H1/H2/H3 drafts, root-level `method-*.md` and `related-work-*.md` historical drafts. Current paper writing source of truth is `paper/`.
