# Candidate 生命周期规则

更新时间：2026-05-26

本规则用于把候选从“无限微调”改成可审计生命周期。

## 生命周期

1. method review：说明候选机制、来源、差异点和风险。
2. run sheet：填写 `docs/experiment_run_sheet_template_cn.md`。
3. smoke：只验证代码路径、输出目录和 decode，不得写成效果。
4. 166 enhance：基于 MyEdge raw split 生成候选输入资产，并统一排除 `chazhuang.3.jpg` 与 `chazhuang.6.jpg` 后进入主筛选。
5. fixed detector：固定 DiffusionEdge/MSFI，不改 detector，不改权重，不改 GT。
6. eval/show intake：读取正式 `eval_bdry.txt` 和 `show.log`。
7. structure proxy：只作为补充诊断，不替代 ODS/OIS/AP/AC。
8. decision：归档、停止、重构或晋级。
9. registry/log：同步 registry、状态文档和 `research-log.md`。

## 晋级规则

- proxy-only 只能晋级到 fixed-detector gate，不能晋级到正式结果。
- mixed gate 之后不得自动派生同族小修补候选，必须先做 method review。
- 连续两个同族候选都是 mixed/weak 时，该 family 进入暂停审计。
- 只有 strong pass 或明确候选通过且机制价值充足时，才考虑 502/496 补充增强指标。
- 2770 full-pool 只在 MyEdge 166 complete-case 通过且 full-pool clean protocol/readiness 合格后作为可选工程扩展。

## 归档规则

候选失败不删除。失败结论应记录为有效证据，说明失败机制和后续禁止重复的设计。
