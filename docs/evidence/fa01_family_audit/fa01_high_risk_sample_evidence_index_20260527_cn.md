# FA01 high-risk sample evidence index

日期：2026-05-27

## 1. 状态

- status: `complete_path_index_no_new_experiment`
- 输入：FA01 168 raw-vs-Final per-image enhancement proxy、FA01 top adverse detector proxy cases、已点名 high-risk 样本。
- 输出目录：`docs/evidence/fa01_family_audit/fa01_high_risk_sample_index_20260527/`
- 边界：本索引只记录路径与存在性，不复制大图，不运行增强、MyEdge sampling、WSL eval/show、训练、502/496 或 2770。

## 2. 选择规则

样本进入索引的条件：

- 每个变体按 `grad_mean_ratio` 取 top 5。
- 每个变体按 `mean_abs_bgr_delta` 取 top 3。
- FA01 文档中已点名的 `tama.14`、`tama.11`、`tama.9`、`tama.13`、`weixiaoyuanjia.21`、`weixiaoyuanjia.22`、`donghaiyuanjia.18`、`jianci.4`。
- 每个变体/检测器按 `f1_loss`、`false_edge_increase`、`endpoint_increase` 取 top 5 detector-adverse cases。

最终索引包含 `57` 个 stem。它覆盖了增强强度异常、视觉风险、FF01/FF02 已知风险、以及 detector structure proxy 最差样本。

## 3. 产物

- 样本摘要：`docs/evidence/fa01_family_audit/fa01_high_risk_sample_index_20260527/fa01_high_risk_sample_summary.csv`
- Stage1/raw/GT 路径：`docs/evidence/fa01_family_audit/fa01_high_risk_sample_index_20260527/fa01_high_risk_stage1_paths.csv`
- MyEdge detector 输出路径：`docs/evidence/fa01_family_audit/fa01_high_risk_sample_index_20260527/fa01_high_risk_detector_paths.csv`
- JSON index：`docs/evidence/fa01_family_audit/fa01_high_risk_sample_index_20260527/fa01_high_risk_index.json`

## 4. 用法

每个 high-risk stem 都能从路径表定位：

- raw input：`data/inputImg/Original`
- GT edge：`D:/Desktop/MyEdgeCodex/eval-edge-py/GT/ALGAE`
- Stage1 outputs：legacy Final、P27、D01、FF01、FF02
- MyEdge outputs：raw anchor、legacy Final、P27、D01、FF01、FF02 在 MSFI 和 DiffusionEdge baseline 下的 `png`、`white`、`overlay`、`error_map`、`mat`、`mat-eval`、`nms`、`nms-eval`

下一步人工或脚本审查应优先看：

- `weixiaoyuanjia.21`：FF01/FF02 均已点名，FF01 false-edge severe。
- `weixiaoyuanjia.26`：FF01/FF02 detector-adverse false-edge top case。
- `xuehong.9`、`xuehong.13`、`xuehong.11`：FF01/FF02 false-edge adverse cluster。
- `donghaiyuanjia.26`：FF01/FF02 adverse cluster。
- `tama.14`、`tama.11`、`tama.9`：enhancement/proxy high-gradient cluster。
- `jianci.4`、`donghaiyuanjia.18`：FF01/FF02 已点名风险样本。

## 5. 决策边界

该索引不是新结果，也不是下游正收益证据。它的作用是让后续 failure audit 能逐图定位“增强变化 -> detector 输出 -> GT/error map”的证据链，避免继续凭全局均值猜测失败原因。
