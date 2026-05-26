# Stage1-MyEdge provenance 派生 artifacts 状态

生成时间：`2026-05-25T02:31:01`

状态：`pending_manual_provenance_review`

本报告由人工 provenance review 模板派生。当前脚本只读取复核表，不推断人工结论，不运行 Stage1，不运行 MyEdge，不生成指标或图表。

## 计数

- 总行数：`1510`
- pending：`1510`
- reviewed：`0`
- invalid：`0`
- positive relations：`0`
- paper-usable relations：`0`
- confirmed original IDs：`0`
- split leakage guard candidates：`0`
- can generate final provenance：`False`

## 输出

- confirmed positive relations：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/derived_provenance_artifacts/confirmed_positive_relations.tsv`
- paper-usable relations：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/derived_provenance_artifacts/paper_usable_provenance_relations.tsv`
- negative/uncertain relations：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/derived_provenance_artifacts/reviewed_negative_or_uncertain_relations.tsv`
- confirmed original-id map：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/derived_provenance_artifacts/confirmed_original_id_map.tsv`
- split leakage guard candidates：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/derived_provenance_artifacts/split_leakage_guard_candidates.tsv`
- invalid rows：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/derived_provenance_artifacts/provenance_artifacts_invalid_rows_20260525.tsv`

## 边界

- 当前如果仍有 pending 或 invalid，不能把任何派生表写成最终 provenance 结论。
- 即使 future 状态达到 `final_provenance_artifacts_ready`，它也只证明人工复核的 source relation；不能替代 MyEdge 带 GT 下游评测、Stage1 full2770 增强结果或参考论文 split/GT 证明。
