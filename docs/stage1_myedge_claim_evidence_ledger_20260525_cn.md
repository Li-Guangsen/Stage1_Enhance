# Stage1Codex + MyEdgeCodex claim-to-evidence ledger

日期：2026-05-25

本文是跨 Stage1Codex 与 MyEdgeCodex 的论文主张证据总账。它只读取本地已落盘文件，不运行增强、训练、采样、`eval.py`、`show.py`、图表生成或指标重算。

## Executive Summary

- Overall status: `claim_boundaries_locked_major_experiment_claims_pending`
- No experiment executed by this script: `True`
- Claim count: `22`
- Stage1 formal stage count: `502`
- Stage1 formal comparison count: `496`
- Full image pool / default candidate / cv2-readable candidate: `2777` / `2774` / `2770`
- Manual review pending rows: `544`
- Stage1 full2770 readiness: `candidate_full2770_ready_after_explicit_approval_clean_protocol_blocked`
- MyEdge P1 readiness: `superseded_by_completed_p1`
- MyEdge P1 intake: `complete_with_report_assets`
- MyEdge MSFI stage-wise: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 P4: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 baseline P5C: `complete_with_report_assets`
- MyEdge downstream-driven Stage1 structure P6: `complete`
- MyEdge downstream-driven Stage1 structure P6 paired review: `complete`
- MyEdge generic enhancement controls P7: `complete_with_report_assets`
- MyEdge MSFI metrics: ODS `0.783527`, OIS `0.794213`, AP `0.345899`, AC `0.796846`

## Status Counts

| Write status | Count |
|---|---:|
| `allowed_fact` | 3 |
| `allowed_with_boundary` | 14 |
| `planned_only_not_claimable` | 4 |
| `readiness_only` | 1 |

## Immediate Paper-Safe Claims

- 正式 Stage1 主线、正式结果目录、full502_clean_v1 阶段表和 compare9_complete496_v1 主表已经锁定。
- Stage1 当前只能作为 MyEdge/MSFI 论文中的 structure-preserving input formation 候选支撑；P1 和两条 fixed-detector stage-wise 诊断均不支持旧 Stage1 的正向下游增益。
- Stage1 P4/P5C downstream-driven edge-preserve 变体已把旧 Final 的下游损伤基本拉回 raw 附近，并在 MSFI 与 DiffusionEdge baseline 两个固定检测器下形成 edge-safe 候选证据；P6/P6B 进一步给出结构 proxy 与逐图配对诊断，但当前不能写稳定优于 raw。
- Generic controls P7 已完成固定 MSFI 与 DiffusionEdge baseline 评测、结构 proxy 和 paired review；当前只能写成 168 张轻量 luminance-only control 诊断，不能写成 Stage1 稳定正向下游收益。
- MyEdge MSFI 当前可写 mixed metric profile：ODS/OIS 提升，AP 下降，AC 基本持平。
- MyEdge P1、DiffusionEdge baseline stage-wise、MSFI stage-wise 与 P4 诊断已完成；当前结果整体不支持旧 Stage1 正向下游收益，full2770 仍只是执行准备，不能写结果。

## Claims Waiting For Evidence

- Generic enhancement controls 的 P7 repeat/control 和 generic-vs-Stage1 对照；P6B 与 P7 paired review 已完成但只属结构 proxy 诊断。
- MSFI frequency token / spatial-frequency interaction / timestep gating 的独立有效性。
- MSFI 相比 Sobel/CIAFF-like/Fourier/attention 替换模块的优势。
- 低对比、弱边界、气泡/杂质、模糊边界子集鲁棒性。
- 效率、PR/AP trade-off、失败案例与投稿级 qualitative 图组。
- 与两篇同实验室参考论文数据集的精确关系和可投稿数据说明。

## Forbidden Wording

- Stage1 已提升 ODS/OIS/AP/AC，或 Stage1 Final 已被证明是 positive downstream enhancement。
- Stage1 full2770 已完成、reviewed clean manifest 已生成，或 2777 图像池已经是正式清洗协议。
- P6/P6B 结构 proxy 已证明 Stage1 稳定提升下游边缘检测，或可以替代 ODS/OIS/AP/AC。
- 直接运行 `python main.py` 就是正式主线。
- `MS_SSIM` / `PSNR` 表示相对增强真值的质量。
- MSFI 全面领先、SOTA、所有指标最优，或回避 AP 下降。
- HLRP / Histoformer 在一般场景中无效。
- HVDualformer / ABC-Former 是标准水下增强模型。
- `WWPF` 因输出 496 张或激进指标而可以删除。
- 机助 `machine_suggestion` 等同于人工 `reviewer_decision`。
- 两篇参考论文的数据描述可以直接照搬到本项目。

## Claim Matrix

| ID | Scope | Claim | Write status | Allowed wording | Current evidence | Missing evidence | Paper boundary | Next gate |
|---|---|---|---|---|---|---|---|---|
| C01 | Stage1 formal mainline | Stage1 当前正式主线配置和正式结果目录已经锁定。 | `allowed_fact` | 可以写：正式主线显式使用 `locked_full506_final_mainline.json`，正式结果副本位于 `full506_final_mainline`。 | `experiments/optimization_v1/configs/locked_full506_final_mainline.json`; `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline` | 无。 | 不能把默认 `python main.py` 写成正式论文主线；任何正式重跑都必须显式传锁定配置。 | 保持只读；除非另立协议，不替换正式 502/496 口径。 |
| C02 | Stage1 formal stage table | `full502_clean_v1` 阶段进度表已经完成。 | `allowed_fact` | 可以写：阶段表基于 `full502_clean_v1`，complete cases 为 `502` 张。 | `metrics/manifests/full502_clean_v1.txt`; `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502/summary.json`; `metrics/outputs/evaluate_protocol_v2/official_stage_progress_full502/mean_metrics_table.md` | 无。 | 这是 Stage1 六阶段增强指标表，不是外部方法主表，也不是带 GT 边缘检测结果。 | 用于中文主稿和证据包的正式阶段表。 |
| C03 | Stage1 formal comparison table | `compare9_complete496_v1` 九方法 complete-case 主表已经完成。 | `allowed_fact` | 可以写：外部主比较基于 `496` 张 complete-case，方法数 `9`。 | `metrics/manifests/compare9_complete496_v1.txt`; `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/summary.json`; `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/mean_metrics_table.md` | 无。 | `WWPF` 官方实现稳定输出 496 张，主表使用 complete-case；不能用各方法各自样本数均值混比。 | 用于正式外部主比较；保留全部 9 方法。 |
| C04 | Stage1 historical full506 | `full506` 只表示历史搜索与主线锁定背景。 | `allowed_with_boundary` | 可以写：历史 full506 用于参数搜索、锁定和正式结果副本背景；当前论文主表口径仍为 `full502_clean_v1` 与 `compare9_complete496_v1`。 | `docs/stage1_myedge_long_term_closure_plan_cn.md`; `paper/underwater_image_enhancement_evidence_pack_cn.md` | 无。 | 不能把 `full506` 写成当前正式阶段表或外部主表的样本口径。 | 全文搜索 `full506`，确保只作为历史背景或路径名出现。 |
| C05 | Metric interpretation | `MS_SSIM` / `PSNR` 在当前增强协议中是相对原图的结构一致性。 | `allowed_with_boundary` | 可以写：二者反映增强结果相对原始输入的结构一致性或保守相似性。 | `paper/underwater_image_enhancement_draft_cn.md`; `paper/underwater_image_enhancement_evidence_pack_cn.md`; `docs/comparison_methods_results_index_cn.md` | 无。 | 不能写成相对增强真值的质量指标，也不能用它们证明增强视觉质量真值更好。 | 继续在主稿、图注和表注中统一解释。 |
| C06 | External baseline boundaries | 外部方法的论文分类与当前协议下表现边界已经明确。 | `allowed_with_boundary` | 可以写：`WWPF` 是激进但可接受的强基线；`HLRP` / `Histoformer` 可作为当前 HAB 显微协议下失败案例或补充分析；`HVDualformer` / `ABC-Former` 是白平衡方法。 | `docs/comparison_methods_results_index_cn.md`; methods=ABC-Former, CBF, GDCP, HLRP, HVDualformer, Histoformer, Ours, SGUIE-Net, WWPF | 若写 related work 细节，仍需回到本地 Zotero/PDF 或本地文献笔记核验。 | 不能删除 `WWPF`；不能把 HLRP/Histoformer 的当前复现问题泛化为原方法无效；不能把白平衡方法写成标准水下增强模型。 | 主稿和图表计划中保持该分类。 |
| C07 | Stage1 no-GT edge proxy | Stage1 已形成无 GT 边缘结构 proxy 支撑包。 | `allowed_with_boundary` | 可以写：当前已有 Sobel/Otsu 风格的无 GT 边缘结构 proxy，可用于结构保持讨论、选图和失败案例筛查。 | `metrics/outputs/downstream_edge_validation/official_full502_mainline/stage_full502_proxy/summary.json`; `metrics/outputs/downstream_edge_validation/official_full502_mainline/compare9_complete496_proxy/summary.json` | MyEdge / DiffusionEdge 带 GT 的 ODS/OIS/AP/AC 仍缺。 | 不能把无 GT proxy 写成下游边缘检测正式指标，也不能据此声称 Stage1 已提升 ODS/OIS/AP/AC。 | 后续与 MyEdge P1 fixed-detector 结果衔接。 |
| C08 | Full algae image pool audit | 完整增强图像池已完成 manifest、decode、重复和质量审计。 | `allowed_with_boundary` | 可以写：外部完整增强图像池含 `2777` 张图像，默认候选 `2774` 张，OpenCV 可读候选 `2770` 张；当前人工复核仍 pending `544`。 | `docs/full_enhancement_dataset_inventory_cn.md`; `metrics/manifests/full_algae_dewatermark_v1_audit.json`; `metrics/manifests/full_algae_dewatermark_v1.txt`; `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt`; `metrics/manifests/full_algae_dewatermark_v1_decode_audit.summary.json` | 人工复核后的 clean manifest、split leakage guard、与两篇参考论文具体数据子集的本地重合关系仍缺。 | 不能把 2777 图像池写成已清洗正式协议、已完成增强结果或带 GT edge 数据集。 | 先完成人工复核，再决定 clean protocol 与 full-pool 长跑。 |
| C09 | Stage1 full2770 execution readiness | Stage1 2770 张 OpenCV 可读候选长跑已经完成执行准备，但未执行。 | `readiness_only` | 可以写：`cv2readable2770` candidate run 在明确授权后具备执行条件；当前 full2770 输出根不存在，intake 为 `not_started`。 | `docs/stage1_full2770_execution_readiness_20260525_cn.json`; status=`candidate_full2770_ready_after_explicit_approval_clean_protocol_blocked` | 2770 张完整增强输出、post-run intake、run report、reviewed clean protocol 仍缺。 | 不能写 full2770 已完成；不能把 candidate long run 写成 reviewed clean full-pool protocol。 | 需要明确授权后才可运行长跑；完成后先 intake 再更新状态文档。 |
| C10 | MyEdge formal MSFI result | MyEdge MSFI 50k 主结果已存在，但指标画像是 mixed profile。 | `allowed_with_boundary` | 可以写：MSFI 50k 相比 DiffusionEdge baseline 50k 在 ODS/OIS 上提升，AP 下降，AC 基本持平；MSFI ODS `0.783527` / OIS `0.794213` / AP `0.345899` / AC `0.796846`；baseline ODS `0.770521` / OIS `0.779986` / AP `0.363065` / AC `0.796900`。 | `docs/paper_assets/experiment_status.csv`; `docs/paper_assets/paper_ready_results.md` | AP trade-off 的 PR 曲线/阈值分析、效率、失败案例和更多消融仍缺。 | 不能写全面领先、SOTA、所有指标最优，也不能回避 AP 下降。 | 下一步补 PR/AP trade-off、效率、失败案例和消融。 |
| C11 | Stage1-to-MyEdge P1 status | Stage1 Final -> MyEdge fixed-detector P1 已完成执行、intake 和 report asset sync。 | `allowed_with_boundary` | 可以写：168 张 coupling manifest、Stage1 Final、GT、MSFI/baseline config template 和 baseline checkpoint 冻结记录均已核对；P1 intake 当前为 `complete_with_report_assets`。 | `docs/stage1_myedge_coupling_status_20260525_cn.json`; readiness_status=`superseded_by_completed_p1`; intake_status=`complete_with_report_assets` | stage-wise、generic enhancement controls、退化子集和形态一致性证据仍缺。 | P1 只能按 168 张 / Stage1 Final / fixed detector 解释，不能外推到 full502/full2770 或所有阶段。 | 下一步补 Stage1 stage-wise / generic enhancement controls。 |
| C12 | Stage1 downstream edge gain | Stage1 Final 当前能否作为 positive downstream edge enhancement 证据。 | `allowed_with_boundary` | 可以写：P1 fixed-detector 结果已完成，但当前不支持“Stage1 Final 提升下游边缘检测”的正向结论；Stage1 Final -> MSFI mat ODS/OIS/AP/AC = `0.588287` / `0.671357` / `0.263997` / `0.7403`；Stage1 Final -> DiffusionEdge baseline mat ODS/OIS/AP/AC = `0.530094` / `0.56791` / `0.224073` / `0.7349`；DiffusionEdge baseline stage-wise 诊断状态为 `complete_with_report_assets`，结果为 Raw ODS/OIS/AP/AC 0.770521/0.779986/0.363065/0.7969; BPH ODS/OIS/AP/AC 0.712919/0.722432/0.338546/0.7942; IMF1Ray ODS/OIS/AP/AC 0.687163/0.722376/0.355401/0.7417; RGHS ODS/OIS/AP/AC 0.612234/0.65375/0.286407/0.7519; CLAHE ODS/OIS/AP/AC 0.584453/0.665213/0.265935/0.7534; Fused ODS/OIS/AP/AC 0.629095/0.689792/0.302611/0.7539; Final ODS/OIS/AP/AC 0.530094/0.56791/0.224073/0.7349；MSFI stage-wise 诊断状态为 `complete_with_report_assets`，结果为 Raw ODS/OIS/AP/AC 0.783527/0.794213/0.345899/0.796846; BPH ODS/OIS/AP/AC 0.739237/0.752407/0.31061/0.7942; IMF1Ray ODS/OIS/AP/AC 0.731747/0.754032/0.350926/0.7573; RGHS ODS/OIS/AP/AC 0.67172/0.723929/0.296742/0.7619; CLAHE ODS/OIS/AP/AC 0.639906/0.720816/0.279873/0.775; Fused ODS/OIS/AP/AC 0.669946/0.721055/0.29117/0.7683; Final ODS/OIS/AP/AC 0.588287/0.671357/0.263997/0.7403。 | `output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524`; `output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525`; `docs/paper_assets/stage1_coupling/stagewise_baseline_p2_results_20260525.json`; `docs/paper_assets/stage1_coupling/stagewise_msfi_p3_results_20260525.json`; `docs/stage1_myedge_coupling_status_20260525_cn.json` | 还缺 generic enhancement controls、repeat/control、raw-anchor paired delta 表、退化子集与形态一致性指标。 | 不能写 Stage1 Final 或 Stage1 各阶段已提升 ODS/OIS/AP/AC；当前 P1/P2 更应写成负向/诊断性证据。 | 补 generic enhancement controls 和 P4 repeat/control，定位是否为增强分布迁移、detector-specific 问题或可稳定利用的 edge-safe 输入形成策略。 |
| C13 | Stage1 downstream-driven P4 variant | 不覆盖旧主线的 edge-preserve Stage1 变体是否已把下游损伤拉回 raw 附近。 | `allowed_with_boundary` | 可以写：P4 downstream-driven edge-preserve 诊断已完成，旧 Stage1 Final 的大幅下游损伤可通过保留 raw luminance/spatial structure 并只进行轻量 BPH color/illumination transfer 基本消除；P4 状态为 `complete_with_report_assets`，结果为 historical_raw_msfi_anchor ODS/OIS/AP/AC 0.783527/0.794213/0.345899/0.796846; edge_preserve_original_control ODS/OIS/AP/AC 0.783082/0.794168/0.337353/0.7972; edge_preserve_raw_bph_mild_v1 ODS/OIS/AP/AC 0.782743/0.793599/0.345909/0.7957; edge_preserve_raw_bph_moderate_v1 ODS/OIS/AP/AC 0.782999/0.794527/0.345952/0.7952; legacy_stage1_final_p1 ODS/OIS/AP/AC 0.588287/0.671357/0.263997/0.7403。 | `docs/paper_assets/stage1_coupling/downstream_variant_p4_results_20260525.json` | P6B paired review 已完成并补强逐图配对诊断；仍缺 repeat/control、generic enhancement controls 和更稳的 502/168 交叉解释，P5C/P6/P6B 仍不足以支撑稳定正向收益。 | 不能写 P4 稳定优于 raw；当前最强边界是 edge_preserve_raw_bph_moderate_v1 接近 historical raw anchor，并在同轮 original-control 下改善 AP/OIS 但 AC 略降。 | 先补 repeat/control 与 generic enhancement controls；成功前不启动 full2770。 |
| C13B | Stage1 downstream-driven P5C baseline-side check | 不覆盖旧主线的 edge-preserve Stage1 变体是否在第二检测器 DiffusionEdge baseline 下也接近 raw。 | `allowed_with_boundary` | 可以写：P5C baseline-side 诊断已完成，edge-preserve 方向不是 MSFI-only；P5C 状态为 `complete_with_report_assets`，结果为 historical_raw_diffusionedge_anchor ODS/OIS/AP/AC 0.770521/0.779986/0.363065/0.7969; edge_preserve_original_control ODS/OIS/AP/AC 0.77147/0.78149/0.362827/0.7934; edge_preserve_raw_bph_mild_v1 ODS/OIS/AP/AC 0.770699/0.782323/0.370985/0.7941; edge_preserve_raw_bph_moderate_v1 ODS/OIS/AP/AC 0.771168/0.782422/0.363047/0.794; legacy_stage1_final_p1 ODS/OIS/AP/AC 0.530094/0.56791/0.224073/0.7349。 | `docs/paper_assets/stage1_coupling/downstream_variant_baseline_p5c_results_20260525.json` | P6B paired review 已完成并补强逐图配对诊断；仍缺 repeat/control、generic enhancement controls 和 generic-vs-Stage1 对照，P6/P6B 仍不能替代稳定正向收益证据。 | 不能写 P5C 证明 Stage1 稳定提升下游；mild 虽有 AP/OIS 正向信号，但 AC 仍低于 raw，且只覆盖 168 张 / 固定 DiffusionEdge baseline 50k。 | 先补 repeat/control、generic enhancement controls 和结构连续性 / 背景伪边分析；成功前不启动 full2770。 |
| C13C | Stage1 downstream-driven P6 structure proxy | P4/P5C 现有 MAT 输出的结构、碎裂与伪边 proxy 诊断已经完成。 | `allowed_with_boundary` | 可以写：P6 只读已有 P4/P5C MAT 与 GT，以各 run ODS threshold 二值化并用 2px tolerance 计算结构 proxy；P6 状态为 `complete`，P6B paired review 状态为 `complete`，关键结果为 msfi_p4/historical_raw_msfi_anchor F1/precision/recall/false-edge/components/endpoints 0.8554/0.8783/0.8507/0.1217/4.2507/9.4521; msfi_p4/edge_preserve_raw_bph_moderate_v1 F1/precision/recall/false-edge/components/endpoints 0.8568/0.8851/0.8471/0.1149/3.6899/8.0349; msfi_p4/legacy_stage1_final_p1 F1/precision/recall/false-edge/components/endpoints 0.6446/0.6114/0.7669/0.3886/63.2304/100.3726; diffusionedge_baseline_p5c/historical_raw_diffusionedge_anchor F1/precision/recall/false-edge/components/endpoints 0.8491/0.8794/0.8392/0.1206/4.6940/11.3757; diffusionedge_baseline_p5c/edge_preserve_raw_bph_mild_v1 F1/precision/recall/false-edge/components/endpoints 0.8475/0.8735/0.8416/0.1265/4.5799/11.6185; diffusionedge_baseline_p5c/legacy_stage1_final_p1 F1/precision/recall/false-edge/components/endpoints 0.5522/0.4840/0.7062/0.5160/140.1426/235.1233。 | `docs/paper_assets/stage1_coupling/downstream_variant_structure_p6_metrics_20260525.json`; paired=`docs/paper_assets/stage1_coupling/downstream_variant_structure_p6_paired_review_20260525.json` | 还缺 repeat/control、generic enhancement controls、generic-vs-Stage1 对照和正式 full502/full2770 范围验证。 | P6/P6B 是 168 张 MyEdge split 上的结构诊断 proxy，不替代 ODS/OIS/AP/AC；只能支持旧 Final 伪边/碎裂严重、P4/MSFI moderate 有降低伪边与碎裂的诊断性叙述。 | 基于 P6/P6B 设计下一轮 generic controls 与 repeat/control；成功前不启动 full2770。 |
| C13D | Stage1 generic enhancement controls P7 | 两个非 BPH 的 generic luminance-only controls 已完成 168 张固定 MSFI 与 DiffusionEdge baseline 下游诊断。 | `allowed_with_boundary` | 可以写：P7 在 168 张 MyEdge split 上完成 fixed MSFI 50k 与 fixed DiffusionEdge baseline 50k 诊断；当前状态为 `complete_with_report_assets`，关键结果为 MSFI/historical_raw_msfi_anchor ODS/OIS/AP/AC 0.783527/0.794213/0.345899/0.796846; MSFI/generic_luma_clahe_mild_v1 ODS/OIS/AP/AC 0.781721/0.793016/0.345003/0.7934; MSFI/generic_luma_gamma_mild_v1 ODS/OIS/AP/AC 0.782883/0.794223/0.345982/0.7952; MSFI/legacy_stage1_final_p1 ODS/OIS/AP/AC 0.588287/0.671357/0.263997/0.7403; Baseline/historical_raw_diffusionedge_anchor ODS/OIS/AP/AC 0.770521/0.779986/0.363065/0.7969; Baseline/generic_luma_clahe_mild_v1 ODS/OIS/AP/AC 0.769295/0.784093/0.366887/0.7915; Baseline/generic_luma_gamma_mild_v1 ODS/OIS/AP/AC 0.771645/0.782024/0.371366/0.7936; Baseline/legacy_stage1_final_p1 ODS/OIS/AP/AC 0.530094/0.56791/0.224073/0.7349。 | `docs/paper_assets/stage1_coupling/generic_control_p7_msfi_preflight_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_baseline_preflight_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_msfi_results_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_baseline_results_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_structure_metrics_20260525.json`; `docs/paper_assets/stage1_coupling/generic_control_p7_structure_paired_review_20260525.json`; msfi_results=complete_with_report_assets; baseline_results=complete_with_report_assets; structure=complete; paired=complete; MSFI/historical_raw_msfi_anchor ODS/OIS/AP/AC 0.783527/0.794213/0.345899/0.796846; MSFI/generic_luma_clahe_mild_v1 ODS/OIS/AP/AC 0.781721/0.793016/0.345003/0.7934; MSFI/generic_luma_gamma_mild_v1 ODS/OIS/AP/AC 0.782883/0.794223/0.345982/0.7952; MSFI/legacy_stage1_final_p1 ODS/OIS/AP/AC 0.588287/0.671357/0.263997/0.7403; Baseline/historical_raw_diffusionedge_anchor ODS/OIS/AP/AC 0.770521/0.779986/0.363065/0.7969; Baseline/generic_luma_clahe_mild_v1 ODS/OIS/AP/AC 0.769295/0.784093/0.366887/0.7915; Baseline/generic_luma_gamma_mild_v1 ODS/OIS/AP/AC 0.771645/0.782024/0.371366/0.7936; Baseline/legacy_stage1_final_p1 ODS/OIS/AP/AC 0.530094/0.56791/0.224073/0.7349 | 仍缺 P7 repeat/control 以及 full502/full2770 范围验证；P7 结构/伪边 proxy 与 paired review 已完成但仍属诊断证据。 | P7 只支持 lightweight luminance-only control 的 168 张诊断：gamma 在 baseline 侧有小幅 ODS/OIS/AP 信号，MSFI 侧基本贴近 raw；结构 proxy 上 MSFI/gamma 有轻微信号但 baseline/gamma 仍 mixed，不能写 Stage1 全流程或稳定正向下游收益。 | 下一步优先做 P7 repeat/control；成功前不启动 full2770。 |
| C14 | MSFI component ablation | MSFI 的 frequency token、spatial-frequency interaction、timestep gating 各自有效。 | `planned_only_not_claimable` | 当前只能写成 planned ablation 或 future evidence requirement。 | `docs/research_contracts/msfi_component_ablation_v1.md` | 组件级实验结果、统一评测表、统计解释和图组缺失。 | 合同存在不等于结果完成；不能写任一组件已被独立证明有效。 | 在 MyEdge 侧完成组件消融并同步结果。 |
| C15 | MSFI replacement comparison | MSFI 优于 Sobel/CIAFF-like/Fourier/CBAM/SE/ECA/ASPP/FPN 替换模块。 | `planned_only_not_claimable` | 当前只能写成必须补齐的对标实验。 | `docs/research_contracts/msfi_replacement_module_v1.md` | 替换模块训练/评测结果缺失。 | 不能借参考论文或计划文件推断 MSFI 已优于这些模块。 | 在 MyEdge 侧完成替换模块对比，直接回应 ESWA 参考论文重合风险。 |
| C16 | Degradation subset robustness | 方法对低对比、弱边界、气泡/杂质、模糊边界等退化子集鲁棒。 | `planned_only_not_claimable` | 当前只能写成后续分层分析计划。 | `docs/research_contracts/degradation_stratified_edge_analysis_v1.md`; manual pending=`544` | 人工确认的退化子集标签、带 GT 子集 manifest、子集指标表缺失。 | 不能泛化声称复杂退化鲁棒；也不能把质量异常机助建议直接当人工标签。 | 先完成 full-pool manual review，再在 MyEdge 侧形成带 GT 子集评测。 |
| C17 | Efficiency, PR and failure cases | 论文已有投稿级效率、PR/AP trade-off、失败案例和 qualitative assets。 | `planned_only_not_claimable` | 当前只能写：Figure 1/2 与部分方法/结果资产已有，PR、效率和失败案例仍待补。 | `docs/research_contracts/paper_efficiency_pr_failure_analysis_v1.md` | Params/FLOPs/FPS/显存、PR curve、TP/FP/FN overlay、failure-case panel 缺失或未在 Stage1 侧接收。 | 不能写更快、更轻量、更可部署或已经完成 AP trade-off 解释。 | 完成 MyEdge 效率与 paper asset 合同，并同步可引用文档。 |
| C18 | Dataset relation to two Wu et al. 2026 papers | 本项目数据与两篇同实验室一区论文数据集关系已经可以写清。 | `allowed_with_boundary` | 可以写：Zotero 本地缓存已核验两篇参考论文的数据描述字段；本项目当前只能确认自身 2777/2774/2770 图像池，尚不能证明与 676/1026 子集精确重合。 | `docs/reference_dataset_relation_audit_20260525_cn.md`; `literature/wu2026_eswa_hab_edge_detection.md`; `literature/wu2026_eaai_hab_segmentation.md`; `docs/full_enhancement_dataset_inventory_cn.md` | 本项目自己的设备/倍率/物种/专家标注说明、与 676/1026 子集的文件级交集或差异证明仍缺。 | 不能照搬参考论文的数据描述，也不能把“同实验室”写成已经本地核验的同一数据划分。 | 补齐文件级清单、hash、原始采集编号、标注文件或实验室登记证明，才能声称与参考论文数据存在精确关系。 |
| C19 | Overall paper framing | 论文主线应以 MyEdge/MSFI 为核心，Stage1 是任务驱动结构保持输入支撑。 | `allowed_with_boundary` | 可以写：Stage1 提供 structure-preserving input formation 和证据支撑；主创新应落在 spatial-frequency weak-boundary diffusion 与后续 GT edge evidence。 | `docs/stage1_myedge_long_term_closure_plan_cn.md`; `docs/stage1_myedge_evidence_gap_dashboard_20260525_cn.json`; `docs/stage1_myedge_next_gate_board_20260525_cn.json` | MyEdge 消融、Stage1 P1、退化子集和效率证据仍缺。 | 不能把总论文写成简单的 Stage1 + MyEdge 流水线，也不能把 Stage1 单独包装成完整一区主创新闭环。 | 按 gate board 推进 P1、消融、替换、退化子集、效率和写作同步。 |

## How To Use

1. 写中文主稿或证据包时，先查 `allowed_fact` 与 `allowed_with_boundary` 行。
2. `readiness_only` 行只能写“准备就绪但未执行”，不能写实验结果。
3. `planned_only_not_claimable` 与 `missing` 行只能写成未来工作、待验证假设或实验计划。
4. 后续只要 MyEdge P1、MSFI 消融、full2770 或人工复核状态变化，应重新运行本脚本并同步 `research-log.md`。
