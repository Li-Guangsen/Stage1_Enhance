# Stage1-MyEdge 文件级关系审计（只读）

生成时间：`2026-05-25T02:11:56`

状态：`stage1_myedge_168_outputs_aligned_raw_bytes_differ_or_unproven`

本审计只读取本地 manifest 和文件元数据，用于确认 Stage1 正式结果、MyEdge 168 测试集、完整去水印藻类图像池之间的文件级关系。它不运行 Stage1，不运行 MyEdge，不生成指标，不生成图表。

## 输入路径

| Role | Path |
|---|---|
| Stage1 root | `D:\Desktop\Stage1Codex` |
| MyEdge root | `D:\Desktop\MyEdgeCodex` |
| Full algae pool root | `D:\Desktop\去水印所有藻类图像` |
| Coupling manifest | `D:\Desktop\MyEdgeCodex\docs\paper_assets\stage1_coupling\stage1_myedge_168_coupling_manifest_20260524.csv` |
| Stage1 original root | `D:\Desktop\Stage1Codex\data\inputImg\Original` |
| Stage1 formal result root | `D:\Desktop\Stage1Codex\experiments\h2-full506-direct\outputs\full506\runs\full506_final_mainline` |
| full502 manifest | `D:\Desktop\Stage1Codex\metrics\manifests\full502_clean_v1.txt` |
| compare496 manifest | `D:\Desktop\Stage1Codex\metrics\manifests\compare9_complete496_v1.txt` |
| full pool manifest | `D:\Desktop\Stage1Codex\metrics\manifests\full_algae_dewatermark_v1.txt` |
| full pool cv2-readable manifest | `D:\Desktop\Stage1Codex\metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt` |

## 核心计数

| Item | Count |
|---|---:|
| MyEdge coupling rows | 168 |
| MyEdge raw exists | 168 |
| GT exists | 168 |
| Stage1 original exists by filename | 168 |
| Stage1 all six stage paths exist | 168 |
| Stage1 Final exists | 168 |
| In full502_clean_v1 by stem | 168 |
| In compare9_complete496_v1 by stem | 166 |
| In full pool 2774 by filename | 0 |
| In full pool 2774 by stem | 0 |
| In full pool cv2-readable 2770 by filename | 0 |
| In full pool cv2-readable 2770 by stem | 0 |
| MyEdge raw and Stage1 original same size | 0 |
| MyEdge raw and Stage1 original same SHA256 | 0 |

## 重复键检查

| Set | Duplicate keys | Duplicate items | Example |
|---|---:|---:|---|
| myedge_stem_duplicates | 0 | 0 | {} |
| myedge_filename_duplicates | 0 | 0 | {} |
| full502_stem_duplicates | 0 | 0 | {} |
| compare496_stem_duplicates | 0 | 0 | {} |
| fullpool_2774_stem_duplicates | 28 | 132 | {'large (1)': 13, 'large (2)': 5, 'large': 18, 'MossImage': 2, '图片': 4, '图片1': 2, '图片2': 5, 'large1': 3, 'medium': 24, '图片_cleanup': 2} |
| fullpool_cv2_2770_stem_duplicates | 28 | 132 | {'large (1)': 13, 'large (2)': 5, 'large': 18, 'MossImage': 2, '图片': 4, '图片1': 2, '图片2': 5, 'large1': 3, 'medium': 24, '图片_cleanup': 2} |

## 可以写入论文/文档的安全表述

- MyEdge ALGAE 168-row coupling manifest can be used as a future fixed-detector Stage1-to-edge protocol source only after explicit execution approval.
- All rows with existing Stage1 six-stage paths and GT support a future staged comparison of Original/Stage1 Final under the same MyEdge evaluation code.
- The current audit is file-level evidence only; it is not a downstream metric result and does not prove Stage1 improves edge detection.
- MyEdge raw inputs and Stage1 formal originals should be described as stem/path aligned, not byte-identical, unless a later provenance audit proves identity.

## 不能越界的地方

- No Stage1 full2770 run was executed.
- No MyEdge staging, sampling, eval.py, show.py, report sync, training, or metric recomputation was executed.
- Full-pool 2774/2770 membership by filename/stem is only a local filename relation; it does not establish identical acquisition split, GT identity, or reference-paper overlap.
- Manual full-pool review remains required before a clean full-pool protocol can be claimed.

## 下一步动作

- If the user explicitly approves high-risk MyEdge operations, run P1 fixed-detector Stage1 Final -> MSFI and Stage1 Final -> DiffusionEdge baseline exactly from the readiness pack.
- Before writing any dataset-same claim, add an original-id/provenance table that can connect the 2777 full pool, Stage1 formal 502, MyEdge 168, and reference-paper datasets beyond filename stems.
- Finish manual review for the 544 full-pool rows before creating any clean full-pool manifest.
- Keep Stage1 as task-driven structure-preserving support for MyEdge/MSFI, not as a standalone SOTA enhancement claim.

## 负例/边界样例

### Negative examples: `in_compare9_complete496_v1_by_stem`

| row_id | stem | raw_filename | MyEdge size | Stage1 original size |
|---:|---|---|---:|---:|
| 1 | chazhuang.3 | chazhuang.3.jpg | 14529 | 7249 |
| 3 | chazhuang.6 | chazhuang.6.jpg | 19619 | 6164 |
### Negative examples: `in_fullpool_2774_by_stem`

| row_id | stem | raw_filename | MyEdge size | Stage1 original size |
|---:|---|---|---:|---:|
| 1 | chazhuang.3 | chazhuang.3.jpg | 14529 | 7249 |
| 2 | chazhuang.4 | chazhuang.4.jpg | 15754 | 3947 |
| 3 | chazhuang.6 | chazhuang.6.jpg | 19619 | 6164 |
| 4 | chichaoyiwan.1 | chichaoyiwan.1.jpg | 13740 | 3862 |
| 5 | chichaoyiwan.16 | chichaoyiwan.16.jpg | 15281 | 4138 |
| 6 | chichaoyiwan.2 | chichaoyiwan.2.jpg | 30958 | 3973 |
| 7 | chichaoyiwan.3 | chichaoyiwan.3.jpg | 13803 | 3795 |
| 8 | chichaoyiwan.4 | chichaoyiwan.4.jpg | 13484 | 3710 |
| 9 | chichaoyiwan.5 | chichaoyiwan.5.jpg | 13953 | 3573 |
| 10 | chichaoyiwan.6 | chichaoyiwan.6.jpg | 12847 | 3081 |
### Negative examples: `in_fullpool_cv2_2770_by_stem`

| row_id | stem | raw_filename | MyEdge size | Stage1 original size |
|---:|---|---|---:|---:|
| 1 | chazhuang.3 | chazhuang.3.jpg | 14529 | 7249 |
| 2 | chazhuang.4 | chazhuang.4.jpg | 15754 | 3947 |
| 3 | chazhuang.6 | chazhuang.6.jpg | 19619 | 6164 |
| 4 | chichaoyiwan.1 | chichaoyiwan.1.jpg | 13740 | 3862 |
| 5 | chichaoyiwan.16 | chichaoyiwan.16.jpg | 15281 | 4138 |
| 6 | chichaoyiwan.2 | chichaoyiwan.2.jpg | 30958 | 3973 |
| 7 | chichaoyiwan.3 | chichaoyiwan.3.jpg | 13803 | 3795 |
| 8 | chichaoyiwan.4 | chichaoyiwan.4.jpg | 13484 | 3710 |
| 9 | chichaoyiwan.5 | chichaoyiwan.5.jpg | 13953 | 3573 |
| 10 | chichaoyiwan.6 | chichaoyiwan.6.jpg | 12847 | 3081 |
### Negative examples: `raw_stage1_sha256_equal`

| row_id | stem | raw_filename | MyEdge size | Stage1 original size |
|---:|---|---|---:|---:|
| 1 | chazhuang.3 | chazhuang.3.jpg | 14529 | 7249 |
| 2 | chazhuang.4 | chazhuang.4.jpg | 15754 | 3947 |
| 3 | chazhuang.6 | chazhuang.6.jpg | 19619 | 6164 |
| 4 | chichaoyiwan.1 | chichaoyiwan.1.jpg | 13740 | 3862 |
| 5 | chichaoyiwan.16 | chichaoyiwan.16.jpg | 15281 | 4138 |
| 6 | chichaoyiwan.2 | chichaoyiwan.2.jpg | 30958 | 3973 |
| 7 | chichaoyiwan.3 | chichaoyiwan.3.jpg | 13803 | 3795 |
| 8 | chichaoyiwan.4 | chichaoyiwan.4.jpg | 13484 | 3710 |
| 9 | chichaoyiwan.5 | chichaoyiwan.5.jpg | 13953 | 3573 |
| 10 | chichaoyiwan.6 | chichaoyiwan.6.jpg | 12847 | 3081 |
