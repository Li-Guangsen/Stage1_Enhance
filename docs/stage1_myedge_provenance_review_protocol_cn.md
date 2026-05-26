# Stage1 / MyEdge / full-pool provenance 人工复核协议

更新时间：2026-05-25

本协议用于确认 `Stage1Codex`、`MyEdgeCodex` 和完整去水印藻类图像池之间的真实数据来源关系。它只处理 provenance，不处理增强指标、边缘检测指标、训练、采样或图表生成。

## 1. 背景

当前已经有两层只读审计：

- 文件级审计：`docs/stage1_myedge_file_relation_audit_20260525_cn.md`
- 视觉关系审计：`docs/stage1_myedge_visual_relation_audit_20260525_cn.md`

文件级审计说明：MyEdge 168 与 Stage1 formal 502 可以按 stem/path 衔接，但 MyEdge raw 与 Stage1 formal original 的 SHA256 相同数为 `0/168`，且与 `full_algae_dewatermark_v1` 的 `2774/2770` manifest 暂无文件名或 stem 直连。

视觉关系审计说明：MyEdge raw 与 Stage1 formal original 有 `123/168` 个 exact/strong 视觉候选；但 MyEdge raw 到 full-pool 只有 `8/168` 个 strong top-1 候选，Stage1 formal 502 到 full-pool 只有 `40/502` 个 exact/strong top-1 候选。

因此，当前不能把 visual hash 候选写成数据同源事实。必须经过人工 provenance 复核。

## 2. 文件入口

- 全量复核模板：`metrics/manifests/stage1_myedge_provenance_review/provenance_review_template.tsv`
- P0/P1 优先队列：`metrics/manifests/stage1_myedge_provenance_review/provenance_priority_review_queue.tsv`
- 复核入口摘要：`metrics/manifests/stage1_myedge_provenance_review/provenance_review_index_20260525.md`
- 当前校验状态：`metrics/manifests/stage1_myedge_provenance_review/provenance_review_validation_status_20260525.md`
- invalid rows：`metrics/manifests/stage1_myedge_provenance_review/provenance_review_invalid_rows_20260525.tsv`
- 模板生成脚本：`metrics/scripts/build_stage1_myedge_provenance_review_template.py`
- 校验脚本：`metrics/scripts/validate_stage1_myedge_provenance_review.py`
- 派生脚本：`metrics/scripts/derive_stage1_myedge_provenance_artifacts.py`
- 派生状态：`metrics/manifests/stage1_myedge_provenance_review/derived_provenance_artifacts/provenance_artifacts_status_20260525.md`

## 3. 当前状态

- 全量 review 行数：`1510`
- P0/P1 优先行数：`208`
- full-pool 候选行数：`1342`
- `reviewer_decision` 已填写：`0`
- pending：`1510`
- invalid：`0`
- 可作为 paper-positive 的行数：`0`
- 派生状态：`pending_manual_provenance_review`
- confirmed original-id map 行数：`0`
- split leakage guard candidate 行数：`0`

当前状态是 `pending_manual_provenance_review`。这表示已有复核入口，但尚无人工确认的 provenance 结论。

## 4. 字段说明

核心机器字段：

- `review_id`：复核行唯一编号。
- `priority`：复核优先级，P0/P1 优先。
- `relation_scope`：关系类型，例如 MyEdge raw 到 Stage1 original，或 Stage1/MyEdge 到 full-pool。
- `source_*`：待确认关系的源图像信息。
- `candidate_*`：候选匹配图像信息。
- `candidate_band`：视觉候选等级。
- `combined_hash_hamming`、`thumb_rmse_32`：候选排序辅助指标。
- `machine_suggestion`：机器建议，仅供导航。

必须人工填写的字段：

- `reviewer_decision`
- `confirmed_original_id`
- `confirmed_relation_note`
- `species_label_checked`
- `split_overlap_risk`
- `paper_use_allowed`
- `reviewer`
- `review_date`
- `review_notes`

## 5. reviewer_decision 合法值

- `confirmed_same_original`
- `confirmed_same_visual_subject_reencoded_or_cropped`
- `confirmed_related_same_species_not_same_original`
- `confirmed_different`
- `uncertain_needs_followup`

建议解释：

- `confirmed_same_original`：人工确认两者来自同一原始图像。
- `confirmed_same_visual_subject_reencoded_or_cropped`：人工确认主体一致，但可能经过重编码、裁剪、缩放或压缩。
- `confirmed_related_same_species_not_same_original`：同物种或同类形态，但不是同一原始图。
- `confirmed_different`：确认不是同一原始图，也不应作为同源证据。
- `uncertain_needs_followup`：当前证据不足，需要后续查原始编号、采集记录或人工专家确认。

## 6. 进入论文写作的门槛

只有同时满足以下条件的行，才能用于论文数据来源描述：

1. `reviewer_decision` 已填写合法值。
2. `reviewer` 和 `review_date` 已填写。
3. 若 decision 为 `confirmed_same_original` 或 `confirmed_same_visual_subject_reencoded_or_cropped`，必须填写 `confirmed_original_id`。
4. `paper_use_allowed` 为 `yes` 或 `only_with_boundary`。
5. 运行 `metrics/scripts/validate_stage1_myedge_provenance_review.py` 后 invalid 为 `0`。
6. 运行 `metrics/scripts/derive_stage1_myedge_provenance_artifacts.py` 后 `can_generate_final_provenance=true`。

即使满足这些条件，也只能证明本模板中的 provenance 关系；不能自动证明 Stage1 提升 ODS/OIS/AP/AC，也不能自动证明与两篇参考论文的 split、GT 或标注协议完全一致。

## 7. 建议复核顺序

1. 先处理 `provenance_priority_review_queue.tsv` 中的 P0/P1 行。
2. 先确认 MyEdge raw 与 Stage1 original 是否可写为同一视觉样本或同一原图的重编码版本。
3. 再确认 MyEdge/Stage1 与 full-pool 的 strong 候选是否是真实 original-id 对应。
4. 对 `confirmed_same_original` 或 `confirmed_same_visual_subject_reencoded_or_cropped` 的行，统一分配可追踪的 `confirmed_original_id`。
5. 对涉及 train/test 或论文 split 的行，填写 `split_overlap_risk`。
6. 校验通过后，再同步更新 `research-state.yaml`、主张证据总账和论文数据说明。
7. 通过派生脚本生成 `confirmed_original_id_map.tsv`、`paper_usable_provenance_relations.tsv` 和 `split_leakage_guard_candidates.tsv`。

## 8. 禁止事项

- 不能把 `machine_suggestion` 当作人工结论。
- 不能把 visual hash 候选写成同一原图事实。
- 不能在 pending 行上写论文数据来源结论。
- 不能用 provenance 复核替代 MyEdge 带 GT 下游评测。
- 不能用本协议替代 full-pool 人工 clean manifest。
