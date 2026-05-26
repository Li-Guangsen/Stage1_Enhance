# 命令与环境规则

更新时间：2026-05-26

## Python

- Codex 侧文档生成、YAML/CSV 检查和轻量结构校验使用 `D:/Desktop/DeepLearning/my_env/python.exe`。
- 不使用裸 `python`，除非任务就是检查系统默认 Python。
- Stage1 增强实验环境按 Stage1 既有文档和 run sheet 记录，不能在聊天中省略环境。

## PowerShell / CMD / WSL

- 给用户命令时必须写清执行上下文：Windows PowerShell、CMD、WSL 或远程服务器。
- Windows CMD 不支持 `Tee-Object`。
- PowerShell 中可用 `Tee-Object` 保存日志。
- WSL 简单命令可用单引号 `wsl bash -lc '...'`。
- 含 Bash 变量、数组、循环、多 run 的 WSL 命令必须写成 `.sh` 文件，再用 `wsl bash script.sh` 执行。
- 禁止把复杂 Bash 放进 PowerShell 双引号 `$cmd` 后再调用 `wsl bash -lc "$cmd"`。

## 日志

- 任何实验、sampling、eval/show 或指标 intake 都必须保存日志。
- 日志路径必须落入候选专属 output root 或 `logs/`。
- 如果命令失败，失败日志仍保留并在 status 中标注为历史失败，不覆盖正式成功日志。
