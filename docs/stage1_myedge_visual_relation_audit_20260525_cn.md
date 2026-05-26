# Stage1-MyEdge-fullpool 视觉关系审计（只读）

生成时间：`2026-05-25T02:23:56`

状态：`visual_candidates_only_not_proven_provenance`

本审计用 PIL 读取本地图片，计算 aHash、dHash 和 32x32 灰度缩略图 RMSE，用来辅助判断 MyEdge 168、Stage1 formal originals 与完整去水印图像池之间是否存在视觉级候选关系。它不运行 Stage1，不运行 MyEdge，不生成边缘检测指标，不生成新图表。

## 输入路径

| Role | Path |
|---|---|
| Stage1 root | `D:\Desktop\Stage1Codex` |
| MyEdge root | `D:\Desktop\MyEdgeCodex` |
| Full algae pool root | `D:\Desktop\去水印所有藻类图像` |
| Coupling manifest | `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\stage1_myedge_168_coupling_manifest_20260524.csv` |
| full502 manifest | `D:\Desktop\Stage1Codex\metrics\manifests\full502_clean_v1.txt` |
| compare496 manifest | `D:\Desktop\Stage1Codex\metrics\manifests\compare9_complete496_v1.txt` |
| fullpool manifest | `D:\Desktop\Stage1Codex\metrics\manifests\full_algae_dewatermark_v1.txt` |
| fullpool cv2-readable manifest | `D:\Desktop\Stage1Codex\metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt` |
| candidate TSV | `D:\Desktop\Stage1Codex\metrics\manifests\stage1_myedge_visual_relation_candidates_20260525.tsv` |

## 判定口径

- exact/reencoded candidate：combined aHash+dHash hamming == 0 and 32x32 RMSE <= 1.0
- strong candidate：combined aHash+dHash hamming <= 8 and 32x32 RMSE <= 12.0
- possible candidate：combined aHash+dHash hamming <= 16 and 32x32 RMSE <= 24.0
- 边界：Perceptual-hash candidates are review aids only; they do not prove provenance, identical source images, GT identity, or split overlap.

## 核心计数

| Item | Count |
|---|---:|
| myedge_rows | 168 |
| myedge_read_ok | 168 |
| stage1_for_myedge_read_ok | 168 |
| stage1_full502_rows | 502 |
| stage1_full502_read_ok | 502 |
| compare496_rows | 496 |
| fullpool_2774_rows | 2774 |
| fullpool_2774_read_ok_by_pil | 2774 |
| fullpool_cv2_2770_rows | 2770 |
| fullpool_cv2_2770_ids_seen | 2770 |
| myedge_vs_stage1_exact_or_reencoded | 8 |
| myedge_vs_stage1_strong_or_exact | 123 |
| myedge_vs_fullpool_top1_exact_or_reencoded | 0 |
| myedge_vs_fullpool_top1_strong_or_exact | 8 |
| stage1_full502_vs_fullpool_top1_exact_or_reencoded | 3 |
| stage1_full502_vs_fullpool_top1_strong_or_exact | 40 |

## 候选等级分布

| Comparison | Band | Count |
|---|---|---:|
| myedge_vs_stage1 | exact_or_reencoded_visual_candidate | 8 |
| myedge_vs_stage1 | possible_visual_candidate | 37 |
| myedge_vs_stage1 | strong_visual_candidate | 115 |
| myedge_vs_stage1 | weak_or_no_visual_candidate | 8 |
| myedge_vs_fullpool_top1 | possible_visual_candidate | 5 |
| myedge_vs_fullpool_top1 | strong_visual_candidate | 8 |
| myedge_vs_fullpool_top1 | weak_or_no_visual_candidate | 155 |
| stage1_full502_vs_fullpool_top1 | exact_or_reencoded_visual_candidate | 3 |
| stage1_full502_vs_fullpool_top1 | possible_visual_candidate | 18 |
| stage1_full502_vs_fullpool_top1 | strong_visual_candidate | 37 |
| stage1_full502_vs_fullpool_top1 | weak_or_no_visual_candidate | 444 |

## 强候选样例：MyEdge raw -> fullpool

| source_id | rank | candidate | combined | rmse32 | band |
|---|---:|---|---:|---:|---|
| haiyangyuanjia.6 | 1 | 14、Prorocentrum micans-海洋原甲藻/Prorocentrum_10_600x500_micans_nies.go.jp0296L.jpg | 0 | 2.7045 | strong_visual_candidate |
| jianci.6 | 1 | 25、Pseudo-nitzschia pungens-尖刺拟菱形藻/尖刺拟菱形藻1_cleanup.png | 8 | 0.8604 | strong_visual_candidate |
| jiaomaozao.13 | 1 | 19、Chaetoceros curvisetus-旋链角毛藻/RE7dCN88oVHk_cleanup.jpg | 2 | 2.9863 | strong_visual_candidate |
| jiaomaozao.17 | 1 | 23-3、Chaetoceros didymus-双突角毛藻-新补充-细胞两段有凸起点/URr54Fvvm2dc_cleanup.jpg | 3 | 1.2339 | strong_visual_candidate |
| jiaomaozao.29 | 1 | 23-4、Chaetoceros peruvianus-秘鲁角毛藻 -新补充/AQcysKHBV8gY_cleanup.jpg | 6 | 0.7979 | strong_visual_candidate |
| mishikailun.8 | 1 | 11、Karenia mikimotoi-米氏凯伦藻/Karenia-mikimotoi.jpg | 5 | 7.4671 | strong_visual_candidate |
| yuanjiazao.6 | 1 | 13、Prorocentrum lima-利玛原甲藻/V8hw8CyaruRB_cleanup.jpg | 4 | 0.75 | strong_visual_candidate |
| yuanjiazao.8 | 1 | 17、Prorocentrum triestinum-三角棘原甲藻/xAWGXHyNXGoS_cleanup.jpg | 8 | 1.0169 | strong_visual_candidate |

## 强候选样例：Stage1 formal original -> fullpool

| source_id | rank | candidate | combined | rmse32 | band |
|---|---:|---|---:|---:|---|
| danmai.3 | 1 | 27、Leptocylindrus danicus-丹麦细柱藻/EJqjD6FDkEUi_cleanup.jpg | 3 | 1.0982 | strong_visual_candidate |
| duolie.1 | 1 | 26、Pseudo-nitzschia multiseries-多列拟菱形藻/需要去水印-Pseudo-nitzschia-multiseries-100X_cleanup.jpg | 3 | 1.324 | strong_visual_candidate |
| duolie.11 | 1 | 26、Pseudo-nitzschia multiseries-多列拟菱形藻/需要去水印-Pseudo-nitzschia-multiseries-100X_cleanup.jpg | 3 | 1.5023 | strong_visual_candidate |
| hailianzao.11 | 1 | 34、Thalassiosira rotula-圆海链藻/XgpcgS5mPvna_cleanup.jpg | 4 | 0.8716 | strong_visual_candidate |
| hailianzao.13 | 1 | 34、Thalassiosira rotula-圆海链藻/7ew5fZds5V3r_cleanup.jpg | 7 | 0.8167 | strong_visual_candidate |
| haiyangyuanjia.6 | 1 | 14、Prorocentrum micans-海洋原甲藻/Prorocentrum_10_600x500_micans_nies.go.jp0296L.jpg | 0 | 2.7029 | strong_visual_candidate |
| jianci.6 | 1 | 25、Pseudo-nitzschia pungens-尖刺拟菱形藻/尖刺拟菱形藻1_cleanup.png | 6 | 3.725 | strong_visual_candidate |
| jiaomaozao.1 | 1 | 23-2、Chaetoceros decipiens-并基角毛藻-新补充/dExFXeY2Nnhx_cleanup.jpg | 5 | 0.8046 | strong_visual_candidate |
| jiaomaozao.11 | 1 | 23-2、Chaetoceros decipiens-并基角毛藻-新补充/Q91ko4PG9WmR_cleanup.jpg | 5 | 3.2228 | strong_visual_candidate |
| jiaomaozao.12 | 1 | 22、Chaetoceros socialis-聚生角毛藻/Rb9UUxeWRCK6_cleanup.jpg | 2 | 2.2361 | strong_visual_candidate |

## 可以写的安全表述

- MyEdge 168 and Stage1 formal originals are visually very close under perceptual hashes only if the exact/strong counts support it; this remains a candidate relation until manually reviewed.
- Full-pool visual candidate matches, if present, can guide provenance review and subset mapping, but cannot be cited as dataset identity without a manual source-id table.
- This audit is a data-provenance aid and not a downstream edge-detection result.

## 不能越界的地方

- No Stage1 enhancement, full2770 run, MyEdge staging/sampling, eval.py, show.py, training, or metric recomputation was executed.
- Visual hash equality is not byte equality and does not prove same split, same GT, same annotation, same acquisition protocol, or reference-paper overlap.
- The full-pool manual review and clean manifest remain pending.

## 下一步动作

- Use the TSV candidates to manually build an original-id/provenance table before any manuscript claim about shared data.
- If strong full-pool candidates are sparse, keep the 2777/2774/2770 full pool as an additional enhancement pool rather than claiming it contains the MyEdge 168 or reference-paper subsets.
- After provenance review, update the claim ledger and dataset description with confirmed, not inferred, relationships.
