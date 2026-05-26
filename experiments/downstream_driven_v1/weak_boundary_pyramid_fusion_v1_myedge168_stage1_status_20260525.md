# weak_boundary_pyramid_fusion_v1 MyEdge168 Stage1 状态

日期：2026-05-25

## 状态

- 总状态：`candidate_rescues_legacy_but_not_near_raw`
- 候选编号：P14
- 配置：`experiments/downstream_driven_v1/configs/weak_boundary_pyramid_fusion_v1.json`
- Final mode：`weak_boundary_pyramid_fusion_bph`
- 角色：P12/P13 之后的非正式 downstream-driven 弱边界局部融合候选。

## Stage1 输出

| 范围 | 输出根 | Final PNG | Final JPG | 解码失败 |
| --- | --- | ---: | ---: | ---: |
| 2 张 smoke | `experiments/downstream_driven_v1/outputs/smoke_myedge168/weak_boundary_pyramid_fusion_v1` | 2 | 2 | 0 |
| MyEdge 168 split | `experiments/downstream_driven_v1/outputs/myedge168/weak_boundary_pyramid_fusion_v1` | 168 | 168 | 0 |
| `full502_clean_v1` | `experiments/downstream_driven_v1/outputs/full502/weak_boundary_pyramid_fusion_v1` | 502 | 502 | 0 |

## MyEdge fixed-detector 结果

结果入口：

- `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\weak_boundary_pyramid_fusion_p14_results_20260525.md`
- `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\weak_boundary_pyramid_fusion_p14_structure_metrics_20260525.md`
- `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\weak_boundary_pyramid_fusion_p14_downstream_gate_20260525.md`

| Detector | ODS | OIS | AP | AC |
| --- | ---: | ---: | ---: | ---: |
| MSFI raw anchor | 0.783527 | 0.794213 | 0.345899 | 0.796846 |
| MSFI P14 | 0.784373 | 0.795164 | 0.346405 | 0.7940 |
| DiffusionEdge baseline raw anchor | 0.770521 | 0.779986 | 0.363065 | 0.7969 |
| DiffusionEdge baseline P14 | 0.773454 | 0.784037 | 0.372930 | 0.7935 |

结构 proxy vs raw：

- MSFI P14：dF1 `+0.0017`、dFalse-edge `-0.0151`、dEndpoints/kpx `-1.4952`。
- DiffusionEdge baseline P14：dF1 `+0.0013`、dFalse-edge `+0.0034`、dEndpoints/kpx `-0.1187`。

Gate：

- `candidate_rescues_legacy_but_not_near_raw`
- MSFI 侧 `near raw` 且 structure non-worse。
- DiffusionEdge baseline 侧能救回 legacy Final 损伤，但 AC 低于 raw，false-edge ratio 略高于 raw，因此不是强通过。

## 502/496 增强指标

| Protocol | Count | EME | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P14 / `full502_clean_v1` | 502 | 2.6005 | 26.9240 | 2.7764 | 0.9981 | 47.6219 | 2.2432 | 7.3917 |
| P14 / `compare9_complete496_v1` | 496 | 2.4955 | 25.5663 | 2.7122 | 0.9981 | 47.6324 | 2.2674 | 7.2119 |

## 边界

- P14 是非正式候选，不替代 `experiments/optimization_v1/configs/locked_full506_final_mainline.json` 和正式结果目录。
- P14 能救回旧 `Final` 在 fixed detector 下的大幅损伤，但不是强通过，也不能写成 Stage1 稳定提升下游边缘检测。
- P14 的增强指标比 P13 更保守，远弱于 FormalFinal 的 EME、Contrast、AvgGra、UCIQE 和 UIQM。
- `MS_SSIM` 和 `PSNR` 仍只能解释为相对原图的结构一致性，不是增强真值质量。
- 不进入 2770 full-pool。
