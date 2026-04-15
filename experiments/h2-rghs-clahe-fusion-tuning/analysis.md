# H2 RGHS / CLAHE / Fusion 顺序优化

## 当前状态

- 创建时间：`2026-04-16T00:24:53`
- 最近更新：`2026-04-16T02:28:43`
- 总状态：`setup_completed`
- 主线基线：`D:\Desktop\Stage1Codex\experiments\optimization_v1\configs\locked_full506_mainline.json`
- smoke12 manifest：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\manifests\smoke12.txt`
- pilot92 manifest：`D:\Desktop\Stage1Codex\data\eval_subset_pilot92_v1.txt`
- full506 manifest：`D:\Desktop\Stage1Codex\metrics\outputs\evaluate_protocol_v2\full506_c25\complete_case_manifest.txt`

## Setup

- pilot92 baseline 输出：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\results\baseline_mainline_pilot92`
- pilot92 baseline 评测：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\scores\baseline_mainline_pilot92_final`
- smoke12 baseline 评测：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\scores\baseline_mainline_smoke12_final`
- full506 chunk manifests：`['D:\\Desktop\\Stage1Codex\\experiments\\h2-rghs-clahe-fusion-tuning\\manifests\\full506_chunk1.txt', 'D:\\Desktop\\Stage1Codex\\experiments\\h2-rghs-clahe-fusion-tuning\\manifests\\full506_chunk2.txt', 'D:\\Desktop\\Stage1Codex\\experiments\\h2-rghs-clahe-fusion-tuning\\manifests\\full506_chunk3.txt', 'D:\\Desktop\\Stage1Codex\\experiments\\h2-rghs-clahe-fusion-tuning\\manifests\\full506_chunk4.txt']`

## RGHS

- 状态：`smoke_completed`
- baseline 配置：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\configs\setup\baseline_mainline_pilot92.json`
- baseline pilot 输出：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\results\baseline_mainline_pilot92`
- smoke 排序：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\scores\rghs_smoke_rghs\ranked.json`
- smoke Final 回退检查：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\scores\rghs_smoke_final\ranked.json`
- `rghs_s07`: ΔMS-SSIM=0.188640, ΔPSNR=4.3747, ΔUCIQE=0.0987, ΔUIQM=-2.0251, gate_pass=True
- `rghs_s06`: ΔMS-SSIM=0.173402, ΔPSNR=4.2427, ΔUCIQE=0.0994, ΔUIQM=-1.6542, gate_pass=True
- `rghs_s02`: ΔMS-SSIM=0.093022, ΔPSNR=1.8660, ΔUCIQE=0.0525, ΔUIQM=-1.0220, gate_pass=True

- pilot 排序：``
- pilot 排序尚未生成

- winner：`baseline`
- winner 参数：`D:\Desktop\Stage1Codex\experiments\h2-rghs-clahe-fusion-tuning\configs\setup\baseline_mainline_pilot92.json`

## CLAHE

- 状态：`pending`
- baseline 配置：``
- baseline pilot 输出：``
- smoke 排序：``
- smoke 排序尚未生成

- pilot 排序：``
- pilot 排序尚未生成

- winner：`baseline`
- winner 参数：``

## FUSION

- 状态：`pending`
- baseline 配置：``
- baseline pilot 输出：``
- smoke 排序：``
- smoke 排序尚未生成

- pilot 排序：``
- pilot 排序尚未生成

- winner：`baseline`
- winner 参数：``

## Full506

- 状态：`pending`
- baseline 目录：`D:\Desktop\Stage1Codex\experiments\h1-graypixel-bph-ablation\outputs\full506\runs\full506_locked_mainline`
- 排序结果：``
- 尚未进入 full506

- 最终 winner：``
- 最终说明：``
