# Stage1 实验 Registry Schema

更新时间：2026-05-27

本文件定义 `metrics/experiment_registry.csv` 和 `metrics/candidate_registry.csv` 的字段含义与最低校验规则。它不是实验结果表；它只用于约束候选生命周期和提交前审计。

## experiment_registry.csv

固定字段：

| 字段 | 含义 | 最低规则 |
| --- | --- | --- |
| `run_id` | 运行编号，例如 `P12`、`D01` | 必填，唯一 |
| `candidate_id` | 候选唯一名称 | 必填 |
| `protocol` | 协议族，例如 `downstream_driven_v1` | 必填 |
| `input_split` | 输入口径，例如 `myedge166_complete_case`；历史记录可保留 `myedge168` | 必填 |
| `config_path` | 候选配置路径 | 必填；未知写 `pending_audit` |
| `output_root` | 输出根目录 | 必填；未知写 `pending_audit` |
| `code_entry` | 代码入口或 `final.mode` | 必填；未知写 `pending_audit` |
| `commands_log` | 命令日志路径 | 未审计写 `pending_audit` |
| `runtime_sec` | 运行时间秒数 | 未审计写 `pending_audit` |
| `status` | run 状态 | 枚举或 `pending_audit` |
| `gate_result` | gate 结果 | 枚举或 `pending_audit` |
| `decision` | 当前处理决定 | 枚举或 `pending_audit` |
| `evidence_doc` | 证据文档路径 | 必填；未知写 `pending_audit` |
| `next_action` | 下一步动作 | 必填 |

允许的 `gate_result` 初始枚举：

- `candidate_rescues_legacy_but_not_near_raw`
- `candidate_metric_near_raw_structure_mixed`
- `proxy_or_partial_pending_audit`
- `pending_audit`

允许的 `decision` 初始枚举：

- `archive_diagnostic`
- `archive_pending_audit`
- `pending_audit`

## candidate_registry.csv

固定字段：

| 字段 | 含义 | 最低规则 |
| --- | --- | --- |
| `candidate_id` | 候选编号 | 必填，唯一 |
| `family` | 方法族 | 必填 |
| `method_summary` | 简短机制说明 | 必填 |
| `design_doc` | 设计或状态入口 | 必填 |
| `first_run` | 首次 run id | 必填 |
| `last_run` | 最近 run id | 必填 |
| `best_gate_result` | 该候选目前最好 gate | 必填 |
| `current_decision` | 当前决策 | 必填 |
| `archive_status` | 归档状态 | 必填 |
| `may_iterate` | 是否可继续迭代 | 只能是 `yes` 或 `no` |
| `notes` | 边界说明 | 必填 |

## 提交前校验

提交治理层前至少检查：

1. 每行字段数必须等于 header 字段数。
2. header 不允许空字段。
3. `run_id` 和 `candidate_id` 不允许空。
4. `may_iterate` 只能是 `yes` 或 `no`。
5. mixed/weak 候选不得写成 completed goal、formal mainline 或 stable downstream gain。
6. `P28` 这类未完成 fixed-detector 审计的候选必须保持 `pending_audit` 或 `proxy_or_partial_pending_audit`。
