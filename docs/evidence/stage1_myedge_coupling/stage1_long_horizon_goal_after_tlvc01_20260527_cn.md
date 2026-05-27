# TLVC01 后的长期目标与执行计划

日期：2026-05-27

## 1. 纠正结论

当前证据不支持继续把 Stage1-only direct replacement 作为主线。

已经完成的纠偏事实：

- D01：机制更完整，但视觉接近 raw、没有 502/496 外部增强对比、168 fixed-detector 不是 strong pass。
- FF01/FF02：恢复了灰像素、IMF/频域、多分支融合和收口，但 direct replacement 让 fixed MSFI / DiffusionEdge 明显掉 ODS/AP 和结构 proxy。
- TLVC01：修正 raw input protocol，用 exact MyEdge raw 生成 topology-locked 完整流程输出，固定 detector 不再崩塌，但 gate 仍为 `candidate_rescues_legacy_but_not_near_raw`，不是下游正收益。

因此，阶段性结论是：

`完整增强图像直接替换 raw 输入` 在当前 fixed detectors 下还没有产生可写成论文主张的正收益。继续做 TLVC02/FF03/P29/D02 式小幅 guard、fallback、raw-pullback 会重复消耗，不符合原始目标。

## 2. 长期目标

长期目标改为：

**以 MyEdge/MSFI spatial-frequency weak-boundary diffusion 为主创新，Stage1 不再直接替换 raw，而是把完整增强流程拆成可解释 sidecar evidence，作为 raw 主输入旁路的结构保持、色度恢复、弱边界支持和风险抑制信号，最终验证它是否能在 168 fixed validation 上带来稳定正收益。**

核心原则：

- raw image 保持 detector topology anchor；
- Stage1 full enhancement 不再作为唯一输入图像；
- 灰像素/BPH、IMF/频域、RGHS/CLAHE、多分支融合、滤波收口仍保留，但输出为 sidecar maps / auxiliary conditions；
- 正收益必须来自 MyEdge/MSFI 侧明确 ablation，而不是把 proxy 或 legacy rescue 写成完成。

## 3. 执行路线

### WP0：证据冻结与失败归档

状态：基本完成。

产物：

- `experiments/topology_locked_visual_chroma_full_flow_v1/topology_locked_visual_chroma_full_flow_v1_fixed_detector_tlvc01_status_20260527.md`
- `docs/evidence/fa01_family_audit/stage1_full_flow_family_failure_audit_fa01_20260527_cn.md`
- `docs/evidence/fa01_family_audit/fa01_visual_error_map_review_20260527_cn.md`
- registry 中 FF01/FF02/TLVC01 均为 archived diagnostic。

### WP1：Stage1 sidecar map 定义与 168 导出

状态：5 个 high-risk 样本 smoke 已完成，168 全量尚未执行。

目标：

- 对 168 split 导出 topology anchor、color compensation、frequency detail、visibility、fusion/luma risk、background false-edge risk、weak-boundary support maps。
- 输出 manifest、decode report、map statistics 和 panel review。
- 不训练、不改 MyEdge，仅准备可复现输入条件。

入口：

- `docs/evidence/stage1_myedge_coupling/stage1_sidecar_map_definition_fa01_20260527_cn.md`
- `metrics/scripts/export_fa01_stage1_sidecar_maps.py`

### WP2：MyEdge/MSFI sidecar adaptation run sheet

状态：草案存在，未授权训练。

目标：

- 在 MyEdge 侧写独立 run sheet，明确 train/val/test、checkpoint、输出根、日志和 ablation。
- 设计 raw-only baseline、raw+topology sidecar、raw+color/frequency sidecar、raw+all sidecars、risk-suppressed variants。
- 明确禁止与 fixed-detector direct replacement 结果混表。

入口：

- `docs/evidence/stage1_myedge_coupling/myedge_msfi_stage1_sidecar_adaptation_protocol_fa01_20260527_cn.md`

### WP3：MyEdge/MSFI adaptation 训练与 168 验证

状态：未开始；需要单独授权。

最低验收：

- 不改变 168 GT validation split；
- 输出 isolated training/eval roots；
- 与 raw-only MSFI 和 DiffusionEdge anchors 对比；
- 至少一个 detector/model route 明确优于 raw anchor，且 AP/AC/structure proxy 不崩。

### WP4：消融与论文证据链

状态：未开始。

必须有：

- sidecar module ablation；
- weak-boundary / false-edge / endpoint 结构 proxy；
- fixed ODS/OIS/AP/AC；
- failure-case panels；
- 与 Wu 2026 ESWA/EAAI 的边界说明；
- 502/496 只作为 Stage1 enhancement side evidence，不替代 downstream validation。

## 4. 当前禁止事项

- 不新增 TLVC02/FF03/P29/D02 作为同族小修。
- 不把 `candidate_rescues_legacy_but_not_near_raw` 写成候选通过。
- 不把 2770 full-pool readiness 写成正式验证。
- 不在未授权时启动 MyEdge 训练或 checkpoint 修改。
- 不用 Stage1 `data/inputImg/Original` 替代 MyEdge raw anchor 做 168 downstream candidate。

## 5. 下一步

若继续推进，下一步不是再调 Stage1 direct replacement，而是：

1. 把 WP1 从 5-sample sidecar smoke 扩展到 168 split。
2. 生成 168 sidecar export report、manifest 和 panel index。
3. 在 MyEdge 仓库建立 sidecar adaptation run sheet。
4. 得到明确授权后再训练/验证 MyEdge/MSFI adaptation。

这条路线保留了用户要求的完整增强流程和创新模块，但把它从“替换图像”改为“辅助证据输入”，以避免 fixed detector 对 raw 分布的偏好继续吞掉增强收益。
