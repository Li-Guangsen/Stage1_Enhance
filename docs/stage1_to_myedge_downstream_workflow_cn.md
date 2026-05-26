# Stage1 -> MyEdge 下游验证工作流

更新时间：2026-05-26

本文件只规范流程，不授权自动运行训练、增强、sampling、`eval.py` 或 `show.py`。

## 标准链路

1. Stage1 生成 168 张带 GT split 的 candidate Final 输出。
2. 只读检查 stem、数量、decode 和 manifest。
3. MyEdge 侧按同 stem staging 到 Stage1 coupling run。
4. 使用固定 MSFI 50k 和固定 DiffusionEdge baseline 50k detector。
5. Windows PowerShell 只运行 sampling 命令；执行前必须明确环境和输出 root。
6. WSL `eval.py` / `show.py` 使用 `.sh` 脚本执行，多 run、数组、循环不得塞进 PowerShell 双引号 `$cmd`。
7. result intake 读取 `eval_bdry.txt`、`show.log`、run report 和 manifest。
8. structure proxy 只作为补充诊断。
9. gate 决策写回 Stage1 状态、registry 和 `research-log.md`。

## 口径边界

- 168 张带 GT split 是 downstream validation 核心。
- 502/496 只用于 Stage1 增强指标与 complete-case 对照。
- 2770 full-pool 不能替代带 GT downstream validation。
- fixed detector 期间不得改 detector、权重、GT、MAT、eval protocol 或 MyEdge 正式结果资产。

## 命令环境原则

- Stage1 本地增强环境按现有 Stage1 文档记录执行。
- Codex 侧 YAML/CSV/文档检查使用 `D:/Desktop/DeepLearning/my_env/python.exe`。
- 给用户命令时必须标明 Windows PowerShell、CMD、WSL 或远程服务器。
