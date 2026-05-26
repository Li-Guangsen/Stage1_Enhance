# 完整增强图像池审计（full_algae_dewatermark_v1）

更新时间：2026-05-25

## 1. 定位

`full_algae_dewatermark_v1` 是当前工作站外部完整增强图像池的候选清单与审计结果，来源为：

- `D:\Desktop\去水印所有藻类图像`

该目录当前没有复制进仓库。本轮只生成 manifest、inventory、decode / dimension 审计表、内容重复审计表和 full run 接收状态报告，没有运行 2770 张完整增强实验、没有生成新图表、没有重跑评测，也没有覆盖现有正式结果。

它的作用是为后续“完整图像池增强”和“Stage1 -> MyEdge 衔接”提供数据入口，不替代当前正式论文口径：

- 正式阶段评测仍是 `full502_clean_v1`
- 正式主比较仍是 `compare9_complete496_v1`
- `full506` 仍只表示历史搜索与锁定背景，不是当前主表口径

默认候选 manifest 只包含顶层物种/类别文件夹下的图像，排除根目录下的说明图、文本和 PDF 文件。

## 2. 审计摘要

| 项目 | 数值 |
| --- | ---: |
| 源目录总文件数 | 2785 |
| 顶层数据文件夹数 | 80 |
| 图像文件总数 | 2777 |
| 候选 manifest 图像数 | 2774 |
| OpenCV 可读候选图像数 | 2770 |
| OpenCV 解码失败候选图像数 | 4 |
| 根目录图像数（默认排除） | 3 |
| 根目录文件数（已记录） | 7 |
| 重名 stem 分组数 | 28 |
| 涉及重名 stem 的图像数 | 122 |
| 严格重复候选组数（SHA-256） | 3 |
| 严格重复候选图像数 | 6 |
| 近重复候选对数（pHash<=4 且 dHash<=8） | 30 |
| 质量异常人工复核候选数（2% 分位阈值并集） | 507 |
| 0 字节图像 | 0 |
| 小于 1KB 图像 | 0 |

图像扩展名分布：

| 扩展名 | 数量 |
| --- | ---: |
| `.jpg` | 2512 |
| `.png` | 217 |
| `.jpeg` | 34 |
| `.webp` | 14 |

根目录文件记录：

| 文件 | 说明 |
| --- | --- |
| `000-赤潮爆发.jpg` | 根目录说明图，默认不进候选 manifest |
| `000-赤潮藻爆发海岸.jpg` | 根目录说明图，默认不进候选 manifest |
| `000-样本采集.jpg` | 根目录说明图，默认不进候选 manifest |
| `000-ReadMe.txt` | 根目录说明文件 |
| `图像增强数据集.txt` | 根目录说明文件 |
| `藻类-保存观察.pdf` | 根目录 PDF |
| `中国海洋浮游植物和赤潮物种的生物多样性研究进展-东海.pdf` | 根目录 PDF |

## 3. 已生成资产

| 资产 | 含义 |
| --- | --- |
| `metrics/manifests/full_algae_dewatermark_v1.txt` | 默认候选 manifest，2774 张顶层文件夹内图像 |
| `metrics/manifests/full_algae_dewatermark_v1_inventory.tsv` | 全量图像 inventory，2777 行 |
| `metrics/manifests/full_algae_dewatermark_v1_folder_counts.tsv` | 80 个顶层文件夹的图像数 |
| `metrics/manifests/full_algae_dewatermark_v1_root_files.tsv` | 7 个根目录文件记录 |
| `metrics/manifests/full_algae_dewatermark_v1_audit.json` | 机器可读审计摘要 |
| `metrics/manifests/full_algae_dewatermark_v1_decode_audit.tsv` | 2777 张图像逐图 OpenCV 解码、尺寸、通道和 dtype 审计 |
| `metrics/manifests/full_algae_dewatermark_v1_decode_audit.summary.json` | 机器可读 decode / dimension 审计摘要 |
| `metrics/manifests/full_algae_dewatermark_v1_decode_audit.summary.md` | 人类可读 decode / dimension 审计摘要 |
| `metrics/manifests/full_algae_dewatermark_v1_decode_audit_folder_summary.tsv` | 80 个顶层文件夹的 decode 和主尺寸摘要 |
| `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt` | OpenCV 可读的候选 manifest，2770 张 |
| `metrics/manifests/full_algae_dewatermark_v1_decode_failures.tsv` | 4 个 OpenCV 解码失败候选文件 |
| `metrics/scripts/audit_image_duplicates.py` | 完整图像池严格重复 / 近重复候选只读审计脚本 |
| `metrics/manifests/full_algae_dewatermark_v1_duplicate_audit.tsv` | 2777 张逐图 SHA-256、灰度图 hash、aHash/dHash/pHash 审计 |
| `metrics/manifests/full_algae_dewatermark_v1_duplicate_audit.summary.md` | 人类可读重复 / 近重复审计摘要 |
| `metrics/manifests/full_algae_dewatermark_v1_duplicate_audit.summary.json` | 机器可读重复 / 近重复审计摘要 |
| `metrics/manifests/full_algae_dewatermark_v1_duplicate_audit_exact_duplicate_groups.tsv` | 严格重复候选组 |
| `metrics/manifests/full_algae_dewatermark_v1_duplicate_audit_near_duplicate_pairs.tsv` | 近重复候选图像对，需人工复核 |
| `metrics/scripts/audit_image_quality_outliers.py` | 完整图像池质量异常候选只读审计脚本 |
| `metrics/manifests/full_algae_dewatermark_v1_quality_audit.tsv` | 2777 张逐图亮度、对比、饱和度、模糊度、尺寸和熵统计 |
| `metrics/manifests/full_algae_dewatermark_v1_quality_audit.summary.md` | 人类可读质量异常审计摘要 |
| `metrics/manifests/full_algae_dewatermark_v1_quality_audit.summary.json` | 机器可读质量异常审计摘要 |
| `metrics/manifests/full_algae_dewatermark_v1_quality_audit_outliers.tsv` | 基于分位阈值的质量异常人工复核候选 |
| `metrics/scripts/build_fullpool_manual_review_sheets.py` | 从解码失败、重复、近重复和质量异常审计结果生成统一人工复核表 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_index.md` | 人工复核入口摘要，当前 `544` 条均为 `pending` |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/all_manual_review_issues.tsv` | 统一人工复核表，覆盖 4 类问题 |
| `metrics/scripts/validate_fullpool_manual_review.py` | 人工复核表字段完整性和合法性校验脚本 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_validation_status_20260525.md` | 当前人工复核校验报告，状态为 `pending_manual_review` |
| `metrics/scripts/build_fullpool_p0_review_pack.py` | 生成 P0 复核辅助包的脚本，只产生机助建议和预览图 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_review_pack_summary.md` | P0 复核辅助包摘要，状态为 `recommendations_only_pending_manual_review` |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_review_recommendations.tsv` | P0 机助建议表，7 行，`machine_suggestion` 不是人工决策 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_contact_sheet.png` | P0 decode failures 和 exact duplicate groups 的联系图 |
| `metrics/scripts/build_fullpool_p1_review_pack.py` | 生成 P1 复核辅助包的脚本，只产生机助建议和预览图 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_review_pack_summary.md` | P1 复核辅助包摘要，状态为 `recommendations_only_pending_manual_review` |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_review_recommendations.tsv` | P1 机助建议表，134 行，`machine_suggestion` 不是人工决策 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_near_duplicate_contact_sheet.png` | P1 近重复强候选联系图 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_quality_contact_sheet_001.png` | P1 质量异常候选联系图，分片 1 |
| `metrics/scripts/build_fullpool_p2_review_pack.py` | 生成 P2 复核辅助包的脚本，只产生机助建议和预览图 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_review_pack_summary.md` | P2 复核辅助包摘要，状态为 `recommendations_only_pending_manual_review` |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_review_recommendations.tsv` | P2 机助建议表，403 行，`machine_suggestion` 不是人工决策 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_near_duplicate_contact_sheet.png` | P2 近重复候选联系图 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_quality_contact_sheet_001.png` | P2 质量异常候选联系图，分片 1 |
| `metrics/scripts/build_fullpool_manual_review_dashboard.py` | 整合 P0/P1/P2 复核建议并生成统一人工复核队列的脚本 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_dashboard_20260525.md` | 统一人工复核 dashboard，状态为 `ready_pending_manual_review` |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/all_priority_review_queue.tsv` | P0/P1/P2 统一人工复核队列，544 行 |
| `metrics/scripts/build_fullpool_manual_review_decision_template.py` | 从统一复核队列生成待人工填写决策模板的脚本 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_template.tsv` | 人工决策填写模板，544 行，当前未填写 |
| `metrics/scripts/apply_fullpool_manual_review_decisions.py` | dry-run 校验并可在显式 `--apply` 时写回人工决策的脚本 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_apply_report_20260525.md` | 当前决策回写 dry-run 报告，状态为 `no_decisions_to_apply` |
| `metrics/scripts/derive_fullpool_review_artifacts.py` | 仅基于已验证人工决策派生转换、排除、去重和 split guard 清单的脚本 |
| `metrics/manifests/full_algae_dewatermark_v1_manual_review/derived_review_artifacts/review_artifacts_status_20260525.md` | 当前人工复核派生状态，`pending_manual_review`，未生成 clean manifest |
| `docs/full_enhancement_dataset_manual_review_protocol_cn.md` | 人工复核协议文档 |
| `metrics/scripts/intake_stage1_fullpool_run_outputs.py` | 2770 张 full run 的只读接收脚本 |
| `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline_intake_status_20260525.md` | 当前 full run 接收状态报告，状态为 `not_started` |

这些资产是“数据审计与接收准备资产”，不是 2770 张完整增强实验结果。

## 4. Decode / dimension 审计结论

本轮使用 `metrics/scripts/audit_image_manifest_decode.py` 对 inventory 中的 2777 张图像做 OpenCV 解码审计。该审计与当前 Stage1 主流程一致，因为 `main.py` 和正式评测脚本都依赖 OpenCV 读图。

| 范围 | 行数 | OpenCV 可读 | 解码失败 | 缺失文件 | 宽度范围 | 高度范围 |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| 全量图像 | 2777 | 2773 | 4 | 0 | 67-4096 | 54-4096 |
| 默认候选图像 | 2774 | 2770 | 4 | 0 | 67-4096 | 54-4096 |
| 根目录说明图 | 3 | 3 | 0 | 0 | 1144-1144 | 856-856 |

默认候选图像的通道和类型分布：

- `3` 通道：2514 张。
- `4` 通道：256 张。
- dtype：2770 张均为 `uint8`。
- 最常见尺寸：`450x450x3`，781 张。

4 个 OpenCV 解码失败文件都带 `.jpg` 扩展，但字节头是 `GIF89a`。Pillow 可以识别它们为 GIF，但当前 Stage1 主流程的 OpenCV 读取路径不能直接处理它们：

| 文件 | 内容签名 | 当前处理建议 |
| --- | --- | --- |
| `46、Coscinodiscus asteromphalus-星脐圆筛藻-新补充-细胞表面排列规整-有中心但不是蛋白核/coscinodiscusasteromphalus_akw.jpg` | `GIF89a` | full-pool OpenCV run 前排除或转换 |
| `47、Coscinodiscus radiatus-辐射圆筛藻 -新补充-细胞表面排列不规整-有中心但不是蛋白核/coscinodiscusradiatus_akw.jpg` | `GIF89a` | full-pool OpenCV run 前排除或转换 |
| `55、Paralia sulcata-具槽帕拉藻/paraliasulcata_akw.jpg` | `GIF89a` | full-pool OpenCV run 前排除或转换 |
| `8-5、Protoperidinium bipes-双刺原多甲藻-新补充/protoperidiniumbipes_akw.jpg` | `GIF89a` | full-pool OpenCV run 前排除或转换 |

因此，后续如果直接使用当前 Stage1 / OpenCV 流程，安全 smoke 入口应优先使用：

- `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt`

同时，`main.py` 已做向后兼容的完整图像池 I/O 修正：

- 使用 `np.fromfile + cv2.imdecode` 安全读取中文路径。
- 使用 `cv2.imencode + tofile` 安全写入中文路径。
- manifest 支持带空格、`#` 和子目录的相对路径。
- 新增 `.webp` 输入扩展支持。
- 当输入是子目录相对路径时，输出保留子目录结构，避免重名 stem 覆盖。

已完成静态验证：

- `full502_clean_v1` 仍解析为 502 张，平铺输出路径保持 `results/png/Final/<stem>_Final.png`。
- `full_algae_dewatermark_v1_cv2_readable_candidate.txt` 解析为 2770 张，首张中文路径图像可被新读图函数读取。
- Stage1 full-pool 1 张和 10 张 smoke 已完成，输出见 `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/smoke_summary.md`。
- 2770 张 full run 预算已形成，见 `experiments/full-algae-dewatermark-v1/run_budget_estimate.md`；当前估算耗时约 46-60 小时，六阶段 JPG/PNG 输出约 3.04 GiB。
- `experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1` 已补充运行日志，未来日志路径为 `experiments/full-algae-dewatermark-v1/outputs/cv2readable2770/runs/full2770_locked_final_mainline/logs/full2770_locked_final_mainline.log`。
- `metrics/scripts/intake_stage1_fullpool_run_outputs.py` 已生成当前接收报告；状态为 `not_started`，输出根目录不存在，预期 `33240` 个输出文件中当前存在 `0` 个。

## 5. 内容重复 / 近重复审计结论

本轮使用 `metrics/scripts/audit_image_duplicates.py` 对 inventory 中的 2777 张图像做只读内容审计。该审计不改变 manifest，也不删除或转换任何图像。

审计口径：

- 严格重复：文件级 SHA-256 完全一致。
- 灰度图重复：解码并转为灰度后的像素 SHA-256 完全一致。
- 近重复候选：`pHash` 汉明距离 `<=4` 且 `dHash` 汉明距离 `<=8`。

审计结果：

| 项目 | 数值 |
| --- | ---: |
| 审计图像行数 | 2777 |
| 候选图像行数 | 2774 |
| hash 可读图像数 | 2777 |
| OpenCV 解码图像数 | 2773 |
| Pillow fallback 解码图像数 | 4 |
| 严格文件重复组数 | 3 |
| 严格文件重复图像数 | 6 |
| 灰度图重复组数 | 3 |
| 灰度图重复图像数 | 6 |
| 近重复候选对数 | 30 |

3 组严格重复候选为：

| 组 | 图像 |
| --- | --- |
| `file_sha256_0001` | `3、Amphidinium carterae Hulburt-强壮前沟藻/CCMP124_algae_01.jpg` 与 `3、Amphidinium carterae Hulburt-强壮前沟藻/CCMP124_algae_02.jpg` |
| `file_sha256_0002` | `8-1、Gonyaulax verior-春膝沟藻-补充新/large.jpg` 与 `8、Gonyaulax spinifera-具刺膝沟藻/large.jpg` |
| `file_sha256_0003` | `24、Chaetoceros affinis-窄隙角毛藻/franz_neidl_imgp3353_6_chaetoceros_affinis_060210_20100328223743_small.jpg` 与 `24、Chaetoceros affinis-窄隙角毛藻/franz_neidl_imgp3353_6_chaetoceros_affinis_060210_201003282237434_small.jpg` |

边界：

- 近重复候选是人工复核入口，不是自动清洗规则。
- 严格重复候选也不能直接删除；是否去重取决于后续论文数据协议、类别标签和训练/测试划分需求。
- 这次审计不改变 `full502_clean_v1`、`compare9_complete496_v1` 或 2770 张 OpenCV 可读候选 manifest。

## 6. 质量异常审计结论

本轮使用 `metrics/scripts/audit_image_quality_outliers.py` 对 inventory 中的 2777 张图像做只读质量统计，计算亮度、对比、饱和度、Laplacian 清晰度、Tenengrad 边缘能量、尺寸、长宽比和灰度熵。

审计口径：

- 阈值基于候选图像的 `2%` / `98%` 分位数。
- 输出的是人工复核候选，不是自动排除清单。
- 该审计不改变任何 manifest 或正式结果目录。

审计结果：

| 项目 | 数值 |
| --- | ---: |
| 审计图像行数 | 2777 |
| 候选图像行数 | 2774 |
| 质量统计可读图像数 | 2777 |
| OpenCV 解码图像数 | 2773 |
| Pillow fallback 解码图像数 | 4 |
| 质量异常人工复核候选数 | 507 |

主要异常标记计数：

| 标记 | 数量 |
| --- | ---: |
| `low_luminance` | 56 |
| `high_luminance` | 56 |
| `low_contrast` | 56 |
| `low_laplacian_sharpness` | 56 |
| `low_tenengrad_edges` | 56 |
| `low_saturation` | 56 |
| `high_saturation` | 56 |
| `small_resolution` | 56 |
| `large_resolution` | 62 |
| `low_aspect_ratio` | 56 |
| `high_aspect_ratio` | 56 |

边界：

- `507` 是多个异常标记的并集，不表示 507 张都应排除。
- 低清晰度、低对比或高饱和样本可能正是退化 HAB 显微图像的任务难例；后续更适合先做人工标签或分层评测，而不是直接删除。
- 如果未来做训练/测试划分，质量异常标签可用于分层抽样和失败案例分析。

## 7. 人工复核入口

本轮使用 `metrics/scripts/build_fullpool_manual_review_sheets.py` 将审计结果整理为可填写的人工复核 sheets：

| Sheet | 行数 | 用途 |
| --- | ---: | --- |
| `decode_failures_review.tsv` | 4 | 决定 4 个 `GIF89a` 内容文件是转换、排除还是保留为外部资产 |
| `exact_duplicates_review.tsv` | 3 | 复核严格重复组，决定保留、去重或仅做划分防泄漏 |
| `near_duplicates_review.tsv` | 30 | 复核近重复候选对，决定是否重复或仅做划分防泄漏 |
| `quality_outliers_review.tsv` | 507 | 复核质量异常候选，标注有效退化样本、失败案例候选或清洗排除候选 |
| `all_manual_review_issues.tsv` | 544 | 统一复核表，汇总以上 4 类问题 |

所有 review 行当前均为 `review_status=pending`。填写 `reviewer_decision` 前，不得修改 manifest、不得删除或转换原图。任何清洗决策都需要保留 `decision_reason`、`reviewer` 和 `review_date`。

当前使用 `metrics/scripts/validate_fullpool_manual_review.py` 完成字段校验：

- `overall_status = pending_manual_review`
- `pending_rows = 544`
- `reviewed_rows = 0`
- `needs_followup_rows = 0`
- `invalid_rows = 0`

协议文档见 `docs/full_enhancement_dataset_manual_review_protocol_cn.md`。

为降低 P0 人工复核成本，当前已生成 P0 复核辅助包：

- 脚本：`metrics/scripts/build_fullpool_p0_review_pack.py`
- 摘要：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_review_pack_summary.md`
- 机助建议：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_review_recommendations.tsv`
- 联系图：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/p0_contact_sheet.png`

该辅助包覆盖 `7` 条 P0 行：4 个 decode failures 和 3 个 exact duplicate groups。当前状态是 `recommendations_only_pending_manual_review`。其中 `machine_suggestion` 只是复核建议，不是 `reviewer_decision`；不得根据该表直接修改 manifest、删除原图、转换原图或生成 split leakage guard。

当前也已生成 P1 复核辅助包：

- 脚本：`metrics/scripts/build_fullpool_p1_review_pack.py`
- 摘要：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_review_pack_summary.md`
- 机助建议：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_review_recommendations.tsv`
- 联系图：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/p1_near_duplicate_contact_sheet.png` 和 `p1_quality_contact_sheet_*.png`

该辅助包覆盖 `134` 条 P1 行：9 条近重复强候选和 125 条质量异常关键候选。当前状态是 `recommendations_only_pending_manual_review`。其中质量异常样本的机助建议主要是 `subset_label_only`，意图是优先服务退化分层、失败案例和后续边缘任务分析；不得把这些建议直接写成排除规则。

当前也已生成 P2 复核辅助包：

- 脚本：`metrics/scripts/build_fullpool_p2_review_pack.py`
- 摘要：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_review_pack_summary.md`
- 机助建议：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_review_recommendations.tsv`
- 联系图：`metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/p2_near_duplicate_contact_sheet.png` 和 `p2_quality_contact_sheet_*.png`

该辅助包覆盖 `403` 条 P2 行：21 条近重复候选和 382 条质量异常候选。当前状态是 `recommendations_only_pending_manual_review`。其中质量异常样本的机助建议主要是 `subset_label_only`，意图是优先服务数据覆盖说明、退化分层、失败案例和有效难例筛选；近重复建议主要用于未来 split leakage guard，不得把这些建议直接写成删除或排除规则。

当前还生成了统一人工复核 dashboard：

- 脚本：`metrics/scripts/build_fullpool_manual_review_dashboard.py`
- dashboard：`metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_dashboard_20260525.md`
- 统一队列：`metrics/manifests/full_algae_dewatermark_v1_manual_review/all_priority_review_queue.tsv`

该 dashboard 将 P0/P1/P2 三层机助建议合并为 `544` 行人工复核队列，按 P0 -> P1 -> P2 排序，并为每行记录目标 review sheet、预览图路径和 `machine_suggestion`。当前队列状态是 `ready_pending_manual_review`，仍不能替代人工 `reviewer_decision`。

当前还生成了人工决策填写模板和 dry-run 回写报告：

- 模板脚本：`metrics/scripts/build_fullpool_manual_review_decision_template.py`
- 决策模板：`metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_template.tsv`
- 回写脚本：`metrics/scripts/apply_fullpool_manual_review_decisions.py`
- dry-run 报告：`metrics/manifests/full_algae_dewatermark_v1_manual_review/manual_review_decision_apply_report_20260525.md`

该模板包含 `544` 行，与统一队列一一对应。当前模板尚未填写，dry-run 状态为 `no_decisions_to_apply`，说明没有任何人工决策被写回 review sheets。后续只有在模板通过 dry-run 且显式传 `--apply` 时，回写脚本才会更新原始 review sheets；写回后仍必须重新运行人工复核校验和派生脚本。

当前还新增了人工复核派生脚本：

- 脚本：`metrics/scripts/derive_fullpool_review_artifacts.py`
- 当前状态：`metrics/manifests/full_algae_dewatermark_v1_manual_review/derived_review_artifacts/review_artifacts_status_20260525.md`

该脚本只在人工复核字段完整、无 invalid、无 pending 且无 unresolved decision 时，才会生成 `reviewed_cv2_clean_manifest.txt`。当前 544 行仍全部 pending，因此派生状态为 `pending_manual_review`、`can_generate_clean_manifest=False`，只生成空的转换/排除/去重/split guard 候选表和状态报告，没有生成 clean manifest。

## 8. 与当前正式口径的关系

当前仓库内同时存在四类口径：

| 口径 | 数量 | 当前角色 |
| --- | ---: | --- |
| `full_algae_dewatermark_v1` | 2774 候选 / 2777 图像总数 | 完整增强图像池候选清单，基础审计完成，尚未成为正式评测协议 |
| `full_algae_dewatermark_v1_cv2_readable_candidate` | 2770 | OpenCV 可读候选清单，可作为后续 Stage1 full-pool run 的安全入口；当前 full2770 接收状态为 `not_started` |
| `full502_clean_v1` | 502 | 当前正式阶段评测口径 |
| `compare9_complete496_v1` | 496 | 当前正式 `Ours + 8 baselines` 主比较口径 |

因此，后续写作和实验不能直接把 `2774/2777` 写成已经完成的正式结果。它目前只能写成“发现并审计出的更大候选图像池”。

## 9. 与两篇同方向参考论文的数据描述关系

根据本地 Zotero 条目、Zotero 本地全文缓存和已落库文献笔记，两个同方向核心参考的可借鉴点是“数据描述结构”，不是未经核验的数值照搬。结构化审计见 `docs/reference_dataset_relation_audit_20260525_cn.md`。

### ESWA 2026 HAB 边缘检测论文

- 论文：`Enhanced edge detection of harmful algal Blooms using diffusion probability models and Sobel-convolutional attention mechanisms`
- 期刊：`Expert Systems with Applications 298:129663`
- DOI：`10.1016/j.eswa.2025.129663`
- 数据描述：来自中国海洋大学 Applied Microalgal Biology Laboratory 的 HAB 显微图像；676 张高分辨率显微图像；36 个 HAB 物种；按物种层面 70/30 划分为 473 张训练、203 张测试；使用 LabelMe 标注边缘 GT，并由海洋生物专家交叉核验。

### EAAI 2026 HAB 分割论文

- 论文：`Microscopic image segmentation of harmful algal blooms using pyramid fusion enhancement and dual-branch network`
- 期刊：`Engineering Applications of Artificial Intelligence 177:114948`
- DOI：`10.1016/j.engappai.2026.114948`
- 数据描述：来自中国海洋大学 Applied Micro-algae Biology Laboratory / AICO Lab 的 HAB 显微图像；1026 张图像；分割实验按 8:2 划分；报告分割指标、增强消融、下游分类和效率分析。

当前用户说明本项目图像与这两篇论文来自同一实验室。仓库文档中可以据此设计同样严谨的数据描述框架，但在正式论文中仍需本地证据确认以下字段后再写成 Stage1 项目事实：

- 显微镜型号、相机型号、倍率和成像协议
- 物种数量、每类样本数、采样地点和采样时间
- 是否存在专家标注、标注软件、标注者人数和一致性流程
- 当前 2777 图像池与两篇论文 676/1026 数据子集之间的包含关系

## 10. 当前清洗策略

当前候选清单采用保守规则：

- 只纳入顶层文件夹下的图像。
- 根目录说明图不纳入默认候选 manifest。
- manifest 使用相对路径，不使用文件 stem 作为唯一 ID。
- 后续脚本不能假设文件名唯一，因为已经发现 28 组重名 stem。

已经完成的审计包括：

- 文件级 inventory。
- OpenCV 解码审计。
- 图像尺寸、通道和 dtype 统计。
- 严格重复和近重复候选审计。
- 质量异常候选审计。
- 人工复核 sheets。

尚未完成的审计包括：

- 4 个 `GIF89a` 伪 `.jpg` 文件的转换或排除决策。
- 严格重复、近重复和质量异常候选的人工复核与清洗决策。
- 失焦、污染、强遮挡等仍需人工标签。

## 11. 后续动作

在允许跑实验前，建议先完成：

1. 先参考 `metrics/manifests/full_algae_dewatermark_v1_manual_review/p0_review_pack/` 完成 P0 人工复核，并把最终人工决策写回对应 review sheets 的 `reviewer_decision`、`decision_reason`、`reviewer` 和 `review_date`。
2. 再参考 `metrics/manifests/full_algae_dewatermark_v1_manual_review/p1_review_pack/` 处理 P1 近重复强候选和质量异常关键候选；质量异常优先作为退化子集或失败案例候选确认，不应直接排除。
3. 最后参考 `metrics/manifests/full_algae_dewatermark_v1_manual_review/p2_review_pack/` 处理 P2 候选；P2 质量异常优先作为数据覆盖、退化分层、失败案例或有效难例候选，P2 近重复优先形成 split leakage guard。
4. 根据人工复核结果决定 4 个 `GIF89a` 伪 `.jpg` 文件是转换为标准 PNG/JPEG，还是从 OpenCV full-pool 协议中排除。
5. 根据人工复核结果决定严格重复、近重复和质量异常候选是保留、去重、排除，还是仅在训练/测试划分中做泄漏防护或子集标签。
6. 决定完整图像池是复制、软链接还是按外部绝对路径读取；当前 `main.py` 已支持外部中文路径，但论文/复现协议仍需写清外部资产边界。
7. 复核完成后先运行 `metrics/scripts/validate_fullpool_manual_review.py`，再运行 `metrics/scripts/derive_fullpool_review_artifacts.py`；只有派生状态允许生成 clean manifest 时，才能使用派生清单。
8. 若允许长时间增强实验，基于 `metrics/manifests/full_algae_dewatermark_v1_cv2_readable_candidate.txt` 或经复核派生的 reviewed manifest，显式使用 `experiments/optimization_v1/configs/locked_full506_final_mainline.json` 跑完整增强，输出到新的目录，不能覆盖现有正式结果；推荐入口为 `experiments/full-algae-dewatermark-v1/run_full_cv2readable2770_locked.ps1`。
9. 完整运行后先执行 `metrics/scripts/intake_stage1_fullpool_run_outputs.py`；只有接收状态达到 `complete_with_log_and_run_report`，并经人工审阅后，才能写成完整扩展增强资产。
10. 完整图像池结果只能作为新增协议，不能回写替代 `full502_clean_v1` 和 `compare9_complete496_v1`，除非后续完成独立评测、文档同步和人工验收。
