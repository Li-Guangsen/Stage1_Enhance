# 实验证据资产分层索引

更新时间：2026-05-27

本文件是 Stage1Codex 的证据边界主表，用于避免把 source asset、paper metric、downstream diagnostic、proxy、readiness 或候选输出误写成同一类事实。

## 1. 标签定义

| 标签 | 含义 |
| --- | --- |
| `formal source asset` | 当前正式增强源资产，可作为结果来源路径，但不等于论文统计口径 |
| `paper metric` | 可用于论文增强指标表的正式统计口径 |
| `downstream diagnostic` | 固定 detector / 带 GT 或相关诊断结果，只能在限定口径下解释 |
| `proxy only` | 结构代理、Sobel/Otsu、paired proxy 等补充诊断，不是下游精度 |
| `readiness only` | 预执行、manifest、decode、staging、脚本准备，不是结果 |
| `historical / archived` | 历史搜索、旧口径或归档资产 |
| `not claimable` | 不能作为论文结果主张，只能作为待复核或不可见事实 |

## 2. 当前资产分层

| 资产层 | 代表路径/对象 | 标签 | 当前角色 | 不能写成 |
| --- | --- | --- | --- | --- |
| locked config | `experiments/optimization_v1/configs/locked_full506_final_mainline.json` | `formal source asset` | Stage1 locked enhancement 配置 | 当前总体论文主创新 |
| formal output root | `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline` | `formal source asset` | 502/496 paper metrics 的源结果资产 | `full506` 主表样本口径 |
| locked Final | `.../png/Final` | `formal source asset` / `downstream diagnostic` | 增强主表中的 formal output；MyEdge 168 fixed-detector 中的 legacy negative control | 稳定提升 downstream ODS/OIS/AP/AC |
| stage metrics | `full502_clean_v1` | `paper metric` | 502 张阶段进度表 | downstream validation |
| comparison metrics | `compare9_complete496_v1` | `paper metric` | 496 张 9 方法 complete-case 主比较 | full506 主表或 downstream validation |
| raw anchor | MyEdge 168 raw input | `downstream diagnostic` | fixed-detector 强 anchor | Stage1 方法结果 |
| negative baseline | locked Final -> fixed MSFI/DiffusionEdge | `downstream diagnostic` | 旧主线负向下游证据 | 新候选失败的重复任务 |
| P12-P28 | `experiments/downstream_driven_v1` | `downstream diagnostic` / `historical / archived` | 候选、对照、失败或诊断证据 | 正式增强主线、strong pass |
| D01 | `experiments/downstream_driven_v2` | `downstream diagnostic` / `historical / archived` | mechanism-complete weak diagnostic candidate | strong pass、正式主线、稳定下游收益 |
| FF01/FF02 | `experiments/full_flow_downstream_stage1_mainline_v1`、`experiments/full_flow_downstream_stage1_mainline_v2` | `downstream diagnostic` / `historical / archived` | 完整增强主线恢复轨道的失败诊断证据 | 下游正收益、candidate pass、502/496 或 2770 推广入口 |
| TLVC01 | `experiments/topology_locked_visual_chroma_full_flow_v1` | `downstream diagnostic` / `historical / archived` | topology-locked 完整流程纠偏候选；证明 exact MyEdge raw topology lock 可降低 direct replacement 风险 | 下游正收益、candidate pass、502/496 或 2770 推广入口 |
| FA01 failure audit | `docs/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`、`docs/fa01_stage1_full_flow_family_audit_tables_20260527/` | `downstream diagnostic` / `proxy only` | FF01/FF02/P27/D01 family-level 失败归因与下一阶段假设来源 | 新候选、训练结果、downstream 正收益 |
| FA01 high-risk index | `docs/fa01_high_risk_sample_evidence_index_20260527_cn.md`、`docs/fa01_high_risk_sample_index_20260527/` | `downstream diagnostic` / `proxy only` | high-risk stem 到 raw、GT、Stage1、MyEdge white/overlay/error_map 的路径索引 | 人工结论、训练结果、正收益证据 |
| FA01 correlation audit | `docs/fa01_per_image_correlation_audit_20260527_cn.md`、`docs/fa01_per_image_correlation_audit_20260527/` | `proxy only` | per-image enhancement proxy 与 detector structure proxy 的相关诊断 | ODS/OIS/AP/AC 重算、因果证明 |
| FA01 visual/error-map review | `docs/fa01_visual_error_map_review_20260527_cn.md`、`docs/fa01_visual_error_map_review_20260527/` | `downstream diagnostic` / `proxy only` | 11 个 high-risk 样本的 raw/GT/Stage1/fixed-detector error-map 审查面板和失败模式标签 | 新实验、人工最终判读、下游正收益 |
| MyEdge/MSFI sidecar protocol | `docs/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md` | `readiness only` / `not claimable` | adaptation run sheet 草案输入 | 已训练、已验证、fixed-detector 结果 |
| Stage1 sidecar map smoke | `docs/stage1_sidecar_map_definition_fa01_20260527_cn.md`、`docs/fa01_stage1_sidecar_map_smoke_20260527/` | `readiness only` / `not claimable` | no-training sidecar evidence/risk map 导出格式和 5 样本 smoke | MyEdge adaptation 结果、fixed-detector 结果、论文正收益 |
| TLVC01 后长期计划 | `docs/stage1_long_horizon_goal_after_tlvc01_20260527_cn.md` | `readiness only` / `not claimable` | 从 Stage1 direct replacement 转向 raw+sidecar adaptation 的执行计划 | 已训练、已验证、downstream 正收益 |
| 168 downstream | MyEdge Stage1 coupling run dirs | `downstream diagnostic` | fixed-detector downstream validation 核心 | 可被 502/496/2770 替代 |
| structure proxy | `stage1_myedge168_gt_edge_proxy_prescreen*`、P6/P6B、Sobel/Otsu proxy | `proxy only` | 筛查、选图和结构诊断 | ODS/OIS/AP/AC 或 downstream accuracy |
| full-pool manifests | `full_algae_dewatermark_v1*` | `readiness only` | cv2-readable full-pool candidate / qualitative engineering pool | 正式 full-pool result |
| full-pool review sheets | `metrics/manifests/full_algae_dewatermark_v1_manual_review/` | `readiness only` / `not claimable` | 人工复核入口，当前 pending | clean manifest 或人工结论 |
| Wu 2026 refs | `literature/wu2026_*`、`docs/reference_dataset_relation_audit_20260525_cn.md` | `downstream diagnostic` / `not claimable` | nearest-neighbor / overlap-risk anchor | 本项目数据 overlap 已证明 |
| registries | `metrics/experiment_registry.csv`、`metrics/candidate_registry.csv` | `paper metric` / governance source | Pxx/Dxx 生命周期唯一机器可读总账 | 第二套手写候选真相表 |
| run reports/logs | status `.md/.json`、`eval_bdry.txt`、`show.log` | `downstream diagnostic` | 可追溯结果证据 | 不需 manifest 或配置即可引用的独立事实 |
| historical assets | `results_optimized_c25`、旧 `full506`、`metrics/archive/`、`AIlog/`、`notion_mirror/` | `historical / archived` | 审计背景 | 当前正式入口 |

## 3. 固定解释规则

- `full506_final_mainline` 是 source asset path，不是 paper metric count。
- `full502_clean_v1` 和 `compare9_complete496_v1` 才是当前正式论文统计口径。
- MyEdge 168 结论只覆盖 fixed MSFI 50k、fixed DiffusionEdge baseline 50k 和 168 张带 GT split。
- Sobel/Otsu proxy、structure proxy、paired proxy 必须标注为 `diagnostic only, not downstream accuracy`。
- `candidate_rescues_legacy_but_not_near_raw`、`candidate_metric_near_raw_structure_mixed` 和 `mechanism-complete weak candidate` 不能写成完成或成功。
- 2770 full-pool readiness 不是正式 full-pool result，也不是 downstream validation。
- Wu et al. 2026 两篇论文是最近邻风险和写作边界来源；本项目与其数据、split、GT 的文件级关系仍未证明。

## 4. 论文主张使用方式

可直接写：

- Stage1 已有 formal enhancement source asset。
- `full502_clean_v1` 阶段表和 `compare9_complete496_v1` 主比较表已经形成。
- locked Stage1 `Final` 在 168 fixed-detector downstream 诊断中是 negative control。
- P12-P28/D01 是归档候选和诊断证据。
- Stage1 当前定位为 MyEdge/MSFI 的结构保持增强输入支撑。

必须带边界写：

- 外部 baseline 的优劣。
- HLRP/Histoformer 的失败现象。
- WWPF 的强基线表现。
- Pxx/D01 相对 legacy Final 的 recovery。
- 任何 168 split 的 downstream 结论。

不能写：

- Stage1 已稳定提升 downstream ODS/OIS/AP/AC。
- D01/P27 是正式成功候选。
- 2770 是正式结果。
- proxy 指标等同于 downstream accuracy。
- Wu 2026 数据集与本项目已经证明完全相同。
