# Stage1-MyEdge Provenance 复核校验状态

生成时间：`2026-05-25T02:26:48`

状态：`pending_manual_provenance_review`

本校验只检查人工 provenance review 模板字段是否合法，不推断结论，不生成 clean manifest，不改变任何实验结果。

## 计数

- 总行数：`1510`
- pending 行数：`1510`
- reviewed 行数：`0`
- invalid 行数：`0`
- 可作为 paper-positive 的行数：`0`
- invalid rows：`D:/Desktop/Stage1Codex/metrics/manifests/stage1_myedge_provenance_review/provenance_review_invalid_rows_20260525.tsv`

## Decision Counts

| Item | Count |
|---|---:|
| (blank) | 1510 |

## Paper Use Counts

| Item | Count |
|---|---:|
| (blank) | 1510 |

## 边界

- pending 行不能用于 provenance 论文结论。
- invalid 行必须修正后才能使用。
- 即使校验通过，`paper_use_allowed=yes` 也只证明人工确认了本模板中的 provenance 关系，不自动证明 Stage1 下游收益或参考论文 overlap。
