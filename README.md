# Stage1Codex

面向有害藻华水下显微图像的分阶段增强项目，不是一般自然场景水下增强仓库。

当前仓库已经完成正式主线锁定、正式阶段评测和正式外部主表评测。它现在更接近“论文底稿 + 正式结果入口 + 后续下游衔接工作台”，而不是早期探索期实验仓库。

## 1. 当前正式主线

当前正式增强链路为：

`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`

当前锁定组合为：

- `BPH = r2_05_G_P_A_B`
- `IMF1Ray = locked existing output`
- `RGHS = rghs_s07`
- `CLAHE = clahe_s05`
- `Fusion = fusion_s10`
- `Final = r4_03 / homomorphic_entropy`

当前唯一正式配置：

- `experiments/optimization_v1/configs/locked_full506_final_mainline.json`

当前唯一正式结果副本：

- `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`

正式运行提醒：

- 当前正式主线必须显式传 `experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 直接运行 `python main.py` 的默认参数不会自动落到当前正式论文主线
- 当前不会把 `main.py` 默认入口升格为正式主线，以免历史流程和正式流程混淆

## 2. 当前正式评测口径

当前正式论文口径分为两层：

- `full502_clean_v1`
  - 用于阶段进度表
  - manifest: `metrics/manifests/full502_clean_v1.txt`
- `compare9_complete496_v1`
  - 用于 `Ours + 8 baselines` 主比较表
  - manifest: `metrics/manifests/compare9_complete496_v1.txt`

需要明确：

- `full506` 现在只表示历史搜索与锁定背景，不再是当前正式论文主表口径
- 当前不是“还没统一评测”，而是已经形成正式阶段表和正式主比较表

## 3. 当前正式结果入口

只看这两个目录即可：

- 阶段进度表：`metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
- 外部主比较表：`metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`

辅助入口：

- 方法注册表：`metrics/configs/official_method_registry.json`
- manifest 生成脚本：`metrics/scripts/build_official_manifests.py`
- 正式评测脚本：`metrics/scripts/run_official_evaluations.ps1`

还需要明确一件事：

- 当前仓库内已经保存正式主表输出，因此“阅读结果”不依赖外部方法源码仓库
- 但如果你要在本机重新生成 `official_compare9_complete496`，则仍依赖 `metrics/configs/official_method_registry.json` 中登记的外部方法结果目录
- 这些外部方法结果目录目前是当前工作站上的绝对路径资产，不随本仓库一起分发

## 4. 当前增强与评测环境

下面这条环境说明只适用于当前正式增强与正式评测，不自动覆盖仓库内所有历史脚本：

- conda 根目录：`D:\miniconda3`
- 当前增强与评测环境：`D:\Desktop\EdgeDetection\my_env`

推荐的交互式启动方式：

```bat
cmd.exe /K "D:\miniconda3\Scripts\activate.bat D:\Desktop\EdgeDetection\my_env"
```

推荐的一次性运行方式：

```bat
cmd.exe /D /S /C "call D:\miniconda3\Scripts\activate.bat D:\Desktop\EdgeDetection\my_env && python main.py --params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json"
```

当前已做过 smoke 验证：

- 能用该环境跑 `main.py` 的当前正式主线配置
- 能用该环境跑 `metrics/evaluate_protocol_v2.py`

正式评测脚本 `metrics/scripts/run_official_evaluations.ps1` 也统一指向这套环境，但这不表示仓库内所有历史脚本都已经收口到同一解释器。

正式重跑命令：

```bat
cmd.exe /D /S /C "call D:\miniconda3\Scripts\activate.bat D:\Desktop\EdgeDetection\my_env && powershell -ExecutionPolicy Bypass -File metrics\scripts\run_official_evaluations.ps1"
```

需要注意：

- 该脚本会先重建正式 manifest
- 然后覆盖 `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
- 以及覆盖 `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`

如果只是确认环境或流程是否通，优先做 1 张图 smoke，而不是直接重跑正式全量评测。

## 5. 新接手阅读顺序

第一次进入仓库，按这个顺序看：

1. `docs/project_handoff_guide_cn.md`
2. `docs/project_status_overview_cn.md`
3. `docs/comparison_methods_results_index_cn.md`
4. `research-state.yaml`

这四份文件的职责已经拆开：`README.md` 只做总导航，`project_handoff_guide_cn.md` 负责交接全景，`project_status_overview_cn.md` 负责正式状态快照，`comparison_methods_results_index_cn.md` 负责主表与对比方法索引。

如果要看代码实现，再看：

- `main.py`
- `lgsbph.py`
- `pybemd.py`
- `wb_safe_contrast.py`
- `clahe_guided_visibility.py`
- `fusion_three.py`
- `lvbo.py`

## 6. 当前还缺什么

当前最关键的缺口不是统一评测，而是：

- 与当前正式主线严格对齐的下游边缘验证总表
- paper-ready 的代表性 qualitative panel 与失败案例图组
- 数据采集/覆盖范围/公开性说明，以及运行时间与资源说明

## 7. 结果解释边界

当前主表解释统一采用以下口径：

- `MS_SSIM` 与 `PSNR` 表示增强结果相对原图的结构一致性，不是相对增强真值的质量指标
- `WWPF` 保留在主表中，作为激进但可接受的强基线
- `HLRP` 与 `Histoformer` 的数值保留在正式主表中，但正文层面只在当前 HAB 显微图像协议下作为失败案例或补充分析讨论
- 这些结论只适用于当前有害藻华显微图像任务、本地复现实验和当前指标解释，不构成对原方法既有论文结论的否定

## 8. 历史资产说明

以下内容属于历史搜索、旧口径结果或归档背景，不再作为正式论文入口：

- `results_optimized_c25`
- 旧 `full506` 评测目录
- `metrics/archive/`
- 其他围绕旧 `c25`、旧 `506` 口径生成的临时汇总与对比输出

如果需要理解这些资产与当前正式口径的关系，请看：

- `docs/project_handoff_guide_cn.md`
- `docs/project_status_overview_cn.md`
- `research-state.yaml`
