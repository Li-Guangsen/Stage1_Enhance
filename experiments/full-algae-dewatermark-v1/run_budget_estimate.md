# full_algae_dewatermark_v1 full-run budget estimate

更新时间：2026-05-24

## 当前结论

当前建议不要在无人值守前直接启动 2770 张完整增强。先按下面预算预留资源：

- 时间预算：约 46-60 小时。
- 磁盘预算：Stage1 六阶段 JPG/PNG 输出约 3.1 GiB，建议至少预留 5 GiB；如果后续生成评测表、diagnostics、panels 或备份，建议预留 8-10 GiB。
- 运行策略：使用可恢复脚本 `run_full_cv2readable2770_locked.ps1`，默认启用 `--skip-existing`，中断后可继续。

## 估算依据

10 张 smoke 输出目录：

- `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_limit10_locked_final_mainline`

10 张 smoke 输出统计：

| 项目 | 数值 |
| --- | ---: |
| 图像数 | 10 |
| 输出文件数 | 120 |
| 总输出大小 | 11.24 MiB |
| 平均每输入图输出大小 | 1.124 MiB |

按 2770 张估算：

| 目标 | 估算 |
| --- | ---: |
| 输出文件数 | 33240 |
| 输出大小 | 3.04 GiB |

注意：这是从首批 10 张 smoke 外推的估算。完整图像池尺寸跨度很大，实际输出大小可能偏离；建议至少按 5 GiB 预留。

## 时间估算

已观测 smoke wall time：

- 1 张 smoke：约 62 秒。
- 10 张 smoke：第一次运行 5 分钟工具超时前完成 7 张和第 8 张部分输出，续跑补齐剩余图像，总体可按约 55-65 秒/图估算。

按 2770 张估算：

| 单图耗时 | 2770 张耗时 |
| ---: | ---: |
| 55 秒/图 | 42.3 小时 |
| 60 秒/图 | 46.2 小时 |
| 65 秒/图 | 50.0 小时 |

考虑工具超时、I/O 波动和 warning，实际调度建议按 46-60 小时准备。

## 推荐长跑命令

在仓库根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File experiments\full-algae-dewatermark-v1\run_full_cv2readable2770_locked.ps1
```

只做小批量测试：

```powershell
powershell -ExecutionPolicy Bypass -File experiments\full-algae-dewatermark-v1\run_full_cv2readable2770_locked.ps1 -Limit 20
```

该脚本默认启用 `--skip-existing`。如果必须重跑已有输出，可使用：

```powershell
powershell -ExecutionPolicy Bypass -File experiments\full-algae-dewatermark-v1\run_full_cv2readable2770_locked.ps1 -NoSkipExisting
```

## 完整性检查

10 张 smoke 检查命令：

```powershell
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\summarize_stage1_run_outputs.py --manifest metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt --limit 10 --output-dir experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\smoke_limit10_locked_final_mainline
```

未来 2770 张完整增强完成后，检查命令：

```powershell
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\summarize_stage1_run_outputs.py --manifest metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt --output-dir experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\full2770_locked_final_mainline --output-json experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\full2770_locked_final_mainline_completeness.json
```

验收标准：

- JPG 六阶段各 2770 个文件。
- PNG 六阶段各 2770 个文件。
- `all_complete = true`。

## 当前未做

- 未启动 2770 张完整增强。
- 未评测 full-pool 输出。
- 未将 full-pool 结果替代当前正式 502/496 论文口径。
