# Codex 指令加载验证

更新时间：2026-05-26

本文件记录如何确认 Codex/agent 是否读取了根 `AGENTS.md` 和近场 override。它是验证说明，不要求每轮都运行。

## 规则来源

- 根规则：`AGENTS.md`
- 实验近场规则：`experiments/AGENTS.override.md`
- 完整执行规则：`docs/project_execution_rules_cn.md`
- 当前治理入口：`docs/current_experiment_status_cn.md`

## 验证命令

从仓库根目录运行：

```powershell
codex --ask-for-approval never "Summarize the current instructions."
```

从 `experiments/` 运行：

```powershell
codex --cd experiments --ask-for-approval never "Show which instruction files are active."
```

预期输出应能体现根 `AGENTS.md` 与 `experiments/AGENTS.override.md` 均生效。

## 截断风险

如果 agent 输出看不到治理规则，优先检查：

- 是否在正确 cwd 启动。
- 是否有 nested instruction 文件覆盖。
- 项目文档是否过大导致 instruction truncation。
- Codex 配置中的 `project_doc_max_bytes` 是否过小。

发现加载异常时，不继续实验；先修正入口或压缩规则，再记录到 `research-log.md`。
