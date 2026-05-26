# Stage1 enhancement-to-edge 支撑包说明（中文）

更新时间：2026-05-24

本文档记录 Stage1Codex 当前已经形成的增强到边缘结构支撑包。它的作用是把 Stage1 从“普通图像增强结果”转成后续 MyEdge 主论文可引用的 `task-driven structure-preserving enhancement` 证据入口。

重要边界：

- 本支撑包是无人工边缘 GT 的代理验证，不替代 MyEdge / DiffusionEdge 体系中的 ODS、OIS、AP、AC 主实验。
- 本支撑包可以说明 Stage1 已形成可执行、可追溯的边缘结构代理结果；不能写成已经证明下游边缘检测精度提升。
- 边缘响应、skeleton 密度或端点密度的变化只能作为筛查和选图依据，不能直接等同于生物结构更准确。

## 1. 固定输入

正式主线：

- 配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 正式结果：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`

两套验证口径：

| Suite | Manifest | Count | 方法集合 |
| --- | --- | ---: | --- |
| `stage_full502_proxy` | `metrics/manifests/full502_clean_v1.txt` | 502 | `Original`、`BPH`、`IMF1Ray`、`RGHS`、`CLAHE`、`Fused`、`Final` |
| `compare9_complete496_proxy` | `metrics/manifests/compare9_complete496_v1.txt` | 496 | `Original`、`Ours`、8 个外部增强方法 |

其中 `compare9_complete496_proxy` 继续保留 `WWPF`，并沿用其官方实现稳定输出 496 张的 complete-case 边界。

## 2. 当前输出

输出根目录：

`metrics/outputs/downstream_edge_validation/official_full502_mainline`

核心产物：

| Suite | Complete cases | Failures | Summary | Per-image | Panels |
| --- | ---: | ---: | --- | --- | --- |
| `stage` | 502 | 0 | `stage_full502_proxy/summary.md` | `stage_full502_proxy/per_image_metrics.csv` | `stage_full502_proxy/qualitative_panels/` |
| `compare` | 496 | 0 | `compare9_complete496_proxy/summary.md` | `compare9_complete496_proxy/per_image_metrics.csv` | `compare9_complete496_proxy/qualitative_panels/` |

自动生成的定性图候选：

- 阶段图候选：`duolie.5`、`juciqigou.2`、`weiruan.2`、`weiruan.4`
- 外部对比/失败案例候选：`lianzhuang.2`、`qiangzhuang.13`、`qiangzhuang.8`、`xuanlianjiaomao.6`
- 每个候选样本同时生成原图/增强结果 panel 和 edge overlay panel。

这些图组是候选图，不等于最终投稿图。正式使用前仍需人工核查细胞边界、背景杂质和伪边缘表现。

## 3. 代理边缘方法

当前脚本：

`metrics/scripts/run_downstream_edge_proxy_stage1.py`

运行环境：

- Python：`D:\Desktop\EdgeDetection\my_env\python.exe`
- 依赖：`cv2`、`numpy`、`skimage`
- 本轮运行使用 CPU 图像处理；未训练网络，未使用 MyEdge 模型。

执行命令：

```powershell
& 'D:\Desktop\EdgeDetection\my_env\python.exe' metrics\scripts\run_downstream_edge_proxy_stage1.py --suite both --panel-count 4 --output-root metrics\outputs\downstream_edge_validation\official_full502_mainline --quiet
```

代理方法流程：

1. 读取 manifest 对应样本。
2. 将图像统一 resize 到 `320x320`。
3. 灰度化并做 Gaussian blur。
4. 计算 Sobel magnitude。
5. 用 Otsu 阈值生成二值 edge mask。
6. 统计连通域、skeleton、端点和分叉点。
7. 对每个方法计算相对 `Original` 的差值。

本轮记录的运行耗时：

- `stage_full502_proxy`：18.521 秒
- `compare9_complete496_proxy`：24.734 秒

## 4. 当前主要观察

### 4.1 阶段级代理结果

在 `full502_clean_v1` 上，`Final` 相对 `Original` 的平均边缘结构代理变化为：

- `edge_density`：0.051260 -> 0.080834，`+0.029573`
- `sobel_mean`：0.050954 -> 0.188390，`+0.137436`
- `skeleton_density`：0.021057 -> 0.044573，`+0.023516`
- `skeleton_endpoint_density`：0.060085 -> 0.080043

阶段趋势显示，从 `IMF1Ray` 到 `Final`，边缘响应和 skeleton 密度整体增加。这个结果支持将 Stage1 写成“为边界结构形成提供输入证据”的候选支撑，但还不能说明边缘检测精度已经提高。

### 4.2 外部增强对比代理结果

在 `compare9_complete496_v1` 上，`Ours` 相对 `Original` 的平均边缘结构代理变化为：

- `edge_density`：0.050500 -> 0.080303，`+0.029803`
- `sobel_mean`：0.049577 -> 0.187681，`+0.138104`
- `skeleton_density`：0.020754 -> 0.044333，`+0.023579`
- `skeleton_endpoint_density`：0.059768 -> 0.080099

外部方法中，`HLRP`、`Histoformer` 和 `WWPF` 的边缘响应代理值更激进：

- `HLRP edge_density = 0.207390`
- `Histoformer edge_density = 0.193116`
- `WWPF edge_density = 0.111171`

该现象应谨慎解释。更高边缘响应可能来自真实边界增强，也可能来自过增强、噪声、杂质和伪边缘。结合当前增强主表和定性观察，`HLRP` 与 `Histoformer` 仍应作为当前 HAB 显微协议下的失败案例或补充分析，而不是稳健强基线。

## 5. 对 MyEdge 的交接意义

Stage1 当前可以提供三类输入给 MyEdge 主论文：

1. 阶段级输入：`Original`、`BPH`、`IMF1Ray`、`RGHS`、`CLAHE`、`Fused`、`Final`
2. 外部增强输入：`Ours` 与 8 个外部增强方法的 complete-case 结果
3. 选图候选：阶段演化图、外部对比图、edge overlay 和失败案例候选

MyEdge 后续需要补的是真正带 GT 或固定 detector 的边缘检测实验：

- `Original / Stage1 stages / external enhancements -> same detector`
- 固定 DiffusionEdge 与固定 MSFI 两套评估
- ODS、OIS、AP、AC、edge thickness、断边率、伪边缘率等任务指标
- 对低对比、弱边界、气泡/杂质和模糊边界样本做子集分析

## 6. 写作建议

可写：

- Stage1 已完成正式增强主线、正式增强主表和无 GT 边缘结构代理支撑包。
- Stage1 的角色应从“独立普通增强论文主创新”调整为“面向 MyEdge 的结构保持增强输入形成”。
- 当前 proxy 结果显示 `Final` 相比 `Original` 提高了 Sobel 边缘响应和 skeleton 密度，可作为后续 GT 边缘实验的输入依据。

不可写：

- Stage1 已经证明 ODS/OIS/AP/AC 提升。
- Stage1 已经完成下游边缘任务闭环。
- HLRP/Histoformer 在一般水下场景中无效。
- 边缘响应越多即代表边缘质量越好。
