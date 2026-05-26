# 两篇 Wu et al. 2026 参考论文与 Stage1 完整图像池关系审计

生成时间：2026-05-25T02:03:27

## 1. 结论

- 总状态：`reference_dataset_descriptions_verified_exact_overlap_missing`。
- 已核验：两篇参考论文的数据集描述可以作为本项目数据说明和证据链设计的参考模板。
- 未核验：当前仓库仍没有文件级证据证明 Stage1 的 2777 图像池与 ESWA 的 676 图边缘数据集或 EAAI 的 1026 图分割数据集存在精确包含、交集或同一划分关系。
- 因此，论文中可以借鉴两篇论文的数据描述字段和实验组织方式，但不能照搬它们的数据规模、split、GT 标注或设备协议作为本项目事实。

## 2. 数量口径

| 对象 | 数量/口径 | 当前任务 | 关系状态 |
| --- | --- | --- | --- |
| Stage1 当前完整图像池 | 2777 图像文件；2774 默认候选；2770 OpenCV 可读候选 | 增强覆盖与后续下游输入 | 本仓库已核验，但 clean manifest 仍缺 |
| ESWA 2026 边缘检测参考 | 676 张，36 个物种，473/203 train/test | HAB edge detection | Zotero 本地缓存核验为参考论文事实；与 Stage1 精确 overlap 未证 |
| EAAI 2026 分割参考 | 1026 张，8:2 train/validation | HAB segmentation | Zotero 本地缓存核验为参考论文事实；与 Stage1 精确 overlap 未证 |

## 3. 审计矩阵

| ID | 来源 | 字段 | 核验值 | 状态 | 可用写法 | 禁止写法 | 仍缺证据 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R01 | Wu et al. 2026 ESWA edge reference | dataset_source | Applied Microalgal Biology Laboratory at Ocean University of China | verified_in_local_zotero_cache | 可写：ESWA 参考文献的数据由中国海洋大学相关微藻实验室提供。 | 不可写：Stage1 当前 2777 图像池已经被证明就是该 676 图边缘数据集。 | 需要本项目自己的采集说明、物种清单和与 676 图边缘集的文件级对应关系。 |
| R02 | Wu et al. 2026 ESWA edge reference | dataset_size_species | 676 high-resolution microscopic images, 36 HAB species | verified_in_local_zotero_cache | 可写：ESWA 参考文献报告 676 张 HAB 显微图像、36 个常见有害藻华物种。 | 不可写：我们的 2777 图像池自动包含或扩展该 676 图集合。 | 需要文件名、原始编号或哈希层面的 overlap / subset 证明。 |
| R03 | Wu et al. 2026 ESWA edge reference | acquisition_and_annotation | Olympus CX43 + Canon EOS 5D Mark IV, 400x, bright-field; LabelMe edge maps by two HAB experts | verified_in_local_zotero_cache | 可借鉴写法：说明显微镜、相机、倍率、明场条件、专家交叉核验和分歧协商流程。 | 不可写：当前 Stage1 full-pool 已有同等专家标注或同一设备参数。 | 需要本项目实际设备、倍率、拍摄协议、标注者资质和标注软件记录。 |
| R04 | Wu et al. 2026 ESWA edge reference | split_and_edge_protocol | 473 train / 203 test, 70/30 species-level split; ODS/OIS/AP/AC edge evaluation; no NMS | verified_in_local_zotero_cache | 可借鉴：若做 MyEdge/Stage1 coupling，优先报告 ODS/OIS/AP/AC、是否 NMS、split 单位和评估阈值。 | 不可写：Stage1 502/496 增强主表等价于 ESWA 的 203 张 edge test。 | 需要 MyEdge 当前 168 张测试集与 ESWA 203 测试集的关系说明，或明确它们是不同本地协议。 |
| R05 | Wu et al. 2026 EAAI segmentation reference | dataset_source_size_split | AICO/OUC HAB microscopy dataset, 1026 images, 8:2 train/validation split | verified_in_local_zotero_cache | 可写：EAAI 参考文献在同方向 HAB 显微分割任务中报告 1026 张数据和 8:2 划分。 | 不可写：Stage1 2777 图像池已经证明与 EAAI 1026 图分割集同一划分或同一标注集合。 | 需要文件级 overlap、分割 mask 对应关系、训练/验证名单或数据登记表。 |
| R06 | Wu et al. 2026 EAAI segmentation reference | evidence_chain_to_borrow | task-oriented enhancement + segmentation coupling; enhancement ablation; boundary metrics; efficiency; cross-dataset and downstream analyses | verified_in_local_zotero_cache | 可借鉴：把增强写成任务驱动结构输入，并用下游边界、效率、失败案例和应用指标支撑。 | 不可写：Stage1 已经完成这些 EAAI 风格下游分割或分类证据。 | 需要 Stage1->MyEdge 固定 detector 结果、效率、失败案例、退化子集和至少一种应用级验证。 |
| R07 | Stage1Codex current full algae pool | current_pool_counts | {"image_files_total": 2777, "default_candidate_manifest": 2774, "cv2_readable_candidate_manifest": 2770, "decode_failures": 4} | verified_in_repo | 可写：本项目当前完整增强图像池为 2777 个图像文件，默认候选 2774，OpenCV 可读候选 2770。 | 不可写：full2770 已经完成增强，或 full2770 已替代正式 502/496 论文口径。 | 需要人工复核后 clean manifest；如获授权，还需要 full2770 正式长跑和 intake 接收。 |
| R08 | Stage1Codex current full algae pool | manual_review_state | {"pending_rows": 544, "clean_manifest_exists": false} | verified_in_repo | 可写：完整图像池仍有 544 条人工复核 pending，clean manifest 尚未生成。 | 不可写：重复/近重复/质量异常已经人工清洗完毕。 | 需要人工填写 reviewer_decision 并派生 reviewed clean manifest。 |
| R09 | Cross-dataset relation | current_relation_status | same lab is user-reported; exact overlap with ESWA 676 or EAAI 1026 is unproven in local repo | relation_unproven | 可写：两篇参考论文提供了同方向同实验室 HAB 显微数据描述模板；本项目需另行给出 2777/2774/2770 图像池的本地证据。 | 不可写：本项目与两篇论文使用完全相同数据集、同一 split、同一 GT 标注或同一统计口径。 | 需要文件级清单比对、哈希比对、原始采集编号、标注文件或实验室数据登记证明。 |

## 4. 可借鉴的论文写法

- 数据描述字段：数据来源实验室、图像规模、物种覆盖、显微设备、倍率、光照条件、重复拍摄、标注工具、专家资质、交叉核验、分歧协商、split 单位。
- ESWA 路线可借鉴：edge GT、ODS/OIS/AP/AC、是否使用 NMS、强 edge baseline、增强前后 edge ablation、CIAFF/Sobel 替换模块对比。
- EAAI 路线可借鉴：task-oriented enhancement coupling、boundary metrics、效率、cross-dataset 解释、下游形态/分类应用、失败案例和局限讨论。
- Stage1 当前只能把这些作为未来补证协议或写作模板，不能把参考论文数值写成 Stage1 结果。

## 5. 投稿前必须补齐

1. 建立 Stage1 2777/2774/2770 图像池与两篇参考论文数据集的文件级关系：原始编号、文件名、hash、采集表或人工登记证明至少一种。
2. 补齐本项目自己的数据采集说明：实验室、设备、相机、倍率、明场/照明、物种范围、采样或去水印流程。
3. 若要写下游边缘检测，必须在 MyEdge 协议下补齐 168 张或后续扩展集的 GT、split 和 ODS/OIS/AP/AC，而不是用 Stage1 增强指标代替。
4. 若使用完整图像池作为增强覆盖证据，先完成人工复核并生成 reviewed clean manifest；候选 full2770 长跑需要另行明确授权。

## 6. 状态计数

- `relation_unproven`: 1
- `verified_in_local_zotero_cache`: 6
- `verified_in_repo`: 2

## 7. 本审计边界

- 本审计只读取仓库文件和 Zotero 本地缓存，不访问在线页面。
- 本审计不运行 Stage1 增强、不运行 MyEdge sampling/eval/show、不训练、不生成新图表、不重算指标。
- 本审计不是 overlap 证明；它只是把参考论文数据描述和本项目当前数据池之间的可写边界固定下来。
