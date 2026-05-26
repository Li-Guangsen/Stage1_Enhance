# 下游边缘验证协议规划（中文）

更新时间：2026-05-25

本文档最初是未来下游边缘验证的协议规划。当前已经完成第一版 Stage1 无 GT 边缘结构代理验证，并生成到 `metrics/outputs/downstream_edge_validation/official_full502_mainline`。该结果包用于 Stage1 到 MyEdge 的衔接准备，不替代带 GT 的 MyEdge / DiffusionEdge 边缘检测主实验。

## 1. 协议目标

目标是验证当前正式增强结果是否有助于 HAB 显微图像的结构可读性和边缘提取，而不是重新选择增强主线。当前分为两层：

- 已完成：无 GT 边缘结构代理验证，覆盖阶段级和外部增强方法级输入。
- 待完成：带 GT 或固定 detector 的 MyEdge 边缘检测评测，报告 ODS/OIS/AP/AC 等任务指标。

当前阶段不能写成“下游边缘检测精度已经提升”。论文中可以写成“Stage1 已形成无 GT 边缘结构代理支撑包，正式 MyEdge 下游验证仍待完成”。

补充：当前已从 `D:\Desktop\MyEdgeCodex` 只读同步 Stage1 -> MyEdge 168 张带 GT coupling 状态快照：

- 快照：`docs/stage1_myedge_coupling_status_20260525_cn.md`
- MyEdge 168-image coupling manifest：`168` 行
- GT missing：`0`
- Stage1 六阶段缺失：`0`
- P1 result intake：`not_started`
- P1 output roots：不存在

该快照只证明未来带 GT 固定 detector 验证的输入对齐已经有 MyEdge 侧 planning asset，不证明 Stage1 已提升 ODS/OIS/AP/AC。

## 2. 固定输入

- 原图目录：`data/inputImg/Original`
- 增强结果目录：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`
- 样本清单：`metrics/manifests/full502_clean_v1.txt`
- 正式配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`

输入边界：

- 不使用旧 `pilot92-v1` 作为正式验证口径。
- 不使用旧 `full506` 评测目录作为正式主表或正式下游入口。
- 第一版代理验证已经扩展为两套：`stage_full502_proxy` 覆盖阶段级输出，`compare9_complete496_proxy` 覆盖外部增强方法 complete-case 输出。

## 3. 推荐输出位置

当前输出目录：

`metrics/outputs/downstream_edge_validation/official_full502_mainline`

当前已生成产物集合：

- `index.md`
- `stage_full502_proxy/summary.md`
- `stage_full502_proxy/summary.csv`
- `stage_full502_proxy/per_image_metrics.csv`
- `stage_full502_proxy/method_note.md`
- `stage_full502_proxy/qualitative_panels/`
- `compare9_complete496_proxy/summary.md`
- `compare9_complete496_proxy/summary.csv`
- `compare9_complete496_proxy/per_image_metrics.csv`
- `compare9_complete496_proxy/method_note.md`
- `compare9_complete496_proxy/qualitative_panels/`

详细解释见 `docs/stage1_enhancement_to_edge_support_cn.md`。

## 4. 指标与记录字段规划

当前 `per_image_metrics.csv` 包含：

| 字段 | 含义 |
| --- | --- |
| `suite` | `stage` 或 `compare` |
| `method` | 输入方法或阶段 |
| `stem` | 与 manifest 一致的样本 ID |
| `image_path` | 实际读取图像路径 |
| `edge_density` | Sobel/Otsu 二值边缘密度 |
| `sobel_mean` | Sobel magnitude 均值 |
| `skeleton_density` | skeleton 像素密度 |
| `skeleton_endpoint_density` | skeleton 端点密度 |
| `delta_*_vs_original` | 相对同图 `Original` 的差值 |

`summary.md` 已说明 manifest、complete cases、失败数、边缘代理方法、主要均值和解释边界。

## 5. 论文写作边界

当前 proxy 完成后，正文可以写：

- 当前方法面向结构可读性和边缘敏感分析设计。
- 当前正式增强结果已形成阶段表和外部主比较表。
- Stage1 已形成无 GT 边缘结构代理支撑包，可供 MyEdge 后续固定 detector 或 GT 边缘评测使用。

不能写：

- “已经证明下游边缘检测显著提升”。
- “边缘友好闭环已经完成”。
- “增强结果直接带来稳定下游性能提升”。

完成该实验之后，也仍需区分：

- 边缘响应变多不必然等于生物结构更准确。
- 边缘指标应与定性图组和失败案例共同解释。
- 任何负面或正面结论都限定在当前 HAB 显微图像协议下。

## 6. 后续执行顺序

1. 在 MyEdgeCodex 中继续使用已有 168 张 coupling manifest、P1 command sheet 和 intake/sync 脚本；执行前必须获得高风险确认。
2. 先 staging Stage1 Final 到原 MyEdge stem 文件名，再分别跑固定 `MSFI 50k` 和 `DiffusionEdge baseline 50k`。
3. 运行 MyEdge `eval.py` / `show.py` 后，用 MyEdge 只读 intake 脚本确认 P1 核心输出和 report assets 完整。
4. 再把 ODS、OIS、AP、AC、edge thickness、断边率、伪边缘率等任务指标同步回 Stage1 证据包。
5. 人工抽查本支撑包生成的候选 panel 和 MyEdge P1 overlay/error-map，筛选最终投稿图。
6. 将 MyEdge 结果回写到总体论文证据包，而不是把当前 proxy 或 `not_started` 快照误写成最终下游结论。
