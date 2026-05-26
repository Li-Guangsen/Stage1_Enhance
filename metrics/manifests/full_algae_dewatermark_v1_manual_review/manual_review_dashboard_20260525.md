# full_algae_dewatermark_v1 manual review dashboard

日期：2026-05-25

本文是完整增强图像池人工复核的统一入口。它只整合 P0/P1/P2 复核辅助包和校验状态，不填写人工决策，不修改 manifest，不运行增强。

## Current Status

- Overall review status: `pending_manual_review`
- Total review rows: `544`
- Pending rows: `544`
- Reviewed rows: `0`
- Invalid rows: `0`
- Derived clean manifest allowed: `False`
- Unified queue status: `ready_pending_manual_review`

## Outputs

- unified review queue: `metrics\manifests\full_algae_dewatermark_v1_manual_review\all_priority_review_queue.tsv`
- dashboard json: `metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_dashboard_20260525.json`
- review sheet: `metrics\manifests\full_algae_dewatermark_v1_manual_review\all_manual_review_issues.tsv`
- validation status: `metrics\manifests\full_algae_dewatermark_v1_manual_review\manual_review_validation_status_20260525.md`
- derived status: `metrics\manifests\full_algae_dewatermark_v1_manual_review\derived_review_artifacts\review_artifacts_status_20260525.md`

### Priority Counts

| Key | Count |
| --- | ---: |
| `P0` | 7 |
| `P1` | 134 |
| `P2` | 403 |

### Issue Type Counts

| Key | Count |
| --- | ---: |
| `decode_failure` | 4 |
| `exact_duplicate_group` | 3 |
| `near_duplicate_pair` | 30 |
| `quality_outlier` | 507 |

### Machine Suggestion Counts

| Key | Count |
| --- | ---: |
| `deduplicate_for_clean_pool` | 2 |
| `exclude_from_opencv_fullpool` | 4 |
| `keep_but_split_guard` | 11 |
| `mark_duplicate` | 2 |
| `needs_manual_visual_check` | 18 |
| `subset_label_only` | 507 |

## Recommended Review Order

1. 先处理 P0：4 个 decode failures 和 3 个 exact duplicate groups。
2. 再处理 P1：近重复强候选和低清晰度、低边缘能量、低对比等关键质量异常。
3. 最后处理 P2：其余近重复和质量异常候选。
4. 每一行的最终人工决策必须写回 `target_review_sheet` 对应 TSV 的 `review_status`、`reviewer_decision`、`decision_reason`、`reviewer` 和 `review_date`。

## Decision Template Workflow

如果不想直接编辑 4 个 review sheets，可先生成并填写统一决策模板：

```bat
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\build_fullpool_manual_review_decision_template.py
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\apply_fullpool_manual_review_decisions.py
```

第二条命令默认 dry-run，只生成 apply plan，不写回 review sheets。只有 dry-run 无 invalid 后，才允许显式传 `--apply`。

## Commands After Manual Review

```bat
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\validate_fullpool_manual_review.py
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\derive_fullpool_review_artifacts.py
```

只有 `overall_status=complete_validated` 且 `can_generate_clean_manifest=True` 时，才能把派生 clean manifest 或 split leakage guard 作为后续 full-pool 协议入口。

## Boundary

- `machine_suggestion` 只是复核建议，不是 `reviewer_decision`。
- P0/P1/P2 复核包和本 dashboard 不会删除、转换或排除任何原图。
- P1/P2 质量异常优先作为退化分层、失败案例、数据覆盖或有效难例候选，不是自动排除依据。
- P1/P2 近重复优先作为 future split leakage guard 候选，不是自动删除依据。
- 当前仍不能启动或声明 2770 张 full-pool 正式增强完成；full run 需要单独批准并通过接收脚本。
