# 完整增强图像池人工复核协议

更新时间：2026-05-25

本文档定义 `full_algae_dewatermark_v1` 的人工复核流程。它只服务于完整图像池数据质量收口，不替代当前正式 `full502_clean_v1` / `compare9_complete496_v1` 论文结果口径。

## 1. 当前复核入口

人工复核表目录：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/`

入口摘要：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_index.md`

统一复核表：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/all_manual_review_issues.tsv`

当前校验报告：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_validation_status_20260525.md`

P0 复核辅助包：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_review_pack_summary.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_review_recommendations.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_contact_sheet.png`

P1 复核辅助包：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_review_pack_summary.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_review_recommendations.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_near_duplicate_contact_sheet.png`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_quality_contact_sheet_001.png`

P2 复核辅助包：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_review_pack_summary.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_review_recommendations.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_near_duplicate_contact_sheet.png`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_quality_contact_sheet_001.png`

统一复核 dashboard：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_dashboard_20260525.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/all_priority_review_queue.tsv`

人工决策填写模板：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_template.tsv`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_template_20260525.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_apply_report_20260525.md`

人工复核派生状态：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/derived_review_artifacts/review_artifacts_status_20260525.md`

当前状态：

- `overall_status = pending_manual_review`
- 总复核行数：`544`
- pending：`544`
- reviewed：`0`
- needs_followup：`0`
- invalid：`0`
- P0 复核辅助包状态：`recommendations_only_pending_manual_review`
- P1 复核辅助包状态：`recommendations_only_pending_manual_review`
- P2 复核辅助包状态：`recommendations_only_pending_manual_review`
- 统一复核队列状态：`ready_pending_manual_review`
- 人工决策模板状态：`ready_for_human_fill`
- 当前 dry-run 回写状态：`no_decisions_to_apply`
- 派生清单状态：`pending_manual_review`，当前未生成 clean manifest

注意：P0/P1/P2 复核辅助包、统一复核队列和决策模板中的 `machine_suggestion` 不是人工 `reviewer_decision`，只能作为填写 review sheets 前的辅助参考。

## 2. 复核范围

| 类型 | 行数 | 优先级 | 复核目的 |
| --- | ---: | --- | --- |
| `decode_failure` | 4 | P0 | 判断 4 个 `GIF89a` 内容文件是转换、排除还是保留为外部资产 |
| `exact_duplicate_group` | 3 | P0 | 判断严格重复组是否保留、去重或仅做划分防泄漏 |
| `near_duplicate_pair` | 30 | P1/P2 | 判断近重复候选是否重复，至少为训练/测试划分提供 leakage guard |
| `quality_outlier` | 507 | P1/P2 | 判断质量异常候选是有效退化样本、失败案例候选、子集标签还是清洗排除候选 |

当前 P0 行数为 `7`：4 个 decode failures + 3 个 exact duplicate groups。

## 3. 字段填写规则

每一行都必须保留原始 `issue_id`。人工决策只能填写以下字段：

- `review_status`
- `reviewer_decision`
- `decision_reason`
- `reviewer`
- `review_date`

字段要求：

- `review_status` 可取 `pending`、`reviewed`、`needs_followup`。
- `pending` 行不得填写 decision 字段。
- `reviewed` 或 `needs_followup` 行必须填写 `reviewer_decision`、`decision_reason`、`reviewer`、`review_date`。
- `review_date` 使用 `YYYY-MM-DD`。
- `reviewer_decision` 必须来自该行 `allowed_decisions`。

## 4. 推荐复核顺序

1. 先处理 P0：
   - `decode_failures_review.tsv`
   - `exact_duplicates_review.tsv`
   - 可先查看 `p0_review_pack/p0_review_recommendations.tsv` 和 `p0_review_pack/p0_contact_sheet.png`，但最终决策必须写回对应 review sheets。
   - 也可从 `all_priority_review_queue.tsv` 中按 `review_order` 顺序处理，`target_review_sheet` 指明写回位置。
   - 如果使用 `manual_review_decision_template.tsv`，只填写 `*_to_apply` 字段，先 dry-run，再显式 `--apply`。
2. 再处理 P1：
   - `near_duplicates_review.tsv` 中 `phash_distance=0` 且 `dhash_distance=0` 的候选
   - `quality_outliers_review.tsv` 中低清晰度、低边缘能量、低对比候选
   - 可先查看 `p1_review_pack/p1_review_recommendations.tsv`、`p1_near_duplicate_contact_sheet.png` 和 `p1_quality_contact_sheet_*.png`，但最终决策必须写回对应 review sheets。
3. 最后处理 P2：
   - 其他近重复和质量异常候选
   - 可先查看 `p2_review_pack/p2_review_recommendations.tsv`、`p2_near_duplicate_contact_sheet.png` 和 `p2_quality_contact_sheet_*.png`，但最终决策必须写回对应 review sheets。
   - P2 质量异常优先作为数据覆盖、退化分层、失败案例或有效难例候选确认，不应自动排除。
   - P2 近重复优先记录为 future split leakage guard 候选，不应自动删除。

## 5. 决策边界

- 复核表不是清洗结果。
- 不能因为某行出现在复核表中就自动删除或排除。
- 严格重复和近重复至少应在 MyEdge 训练/测试划分中作为 leakage guard。
- 质量异常样本可能是有效退化样本，不应直接按低质量删除。
- P1 质量异常候选优先标注为退化子集、失败案例候选或有效难例；除非人工理由明确，否则不要直接排除。
- P2 质量异常候选优先标注为数据覆盖、退化分层、失败案例候选或有效难例；除非人工理由明确，否则不要直接排除。
- 只有校验状态达到 `complete_validated` 或按协议接受 `review_ready_with_followups` 后，才能派生新的 full-pool clean manifest 或 split guard 文件。

## 6. 校验命令

```bat
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\validate_fullpool_manual_review.py
```

校验脚本：

- `metrics/scripts/validate_fullpool_manual_review.py`

输出：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_validation_status_20260525.json`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_validation_status_20260525.md`
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_invalid_rows_20260525.tsv`

当前校验结论是 `pending_manual_review`，表示还不能生成清洗 manifest、转换清单、排除清单或 split leakage guard。

## 6.1 决策模板 dry-run 与回写

如果采用统一模板填写人工决策，先生成模板：

```bat
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\build_fullpool_manual_review_decision_template.py
```

填写 `manual_review_decision_template.tsv` 后，先 dry-run：

```bat
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\apply_fullpool_manual_review_decisions.py
```

只有 dry-run 报告显示 `invalid_decision_rows=0` 且 `status=dry_run_valid` 时，才允许显式写回：

```bat
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\apply_fullpool_manual_review_decisions.py --apply
```

写回后必须重新运行 `validate_fullpool_manual_review.py`；只有校验通过后，才能运行派生脚本。

## 7. 派生清单命令

只有人工复核字段填写完成并通过校验后，才允许派生转换、排除、去重和 split guard 清单：

```bat
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\derive_fullpool_review_artifacts.py
```

派生脚本：

- `metrics/scripts/derive_fullpool_review_artifacts.py`

输出目录：

- `metrics/manifests/full_algae_dewatermark_v1_manual_review/derived_review_artifacts/`

当前输出：

- `review_artifacts_status_20260525.md`
- `review_artifacts_status_20260525.json`
- `conversion_candidates.tsv`
- `exclusion_candidates.tsv`
- `deduplicate_drop_candidates.tsv`
- `split_leakage_guard_candidates.tsv`
- `subset_label_candidates.tsv`
- `invalid_rows.tsv`

当前状态仍为 `pending_manual_review`，所以这些派生表为空或仅包含表头，`reviewed_cv2_clean_manifest.txt` 未生成。只有 `overall_status=complete_validated` 且 `can_generate_clean_manifest=True` 时，才可把派生 manifest 作为后续 full-pool run 入口。
