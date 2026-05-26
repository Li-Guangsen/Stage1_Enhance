# Stage1-MyEdge Provenance P0/P1 复核辅助包

生成时间：`2026-05-25T02:40:52`

状态：`review_aid_ready_pending_manual_decision`

本辅助包为 provenance P0/P1 优先队列生成 source/candidate 并排 contact sheets，只服务于人工复核。它不填写 `reviewer_decision`，不推断同源关系，不运行 Stage1，不运行 MyEdge，不生成指标。

## 计数

- P0/P1 review rows：`208`
- contact sheets：`54`
- reviewer_decision filled：`0`
- reviewer_decision pending：`208`

## Priority Counts

| Item | Count |
|---|---:|
| P0 | 126 |
| P1 | 82 |

## Relation Scope Counts

| Item | Count |
|---|---:|
| myedge_raw_to_fullpool_visual_candidate | 8 |
| myedge_raw_to_stage1_original_same_filename | 160 |
| stage1_original_to_fullpool_visual_candidate | 40 |

## Candidate Band Counts

| Item | Count |
|---|---:|
| exact_or_reencoded_visual_candidate | 11 |
| possible_visual_candidate | 37 |
| strong_visual_candidate | 160 |

## 输出

- contact sheets 目录：`D:\Desktop\Stage1Codex\metrics\manifests\stage1_myedge_provenance_review\p0_p1_review_pack\contact_sheets`
- pack index：`D:\Desktop\Stage1Codex\metrics\manifests\stage1_myedge_provenance_review\p0_p1_review_pack\provenance_p0_p1_review_pack_index.tsv`

## 边界

- contact sheet 是人工复核辅助，不是论文图。
- `machine_suggestion` 和视觉指标不能作为人工结论。
- 只有人工填写并通过 provenance 校验/派生后，才能更新数据来源说明。
