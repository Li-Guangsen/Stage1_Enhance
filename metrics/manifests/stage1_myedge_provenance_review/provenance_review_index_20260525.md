# Stage1-MyEdge Provenance 人工复核入口

生成时间：`2026-05-25T02:26:00`

状态：`pending_manual_provenance_review`

本文件夹把视觉候选关系转成可人工填写的 provenance review 模板。它只服务于数据来源关系确认，不运行 Stage1，不运行 MyEdge，不生成指标，不生成图表。

## 文件

- 全量模板：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/provenance_review_template.tsv`
- 优先队列：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/provenance_priority_review_queue.tsv`

## 计数

- 全量 review 行数：`1510`
- P0/P1 优先行数：`208`
- full-pool 候选行数：`1342`
- 已填写 reviewer decision：`0`
- pending reviewer decision：`1510`

### Priority Counts

| Item | Count |
|---|---:|
| P0 | 126 |
| P1 | 82 |
| P2 | 37 |
| P3 | 599 |
| P4 | 666 |

### Relation Scope Counts

| Item | Count |
|---|---:|
| myedge_raw_to_fullpool_visual_candidate | 840 |
| myedge_raw_to_stage1_original_same_filename | 168 |
| stage1_original_to_fullpool_visual_candidate | 502 |

### Candidate Band Counts

| Item | Count |
|---|---:|
| exact_or_reencoded_visual_candidate | 11 |
| possible_visual_candidate | 66 |
| strong_visual_candidate | 160 |
| weak_or_no_visual_candidate | 1273 |

## reviewer_decision 合法值

- `confirmed_same_original`
- `confirmed_same_visual_subject_reencoded_or_cropped`
- `confirmed_related_same_species_not_same_original`
- `confirmed_different`
- `uncertain_needs_followup`

## 使用规则

- `machine_suggestion` 只是机器建议，不能当作人工结论。
- `reviewer_decision` 为空表示尚未确认 provenance。
- 只有人工填写并经过后续校验的行，才能用于论文数据来源描述、original-id 映射或 split leakage guard。
- visual hash 候选不能证明同一原图、同一 split、同一 GT、同一采集协议或参考论文数据集 overlap。
