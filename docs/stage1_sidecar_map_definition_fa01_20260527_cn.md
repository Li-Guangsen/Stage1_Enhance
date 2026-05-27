# FA01 Stage1 sidecar map definition and no-training smoke

日期：2026-05-27

## 1. 定位

本文件把 Stage1 full-flow 从“直接替换 raw 的增强图”纠偏为“raw 主输入 + Stage1 sidecar evidence maps”的可执行入口。本次只导出 maps，不训练 detector，不改 checkpoint，不跑 MyEdge eval，也不声称 downstream positive。

## 2. Sidecar Maps

| map | definition |
|---|---|
| `topology_anchor_luma` | Raw Lab-L luma; keeps raw topology as the primary edge-distribution anchor. |
| `color_compensation_magnitude` | Robust-normalized Lab ab magnitude between BPH and raw; highlights where gray-pixel/BPH color formation acts. |
| `frequency_detail_evidence` | Robust-normalized absolute luma difference between IMF1Ray and BPH; captures IMF/frequency detail evidence. |
| `contrast_visibility_evidence` | Robust-normalized max luma change from RGHS/CLAHE against BPH; captures contrast and local-visibility evidence. |
| `fusion_luma_delta_risk` | Robust-normalized absolute luma difference between Final and raw; marks where direct replacement changes raw topology. |
| `background_false_edge_risk` | Final-gradient gain in weak raw-gradient regions, weighted by Final-vs-raw luma delta; flags possible new background edges. |
| `weak_boundary_support` | Frequency detail retained outside background-risk regions; sidecar signal for weak-boundary support. |

## 3. No-training Smoke

- stage root: `experiments/full_flow_downstream_stage1_mainline_v2/outputs/myedge168/full_flow_downstream_stage1_mainline_v2/png`
- generated stems: `5` / requested `5`
- scope: sidecar export completeness only; no detector validation.

| stem | panel | metadata |
|---|---|---|
| weixiaoyuanjia.26 | [panel](docs/fa01_stage1_sidecar_map_smoke_20260527/panels/weixiaoyuanjia.26_sidecar_smoke_panel.jpg) | [metadata](docs/fa01_stage1_sidecar_map_smoke_20260527/maps/weixiaoyuanjia.26/weixiaoyuanjia.26_sidecar_metadata.json) |
| xuehong.9 | [panel](docs/fa01_stage1_sidecar_map_smoke_20260527/panels/xuehong.9_sidecar_smoke_panel.jpg) | [metadata](docs/fa01_stage1_sidecar_map_smoke_20260527/maps/xuehong.9/xuehong.9_sidecar_metadata.json) |
| donghaiyuanjia.26 | [panel](docs/fa01_stage1_sidecar_map_smoke_20260527/panels/donghaiyuanjia.26_sidecar_smoke_panel.jpg) | [metadata](docs/fa01_stage1_sidecar_map_smoke_20260527/maps/donghaiyuanjia.26/donghaiyuanjia.26_sidecar_metadata.json) |
| tama.14 | [panel](docs/fa01_stage1_sidecar_map_smoke_20260527/panels/tama.14_sidecar_smoke_panel.jpg) | [metadata](docs/fa01_stage1_sidecar_map_smoke_20260527/maps/tama.14/tama.14_sidecar_metadata.json) |
| jianci.4 | [panel](docs/fa01_stage1_sidecar_map_smoke_20260527/panels/jianci.4_sidecar_smoke_panel.jpg) | [metadata](docs/fa01_stage1_sidecar_map_smoke_20260527/maps/jianci.4/jianci.4_sidecar_metadata.json) |

## 4. Decision Boundary

sidecar route 只有在 MyEdge/MSFI 侧建立独立 adaptation run sheet、raw-only adapted baseline、训练配置和 168 eval 后，才能讨论 downstream gain。当前 smoke 只证明：Stage1 的灰像素/BPH、IMF/frequency、RGHS/CLAHE visibility、fusion risk 可以被稳定拆成可消费的 evidence/risk maps。
