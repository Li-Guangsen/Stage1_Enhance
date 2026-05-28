# 项目执行规则（中文）

更新时间：2026-05-27

本文档用于把本项目中反复踩坑的地方沉淀成仓库内可见规则。它面向下一次接手本项目的人类或智能体，尤其是 Codex / AI。根目录 `AGENTS.md` 是短入口，本文件是完整规则来源。

核心原则很简单：智能体运行时无法在当前情境访问的内容，对它来说就等于不存在。因此，项目记忆必须写进本仓库的本地、已版本化文件里。

## 1. 可见性原则

规则：只把本仓库中的代码、Markdown、YAML、配置、manifest、结果表和可执行计划当作项目事实来源。

理由：聊天历史、Notion 在线页面、Google Docs、个人脑内记忆和网上公开泛知识，通常不会自动出现在下一次智能体上下文里。如果关键规则只停留在这些地方，下一次执行时就等于没有规则。

执行要求：

- 新任务开始后，先读本地文档，再做判断。
- 如果某个事实没有写进仓库，必须标记为“当前不可见”或“待确认”，不能当作已确认事实。
- Notion 镜像可以作为本地辅助材料读 `notion_mirror/`，但在线 Notion 不是默认可见事实。
- 网上公开内容不能替代本仓库当前正式口径。

## 2. 文档入口规则

规则：不同任务必须先读对应入口文档，不允许跳过交接文档直接改代码、写论文或重跑实验。

理由：本项目已经不是早期探索仓库，而是“论文底稿 + 正式结果入口 + 后续下游衔接工作台”。直接凭文件名或旧经验推进，很容易把历史口径写成正式口径。

每次任务的最低阅读顺序：

1. `AGENTS.md`
2. `README.md`
3. `docs/project_execution_rules_cn.md`
4. `docs/project_handoff_guide_cn.md`
5. `docs/project_status_overview_cn.md`
6. `docs/evidence_index_cn.md`
7. `research-state.yaml`

如果任务涉及正式结果、baseline、对比方法、主表解释，必须再读：

- `docs/comparison_methods_results_index_cn.md`
- `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502/mean_metrics_table.md`
- `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/mean_metrics_table.md`

如果任务涉及论文写作，必须再读：

- `paper/underwater_image_enhancement_draft_cn.md`
- `paper/underwater_image_enhancement_evidence_pack_cn.md`
- `paper/comparison_methods_related_work_pack_cn.md`
- `method-underwater-enhancement.md`
- `method-underwater-enhancement-paper-ready.md`
- `method-figure-underwater-enhancement.md`
- `related-work-underwater-enhancement.md`

如果任务涉及实验协议或历史调参，必须再读对应实验目录下的 `protocol.md`、`analysis.md`、`selection.json` 或 `summary.json`。

## 3. 正式口径规则

规则：当前正式主线、正式样本口径和正式结果入口必须使用最新文档中的锁定口径。

理由：仓库中保留了大量历史搜索资产，包括 `pilot92`、旧 `full506`、旧 `c25`、H1/H2/H3 中间输出等。如果不先区分正式口径和历史资产，论文和实验说明会自相矛盾。

当前正式主线：

- 正式配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 正式结果副本：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 正式最终输出：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final`

当前正式评测口径：

- 阶段进度表：`full502_clean_v1`
- 阶段 manifest：`metrics/manifests/full502_clean_v1.txt`
- 阶段输出：`metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
- 外部主比较表：`compare9_complete496_v1`
- 主比较 manifest：`metrics/manifests/compare9_complete496_v1.txt`
- 主比较输出：`metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`

必须遵守：

- `full506` 只表示历史搜索与锁定背景，不再是当前论文正式主表口径。
- 当前不是“还没统一评测”，而是正式阶段表和正式 `9` 方法 complete-case 主表已经形成。
- 任何论文表述都不得把旧 `full506` 目录直接写成当前正式主表。
- `full_algae_dewatermark_v1` 是外部完整增强图像池候选清单，来源为 `D:\Desktop\去水印所有藻类图像`；当前只完成 manifest / inventory 审计，不替代 `full502_clean_v1` 或 `compare9_complete496_v1`。
- `full_algae_dewatermark_v1` 的 OpenCV decode 审计发现 4 个候选文件为 `.jpg` 扩展但 `GIF89a` 内容；后续如在完整图像池上运行 Stage1，必须先转换或排除这 4 个文件，优先使用 `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt` 做 smoke run，且输出到新目录，不得覆盖当前正式结果副本。
- 当前 `main.py` 已支持完整图像池所需的中文路径安全读写、相对路径 manifest、`.webp` 和嵌套输出。后续如果新增 full-pool 评测脚本，必须按相对路径追踪样本，不能只按 stem 合并，因为完整图像池存在重名 stem。
- `metrics/scripts/audit_image_duplicates.py` 的严格重复和近重复输出只能作为人工复核入口，不能自动作为删除、排除或改写 manifest 的依据；任何清洗决策必须另写清洗规则、清单和对 502/496 正式口径的影响。
- `metrics/scripts/audit_image_quality_outliers.py` 的质量异常输出是基于分位数的人工复核候选，不是“低质量样本已确认”或自动排除依据；正式清洗必须另有人工确认记录。
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/` 下的 review sheets 当前全部是 `pending` 人工复核入口；只有填写 `reviewer_decision`、`decision_reason`、`reviewer` 和 `review_date` 后，才能据此形成新的清洗 manifest 或 split leakage guard。
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/` 下的 P0 复核辅助包只包含 `machine_suggestion`、预览图和摘要；这些建议不是人工 `reviewer_decision`，不能直接驱动 manifest 改写、原图删除/转换、清洗清单或 split leakage guard。
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/` 下的 P1 复核辅助包同样只包含 `machine_suggestion`、预览图和摘要；P1 质量异常建议优先用于退化子集/失败案例候选，不能直接写成排除规则。
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/` 下的 P2 复核辅助包同样只包含 `machine_suggestion`、预览图和摘要；P2 质量异常建议优先用于数据覆盖、退化分层、失败案例或有效难例候选，P2 近重复建议优先用于 future split leakage guard，不能直接写成排除或删除规则。
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_dashboard_20260525.md` 和 `all_priority_review_queue.tsv` 只是 P0/P1/P2 机助建议的统一人工复核入口；`target_review_sheet` 指示人工决策应写回哪个原始 review sheet，不能把统一队列本身当作清洗结果。
- `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_template.tsv` 是待人工填写模板；只有人工填写 `*_to_apply` 字段、`apply_fullpool_manual_review_decisions.py` dry-run 无 invalid，并显式传 `--apply` 后，才允许写回原始 review sheets。未传 `--apply` 时该脚本只能生成 apply plan 和 invalid report，不能改写复核表。
- 生成任何 full-pool clean manifest、转换清单、排除清单或 split leakage guard 前，必须先运行 `metrics/scripts/validate_fullpool_manual_review.py`；当前校验状态为 `pending_manual_review`，不能派生清洗结果。
- `metrics/scripts/derive_fullpool_review_artifacts.py` 是人工复核完成后的唯一派生入口；当 review sheet 仍有 pending、invalid 或 unresolved decisions 时，它只能生成状态报告和空/部分候选表，不能生成 `reviewed_cv2_clean_manifest.txt`。当前派生状态为 `pending_manual_review`。
- Stage1 2770 张 full-pool 完整运行后，必须先运行 `metrics/scripts/intake_stage1_fullpool_run_outputs.py` 做只读接收；只有状态达到 `complete_with_log_and_run_report` 并经人工审阅后，才能把 full-pool 写成完整扩展增强资产。当前 `full2770_locked_final_mainline_intake_status_20260525` 状态是 `not_started`，不能写成已完成。
- `docs/stage1_myedge_coupling_status_20260525_cn.md` 是 Stage1 侧从 MyEdgeCodex planning / intake 文件只读同步的状态快照；当前 P1、P2、P3、P4、P5C 与 P6 已陆续完成或同步，但都只能按各自边界解释，不能据此写 Stage1 已稳定提升 ODS/OIS/AP/AC、pseudo-edge suppression 或 morphology consistency。

## 4. 写作语言规则

规则：当前写作默认中文主稿优先。

理由：仓库已经明确当前写作与结果收口的语言重心是中文主稿。此前根目录写作草稿混入过大量英文说明，导致“文档是否应中文”这个规则没有被执行到位。

执行要求：

- 新增项目文档、执行规则、状态总结和论文底稿，默认写中文。
- 英文只保留在论文题名、方法名、缩写、原论文标题、路径、代码符号，以及明确标注的英文辅助稿中。
- 不要把英文 outline 或英文 skeleton 当作当前主稿。
- 如果生成双语内容，必须明确标注哪部分是中文主稿，哪部分是英文辅助。

## 5. 实验执行规则

规则：正式增强和正式评测必须显式使用锁定配置，并优先做 smoke，再做全量。

理由：`main.py` 默认参数不是当前正式论文主线。正式评测脚本会覆盖正式输出目录，直接全量重跑风险较高。

执行要求：

- 正式跑图必须显式传：
  `--params-json experiments\optimization_v1\configs\locked_full506_final_mainline.json`
- 不要把 `python main.py` 默认运行结果当作正式主线。
- 如果只是确认流程是否通，优先使用 1 张图 smoke。
- full-pool 长跑建议使用 `experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1`，该入口默认 `--skip-existing` 并写日志；运行结束后必须使用 `metrics/scripts/intake_stage1_fullpool_run_outputs.py` 生成接收报告。
- 正式评测脚本 `metrics/scripts/run_official_evaluations.ps1` 会覆盖：
  - `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502`
  - `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496`
- 重跑 `official_compare9_complete496` 依赖外部方法结果目录，这些目录目前是当前工作站上的绝对路径资产，不随仓库分发。
- 当前正式增强与评测环境是 `D:\Desktop\EdgeDetection\my_env`，但该环境说明不自动覆盖所有历史脚本、图表脚本和外部方法源码。
- 如果 Stage1 任务需要调用 MyEdge 的 WSL 评测命令，不要把复杂 Bash 写进 PowerShell 双引号 `$cmd` 再执行 `wsl bash -lc "$cmd"`。PowerShell 会在进入 WSL 前提前展开 Bash 的 `$run`、`$root`、`$PY`、`${run}` 等变量，造成空变量、空日志路径或 `command not found`。简单 WSL 命令用单引号 `wsl bash -lc 'cd /mnt/d/Desktop/MyEdgeCodex/eval-edge-py && ...'`；多 run、数组或循环必须写成 `.sh` 脚本再用 `wsl bash script.sh` 执行。

## 6. 论文解释规则

规则：实验指标、外部方法和负面结论必须按当前 HAB 显微图像协议限定解释。

理由：当前结果支持论文主线，但仍有边界。过度声称会直接损害稿件可信度。

必须遵守：

- `MS_SSIM` 和 `PSNR` 解释为增强结果相对原图的结构一致性，不是相对增强真值的质量指标。
- 内部 composite score 只作为调参与筛选工具，不作为论文主结果指标。
- 不写“全面领先外部 SOTA”。
- 不写“所有指标最优”。
- 不把“边缘友好”写成已经完成大规模下游任务闭环；当前仍缺与正式主线严格对齐的下游边缘验证总表。
- 不因为 `WWPF` 在部分无参考指标上高于本文方法就将其删除；必须保留并说明其 496 张实现边界。
- `HLRP` 与 `Histoformer` 可以作为当前 HAB 显微协议下的失败案例或补充分析，但不能写成对原论文方法在一般水下场景中普遍无效。
- `HVDualformer` 与 `ABC-Former` 是白平衡方法，related work 中不能混写成标准水下增强模型。

## 7. 方法命名规则

规则：论文中必须按真实职责描述各阶段，不能只沿用历史阶段名。

理由：`RGHS` 和 `CLAHE` 是代码、配置和结果目录中的历史名。如果直接写成标准算法名，会让审稿人误判为简单拼接现成模块。

当前阶段职责：

| 阶段 | 论文中的真实职责 |
| --- | --- |
| `BPH` | 灰像素引导的前置白平衡 |
| `IMF1Ray` | IMF1-Rayleigh 高频细节分支 |
| `RGHS` | 白平衡安全对比分支 |
| `CLAHE` | CLAHE 引导的局部可见性分支 |
| `Fused` | 特征门控的三分支亮度结构融合 |
| `Final` | 轻量照明与对比收口 |

必须遵守：

- 不把 `RGHS` 写成标准现成 RGHS 模块。
- 不把 `CLAHE` 写成直接输出普通 CLAHE 图像。
- 不把 `Final` 收口层写成主要创新点。
- 方法创新更适合写成“职责化分支设计 + 特征门控融合 + 面向结构可读性的设计动机”。

## 8. 多代理使用规则

规则：对于长上下文、跨目录、跨结果表或需要独立复核的复杂任务，可以使用主代理 + 子代理模式；实际启动子代理前必须有用户明确授权或当前系统级工具说明明确允许。

理由：本项目文档入口多、历史资产多、正式口径严格。把所有阅读、核对和复核都压进主代理上下文，容易造成上下文膨胀和口径混乱。OpenAI Codex 官方文档也说明，即便有大上下文窗口，主线程被大量中间输出、日志和探索笔记污染后，可靠性会下降；子代理适合把噪声工作移出主线程，但不能替代主代理的最终判断。

官方配置依据（2026-04-26 查阅 OpenAI Codex 官方文档）：

- Codex 子代理默认可用，但只会在明确要求时启动。
- 子代理会消耗额外 token，不应把简单任务拆成多代理任务。
- 全局子代理配置位于 Codex 配置的 `[agents]`。
- `agents.max_threads` 控制并发打开的 agent thread 数，官方默认值为 `6`。
- `agents.max_depth` 控制派生嵌套深度，官方默认值为 `1`，根会话从深度 `0` 开始；默认允许直接子代理，但阻止更深层递归派生。
- 提高 `agents.max_depth` 会增加 token、延迟、本地资源消耗和调度不可预测性，因此本项目默认不提高。

执行要求：

- 主代理必须先读取本任务对应的入口文档，再决定是否拆分子任务。
- 主代理负责拆分任务、限定正式口径、说明输入输出边界、汇总子代理结论并做最终验收。
- 子代理只处理边界清晰的局部任务，例如读取指定文件、核对指定结果表、检查特定目录、抽查样本或做独立复核。
- 子代理任务说明必须写清楚可读范围、不可修改文件、不可运行正式全量实验、不可自行改变论文口径或项目状态。
- 子代理输出只能作为当前任务的辅助结论，必须由主代理回到仓库文件和正式规则中复核后再采用。
- 不得把子代理聊天历史、个人记忆、在线 Notion、网页泛知识或未落盘内容当作项目事实。
- 涉及文件修改、实验运行、正式结果覆盖、论文口径变更或状态文档维护时，主代理仍是唯一负责最终动作和最终说明的执行者。
- 如果子代理发现需要改变项目状态的事项，主代理必须按状态维护规则同步对应文档和 `research-log.md`。

数量与深度控制：

- 默认每轮使用 `1-3` 个直接子代理，优先拆给 `explorer` 做只读核对。
- 只有当用户明确要求大规模并行复核，或任务天然分成 `4-6` 个互不依赖的独立问题时，才可以扩展到最多 `6` 个直接子代理。
- 超过 `6` 个独立问题时，必须分批执行，先等待、汇总并关闭上一批，再决定是否启动下一批。
- 子代理深度默认保持 `1`：主代理可以派生直接子代理，子代理不得继续派生孙代理。
- 不得为了“更彻底”而提高 `agents.max_depth`。如确需递归派生，必须先得到用户明确确认，并在完成后追加 `research-log.md` 说明原因、风险和结果。
- 对本项目推荐的 Codex 配置约束是：`[agents] max_threads <= 6`，`max_depth = 1`。如果将来新增项目级 `.codex/config.toml`，不得把这两个限制放宽为默认行为。
- 多个子代理的写入范围必须互斥；如果无法保证互斥，只能使用只读 `explorer` 或由主代理本地完成写入。

适用场景：

- 长任务预计会读取大量论文草稿、结果表、配置和日志时。
- 需要同时核对多个目录、多个方法结果或多个写作资产时。
- 需要让一个子代理独立复核主代理初步判断时。
- 需要控制主代理上下文长度，把局部证据采集与最终口径判断分离时。

不适用场景：

- 简单问答、单文件小改或可由主代理直接完成的短任务。
- 需要连续调试同一段代码且上下文强耦合的任务。
- 涉及高风险写入、删除、覆盖正式结果或全量实验运行的动作本身。
- 用户没有明确要求或授权使用多代理，而当前系统级工具说明也不允许主动派生子代理时。

## 9. 状态维护规则

规则：任何改变项目状态的工作完成后，必须同步更新对应文档和日志。

理由：如果只改代码、只改论文或只在聊天里说明，下次智能体接手时仍然不可见。此前 `research-log.md` 曾停在 2026-04-17，后续进展分散到其他文档里，就是典型踩坑。

执行要求：

- `research-log.md` 只追加，不回写历史条目。
- 改变正式主线、正式结果、正式口径时，必须同步检查：
  - `README.md`
  - `research-state.yaml`
  - `docs/project_handoff_guide_cn.md`
  - `docs/project_status_overview_cn.md`
  - `docs/comparison_methods_results_index_cn.md`
- 改变论文写作资产时，必须同步检查相关根目录草稿和 `paper/` 中文主稿/证据包。
- 新增实验、重跑结果或改变口径时，必须留下可追溯的配置、manifest、输出目录和日志记录。

## 10. 防踩坑规则

规则：如果发现 AI 执行不顺手，任务结束时要把问题转成执行规则。

理由：智能体不会天然继承上一次踩坑经验。只有把经验写进仓库，下次才有机会被读取。

执行要求：

- 把“不要再这样做”改写成可执行规则。
- 优先补进 `docs/project_execution_rules_cn.md`。
- 如果是所有智能体每次都必须知道的短规则，再同步补进 `AGENTS.md`。
- 如果规则改变了项目接手方式，同步更新 `README.md` 的阅读顺序。
- 如果规则来自一次具体项目行动，同步追加 `research-log.md`。

## 11. 实验治理与候选生命周期规则

规则：Stage1 downstream-driven 实验当前进入治理与候选归档优先状态；没有 method design、run sheet、isolated output root、config、log、status 和 decision，不新增候选。

理由：P12-P28/D01 已经证明连续 `guard`、`fallback`、`raw-pullback` 和 near-raw 小候选会消耗大量时间与上下文，但不能自然形成稳定、可讲、可消融的增强方法主线。工程上必须把候选视为有生命周期的 run，而不是无边界调参。

执行要求：

- 新候选必须先使用 `docs/experiment_run_sheet_template_cn.md` 填写 run sheet。
- `experiments/` 下工作必须同时遵守 `experiments/AGENTS.override.md`。
- 每个候选都必须进入 `metrics/experiment_registry.csv` 和 `metrics/candidate_registry.csv`。
- Registry 字段和枚举必须遵守 `metrics/registry_schema_cn.md`；字段数错位时不得提交。
- `candidate_rescues_legacy_but_not_near_raw`、`candidate_metric_near_raw_structure_mixed`、`mechanism-complete weak candidate`、proxy-only 和 readiness-only 不能写成目标完成。
- D01 `d01_structure_flow_v1` 当前只能写成 `mechanism-complete weak candidate`，不是正式增强主线。
- FF01/FF02 是完整增强主线恢复轨道的诊断失败证据；FF02 已完成 detector-compatible 机制级重设计，但 gate 仍为 `candidate_rescues_legacy_but_not_near_raw`，不得继续同族 FF03 小修或写成 downstream 正收益。
- TLVC01 是 topology-locked visual-chroma 完整流程纠偏证据；它修正了 MyEdge raw input mismatch，但 gate 仍为 `candidate_rescues_legacy_but_not_near_raw`，不得继续 TLVC02/FF03/P29/D02 小修或写成 downstream 正收益。
- FA01 visual/error-map review 与 Stage1 sidecar map smoke 只能写成诊断/导出准备；它们没有训练、没有 detector adaptation、没有 fixed-detector rerun，不能写成 downstream 正收益。
- 连续两个同族候选为 mixed/weak 时，必须停止同族派生，先做 method review 或归档。
- 当前主筛选口径统一为 MyEdge 166 complete-case：从 MyEdge 168 raw split 中排除 `chazhuang.3.jpg` 与 `chazhuang.6.jpg`。后续 Stage1 candidate 的增强指标筛选和 fixed-detector downstream validation 都必须使用这 166 张；历史 168 结果只能作为历史诊断证据。502/496 只用于 Stage1 增强指标和 complete-case 对照；2770 full-pool 不能替代 downstream validation。
- 失败候选必须保留为有效证据，不删除、不覆盖、不用下一轮结果掩盖。

## 12. Codex 指令加载与命令环境规则

规则：在长任务或换 agent 前，应确认根 `AGENTS.md` 和 `experiments/AGENTS.override.md` 可被发现；命令上下文必须明确。

执行要求：

- 指令加载验证见 `docs/codex_instruction_verification_cn.md`。
- 命令环境规则见 `docs/command_environment_rules_cn.md`。
- Codex 侧文档、YAML、CSV 检查使用 `D:/Desktop/DeepLearning/my_env/python.exe`。
- 不使用裸 `python`，除非任务就是检查系统默认 Python。
- 给用户命令时必须明确 Windows PowerShell、CMD、WSL 或远程服务器。
- 多 run WSL eval/show 使用 `.sh`，不要把复杂 Bash 塞进 PowerShell 双引号 `$cmd`。
