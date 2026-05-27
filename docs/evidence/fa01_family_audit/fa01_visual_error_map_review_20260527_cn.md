# FA01 high-risk visual/error-map review

日期：2026-05-27

## 1. 目的

本审查只整理既有 FA01 证据：raw、GT、legacy Stage1 Final、P27、D01、FF01、FF02，以及 fixed MSFI/DiffusionEdge 的 error-map。它不是新候选、不是新实验，也不替代 168 fixed-detector gate。

## 2. 结论

- high-risk 样本的共同问题不是单一颜色偏移，而是 detector error-map 中的边界损失、背景 false-edge、骨架端点碎片化和 luma/detail topology drift 的组合。

- FF01/FF02 的完整增强骨架在视觉/色度上比 P27/D01 更明显，但现有 fixed raw-trained detector 对这种输入分布并不稳定；继续 FF03 式同族小修没有足够证据价值。

- 下一步应把 Stage1 输出拆成 sidecar evidence maps 或进入独立 MyEdge/MSFI adaptation protocol，而不是继续把增强图直接替换 raw 作为 fixed-detector 输入。

## 3. 审查样本与模式标签

| stem | pattern tags | worst dF1 | max dFalse | max dEndpoints | max BGR | max chroma | panel |
|---|---:|---:|---:|---:|---:|---:|---|
| weixiaoyuanjia.26 | boundary_f1_loss;false_edge_increase;endpoint_fragmentation;luma_detail_topology_drift;large_color_chroma_shift | -0.445499 | 0.607127 | 29.411765 | 30.956152 | 15.435522 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/weixiaoyuanjia.26_fa01_visual_error_map_panel.jpg) |
| xuehong.9 | boundary_f1_loss;false_edge_increase;endpoint_fragmentation | -0.318209 | 0.589210 | 23.483366 | 7.088324 | 3.905811 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/xuehong.9_fa01_visual_error_map_panel.jpg) |
| xuehong.13 | boundary_f1_loss;false_edge_increase;endpoint_fragmentation | -0.367885 | 0.572903 | 4.726463 | 7.098565 | 3.912910 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/xuehong.13_fa01_visual_error_map_panel.jpg) |
| xuehong.11 | boundary_f1_loss;false_edge_increase;endpoint_fragmentation | -0.343801 | 0.551388 | 24.399804 | 7.085648 | 3.905259 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/xuehong.11_fa01_visual_error_map_panel.jpg) |
| donghaiyuanjia.26 | boundary_f1_loss;false_edge_increase;endpoint_fragmentation;large_color_chroma_shift | -0.389637 | 0.550916 | 14.285714 | 29.263998 | 14.354980 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/donghaiyuanjia.26_fa01_visual_error_map_panel.jpg) |
| weixiaoyuanjia.21 | boundary_f1_loss;false_edge_increase;endpoint_fragmentation;luma_detail_topology_drift;large_color_chroma_shift | -0.443258 | 0.583796 | 73.298429 | 29.757481 | 15.207690 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/weixiaoyuanjia.21_fa01_visual_error_map_panel.jpg) |
| tama.14 | endpoint_fragmentation;luma_detail_topology_drift | -0.011905 | 0.023529 | 12.345679 | 6.249840 | 3.424649 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/tama.14_fa01_visual_error_map_panel.jpg) |
| tama.11 | luma_detail_topology_drift | -0.014149 | 0.027540 | 0.000000 | 6.279372 | 3.434350 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/tama.11_fa01_visual_error_map_panel.jpg) |
| tama.9 | luma_detail_topology_drift | -0.017405 | 0.033986 | 0.000000 | 6.252282 | 3.407031 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/tama.9_fa01_visual_error_map_panel.jpg) |
| jianci.4 | boundary_f1_loss;false_edge_increase;endpoint_fragmentation;luma_detail_topology_drift;large_color_chroma_shift | -0.155261 | 0.214693 | 11.992125 | 14.213421 | 13.942305 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/jianci.4_fa01_visual_error_map_panel.jpg) |
| donghaiyuanjia.18 | boundary_f1_loss;false_edge_increase;endpoint_fragmentation;luma_detail_topology_drift;large_color_chroma_shift | -0.282283 | 0.435188 | 11.538462 | 27.765541 | 11.531992 | [panel](docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527/panels/donghaiyuanjia.18_fa01_visual_error_map_panel.jpg) |

## 4. 文件索引

- `fa01_visual_error_map_panels.csv`：每个 panel 的相对路径和选样原因。
- `fa01_visual_error_map_pattern_tags.csv`：基于 per-image proxy 的失败模式标签。
- `fa01_visual_error_map_review_index.json`：生成参数、输入文件和输出统计。

## 5. 后续约束

该审查支持 FA01 的决策：先停止 same-family full-flow patching，优先定义 Stage1 sidecar maps 和 no-training export smoke；若要证明 downstream 正收益，必须另立适配协议或新方法族，并保持 fixed-detector 结果与 adaptation 结果分账。
