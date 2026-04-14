# Optimization v1 analysis

## Objective

在 pilot92-v1 上优化增强后综合指标。综合评分采用 `metrics/score_protocol_v2.py` 中的加权 log-ratio：

- 结构/边缘主指标：SIFT_KP、AvgGra、Contrast、EME、EMEE
- 感知质量：UCIQE、UIQM、Entropy
- 结构保持参考：MS_SSIM、PSNR

PSNR 和 MS-SSIM 不作为主优化目标，但用于避免过增强。当前筛选规则为：优先看综合分，同时保留 `Mean_MS_SSIM >= 0.85` 的候选作为更稳妥论文配置。

## Baseline observations

标准化评估路径：

```bat
python metrics\evaluate_protocol_v2.py --manifest data\eval_subset_pilot92_v1.txt --output-dir metrics\outputs\evaluate_protocol_v2\pilot92_stages --method BPH=results\png\BPH --method IMF1Ray=results\png\IMF1Ray --method RGHS=results\png\RGHS --method CLAHE=results\png\CLAHE --method Fused=results\png\Fused --method Final=results\png\Final
```

结果显示 `Final` 是现有阶段中综合分最高的阶段。`Final` 相比 `Fused` 明显提高 Contrast、AvgGra、SIFT_KP、UCIQE、MS_SSIM、PSNR，但 Entropy 和 UIQM 有下降空间。因此优化重点放在融合后的 refinement 和轻量融合权重，而不是重跑 IMF1Ray。

## Candidate search

候选生成脚本：

```bat
python experiments\optimization_v1\run_post_stage_search.py --manifest data\eval_subset_pilot92_v1.txt --output-dir experiments\optimization_v1\results\post_stage_search_round2
```

候选评估脚本：

```bat
python metrics\evaluate_protocol_v2.py --quiet --manifest data\eval_subset_pilot92_v1.txt --output-dir metrics\outputs\evaluate_protocol_v2\pilot92_post_stage_search_round2 --methods-root experiments\optimization_v1\results\post_stage_search_round2 --methods-subdir Final
```

综合评分排序前 5：

| Candidate | Composite | SIFT_KP | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM | Entropy | Contrast |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c05_homo_entropy | 10.1384 | 2844.72 | 12.4772 | 0.8204 | 19.6390 | 4.0932 | 21.1969 | 5.6750 | 477.35 |
| c25_rghs_entropy_mid | 10.1240 | 2851.09 | 12.3440 | 0.8506 | 20.1176 | 4.7147 | 19.8783 | 5.4392 | 480.83 |
| c24_strong_entropy_light | 10.0626 | 2863.96 | 12.3527 | 0.8729 | 20.7606 | 5.4182 | 18.5151 | 5.1337 | 484.40 |
| c21_current_entropy_mid | 9.8749 | 2864.20 | 12.3872 | 0.8490 | 20.3953 | 4.5341 | 19.9615 | 5.4572 | 480.22 |
| c23_homo_entropy_balanced | 8.6783 | 2838.57 | 12.2417 | 0.8348 | 19.9260 | 4.1536 | 20.4173 | 5.6029 | 466.55 |

## Current decision

推荐配置：`c25_rghs_entropy_mid`，已保存为 `experiments/optimization_v1/configs/best_c25_balanced.json`。

原因：

- 综合分几乎等同最高分 `c05`，只低 0.014。
- 相比 `c05`，MS_SSIM 从 0.8204 提升到 0.8506，结构保持更稳。
- 相比当前 `c00_current`，SIFT_KP、AvgGra、Contrast、Entropy、UCIQE、UIQM 均提高。
- 视觉诊断抽查未见明显过增强失真。

`c05_homo_entropy` 已保存为 `metric_max_c05.json`，可作为单纯追求综合评分的激进配置，但不建议直接作为论文默认配置，除非全量 506 和人工视觉检查均通过。

## Full506 tuning update

2026-04-13 已将调参从 pilot92-v1 转移到全量 `data/inputImg/Original` 506 张，并使用同一份 complete-case manifest 评估。所有正式比较均使用 PNG 结果。

第一轮 full506 基准 `c25_full506`：

| Method | Count | EME | EMEE | Entropy | Contrast | AvgGra | SIFT_KP | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c25 | 506 | 12.5928 | 1.0072 | 5.8934 | 570.5867 | 15.3836 | 3999.27 | 0.7267 | 16.1012 | 3.6353 | 25.8135 |

随后基于 full506 中间阶段进行四轮后处理/融合细化搜索：

- Round 1: `full506_post_stage_search`, 17 个候选，最优 `c05_homo_entropy`。
- Round 2: `full506_refine_round2`, 16 个候选，最优 `r2_06_homo_stronger_c05_entropy`。
- Round 3: `full506_refine_round3`, 14 个候选，最优 `r3_03_gamma_050_195_55`。
- Round 4: `full506_refine_round4`, 9 个边界验证候选，最优 `r4_03_gamma_050_210_48`。

最终直接对比输出：

```text
metrics/outputs/evaluate_protocol_v2/full506_final_compare_c25_r4_03
```

| Method | Count | Composite vs c25 | EME | EMEE | Entropy | Contrast | AvgGra | SIFT_KP | MS_SSIM | PSNR | UCIQE | UIQM |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c25 | 506 | 0.0000 | 12.5928 | 1.0072 | 5.8934 | 570.5867 | 15.3836 | 3999.27 | 0.7267 | 16.1012 | 3.6353 | 25.8135 |
| r4_03 | 506 | 11.3829 | 14.4266 | 1.1122 | 5.9260 | 689.6882 | 17.4981 | 4207.91 | 0.6993 | 16.0642 | 4.6089 | 28.9724 |

相对 `c25`，`r4_03` 提升 EME、EMEE、Entropy、Contrast、AvgGra、SIFT_KP、UCIQE、UIQM；PSNR 基本持平，MS-SSIM 下降约 0.0273。由于研究目标偏向边缘/结构提取，当前将 `r4_03` 作为 full506 指标最优配置，但论文中需如实说明其 MS-SSIM 有小幅牺牲。

最终配置已保存：

```text
experiments/optimization_v1/configs/best_full506_r4_03.json
```

视觉诊断抽样输出：

```text
metrics/diagnostics/full506_final_compare_c25_r4_03
```
