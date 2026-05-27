# Stage1/MyEdge168 GT Edge Proxy Prescreen

Date: 2026-05-27

## Scope

- Reads MyEdge 168-image coupling manifest, raw inputs, GT edge maps, locked Stage1 Final outputs, and existing downstream-driven Stage1 candidate outputs.
- Builds image-gradient proxy edges with Sobel magnitude + Otsu threshold, then matches them to GT edge maps with 2 px tolerance.
- Does not run MyEdge sampling, WSL `eval.py`, WSL `show.py`, training, or formal Stage1 full502/full2770 enhancement.
- This is a prescreen only. It cannot replace fixed-detector ODS/OIS/AP/AC, detector MAT structure proxy, repeat/control, or paper-ready downstream evidence.

## Summary

| Variant | n | Decision | F1 | Precision | Recall | False-edge ratio | Missed-GT ratio | Components / 1k edge px | Endpoints / 1k skeleton px | Mean abs luma delta | dF1 | dFalse-edge | dEndpoints |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `raw_input_anchor` | 168 | `raw_anchor` | 0.581331 | 0.476307 | 0.896202 | 0.523693 | 0.103798 | 10.623044 | 56.100962 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `legacy_stage1_final` | 168 | `proxy_negative_or_risky` | 0.409419 | 0.291554 | 0.942396 | 0.708446 | 0.057604 | 24.482514 | 78.854652 | 32.072009 | -0.171912 | 0.184754 | 22.753689 |
| `edge_preserve_original_control` | 168 | `raw_equivalent_control` | 0.581331 | 0.476307 | 0.896202 | 0.523693 | 0.103798 | 10.623044 | 56.100962 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `edge_preserve_raw_bph_mild_v1` | 168 | `proxy_edge_safe_candidate` | 0.581426 | 0.476818 | 0.895600 | 0.523182 | 0.104400 | 10.704260 | 56.403390 | 0.669904 | 0.000096 | -0.000510 | 0.302428 |
| `edge_preserve_raw_bph_moderate_v1` | 168 | `proxy_edge_safe_candidate` | 0.581700 | 0.477023 | 0.895544 | 0.522977 | 0.104456 | 10.739858 | 56.760669 | 0.589247 | 0.000369 | -0.000715 | 0.659706 |
| `generic_luma_clahe_mild_v1` | 168 | `proxy_mixed_watch` | 0.573760 | 0.467591 | 0.900381 | 0.532409 | 0.099619 | 11.280220 | 57.921956 | 1.157459 | -0.007571 | 0.008716 | 1.820994 |
| `generic_luma_gamma_mild_v1` | 168 | `proxy_edge_safe_candidate` | 0.581190 | 0.476364 | 0.895731 | 0.523636 | 0.104269 | 10.660389 | 56.089737 | 1.028215 | -0.000141 | -0.000057 | -0.011225 |
| `edge_safe_gamma_bph_v1` | 168 | `proxy_edge_safe_candidate` | 0.581399 | 0.476646 | 0.895854 | 0.523354 | 0.104146 | 10.788912 | 56.143160 | 0.706679 | 0.000069 | -0.000339 | 0.042197 |
| `boundary_aware_luma_bph_v1` | 168 | `proxy_edge_safe_candidate` | 0.582988 | 0.478175 | 0.895771 | 0.521825 | 0.104229 | 10.827427 | 56.464323 | 0.433829 | 0.001657 | -0.001868 | 0.363361 |
| `skeleton_safe_luma_bph_v1` | 168 | `proxy_positive_candidate` | 0.582406 | 0.478091 | 0.894752 | 0.521909 | 0.105248 | 10.185774 | 54.798263 | 0.557185 | 0.001075 | -0.001783 | -1.302699 |
| `c01_microstructure_csp_v1` | 168 | `proxy_edge_safe_candidate` | 0.581825 | 0.477212 | 0.896573 | 0.522788 | 0.103427 | 10.890952 | 56.491049 | 0.756317 | 0.000495 | -0.000905 | 0.390087 |
| `topology_guarded_microfusion_v1` | 168 | `proxy_edge_safe_candidate` | 0.583029 | 0.479294 | 0.894911 | 0.520706 | 0.105089 | 10.510573 | 56.240639 | 0.969681 | 0.001698 | -0.002987 | 0.139677 |
| `topology_pruned_microfusion_v1` | 168 | `proxy_positive_candidate` | 0.582945 | 0.478609 | 0.895764 | 0.521391 | 0.104236 | 10.672734 | 55.708294 | 0.956613 | 0.001614 | -0.002302 | -0.392668 |
| `baseline_stabilized_microfusion_v1` | 168 | `proxy_positive_candidate` | 0.582533 | 0.478155 | 0.895754 | 0.521845 | 0.104246 | 10.639857 | 55.844029 | 0.968217 | 0.001203 | -0.001847 | -0.256934 |
| `endpoint_stabilized_weak_boundary_v1` | 168 | `proxy_positive_candidate` | 0.581774 | 0.477408 | 0.894545 | 0.522592 | 0.105455 | 10.240943 | 55.291316 | 1.093138 | 0.000443 | -0.001100 | -0.809646 |
| `balanced_weak_boundary_pyramid_fusion_v1` | 168 | `proxy_positive_candidate` | 0.583371 | 0.479467 | 0.894977 | 0.520533 | 0.105023 | 10.293365 | 55.851367 | 0.940168 | 0.002041 | -0.003159 | -0.249596 |
| `ac_guarded_weak_boundary_fusion_v1` | 168 | `proxy_positive_candidate` | 0.583110 | 0.479076 | 0.894917 | 0.520924 | 0.105083 | 10.439433 | 55.842308 | 1.032475 | 0.001780 | -0.002768 | -0.258654 |
| `precision_rebalanced_ac_guarded_weak_boundary_fusion_v1` | 168 | `proxy_positive_candidate` | 0.581407 | 0.476899 | 0.895121 | 0.523101 | 0.104879 | 10.535039 | 55.779742 | 0.962900 | 0.000077 | -0.000591 | -0.321220 |
| `false_edge_floor_ac_guarded_weak_boundary_fusion_v1` | 168 | `proxy_positive_candidate` | 0.582568 | 0.478533 | 0.894301 | 0.521467 | 0.105699 | 10.391925 | 55.193017 | 0.918940 | 0.001237 | -0.002226 | -0.907946 |
| `ap_preserving_ac_guarded_weak_boundary_fusion_v1` | 168 | `proxy_positive_candidate` | 0.581611 | 0.477164 | 0.895004 | 0.522836 | 0.104996 | 10.409490 | 55.487330 | 0.951648 | 0.000280 | -0.000856 | -0.613632 |
| `dual_anchor_false_edge_floor_v1` | 168 | `proxy_positive_candidate` | 0.581424 | 0.476871 | 0.895322 | 0.523129 | 0.104678 | 10.452074 | 55.373245 | 0.954037 | 0.000093 | -0.000564 | -0.727718 |
| `raw_detail_lowfreq_chroma_v1` | 168 | `proxy_edge_safe_candidate` | 0.581559 | 0.476652 | 0.896120 | 0.523348 | 0.103880 | 10.712563 | 56.177247 | 0.677422 | 0.000228 | -0.000344 | 0.076285 |
| `raw_detail_chroma_guard_v1` | 168 | `proxy_edge_safe_candidate` | 0.581260 | 0.476359 | 0.896070 | 0.523641 | 0.103930 | 10.707852 | 56.275929 | 0.693654 | -0.000071 | -0.000051 | 0.174966 |
| `d01_structure_flow_v1` | 168 | `proxy_edge_safe_candidate` | 0.581921 | 0.476979 | 0.896177 | 0.523021 | 0.103823 | 10.862763 | 56.583852 | 0.771249 | 0.000590 | -0.000672 | 0.482890 |
| `topology_locked_visual_chroma_full_flow_v1` | 168 | `proxy_negative_or_risky` | 0.551020 | 0.434348 | 0.896224 | 0.565652 | 0.103776 | 10.883136 | 55.607880 | 2.079218 | -0.030310 | 0.041960 | -0.493082 |

## Reading

- `proxy_positive_candidate`: the image-gradient proxy improves or preserves F1 while reducing false-edge ratio and skeleton endpoints versus raw.
- `raw_equivalent_control`: the Stage1 diagnostic chain reproduced raw input for the control variant; this is a sanity check, not an enhancement gain.
- `proxy_edge_safe_candidate`: the proxy remains close to raw under small F1, false-edge, and endpoint tolerances.
- `proxy_mixed_watch`: mixed proxy behavior; do not prioritize without detector evidence.
- `proxy_negative_or_risky`: likely boundary/proxy risk before detector sampling.

## Boundary

- These rows are image-gradient-to-GT proxies, not detector predictions.
- A candidate can pass this prescreen and still fail fixed DiffusionEdge/MSFI sampling.
- A candidate cannot be claimed as downstream-improving until MyEdge sampling/eval/show, result intake, detector MAT structure proxy, and review are complete.
- Do not expand any candidate to 2770 full-pool from this prescreen alone.

## Output Files

- Summary CSV: `docs/stage1_myedge168_gt_edge_proxy_prescreen_topology_locked_visual_chroma_v1_20260527_cn.summary.csv`
- Delta CSV: `docs/stage1_myedge168_gt_edge_proxy_prescreen_topology_locked_visual_chroma_v1_20260527_cn.delta_vs_raw.csv`
- Per-image CSV: `docs/stage1_myedge168_gt_edge_proxy_prescreen_topology_locked_visual_chroma_v1_20260527_cn.per_image.csv`
- JSON: `docs/stage1_myedge168_gt_edge_proxy_prescreen_topology_locked_visual_chroma_v1_20260527_cn.json`
