# full_algae_dewatermark_v1 Stage1 full-pool protocol

更新时间：2026-05-25

## 定位

本目录用于记录完整增强图像池 `full_algae_dewatermark_v1` 的 Stage1 full-pool 扩展协议。

当前状态：

- 已完成数据 inventory。
- 已完成 OpenCV decode / dimension / channel / dtype 审计。
- 已完成 `main.py` full-pool I/O 兼容修正。
- 已完成 1 张与 10 张 smoke。
- 已完成 2770 张 full run 时间/磁盘预算估算。
- 已准备可恢复 full run 脚本。
- 已准备 full run 只读接收脚本，并生成当前 `not_started` 状态报告。
- 尚未运行 2770 张完整增强。
- 尚未把 full-pool 结果升格为论文正式主表。

当前正式论文结果仍以以下口径为准：

- 阶段评测：`full502_clean_v1`
- 主比较：`compare9_complete496_v1`

## 输入口径

源目录：

- `D:\Desktop\去水印所有藻类图像`

候选 manifest：

- `metrics/manifests/full_algae_dewatermark_v1.txt`
- 数量：2774

OpenCV 可读候选 manifest：

- `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt`
- 数量：2770

decode 失败清单：

- `metrics/manifests/full_algae_dewatermark_v1_decode_failures.tsv`
- 数量：4
- 原因：`.jpg` 扩展但文件内容签名为 `GIF89a`

当前 full-pool smoke 采用 `full_algae_dewatermark_v1_cv2_readable_candidate.txt`，即暂时排除 4 个 OpenCV 不可读候选文件。

## 锁定配置

Stage1 增强必须显式使用：

- `experiments/optimization_v1/configs/locked_full506_final_mainline.json`

不能把默认 `python main.py` 当作正式主线。

## Smoke 输出

1 张 smoke：

- `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_limit1_locked_final_mainline`
- 结果：成功。
- 输出完整性：JPG/PNG 六阶段各 1 个文件。

10 张 smoke：

- `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_limit10_locked_final_mainline`
- 结果：成功。
- 输出完整性：JPG/PNG 六阶段各 10 个文件。
- 完整性检查 JSON：`experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_limit10_locked_final_mainline_completeness.json`
- 说明：第一次 10 张运行在 5 分钟工具超时前已完成前 7 张和第 8 张部分输出；随后用 `--skip-existing` 续跑补齐到 10 张。最终输出完整。

10 张 smoke 覆盖：

- 中文顶层文件夹路径。
- 文件名空格。
- 文件名括号。
- 至少 1 张 4 通道输入，进入 OpenCV `IMREAD_COLOR` 后按 3 通道处理。
- 嵌套输出目录。

## Full-run 预算

预算文档：

- `experiments/full-algae-dewatermark-v1/run_budget_estimate.md`

当前估算：

- 2770 张完整增强耗时约 `46-60` 小时。
- 六阶段 JPG/PNG 输出约 `3.04 GiB`。
- 建议至少预留 `5 GiB`，若后续还要生成评测、diagnostics、panels 或备份，建议预留 `8-10 GiB`。

该估算来自 10 张 smoke 输出大小和观测 wall time，只作为运行调度依据，不是实验结果。

## Full-run 入口

可恢复 full run 脚本：

- `experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1`

该脚本未来运行时会写入日志：

- `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline/logs/full2770_locked_final_mainline.log`

默认命令：

```powershell
powershell -ExecutionPolicy Bypass -File experiments\full-algae-dewatermark-v1\run_full_cv2readable2770_locked.ps1
```

该脚本默认启用 `--skip-existing`，因此中断后可再次运行继续补齐。若要先做更大一点的小批量，可使用：

```powershell
powershell -ExecutionPolicy Bypass -File experiments\full-algae-dewatermark-v1\run_full_cv2readable2770_locked.ps1 -Limit 20
```

完整性检查脚本：

- `metrics/scripts/summarize_stage1_run_outputs.py`

只读接收脚本：

- `metrics/scripts/intake_stage1_fullpool_run_outputs.py`

当前只读接收状态报告：

- `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.md`
- `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.json`

当前状态为 `not_started`：输出根目录不存在，预期 `2770` 张、`33240` 个六阶段 JPG/PNG 输出文件，当前存在 `0` 个。该报告不是运行记录，不能写成 2770 张完整增强已完成。

未来 2770 张完整增强完成后，使用：

```powershell
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\summarize_stage1_run_outputs.py --manifest metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt --output-dir experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\full2770_locked_final_mainline --output-json experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\full2770_locked_final_mainline_completeness.json
```

推荐的 full run 接收命令：

```powershell
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\intake_stage1_fullpool_run_outputs.py
```

只有当接收状态达到 `core_outputs_complete` 或 `complete_with_log_and_run_report` 后，才允许写入 full run 的 `run_report.md`：

```powershell
D:\Desktop\EdgeDetection\my_env\python.exe metrics\scripts\intake_stage1_fullpool_run_outputs.py --write-run-report
```

## Smoke 命令

1 张 smoke：

```bat
D:\Desktop\EdgeDetection\my_env\python.exe main.py --input-dir "D:\Desktop\去水印所有藻类图像" --manifest metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt --limit 1 --params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json --output-dir experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\smoke_limit1_locked_final_mainline
```

10 张 smoke 初次运行：

```bat
D:\Desktop\EdgeDetection\my_env\python.exe main.py --input-dir "D:\Desktop\去水印所有藻类图像" --manifest metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt --limit 10 --params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json --output-dir experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\smoke_limit10_locked_final_mainline
```

10 张 smoke 续跑：

```bat
D:\Desktop\EdgeDetection\my_env\python.exe main.py --input-dir "D:\Desktop\去水印所有藻类图像" --manifest metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt --limit 10 --params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json --output-dir experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\smoke_limit10_locked_final_mainline --skip-existing
```

## 下一步

在运行 2770 张完整增强前，还需要：

1. 决定 4 个 `GIF89a` 内容文件是转换为标准图像，还是长期排除于 OpenCV full-pool 协议。
2. 选择运行窗口并预留至少 5 GiB 磁盘空间。
3. 确认 full-pool 评测脚本能按相对路径追踪样本，不能只按 stem 合并。
4. 完整 full run 必须写入新目录，不能覆盖正式 502/496 结果。
5. full run 后必须先运行只读接收脚本；未达到 `complete_with_log_and_run_report` 前，不能把 full-pool 写成完整扩展增强资产。
