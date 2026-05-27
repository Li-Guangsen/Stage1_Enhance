# FA01 per-image correlation audit

日期：2026-05-27

## 1. 状态

- status: `complete_readonly_correlation_audit`
- 范围：P27、D01、FF01、FF02；MyEdge 168 split；fixed MSFI 50k 与 fixed DiffusionEdge baseline 50k。
- 输入：`docs/evidence/fa01_family_audit/fa01_stage1_full_flow_family_audit_tables_20260527/fa01_enhancement_proxy_168_per_image.csv` 与 MyEdge structure-proxy per-image CSV。
- 边界：本审计只计算 per-image proxy 相关；不重算 ODS/OIS/AP/AC，不运行 sampling/eval/show，不训练，不生成新候选。

## 2. 产物

- 合并明细：`docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527/fa01_per_image_enhancement_structure_merged.csv`
- 全量相关：`docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527/fa01_per_image_correlations.csv`
- Top correlations：`docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527/fa01_top_correlations.csv`
- Top adverse cases：`docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527/fa01_top_adverse_per_image_cases.csv`
- Variant summary：`docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527/fa01_per_image_correlation_variant_summary.csv`
- JSON index：`docs/evidence/fa01_family_audit/fa01_per_image_correlation_audit_20260527/fa01_per_image_correlation_index.json`

## 3. Variant-level proxy summary

| Variant | Detector | BGR delta | Chroma delta | Grad ratio | dF1 | dFalse-edge | dEndpoints/kpx |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P27 | MSFI | 2.1238 | 0.8445 | 1.2599 | +0.000577 | -0.013685 | -1.160557 |
| P27 | DiffusionEdge | 2.1238 | 0.8445 | 1.2599 | -0.000099 | +0.003972 | -0.176182 |
| D01 | MSFI | 2.7677 | 1.2302 | 1.2931 | +0.000343 | -0.013767 | -1.140514 |
| D01 | DiffusionEdge | 2.7677 | 1.2302 | 1.2931 | -0.000327 | +0.005265 | +0.353641 |
| FF01 | MSFI | 8.6772 | 5.8024 | 1.0646 | -0.053426 | +0.079593 | +1.891529 |
| FF01 | DiffusionEdge | 8.6772 | 5.8024 | 1.0646 | -0.067472 | +0.095084 | +4.291561 |
| FF02 | MSFI | 11.7138 | 7.9785 | 0.9450 | -0.050686 | +0.073386 | +2.062959 |
| FF02 | DiffusionEdge | 11.7138 | 7.9785 | 0.9450 | -0.066633 | +0.089035 | +3.758488 |

## 4. Correlation findings

最强相关主要集中在 `delta_pred_edge_density`，不是直接集中在 dF1 或 dFalse-edge：

- P27/D01 在 MSFI 上，`grad_mean_ratio` 与 `delta_pred_edge_density` 的 Spearman 约 `0.55`。
- P27/D01 在 MSFI 上，`mean_abs_luma_delta` 与 `delta_pred_edge_density` 的 Spearman 约 `-0.51` 到 `-0.55`。
- FF01 在 DiffusionEdge 上，`mean_abs_luma_delta` 与 `delta_endpoints` 的 Pearson 约 `0.46`。
- FF01/FF02 的 false-edge / F1 损伤与单一增强 proxy 的相关并不稳定，说明不能用一个简单阈值解释或修复 full-flow failure。

解释：

- `grad ratio` 对 near-raw family 的 pred-edge density 有一定解释力，但对 FF01/FF02 的 main failure 不够。
- FF02 平均 `grad ratio < 1` 仍然掉 ODS/AP，进一步支持“失败不只是全局梯度放大”。
- 色度/低频变化、局部 topology drift、背景纹理响应、detector raw-distribution bias 需要联合解释。

## 5. Adverse-case findings

FF01/FF02 的 false-edge 最差样本形成了新的风险簇：

- `weixiaoyuanjia.26`：FF01/FF02 在两个 detector 上都是 false-edge adverse top case。
- `xuehong.9`、`xuehong.13`、`xuehong.11`：FF01/FF02 repeated adverse cluster。
- `donghaiyuanjia.26`：FF01/FF02 repeated adverse cluster。
- `weixiaoyuanjia.21`：FF01 DiffusionEdge false-edge rank 1，且 FF01/FF02 状态文档均点名。

这说明 high-risk 审计不能只看 `tama.*` 高梯度样本；还必须看 high color/chroma shift 后 detector error map 的 false-edge 增加。

## 6. Hypothesis update

FA01 WP2 的假设状态：

- H1 raw-topology dominance：仍然成立，但不是唯一因素。
- H2 chroma/low-frequency shift sensitivity：证据增强。FF02 更高 chroma/BGR delta 且更差 AP/ODS，即使 mean grad ratio 更低。
- H3 background false-edge amplification：证据增强。FF01/FF02 adverse cases 出现 repeated false-edge clusters。
- H4 sidecar/adaptation route：优先级上升。Stage1 直接替换 raw 输入的 fixed-detector 路线继续不稳。
- H5 Stage1-only fixed-detector positive gain infeasible：当前证据继续支持，但还需 high-risk visual/error-map review 完成后作为停止条件。

## 7. 下一步

下一步不应创建 FF03/P29/D02，而应：

1. 用 high-risk index 打开 raw、GT、Stage1 output、white/overlay/error_map 做人工或脚本分型。
2. 对 `weixiaoyuanjia.26`、`xuehong.9/13/11`、`donghaiyuanjia.26`、`weixiaoyuanjia.21`、`tama.14` 做 panel review。
3. 起草 MyEdge/MSFI adaptation protocol：raw 主输入 + Stage1 sidecar / dual-input / weak-boundary evidence，而不是直接替换 fixed-detector raw 输入。
