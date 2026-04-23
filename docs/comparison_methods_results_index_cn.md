# 对比方法与结果索引（中文）

更新时间：2026-04-24

## 1. 正式参评集合

当前正式主表使用 `9` 方法：

- `Ours`
- `HVDualformer`
- `ABC-Former`
- `GDCP`
- `CBF`
- `HLRP`
- `SGUIE-Net`
- `Histoformer`
- `WWPF`

主表统一使用：

- manifest：`metrics/manifests/compare9_complete496_v1.txt`
- count：`496`
- summary：`metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/summary.json`

接手时需要知道：

- 当前正式主表结果已经落盘，可直接阅读
- 但除 `Ours` 外，其余对比方法当前都指向本机绝对路径下的结果目录
- 因此“查看正式结果”和“在新机器上重跑主比较”不是同一难度级别

## 2. 方法结构表

| Method | 分类 | 论文标题 | 输出目录 | 当前样本数 | 备注 |
|---|---|---|---|---:|---|
| Ours | 正式主线 | This work | `experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline/png/Final` | 502 | 正式组合版主线 |
| HVDualformer | 深度白平衡 | HVDualformer: Histogram-Vision Dual Transformer for White Balance | `D:\Desktop\2025AAAI_HVDual_former\lgsresults` | 502 | 白平衡方法，实验节保留 |
| ABC-Former | 深度白平衡 | ABC-Former: Auxiliary Bimodal Cross-domain Transformer with Interactive Channel Attention for White Balance | `D:\Desktop\2025CVPR_ABC-Former\ABC-Former\lgsresults` | 502 | 白平衡方法，实验节保留 |
| GDCP | 传统/非深度水下增强 | Generalization of the Dark Channel Prior for Single Image Restoration | `D:\Desktop\2018_Generalization-of-the-Dark-Channel-Prior\lgsresults` | 502 | 物理先验恢复 |
| CBF | 传统/非深度水下增强 | Color Balance and Fusion for Underwater Image Enhancement | `D:\Desktop\2018_Color-Balance-and-fusion-for-underwater-image-enhancement\lgsresult` | 502 | 经典融合 |
| HLRP | 传统/非深度水下增强 | Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors | `D:\Desktop\2022_HLRP-main\HLRP_Code\lgsresult` | 502 | Retinex 变分优化 |
| SGUIE-Net | 深度水下增强 | SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception | `D:\Desktop\2022_SGUIE_Net_Simple\lgsresults` | 502 | 语义注意力增强 |
| Histoformer | 深度水下增强 | Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement | `D:\Desktop\2024_Histoformer-main\lgsresults` | 502 | 直方图 Transformer |
| WWPF | 传统/非深度水下增强 | Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion | `D:\Desktop\2024_WWPF_code\2023-WWPE\datasets\lgsresults` | 496 | 官方包仅稳定输出 496 张 |

说明：

- 除 `Ours` 外，上表目录目前都是当前工作站上的外部结果资产
- 正式主表已经可直接引用，但若这些绝对路径在另一台机器上不存在，则不能直接重跑 `official_compare9_complete496`

## 3. complete-case 缺失说明

`WWPF` 相对 `full502_clean_v1` 缺失的 6 张图为：

- `chazhuang.10`
- `chazhuang.12`
- `chazhuang.3`
- `chazhuang.6`
- `haiyangyuanjia.5`
- `suojiao.3`

因此正式主表不按各方法各自均值比较，而是统一按 `496` 张 complete-case 统计。

## 4. 正式对比结果（compare9 complete496）

来自 `metrics/outputs/evaluate_protocol_v2/official_compare9_complete496/mean_metrics_table.md`：

| Method | Count | EME | EMEE | Entropy | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ours | 496 | 11.5094 | 0.9459 | 5.6527 | 543.0379 | 14.8101 | 0.7689 | 17.6237 | 4.1371 | 23.7718 |
| HVDualformer | 496 | 2.7191 | 0.4487 | 4.0512 | 26.1360 | 2.9491 | 0.9916 | 34.8337 | 1.7619 | 7.6243 |
| ABC-Former | 496 | 2.5160 | 0.4374 | 3.9950 | 25.7323 | 2.9308 | 0.9985 | 41.1282 | 2.1923 | 7.1974 |
| GDCP | 496 | 7.0593 | 0.6978 | 5.2147 | 101.2764 | 6.2555 | 0.8736 | 23.2668 | 3.8016 | 16.2377 |
| CBF | 496 | 7.2162 | 0.6997 | 6.6149 | 96.9364 | 6.8343 | 0.7531 | 17.5284 | 2.9776 | 16.7735 |
| HLRP | 496 | 19.4035 | 1.3606 | 7.1098 | 458.8925 | 18.4152 | 0.2474 | 11.1560 | 3.7262 | 40.4346 |
| SGUIE-Net | 496 | 6.2661 | 0.6525 | 4.8434 | 92.4756 | 5.8142 | 0.9027 | 24.6537 | 3.2959 | 14.9255 |
| Histoformer | 496 | 18.8692 | 1.3602 | 7.0453 | 511.9787 | 18.0899 | 0.4128 | 15.1170 | 5.3624 | 40.0926 |
| WWPF | 496 | 12.4182 | 1.0066 | 6.2425 | 358.6978 | 14.2527 | 0.5544 | 15.2439 | 2.7650 | 25.4710 |

## 5. 当前可用结论边界

- 当前总表已经统一到同一 complete-case 口径，可以正式引用
- `MS_SSIM` 与 `PSNR` 在当前论文口径下应解释为增强结果相对原图的结构一致性，而不是相对增强真值的质量指标
- `HVDualformer` 与 `ABC-Former` 仍属于白平衡方法，不能在 related work 中混写为标准水下增强方法
- 当前对比结果是“增强指标总表”，还不是“增强 + 下游边缘验证”的完整闭环
- `WWPF` 的 496 样本实现边界必须在论文里如实说明

## 6. 主表叙述策略

- 正式数值表继续保留全部 `9` 方法，不人为删除 `WWPF`、`HLRP` 或 `Histoformer`
- 正文主讨论建议围绕 `Ours`、`HVDualformer`、`ABC-Former`、`GDCP`、`CBF`、`SGUIE-Net` 和 `WWPF` 展开
- `WWPF` 应保留在主表中，作为“激进但可接受的强基线”处理
- `HLRP` 与 `Histoformer` 虽保留在正式数值表中，但在正文层面更适合作为失败案例或补充分析，而不宜与稳健方法作同等层级的正向讨论
- 上述区分都限定在当前 HAB 显微图像协议下，不应被写成对原论文方法在一般水下场景中的否定

## 7. 当前推荐结果解读

- `HVDualformer` 与 `ABC-Former` 的 `MS_SSIM/PSNR` 很高，说明它们与原图更接近，但 `EME`、`Contrast`、`AvgGra`、`UCIQE` 和 `UIQM` 普遍偏低，因此更适合作为保守白平衡基线，而不是强增强方法
- `GDCP`、`CBF` 与 `SGUIE-Net` 代表中等增强强度的方法组，在结构一致性与视觉改善之间较为稳健，但综合增强收益仍弱于本文方法
- `WWPF` 在 `EME`、`EMEE` 和 `UIQM` 上高于本文方法，说明其增强更激进；但其 `MS_SSIM` 与 `PSNR` 明显更低，说明其通过更大的结构偏离换取了更强的无参考视觉刺激
- `HLRP` 与 `Histoformer` 虽然部分无参考指标较高，但当前显微场景复现实验已经出现明显偏色、过噪和结构失真，因此更适合作为失败案例，而不是稳健主比较对象
- 在保留 `WWPF` 的稳健方法集合中，本文方法在 `Contrast`、`AvgGra` 和 `UCIQE` 上排名第一，在 `EME`、`EMEE` 和 `UIQM` 上排名第二，在 `Entropy` 上排名第三；这说明本文方法并非最接近原图的保守方案，但在增强收益和结构稳定性之间取得了更均衡的表现
- 这些结论都只针对当前有害藻华显微图像任务、本地复现实验和当前指标解释，不构成对原方法既有论文结论的直接否定
